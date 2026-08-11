#!/usr/bin/env python3
"""Build a monitor-muted Max patch for EV/V12/V10 runtime renders."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from build_project import Patcher, write_json


PROFILE_SETTINGS = {
    "ev": {
        "rpm": 650.0,
        "weights": (1.0, 0.0, 0.0),
        "rumble": (0.0, 0.0, 0.0),
        "ir_mix": 0.10,
    },
    "v12": {
        "rpm": 780.0,
        "weights": (0.0, 1.0, 0.0),
        "rumble": (0.90, 0.62, 0.58),
        "ir_mix": 0.20,
    },
    "v10": {
        "rpm": 850.0,
        "weights": (0.0, 0.0, 1.0),
        "rumble": (0.92, 0.74, 0.72),
        "ir_mix": 0.18,
    },
}

DSP_SETTLE_MS = 6000


def make_probe(
    wav_output: Path,
    profile: str = "v12",
    rumble_enabled: bool = True,
    *,
    rpm: float | None = None,
    throttle: float = 0.0,
    load_value: float = 0.0,
    sweep_to_rpm: float | None = None,
    render_ms: int = 4000,
    driver_mode: str = "nonrealtime",
    start_enabled: bool = True,
    ignition_enabled: bool = True,
) -> dict:
    settings = PROFILE_SETTINGS[profile]
    ev_weight, v12_weight, v10_weight = settings["weights"]
    rumble_values = settings["rumble"] if rumble_enabled else (0.0, 0.0, 0.0)
    cabin_rumble, exhaust_boom, structure_vibration = rumble_values
    initial_rpm = settings["rpm"] if rpm is None else rpm
    p = Patcher(980, 680)
    state = "rumble" if rumble_enabled else "dry"
    p.comment(f"Automated {profile.upper()} idle {state} render; hardware monitor is multiplied by zero", 25, 15, 700)
    controller = p.new("engine_controller", 300, 290, 125, numinlets=1, numoutlets=1)
    powertrain = p.new("powertrain~", 300, 330, 95, numinlets=1, numoutlets=2)
    rumble = p.new("cabin_rumble~", 430, 330, 110, numinlets=3, numoutlets=2)
    add_l = p.new("+~", 300, 375, 40, numinlets=2, numoutlets=1)
    add_r = p.new("+~", 430, 375, 40, numinlets=2, numoutlets=1)
    cabin = p.new("cabin_master~", 300, 415, 110, numinlets=3, numoutlets=2)
    mix = p.new("mix_master~", 300, 455, 100, numinlets=3, numoutlets=2)
    for controlled in (powertrain, rumble, cabin, mix):
        p.connect(controller, controlled, 0, 0)
    p.connect(powertrain, add_l, 0, 0)
    p.connect(powertrain, rumble, 0, 1)
    p.connect(rumble, add_l, 0, 1)
    p.connect(powertrain, add_r, 1, 0)
    p.connect(powertrain, rumble, 1, 2)
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
            f"ignition {int(ignition_enabled)}",
            f"rpm {initial_rpm:g}",
            f"throttle {throttle:g}",
            f"load {load_value:g}",
            f"cabin_rumble {cabin_rumble:g}",
            f"exhaust_boom {exhaust_boom:g}",
            f"structure_vibration {structure_vibration:g}",
            f"cabin_ir_mix {settings['ir_mix']:g}",
            "eq_highmid 3800. -3. 1.",
            "eq_high 9000. -4.",
            "master_trim_db -8.",
        )
    ):
        initial = p.new(f"loadmess {message}", 25, 110 + index * 32, 245, numinlets=1, numoutlets=1)
        p.connect(initial, controller)

    load = p.new("loadbang", 500, 110, 65, numinlets=1, numoutlets=1)
    start_delay = p.new("delay 100", 500, 150, 70, numinlets=2, numoutlets=1)
    record_start = p.message("1", 590, 190, 30)
    record_stop = p.message("0", 680, 190, 30)
    p.connect(load, start_delay)
    if start_enabled:
        start = p.message("start 1", 500, 190, 55)
        p.connect(start_delay, start)
        p.connect(start, controller)

    if sweep_to_rpm is not None:
        sweep_delay = p.new(f"delay {DSP_SETTLE_MS}", 500, 230, 85, numinlets=2, numoutlets=1)
        sweep_message = p.message(
            f"{initial_rpm:g}, {sweep_to_rpm:g} {render_ms}", 500, 270, 185
        )
        sweep_line = p.new("line 0.", 500, 310, 60, numinlets=2, numoutlets=2)
        sweep_named = p.new("prepend rpm", 500, 350, 90, numinlets=1, numoutlets=1)
        p.connect(load, sweep_delay)
        p.connect(sweep_delay, sweep_message)
        p.connect(sweep_message, sweep_line)
        p.connect(sweep_line, sweep_named)
        p.connect(sweep_named, controller)

    recorder = p.new("sfrecord~ 2", 300, 515, 90, numinlets=3, numoutlets=1)
    open_file = p.message(f"open {wav_output}", 500, 250, 380)
    p.connect(open_file, recorder)
    p.connect(record_stop, recorder)
    p.connect(record_start, recorder)
    p.connect(mix, recorder, 0, 0)
    p.connect(mix, recorder, 1, 1)

    mute_l = p.new("*~ 0.", 300, 545, 60, numinlets=2, numoutlets=1)
    mute_r = p.new("*~ 0.", 430, 545, 60, numinlets=2, numoutlets=1)
    dac = p.add("ezdac~", None, 365, 600, 60, 45, numinlets=2, numoutlets=0)
    p.connect(mix, mute_l, 0, 0)
    p.connect(mix, mute_r, 1, 0)
    p.connect(mute_l, dac, 0, 0)
    p.connect(mute_r, dac, 0, 1)
    if driver_mode == "nonrealtime":
        dsp_stop_at_load = p.message(";\rdsp stop", 500, 535, 85)
        driver_delay = p.new("delay 3000", 595, 535, 75, numinlets=2, numoutlets=1)
        driver_select = p.message(";\rdsp setdriver NonRealTime", 500, 565, 165)
        sample_rate_delay = p.new("delay 1000", 500, 600, 75, numinlets=2, numoutlets=1)
        sample_rate = p.message(";\rdsp sr 48000", 500, 630, 100)
        driver_ready = p.new("delay 2000", 630, 565, 75, numinlets=2, numoutlets=1)
        start_trigger = p.new("t b b b b", 630, 600, 75, numinlets=1, numoutlets=4)
        dsp_start = p.message("1", 720, 600, 30)
        metro_start = p.message("1", 630, 635, 30)
        metro = p.new("metro 10", 670, 635, 65, numinlets=2, numoutlets=1)
        dsp_time = p.new("dsptime~", 745, 635, 70, numinlets=1, numoutlets=1)
        rendered = p.new(f"past {render_ms}", 825, 635, 85, numinlets=1, numoutlets=1)
        stop_trigger = p.new("t b b b", 825, 600, 65, numinlets=1, numoutlets=3)
        metro_stop = p.message("0", 895, 565, 30)
        dsp_stop = p.message("0", 895, 600, 30)
        p.connect(load, dsp_stop_at_load)
        p.connect(load, driver_delay)
        p.connect(driver_delay, driver_select)
        p.connect(driver_delay, sample_rate_delay)
        p.connect(sample_rate_delay, sample_rate)
        p.connect(sample_rate_delay, driver_ready)
        p.connect(driver_ready, start_trigger)
        p.connect(start_trigger, open_file, 3, 0)
        p.connect(start_trigger, record_start, 2, 0)
        p.connect(start_trigger, metro_start, 1, 0)
        p.connect(start_trigger, dsp_start, 0, 0)
        p.connect(dsp_start, dac)
        p.connect(metro_start, metro)
        p.connect(metro, dsp_time)
        p.connect(dsp_time, rendered)
        p.connect(rendered, stop_trigger)
        p.connect(stop_trigger, record_stop, 2, 0)
        p.connect(stop_trigger, metro_stop, 1, 0)
        p.connect(stop_trigger, dsp_stop, 0, 0)
        p.connect(dsp_stop, dac)
        p.connect(metro_stop, metro)
    else:
        record_delay = p.new(
            f"delay {DSP_SETTLE_MS}", 590, 150, 85,
            numinlets=2, numoutlets=1,
        )
        stop_delay = p.new(
            f"delay {DSP_SETTLE_MS + render_ms}", 680, 150, 105,
            numinlets=2, numoutlets=1,
        )
        driver_delay = p.new("delay 1500", 500, 580, 75, numinlets=2, numoutlets=1)
        driver_select = p.message(
            ";\rdsp setdriver \"Core Audio\"", 585, 580, 170
        )
        dsp_delay = p.new("delay 1500", 765, 580, 75, numinlets=2, numoutlets=1)
        dsp_on = p.message("1", 850, 580, 30)
        p.connect(load, record_delay)
        p.connect(load, stop_delay)
        p.connect(load, open_file)
        p.connect(record_delay, record_start)
        p.connect(stop_delay, record_stop)
        p.connect(load, driver_delay)
        p.connect(driver_delay, driver_select)
        p.connect(driver_delay, dsp_delay)
        p.connect(dsp_delay, dsp_on)
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
    parser.add_argument("--rpm", type=float)
    parser.add_argument("--throttle", type=float, default=0.0)
    parser.add_argument("--load", dest="load_value", type=float, default=0.0)
    parser.add_argument("--sweep-to-rpm", type=float)
    parser.add_argument("--render-ms", type=int, default=4000)
    parser.add_argument("--start", choices=("on", "off"), default="on")
    parser.add_argument("--ignition", choices=("on", "off"), default="on")
    parser.add_argument(
        "--driver", choices=("nonrealtime", "coreaudio"), default="nonrealtime"
    )
    args = parser.parse_args()
    if args.driver == "nonrealtime" and args.sweep_to_rpm is not None:
        parser.error("sweep renders currently require --driver coreaudio")
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
        if source.name.startswith("cabin_ir_"):
            shutil.copy2(source, bundle / source.name)
    if args.sweep_to_rpm is not None:
        state = "sweep"
    elif args.rpm is not None:
        state = f"rpm{args.rpm:g}"
    else:
        state = "idle"
    patch = bundle / f"runtime_probe_{args.profile}_{state}_{args.rumble}.maxpat"
    wav = bundle / f"{args.profile}_{state}_{args.rumble}.wav"
    write_json(
        patch,
        make_probe(
            wav,
            args.profile,
            args.rumble == "on",
            rpm=args.rpm,
            throttle=args.throttle,
            load_value=args.load_value,
            sweep_to_rpm=args.sweep_to_rpm,
            render_ms=args.render_ms,
            driver_mode=args.driver,
            start_enabled=args.start == "on",
            ignition_enabled=args.ignition == "on",
        ),
    )
    print(patch)


if __name__ == "__main__":
    main()
