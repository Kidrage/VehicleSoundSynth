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
    open_file = p.message(f"open {wav_output}", 430, 70, 440)
    p.connect(open_file, recorder)
    p.connect(mix, recorder, 0, 0)
    p.connect(mix, recorder, 1, 1)

    record_start = p.message("1", 430, 215, 30)
    record_stop = p.message("0", 525, 215, 30)
    p.connect(record_start, recorder)
    p.connect(record_stop, recorder)

    mute_l = p.new("*~ 0.", 310, 465, 60, numinlets=2, numoutlets=1)
    mute_r = p.new("*~ 0.", 430, 465, 60, numinlets=2, numoutlets=1)
    dac = p.add("ezdac~", None, 370, 525, 60, 45, numinlets=2, numoutlets=0)
    p.connect(mix, mute_l, 0, 0)
    p.connect(mix, mute_r, 1, 0)
    p.connect(mute_l, dac, 0, 0)
    p.connect(mute_r, dac, 0, 1)
    load = p.new("loadbang", 525, 525, 65, numinlets=1, numoutlets=1)
    dsp_stop_at_load = p.message(";\rdsp stop", 600, 525, 85)
    driver_delay = p.new("delay 3000", 600, 555, 75, numinlets=2, numoutlets=1)
    driver_select = p.message(";\rdsp setdriver NonRealTime", 685, 555, 165)
    sample_rate_delay = p.new("delay 1000", 600, 585, 75, numinlets=2, numoutlets=1)
    sample_rate_value = p.message(";\rdsp sr 48000", 685, 585, 110)
    driver_ready = p.new("delay 2000", 805, 555, 75, numinlets=2, numoutlets=1)
    start_trigger = p.new("t b b b b b", 805, 585, 90, numinlets=1, numoutlets=5)
    dsp_start = p.message("1", 900, 585, 30)
    metro_start = p.message("1", 805, 615, 30)
    metro = p.new("metro 10", 845, 615, 65, numinlets=2, numoutlets=1)
    current_time = p.new("dsptime~", 805, 645, 70, numinlets=1, numoutlets=1)
    baseline_time = p.new("dsptime~", 725, 645, 70, numinlets=1, numoutlets=1)
    elapsed = p.new("- 0.", 725, 615, 55, numinlets=2, numoutlets=1)
    rendered = p.new("past 2000", 635, 615, 75, numinlets=1, numoutlets=1)
    stop_trigger = p.new("t b b b", 635, 645, 65, numinlets=1, numoutlets=3)
    metro_stop = p.message("0", 595, 615, 30)
    dsp_stop = p.message("0", 595, 645, 30)
    p.connect(load, dsp_stop_at_load)
    p.connect(load, driver_delay)
    p.connect(driver_delay, driver_select)
    p.connect(driver_delay, sample_rate_delay)
    p.connect(sample_rate_delay, sample_rate_value)
    p.connect(sample_rate_delay, driver_ready)
    p.connect(driver_ready, start_trigger)
    p.connect(start_trigger, open_file, 4, 0)
    p.connect(start_trigger, record_start, 3, 0)
    p.connect(start_trigger, dsp_start, 2, 0)
    p.connect(start_trigger, baseline_time, 1, 0)
    p.connect(start_trigger, metro_start, 0, 0)
    p.connect(dsp_start, dac)
    p.connect(metro_start, metro)
    p.connect(metro, current_time)
    p.connect(current_time, elapsed, 0, 0)
    p.connect(baseline_time, elapsed, 0, 1)
    p.connect(elapsed, rendered)
    p.connect(rendered, stop_trigger)
    p.connect(stop_trigger, record_stop, 2, 0)
    p.connect(stop_trigger, metro_stop, 1, 0)
    p.connect(stop_trigger, dsp_stop, 0, 0)
    p.connect(dsp_stop, dac)
    p.connect(metro_stop, metro)
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
