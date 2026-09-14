#!/usr/bin/env python3
"""Verify ACTUAL Max-exported C++, not a Python reimplementation of Gen.

Requires numpy, clang++, and a completed build_dna_v3_export.py Max export.
This proves source DSP at both sample rates; it does not certify the whole
BEAP/Max runtime, perceptual acceptance, or full-profile CPU budget.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('export_root',type=Path)
    args=parser.parse_args()
    root=args.export_root.resolve()
    results={'scope':'Max-exported source DSP only; whole-runtime/listening acceptance separate', 'checks':[], 'renders':{}}
    failures=[]
    def check(name, ok, detail):
        results['checks'].append({'name':name,'pass':bool(ok),'detail':detail})
        if not ok: failures.append(name)
    binaries={}
    names=('ferrari_dna_source_v3','v10_dna_source_v3','v12_dna_source_v3','dna_v3_output','v10_powertrain_v2','v12_powertrain_v2')
    for name in names:
        folder=root/name
        executable=folder/'qa_runner'
        c_objects=[]
        for source in ('json','json_builder'):
            obj=folder/(source+'.o')
            subprocess.run(['clang','-O2','-c',str(folder/'gen_dsp'/(source+'.c')),'-o',str(obj)],check=True)
            c_objects.append(str(obj))
        subprocess.run(['clang++','-std=c++17','-O2',f'-DGEN_HEADER="{name}.h"',f'-DGEN_NAMESPACE={name}',
                        '-I'+str(folder),'-I'+str(folder/'gen_dsp'),str(ROOT/'tools/native_gen_runner.cpp'),
                        str(folder/(name+'.cpp')),str(folder/'gen_dsp/genlib.cpp'),*c_objects,'-o',str(executable)],check=True)
        binaries[name]=executable
    serial=0
    def render(name,sr,params,seconds=2):
        nonlocal serial
        serial+=1
        destination=root/f'qa_{serial:03d}.f64'
        completed=subprocess.run([str(binaries[name]),str(sr),str(seconds),str(destination),
                                  *(f'{key}={value}' for key,value in params.items())],check=True,text=True,capture_output=True)
        meta=json.loads(completed.stdout)
        data=np.fromfile(destination,dtype=np.float64).reshape(-1,meta['channels'])
        meta.update(name=name,params=params,sha256=hashlib.sha256(destination.read_bytes()).hexdigest())
        results['renders'][destination.name]=meta
        return data,meta
    common={'engine_running':1,'combustion_gain':1,'shift_cut':1,'throttle':.7,'load':.7}
    for sr in (44100,48000):
        for profile in ('ferrari','v10','v12'):
            name=profile+'_dna_source_v3'
            for rpm in (740 if profile!='v12' else 780,2000,4000,6500,8000):
                x,meta=render(name,sr,dict(common,rpm=rpm))
                core=x[sr:,0:4]
                check(f'{profile}/{sr}/{rpm}/finite-headroom',np.isfinite(x).all() and abs(core).max()<1,float(abs(core).max()))
                check(f'{profile}/{sr}/{rpm}/four-audible-groups',np.all(np.sqrt(np.mean(core**2,axis=0))>1e-7),np.sqrt(np.mean(core**2,axis=0)).tolist())
            if profile!='ferrari':
                for rpm in (740 if profile=='v10' else 780,1200):
                    new,_=render(name,sr,dict(common,rpm=rpm))
                    old,_=render(profile+'_powertrain_v2',sr,dict(common,rpm=rpm))
                    difference=float(np.max(abs(new[:,:][:,4:6]-old)))
                    check(f'{profile}/{sr}/{rpm}/legacy-null',difference<1e-12 and np.max(abs(new[:,6]))==0,difference)
            x,_=render(name,sr,dict(common,rpm=4000),3)
            for key,channel in (('v3_aggression',0),('v3_body',1),('v3_character',2),('v3_softness',3),('v3_load_response',0)):
                ends=[]
                for value in (0,.5,1):
                    y,_=render(name,sr,dict(common,rpm=4000,**{key:value}))
                    ends.append(y[sr:,channel])
                changes=[float(np.sqrt(np.mean((ends[i+1]-ends[i])**2))) for i in range(2)]
                check(f'{profile}/{sr}/{key}/endpoints',min(changes)>1e-5,changes)
            for value in (0,1):
                y,_=render(name,sr,dict(common,rpm=4000,v3_release_mass=value,release_seconds=1),2)
                tail=float(np.sqrt(np.mean(y[int(sr*1.15):int(sr*1.30),1]**2)))
                if value==0: short_tail=tail
                else: check(f'{profile}/{sr}/release-mass',tail>short_tail,{'short':short_tail,'long':tail})
            off,_=render(name,sr,dict(common,rpm=4000,engine_running=0))
            check(f'{profile}/{sr}/lifecycle-off',float(abs(off[:,:4]).max())==0,float(abs(off[:,:4]).max()))
            swept,_=render(name,sr,dict(common,rpm=740,sweep_end=10000),3)
            check(f'{profile}/{sr}/sweep-headroom',float(abs(swept[:,:4]).max())<1,float(abs(swept[:,:4]).max()))
        for width in (0,.5,1):
            x,_=render('dna_v3_output',sr,{'v3_width':width,'test_mix_input':1})
            mid=(x[sr:,0]+x[sr:,1])/2; side=(x[sr:,0]-x[sr:,1])/2
            ratio=float(np.sum(side**2)/np.sum(mid**2))
            check(f'output/{sr}/width-{width}',ratio==0 if width==0 else ratio>0,ratio)
            if width==1: check(f'output/{sr}/mono-fold',10*np.log10(1+ratio)<=3,float(10*np.log10(1+ratio)))
    results['failures']=failures
    (root/'native_report.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'checks':len(results['checks']),'failures':failures,'report':str(root/'native_report.json')},indent=2))
    return bool(failures)


if __name__=='__main__':
    raise SystemExit(main())
