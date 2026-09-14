#!/usr/bin/env python3
"""Actual Max-exported source checks; NOT a full BEAP/listening certification."""
import argparse
import json
import subprocess
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('export_root',type=Path)
    root = parser.parse_args().export_root.resolve()
    binaries = {}
    for name in ('ioniq6n_powertrain','ioniq6n_powertrain_v2'):
        folder = root/name
        objects = []
        for name_c in ('json','json_builder'):
            obj = folder/(name_c+'.o')
            subprocess.run(['clang','-O2','-c',str(folder/'gen_dsp'/(name_c+'.c')),'-o',str(obj)],check=True)
            objects.append(str(obj))
        binary = folder/'runner'
        subprocess.run(['clang++','-std=c++17','-O2',f'-DGEN_HEADER="{name}.h"',f'-DGEN_NAMESPACE={name}',
            '-I'+str(folder),'-I'+str(folder/'gen_dsp'),str(ROOT/'tools/native_gen_runner.cpp'),
            str(folder/(name+'.cpp')),str(folder/'gen_dsp/genlib.cpp'),*objects,'-o',str(binary)],check=True)
        binaries[name] = binary
    checks, audit = [], []
    serial = 0
    def render(sr,params,new=True):
        nonlocal serial
        serial += 1
        dest = root/f'detail_{serial:03d}.f64'
        name = 'ioniq6n_powertrain'+('_v2' if new else '')
        subprocess.run([str(binaries[name]),str(sr),'3',str(dest),*(f'{k}={v}' for k,v in params.items())],check=True,capture_output=True)
        return np.fromfile(dest,dtype=np.float64).reshape(-1,2)
    def check(name,passed,value):
        checks.append({'name':name,'pass':bool(passed),'value':value})
    def rms(x): return float(np.sqrt(np.mean(x*x)))
    defaults = {'motor_order':.72,'body_pressure':.86,'cavity_structure':.78,'mechanical_texture':.58,
        'hf_edge':.34,'load_depth':.82,'release_mass':.68,'ready_bed':.42,'stereo_width':.62,'saturation':.24}
    for sr in (44100,48000):
        for rpm in (650,1200,2000,4000,6500,8000):
            params = dict(rpm=rpm,throttle=1,load=1,accel=1,engine_running=1)
            old = render(sr,params,new=False)
            zero = render(sr,dict(params,accel_orders=0))
            check(f'{sr}/{rpm}/zero-null',np.array_equal(old,zero),float(np.max(abs(old-zero))))
            new = render(sr,params)
            check(f'{sr}/{rpm}/headroom',abs(new).max()<1,float(abs(new).max()))
            if rpm<=1200:
                check(f'{sr}/{rpm}/idle-null',np.array_equal(old,new),float(np.max(abs(old-new))))
            else:
                a,b = old[sr:],new[sr:]
                difference = rms(a/rms(a)-b/rms(b))
                check(f'{sr}/{rpm}/not-gain-only',difference>0.005,difference)
            mid = new[sr:].mean(axis=1)
            fold = 20*np.log10(rms(new[sr:])/rms(mid))
            check(f'{sr}/{rpm}/mono-fold',fold<=3,float(fold))
        for key in ('accel','throttle','load'):
            params = dict(rpm=4000,throttle=1,load=1,accel=1,engine_running=1)
            params[key] = 0
            old,new = render(sr,params,False),render(sr,params)
            check(f'{sr}/{key}/no-enhancement',np.array_equal(old,new),float(np.max(abs(old-new))))
        for key in defaults:
            params = dict(rpm=4000,throttle=.8,load=.8,accel=0,engine_running=1,accel_orders=0)
            if key=='ready_bed': params.update(rpm=650,throttle=0,load=0)
            if key=='release_mass': params.update(accel=-.8,throttle=0,load=0)
            low = render(sr,dict(params,**{key:0}))[sr:]
            high = render(sr,dict(params,**{key:1}))[sr:]
            delta = rms(high-low)/max(rms(low),1e-12)
            audit.append({'sr':sr,'macro':key,'relative_difference':delta,'scope':'source before BEAP'})
            check(f'{sr}/{key}/connected',delta>1e-5,delta)
    report = {'scope':'Actual Max-exported Gen only. BEAP filtering/persistence/listening require separate native acceptance.',
        'checks':checks,'macro_audit':audit,'failures':[x['name'] for x in checks if not x['pass']]}
    (root/'native_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'checks':len(checks),'failures':report['failures'],'report':str(root/'native_report.json')}))
    return bool(report['failures'])

if __name__=='__main__':
    raise SystemExit(main())
