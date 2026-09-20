#!/usr/bin/env python3
"""Generate only Ferrari V5 integration outputs; preserve old seed/state."""
from pathlib import Path
import subprocess

try:
    from . import build_project as b, ferrari_sf90_v5 as v5
except ImportError:
    import build_project as b
    import ferrari_sf90_v5 as v5


def outputs():
    result = dict(v5.outputs())
    result["VehicleSoundSynth-V6.maxproj"] = b.project_file()
    result["patchers/vehicle_engine_ferrari~.maxpat"] = b.make_profile_engine("ferrari")
    result["gen/ferrari_dna_source_v5.gendsp"] = b.make_gen(
        b.GEN_CODE["ferrari_dna_source_v5"])
    return result


def main():
    root = Path(__file__).resolve().parents[1]
    branch = subprocess.check_output(
        ["git", "branch", "--show-current"], cwd=root, text=True).strip()
    if branch != "codex/v6-ferrari-sf90-v5":
        raise SystemExit("Ferrari V5 installer requires codex/v6-ferrari-sf90-v5")
    docs = outputs()
    for name, doc in docs.items():
        path = root / name
        if name == v5.SEED and path.exists():
            print("Preserve seed:", name)
            continue
        b.write_json(path, doc)
        print(name)


if __name__ == "__main__":
    main()
