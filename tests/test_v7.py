"""V7 candidate regression gates. Scalar GenExpr math != native Max acceptance."""
import hashlib,json,subprocess,tempfile,unittest
from pathlib import Path
import numpy as np
from tools.build_v7 import ROOT,SOURCE_NAMES,build
from tools.v7.schema import PARAMS,PROFILES,defaults
from tools.v7.scalar_harness import Kernel,compile_library

def node(script):
    r=subprocess.run(['node','-e',script],cwd=ROOT,text=True,capture_output=True,check=True)
    return json.loads(r.stdout)
def patch(name):return json.loads((ROOT/name).read_text())['patcher']
def rms(x):return np.sqrt(np.mean(np.square(x)))

class V7Graph(unittest.TestCase):
    def test_baseline_seeds_not_overwritten(self):
        m=json.loads((ROOT/'assets/v7/resource_map.json').read_text())
        for rel,h in m['protected_seed_sha256'].items():
            self.assertEqual(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest(),h,rel)
    def test_generated_determinism_and_protection(self):
        for rel,text in build().items():self.assertEqual((ROOT/rel).read_text(),text,rel)
    def test_all_graph_ports(self):
        def check(p,label):
            by={x['box']['id']:x['box'] for x in p['boxes']};self.assertEqual(len(by),len(p['boxes']),label)
            for e in p['lines']:
                s,so=e['patchline']['source'];d,di=e['patchline']['destination']
                self.assertIn(s,by,label);self.assertIn(d,by,label)
                self.assertLess(so,by[s].get('numoutlets',1),(label,s));self.assertLess(di,by[d].get('numinlets',1),(label,d))
            for b in by.values():
                if 'patcher' in b:check(b['patcher'],label+'/'+b['id'])
        for f in sorted((ROOT/'patchers').glob('v7_*.maxpat')):check(json.loads(f.read_text())['patcher'],f.name)
    def test_five_profiles_have_mass_balance_and_state(self):
        for p in PROFILES:
            e=patch(f'patchers/v7_vehicle_engine_{p}~.maxpat');texts='\n'.join(x['box'].get('text','') for x in e['boxes'])
            self.assertIn(f'v7_mass_{p}.gendsp',texts);self.assertIn('v7_balance.gendsp',texts)
            self.assertIn('v7-mass-solo',[x['box']['id'] for x in e['boxes']])
            # Mass must NOT enter the rumble generator's audio input.
            by={x['box']['id']:x['box'] for x in e['boxes']}
            for edge in e['lines']:
                l=edge['patchline']
                if l['source'][0].startswith('v7-mass'):
                    self.assertNotIn('cabin_rumble',by[l['destination'][0]].get('text',''))
            host=json.dumps(patch(f'patchers/v7_profile_runtime_host_{p}.maxpat'))
            self.assertIn('v7_profile_state.js '+p,host);self.assertIn('v7-filter',host)
    def test_ui_units_no_feedback_loop(self):
        for page in ('tone','response'):
            p=patch(f'patchers/v7_{page}_console.maxpat');by={e['box']['id']:e['box'] for e in p['boxes']}
            for n,b in by.items():
                if n in PARAMS:
                    self.assertEqual(b['minimum'],PARAMS[n]['min']);self.assertEqual(b['maximum'],PARAMS[n]['max'])
                    self.assertTrue(b['hint']);self.assertEqual(by['set-'+n]['text'],'prepend set')
            self.assertFalse(any(b.get('text','').startswith('loadmess') for b in by.values()))
    def test_owner_saves_and_isolated_paths(self):
        for p in PROFILES:
            text=json.dumps(patch(f'patchers/v7_vehicle_engine_{p}~.maxpat'))
            for name in ('dna_save','noise_save','start_save','backfire_save','event_save'):self.assertIn(name,text)
        m=json.loads((ROOT/'assets/v7/resource_map.json').read_text())
        for original,copied in m['mapping'].items():
            if original.endswith('.js'):
                text=(ROOT/copied).read_text()
                self.assertNotRegex(text,r'/presets/local/(?!v7_)')
    def test_main_dsp_free_v7_entries(self):
        p=patch('main.maxpat');text=json.dumps(p)
        for suffix in ('EV','V10','V12','IONIQ6N','Ferrari'):self.assertIn('EV-Engine-V7-'+suffix+'.maxpat',text)
        for b in (x['box'] for x in p['boxes']):self.assertNotRegex(b.get('text',''),r'^(gen~|ezdac~|cycle~|adc~|dac~)')

class V7Drive(unittest.TestCase):
    def test_lift_does_not_upshift(self):
        out=node('''const X=require('./code/v7_drive_model.js');let all=[];for(let mode of [0,1]){let m=new X.DriveModel('ioniq6n');m.v7Enabled=mode;m.running=1;m.ignition=1;m.startElapsed=1;m.launchCoupled=true;m.gear=1;m.speed=6000/m.config.ratios[0];m.rpm=6000;m.throttle=.9;m.v7StrategyThrottle=.9;m.manualThrottle=0;let e=m.tick(.02);all.push({gear:m.gear,e});}console.log(JSON.stringify(all));''')
        self.assertEqual(out[0]['gear'],2);self.assertEqual(out[1]['gear'],1)
    def test_full_eight_gears_and_high_rpm_span(self):
        out=node('''const X=require('./code/v7_drive_model.js');let m=new X.DriveModel('ioniq6n');m.handle('ignition',[1]);m.handle('start',[1]);m.handle('throttle',[1]);let shifts=[],invalid=[];for(let i=0;i<1600;i++){let e=m.tick(.02);if(e.some(x=>x[0]=='shift'&&x[1]===1))shifts.push([m.gear,m.rpm]);if(!Number.isFinite(m.rpm)||m.rpm>8000.001||m.gear>8)invalid.push(i);}console.log(JSON.stringify({shifts,invalid}));''')
        self.assertEqual([x[0] for x in out['shifts']],list(range(2,9)));self.assertFalse(out['invalid'])
        self.assertTrue(all(7770<x[1]<7999 for x in out['shifts']))
    def test_coast_brake_monotonic_down_gears_and_finite(self):
        out=node('''const X=require('./code/v7_drive_model.js');let result=[];for(let p of ['ev','v10','v12','ioniq6n','ferrari']){let m=new X.DriveModel(p);m.handle('ignition',[1]);m.handle('start',[1]);m.handle('throttle',[1]);for(let i=0;i<1000;i++)m.tick(.02);m.handle('throttle',[0]);m.handle('brake',[.8]);let gears=[];for(let i=0;i<1500;i++){let e=m.tick(.02);if(e.some(x=>x[0]=='shift'&&x[1]===1))gears.push(m.gear);}result.push({p,gears,rpm:m.rpm,speed:m.speed});}console.log(JSON.stringify(result));''')
        for r in out:
            self.assertEqual(r['gears'],sorted(r['gears'],reverse=True));self.assertLess(r['speed'],1)
    def test_nan_inputs_and_external_telemetry_not_faked(self):
        out=node('''const X=require('./code/v7_drive_model.js');let m=new X.DriveModel('ioniq6n');let initial=m.snapshot();m.handle('throttle',[NaN]);m.handle('brake',[Infinity]);let a=m.handle('rpm',[9000]);let b=m.handle('gear',[8]);console.log(JSON.stringify({initial,s:m.snapshot(),a,b}));''')
        self.assertEqual(out['s'],out['initial']);self.assertEqual(out['a'][0][1],650);self.assertEqual(out['b'][0][1],1)
    def test_cut_holds_pitch_then_sweep(self):
        out=node('''const X=require('./code/v7_drive_model.js');let m=new X.DriveModel('ioniq6n');m.running=1;m.launchCoupled=true;m.speed=80;m.rpm=7700;m.gear=1;m.beginShift(1,[]);let out=[];for(let i=0;i<20;i++){if(m.shift)m.updateShift(.02,[]);out.push([m.rpm,m.shiftCut]);}console.log(JSON.stringify(out));''')
        self.assertAlmostEqual(out[0][0],7700);self.assertAlmostEqual(out[1][0],7700);self.assertLess(out[3][0],out[2][0]);self.assertAlmostEqual(out[-1][1],1)

class V7State(unittest.TestCase):
    def test_roundtrip_cross_profile_corruption_and_no_drive_state(self):
        script=(ROOT/'tools/v7/test_state_vm.js').read_text()
        result=node(script)
        self.assertTrue(result['pass'],result)

class V7ScalarMath(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();paths=[ROOT/'gen'/(prefix+stem+'.gendsp') for stem in SOURCE_NAMES.values() for prefix in ('','v7_')]
        paths+=list((ROOT/'gen').glob('v7_mass_*.gendsp'))+[ROOT/'gen'/(x+'.gendsp') for x in ('v7_balance','v7_dynamics','v7_clip_counter')]
        cls.lib=compile_library(paths,Path(cls.tmp.name))
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_source_bypass_null_all_five(self):
        for profile,stem in SOURCE_NAMES.items():
            params=dict(rpm=4800,throttle=.6,load=.6,engine_running=1,combustion_gain=1,shift_cut=1)
            a=Kernel(self.lib,stem,**params);b=Kernel(self.lib,'v7_'+stem,**params,v7_enable=0)
            x=a.render(.8);y=b.render(.8);self.assertLess(np.max(np.abs(x-y)),1e-9,profile)
    def test_sources_finite_across_rates_and_states(self):
        for sr in (44100,48000,96000):
            for profile,stem in SOURCE_NAMES.items():
                k=Kernel(self.lib,'v7_'+stem,sr,**defaults(profile),rpm=7800,load=1,throttle=1,engine_running=1,combustion_gain=1,shift_cut=1)
                a=k.render(.4);self.assertTrue(np.isfinite(a).all(),(profile,sr));self.assertGreater(np.max(abs(a[:,:2])),1e-6)
                k.set(engine_running=0,combustion_gain=0,throttle=0,load=0);b=k.render(.4);self.assertTrue(np.isfinite(b).all())
    def test_brightness_db_endpoints_and_flat_identity(self):
        sr=48000;n=sr;t=np.arange(n)/sr;inp=np.column_stack([.1*np.sin(2*np.pi*8000*t)]*2)
        base=dict(v7_enable=1,v7_body_db=0,v7_cavity_db=0,v7_mechanical_db=0,v7_brightness_db=0)
        k=Kernel(self.lib,'v7_balance',**base);a=k.render(input=inp)
        self.assertLess(np.max(abs(a[:,:2]-inp)),1e-9)
        k.set(v7_brightness_db=6);b=k.render(input=inp)
        diff=20*np.log10(rms(b[sr//2:,:2])/rms(inp[sr//2:]));self.assertAlmostEqual(diff,6,delta=.1)
        k.set(v7_brightness_db=-12);c=k.render(input=inp)
        diff=20*np.log10(rms(c[sr//2:,:2])/rms(inp[sr//2:]));self.assertAlmostEqual(diff,-12,delta=.15)
    def test_low_bed_stays_low_at_high_rpm(self):
        for p in PROFILES:
            k=Kernel(self.lib,'v7_mass_'+p,**defaults(p),engine_running=1,throttle=.7,load=.7,powertrain_level_db=0)
            k.set(rpm=2000);a=k.render(1.5)[-48000:,0];k.set(rpm=8000);b=k.render(1.5)[-48000:,0]
            def power(x,lo,hi):
                fft=np.fft.rfft(x);f=np.fft.rfftfreq(len(x),1/48000);return np.sum(abs(fft[(f>=lo)&(f<hi)])**2)
            self.assertLess(abs(10*np.log10(power(b,20,120)/power(a,20,120))),1,p)
            self.assertLess(power(b,250,6000)/power(b,20,250),.01,p)
            k.set(v7_sub_db=-60,v7_foundation_db=-60);z=k.render(1.5);self.assertLess(np.max(abs(z[-24000:,0])),1e-9)
    def test_filter_extreme_stability_all_rates(self):
        rng=np.random.default_rng(7)
        for sr in (44100,48000,96000):
            for value in (-12,6):
                k=Kernel(self.lib,'v7_balance',sr,v7_body_db=value,v7_cavity_db=value,v7_mechanical_db=value,v7_brightness_db=value)
                x=rng.normal(0,.03,(sr//2,2));y=k.render(input=x);self.assertTrue(np.isfinite(y).all());self.assertLess(np.max(abs(y[:,:2])),2)
    def test_compressor_units_stereo_link_and_knee(self):
        sr=48000;t=np.arange(sr*2)/sr
        x=.5*np.sin(2*np.pi*1000*t);inp=np.column_stack((x,x*.1))
        k=Kernel(self.lib,'v7_dynamics',v7_comp_threshold_db=-18,v7_comp_ratio=2,v7_output_trim_db=0)
        y=k.render(input=inp);a=inp[-sr:];b=y[-sr:,:2]
        level=20*np.log10(rms(a[:,0]));expected=(level+18)/2
        gr=20*np.log10(rms(a[:,0])/rms(b[:,0]));self.assertAlmostEqual(gr,expected,delta=.1)
        self.assertLess(np.max(abs(b[:,1]-.1*b[:,0])),1e-10)
        self.assertAlmostEqual(float(np.mean(y[-sr:,2])),gr,delta=.1)
    def test_emergency_guard_counter(self):
        k=Kernel(self.lib,'v7_clip_counter');x=np.ones((100,2))*2;y=k.render(input=x)
        self.assertLessEqual(np.max(y[:,:2]),.891);self.assertEqual(y[-1,2],100)

if __name__=='__main__':unittest.main()

class V7BindingAndContracts(unittest.TestCase):
    def test_all_v7_gen_parameters_exposed_and_finite_bounded(self):
        import re
        for f in (ROOT/'gen').glob('v7_*.gendsp'):
            p=json.loads(f.read_text())['patcher'];text='\n'.join(x['box'].get('code','') for x in p['boxes'])
            exposed={b['box']['text'].split()[1]:b['box']['text'] for b in p['boxes'] if b['box'].get('text','').startswith('param ')}
            for name,args in re.findall(r'\bParam (\w+)\(([^;]+)\);',text):
                self.assertIn(name,exposed,(f.name,name));self.assertIn('@min',exposed[name]);self.assertIn('@max',exposed[name])
    def test_binding_is_complete_dry_run_and_never_writes_local(self):
        from tools.v7_bind_profile import publish
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'assets/v7').mkdir(parents=True);(root/'presets/local').mkdir(parents=True)
            for name in ('state_owners.json','parameter_contracts.json'):shutil.copy(ROOT/'assets/v7'/name,root/'assets/v7'/name)
            owners=json.loads((root/'assets/v7/state_owners.json').read_text())['ioniq6n']
            for name in owners:
                d={'pattrstorage':{'name':'test','slots':{'1':{'data':{'knob':[.5]}}}}}
                if name=='ioniq6n_profile.json':d=json.loads((ROOT/'presets/v7_factories'/name).read_text())
                (root/'presets/local'/('v7_'+name)).write_text(json.dumps(d))
            before={f.name:f.read_bytes() for f in (root/'presets/local').iterdir()}
            report=publish(root,'ioniq6n');self.assertEqual(report['count'],8);self.assertFalse((root/'presets/v7_bindings').exists())
            publish(root,'ioniq6n',True)
            self.assertEqual(len(list((root/'presets/v7_bindings').glob('*.json'))),9)
            self.assertEqual(before,{f.name:f.read_bytes() for f in (root/'presets/local').iterdir()})
            (root/'presets/local'/('v7_'+owners[-1])).unlink()
            with self.assertRaisesRegex(ValueError,'Incomplete engine save'):publish(root,'ioniq6n',True)
    def test_binding_rejects_cross_profile_and_private_paths(self):
        from tools.v7_bind_profile import validate_values
        with self.assertRaises(ValueError):validate_values({'sample':'/Users/local/private.wav'})
        with self.assertRaises(ValueError):validate_values({'bad':float('nan')})
    def test_top_level_v7_local_bpatchers_are_all_versioned(self):
        for f in (ROOT/'patchers').glob('v7_*.maxpat'):
            for e in json.loads(f.read_text())['patcher']['boxes']:
                b=e['box'];name=b.get('name','').split('/')[-1]
                if b['maxclass']=='bpatcher' and (ROOT/'patchers'/name).is_file():self.assertTrue(name.startswith('v7_'),(f.name,name))

    def test_project_declares_gen_in_code_category(self):
        contents=json.loads((ROOT/'EV-Engine-V7.maxproj').read_text())['contents']
        for rel,meta in contents['patchers'].items():self.assertTrue(rel.endswith('.maxpat'),rel)
        for f in (ROOT/'gen').glob('v7_*.gendsp'):
            rel=str(f.relative_to(ROOT));self.assertEqual(contents['code'][rel]['kind'],'gendsp')
        for category in contents.values():
            for rel in category:self.assertTrue((ROOT/rel).is_file(),rel)
