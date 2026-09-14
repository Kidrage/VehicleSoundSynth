import json
import subprocess
import unittest
from pathlib import Path
from tools import build_project as builder

ROOT = Path(__file__).resolve().parents[1]


class DesignControlTests(unittest.TestCase):
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
