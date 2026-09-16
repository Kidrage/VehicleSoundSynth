"""Repair contracts. These tests are not native Max or listening acceptance."""
import copy
import json
import subprocess
import unittest
from pathlib import Path
from tools import build_project as b, timbre_repair as r

ROOT=Path(__file__).resolve().parents[1]


def boxes(doc):
    return {x['box']['id']:x['box'] for x in doc['patcher']['boxes']}


class TimbreRepairTests(unittest.TestCase):
    def test_ioniq_map_preserves_idle_and_is_monotone_c1(self):
        for amount in (0,.25,.5,1):
            previous=-1
            for rpm in range(10001):
                value=r.acoustic_rpm(rpm,amount)
                self.assertGreater(value,previous)
                if rpm<=2600 or amount==0:self.assertEqual(value,rpm)
                previous=value
        self.assertEqual(r.acoustic_rpm(7600),5500)
        for knot in (2600,4200):
            dl=(r.acoustic_rpm(knot)-r.acoustic_rpm(knot-.001))/.001
            dr=(r.acoustic_rpm(knot+.001)-r.acoustic_rpm(knot))/.001
            self.assertAlmostEqual(dl,dr,places=5)

    def test_old_dsp_state_and_untouched_voices_are_byte_identical(self):
        names=subprocess.check_output(['git','ls-tree','-r','--name-only',r.BASELINE,
                                      'gen','patchers','code','presets','media'],cwd=ROOT,text=True).splitlines()
        allowed={'patchers/vehicle_engine_ioniq6n~.maxpat','patchers/vehicle_engine_ferrari~.maxpat'}
        self.assertGreater(len(names),200)
        for name in names:
            if name not in allowed:
                self.assertEqual((ROOT/name).read_bytes(),subprocess.check_output(['git','show',r.BASELINE+':'+name],cwd=ROOT),name)

    def test_only_two_engine_references_change(self):
        for profile,oldname,newname in [('ioniq6n','ioniq6n_sound_dna_v2~','ioniq6n_sound_dna_v3~'),
                                         ('ferrari','ferrari_acoustic_v3~','ferrari_acoustic_v4~')]:
            old=json.loads(subprocess.check_output(['git','show',r.BASELINE+':patchers/vehicle_engine_'+profile+'~.maxpat'],cwd=ROOT))
            new=copy.deepcopy(b.make_profile_engine(profile))
            count=0
            for box in boxes(new).values():
                if box.get('text')==newname:box['text']=oldname;count+=1
            self.assertEqual(count,1)
            self.assertEqual(new,old)

    def test_ioniq_preserves_all_beap_audio_objects(self):
        old=b.make_sound_dna('ioniq6n',version=2)
        new=r.make_ioniq_designer()
        def beap(doc):return {x.get('varname'):x['patcher'] for x in boxes(doc).values() if x['maxclass']=='bpatcher'}
        self.assertEqual(beap(old),beap(new))
        self.assertEqual(beap(b.dna_v3.make_designer('ferrari')),beap(r.make_ferrari_designer()))

    def test_new_control_reaches_the_actual_source(self):
        for doc in (r.make_ioniq_designer(),r.make_ioniq_powertrain(),r.make_ferrari_designer()):
            bs=boxes(doc); wires=[x['patchline'] for x in doc['patcher']['lines']]
            self.assertEqual(bs['repair-route']['text'],'route reference_restore')
            self.assertEqual(bs['repair-clip']['text'],'clip 0 1')
            self.assertEqual(bs['repair-tag']['text'],'prepend reference_restore')
            self.assertTrue(any(w['source']==['repair-tag',0] for w in wires))
            self.assertEqual(sum(w['source']==['repair-route',1] for w in wires),1)
        doc=r.make_ferrari_designer()
        self.assertIn('prepend accel',[x.get('text') for x in boxes(doc).values()])

    def test_single_ferrari_source_keeps_residuals_and_noise_independent(self):
        doc=r.make_ferrari_acoustic(); bs=boxes(doc)
        gen=[x for x in bs.values() if x.get('text','').startswith('gen~')]
        self.assertEqual(len(gen),1)
        self.assertIn('ferrari_dna_source_v4',gen[0]['text'])
        noise=next(x for x in bs.values() if x.get('text')=='vehicle_noise_ferrari_v2~')
        inputs=[x['patchline']['source'] for x in doc['patcher']['lines'] if x['patchline']['destination'][0]==noise['id']]
        self.assertIn([gen[0]['id'],7],inputs)
        self.assertIn([gen[0]['id'],8],inputs)
        self.assertIn([gen[0]['id'],9],inputs)
        old=b.GEN_CODE['ferrari_dna_source_v3'];new=b.GEN_CODE['ferrari_dna_source_v4']
        residual=old[old.index('// Random residuals'):]
        self.assertIn(residual,new)
        self.assertEqual(old.count('noise()'),new.count('noise()'))
        self.assertNotIn('noise()',new[new.index('// Material restoration'):])

    def test_ioniq_has_no_new_oscillators_or_random_noise(self):
        old=b.GEN_CODE['ioniq6n_powertrain_v2'];new=b.GEN_CODE['ioniq6n_powertrain_v3']
        for token in ('cycle(','noise(','phasor('):self.assertEqual(old.count(token),new.count(token))
        for prefix in ('ready_weight =','ready =','gain =','drive ='):
            a=next(line for line in old.splitlines() if line.startswith(prefix))
            self.assertIn(a,new)
        self.assertIn('repair_up*repair_up*(3-2*repair_up)',new)

    def test_factory_has_complete_state_and_restore_default(self):
        for profile,doc,key in [('ioniq6n',r.make_ioniq_designer(),'dna_reference_restore'),
                                ('ferrari',r.make_ferrari_designer(),'reference_restore')]:
            data=r.factory(profile,doc)['pattrstorage']['slots']['99']['data']
            self.assertEqual(data[key],[1.])
            for name,value in b.dna_v3.beap_factory_data(doc).items():self.assertEqual(data[name],value)
            texts=[x.get('text','') for x in boxes(doc).values()]
            self.assertNotIn('closebang',texts)
            self.assertTrue(any('timbre_repair_state.js '+profile in text for text in texts))

    def test_migration_is_whitelisted_validated_and_readonly_to_older_versions(self):
        js="""
const s=require('./code/timbre_repair_state.js');
const factory={'dna_reference_restore':[1],'dna_motor_order':[.72],'DNA_Cavity::Freq':[315]};
console.log(JSON.stringify({paths:s.paths('ioniq6n','/qa/patchers/x.maxpat'),
ferrari:s.paths('ferrari','/qa/patchers/x.maxpat'),
merged:s.merge(factory,{'dna_motor_order':[.2],'DNA_Cavity::Freq':[420],'sc_gain':[1]}),
bad:[null,'0',{length:1},[null],[Infinity],['1']].map(v=>s.merge(factory,{'dna_motor_order':v}))}));
"""
        data=json.loads(subprocess.check_output(['node','-e',js],cwd=ROOT,text=True))
        self.assertEqual(data['merged'],{'dna_reference_restore':[1],'dna_motor_order':[.2],'DNA_Cavity::Freq':[420]})
        for bad in data['bad']:self.assertEqual(bad['dna_motor_order'],[.72])
        self.assertTrue(data['paths']['local'].endswith('ioniq6n_sound_dna_v3.json'))
        self.assertTrue(data['ferrari']['local'].endswith('ferrari_sound_dna_v4.json'))
        self.assertEqual(len(data['paths']['previous']),2)
        self.assertEqual(len(data['ferrari']['previous']),1)
        source=(ROOT/'code/timbre_repair_state.js').read_text()
        self.assertEqual(source.count("outlet(0,'write'"),1)
        self.assertIn("paths(profile,this.patcher.filepath).local",source)

    def test_generated_graph_ports_have_no_dangling_connections(self):
        def validate(p):
            bs={x['box']['id']:x['box'] for x in p['boxes']}
            self.assertEqual(len(bs),len(p['boxes']))
            for item in p.get('lines',[]):
                w=item['patchline'];src,oi=w['source'];dst,ii=w['destination']
                self.assertIn(src,bs);self.assertIn(dst,bs)
                if 'numoutlets' in bs[src]:self.assertLess(oi,bs[src]['numoutlets'],(src,oi))
                if 'numinlets' in bs[dst]:self.assertLess(ii,bs[dst]['numinlets'],(dst,ii))
            for item in bs.values():
                if 'patcher' in item:validate(item['patcher'])
        for name,doc in r.outputs().items():
            if 'patcher' in doc:validate(doc['patcher'])

    def test_project_registers_both_new_and_old_versions(self):
        contents=b.project_file()['contents']
        for path in r.SEEDS:self.assertIn(path,contents['patchers'])
        for path in ('gen/ioniq6n_powertrain_v3.gendsp','gen/ferrari_dna_source_v4.gendsp','code/timbre_repair_state.js'):
            self.assertIn(path,contents['code'])
        self.assertIn('gen/ferrari_dna_source_v3.gendsp',contents['code'])
        self.assertIn('patchers/ioniq6n_sound_dna_v2~.maxpat',contents['patchers'])

    def test_repair_generation_is_deterministic(self):
        self.assertEqual(r.outputs(),r.outputs())


if __name__=='__main__':unittest.main()
