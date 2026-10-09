"""R2 controls/save inspection; equation and VM checks are NOT native Max tests."""
import json, subprocess, tempfile, unittest, shutil, hashlib
from pathlib import Path
import numpy as np
from tools.build_v7 import ROOT, SOURCE_NAMES
from tools.v7.schema import PROFILES, defaults
from tools.v7.scalar_harness import Kernel, compile_library
from tools.v7.review import LAB_PARAMS, BANDS
from tests.test_v7 import node, patch, rms

class V7R2GraphAndState(unittest.TestCase):
    def test_strict_state_migration_backup_and_owner_receipts(self):
        result=node((ROOT/'tools/v7/test_state_r2_vm.js').read_text())
        self.assertTrue(result['pass']);self.assertGreaterEqual(result['checks'],70)
    def test_native_names_match_contract_and_are_not_guesses(self):
        contracts=json.loads((ROOT/'assets/v7/state_contracts.json').read_text())
        storage_names=set()
        for p in (ROOT/'patchers').glob('v7_*.maxpat'):
            for e in json.loads(p.read_text())['patcher']['boxes']:
                text=e['box'].get('text','')
                if text.startswith('pattrstorage '):storage_names.add(text.split()[1])
        for profile,owners in contracts.items():
            resolved={n.replace('#1',profile) for n in storage_names}
            for c in owners[1:]:self.assertIn(c['storage'],resolved,(profile,c))
    def test_six_tabs_and_lab_controls(self):
        console=patch('patchers/v7_runtime_console.maxpat')
        tab=next(e['box'] for e in console['boxes'] if e['box']['maxclass']=='tab')
        self.assertEqual(len(tab['tabs']),6)
        p=patch('patchers/v7_lab_console.maxpat');by={e['box']['id']:e['box'] for e in p['boxes']}
        for name in LAB_PARAMS:
            self.assertIn(name,by);self.assertTrue(by[name]['annotation'])
        for key,*_ in BANDS:self.assertEqual(by[key]['ignoreclick'],1)
    def test_speed_reaches_only_audio_receivers_and_meter_is_read_only(self):
        for profile in PROFILES:
            p=patch(f'patchers/v7_vehicle_engine_{profile}~.maxpat')
            lines=[x['patchline'] for x in p['lines']]
            dst={l['destination'][0] for l in lines if l['source'][0]=='v7-speed-route'}
            self.assertEqual(dst,{'v7-mass','v7-balance'})
            for l in lines:
                if l['source'][0]=='v7-meter':self.assertTrue(l['destination'][0].startswith('v7-meter-'))
    def test_command_state_primes_before_native_saves(self):
        for profile in PROFILES:
            p=patch(f'patchers/v7_profile_runtime_host_{profile}.maxpat');by={e['box']['id']:e['box'] for e in p['boxes']};lines=[l['patchline'] for l in p['lines']]
            nodes=[b for b in by.values() if b['id'].startswith('v7-command-order')]
            self.assertGreaterEqual(len(nodes),2)
            for b in nodes:
                self.assertEqual(b['text'],'t l l')
                self.assertTrue(any(l['source']==[b['id'],1] and l['destination']==['v7-state',0] for l in lines))
    def test_engine_specific_storage_identity_rejected_by_publisher(self):
        from tools.v7_bind_profile import collect
        with tempfile.TemporaryDirectory() as tmp:
            r=Path(tmp);(r/'assets/v7').mkdir(parents=True);(r/'presets/local').mkdir(parents=True)
            for f in ('state_owners.json','state_contracts.json','parameter_contracts.json'):shutil.copy(ROOT/'assets/v7'/f,r/'assets/v7'/f)
            cs=json.loads((r/'assets/v7/state_contracts.json').read_text())['ev']
            for c in cs:
                d=json.loads((ROOT/'presets/v7_factories/ev_profile.json').read_text()) if c['storage'] is None else {'pattrstorage':{'name':c['storage'],'slots':{'1':{'data':{'x':[.5]}}}}}
                (r/'presets/local'/('v7_'+c['file'])).write_text(json.dumps(d))
            self.assertEqual(len(collect(r,'ev')),8)
            p=r/'presets/local'/('v7_'+cs[5]['file']);d=json.loads(p.read_text());d['pattrstorage']['name']='ferrari_sound_dna_v5';p.write_text(json.dumps(d))
            with self.assertRaisesRegex(ValueError,'Wrong engine/owner'):collect(r,'ev')
    def test_drive_strategy_hysteresis_does_not_filter_telemetry(self):
        out=node("""const {DriveModel}=require('./code/v7_drive_model.js');let m=new DriveModel('ioniq6n');m.running=1;m.startElapsed=1;let result=[];for(let t of [.17,.14,.09,.07,.1,.15,.17]){m.manualThrottle=t;m.tick(.02);result.push([m.v7State,m.throttle]);}console.log(JSON.stringify(result));""")
        self.assertEqual([x[0] for x in out],['drive','drive','drive','coast','coast','coast','drive'])
        self.assertEqual([x[1] for x in out],[.17,.14,.09,.07,.1,.15,.17])
    def test_brake_hysteresis(self):
        out=node("""const {DriveModel}=require('./code/v7_drive_model.js');let m=new DriveModel('v10');m.running=1;m.startElapsed=1;let a=[];for(let b of [.07,.04,.025,.015,.04]){m.manualBrake=b;m.tick(.02);a.push(m.v7State);}console.log(JSON.stringify(a));""")
        self.assertEqual(out,['brake','brake','brake','coast','coast'])
    def test_no_shift_when_engine_off(self):
        out=node("""const {DriveModel}=require('./code/v7_drive_model.js');let a=[];for(let p of ['v10','v12','ioniq6n','ferrari']){let m=new DriveModel(p);m.gear=5;m.rpm=800;m.maybeShift([]);a.push(m.gear);}console.log(JSON.stringify(a));""")
        self.assertEqual(out,[5]*4)

class V7R2Equations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();work=Path(cls.tmp.name);paths=[ROOT/'gen'/('v7_'+stem+'.gendsp') for stem in SOURCE_NAMES.values()]+list((ROOT/'gen').glob('v7_mass_*.gendsp'))+[ROOT/'gen'/(n+'.gendsp') for n in ('v7_balance','v7_meter')]
        for profile,stem in SOURCE_NAMES.items():
            d=json.loads((ROOT/'gen'/('v7_'+stem+'.gendsp')).read_text());cb=next(e['box'] for e in d['patcher']['boxes'] if 'code' in e['box'])
            a,b=('h2','h3_l') if profile=='ev' else ('order2','order3') if profile=='ioniq6n' else ('v3_h2','v3_h3')
            cb['code']+=f'\nout7={a};out8={b};out9=v7_lenv;out10='+('sf_effort' if profile=='ferrari' else 'v7_tenv')+';\n'
            f=work/('probe_'+profile+'.gendsp');f.write_text(json.dumps(d));paths.append(f)
        cls.lib=compile_library(paths,work)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def test_partial_endpoint_gain_all_five(self):
        for p in PROFILES:
            args={**defaults(p),'engine_running':1,'combustion_gain':1,'throttle':.6,'load':.6,'rpm':4000}
            a=Kernel(self.lib,'probe_'+p,**args).render(1.5)
            for param,ch in [('v7_order2_db',6),('v7_order3_db',7)]:
                b=Kernel(self.lib,'probe_'+p,**{**args,param:-12}).render(1.5)
                db=20*np.log10(rms(b[-24000:,ch])/rms(a[-24000:,ch]))
                self.assertAlmostEqual(db,-12,delta=.02,msg=p+param)
                self.assertGreater(rms(a[-24000:,:4]-b[-24000:,:4]),1e-6,p)
    def test_ferrari_actual_effort_respects_attack(self):
        for tau in (10,65,180):
            k=Kernel(self.lib,'probe_ferrari',**{**defaults('ferrari'),'v7_attack_ms':tau},engine_running=1,combustion_gain=1,rpm=4000)
            k.render(1);k.set(throttle=1,load=1);x=k.render(tau*.001)
            self.assertAlmostEqual(float(x[-1,9]),1-np.exp(-1),delta=.002)
    def test_negative_ice_load_is_not_positive_throttle(self):
        for p in ('v10','v12','ferrari'):
            k=Kernel(self.lib,'probe_'+p,**defaults(p),load=-1,throttle=0,engine_running=1,combustion_gain=1,rpm=4000)
            self.assertLess(abs(k.render(1)[-1,8]),1e-9,p)
    def test_speed_mass_endpoint_all_five(self):
        for p in PROFILES:
            args={**defaults(p),'speed_kph':180,'engine_running':1,'throttle':.7,'load':.7,'rpm':7800,'powertrain_level_db':0}
            a=Kernel(self.lib,'v7_mass_'+p,**args).render(6)[-24000:,0]
            b=Kernel(self.lib,'v7_mass_'+p,**{**args,'v7_speed_weight_db':6}).render(6)[-24000:,0]
            self.assertAlmostEqual(20*np.log10(rms(b)/rms(a)),6,delta=.02,msg=p)
    def test_speed_controls_are_neutral_below_60(self):
        a=Kernel(self.lib,'v7_mass_ev',speed_kph=40,engine_running=1).render(1)
        b=Kernel(self.lib,'v7_mass_ev',speed_kph=40,engine_running=1,v7_speed_weight_db=6).render(1)
        self.assertLess(np.max(abs(a-b)),1e-12)
    def test_speed_edge_high_frequency_cut_and_low_frequency_retention(self):
        for hz,expected in ((8000,-6),(80,0)):
            t=np.arange(48000*6)/48000;inp=np.column_stack([.1*np.cos(2*np.pi*hz*t)]*2)
            k=Kernel(self.lib,'v7_balance',speed_kph=180,v7_speed_edge_db=-6,v7_cavity_db=0)
            out=k.render(input=inp)
            self.assertAlmostEqual(20*np.log10(rms(out[-24000:,:2])/rms(inp[-24000:])),expected,delta=.1)
    def test_monitor_center_calibration_and_silence(self):
        z=Kernel(self.lib,'v7_meter').render(input=np.zeros((100,2)))
        self.assertTrue(np.all(z[:,:4]==-120))
        for ch,(_,hz,*_) in enumerate(BANDS):
            t=np.arange(96000)/48000;inp=np.column_stack([.1*np.cos(2*np.pi*hz*t)]*2)
            y=Kernel(self.lib,'v7_meter').render(input=inp)
            self.assertAlmostEqual(float(np.mean(y[-24000:,ch])),-23.0103,delta=.04)
    def test_renderer_telemetry_is_actual_ioniq_root(self):
        for rpm in (1450,4000,7800):
            k=Kernel(self.lib,'v7_ioniq6n_powertrain_v4',**defaults('ioniq6n'),rpm=rpm,throttle=.7,load=.7,engine_running=1)
            y=k.render(2);render=float(y[-1,4]);root=float(y[-1,5]);d=max(rpm-2600,0);compress=.5*(d*d/3200 if d<1600 else d-800)
            self.assertAlmostEqual(render,rpm-compress*.3,delta=.1)
            self.assertAlmostEqual(root,52+.047*render,delta=.01)
