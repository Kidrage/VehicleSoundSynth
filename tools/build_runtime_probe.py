#!/usr/bin/env python3
"""Build a temporary, monitor-muted Max patch that records the V12 idle bus."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from build_project import Patcher, write_json


def make_probe(wav_output: Path) -> dict:
    p = Patcher(980, 680)
    p.comment("Automated V12 idle render; hardware monitor is multiplied by zero", 25, 15, 600)
    controller = p.new("engine_controller", 300, 290, 125, numinlets=1, numoutlets=1)
    powertrain = p.new("powertrain~", 300, 330, 95, numinlets=1, numoutlets=2)
    cabin = p.new("cabin_master~", 300, 370, 110, numinlets=3, numoutlets=2)
    mix = p.new("mix_master~", 300, 410, 100, numinlets=3, numoutlets=2)
    for controlled in (powertrain, cabin, mix):
        p.connect(controller, controlled, 0, 0)
    p.connect(powertrain, cabin, 0, 1)
    p.connect(powertrain, cabin, 1, 2)
    p.connect(cabin, mix, 0, 1)
    p.connect(cabin, mix, 1, 2)
    for index, message in enumerate(
        (
            "engine_type v12",
            "ev_weight 0.",
            "v12_weight 1.",
            "v10_weight 0.",
            "ignition 1",
            "rpm 780.",
            "throttle 0.",
            "load 0.",
            "eq_highmid 3800. -3. 1.",
            "eq_high 9000. -4.",
            "master_trim_db -7.",
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

    recorder = p.new("sfrecord~ 2", 300, 470, 90, numinlets=3, numoutlets=1)
    open_file = p.new(f"loadmess open {wav_output}", 500, 250, 380, numinlets=1, numoutlets=1)
    p.connect(open_file, recorder)
    p.connect(record_delay, record_start)
    p.connect(record_start, recorder)
    p.connect(stop_delay, record_stop)
    p.connect(record_stop, recorder)
    p.connect(mix, recorder, 0, 0)
    p.connect(mix, recorder, 1, 1)

    mute_l = p.new("*~ 0.", 300, 500, 60, numinlets=2, numoutlets=1)
    mute_r = p.new("*~ 0.", 430, 500, 60, numinlets=2, numoutlets=1)
    dac = p.add("ezdac~", None, 365, 555, 60, 45, numinlets=2, numoutlets=0)
    dsp_on = p.new("loadmess 1", 500, 555, 80, numinlets=1, numoutlets=1)
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
        default=Path("/private/tmp/VehicleSoundSynthV2_probe_bundle"),
        help="Dedicated temporary bundle directory populated with runtime dependencies",
    )
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
    wav = bundle / "v12_idle.wav"
    write_json(patch, make_probe(wav))
    print(patch)


if __name__ == "__main__":
    main()
