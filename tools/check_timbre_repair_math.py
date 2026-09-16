#!/usr/bin/env python3
"""Numerical SOURCE proxy (not native Max, not BEAP, not a listening render).

Translates this task's small GenExpr subset to scalar C++ using explicit
reference models for slide/phasor/cycle/noise. Proves algebraic bypass, finite
values, and bounded source levels across rates; does NOT certify Gen export,
Max scheduler, BEAP filters, runtime CPU, speaker response or perceived quality.
No Cycling '74 implementation code is copied. Compiler: c++ in PATH.
"""
from pathlib import Path
import argparse
import json
import re
import shutil
import subprocess
import tempfile
try:
    from . import build_project as b
except ImportError:
    import build_project as b

SUPPORT = r'''
#include <cmath>
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
using std::abs; using std::cos; using std::sin; using std::pow;
using std::sqrt; using std::exp; using std::tanh;
double max(double a,double b){return std::max(a,b);}
double min(double a,double b){return std::min(a,b);}
double clamp(double a,double l,double h){return max(l,min(a,h));}
double wrap(double a,double l,double h){return a-(h-l)*std::floor((a-l)/(h-l));}
struct Ops {
 double samplerate=48000;
 std::array<double,128> sl{}, ph{}, cy{};
 uint32_t rng=0x31415926;
 double slide(int i,double x,double u,double d){double n=x>sl[i]?u:d;sl[i]+=(x-sl[i])/max(1,n);return sl[i];}
 double phasor(int i,double hz){double y=ph[i];ph[i]=wrap(y+hz/samplerate,0,1);return y;}
 double cycle(int i,double hz){double y=sin(cy[i]*6.283185307179586);cy[i]=wrap(cy[i]+hz/samplerate,0,1);return y;}
 double noise(int){rng=rng*1664525u+1013904223u;return double(rng)/2147483648.0-1;}
};
'''


def translate(name,code):
    code=re.sub(r'//[^\n]*','',code)
    params=re.findall(r'Param\s+(\w+)\(([-+.\d]+),\s*min=[-+.\d]+,\s*max=[-+.\d]+\);',code)
    histories=re.findall(r'History\s+(\w+)\(([-+.\d]+)\);',code)
    code=re.sub(r'(?:Param|History)\s+\w+\([^;]*\);','',code)
    members={k for k,v in params+histories};assigned=set(members)
    # Expose these unused controls uniformly in the numerical harness only.
    extras={'accel','combustion_gain','reference_restore'}-members
    fields='\n'.join('double '+k+'='+v+';' for k,v in params+histories)+''.join('double '+k+'=0;' for k in sorted(extras))
    assigned |= extras
    count={k:0 for k in ('slide','phasor','cycle','noise')}
    def ops(m):
        k=m.group(1);i=count[k];count[k]+=1
        return k+'('+str(i)+(',' if k!='noise' else '')
    code=re.sub(r'\b(slide|phasor|cycle|noise)\(',ops,code)
    body=[]
    for statement in code.split(';'):
        statement=statement.strip()
        if not statement:continue
        m=re.fullmatch(r'(\w+)\s*=\s*(.*)',statement,re.S)
        if not m:raise ValueError('Unsupported expression: '+statement)
        lhs,rhs=m.groups()
        if re.search(r'[^\w\s.\d()+*/?:,<>=!\-]',rhs):raise ValueError(rhs)
        body.append(('' if lhs in assigned else 'double ')+lhs+' = '+rhs+';')
        assigned.add(lhs)
    outputs=[f'out{i}' if f'out{i}' in assigned else '0' for i in range(1,11)]
    return f'struct {name}:Ops {{\n{fields}\nstd::array<double,10> step(){{\n'+ '\n'.join(body)+'\nreturn {'+','.join(outputs)+'};\n}\n};\n'


def run(output):
    compiler=shutil.which('c++')
    if not compiler:raise RuntimeError('C++ compiler required for numerical proxy')
    pairs=[('ioniq',b.GEN_CODE['ioniq6n_powertrain_v2'],b.GEN_CODE['ioniq6n_powertrain_v3']),
           ('ferrari',b.GEN_CODE['ferrari_dna_source_v3'],b.GEN_CODE['ferrari_dna_source_v4'])]
    main=[]; program=SUPPORT
    for index,(profile,old,new) in enumerate(pairs):
        program+=translate('Old'+str(index),old)+translate('New'+str(index),new)
        for rate in (44100,48000):
            for rpm in (650 if profile=='ioniq' else 740,1450,2600,4000,6500,8000,10000):
                for effort in (0,.3,1):
                    main.append(f'''{{Old{index} a;New{index} z,n; a.samplerate=z.samplerate=n.samplerate={rate};
 a.rpm=z.rpm=n.rpm={rpm}; a.throttle=z.throttle=n.throttle={effort};a.load=z.load=n.load={effort};
 a.accel=z.accel=n.accel={effort};a.engine_running=z.engine_running=n.engine_running=1;
 a.combustion_gain=z.combustion_gain=n.combustion_gain=1;z.reference_restore=0;n.reference_restore=1;
 double diff=0,noiseDiff=0,peak=0,powA=0,powN=0,idleDiff=0;int samples=0;bool finite=true;
 for(int s=0;s<{rate}*2;s++){{auto x=a.step(),y=z.step(),v=n.step();
 for(int k=0;k<{2 if profile=='ioniq' else 4};k++){{diff=max(diff,abs(x[k]-y[k]));finite=finite && std::isfinite(v[k]);peak=max(peak,abs(v[k]));idleDiff=max(idleDiff,abs(x[k]-v[k]));
 if(s>{rate}){{powA+=x[k]*x[k];powN+=v[k]*v[k];samples++;}}}}
 for(int k=7;k<10;k++)noiseDiff=max(noiseDiff,abs(x[k]-v[k]));}}
 printf("{profile},{rate},{rpm},{effort},%.17g,%.17g,%.9g,%.9g,%.9g,%.17g,%d\\n",diff,noiseDiff,peak,sqrt(powA/max(samples,1)),sqrt(powN/max(samples,1)),idleDiff,finite);}}''')
    program+='int main(){\n'+'\n'.join(main)+'\n}\n'
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='vss-math-') as directory:
        src=Path(directory)/'proxy.cpp';src.write_text(program)
        exe=Path(directory)/'proxy'
        subprocess.run([compiler,'-O2','-std=c++17',str(src),'-o',str(exe)],check=True,capture_output=True,text=True)
        result=subprocess.check_output([str(exe)],text=True)
    header='profile,sample_rate,rpm,effort,bypass_max_abs,residual_max_abs,peak,rms_before,rms_after,restore_max_abs,finite\n'
    (output/'source_proxy.csv').write_text(header+result)
    rows=[]
    for line in result.splitlines():
        v=line.split(',');rows.append(dict(zip(header.strip().split(','),[v[0]]+[float(x) for x in v[1:]])))
    failures=[]
    for row in rows:
        if row['bypass_max_abs']!=0:failures.append(['bypass',row])
        if row['finite']!=1 or row['peak']>=.95:failures.append(['finite/headroom',row])
        if row['profile']=='ferrari' and row['residual_max_abs']!=0:failures.append(['residual',row])
        if row['profile']=='ioniq' and row['rpm']<=1450 and row['restore_max_abs']!=0:failures.append(['idle/activation',row])
    report={'kind':'scalar mathematical source proxy, NOT native Max/BEAP/export',
            'cases':len(rows),'failures':failures,'peak_max':max(x['peak'] for x in rows),
            'bypass_max_abs':max(x['bypass_max_abs'] for x in rows),
            'native_max_tested':False,'listening_tested':False}
    (output/'source_proxy_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    if failures:raise SystemExit(1)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    run(parser.parse_args().output)
