#!/usr/bin/env python3
"""Build a temporary, monitor-muted Max patch that records the V12 idle bus."""

from __future__ import annotations

import argparse
from pathlib import Path

from build_project import Patcher, write_json


def make_probe(wav_output: Path) -> dict:
    p = Patcher(980, 680)
    p.comment("Automated V12 idle render; hardware monitor is multiplied by zero", 25, 15, 600)
    engine = p.new("vehicle_engine~", 340, 330, 120, numinlets=1, numoutlets=2)
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
        p.connect(initial, engine)

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
    p.connect(start, engine)

    recorder = p.new("sfrecord~ 2", 340, 440, 90, numinlets=3, numoutlets=1)
    open_file = p.new(f"loadmess open {wav_output}", 500, 250, 380, numinlets=1, numoutlets=1)
    p.connect(open_file, recorder)
    p.connect(record_delay, record_start)
    p.connect(record_start, recorder)
    p.connect(stop_delay, record_stop)
    p.connect(record_stop, recorder)
    p.connect(engine, recorder, 0, 0)
    p.connect(engine, recorder, 1, 1)

    mute_l = p.new("*~ 0.", 300, 500, 60, numinlets=2, numoutlets=1)
    mute_r = p.new("*~ 0.", 430, 500, 60, numinlets=2, numoutlets=1)
    dac = p.add("ezdac~", None, 365, 555, 60, 45, numinlets=2, numoutlets=0)
    dsp_on = p.new("loadmess 1", 500, 555, 80, numinlets=1, numoutlets=1)
    p.connect(engine, mute_l, 0, 0)
    p.connect(engine, mute_r, 1, 0)
    p.connect(mute_l, dac, 0, 0)
    p.connect(mute_r, dac, 0, 1)
    p.connect(dsp_on, dac)
    return p.document()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--patch",
        type=Path,
        default=Path("/private/tmp/VehicleSoundSynthV2_probe_bundle/runtime_probe.maxpat"),
    )
    parser.add_argument(
        "--wav",
        type=Path,
        default=Path("/private/tmp/VehicleSoundSynthV2_probe_bundle/v12_idle.wav"),
    )
    args = parser.parse_args()
    write_json(args.patch, make_probe(args.wav.resolve()))
    print(args.patch.resolve())


if __name__ == "__main__":
    main()
