"""Exercise the real 20 ms controller, not a replacement vehicle simulation."""
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def probe(body):
    script = """
const {DriveModel} = require(process.argv[1]);
function make(off=false) {
 const m=new DriveModel('ioniq6n');
 m.handle('ignition',[1]); m.handle('start',[1]);
 if(off) m.handle('eshift_enable',[0]);
 m.handle('throttle',[1]); return m;
}
function run(m,seconds) {
 const rows=[]; for(let i=0;i<Math.round(seconds/.02);i++) {
  const events=m.tick(.02); rows.push({state:m.snapshot(), events});
 } return rows;
}
""" + body
    return json.loads(subprocess.check_output(
        ['node', '-e', script, str(ROOT/'code/drive_model.js')], text=True))


class IoniqControlV3Tests(unittest.TestCase):
    def test_shutdown_and_restart_close_an_in_progress_shift(self):
        data = probe("""
const rows=[];
for(const action of ['off','restart']) {
 const m=make(); for(let i=0;i<2000 && !m.shift;i++) m.tick(.02);
 const active=!!m.shift;
 const events=m.handle(action==='off'?'ignition':'start',[action==='off'?0:1]);
 const later=run(m,2).flatMap(x=>x.events);
 rows.push({active,events,later});
}
console.log(JSON.stringify(rows));
""")
        for row in data:
            self.assertTrue(row['active'])
            self.assertIn(['shift', 0], row['events'])
        self.assertNotIn(['shift',1],data[0]['later'])

    def test_duplicate_mode_request_preserves_running_state(self):
        data = probe("""
const m=make(); run(m,60); const before=m.snapshot(); let events=[];
for(let i=0;i<100;i++) events.push(...m.handle('eshift_enable',[1]));
console.log(JSON.stringify({before, after:m.snapshot(), events}));
""")
        self.assertEqual(data['before'], data['after'])
        self.assertFalse(any(e[0] in ('gear', 'shift', 'shift_cut') for e in data['events']))

    def test_mode_transition_is_continuous_bounded_and_converges(self):
        data = probe("""
const m=make(true); run(m,60); const before=m.snapshot();
const events=m.handle('eshift_enable',[1]); const immediate=m.snapshot();
const on=run(m,1); m.handle('eshift_enable',[0]); const off=run(m,1);
console.log(JSON.stringify({before, immediate, events, on, off}));
""")
        self.assertEqual(data['before']['rpm'], data['immediate']['rpm'])
        self.assertEqual(8, data['immediate']['gear'])
        last = data['before']['rpm']
        for row in data['on'] + data['off']:
            rpm = row['state']['rpm']
            self.assertLessEqual(rpm, 10000)
            self.assertLess(abs(rpm-last), 300)
            last = rpm
        self.assertAlmostEqual(8000, data['on'][-1]['state']['rpm'], delta=1)
        self.assertAlmostEqual(9950, data['off'][-1]['state']['rpm'], delta=1)
        self.assertFalse(any(e[0]=='shift' and e[1]==1 for e in data['events']))

    def test_virtual_redline_and_off_mapping(self):
        data = probe("""
const on=run(make(),60),off=run(make(true),60);
console.log(JSON.stringify({on, off:off.at(-1).state}));
""")
        self.assertEqual(8, data['on'][-1]['state']['gear'])
        self.assertAlmostEqual(8000, max(x['state']['rpm'] for x in data['on']), delta=1)
        self.assertEqual(9950, data['off']['rpm'])
        self.assertEqual(300, data['off']['speed'])

    def test_gear_input_does_not_publish_false_internal_state(self):
        data = probe("""
const m=make();run(m,4);const events=m.handle('gear',[6]);
console.log(JSON.stringify({events, gear:m.snapshot().gear}));
""")
        self.assertEqual([['gear', data['gear']]], data['events'])

    def test_other_profiles_and_single_speed_replay_are_unchanged(self):
        data = probe("""
const vm=require('vm'),cp=require('child_process');
const context={module:{exports:{}}};vm.createContext(context);
vm.runInContext(cp.execFileSync('git',['show','cff9d08:code/drive_model.js'],
 {cwd:require('path').dirname(process.argv[1]),encoding:'utf8'}),context);
const matches={};
for(const profile of ['ev','v10','v12','ferrari','ioniq6n']) {
 const a=new DriveModel(profile),b=new context.module.exports.DriveModel(profile);
 let ok=true;
 for(const m of [a,b]) {m.handle('ignition',[1]);m.handle('start',[1]);
  if(profile==='ioniq6n')m.handle('eshift_enable',[0]);}
 for(let i=0;i<3000;i++) {
  const pedal=i<1800?1:(i<2100?0.3:0),brake=i>2500?.8:0;
  for(const m of [a,b]) {m.handle('throttle',[pedal]);m.handle('brake',[brake]);}
  if(JSON.stringify([a.tick(.02),a.snapshot()])!==JSON.stringify([b.tick(.02),b.snapshot()]))ok=false;
 }
 matches[profile]=ok;
}
console.log(JSON.stringify(matches));
""")
        self.assertTrue(all(data.values()), data)

    def test_reentrant_switch_start_stop_and_nonfinite_inputs(self):
        data = probe("""
const m=make();run(m,20);let issues=[],active=0,peak=0;
function inspect(events) { for(const e of events) if(e[0]==='shift') {
 active+=e[1]===1?1:-1;if(active<0||active>1)issues.push('unpaired shift');}}
// Establish the currently active ordinary shift, if any.
active=m.snapshot().shifting;
for(let i=0;i<1000;i++) {
 if(i%23===0)inspect(m.handle('eshift_enable',[(i/23|0)%2]));
 if(i%31===0)for(let n=0;n<100;n++)inspect(m.handle('eshift_enable',[m.eShiftEnabled]));
 const events=m.tick(.02);inspect(events);const s=m.snapshot();peak=Math.max(peak,s.rpm);
 if(!Number.isFinite(s.rpm)||s.rpm>10000||s.gear<1||s.gear>8)issues.push('range');
}
m.handle('ignition',[0]);m.handle('ignition',[1]);m.handle('start',[1]);
const restart=m.snapshot();m.handle('throttle',[NaN]);m.handle('eshift_enable',[Infinity]);
const rows=run(m,1);
console.log(JSON.stringify({issues,peak,restart,finite:rows.every(x=>Number.isFinite(x.state.rpm))}));
""")
        self.assertEqual([], data['issues'])
        self.assertEqual(1450, data['restart']['rpm'])
        self.assertEqual(1, data['restart']['gear'])
        self.assertTrue(data['finite'])

    def test_launch_and_locked_lift_follow_wheel_target(self):
        data = probe("""
const m=make(), rows=run(m,6);m.handle('throttle',[0]);const lift=run(m,.6);
console.log(JSON.stringify({rows, lift, ratios:m.config.ratios}));
""")
        shifts = [x for x in data['rows'] if ['shift', 1] in x['events']]
        self.assertTrue(shifts)
        self.assertGreater(shifts[0]['state']['rpm'], 7500)
        # During a locked first lift, RPM must approach wheel speed rather than
        # be driven 18% below it. Skip actual shifts and their short settling.
        last = data['lift'][-1]['state']
        if not last['shifting']:
            wheel = last['speed'] * data['ratios'][last['gear']-1]
            self.assertGreater(last['rpm'], wheel * .98)
