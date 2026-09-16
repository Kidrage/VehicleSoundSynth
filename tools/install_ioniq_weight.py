#!/usr/bin/env python3
"""Generate only IONIQ weight resources; never overwrite designer/local state."""
from pathlib import Path
import subprocess
try:
    from . import build_project as b, ioniq_weight_balance as w
except ImportError:
    import build_project as b, ioniq_weight_balance as w


def outputs():
    result=w.outputs()
    result['VehicleSoundSynth-V6.maxproj']=b.project_file()
    result['patchers/vehicle_engine_ioniq6n~.maxpat']=b.make_profile_engine('ioniq6n')
    result['gen/ioniq6n_powertrain_v4.gendsp']=b.make_gen(b.GEN_CODE['ioniq6n_powertrain_v4'])
    result['gen/ioniq6n_weight_bed.gendsp']=b.make_gen(b.GEN_CODE['ioniq6n_weight_bed'],input_count=2)
    return result


def main():
    root=Path(__file__).resolve().parents[1]
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip()
    if branch!='codex/v6-ioniq-dna-accel-detail':raise SystemExit('Wrong branch; pre-generated download needs no rebuild.')
    docs=outputs()
    for name,doc in docs.items():
        if name in w.SEEDS and (root/name).exists():print('Preserve seed:',name)
        else:b.write_json(root/name,doc);print(name)


if __name__=='__main__':main()
