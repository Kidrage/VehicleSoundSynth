#!/usr/bin/env python3
"""Isolated, monitor-muted BEAP probe. Never auto-closes Max windows."""
import argparse
import copy
import shutil
from pathlib import Path
try:
    from . import build_project as b
except ImportError:
    import build_project as b

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target',type=Path)
    parser.add_argument('--state-only',action='store_true')
    args=parser.parse_args()
    target=args.target.resolve()
    root=Path(__file__).resolve().parents[1]
    if target==root or root in target.parents or target in root.parents:
        parser.error('Use a separate QA directory')
    target.mkdir(parents=True,exist_ok=True)
    (target/'presets/local').mkdir(parents=True,exist_ok=True)
    designer=copy.deepcopy(b.make_sound_dna('ioniq6n',version=2))
    b.write_json(target/'presets/ioniq6n_sound_dna_v2_factory.json',b.ioniq_dna_v2.factory(designer))
    shutil.copyfile(root/'code/ioniq_dna_v2_state.js',target/'ioniq_dna_v2_state.js')
    for item in designer['patcher']['boxes']:
        box=item['box']
        if box.get('text')=='ioniq6n_powertrain_v2~':
            box['text']='p qa_powertrain'
            box['patcher']=b.make_ioniq6n_powertrain(version=2)['patcher']
            for node in box['patcher']['boxes']:
                if node['box'].get('text','').startswith('gen~ '):
                    node['box']['text']=f'gen~ @gen "{root/"gen/ioniq6n_powertrain_v2.gendsp"}"'
        if box.get('text','').startswith('js Patcher:/code/ioniq_dna_v2_state.js'):
            box['text']=f'js "{target/"ioniq_dna_v2_state.js"}"'
            box['varname']='qa_state'
    # Keep an actual file-backed Designer so this.patcher.filepath has the
    # same persistence semantics as the shipped abstraction, not an inline p.
    b.write_json(target/'patchers/ioniq6n_sound_dna_v2~.maxpat',designer)
    p=b.Patcher(1400,800)
    voice=p.add('bpatcher',None,20,100,240,100,name=str(target/'patchers/ioniq6n_sound_dna_v2~.maxpat'),varname='qa_voice',numoutlets=2)
    load=p.new('loadbang',20,20,80)
    recorder=p.new('sfrecord~ 2',300,100,120,numinlets=3)
    dac=p.new('dac~',500,100,70,numinlets=2,numoutlets=0)
    p.connect(voice,recorder,0,0); p.connect(voice,recorder,1,1)
    def at(ms,text,destination):
        delay=p.new(f'delay {ms}',20,200+len(p.boxes)*5,100,numinlets=2)
        message=p.message(text,140,200+len(p.boxes)*5,1000)
        p.connect(load,delay); p.connect(delay,message); p.connect(message,destination)
    at(100,f'open "{target/"beap.wav"}"',recorder)
    at(300,'; dsp setdriver "Core Audio"',dac)
    at(1000,'1',dac)
    at(2000,'1',recorder)
    scenarios=[]
    base=dict(b.IONIQ6N_DNA_DEFAULTS,accel_orders=0,rpm=4000,throttle=.8,load=.8,accel=0,engine_running=1)
    for key in b.IONIQ6N_DNA_DEFAULTS:
        for value in (0,1):
            params=dict(base)
            if key=='ready_bed': params.update(rpm=650,throttle=0,load=0)
            if key=='release_mass': params.update(accel=-.8,throttle=0,load=0)
            params[key]=value
            scenarios.append({'macro':key,'value':value,'params':params})
    for value in (0,.3,1):
        scenarios.append({'macro':'accel_orders','value':value,'params':dict(base,accel=1,throttle=1,load=1,accel_orders=value)})
    if args.state_only:
        scenarios=[]
    for i,scenario in enumerate(scenarios):
        at(2000+i*2500,', '.join(f'{k} {v}' for k,v in scenario['params'].items()),voice)
    end=2000+len(scenarios)*2500
    at(end,'0',recorder)
    at(end+500,'0',dac)
    state_probe=p.new(f'js "{root/"tools/ioniq_detail_state_probe.js"}" "{target/"state-report.json"}"',800,100,500)
    at(end+1500,'bang',state_probe)
    console=p.new('console',700,100,90,numoutlets=3)
    at(end+3000,f'write "{target/"runtime.console.txt"}"',console)
    b.write_json(target/'scenarios.json',{'interval_seconds':2.5,'scenarios':scenarios})
    b.write_json(target/'runtime.maxpat',p.document())
    print(target/'runtime.maxpat')

if __name__=='__main__':
    main()
