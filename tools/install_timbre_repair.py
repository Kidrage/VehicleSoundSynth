#!/usr/bin/env python3
"""Scoped repair generation. Never refresh existing designer seeds or local state."""
from pathlib import Path
import subprocess
try:
    from . import build_project as b, timbre_repair as repair
except ImportError:
    import build_project as b, timbre_repair as repair


def outputs():
    result=repair.outputs()
    result['VehicleSoundSynth-V6.maxproj']=b.project_file()
    for profile in ('ioniq6n','ferrari'):
        result[f'patchers/vehicle_engine_{profile}~.maxpat']=b.make_profile_engine(profile)
    for name in ('ioniq6n_powertrain_v3','ferrari_dna_source_v4'):
        result[f'gen/{name}.gendsp']=b.make_gen(b.GEN_CODE[name])
    return result


def main():
    root=Path(__file__).resolve().parents[1]
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip()
    if branch!='codex/v6-ioniq-dna-accel-detail':
        raise SystemExit('Scoped installer requires codex/v6-ioniq-dna-accel-detail; download already contains generated files.')
    documents=outputs()  # Validate dependencies before writing anything.
    for name,doc in documents.items():
        if name in repair.SEEDS and (root/name).exists():
            print('Preserve seed:',name)
            continue
        b.write_json(root/name,doc)
        print(name)


if __name__=='__main__':
    main()
