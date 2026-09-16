"""IONIQ-only enhancement: reversible sound and complete state contract."""
import unittest
import json
import subprocess
from tools import build_project as b


class IoniqDNAV2Tests(unittest.TestCase):
    def test_accel_orders_is_a_live_versioned_control(self):
        patch = b.make_sound_dna('ioniq6n', version=2)['patcher']
        boxes = [x['box'] for x in patch['boxes']]
        self.assertIn('dna_accel_orders', [x.get('varname') for x in boxes])
        self.assertIn('ioniq6n_powertrain_v2~', [x.get('text') for x in boxes])
        self.assertIn('ioniq6n_powertrain_v2', b.GEN_CODE)

    def test_factory_reset_includes_nested_beap_and_macros(self):
        document = b.make_sound_dna('ioniq6n', version=2)
        factory = b.ioniq_dna_v2.factory(document)['pattrstorage']['slots']['99']['data']
        self.assertEqual(factory['dna_accel_orders'], [.30])
        self.assertEqual(factory['dna_motor_order'], [.72])
        for name, value in b.dna_v3.beap_factory_data(document).items():
            self.assertEqual(factory[name], value)
        texts = [x['box'].get('text','') for x in document['patcher']['boxes']]
        self.assertIn('js Patcher:/code/ioniq_dna_v2_state.js', texts)
        self.assertNotIn('closebang', texts)

    def test_state_migration_is_whitelisted_and_defaults_complete(self):
        script = """
const s=require('./code/ioniq_dna_v2_state.js');
const factory={'dna_accel_orders':[.3],'dna_motor_order':[.72],'DNA_Cavity::Freq':[315]};
const saved={'dna_motor_order':[.4],'DNA_Cavity::Freq':[400],'soundscape_level':[1]};
console.log(JSON.stringify({data:s.merge(factory,saved),paths:s.paths('/qa/patchers/dna.maxpat')}));
"""
        result = json.loads(subprocess.check_output(['node','-e',script],text=True))
        self.assertEqual(result['data'], {'dna_accel_orders':[.3],'dna_motor_order':[.4],'DNA_Cavity::Freq':[400]})
        self.assertEqual(result['paths']['local'],'/qa/presets/local/ioniq6n_sound_dna_v2.json')

    def test_audio_graph_keeps_all_accepted_beap_boxes_and_connections(self):
        old = b.make_sound_dna('ioniq6n')['patcher']
        new = b.make_sound_dna('ioniq6n',version=2)['patcher']
        def modules(patch):
            return {x['box']['varname']:x['box']['patcher'] for x in patch['boxes'] if x['box']['maxclass']=='bpatcher'}
        self.assertEqual(modules(old),modules(new))
        # V2 remains a rollback resource; active repair is separately versioned.
        self.assertIn('ioniq6n_sound_dna_v3~',json.dumps(b.make_profile_engine('ioniq6n')))

    def test_malformed_saved_values_fall_back_without_aborting_reload(self):
        script = """
const s=require('./code/ioniq_dna_v2_state.js');
const factory={'dna_motor_order':[.72]};
console.log(JSON.stringify(['0',{length:1},[null],['.4'],[NaN]].map(value=>s.merge(factory,{'dna_motor_order':value}))));
"""
        result = json.loads(subprocess.check_output(['node','-e',script],text=True))
        self.assertEqual(result,[{'dna_motor_order':[.72]}]*5)

    def test_every_macro_reaches_bounded_gen_input(self):
        patch = b.make_ioniq6n_powertrain(version=2)['patcher']
        boxes = {x['box']['id']:x['box'] for x in patch['boxes']}
        lines = [x['patchline'] for x in patch['lines']]
        router = next(x for x in boxes.values() if x.get('text','').startswith('route '))
        names = router['text'].split()[1:]
        gen = next(x['id'] for x in boxes.values() if x.get('text','').startswith('gen~ '))
        for key,_,_,_ in b.DNA_PARAMETER_SPECS['ioniq6n']+b.ioniq_dna_v2.SPECS:
            clip = next(x['destination'][0] for x in lines if x['source']==[router['id'],names.index(key)])
            self.assertEqual(boxes[clip]['text'],'clip 0 1')
            tag = next(x['destination'][0] for x in lines if x['source']==[clip,0])
            self.assertEqual(boxes[tag]['text'],'prepend '+key)
            self.assertIn({'source':[tag,0],'destination':[gen,0]},lines)
