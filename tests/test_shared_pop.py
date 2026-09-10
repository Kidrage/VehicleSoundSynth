"""Shared short-sample Pop: profile voicing without changing event authority."""
import json
import subprocess
import unittest
from pathlib import Path
from tools import build_project as builder

ROOT = Path(__file__).resolve().parents[1]


class SharedPopTests(unittest.TestCase):
    def run_node(self, script):
        result = subprocess.run(
            ['node', '-e', script, str(ROOT / 'code/ferrari_pop_control.js')],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_profile_pitch_and_event_authority_are_independent(self):
        self.run_node(r'''
const {PopControl} = require(process.argv[1]);
for (const [profile, pitch] of Object.entries({ferrari:0,v10:-1,v12:-2,ev:1,ioniq6n:0})) {
  const out=[]; const c=new PopControl((port,msg)=>out.push([port,msg]),profile);
  const send=(name,...args)=>c.handle(name,args);
  send('loaded',1); send('backfire_seed',100); out.length=0;
  send('audition');
  const hit=out.find(x=>x[1][0]==='play')[1];
  const measured=12*Math.log2(240/hit[1]);
  if (Math.abs(measured-pitch)>0.13) throw Error(profile+' factory pitch lost: '+measured);
  out.length=0; send('ignition',1); send('engine_running',1);
  send('overrun',1); send('shift',1); send('pop',1);
  if ((profile==='ev'||profile==='ioniq6n') && out.length) throw Error(profile+' bypassed its event authority');
  if (profile==='v10'||profile==='v12'||profile==='ferrari') {
    if (!out.some(x=>x[1][0]==='burst')) throw Error(profile+' lost ICE burst');
    if (out.filter(x=>x[1][0]==='play').length!==2) throw Error(profile+' lost ICE singles');
  }
}
''')

    def test_validated_n_event_and_all_shutdown_paths_cancel_players_and_burst(self):
        self.run_node(r'''
const {PopControl}=require(process.argv[1]);
for (const stopName of ['ignition','engine_running','event_enable','backfire_enable','profile_active']) {
  const out=[]; const c=new PopControl((port,msg)=>out.push([port,msg]),'ioniq6n');
  const send=(name,...args)=>c.handle(name,args);
  send('loaded',1); send('ignition',1); send('engine_running',1);
  send('event_hit',0.7); send('event_hit',0.9);
  if (JSON.stringify(out.filter(x=>x[1][0]==='target').map(x=>x[1][1]))!=='[1,2]') throw Error('validated hits lost');
  out.length=0; send(stopName,0);
  if (JSON.stringify(out)!==JSON.stringify([[1,['stop']],[0,['target',0]],[0,['stop']]])) throw Error(stopName+' failed cancellation');
  out.length=0; send('event_hit',1);
  if(out.length) throw Error(stopName+' allowed a late event');
  send('audition');
  if(out.filter(x=>x[1][0]==='play').length!==1) throw Error('explicit preview lost');
}
const a=[],b=[];
const one=new PopControl((port,msg)=>a.push([port,msg]),'v10');
const two=new PopControl((port,msg)=>b.push([port,msg]),'v12');
one.handle('loaded',[1]); two.handle('loaded',[1]); one.handle('pitch',[3]);
one.handle('audition',[]); two.handle('audition',[]);
if(a[1][1][1]===b[1][1][1]) throw Error('profiles share pitch or player state');
''')

    def test_live_designers_share_media_but_have_separate_controls_and_state(self):
        for profile, defaults in {
            'ferrari': (0., 4200., 0.), 'v10': (-1., 3800., -3.),
            'v12': (-2., 3200., -3.), 'ev': (1., 5000., -3.),
            'ioniq6n': (0., 4200., -3.),
        }.items():
            patch = builder.make_shared_pop_designer(profile)['patcher']
            boxes = {x['box']['id']: x['box'] for x in patch['boxes']}
            texts = [x.get('text', '') for x in boxes.values()]
            self.assertEqual(len([x for x in texts if x.startswith('buffer~ ')]), 1)
            self.assertIn('replace Patcher:/media/ferrari_pop_v3.wav', texts)
            self.assertEqual(len([x for x in texts if x.startswith('poly~ ferrari_pop_sample_voice~ 2 ')]), 1)
            self.assertFalse(any(x.startswith(('noise~', 'cycle~', 'gen~')) for x in texts))
            for name, default in zip(('pitch', 'tone', 'level'), defaults):
                knob = next(x for x, b in boxes.items() if b.get('varname') == 'pop_' + name)
                sources = [x['patchline']['source'][0] for x in patch['lines'] if x['patchline']['destination'] == [knob, 0]]
                self.assertIn('loadmess ' + format(default, 'g'), [boxes[x].get('text') for x in sources])
            version = 3 if profile == 'ferrari' else 4
            self.assertTrue(any(x.startswith('pattrstorage ' + profile + '_pop_v' + str(version)) for x in texts))
            storage = next(x for x in texts if x.startswith('pattrstorage '))
            self.assertIn('@savemode ' + ('3' if profile == 'ferrari' else '0'), storage)
            self.assertIn('js Patcher:/code/ferrari_pop_state.js' + ('' if profile == 'ferrari' else ' ' + profile), texts)

    def test_ioniq_release_edges_reach_only_armed_live_sampler(self):
        p = builder.make_ioniq6n_n_event_host()['patcher']
        boxes = {x['box']['id']: x['box'] for x in p['boxes']}
        def ids(text):
            return [i for i, b in boxes.items() if b.get('text') == text]
        edges = [(x['patchline']['source'], x['patchline']['destination']) for x in p['lines']]
        self.assertEqual(len(ids('ioniq6n_pop_v4~')), 1)
        self.assertFalse(ids('ioniq6n_n_event_beap~'))
        self.assertFalse(ids('line~'), 'Sample replacement must retire the obsolete audio envelope DSP')
        release = next(i for i, b in boxes.items() if b.get('varname') == 'n_release_edge')
        mode_select = ids('sel ignition evolution lightspeed')[0]
        for gate_name in ('n_bubble_gate', 'n_afterburner_gate'):
            gate = next(i for i,b in boxes.items() if b.get('varname') == gate_name)
            self.assertIn(([release, 0], [gate, 1]), edges, 'An event edge is data, not a pak bang retaining zero')
            self.assertTrue(any(d == [gate, 0] for _, d in edges), 'Lifecycle and mode must own the gate control')
        for arm in ids('int 0'):
            inbound = [(s, d) for s,d in edges if d[0] == arm]
            self.assertTrue(inbound)
            self.assertTrue(all(d[1] == 0 for _,d in inbound), 'Mode changes must emit a value, not leave a cold int unbanged')
        self.assertEqual(len([s for s,d in edges if s[0] == mode_select]), 5)

    def test_each_transient_keeps_start_separate_from_sample_event_voice(self):
        for profile in ('ev', 'v10', 'v12', 'ferrari'):
            p = builder.make_profile_transient(profile)['patcher']
            boxes = {x['box']['id']: x['box'] for x in p['boxes']}
            event = next((i for i,b in boxes.items() if b.get('text') == profile + '_backfire_host~'), None)
            self.assertIsNotNone(event, profile + ' must use its sole sample event host')
            router = next(i for i,b in boxes.items() if b.get('text','').startswith('route starter start_style '))
            inbound = [x['patchline']['source'] for x in p['lines'] if x['patchline']['destination'][0] == event]
            self.assertEqual(inbound, [[router, 8]], 'Starter may not be forwarded as a Pop event')

    def test_new_presets_are_profile_scoped_and_save_cancels_stale_restore(self):
        script = r'''
const fs=require('fs'),vm=require('vm');
const code=fs.readFileSync(process.argv[1],'utf8');
for(const profile of ['ev','v10','v12','ioniq6n','ferrari']) {
  const messages=[],tasks=[],reads=[];
  const ctx={jsarguments:['ferrari_pop_state.js',profile],patcher:{filepath:'/test/project/patchers/voice.maxpat'},
    outlet:(...m)=>messages.push(m),
    File:function(path){reads.push(path);this.isopen=true;this.close=()=>{};},
    Task:function(fn){this.cancelled=false;this.cancel=()=>{this.cancelled=true;};this.schedule=()=>tasks.push(this);this.run=()=>{if(!this.cancelled)fn();};}
  };
  vm.createContext(ctx);vm.runInContext(code,ctx);
  ctx.restore();
  const expected='/test/project/presets/local/'+profile+'_pop_v'+(profile==='ferrari'?'3':'4')+'.json';
  if(reads[0]!==expected)throw Error('cross-profile/old preset read '+reads[0]);
  ctx.save(); const before=messages.length; tasks.forEach(t=>t.run());
  if(messages.length!==before)throw Error('pending restore overwrote newer Save/defaults');
  if(JSON.stringify(messages.slice(-2))!==JSON.stringify([[0,'store',1],[0,'write',expected]]))throw Error('save did not target live state');
  ctx.restore();tasks.forEach(t=>t.run());
  if(JSON.stringify(messages[messages.length-1])!=='[0,1]')throw Error('reopen did not recall slot1');
}
'''
        result = subprocess.run(['node', '-e', script, str(ROOT/'code/ferrari_pop_state.js')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_real_burst_scheduler_cannot_emit_after_shutdown(self):
        self.run_node(r'''
const fs=require('fs'),vm=require('vm'),path=require('path');
const {PopControl}=require(process.argv[1]);
const schedulerCode=fs.readFileSync(path.join(path.dirname(process.argv[1]),'backfire_burst.js'),'utf8');
for(const profile of ['v10','v12','ferrari']) {
  const players=[],tasks=[];let control;
  const scheduler={outlet:(port,...args)=>control.handle('hit',args),
    Task:function(fn){this.cancelled=false;this.cancel=()=>{this.cancelled=true;};this.schedule=()=>tasks.push(this);this.run=()=>{if(!this.cancelled)fn();};}
  };
  vm.createContext(scheduler);vm.runInContext(schedulerCode,scheduler);
  control=new PopControl((port,msg)=>{
    if(port===0)players.push(msg);
    else scheduler[msg[0]](...msg.slice(1));
  },profile);
  for(const [name,value] of [['loaded',1],['ignition',1],['engine_running',1],['backfire_seed',1],['overrun',0.7]]) control.handle(name,[value]);
  if(players.filter(x=>x[0]==='play').length!==1 || tasks.length!==4)throw Error('original 5-hit schedule changed');
  control.handle('ignition',[0]);const before=players.length;
  tasks.forEach(t=>t.run());
  if(players.length!==before || tasks.some(t=>!t.cancelled))throw Error(profile+' left delayed hits alive');
}
''')


if __name__ == '__main__':
    unittest.main()
