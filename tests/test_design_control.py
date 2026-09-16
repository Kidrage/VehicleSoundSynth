import json
import subprocess
import unittest
from pathlib import Path
from tools import build_project as builder

ROOT = Path(__file__).resolve().parents[1]


class DesignControlTests(unittest.TestCase):
    def test_audit_reads_beap_ranges_and_real_v3_save_namespace(self):
        from tools.audit_v3_controls import visible_controls
        rows=visible_controls(ROOT)
        mixer=next(row for row in rows if row['profile']=='ferrari'
                   and row['file'].endswith('ferrari_dna_v4_designer~.maxpat')
                   and row['object']=='/V3_Group_Mixer/in2')
        self.assertEqual((mixer['UI_min'],mixer['UI_max']),(-72,0))
        self.assertEqual(mixer['save_namespace'],'ferrari_sound_dna_v4.json')
        self.assertIn('dbtoa',mixer['DSP_mapping'])
        self.assertEqual(mixer['status'],'native_unverified')

    def test_registry_documents_every_design_and_mixer_selector_without_owning_state(self):
        script = """
const d=require('./code/design_control.js'), r=d.registry;
const names=[...r.direct,...Object.keys(r.normalized),
 ...Object.values(r.modes).flatMap(x=>Object.keys(x)),
 'powertrain_level_db','start_level_db','transient_level_db','soundscape_level_db',
 'road_level_db','rumble_level_db','master_trim_db','eshift_enable','dna_open'];
console.log(JSON.stringify(names.map(name=>[name,d.describe(name)])));
"""
        contracts=json.loads(subprocess.check_output(['node','-e',script],cwd=ROOT,text=True))
        for name, contract in contracts:
            for key in ('owner','payload','bypass_drive_gate','readback','save','context','profiles'):
                self.assertIn(key,contract,(name,key))
            self.assertNotEqual(contract['owner'],'design_control',name)
        byname=dict(contracts)
        self.assertEqual(byname['eq_lowmid']['bounds'],[[120,1200],[-12,12],[.3,4]])
        self.assertEqual(byname['compressor_ratio']['save'],'not persisted')
        self.assertEqual(byname['eshift_enable']['owner'],'DriveModel; engine receives notification only')

    def test_bounded_payload_is_applied_before_same_feedback(self):
        script = """
const fs=require('fs'),vm=require('vm'),file=process.argv[1],calls=[];
const c={jsarguments:['design_control.js','ferrari'],outlet:(...a)=>calls.push(a),
 arrayfromargs:a=>Array.from(a)};vm.createContext(c);vm.runInContext(fs.readFileSync(file,'utf8'),c);
c.messagename='eq_lowmid';c.anything(99999,30,.01);
c.messagename='compressor_ratio';c.anything(100);
c.messagename='eq_lowmid';c.anything(400,2); // invalid arity: no partial EQ update
c.messagename='compressor_ratio';c.anything(NaN);
console.log(JSON.stringify(calls));
"""
        calls = json.loads(subprocess.check_output(['node','-e',script,str(ROOT/'code/design_control.js')],text=True))
        self.assertEqual([[0,['eq_lowmid',1200,12,.3]],[1,['eq_lowmid',1200,12,.3]],
                          [0,['compressor_ratio',50]],[1,['compressor_ratio',50]]], calls)

    def test_engine_tone_feedback_has_no_request_bypass(self):
        for profile in builder.PROFILE_ORDER:
            p=builder.make_profile_engine(profile)['patcher']
            boxes={x['box']['id']:x['box'] for x in p['boxes']}
            adapter=next(i for i,b in boxes.items() if b.get('text')==f'js Patcher:/code/design_control.js {profile}')
            edges=[x['patchline'] for x in p['lines']]
            applied=[e for e in edges if e['source']==[adapter,0]]
            feedback=[e for e in edges if e['source']==[adapter,1]]
            self.assertEqual(1,len(applied));self.assertEqual(1,len(feedback))
            self.assertEqual(f'engine_controller_{profile}',boxes[applied[0]['destination'][0]]['text'])
            self.assertEqual('outlet',boxes[feedback[0]['destination'][0]]['maxclass'])

    def test_ioniq_notification_is_removed_before_source_selection(self):
        p=builder.make_profile_runtime_host('ioniq6n')['patcher']
        boxes={x['box']['id']:x['box'] for x in p['boxes']}
        bytext={b.get('text'):i for i,b in boxes.items()}
        edges=[x['patchline'] for x in p['lines']]
        driver=bytext['drive_simulator_ioniq6n']; split=bytext['routepass eshift_enable']
        engine=bytext['vehicle_engine_ioniq6n~'];source=bytext['switch 2']
        self.assertEqual([{'source':[driver,0],'destination':[split,0]}],
                         [e for e in edges if e['source']==[driver,0]])
        self.assertIn({'source':[split,0],'destination':[engine,0]},edges)
        self.assertIn({'source':[split,1],'destination':[source,1]},edges)
        self.assertNotIn({'source':[split,0],'destination':[source,1]},edges)
