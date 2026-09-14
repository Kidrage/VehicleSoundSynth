#!/usr/bin/env python3
"""Build a silent native Gen compilation/export probe in a separate QA folder."""
import argparse
from pathlib import Path
try:
    from . import build_project as b
except ImportError:
    import build_project as b

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    target = parser.parse_args().output.resolve()
    root = Path(__file__).resolve().parents[1]
    if target == root or root in target.parents or target in root.parents:
        parser.error('Use a separate temporary directory')
    target.mkdir(parents=True,exist_ok=True)
    p = b.Patcher(1250,450)
    load = p.new('loadbang',20,20,80)
    delay = p.new('delay 500',120,20,90,numinlets=2)
    p.connect(load,delay)
    for i,name in enumerate(('ioniq6n_powertrain','ioniq6n_powertrain_v2')):
        folder = target/name
        folder.mkdir(exist_ok=True)
        node = p.new(f'gen~ @gen "{root/"gen"/(name+".gendsp")}" @exportfolder "{folder}" @exportname {name}',20,100+i*120,1200,numoutlets=2)
        export = p.message('exportcode',20,65+i*120,100)
        p.connect(delay,export)
        p.connect(export,node)
    console = p.new('console',20,390,90,numoutlets=3)
    write = p.message(f'write "{target/"export.console.txt"}"',220,390,850)
    log_delay = p.new('delay 4000',120,340,100,numinlets=2)
    p.connect(load,log_delay)
    p.connect(log_delay,write)
    p.connect(write,console)
    b.write_json(target/'export.maxpat',p.document())
    print(target/'export.maxpat')

if __name__ == '__main__':
    main()
