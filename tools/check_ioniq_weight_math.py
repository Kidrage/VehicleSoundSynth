#!/usr/bin/env python3
"""SOURCE-only numerical/FFT proxy. NOT native Max, BEAP or listening evidence.

Uses the existing explicitly independent scalar GenExpr model. No Max code,
reference audio, vendor export or simulated WAV is presented as native output.
Requires NumPy and a C++ compiler. Generates CSV/JSON, never writes the repo.
"""
from pathlib import Path
import argparse
import csv
import json
import subprocess
import tempfile
import numpy as np
try:
    from . import build_project as b
    from .check_timbre_repair_math import SUPPORT,translate
except ImportError:
    import build_project as b
    from check_timbre_repair_math import SUPPORT,translate

MAIN=r'''
#include <cstdlib>
int main(int argc,char**v){
 if(argc!=8)return 2;
 int sr=atoi(v[1]);double r=atof(v[2]),effort=atof(v[3]);int mode=atoi(v[4]);
 double balance=atof(v[5]),running=atof(v[6]);int scenario=atoi(v[7]);
 Old old;New now;Bed bed;
 old.samplerate=now.samplerate=bed.samplerate=sr;
 old.rpm=now.rpm=bed.rpm=r;
 old.throttle=now.throttle=effort;old.load=now.load=effort;
 old.engine_running=now.engine_running=running;bed.in1=running*5;
 now.weight_balance=bed.weight_balance=balance;
 bed.mode=mode;bed.in2=.12+.88*effort;
 if(scenario==4){now.foundation=bed.foundation=1;now.body_pressure=now.cavity_structure=1;}
 for(int s=0;s<3*sr;s++){
   if(scenario==1 && s==2*sr){old.engine_running=now.engine_running=0;bed.in1=0;}
   if(scenario==2 && s==2*sr){old.throttle=now.throttle=0;old.load=now.load=0;bed.in2=.12;old.accel=now.accel=-.8;}
   if(scenario==3){double rr=650+7350*double(s)/(3*sr);old.rpm=now.rpm=bed.rpm=rr;}
   auto a=old.step(),c=now.step(),d=bed.step();
   double row[7]={a[0],a[1],c[0],c[1],c[2],c[3],d[0]};
   fwrite(row,sizeof(double),7,stdout);
 }
}
'''


def power(x,sr,lo,hi):
    x=np.asarray(x);spec=np.fft.rfft(x*np.hanning(len(x)))
    f=np.fft.rfftfreq(len(x),1/sr);p=abs(spec)**2
    return float(p[(f>=lo)&(f<hi)].sum())


def rms(x):return float(np.sqrt(np.mean(np.asarray(x)**2)))


def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    sc='Param in1(0, min=0, max=5);\nParam in2(0, min=0, max=1);\n'+b.GEN_CODE['ioniq6n_weight_bed']
    program=SUPPORT+translate('Old',b.GEN_CODE['ioniq6n_powertrain_v3'])+translate('New',b.GEN_CODE['ioniq6n_powertrain_v4'])+translate('Bed',sc)+MAIN
    rows=[];failures=[];wave_checks=[]
    with tempfile.TemporaryDirectory(prefix='ioniq-weight-math-') as td:
        p=Path(td);(p/'main.cpp').write_text(program)
        cp=subprocess.run(['c++','-O2','-std=c++17',str(p/'main.cpp'),'-o',str(p/'check')],capture_output=True,text=True)
        if cp.returncode:raise RuntimeError(cp.stderr[-12000:])
        def render(sr,rpm,effort,mode=1,balance=1,run=1,scenario=0):
            raw=subprocess.check_output([str(p/'check'),*[str(v) for v in (sr,rpm,effort,mode,balance,run,scenario)]])
            a=np.frombuffer(raw,dtype=np.float64).reshape(-1,7)
            if not np.isfinite(a).all():raise AssertionError('Nonfinite scalar source')
            return a
        for sr in (44100,48000):
            for rpm in (650,1450,2800,4000,6000,8000,10000):
                for effort in (.2,1.):
                    a=render(sr,rpm,effort);ss=a[-sr:];old=rms(ss[:,0]);new=rms(ss[:,2]);bed=rms(ss[:,4]+ss[:,5]);scbed=rms(ss[:,6]);peak=float(abs(a[:,2:]).max())
                    if peak>=.95:failures.append(['source_peak',sr,rpm,effort,peak])
                    idle_delta=float(abs(a[:,:2]-a[:,2:4]).max()) if rpm<=1450 else None
                    if rpm<=1450 and (idle_delta!=0 or np.any(a[:,4:])):failures.append(['idle',sr,rpm])
                    root=b.timbre_repair.acoustic_rpm(rpm)*.047+52
                    before=power(ss[:,0],sr,root-2,root+2);after=power(ss[:,2],sr,root-2,root+2)
                    reduction=10*np.log10(max(after,1e-30)/max(before,1e-30))
                    if rpm>=2800 and reduction> -5:failures.append(['root_not_reduced',sr,rpm,float(reduction)])
                    foundation_fraction=power(ss[:,4]+ss[:,5],sr,120,600)/max(power(ss[:,4]+ss[:,5],sr,20,20000),1e-30)
                    sc_fraction=power(ss[:,6],sr,120,600)/max(power(ss[:,6],sr,20,20000),1e-30)
                    if rpm>=2800 and (foundation_fraction<.65 or sc_fraction<.60):failures.append(['insufficient_lowmid',sr,rpm])
                    rows.append(dict(sample_rate=sr,rpm=rpm,effort=effort,core_rms_before=old,core_rms_after=new,
                        foundation_rms=bed,soundscape_foundation_rms=scbed,root_change_db=float(reduction),
                        dna_foundation_120_600_fraction=foundation_fraction,sc_foundation_120_600_fraction=sc_fraction,
                        source_peak=peak,idle_max_abs=idle_delta))
            for mode in range(3):
                for rpm in (2800,8000):
                    a=render(sr,rpm,.7,mode=mode)
                    wave_checks.append(dict(kind='sc_mode',sample_rate=sr,rpm=rpm,mode=mode,rms=rms(a[-sr:,6])))
            for mode in range(3):
                extremes=render(sr,10000,1,mode=mode,scenario=4)
                peak=float(abs(extremes[:,2:]).max())
                wave_checks.append(dict(kind='full_foundation',sample_rate=sr,mode=mode,peak=peak))
                if peak>=.95:failures.append(['max_foundation_peak',sr,mode,peak])
            for scenario in (0,1,2,3):
                a=render(sr,8000,.8,balance=0,scenario=scenario)
                error=float(abs(a[:,:2]-a[:,2:4]).max())
                if error!=0 or np.any(a[:,4:]):failures.append(['bypass',sr,scenario,error])
                wave_checks.append(dict(kind='bypass',sample_rate=sr,scenario=scenario,max_abs=error))
            off=render(sr,8000,1,scenario=1)
            tail=float(abs(off[-int(.1*sr):,2:]).max())
            if tail>2e-4:failures.append(['shutdown',sr,tail])
            wave_checks.append(dict(kind='shutdown',sample_rate=sr,tail_peak=tail))
            silent=render(sr,8000,1,run=0)
            if np.any(silent[:,2:]):failures.append(['off_start',sr])
    for sr in (44100,48000):
        for effort in (.2,1.):
            lo=next(r for r in rows if (r['sample_rate'],r['rpm'],r['effort'])==(sr,2800,effort))
            hi=next(r for r in rows if (r['sample_rate'],r['rpm'],r['effort'])==(sr,8000,effort))
            for field in ('foundation_rms','soundscape_foundation_rms'):
                delta=float(20*np.log10(hi[field]/lo[field]))
                wave_checks.append(dict(kind='high_rpm_retention',sample_rate=sr,effort=effort,stem=field,change_db=delta))
                if delta < -3:failures.append(['weight_lost',sr,effort,field,delta])
    with (output/'source_metrics.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    report=dict(kind='independent scalar SOURCE/FFT proxy; NOT Max/BEAP runtime',steady_cases=len(rows),
        supplementary_checks=wave_checks,failures=failures,max_source_peak=max(r['source_peak'] for r in rows),
        native_max_tested=False,full_mix_tested=False,listening_tested=False)
    (output/'source_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='supplementary_checks'},indent=2))
    if failures:raise SystemExit(1)
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('output',type=Path);run(p.parse_args().output)
