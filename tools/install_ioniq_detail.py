#!/usr/bin/env python3
"""Install IONIQ-only generated detail assets; preserve existing Designer seeds."""
import subprocess
from pathlib import Path
try:
    from . import build_project as b
except ImportError:
    import build_project as b


def outputs():
    designer = b.make_sound_dna('ioniq6n',version=2)
    return {
        'VehicleSoundSynth-V6.maxproj':b.project_file(),
        'patchers/vehicle_engine_ioniq6n~.maxpat':b.make_profile_engine('ioniq6n'),
        'patchers/ioniq6n_sound_dna_v2~.maxpat':designer,
        'patchers/ioniq6n_powertrain_v2~.maxpat':b.make_ioniq6n_powertrain(version=2),
        'gen/ioniq6n_powertrain_v2.gendsp':b.make_gen(b.GEN_CODE['ioniq6n_powertrain_v2']),
        'presets/ioniq6n_sound_dna_v2_factory.json':b.ioniq_dna_v2.factory(designer),
    }


def main():
    root = Path(__file__).resolve().parents[1]
    branch = subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip()
    if branch != 'codex/v6-ioniq-dna-accel-detail':
        raise SystemExit('Only the isolated IONIQ detail branch is allowed')
    for name, document in outputs().items():
        if name == 'patchers/ioniq6n_sound_dna_v2~.maxpat' and (root/name).exists():
            continue
        b.write_json(root/name,document)
        print(name)


if __name__ == '__main__':
    main()
