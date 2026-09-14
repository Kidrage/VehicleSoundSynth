#!/usr/bin/env python3
"""Install only scoped generated outputs into the explicit V3 candidate branch.

Never run the full generator over the user's working project. Seed-once V3
designers are written only when absent; existing user-owned graphs are preserved.
"""
import argparse
import hashlib
import shutil
import subprocess
import tempfile
from pathlib import Path

try:
    from . import build_project as b
except ImportError:
    import build_project as b


def control_outputs():
    outputs = {'VehicleSoundSynth-V6.maxproj': b.project_file()}
    for profile in b.PROFILE_ORDER:
        outputs[f'patchers/profile_runtime_host_{profile}.maxpat'] = b.make_profile_runtime_host(profile)
        outputs[f'patchers/vehicle_engine_{profile}~.maxpat'] = b.make_profile_engine(profile)
    for profile in b.dna_v3.PROFILES:
        voice = 'ferrari_acoustic_v3~' if profile == 'ferrari' else profile+'_sound_dna_v3~'
        outputs[f'patchers/{voice}.maxpat'] = b.dna_v3.make_acoustic(profile)
        outputs[f'presets/{profile}_sound_dna_v3_factory.json'] = b.dna_v3.factory(profile)
        name = profile+'_dna_source_v3'
        outputs[f'gen/{name}.gendsp'] = b.make_gen(b.GEN_CODE[name])
    outputs['gen/dna_v3_output.gendsp'] = b.make_gen(b.GEN_CODE['dna_v3_output'],input_count=4)
    outputs['presets/ferrari_noise_v2_factory.json'] = b.make_vehicle_noise_factory('ferrari',version=2)
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    branch = subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip()
    if branch != 'codex/v6-control-dna-v3':
        parser.error('Installer is restricted to the isolated codex/v6-control-dna-v3 worktree')
    outputs = control_outputs()
    for profile in b.dna_v3.PROFILES:
        name = f'patchers/{profile}_dna_v3_designer~.maxpat'
        if not (root/name).exists():
            outputs[name] = b.dna_v3.make_designer(profile)
    name = 'patchers/vehicle_noise_ferrari_v2~.maxpat'
    if not (root/name).exists():
        outputs[name] = b.make_vehicle_noise('ferrari',version=2)
    with tempfile.TemporaryDirectory(prefix='vss-v3-install-') as temporary:
        stage = Path(temporary)
        for name, document in outputs.items():
            b.write_json(stage/name, document)
        for name in sorted(outputs):
            target = root/name
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(stage/name,target)
            print(hashlib.sha256(target.read_bytes()).hexdigest(),name)


if __name__ == '__main__':
    main()
