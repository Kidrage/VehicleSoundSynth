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

STATE_NAMES = (
    "speed_kph",
    "rpm",
    "throttle",
    "brake",
    "load",
    "accel",
    "gear",
    "shift",
    "pop",
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
)
ALL_MESSAGES = STATE_NAMES + MACRO_NAMES


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
    p = Patcher(1050, 620)
    p.comment("vehicle_engine~ — public message seam and layered stereo renderer", 25, 15, 520)
    control = inlet(p, 45, 65)
    fan = p.new("t l l l l l", 45, 110, 95, numinlets=1, numoutlets=5)
    contract = route(p, ALL_MESSAGES, 165, 110, 790)
    p.comment("Contract monitor: every documented state and macro name is accepted", 165, 145, 490)
    power = p.new("powertrain~", 95, 220, 95, numinlets=1, numoutlets=2)
    transient = p.new("transient~", 285, 220, 90, numinlets=1, numoutlets=2)
    road = p.new("road_air~", 465, 220, 85, numinlets=1, numoutlets=2)
    cabin = p.new("cabin_master~", 690, 390, 110, numinlets=3, numoutlets=2)
    add_l1 = p.new("+~", 130, 310, 35, numinlets=2, numoutlets=1)
    add_l2 = p.new("+~", 235, 350, 35, numinlets=2, numoutlets=1)
    add_r1 = p.new("+~", 390, 310, 35, numinlets=2, numoutlets=1)
    add_r2 = p.new("+~", 495, 350, 35, numinlets=2, numoutlets=1)
    left = outlet(p, 700, 510, signal=True)
    right = outlet(p, 790, 510, signal=True)

    p.connect(control, fan)
    p.connect(fan, contract, 4)
    p.connect(fan, power, 3)
    p.connect(fan, transient, 2)
    p.connect(fan, road, 1)
    p.connect(fan, cabin, 0, 0)
    p.connect(power, add_l1, 0, 0)
    p.connect(transient, add_l1, 0, 1)
    p.connect(add_l1, add_l2, 0, 0)
    p.connect(road, add_l2, 0, 1)
    p.connect(power, add_r1, 1, 0)
    p.connect(transient, add_r1, 1, 1)
    p.connect(add_r1, add_r2, 0, 0)
    p.connect(road, add_r2, 1, 1)
    p.connect(add_l2, cabin, 0, 1)
    p.connect(add_r2, cabin, 0, 2)
    p.connect(cabin, left, 0)
    p.connect(cabin, right, 1)
    return p.document()


def make_powertrain() -> dict[str, Any]:
    p = Patcher(1280, 780)
    p.comment("Three bounded Gen powertrains, smoothed and continuously weighted", 25, 15, 500)
    control = inlet(p, 35, 65)
    names = ("rpm", "throttle", "load", "aggression", "brightness", "body", "texture", "ev_weight", "v12_weight", "v10_weight")
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
    for index, name in enumerate(names[:7]):
        low, high = bounds[name]
        x = 35 + index * 160
        bounded = p.new(f"clip {low:g} {high:g}", x, 175, 90, numinlets=3, numoutlets=1)
        named = p.message(f"{name} $1", x, 220, 105)
        p.connect(router, bounded, index)
        p.connect(bounded, named)
        for gen in gens:
            p.connect(named, gen)

    lines: list[str] = []
    for index, name in enumerate(names[7:]):
        x = 230 + index * 290
        bounded = p.new("clip 0. 1.", x, 285, 75, numinlets=3, numoutlets=1)
        packed = p.new("pack 0. 40", x, 320, 85, numinlets=2, numoutlets=1)
        smoothed = p.new("line~", x, 355, 50, numinlets=2, numoutlets=2)
        p.connect(router, bounded, index + 7)
        p.connect(bounded, packed)
        p.connect(packed, smoothed)
        lines.append(smoothed)

    defaults = [(1.0, lines[0]), (0.0, lines[1]), (0.0, lines[2])]
    for index, (value, destination) in enumerate(defaults):
        initial = p.new(f"loadmess {value:g}", 1030, 285 + index * 38, 80, numinlets=1, numoutlets=1)
        p.connect(initial, destination)

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


def make_transient() -> dict[str, Any]:
    p = Patcher(1040, 650)
    p.comment("Sample transients are optional; missing buffers never stop continuous layers", 25, 15, 520)
    control = inlet(p, 35, 60)
    router = route(p, ("shift", "pop", "click", "aggression", "texture"), 35, 100, 430)
    names = ("shift_thump", "exhaust_pop", "mechanical_click")
    players: list[str] = []
    gains = (0.50, 0.38, 0.24)
    for index, name in enumerate(names):
        x = 45 + index * 300
        buffer_box = p.new(f"buffer~ {name} media/{name}.wav", x, 175, 245, numinlets=1, numoutlets=2)
        select = p.new("sel 1", x, 220, 45, numinlets=1, numoutlets=2)
        start = p.message("start", x, 260, 45)
        player = p.new(f"play~ {name} 1", x, 305, 125, numinlets=1, numoutlets=2)
        gain = p.new(f"*~ {gains[index]:.2f}", x, 350, 65, numinlets=2, numoutlets=1)
        p.connect(router, select, index)
        p.connect(select, start)
        p.connect(start, player)
        p.connect(player, gain)
        players.append(gain)
        _ = buffer_box

    aggression_clip = p.new("clip 0. 1.", 690, 105, 75, numinlets=3, numoutlets=1)
    aggression_gain = p.new("expr 0.7 + 0.6*$f1", 690, 145, 145, numinlets=1, numoutlets=1)
    aggression_pack = p.new("pack 0. 25", 690, 185, 85, numinlets=2, numoutlets=1)
    aggression_line = p.new("line~", 690, 225, 50, numinlets=2, numoutlets=2)
    p.connect(router, aggression_clip, 3)
    p.connect(aggression_clip, aggression_gain)
    p.connect(aggression_gain, aggression_pack)
    p.connect(aggression_pack, aggression_line)
    default_gain = p.new("loadmess 1.", 815, 225, 85, numinlets=1, numoutlets=1)
    p.connect(default_gain, aggression_line)

    add1 = p.new("+~", 270, 430, 35, numinlets=2, numoutlets=1)
    add2 = p.new("+~", 440, 470, 35, numinlets=2, numoutlets=1)
    master = p.new("*~", 530, 510, 40, numinlets=2, numoutlets=1)
    left_gain = p.new("*~ 0.96", 450, 550, 65, numinlets=2, numoutlets=1)
    right_gain = p.new("*~ 0.88", 590, 550, 65, numinlets=2, numoutlets=1)
    left = outlet(p, 470, 600, signal=True)
    right = outlet(p, 610, 600, signal=True)
    p.connect(players[0], add1, 0, 0)
    p.connect(players[1], add1, 0, 1)
    p.connect(add1, add2, 0, 0)
    p.connect(players[2], add2, 0, 1)
    p.connect(add2, master, 0, 0)
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
    speed_curve = p.new("expr pow($f1/300., 0.7) * 0.32", 35, 195, 190, numinlets=1, numoutlets=1)
    speed_pack = p.new("pack 0. 120", 35, 235, 90, numinlets=2, numoutlets=1)
    speed_line = p.new("line~", 35, 275, 50, numinlets=2, numoutlets=2)
    bright_clip = p.new("clip 0. 1.", 285, 155, 75, numinlets=3, numoutlets=1)
    cutoff_expr = p.new("expr 700. + 6500.*$f1", 285, 195, 165, numinlets=1, numoutlets=1)
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
    for value, destination, x in ((0.0, speed_line, 550), (2600.0, cutoff_line, 670)):
        default = p.new(f"loadmess {value:g}", x, 275, 95, numinlets=1, numoutlets=1)
        p.connect(default, destination)

    channels: list[str] = []
    for index, x in enumerate((220, 610)):
        noise = p.new("noise~", x, 350, 55, numinlets=0, numoutlets=1)
        highpass = p.new("hip~ 65", x, 390, 65, numinlets=2, numoutlets=1)
        lowpass = p.new("lores~ 1800 0.65", x, 430, 120, numinlets=3, numoutlets=1)
        gain = p.new("*~", x, 475, 40, numinlets=2, numoutlets=1)
        stereo = p.new(f"*~ {0.96 - index * 0.05:.2f}", x, 520, 65, numinlets=2, numoutlets=1)
        p.connect(noise, highpass)
        p.connect(highpass, lowpass)
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
    p.comment("Cabin tone/width and conservative master protection", 25, 15, 470)
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
    side_width = p.new("*~", 400, 470, 40, numinlets=2, numoutlets=1)
    reconstruct_l = p.new("+~", 280, 520, 40, numinlets=2, numoutlets=1)
    reconstruct_r = p.new("-~", 520, 520, 40, numinlets=2, numoutlets=1)
    p.connect(left_in, mid_sum, 0, 0)
    p.connect(right_in, mid_sum, 0, 1)
    p.connect(mid_sum, mid)
    p.connect(left_in, side_diff, 0, 0)
    p.connect(right_in, side_diff, 0, 1)
    p.connect(side_diff, side)
    p.connect(side, side_width, 0, 0)
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
    limiter = p.new("omx.peaklim~", 475, 675, 105, numinlets=2, numoutlets=4)
    clip_l = p.new("clip~ -0.891 0.891", 300, 710, 130, numinlets=3, numoutlets=1)
    clip_r = p.new("clip~ -0.891 0.891", 650, 710, 130, numinlets=3, numoutlets=1)
    p.connect(masters[0], limiter, 0, 0)
    p.connect(masters[1], limiter, 0, 1)
    p.connect(limiter, clip_l, 0, 0)
    p.connect(limiter, clip_r, 1, 0)
    left = outlet(p, 430, 710, signal=True)
    right = outlet(p, 790, 710, signal=True)
    p.connect(clip_l, left)
    p.connect(clip_r, right)
    p.connect(control, router)
    return p.document()


def make_drive_simulator() -> dict[str, Any]:
    p = Patcher(1120, 720)
    p.comment("Internal drive simulator: manual pedals or deterministic auto cycle", 25, 15, 520)
    control = inlet(p, 35, 65)
    router = route(p, ("throttle", "brake", "auto"), 35, 105, 240)
    throttle_clip = p.new("clip 0. 1.", 35, 155, 75, numinlets=3, numoutlets=1)
    brake_clip = p.new("clip 0. 1.", 145, 155, 75, numinlets=3, numoutlets=1)
    auto_clip = p.new("clip 0 1", 255, 155, 65, numinlets=3, numoutlets=1)
    tick = p.new("qmetro 50", 420, 105, 75, numinlets=2, numoutlets=1)
    load = p.new("loadmess 1", 420, 65, 75, numinlets=1, numoutlets=1)
    counter = p.new("counter 0 399", 420, 155, 95, numinlets=5, numoutlets=4)
    state = p.new("pak 0. 0. 0 0", 250, 220, 105, numinlets=4, numoutlets=1)
    effective = p.new("expr if($f3 > 0.5, 0.55 + 0.4*sin($f4*0.0314159), $f1)", 250, 265, 360, numinlets=4, numoutlets=1)
    target_speed = p.new("expr max(0., min(300., $f1*260. - $f2*180.))", 250, 310, 315, numinlets=2, numoutlets=1)
    speed_smooth = p.new("slide 0. 3 12", 250, 350, 90, numinlets=3, numoutlets=1)
    speed_split = p.new("t f f f", 250, 395, 70, numinlets=1, numoutlets=3)
    rpm = p.new("expr min(10000., 650. + $f1*31. + $f2*1400.)", 410, 440, 300, numinlets=2, numoutlets=1)
    rpm_pack = p.new("pak 0. 0.", 410, 395, 75, numinlets=2, numoutlets=1)
    gear = p.new("expr if($f1 < 1., 0, min(6, int($f1/45.)+1))", 735, 395, 285, numinlets=1, numoutlets=1)
    gear_change = p.new("change", 735, 440, 55, numinlets=1, numoutlets=1)
    gear_trigger = p.new("t b i", 735, 480, 50, numinlets=1, numoutlets=2)
    shift_on = p.message("shift 1", 690, 525, 55)
    shift_delay = p.new("delay 80", 805, 525, 65, numinlets=2, numoutlets=1)
    shift_off = p.message("shift 0", 805, 565, 55)
    output = outlet(p, 550, 660)

    p.connect(control, router)
    p.connect(router, throttle_clip, 0)
    p.connect(router, brake_clip, 1)
    p.connect(router, auto_clip, 2)
    p.connect(throttle_clip, state, 0, 0)
    p.connect(brake_clip, state, 0, 1)
    p.connect(auto_clip, state, 0, 2)
    p.connect(load, tick)
    p.connect(tick, counter)
    p.connect(counter, state, 0, 3)
    p.connect(state, effective)
    p.connect(effective, target_speed, 0, 0)
    p.connect(brake_clip, target_speed, 0, 1)
    p.connect(target_speed, speed_smooth)
    p.connect(speed_smooth, speed_split)
    p.connect(speed_split, rpm_pack, 1, 0)
    p.connect(effective, rpm_pack, 0, 1)
    p.connect(rpm_pack, rpm)
    p.connect(speed_split, gear, 2)
    p.connect(gear, gear_change)
    p.connect(gear_change, gear_trigger)
    p.connect(gear_trigger, shift_on, 0)
    p.connect(gear_trigger, shift_delay, 0)
    p.connect(shift_delay, shift_off)

    named_sources = [
        (speed_split, 0, "prepend speed_kph", 250, 485),
        (rpm, 0, "prepend rpm", 410, 485),
        (effective, 0, "prepend throttle", 35, 395),
        (brake_clip, 0, "prepend brake", 35, 440),
        (effective, 0, "expr max(-1., min(1., $f1*1.6))", 35, 485),
        (effective, 0, "expr max(-1., min(1., $f1*2.-$f2*2.))", 35, 530),
        (gear_trigger, 1, "prepend gear", 735, 610),
    ]
    for index, (source, source_outlet, text, x, y) in enumerate(named_sources):
        object_box = p.new(text, x, y, 185 if text.startswith("expr") else 115, numinlets=2 if index == 5 else 1, numoutlets=1)
        p.connect(source, object_box, source_outlet)
        if index == 5:
            p.connect(brake_clip, object_box, 0, 1)
            named = p.new("prepend accel", x, y + 38, 95, numinlets=1, numoutlets=1)
            p.connect(object_box, named)
            p.connect(named, output)
        elif index == 4:
            named = p.new("prepend load", x, y + 38, 90, numinlets=1, numoutlets=1)
            p.connect(object_box, named)
            p.connect(named, output)
        else:
            p.connect(object_box, output)
    p.connect(shift_on, output)
    p.connect(shift_off, output)
    return p.document()


def add_labeled_number(p: Patcher, label: str, name: str, x: float, y: float, engine: str) -> None:
    p.comment(label, x, y, 110)
    number = p.add("flonum", None, x, y + 24, 75, numinlets=1, numoutlets=2)
    bounded = p.new("clip 0. 1.", x, y + 58, 75, numinlets=3, numoutlets=1)
    named = p.new(f"prepend {name}", x, y + 92, 110, numinlets=1, numoutlets=1)
    p.connect(number, bounded)
    p.connect(bounded, named)
    p.connect(named, engine)


def make_main() -> dict[str, Any]:
    p = Patcher(1420, 900)
    p.comment("VehicleSoundSynth — morphable procedural vehicle acoustics", 25, 15, 600)
    p.comment("Audio starts OFF — lower your monitoring level, then enable DSP", 25, 45, 520)
    load_off = p.new("loadmess 0", 25, 80, 80, numinlets=1, numoutlets=1)
    audio_toggle = p.add("toggle", None, 120, 80, 24, 24, numinlets=1, numoutlets=1)
    dsp_message = p.message("; dsp $1", 160, 80, 60)
    ramp_message = p.message("$1 60", 235, 80, 55)
    audio_line = p.new("line~", 305, 80, 50, numinlets=2, numoutlets=2)
    p.connect(load_off, audio_toggle)
    p.connect(audio_toggle, dsp_message)
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
    mode_select = p.new("expr if($i1 == 2, 2, 1)", 260, 165, 160, numinlets=1, numoutlets=1)
    auto_mode = p.new("== 1", 260, 205, 45, numinlets=2, numoutlets=1)
    auto_named = p.new("prepend auto", 320, 205, 95, numinlets=1, numoutlets=1)
    drive = p.new("drive_simulator", 25, 375, 110, numinlets=1, numoutlets=1)
    external = p.new("r vss.input", 150, 375, 85, numinlets=0, numoutlets=1)
    selector = p.new("selector 2", 25, 420, 75, numinlets=3, numoutlets=1)
    engine = p.new("vehicle_engine~", 550, 620, 115, numinlets=1, numoutlets=2)
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
        "ev_weight 1., v12_weight 0., v10_weight 0., aggression 0.25, brightness 0.72, body 0.34, texture 0.20, cabin_width 0.82",
        "ev_weight 0., v12_weight 1., v10_weight 0., aggression 0.62, brightness 0.78, body 0.72, texture 0.52, cabin_width 0.64",
        "ev_weight 0., v12_weight 0., v10_weight 1., aggression 0.90, brightness 0.66, body 0.84, texture 0.86, cabin_width 0.56",
    ]
    for index, value in enumerate(presets):
        message = p.message(value, 465, 215 + index * 52, 760)
        p.connect(preset_select, message, index)
        p.connect(message, engine)
    preset_load = p.new("loadmess 0", 775, 165, 80, numinlets=1, numoutlets=1)
    p.connect(preset_load, preset)
    p.connect(preset, preset_select)

    weight_labels = (("EV Weight", "ev_weight"), ("V12 Weight", "v12_weight"), ("V10 Weight", "v10_weight"))
    for index, (label, name) in enumerate(weight_labels):
        add_labeled_number(p, label, name, 325 + index * 135, 400, engine)
    macros = (("Aggression", "aggression"), ("Brightness", "brightness"), ("Body", "body"), ("Texture", "texture"), ("Cabin Width", "cabin_width"))
    for index, (label, name) in enumerate(macros):
        add_labeled_number(p, label, name, 730 + index * 135, 400, engine)

    mute_l = p.new("*~", 550, 675, 40, numinlets=2, numoutlets=1)
    mute_r = p.new("*~", 690, 675, 40, numinlets=2, numoutlets=1)
    p.comment("Stereo meter~ and spectroscope~ monitoring", 825, 640, 315)
    meter_l = p.add("meter~", None, 550, 725, 65, numinlets=1, numoutlets=1)
    meter_r = p.add("meter~", None, 690, 725, 65, numinlets=1, numoutlets=1)
    spectrum_l = p.add("spectroscope~", None, 825, 675, 105, numinlets=2, numoutlets=1)
    spectrum_r = p.add("spectroscope~", None, 945, 675, 105, numinlets=2, numoutlets=1)
    dac = p.add("ezdac~", None, 620, 790, 65, 48, numinlets=2, numoutlets=0)
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
    "v12_powertrain": """// Smooth, bounded high-rev twelve-cylinder firing model.\nParam rpm(650, min=0, max=10000);\nParam throttle(0, min=0, max=1);\nParam load(0, min=-1, max=1);\nParam aggression(0.6, min=0, max=1);\nParam brightness(0.75, min=0, max=1);\nParam body(0.7, min=0, max=1);\nParam texture(0.5, min=0, max=1);\nr = slide(clamp(rpm, 0, 10000), 1000, 1600);\nt = slide(clamp(throttle, 0, 1), 650, 1200);\nf = clamp(r / 60 * 6, 35, 1000);\na = clamp(0.025 + t * 0.30 + max(clamp(load, -1, 1), 0) * 0.10, 0, 0.46);\nfund = cycle(f) * (0.38 + body * 0.18);\nh2 = cycle(clamp(f * 2, 40, 4000)) * (0.20 + brightness * 0.12);\nh3 = cycle(clamp(f * 3, 50, 6500)) * (0.09 + texture * 0.12);\nsig = clamp((fund + h2 + h3) * a * (0.85 + aggression * 0.18), -0.80, 0.80);\nout1 = sig;\nout2 = clamp((cycle(f * 0.997) * 0.40 + h2 * 0.95 + h3 * 1.04) * a, -0.80, 0.80);""",
    "v10_powertrain": """// Smooth, bounded cross-plane-inspired ten-cylinder identity.\nParam rpm(650, min=0, max=10000);\nParam throttle(0, min=0, max=1);\nParam load(0, min=-1, max=1);\nParam aggression(0.9, min=0, max=1);\nParam brightness(0.65, min=0, max=1);\nParam body(0.85, min=0, max=1);\nParam texture(0.85, min=0, max=1);\nr = slide(clamp(rpm, 0, 10000), 850, 1300);\nt = slide(clamp(throttle, 0, 1), 500, 900);\nf = clamp(r / 60 * 5, 32, 850);\na = clamp(0.03 + t * 0.33 + max(clamp(load, -1, 1), 0) * 0.12, 0, 0.48);\nlow = cycle(f * 0.5) * (0.22 + body * 0.22);\nfire = cycle(f) * (0.34 + aggression * 0.16);\nrasp = cycle(clamp(f * 2.5, 55, 5000)) * (0.10 + texture * 0.18 + brightness * 0.06);\nsig = clamp((low + fire + rasp) * a, -0.82, 0.82);\nout1 = sig;\nout2 = clamp((cycle(f * 0.503) * 0.32 + fire * 0.96 + rasp * 1.08) * a, -0.82, 0.82);""",
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
                }
            ],
            "classnamespace": "dsp.gen",
            "fileversion": 1,
            "lines": [],
            "rect": [50.0, 50.0, 850.0, 680.0],
        }
    }


PRESETS = {
    "Aggressive V10": {
        "aggression": 0.90,
        "body": 0.84,
        "brightness": 0.66,
        "cabin_width": 0.56,
        "ev_weight": 0.0,
        "texture": 0.86,
        "v10_weight": 1.0,
        "v12_weight": 0.0,
    },
    "Future EV": {
        "aggression": 0.25,
        "body": 0.34,
        "brightness": 0.72,
        "cabin_width": 0.82,
        "ev_weight": 1.0,
        "texture": 0.20,
        "v10_weight": 0.0,
        "v12_weight": 0.0,
    },
    "High-Rev V12": {
        "aggression": 0.62,
        "body": 0.72,
        "brightness": 0.78,
        "cabin_width": 0.64,
        "ev_weight": 0.0,
        "texture": 0.52,
        "v10_weight": 0.0,
        "v12_weight": 1.0,
    },
}


def wav_samples(name: str, frames: int, sample_rate: int = 48000) -> list[float]:
    rng = random.Random({"shift_thump": 1229, "exhaust_pop": 7717, "mechanical_click": 31337}[name])
    values: list[float] = []
    for index in range(frames):
        time = index / sample_rate
        if name == "shift_thump":
            envelope = math.exp(-time * 24.0)
            value = 0.64 * envelope * math.sin(2.0 * math.pi * (72.0 - 18.0 * time) * time)
        elif name == "exhaust_pop":
            envelope = math.exp(-time * 34.0)
            value = envelope * (0.46 * rng.uniform(-1.0, 1.0) + 0.24 * math.sin(2.0 * math.pi * 118.0 * time))
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
    contents: dict[str, dict[str, Any]] = {}
    patchers = [
        "main.maxpat",
        "patchers/vehicle_engine~.maxpat",
        "patchers/powertrain~.maxpat",
        "patchers/transient~.maxpat",
        "patchers/road_air~.maxpat",
        "patchers/cabin_master~.maxpat",
        "patchers/drive_simulator.maxpat",
    ]
    for name in patchers:
        contents[name] = {"kind": "patcher", "local": 1}
    for name in GEN_CODE:
        contents[f"gen/{name}.gendsp"] = {"kind": "gendsp", "local": 1}
    for name in ("shift_thump.wav", "exhaust_pop.wav", "mechanical_click.wav"):
        contents[f"media/{name}"] = {"kind": "mediafile", "local": 1}
    contents["presets/sound_dna.json"] = {"kind": "data", "local": 1}
    return {
        "autolocalize": 0,
        "autoorganize": 0,
        "contents": contents,
        "hideprojectwindow": 0,
        "name": "VehicleSoundSynth",
        # Max 8.6.x deserializes this field as a dictionary. Supplying a JSON
        # array crashes project_deserialize_searchpath before the project opens.
        # Project-local folders and their subfolders are searched automatically.
        "searchpath": {},
        "showdependencies": 1,
        "version": 1,
        "viewrect": [80.0, 80.0, 620.0, 780.0],
    }


def build_project(root: Path) -> None:
    outputs = {
        "main.maxpat": make_main(),
        "patchers/vehicle_engine~.maxpat": make_engine(),
        "patchers/powertrain~.maxpat": make_powertrain(),
        "patchers/transient~.maxpat": make_transient(),
        "patchers/road_air~.maxpat": make_road_air(),
        "patchers/cabin_master~.maxpat": make_cabin_master(),
        "patchers/drive_simulator.maxpat": make_drive_simulator(),
        "presets/sound_dna.json": PRESETS,
        "VehicleSoundSynth.maxproj": project_file(),
    }
    for relative_path, value in outputs.items():
        write_json(root / relative_path, value)
    for name, code in GEN_CODE.items():
        write_json(root / "gen" / f"{name}.gendsp", make_gen(code))
    for name, frames in (("shift_thump", 9600), ("exhaust_pop", 7200), ("mechanical_click", 2400)):
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
    print(f"Generated VehicleSoundSynth project at {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
