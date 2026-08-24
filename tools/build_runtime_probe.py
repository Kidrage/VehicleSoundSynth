#!/usr/bin/env python3
"""Build a monitor-muted Max patch for EV/V12/V10 runtime renders."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
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
        "rpm": 740.0,
        "weights": (0.0, 0.0, 1.0),
        "rumble": (0.92, 0.74, 0.72),
        "ir_mix": 0.18,
    },
}

DSP_SETTLE_MS = 6000

SCENARIOS = {
    "idle-v12": {"profile": "v12", "rpm": 780.0},
    "idle-v10": {"profile": "v10", "rpm": 740.0},
    "high-v12-3500": {"profile": "v12", "rpm": 3500.0, "throttle": 0.72, "load": 0.65, "lock_rpm": True},
    "high-v10-4200": {"profile": "v10", "rpm": 4200.0, "throttle": 0.78, "load": 0.70, "lock_rpm": True},
    "ev-soundscape-on": {
        "profile": "ev", "rpm": 1800.0, "throttle": 0.35,
        "soundscape_enable": 1, "soundscape_level_db": -3.0,
    },
    "ev-soundscape-off": {
        "profile": "ev", "rpm": 1800.0, "throttle": 0.35,
        "soundscape_enable": 0,
    },
    "ev-soundscape-solo": {
        "profile": "ev", "rpm": 1800.0, "throttle": 0.35,
        "soundscape_enable": 1, "soundscape_level_db": -3.0,
        "soundscape_solo": 1,
    },
    "v10-soundscape-on": {
        "profile": "v10", "rpm": 1800.0, "throttle": 0.35, "lock_rpm": True,
        "soundscape_level_db": -8.0, "soundscape_enable": 1,
    },
    "v10-soundscape-off": {
        "profile": "v10", "rpm": 1800.0, "throttle": 0.35, "lock_rpm": True,
        "soundscape_enable": 0,
    },
    "v12-soundscape-on": {
        "profile": "v12", "rpm": 1800.0, "throttle": 0.35, "lock_rpm": True,
        "soundscape_level_db": -9.0, "soundscape_enable": 1,
    },
    "v12-soundscape-off": {
        "profile": "v12", "rpm": 1800.0, "throttle": 0.35, "lock_rpm": True,
        "soundscape_enable": 0,
    },
    "shift-up": {"profile": "v12", "rpm": 3200.0, "event": "shift_dir 1, shift 1"},
    "shift-down": {"profile": "v10", "rpm": 2800.0, "event": "shift_dir -1, shift 1"},
    "intake-backfire": {
        "profile": "v10", "rpm": 3600.0, "lock_rpm": True,
        "event": "intake_backfire 1",
    },
    "exhaust-pop": {
        "profile": "v12", "rpm": 3300.0, "lock_rpm": True,
        "event": "exhaust_pop 1",
    },
    "v10-backfire-running": {
        "profile": "v10", "rpm": 3600.0, "lock_rpm": True,
        "event": "exhaust_pop 1",
    },
    "v10-backfire-ignition-off": {
        "profile": "v10", "rpm": 3600.0, "lock_rpm": True,
        "event": "exhaust_pop 1", "ignition_enabled": False,
    },
    "v12-backfire-running": {
        "profile": "v12", "rpm": 3300.0, "lock_rpm": True,
        "event": "exhaust_pop 1",
    },
    "v12-backfire-ignition-off": {
        "profile": "v12", "rpm": 3300.0, "lock_rpm": True,
        "event": "exhaust_pop 1", "ignition_enabled": False,
    },
    "v10-lifecycle-idle": {
        "profile": "v10", "rpm": 740.0, "throttle": 0.08, "load": 0.15,
        "lock_rpm": True, "lifecycle_role": "idle", "extra_messages": ("accel 0",),
    },
    "v10-lifecycle-acceleration": {
        "profile": "v10", "rpm": 740.0, "sweep_to_rpm": 3420.0,
        "throttle": 0.82, "load": 0.76, "lifecycle_role": "acceleration",
        "extra_messages": ("accel 0.82",),
    },
    "v10-lifecycle-loaded-hold": {
        "profile": "v10", "rpm": 3420.0, "throttle": 0.68, "load": 0.84,
        "lock_rpm": True, "lifecycle_role": "loaded_hold", "extra_messages": ("accel 0",),
    },
    "v10-lifecycle-shift-recovery": {
        "profile": "v10", "rpm": 2000.0, "sweep_to_rpm": 1260.0,
        "throttle": 0.42, "load": 0.52, "lifecycle_role": "shift_recovery",
        "extra_messages": ("accel -0.58",), "event": "shift_dir -1, shift 1",
    },
    "v10-lifecycle-deceleration": {
        "profile": "v10", "rpm": 2000.0, "sweep_to_rpm": 1260.0,
        "throttle": 0.10, "load": 0.18, "lifecycle_role": "deceleration",
        "extra_messages": ("accel -0.82",),
    },
    "v10-lifecycle-drive": {
        "profile": "v10", "drive_lifecycle": True,
        "extra_messages": ("auto 1",),
    },
}


def actual_drive_trace(model_path: Path, profile: str, render_ms: int) -> dict:
    """Run the exact JS drivetrain used by Max and return its emitted state trace."""
    script = r"""
const fs = require("fs");
const modelPath = process.argv[1];
const profile = process.argv[2];
const renderMs = Number(process.argv[3]);
const {DriveModel} = require(modelPath);
const model = new DriveModel(profile);
const commands = [["ignition", 1], ["start", 1], ["auto", 1]];
const commandEvents = [];
for (const [name, value] of commands) {
  for (const event of model.handle(name, [value])) commandEvents.push({time: model.time, message: event});
}
const snapshots = [];
const events = commandEvents.slice();
for (let index = 0; index < Math.round(renderMs / 20); index += 1) {
  const emitted = model.tick(0.02);
  for (const message of emitted) {
    if (message[0] === "shift" || message[0] === "shift_dir" || message[0] === "gear") {
      events.push({time: model.time, message});
    }
  }
  snapshots.push(model.snapshot());
}
process.stdout.write(JSON.stringify({profile, render_ms: renderMs, step_ms: 20, commands, events, snapshots}));
"""
    result = subprocess.run(
        ["node", "-e", script, str(model_path), profile, str(render_ms)],
        check=True,
        capture_output=True,
        text=True,
    )
    trace = json.loads(result.stdout)
    trace.update({
        "schema_version": 1,
        "drive_model_path": "code/drive_model.js",
        "drive_model_sha256": hashlib.sha256(model_path.read_bytes()).hexdigest(),
    })
    return trace


def make_probe(
    wav_output: Path,
    profile: str = "v12",
    rumble_enabled: bool = True,
    *,
    rpm: float | None = None,
    throttle: float = 0.0,
    load_value: float = 0.0,
    lock_rpm: bool = False,
    sweep_to_rpm: float | None = None,
    render_ms: int = 4000,
    driver_mode: str = "nonrealtime",
    start_enabled: bool = True,
    ignition_enabled: bool = True,
    tap: str = "final",
    extra_messages: tuple[str, ...] = (),
    event_message: str | None = None,
    drive_lifecycle: bool = False,
) -> dict:
    settings = PROFILE_SETTINGS[profile]
    rumble_values = settings["rumble"] if rumble_enabled else (0.0, 0.0, 0.0)
    cabin_rumble, exhaust_boom, structure_vibration = rumble_values
    initial_rpm = settings["rpm"] if rpm is None else rpm
    p = Patcher(980, 680)
    state = "rumble" if rumble_enabled else "dry"
    p.comment(f"Automated {profile.upper()} idle {state} render; hardware monitor is multiplied by zero", 25, 15, 700)
    p.comment("Runtime acceptance requires the written WAV to report exactly 48000 Hz; any other rate is a hard failure", 25, 42, 820)
    drive = p.new(f"drive_simulator_{profile}", 100, 290, 165, numinlets=1, numoutlets=1)
    controller = p.new(f"engine_controller_{profile}", 300, 290, 165, numinlets=1, numoutlets=1)
    drive_router = p.new("route rpm", 100, 320, 75, numinlets=1, numoutlets=2)
    rpm_select = p.new("switch 2", 190, 290, 70, numinlets=3, numoutlets=1)
    rpm_select_default = p.new("loadmess 1", 190, 260, 80, numinlets=1, numoutlets=1)
    rpm_named = p.new("prepend rpm", 190, 320, 90, numinlets=1, numoutlets=1)
    powertrain = p.new(f"{profile}_powertrain~", 300, 330, 135, numinlets=1, numoutlets=2)
    soundscape = p.new(
        f"{profile}_cinematic_soundscape_host~", 445, 330, 205,
        numinlets=1, numoutlets=2,
    )
    transient = p.new(f"transient_{profile}~", 160, 330, 125, numinlets=1, numoutlets=2)
    road = p.new("road_air~", 70, 330, 85, numinlets=1, numoutlets=2)
    rumble = p.new("cabin_rumble~", 430, 330, 110, numinlets=3, numoutlets=2)
    add_l = p.new("+~", 300, 375, 40, numinlets=2, numoutlets=1)
    add_r = p.new("+~", 430, 375, 40, numinlets=2, numoutlets=1)
    cabin = p.new("cabin_master~", 300, 415, 110, numinlets=3, numoutlets=2)
    mix = p.new("mix_master~", 300, 455, 100, numinlets=3, numoutlets=2)
    p.connect(drive, drive_router)
    p.connect(drive_router, rpm_select, 0, 1)
    p.connect(drive_router, controller, 1, 0)
    p.connect(rpm_select_default, rpm_select, 0, 0)
    p.connect(rpm_select, rpm_named)
    p.connect(rpm_named, controller)
    for controlled in (powertrain, transient, road, rumble, cabin, mix):
        p.connect(controller, controlled, 0, 0)
    p.connect(controller, soundscape, 0, 0)
    solo_router = p.new("route soundscape_solo pad_solo", 660, 300, 210, numinlets=1, numoutlets=3)
    solo_clip = p.new("clip 0 1", 660, 335, 65, numinlets=3, numoutlets=1)
    solo_gain = p.new("expr 1-$i1", 735, 335, 80, numinlets=1, numoutlets=1)
    solo_pack = p.new("pack 0. 35", 825, 335, 80, numinlets=2, numoutlets=1)
    solo_line = p.new("line~", 915, 335, 50, numinlets=2, numoutlets=2)
    solo_default = p.new("loadmess 0", 660, 370, 80, numinlets=1, numoutlets=1)
    core_l = p.new("*~", 300, 345, 40, numinlets=2, numoutlets=1)
    core_r = p.new("*~", 430, 345, 40, numinlets=2, numoutlets=1)
    p.connect(controller, solo_router)
    p.connect(solo_router, solo_clip, 0)
    p.connect(solo_router, solo_clip, 1)
    p.connect(solo_default, solo_clip)
    p.connect(solo_clip, solo_gain)
    p.connect(solo_gain, solo_pack)
    p.connect(solo_pack, solo_line)
    p.connect(powertrain, core_l, 0, 0)
    p.connect(powertrain, core_r, 1, 0)
    p.connect(solo_line, core_l, 0, 1)
    p.connect(solo_line, core_r, 0, 1)
    p.connect(core_l, add_l, 0, 0)
    p.connect(transient, add_l, 0, 1)
    p.connect(powertrain, rumble, 0, 1)
    road_l = p.new("+~", 250, 395, 40, numinlets=2, numoutlets=1)
    sum_l = p.new("+~", 300, 420, 40, numinlets=2, numoutlets=1)
    pad_sum_l = p.new("+~", 205, 375, 40, numinlets=2, numoutlets=1)
    p.connect(add_l, pad_sum_l, 0, 0)
    p.connect(soundscape, pad_sum_l, 0, 1)
    engine_l = pad_sum_l
    p.connect(engine_l, road_l, 0, 0)
    p.connect(road, road_l, 0, 1)
    p.connect(road_l, sum_l, 0, 0)
    p.connect(rumble, sum_l, 0, 1)
    p.connect(core_r, add_r, 0, 0)
    p.connect(transient, add_r, 1, 1)
    p.connect(powertrain, rumble, 1, 2)
    road_r = p.new("+~", 480, 395, 40, numinlets=2, numoutlets=1)
    sum_r = p.new("+~", 430, 420, 40, numinlets=2, numoutlets=1)
    pad_sum_r = p.new("+~", 525, 375, 40, numinlets=2, numoutlets=1)
    p.connect(add_r, pad_sum_r, 0, 0)
    p.connect(soundscape, pad_sum_r, 1, 1)
    engine_r = pad_sum_r
    p.connect(engine_r, road_r, 0, 0)
    p.connect(road, road_r, 1, 1)
    p.connect(road_r, sum_r, 0, 0)
    p.connect(rumble, sum_r, 1, 1)
    p.connect(sum_l, cabin, 0, 1)
    p.connect(sum_r, cabin, 0, 2)
    p.connect(cabin, mix, 0, 1)
    p.connect(cabin, mix, 1, 2)
    default_messages = (
            f"ignition {int(ignition_enabled)}",
            f"rpm {initial_rpm:g}",
            f"throttle {throttle:g}",
            f"load {load_value:g}",
            "accel 0",
            f"cabin_rumble {cabin_rumble:g}",
            f"exhaust_boom {exhaust_boom:g}",
            f"structure_vibration {structure_vibration:g}",
            f"cabin_ir_mix {settings['ir_mix']:g}",
            "eq_highmid 3800. -3. 1.",
            "eq_high 9000. -4.",
        "master_trim_db -8.",
    )
    default_messages += ("soundscape_enable 0",)
    if drive_lifecycle:
        default_messages = (
            "ignition 0", "auto 1",
            f"cabin_rumble {cabin_rumble:g}",
            f"exhaust_boom {exhaust_boom:g}",
            f"structure_vibration {structure_vibration:g}",
            f"cabin_ir_mix {settings['ir_mix']:g}",
            "eq_highmid 3800. -3. 1.", "eq_high 9000. -4.",
            "master_trim_db -8.",
        )
    overridden = {message.split(maxsplit=1)[0] for message in extra_messages}
    control_messages = tuple(
        message for message in default_messages
        if message.split(maxsplit=1)[0] not in overridden
    ) + extra_messages
    for index, message in enumerate(control_messages):
        initial = p.new(f"loadmess {message}", 25, 110 + index * 32, 245, numinlets=1, numoutlets=1)
        p.connect(initial, drive)

    load = p.new("loadbang", 500, 110, 65, numinlets=1, numoutlets=1)
    start_delay = p.new("delay 100", 500, 150, 70, numinlets=2, numoutlets=1)
    record_start = p.message("1", 590, 190, 30)
    record_stop = p.message("0", 680, 190, 30)
    p.connect(load, start_delay)
    event = None
    if event_message is not None:
        event = p.message(event_message, 790, 190, 190)
        p.connect(event, drive)
        if driver_mode == "coreaudio":
            event_delay = p.new("delay 7800", 790, 150, 85, numinlets=2, numoutlets=1)
            p.connect(load, event_delay)
            p.connect(event_delay, event)
    if start_enabled and not drive_lifecycle:
        start = p.message("start 1", 500, 190, 55)
        p.connect(start_delay, start)
        p.connect(start, drive)

    sweep_order = None
    if sweep_to_rpm is not None:
        sweep_delay = p.new(f"delay {DSP_SETTLE_MS}", 500, 230, 85, numinlets=2, numoutlets=1)
        sweep_order = p.new("t b b", 590, 230, 50, numinlets=1, numoutlets=2)
        sweep_message = p.message(
            f"{initial_rpm:g}, {sweep_to_rpm:g} {render_ms}", 500, 270, 185
        )
        sweep_line = p.new("line 0.", 500, 310, 60, numinlets=2, numoutlets=2)
        sweep_select = p.message("2", 590, 310, 30)
        if driver_mode == "coreaudio":
            p.connect(load, sweep_delay)
        p.connect(sweep_delay, sweep_order)
        p.connect(sweep_order, sweep_select, 1, 0)
        p.connect(sweep_order, sweep_message, 0, 0)
        p.connect(sweep_message, sweep_line)
        p.connect(sweep_select, rpm_select, 0, 0)
        p.connect(sweep_line, rpm_select, 0, 2)

    recorder = p.new("sfrecord~ 2", 300, 515, 90, numinlets=3, numoutlets=1)
    open_file = p.message(f"open {wav_output}", 500, 250, 380)
    p.connect(open_file, recorder)
    p.connect(record_stop, recorder)
    p.connect(record_start, recorder)
    record_left, record_right = (sum_l, sum_r) if tap == "pre-cabin" else (mix, mix)
    record_left_outlet, record_right_outlet = (0, 0) if tap == "pre-cabin" else (0, 1)
    p.connect(record_left, recorder, record_left_outlet, 0)
    p.connect(record_right, recorder, record_right_outlet, 1)

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
        sample_rate_value = p.message(";\rdsp sr 48000", 500, 630, 110)
        sample_rate_number = p.message("48000", 500, 665, 55)
        sample_rate_status = p.new("adstatus sr", 500, 700, 75, numinlets=2, numoutlets=2)
        sample_rate_override = p.new("loadmess override 1", 500, 735, 125, numinlets=1, numoutlets=1)
        driver_ready = p.new("delay 2000", 630, 565, 75, numinlets=2, numoutlets=1)
        start_trigger = p.new("t b b b b b b", 630, 600, 105, numinlets=1, numoutlets=6)
        dsp_start = p.message("1", 720, 600, 30)
        replay_messages = list(control_messages)
        if start_enabled and ignition_enabled:
            # The load-time start occurs while DSP is stopped, so signal-rate
            # line~ gates cannot advance. Reset the lifecycle lock and replay
            # the complete state only after DSP is running.
            replay_messages.extend(("ignition 0", "ignition 1", "start 1"))
        elif start_enabled:
            replay_messages.append("start 1")
        runtime_replay = p.message(", ".join(replay_messages), 720, 565, 250)
        metro_start = p.message("1", 630, 635, 30)
        metro = p.new("metro 10", 670, 635, 65, numinlets=2, numoutlets=1)
        current_time = p.new("dsptime~", 745, 635, 70, numinlets=1, numoutlets=1)
        baseline_time = p.new("dsptime~", 745, 665, 70, numinlets=1, numoutlets=1)
        elapsed = p.new("- 0.", 825, 665, 55, numinlets=2, numoutlets=1)
        rendered = p.new(f"past {render_ms}", 825, 635, 85, numinlets=1, numoutlets=1)
        stop_trigger = p.new("t b b b b", 825, 600, 75, numinlets=1, numoutlets=4)
        metro_stop = p.message("0", 895, 565, 30)
        dsp_stop = p.message("0", 895, 600, 30)
        close_delay = p.new("delay 1000", 895, 635, 75, numinlets=2, numoutlets=1)
        close_message = p.message("wclose", 895, 670, 55)
        patcher_control = p.new("thispatcher", 895, 705, 85, numinlets=1, numoutlets=2)
        eq_save = p.new("s vehicle_bus_eq.save", 805, 740, 145, numinlets=1, numoutlets=0)
        record_begin = p.new("t b b b", 610, 700, 65, numinlets=1, numoutlets=3)
        p.connect(load, dsp_stop_at_load)
        p.connect(load, driver_delay)
        p.connect(driver_delay, driver_select)
        p.connect(driver_delay, sample_rate_delay)
        p.connect(sample_rate_delay, sample_rate_value)
        p.connect(sample_rate_delay, sample_rate_number)
        p.connect(sample_rate_number, sample_rate_status, 0, 1)
        p.connect(sample_rate_override, sample_rate_status)
        p.connect(sample_rate_delay, driver_ready)
        p.connect(driver_ready, start_trigger)
        p.connect(start_trigger, open_file, 5, 0)
        p.connect(start_trigger, dsp_start, 4, 0)
        p.connect(start_trigger, runtime_replay, 3, 0)
        p.connect(runtime_replay, drive)
        if lock_rpm:
            catch_complete = p.new("delay 1000", 540, 665, 75, numinlets=2, numoutlets=1)
            lock_order = p.new("t b b b", 540, 700, 65, numinlets=1, numoutlets=3)
            lock_value = p.message(f"{initial_rpm:g}", 520, 735, 55)
            lock_select = p.message("2", 585, 735, 30)
            record_after_lock = p.new("delay 20", 675, 735, 65, numinlets=2, numoutlets=1)
            p.connect(start_trigger, catch_complete, 2, 0)
            p.connect(catch_complete, lock_order)
            p.connect(lock_order, lock_select, 2, 0)
            p.connect(lock_select, rpm_select, 0, 0)
            p.connect(lock_order, lock_value, 1, 0)
            p.connect(lock_value, rpm_select, 0, 2)
            p.connect(lock_order, record_after_lock, 0, 0)
            p.connect(record_after_lock, record_begin)
        else:
            p.connect(start_trigger, record_begin, 2, 0)
        p.connect(record_begin, record_start, 2, 0)
        p.connect(record_begin, baseline_time, 1, 0)
        p.connect(record_begin, metro_start, 0, 0)
        if sweep_order is not None:
            p.connect(record_begin, sweep_order, 0, 0)
        p.connect(dsp_start, dac)
        p.connect(metro_start, metro)
        p.connect(metro, current_time)
        p.connect(current_time, elapsed, 0, 0)
        p.connect(baseline_time, elapsed, 0, 1)
        p.connect(elapsed, rendered)
        if event is not None:
            event_at = p.new("past 1800", 825, 700, 75, numinlets=1, numoutlets=1)
            p.connect(elapsed, event_at)
            p.connect(event_at, event)
        p.connect(rendered, stop_trigger)
        p.connect(stop_trigger, record_stop, 3, 0)
        p.connect(stop_trigger, metro_stop, 2, 0)
        p.connect(stop_trigger, dsp_stop, 1, 0)
        p.connect(stop_trigger, close_delay, 0, 0)
        p.connect(stop_trigger, eq_save, 0, 0)
        p.connect(close_delay, close_message)
        p.connect(close_message, patcher_control)
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
        if drive_lifecycle:
            lifecycle_start = p.message("ignition 1, start 1, auto 1", 725, 500, 175)
            lifecycle_start_delay = p.new(
                f"delay {DSP_SETTLE_MS}", 625, 500, 85,
                numinlets=2, numoutlets=1,
            )
            p.connect(load, lifecycle_start_delay)
            p.connect(lifecycle_start_delay, lifecycle_start)
            p.connect(lifecycle_start, drive)
        if lock_rpm:
            lock_delay = p.new(
                f"delay {DSP_SETTLE_MS - 100}", 765, 545, 90,
                numinlets=2, numoutlets=1,
            )
            lock_order = p.new("t b b", 865, 545, 50, numinlets=1, numoutlets=2)
            lock_value = p.message(f"{initial_rpm:g}", 925, 530, 55)
            lock_select = p.message("2", 925, 560, 30)
            p.connect(load, lock_delay)
            p.connect(lock_delay, lock_order)
            p.connect(lock_order, lock_select, 1, 0)
            p.connect(lock_select, rpm_select, 0, 0)
            p.connect(lock_order, lock_value, 0, 0)
            p.connect(lock_value, rpm_select, 0, 2)
    return p.document()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bundle-root",
        type=Path,
        default=Path("/private/tmp/VehicleSoundSynthV4_probe_bundle"),
        help="Dedicated temporary bundle directory populated with runtime dependencies",
    )
    parser.add_argument(
        "--local-media-dir",
        type=Path,
        help="Optional local-only Ferrari media directory; defaults to media/local",
    )
    parser.add_argument("--profile", choices=sorted(PROFILE_SETTINGS), default="v12")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS))
    parser.add_argument("--tap", choices=("pre-cabin", "final"), default="final")
    parser.add_argument("--stem", choices=("powertrain", "transient", "road", "rumble"))
    parser.add_argument("--stem-db", type=float)
    parser.add_argument("--eq-message", action="append", default=[])
    parser.add_argument("--eq-bypass", choices=(0, 1), type=int)
    parser.add_argument("--master-trim-db", type=float)
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
    scenario = SCENARIOS.get(args.scenario, {})
    profile = scenario.get("profile", args.profile)
    rpm = scenario.get("rpm", args.rpm)
    throttle = scenario.get("throttle", args.throttle)
    load_value = scenario.get("load", args.load_value)
    lock_rpm = bool(scenario.get("lock_rpm", False))
    extra_messages = list(scenario.get("extra_messages", ())) + list(args.eq_message)
    for name in (
        "soundscape_enable", "soundscape_level_db", "soundscape_motion",
        "soundscape_space", "soundscape_solo",
    ):
        if name in scenario:
            extra_messages.append(f"{name} {scenario[name]:g}")
    if args.stem is not None and args.stem_db is not None:
        extra_messages.append(f"{args.stem}_level_db {args.stem_db:g}")
    if args.eq_bypass is not None:
        extra_messages.append(f"eq_bypass {args.eq_bypass}")
    if args.master_trim_db is not None:
        extra_messages.append(f"master_trim_db {args.master_trim_db:g}")
    root = Path(__file__).resolve().parents[1]
    bundle = args.bundle_root.resolve()
    media = bundle / "media"
    presets = bundle / "presets"
    media.mkdir(parents=True, exist_ok=True)
    (presets / "local").mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        root / "presets" / "vehicle_bus_eq_default.json",
        presets / "vehicle_bus_eq_default.json",
    )
    for source in (root / "patchers").glob("*.maxpat"):
        document = json.loads(source.read_text(encoding="utf-8"))
        for item in document["patcher"]["boxes"]:
            text = item["box"].get("text")
            if text:
                item["box"]["text"] = (
                    text.replace((root / "media" / "local").as_posix() + "/", "")
                    .replace((root / "media").as_posix() + "/", "")
                    .replace((root / "gen").as_posix() + "/", "")
                    .replace((root / "code").as_posix() + "/", "")
                    .replace("Patcher:/media/local/", "")
                    .replace("Patcher:/media/", "")
                    .replace("Patcher:/gen/", "")
                    .replace("Patcher:/code/", "")
                    .replace("../gen/", "")
                    .replace("../code/", "")
                    .replace("../media/local/", "")
                    .replace("../media/", "")
                    .replace("gen/", "")
                    .replace("code/", "")
                    .replace("media/local/", "")
                    .replace("media/", "")
                )
        write_json(bundle / source.name, document)
    for source in (root / "gen").glob("*.gendsp"):
        shutil.copy2(source, bundle / source.name)
    for source in (root / "code").glob("*.js"):
        shutil.copy2(source, bundle / source.name)
    runtime_media_names = {
        "cabin_ir_l.wav", "cabin_ir_r.wav", "starter_v10.wav", "starter_v12.wav",
    }
    for source in (root / "media").glob("*.wav"):
        if source.name not in runtime_media_names:
            continue
        shutil.copy2(source, media / source.name)
        # Some patchers use an explicit media/foo.wav argument while Max resolves
        # abstractions from the bundle root. Keep both layouts in the probe.
        shutil.copy2(source, bundle / source.name)
    local_media_source = (
        args.local_media_dir.resolve()
        if args.local_media_dir is not None
        else root / "media" / "local"
    )
    if local_media_source.is_dir():
        local_media_destination = media / "local"
        local_media_destination.mkdir(parents=True, exist_ok=True)
        for source in local_media_source.glob("ferrari_sf90_startup.wav"):
            shutil.copy2(source, local_media_destination / source.name)
            # Runtime probes are opened directly, without first registering the
            # generated project search path. Mirror local-only files at the
            # bundle root so bare buffer names resolve exactly like CC0 media.
            shutil.copy2(source, bundle / source.name)
    sweep_to_rpm = scenario.get("sweep_to_rpm", args.sweep_to_rpm)
    if sweep_to_rpm is not None:
        state = "sweep"
    elif args.rpm is not None:
        state = f"rpm{args.rpm:g}"
    else:
        state = "idle"
    if args.scenario is not None:
        state = args.scenario
    patch = bundle / f"runtime_probe_{profile}_{state}_{args.rumble}.maxpat"
    wav = bundle / f"{profile}_{state}_{args.rumble}_{args.tap}.wav"
    write_json(
        patch,
        make_probe(
            wav,
            profile,
            args.rumble == "on",
            rpm=rpm,
            throttle=throttle,
            load_value=load_value,
            lock_rpm=lock_rpm,
            sweep_to_rpm=sweep_to_rpm,
            render_ms=args.render_ms,
            driver_mode=args.driver,
            start_enabled=args.start == "on",
            ignition_enabled=bool(scenario.get("ignition_enabled", args.ignition == "on")),
            tap=args.tap,
            extra_messages=tuple(extra_messages),
            event_message=scenario.get("event"),
            drive_lifecycle=bool(scenario.get("drive_lifecycle", False)),
        ),
    )
    if "lifecycle_role" in scenario:
        initial_rpm = rpm if rpm is not None else PROFILE_SETTINGS[profile]["rpm"]
        end_rpm = initial_rpm
        if sweep_to_rpm is not None:
            end_rpm = sweep_to_rpm
        write_json(
            wav.with_suffix(".lifecycle.json"),
            {
                "schema_version": 1,
                "role": scenario["lifecycle_role"],
                "render_ms": args.render_ms,
                "start_rpm": initial_rpm,
                "end_rpm": end_rpm,
                "start_firing_hz": initial_rpm / 12.0,
                "end_firing_hz": end_rpm / 12.0,
                "cadence_derivative_hz_s": (
                    (end_rpm - initial_rpm) / 12.0 / max(args.render_ms / 1000.0, 1e-9)
                ),
                "event": scenario.get("event"),
            },
        )
    if scenario.get("drive_lifecycle"):
        trace = actual_drive_trace(root / "code" / "drive_model.js", profile, args.render_ms)
        trace.update({
            "probe_file": patch.name,
            "probe_sha256": hashlib.sha256(patch.read_bytes()).hexdigest(),
            "wav_file": wav.name,
        })
        write_json(
            wav.with_suffix(".drive.json"),
            trace,
        )
    project_name = bundle.name
    required_patchers = {
        patch.name,
        f"drive_simulator_{profile}.maxpat",
        f"engine_controller_{profile}.maxpat",
        f"{profile}_powertrain~.maxpat",
        f"transient_{profile}~.maxpat",
        "transient~.maxpat",
        "road_air~.maxpat",
        "cabin_rumble~.maxpat",
        "cabin_master~.maxpat",
        "mix_master~.maxpat",
        "engine_start_voice.maxpat",
        "engine_start_beap~.maxpat",
    }
    required_patchers.update({
        f"{profile}_cinematic_soundscape_host~.maxpat",
        "cinematic_soundscape_voice.maxpat",
        "cinematic_soundscape_beap~.maxpat",
    })
    if profile != "ev":
        required_patchers.update({
            f"{profile}_backfire_host~.maxpat",
            f"{profile}_backfire_beap~.maxpat",
        })
    patcher_contents = {
        path.name: {"kind": "patcher", "local": 1}
        for path in sorted(bundle.glob("*.maxpat"))
        if path.name in required_patchers
    }
    code_contents = {
        path.name: {"kind": "gendsp", "local": 1}
        for path in sorted(bundle.glob("*.gendsp"))
    }
    code_contents.update({
        path.name: {"kind": "javascript", "local": 1}
        for path in sorted(bundle.glob("*.js"))
    })
    media_contents = {
        path.relative_to(bundle).as_posix(): {"kind": "mediafile", "local": 1}
        for path in sorted(media.rglob("*.wav"))
    }
    data_contents = {
        "presets/vehicle_bus_eq_default.json": {"kind": "data", "local": 1},
    }
    write_json(
        bundle / f"{project_name}.maxproj",
        {
            "name": project_name,
            "version": 1,
            "autolocalize": 0,
            "autoorganize": 0,
            "contents": {
                "patchers": patcher_contents,
                "code": code_contents,
                "media": media_contents,
                "data": data_contents,
            },
            "searchpath": {
                "bundle": {"path": ".", "recursive": 1},
                "media": {"path": "./media", "recursive": 1},
            },
        },
    )
    print(patch)


if __name__ == "__main__":
    main()
