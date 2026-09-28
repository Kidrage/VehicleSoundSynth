#!/usr/bin/env python3
"""Constrained GenExpr -> scalar C++ verification harness, NOT Cycling '74 Gen export.
It checks equations, finite output, envelopes, spectra and bypass nulls only.
It cannot certify Gen compilation, BEAP/Max scheduling, native CPU, or in-car sound.
"""
from __future__ import annotations
import ctypes,json,re,subprocess,tempfile
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
HEADER=r'''
#include <cmath>
#include <algorithm>
#include <string>
#include <map>
#include <vector>
#include <cstdint>
using std::sin;using std::cos;using std::tanh;using std::sqrt;using std::floor;using std::exp;using std::log10;using std::pow;
inline double clamp(double x,double a,double b){return std::max(a,std::min(b,x));}
inline double min(double x,double y){return std::min(x,y);}inline double max(double x,double y){return std::max(x,y);}
inline double abs(double x){return std::abs(x);}inline double wrap(double x,double l,double h){return x-floor((x-l)/(h-l))*(h-l);}
struct Base {
 double samplerate=48000; double phases[1024]={},slides[1024]={};uint32_t random=0x739c9d9;
 std::map<std::string,double*> parameters;std::map<std::string,std::pair<double,double>> limits;
 virtual ~Base(){};
 double cycle(int id,double f){double p=phases[id];phases[id]=wrap(p+f/samplerate,0.,1.);return cos(p*6.283185307179586);}
 double phasor(int id,double f){double p=phases[id];phases[id]=wrap(p+f/samplerate,0.,1.);return p;}
 double slide(int id,double x,double up,double down){double& y=slides[id];y+=(x-y)/max(x>y?up:down,1.);return y;}
 double noise(int id){random^=random<<13;random^=random>>17;random^=random<<5;return double(random)/2147483648.-1.;}
 virtual void step(const double* input,double* output)=0;
 void set(std::string key,double value){if(parameters.count(key))*parameters[key]=clamp(value,limits[key].first,limits[key].second);}
};
'''
def code_of(path:Path):
    return '\n'.join(e['box'].get('code','') for e in json.loads(path.read_text())['patcher']['boxes'])
def translate(name,code):
    code=re.sub(r'/\*.*?\*/','',code,flags=re.S);code=re.sub(r'//[^\n]*','',code)
    params=re.findall(r'\bParam\s+(\w+)\(([^;]+)\);',code)
    history=re.findall(r'\bHistory\s+(\w+)\(([^;]+)\);',code)
    code=re.sub(r'\b(?:Param|History)\s+\w+\([^;]+\);','',code)
    for fn in ('cycle','phasor','slide','noise'):
        count=[0]
        def repl(m):
            i=count[0];count[0]+=1
            if fn=='noise':return f'noise({i})'
            return f'{fn}({i},'
        if fn=='noise':code=re.sub(r'\bnoise\(\s*\)',repl,code)
        else:code=re.sub(r'\b'+fn+r'\(',repl,code)
        # cycle and phasor must not share their per-instance phase IDs.
        if fn=='phasor':code=re.sub(r'phasor\((\d+),',lambda m:f'phasor({int(m[1])+512},',code)
    assigned=set(re.findall(r'\b([A-Za-z_]\w*)\s*=(?!=)',code))
    reserved={p[0] for p in params}|{p[0] for p in history}|{'in'+str(i) for i in range(1,11)}
    locals_=assigned-reserved
    text=f'struct {name} : Base {{\n'
    for k,v in params:text+=f'double {k}={v.split(",")[0]};\n'
    for k,v in history:text+=f'double {k}={v};\n'
    text+=f'{name}(double sr) {{samplerate=sr;\n'
    for k,v in params:
        lo=re.search(r'min\s*=\s*([-+.\d]+)',v);hi=re.search(r'max\s*=\s*([-+.\d]+)',v)
        text+=f'parameters["{k}"]=&{k};limits["{k}"]={{{lo[1] if lo else "-1e12"},{hi[1] if hi else "1e12"}}};\n'
    text+='}\nvoid step(const double* input,double* output) override {\n'
    for i in range(1,11):text+=f'double in{i}=input[{i-1}];\n'
    for k in sorted(locals_):text+=f'double {k}=0;\n'
    text+=code+'\n'
    for i in range(10):text+=f'output[{i}]='+('out'+str(i+1) if 'out'+str(i+1) in assigned else '0')+';\n'
    return text+'}\n};\n'

def compile_library(paths,work:Path):
    work.mkdir(parents=True,exist_ok=True);text=HEADER;names=[]
    for n,p in enumerate(paths):
        name='Kernel'+str(n);text+=translate(name,code_of(p));names.append((p.stem,name))
    text+='extern "C" {\nvoid* create_kernel(const char* name,double sr){std::string s(name);\n'
    for key,cl in names:text+=f'if(s=="{key}")return new {cl}(sr);\n'
    text+='return nullptr;}\nvoid free_kernel(void* p){delete static_cast<Base*>(p);}\nvoid set_kernel(void* p,const char* name,double v){static_cast<Base*>(p)->set(name,v);}\n'
    text+='void render_kernel(void* ptr,int n,const double* input,double* output){auto p=static_cast<Base*>(ptr);for(int i=0;i<n;i++)p->step(input+i*10,output+i*10);}\n}\n'
    cpp=work/'scalar.cpp';cpp.write_text(text)
    subprocess.run(['g++','-std=c++17','-O2','-shared','-fPIC',str(cpp),'-o',str(work/'scalar.so')],check=True,capture_output=True)
    lib=ctypes.CDLL(str(work/'scalar.so'))
    lib.create_kernel.argtypes=[ctypes.c_char_p,ctypes.c_double];lib.create_kernel.restype=ctypes.c_void_p
    lib.free_kernel.argtypes=[ctypes.c_void_p]
    lib.set_kernel.argtypes=[ctypes.c_void_p,ctypes.c_char_p,ctypes.c_double]
    arr=np.ctypeslib.ndpointer(dtype=np.float64,ndim=2,flags='C_CONTIGUOUS')
    lib.render_kernel.argtypes=[ctypes.c_void_p,ctypes.c_int,arr,arr]
    return lib
class Kernel:
    def __init__(self,lib,name,sr=48000,**params):
        self.lib=lib;self.sr=sr;self.ptr=lib.create_kernel(name.encode(),sr)
        if not self.ptr:raise ValueError(name)
        self.set(**params)
    def set(self,**params):
        for k,v in params.items():self.lib.set_kernel(self.ptr,k.encode(),float(v))
    def render(self,seconds=None,input=None):
        if input is None:input=np.zeros((round(seconds*self.sr),10))
        else:
            input=np.asarray(input,dtype=np.float64)
            if input.shape[1]!=10:input=np.pad(input,((0,0),(0,10-input.shape[1])))
            input=np.ascontiguousarray(input)
        out=np.zeros_like(input);self.lib.render_kernel(self.ptr,len(out),input,out);return out
    def close(self):
        if self.ptr:self.lib.free_kernel(self.ptr);self.ptr=None
    def __del__(self):self.close()
