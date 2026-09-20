"""IONIQ running-weight regression contracts; not native Max listening tests."""
import copy
import json
from pathlib import Path
import subprocess
import unittest
from tools import build_project as b, ioniq_weight_balance as w
from tools.install_ioniq_weight import outputs
ROOT=Path(__file__).resolve().parents[1]


def boxes(d):return {i['box']['id']:i['box'] for i in d['patcher']['boxes']}
def wires(d):return [i['patchline'] for i in d['patcher']['lines']]


class IoniqWeightTests(unittest.TestCase):
    def test_all_prior_audio_and_state_except_ioniq_adapter_are_unchanged(self):
        paths=subprocess.check_output(['git','ls-tree','-r','--name-only',w.BASELINE,'gen','patchers','code','presets','media'],cwd=ROOT,text=True).splitlines()
        self.assertEqual(len(paths),268)
        for p in paths:
            if p in {'patchers/vehicle_engine_ioniq6n~.maxpat','patchers/vehicle_engine_ferrari~.maxpat'}:continue
            self.assertEqual((ROOT/p).read_bytes(),subprocess.check_output(['git','show',w.BASELINE+':'+p],cwd=ROOT),p)

    def test_only_ioniq_dna_and_soundscape_references_change(self):
        old=json.loads(subprocess.check_output(['git','show',w.BASELINE+':patchers/vehicle_engine_ioniq6n~.maxpat'],cwd=ROOT))
        new=b.make_profile_engine('ioniq6n');n=0
        replacements={'ioniq6n_sound_dna_v4~':'ioniq6n_sound_dna_v3~','ioniq6n_cinematic_soundscape_host_v3~':'ioniq6n_cinematic_soundscape_host~'}
        for box in boxes(new).values():
            if box.get('text') in replacements:box['text']=replacements[box['text']];n+=1
        self.assertEqual(n,2);self.assertEqual(new,old)

    def test_no_pitch_map_or_other_order_rewrite_and_no_random_source(self):
        old=b.GEN_CODE['ioniq6n_powertrain_v3'];new=b.GEN_CODE['ioniq6n_powertrain_v4']
        for prefix in ('root =','body =','ready_weight =','ready =','order2 =','order3 =','gain ='):
            self.assertIn(next(l for l in old.splitlines() if l.startswith(prefix)),new)
        self.assertEqual(old.count('cycle(')+2,new.count('cycle('))
        self.assertNotIn('noise(',new);self.assertIn('(1-.62*wb_active)',new)
        self.assertIn('(r-1600)/1200',new)
        self.assertIn('wb_control*wb_progress*wb_progress*(3-2*wb_progress)',new)

    def test_foundation_does_not_follow_pitch_or_speed(self):
        _,code=w.foundation_code()
        self.assertNotIn('root',code);self.assertNotIn('speed',code)
        sc=b.GEN_CODE['ioniq6n_weight_bed']
        self.assertNotIn('transpose',sc.split('out1 =')[1])
        self.assertIn('in1/5',sc);self.assertIn('(in2-.12)/.88',sc)
        self.assertIn('wb_exciter-wb_x2',sc)
        self.assertIn('samplerate*.09',sc)

    def test_existing_beap_modules_are_identical(self):
        def embedded(d):return {x['varname']:x['patcher'] for x in boxes(d).values() if x['maxclass']=='bpatcher'}
        self.assertEqual(embedded(w.make_dna()),embedded(b.timbre_repair.make_ioniq_designer()))
        for m in w.MODES:self.assertEqual(embedded(w.make_mode(m)),embedded(b.make_ioniq6n_soundscape_beap(m,version=2)))

    def test_foundation_passes_real_dna_fader_and_filters(self):
        d=w.make_powertrain();bs=boxes(d);ww=wires(d)
        source=next(x['id'] for x in bs.values() if x.get('text','').startswith('gen~'))
        gain=None
        for ch in range(4):
            trim=next(x['destination'][0] for x in ww if x['source']==[source,ch])
            got=next(x['source'] for x in ww if x['destination']==[trim,1])
            if gain is None:gain=got
            self.assertEqual(gain,got)
        d=w.make_dna();bs=boxes(d);ww=wires(d)
        for ch,name in ((2,'DNA_Body_Modal'),(3,'DNA_Cavity')):
            f=next(x['id'] for x in bs.values() if x.get('varname')==name)
            self.assertIn({'source':[f'wb-band-sum{ch}',0],'destination':[f,0]},ww)
            self.assertTrue(any(x['source'][1]==ch and x['destination']==[f'wb-band-sum{ch}',1] for x in ww))

    def test_soundscape_mass_has_dry_path_before_safety_and_trim(self):
        for mode in w.MODES:
            d=w.make_mode(mode);bs=boxes(d);ww=wires(d)
            safe=[x['id'] for x in bs.values() if x.get('text')=='svf~ 28 0.7']
            self.assertEqual(len(safe),2)
            for i,o in enumerate(safe):
                self.assertIn({'source':['wb-gen',0],'destination':[f'wb-dry-sum{i}',1]},ww)
                self.assertIn({'source':[f'wb-dry-sum{i}',0],'destination':[o,0]},ww)
            self.assertIn('wb-autopattr',bs)
            self.assertEqual(bs['wb-route']['text'],'route weight_balance foundation rpm')

    def test_soundscape_host_keeps_existing_gates_and_fader(self):
        old=b.make_ioniq6n_soundscape_host();new=w.make_host()
        ob,nb=boxes(old),boxes(new)
        for name in ob:
            if ob[name].get('text','').startswith(('ioniq6n_soundscape_','js Patcher:/code/ioniq6n_bed_state.js','pattrstorage ')):continue
            self.assertEqual(ob[name],nb[name])
        for edge in wires(old):self.assertIn(edge,wires(new))
        voices=[x for x in nb.values() if x.get('text','').startswith('ioniq6n_soundscape_')]
        for v in voices:self.assertIn({'source':['wb-rpm-tag',0],'destination':[v['id'],8]},wires(new))

    def test_complete_factory_covers_every_named_beap_client(self):
        for kind in ('dna','soundscape'):
            data=w.factory(kind)['pattrstorage']['slots']['99']['data']
            if kind=='dna':
                self.assertEqual(data['dna_weight_balance'],[1.]);self.assertEqual(data['dna_foundation'],[.7])
            else:
                for m in w.MODES:
                    prefix=f'ioniq6n_soundscape_{m}_bed_v3_beap~::'
                    for k in b.dna_v3.beap_factory_data(w.make_mode(m)):self.assertIn(prefix+k,data)
                    self.assertEqual(data[prefix+'bed_weight_balance'],[1.])

    def test_state_migrates_all_versions_without_touching_older_paths(self):
        script="""
const s=require('./code/ioniq_weight_state.js');
const a='ioniq6n_soundscape_evolution_bed_v3_beap~::';
const f={n_sound_mode_state:['evolution'],[a+'Score_Body::Freq']:[.6],[a+'bed_foundation']:[.7]};
const saved={n_sound_mode_state:['lightspeed'],'ioniq6n_soundscape_evolution_bed_v2_beap~::Score_Body::Freq':[.88]};
console.log(JSON.stringify({merged:s.merge(f,saved),
 bad:s.merge(f,{n_sound_mode_state:['bad'],[a+'bed_foundation']:'wrong'}),
 dna:s.paths('dna','/qa/patchers/d.maxpat'),sc:s.paths('soundscape','/qa/patchers/s.maxpat'),
 old:s.remap({'ioniq6n_soundscape_ignition_beap~::A':[.1]})}));
"""
        result=json.loads(subprocess.check_output(['node','-e',script],cwd=ROOT,text=True))
        self.assertEqual(result['merged']['n_sound_mode_state'],['lightspeed'])
        self.assertEqual(result['merged']['ioniq6n_soundscape_evolution_bed_v3_beap~::Score_Body::Freq'],[.88])
        self.assertEqual(result['bad']['n_sound_mode_state'],['evolution'])
        self.assertEqual(len(result['dna']['previous']),3);self.assertEqual(len(result['sc']['previous']),2)
        self.assertTrue(result['dna']['local'].endswith('ioniq6n_sound_dna_v4.json'))
        self.assertTrue(result['sc']['local'].endswith('ioniq6n_soundscape_modes_v3.json'))
        self.assertEqual(result['old'],{'ioniq6n_soundscape_ignition_bed_v3_beap~::A':[.1]})
        js=(ROOT/'code/ioniq_weight_state.js').read_text()
        self.assertEqual(js.count("outlet(0,'write'"),1)
        self.assertIn("paths(kind,this.patcher.filepath).local",js)

    def test_invalid_numeric_state_falls_back_and_new_controls_are_bounded(self):
        script="""
const s=require('./code/ioniq_weight_state.js');const f={dna_weight_balance:[1],dna_foundation:[.7]};
console.log(JSON.stringify({bad:[null,'x',{},[Infinity],[NaN],['1'],[1,2]].map(v=>s.merge(f,{dna_foundation:v})),
 bounded:s.merge(f,{dna_foundation:[2],dna_weight_balance:[-1],foreign:[1]})}));
"""
        d=json.loads(subprocess.check_output(['node','-e',script],cwd=ROOT,text=True))
        for x in d['bad']:self.assertEqual(x['dna_foundation'],[.7])
        self.assertEqual(d['bounded'],{'dna_weight_balance':[0],'dna_foundation':[1]})

    def test_all_generated_ports_and_ids_are_valid(self):
        def check(p):
            bs={x['box']['id']:x['box'] for x in p['boxes']};self.assertEqual(len(bs),len(p['boxes']))
            for x in p.get('lines',[]):
                src,o=x['patchline']['source'];dst,i=x['patchline']['destination']
                self.assertIn(src,bs);self.assertIn(dst,bs)
                if 'numoutlets' in bs[src]:self.assertLess(o,bs[src]['numoutlets'])
                if 'numinlets' in bs[dst]:self.assertLess(i,bs[dst]['numinlets'])
            for o in bs.values():
                if 'patcher' in o:check(o['patcher'])
        for d in outputs().values():
            if 'patcher' in d:check(d['patcher'])

    def test_project_contains_both_new_and_rollback_resources(self):
        p=b.project_file()['contents']
        for f in w.SEEDS:self.assertIn(f,p['patchers'])
        self.assertIn('patchers/ioniq6n_sound_dna_v3~.maxpat',p['patchers'])
        self.assertIn('patchers/ioniq6n_soundscape_evolution_bed_v2_beap~.maxpat',p['patchers'])
        self.assertIn('gen/ioniq6n_weight_bed.gendsp',p['code'])
        self.assertIn('gen/ioniq6n_powertrain_v4.gendsp',p['code'])

    def test_scoped_generator_is_deterministic(self):
        self.assertEqual(outputs(),outputs())
        for path,doc in outputs().items():self.assertEqual(json.loads((ROOT/path).read_text()),doc,path)


if __name__=='__main__':unittest.main()
