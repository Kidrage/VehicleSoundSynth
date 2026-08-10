#!/usr/bin/env python3
"""Build a monitor-muted Max probe for objective EQ/trim/bypass measurements."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from build_project import Patcher, write_json


def make_probe(
    wav_output: Path,
    frequency: float,
    eq_message: str,
    trim_db: float,
    bypass: int,
) -> dict:
    p = Patcher(940, 660)
    p.comment("Automated mix_master~ response probe; hardware monitor is multiplied by zero", 25, 15, 720)
    oscillator = p.new(f"cycle~ {frequency:g}", 100, 210, 105, numinlets=2, numoutlets=1)
    source = p.new("*~ 0.08", 100, 250, 65, numinlets=2, numoutlets=1)
    mix = p.new("mix_master~", 310, 310, 100, numinlets=3, numoutlets=2)
    p.connect(oscillator, source)
    p.connect(source, mix, 0, 1)
    p.connect(source, mix, 0, 2)

    for index, message in enumerate(
        (eq_message, f"master_trim_db {trim_db:g}", f"eq_bypass {bypass}")
    ):
        initial = p.new(f"loadmess {message}", 25, 70 + index * 38, 330, numinlets=1, numoutlets=1)
        p.connect(initial, mix)

    recorder = p.new("sfrecord~ 2", 310, 405, 90, numinlets=3, numoutlets=1)
    open_file = p.new(f"loadmess open {wav_output}", 430, 70, 440, numinlets=1, numoutlets=1)
    p.connect(open_file, recorder)
    p.connect(mix, recorder, 0, 0)
    p.connect(mix, recorder, 1, 1)

    load = p.new("loadbang", 430, 135, 65, numinlets=1, numoutlets=1)
    record_delay = p.new("delay 700", 430, 175, 70, numinlets=2, numoutlets=1)
    record_start = p.message("1", 430, 215, 30)
    stop_delay = p.new("delay 2700", 525, 175, 80, numinlets=2, numoutlets=1)
    record_stop = p.message("0", 525, 215, 30)
    p.connect(load, record_delay)
    p.connect(load, stop_delay)
    p.connect(record_delay, record_start)
    p.connect(record_start, recorder)
    p.connect(stop_delay, record_stop)
    p.connect(record_stop, recorder)

    mute_l = p.new("*~ 0.", 310, 465, 60, numinlets=2, numoutlets=1)
    mute_r = p.new("*~ 0.", 430, 465, 60, numinlets=2, numoutlets=1)
    dac = p.add("ezdac~", None, 370, 525, 60, 45, numinlets=2, numoutlets=0)
    dsp_on = p.new("loadmess 1", 525, 525, 80, numinlets=1, numoutlets=1)
    p.connect(mix, mute_l, 0, 0)
    p.connect(mix, mute_r, 1, 0)
    p.connect(mute_l, dac, 0, 0)
    p.connect(mute_r, dac, 0, 1)
    p.connect(dsp_on, dac)
    return p.document()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle-root", type=Path, required=True)
    parser.add_argument("--frequency", type=float, required=True)
    parser.add_argument("--eq-message", default="eq_low 90. 0.")
    parser.add_argument("--trim-db", type=float, default=-8.0)
    parser.add_argument("--bypass", type=int, choices=(0, 1), default=0)
    parser.add_argument("--output-name", default="mix_probe.wav")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    bundle = args.bundle_root.resolve()
    bundle.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / "patchers" / "mix_master~.maxpat", bundle / "mix_master~.maxpat")
    wav = bundle / args.output_name
    patch = bundle / f"mix_probe_{Path(args.output_name).stem}.maxpat"
    write_json(
        patch,
        make_probe(wav, args.frequency, args.eq_message, args.trim_db, args.bypass),
    )
    print(patch)


if __name__ == "__main__":
    main()
