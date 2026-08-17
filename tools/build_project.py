#!/usr/bin/env python3
"""Deterministically generate the VehicleSoundSynth Max project and media."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import random
import re
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
PROJECT_NAME = "VehicleSoundSynth-V4"
PROJECT_FILENAME = f"{PROJECT_NAME}.maxproj"
BEAP_CLIPPING_ROOT = Path(
    "/Applications/Max.app/Contents/Resources/C74/packages/BEAP/clippings/BEAP"
)
BEAP_CLIPPING_SHA256 = {
    "Oscillator/bp.Oscillator.maxpat": "b911b4447ae94090f1e64582eca1e761e7a3593d5d9852369e4644a1a42efc2b",
    "Mixers/bp.Audio Mixer.maxpat": "e63e00727b7bd5bf8b5aa8119dc276578ba9122e7e282040364aa82435061ce5",
    "Filter/bp.Ladder.maxpat": "1292c18863374400f4f1924939c3321fb66c0f04dae357184a373f819be3c380",
    "Envelope/bp.ADSR.maxpat": "86e9594b9aa21a6794eb544f3ecb9730d2154e60acefdbc903f06c30fe4231dd",
    "Level/bp.VCA.maxpat": "aa62bb0c452f34fb7f326b7a9ca74db9f5c85f7dfde5898d13e1ba96255b74ed",
}

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
    "cabin_ir_mix",
    "powertrain_level_db",
    "transient_level_db",
    "road_level_db",
    "rumble_level_db",
    "pad_level_db",
    "pad_mute",
    "pad_solo",
    "reference_texture_level_db",
    "reference_texture_mute",
    "eq_low",
    "eq_lowmid",
    "eq_highmid",
    "eq_high",
    "eq_bypass",
    "master_trim_db",
)
ALL_MESSAGES = STATE_NAMES + MACRO_NAMES

MEDIA_FRAMES = {
    "cabin_ir_l": 4096,
    "cabin_ir_r": 4096,
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
ENGINE_TEXTURE_FILES = tuple(
    f"engine_texture_{anchor}_{variant}.wav"
    for anchor in ("065", "110", "180", "260", "380", "520")
    for variant in ("a", "b")
)

def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class Patcher:
    """Small builder that makes port counts and patch-cord references explicit."""

    def __init__(self, width: float = 1100.0, height: float = 760.0) -> None:
        self.boxes: list[dict[str, Any]] = []
        self.lines: list[dict[str, Any]] = []
        self.parameters: dict[str, Any] = {}
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

    def embedded_bpatcher(
        self,
        template: dict[str, Any],
        source_parameters: dict[str, Any],
        x: float,
        y: float,
        varname: str,
    ) -> str:
        box = copy.deepcopy(template)
        source_id = box["id"]
        box_id = f"obj-{self._next_id}"
        self._next_id += 1
        width, height = box["patching_rect"][2:4]
        box["id"] = box_id
        box["patching_rect"] = [float(x), float(y), float(width), float(height)]
        box["varname"] = varname
        self.boxes.append({"box": box})
        for key, value in source_parameters.items():
            if key == "parameterbanks" or not key.startswith(f"{source_id}::"):
                continue
            localized = copy.deepcopy(value)
            localized[0] = f"{varname}.{localized[0]}"
            localized[1] = f"{varname}.{localized[1]}"
            self.parameters[f"{box_id}{key[len(source_id):]}"] = localized
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
        document = {
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
        if self.parameters:
            document["patcher"]["parameters"] = {
                **self.parameters,
                "parameterbanks": {},
            }
        return document


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


def _set_beap_initial(box: dict[str, Any], varname: str, value: float | int) -> None:
    matches = 0
    restore_matches = 0

    def visit(item: Any) -> None:
        nonlocal matches, restore_matches
        if isinstance(item, dict):
            if item.get("varname") == varname:
                attributes = item.setdefault("saved_attribute_attributes", {}).setdefault(
                    "valueof", {}
                )
                attributes["parameter_initial"] = [value]
                attributes["parameter_initial_enable"] = 1
                matches += 1
            restore = item.get("restore")
            if isinstance(restore, dict) and varname in restore:
                restore[varname] = [value]
                restore_matches += 1
            for child in item.values():
                visit(child)
        elif isinstance(item, list):
            for child in item:
                visit(child)

    visit(box)
    if matches != 1:
        raise ValueError(f"Expected one BEAP parameter {varname!r}, found {matches}")
    if restore_matches != 1:
        raise ValueError(
            f"Expected one BEAP restore value {varname!r}, found {restore_matches}"
        )


def add_beap_module(
    patch: Patcher,
    relative_path: str,
    x: float,
    y: float,
    varname: str,
    *,
    initial: dict[str, float | int] | None = None,
) -> str:
    clipping = BEAP_CLIPPING_ROOT / relative_path
    if not clipping.is_file():
        raise FileNotFoundError(
            f"BEAP clipping not found: {clipping}. Install Max 8.6.5 with BEAP."
        )
    payload = clipping.read_bytes()
    expected_digest = BEAP_CLIPPING_SHA256[relative_path]
    actual_digest = hashlib.sha256(payload).hexdigest()
    if actual_digest != expected_digest:
        raise RuntimeError(
            f"Unsupported BEAP clipping revision: {clipping} "
            f"(expected Max 8.6.5 SHA-256 {expected_digest}, got {actual_digest})"
        )
    document = json.loads(payload)["patcher"]
    box = copy.deepcopy(document["boxes"][0]["box"])
    for parameter, value in (initial or {}).items():
        _set_beap_initial(box, parameter, value)
    return patch.embedded_bpatcher(
        box,
        document.get("parameters", {}),
        x,
        y,
        varname,
    )


def make_ev_pad_beap() -> dict[str, Any]:
    """Seed a user-editable dual-mono BEAP pad; never overwrite it after creation."""
    p = Patcher(1780, 790)
    p.comment(
        "USER-TUNABLE EV PAD — two independent BEAP chains; this file is preserved on rebuild",
        25,
        15,
        900,
    )
    pitch_cv = inlet(p, 45, 60, signal=True)
    gate_cv = inlet(p, 145, 60, signal=True)
    throttle_cv = inlet(p, 245, 60, signal=True)
    p.comment("Pitch CV (1V/oct)", 25, 95, 125)
    p.comment("Gate (0/5V)", 145, 95, 100)
    p.comment("Throttle CV", 260, 95, 100)

    root_pitch = p.new("+~ 1.", 380, 75, 55, numinlets=2, numoutlets=1)
    # One octave plus log2(3/2): an exact fifth, so shared harmonics remain
    # locked instead of producing a slow equal-temperament beat.
    fifth_pitch = p.new("+~ 1.5849625", 465, 75, 90, numinlets=2, numoutlets=1)
    filter_cv_offset = p.new("-~ 0.75", 590, 75, 70, numinlets=2, numoutlets=1)
    filter_cv = p.new("*~ 0.666667", 675, 75, 85, numinlets=2, numoutlets=1)
    p.connect(pitch_cv, root_pitch)
    p.connect(pitch_cv, fifth_pitch)
    p.connect(throttle_cv, filter_cv_offset)
    p.connect(filter_cv_offset, filter_cv)

    channel_specs = (
        ("L", 140.0, 1, 0),
        ("R", 430.0, 0, 1),
    )
    for channel, y, first_waveform, second_waveform in channel_specs:
        p.comment(f"{channel} CHANNEL", 25, y - 25, 110)
        osc_a = add_beap_module(
            p,
            "Oscillator/bp.Oscillator.maxpat",
            25,
            y,
            f"{channel}_Osc_A",
            initial={"Waveform": first_waveform},
        )
        osc_b = add_beap_module(
            p,
            "Oscillator/bp.Oscillator.maxpat",
            355,
            y,
            f"{channel}_Osc_B",
            initial={"Waveform": second_waveform},
        )
        mixer = add_beap_module(
            p,
            "Mixers/bp.Audio Mixer.maxpat",
            685,
            y,
            f"{channel}_Mixer",
            initial={"in1": -15, "in2": -18},
        )
        ladder = add_beap_module(
            p,
            "Filter/bp.Ladder.maxpat",
            910,
            y,
            f"{channel}_Ladder",
            initial={"Freq": 1200, "Res": 8},
        )
        envelope = add_beap_module(
            p,
            "Envelope/bp.ADSR.maxpat",
            1225,
            y,
            f"{channel}_ADSR",
            initial={"Attack": 450, "Decay": 1000, "Sustain": 70, "Release": 1600},
        )
        vca = add_beap_module(
            p,
            "Level/bp.VCA.maxpat",
            1480,
            y,
            f"{channel}_VCA",
        )
        envelope_throttle = p.new("*~", 1235, y + 135, 40, numinlets=2, numoutlets=1)
        vca_cv = p.new("*~ 0.6", 1295, y + 135, 65, numinlets=2, numoutlets=1)
        channel_out = outlet(p, 1645, y + 70, signal=True)

        p.connect(root_pitch, osc_a, 0, 0)
        p.connect(fifth_pitch, osc_b, 0, 0)
        p.connect(osc_a, mixer, 0, 0)
        p.connect(osc_b, mixer, 0, 1)
        p.connect(mixer, ladder, 0, 0)
        p.connect(filter_cv, ladder, 0, 1)
        p.connect(gate_cv, envelope, 0, 0)
        p.connect(envelope, envelope_throttle, 0, 0)
        p.connect(throttle_cv, envelope_throttle, 0, 1)
        p.connect(envelope_throttle, vca_cv)
        p.connect(ladder, vca, 0, 0)
        p.connect(vca_cv, vca, 0, 1)
        p.connect(vca, channel_out)
    return p.document()


def make_ev_pad_driver() -> dict[str, Any]:
    """Translate EV messages to BEAP CV and contain pad bandwidth/level."""
    p = Patcher(980, 650)
    p.comment("EV-only BEAP pad driver — RPM pitch, ignition gate, throttle filter/level", 25, 15, 700)
    control = inlet(p, 35, 65)
    router = route(p, ("rpm", "throttle", "ignition", "pad_level_db", "pad_mute"), 35, 105, 500)
    p.connect(control, router)

    rpm_clip = p.new("clip 0. 10000.", 35, 155, 105, numinlets=3, numoutlets=1)
    pitch_map = p.new(
        "expr log(max(55.,min(760.,55.+$f1*.052))/261.625565)/log(2.)",
        35,
        195,
        390,
        numinlets=1,
        numoutlets=1,
    )
    pitch_pack = p.new("pack 0. 60", 35, 235, 85, numinlets=2, numoutlets=1)
    pitch_line = p.new("line~", 35, 275, 50, numinlets=2, numoutlets=2)
    p.connect(router, rpm_clip, 0)
    p.connect(rpm_clip, pitch_map)
    p.connect(pitch_map, pitch_pack)
    p.connect(pitch_pack, pitch_line)

    throttle_clip = p.new("clip 0. 1.", 455, 155, 75, numinlets=3, numoutlets=1)
    throttle_map = p.new("expr 0.75+3.*$f1", 455, 195, 125, numinlets=1, numoutlets=1)
    throttle_pack = p.new("pack 0. 120", 455, 235, 95, numinlets=2, numoutlets=1)
    throttle_line = p.new("line~", 455, 275, 50, numinlets=2, numoutlets=2)
    p.connect(router, throttle_clip, 1)
    p.connect(throttle_clip, throttle_map)
    p.connect(throttle_map, throttle_pack)
    p.connect(throttle_pack, throttle_line)

    ignition_clip = p.new("clip 0. 1.", 625, 155, 75, numinlets=3, numoutlets=1)
    gate_map = p.new("expr $f1*5.", 625, 195, 90, numinlets=1, numoutlets=1)
    gate_pack = p.new("pack 0. 10", 625, 235, 85, numinlets=2, numoutlets=1)
    gate_line = p.new("line~", 625, 275, 50, numinlets=2, numoutlets=2)
    p.connect(router, ignition_clip, 2)
    p.connect(ignition_clip, gate_map)
    p.connect(gate_map, gate_pack)
    p.connect(gate_pack, gate_line)

    for index, (text, target) in enumerate(
        (("650", rpm_clip), ("0.", throttle_clip), ("0.", ignition_clip))
    ):
        initial = p.new(f"loadmess {text}", 760, 155 + index * 40, 90, numinlets=1, numoutlets=1)
        p.connect(initial, target)

    pad = p.new("ev_pad_beap~", 285, 345, 115, numinlets=3, numoutlets=2)
    hp_l = p.new("svf~ 120 0.7", 215, 395, 100, numinlets=3, numoutlets=4)
    hp_r = p.new("svf~ 120 0.7", 455, 395, 100, numinlets=3, numoutlets=4)
    low_sum = p.new("+~", 35, 455, 40, numinlets=2, numoutlets=1)
    low_mid = p.new("*~ 0.5", 85, 455, 60, numinlets=2, numoutlets=1)
    direct_l = p.new("*~ 0.82", 165, 455, 65, numinlets=2, numoutlets=1)
    cross_l = p.new("*~ 0.18", 245, 455, 65, numinlets=2, numoutlets=1)
    direct_r = p.new("*~ 0.82", 405, 455, 65, numinlets=2, numoutlets=1)
    cross_r = p.new("*~ 0.18", 485, 455, 65, numinlets=2, numoutlets=1)
    high_l = p.new("+~", 215, 495, 40, numinlets=2, numoutlets=1)
    high_r = p.new("+~", 455, 495, 40, numinlets=2, numoutlets=1)
    sum_l = p.new("+~", 215, 525, 40, numinlets=2, numoutlets=1)
    sum_r = p.new("+~", 455, 525, 40, numinlets=2, numoutlets=1)
    pad_level = add_db_gain_control(p, router, 3, 665, 345, -3.0)
    mute_clip = p.new("clip 0 1", 665, 495, 65, numinlets=3, numoutlets=1)
    mute_gain = p.new("expr 1-$i1", 740, 495, 80, numinlets=1, numoutlets=1)
    mute_pack = p.new("pack 0. 30", 665, 535, 85, numinlets=2, numoutlets=1)
    mute_line = p.new("line~", 765, 535, 50, numinlets=2, numoutlets=2)
    mute_default = p.new("loadmess 0", 835, 495, 80, numinlets=1, numoutlets=1)
    gain_l = p.new("*~", 215, 570, 40, numinlets=2, numoutlets=1)
    gain_r = p.new("*~", 455, 570, 40, numinlets=2, numoutlets=1)
    mute_l = p.new("*~", 215, 575, 40, numinlets=2, numoutlets=1)
    mute_r = p.new("*~", 455, 575, 40, numinlets=2, numoutlets=1)
    left = outlet(p, 215, 535, signal=True)
    right = outlet(p, 455, 535, signal=True)
    p.connect(pitch_line, pad, 0, 0)
    p.connect(gate_line, pad, 0, 1)
    p.connect(throttle_line, pad, 0, 2)
    p.connect(pad, hp_l, 0, 0)
    p.connect(pad, hp_r, 1, 0)
    p.connect(hp_l, low_sum, 0, 0)
    p.connect(hp_r, low_sum, 0, 1)
    p.connect(low_sum, low_mid)
    p.connect(hp_l, direct_l, 1, 0)
    p.connect(hp_r, cross_l, 1, 0)
    p.connect(hp_r, direct_r, 1, 0)
    p.connect(hp_l, cross_r, 1, 0)
    p.connect(direct_l, high_l, 0, 0)
    p.connect(cross_l, high_l, 0, 1)
    p.connect(direct_r, high_r, 0, 0)
    p.connect(cross_r, high_r, 0, 1)
    p.connect(low_mid, sum_l, 0, 0)
    p.connect(high_l, sum_l, 0, 1)
    p.connect(low_mid, sum_r, 0, 0)
    p.connect(high_r, sum_r, 0, 1)
    p.connect(router, mute_clip, 4)
    p.connect(mute_default, mute_clip)
    p.connect(mute_clip, mute_gain)
    p.connect(mute_gain, mute_pack)
    p.connect(mute_pack, mute_line)
    p.connect(sum_l, gain_l)
    p.connect(sum_r, gain_r)
    p.connect(pad_level, gain_l, 0, 1)
    p.connect(pad_level, gain_r, 0, 1)
    p.connect(gain_l, mute_l)
    p.connect(gain_r, mute_r)
    p.connect(mute_line, mute_l, 0, 1)
    p.connect(mute_line, mute_r, 0, 1)
    p.connect(mute_l, left)
    p.connect(mute_r, right)
    return p.document()


def add_db_gain_control(
    patch: Patcher,
    router: str,
    route_outlet: int,
    x: float,
    y: float,
    default_db: float,
) -> str:
    """Create a click-safe -60..+6 dB control and return its signal line."""
    bounded = patch.new("clip -60. 6.", x, y, 85, numinlets=3, numoutlets=1)
    amplitude = patch.new("expr pow(10., $f1/20.)", x, y + 36, 150, numinlets=1, numoutlets=1)
    packed = patch.new("pack 0. 50", x, y + 72, 85, numinlets=2, numoutlets=1)
    smoothed = patch.new("line~", x, y + 108, 50, numinlets=2, numoutlets=2)
    initial = patch.new(f"loadmess {default_db:g}", x + 100, y, 95, numinlets=1, numoutlets=1)
    patch.connect(router, bounded, route_outlet)
    patch.connect(initial, bounded)
    patch.connect(bounded, amplitude)
    patch.connect(amplitude, packed)
    patch.connect(packed, smoothed)
    return smoothed


def make_engine() -> dict[str, Any]:
    p = Patcher(1550, 900)
    p.comment("vehicle_engine~ — lifecycle-aware public seam and layered stereo renderer", 25, 15, 620)
    control = inlet(p, 45, 65)
    controller = p.new("engine_controller", 45, 105, 125, numinlets=1, numoutlets=1)
    fan = p.new("t l l l l l l l", 45, 150, 135, numinlets=1, numoutlets=7)
    contract = route(p, ALL_MESSAGES, 190, 150, 900)
    p.comment("Contract monitor: every documented state, event, macro, and mix message is accepted", 190, 185, 620)
    power = p.new("powertrain~", 95, 260, 95, numinlets=1, numoutlets=2)
    transient = p.new("transient~", 285, 260, 90, numinlets=1, numoutlets=2)
    road = p.new("road_air~", 465, 260, 85, numinlets=1, numoutlets=2)
    rumble = p.new("cabin_rumble~", 625, 260, 110, numinlets=3, numoutlets=2)
    cabin = p.new("cabin_master~", 800, 460, 110, numinlets=3, numoutlets=2)
    mix = p.add(
        "bpatcher", None, 535, 500, 970, 340,
        numinlets=3, numoutlets=2, name="mix_master~.maxpat",
        presentation=1, presentation_rect=[15.0, 15.0, 970.0, 340.0],
    )
    add_l1 = p.new("+~", 130, 350, 35, numinlets=2, numoutlets=1)
    add_l2 = p.new("+~", 235, 390, 35, numinlets=2, numoutlets=1)
    add_l3 = p.new("+~", 340, 430, 35, numinlets=2, numoutlets=1)
    add_r1 = p.new("+~", 390, 350, 35, numinlets=2, numoutlets=1)
    add_r2 = p.new("+~", 495, 390, 35, numinlets=2, numoutlets=1)
    add_r3 = p.new("+~", 600, 430, 35, numinlets=2, numoutlets=1)
    pre_cabin_l = p.new("send~ vss_pre_cabin_l", 675, 390, 145, numinlets=1, numoutlets=0)
    pre_cabin_r = p.new("send~ vss_pre_cabin_r", 675, 430, 145, numinlets=1, numoutlets=0)
    left = outlet(p, 1015, 830, signal=True)
    right = outlet(p, 1105, 830, signal=True)

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
    p.connect(power, rumble, 0, 1)
    p.connect(transient, add_l1, 0, 1)
    p.connect(add_l1, add_l2, 0, 0)
    p.connect(road, add_l2, 0, 1)
    p.connect(add_l2, add_l3, 0, 0)
    p.connect(rumble, add_l3, 0, 1)
    p.connect(add_l3, pre_cabin_l)
    p.connect(power, add_r1, 1, 0)
    p.connect(power, rumble, 1, 2)
    p.connect(transient, add_r1, 1, 1)
    p.connect(add_r1, add_r2, 0, 0)
    p.connect(road, add_r2, 1, 1)
    p.connect(add_r2, add_r3, 0, 0)
    p.connect(rumble, add_r3, 1, 1)
    p.connect(add_r3, pre_cabin_r)
    p.connect(add_l3, cabin, 0, 1)
    p.connect(add_r3, cabin, 0, 2)
    p.connect(cabin, mix, 0, 1)
    p.connect(cabin, mix, 1, 2)
    p.connect(mix, left, 0)
    p.connect(mix, right, 1)
    return p.document(presentation=True)


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
    start_state = p.new("pack 0 0 0 1", 420, 245, 105, numinlets=4, numoutlets=1)
    start_valid = p.new("expr $i1*$i2*$i3*$i4", 420, 285, 155, numinlets=4, numoutlets=1)
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

    start_trigger = p.new("t b b b b", 420, 365, 80, numinlets=1, numoutlets=4)
    lock_start = p.message("0", 330, 365, 30)
    unlock_start = p.message("1", 315, 285, 30)
    initial_start_unlock = p.new("loadmess 1", 315, 325, 75, numinlets=1, numoutlets=1)
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
    p.connect(start_trigger, lock_start, 3)
    p.connect(lock_start, start_state, 0, 3)
    p.connect(unlock_start, start_state, 0, 3)
    p.connect(initial_start_unlock, start_state, 0, 3)
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
    p.connect(ignition_off, unlock_start, 0)
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
    p = Patcher(1180, 800)
    p.comment("VISIBLE MASTER EQ — drag four nodes or use the public eq_* messages", 25, 15, 700)
    control = inlet(p, 35, 60)
    left_in = inlet(p, 170, 60, signal=True)
    right_in = inlet(p, 280, 60, signal=True)
    router = route(p, ("eq_low", "eq_lowmid", "eq_highmid", "eq_high", "eq_bypass", "master_trim_db"), 35, 105, 640)
    p.connect(control, router)

    band_specs = (
        ("lowshelf", 6, 90.0, 30.0, 400.0, 0.7),
        ("peaknotch", 5, 250.0, 120.0, 1200.0, 0.8),
        ("peaknotch", 5, 3800.0, 1000.0, 8000.0, 1.0),
        ("highshelf", 7, 9000.0, 4000.0, 16000.0, 0.7),
    )
    saved_filters: list[float | int] = []
    for index, (_, mode, frequency, _, _, q_value) in enumerate(band_specs):
        saved_filters.extend((index, mode, 1, 0, 0, frequency, 1.0, q_value, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
    graph = p.add(
        "filtergraph~", None, 35, 165, 720, 250,
        numinlets=8, numoutlets=7, nfilters=4, autoout=1,
        setfilter=saved_filters, presentation=1,
        presentation_rect=[15.0, 35.0, 720.0, 250.0],
    )

    selected = p.add(
        "number", None, 790, 445, 55, numinlets=1, numoutlets=2,
        presentation=1, presentation_rect=[770.0, 55.0, 55.0, 22.0],
    )
    for label, rect in (
        ("Node 0–3", [770.0, 35.0, 90.0, 18.0]),
        ("Frequency Hz", [770.0, 85.0, 100.0, 18.0]),
        ("Gain dB", [770.0, 135.0, 90.0, 18.0]),
        ("Q / S", [770.0, 185.0, 90.0, 18.0]),
        ("Bypass", [900.0, 295.0, 60.0, 18.0]),
    ):
        p.add("comment", label, 1080, 520, 100, 18, numinlets=1, numoutlets=0, presentation=1, presentation_rect=rect)
    selected_clip = p.new("clip 0 3", 790, 475, 65, numinlets=3, numoutlets=1)
    selected_message = p.new("prepend setfilter", 865, 475, 105, numinlets=1, numoutlets=1)
    selected_set = p.new("prepend set", 980, 475, 85, numinlets=1, numoutlets=1)
    selected_default = p.new("loadmess 0", 1070, 475, 80, numinlets=1, numoutlets=1)
    p.connect(selected, selected_clip)
    p.connect(selected_clip, selected_message)
    p.connect(selected_message, graph)
    p.connect(graph, selected_set, 6)
    p.connect(selected_set, selected)
    p.connect(selected_default, selected)

    frequency_ui = p.add(
        "flonum", None, 790, 515, 80, numinlets=1, numoutlets=2,
        presentation=1, presentation_rect=[770.0, 105.0, 80.0, 22.0],
    )
    gain_ui = p.add(
        "flonum", None, 885, 515, 70, numinlets=1, numoutlets=2,
        presentation=1, presentation_rect=[770.0, 155.0, 80.0, 22.0],
    )
    q_ui = p.add(
        "flonum", None, 970, 515, 70, numinlets=1, numoutlets=2,
        presentation=1, presentation_rect=[770.0, 205.0, 80.0, 22.0],
    )
    frequency_set = p.new("prepend set", 790, 550, 85, numinlets=1, numoutlets=1)
    # filtergraph~ stores its gain parameter as a power ratio: 10*log10(gain).
    gain_to_db = p.new("expr 10.*log(max($f1,0.000001))/log(10.)", 885, 550, 250, numinlets=1, numoutlets=1)
    gain_set = p.new("prepend set", 885, 585, 85, numinlets=1, numoutlets=1)
    q_set = p.new("prepend set", 970, 620, 85, numinlets=1, numoutlets=1)
    edit_gain = p.new("expr pow(10., $f1/10.)", 885, 655, 150, numinlets=1, numoutlets=1)
    edit_pack = p.new("pak 1000. 1. 0.8", 790, 690, 130, numinlets=3, numoutlets=1)
    edit_order = p.new("t b l", 790, 725, 50, numinlets=1, numoutlets=2)
    p.connect(graph, frequency_set, 1)
    p.connect(frequency_set, frequency_ui)
    p.connect(graph, gain_to_db, 2)
    p.connect(gain_to_db, gain_set)
    p.connect(gain_set, gain_ui)
    p.connect(graph, q_set, 3)
    p.connect(q_set, q_ui)
    p.connect(frequency_ui, edit_pack, 0, 0)
    p.connect(gain_ui, edit_gain)
    p.connect(edit_gain, edit_pack, 0, 1)
    p.connect(q_ui, edit_pack, 0, 2)
    p.connect(edit_pack, edit_order)
    p.connect(edit_order, graph, 1, 5)
    p.connect(edit_order, graph, 0, 0)

    for index, (mode_name, _, default_freq, min_freq, max_freq, default_q) in enumerate(band_specs):
        x = 35 + index * 260
        is_peak = mode_name == "peaknotch"
        unpack = p.new(
            "unpack 0. 0. 0." if is_peak else "unpack 0. 0.",
            x, 445, 105, numinlets=1, numoutlets=3 if is_peak else 2,
        )
        freq_clip = p.new(f"clip {min_freq:g} {max_freq:g}", x, 205, 105, numinlets=3, numoutlets=1)
        gain_clip = p.new("clip -12. 12.", x + 110, 485, 85, numinlets=3, numoutlets=1)
        gain_linear = p.new("expr pow(10., $f1/10.)", x + 110, 525, 150, numinlets=1, numoutlets=1)
        q_clip = p.new("clip 0.3 4.", x + 200, 485, 75, numinlets=3, numoutlets=1) if is_peak else None
        packed = p.new(f"pak {default_freq:g} 1. {default_q:g}", x, 565, 125, numinlets=3, numoutlets=1)
        ordered = p.new("t b l b", x, 600, 65, numinlets=1, numoutlets=3)
        select = p.message(f"setfilter {index}", x + 60, 600, 75)
        select_value = p.message(f"{index}", x + 140, 600, 30)
        p.connect(router, unpack, index)
        p.connect(unpack, freq_clip, 0)
        p.connect(unpack, gain_clip, 1)
        p.connect(freq_clip, packed, 0, 0)
        p.connect(freq_clip, frequency_set)
        p.connect(gain_clip, gain_linear)
        p.connect(gain_clip, gain_set)
        p.connect(gain_linear, packed, 0, 1)
        if q_clip is not None:
            p.connect(unpack, q_clip, 2)
            p.connect(q_clip, packed, 0, 2)
            p.connect(q_clip, q_set)
        p.connect(packed, ordered)
        p.connect(ordered, select, 2)
        p.connect(ordered, select_value, 2)
        p.connect(select, graph)
        p.connect(select_value, selected_set)
        p.connect(ordered, graph, 1, 5)
        p.connect(ordered, graph, 0, 0)

    left_filter = p.new("cascade~ 4", 790, 205, 80, numinlets=2, numoutlets=1)
    right_filter = p.new("cascade~ 4", 900, 205, 80, numinlets=2, numoutlets=1)
    p.connect(left_in, left_filter)
    p.connect(right_in, right_filter)
    p.connect(graph, left_filter, 0, 1)
    p.connect(graph, right_filter, 0, 1)

    reset = p.add(
        "message", "Reset EQ", 760, 35, 70, numinlets=2, numoutlets=1,
        presentation=1, presentation_rect=[870.0, 255.0, 75.0, 22.0],
    )
    reset_values = p.message(
        "setparams 0 90. 1. 0.7, setparams 1 250. 1. 0.8, setparams 2 3800. 1. 1., setparams 3 9000. 1. 0.7, bang",
        840, 35, 300,
    )
    p.connect(reset, reset_values)
    p.connect(reset_values, graph)

    bypass_ui = p.add("toggle", None, 760, 85, 22, 22, numinlets=1, numoutlets=1, presentation=1, presentation_rect=[870.0, 295.0, 22.0, 22.0])
    p.comment("Bypass", 790, 85, 60)
    bypass_clip = p.new("clip 0 1", 790, 125, 65, numinlets=3, numoutlets=1)
    bypass_split = p.new("t f f", 865, 125, 55, numinlets=1, numoutlets=2)
    wet_expr = p.new("expr 1.-$f1", 930, 125, 90, numinlets=1, numoutlets=1)
    dry_pack = p.new("pack 0. 30", 865, 165, 85, numinlets=2, numoutlets=1)
    wet_pack = p.new("pack 0. 30", 965, 165, 85, numinlets=2, numoutlets=1)
    dry_line = p.new("line~", 865, 245, 50, numinlets=2, numoutlets=2)
    wet_line = p.new("line~", 965, 245, 50, numinlets=2, numoutlets=2)
    bypass_default = p.new("loadmess 0", 1060, 125, 80, numinlets=1, numoutlets=1)
    p.connect(router, bypass_clip, 4)
    p.connect(bypass_ui, bypass_clip)
    p.connect(bypass_default, bypass_clip)
    p.connect(bypass_clip, bypass_split)
    p.connect(bypass_split, dry_pack, 1)
    p.connect(bypass_split, wet_expr, 0)
    p.connect(wet_expr, wet_pack)
    p.connect(dry_pack, dry_line)
    p.connect(wet_pack, wet_line)

    trim_clip = p.new("clip -24. 0.", 790, 315, 85, numinlets=3, numoutlets=1)
    trim_amp = p.new("expr pow(10., $f1/20.)", 790, 350, 150, numinlets=1, numoutlets=1)
    trim_pack = p.new("pack 0. 50", 790, 385, 85, numinlets=2, numoutlets=1)
    trim_line = p.new("line~", 790, 420, 50, numinlets=2, numoutlets=2)
    trim_default = p.new("loadmess -8.", 900, 315, 95, numinlets=1, numoutlets=1)
    p.connect(router, trim_clip, 5)
    p.connect(trim_default, trim_clip)
    p.connect(trim_clip, trim_amp)
    p.connect(trim_amp, trim_pack)
    p.connect(trim_pack, trim_line)

    masters: list[str] = []
    for index, (dry, wet) in enumerate(((left_in, left_filter), (right_in, right_filter))):
        x = 300 + index * 330
        dry_gain = p.new("*~", x, 630, 40, numinlets=2, numoutlets=1)
        wet_gain = p.new("*~", x + 70, 630, 40, numinlets=2, numoutlets=1)
        blend = p.new("+~", x + 35, 670, 40, numinlets=2, numoutlets=1)
        trim = p.new("*~", x + 35, 705, 40, numinlets=2, numoutlets=1)
        p.connect(dry, dry_gain, 0, 0)
        p.connect(dry_line, dry_gain, 0, 1)
        p.connect(wet, wet_gain, 0, 0)
        p.connect(wet_line, wet_gain, 0, 1)
        p.connect(dry_gain, blend, 0, 0)
        p.connect(wet_gain, blend, 0, 1)
        p.connect(blend, trim, 0, 0)
        p.connect(trim_line, trim, 0, 1)
        masters.append(trim)
    limiter = p.new("omx.peaklim~", 500, 700, 105, numinlets=2, numoutlets=4)
    clip_l = p.new("clip~ -0.891 0.891", 365, 740, 130, numinlets=3, numoutlets=1)
    clip_r = p.new("clip~ -0.891 0.891", 630, 740, 130, numinlets=3, numoutlets=1)
    left = outlet(p, 470, 770, signal=True)
    right = outlet(p, 650, 770, signal=True)
    p.connect(masters[0], limiter, 0, 0)
    p.connect(masters[1], limiter, 0, 1)
    p.connect(limiter, clip_l, 0, 0)
    p.connect(limiter, clip_r, 1, 0)
    p.connect(clip_l, left)
    p.connect(clip_r, right)
    return p.document(presentation=True)


def make_powertrain() -> dict[str, Any]:
    p = Patcher(1280, 780)
    p.comment("Three bounded Gen powertrains plus an EV-only dual BEAP pad", 25, 15, 580)
    control = inlet(p, 35, 65)
    tonal_names = ("rpm", "throttle", "load", "aggression", "brightness", "body", "texture")
    fuel_names = ("engine_running", "combustion_gain", "shift_cut")
    weight_names = ("ev_weight", "v12_weight", "v10_weight")
    pad_names = (
        "ignition", "pad_level_db", "pad_mute", "pad_solo",
        "reference_texture_level_db", "reference_texture_mute", "rpm",
    )
    names = tonal_names + fuel_names + weight_names + pad_names + ("powertrain_level_db",)
    router = route(p, names, 35, 105, 760)
    gens = [
        p.new("gen~ @gen ev_powertrain", 220, 395, 165, numinlets=1, numoutlets=2),
        p.new("gen~ @gen v12_powertrain", 510, 395, 175, numinlets=1, numoutlets=2),
        p.new("gen~ @gen v10_powertrain", 800, 395, 175, numinlets=1, numoutlets=2),
    ]
    ev_pad = p.new("ev_pad_driver~", 35, 395, 120, numinlets=1, numoutlets=2)
    reference = p.new("reference_texture~", 1005, 395, 135, numinlets=1, numoutlets=2)
    motor_l = p.new("*~", 165, 425, 40, numinlets=2, numoutlets=1)
    motor_r = p.new("*~", 220, 425, 40, numinlets=2, numoutlets=1)
    ev_sum_l = p.new("+~", 220, 445, 40, numinlets=2, numoutlets=1)
    ev_sum_r = p.new("+~", 295, 445, 40, numinlets=2, numoutlets=1)
    p.connect(gens[0], motor_l, 0, 0)
    p.connect(gens[0], motor_r, 1, 0)
    p.connect(motor_l, ev_sum_l, 0, 0)
    p.connect(motor_r, ev_sum_r, 0, 0)
    p.connect(ev_pad, ev_sum_l, 0, 1)
    p.connect(ev_pad, ev_sum_r, 1, 1)
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
        if name in {"rpm", "throttle"}:
            p.connect(named, ev_pad)

    for index, name in enumerate(fuel_names):
        x = 720 + index * 160
        bounded = p.new("clip 0. 1.", x, 175, 75, numinlets=3, numoutlets=1)
        named = p.message(f"{name} $1", x, 220, 125)
        p.connect(router, bounded, len(tonal_names) + index)
        p.connect(bounded, named)
        p.connect(named, gens[1])
        p.connect(named, gens[2])

    for offset, name in enumerate(("ignition", "pad_level_db", "pad_mute")):
        x = 970 + offset * 100
        named = p.new(f"prepend {name}", x, 245, 95, numinlets=1, numoutlets=1)
        p.connect(router, named, names.index(name))
        p.connect(named, ev_pad)

    solo_clip = p.new("clip 0 1", 970, 285, 65, numinlets=3, numoutlets=1)
    solo_gain = p.new("expr 1-$i1", 1045, 285, 80, numinlets=1, numoutlets=1)
    solo_pack = p.new("pack 0. 30", 970, 325, 85, numinlets=2, numoutlets=1)
    solo_line = p.new("line~", 1070, 325, 50, numinlets=2, numoutlets=2)
    solo_default = p.new("loadmess 0", 1140, 285, 80, numinlets=1, numoutlets=1)
    p.connect(router, solo_clip, names.index("pad_solo"))
    p.connect(solo_default, solo_clip)
    p.connect(solo_clip, solo_gain)
    p.connect(solo_gain, solo_pack)
    p.connect(solo_pack, solo_line)
    p.connect(solo_line, motor_l, 0, 1)
    p.connect(solo_line, motor_r, 0, 1)
    p.connect(control, reference)

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
        if index == 0:
            p.connect(ev_sum_l, left_mult, 0, 0)
            p.connect(ev_sum_r, right_mult, 0, 0)
        else:
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
    add_l3 = p.new("+~", 520, 645, 35, numinlets=2, numoutlets=1)
    add_r3 = p.new("+~", 810, 645, 35, numinlets=2, numoutlets=1)
    stem_level = add_db_gain_control(p, router, len(names) - 1, 1030, 525, -3.0)
    trim_l = p.new("*~", 520, 685, 40, numinlets=2, numoutlets=1)
    trim_r = p.new("*~", 810, 685, 40, numinlets=2, numoutlets=1)
    left = outlet(p, 520, 720, signal=True)
    right = outlet(p, 810, 720, signal=True)
    p.connect(left_mults[0], add_l1, 0, 0)
    p.connect(left_mults[1], add_l1, 0, 1)
    p.connect(add_l1, add_l2, 0, 0)
    p.connect(left_mults[2], add_l2, 0, 1)
    p.connect(right_mults[0], add_r1, 0, 0)
    p.connect(right_mults[1], add_r1, 0, 1)
    p.connect(add_r1, add_r2, 0, 0)
    p.connect(right_mults[2], add_r2, 0, 1)
    p.connect(add_l2, add_l3, 0, 0)
    p.connect(reference, add_l3, 0, 1)
    p.connect(add_r2, add_r3, 0, 0)
    p.connect(reference, add_r3, 1, 1)
    p.connect(add_l3, trim_l)
    p.connect(add_r3, trim_r)
    p.connect(stem_level, trim_l, 0, 1)
    p.connect(stem_level, trim_r, 0, 1)
    p.connect(trim_l, left)
    p.connect(trim_r, right)
    p.connect(control, router)
    return p.document()


def make_reference_texture() -> dict[str, Any]:
    """Crossfade a normalized six-anchor stereo residual bank at near-unity speed."""
    p = Patcher(2300, 1080)
    p.comment("CC0 stereo engine residual bank — six firing-rate anchors, two asynchronous loops each", 25, 15, 1050)
    control = inlet(p, 35, 65)
    names = (
        "throttle", "engine_running", "v12_weight", "v10_weight",
        "reference_texture_level_db", "reference_texture_mute", "rpm",
    )
    router = route(p, names, 35, 105, 650)
    p.connect(control, router)

    rpm = p.new("clip 0. 10000.", 35, 155, 105, numinlets=3, numoutlets=1)
    v12 = p.new("clip 0. 1.", 155, 155, 75, numinlets=3, numoutlets=1)
    firing = p.new("expr max(30.,min(850.,($f1/60.)*(5.+$f2)))", 245, 155, 285, numinlets=2, numoutlets=1)
    p.connect(router, rpm, 6)
    p.connect(router, v12, 2)
    p.connect(rpm, firing, 0, 0)
    p.connect(v12, firing, 0, 1)

    throttle = p.new("clip 0. 1.", 550, 155, 75, numinlets=3, numoutlets=1)
    load_lift = p.new("expr pow(10., (3.*$f1)/20.)", 640, 155, 190, numinlets=1, numoutlets=1)
    load_pack = p.new("pack 0. 100", 845, 155, 90, numinlets=2, numoutlets=1)
    load_line = p.new("line~", 950, 155, 50, numinlets=2, numoutlets=2)
    p.connect(router, throttle, 0)
    p.connect(throttle, load_lift)
    p.connect(load_lift, load_pack)
    p.connect(load_pack, load_line)

    running = p.new("clip 0. 1.", 1020, 155, 75, numinlets=3, numoutlets=1)
    v10 = p.new("clip 0. 1.", 1110, 155, 75, numinlets=3, numoutlets=1)
    profile_sum = p.new("+", 1200, 155, 35, numinlets=2, numoutlets=1)
    profile_clip = p.new("clip 0. 1.", 1250, 155, 75, numinlets=3, numoutlets=1)
    gate_product = p.new("*", 1340, 155, 35, numinlets=2, numoutlets=1)
    gate_pack = p.new("pack 0. 100", 1390, 155, 90, numinlets=2, numoutlets=1)
    gate_line = p.new("line~", 1495, 155, 50, numinlets=2, numoutlets=2)
    p.connect(router, running, 1)
    p.connect(router, v10, 3)
    p.connect(v12, profile_sum, 0, 0)
    p.connect(v10, profile_sum, 0, 1)
    p.connect(profile_sum, profile_clip)
    p.connect(running, gate_product, 0, 0)
    p.connect(profile_clip, gate_product, 0, 1)
    p.connect(gate_product, gate_pack)
    p.connect(gate_pack, gate_line)

    level = add_db_gain_control(p, router, 4, 1570, 155, -24.0)
    mute_clip = p.new("clip 0 1", 1770, 155, 65, numinlets=3, numoutlets=1)
    mute_gain = p.new("expr 1-$i1", 1850, 155, 80, numinlets=1, numoutlets=1)
    mute_pack = p.new("pack 0. 40", 1945, 155, 85, numinlets=2, numoutlets=1)
    mute_line = p.new("line~", 2045, 155, 50, numinlets=2, numoutlets=2)
    mute_default = p.new("loadmess 0", 2110, 155, 80, numinlets=1, numoutlets=1)
    p.connect(router, mute_clip, 5)
    p.connect(mute_default, mute_clip)
    p.connect(mute_clip, mute_gain)
    p.connect(mute_gain, mute_pack)
    p.connect(mute_pack, mute_line)

    anchors = (("065", 65.0, 45.0), ("110", 110.0, 70.0), ("180", 180.0, 85.0),
               ("260", 260.0, 120.0), ("380", 380.0, 150.0), ("520", 520.0, 170.0))
    channel_layers: list[list[str]] = [[], []]
    for index, (name, anchor, width) in enumerate(anchors):
        x = 35 + index * 360
        buffer_a = p.new(f"buffer~ tex_{name}_a engine_texture_{name}_a.wav", x, 245, 285, numinlets=2, numoutlets=2)
        buffer_b = p.new(f"buffer~ tex_{name}_b engine_texture_{name}_b.wav", x, 280, 285, numinlets=2, numoutlets=2)
        speed_map = p.new(f"expr max(.9,min(1.1,$f1/{anchor:g}.))", x, 320, 210, numinlets=1, numoutlets=1)
        speed_pack = p.new("pack 0. 120", x, 355, 90, numinlets=2, numoutlets=1)
        speed_line = p.new("line~", x + 105, 355, 50, numinlets=2, numoutlets=2)
        groove_a = p.new(f"groove~ tex_{name}_a 2 @loop 1", x, 395, 220, numinlets=3, numoutlets=3)
        groove_b = p.new(f"groove~ tex_{name}_b 2 @loop 1", x, 430, 220, numinlets=3, numoutlets=3)
        weight_expression = (
            "expr sqrt(max(0.,1.-abs(min($f1,650.)-520.)/170.))"
            if name == "520"
            else f"expr sqrt(max(0.,1.-abs($f1-{anchor:g}.)/{width:g}.))"
        )
        weight_map = p.new(
            weight_expression,
            x, 470, 265, numinlets=1, numoutlets=1,
        )
        weight_pack = p.new("pack 0. 120", x, 505, 90, numinlets=2, numoutlets=1)
        weight_line = p.new("line~", x + 105, 505, 50, numinlets=2, numoutlets=2)
        p.connect(firing, speed_map)
        p.connect(speed_map, speed_pack)
        p.connect(speed_pack, speed_line)
        p.connect(speed_line, groove_a)
        p.connect(speed_line, groove_b)
        p.connect(firing, weight_map)
        p.connect(weight_map, weight_pack)
        p.connect(weight_pack, weight_line)
        for channel in (0, 1):
            pair_sum = p.new("+~", x + channel * 125, 555, 40, numinlets=2, numoutlets=1)
            pair_average = p.new("*~ 0.5", x + channel * 125, 590, 60, numinlets=2, numoutlets=1)
            anchor_gain = p.new("*~", x + channel * 125, 625, 40, numinlets=2, numoutlets=1)
            p.connect(groove_a, pair_sum, channel, 0)
            p.connect(groove_b, pair_sum, channel, 1)
            p.connect(pair_sum, pair_average)
            p.connect(pair_average, anchor_gain, 0, 0)
            p.connect(weight_line, anchor_gain, 0, 1)
            channel_layers[channel].append(anchor_gain)

    def sum_layers(signals: list[str], x: float) -> str:
        current = signals[0]
        for index, signal in enumerate(signals[1:]):
            summer = p.new("+~", x, 700 + index * 35, 40, numinlets=2, numoutlets=1)
            p.connect(current, summer, 0, 0)
            p.connect(signal, summer, 0, 1)
            current = summer
        return current

    outputs: list[str] = []
    for channel, x in ((0, 550), (1, 900)):
        layer_sum = sum_layers(channel_layers[channel], x)
        bank_trim = p.new("*~ 0.55", x + 70, 840, 65, numinlets=2, numoutlets=1)
        load_gain = p.new("*~", x + 150, 840, 40, numinlets=2, numoutlets=1)
        life_gain = p.new("*~", x + 210, 840, 40, numinlets=2, numoutlets=1)
        level_gain = p.new("*~", x + 270, 840, 40, numinlets=2, numoutlets=1)
        mute_stage = p.new("*~", x + 330, 840, 40, numinlets=2, numoutlets=1)
        p.connect(layer_sum, bank_trim)
        p.connect(bank_trim, load_gain, 0, 0)
        p.connect(load_line, load_gain, 0, 1)
        p.connect(load_gain, life_gain)
        p.connect(gate_line, life_gain, 0, 1)
        p.connect(life_gain, level_gain)
        p.connect(level, level_gain, 0, 1)
        p.connect(level_gain, mute_stage)
        p.connect(mute_line, mute_stage, 0, 1)
        outputs.append(mute_stage)
    left = outlet(p, 880, 940, signal=True)
    right = outlet(p, 1160, 940, signal=True)
    p.connect(outputs[0], left)
    p.connect(outputs[1], right)
    return p.document()


def make_cabin_rumble() -> dict[str, Any]:
    p = Patcher(1540, 900)
    p.comment(
        "Powertrain-driven cabin modes — coherent combustion excitation, mounts, body and exhaust",
        25,
        15,
        850,
    )
    control = inlet(p, 35, 65)
    left_in = inlet(p, 190, 65, signal=True)
    right_in = inlet(p, 300, 65, signal=True)
    names = (
        "cabin_rumble",
        "exhaust_boom",
        "structure_vibration",
        "body",
        "aggression",
        "rumble_level_db",
    )
    router = route(p, names, 35, 105, 650)
    p.connect(control, router)

    def normalized_line(name: str, index: int, expression: str, default: float) -> str:
        x = 35 + index * 230
        bounded = p.new("clip 0. 1.", x, 155, 75, numinlets=3, numoutlets=1)
        mapped = p.new(expression, x, 195, 175, numinlets=1, numoutlets=1)
        packed = p.new("pack 0. 60", x, 235, 85, numinlets=2, numoutlets=1)
        line = p.new("line~", x, 275, 50, numinlets=2, numoutlets=2)
        initial = p.new(f"loadmess {default:g}", x + 95, 275, 95, numinlets=1, numoutlets=1)
        p.connect(router, bounded, index)
        p.connect(bounded, mapped)
        p.connect(mapped, packed)
        p.connect(packed, line)
        p.connect(initial, bounded)
        return line

    cabin_gain = normalized_line("cabin_rumble", 0, "expr $f1*0.82", 0.90)
    exhaust_gain = normalized_line("exhaust_boom", 1, "expr $f1*0.62", 0.62)
    structure_gain = normalized_line("structure_vibration", 2, "expr $f1*0.58", 0.58)
    body_gain = normalized_line("body", 3, "expr 0.72+0.48*$f1", 0.72)
    drive_gain = normalized_line("aggression", 4, "expr 0.82+0.28*$f1", 0.62)
    stem_level = add_db_gain_control(p, router, 5, 1190, 155, -5.0)

    mid_sum = p.new("+~", 220, 350, 40, numinlets=2, numoutlets=1)
    mid = p.new("*~ 0.5", 220, 390, 60, numinlets=2, numoutlets=1)
    subsonic_guard = p.new("svf~ 28 0.7", 220, 430, 90, numinlets=3, numoutlets=4)
    excitation = p.new("onepole~ 520", 220, 470, 100, numinlets=2, numoutlets=1)
    p.connect(left_in, mid_sum, 0, 0)
    p.connect(right_in, mid_sum, 0, 1)
    p.connect(mid_sum, mid)
    p.connect(mid, subsonic_guard)
    p.connect(subsonic_guard, excitation, 1, 0)

    mode_signals: list[str] = []
    for index, (frequency, resonance, weight) in enumerate(
        ((48, 0.72, 0.14), (68, 0.72, 0.42), (92, 0.66, 0.34), (118, 0.60, 0.22))
    ):
        x = 380 + index * 185
        mode = p.new(f"svf~ {frequency} {resonance:g}", x, 430, 105, numinlets=3, numoutlets=4)
        weighted = p.new(f"*~ {weight:g}", x, 475, 65, numinlets=2, numoutlets=1)
        p.connect(excitation, mode)
        p.connect(mode, weighted, 2, 0)
        mode_signals.append(weighted)
    modes_a = p.new("+~", 520, 535, 40, numinlets=2, numoutlets=1)
    modes_b = p.new("+~", 750, 535, 40, numinlets=2, numoutlets=1)
    modes_sum = p.new("+~", 635, 580, 40, numinlets=2, numoutlets=1)
    modes_gain = p.new("*~", 635, 620, 40, numinlets=2, numoutlets=1)
    p.connect(mode_signals[0], modes_a, 0, 0)
    p.connect(mode_signals[1], modes_a, 0, 1)
    p.connect(mode_signals[2], modes_b, 0, 0)
    p.connect(mode_signals[3], modes_b, 0, 1)
    p.connect(modes_a, modes_sum, 0, 0)
    p.connect(modes_b, modes_sum, 0, 1)
    p.connect(modes_sum, modes_gain, 0, 0)
    p.connect(cabin_gain, modes_gain, 0, 1)

    structure_tone = p.new("onepole~ 185", 255, 535, 105, numinlets=2, numoutlets=1)
    structure_mix = p.new("*~", 255, 580, 40, numinlets=2, numoutlets=1)
    exhaust_mode = p.new("svf~ 74 0.58", 1030, 430, 100, numinlets=3, numoutlets=4)
    exhaust_mix = p.new("*~", 1030, 480, 40, numinlets=2, numoutlets=1)
    p.connect(excitation, structure_tone)
    p.connect(structure_tone, structure_mix)
    p.connect(structure_gain, structure_mix, 0, 1)
    p.connect(excitation, exhaust_mode)
    p.connect(exhaust_mode, exhaust_mix, 0, 0)
    p.connect(exhaust_gain, exhaust_mix, 0, 1)

    low_sum = p.new("+~", 460, 680, 40, numinlets=2, numoutlets=1)
    full_sum = p.new("+~", 650, 680, 40, numinlets=2, numoutlets=1)
    body_stage = p.new("*~", 650, 720, 40, numinlets=2, numoutlets=1)
    drive_stage = p.new("*~", 650, 755, 40, numinlets=2, numoutlets=1)
    guard = p.new("clip~ -0.72 0.72", 650, 790, 125, numinlets=3, numoutlets=1)
    trim_l = p.new("*~", 565, 825, 40, numinlets=2, numoutlets=1)
    trim_r = p.new("*~", 735, 825, 40, numinlets=2, numoutlets=1)
    left = outlet(p, 585, 865, signal=True)
    right = outlet(p, 755, 865, signal=True)
    p.connect(structure_mix, low_sum, 0, 0)
    p.connect(modes_gain, low_sum, 0, 1)
    p.connect(low_sum, full_sum, 0, 0)
    p.connect(exhaust_mix, full_sum, 0, 1)
    p.connect(full_sum, body_stage)
    p.connect(body_gain, body_stage, 0, 1)
    p.connect(body_stage, drive_stage)
    p.connect(drive_gain, drive_stage, 0, 1)
    p.connect(drive_stage, guard)
    p.connect(guard, trim_l)
    p.connect(guard, trim_r)
    p.connect(stem_level, trim_l, 0, 1)
    p.connect(stem_level, trim_r, 0, 1)
    p.connect(trim_l, left)
    p.connect(trim_r, right)
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
        "transient_level_db",
    )
    router = route(p, event_names, 35, 100, 850)
    players: list[str] = []

    starter_sel = p.new("sel 1", 35, 150, 45, numinlets=1, numoutlets=2)
    profile_sel = p.new("sel ev v12 v10", 105, 150, 105, numinlets=1, numoutlets=4)
    profile_gate = p.new("gate 2", 35, 195, 55, numinlets=2, numoutlets=2)
    p.connect(router, starter_sel, 0)
    p.connect(starter_sel, profile_gate, 0, 1)
    starter_stop = p.message("stop", 240, 195, 45)
    p.connect(starter_sel, starter_stop, 1)
    p.connect(router, profile_sel, 10)
    for outlet_index, value in ((0, 0), (1, 1), (2, 2)):
        message = p.message(str(value), 105 + outlet_index * 45, 195, 30)
        p.connect(profile_sel, message, outlet_index)
        p.connect(message, profile_gate, 0, 0)

    for index, (name, gate_outlet) in enumerate((("starter_v12", 0), ("starter_v10", 1))):
        x = 35 + index * 300
        p.new(f"buffer~ {name} {name}.wav", x, 245, 210, numinlets=1, numoutlets=2)
        start = p.message("start", x, 285, 45)
        player = p.new(f"play~ {name} 1", x, 325, 145, numinlets=1, numoutlets=2)
        gain = p.new("*~ 0.16", x, 365, 65, numinlets=2, numoutlets=1)
        p.connect(profile_gate, start, gate_outlet)
        p.connect(start, player)
        p.connect(starter_stop, player)
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
            p.new(f"buffer~ {name} {name}.wav", px, y + 82, 165, numinlets=1, numoutlets=2)
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

    p.new("buffer~ mechanical_click mechanical_click.wav", 1445, 740, 220, numinlets=1, numoutlets=2)
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

    texture_clip = p.new("clip 0. 1.", 1530, 300, 75, numinlets=3, numoutlets=1)
    texture_gain = p.new("expr 0.72+0.46*$f1", 1530, 340, 155, numinlets=1, numoutlets=1)
    texture_pack = p.new("pack 0. 35", 1530, 380, 85, numinlets=2, numoutlets=1)
    texture_line = p.new("line~", 1530, 420, 50, numinlets=2, numoutlets=2)
    texture_default = p.new("loadmess 0.9", 1630, 420, 95, numinlets=1, numoutlets=1)
    p.connect(router, texture_clip, 9)
    p.connect(texture_clip, texture_gain)
    p.connect(texture_gain, texture_pack)
    p.connect(texture_pack, texture_line)
    p.connect(texture_default, texture_clip)

    for index in range(2):
        starter_lowpass = p.new(
            "svf~ 3500 0.7", 35 + index * 300, 1040, 105,
            numinlets=3, numoutlets=4,
        )
        p.connect(players[index], starter_lowpass)
        players[index] = starter_lowpass

    mixed = players[0]
    for index, player in enumerate(players[1:]):
        add = p.new("+~", 240 + (index % 8) * 105, 1080 + (index // 8) * 45, 35, numinlets=2, numoutlets=1)
        p.connect(mixed, add, 0, 0)
        p.connect(player, add, 0, 1)
        mixed = add
    master = p.new("*~", 920, 1220, 40, numinlets=2, numoutlets=1)
    texture_master = p.new("*~", 920, 1255, 40, numinlets=2, numoutlets=1)
    left_gain = p.new("*~ 0.94", 820, 1280, 65, numinlets=2, numoutlets=1)
    right_gain = p.new("*~ 0.88", 980, 1280, 65, numinlets=2, numoutlets=1)
    stem_level = add_db_gain_control(p, router, len(event_names) - 1, 1610, 105, -7.0)
    trim_l = p.new("*~", 820, 1330, 40, numinlets=2, numoutlets=1)
    trim_r = p.new("*~", 980, 1330, 40, numinlets=2, numoutlets=1)
    left = outlet(p, 850, 1405, signal=True)
    right = outlet(p, 1010, 1405, signal=True)
    p.connect(mixed, master, 0, 0)
    p.connect(aggression_line, master, 0, 1)
    p.connect(master, texture_master)
    p.connect(texture_line, texture_master, 0, 1)
    p.connect(texture_master, left_gain)
    p.connect(texture_master, right_gain)
    p.connect(left_gain, trim_l)
    p.connect(right_gain, trim_r)
    p.connect(stem_level, trim_l, 0, 1)
    p.connect(stem_level, trim_r, 0, 1)
    p.connect(trim_l, left)
    p.connect(trim_r, right)
    p.connect(control, router)
    return p.document()


def make_road_air() -> dict[str, Any]:
    p = Patcher(1280, 820)
    p.comment("Tire: 70-900 Hz pink/brown bed; Wind: 400-4000 Hz restrained stereo air", 25, 15, 700)
    control = inlet(p, 35, 60)
    names = ("speed_kph", "brightness", "texture", "cabin_width", "road_level_db")
    router = route(p, names, 35, 100, 520)
    speed_clip = p.new("clip 0. 300.", 35, 155, 85, numinlets=3, numoutlets=1)
    tire_curve = p.new("expr pow($f1/300., 0.8)*0.065", 35, 195, 205, numinlets=1, numoutlets=1)
    wind_curve = p.new("expr pow($f1/300., 1.7)*0.045", 250, 195, 205, numinlets=1, numoutlets=1)
    tire_pack = p.new("pack 0. 120", 35, 235, 90, numinlets=2, numoutlets=1)
    wind_pack = p.new("pack 0. 120", 250, 235, 90, numinlets=2, numoutlets=1)
    tire_line = p.new("line~", 35, 275, 50, numinlets=2, numoutlets=2)
    wind_line = p.new("line~", 250, 275, 50, numinlets=2, numoutlets=2)
    bright_clip = p.new("clip 0. 1.", 285, 155, 75, numinlets=3, numoutlets=1)
    cutoff_expr = p.new("expr 1400.+2600.*$f1", 470, 195, 175, numinlets=1, numoutlets=1)
    cutoff_pack = p.new("pack 0. 80", 470, 235, 85, numinlets=2, numoutlets=1)
    cutoff_line = p.new("line~", 470, 275, 50, numinlets=2, numoutlets=2)
    texture_clip = p.new("clip 0. 1.", 670, 155, 75, numinlets=3, numoutlets=1)
    tire_texture_expr = p.new("expr 0.58+0.32*$f1", 670, 195, 155, numinlets=1, numoutlets=1)
    wind_texture_expr = p.new("expr 0.30+0.48*$f1", 835, 195, 155, numinlets=1, numoutlets=1)
    tire_texture_pack = p.new("pack 0. 80", 670, 235, 85, numinlets=2, numoutlets=1)
    wind_texture_pack = p.new("pack 0. 80", 835, 235, 85, numinlets=2, numoutlets=1)
    tire_texture_line = p.new("line~", 670, 275, 50, numinlets=2, numoutlets=2)
    wind_texture_line = p.new("line~", 835, 275, 50, numinlets=2, numoutlets=2)
    width_clip = p.new("clip 0. 1.", 1010, 155, 75, numinlets=3, numoutlets=1)
    width_expr = p.new("expr 0.55+0.45*$f1", 1010, 195, 155, numinlets=1, numoutlets=1)
    width_pack = p.new("pack 0. 80", 1010, 235, 85, numinlets=2, numoutlets=1)
    width_line = p.new("line~", 1010, 275, 50, numinlets=2, numoutlets=2)
    p.connect(router, speed_clip, 0)
    p.connect(speed_clip, tire_curve)
    p.connect(speed_clip, wind_curve)
    p.connect(tire_curve, tire_pack)
    p.connect(wind_curve, wind_pack)
    p.connect(tire_pack, tire_line)
    p.connect(wind_pack, wind_line)
    p.connect(router, bright_clip, 1)
    p.connect(bright_clip, cutoff_expr)
    p.connect(cutoff_expr, cutoff_pack)
    p.connect(cutoff_pack, cutoff_line)
    p.connect(router, texture_clip, 2)
    p.connect(texture_clip, tire_texture_expr)
    p.connect(texture_clip, wind_texture_expr)
    p.connect(tire_texture_expr, tire_texture_pack)
    p.connect(wind_texture_expr, wind_texture_pack)
    p.connect(tire_texture_pack, tire_texture_line)
    p.connect(wind_texture_pack, wind_texture_line)
    p.connect(router, width_clip, 3)
    p.connect(width_clip, width_expr)
    p.connect(width_expr, width_pack)
    p.connect(width_pack, width_line)
    for value, destination, x in (
        (0.0, tire_line, 35), (0.0, wind_line, 250), (3000.0, cutoff_line, 470),
        (0.75, tire_texture_line, 670), (0.66, wind_texture_line, 835), (0.80, width_line, 1010),
    ):
        default = p.new(f"loadmess {value:g}", x, 275, 95, numinlets=1, numoutlets=1)
        p.connect(default, destination)

    tire = p.new("pink~", 175, 365, 55, numinlets=0, numoutlets=1)
    tire_highpass = p.new("svf~ 70 0.65", 175, 405, 95, numinlets=3, numoutlets=4)
    tire_lowpass = p.new("lores~ 900 0.45", 175, 445, 115, numinlets=3, numoutlets=1)
    tire_speed = p.new("*~", 175, 485, 40, numinlets=2, numoutlets=1)
    tire_color = p.new("*~", 175, 525, 40, numinlets=2, numoutlets=1)
    p.connect(tire, tire_highpass)
    p.connect(tire_highpass, tire_lowpass, 1, 0)
    p.connect(tire_lowpass, tire_speed)
    p.connect(tire_line, tire_speed, 0, 1)
    p.connect(tire_speed, tire_color)
    p.connect(tire_texture_line, tire_color, 0, 1)

    channels: list[str] = []
    for index, x in enumerate((480, 820)):
        wind = p.new("noise~", x, 365, 55, numinlets=0, numoutlets=1)
        wind_highpass = p.new("svf~ 400 0.7", x, 405, 100, numinlets=3, numoutlets=4)
        wind_lowpass = p.new("lores~ 3000 0.38", x, 445, 125, numinlets=3, numoutlets=1)
        wind_speed = p.new("*~", x, 485, 40, numinlets=2, numoutlets=1)
        wind_color = p.new("*~", x, 525, 40, numinlets=2, numoutlets=1)
        wind_width = p.new("*~", x, 565, 40, numinlets=2, numoutlets=1)
        channel_mix = p.new("+~", x, 610, 40, numinlets=2, numoutlets=1)
        p.connect(wind, wind_highpass)
        p.connect(wind_highpass, wind_lowpass, 1, 0)
        p.connect(cutoff_line, wind_lowpass, 0, 1)
        p.connect(wind_lowpass, wind_speed)
        p.connect(wind_line, wind_speed, 0, 1)
        p.connect(wind_speed, wind_color)
        p.connect(wind_texture_line, wind_color, 0, 1)
        p.connect(wind_color, wind_width)
        p.connect(width_line, wind_width, 0, 1)
        p.connect(tire_color, channel_mix, 0, 0)
        p.connect(wind_width, channel_mix, 0, 1)
        channels.append(channel_mix)
    stem_level = add_db_gain_control(p, router, len(names) - 1, 1080, 330, -16.0)
    trim_l = p.new("*~", 480, 665, 40, numinlets=2, numoutlets=1)
    trim_r = p.new("*~", 820, 665, 40, numinlets=2, numoutlets=1)
    left = outlet(p, 500, 740, signal=True)
    right = outlet(p, 840, 740, signal=True)
    p.connect(channels[0], trim_l)
    p.connect(channels[1], trim_r)
    p.connect(stem_level, trim_l, 0, 1)
    p.connect(stem_level, trim_r, 0, 1)
    p.connect(trim_l, left)
    p.connect(trim_r, right)
    p.connect(control, router)
    return p.document()


def make_cabin_master() -> dict[str, Any]:
    p = Patcher(1380, 1220)
    p.comment("RPM-adaptive cabin field: mono bass below 120 Hz, preserved stereo mid/high field", 25, 15, 860)
    control = inlet(p, 35, 65)
    left_in = inlet(p, 210, 65, signal=True)
    right_in = inlet(p, 330, 65, signal=True)
    router = route(p, ("aggression", "brightness", "body", "texture", "cabin_width", "cabin_ir_mix", "rpm"), 35, 115, 620)

    controls: dict[str, str] = {}
    expressions = {
        "aggression": "expr 0.48 + 0.20*$f1",
        "brightness": "expr 4500. + 14500.*$f1",
        "body": "expr 0.78 + 0.25*$f1",
        "texture": "expr 0.94 + 0.06*$f1",
        "cabin_width": "expr 0.6 + 1.2*$f1",
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

    defaults = {"aggression": 0.55, "brightness": 12000.0, "body": 0.9, "texture": 0.97, "cabin_width": 1.5}
    for index, (name, value) in enumerate(defaults.items()):
        initial = p.new(f"loadmess {value:g}", 1040, 175 + index * 36, 100, numinlets=1, numoutlets=1)
        p.connect(initial, controls[name])

    ir_clip = p.new("clip 0. 1.", 1080, 355, 75, numinlets=3, numoutlets=1)
    dry_curve = p.new("expr sqrt(1.-$f1)", 1010, 395, 130, numinlets=1, numoutlets=1)
    wet_curve = p.new("expr sqrt($f1)", 1160, 395, 105, numinlets=1, numoutlets=1)
    dry_pack = p.new("pack 0. 80", 1010, 435, 85, numinlets=2, numoutlets=1)
    wet_pack = p.new("pack 0. 80", 1160, 435, 85, numinlets=2, numoutlets=1)
    dry_line = p.new("line~", 1010, 475, 50, numinlets=2, numoutlets=2)
    wet_line = p.new("line~", 1160, 475, 50, numinlets=2, numoutlets=2)
    ir_default = p.new("loadmess 0.18", 1080, 315, 105, numinlets=1, numoutlets=1)
    p.connect(router, ir_clip, 5)
    p.connect(ir_default, ir_clip)
    p.connect(ir_clip, dry_curve)
    p.connect(ir_clip, wet_curve)
    p.connect(dry_curve, dry_pack)
    p.connect(wet_curve, wet_pack)
    p.connect(dry_pack, dry_line)
    p.connect(wet_pack, wet_line)

    rpm_clip = p.new("clip 0. 10000.", 1240, 315, 105, numinlets=3, numoutlets=1)
    rpm_mid_curve = p.new("expr 1.-0.1*min(1.,max(0.,($f1-1500.)/2500.))", 1000, 525, 285, numinlets=1, numoutlets=1)
    rpm_high_curve = p.new("expr 1.-0.05*min(1.,max(0.,($f1-1500.)/2500.))", 1000, 565, 295, numinlets=1, numoutlets=1)
    rpm_mid_pack = p.new("pack 0. 80", 1000, 605, 85, numinlets=2, numoutlets=1)
    rpm_high_pack = p.new("pack 0. 80", 1120, 605, 85, numinlets=2, numoutlets=1)
    rpm_mid_line = p.new("line~", 1000, 645, 50, numinlets=2, numoutlets=2)
    rpm_high_line = p.new("line~", 1120, 645, 50, numinlets=2, numoutlets=2)
    rpm_default = p.new("loadmess 800.", 1240, 355, 100, numinlets=1, numoutlets=1)
    p.connect(router, rpm_clip, 6)
    p.connect(rpm_default, rpm_clip)
    p.connect(rpm_clip, rpm_mid_curve)
    p.connect(rpm_clip, rpm_high_curve)
    p.connect(rpm_mid_curve, rpm_mid_pack)
    p.connect(rpm_high_curve, rpm_high_pack)
    p.connect(rpm_mid_pack, rpm_mid_line)
    p.connect(rpm_high_pack, rpm_high_line)

    masters: list[str] = []
    for signal, x in ((left_in, 300), (right_in, 650)):
        lowpass = p.new("onepole~ 12000", x, 565, 105, numinlets=2, numoutlets=1)
        body_gain = p.new("*~", x, 605, 40, numinlets=2, numoutlets=1)
        texture_gain = p.new("*~", x, 640, 40, numinlets=2, numoutlets=1)
        master_gain = p.new("*~", x, 675, 40, numinlets=2, numoutlets=1)
        p.connect(signal, lowpass, 0, 0)
        p.connect(controls["brightness"], lowpass, 0, 1)
        p.connect(lowpass, body_gain, 0, 0)
        p.connect(controls["body"], body_gain, 0, 1)
        p.connect(body_gain, texture_gain, 0, 0)
        p.connect(controls["texture"], texture_gain, 0, 1)
        p.connect(texture_gain, master_gain, 0, 0)
        p.connect(controls["aggression"], master_gain, 0, 1)
        masters.append(master_gain)
    p.new("buffer~ cabin_ir_l cabin_ir_l.wav", 25, 740, 235, numinlets=2, numoutlets=2)
    p.new("buffer~ cabin_ir_r cabin_ir_r.wav", 25, 780, 235, numinlets=2, numoutlets=2)
    ir_l = p.new("buffir~ cabin_ir_l 0 4096", 300, 740, 180, numinlets=3, numoutlets=1)
    ir_r = p.new("buffir~ cabin_ir_r 0 4096", 650, 740, 180, numinlets=3, numoutlets=1)
    dry_l = p.new("*~", 300, 785, 40, numinlets=2, numoutlets=1)
    wet_l = p.new("*~", 390, 785, 40, numinlets=2, numoutlets=1)
    dry_r = p.new("*~", 650, 785, 40, numinlets=2, numoutlets=1)
    wet_r = p.new("*~", 740, 785, 40, numinlets=2, numoutlets=1)
    mixed_l = p.new("+~", 345, 830, 40, numinlets=2, numoutlets=1)
    mixed_r = p.new("+~", 695, 830, 40, numinlets=2, numoutlets=1)
    p.connect(masters[0], ir_l)
    p.connect(masters[1], ir_r)
    p.connect(masters[0], dry_l)
    p.connect(masters[1], dry_r)
    p.connect(ir_l, wet_l)
    p.connect(ir_r, wet_r)
    p.connect(dry_line, dry_l, 0, 1)
    p.connect(dry_line, dry_r, 0, 1)
    p.connect(wet_line, wet_l, 0, 1)
    p.connect(wet_line, wet_r, 0, 1)
    p.connect(dry_l, mixed_l, 0, 0)
    p.connect(wet_l, mixed_l, 0, 1)
    p.connect(dry_r, mixed_r, 0, 0)
    p.connect(wet_r, mixed_r, 0, 1)

    cross_l = p.new("cross~ 120", 300, 865, 80, numinlets=2, numoutlets=2)
    cross_r = p.new("cross~ 120", 650, 865, 80, numinlets=2, numoutlets=2)
    low_sum = p.new("+~", 395, 900, 40, numinlets=2, numoutlets=1)
    low_mid = p.new("*~ 0.5", 395, 935, 60, numinlets=2, numoutlets=1)
    phase_l = p.new("allpass~ 8. 1.7 0.42", 500, 865, 135, numinlets=3, numoutlets=1)
    phase_r = p.new("allpass~ 8. 2.3 -0.36", 790, 865, 145, numinlets=3, numoutlets=1)
    band_l = p.new("cross~ 2000", 500, 910, 90, numinlets=2, numoutlets=2)
    band_r = p.new("cross~ 2000", 790, 910, 90, numinlets=2, numoutlets=2)

    mid_sum = p.new("+~", 470, 950, 40, numinlets=2, numoutlets=1)
    mid_mid = p.new("*~ 0.5", 470, 985, 60, numinlets=2, numoutlets=1)
    mid_diff = p.new("-~", 570, 950, 40, numinlets=2, numoutlets=1)
    mid_side = p.new("*~ 0.5", 570, 985, 60, numinlets=2, numoutlets=1)
    mid_width = p.new("*~", 640, 985, 40, numinlets=2, numoutlets=1)
    mid_rpm = p.new("*~", 690, 985, 40, numinlets=2, numoutlets=1)
    mid_safe = p.new("*~ 0.24", 740, 985, 65, numinlets=2, numoutlets=1)
    mid_left = p.new("+~", 470, 1025, 40, numinlets=2, numoutlets=1)
    mid_right = p.new("-~", 570, 1025, 40, numinlets=2, numoutlets=1)

    high_sum = p.new("+~", 835, 950, 40, numinlets=2, numoutlets=1)
    high_mid = p.new("*~ 0.5", 835, 985, 60, numinlets=2, numoutlets=1)
    high_diff = p.new("-~", 935, 950, 40, numinlets=2, numoutlets=1)
    high_side = p.new("*~ 0.5", 935, 985, 60, numinlets=2, numoutlets=1)
    high_width = p.new("*~", 1005, 985, 40, numinlets=2, numoutlets=1)
    high_rpm = p.new("*~", 1055, 985, 40, numinlets=2, numoutlets=1)
    high_safe = p.new("*~ 0.26", 1105, 985, 65, numinlets=2, numoutlets=1)

    tap_l = p.new("tapin~ 8.", 1200, 900, 75, numinlets=1, numoutlets=1)
    reflect_l = p.new("tapout~ 0.65", 1200, 935, 85, numinlets=1, numoutlets=1)
    reflect_l_gain = p.new("*~ 0.04", 1200, 970, 65, numinlets=2, numoutlets=1)
    tap_r = p.new("tapin~ 8.", 1290, 900, 75, numinlets=1, numoutlets=1)
    reflect_r = p.new("tapout~ 1.35", 1290, 935, 85, numinlets=1, numoutlets=1)
    reflect_r_gain = p.new("*~ 0.04", 1290, 970, 65, numinlets=2, numoutlets=1)

    high_left = p.new("+~", 835, 1025, 40, numinlets=2, numoutlets=1)
    high_right = p.new("-~", 935, 1025, 40, numinlets=2, numoutlets=1)
    high_left_ref = p.new("+~", 835, 1065, 40, numinlets=2, numoutlets=1)
    high_right_ref = p.new("+~", 935, 1065, 40, numinlets=2, numoutlets=1)
    upper_l = p.new("+~", 590, 1105, 40, numinlets=2, numoutlets=1)
    upper_r = p.new("+~", 890, 1105, 40, numinlets=2, numoutlets=1)
    final_l = p.new("+~", 500, 1145, 40, numinlets=2, numoutlets=1)
    final_r = p.new("+~", 980, 1145, 40, numinlets=2, numoutlets=1)
    left = outlet(p, 500, 1185, signal=True)
    right = outlet(p, 980, 1185, signal=True)

    p.connect(mixed_l, cross_l)
    p.connect(mixed_r, cross_r)
    p.connect(cross_l, low_sum, 0, 0)
    p.connect(cross_r, low_sum, 0, 1)
    p.connect(low_sum, low_mid)
    p.connect(cross_l, phase_l, 1, 0)
    p.connect(cross_r, phase_r, 1, 0)
    p.connect(phase_l, band_l)
    p.connect(phase_r, band_r)
    p.connect(band_l, mid_sum, 0, 0)
    p.connect(band_r, mid_sum, 0, 1)
    p.connect(mid_sum, mid_mid)
    p.connect(band_l, mid_diff, 0, 0)
    p.connect(band_r, mid_diff, 0, 1)
    p.connect(mid_diff, mid_side)
    p.connect(mid_side, mid_width)
    p.connect(controls["cabin_width"], mid_width, 0, 1)
    p.connect(mid_width, mid_rpm)
    p.connect(rpm_mid_line, mid_rpm, 0, 1)
    p.connect(mid_rpm, mid_safe)
    p.connect(mid_mid, mid_left, 0, 0)
    p.connect(mid_safe, mid_left, 0, 1)
    p.connect(mid_mid, mid_right, 0, 0)
    p.connect(mid_safe, mid_right, 0, 1)
    p.connect(band_l, high_sum, 1, 0)
    p.connect(band_r, high_sum, 1, 1)
    p.connect(high_sum, high_mid)
    p.connect(band_l, high_diff, 1, 0)
    p.connect(band_r, high_diff, 1, 1)
    p.connect(high_diff, high_side)
    p.connect(high_side, high_width)
    p.connect(controls["cabin_width"], high_width, 0, 1)
    p.connect(high_width, high_rpm)
    p.connect(rpm_high_line, high_rpm, 0, 1)
    p.connect(high_rpm, high_safe)
    p.connect(band_r, tap_l, 1, 0)
    p.connect(tap_l, reflect_l)
    p.connect(reflect_l, reflect_l_gain)
    p.connect(band_l, tap_r, 1, 0)
    p.connect(tap_r, reflect_r)
    p.connect(reflect_r, reflect_r_gain)
    p.connect(high_mid, high_left, 0, 0)
    p.connect(high_safe, high_left, 0, 1)
    p.connect(high_mid, high_right, 0, 0)
    p.connect(high_safe, high_right, 0, 1)
    p.connect(high_left, high_left_ref, 0, 0)
    p.connect(reflect_l_gain, high_left_ref, 0, 1)
    p.connect(high_right, high_right_ref, 0, 0)
    p.connect(reflect_r_gain, high_right_ref, 0, 1)
    p.connect(mid_left, upper_l, 0, 0)
    p.connect(high_left_ref, upper_l, 0, 1)
    p.connect(mid_right, upper_r, 0, 0)
    p.connect(high_right_ref, upper_r, 0, 1)
    p.connect(low_mid, final_l, 0, 0)
    p.connect(upper_l, final_l, 0, 1)
    p.connect(low_mid, final_r, 0, 0)
    p.connect(upper_r, final_r, 0, 1)
    p.connect(final_l, left)
    p.connect(final_r, right)
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


def add_labeled_number(p: Patcher, label: str, name: str, x: float, y: float, engine: str) -> str:
    p.comment(label, x, y, 110)
    number = p.add("flonum", None, x, y + 24, 75, numinlets=1, numoutlets=2)
    bounded = p.new("clip 0. 1.", x, y + 58, 75, numinlets=3, numoutlets=1)
    named = p.new(f"prepend {name}", x, y + 92, 110, numinlets=1, numoutlets=1)
    p.connect(number, bounded)
    p.connect(bounded, named)
    p.connect(named, engine)
    return number


def add_labeled_db_number(
    p: Patcher,
    label: str,
    name: str,
    default_db: float,
    x: float,
    y: float,
    engine: str,
) -> str:
    p.comment(label, x, y, 150)
    number = p.add("flonum", None, x, y + 24, 75, numinlets=1, numoutlets=2)
    bounded = p.new("clip -60. 6.", x, y + 58, 85, numinlets=3, numoutlets=1)
    named = p.new(f"prepend {name}", x, y + 92, 155, numinlets=1, numoutlets=1)
    initial = p.new(f"loadmess {default_db:g}", x + 82, y + 24, 90, numinlets=1, numoutlets=1)
    p.connect(number, bounded)
    p.connect(bounded, named)
    p.connect(named, engine)
    p.connect(initial, number)
    return number


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
    p = Patcher(1680, 1600)
    p.comment("VehicleSoundSynth V4 — RPM-adaptive cabin field, dual Ferrari texture, 7-speed DCT, and final mix", 25, 15, 900)
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
    engine = p.add(
        "bpatcher", None, 650, 970, 1000, 370,
        numinlets=1, numoutlets=2, name="vehicle_engine~.maxpat",
    )
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
        "engine_type ev, ev_weight 1., v12_weight 0., v10_weight 0., aggression 0.25, brightness 0.72, body 0.34, texture 0.20, cabin_width 0.90, cabin_rumble 0., exhaust_boom 0., structure_vibration 0., cabin_ir_mix 0.10, powertrain_level_db -2., transient_level_db -9., road_level_db -14., rumble_level_db -60., pad_level_db -3., pad_mute 0, pad_solo 0, reference_texture_level_db -20., reference_texture_mute 0, master_trim_db -8.",
        "engine_type v12, ev_weight 0., v12_weight 1., v10_weight 0., aggression 0.62, brightness 0.78, body 0.72, texture 0.52, cabin_width 0.82, cabin_rumble 0.90, exhaust_boom 0.62, structure_vibration 0.58, cabin_ir_mix 0.20, powertrain_level_db -3., transient_level_db -7., road_level_db -16., rumble_level_db -5., pad_level_db -3., pad_mute 0, pad_solo 0, reference_texture_level_db -24., reference_texture_mute 0, master_trim_db -8.",
        "engine_type v10, ev_weight 0., v12_weight 0., v10_weight 1., aggression 0.90, brightness 0.66, body 0.84, texture 0.86, cabin_width 0.78, cabin_rumble 0.92, exhaust_boom 0.74, structure_vibration 0.72, cabin_ir_mix 0.18, powertrain_level_db -3., transient_level_db -6., road_level_db -16., rumble_level_db -4., pad_level_db -3., pad_mute 0, pad_solo 0, reference_texture_level_db -24., reference_texture_mute 0, master_trim_db -8.",
    ]
    preset_messages: list[str] = []
    for index, value in enumerate(presets):
        message = p.message(value, 465, 215 + index * 52, 760)
        preset_messages.append(message)
        p.connect(preset_select, message, index)
        p.connect(message, engine)
        p.connect(message, drive)
    preset_load = p.new("loadmess 0", 775, 165, 80, numinlets=1, numoutlets=1)
    p.connect(preset_load, preset)
    p.connect(preset, preset_select)

    ui_targets: dict[str, str] = {}
    weight_labels = (("EV Weight", "ev_weight"), ("V12 Weight", "v12_weight"), ("V10 Weight", "v10_weight"))
    for index, (label, name) in enumerate(weight_labels):
        ui_targets[name] = add_labeled_number(p, label, name, 325 + index * 135, 400, engine)
    macros = (("Aggression", "aggression"), ("Brightness", "brightness"), ("Body", "body"), ("Texture", "texture"), ("Cabin Width", "cabin_width"))
    for index, (label, name) in enumerate(macros):
        ui_targets[name] = add_labeled_number(p, label, name, 730 + index * 135, 400, engine)
    rumble_controls = (
        ("Cabin Rumble", "cabin_rumble"),
        ("Exhaust Boom", "exhaust_boom"),
        ("Structure Vibration", "structure_vibration"),
    )
    for index, (label, name) in enumerate(rumble_controls):
        ui_targets[name] = add_labeled_number(p, label, name, 730 + index * 180, 470, engine)
    ui_targets["cabin_ir_mix"] = add_labeled_number(
        p, "Cabin IR Mix", "cabin_ir_mix", 1270, 470, engine
    )

    stem_controls = (
        ("Powertrain dB", "powertrain_level_db", -3.0),
        ("Transient dB", "transient_level_db", -7.0),
        ("Road / Air dB", "road_level_db", -16.0),
        ("Rumble dB", "rumble_level_db", -5.0),
    )
    for index, (label, name, default_db) in enumerate(stem_controls):
        ui_targets[name] = add_labeled_db_number(
            p, label, name, default_db, 730 + index * 200, 565, engine
        )

    ui_targets["pad_level_db"] = add_labeled_db_number(
        p, "EV Pad dB", "pad_level_db", -3.0, 730, 635, engine
    )
    ui_targets["reference_texture_level_db"] = add_labeled_db_number(
        p, "Engine Texture dB", "reference_texture_level_db", -24.0, 930, 635, engine
    )
    for index, (label, name) in enumerate(
        (("Pad Mute", "pad_mute"), ("Pad Solo", "pad_solo"), ("Texture Mute", "reference_texture_mute"))
    ):
        x = 1130 + index * 150
        p.comment(label, x, 635, 110)
        toggle = p.add("toggle", None, x, 660, 24, 24, numinlets=1, numoutlets=1)
        named = p.new(f"prepend {name}", x + 35, 660, 110, numinlets=1, numoutlets=1)
        p.connect(toggle, named)
        p.connect(named, engine)
        ui_targets[name] = toggle

    p.comment("Fuel lifecycle", 25, 690, 140)
    p.comment("Ignition", 25, 720, 75)
    ignition_toggle = p.add("toggle", None, 25, 746, 24, 24, numinlets=1, numoutlets=1)
    ignition_named = p.new("prepend ignition", 60, 746, 105, numinlets=1, numoutlets=1)
    p.comment("Engine Start", 190, 720, 100)
    start_button = p.add("button", None, 190, 746, 24, 24, numinlets=1, numoutlets=1)
    start_value = p.message("1", 225, 746, 30)
    start_named = p.new("prepend start", 270, 746, 90, numinlets=1, numoutlets=1)
    p.comment("Automatic mode uses profile-aware 7-speed DCT shift points", 390, 725, 410)
    p.connect(load_off, ignition_toggle)
    p.connect(ignition_toggle, ignition_named)
    p.connect(ignition_named, engine)
    p.connect(ignition_named, drive)
    p.connect(start_button, start_value)
    p.connect(start_value, start_named)
    p.connect(start_named, engine)
    p.connect(start_named, drive)

    p.comment("Global four-band EQ", 25, 800, 190)
    add_eq_band(p, "Low Shelf", "eq_low", 25, 830, 90.0, engine)
    add_eq_band(p, "Low-Mid", "eq_lowmid", 265, 830, 250.0, engine, q=0.8)
    add_eq_band(p, "High-Mid", "eq_highmid", 515, 830, 3800.0, engine, q=1.0)
    add_eq_band(p, "High Shelf", "eq_high", 765, 830, 9000.0, engine)
    p.comment("EQ Bypass", 1010, 830, 90)
    eq_bypass = p.add("toggle", None, 1010, 858, 24, 24, numinlets=1, numoutlets=1)
    eq_bypass_named = p.new("prepend eq_bypass", 1045, 858, 120, numinlets=1, numoutlets=1)
    p.comment("Master Trim (dB)", 1200, 830, 125)
    trim = p.add("flonum", None, 1200, 858, 70, numinlets=1, numoutlets=2)
    trim_clip = p.new("clip -24. 0.", 1200, 892, 85, numinlets=3, numoutlets=1)
    trim_named = p.new("prepend master_trim_db", 1200, 926, 155, numinlets=1, numoutlets=1)
    trim_default = p.new("loadmess -8.", 1300, 858, 95, numinlets=1, numoutlets=1)
    p.connect(load_off, eq_bypass)
    p.connect(eq_bypass, eq_bypass_named)
    p.connect(eq_bypass_named, engine)
    p.connect(trim, trim_clip)
    p.connect(trim_clip, trim_named)
    p.connect(trim_named, engine)
    p.connect(trim_default, trim)
    ui_targets["master_trim_db"] = trim

    sync_names = (
        "ev_weight", "v12_weight", "v10_weight", "aggression", "brightness",
        "body", "texture", "cabin_width", "cabin_rumble", "exhaust_boom",
        "structure_vibration", "cabin_ir_mix", "powertrain_level_db", "transient_level_db",
        "road_level_db", "rumble_level_db", "master_trim_db",
        "pad_level_db", "pad_mute", "pad_solo", "reference_texture_level_db",
        "reference_texture_mute",
    )
    p.comment("Preset/UI state synchronizer", 1380, 830, 220)
    preset_sync = route(p, sync_names, 1380, 860, 280)
    for message in preset_messages:
        p.connect(message, preset_sync)
    for index, name in enumerate(sync_names):
        p.connect(preset_sync, ui_targets[name], index)

    mute_l = p.new("*~", 1460, 1010, 40, numinlets=2, numoutlets=1)
    mute_r = p.new("*~", 1550, 1010, 40, numinlets=2, numoutlets=1)
    p.comment("Post-EQ stereo monitoring", 1450, 970, 210)
    meter_l = p.add("meter~", None, 1460, 1060, 65, numinlets=1, numoutlets=1)
    meter_r = p.add("meter~", None, 1550, 1060, 65, numinlets=1, numoutlets=1)
    spectrum_l = p.add("spectroscope~", None, 1440, 1120, 105, numinlets=2, numoutlets=1)
    spectrum_r = p.add("spectroscope~", None, 1550, 1120, 105, numinlets=2, numoutlets=1)
    dac = p.add("ezdac~", None, 1510, 1240, 65, 48, numinlets=2, numoutlets=0)
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

    # Manual-only keyboard pedals. Key-repeat events are collapsed by `change`
    # so a held key follows one uninterrupted linear envelope. Leaving Manual
    # mode releases both pedals to prevent a hidden stuck throttle or brake.
    p.comment(
        "Manual keyboard: hold W = throttle up; release W = throttle down; hold S = fast brake; release S = brake off",
        25,
        215,
        430,
    )
    key_down = p.new("key", 25, 1270, 45, numinlets=0, numoutlets=1)
    key_up = p.new("keyup", 85, 1270, 55, numinlets=0, numoutlets=1)
    down_select = p.new("sel 119 87 115 83", 25, 1310, 125, numinlets=1, numoutlets=5)
    up_select = p.new("sel 119 87 115 83", 165, 1310, 125, numinlets=1, numoutlets=5)
    manual_enabled = p.new("== 0", 305, 1270, 45, numinlets=2, numoutlets=1)
    manual_disabled = p.new("sel 0", 365, 1270, 45, numinlets=1, numoutlets=2)
    w_gate = p.new("gate 1", 25, 1350, 55, numinlets=2, numoutlets=1)
    s_gate = p.new("gate 1", 165, 1350, 55, numinlets=2, numoutlets=1)
    w_pressed = p.message("1", 90, 1350, 30)
    w_released = p.message("0", 125, 1350, 30)
    s_pressed = p.message("1", 230, 1350, 30)
    s_released = p.message("0", 265, 1350, 30)
    release_both = p.message("0", 425, 1270, 30)
    w_change = p.new("change", 25, 1390, 55, numinlets=1, numoutlets=3)
    s_change = p.new("change", 165, 1390, 55, numinlets=1, numoutlets=3)
    w_state = p.new("sel 1 0", 25, 1430, 55, numinlets=1, numoutlets=3)
    s_state = p.new("sel 1 0", 165, 1430, 55, numinlets=1, numoutlets=3)
    throttle_up = p.message("1. 2500", 25, 1470, 65)
    throttle_release = p.message("0. 1400", 95, 1470, 65)
    brake_on = p.message("1. 120", 165, 1470, 55)
    brake_off = p.message("0.", 225, 1470, 30)
    throttle_line = p.new("line 0.", 25, 1510, 60, numinlets=2, numoutlets=2)
    brake_line = p.new("line 0.", 165, 1510, 60, numinlets=2, numoutlets=2)
    throttle_state_set = p.new("prepend set", 95, 1510, 85, numinlets=1, numoutlets=1)
    brake_state_set = p.new("prepend set", 235, 1510, 85, numinlets=1, numoutlets=1)
    throttle_display_set = p.new("prepend set", 25, 1550, 85, numinlets=1, numoutlets=1)
    brake_display_set = p.new("prepend set", 165, 1550, 85, numinlets=1, numoutlets=1)

    p.connect(key_down, down_select)
    p.connect(key_up, up_select)
    for outlet_index in (0, 1):
        p.connect(down_select, w_pressed, outlet_index)
        p.connect(up_select, w_released, outlet_index)
    for outlet_index in (2, 3):
        p.connect(down_select, s_pressed, outlet_index)
        p.connect(up_select, s_released, outlet_index)
    p.connect(mode, manual_enabled)
    p.connect(manual_enabled, manual_disabled)
    p.connect(manual_enabled, w_gate, 0, 0)
    p.connect(manual_enabled, s_gate, 0, 0)
    p.connect(w_pressed, w_gate, 0, 1)
    p.connect(w_released, w_gate, 0, 1)
    p.connect(s_pressed, s_gate, 0, 1)
    p.connect(s_released, s_gate, 0, 1)
    p.connect(manual_disabled, release_both, 0)
    p.connect(release_both, w_change)
    p.connect(release_both, s_change)
    p.connect(w_gate, w_change)
    p.connect(s_gate, s_change)
    p.connect(w_change, w_state)
    p.connect(s_change, s_state)
    p.connect(w_state, throttle_up, 0)
    p.connect(w_state, throttle_release, 1)
    p.connect(s_state, brake_on, 0)
    p.connect(s_state, brake_off, 1)
    p.connect(throttle_up, throttle_line)
    p.connect(throttle_release, throttle_line)
    p.connect(brake_on, brake_line)
    p.connect(brake_off, brake_line)
    p.connect(throttle, throttle_state_set)
    p.connect(throttle_state_set, throttle_line)
    p.connect(brake, brake_state_set)
    p.connect(brake_state_set, brake_line)
    p.connect(throttle_line, throttle_clip)
    p.connect(brake_line, brake_clip)
    p.connect(throttle_line, throttle_display_set)
    p.connect(throttle_display_set, throttle)
    p.connect(brake_line, brake_display_set)
    p.connect(brake_display_set, brake)
    return p.document(presentation=False)


LEGACY_GEN_CODE = {
    "v12_powertrain": """// Lifecycle-gated four-stroke V12 with idle body and load-dependent harmonic lift.\nParam rpm(780, min=0, max=10000);\nParam throttle(0, min=0, max=1);\nParam load(0, min=-1, max=1);\nParam aggression(0.6, min=0, max=1);\nParam brightness(0.75, min=0, max=1);\nParam body(0.7, min=0, max=1);\nParam texture(0.5, min=0, max=1);\nParam engine_running(0, min=0, max=1);\nParam combustion_gain(0, min=0, max=1);\nParam shift_cut(1, min=0, max=1);\nr = slide(clamp(rpm, 0, 10000), 700, 1100);\nt = slide(clamp(throttle, 0, 1), 420, 850);\nl = max(clamp(load, -1, 1), 0);\nrun = slide(clamp(engine_running * combustion_gain * shift_cut, 0, 1), 480, 1900);\nspeedmix = clamp((r - 780) / 8220, 0, 1);\nrough = 1 + cycle(1.31) * (0.004 * (1-speedmix)) + cycle(2.17) * 0.0015;\nf = clamp(r / 60 * 6 * rough, 35, 1000);\nidle = 0.145 + body * 0.035;\na = clamp(idle + t * 0.26 + l * 0.13, 0, 0.56) * run;\nsub = cycle(clamp(f * 0.5, 24, 520)) * (0.34 + body * 0.24) * (1-speedmix*0.45);\nfund = cycle(f) * (0.58 + body * 0.12);\nh2 = cycle(clamp(f * 2, 45, 3000)) * (0.16 + brightness * 0.18 + speedmix * 0.12);\nh3 = cycle(clamp(f * 3, 55, 5000)) * (0.07 + texture * 0.11 + speedmix * 0.12);\nh5 = cycle(clamp(f * 5, 70, 8000)) * (0.025 + brightness * speedmix * 0.10);\nh8 = cycle(clamp(f * 8, 90, 11000)) * (0.008 + texture * speedmix * 0.055);\nintake = cycle(clamp(f * 1.5, 45, 1800)) * t * (0.035 + texture * 0.055);\nleft = (sub + fund + h2 + h3 + h5 + h8 + intake) * a * (0.82 + aggression * 0.15);\nright = (cycle(clamp(f * 0.5015, 24, 520)) * (0.32 + body*0.22) * (1-speedmix*0.45) + cycle(f * 0.9985) * 0.58 + h2*0.96 + h3*1.03 + h5*0.98 + h8*1.04 + intake) * a * (0.82 + aggression*0.15);\nout1 = clamp(left, -0.86, 0.86);\nout2 = clamp(right, -0.86, 0.86);""",
    "v10_powertrain": """// Lifecycle-gated four-stroke V10 with stronger half-order rumble and uneven sidebands.\nParam rpm(850, min=0, max=10000);\nParam throttle(0, min=0, max=1);\nParam load(0, min=-1, max=1);\nParam aggression(0.9, min=0, max=1);\nParam brightness(0.65, min=0, max=1);\nParam body(0.85, min=0, max=1);\nParam texture(0.85, min=0, max=1);\nParam engine_running(0, min=0, max=1);\nParam combustion_gain(0, min=0, max=1);\nParam shift_cut(1, min=0, max=1);\nr = slide(clamp(rpm, 0, 10000), 620, 980);\nt = slide(clamp(throttle, 0, 1), 360, 760);\nl = max(clamp(load, -1, 1), 0);\nrun = slide(clamp(engine_running * combustion_gain * shift_cut, 0, 1), 420, 1650);\nspeedmix = clamp((r - 850) / 7650, 0, 1);\nrough = 1 + cycle(0.93) * (0.008 * (1-speedmix)) + cycle(1.71) * 0.003;\nf = clamp(r / 60 * 5 * rough, 32, 850);\nidle = 0.165 + body * 0.04;\na = clamp(idle + t * 0.29 + l * 0.15, 0, 0.60) * run;\nsub = cycle(clamp(f * 0.5, 24, 450)) * (0.42 + body * 0.24) * (1-speedmix*0.38);\nfire = cycle(f) * (0.50 + aggression * 0.16);\nside = cycle(clamp(f * 1.5, 48, 1900)) * (0.06 + texture * 0.10);\nh2 = cycle(clamp(f * 2, 55, 3400)) * (0.11 + brightness * 0.14);\nrasp = cycle(clamp(f * 2.5, 65, 5000)) * (0.08 + texture * 0.17 + speedmix * 0.10);\nmetal = cycle(clamp(f * 5, 90, 8500)) * brightness * speedmix * 0.075;\nleft = (sub + fire + side + h2 + rasp + metal) * a;\nright = (cycle(clamp(f * 0.503, 24, 450)) * (0.40 + body*0.22) * (1-speedmix*0.38) + cycle(f*0.997)*0.50 + side*1.08 + h2*0.94 + rasp*1.06 + metal) * a;\nout1 = clamp(left, -0.88, 0.88);\nout2 = clamp(right, -0.88, 0.88);""",
    "cabin_rumble": """// Strong but bounded in-cabin combustion rumble with centered low-frequency output.\nParam firing_order(0, min=0, max=6);\nParam rpm(780, min=0, max=10000);\nParam throttle(0, min=0, max=1);\nParam load(0, min=-1, max=1);\nParam gear(1, min=1, max=7);\nParam engine_running(0, min=0, max=1);\nParam combustion_gain(0, min=0, max=1);\nParam shift_cut(1, min=0, max=1);\nParam cabin_rumble(0, min=0, max=1);\nParam exhaust_boom(0, min=0, max=1);\nParam structure_vibration(0, min=0, max=1);\nParam body(0.7, min=0, max=1);\nParam aggression(0.6, min=0, max=1);\nr = slide(clamp(rpm, 0, 10000), 700, 1200);\nt = slide(clamp(throttle, 0, 1), 420, 900);\nl = max(clamp(load, -1, 1), 0);\ng = clamp(gear, 1, 7);\norder = clamp(firing_order, 0, 6);\nfuel = clamp(order / 5, 0, 1);\nrun = slide(clamp(engine_running * combustion_gain, 0, 1), 360, 2200);\nshift = slide(clamp(0.35 + 0.65 * shift_cut, 0, 1), 150, 1100);\nfire_hz = clamp(r / 60 * order, 28, 1000);\nhalf_hz = clamp(fire_hz * 0.5, 28, 420);\nspeedmix = clamp((r - 780) / 8220, 0, 1);\nidle_weight = 1 - speedmix * 0.55;\ndrive_weight = 0.45 + 0.55 * max(t, l);\ngear_weight = 0.86 + 0.02 * g;\nrough = 1 + cycle(1.17) * (0.006 * idle_weight) + cycle(2.03) * 0.002;\nmount = (cycle(half_hz * rough) * 0.72 + cycle(clamp(half_hz * 1.5, 35, 630)) * 0.18) * structure_vibration * (0.055 + body * 0.045) * idle_weight;\nmode_pulse = 0.62 + 0.38 * abs(cycle(clamp(fire_hz * 0.5, 28, 500)));\nmode1 = cycle(clamp(48 + (half_hz - 39) * 0.10, 44, 54)) * 0.45;\nmode2 = cycle(clamp(68 + (half_hz - 39) * 0.08, 63, 74)) * 0.33;\nmode3 = cycle(clamp(92 + (half_hz - 39) * 0.06, 86, 100)) * 0.20;\nmode4 = cycle(clamp(118 + (half_hz - 39) * 0.04, 110, 126)) * 0.12;\ncabin = (mode1 + mode2 + mode3 + mode4) * mode_pulse * cabin_rumble * (0.025 + body * 0.020) * (0.70 + idle_weight * 0.30);\nexhaust = (cycle(half_hz) * 0.65 + cycle(fire_hz) * 0.25 + cycle(clamp(fire_hz * 2, 56, 2000)) * 0.10) * exhaust_boom * (0.025 + t * 0.055 + l * 0.045) * (0.80 + aggression * 0.20);\nsig = clamp((mount + cabin + exhaust * drive_weight) * run * shift * gear_weight * fuel * 1.18, -0.48, 0.48);\nout1 = sig;\nout2 = sig;""",
}

# Only the current models below are emitted. The legacy dictionary is retained
# solely as migration context and cannot leak into generated project artifacts.
GEN_CODE: dict[str, str] = {}
GEN_CODE.update({
    "ev_powertrain": """// Phase-coherent EV motor: stable low fundamental with harmonic upper structure.
Param rpm(650, min=0, max=10000);
Param throttle(0, min=0, max=1);
Param load(0, min=-1, max=1);
Param aggression(0.25, min=0, max=1);
Param brightness(0.7, min=0, max=1);
Param body(0.35, min=0, max=1);
Param texture(0.2, min=0, max=1);
r = slide(clamp(rpm, 0, 10000), 1200, 1800);
t = slide(clamp(throttle, 0, 1), 700, 1400);
l = abs(clamp(load, -1, 1));
f = clamp(55 + r * 0.052, 55, 760);
a = clamp(0.03 + t * 0.20 + l * 0.05, 0, 0.28);
coherent_low = cycle(f) * (0.58 + body * 0.18);
h2 = cycle(clamp(f * 2, 110, 1520)) * (0.08 + body * 0.05);
h3 = cycle(clamp(f * 3, 165, 2280)) * (0.035 + texture * 0.055);
inverter = cycle(clamp(f * (2.8 + brightness), 150, 4200)) * (0.10 + texture * 0.14);
sheen_l = cycle(clamp(f * (5.2 + brightness * 0.4), 300, 6200)) * aggression * 0.025;
sheen_r = cycle(clamp(f * (6.2 + brightness * 0.4), 360, 7200)) * aggression * 0.025;
base = coherent_low + h2 + h3 + inverter;
left_drive = (base + sheen_l) * a;
right_drive = (coherent_low + h2 * 0.99 + h3 * 1.02 + inverter * 0.98 + sheen_r) * a;
out1 = tanh(left_drive * 1.2) / 1.2;
out2 = tanh(right_drive * 1.2) / 1.2;""",
    "v12_powertrain": """// Four-stroke V12: two phase-locked six-cylinder banks and load-shaped combustion residual.
Param rpm(780, min=0, max=10000);
Param throttle(0, min=0, max=1);
Param load(0, min=-1, max=1);
Param aggression(0.6, min=0, max=1);
Param brightness(0.75, min=0, max=1);
Param body(0.7, min=0, max=1);
Param texture(0.5, min=0, max=1);
Param engine_running(0, min=0, max=1);
Param combustion_gain(0, min=0, max=1);
Param shift_cut(1, min=0, max=1);
r = slide(clamp(rpm, 0, 10000), 700, 1100);
t = slide(clamp(throttle, 0, 1), 420, 850);
l = max(clamp(load, -1, 1), 0);
run = slide(clamp(engine_running * combustion_gain * shift_cut, 0, 1), 480, 1900);
speedmix = clamp((r - 780) / 8220, 0, 1);
events = 6;
crank = clamp(r / 60, 6, 170);
bank_events = 3;
cycle_variation = clamp(cycle(crank * 0.5) * 0.020 + cycle(crank * 1.5) * 0.008, -0.03, 0.03);
bank_fire = clamp(crank * bank_events * (1 + cycle_variation), 18, 525);
fire = bank_fire * 2;
bank_phase_l = phasor(bank_fire);
bank_phase_r = bank_phase_l + 0.5;
bank_phase_r = bank_phase_r - floor(bank_phase_r);
sharpness = 8 + t * 7 + aggression * 3;
pulse_mean = (1 - exp(-sharpness)) / sharpness;
pulse_l = exp(-bank_phase_l * sharpness) - pulse_mean;
pulse_r = exp(-bank_phase_r * sharpness) - pulse_mean;
cylinder = 0.97 + cycle(crank * 0.5) * (0.020 + speedmix * 0.035) + cycle(crank * 1.5) * (0.010 + speedmix * 0.020);
idle = 0.205 + body * 0.050;
a = clamp(idle + t * 0.30 + l * 0.16, 0, 0.67) * run;
sub = cycle(clamp(fire * 0.5, 24, 520)) * (0.055 + body * 0.045) * (1-speedmix*0.55);
h1 = cycle(fire) * (0.16 + body * 0.08);
h2 = cycle(clamp(fire * 2, 45, 3200)) * (0.0945 + brightness * 0.108 + speedmix * 0.081);
h3 = cycle(clamp(fire * 3, 55, 5200)) * (0.05625 + texture * 0.06875 + speedmix * 0.0625);
h4 = cycle(clamp(fire * 4, 70, 7000)) * speedmix * (0.025 + brightness * 0.050);
h6 = cycle(clamp(fire * 6, 90, 9800)) * brightness * speedmix * 0.025;
h8 = cycle(clamp(fire * 8, 110, 12000)) * texture * speedmix * 0.014;
sideband_low = cycle(clamp(fire * 0.83, 35, 1500)) * (0.018 + speedmix * 0.075);
sideband_high = cycle(clamp(fire * 1.17, 40, 1900)) * (0.018 + speedmix * 0.072);
order23 = cycle(clamp(fire * 2.33, 60, 4100)) * speedmix * 0.045;
order27 = cycle(clamp(fire * 2.67, 70, 4700)) * speedmix * 0.040;
intake = cycle(clamp(fire * 1.5, 45, 2200)) * t * (0.025 + texture * 0.040);
residual_gate_l = clamp(abs(pulse_l) * 1.7, 0, 1);
residual_gate_r = clamp(abs(pulse_r) * 1.7, 0, 1);
residual_l = (cycle(clamp(fire * 1.33, 40, 2200)) * 0.040 + cycle(clamp(fire * 2.17, 65, 4200)) * 0.024) * residual_gate_l * (0.35 + texture * 0.65);
residual_r = (cycle(clamp(fire * 1.33, 40, 2200)) * 0.040 + cycle(clamp(fire * 2.17, 65, 4200)) * 0.024) * residual_gate_r * (0.35 + texture * 0.65);
bank_l = (pulse_l * 0.88 + pulse_r * 0.12) * cylinder * (0.48 + body * 0.16) * (1 - speedmix * 0.30);
bank_r = (pulse_r * 0.88 + pulse_l * 0.12) * cylinder * (0.48 + body * 0.16) * (1 - speedmix * 0.30);
resonance = sub + h1 + sideband_low + sideband_high + h2 + order23 + order27 + h3 + h4 + h6 + h8 + intake;
left_drive = (bank_l + resonance + residual_l) * a * (0.86 + aggression * 0.14);
right_drive = (bank_r + resonance + residual_r) * a * (0.86 + aggression * 0.14);
out1 = clamp(tanh(left_drive * 1.35) / 1.25, -0.86, 0.86);
out2 = clamp(tanh(right_drive * 1.35) / 1.25, -0.86, 0.86);""",
    "v10_powertrain": """// Four-stroke V10: phase-locked five-cylinder banks with odd-order intake colour.
Param rpm(850, min=0, max=10000);
Param throttle(0, min=0, max=1);
Param load(0, min=-1, max=1);
Param aggression(0.9, min=0, max=1);
Param brightness(0.65, min=0, max=1);
Param body(0.85, min=0, max=1);
Param texture(0.85, min=0, max=1);
Param engine_running(0, min=0, max=1);
Param combustion_gain(0, min=0, max=1);
Param shift_cut(1, min=0, max=1);
r = slide(clamp(rpm, 0, 10000), 620, 980);
t = slide(clamp(throttle, 0, 1), 360, 760);
l = max(clamp(load, -1, 1), 0);
run = slide(clamp(engine_running * combustion_gain * shift_cut, 0, 1), 420, 1650);
speedmix = clamp((r - 850) / 7650, 0, 1);
events = 5;
crank = clamp(r / 60, 6, 170);
bank_events = 2.5;
cycle_variation = clamp(cycle(crank * 0.5) * 0.024 + cycle(crank * 2.5) * 0.006, -0.03, 0.03);
bank_fire = clamp(crank * bank_events * (1 + cycle_variation), 16, 450);
fire = bank_fire * 2;
bank_phase_l = phasor(bank_fire);
bank_phase_r = bank_phase_l + 0.5;
bank_phase_r = bank_phase_r - floor(bank_phase_r);
sharpness = 7 + t * 9 + aggression * 4;
pulse_mean = (1 - exp(-sharpness)) / sharpness;
pulse_l = exp(-bank_phase_l * sharpness) - pulse_mean;
pulse_r = exp(-bank_phase_r * sharpness) - pulse_mean;
cylinder = 0.95 + cycle(crank * 0.5) * (0.030 + speedmix * 0.045) + cycle(crank * 2.5) * (0.016 + speedmix * 0.024);
idle = 0.225 + body * 0.055;
a = clamp(idle + t * 0.32 + l * 0.18, 0, 0.70) * run;
sub = cycle(clamp(fire * 0.5, 24, 460)) * (0.060 + body * 0.052) * (1-speedmix*0.50);
h1 = cycle(fire) * (0.17 + aggression * 0.08);
h15 = cycle(clamp(fire * 1.5, 45, 1800)) * (0.040 + texture * 0.050);
h2 = cycle(clamp(fire * 2, 55, 3500)) * (0.08775 + brightness * 0.0945 + speedmix * 0.07425);
h25 = cycle(clamp(fire * 2.5, 65, 5200)) * (0.055 + texture * 0.075 + speedmix * 0.060);
h3 = cycle(clamp(fire * 3, 75, 6500)) * (0.0425 + aggression * 0.050 + speedmix * 0.050);
h5 = cycle(clamp(fire * 5, 95, 9000)) * brightness * speedmix * 0.040;
h7 = cycle(clamp(fire * 7, 120, 12000)) * texture * speedmix * 0.020;
sideband_low = cycle(clamp(fire * 0.81, 32, 1450)) * (0.022 + speedmix * 0.080);
sideband_high = cycle(clamp(fire * 1.19, 40, 1900)) * (0.022 + speedmix * 0.078);
order22 = cycle(clamp(fire * 2.20, 60, 4000)) * speedmix * 0.070;
order28 = cycle(clamp(fire * 2.80, 75, 5100)) * speedmix * 0.060;
intake_fm = fire * 1.25 * (1 + cycle(crank) * 0.008);
intake = cycle(clamp(intake_fm, 45, 2600)) * t * (0.035 + texture * 0.055);
residual_gate_l = clamp(abs(pulse_l) * 1.8, 0, 1);
residual_gate_r = clamp(abs(pulse_r) * 1.8, 0, 1);
residual_l = (cycle(clamp(fire * 1.37, 40, 2300)) * 0.045 + cycle(clamp(fire * 2.23, 65, 4300)) * 0.028) * residual_gate_l * (0.30 + texture * 0.70);
residual_r = (cycle(clamp(fire * 1.37, 40, 2300)) * 0.045 + cycle(clamp(fire * 2.23, 65, 4300)) * 0.028) * residual_gate_r * (0.30 + texture * 0.70);
bank_l = (pulse_l * 0.86 + pulse_r * 0.14) * cylinder * (0.50 + body * 0.16) * (1 - speedmix * 0.32);
bank_r = (pulse_r * 0.86 + pulse_l * 0.14) * cylinder * (0.50 + body * 0.16) * (1 - speedmix * 0.32);
resonance = sub + h1 + sideband_low + sideband_high + h15 + h2 + order22 + h25 + order28 + h3 + h5 + h7 + intake;
left_drive = (bank_l + resonance + residual_l) * a * (0.88 + aggression * 0.12);
right_drive = (bank_r + resonance + residual_r) * a * (0.88 + aggression * 0.12);
out1 = clamp(tanh(left_drive * 1.42) / 1.27, -0.88, 0.88);
out2 = clamp(tanh(right_drive * 1.42) / 1.27, -0.88, 0.88);""",
})
# Cabin rumble is now a signal-driven MSP resonator bank fed by the same
# combustion signal as the main powertrain; the former free-running Gen model
# is deliberately not emitted or declared.
GEN_CODE.pop("cabin_rumble", None)


def make_gen(code: str) -> dict[str, Any]:
    """Build a Gen patcher and expose every codebox Param at patcher scope."""
    matches = re.findall(
        r"^Param\s+(\w+)\(([-+0-9.]+),\s*min=([-+0-9.]+),\s*max=([-+0-9.]+)\);",
        code,
        flags=re.MULTILINE,
    )
    boxes = [
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
                "id": "obj-2", "maxclass": "newobj", "numinlets": 1,
                "numoutlets": 0, "patching_rect": [40.0, 640.0, 45.0, 22.0],
                "text": "out 1",
            }
        },
        {
            "box": {
                "id": "obj-3", "maxclass": "newobj", "numinlets": 1,
                "numoutlets": 0, "patching_rect": [120.0, 640.0, 45.0, 22.0],
                "text": "out 2",
            }
        },
    ]
    for index, (name, default, minimum, maximum) in enumerate(matches, start=4):
        boxes.append({
            "box": {
                "id": f"obj-{index}", "maxclass": "newobj", "numinlets": 0,
                "numoutlets": 1,
                "patching_rect": [840.0, 40.0 + (index - 4) * 32.0, 220.0, 22.0],
                "text": f"param {name} {default} @min {minimum} @max {maximum}",
            }
        })
    return {
        "patcher": {
            "appversion": APP_VERSION,
            "boxes": boxes,
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
        "cabin_width": 0.78,
        "cabin_rumble": 0.92,
        "exhaust_boom": 0.74,
        "structure_vibration": 0.72,
        "cabin_ir_mix": 0.18,
        "powertrain_level_db": -3.0,
        "transient_level_db": -6.0,
        "road_level_db": -16.0,
        "rumble_level_db": -4.0,
        "pad_level_db": -3.0,
        "pad_mute": 0.0,
        "pad_solo": 0.0,
        "reference_texture_level_db": -24.0,
        "reference_texture_mute": 0.0,
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
        "cabin_width": 0.90,
        "cabin_rumble": 0.0,
        "exhaust_boom": 0.0,
        "structure_vibration": 0.0,
        "cabin_ir_mix": 0.10,
        "powertrain_level_db": -2.0,
        "transient_level_db": -9.0,
        "road_level_db": -14.0,
        "rumble_level_db": -60.0,
        "pad_level_db": -3.0,
        "pad_mute": 0.0,
        "pad_solo": 0.0,
        "reference_texture_level_db": -20.0,
        "reference_texture_mute": 0.0,
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
        "cabin_width": 0.82,
        "cabin_rumble": 0.90,
        "exhaust_boom": 0.62,
        "structure_vibration": 0.58,
        "cabin_ir_mix": 0.20,
        "powertrain_level_db": -3.0,
        "transient_level_db": -7.0,
        "road_level_db": -16.0,
        "rumble_level_db": -5.0,
        "pad_level_db": -3.0,
        "pad_mute": 0.0,
        "pad_solo": 0.0,
        "reference_texture_level_db": -24.0,
        "reference_texture_mute": 0.0,
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
        if name.startswith("cabin_ir_"):
            side = 1 if name.endswith("_l") else -1
            reflections = {
                0: 0.72,
                61 + side * 7: 0.18,
                137 - side * 11: -0.12,
                263 + side * 17: 0.09,
                487 - side * 23: -0.055,
                811 + side * 31: 0.032,
            }
            value = reflections.get(index, 0.0)
        elif name == "reference_texture_fallback":
            # A seamless, narrow-band combustion residual. Runtime gain is low;
            # this exists only to avoid missing-buffer errors without local media.
            value = (
                0.115 * math.sin(2.0 * math.pi * 160.0 * time)
                + 0.060 * math.sin(2.0 * math.pi * 320.0 * time + 0.35)
                + 0.032 * math.sin(2.0 * math.pi * 480.0 * time + 0.8)
                + 0.018 * math.sin(2.0 * math.pi * 800.0 * time + 1.1)
            )
        elif name.startswith("starter_"):
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
    channels = 2 if name == "reference_texture_fallback" else 1
    if channels == 2:
        delayed = 17
        payload = b"".join(
            struct.pack(
                "<hh",
                round(sample * 32767.0),
                round((0.88 * sample + 0.12 * samples[(index - delayed) % frames]) * 32767.0),
            )
            for index, sample in enumerate(samples)
        )
    else:
        payload = b"".join(struct.pack("<h", round(sample * 32767.0)) for sample in samples)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(channels)
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
        "patchers/ev_pad_driver~.maxpat",
        "patchers/ev_pad_beap~.maxpat",
        "patchers/reference_texture~.maxpat",
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
    for name in ENGINE_TEXTURE_FILES:
        contents["media"][f"media/{name}"] = {"kind": "mediafile", "local": 1}
    contents["data"]["presets/sound_dna.json"] = {"kind": "data", "local": 1}
    contents["data"]["assets/ferrari_sf90_acoustic_target.json"] = {"kind": "data", "local": 1}
    contents["data"]["assets/engine_texture_bank.json"] = {"kind": "data", "local": 1}
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
            for name in ("patchers", "gen", "code", "media", "presets")
        },
        "showdependencies": 1,
        "version": 1,
        "viewrect": [80.0, 80.0, 620.0, 780.0],
    }


def build_project(root: Path) -> None:
    stale_signal_independent_rumble = root / "gen" / "cabin_rumble.gendsp"
    if stale_signal_independent_rumble.is_file():
        stale_signal_independent_rumble.unlink()
    outputs = {
        "main.maxpat": make_main(),
        "patchers/vehicle_engine~.maxpat": make_engine(),
        "patchers/engine_controller.maxpat": make_engine_controller(),
        "patchers/powertrain~.maxpat": make_powertrain(),
        "patchers/ev_pad_driver~.maxpat": make_ev_pad_driver(),
        "patchers/reference_texture~.maxpat": make_reference_texture(),
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
    user_pad = root / "patchers" / "ev_pad_beap~.maxpat"
    if not user_pad.exists():
        write_json(user_pad, make_ev_pad_beap())
    for name, code in GEN_CODE.items():
        write_json(root / "gen" / f"{name}.gendsp", make_gen(code))
    for name, frames in MEDIA_FRAMES.items():
        media_path = root / "media" / f"{name}.wav"
        # Curated recordings and IRs are source assets, never disposable build
        # products. Generate deterministic fallback media only when absent.
        if not media_path.exists():
            write_wav(media_path, name, frames)


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
