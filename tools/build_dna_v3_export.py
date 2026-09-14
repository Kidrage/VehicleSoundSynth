#!/usr/bin/env python3
"""Build a temporary Max-native Gen export/console probe, no production writes."""
import argparse
from pathlib import Path
try:
    from . import build_project as b
except ImportError:
    import build_project as b


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output',type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    target = args.output.resolve()
    if target == root or target in root.parents or root in target.parents:
        parser.error('Use a separate temporary QA directory')
    target.mkdir(parents=True,exist_ok=True)
    p = b.Patcher(1200,800)
    load = p.new('loadbang',20,20,80)
    order = p.new('t b b b b b b b', 150,20,190,numoutlets=7)
    p.connect(load,order)
    for i,name in enumerate(('ferrari_dna_source_v3','v10_dna_source_v3','v12_dna_source_v3','dna_v3_output','v10_powertrain_v2','v12_powertrain_v2')):
        folder = target/name
        folder.mkdir(exist_ok=True)
        node = p.new(f'gen~ @gen "{root / "gen" / (name+".gendsp")}" @exportfolder "{folder}" @exportname {name}',20,80+i*80,1130,numinlets=4 if name=='dna_v3_output' else 1,numoutlets=2 if name.endswith(('_v2','output')) else 10)
        export = p.message('exportcode',170,120+i*80,100)
        p.connect(order,export,6-i)
        p.connect(export,node)
    console = p.new('console',20,710,90,numoutlets=3)
    write = p.message(f'write "{target/"export.console.txt"}"',270,710,700)
    p.connect(order,write)
    p.connect(write,console)
    b.write_json(target/'export.maxpat',p.document())
    print(target/'export.maxpat')


if __name__ == '__main__':
    main()
