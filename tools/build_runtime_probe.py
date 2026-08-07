#!/usr/bin/env python3
"""Build a monitor-muted Max patch for V12/V10 idle rumble A/B renders."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from build_project import Patcher, write_json


PROFILE_SETTINGS = {
    "v12": {
        "rpm": 780.0,
        "weights": (0.0, 1.0, 0.0),
        "rumble": (0.90, 0.62, 0.58),
    },
    "v10": {
        "rpm": 850.0,
        "weights": (0.0, 0.0, 1.0),
        "rumble": (0.92, 0.74, 0.72),
    },
}


def make_probe(wav_output: Path, profile: str = "v12", rumble_enabled: bool = True) -> dict:
    settings = PROFILE_SETTINGS[profile]
    ev_weight, v12_weight, v10_weight = settings["weights"]
    rumble_values = settings["rumble"] if rumble_enabled else (0.0, 0.0, 0.0)
    cabin_rumble, exhaust_boom, structure_vibration = rumble_values
    p = Patcher(980, 680)
    state = "rumble" if rumble_enabled else "dry"
    p.comment(f"Automated {profile.upper()} idle {state} render; hardware monitor is multiplied by zero", 25, 15, 700)
    controller = p.new("engine_controller", 300, 290, 125, numinlets=1, numoutlets=1)
    powertrain = p.new("powertrain~", 300, 330, 95, numinlets=1, numoutlets=2)
    rumble = p.new("cabin_rumble~", 430, 330, 110, numinlets=1, numoutlets=2)
    add_l = p.new("+~", 300, 375, 40, numinlets=2, numoutlets=1)
    add_r = p.new("+~", 430, 375, 40, numinlets=2, numoutlets=1)
    cabin = p.new("cabin_master~", 300, 415, 110, numinlets=3, numoutlets=2)
    mix = p.new("mix_master~", 300, 455, 100, numinlets=3, numoutlets=2)
    for controlled in (powertrain, rumble, cabin, mix):
        p.connect(controller, controlled, 0, 0)
    p.connect(powertrain, add_l, 0, 0)
    p.connect(rumble, add_l, 0, 1)
    p.connect(powertrain, add_r, 1, 0)
    p.connect(rumble, add_r, 1, 1)
    p.connect(add_l, cabin, 0, 1)
    p.connect(add_r, cabin, 0, 2)
    p.connect(cabin, mix, 0, 1)
    p.connect(cabin, mix, 1, 2)
    for index, message in enumerate(
        (
            f"engine_type {profile}",
            f"ev_weight {ev_weight:g}",
            f"v12_weight {v12_weight:g}",
            f"v10_weight {v10_weight:g}",
            "ignition 1",
            f"rpm {settings['rpm']:g}",
            "throttle 0.",
            "load 0.",
            f"cabin_rumble {cabin_rumble:g}",
            f"exhaust_boom {exhaust_boom:g}",
            f"structure_vibration {structure_vibration:g}",
            "eq_highmid 3800. -3. 1.",
            "eq_high 9000. -4.",
            "master_trim_db -8.",
        )
    ):
        initial = p.new(f"loadmess {message}", 25, 110 + index * 32, 245, numinlets=1, numoutlets=1)
        p.connect(initial, controller)

    load = p.new("loadbang", 500, 110, 65, numinlets=1, numoutlets=1)
    start_delay = p.new("delay 100", 500, 150, 70, numinlets=2, numoutlets=1)
    start = p.message("start 1", 500, 190, 55)
    record_delay = p.new("delay 700", 590, 150, 70, numinlets=2, numoutlets=1)
    record_start = p.message("1", 590, 190, 30)
    stop_delay = p.new("delay 4700", 680, 150, 80, numinlets=2, numoutlets=1)
    record_stop = p.message("0", 680, 190, 30)
    p.connect(load, start_delay)
    p.connect(load, record_delay)
    p.connect(load, stop_delay)
    p.connect(start_delay, start)
    p.connect(start, controller)

    recorder = p.new("sfrecord~ 2", 300, 515, 90, numinlets=3, numoutlets=1)
    open_file = p.new(f"loadmess open {wav_output}", 500, 250, 380, numinlets=1, numoutlets=1)
    p.connect(open_file, recorder)
    p.connect(record_delay, record_start)
    p.connect(record_start, recorder)
    p.connect(stop_delay, record_stop)
    p.connect(record_stop, recorder)
    p.connect(mix, recorder, 0, 0)
    p.connect(mix, recorder, 1, 1)

    mute_l = p.new("*~ 0.", 300, 545, 60, numinlets=2, numoutlets=1)
    mute_r = p.new("*~ 0.", 430, 545, 60, numinlets=2, numoutlets=1)
    dac = p.add("ezdac~", None, 365, 600, 60, 45, numinlets=2, numoutlets=0)
    dsp_on = p.new("loadmess 1", 500, 600, 80, numinlets=1, numoutlets=1)
    p.connect(mix, mute_l, 0, 0)
    p.connect(mix, mute_r, 1, 0)
    p.connect(mute_l, dac, 0, 0)
    p.connect(mute_r, dac, 0, 1)
    p.connect(dsp_on, dac)
    return p.document()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bundle-root",
        type=Path,
        default=Path("/private/tmp/VehicleSoundSynthV3_probe_bundle"),
        help="Dedicated temporary bundle directory populated with runtime dependencies",
    )
    parser.add_argument("--profile", choices=sorted(PROFILE_SETTINGS), default="v12")
    parser.add_argument("--rumble", choices=("on", "off"), default="on")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    bundle = args.bundle_root.resolve()
    media = bundle / "media"
    media.mkdir(parents=True, exist_ok=True)
    for source in (root / "patchers").glob("*.maxpat"):
        shutil.copy2(source, bundle / source.name)
    for source in (root / "gen").glob("*.gendsp"):
        shutil.copy2(source, bundle / source.name)
    for source in (root / "media").glob("*.wav"):
        shutil.copy2(source, media / source.name)
    patch = bundle / "runtime_probe.maxpat"
    wav = bundle / f"{args.profile}_idle_{args.rumble}.wav"
    write_json(patch, make_probe(wav, args.profile, args.rumble == "on"))
    print(patch)


if __name__ == "__main__":
    main()
