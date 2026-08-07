#!/usr/bin/env python3
"""Deterministically generate the VehicleSoundSynth Max project and media."""

from __future__ import annotations

import argparse
import json
import math
import random
import struct
import wave
from pathlib import Path
from typing import Any


APP_VERSION = {
    "major": 8,
    "minor": 6,
    "revision": 5,
    "architecture": "x64",
    "modernui": 1,
}
PROJECT_NAME = "VehicleSoundSynth-V3"
PROJECT_FILENAME = f"{PROJECT_NAME}.maxproj"

STATE_NAMES = (
    "engine_type",
    "ignition",
    "start",
    "speed_kph",
    "rpm",
    "throttle",
    "brake",
    "load",
    "accel",
    "gear",
    "shift",
    "shift_dir",
    "pop",
    "intake_backfire",
    "exhaust_pop",
    "click",
)
MACRO_NAMES = (
    "ev_weight",
    "v12_weight",
    "v10_weight",
    "aggression",
    "brightness",
    "body",
    "texture",
    "cabin_width",
    "cabin_rumble",
    "exhaust_boom",
    "structure_vibration",
    "eq_low",
    "eq_lowmid",
    "eq_highmid",
    "eq_high",
    "eq_bypass",
    "master_trim_db",
)
ALL_MESSAGES = STATE_NAMES + MACRO_NAMES

MEDIA_FRAMES = {
    "shift_thump": 9600,
    "exhaust_pop": 7200,
    "mechanical_click": 2400,
    "starter_v12": 33600,
    "starter_v10": 33600,
    **{f"shift_up_{index:02d}": 7200 for index in range(1, 4)},
    **{f"shift_down_{index:02d}": 8400 for index in range(1, 4)},
    **{f"intake_backfire_{index:02d}": 9600 for index in range(1, 4)},
    **{f"exhaust_pop_{index:02d}": 7200 for index in range(1, 5)},
    **{f"exhaust_crackle_{index:02d}": 4800 for index in range(1, 4)},
}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class Patcher:
    """Small builder that makes port counts and patch-cord references explicit."""

    def __init__(self, width: float = 1100.0, height: float = 760.0) -> None:
        self.boxes: list[dict[str, Any]] = []
        self.lines: list[dict[str, Any]] = []
        self._next_id = 1
        self.width = width
        self.height = height

    def add(
        self,
        maxclass: str,
        text: str | None,
        x: float,
        y: float,
        width: float,
        height: float = 22.0,
        *,
        numinlets: int = 1,
        numoutlets: int = 1,
        **extra: Any,
    ) -> str:
        box_id = f"obj-{self._next_id}"
        self._next_id += 1
        box: dict[str, Any] = {
            "id": box_id,
            "maxclass": maxclass,
            "numinlets": numinlets,
            "numoutlets": numoutlets,
            "patching_rect": [float(x), float(y), float(width), float(height)],
        }
        if text is not None:
            box["text"] = text
        if numoutlets:
            box["outlettype"] = [""] * numoutlets
        box.update(extra)
        self.boxes.append({"box": box})
        return box_id

    def new(
        self,
        text: str,
        x: float,
        y: float,
        width: float,
        *,
        numinlets: int = 1,
        numoutlets: int = 1,
        **extra: Any,
    ) -> str:
        return self.add(
            "newobj",
            text,
            x,
            y,
            width,
            numinlets=numinlets,
            numoutlets=numoutlets,
            **extra,
        )

    def comment(self, text: str, x: float, y: float, width: float, height: float = 22.0) -> str:
        return self.add("comment", text, x, y, width, height, numinlets=1, numoutlets=0)

    def message(self, text: str, x: float, y: float, width: float) -> str:
        return self.add("message", text, x, y, width, numinlets=2, numoutlets=1)

    def connect(self, source: str, destination: str, source_outlet: int = 0, destination_inlet: int = 0) -> None:
        self.lines.append(
            {
                "patchline": {
                    "destination": [destination, destination_inlet],
                    "source": [source, source_outlet],
                }
            }
        )

    def document(self, *, presentation: bool = False) -> dict[str, Any]:
        return {
            "patcher": {
                "appversion": APP_VERSION,
                "bglocked": 0,
                "boxes": self.boxes,
                "classnamespace": "box",
                "default_fontface": 0,
                "default_fontname": "Arial",
                "default_fontsize": 12.0,
                "enablehscroll": 1,
                "enablevscroll": 1,
                "fileversion": 1,
                "gridonopen": 1,
                "gridsize": [15.0, 15.0],
                "gridsnaponopen": 1,
                "lines": self.lines,
                "objectsnaponopen": 1,
                "openinpresentation": int(presentation),
                "rect": [50.0, 50.0, self.width, self.height],
                "toolbarvisible": 1,
            }
        }


def inlet(patch: Patcher, x: float, y: float, *, signal: bool = False) -> str:
    return patch.add(
        "inlet",
        None,
        x,
        y,
        30,
        numinlets=0,
        numoutlets=1,
        outlettype=["signal" if signal else ""],
    )


def outlet(patch: Patcher, x: float, y: float, *, signal: bool = False) -> str:
    return patch.add(
        "outlet",
        None,
        x,
        y,
        30,
        numinlets=1,
        numoutlets=0,
        comment="signal" if signal else "messages",
    )


def route(patch: Patcher, names: tuple[str, ...], x: float, y: float, width: float) -> str:
    return patch.new(
        "route " + " ".join(names),
        x,
        y,
        width,
        numinlets=1,
        numoutlets=len(names) + 1,
    )


def make_engine() -> dict[str, Any]:
    p = Patcher(1320, 760)
    p.comment("vehicle_engine~ — lifecycle-aware public seam and layered stereo renderer", 25, 15, 620)
    control = inlet(p, 45, 65)
    controller = p.new("engine_controller", 45, 105, 125, numinlets=1, numoutlets=1)
    fan = p.new("t l l l l l l l", 45, 150, 135, numinlets=1, numoutlets=7)
    contract = route(p, ALL_MESSAGES, 190, 150, 900)
    p.comment("Contract monitor: every documented state, event, macro, and mix message is accepted", 190, 185, 620)
    power = p.new("powertrain~", 95, 260, 95, numinlets=1, numoutlets=2)
    transient = p.new("transient~", 285, 260, 90, numinlets=1, numoutlets=2)
    road = p.new("road_air~", 465, 260, 85, numinlets=1, numoutlets=2)
    rumble = p.new("cabin_rumble~", 625, 260, 110, numinlets=1, numoutlets=2)
    cabin = p.new("cabin_master~", 800, 460, 110, numinlets=3, numoutlets=2)
    mix = p.new("mix_master~", 1010, 570, 100, numinlets=3, numoutlets=2)
    add_l1 = p.new("+~", 130, 350, 35, numinlets=2, numoutlets=1)
    add_l2 = p.new("+~", 235, 390, 35, numinlets=2, numoutlets=1)
    add_l3 = p.new("+~", 340, 430, 35, numinlets=2, numoutlets=1)
    add_r1 = p.new("+~", 390, 350, 35, numinlets=2, numoutlets=1)
    add_r2 = p.new("+~", 495, 390, 35, numinlets=2, numoutlets=1)
    add_r3 = p.new("+~", 600, 430, 35, numinlets=2, numoutlets=1)
    left = outlet(p, 1015, 690, signal=True)
    right = outlet(p, 1105, 690, signal=True)

    p.connect(control, controller)
    p.connect(controller, fan)
    p.connect(fan, contract, 6)
    p.connect(fan, power, 5)
    p.connect(fan, transient, 4)
    p.connect(fan, road, 3)
    p.connect(fan, rumble, 2)
    p.connect(fan, cabin, 1, 0)
    p.connect(fan, mix, 0, 0)
    p.connect(power, add_l1, 0, 0)
    p.connect(transient, add_l1, 0, 1)
    p.connect(add_l1, add_l2, 0, 0)
    p.connect(road, add_l2, 0, 1)
    p.connect(add_l2, add_l3, 0, 0)
    p.connect(rumble, add_l3, 0, 1)
    p.connect(power, add_r1, 1, 0)
    p.connect(transient, add_r1, 1, 1)
    p.connect(add_r1, add_r2, 0, 0)
    p.connect(road, add_r2, 1, 1)
    p.connect(add_r2, add_r3, 0, 0)
    p.connect(rumble, add_r3, 1, 1)
    p.connect(add_l3, cabin, 0, 1)
    p.connect(add_r3, cabin, 0, 2)
    p.connect(cabin, mix, 0, 1)
    p.connect(cabin, mix, 1, 2)
    p.connect(mix, left, 0)
    p.connect(mix, right, 1)
    return p.document()


def make_engine_controller() -> dict[str, Any]:
    p = Patcher(1160, 760)
    p.comment("Fuel lifecycle and shift-envelope controller; original messages pass through", 25, 15, 620)
    control = inlet(p, 35, 65)
    split = p.new("t l l", 35, 105, 55, numinlets=1, numoutlets=2)
    router = route(
        p,
        ("engine_type", "ignition", "start", "shift", "shift_dir", "exhaust_pop", "pop"),
        150,
        105,
        560,
    )
    output = outlet(p, 560, 690)
    p.connect(control, split)
    p.connect(split, output, 0)
    p.connect(split, router, 1)

    engine_type = p.new("sel ev v12 v10", 150, 165, 105, numinlets=1, numoutlets=4)
    fuel_off = p.message("0", 135, 205, 30)
    fuel_v12 = p.message("1", 180, 205, 30)
    fuel_v10 = p.message("1", 225, 205, 30)
    p.connect(router, engine_type, 0)
    p.connect(engine_type, fuel_off, 0)
    p.connect(engine_type, fuel_v12, 1)
    p.connect(engine_type, fuel_v10, 2)

    ignition = p.new("clip 0 1", 315, 165, 65, numinlets=3, numoutlets=1)
    ignition_off = p.new("sel 0", 315, 205, 45, numinlets=1, numoutlets=2)
    start_clip = p.new("clip 0 1", 420, 165, 65, numinlets=3, numoutlets=1)
    start_state = p.new("pack 0 0 0", 420, 245, 90, numinlets=3, numoutlets=1)
    start_valid = p.new("expr $i1*$i2*$i3", 420, 285, 130, numinlets=3, numoutlets=1)
    start_edge = p.new("sel 1", 420, 325, 45, numinlets=1, numoutlets=2)
    p.connect(router, ignition, 1)
    p.connect(ignition, ignition_off)
    p.connect(ignition, start_state, 0, 1)
    p.connect(router, start_clip, 2)
    p.connect(start_clip, start_state, 0, 0)
    p.connect(fuel_off, start_state, 0, 2)
    p.connect(fuel_v12, start_state, 0, 2)
    p.connect(fuel_v10, start_state, 0, 2)
    p.connect(start_state, start_valid)
    p.connect(start_valid, start_edge)

    start_trigger = p.new("t b b b", 420, 365, 70, numinlets=1, numoutlets=3)
    starter_on = p.message("starter 1", 350, 410, 70)
    running_off = p.message("engine_running 0", 435, 410, 105)
    combustion_off = p.message("combustion_gain 0", 560, 410, 115)
    catch_delay = p.new("delay 500", 700, 410, 70, numinlets=2, numoutlets=1)
    cancel_catch = p.message("stop", 780, 410, 45)
    catch_trigger = p.new("t b b b", 700, 450, 70, numinlets=1, numoutlets=3)
    starter_off = p.message("starter 0", 640, 495, 70)
    running_on = p.message("engine_running 1", 730, 495, 105)
    combustion_on = p.message("combustion_gain 1", 855, 495, 115)
    p.connect(start_edge, start_trigger, 0)
    p.connect(start_trigger, starter_on, 2)
    p.connect(start_trigger, running_off, 1)
    p.connect(start_trigger, combustion_off, 0)
    p.connect(start_trigger, catch_delay, 0)
    p.connect(catch_delay, catch_trigger)
    p.connect(catch_trigger, starter_off, 2)
    p.connect(catch_trigger, running_on, 1)
    p.connect(catch_trigger, combustion_on, 0)
    for item in (starter_on, running_off, combustion_off, starter_off, running_on, combustion_on):
        p.connect(item, output)

    stop_trigger = p.new("t b b b", 315, 245, 70, numinlets=1, numoutlets=3)
    p.connect(ignition_off, stop_trigger, 0)
    p.connect(ignition_off, cancel_catch, 0)
    p.connect(cancel_catch, catch_delay)
    p.connect(stop_trigger, starter_off, 2)
    p.connect(stop_trigger, running_off, 1)
    p.connect(stop_trigger, combustion_off, 0)

    shift_generic = p.new("sel 1", 35, 325, 45, numinlets=1, numoutlets=2)
    shift_direction = p.new("sel -1 1", 105, 325, 60, numinlets=1, numoutlets=3)
    cut = p.message("shift_cut 0.22", 35, 380, 95)
    recover_delay = p.new("delay 90", 145, 380, 65, numinlets=2, numoutlets=1)
    recover = p.message("shift_cut 1", 225, 380, 75)
    p.connect(router, shift_generic, 3)
    p.connect(router, shift_direction, 4)
    p.connect(shift_generic, cut, 0)
    p.connect(shift_generic, recover_delay, 0)
    for outlet_index in (0, 1):
        p.connect(shift_direction, cut, outlet_index)
        p.connect(shift_direction, recover_delay, outlet_index)
    p.connect(recover_delay, recover)
    p.connect(cut, output)
    p.connect(recover, output)

    exhaust_request = p.new("sel 1", 250, 325, 45, numinlets=1, numoutlets=2)
    pop_request = p.new("sel 1", 315, 325, 45, numinlets=1, numoutlets=2)
    exhaust_on = p.message("exhaust_pop 1", 285, 455, 95)
    exhaust_delay = p.new("delay 70", 395, 455, 65, numinlets=2, numoutlets=1)
    exhaust_off = p.message("exhaust_pop 0", 475, 455, 95)
    crackle_delay = p.new("delay 120", 585, 455, 70, numinlets=2, numoutlets=1)
    crackle_on = p.message("crackle 1", 670, 455, 70)
    crackle_off_delay = p.new("delay 170", 755, 455, 70, numinlets=2, numoutlets=1)
    crackle_off = p.message("crackle 0", 840, 455, 70)
    p.connect(router, exhaust_request, 5)
    p.connect(router, pop_request, 6)
    p.connect(shift_direction, exhaust_on, 0)
    p.connect(shift_direction, exhaust_delay, 0)
    p.connect(shift_direction, crackle_delay, 0)
    p.connect(shift_direction, crackle_off_delay, 0)
    for trigger in (exhaust_request, pop_request):
        p.connect(trigger, crackle_delay, 0)
        p.connect(trigger, crackle_off_delay, 0)
    p.connect(exhaust_delay, exhaust_off)
    p.connect(crackle_delay, crackle_on)
    p.connect(crackle_off_delay, crackle_off)
    for item in (exhaust_on, exhaust_off, crackle_on, crackle_off):
        p.connect(item, output)

    for index, text in enumerate(("combustion_gain 0", "engine_running 0", "shift_cut 1", "starter 0")):
        initial = p.new(f"loadmess {text}", 35 + index * 180, 585, 150, numinlets=1, numoutlets=1)
        p.connect(initial, output)
    return p.document()


def make_mix_master() -> dict[str, Any]:
    p = Patcher(1540, 980)
    p.comment("Four-band stereo parametric EQ, click-safe bypass, trim, and final protection", 25, 15, 700)
    control = inlet(p, 35, 60)
    left_in = inlet(p, 170, 60, signal=True)
    right_in = inlet(p, 280, 60, signal=True)
    router = route(p, ("eq_low", "eq_lowmid", "eq_highmid", "eq_high", "eq_bypass", "master_trim_db"), 35, 105, 640)
    p.connect(control, router)

    band_specs = (
        ("lowshelf", 90.0, 30.0, 400.0, 0.7, 0),
        ("peaknotch", 250.0, 120.0, 1200.0, 0.8, 1),
        ("peaknotch", 3800.0, 1000.0, 8000.0, 1.0, 2),
        ("highshelf", 9000.0, 4000.0, 16000.0, 0.7, 3),
    )
    graphs: list[str] = []
    for index, (mode, default_freq, min_freq, max_freq, default_q, route_outlet) in enumerate(band_specs):
        x = 35 + index * 350
        is_peak = mode == "peaknotch"
        unpack = p.new("unpack 0. 0. 0." if is_peak else "unpack 0. 0.", x, 165, 105, numinlets=1, numoutlets=3 if is_peak else 2)
        freq_clip = p.new(f"clip {min_freq:g} {max_freq:g}", x, 205, 105, numinlets=3, numoutlets=1)
        gain_clip = p.new("clip -12. 12.", x + 115, 205, 85, numinlets=3, numoutlets=1)
        gain_linear = p.new("expr pow(10., $f1/20.)", x + 115, 245, 150, numinlets=1, numoutlets=1)
        q_clip = p.new("clip 0.3 4.", x + 220, 205, 85, numinlets=3, numoutlets=1) if is_peak else None
        packed = p.new("pak 0. 1. 1.", x, 285, 100, numinlets=3, numoutlets=1)
        named = p.new(f"prepend {mode}", x, 325, 125, numinlets=1, numoutlets=1)
        graph = p.add("filtergraph~", None, x, 365, 230, 110, numinlets=8, numoutlets=7)
        p.connect(router, unpack, route_outlet)
        p.connect(unpack, freq_clip, 0)
        p.connect(unpack, gain_clip, 1)
        p.connect(freq_clip, packed, 0, 0)
        p.connect(gain_clip, gain_linear)
        p.connect(gain_linear, packed, 0, 1)
        if q_clip is not None:
            p.connect(unpack, q_clip, 2)
            p.connect(q_clip, packed, 0, 2)
        default = p.new(f"loadmess {mode} {default_freq:g} 1. {default_q:g}", x, 490, 210, numinlets=1, numoutlets=1)
        p.connect(packed, named)
        p.connect(named, graph)
        p.connect(default, graph)
        graphs.append(graph)

    left_signal = left_in
    right_signal = right_in
    for index, graph in enumerate(graphs):
        x = 120 + index * 175
        left_filter = p.new("biquad~", x, 570, 65, numinlets=6, numoutlets=1)
        right_filter = p.new("biquad~", x, 615, 65, numinlets=6, numoutlets=1)
        p.connect(left_signal, left_filter)
        p.connect(right_signal, right_filter)
        p.connect(graph, left_filter)
        p.connect(graph, right_filter)
        left_signal = left_filter
        right_signal = right_filter

    bypass_clip = p.new("clip 0 1", 1030, 165, 65, numinlets=3, numoutlets=1)
    bypass_split = p.new("t f f", 1030, 205, 55, numinlets=1, numoutlets=2)
    wet_expr = p.new("expr 1.-$f1", 1100, 245, 90, numinlets=1, numoutlets=1)
    dry_pack = p.new("pack 0. 30", 980, 285, 85, numinlets=2, numoutlets=1)
    wet_pack = p.new("pack 0. 30", 1100, 285, 85, numinlets=2, numoutlets=1)
    dry_line = p.new("line~", 980, 325, 50, numinlets=2, numoutlets=2)
    wet_line = p.new("line~", 1100, 325, 50, numinlets=2, numoutlets=2)
    bypass_default = p.new("loadmess 0", 1210, 205, 80, numinlets=1, numoutlets=1)
    p.connect(router, bypass_clip, 4)
    p.connect(bypass_default, bypass_clip)
    p.connect(bypass_clip, bypass_split)
    p.connect(bypass_split, dry_pack, 1)
    p.connect(bypass_split, wet_expr, 0)
    p.connect(wet_expr, wet_pack)
    p.connect(dry_pack, dry_line)
    p.connect(wet_pack, wet_line)

    trim_clip = p.new("clip -24. 0.", 1230, 285, 85, numinlets=3, numoutlets=1)
    trim_amp = p.new("expr pow(10., $f1/20.)", 1230, 325, 150, numinlets=1, numoutlets=1)
    trim_pack = p.new("pack 0. 50", 1230, 365, 85, numinlets=2, numoutlets=1)
    trim_line = p.new("line~", 1230, 405, 50, numinlets=2, numoutlets=2)
    trim_default = p.new("loadmess -6.", 1360, 285, 95, numinlets=1, numoutlets=1)
    p.connect(router, trim_clip, 5)
    p.connect(trim_default, trim_clip)
    p.connect(trim_clip, trim_amp)
    p.connect(trim_amp, trim_pack)
    p.connect(trim_pack, trim_line)

    masters: list[str] = []
    for index, (dry, wet) in enumerate(((left_in, left_signal), (right_in, right_signal))):
        x = 380 + index * 420
        dry_gain = p.new("*~", x, 700, 40, numinlets=2, numoutlets=1)
        wet_gain = p.new("*~", x + 90, 700, 40, numinlets=2, numoutlets=1)
        blend = p.new("+~", x + 45, 745, 40, numinlets=2, numoutlets=1)
        trim = p.new("*~", x + 45, 785, 40, numinlets=2, numoutlets=1)
        p.connect(dry, dry_gain, 0, 0)
        p.connect(dry_line, dry_gain, 0, 1)
        p.connect(wet, wet_gain, 0, 0)
        p.connect(wet_line, wet_gain, 0, 1)
        p.connect(dry_gain, blend, 0, 0)
        p.connect(wet_gain, blend, 0, 1)
        p.connect(blend, trim, 0, 0)
        p.connect(trim_line, trim, 0, 1)
        masters.append(trim)
    limiter = p.new("omx.peaklim~", 610, 835, 105, numinlets=2, numoutlets=4)
    clip_l = p.new("clip~ -0.891 0.891", 430, 875, 130, numinlets=3, numoutlets=1)
    clip_r = p.new("clip~ -0.891 0.891", 810, 875, 130, numinlets=3, numoutlets=1)
    left = outlet(p, 575, 925, signal=True)
    right = outlet(p, 765, 925, signal=True)
    p.connect(masters[0], limiter, 0, 0)
    p.connect(masters[1], limiter, 0, 1)
    p.connect(limiter, clip_l, 0, 0)
    p.connect(limiter, clip_r, 1, 0)
    p.connect(clip_l, left)
    p.connect(clip_r, right)
    return p.document()


def make_powertrain() -> dict[str, Any]:
    p = Patcher(1280, 780)
    p.comment("Three bounded Gen powertrains, smoothed and continuously weighted", 25, 15, 500)
    control = inlet(p, 35, 65)
    tonal_names = ("rpm", "throttle", "load", "aggression", "brightness", "body", "texture")
    fuel_names = ("engine_running", "combustion_gain", "shift_cut")
    weight_names = ("ev_weight", "v12_weight", "v10_weight")
    names = tonal_names + fuel_names + weight_names
    router = route(p, names, 35, 105, 760)
    gens = [
        p.new("gen~ @gen ev_powertrain", 220, 395, 165, numinlets=1, numoutlets=2),
        p.new("gen~ @gen v12_powertrain", 510, 395, 175, numinlets=1, numoutlets=2),
        p.new("gen~ @gen v10_powertrain", 800, 395, 175, numinlets=1, numoutlets=2),
    ]
    bounds = {
        "rpm": (0.0, 10000.0),
        "throttle": (0.0, 1.0),
        "load": (-1.0, 1.0),
        "aggression": (0.0, 1.0),
        "brightness": (0.0, 1.0),
        "body": (0.0, 1.0),
        "texture": (0.0, 1.0),
    }
    for index, name in enumerate(tonal_names):
        low, high = bounds[name]
        x = 35 + index * 160
        bounded = p.new(f"clip {low:g} {high:g}", x, 175, 90, numinlets=3, numoutlets=1)
        named = p.message(f"{name} $1", x, 220, 105)
        p.connect(router, bounded, index)
        p.connect(bounded, named)
        for gen in gens:
            p.connect(named, gen)

    for index, name in enumerate(fuel_names):
        x = 720 + index * 160
        bounded = p.new("clip 0. 1.", x, 175, 75, numinlets=3, numoutlets=1)
        named = p.message(f"{name} $1", x, 220, 125)
        p.connect(router, bounded, len(tonal_names) + index)
        p.connect(bounded, named)
        p.connect(named, gens[1])
        p.connect(named, gens[2])

    lines: list[str] = []
    for index, name in enumerate(weight_names):
        x = 230 + index * 290
        bounded = p.new("clip 0. 1.", x, 285, 75, numinlets=3, numoutlets=1)
        packed = p.new("pack 0. 40", x, 320, 85, numinlets=2, numoutlets=1)
        smoothed = p.new("line~", x, 355, 50, numinlets=2, numoutlets=2)
        p.connect(router, bounded, len(tonal_names) + len(fuel_names) + index)
        p.connect(bounded, packed)
        p.connect(packed, smoothed)
        lines.append(smoothed)

    defaults = [(1.0, lines[0]), (0.0, lines[1]), (0.0, lines[2])]
    for index, (value, destination) in enumerate(defaults):
        initial = p.new(f"loadmess {value:g}", 1030, 285 + index * 38, 80, numinlets=1, numoutlets=1)
        p.connect(initial, destination)

    for index, text in enumerate(("engine_running 0", "combustion_gain 0", "shift_cut 1")):
        initial = p.new(f"loadmess {text}", 1030, 405 + index * 38, 155, numinlets=1, numoutlets=1)
        p.connect(initial, gens[1])
        p.connect(initial, gens[2])

    left_mults: list[str] = []
    right_mults: list[str] = []
    for index, gen in enumerate(gens):
        x = 210 + index * 290
        left_mult = p.new("*~", x, 485, 40, numinlets=2, numoutlets=1)
        right_mult = p.new("*~", x + 75, 485, 40, numinlets=2, numoutlets=1)
        p.connect(gen, left_mult, 0, 0)
        p.connect(gen, right_mult, 1, 0)
        p.connect(lines[index], left_mult, 0, 1)
        p.connect(lines[index], right_mult, 0, 1)
        left_mults.append(left_mult)
        right_mults.append(right_mult)

    add_l1 = p.new("+~", 360, 565, 35, numinlets=2, numoutlets=1)
    add_l2 = p.new("+~", 520, 610, 35, numinlets=2, numoutlets=1)
    add_r1 = p.new("+~", 650, 565, 35, numinlets=2, numoutlets=1)
    add_r2 = p.new("+~", 810, 610, 35, numinlets=2, numoutlets=1)
    left = outlet(p, 520, 680, signal=True)
    right = outlet(p, 810, 680, signal=True)
    p.connect(left_mults[0], add_l1, 0, 0)
    p.connect(left_mults[1], add_l1, 0, 1)
    p.connect(add_l1, add_l2, 0, 0)
    p.connect(left_mults[2], add_l2, 0, 1)
    p.connect(right_mults[0], add_r1, 0, 0)
    p.connect(right_mults[1], add_r1, 0, 1)
    p.connect(add_r1, add_r2, 0, 0)
    p.connect(right_mults[2], add_r2, 0, 1)
    p.connect(add_l2, left)
    p.connect(add_r2, right)
    p.connect(control, router)
    return p.document()


def make_cabin_rumble() -> dict[str, Any]:
    p = Patcher(1420, 820)
    p.comment("Lifecycle-gated engine, mount, body, cabin, and exhaust low-frequency system", 25, 15, 760)
    control = inlet(p, 35, 65)
    names = (
        "engine_type",
        "rpm",
        "throttle",
        "load",
        "gear",
        "engine_running",
        "combustion_gain",
        "shift_cut",
        "cabin_rumble",
        "exhaust_boom",
        "structure_vibration",
        "body",
        "aggression",
    )
    router = route(p, names, 35, 105, 1120)
    engine_type = p.new("sel ev v12 v10", 35, 165, 105, numinlets=1, numoutlets=4)
    firing_messages = (
        p.message("firing_order 0", 35, 205, 105),
        p.message("firing_order 6", 155, 205, 105),
        p.message("firing_order 5", 275, 205, 105),
    )
    gen = p.new("gen~ @gen cabin_rumble", 565, 430, 180, numinlets=1, numoutlets=2)
    p.connect(router, engine_type, 0)
    for index, message in enumerate(firing_messages):
        p.connect(engine_type, message, index)
        p.connect(message, gen)

    forwarded = names[1:]
    for index, name in enumerate(forwarded):
        column = index % 6
        row = index // 6
        named = p.new(f"prepend {name}", 400 + column * 165, 165 + row * 75, 145, numinlets=1, numoutlets=1)
        p.connect(router, named, index + 1)
        p.connect(named, gen)

    initial = p.new("loadmess firing_order 0", 35, 260, 155, numinlets=1, numoutlets=1)
    p.connect(initial, gen)
    highpass_l = p.new("svf~ 28 0.7", 470, 535, 90, numinlets=3, numoutlets=4)
    highpass_r = p.new("svf~ 28 0.7", 750, 535, 90, numinlets=3, numoutlets=4)
    left = outlet(p, 500, 650, signal=True)
    right = outlet(p, 780, 650, signal=True)
    p.connect(gen, highpass_l, 0, 0)
    p.connect(gen, highpass_r, 1, 0)
    p.connect(highpass_l, left, 1, 0)
    p.connect(highpass_r, right, 1, 0)
    p.connect(control, router)
    return p.document()


def make_transient() -> dict[str, Any]:
    p = Patcher(1900, 1500)
    p.comment("Profile-aware, round-robin transient families; missing buffers never stop continuous layers", 25, 15, 760)
    control = inlet(p, 35, 60)
    event_names = (
        "starter",
        "shift",
        "shift_dir",
        "pop",
        "intake_backfire",
        "exhaust_pop",
        "crackle",
        "click",
        "aggression",
        "texture",
        "engine_type",
        "engine_running",
    )
    router = route(p, event_names, 35, 100, 850)
    players: list[str] = []

    starter_sel = p.new("sel 1", 35, 150, 45, numinlets=1, numoutlets=2)
    profile_sel = p.new("sel ev v12 v10", 105, 150, 105, numinlets=1, numoutlets=4)
    profile_gate = p.new("gate 2", 35, 195, 55, numinlets=2, numoutlets=2)
    p.connect(router, starter_sel, 0)
    p.connect(starter_sel, profile_gate, 0, 1)
    p.connect(router, profile_sel, 10)
    for outlet_index, value in ((0, 0), (1, 1), (2, 2)):
        message = p.message(str(value), 105 + outlet_index * 45, 195, 30)
        p.connect(profile_sel, message, outlet_index)
        p.connect(message, profile_gate, 0, 0)

    for index, (name, gate_outlet) in enumerate((("starter_v12", 0), ("starter_v10", 1))):
        x = 35 + index * 300
        p.new(f"buffer~ {name} media/{name}.wav", x, 245, 245, numinlets=1, numoutlets=2)
        start = p.message("start", x, 285, 45)
        player = p.new(f"play~ {name} 1", x, 325, 145, numinlets=1, numoutlets=2)
        gain = p.new("*~ 0.26", x, 365, 65, numinlets=2, numoutlets=1)
        p.connect(profile_gate, start, gate_outlet)
        p.connect(start, player)
        p.connect(player, gain)
        players.append(gain)

    shift_sel = p.new("sel 1", 650, 150, 45, numinlets=1, numoutlets=2)
    shift_direction = p.new("sel -1 1", 720, 150, 60, numinlets=1, numoutlets=3)
    pop_sel = p.new("sel 1", 805, 150, 45, numinlets=1, numoutlets=2)
    intake_sel = p.new("sel 1", 875, 150, 45, numinlets=1, numoutlets=2)
    exhaust_sel = p.new("sel 1", 945, 150, 45, numinlets=1, numoutlets=2)
    crackle_sel = p.new("sel 1", 1015, 150, 45, numinlets=1, numoutlets=2)
    click_sel = p.new("sel 1", 1085, 150, 45, numinlets=1, numoutlets=2)
    p.connect(router, shift_sel, 1)
    p.connect(router, shift_direction, 2)
    p.connect(router, pop_sel, 3)
    p.connect(router, intake_sel, 4)
    p.connect(router, exhaust_sel, 5)
    p.connect(router, crackle_sel, 6)
    p.connect(router, click_sel, 7)

    shift_up_gate = p.new("gate 1", 650, 205, 55, numinlets=2, numoutlets=1)
    shift_down_gate = p.new("gate 1", 720, 205, 55, numinlets=2, numoutlets=1)
    intake_gate = p.new("gate 1", 875, 205, 55, numinlets=2, numoutlets=1)
    exhaust_gate = p.new("gate 1", 945, 205, 55, numinlets=2, numoutlets=1)
    crackle_gate = p.new("gate 1", 1015, 205, 55, numinlets=2, numoutlets=1)
    fuel_event_off = p.message("0", 1090, 205, 30)
    fuel_event_v12 = p.message("1", 1130, 205, 30)
    fuel_event_v10 = p.message("1", 1170, 205, 30)
    running_clip = p.new("clip 0 1", 1210, 205, 65, numinlets=3, numoutlets=1)
    event_state = p.new("pak 0 0", 1090, 245, 70, numinlets=2, numoutlets=1)
    event_enabled = p.new("expr $i1*$i2", 1175, 245, 105, numinlets=2, numoutlets=1)
    p.connect(profile_sel, fuel_event_off, 0)
    p.connect(profile_sel, fuel_event_v12, 1)
    p.connect(profile_sel, fuel_event_v10, 2)
    for message in (fuel_event_off, fuel_event_v12, fuel_event_v10):
        p.connect(message, event_state, 0, 0)
    p.connect(router, running_clip, 11)
    p.connect(running_clip, event_state, 0, 1)
    p.connect(event_state, event_enabled)
    for event_gate in (shift_up_gate, shift_down_gate, intake_gate, exhaust_gate, crackle_gate):
        p.connect(event_enabled, event_gate, 0, 0)
    p.connect(shift_sel, shift_up_gate, 0, 1)
    p.connect(shift_direction, shift_up_gate, 1, 1)
    p.connect(shift_direction, shift_down_gate, 0, 1)
    p.connect(intake_sel, intake_gate, 0, 1)
    p.connect(pop_sel, exhaust_gate, 0, 1)
    p.connect(exhaust_sel, exhaust_gate, 0, 1)
    p.connect(crackle_sel, crackle_gate, 0, 1)

    def add_family(
        names: tuple[str, ...],
        gain_value: float,
        x: float,
        y: float,
        triggers: tuple[tuple[str, int], ...],
    ) -> None:
        counter = p.new(f"counter 0 {len(names)-1}", x, y, 90, numinlets=5, numoutlets=4)
        selector = p.new("sel " + " ".join(str(index) for index in range(len(names))), x, y + 38, 105, numinlets=1, numoutlets=len(names) + 1)
        p.connect(counter, selector)
        for source, source_outlet in triggers:
            p.connect(source, counter, source_outlet)
        for index, name in enumerate(names):
            px = x + index * 190
            p.new(f"buffer~ {name} media/{name}.wav", px, y + 82, 180, numinlets=1, numoutlets=2)
            start = p.message("start", px, y + 122, 45)
            player = p.new(f"play~ {name} 1", px, y + 162, 155, numinlets=1, numoutlets=2)
            gain = p.new(f"*~ {gain_value:.2f}", px, y + 202, 65, numinlets=2, numoutlets=1)
            p.connect(selector, start, index)
            p.connect(start, player)
            p.connect(player, gain)
            players.append(gain)

    add_family(tuple(f"shift_up_{index:02d}" for index in range(1, 4)), 0.32, 35, 440, ((shift_up_gate, 0),))
    add_family(tuple(f"shift_down_{index:02d}" for index in range(1, 4)), 0.38, 650, 440, ((shift_down_gate, 0),))
    add_family(tuple(f"intake_backfire_{index:02d}" for index in range(1, 4)), 0.34, 1265, 440, ((intake_gate, 0),))
    add_family(tuple(f"exhaust_pop_{index:02d}" for index in range(1, 5)), 0.30, 35, 740, ((exhaust_gate, 0),))
    add_family(tuple(f"exhaust_crackle_{index:02d}" for index in range(1, 4)), 0.18, 830, 740, ((crackle_gate, 0),))

    p.new("buffer~ mechanical_click media/mechanical_click.wav", 1445, 740, 245, numinlets=1, numoutlets=2)
    click_start = p.message("start", 1445, 780, 45)
    click_player = p.new("play~ mechanical_click 1", 1445, 820, 155, numinlets=1, numoutlets=2)
    click_gain = p.new("*~ 0.18", 1445, 860, 65, numinlets=2, numoutlets=1)
    p.connect(click_sel, click_start, 0)
    p.connect(click_start, click_player)
    p.connect(click_player, click_gain)
    players.append(click_gain)

    aggression_clip = p.new("clip 0. 1.", 1400, 105, 75, numinlets=3, numoutlets=1)
    aggression_gain = p.new("expr 0.72 + 0.38*$f1", 1400, 145, 155, numinlets=1, numoutlets=1)
    aggression_pack = p.new("pack 0. 25", 1400, 185, 85, numinlets=2, numoutlets=1)
    aggression_line = p.new("line~", 1400, 225, 50, numinlets=2, numoutlets=2)
    p.connect(router, aggression_clip, 8)
    p.connect(aggression_clip, aggression_gain)
    p.connect(aggression_gain, aggression_pack)
    p.connect(aggression_pack, aggression_line)
    default_gain = p.new("loadmess 1.", 815, 225, 85, numinlets=1, numoutlets=1)
    p.connect(default_gain, aggression_line)

    mixed = players[0]
    for index, player in enumerate(players[1:]):
        add = p.new("+~", 240 + (index % 8) * 105, 1080 + (index // 8) * 45, 35, numinlets=2, numoutlets=1)
        p.connect(mixed, add, 0, 0)
        p.connect(player, add, 0, 1)
        mixed = add
    master = p.new("*~", 920, 1220, 40, numinlets=2, numoutlets=1)
    left_gain = p.new("*~ 0.94", 820, 1280, 65, numinlets=2, numoutlets=1)
    right_gain = p.new("*~ 0.88", 980, 1280, 65, numinlets=2, numoutlets=1)
    left = outlet(p, 850, 1360, signal=True)
    right = outlet(p, 1010, 1360, signal=True)
    p.connect(mixed, master, 0, 0)
    p.connect(aggression_line, master, 0, 1)
    p.connect(master, left_gain)
    p.connect(master, right_gain)
    p.connect(left_gain, left)
    p.connect(right_gain, right)
    p.connect(control, router)
    return p.document()


def make_road_air() -> dict[str, Any]:
    p = Patcher(1040, 650)
    p.comment("Independent road/air noise, bounded by speed and smoothed before gain/filtering", 25, 15, 560)
    control = inlet(p, 35, 60)
    router = route(p, ("speed_kph", "throttle", "brightness", "texture", "cabin_width"), 35, 100, 470)
    speed_clip = p.new("clip 0. 300.", 35, 155, 85, numinlets=3, numoutlets=1)
    speed_curve = p.new("expr pow($f1/300., 0.7) * 0.12", 35, 195, 190, numinlets=1, numoutlets=1)
    speed_pack = p.new("pack 0. 120", 35, 235, 90, numinlets=2, numoutlets=1)
    speed_line = p.new("line~", 35, 275, 50, numinlets=2, numoutlets=2)
    bright_clip = p.new("clip 0. 1.", 285, 155, 75, numinlets=3, numoutlets=1)
    cutoff_expr = p.new("expr 500. + 3000.*$f1", 285, 195, 165, numinlets=1, numoutlets=1)
    cutoff_pack = p.new("pack 0. 80", 285, 235, 85, numinlets=2, numoutlets=1)
    cutoff_line = p.new("line~", 285, 275, 50, numinlets=2, numoutlets=2)
    p.connect(router, speed_clip, 0)
    p.connect(speed_clip, speed_curve)
    p.connect(speed_curve, speed_pack)
    p.connect(speed_pack, speed_line)
    p.connect(router, bright_clip, 2)
    p.connect(bright_clip, cutoff_expr)
    p.connect(cutoff_expr, cutoff_pack)
    p.connect(cutoff_pack, cutoff_line)
    for value, destination, x in ((0.0, speed_line, 550), (1700.0, cutoff_line, 670)):
        default = p.new(f"loadmess {value:g}", x, 275, 95, numinlets=1, numoutlets=1)
        p.connect(default, destination)

    channels: list[str] = []
    for index, x in enumerate((220, 610)):
        noise = p.new("noise~", x, 350, 55, numinlets=0, numoutlets=1)
        highpass = p.new("svf~ 65 0.5", x, 390, 85, numinlets=3, numoutlets=4)
        lowpass = p.new("lores~ 1800 0.35", x, 430, 120, numinlets=3, numoutlets=1)
        gain = p.new("*~", x, 475, 40, numinlets=2, numoutlets=1)
        stereo = p.new(f"*~ {0.96 - index * 0.05:.2f}", x, 520, 65, numinlets=2, numoutlets=1)
        p.connect(noise, highpass)
        p.connect(highpass, lowpass, 1, 0)
        p.connect(cutoff_line, lowpass, 0, 1)
        p.connect(lowpass, gain, 0, 0)
        p.connect(speed_line, gain, 0, 1)
        p.connect(gain, stereo)
        channels.append(stereo)
    left = outlet(p, 250, 585, signal=True)
    right = outlet(p, 640, 585, signal=True)
    p.connect(channels[0], left)
    p.connect(channels[1], right)
    p.connect(control, router)
    return p.document()


def make_cabin_master() -> dict[str, Any]:
    p = Patcher(1180, 760)
    p.comment("Cabin tone and stereo width; final EQ/protection lives in mix_master~", 25, 15, 560)
    control = inlet(p, 35, 65)
    left_in = inlet(p, 210, 65, signal=True)
    right_in = inlet(p, 330, 65, signal=True)
    router = route(p, ("aggression", "brightness", "body", "texture", "cabin_width"), 35, 115, 455)

    controls: dict[str, str] = {}
    expressions = {
        "aggression": "expr 0.48 + 0.20*$f1",
        "brightness": "expr 4500. + 14500.*$f1",
        "body": "expr 0.78 + 0.25*$f1",
        "texture": "expr 0.94 + 0.06*$f1",
        "cabin_width": "expr 0.25 + 1.05*$f1",
    }
    for index, name in enumerate(expressions):
        x = 35 + index * 205
        bounded = p.new("clip 0. 1.", x, 175, 75, numinlets=3, numoutlets=1)
        expression = p.new(expressions[name], x, 215, 165, numinlets=1, numoutlets=1)
        packed = p.new("pack 0. 60", x, 255, 85, numinlets=2, numoutlets=1)
        line = p.new("line~", x, 295, 50, numinlets=2, numoutlets=2)
        p.connect(router, bounded, index)
        p.connect(bounded, expression)
        p.connect(expression, packed)
        p.connect(packed, line)
        controls[name] = line

    defaults = {"aggression": 0.55, "brightness": 12000.0, "body": 0.9, "texture": 0.97, "cabin_width": 0.9}
    for index, (name, value) in enumerate(defaults.items()):
        initial = p.new(f"loadmess {value:g}", 1040, 175 + index * 36, 100, numinlets=1, numoutlets=1)
        p.connect(initial, controls[name])

    mid_sum = p.new("+~", 220, 390, 40, numinlets=2, numoutlets=1)
    mid = p.new("*~ 0.5", 220, 430, 60, numinlets=2, numoutlets=1)
    side_diff = p.new("-~", 400, 390, 40, numinlets=2, numoutlets=1)
    side = p.new("*~ 0.5", 400, 430, 60, numinlets=2, numoutlets=1)
    side_highpass = p.new("svf~ 120 0.7", 400, 470, 100, numinlets=3, numoutlets=4)
    side_width = p.new("*~", 400, 510, 40, numinlets=2, numoutlets=1)
    reconstruct_l = p.new("+~", 280, 550, 40, numinlets=2, numoutlets=1)
    reconstruct_r = p.new("-~", 520, 550, 40, numinlets=2, numoutlets=1)
    p.connect(left_in, mid_sum, 0, 0)
    p.connect(right_in, mid_sum, 0, 1)
    p.connect(mid_sum, mid)
    p.connect(left_in, side_diff, 0, 0)
    p.connect(right_in, side_diff, 0, 1)
    p.connect(side_diff, side)
    p.connect(side, side_highpass, 0, 0)
    p.connect(side_highpass, side_width, 1, 0)
    p.connect(controls["cabin_width"], side_width, 0, 1)
    p.connect(mid, reconstruct_l, 0, 0)
    p.connect(side_width, reconstruct_l, 0, 1)
    p.connect(mid, reconstruct_r, 0, 0)
    p.connect(side_width, reconstruct_r, 0, 1)

    masters: list[str] = []
    for signal, x in ((reconstruct_l, 300), (reconstruct_r, 650)):
        lowpass = p.new("onepole~ 12000", x, 565, 105, numinlets=2, numoutlets=1)
        body_gain = p.new("*~", x, 605, 40, numinlets=2, numoutlets=1)
        master_gain = p.new("*~", x, 640, 40, numinlets=2, numoutlets=1)
        p.connect(signal, lowpass, 0, 0)
        p.connect(controls["brightness"], lowpass, 0, 1)
        p.connect(lowpass, body_gain, 0, 0)
        p.connect(controls["body"], body_gain, 0, 1)
        p.connect(body_gain, master_gain, 0, 0)
        p.connect(controls["aggression"], master_gain, 0, 1)
        masters.append(master_gain)
    left = outlet(p, 430, 710, signal=True)
    right = outlet(p, 790, 710, signal=True)
    p.connect(masters[0], left)
    p.connect(masters[1], right)
    p.connect(control, router)
    return p.document()


def make_drive_simulator() -> dict[str, Any]:
    p = Patcher(1420, 900)
    p.comment("Internal drive simulator: integrated speed and profile-aware 7-speed DCT", 25, 15, 620)
    p.comment("V12 ratios 3.10 2.13 1.62 1.29 1.03 0.84 0.70", 735, 15, 470)
    p.comment("V10 ratios 3.13 2.10 1.52 1.20 0.94 0.76 0.62", 735, 42, 470)
    control = inlet(p, 35, 65)
    router = route(p, ("throttle", "brake", "auto", "engine_type", "ignition", "start"), 35, 105, 500)
    throttle_clip = p.new("clip 0. 1.", 35, 155, 75, numinlets=3, numoutlets=1)
    brake_clip = p.new("clip 0. 1.", 145, 155, 75, numinlets=3, numoutlets=1)
    auto_clip = p.new("clip 0 1", 255, 155, 65, numinlets=3, numoutlets=1)
    engine_type = p.new("sel ev v12 v10", 355, 155, 105, numinlets=1, numoutlets=4)
    profile_ev = p.message("0", 355, 195, 30)
    profile_v12 = p.message("12", 400, 195, 35)
    profile_v10 = p.message("10", 450, 195, 35)
    profile_default = p.new("loadmess 0", 500, 195, 80, numinlets=1, numoutlets=1)
    p.comment("Drive lifecycle gate: EV is always enabled; fuel requires ignition + start", 35, 225, 500)
    ignition_clip = p.new("clip 0 1", 35, 250, 65, numinlets=3, numoutlets=1)
    ignition_off = p.new("sel 0", 110, 250, 45, numinlets=1, numoutlets=2)
    start_clip = p.new("clip 0 1", 165, 250, 65, numinlets=3, numoutlets=1)
    start_gate = p.new("gate 1", 240, 250, 55, numinlets=2, numoutlets=1)
    reset_start = p.message("0", 305, 250, 30)
    lifecycle_state = p.new("pak 0 0 0", 35, 280, 90, numinlets=3, numoutlets=1)
    drive_enabled = p.new(
        "expr ($i3==0)+(($i3!=0)*$i1*$i2)",
        135,
        280,
        220,
        numinlets=3,
        numoutlets=1,
    )

    tick = p.new("qmetro 50", 610, 105, 75, numinlets=2, numoutlets=1)
    load = p.new("loadmess 1", 610, 65, 75, numinlets=1, numoutlets=1)
    tick_order = p.new("t b b b", 610, 145, 70, numinlets=1, numoutlets=3)
    counter = p.new("counter 0 399", 610, 185, 95, numinlets=5, numoutlets=4)
    state = p.new("pak 0. 0. 0 0", 250, 250, 105, numinlets=4, numoutlets=1)
    effective_throttle = p.new(
        "expr ($f3>.5)*((($f4>=40)*($f4<210))*(0.18+0.77*min(1.,($f4-40.)/120.))+(($f4>=210)*($f4<260))*.35)+($f3<=.5)*$f1",
        35,
        295,
        700,
        numinlets=4,
        numoutlets=1,
    )
    effective_brake = p.new(
        "expr ($f3>.5)*(($f4>=260)*($f4<370))*.42+($f3<=.5)*$f2",
        755,
        295,
        430,
        numinlets=4,
        numoutlets=1,
    )
    enabled_throttle = p.new("* 1.", 500, 325, 50, numinlets=2, numoutlets=1)

    speed_store = p.new("f 0.", 610, 250, 50, numinlets=2, numoutlets=1)
    speed_state = p.new("pack 0. 0. 0.", 610, 340, 105, numinlets=3, numoutlets=1)
    speed_integrator = p.new(
        "expr max(0.,min(300.,$f1+0.05*($f2*(34.-0.07*$f1)-(0.5+0.00012*$f1*$f1)-$f3*55.)))",
        610,
        380,
        620,
        numinlets=3,
        numoutlets=1,
    )
    speed_split = p.new("t f f f", 610, 425, 70, numinlets=1, numoutlets=3)

    gear_store = p.new("int 1", 850, 250, 50, numinlets=2, numoutlets=1)
    gear_default = p.new("loadmess 1", 910, 250, 80, numinlets=1, numoutlets=1)
    ev_rpm_state = p.new("pak 0. 0.", 505, 470, 75, numinlets=2, numoutlets=1)
    v12_rpm_state = p.new("pak 0. 1", 610, 470, 75, numinlets=2, numoutlets=1)
    v10_rpm_state = p.new("pak 0. 1", 715, 470, 75, numinlets=2, numoutlets=1)
    ev_rpm = p.new("expr min(10000.,650.+$f1*31.+$f2*1400.)", 455, 510, 245, numinlets=2, numoutlets=1)
    v12_rpm = p.new(
        "expr max(780.,$f1*(($i2==1)*107.+($i2==2)*73.5+($i2==3)*55.9+($i2==4)*44.5+($i2==5)*35.6+($i2==6)*29.+($i2==7)*24.2))",
        710,
        510,
        530,
        numinlets=2,
        numoutlets=1,
    )
    v10_rpm = p.new(
        "expr max(850.,$f1*(($i2==1)*114.2+($i2==2)*76.7+($i2==3)*55.5+($i2==4)*43.8+($i2==5)*34.3+($i2==6)*27.7+($i2==7)*22.6))",
        710,
        540,
        540,
        numinlets=2,
        numoutlets=1,
    )
    rpm_switch = p.new("switch 3", 505, 550, 75, numinlets=4, numoutlets=1)
    rpm_profile_ev = p.message("1", 310, 235, 30)
    rpm_profile_v12 = p.message("2", 350, 235, 30)
    rpm_profile_v10 = p.message("3", 390, 235, 30)
    rpm_profile_default = p.new("loadmess 1", 430, 235, 80, numinlets=1, numoutlets=1)
    rpm_split = p.new("t f f", 610, 590, 55, numinlets=1, numoutlets=2)
    shift_state = p.new("pack 0. 1 0 0.", 820, 550, 115, numinlets=4, numoutlets=1)
    shift_decision = p.new(
        "expr ($i3==12)*((($f1>6200.+2600.*$f4)*($i2<7))-(($f1<2200.+1600.*$f4)*($i2>1)))+($i3==10)*((($f1>5800.+2500.*$f4)*($i2<7))-(($f1<2100.+1500.*$f4)*($i2>1)))",
        820,
        590,
        575,
        numinlets=4,
        numoutlets=1,
    )
    nonzero = p.new("sel 0", 820, 630, 45, numinlets=1, numoutlets=2)
    lockout = p.new("speedlim 350", 880, 630, 85, numinlets=2, numoutlets=1)
    direction = p.new("sel -1 1", 880, 670, 60, numinlets=1, numoutlets=3)
    down_value = p.message("-1", 820, 710, 30)
    up_value = p.message("1", 865, 710, 30)
    down_named = p.message("shift_dir -1", 910, 710, 80)
    up_named = p.message("shift_dir 1", 1005, 710, 75)
    gear_state = p.new("pack 0 1", 820, 750, 70, numinlets=2, numoutlets=1)
    gear_next = p.new("expr $i1+$i2", 820, 785, 95, numinlets=2, numoutlets=1)
    gear_clip = p.new("clip 1 7", 930, 785, 65, numinlets=3, numoutlets=1)
    gear_trigger = p.new("t i i", 1010, 785, 55, numinlets=1, numoutlets=2)
    output = outlet(p, 690, 850)

    p.connect(control, router)
    p.connect(router, throttle_clip, 0)
    p.connect(router, brake_clip, 1)
    p.connect(router, auto_clip, 2)
    p.connect(router, engine_type, 3)
    p.connect(router, ignition_clip, 4)
    p.connect(router, start_clip, 5)
    p.connect(engine_type, profile_ev, 0)
    p.connect(engine_type, profile_v12, 1)
    p.connect(engine_type, profile_v10, 2)
    p.connect(ignition_clip, ignition_off)
    p.connect(ignition_clip, lifecycle_state, 0, 0)
    p.connect(ignition_clip, start_gate, 0, 0)
    p.connect(start_clip, start_gate, 0, 1)
    p.connect(start_gate, lifecycle_state, 0, 1)
    p.connect(ignition_off, reset_start, 0)
    p.connect(reset_start, lifecycle_state, 0, 1)
    for profile in (profile_ev, profile_v12, profile_v10, profile_default):
        p.connect(profile, lifecycle_state, 0, 2)
    p.connect(lifecycle_state, drive_enabled)
    p.connect(engine_type, rpm_profile_ev, 0)
    p.connect(engine_type, rpm_profile_v12, 1)
    p.connect(engine_type, rpm_profile_v10, 2)
    p.connect(rpm_profile_ev, rpm_switch, 0, 0)
    p.connect(rpm_profile_v12, rpm_switch, 0, 0)
    p.connect(rpm_profile_v10, rpm_switch, 0, 0)
    p.connect(rpm_profile_default, rpm_switch, 0, 0)
    p.connect(throttle_clip, state, 0, 0)
    p.connect(brake_clip, state, 0, 1)
    p.connect(auto_clip, state, 0, 2)
    p.connect(load, tick)
    p.connect(tick, tick_order)
    p.connect(tick_order, counter, 2)
    p.connect(tick_order, gear_store, 1)
    p.connect(tick_order, speed_store, 0)
    p.connect(counter, state, 0, 3)
    p.connect(state, effective_throttle)
    p.connect(state, effective_brake)
    p.connect(effective_throttle, enabled_throttle, 0, 0)
    p.connect(drive_enabled, enabled_throttle, 0, 1)
    p.connect(enabled_throttle, speed_state, 0, 1)
    p.connect(effective_brake, speed_state, 0, 2)
    p.connect(speed_store, speed_state, 0, 0)
    p.connect(speed_state, speed_integrator)
    p.connect(speed_integrator, speed_split)
    p.connect(speed_split, speed_store, 2, 1)
    p.connect(speed_split, ev_rpm_state, 1, 0)
    p.connect(speed_split, v12_rpm_state, 1, 0)
    p.connect(speed_split, v10_rpm_state, 1, 0)
    p.connect(gear_store, v12_rpm_state, 0, 1)
    p.connect(gear_store, v10_rpm_state, 0, 1)
    p.connect(gear_store, shift_state, 0, 1)
    p.connect(gear_store, gear_state, 0, 1)
    p.connect(profile_ev, shift_state, 0, 2)
    p.connect(profile_v12, shift_state, 0, 2)
    p.connect(profile_v10, shift_state, 0, 2)
    p.connect(profile_default, shift_state, 0, 2)
    p.connect(enabled_throttle, ev_rpm_state, 0, 1)
    p.connect(enabled_throttle, shift_state, 0, 3)
    p.connect(ev_rpm_state, ev_rpm)
    p.connect(v12_rpm_state, v12_rpm)
    p.connect(v10_rpm_state, v10_rpm)
    p.connect(ev_rpm, rpm_switch, 0, 1)
    p.connect(v12_rpm, rpm_switch, 0, 2)
    p.connect(v10_rpm, rpm_switch, 0, 3)
    p.connect(rpm_switch, rpm_split)
    p.connect(rpm_split, shift_state, 1, 0)
    p.connect(shift_state, shift_decision)
    p.connect(shift_decision, nonzero)
    p.connect(nonzero, lockout, 1)
    p.connect(lockout, direction)
    p.connect(direction, down_value, 0)
    p.connect(direction, down_named, 0)
    p.connect(direction, up_value, 1)
    p.connect(direction, up_named, 1)
    p.connect(down_value, gear_state)
    p.connect(up_value, gear_state)
    p.connect(gear_state, gear_next)
    p.connect(gear_next, gear_clip)
    p.connect(gear_clip, gear_trigger)
    p.connect(gear_trigger, gear_store, 1, 1)
    for message in (down_named, up_named):
        p.connect(message, output)

    intake_state = p.new("pak 0. 0. 0", 1120, 345, 100, numinlets=3, numoutlets=1)
    intake_condition = p.new(
        "expr ($i3!=0)*($f1>0.72)*($f2>2800.)",
        1120,
        385,
        250,
        numinlets=3,
        numoutlets=1,
    )
    intake_change = p.new("change", 1180, 425, 55, numinlets=1, numoutlets=1)
    intake_edge = p.new("sel 1", 1180, 465, 45, numinlets=1, numoutlets=2)
    intake_on = p.message("intake_backfire 1", 1180, 505, 110)
    intake_delay = p.new("delay 90", 1305, 505, 65, numinlets=2, numoutlets=1)
    intake_off = p.message("intake_backfire 0", 1305, 545, 110)
    p.connect(enabled_throttle, intake_state, 0, 0)
    p.connect(rpm_split, intake_state, 1, 1)
    for profile in (profile_ev, profile_v12, profile_v10, profile_default):
        p.connect(profile, intake_state, 0, 2)
    p.connect(intake_state, intake_condition)
    p.connect(intake_condition, intake_change)
    p.connect(intake_change, intake_edge)
    p.connect(intake_edge, intake_on, 0)
    p.connect(intake_edge, intake_delay, 0)
    p.connect(intake_delay, intake_off)
    p.connect(intake_on, output)
    p.connect(intake_off, output)
    named_sources = [
        (speed_split, 0, "prepend speed_kph", 35, 590),
        (rpm_split, 0, "prepend rpm", 170, 590),
        (enabled_throttle, 0, "prepend throttle", 35, 395),
        (effective_brake, 0, "prepend brake", 35, 440),
        (enabled_throttle, 0, "expr max(-1., min(1., $f1*1.6))", 35, 485),
        (enabled_throttle, 0, "expr max(-1., min(1., $f1*2.-$f2*2.))", 35, 530),
        (gear_trigger, 0, "prepend gear", 305, 590),
    ]
    for index, (source, source_outlet, text, x, y) in enumerate(named_sources):
        object_box = p.new(text, x, y, 185 if text.startswith("expr") else 115, numinlets=2 if index == 5 else 1, numoutlets=1)
        p.connect(source, object_box, source_outlet)
        if index == 5:
            p.connect(effective_brake, object_box, 0, 1)
            named = p.new("prepend accel", x, y + 38, 95, numinlets=1, numoutlets=1)
            p.connect(object_box, named)
            p.connect(named, output)
        elif index == 4:
            named = p.new("prepend load", x, y + 38, 90, numinlets=1, numoutlets=1)
            p.connect(object_box, named)
            p.connect(named, output)
        else:
            p.connect(object_box, output)
    return p.document()


def add_labeled_number(p: Patcher, label: str, name: str, x: float, y: float, engine: str) -> None:
    p.comment(label, x, y, 110)
    number = p.add("flonum", None, x, y + 24, 75, numinlets=1, numoutlets=2)
    bounded = p.new("clip 0. 1.", x, y + 58, 75, numinlets=3, numoutlets=1)
    named = p.new(f"prepend {name}", x, y + 92, 110, numinlets=1, numoutlets=1)
    p.connect(number, bounded)
    p.connect(bounded, named)
    p.connect(named, engine)


def add_eq_band(
    p: Patcher,
    label: str,
    name: str,
    x: float,
    y: float,
    default_frequency: float,
    engine: str,
    *,
    q: float | None = None,
) -> None:
    p.comment(f"{label} — Hz / dB" + (" / Q" if q is not None else ""), x, y, 185)
    frequency = p.add("flonum", None, x, y + 24, 65, numinlets=1, numoutlets=2)
    gain = p.add("flonum", None, x + 72, y + 24, 55, numinlets=1, numoutlets=2)
    if q is None:
        values = p.new(f"pak {default_frequency:g} 0.", x, y + 58, 115, numinlets=2, numoutlets=1)
    else:
        q_control = p.add("flonum", None, x + 134, y + 24, 50, numinlets=1, numoutlets=2)
        values = p.new(f"pak {default_frequency:g} 0. {q:g}", x, y + 58, 145, numinlets=3, numoutlets=1)
        q_default = p.new(f"loadmess {q:g}", x + 134, y + 88, 85, numinlets=1, numoutlets=1)
        p.connect(q_control, values, 0, 2)
        p.connect(q_default, q_control)
    named = p.new(f"prepend {name}", x, y + 92, 135, numinlets=1, numoutlets=1)
    frequency_default = p.new(f"loadmess {default_frequency:g}", x, y + 126, 105, numinlets=1, numoutlets=1)
    p.connect(frequency, values, 0, 0)
    p.connect(gain, values, 0, 1)
    p.connect(values, named)
    p.connect(named, engine)
    p.connect(frequency_default, frequency)


def make_main() -> dict[str, Any]:
    p = Patcher(1680, 1160)
    p.comment("VehicleSoundSynth V3 — combustion lifecycle, cabin rumble, 7-speed DCT, and final mix", 25, 15, 860)
    p.comment("Audio starts OFF — lower your monitoring level, then enable DSP", 25, 45, 520)
    load_off = p.new("loadmess 0", 25, 80, 80, numinlets=1, numoutlets=1)
    audio_toggle = p.add("toggle", None, 120, 80, 24, 24, numinlets=1, numoutlets=1)
    ramp_message = p.message("$1 60", 235, 80, 55)
    audio_line = p.new("line~", 305, 80, 50, numinlets=2, numoutlets=2)
    p.connect(load_off, audio_toggle)
    p.connect(audio_toggle, ramp_message)
    p.connect(ramp_message, audio_line)

    p.comment("Drive Source: Internal Manual / Internal Auto / External vss.input", 25, 135, 520)
    mode = p.add(
        "umenu",
        None,
        25,
        165,
        220,
        numinlets=1,
        numoutlets=3,
        items=["Internal Manual", ",", "Internal Auto", ",", "External vss.input"],
    )
    mode_select = p.new("expr 1 + ($i1 == 2)", 260, 165, 145, numinlets=1, numoutlets=1)
    auto_mode = p.new("== 1", 260, 205, 45, numinlets=2, numoutlets=1)
    auto_named = p.new("prepend auto", 320, 205, 95, numinlets=1, numoutlets=1)
    drive = p.new("drive_simulator", 25, 375, 110, numinlets=1, numoutlets=1)
    external = p.new("r vss.input", 150, 375, 85, numinlets=0, numoutlets=1)
    selector = p.new("switch 2", 25, 420, 75, numinlets=3, numoutlets=1)
    engine = p.new("vehicle_engine~", 650, 880, 115, numinlets=1, numoutlets=2)
    p.connect(mode, mode_select)
    p.connect(mode, auto_mode)
    p.connect(load_off, mode)
    p.connect(mode_select, selector, 0, 0)
    p.connect(auto_mode, auto_named)
    p.connect(auto_named, drive)
    p.connect(drive, selector, 0, 1)
    p.connect(external, selector, 0, 2)
    p.connect(selector, engine)

    p.comment("Manual Throttle", 25, 245, 110)
    throttle = p.add("flonum", None, 25, 270, 75, numinlets=1, numoutlets=2)
    throttle_clip = p.new("clip 0. 1.", 25, 305, 75, numinlets=3, numoutlets=1)
    throttle_named = p.new("prepend throttle", 25, 340, 110, numinlets=1, numoutlets=1)
    p.connect(throttle, throttle_clip)
    p.connect(throttle_clip, throttle_named)
    p.connect(throttle_named, drive)
    p.comment("Manual Brake", 150, 245, 100)
    brake = p.add("flonum", None, 150, 270, 75, numinlets=1, numoutlets=2)
    brake_clip = p.new("clip 0. 1.", 150, 305, 75, numinlets=3, numoutlets=1)
    brake_named = p.new("prepend brake", 150, 340, 100, numinlets=1, numoutlets=1)
    p.connect(brake, brake_clip)
    p.connect(brake_clip, brake_named)
    p.connect(brake_named, drive)

    p.comment("Preset: Future EV / High-Rev V12 / Aggressive V10", 465, 135, 450)
    preset = p.add(
        "umenu",
        None,
        465,
        165,
        200,
        numinlets=1,
        numoutlets=3,
        items=["Future EV", ",", "High-Rev V12", ",", "Aggressive V10"],
    )
    preset_select = p.new("sel 0 1 2", 680, 165, 80, numinlets=1, numoutlets=4)
    presets = [
        "engine_type ev, ev_weight 1., v12_weight 0., v10_weight 0., aggression 0.25, brightness 0.72, body 0.34, texture 0.20, cabin_width 0.82, cabin_rumble 0., exhaust_boom 0., structure_vibration 0., master_trim_db -8.",
        "engine_type v12, ev_weight 0., v12_weight 1., v10_weight 0., aggression 0.62, brightness 0.78, body 0.72, texture 0.52, cabin_width 0.64, cabin_rumble 0.90, exhaust_boom 0.62, structure_vibration 0.58, master_trim_db -8.",
        "engine_type v10, ev_weight 0., v12_weight 0., v10_weight 1., aggression 0.90, brightness 0.66, body 0.84, texture 0.86, cabin_width 0.56, cabin_rumble 0.92, exhaust_boom 0.74, structure_vibration 0.72, master_trim_db -8.",
    ]
    for index, value in enumerate(presets):
        message = p.message(value, 465, 215 + index * 52, 760)
        p.connect(preset_select, message, index)
        p.connect(message, engine)
        p.connect(message, drive)
    preset_load = p.new("loadmess 0", 775, 165, 80, numinlets=1, numoutlets=1)
    p.connect(preset_load, preset)
    p.connect(preset, preset_select)

    weight_labels = (("EV Weight", "ev_weight"), ("V12 Weight", "v12_weight"), ("V10 Weight", "v10_weight"))
    for index, (label, name) in enumerate(weight_labels):
        add_labeled_number(p, label, name, 325 + index * 135, 400, engine)
    macros = (("Aggression", "aggression"), ("Brightness", "brightness"), ("Body", "body"), ("Texture", "texture"), ("Cabin Width", "cabin_width"))
    for index, (label, name) in enumerate(macros):
        add_labeled_number(p, label, name, 730 + index * 135, 400, engine)
    rumble_controls = (
        ("Cabin Rumble", "cabin_rumble"),
        ("Exhaust Boom", "exhaust_boom"),
        ("Structure Vibration", "structure_vibration"),
    )
    for index, (label, name) in enumerate(rumble_controls):
        add_labeled_number(p, label, name, 730 + index * 180, 470, engine)

    p.comment("Fuel lifecycle", 25, 530, 140)
    p.comment("Ignition", 25, 560, 75)
    ignition_toggle = p.add("toggle", None, 25, 586, 24, 24, numinlets=1, numoutlets=1)
    ignition_named = p.new("prepend ignition", 60, 586, 105, numinlets=1, numoutlets=1)
    p.comment("Engine Start", 190, 560, 100)
    start_button = p.add("button", None, 190, 586, 24, 24, numinlets=1, numoutlets=1)
    start_value = p.message("1", 225, 586, 30)
    start_named = p.new("prepend start", 270, 586, 90, numinlets=1, numoutlets=1)
    p.comment("Automatic mode uses profile-aware 7-speed DCT shift points", 390, 565, 410)
    p.connect(load_off, ignition_toggle)
    p.connect(ignition_toggle, ignition_named)
    p.connect(ignition_named, engine)
    p.connect(ignition_named, drive)
    p.connect(start_button, start_value)
    p.connect(start_value, start_named)
    p.connect(start_named, engine)
    p.connect(start_named, drive)

    p.comment("Global four-band EQ", 25, 650, 190)
    add_eq_band(p, "Low Shelf", "eq_low", 25, 680, 90.0, engine)
    add_eq_band(p, "Low-Mid", "eq_lowmid", 265, 680, 250.0, engine, q=0.8)
    add_eq_band(p, "High-Mid", "eq_highmid", 515, 680, 3800.0, engine, q=1.0)
    add_eq_band(p, "High Shelf", "eq_high", 765, 680, 9000.0, engine)
    p.comment("EQ Bypass", 1010, 680, 90)
    eq_bypass = p.add("toggle", None, 1010, 708, 24, 24, numinlets=1, numoutlets=1)
    eq_bypass_named = p.new("prepend eq_bypass", 1045, 708, 120, numinlets=1, numoutlets=1)
    p.comment("Master Trim (dB)", 1200, 680, 125)
    trim = p.add("flonum", None, 1200, 708, 70, numinlets=1, numoutlets=2)
    trim_clip = p.new("clip -24. 0.", 1200, 742, 85, numinlets=3, numoutlets=1)
    trim_named = p.new("prepend master_trim_db", 1200, 776, 155, numinlets=1, numoutlets=1)
    trim_default = p.new("loadmess -7.", 1300, 708, 95, numinlets=1, numoutlets=1)
    p.connect(load_off, eq_bypass)
    p.connect(eq_bypass, eq_bypass_named)
    p.connect(eq_bypass_named, engine)
    p.connect(trim, trim_clip)
    p.connect(trim_clip, trim_named)
    p.connect(trim_named, engine)
    p.connect(trim_default, trim)

    mute_l = p.new("*~", 650, 925, 40, numinlets=2, numoutlets=1)
    mute_r = p.new("*~", 790, 925, 40, numinlets=2, numoutlets=1)
    p.comment("Stereo meter~ and spectroscope~ monitoring", 925, 875, 315)
    meter_l = p.add("meter~", None, 650, 975, 65, numinlets=1, numoutlets=1)
    meter_r = p.add("meter~", None, 790, 975, 65, numinlets=1, numoutlets=1)
    spectrum_l = p.add("spectroscope~", None, 925, 925, 105, numinlets=2, numoutlets=1)
    spectrum_r = p.add("spectroscope~", None, 1045, 925, 105, numinlets=2, numoutlets=1)
    dac = p.add("ezdac~", None, 720, 1040, 65, 48, numinlets=2, numoutlets=0)
    p.connect(audio_toggle, dac)
    p.connect(engine, mute_l, 0, 0)
    p.connect(engine, mute_r, 1, 0)
    p.connect(audio_line, mute_l, 0, 1)
    p.connect(audio_line, mute_r, 0, 1)
    p.connect(mute_l, meter_l)
    p.connect(mute_r, meter_r)
    p.connect(mute_l, spectrum_l)
    p.connect(mute_r, spectrum_r)
    p.connect(mute_l, dac, 0, 0)
    p.connect(mute_r, dac, 0, 1)
    return p.document(presentation=False)


GEN_CODE = {
    "ev_powertrain": """// Smooth, bounded EV inverter/motor identity.\nParam rpm(650, min=0, max=10000);\nParam throttle(0, min=0, max=1);\nParam load(0, min=-1, max=1);\nParam aggression(0.25, min=0, max=1);\nParam brightness(0.7, min=0, max=1);\nParam body(0.35, min=0, max=1);\nParam texture(0.2, min=0, max=1);\nr = slide(clamp(rpm, 0, 10000), 1200, 1800);\nt = slide(clamp(throttle, 0, 1), 700, 1400);\nf = clamp(55 + r * 0.052, 55, 760);\na = clamp(0.03 + t * 0.25 + abs(clamp(load, -1, 1)) * 0.08, 0, 0.42);\ncore = cycle(f) * (0.60 + body * 0.20);\ninverter = cycle(clamp(f * (2.8 + brightness), 100, 4200)) * (0.12 + texture * 0.18);\nair = cycle(clamp(f * 1.013, 55, 1000)) * aggression * 0.10;\nsig = clamp((core + inverter + air) * a, -0.78, 0.78);\nout1 = sig;\nout2 = clamp((cycle(f * 1.007) * 0.55 + inverter + air) * a, -0.78, 0.78);""",
    "v12_powertrain": """// Lifecycle-gated four-stroke V12 with idle body and load-dependent harmonic lift.\nParam rpm(780, min=0, max=10000);\nParam throttle(0, min=0, max=1);\nParam load(0, min=-1, max=1);\nParam aggression(0.6, min=0, max=1);\nParam brightness(0.75, min=0, max=1);\nParam body(0.7, min=0, max=1);\nParam texture(0.5, min=0, max=1);\nParam engine_running(0, min=0, max=1);\nParam combustion_gain(0, min=0, max=1);\nParam shift_cut(1, min=0, max=1);\nr = slide(clamp(rpm, 0, 10000), 700, 1100);\nt = slide(clamp(throttle, 0, 1), 420, 850);\nl = max(clamp(load, -1, 1), 0);\nrun = slide(clamp(engine_running * combustion_gain * shift_cut, 0, 1), 480, 1900);\nspeedmix = clamp((r - 780) / 8220, 0, 1);\nrough = 1 + cycle(1.31) * (0.004 * (1-speedmix)) + cycle(2.17) * 0.0015;\nf = clamp(r / 60 * 6 * rough, 35, 1000);\nidle = 0.145 + body * 0.035;\na = clamp(idle + t * 0.26 + l * 0.13, 0, 0.56) * run;\nsub = cycle(clamp(f * 0.5, 24, 520)) * (0.34 + body * 0.24) * (1-speedmix*0.45);\nfund = cycle(f) * (0.58 + body * 0.12);\nh2 = cycle(clamp(f * 2, 45, 3000)) * (0.16 + brightness * 0.18 + speedmix * 0.12);\nh3 = cycle(clamp(f * 3, 55, 5000)) * (0.07 + texture * 0.11 + speedmix * 0.12);\nh5 = cycle(clamp(f * 5, 70, 8000)) * (0.025 + brightness * speedmix * 0.10);\nh8 = cycle(clamp(f * 8, 90, 11000)) * (0.008 + texture * speedmix * 0.055);\nintake = cycle(clamp(f * 1.5, 45, 1800)) * t * (0.035 + texture * 0.055);\nleft = (sub + fund + h2 + h3 + h5 + h8 + intake) * a * (0.82 + aggression * 0.15);\nright = (cycle(clamp(f * 0.5015, 24, 520)) * (0.32 + body*0.22) * (1-speedmix*0.45) + cycle(f * 0.9985) * 0.58 + h2*0.96 + h3*1.03 + h5*0.98 + h8*1.04 + intake) * a * (0.82 + aggression*0.15);\nout1 = clamp(left, -0.86, 0.86);\nout2 = clamp(right, -0.86, 0.86);""",
    "v10_powertrain": """// Lifecycle-gated four-stroke V10 with stronger half-order rumble and uneven sidebands.\nParam rpm(850, min=0, max=10000);\nParam throttle(0, min=0, max=1);\nParam load(0, min=-1, max=1);\nParam aggression(0.9, min=0, max=1);\nParam brightness(0.65, min=0, max=1);\nParam body(0.85, min=0, max=1);\nParam texture(0.85, min=0, max=1);\nParam engine_running(0, min=0, max=1);\nParam combustion_gain(0, min=0, max=1);\nParam shift_cut(1, min=0, max=1);\nr = slide(clamp(rpm, 0, 10000), 620, 980);\nt = slide(clamp(throttle, 0, 1), 360, 760);\nl = max(clamp(load, -1, 1), 0);\nrun = slide(clamp(engine_running * combustion_gain * shift_cut, 0, 1), 420, 1650);\nspeedmix = clamp((r - 850) / 7650, 0, 1);\nrough = 1 + cycle(0.93) * (0.008 * (1-speedmix)) + cycle(1.71) * 0.003;\nf = clamp(r / 60 * 5 * rough, 32, 850);\nidle = 0.165 + body * 0.04;\na = clamp(idle + t * 0.29 + l * 0.15, 0, 0.60) * run;\nsub = cycle(clamp(f * 0.5, 24, 450)) * (0.42 + body * 0.24) * (1-speedmix*0.38);\nfire = cycle(f) * (0.50 + aggression * 0.16);\nside = cycle(clamp(f * 1.5, 48, 1900)) * (0.06 + texture * 0.10);\nh2 = cycle(clamp(f * 2, 55, 3400)) * (0.11 + brightness * 0.14);\nrasp = cycle(clamp(f * 2.5, 65, 5000)) * (0.08 + texture * 0.17 + speedmix * 0.10);\nmetal = cycle(clamp(f * 5, 90, 8500)) * brightness * speedmix * 0.075;\nleft = (sub + fire + side + h2 + rasp + metal) * a;\nright = (cycle(clamp(f * 0.503, 24, 450)) * (0.40 + body*0.22) * (1-speedmix*0.38) + cycle(f*0.997)*0.50 + side*1.08 + h2*0.94 + rasp*1.06 + metal) * a;\nout1 = clamp(left, -0.88, 0.88);\nout2 = clamp(right, -0.88, 0.88);""",
    "cabin_rumble": """// Strong but bounded in-cabin combustion rumble with centered low-frequency output.\nParam firing_order(0, min=0, max=6);\nParam rpm(780, min=0, max=10000);\nParam throttle(0, min=0, max=1);\nParam load(0, min=-1, max=1);\nParam gear(1, min=1, max=7);\nParam engine_running(0, min=0, max=1);\nParam combustion_gain(0, min=0, max=1);\nParam shift_cut(1, min=0, max=1);\nParam cabin_rumble(0, min=0, max=1);\nParam exhaust_boom(0, min=0, max=1);\nParam structure_vibration(0, min=0, max=1);\nParam body(0.7, min=0, max=1);\nParam aggression(0.6, min=0, max=1);\nr = slide(clamp(rpm, 0, 10000), 700, 1200);\nt = slide(clamp(throttle, 0, 1), 420, 900);\nl = max(clamp(load, -1, 1), 0);\ng = clamp(gear, 1, 7);\norder = clamp(firing_order, 0, 6);\nfuel = clamp(order / 5, 0, 1);\nrun = slide(clamp(engine_running * combustion_gain, 0, 1), 360, 2200);\nshift = slide(clamp(0.35 + 0.65 * shift_cut, 0, 1), 150, 1100);\nfire_hz = clamp(r / 60 * order, 28, 1000);\nhalf_hz = clamp(fire_hz * 0.5, 28, 420);\nspeedmix = clamp((r - 780) / 8220, 0, 1);\nidle_weight = 1 - speedmix * 0.55;\ndrive_weight = 0.45 + 0.55 * max(t, l);\ngear_weight = 0.86 + 0.02 * g;\nrough = 1 + cycle(1.17) * (0.006 * idle_weight) + cycle(2.03) * 0.002;\nmount = (cycle(half_hz * rough) * 0.72 + cycle(clamp(half_hz * 1.5, 35, 630)) * 0.18) * structure_vibration * (0.055 + body * 0.045) * idle_weight;\nmode_pulse = 0.62 + 0.38 * abs(cycle(clamp(fire_hz * 0.5, 28, 500)));\nmode1 = cycle(clamp(48 + (half_hz - 39) * 0.10, 44, 54)) * 0.45;\nmode2 = cycle(clamp(68 + (half_hz - 39) * 0.08, 63, 74)) * 0.33;\nmode3 = cycle(clamp(92 + (half_hz - 39) * 0.06, 86, 100)) * 0.20;\nmode4 = cycle(clamp(118 + (half_hz - 39) * 0.04, 110, 126)) * 0.12;\ncabin = (mode1 + mode2 + mode3 + mode4) * mode_pulse * cabin_rumble * (0.025 + body * 0.020) * (0.70 + idle_weight * 0.30);\nexhaust = (cycle(half_hz) * 0.65 + cycle(fire_hz) * 0.25 + cycle(clamp(fire_hz * 2, 56, 2000)) * 0.10) * exhaust_boom * (0.025 + t * 0.055 + l * 0.045) * (0.80 + aggression * 0.20);\nsig = clamp((mount + cabin + exhaust * drive_weight) * run * shift * gear_weight * fuel, -0.48, 0.48);\nout1 = sig;\nout2 = sig;""",
}


def make_gen(code: str) -> dict[str, Any]:
    return {
        "patcher": {
            "appversion": APP_VERSION,
            "boxes": [
                {
                    "box": {
                        "code": code,
                        "id": "obj-1",
                        "maxclass": "codebox",
                        "numinlets": 1,
                        "numoutlets": 2,
                        "outlettype": ["", ""],
                        "patching_rect": [40.0, 40.0, 760.0, 580.0],
                    }
                },
                {
                    "box": {
                        "id": "obj-2",
                        "maxclass": "newobj",
                        "numinlets": 1,
                        "numoutlets": 0,
                        "patching_rect": [40.0, 640.0, 45.0, 22.0],
                        "text": "out 1",
                    }
                },
                {
                    "box": {
                        "id": "obj-3",
                        "maxclass": "newobj",
                        "numinlets": 1,
                        "numoutlets": 0,
                        "patching_rect": [120.0, 640.0, 45.0, 22.0],
                        "text": "out 2",
                    }
                },
            ],
            "classnamespace": "dsp.gen",
            "fileversion": 1,
            "lines": [
                {"patchline": {"source": ["obj-1", 0], "destination": ["obj-2", 0]}},
                {"patchline": {"source": ["obj-1", 1], "destination": ["obj-3", 0]}},
            ],
            "rect": [50.0, 50.0, 850.0, 680.0],
        }
    }


PRESETS = {
    "Aggressive V10": {
        "engine_type": "v10",
        "aggression": 0.90,
        "body": 0.84,
        "brightness": 0.66,
        "cabin_width": 0.56,
        "cabin_rumble": 0.92,
        "exhaust_boom": 0.74,
        "structure_vibration": 0.72,
        "ev_weight": 0.0,
        "texture": 0.86,
        "v10_weight": 1.0,
        "v12_weight": 0.0,
        "master_trim_db": -8.0,
    },
    "Future EV": {
        "engine_type": "ev",
        "aggression": 0.25,
        "body": 0.34,
        "brightness": 0.72,
        "cabin_width": 0.82,
        "cabin_rumble": 0.0,
        "exhaust_boom": 0.0,
        "structure_vibration": 0.0,
        "ev_weight": 1.0,
        "texture": 0.20,
        "v10_weight": 0.0,
        "v12_weight": 0.0,
        "master_trim_db": -8.0,
    },
    "High-Rev V12": {
        "engine_type": "v12",
        "aggression": 0.62,
        "body": 0.72,
        "brightness": 0.78,
        "cabin_width": 0.64,
        "cabin_rumble": 0.90,
        "exhaust_boom": 0.62,
        "structure_vibration": 0.58,
        "ev_weight": 0.0,
        "texture": 0.52,
        "v10_weight": 0.0,
        "v12_weight": 1.0,
        "master_trim_db": -8.0,
    },
}


def wav_samples(name: str, frames: int, sample_rate: int = 48000) -> list[float]:
    seed = sum((index + 1) * ord(character) for index, character in enumerate(name))
    rng = random.Random(seed)
    suffix = name.rsplit("_", 1)[-1]
    variant = int(suffix) if suffix.isdigit() else 1
    values: list[float] = []
    noise_low = 0.0
    noise_mid = 0.0
    for index in range(frames):
        time = index / sample_rate
        noise_low += 0.16 * (rng.uniform(-1.0, 1.0) - noise_low)
        noise_mid += 0.34 * (rng.uniform(-1.0, 1.0) - noise_mid)
        if name.startswith("starter_"):
            attack = 1.0 - math.exp(-time * 45.0)
            envelope = attack * math.exp(-time * 2.8)
            profile = 1.0 if name.endswith("v12") else 0.92
            frequency = (46.0 + 78.0 * time) * profile
            value = envelope * (
                0.42 * math.sin(2.0 * math.pi * frequency * time)
                + 0.20 * math.sin(2.0 * math.pi * frequency * 2.03 * time)
                + 0.12 * noise_low
            )
        elif name == "shift_thump" or name.startswith("shift_up_"):
            envelope = math.exp(-time * (22.0 + variant))
            value = envelope * (
                0.62 * math.sin(2.0 * math.pi * (76.0 - 20.0 * time + variant * 2.0) * time)
                + 0.08 * noise_low
            )
        elif name.startswith("shift_down_"):
            envelope = math.exp(-time * (18.0 + variant))
            value = envelope * (
                0.54 * math.sin(2.0 * math.pi * (58.0 + variant * 3.0) * time)
                + 0.16 * math.sin(2.0 * math.pi * 132.0 * time)
                + 0.08 * noise_low
            )
        elif name.startswith("intake_backfire_"):
            envelope = (1.0 - math.exp(-time * 120.0)) * math.exp(-time * (12.0 + variant))
            value = envelope * (
                0.34 * noise_mid
                + 0.32 * math.sin(2.0 * math.pi * (185.0 + variant * 22.0) * time)
                + 0.15 * math.sin(2.0 * math.pi * 420.0 * time)
            )
        elif name == "exhaust_pop" or name.startswith("exhaust_pop_"):
            envelope = math.exp(-time * (28.0 + variant * 2.0))
            value = envelope * (
                0.46 * noise_low
                + 0.28 * math.sin(2.0 * math.pi * (92.0 + variant * 9.0) * time)
            )
        elif name.startswith("exhaust_crackle_"):
            envelope = math.exp(-time * (44.0 + variant * 4.0))
            value = envelope * (0.50 * noise_mid + 0.14 * math.sin(2.0 * math.pi * 155.0 * time))
        else:
            envelope = math.exp(-time * 150.0)
            value = envelope * (0.50 * rng.uniform(-1.0, 1.0) + 0.18 * math.sin(2.0 * math.pi * 1900.0 * time))
        values.append(max(-0.9, min(0.9, value)))
    return values


def write_wav(path: Path, name: str, frames: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    samples = wav_samples(name, frames)
    payload = b"".join(struct.pack("<h", round(sample * 32767.0)) for sample in samples)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(48000)
        handle.writeframes(payload)


def project_file() -> dict[str, Any]:
    contents: dict[str, dict[str, dict[str, Any]]] = {
        "patchers": {},
        "code": {},
        "media": {},
        "data": {},
    }
    patchers = [
        "main.maxpat",
        "patchers/vehicle_engine~.maxpat",
        "patchers/engine_controller.maxpat",
        "patchers/powertrain~.maxpat",
        "patchers/cabin_rumble~.maxpat",
        "patchers/transient~.maxpat",
        "patchers/road_air~.maxpat",
        "patchers/cabin_master~.maxpat",
        "patchers/mix_master~.maxpat",
        "patchers/drive_simulator.maxpat",
    ]
    for name in patchers:
        contents["patchers"][name] = {"kind": "patcher", "local": 1}
    for name in GEN_CODE:
        contents["code"][f"gen/{name}.gendsp"] = {"kind": "gendsp", "local": 1}
    for name in MEDIA_FRAMES:
        contents["media"][f"media/{name}.wav"] = {"kind": "mediafile", "local": 1}
    contents["data"]["presets/sound_dna.json"] = {"kind": "data", "local": 1}
    return {
        "autolocalize": 0,
        "autoorganize": 0,
        "contents": contents,
        "hideprojectwindow": 0,
        "name": PROJECT_NAME,
        # Max 8.6.x requires a dictionary here. Explicit ./-relative values
        # prevent common folder names such as patchers and media from resolving
        # to Max's built-in directories instead of this project.
        "searchpath": {
            name: {"path": f"./{name}", "recursive": 1}
            for name in ("patchers", "gen", "media", "presets")
        },
        "showdependencies": 1,
        "version": 1,
        "viewrect": [80.0, 80.0, 620.0, 780.0],
    }


def build_project(root: Path) -> None:
    outputs = {
        "main.maxpat": make_main(),
        "patchers/vehicle_engine~.maxpat": make_engine(),
        "patchers/engine_controller.maxpat": make_engine_controller(),
        "patchers/powertrain~.maxpat": make_powertrain(),
        "patchers/cabin_rumble~.maxpat": make_cabin_rumble(),
        "patchers/transient~.maxpat": make_transient(),
        "patchers/road_air~.maxpat": make_road_air(),
        "patchers/cabin_master~.maxpat": make_cabin_master(),
        "patchers/mix_master~.maxpat": make_mix_master(),
        "patchers/drive_simulator.maxpat": make_drive_simulator(),
        "presets/sound_dna.json": PRESETS,
        PROJECT_FILENAME: project_file(),
    }
    for relative_path, value in outputs.items():
        write_json(root / relative_path, value)
    for name, code in GEN_CODE.items():
        write_json(root / "gen" / f"{name}.gendsp", make_gen(code))
    for name, frames in MEDIA_FRAMES.items():
        write_wav(root / "media" / f"{name}.wav", name, frames)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Destination root (defaults to the repository root).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.output_root.resolve()
    build_project(root)
    print(f"Generated {PROJECT_NAME} project at {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
