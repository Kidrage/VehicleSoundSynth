"""Candidate acoustic contracts; legacy graphs remain rollback authorities."""
import unittest
import json
import subprocess
from pathlib import Path
from tools import build_project as b

ROOT = Path(__file__).resolve().parents[1]


class DNAV3Tests(unittest.TestCase):
    def test_v3_probes_never_auto_close_into_nested_save_modals(self):
        from tools.build_runtime_probe import make_probe
        for driver in ('coreaudio','nonrealtime'):
            patch=make_probe(Path('/private/tmp/v3-test.wav'),'ferrari',False,
                             acoustic_version=3,driver_mode=driver,direct_powertrain=True)['patcher']
            text=[item['box'].get('text','') for item in patch['boxes'] if item['box']['maxclass']=='message']
            self.assertFalse(any('wclose' in value for value in text))

    def test_factory_reset_covers_every_live_beap_restore_client(self):
        for profile in b.dna_v3.PROFILES:
            patch=b.dna_v3.make_designer(profile)['patcher']
            factory=b.dna_v3.factory(profile)['pattrstorage']['slots']['99']['data']
            for item in patch['boxes']:
                box=item['box']
                if box.get('maxclass')!='bpatcher': continue
                for child in box['patcher']['boxes']:
                    for key,value in child['box'].get('restore',{}).items():
                        self.assertEqual(factory.get(box['varname']+'::'+key),value,(profile,key))

    def test_protected_audio_resources_are_byte_unchanged(self):
        files = subprocess.check_output(['git','ls-tree','-r','--name-only','cff9d08','gen','patchers','media','presets'],cwd=ROOT,text=True).splitlines()
        protected = [name for name in files if ('soundscape' in name or 'engine_start' in name or 'pop_' in name
                      or 'activation' in name or 'ioniq6n_powertrain' in name or 'ev_powertrain' in name
                      or 'ioniq6n_sound_dna' in name or 'ev_sound_dna' in name or name.startswith('media/'))]
        self.assertGreater(len(protected),50)
        for name in protected:
            self.assertEqual((ROOT/name).read_bytes(),subprocess.check_output(['git','show','cff9d08:'+name],cwd=ROOT),name)

    def test_noise_v1_and_old_designers_remain_factory_equivalent(self):
        for profile in b.PROFILE_ORDER:
            old=json.loads(subprocess.check_output(['git','show',f'cff9d08:patchers/vehicle_noise_{profile}~.maxpat'],cwd=ROOT))
            self.assertEqual(old,b.make_vehicle_noise(profile),profile)

    def test_v3_migration_preserves_only_unchanged_v2_idle_semantics(self):
        script = """
const s=require('./code/dna_v3_state.js');
console.log(JSON.stringify({paths:s.paths('v10','/candidate/patchers/v10_dna_v3_designer~.maxpat'),
 data:s.migrate({dna_idle_body:[.22],dna_body:[.31],dna_running_body:[1],dna_v3_body:[0],
 'OldFilter::Freq':[100],dna_aggression:['bad']})}));
"""
        result=json.loads(subprocess.check_output(['node','-e',script],cwd=ROOT,text=True))
        self.assertEqual(result['data'],{'legacy_body':.31,'legacy_idle_body':.22})
        self.assertEqual(result['paths']['local'],'/candidate/presets/local/v10_sound_dna_v3.json')
        self.assertTrue(result['paths']['legacy'].endswith('_v2.json'))

    def test_new_macros_and_gain_controls_reach_the_live_designer(self):
        from tests.test_runtime_design_routing import destinations
        for profile in b.dna_v3.PROFILES:
            patch=b.dna_v3.make_designer(profile)['patcher']
            boxes={i['box']['id']:i['box'] for i in patch['boxes']}
            wires=[i['patchline'] for i in patch['lines']]
            for name,_,_ in b.dna_v3.MACROS:
                ui=next(i for i,x in boxes.items() if x.get('varname')==name)
                self.assertTrue(any(x['source'][0]==ui for x in wires),name)
                self.assertEqual(destinations(profile,name,b.make_profile_runtime_host(profile)['patcher']),[(f'vehicle_engine_{profile}~',name)])
            self.assertTrue(any('add_db_gain' not in x.get('text','') and x.get('text','').startswith('route ') and 'powertrain_level_db' in x['text'] for x in boxes.values()))
            self.assertIn('V3_Group_Mixer', [x.get('varname') for x in boxes.values()])

    def test_ferrari_owns_one_source_and_two_independent_stems(self):
        from tools.dna_v3 import make_acoustic
        patch = make_acoustic('ferrari')['patcher']
        boxes = {x['box']['id']: x['box'] for x in patch['boxes']}
        sources = [i for i, x in boxes.items() if x.get('text', '').startswith('gen~')]
        self.assertEqual(len(sources), 1)
        dna = next(i for i,x in boxes.items() if 'dna_v3_designer~' in x.get('text',''))
        noise = next(i for i,x in boxes.items() if 'vehicle_noise_ferrari_v2~' in x.get('text',''))
        self.assertEqual(len([x for x in boxes.values() if x.get('maxclass') == 'outlet']), 4)
        lines = [x['patchline'] for x in patch['lines']]
        self.assertFalse(any(x['source'][0] == dna and x['destination'][0] == noise for x in lines))
        self.assertEqual([x['source'][1] for x in lines if x['source'][0] == sources[0] and x['destination'][0] == noise], [7,8,9])

    def test_separate_deterministic_and_residual_audio_seam(self):
        from tools.dna_v3 import source_code
        for profile in ('ferrari', 'v10', 'v12'):
            code = source_code(profile, b.GEN_CODE.get(profile + '_powertrain'))
            patch = b.make_gen(code)['patcher']
            outputs = [x['box']['text'] for x in patch['boxes']
                       if x['box'].get('text', '').startswith('out ')]
            self.assertEqual(len(outputs), 10)
            # Audio groups are independently available before output gain/mix.
            for index in range(1, 11):
                self.assertIn('out%d =' % index, code)
            self.assertNotIn('powertrain_level_db', code)


if __name__ == '__main__':
    unittest.main()
