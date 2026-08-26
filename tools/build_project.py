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
PROJECT_NAME = "VehicleSoundSynth-V5"
PROJECT_FILENAME = f"{PROJECT_NAME}.maxproj"
VEHICLE_BUS_EQ_DEFAULT = {
    "schema_version": 1,
    "bands": {
        "eq_low": [90.0, 0.0],
        "eq_lowmid": [250.0, 0.0, 0.8],
        "eq_highmid": [3800.0, 0.0, 1.0],
        "eq_high": [9000.0, 0.0],
        "eq_bypass": [0],
    },
}
BEAP_CLIPPING_ROOT = Path(
    "/Applications/Max.app/Contents/Resources/C74/packages/BEAP/clippings/BEAP"
)
BEAP_CLIPPING_SHA256 = {
    "Oscillator/bp.Oscillator.maxpat": "b911b4447ae94090f1e64582eca1e761e7a3593d5d9852369e4644a1a42efc2b",
    "Mixers/bp.Audio Mixer.maxpat": "e63e00727b7bd5bf8b5aa8119dc276578ba9122e7e282040364aa82435061ce5",
    "Filter/bp.Ladder.maxpat": "1292c18863374400f4f1924939c3321fb66c0f04dae357184a373f819be3c380",
    "Envelope/bp.ADSR.maxpat": "86e9594b9aa21a6794eb544f3ecb9730d2154e60acefdbc903f06c30fe4231dd",
    "Level/bp.VCA.maxpat": "aa62bb0c452f34fb7f326b7a9ca74db9f5c85f7dfde5898d13e1ba96255b74ed",
    "Random/bp.Noise.maxpat": "29f0644ed93cf63fbbfa24e5a7d61489d55bcff038885c6fbab72afc6e69de47",
    "Envelope/bp.AD.maxpat": "1b57cd17e4033d60c401d66991044e90e9cd97a950aa772d3a5a3adb74758d47",
    "Filter/bp.MMF.maxpat": "ad0be37d9cffafeef1f7b736527149fba1b63c36d45be82199b33bddf98d11b1",
    "LFO/bp.LFO.maxpat": "122d2f54c95d993eb7d9e2063dca384542ddb547d45e784d515d5237283ed28a",
    "Effects/bp.Chorus.maxpat": "63344b7dd9046a30a9a9f0ccd7632787b27de35c6f3dd12263f91c55a005df8b",
    "Effects/bp.Reverb 2.maxpat": "48556085749a3a3560108523902feb2af7bd3b4ce41ef78c5682f6fc73390479",
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
    "overrun",
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
    "air_detail",
    "cycle_irregularity",
    "stereo_width",
    "throttle_loudness_depth",
    "saturation",
    "torque_ripple_level",
    "gear_mesh_level",
    "electrical_detail",
    "combustion_pulse",
    "intake_detail",
    "exhaust_detail",
    "residual_detail",
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
    "soundscape_enable",
    "soundscape_level_db",
    "soundscape_motion",
    "soundscape_space",
    "soundscape_solo",
    "dna_solo",
    "backfire_enable",
    "backfire_intensity",
    "backfire_solo",
    "reference_texture_level_db",
    "reference_texture_mute",
    "eq_low",
    "eq_lowmid",
    "eq_highmid",
    "eq_high",
    "eq_bypass",
    "master_trim_db",
    "compressor_threshold_db",
    "compressor_ratio",
    "compressor_attack_rate",
    "compressor_release_rate",
    "compressor_makeup_db",
    "compressor_bypass",
)
ALL_MESSAGES = STATE_NAMES + MACRO_NAMES

PROFILE_MESSAGES = tuple(
    name
    for name in ALL_MESSAGES
    if name not in {"engine_type", "ev_weight", "v12_weight", "v10_weight"}
)

PROFILE_CONFIG = {
    "ev": {
        "title": "Future EV",
        "runtime": "VehicleSoundSynth-EV.maxpat",
        "engine": "vehicle_engine_ev~",
        "drive": "drive_simulator_ev",
        "idle_rpm": 650.0,
    },
    "v10": {
        "title": "Ferrari-referenced V10",
        "runtime": "VehicleSoundSynth-V10.maxpat",
        "engine": "vehicle_engine_v10~",
        "drive": "drive_simulator_v10",
        "idle_rpm": 740.0,
    },
    "v12": {
        "title": "Independent V12",
        "runtime": "VehicleSoundSynth-V12.maxpat",
        "engine": "vehicle_engine_v12~",
        "drive": "drive_simulator_v12",
        "idle_rpm": 780.0,
    },
}

DNA_PARAMETER_SPECS = {
    "ev": (
        ("aggression", "Aggression", 0.0, 1.0),
        ("brightness", "Brightness", 0.0, 1.0),
        ("body", "Body", 0.0, 1.0),
        ("texture", "Texture", 0.0, 1.0),
        ("air_detail", "Air Detail", 0.0, 1.0),
        ("cycle_irregularity", "Cycle Irregularity", 0.0, 1.0),
        ("stereo_width", "Stereo / Bank Separation", 0.0, 1.0),
        ("throttle_loudness_depth", "Throttle Loudness Depth dB", 0.0, 8.0),
        ("saturation", "Saturation", 0.0, 1.0),
        ("torque_ripple_level", "Torque Ripple", 0.0, 1.0),
        ("gear_mesh_level", "Gear Mesh", 0.0, 1.0),
        ("electrical_detail", "Electrical Detail", 0.0, 1.0),
    ),
    "v10": (
        ("aggression", "Aggression", 0.0, 1.0),
        ("brightness", "Brightness", 0.0, 1.0),
        ("body", "Body", 0.0, 1.0),
        ("texture", "Texture", 0.0, 1.0),
        ("air_detail", "Air Detail", 0.0, 1.0),
        ("cycle_irregularity", "Cycle Irregularity", 0.0, 1.0),
        ("stereo_width", "Stereo / Bank Separation", 0.0, 1.0),
        ("throttle_loudness_depth", "Throttle Loudness Depth dB", 0.0, 8.0),
        ("saturation", "Saturation", 0.0, 1.0),
        ("combustion_pulse", "Combustion Pulse", 0.0, 1.0),
        ("intake_detail", "Intake Detail", 0.0, 1.0),
        ("exhaust_detail", "Exhaust Detail", 0.0, 1.0),
        ("residual_detail", "Residual Detail", 0.0, 1.0),
    ),
    "v12": (
        ("aggression", "Aggression", 0.0, 1.0),
        ("brightness", "Brightness", 0.0, 1.0),
        ("body", "Body", 0.0, 1.0),
        ("texture", "Texture", 0.0, 1.0),
        ("air_detail", "Air Detail", 0.0, 1.0),
        ("cycle_irregularity", "Cycle Irregularity", 0.0, 1.0),
        ("stereo_width", "Stereo / Bank Separation", 0.0, 1.0),
        ("throttle_loudness_depth", "Throttle Loudness Depth dB", 0.0, 8.0),
        ("saturation", "Saturation", 0.0, 1.0),
        ("combustion_pulse", "Combustion Pulse", 0.0, 1.0),
        ("intake_detail", "Intake Detail", 0.0, 1.0),
        ("exhaust_detail", "Exhaust Detail", 0.0, 1.0),
        ("residual_detail", "Residual Detail", 0.0, 1.0),
    ),
}

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


def make_ev_mode_beap(mode: str) -> dict[str, Any]:
    """Seed an alternate user-owned BEAP soundscape without saw oscillators."""
    document = make_ev_pad_beap()
    patcher = document["patcher"]
    title = mode.capitalize()
    patcher["boxes"][0]["box"]["text"] = (
        f"USER-TUNABLE EV {title.upper()} — BEAP soundscape; this file is preserved on rebuild"
    )
    settings = {
        "expressive": {
            "Mixer": {"in1": -12, "in2": -22},
            "Ladder": {"Freq": 1700, "Res": 14},
            "ADSR": {"Attack": 180, "Decay": 850, "Sustain": 62, "Release": 1200},
        },
        "sport": {
            "Mixer": {"in1": -9, "in2": -20},
            "Ladder": {"Freq": 2200, "Res": 9},
            "ADSR": {"Attack": 70, "Decay": 420, "Sustain": 78, "Release": 650},
        },
    }[mode]
    for item in patcher["boxes"]:
        box = item["box"]
        varname = box.get("varname", "")
        for module, values in settings.items():
            if module in varname:
                for parameter, value in values.items():
                    _set_beap_initial(box, parameter, value)
    return document


def make_ice_pad_beap(profile: str) -> dict[str, Any]:
    """Seed a slow, user-owned cinematic ICE pad without saw oscillators."""
    document = make_ev_pad_beap()
    patcher = document["patcher"]
    patcher["boxes"][0]["box"]["text"] = (
        f"USER-TUNABLE {profile.upper()} CINEMATIC PAD — preserved on rebuild"
    )
    settings = {
        "v10": {
            "Mixer": {"in1": -14, "in2": -19},
            "Ladder": {"Freq": 980, "Res": 7},
            "ADSR": {"Attack": 720, "Decay": 1450, "Sustain": 76, "Release": 2400},
        },
        "v12": {
            "Mixer": {"in1": -16, "in2": -17},
            "Ladder": {"Freq": 1250, "Res": 6},
            "ADSR": {"Attack": 980, "Decay": 1800, "Sustain": 72, "Release": 3000},
        },
    }[profile]
    for item in patcher["boxes"]:
        box = item["box"]
        varname = box.get("varname", "")
        for module, values in settings.items():
            if module in varname:
                for parameter, value in values.items():
                    _set_beap_initial(box, parameter, value)
    return document


def make_ice_pad_voice(profile: str) -> dict[str, Any]:
    p = Patcher(620, 360)
    p.comment(f"{profile.upper()} cinematic pad poly voice", 20, 15, 420)
    pitch = p.new("in~ 1", 35, 65, 45, numinlets=0, numoutlets=1)
    gate = p.new("in~ 2", 125, 65, 45, numinlets=0, numoutlets=1)
    motion = p.new("in~ 3", 215, 65, 45, numinlets=0, numoutlets=1)
    beap = p.new(f"{profile}_pad_beap~", 120, 135, 150, numinlets=3, numoutlets=2)
    p.new("thispoly~", 390, 135, 70, numinlets=2, numoutlets=3)
    left = p.new("out~ 1", 90, 265, 50, numinlets=1, numoutlets=0)
    right = p.new("out~ 2", 260, 265, 50, numinlets=1, numoutlets=0)
    p.connect(pitch, beap, 0, 0)
    p.connect(gate, beap, 0, 1)
    p.connect(motion, beap, 0, 2)
    p.connect(beap, left, 0, 0)
    p.connect(beap, right, 1, 0)
    return p.document()


def make_ice_pad_host(profile: str) -> dict[str, Any]:
    """Map continuous vehicle state to a suspendable cinematic BEAP pad."""
    p = Patcher(980, 650)
    p.comment(f"{profile.upper()} PAD HOST — continuous RPM/throttle CV, independent level and mute", 25, 15, 800)
    control = inlet(p, 35, 65)
    names = ("rpm", "throttle", "ignition", "start", "pad_level_db", "pad_mute")
    router = route(p, names, 35, 105, 520)
    p.connect(control, router)

    rpm = p.new("clip 0. 10000.", 35, 155, 105, numinlets=3, numoutlets=1)
    pitch = p.new(
        "expr log(max(24.,36.7+0.014*$f1)/261.625565)/log(2.)",
        35, 195, 360, numinlets=1, numoutlets=1,
    )
    pitch_pack = p.new("pack 0. 90", 35, 235, 85, numinlets=2, numoutlets=1)
    pitch_line = p.new("line~", 35, 275, 50, numinlets=2, numoutlets=2)
    throttle = p.new("clip 0. 1.", 420, 155, 75, numinlets=3, numoutlets=1)
    motion = p.new(f"expr {1.0 if profile == 'v10' else 0.8:g}+2.4*$f1", 420, 195, 170, numinlets=1, numoutlets=1)
    motion_pack = p.new("pack 0. 140", 420, 235, 95, numinlets=2, numoutlets=1)
    motion_line = p.new("line~", 420, 275, 50, numinlets=2, numoutlets=2)
    ignition = p.new("clip 0 1", 620, 155, 65, numinlets=3, numoutlets=1)
    active_state = p.new("pak 0 0", 700, 155, 75, numinlets=2, numoutlets=1)
    pad_active = p.new("expr $i1 && !$i2", 785, 155, 120, numinlets=2, numoutlets=1)
    gate_cv = p.new("expr $f1*5.", 620, 195, 90, numinlets=1, numoutlets=1)
    gate_pack = p.new("pack 0. 80", 620, 235, 85, numinlets=2, numoutlets=1)
    gate_line = p.new("line~", 620, 275, 50, numinlets=2, numoutlets=2)
    p.connect(router, rpm, 0)
    p.connect(rpm, pitch)
    p.connect(pitch, pitch_pack)
    p.connect(pitch_pack, pitch_line)
    p.connect(router, throttle, 1)
    p.connect(throttle, motion)
    p.connect(motion, motion_pack)
    p.connect(motion_pack, motion_line)
    p.connect(router, ignition, 2)
    p.connect(ignition, active_state, 0, 0)
    p.connect(active_state, pad_active)
    p.connect(pad_active, gate_cv)
    p.connect(gate_cv, gate_pack)
    p.connect(gate_pack, gate_line)

    voice = p.new(f"poly~ {profile}_pad_voice 1", 245, 335, 175, numinlets=3, numoutlets=2)
    unmute = p.message("mute 1 0", 640, 335, 65)
    initial_suspend = p.new("loadmess mute 1 1", 715, 335, 125, numinlets=1, numoutlets=1)
    ignition_edges = p.new("sel 1 0", 620, 305, 55, numinlets=1, numoutlets=3)
    off_reschedule = p.new("t b b", 620, 375, 50, numinlets=1, numoutlets=2)
    cancel = p.message("stop", 680, 375, 40)
    suspend_delay = p.new("delay 3100", 730, 375, 80, numinlets=2, numoutlets=1)
    suspend = p.message("mute 1 1", 820, 375, 65)
    p.connect(pitch_line, voice, 0, 0)
    p.connect(gate_line, voice, 0, 1)
    p.connect(motion_line, voice, 0, 2)
    p.connect(pad_active, ignition_edges)
    p.connect(ignition_edges, cancel, 0)
    p.connect(cancel, suspend_delay)
    p.connect(ignition_edges, unmute, 0)
    p.connect(unmute, voice)
    p.connect(initial_suspend, voice)
    p.connect(ignition_edges, off_reschedule, 1)
    p.connect(off_reschedule, cancel, 1)
    p.connect(off_reschedule, suspend_delay, 0)
    p.connect(suspend_delay, suspend)
    p.connect(suspend, voice)

    level = add_db_gain_control(p, router, 4, 35, 405, -18.0 if profile == "v10" else -20.0)
    mute = p.new("clip 0 1", 35, 455, 65, numinlets=3, numoutlets=1)
    mute_gain = p.new("expr 1-$i1", 110, 455, 80, numinlets=1, numoutlets=1)
    mute_pack = p.new("pack 0. 40", 200, 455, 85, numinlets=2, numoutlets=1)
    mute_line = p.new("line~", 295, 455, 50, numinlets=2, numoutlets=2)
    mute_default = p.new("loadmess 0", 110, 490, 80, numinlets=1, numoutlets=1)
    p.connect(router, mute, 5)
    p.connect(mute_default, mute)
    p.connect(mute, mute_gain)
    p.connect(mute, active_state, 0, 1)
    p.connect(mute_gain, mute_pack)
    p.connect(mute_pack, mute_line)
    outputs = []
    for channel, x in ((0, 245), (1, 455)):
        level_gain = p.new("*~", x, 520, 40, numinlets=2, numoutlets=1)
        mute_stage = p.new("*~", x, 560, 40, numinlets=2, numoutlets=1)
        out = outlet(p, x, 610, signal=True)
        p.connect(voice, level_gain, channel, 0)
        p.connect(level, level_gain, 0, 1)
        p.connect(level_gain, mute_stage)
        p.connect(mute_line, mute_stage, 0, 1)
        p.connect(mute_stage, out)
        outputs.append(out)
    return p.document()


def make_sound_dna(profile: str) -> dict[str, Any]:
    """Seed one editable profile DNA panel around the generated DSP adapter."""
    p = Patcher(1280, 760)
    p.comment(
        f"{profile.upper()} USER-TUNABLE SOUND DNA — synthesis controls only; state/RPM remain drivetrain-owned",
        25, 15, 1050,
    )
    control = inlet(p, 35, 60)
    specs = DNA_PARAMETER_SPECS[profile]
    names = tuple(item[0] for item in specs)
    router = route(p, names, 35, 100, 1160)
    powertrain = p.new(f"{profile}_powertrain~", 475, 610, 150, numinlets=1, numoutlets=2)
    left = outlet(p, 475, 700, signal=True)
    right = outlet(p, 675, 700, signal=True)
    p.connect(control, router)
    # The unmatched outlet is the read-only vehicle state seam: rpm, throttle,
    # load, accel, lifecycle and level controls pass through unchanged.
    p.connect(router, powertrain, len(names), 0)

    p.new("autopattr @autorestore 0", 930, 15, 155, numinlets=1, numoutlets=4)
    open_request = p.new(
        f"r open.{profile}.sound_dna", 760, 15, 160, numinlets=0, numoutlets=1,
    )
    front = p.message("front", 760, 45, 45)
    patcher_window = p.new("thispatcher", 815, 45, 75, numinlets=1, numoutlets=2)
    p.connect(open_request, front)
    p.connect(front, patcher_window)
    storage = p.new(
        f"pattrstorage {profile}_sound_dna @savemode 3 @changemode 1 @autorestore 0",
        930, 50, 300, numinlets=1, numoutlets=4,
    )
    state_path = p.new(
        f"js Patcher:/code/dna_state_path.js {profile}",
        930, 85, 260, numinlets=1, numoutlets=1,
    )
    load = p.new("loadbang", 930, 120, 60, numinlets=1, numoutlets=1)
    restore_delay = p.new("delay 140", 1000, 120, 70, numinlets=2, numoutlets=1)
    restore_order = p.new("t b b", 1080, 120, 50, numinlets=1, numoutlets=2)
    restore = p.message("restore", 1140, 120, 55)
    recall_delay = p.new("delay 35", 1080, 155, 65, numinlets=2, numoutlets=1)
    recall = p.message("1", 1155, 155, 30)
    save = p.message("save", 930, 190, 45)
    close = p.new("closebang", 985, 190, 65, numinlets=0, numoutlets=1)
    p.connect(load, restore_delay)
    p.connect(restore_delay, restore_order)
    p.connect(restore_order, restore, 1)
    p.connect(restore, state_path)
    p.connect(state_path, storage)
    p.connect(restore_order, recall_delay, 0)
    p.connect(recall_delay, recall)
    p.connect(recall, storage)
    p.connect(close, save)
    p.connect(save, state_path)

    preset_name = {"ev": "Future EV", "v10": "Aggressive V10", "v12": "High-Rev V12"}[profile]
    defaults = PRESETS[preset_name]
    reset_button = p.add(
        "message", "Reset DNA", 1080, 210, 75, numinlets=2, numoutlets=1,
        presentation=1, presentation_rect=[1090.0, 690.0, 80.0, 22.0],
    )
    save_button = p.add(
        "message", "Save DNA", 930, 210, 70, numinlets=2, numoutlets=1,
        presentation=1, presentation_rect=[910.0, 690.0, 75.0, 22.0],
    )
    reload_button = p.add(
        "message", "Reload DNA", 1005, 210, 80, numinlets=2, numoutlets=1,
        presentation=1, presentation_rect=[995.0, 690.0, 85.0, 22.0],
    )
    p.connect(save_button, save)
    p.connect(reload_button, restore_order)

    for index, (name, label, low, high) in enumerate(specs):
        column = index % 4
        row = index // 4
        x = 35 + column * 300
        y = 165 + row * 125
        p.add(
            "comment", label, x, y, 220, 20, numinlets=1, numoutlets=0,
            presentation=1, presentation_rect=[x, y, 220.0, 20.0],
        )
        value = p.add(
            "flonum", None, x, y + 25, 90, numinlets=1, numoutlets=2,
            minimum=low, maximum=high, varname=f"dna_{name}",
            presentation=1, presentation_rect=[x, y + 25, 90.0, 22.0],
        )
        bounded = p.new(f"clip {low:g} {high:g}", x + 100, y + 25, 90, numinlets=3, numoutlets=1)
        named = p.new(f"prepend {name}", x + 195, y + 25, 100, numinlets=1, numoutlets=1)
        default_message = p.message(f"{defaults[name]:g}", x, y + 60, 65)
        p.connect(router, value, index)
        p.connect(value, bounded)
        p.connect(bounded, named)
        p.connect(named, powertrain)
        p.connect(load, default_message)
        p.connect(reset_button, default_message)
        p.connect(default_message, value)

    p.connect(powertrain, left, 0, 0)
    p.connect(powertrain, right, 1, 0)
    return p.document(presentation=True)


def make_cinematic_soundscape_beap() -> dict[str, Any]:
    """Seed the one shared, user-owned Prophet-inspired BEAP soundscape."""
    p = Patcher(2820, 980)
    p.comment(
        "USER-TUNABLE CINEMATIC SOUNDSCAPE — shared BEAP core for EV/V10/V12; preserved on rebuild",
        25, 15, 1050,
    )
    pitch_cv = inlet(p, 30, 65, signal=True)
    gate_cv = inlet(p, 120, 65, signal=True)
    tone_cv = inlet(p, 210, 65, signal=True)
    motion_cv = inlet(p, 300, 65, signal=True)
    space_cv = inlet(p, 390, 65, signal=True)
    for label, x in (
        ("Pitch CV", 20), ("Gate 0/5V", 110), ("Tone CV", 205),
        ("Motion 0..1", 295), ("Space 0..1", 390),
    ):
        p.comment(label, x, 95, 95)

    lfo = add_beap_module(
        p, "LFO/bp.LFO.maxpat", 510, 55, "LFO",
        initial={"Frequency": 0.14, "Mute": 0},
    )
    lfo_slow = add_beap_module(
        p, "LFO/bp.LFO.maxpat", 840, 55, "LFO_Slow",
        initial={"Frequency": 0.037, "Mute": 0},
    )
    lfo_scale = p.new("*~ 0.008", 510, 195, 72, numinlets=2, numoutlets=1)
    motion_depth = p.new("*~", 590, 195, 40, numinlets=2, numoutlets=1)
    opposite = p.new("*~ -1.", 640, 195, 58, numinlets=2, numoutlets=1)
    pitch_a = p.new("+~", 710, 165, 40, numinlets=2, numoutlets=1)
    pitch_b_mod = p.new("+~", 710, 215, 40, numinlets=2, numoutlets=1)
    pitch_b = p.new("+~ 0.012", 760, 215, 72, numinlets=2, numoutlets=1)
    slow_pitch = p.new("*~ 0.006", 840, 215, 72, numinlets=2, numoutlets=1)
    slow_motion = p.new("*~", 920, 215, 40, numinlets=2, numoutlets=1)
    pitch_c_base = p.new("+~ 1.5849625", 970, 215, 100, numinlets=2, numoutlets=1)
    pitch_c = p.new("+~", 1080, 215, 40, numinlets=2, numoutlets=1)
    tone_lfo = p.new("*~ 0.06", 510, 245, 68, numinlets=2, numoutlets=1)
    tone_motion = p.new("*~", 590, 245, 40, numinlets=2, numoutlets=1)
    tone_sum = p.new("+~", 640, 245, 40, numinlets=2, numoutlets=1)
    p.connect(lfo, lfo_scale, 0, 0)
    p.connect(lfo_scale, motion_depth, 0, 0)
    p.connect(motion_cv, motion_depth, 0, 1)
    p.connect(motion_depth, pitch_a, 0, 1)
    p.connect(pitch_cv, pitch_a, 0, 0)
    p.connect(motion_depth, opposite)
    p.connect(opposite, pitch_b_mod, 0, 1)
    p.connect(pitch_cv, pitch_b_mod, 0, 0)
    p.connect(pitch_b_mod, pitch_b)
    p.connect(lfo_slow, slow_pitch, 1, 0)
    p.connect(slow_pitch, slow_motion, 0, 0)
    p.connect(motion_cv, slow_motion, 0, 1)
    p.connect(pitch_cv, pitch_c_base)
    p.connect(pitch_c_base, pitch_c, 0, 0)
    p.connect(slow_motion, pitch_c, 0, 1)
    p.connect(lfo, tone_lfo, 1, 0)
    p.connect(tone_lfo, tone_motion, 0, 0)
    p.connect(motion_cv, tone_motion, 0, 1)
    p.connect(tone_motion, tone_sum, 0, 1)
    p.connect(tone_cv, tone_sum, 0, 0)

    osc_a = add_beap_module(
        p, "Oscillator/bp.Oscillator.maxpat", 25, 310, "Osc_A",
        initial={"Waveform": 1, "Offset": -5, "Mute": 0},
    )
    osc_b = add_beap_module(
        p, "Oscillator/bp.Oscillator.maxpat", 355, 310, "Osc_B",
        initial={"Waveform": 3, "Offset": -7, "PW": 43, "PWM": 18, "Mute": 0},
    )
    osc_c = add_beap_module(
        p, "Oscillator/bp.Oscillator.maxpat", 685, 310, "Osc_C",
        initial={"Waveform": 1, "Offset": -12, "Mute": 0},
    )
    noise = add_beap_module(p, "Random/bp.Noise.maxpat", 1015, 310, "Noise")
    noise_gain = p.new("*~ 0.026", 1060, 455, 75, numinlets=2, numoutlets=1)
    mixer = add_beap_module(
        p, "Mixers/bp.Audio Mixer.maxpat", 1190, 310, "Mixer",
        initial={"in1": -7, "in2": -15, "in3": -29, "in4": -19},
    )
    ladder = add_beap_module(
        p, "Filter/bp.Ladder.maxpat", 1435, 310, "Ladder",
        initial={"Freq": 1850, "Res": 7, "CV1": 72},
    )
    mmf = add_beap_module(
        p, "Filter/bp.MMF.maxpat", 1745, 310, "MMF",
        initial={"Freq": 2450, "Res": 9, "FilterType": 0},
    )
    envelope = add_beap_module(
        p, "Envelope/bp.ADSR.maxpat", 2020, 310, "ADSR",
        initial={"Attack": 520, "Decay": 1350, "Sustain": 76, "Release": 2600},
    )
    vca = add_beap_module(p, "Level/bp.VCA.maxpat", 2275, 310, "VCA")
    p.connect(pitch_a, osc_a, 0, 0)
    p.connect(pitch_b, osc_b, 0, 0)
    p.connect(pitch_c, osc_c, 0, 0)
    p.connect(lfo, osc_b, 2, 4)
    p.connect(lfo_slow, osc_c, 2, 4)
    p.connect(osc_a, mixer, 0, 0)
    p.connect(osc_b, mixer, 0, 1)
    p.connect(noise, noise_gain)
    p.connect(noise_gain, mixer, 0, 2)
    p.connect(osc_c, mixer, 0, 3)
    p.connect(mixer, ladder, 0, 0)
    p.connect(tone_sum, ladder, 0, 1)
    p.connect(ladder, mmf, 0, 0)
    p.connect(tone_sum, mmf, 0, 1)
    p.connect(gate_cv, envelope, 0, 0)
    p.connect(mmf, vca, 0, 0)
    p.connect(envelope, vca, 0, 1)

    chorus = add_beap_module(
        p, "Effects/bp.Chorus.maxpat", 25, 610, "Chorus",
        initial={"Center": 620, "Rate": 0.22, "Regen": 0.22, "Width": 28, "bypass": 0},
    )
    reverb = add_beap_module(
        p, "Effects/bp.Reverb 2.maxpat", 420, 610, "Reverb",
        initial={"Damping": 4200, "Decay": 46, "Diffusion": 0.68, "Mix": 100, "Size": 66, "bypass": 0},
    )
    p.connect(vca, chorus)
    p.connect(vca, reverb)
    space_depth = p.new("*~ 0.34", 790, 650, 72, numinlets=2, numoutlets=1)
    p.connect(space_cv, space_depth)
    for channel, x in ((0, 990), (1, 1390)):
        chorus_gain = p.new("*~ 0.72", x, 690, 72, numinlets=2, numoutlets=1)
        reverb_gain = p.new("*~", x + 85, 690, 40, numinlets=2, numoutlets=1)
        blend = p.new("+~", x + 45, 740, 40, numinlets=2, numoutlets=1)
        highpass = p.new("svf~ 120 0.7", x + 45, 785, 100, numinlets=3, numoutlets=4)
        safe = p.new("clip~ -0.8 0.8", x + 45, 825, 105, numinlets=3, numoutlets=1)
        output = outlet(p, x + 45, 875, signal=True)
        p.connect(chorus, chorus_gain, channel, 0)
        p.connect(reverb, reverb_gain, channel, 0)
        p.connect(space_depth, reverb_gain, 0, 1)
        p.connect(chorus_gain, blend, 0, 0)
        p.connect(reverb_gain, blend, 0, 1)
        p.connect(blend, highpass)
        p.connect(highpass, safe, 1, 0)
        p.connect(safe, output)
    return p.document()


def make_cinematic_soundscape_voice() -> dict[str, Any]:
    p = Patcher(760, 430)
    p.comment("Shared cinematic soundscape poly voice", 20, 15, 480)
    signals = [p.new(f"in~ {index}", 30 + (index - 1) * 95, 65, 48, numinlets=0, numoutlets=1) for index in range(1, 6)]
    beap = p.new("cinematic_soundscape_beap~", 175, 145, 205, numinlets=5, numoutlets=2)
    p.new("thispoly~", 500, 145, 70, numinlets=2, numoutlets=3)
    left = p.new("out~ 1", 150, 335, 50, numinlets=1, numoutlets=0)
    right = p.new("out~ 2", 350, 335, 50, numinlets=1, numoutlets=0)
    for index, signal in enumerate(signals):
        p.connect(signal, beap, 0, index)
    p.connect(beap, left, 0, 0)
    p.connect(beap, right, 1, 0)
    return p.document()


def make_cinematic_soundscape_host(profile: str) -> dict[str, Any]:
    """Map one vehicle profile into the shared soundscape macros."""
    p = Patcher(1420, 860)
    p.comment(f"{profile.upper()} CINEMATIC SOUNDSCAPE HOST — continuous vehicle-state mapping and DSP suspension", 25, 15, 980)
    control = inlet(p, 35, 65)
    names = (
        "rpm", "throttle", "load", "accel", "shift", "ignition", "start",
        "soundscape_enable", "soundscape_level_db", "soundscape_motion", "soundscape_space",
        "pad_level_db", "pad_mute", "ev_soundscape_level_db", "ev_soundscape_mute", "ev_mode",
    )
    router = route(p, names, 35, 105, 1250)
    p.connect(control, router)

    for outlet_index in (11, 13):
        alias = p.new("prepend soundscape_level_db", 1050, 150 + 30 * (outlet_index - 11), 190, numinlets=1, numoutlets=1)
        p.connect(router, alias, outlet_index)
        p.connect(alias, router)
    for outlet_index in (12, 14):
        invert = p.new("expr 1-$i1", 1050, 220 + 30 * (outlet_index - 12), 80, numinlets=1, numoutlets=1)
        alias = p.new("prepend soundscape_enable", 1140, 220 + 30 * (outlet_index - 12), 180, numinlets=1, numoutlets=1)
        p.connect(router, invert, outlet_index)
        p.connect(invert, alias)
        p.connect(alias, router)

    if profile == "ev":
        legacy_modes = p.new("sel relax expressive sport", 1050, 315, 210, numinlets=1, numoutlets=4)
        legacy_macros = (
            p.message("soundscape_motion 0.35, soundscape_space 0.55", 1010, 355, 320),
            p.message("soundscape_motion 0.62, soundscape_space 0.42", 1010, 390, 320),
            p.message("soundscape_motion 0.88, soundscape_space 0.24", 1010, 425, 320),
        )
        p.connect(router, legacy_modes, 15)
        for outlet_index, macro_message in enumerate(legacy_macros):
            p.connect(legacy_modes, macro_message, outlet_index)
            p.connect(macro_message, router)

    rpm = p.new("clip 0. 10000.", 35, 170, 105, numinlets=3, numoutlets=1)
    pitch_formula = {
        "ev": "expr log(max(24.,55.+0.032*$f1)/261.625565)/log(2.)",
        "v10": "expr log(max(24.,36.7+0.014*$f1)/261.625565)/log(2.)",
        "v12": "expr log(max(24.,32.7+0.012*$f1)/261.625565)/log(2.)",
    }[profile]
    pitch = p.new(pitch_formula, 35, 210, 390, numinlets=1, numoutlets=1)
    pitch_pack = p.new("pack 0. 90", 35, 250, 85, numinlets=2, numoutlets=1)
    pitch_line = p.new("line~", 35, 290, 50, numinlets=2, numoutlets=2)
    p.connect(router, rpm, 0)
    p.connect(rpm, pitch)
    p.connect(pitch, pitch_pack)
    p.connect(pitch_pack, pitch_line)

    state = p.new("pak 0. 0. 0.", 450, 170, 100, numinlets=3, numoutlets=1)
    base_tone = {"ev": 0.82, "v10": 0.48, "v12": 0.38}[profile]
    tone = p.new(
        f"expr min(3.5,max(0.,{base_tone:g}+1.9*$f1+0.55*max(0.,$f2)+0.25*abs($f3)))",
        450, 210, 500, numinlets=3, numoutlets=1,
    )
    tone_pack = p.new("pack 0. 150", 450, 250, 95, numinlets=2, numoutlets=1)
    tone_line = p.new("line~", 450, 290, 50, numinlets=2, numoutlets=2)
    p.connect(router, state, 1, 0)
    p.connect(router, state, 2, 1)
    p.connect(router, state, 3, 2)
    p.connect(state, tone)
    p.connect(tone, tone_pack)
    p.connect(tone_pack, tone_line)

    motion_state = p.new("pak 0. 0.55", 35, 345, 100, numinlets=2, numoutlets=1)
    motion_map = p.new("expr min(1.,max(0.,0.12+0.42*$f1+0.46*$f2))", 35, 385, 335, numinlets=2, numoutlets=1)
    motion_pack = p.new("pack 0. 180", 35, 425, 95, numinlets=2, numoutlets=1)
    motion_line = p.new("line~", 35, 465, 50, numinlets=2, numoutlets=2)
    motion_default_value = {"ev": 0.62, "v10": 0.52, "v12": 0.42}[profile]
    motion_default = p.new(f"loadmess {motion_default_value:g}", 145, 345, 95, numinlets=1, numoutlets=1)
    p.connect(router, motion_state, 1, 0)
    p.connect(router, motion_state, 9, 1)
    p.connect(motion_default, motion_state, 0, 1)
    p.connect(motion_state, motion_map)
    p.connect(motion_map, motion_pack)
    p.connect(motion_pack, motion_line)

    space_state = p.new("pak 0.45 0.", 420, 345, 100, numinlets=2, numoutlets=1)
    space_map = p.new("expr min(1.,max(0.,0.12+0.72*$f1+0.16*(1.-$f2)))", 420, 385, 355, numinlets=2, numoutlets=1)
    space_pack = p.new("pack 0. 220", 420, 425, 95, numinlets=2, numoutlets=1)
    space_line = p.new("line~", 420, 465, 50, numinlets=2, numoutlets=2)
    space_default_value = {"ev": 0.42, "v10": 0.38, "v12": 0.52}[profile]
    space_default = p.new(f"loadmess {space_default_value:g}", 530, 345, 95, numinlets=1, numoutlets=1)
    p.connect(router, space_state, 10, 0)
    p.connect(router, space_state, 1, 1)
    p.connect(space_default, space_state, 0, 0)
    p.connect(space_state, space_map)
    p.connect(space_map, space_pack)
    p.connect(space_pack, space_line)

    ignition = p.new("clip 0 1", 805, 345, 65, numinlets=3, numoutlets=1)
    enable = p.new("clip 0 1", 880, 345, 65, numinlets=3, numoutlets=1)
    active_state = p.new("pak 0 0", 955, 345, 75, numinlets=2, numoutlets=1)
    active = p.new("expr $i1*$i2", 1040, 345, 90, numinlets=2, numoutlets=1)
    enable_default = p.new("loadmess 0", 880, 380, 80, numinlets=1, numoutlets=1)
    gate_cv = p.new("expr 5.*$f1", 1040, 385, 90, numinlets=1, numoutlets=1)
    gate_pack = p.new("pack 0. 80", 1040, 425, 85, numinlets=2, numoutlets=1)
    gate_line = p.new("line~", 1040, 465, 50, numinlets=2, numoutlets=2)
    p.connect(router, ignition, 5)
    p.connect(router, enable, 7)
    p.connect(enable_default, enable)
    p.connect(ignition, active_state, 0, 0)
    p.connect(enable, active_state, 0, 1)
    p.connect(active_state, active)
    p.connect(active, gate_cv)
    p.connect(gate_cv, gate_pack)
    p.connect(gate_pack, gate_line)

    voice = p.new("poly~ cinematic_soundscape_voice 1", 370, 535, 230, numinlets=5, numoutlets=2)
    for source, inlet_index in ((pitch_line, 0), (gate_line, 1), (tone_line, 2), (motion_line, 3), (space_line, 4)):
        p.connect(source, voice, 0, inlet_index)
    edges = p.new("sel 1 0", 805, 505, 55, numinlets=1, numoutlets=3)
    cancel = p.message("stop", 870, 505, 40)
    unmute = p.message("mute 1 0", 920, 505, 65)
    off_order = p.new("t b b", 805, 545, 50, numinlets=1, numoutlets=2)
    suspend_delay = p.new("delay 3300", 870, 575, 80, numinlets=2, numoutlets=1)
    suspend = p.message("mute 1 1", 960, 575, 65)
    initial_suspend = p.new("loadmess mute 1 1", 1035, 575, 125, numinlets=1, numoutlets=1)
    p.connect(active, edges)
    p.connect(edges, cancel, 0)
    p.connect(cancel, suspend_delay)
    p.connect(edges, unmute, 0)
    p.connect(unmute, voice)
    p.connect(edges, off_order, 1)
    p.connect(off_order, cancel, 1)
    p.connect(off_order, suspend_delay, 0)
    p.connect(suspend_delay, suspend)
    p.connect(suspend, voice)
    p.connect(initial_suspend, voice)

    level = add_db_gain_control(p, router, 8, 35, 555, -14.0 if profile != "v12" else -15.0)
    shift_edge = p.new("sel 1", 680, 535, 45, numinlets=1, numoutlets=2)
    shift_shape = p.message("0.72 35, 1. 300 35", 680, 575, 145)
    shift_line = p.new("line~ 1.", 680, 615, 65, numinlets=2, numoutlets=2)
    start_edge = p.new("sel 1", 835, 640, 45, numinlets=1, numoutlets=2)
    start_shape = p.message("0.35, 1. 950", 835, 680, 105)
    start_line = p.new("line~ 1.", 835, 720, 65, numinlets=2, numoutlets=2)
    p.connect(router, shift_edge, 4)
    p.connect(shift_edge, shift_shape, 0)
    p.connect(shift_shape, shift_line)
    p.connect(router, start_edge, 6)
    p.connect(start_edge, start_shape, 0)
    p.connect(start_shape, start_line)

    for channel, x in ((0, 270), (1, 570)):
        level_gain = p.new("*~", x, 665, 40, numinlets=2, numoutlets=1)
        shift_gain = p.new("*~", x, 705, 40, numinlets=2, numoutlets=1)
        bloom_gain = p.new("*~", x, 745, 40, numinlets=2, numoutlets=1)
        safe = p.new("clip~ -0.65 0.65", x, 785, 120, numinlets=3, numoutlets=1)
        output = outlet(p, x, 825, signal=True)
        p.connect(voice, level_gain, channel, 0)
        p.connect(level, level_gain, 0, 1)
        p.connect(level_gain, shift_gain)
        p.connect(shift_line, shift_gain, 0, 1)
        p.connect(shift_gain, bloom_gain)
        p.connect(start_line, bloom_gain, 0, 1)
        p.connect(bloom_gain, safe)
        p.connect(safe, output)
    return p.document()


def make_ice_backfire_beap(profile: str) -> dict[str, Any]:
    """Seed one editable, layered pressure/crack backfire voice."""
    p = Patcher(2580, 980)
    p.comment(
        f"USER-TUNABLE {profile.upper()} PHYSICAL BACKFIRE — preserved on rebuild",
        25, 15, 980,
    )
    pitch = inlet(p, 45, 65, signal=True)
    gate = inlet(p, 145, 65, signal=True)
    intensity = inlet(p, 245, 65, signal=True)
    pressure_excitation = inlet(p, 345, 65, signal=True)
    open_request = p.new(
        f"r open.{profile}.backfire", 1680, 15, 175,
        numinlets=0, numoutlets=1,
    )
    front = p.message("front", 1865, 15, 45)
    patcher_window = p.new("thispatcher", 1920, 15, 75, numinlets=1, numoutlets=2)
    p.connect(open_request, front)
    p.connect(front, patcher_window)

    p.comment(
        "AUTHORITATIVE POP CONTROLS — tune these first; Pressure Mixer adds optional BEAP colour",
        1680, 65, 820,
    )
    p.comment(
        "Global Pitch applies to all layers. Core Presence: 0.25 = 25%, 1 = unity, 1.5 = 150%.",
        1680, 90, 760,
    )
    tuning_load = p.new("loadbang", 2450, 15, 60, numinlets=1, numoutlets=1)
    tuning_emit = p.new("delay 50", 2450, 45, 65, numinlets=2, numoutlets=1)
    p.connect(tuning_load, tuning_emit)
    tuning_specs = (
        ("Global Pitch (semitones)", "pop_global_pitch_semitones", 0.0, -18.0, 6.0),
        ("Core Presence", "pop_core_presence", 1.0, 0.25, 1.5),
        ("Body Tune", "pop_body_tune", 1.0, 0.5, 1.5),
        ("Crack Tune", "pop_crack_tune", 1.0, 0.5, 1.5),
        ("Decay Scale", "pop_decay_scale", 1.0, 0.5, 2.0),
        ("Low Pressure Level", "pop_low_pressure_level", 0.32, 0.0, 1.0),
        ("Core Body Level", "pop_body_level", 1.0, 0.0, 1.5),
        ("Core Crack Level", "pop_crack_level", 1.0, 0.0, 1.5),
    )
    tuning_sources = []
    for index, (label, varname, default, low, high) in enumerate(tuning_specs):
        column = index % 2
        row = index // 2
        x = 1680 + column * 390
        y = 130 + row * 90
        p.comment(label, x, y, 220)
        value = p.add(
            "flonum", None, x, y + 25, 95, numinlets=1, numoutlets=2,
            minimum=low, maximum=high, value=default, varname=varname,
            parameter_enable=1,
            saved_attribute_attributes={
                "valueof": {
                    "parameter_initial": [default],
                    "parameter_initial_enable": 1,
                    "parameter_longname": varname,
                    "parameter_shortname": label,
                    "parameter_mmin": low,
                    "parameter_mmax": high,
                    "parameter_type": 0,
                }
            },
        )
        bounded = p.new(
            f"clip {low:g} {high:g}", x + 105, y + 25, 95,
            numinlets=3, numoutlets=1,
        )
        p.connect(tuning_emit, value)
        p.connect(value, bounded)
        tuning_sources.append((bounded, varname.removeprefix("pop_")))
    tuning_by_name = {name: source for source, name in tuning_sources}

    p.comment("PRESSURE BODY — low exhaust pressure and chamber bloom", 25, 110, 620)
    p.comment(
        "Pressure Mixer is audible; native MMF/AD/VCA can be subtle on short Max 8.6.5 gates",
        625, 110, 720,
    )
    noise = add_beap_module(p, "Random/bp.Noise.maxpat", 25, 145, "Pressure_Noise")
    osc = add_beap_module(
        p, "Oscillator/bp.Oscillator.maxpat", 300, 145, "Pressure_Osc",
        initial={"Waveform": 0},
    )
    mixer = add_beap_module(
        p, "Mixers/bp.Audio Mixer.maxpat", 625, 145, "Pressure_Mixer",
        initial={
            "in1": -6 if profile == "v10" else -7,
            "in2": -20 if profile == "v10" else -18,
        },
    )
    body_filter = add_beap_module(
        p, "Filter/bp.MMF.maxpat", 845, 145, "Pressure_Body",
        initial={
            "Freq": 390 if profile == "v10" else 285,
            "Res": 10 if profile == "v10" else 8,
            "FilterType": 0,
            "power[1]": 1,
        },
    )
    body_envelope = add_beap_module(
        p, "Envelope/bp.AD.maxpat", 1120, 145, "Pressure_AD",
        initial={
            "Attack": 2 if profile == "v10" else 5,
            "Decay": 220 if profile == "v10" else 310,
        },
    )
    body_vca = add_beap_module(p, "Level/bp.VCA.maxpat", 1320, 145, "Pressure_VCA")
    body_env_amount = p.new("*~ 0.90", 1135, 360, 65, numinlets=2, numoutlets=1)
    # The installed Max 8.6.x BEAP AD/VCA pair can miss a short external edge.
    # This parallel envelope still uses the editable BEAP mixer/filter output,
    # so the visible BEAP tone controls remain authoritative while triggers are
    # deterministic on every supported installation.
    body_gate_trim = p.new(
        f"*~ {0.75 if profile == 'v10' else 0.85:g}",
        1210, 400, 65, numinlets=2, numoutlets=1,
    )
    body_compat_filter = p.new(
        f"lores~ {420 if profile == 'v10' else 310} {0.68 if profile == 'v10' else 0.72:g}",
        985, 400, 110, numinlets=3, numoutlets=1,
    )
    body_mode_a = p.new(
        f"reson~ {5.6 if profile == 'v10' else 6.2:g} {92 if profile == 'v10' else 72} {2.5 if profile == 'v10' else 3.0:g}",
        985, 435, 130, numinlets=4, numoutlets=1,
    )
    body_mode_b = p.new(
        f"reson~ {2.6 if profile == 'v10' else 3.1:g} {220 if profile == 'v10' else 160} {1.6 if profile == 'v10' else 1.9:g}",
        1125, 435, 130, numinlets=4, numoutlets=1,
    )
    body_modes = p.new("+~", 1265, 435, 40, numinlets=2, numoutlets=1)
    body_colour = p.new("+~", 1205, 400, 40, numinlets=2, numoutlets=1)
    body_pressure_vca = p.new("*~", 1290, 400, 40, numinlets=2, numoutlets=1)
    body_sum = p.new("+~", 1340, 390, 40, numinlets=2, numoutlets=1)

    p.comment("EXHAUST CRACK — intensity-brightened broadband shell", 25, 460, 620)
    crack_filter = add_beap_module(
        p, "Filter/bp.MMF.maxpat", 300, 495, "Exhaust_Crack",
        initial={
            "Freq": 1350 if profile == "v10" else 900,
            "Res": 6 if profile == "v10" else 4,
            "FilterType": 0,
            "power[1]": 1,
        },
    )
    crack_envelope = add_beap_module(
        p, "Envelope/bp.AD.maxpat", 575, 495, "Crack_AD",
        initial={
            "Attack": 1 if profile == "v10" else 3,
            "Decay": 58 if profile == "v10" else 92,
        },
    )
    crack_vca = add_beap_module(p, "Level/bp.VCA.maxpat", 775, 495, "Crack_VCA")
    crack_env_amount = p.new("*~ 0.58", 595, 710, 65, numinlets=2, numoutlets=1)
    crack_gate_trim = p.new(
        f"*~ {0.24 if profile == 'v10' else 0.20:g}",
        675, 750, 72, numinlets=2, numoutlets=1,
    )
    crack_compat_filter = p.new(
        f"svf~ {1350 if profile == 'v10' else 900} {0.66 if profile == 'v10' else 0.62:g}",
        545, 750, 115, numinlets=3, numoutlets=4,
    )
    crack_pressure_vca = p.new("*~", 755, 750, 40, numinlets=2, numoutlets=1)
    crack_sum = p.new("+~", 815, 730, 40, numinlets=2, numoutlets=1)

    p.comment("TAIL COLOR / OUTPUT — soft saturation; deep bass remains centered", 1020, 460, 700)
    layer_sum = p.new("+~", 1070, 540, 40, numinlets=2, numoutlets=1)
    drive = p.new("*~ 1.55", 1120, 540, 65, numinlets=2, numoutlets=1)
    soft_clip = p.new("tanh~", 1195, 540, 50, numinlets=1, numoutlets=1)
    split = p.new("svf~ 180 0.7", 1260, 540, 100, numinlets=3, numoutlets=4)
    left_air = p.new(
        f"lores~ {2800 if profile == 'v10' else 2100} 0.58",
        1380, 535, 120, numinlets=3, numoutlets=1,
    )
    right_air = p.new(
        f"lores~ {3200 if profile == 'v10' else 2400} 0.54",
        1380, 585, 120, numinlets=3, numoutlets=1,
    )
    left_mix = p.new("+~", 1520, 535, 40, numinlets=2, numoutlets=1)
    right_mix = p.new("+~", 1520, 585, 40, numinlets=2, numoutlets=1)
    left = outlet(p, 1600, 535, signal=True)
    right = outlet(p, 1600, 585, signal=True)
    # Global Pitch is a whole-voice tuning control, not merely an oscillator
    # offset. Apply it (and the relevant Body/Crack Tune multiplier) to every
    # fixed tonal filter in the editable compatibility/tail path.
    global_pitch_ratio = p.new(
        "expr pow(2.,$f1/12.)", 1680, 620, 145,
        numinlets=1, numoutlets=1,
    )
    p.connect(tuning_by_name["global_pitch_semitones"], global_pitch_ratio)

    def tuned_frequency(base: float, tune_name: str, x: float, y: float) -> str:
        frequency = p.new(
            f"expr {base:g}.*$f1*$f2", x, y, 155,
            numinlets=2, numoutlets=1,
        )
        p.connect(global_pitch_ratio, frequency, 0, 0)
        p.connect(tuning_by_name[tune_name], frequency, 0, 1)
        return frequency

    body_compat_frequency = tuned_frequency(
        420 if profile == "v10" else 310, "body_tune", 1680, 650,
    )
    body_mode_a_frequency = tuned_frequency(
        92 if profile == "v10" else 72, "body_tune", 1840, 650,
    )
    body_mode_b_frequency = tuned_frequency(
        220 if profile == "v10" else 160, "body_tune", 2000, 650,
    )
    crack_compat_frequency = tuned_frequency(
        1350 if profile == "v10" else 900, "crack_tune", 1680, 680,
    )
    left_air_frequency = tuned_frequency(
        2800 if profile == "v10" else 2100, "crack_tune", 1840, 680,
    )
    right_air_frequency = tuned_frequency(
        3200 if profile == "v10" else 2400, "crack_tune", 2000, 680,
    )
    # Keep the editable abstraction's public signal seam to stereo audio only.
    # Named profile-local buses carry saved tuning to the audible host without
    # relying on abstraction outlet ordering or load-time signal/message casts.
    for index, (source, control_name) in enumerate(tuning_sources):
        control_send = p.new(
            f"s {profile}.pop.{control_name}", 1680 + index * 105, 900, 120,
            numinlets=1, numoutlets=0,
        )
        p.connect(source, control_send)

    p.connect(noise, mixer, 0, 0)
    p.connect(pressure_excitation, mixer, 0, 0)
    p.connect(pitch, osc, 0, 0)
    p.connect(osc, mixer, 0, 1)
    p.connect(mixer, body_filter, 0, 0)
    body_filter_motion = p.new("*~ 0.18", 845, 360, 65, numinlets=2, numoutlets=1)
    body_filter_pitch = p.new("+~", 920, 360, 40, numinlets=2, numoutlets=1)
    p.connect(intensity, body_filter_motion)
    p.connect(pitch, body_filter_pitch, 0, 0)
    p.connect(body_filter_motion, body_filter_pitch, 0, 1)
    p.connect(body_filter_pitch, body_filter, 0, 1)
    p.connect(gate, body_envelope, 0, 0)
    p.connect(body_envelope, body_env_amount)
    p.connect(intensity, body_env_amount, 0, 1)
    p.connect(body_filter, body_vca, 0, 0)
    p.connect(body_env_amount, body_vca, 0, 1)
    p.connect(gate, body_gate_trim)
    # Max 8.6.5's native BEAP MMF/AD branch can remain silent on short external
    # gates. Feed the reliable compatibility colour path from the visible BEAP
    # Audio Mixer, so its input balance remains audibly authoritative while the
    # explicit Host Core Body/Crack controls own filter tuning and decay.
    p.connect(mixer, body_compat_filter, 0, 0)
    p.connect(mixer, body_mode_a, 0, 0)
    p.connect(mixer, body_mode_b, 0, 0)
    p.connect(body_compat_frequency, body_compat_filter, 0, 1)
    p.connect(body_mode_a_frequency, body_mode_a, 0, 1)
    p.connect(body_mode_b_frequency, body_mode_b, 0, 1)
    p.connect(body_mode_a, body_modes, 0, 0)
    p.connect(body_mode_b, body_modes, 0, 1)
    p.connect(body_compat_filter, body_colour, 0, 0)
    p.connect(body_modes, body_colour, 0, 1)
    p.connect(body_colour, body_pressure_vca, 0, 0)
    p.connect(body_gate_trim, body_pressure_vca, 0, 1)
    p.connect(body_vca, body_sum, 0, 0)
    p.connect(body_pressure_vca, body_sum, 0, 1)

    p.connect(noise, crack_filter, 0, 0)
    p.connect(pressure_excitation, crack_filter, 0, 0)
    p.connect(pitch, crack_filter, 0, 1)
    p.connect(gate, crack_envelope, 0, 0)
    p.connect(crack_envelope, crack_env_amount)
    p.connect(intensity, crack_env_amount, 0, 1)
    p.connect(crack_filter, crack_vca, 0, 0)
    p.connect(crack_env_amount, crack_vca, 0, 1)
    p.connect(gate, crack_gate_trim)
    p.connect(mixer, crack_compat_filter, 0, 0)
    p.connect(crack_compat_frequency, crack_compat_filter, 0, 1)
    p.connect(crack_compat_filter, crack_pressure_vca, 2, 0)
    p.connect(crack_gate_trim, crack_pressure_vca, 0, 1)
    p.connect(crack_vca, crack_sum, 0, 0)
    p.connect(crack_pressure_vca, crack_sum, 0, 1)

    p.connect(body_sum, layer_sum, 0, 0)
    p.connect(crack_sum, layer_sum, 0, 1)
    p.connect(layer_sum, drive)
    p.connect(drive, soft_clip)
    p.connect(soft_clip, split)
    p.connect(split, left_mix, 0, 0)
    p.connect(split, right_mix, 0, 0)
    p.connect(split, left_air, 1, 0)
    p.connect(split, right_air, 1, 0)
    p.connect(left_air_frequency, left_air, 0, 1)
    p.connect(right_air_frequency, right_air, 0, 1)
    p.connect(left_air, left_mix, 0, 1)
    p.connect(right_air, right_mix, 0, 1)
    p.connect(left_mix, left)
    p.connect(right_mix, right)
    return p.document()


def make_backfire_burst_scheduler() -> dict[str, Any]:
    """Wrap the ES5 burst planner behind one small Max message seam."""
    p = Patcher(620, 260)
    p.comment(
        "OVERRUN / TEST POP BURST — input: burst strength | stop | seed n",
        25, 20, 560,
    )
    p.comment(
        "output: pitch_semitones gain index count; 1..5 hits, 140..200 ms",
        25, 50, 560,
    )
    control = inlet(p, 40, 105)
    scheduler = p.new(
        "js ../code/backfire_burst.js", 145, 105, 190,
        numinlets=1, numoutlets=1,
    )
    output = outlet(p, 405, 105)
    p.connect(control, scheduler)
    p.connect(scheduler, output)
    return p.document()


def make_ice_backfire_host(profile: str) -> dict[str, Any]:
    """Trigger backfire from real overrun/shift state and explicit events."""
    p = Patcher(1080, 700)
    p.comment(f"{profile.upper()} BACKFIRE HOST — overrun/shift pressure release; no sample playback", 25, 15, 820)
    control = inlet(p, 35, 65)
    names = (
        "rpm", "throttle", "accel", "shift", "shift_dir", "intake_backfire",
        "exhaust_pop", "pop", "ignition", "engine_running", "backfire_enable",
        "backfire_intensity", "transient_level_db", "overrun", "backfire_test",
        "backfire_seed",
    )
    router = route(p, names, 35, 105, 960)
    p.connect(control, router)
    rpm = p.new("clip 0. 10000.", 35, 160, 105, numinlets=3, numoutlets=1)
    rpm_store = p.new("f 1800.", 150, 160, 65, numinlets=2, numoutlets=1)
    pitch_map = p.new("expr log(max(35.,48.+0.018*$f1)/261.625565)/log(2.)", 35, 205, 370, numinlets=1, numoutlets=1)
    pitch_sum = p.new("+ 0.", 35, 245, 55, numinlets=2, numoutlets=1)
    pitch_offset = p.new(
        "expr ($f1+$f2)/12.", 100, 245, 145,
        numinlets=2, numoutlets=1,
    )
    pitch_pack = p.new("pack 0. 4", 100, 245, 80, numinlets=2, numoutlets=1)
    pitch_line = p.new("line~", 35, 285, 50, numinlets=2, numoutlets=2)
    p.connect(router, rpm, 0)
    p.connect(rpm, rpm_store, 0, 1)
    p.connect(rpm_store, pitch_map)
    p.connect(pitch_map, pitch_sum, 0, 0)
    p.connect(pitch_offset, pitch_sum, 0, 1)
    p.connect(pitch_sum, pitch_pack)
    p.connect(pitch_pack, pitch_line)

    throttle = p.new("clip 0. 1.", 430, 160, 75, numinlets=3, numoutlets=1)
    p.connect(router, throttle, 1)

    enable = p.new("clip 0 1", 780, 160, 65, numinlets=3, numoutlets=1)
    enable_default = p.new("loadmess 1", 855, 160, 80, numinlets=1, numoutlets=1)
    ignition = p.new("clip 0 1", 780, 200, 65, numinlets=3, numoutlets=1)
    running = p.new("clip 0 1", 855, 200, 65, numinlets=3, numoutlets=1)
    physical_state = p.new("pak 1 0 0", 930, 200, 85, numinlets=3, numoutlets=1)
    physical_gate = p.new(
        "expr ($i1 != 0) && ($i2 != 0) && ($i3 != 0)",
        930,
        240,
        265,
        numinlets=3,
        numoutlets=1,
    )
    single_event_gate = p.new("gate 1", 780, 245, 55, numinlets=2, numoutlets=1)
    burst_event_gate = p.new("gate 1", 845, 245, 55, numinlets=2, numoutlets=1)
    p.connect(router, enable, 10)
    p.connect(router, ignition, 8)
    p.connect(router, running, 9)
    p.connect(enable_default, enable)
    p.connect(enable, physical_state, 0, 0)
    p.connect(ignition, physical_state, 0, 1)
    p.connect(running, physical_state, 0, 2)
    p.connect(physical_state, physical_gate)
    p.connect(physical_gate, single_event_gate, 0, 0)
    p.connect(physical_gate, burst_event_gate, 0, 0)
    p.comment("AUDITION ONLY — bypasses running-state gate; automatic events stay physical", 780, 275, 480)
    backfire_test_edge = p.new(
        "sel 1", 1000, 305, 45, numinlets=1, numoutlets=2,
        varname="backfire_test_edge",
    )
    scheduler = p.new(
        "backfire_burst_scheduler", 930, 345, 170,
        numinlets=1, numoutlets=1,
        varname="overrun_test_burst_scheduler",
    )
    test_burst = p.message("burst 1.", 1000, 335, 70)
    p.connect(router, backfire_test_edge, 14)
    p.connect(backfire_test_edge, test_burst, 0)
    p.connect(test_burst, scheduler)
    p.connect(burst_event_gate, scheduler)
    diagnostic_seed = p.new("prepend seed", 1000, 365, 85, numinlets=1, numoutlets=1)
    p.connect(router, diagnostic_seed, 15)
    p.connect(diagnostic_seed, scheduler)

    event_strength = p.new("f 1.", 650, 285, 55, numinlets=2, numoutlets=1)
    event_strength_default = p.new("loadmess 1.", 710, 285, 85, numinlets=1, numoutlets=1)
    p.connect(event_strength_default, event_strength)

    p.comment("SHIFT / EXPLICIT EVENTS — one hit", 430, 315, 285)
    single_event_trigger = p.new(
        "t b b", 710, 315, 50, numinlets=1, numoutlets=2,
        varname="backfire_single_event_trigger",
    )
    single_pitch = p.message("0.", 710, 345, 30)
    single_hit = p.new("pack 0. 1. 0 1", 745, 345, 105, numinlets=4, numoutlets=1)
    p.connect(single_event_gate, single_event_trigger)
    p.connect(single_event_trigger, event_strength, 1, 0)
    p.connect(event_strength, single_hit, 0, 1)
    p.connect(single_event_trigger, single_pitch, 0, 0)
    p.connect(single_pitch, single_hit, 0, 0)

    p.comment("OVERRUN / TEST POP — 1..5 hit burst", 840, 315, 280)
    hit_order = p.new("t b l", 870, 385, 50, numinlets=1, numoutlets=2)
    hit_values = p.new("unpack 0. 0. 0 0", 930, 385, 125, numinlets=1, numoutlets=4)
    pitch_ratio = p.new(
        "expr pow(2.,($f1+$f2)/12.)", 930, 450, 175,
        numinlets=2, numoutlets=1,
    )
    event_trigger = p.new(
        "t b", 870, 420, 40, numinlets=1, numoutlets=1,
        varname="backfire_event_trigger",
    )
    hit_fire_order = p.new("t b b", 820, 420, 50, numinlets=1, numoutlets=2)
    p.connect(single_hit, hit_order)
    p.connect(scheduler, hit_order)
    p.connect(hit_order, hit_values, 1, 0)
    p.connect(hit_values, pitch_offset, 0, 0)
    p.connect(hit_values, pitch_ratio, 0, 0)
    p.connect(hit_values, event_strength, 1, 1)
    p.connect(hit_order, hit_fire_order, 0, 0)
    p.connect(hit_fire_order, event_strength, 1, 0)
    p.connect(hit_fire_order, event_trigger, 0, 0)

    def fixed_event(index: int, strength: float, x: float) -> None:
        edge = p.new("sel 1", x, 205, 45, numinlets=1, numoutlets=2)
        order = p.new("t b b", x, 245, 50, numinlets=1, numoutlets=2)
        strength_message = p.message(f"{strength:g}", x + 55, 245, 35)
        p.connect(router, edge, index)
        p.connect(edge, order)
        p.connect(order, strength_message, 1)
        p.connect(strength_message, event_strength)
        p.connect(order, single_event_gate, 0, 1)

    fixed_event(3, 0.75, 430)
    fixed_event(5, 1.0, 520)
    fixed_event(6, 1.0, 610)
    fixed_event(7, 1.0, 700)

    overrun_clip = p.new("clip 0. 1.", 430, 285, 75, numinlets=3, numoutlets=1)
    overrun_nonzero = p.new("sel 0.", 515, 285, 50, numinlets=1, numoutlets=2)
    overrun_burst = p.new("prepend burst", 575, 285, 95, numinlets=1, numoutlets=1)
    p.connect(router, overrun_clip, 13)
    p.connect(overrun_clip, overrun_nonzero)
    p.connect(overrun_nonzero, overrun_burst, 1, 0)
    p.connect(overrun_burst, burst_event_gate, 0, 1)

    intensity_default_value = 0.82 if profile == "v10" else 0.55
    intensity = p.new("clip 0. 1.", 35, 345, 75, numinlets=3, numoutlets=1)
    intensity_default = p.new(f"loadmess {intensity_default_value:g}", 120, 345, 105, numinlets=1, numoutlets=1)
    intensity_state = p.new("pak 0.7 0. 1.", 235, 345, 110, numinlets=3, numoutlets=1)
    intensity_map = p.new(
        "expr (0.8+3.2*$f1+0.6*(1.-$f2))*(0.55+0.45*$f3)",
        355, 345, 355, numinlets=3, numoutlets=1,
    )
    intensity_pack = p.new("pack 0. 25", 600, 345, 85, numinlets=2, numoutlets=1)
    intensity_line = p.new("line~", 695, 345, 50, numinlets=2, numoutlets=2)
    p.connect(router, intensity, 11)
    p.connect(intensity_default, intensity)
    p.connect(intensity, intensity_state, 0, 0)
    p.connect(throttle, intensity_state, 0, 1)
    p.connect(event_strength, intensity_state, 0, 2)
    p.connect(intensity_state, intensity_map)
    p.connect(intensity_map, intensity_pack)
    p.connect(intensity_pack, intensity_line)

    gate_message = p.message(
        f"5. 0, 0. {185 if profile == 'v10' else 250}",
        805, 285, 115,
    )
    gate_line = p.new("line~", 805, 345, 50, numinlets=2, numoutlets=2)
    p.connect(event_trigger, rpm_store)
    p.connect(event_trigger, gate_message)
    p.connect(gate_message, gate_line)
    beap = p.new(
        f"{profile}_backfire_beap~", 330, 445, 190,
        numinlets=4, numoutlets=2,
    )
    p.connect(pitch_line, beap, 0, 0)
    p.connect(gate_line, beap, 0, 1)
    p.connect(intensity_line, beap, 0, 2)
    global_pitch = p.new("clip -18. 6.", 35, 385, 90, numinlets=3, numoutlets=1)
    core_presence = p.new("clip 0.25 1.5", 130, 385, 95, numinlets=3, numoutlets=1)
    body_tune = p.new("clip 0.5 1.5", 210, 385, 90, numinlets=3, numoutlets=1)
    crack_tune = p.new("clip 0.5 1.5", 305, 385, 90, numinlets=3, numoutlets=1)
    decay_scale = p.new("clip 0.5 2.", 400, 385, 90, numinlets=3, numoutlets=1)
    low_pressure_level = p.new("clip 0. 1.", 495, 385, 80, numinlets=3, numoutlets=1)
    body_level = p.new("clip 0. 1.5", 580, 385, 85, numinlets=3, numoutlets=1)
    crack_level = p.new("clip 0. 1.5", 670, 385, 85, numinlets=3, numoutlets=1)
    # Parent-side defaults make the host audible immediately. The editable
    # child emits its saved values after 50 ms and therefore remains
    # authoritative; these values only cover Max's abstraction-load window (or
    # a damaged user patch whose message outlets no longer emit).
    for index, (destination, default) in enumerate(
        (
            (global_pitch, "0."), (core_presence, "1."),
            (body_tune, "1."), (crack_tune, "1."),
            (decay_scale, "1."), (low_pressure_level, "0.32"),
            (body_level, "1."), (crack_level, "1."),
        )
    ):
        host_default = p.new(
            f"loadmess {default}", 35 + index * 92, 420, 85,
            numinlets=1, numoutlets=1,
        )
        p.connect(host_default, destination)
    for index, (destination, control_name) in enumerate(
        (
            (global_pitch, "global_pitch_semitones"),
            (core_presence, "core_presence"),
            (body_tune, "body_tune"), (crack_tune, "crack_tune"),
            (decay_scale, "decay_scale"),
            (low_pressure_level, "low_pressure_level"),
            (body_level, "body_level"), (crack_level, "crack_level"),
        )
    ):
        control_receive = p.new(
            f"r {profile}.pop.{control_name}", 35 + index * 92, 450, 120,
            numinlets=0, numoutlets=1,
        )
        p.connect(control_receive, destination)
    p.connect(global_pitch, pitch_offset, 0, 1)
    p.connect(global_pitch, pitch_ratio, 0, 1)
    # BEAP AD/VCA revisions in some Max 8.6.x installs can miss very short
    # external gates. A click-derived control envelope is sample-accurate and
    # excites broadband pressure instead of exposing a naked resonant impulse.
    # The editable BEAP voice remains the colour layer; this generated core owns
    # event audibility, body duration and the two exhaust-wall reflections.
    p.comment("GENERATED PRESSURE CORE — body / crack / two wall reflections", 25, 410, 620)
    pressure_noise = p.new("noise~", 35, 445, 55, numinlets=1, numoutlets=1)
    p.connect(pressure_noise, beap, 0, 3)
    main_click = p.new("click~", 100, 445, 50, numinlets=1, numoutlets=1)
    body_impulse = p.new(
        f"*~ {1120 if profile == 'v10' else 1320}", 160, 445, 75,
        numinlets=2, numoutlets=1,
    )
    body_decay = p.new(
        f"onepole~ {2.4 if profile == 'v10' else 1.9:g}", 245, 445, 90,
        numinlets=2, numoutlets=1,
    )
    body_env = p.new("clip~ 0. 1.", 345, 445, 85, numinlets=3, numoutlets=1)
    crack_impulse = p.new(
        f"*~ {115 if profile == 'v10' else 92}", 160, 480, 65,
        numinlets=2, numoutlets=1,
    )
    crack_decay = p.new(
        f"onepole~ {24 if profile == 'v10' else 18}", 235, 480, 90,
        numinlets=2, numoutlets=1,
    )
    body_decay_map = p.new(
        f"expr {2.4 if profile == 'v10' else 1.9:g}/max(0.5,$f1)",
        245, 520, 185, numinlets=1, numoutlets=1,
    )
    crack_decay_map = p.new(
        f"expr {24 if profile == 'v10' else 18:g}/max(0.5,$f1)",
        245, 550, 185, numinlets=1, numoutlets=1,
    )
    p.connect(decay_scale, body_decay_map)
    p.connect(decay_scale, crack_decay_map)
    p.connect(body_decay_map, body_decay, 0, 1)
    p.connect(crack_decay_map, crack_decay, 0, 1)
    crack_env = p.new("clip~ 0. 1.", 335, 480, 85, numinlets=3, numoutlets=1)
    body_burst = p.new("*~", 440, 445, 40, numinlets=2, numoutlets=1)
    crack_burst = p.new("*~", 440, 480, 40, numinlets=2, numoutlets=1)
    pressure_l = p.new(
        f"lores~ {560 if profile == 'v10' else 420} {0.68 if profile == 'v10' else 0.72:g}",
        490, 435, 115, numinlets=3, numoutlets=1,
    )
    pressure_r = p.new(
        f"lores~ {680 if profile == 'v10' else 500} {0.64 if profile == 'v10' else 0.69:g}",
        490, 465, 115, numinlets=3, numoutlets=1,
    )
    crack_l_filter = p.new(
        f"svf~ {1450 if profile == 'v10' else 1050} {0.58 if profile == 'v10' else 0.60:g}", 615, 435, 110,
        numinlets=3, numoutlets=4,
    )
    crack_r_filter = p.new(
        f"svf~ {1800 if profile == 'v10' else 1350} {0.55 if profile == 'v10' else 0.57:g}", 615, 475, 110,
        numinlets=3, numoutlets=4,
    )
    pressure_l_frequency = p.new(
        f"expr {560 if profile == 'v10' else 420}.*$f1*$f2", 490, 400, 150,
        numinlets=2, numoutlets=1,
    )
    pressure_r_frequency = p.new(
        f"expr {680 if profile == 'v10' else 500}.*$f1*$f2", 645, 400, 150,
        numinlets=2, numoutlets=1,
    )
    crack_l_frequency = p.new(
        f"expr {1450 if profile == 'v10' else 1050}.*$f1*$f2", 800, 400, 160,
        numinlets=2, numoutlets=1,
    )
    crack_r_frequency = p.new(
        f"expr {1800 if profile == 'v10' else 1350}.*$f1*$f2", 965, 400, 160,
        numinlets=2, numoutlets=1,
    )
    p.comment("LOW PRESSURE MODES — coherent below 120 Hz", 490, 505, 360)
    low_mode_a = p.new(
        f"reson~ {5.0 if profile == 'v10' else 5.8:g} {86 if profile == 'v10' else 70} {2.4 if profile == 'v10' else 2.8:g}",
        615, 505, 130, numinlets=4, numoutlets=1,
    )
    low_mode_b = p.new(
        f"reson~ {2.3 if profile == 'v10' else 2.7:g} {230 if profile == 'v10' else 170} {1.5 if profile == 'v10' else 1.8:g}",
        750, 505, 130, numinlets=4, numoutlets=1,
    )
    low_mode_a_frequency = p.new(
        f"expr {86 if profile == 'v10' else 70}.*$f1*$f2",
        615, 535, 145, numinlets=2, numoutlets=1,
    )
    low_mode_b_frequency = p.new(
        f"expr {230 if profile == 'v10' else 170}.*$f1*$f2",
        765, 535, 145, numinlets=2, numoutlets=1,
    )
    low_modes = p.new("+~", 885, 505, 40, numinlets=2, numoutlets=1)
    low_trim = p.new("*~ 0.32", 930, 505, 60, numinlets=2, numoutlets=1)
    pressure_body_l = p.new("+~", 735, 425, 40, numinlets=2, numoutlets=1)
    pressure_body_r = p.new("+~", 735, 495, 40, numinlets=2, numoutlets=1)
    pressure_body_gain_l = p.new("*~ 1.", 780, 425, 48, numinlets=2, numoutlets=1)
    pressure_body_gain_r = p.new("*~ 1.", 780, 495, 48, numinlets=2, numoutlets=1)
    pressure_crack_gain_l = p.new("*~ 1.", 735, 455, 48, numinlets=2, numoutlets=1)
    pressure_crack_gain_r = p.new("*~ 1.", 735, 525, 48, numinlets=2, numoutlets=1)
    pressure_crack_l = p.new("+~", 735, 445, 40, numinlets=2, numoutlets=1)
    pressure_crack_r = p.new("+~", 735, 480, 40, numinlets=2, numoutlets=1)
    core_mix_l = p.new("*~ 1.", 265, 520, 48, numinlets=2, numoutlets=1)
    core_mix_r = p.new("*~ 1.", 485, 520, 48, numinlets=2, numoutlets=1)
    beap_pressure_l = p.new("+~", 310, 490, 40, numinlets=2, numoutlets=1)
    beap_pressure_r = p.new("+~", 530, 490, 40, numinlets=2, numoutlets=1)

    def smoothed_control(source: str, x: float, y: float, initial: float) -> str:
        packed = p.new("pack 0. 20", x, y, 80, numinlets=2, numoutlets=1)
        initial_text = f"{initial:g}"
        if "." not in initial_text:
            initial_text += "."
        line = p.new(
            f"line {initial_text}", x + 85, y, 60,
            numinlets=2, numoutlets=2,
        )
        p.connect(source, packed)
        p.connect(packed, line)
        return line

    # A signal-rate line~ does not advance while the probe/runtime DSP is
    # stopped. Message-rate line keeps saved controls deterministic and feeds
    # float gains that persist across DSP restarts without loading Pop silent.
    low_level_line = smoothed_control(low_pressure_level, 835, 545, 0.32)
    body_level_line = smoothed_control(body_level, 970, 545, 1.0)
    crack_level_line = smoothed_control(crack_level, 1105, 545, 1.0)
    core_presence_line = smoothed_control(core_presence, 1050, 605, 1.0)
    p.connect(main_click, body_impulse)
    p.connect(body_impulse, body_decay)
    p.connect(body_decay, body_env)
    p.connect(main_click, crack_impulse)
    p.connect(crack_impulse, crack_decay)
    p.connect(crack_decay, crack_env)
    p.connect(pressure_noise, body_burst, 0, 0)
    p.connect(body_env, body_burst, 0, 1)
    p.connect(pressure_noise, crack_burst, 0, 0)
    p.connect(crack_env, crack_burst, 0, 1)
    p.connect(body_burst, pressure_l)
    p.connect(body_burst, pressure_r)
    p.connect(body_burst, low_mode_a)
    p.connect(body_burst, low_mode_b)
    p.connect(pitch_ratio, pressure_l_frequency)
    p.connect(pitch_ratio, pressure_r_frequency)
    p.connect(pitch_ratio, crack_l_frequency)
    p.connect(pitch_ratio, crack_r_frequency)
    p.connect(pitch_ratio, low_mode_a_frequency, 0, 0)
    p.connect(pitch_ratio, low_mode_b_frequency, 0, 0)
    p.connect(body_tune, pressure_l_frequency, 0, 1)
    p.connect(body_tune, pressure_r_frequency, 0, 1)
    p.connect(crack_tune, crack_l_frequency, 0, 1)
    p.connect(crack_tune, crack_r_frequency, 0, 1)
    p.connect(body_tune, low_mode_a_frequency, 0, 1)
    p.connect(body_tune, low_mode_b_frequency, 0, 1)
    p.connect(pressure_l_frequency, pressure_l, 0, 1)
    p.connect(pressure_r_frequency, pressure_r, 0, 1)
    p.connect(crack_l_frequency, crack_l_filter, 0, 1)
    p.connect(crack_r_frequency, crack_r_filter, 0, 1)
    p.connect(low_mode_a_frequency, low_mode_a, 0, 1)
    p.connect(low_mode_b_frequency, low_mode_b, 0, 1)
    p.connect(low_mode_a, low_modes, 0, 0)
    p.connect(low_mode_b, low_modes, 0, 1)
    p.connect(low_modes, low_trim)
    p.connect(low_level_line, low_trim, 0, 1)
    p.connect(crack_burst, crack_l_filter)
    p.connect(crack_burst, crack_r_filter)
    p.connect(pressure_l, pressure_body_l, 0, 0)
    p.connect(low_trim, pressure_body_l, 0, 1)
    p.connect(pressure_r, pressure_body_r, 0, 0)
    p.connect(low_trim, pressure_body_r, 0, 1)
    p.connect(pressure_body_l, pressure_body_gain_l, 0, 0)
    p.connect(pressure_body_r, pressure_body_gain_r, 0, 0)
    p.connect(body_level_line, pressure_body_gain_l, 0, 1)
    p.connect(body_level_line, pressure_body_gain_r, 0, 1)
    p.connect(crack_l_filter, pressure_crack_gain_l, 2, 0)
    p.connect(crack_r_filter, pressure_crack_gain_r, 2, 0)
    p.connect(crack_level_line, pressure_crack_gain_l, 0, 1)
    p.connect(crack_level_line, pressure_crack_gain_r, 0, 1)
    p.connect(pressure_body_gain_l, pressure_crack_l, 0, 0)
    p.connect(pressure_crack_gain_l, pressure_crack_l, 0, 1)
    p.connect(pressure_body_gain_r, pressure_crack_r, 0, 0)
    p.connect(pressure_crack_gain_r, pressure_crack_r, 0, 1)
    p.connect(event_trigger, main_click)
    tail_delay_1 = p.new(
        f"delay {55 if profile == 'v10' else 75}", 35, 610, 65,
        numinlets=2, numoutlets=1,
    )
    tail_delay_2 = p.new(
        f"delay {105 if profile == 'v10' else 135}", 35, 640, 70,
        numinlets=2, numoutlets=1,
    )
    tail_depth = p.new(
        "expr max(0.,min(1.,($f1-0.35)/0.65))",
        110, 640, 245, numinlets=1, numoutlets=1,
    )
    tail_level_1_map = p.new(
        f"expr {(0.24 if profile == 'v10' else 0.22):g}+{(0.12 if profile == 'v10' else 0.10):g}*$f1",
        365, 620, 185, numinlets=1, numoutlets=1,
    )
    tail_level_2_map = p.new(
        f"expr {(0.10 if profile == 'v10' else 0.08):g}*$f1",
        365, 650, 145, numinlets=1, numoutlets=1,
    )
    tail_level_1 = p.new("f 0.", 560, 620, 45, numinlets=2, numoutlets=1)
    tail_level_2 = p.new("f 0.", 560, 650, 45, numinlets=2, numoutlets=1)
    p.connect(intensity, tail_depth)
    p.connect(tail_depth, tail_level_1_map)
    p.connect(tail_depth, tail_level_2_map)
    p.connect(tail_level_1_map, tail_level_1, 0, 1)
    p.connect(tail_level_2_map, tail_level_2, 0, 1)
    p.connect(event_trigger, tail_delay_1)
    p.connect(event_trigger, tail_delay_2)
    p.connect(tail_delay_1, tail_level_1)
    p.connect(tail_delay_2, tail_level_2)
    p.connect(tail_level_1, main_click)
    p.connect(tail_level_2, main_click)
    p.connect(pressure_crack_l, core_mix_l, 0, 0)
    p.connect(pressure_crack_r, core_mix_r, 0, 0)
    p.connect(core_presence_line, core_mix_l, 0, 1)
    p.connect(core_presence_line, core_mix_r, 0, 1)
    p.connect(beap, beap_pressure_l, 0, 0)
    p.connect(core_mix_l, beap_pressure_l, 0, 1)
    p.connect(beap, beap_pressure_r, 1, 0)
    p.connect(core_mix_r, beap_pressure_r, 0, 1)
    left_drive = p.new("*~ 4.2", 310, 515, 55, numinlets=2, numoutlets=1)
    right_drive = p.new("*~ 4.2", 530, 515, 55, numinlets=2, numoutlets=1)
    left_sat = p.new("tanh~", 370, 515, 50, numinlets=1, numoutlets=1)
    right_sat = p.new("tanh~", 590, 515, 50, numinlets=1, numoutlets=1)
    left_filter = p.new("svf~ 35 0.7", 310, 545, 95, numinlets=3, numoutlets=4)
    right_filter = p.new("svf~ 35 0.7", 530, 545, 95, numinlets=3, numoutlets=4)
    output_gain_state = p.new("pak 0.7 1.", 780, 430, 90, numinlets=2, numoutlets=1)
    output_gain_expression = (
        "expr (0.60+0.85*$f1)*(0.55+0.45*$f2)"
        if profile == "v10"
        else "expr (0.66+0.94*$f1)*(0.55+0.45*$f2)"
    )
    output_gain_map = p.new(
        output_gain_expression,
        880, 430, 280, numinlets=2, numoutlets=1,
    )
    output_gain_pack = p.new("pack 0. 20", 880, 465, 85, numinlets=2, numoutlets=1)
    output_gain_line = p.new("line~", 975, 465, 50, numinlets=2, numoutlets=2)
    p.connect(intensity, output_gain_state, 0, 0)
    p.connect(event_strength, output_gain_state, 0, 1)
    p.connect(output_gain_state, output_gain_map)
    p.connect(output_gain_map, output_gain_pack)
    p.connect(output_gain_pack, output_gain_line)
    left_gain = p.new("*~", 310, 575, 40, numinlets=2, numoutlets=1)
    right_gain = p.new("*~", 530, 575, 40, numinlets=2, numoutlets=1)
    stem_level = add_db_gain_control(p, router, 12, 780, 530, -6.0)
    left_trim = p.new("*~", 310, 615, 40, numinlets=2, numoutlets=1)
    right_trim = p.new("*~", 530, 615, 40, numinlets=2, numoutlets=1)
    left = outlet(p, 330, 665, signal=True)
    right = outlet(p, 550, 665, signal=True)
    p.connect(beap_pressure_l, left_drive, 0, 0)
    p.connect(beap_pressure_r, right_drive, 0, 0)
    p.connect(left_drive, left_sat)
    p.connect(right_drive, right_sat)
    p.connect(left_sat, left_filter, 0, 0)
    p.connect(right_sat, right_filter, 0, 0)
    p.connect(left_filter, left_gain, 1, 0)
    p.connect(right_filter, right_gain, 1, 0)
    p.connect(output_gain_line, left_gain, 0, 1)
    p.connect(output_gain_line, right_gain, 0, 1)
    p.connect(left_gain, left_trim)
    p.connect(right_gain, right_trim)
    p.connect(stem_level, left_trim, 0, 1)
    p.connect(stem_level, right_trim, 0, 1)
    p.connect(left_trim, left)
    p.connect(right_trim, right)
    return p.document()


def make_ev_mode_voice(mode: str) -> dict[str, Any]:
    """Wrap a user BEAP patcher as a suspendable poly~ voice."""
    p = Patcher(620, 360)
    p.comment(f"EV {mode} poly voice — thispoly~ is controlled by ev_soundscape_host~", 20, 15, 520)
    pitch = p.new("in~ 1", 35, 65, 45, numinlets=0, numoutlets=1)
    gate_cv = p.new("in~ 2", 125, 65, 45, numinlets=0, numoutlets=1)
    throttle_cv = p.new("in~ 3", 215, 65, 45, numinlets=0, numoutlets=1)
    beap_name = "ev_pad_beap~" if mode == "relax" else f"ev_{mode}_beap~"
    beap = p.new(beap_name, 120, 135, 145, numinlets=3, numoutlets=2)
    state = p.new("thispoly~", 390, 135, 70, numinlets=2, numoutlets=3)
    left = p.new("out~ 1", 90, 265, 50, numinlets=1, numoutlets=0)
    right = p.new("out~ 2", 260, 265, 50, numinlets=1, numoutlets=0)
    p.connect(pitch, beap, 0, 0)
    p.connect(gate_cv, beap, 0, 1)
    p.connect(throttle_cv, beap, 0, 2)
    p.connect(beap, left, 0)
    p.connect(beap, right, 1)
    return p.document()


def make_ev_soundscape_host() -> dict[str, Any]:
    """Crossfade EV modes, then suspend the two inactive poly~ voices."""
    p = Patcher(1260, 790)
    p.comment("EV BEAP soundscape host — Relax / Expressive / Sport with 250 ms crossfade and DSP suspend", 25, 15, 900)
    control = inlet(p, 35, 65)
    names = (
        "rpm", "throttle", "ignition", "start", "ev_mode",
        "ev_soundscape_level_db", "ev_soundscape_mute", "pad_level_db", "pad_mute",
    )
    router = route(p, names, 35, 105, 810)
    p.connect(control, router)
    level_alias = p.new("prepend ev_soundscape_level_db", 900, 105, 205, numinlets=1, numoutlets=1)
    mute_alias = p.new("prepend ev_soundscape_mute", 1115, 105, 175, numinlets=1, numoutlets=1)
    p.connect(router, level_alias, 7)
    p.connect(level_alias, router)
    p.connect(router, mute_alias, 8)
    p.connect(mute_alias, router)

    rpm_clip = p.new("clip 0. 10000.", 35, 160, 105, numinlets=3, numoutlets=1)
    pitch_map = p.new(
        "expr log(max(20.,55.+$f1*.052)/261.625565)/log(2.)",
        35, 200, 390, numinlets=1, numoutlets=1,
    )
    pitch_pack = p.new("pack 0. 60", 35, 240, 85, numinlets=2, numoutlets=1)
    pitch_line = p.new("line~", 35, 280, 50, numinlets=2, numoutlets=2)
    throttle_clip = p.new("clip 0. 1.", 455, 160, 75, numinlets=3, numoutlets=1)
    throttle_state = p.new("pak 0. 650.", 455, 200, 85, numinlets=2, numoutlets=1)
    throttle_map = p.new(
        "expr min(4.5,0.9+2.8*$f1+0.7*min(1.,$f2/10000.))",
        550, 200, 430, numinlets=2, numoutlets=1,
    )
    throttle_pack = p.new("pack 0. 120", 455, 240, 95, numinlets=2, numoutlets=1)
    throttle_line = p.new("line~", 455, 280, 50, numinlets=2, numoutlets=2)
    ignition = p.new("clip 0. 1.", 625, 160, 75, numinlets=3, numoutlets=1)
    gate_map = p.new("expr $f1*5.", 625, 200, 90, numinlets=1, numoutlets=1)
    gate_pack = p.new("pack 0. 10", 625, 240, 85, numinlets=2, numoutlets=1)
    gate_line = p.new("line~", 625, 280, 50, numinlets=2, numoutlets=2)
    start_edge = p.new("sel 1", 745, 160, 45, numinlets=1, numoutlets=2)
    start_message = p.message("3.5 0, 0. 650", 745, 200, 105)
    start_line = p.new("line~", 745, 240, 50, numinlets=2, numoutlets=2)
    throttle_plus_start = p.new("+~", 535, 300, 40, numinlets=2, numoutlets=1)
    p.connect(router, rpm_clip, 0)
    p.connect(rpm_clip, pitch_map)
    p.connect(pitch_map, pitch_pack)
    p.connect(pitch_pack, pitch_line)
    p.connect(router, throttle_clip, 1)
    p.connect(throttle_clip, throttle_state, 0, 0)
    p.connect(rpm_clip, throttle_state, 0, 1)
    p.connect(throttle_state, throttle_map)
    p.connect(throttle_map, throttle_pack)
    p.connect(throttle_pack, throttle_line)
    p.connect(router, ignition, 2)
    p.connect(ignition, gate_map)
    p.connect(gate_map, gate_pack)
    p.connect(gate_pack, gate_line)
    p.connect(router, start_edge, 3)
    p.connect(start_edge, start_message, 0)
    p.connect(start_message, start_line)
    p.connect(throttle_line, throttle_plus_start, 0, 0)
    p.connect(start_line, throttle_plus_start, 0, 1)

    modes = ("relax", "expressive", "sport")
    voices: list[str] = []
    gain_lines: list[str] = []
    channel_gains: list[tuple[str, str]] = []
    for index, mode in enumerate(modes):
        x = 60 + index * 350
        voice = p.new(f"poly~ ev_{mode}_voice 1", x, 355, 190, numinlets=3, numoutlets=2)
        gain_pack = p.new("pack 0. 250", x, 400, 85, numinlets=2, numoutlets=1)
        gain_line = p.new("line~", x, 435, 50, numinlets=2, numoutlets=2)
        gain_l = p.new("*~", x, 475, 40, numinlets=2, numoutlets=1)
        gain_r = p.new("*~", x + 85, 475, 40, numinlets=2, numoutlets=1)
        p.connect(pitch_line, voice, 0, 0)
        p.connect(gate_line, voice, 0, 1)
        p.connect(throttle_plus_start, voice, 0, 2)
        p.connect(gain_pack, gain_line)
        p.connect(voice, gain_l, 0, 0)
        p.connect(voice, gain_r, 1, 0)
        p.connect(gain_line, gain_l, 0, 1)
        p.connect(gain_line, gain_r, 0, 1)
        voices.append(voice)
        gain_lines.append(gain_pack)
        channel_gains.append((gain_l, gain_r))

    mode_select = p.new("sel relax expressive sport", 860, 160, 175, numinlets=1, numoutlets=4)
    default_mode = p.new("loadmess relax", 1045, 160, 105, numinlets=1, numoutlets=1)
    p.connect(router, mode_select, 4)
    p.connect(default_mode, mode_select)
    active_mode = p.new("int 0", 860, 465, 45, numinlets=2, numoutlets=1)
    suspend_select = p.new("sel 0 1 2", 920, 465, 80, numinlets=1, numoutlets=4)
    reschedule = p.new("t b b", 860, 425, 50, numinlets=1, numoutlets=2)
    cancel_suspend = p.message("stop", 920, 425, 40)
    suspend_delay = p.new("delay 260", 970, 425, 70, numinlets=2, numoutlets=1)
    p.connect(reschedule, cancel_suspend, 1)
    p.connect(cancel_suspend, suspend_delay)
    p.connect(reschedule, suspend_delay, 0)
    p.connect(suspend_delay, active_mode)
    p.connect(active_mode, suspend_select)
    for selected in range(3):
        y = 200 + selected * 85
        selected_value = p.message(str(selected), 805, y, 30)
        p.connect(mode_select, selected_value, selected)
        p.connect(selected_value, active_mode, 0, 1)
        p.connect(mode_select, reschedule, selected)
        unmute = p.message("mute 1 0", 860, y, 65)
        p.connect(mode_select, unmute, selected)
        p.connect(unmute, voices[selected])
        for index in range(3):
            target = p.message("1." if index == selected else "0.", 1015 + index * 45, y, 35)
            p.connect(mode_select, target, selected)
            p.connect(target, gain_lines[index])
            if index != selected:
                suspend = p.message("mute 1 1", 1015 + index * 85, y + 35, 65)
                p.connect(suspend_select, suspend, selected)
                p.connect(suspend, voices[index])

    left_sum_1 = p.new("+~", 275, 555, 40, numinlets=2, numoutlets=1)
    left_sum_2 = p.new("+~", 475, 590, 40, numinlets=2, numoutlets=1)
    right_sum_1 = p.new("+~", 650, 555, 40, numinlets=2, numoutlets=1)
    right_sum_2 = p.new("+~", 850, 590, 40, numinlets=2, numoutlets=1)
    highpass_l = p.new("svf~ 320 0.7", 475, 620, 100, numinlets=3, numoutlets=4)
    highpass_r = p.new("svf~ 320 0.7", 850, 620, 100, numinlets=3, numoutlets=4)
    p.connect(channel_gains[0][0], left_sum_1, 0, 0)
    p.connect(channel_gains[1][0], left_sum_1, 0, 1)
    p.connect(left_sum_1, left_sum_2, 0, 0)
    p.connect(channel_gains[2][0], left_sum_2, 0, 1)
    p.connect(channel_gains[0][1], right_sum_1, 0, 0)
    p.connect(channel_gains[1][1], right_sum_1, 0, 1)
    p.connect(right_sum_1, right_sum_2, 0, 0)
    p.connect(channel_gains[2][1], right_sum_2, 0, 1)
    p.connect(left_sum_2, highpass_l)
    p.connect(right_sum_2, highpass_r)

    level = add_db_gain_control(p, router, 5, 960, 555, -9.0)
    mute = p.new("clip 0 1", 960, 700, 65, numinlets=3, numoutlets=1)
    mute_gain = p.new("expr 1-$i1", 1035, 700, 80, numinlets=1, numoutlets=1)
    mute_pack = p.new("pack 0. 30", 1125, 700, 85, numinlets=2, numoutlets=1)
    mute_line = p.new("line~", 1125, 735, 50, numinlets=2, numoutlets=2)
    mute_default = p.new("loadmess 0", 1040, 735, 80, numinlets=1, numoutlets=1)
    p.connect(router, mute, 6)
    p.connect(mute_default, mute)
    p.connect(mute, mute_gain)
    p.connect(mute_gain, mute_pack)
    p.connect(mute_pack, mute_line)
    out_l_gain = p.new("*~", 475, 650, 40, numinlets=2, numoutlets=1)
    out_r_gain = p.new("*~", 850, 650, 40, numinlets=2, numoutlets=1)
    out_l_mute = p.new("*~", 475, 700, 40, numinlets=2, numoutlets=1)
    out_r_mute = p.new("*~", 850, 700, 40, numinlets=2, numoutlets=1)
    left = outlet(p, 475, 750, signal=True)
    right = outlet(p, 850, 750, signal=True)
    p.connect(highpass_l, out_l_gain, 1, 0)
    p.connect(highpass_r, out_r_gain, 1, 0)
    p.connect(level, out_l_gain, 0, 1)
    p.connect(level, out_r_gain, 0, 1)
    p.connect(out_l_gain, out_l_mute)
    p.connect(out_r_gain, out_r_mute)
    p.connect(mute_line, out_l_mute, 0, 1)
    p.connect(mute_line, out_r_mute, 0, 1)
    p.connect(out_l_mute, left)
    p.connect(out_r_mute, right)
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


def make_profile_controller(profile: str) -> dict[str, Any]:
    """Lifecycle controller with a fixed profile and no profile-weight traffic."""
    p = Patcher(940, 650)
    p.comment(f"{profile.upper()} fixed lifecycle controller — start lock and catch; drivetrain owns shift envelope", 25, 15, 760)
    control = inlet(p, 35, 65)
    split = p.new("t l l", 35, 105, 55, numinlets=1, numoutlets=2)
    router = route(p, ("ignition", "start", "shift", "shift_dir", "exhaust_pop", "pop"), 120, 105, 520)
    output = outlet(p, 470, 595)
    p.connect(control, split)
    p.connect(split, output, 0)
    p.connect(split, router, 1)

    ignition = p.new("clip 0 1", 120, 165, 65, numinlets=3, numoutlets=1)
    ignition_off = p.new("sel 0", 120, 205, 45, numinlets=1, numoutlets=2)
    start = p.new("clip 0 1", 225, 165, 65, numinlets=3, numoutlets=1)
    unlock = p.new("int 1", 315, 165, 50, numinlets=2, numoutlets=1)
    state = p.new("pak 0 0 1", 225, 205, 90, numinlets=3, numoutlets=1)
    valid = p.new("expr $i1*$i2*$i3", 225, 245, 125, numinlets=3, numoutlets=1)
    edge = p.new("sel 1", 225, 285, 45, numinlets=1, numoutlets=2)
    p.connect(router, ignition, 0)
    p.connect(router, start, 1)
    p.connect(ignition, ignition_off)
    p.connect(ignition, state, 0, 1)
    p.connect(start, state, 0, 0)
    p.connect(unlock, state, 0, 2)
    p.connect(state, valid)
    p.connect(valid, edge)

    catch_ms = 250 if profile == "ev" else 850
    trigger = p.new("t b b b b", 225, 325, 80, numinlets=1, numoutlets=4)
    lock = p.message("0", 190, 365, 30)
    unlock_message = p.message("1", 150, 245, 30)
    starter_on = p.message("starter 1", 235, 365, 70)
    running_off = p.message("engine_running 0", 320, 365, 105)
    combustion_off = p.message("combustion_gain 0", 440, 365, 115)
    delay = p.new(f"delay {catch_ms}", 570, 365, 75, numinlets=2, numoutlets=1)
    caught = p.new("t b b b", 570, 405, 70, numinlets=1, numoutlets=3)
    starter_off = p.message("starter 0", 500, 450, 70)
    running_on = p.message("engine_running 1", 590, 450, 105)
    combustion_on = p.message("combustion_gain 1", 715, 450, 115)
    p.connect(edge, trigger, 0)
    p.connect(trigger, lock, 3)
    p.connect(lock, unlock, 0, 0)
    p.connect(trigger, starter_on, 2)
    p.connect(trigger, running_off, 1)
    p.connect(trigger, combustion_off, 0)
    p.connect(trigger, delay)
    p.connect(delay, caught)
    p.connect(caught, starter_off, 2)
    p.connect(caught, running_on, 1)
    p.connect(caught, combustion_on, 0)
    for message in (starter_on, running_off, combustion_off, starter_off, running_on, combustion_on):
        p.connect(message, output)

    cancel = p.message("stop", 85, 285, 40)
    stop_trigger = p.new("t b b b", 85, 325, 70, numinlets=1, numoutlets=3)
    p.connect(ignition_off, cancel, 0)
    p.connect(cancel, delay)
    p.connect(ignition_off, unlock_message, 0)
    p.connect(unlock_message, unlock)
    p.connect(ignition_off, stop_trigger, 0)
    p.connect(stop_trigger, starter_off, 2)
    p.connect(stop_trigger, running_off, 1)
    p.connect(stop_trigger, combustion_off, 0)

    for index, text in enumerate(("combustion_gain 0", "engine_running 0", "shift_cut 1", "starter 0")):
        initial = p.new(f"loadmess {text}", 35 + index * 180, 545, 150, numinlets=1, numoutlets=1)
        p.connect(initial, output)
    return p.document()


def make_profile_engine(profile: str) -> dict[str, Any]:
    """Compose one profile renderer with shared transient, road, cabin and master modules."""
    p = Patcher(1450, 860)
    p.comment(f"vehicle_engine_{profile}~ — fixed-profile public seam", 25, 15, 620)
    control = inlet(p, 45, 65)
    controller = p.new(f"engine_controller_{profile}", 45, 105, 165, numinlets=1, numoutlets=1)
    fan = p.new("t l l l l l l l", 45, 150, 135, numinlets=1, numoutlets=7)
    contract_names = list(PROFILE_MESSAGES)
    contract_names.extend(("start_style",) if profile != "ev" else ("ev_mode", "ev_soundscape_level_db", "ev_soundscape_mute"))
    contract = route(p, tuple(contract_names), 190, 150, 990)
    power = p.new(f"{profile}_sound_dna~", 95, 260, 145, numinlets=1, numoutlets=2)
    pad = p.new(
        f"{profile}_cinematic_soundscape_host~", 95, 305, 220,
        numinlets=1, numoutlets=2,
    )
    transient = p.new(f"transient_{profile}~", 285, 260, 120, numinlets=1, numoutlets=2)
    road = p.new("road_air~", 465, 260, 85, numinlets=1, numoutlets=2)
    rumble = p.new("cabin_rumble~", 625, 260, 110, numinlets=3, numoutlets=2)
    cabin = p.new("cabin_master~", 800, 450, 110, numinlets=3, numoutlets=2)
    eq = p.add(
        "bpatcher", None, 460, 495, 970, 340,
        numinlets=3, numoutlets=2, name="vehicle_bus_eq~.maxpat",
        presentation=1, presentation_rect=[15.0, 15.0, 970.0, 340.0],
    )
    mix = p.new("mix_master~", 1030, 500, 110, numinlets=3, numoutlets=2)
    add_l1 = p.new("+~", 130, 350, 35, numinlets=2, numoutlets=1)
    add_l2 = p.new("+~", 235, 390, 35, numinlets=2, numoutlets=1)
    add_l3 = p.new("+~", 340, 430, 35, numinlets=2, numoutlets=1)
    add_r1 = p.new("+~", 390, 350, 35, numinlets=2, numoutlets=1)
    add_r2 = p.new("+~", 495, 390, 35, numinlets=2, numoutlets=1)
    add_r3 = p.new("+~", 600, 430, 35, numinlets=2, numoutlets=1)
    left = outlet(p, 1030, 815, signal=True)
    right = outlet(p, 1120, 815, signal=True)
    p.connect(control, controller)
    p.connect(controller, fan)
    p.connect(fan, contract, 6)
    p.connect(fan, power, 5)
    p.connect(fan, pad, 5)
    p.connect(fan, transient, 4)
    p.connect(fan, road, 3)
    p.connect(fan, rumble, 2)
    p.connect(fan, cabin, 1, 0)
    p.connect(fan, mix, 0, 0)
    p.connect(fan, eq, 0, 0)
    solo_router = route(
        p, ("soundscape_solo", "pad_solo", "backfire_solo", "dna_solo"),
        980, 210, 410,
    )
    soundscape_solo_clip = p.new("clip 0 1", 1010, 250, 65, numinlets=3, numoutlets=1)
    backfire_solo_clip = p.new("clip 0 1", 1085, 250, 65, numinlets=3, numoutlets=1)
    dna_solo_clip = p.new("clip 0 1", 1160, 250, 65, numinlets=3, numoutlets=1)
    solo_state = p.new("pak 0 0 0", 1235, 250, 90, numinlets=3, numoutlets=1)
    core_solo_gain = p.new(
        "expr $i3+(1-$i3)*(1-max($i1,$i2))", 1180, 220, 245,
        numinlets=3, numoutlets=1,
    )
    aux_solo_gain = p.new(
        "expr (1-$i3)*(1-max($i1,$i2))", 1180, 280, 215,
        numinlets=3, numoutlets=1,
    )
    transient_solo_gain = p.new(
        "expr (1-$i3)*(1-$i1*(1-$i2))", 1180, 310, 225,
        numinlets=3, numoutlets=1,
    )
    pad_solo_gain = p.new(
        "expr (1-$i3)*(1-$i2)", 1180, 340, 155,
        numinlets=3, numoutlets=1,
    )

    def solo_line(source: str, x: float, y: float) -> str:
        packed = p.new("pack 0. 35", x, y, 85, numinlets=2, numoutlets=1)
        line = p.new("line~", x + 95, y, 50, numinlets=2, numoutlets=2)
        p.connect(source, packed)
        p.connect(packed, line)
        return line

    core_solo_line = solo_line(core_solo_gain, 970, 370)
    aux_solo_line = solo_line(aux_solo_gain, 1115, 370)
    transient_solo_line = solo_line(transient_solo_gain, 1260, 370)
    pad_solo_line = solo_line(pad_solo_gain, 1260, 400)
    solo_default = p.new("loadmess 0", 1090, 285, 80, numinlets=1, numoutlets=1)
    core_l = p.new("*~", 95, 300, 40, numinlets=2, numoutlets=1)
    core_r = p.new("*~", 390, 300, 40, numinlets=2, numoutlets=1)
    transient_l = p.new("*~", 285, 305, 40, numinlets=2, numoutlets=1)
    transient_r = p.new("*~", 335, 305, 40, numinlets=2, numoutlets=1)
    road_l = p.new("*~", 465, 305, 40, numinlets=2, numoutlets=1)
    road_r = p.new("*~", 515, 305, 40, numinlets=2, numoutlets=1)
    rumble_l = p.new("*~", 625, 305, 40, numinlets=2, numoutlets=1)
    rumble_r = p.new("*~", 675, 305, 40, numinlets=2, numoutlets=1)
    pad_l = p.new("*~", 95, 335, 40, numinlets=2, numoutlets=1)
    pad_r = p.new("*~", 390, 335, 40, numinlets=2, numoutlets=1)
    p.connect(control, solo_router)
    p.connect(solo_router, soundscape_solo_clip, 0)
    p.connect(solo_router, soundscape_solo_clip, 1)
    p.connect(solo_router, backfire_solo_clip, 2)
    p.connect(solo_router, dna_solo_clip, 3)
    p.connect(solo_default, soundscape_solo_clip)
    p.connect(solo_default, backfire_solo_clip)
    p.connect(solo_default, dna_solo_clip)
    p.connect(soundscape_solo_clip, solo_state, 0, 0)
    p.connect(backfire_solo_clip, solo_state, 0, 1)
    p.connect(dna_solo_clip, solo_state, 0, 2)
    p.connect(solo_state, core_solo_gain)
    p.connect(solo_state, aux_solo_gain)
    p.connect(solo_state, transient_solo_gain)
    p.connect(solo_state, pad_solo_gain)
    p.connect(power, core_l, 0, 0)
    p.connect(power, core_r, 1, 0)
    p.connect(transient, transient_l, 0, 0)
    p.connect(transient, transient_r, 1, 0)
    p.connect(road, road_l, 0, 0)
    p.connect(road, road_r, 1, 0)
    p.connect(rumble, rumble_l, 0, 0)
    p.connect(rumble, rumble_r, 1, 0)
    for stem_gain in (core_l, core_r):
        p.connect(core_solo_line, stem_gain, 0, 1)
    for stem_gain in (road_l, road_r, rumble_l, rumble_r):
        p.connect(aux_solo_line, stem_gain, 0, 1)
    for stem_gain in (transient_l, transient_r):
        p.connect(transient_solo_line, stem_gain, 0, 1)
    p.connect(pad, pad_l, 0, 0)
    p.connect(pad, pad_r, 1, 0)
    p.connect(pad_solo_line, pad_l, 0, 1)
    p.connect(pad_solo_line, pad_r, 0, 1)
    pad_sum_l = p.new("+~", 95, 340, 35, numinlets=2, numoutlets=1)
    pad_sum_r = p.new("+~", 390, 340, 35, numinlets=2, numoutlets=1)
    p.connect(core_l, pad_sum_l, 0, 0)
    p.connect(pad_l, pad_sum_l, 0, 1)
    p.connect(core_r, pad_sum_r, 0, 0)
    p.connect(pad_r, pad_sum_r, 0, 1)
    power_l = pad_sum_l
    power_r = pad_sum_r
    power_l_out = 0
    power_r_out = 0
    p.connect(power_l, add_l1, power_l_out, 0)
    p.connect(transient_l, add_l1, 0, 1)
    p.connect(add_l1, add_l2, 0, 0)
    p.connect(road_l, add_l2, 0, 1)
    p.connect(add_l2, add_l3, 0, 0)
    p.connect(rumble_l, add_l3, 0, 1)
    p.connect(power_r, add_r1, power_r_out, 0)
    p.connect(transient_r, add_r1, 0, 1)
    p.connect(add_r1, add_r2, 0, 0)
    p.connect(road_r, add_r2, 0, 1)
    p.connect(add_r2, add_r3, 0, 0)
    p.connect(rumble_r, add_r3, 0, 1)
    # Feed the rumble resonator from the already solo-gated powertrain. This
    # prevents stored excitation from leaking into an isolated Soundscape.
    p.connect(core_l, rumble, 0, 1)
    p.connect(core_r, rumble, 0, 2)
    p.connect(add_l3, cabin, 0, 1)
    p.connect(add_r3, cabin, 0, 2)
    p.connect(cabin, eq, 0, 1)
    p.connect(cabin, eq, 1, 2)
    p.connect(eq, mix, 0, 1)
    p.connect(eq, mix, 1, 2)
    p.connect(mix, left, 0)
    p.connect(mix, right, 1)
    return p.document(presentation=True)


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


def make_vehicle_bus_eq() -> dict[str, Any]:
    p = Patcher(1180, 900)
    p.comment("USER-TUNABLE VEHICLE BUS EQ — drag four nodes; saved locally and preserved on rebuild", 25, 15, 850)
    control = inlet(p, 35, 60)
    left_in = inlet(p, 170, 60, signal=True)
    right_in = inlet(p, 280, 60, signal=True)
    master_controls = (
        "eq_low", "eq_lowmid", "eq_highmid", "eq_high", "eq_bypass", "master_trim_db",
    )
    router = route(p, master_controls, 35, 105, 1080)
    p.connect(control, router)
    p.new("autopattr @autorestore 0", 760, 5, 155, numinlets=1, numoutlets=4)
    storage = p.new(
        "pattrstorage vehicle_bus_eq @savemode 3 @changemode 1 @autorestore 0",
        925, 5, 245, numinlets=1, numoutlets=4,
    )
    p.comment(
        "Tracked fallback definition: Patcher:/presets/vehicle_bus_eq_default.json",
        760, 335, 390,
    )
    state_load = p.new("loadbang", 1095, 370, 60, numinlets=1, numoutlets=1)
    state_delay = p.new("delay 120", 1095, 405, 70, numinlets=2, numoutlets=1)
    state_path = p.new("js Patcher:/code/eq_state_path.js", 760, 405, 220, numinlets=1, numoutlets=1)
    local_read = p.message("restore", 990, 405, 55)
    close_save = p.new("closebang", 1095, 475, 65, numinlets=0, numoutlets=1)
    restore_trigger = p.new("t b b", 1095, 510, 50, numinlets=1, numoutlets=2)
    restore_delay = p.new("delay 30", 1035, 545, 65, numinlets=2, numoutlets=1)
    recall_slot = p.message("1", 1110, 545, 30)
    save_now = p.message("save", 850, 510, 45)
    external_save = p.new("r vehicle_bus_eq.save", 760, 475, 135, numinlets=0, numoutlets=1)
    p.connect(state_load, state_delay)
    p.connect(state_delay, restore_trigger)
    p.connect(restore_trigger, local_read, 1)
    p.connect(restore_trigger, restore_delay, 0)
    p.connect(restore_delay, recall_slot)
    p.connect(recall_slot, storage)
    p.connect(local_read, state_path)
    p.connect(state_path, storage)
    p.connect(close_save, save_now)
    p.connect(external_save, save_now)
    p.connect(save_now, state_path)

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
        varname="vehicle_bus_eq_graph",
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

    save_eq = p.add(
        "message", "Save EQ", 760, 65, 70, numinlets=2, numoutlets=1,
        presentation=1, presentation_rect=[955.0, 255.0, 75.0, 22.0],
    )
    reload_eq = p.add(
        "message", "Reload EQ", 840, 65, 80, numinlets=2, numoutlets=1,
        presentation=1, presentation_rect=[1040.0, 255.0, 85.0, 22.0],
    )
    p.connect(save_eq, save_now)
    p.connect(reload_eq, restore_trigger)

    bypass_ui = p.add(
        "toggle", None, 760, 85, 22, 22, numinlets=1, numoutlets=1,
        presentation=1, presentation_rect=[870.0, 295.0, 22.0, 22.0],
        varname="vehicle_bus_eq_bypass",
    )
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
    left = outlet(p, 470, 820, signal=True)
    right = outlet(p, 650, 820, signal=True)
    p.connect(masters[0], left)
    p.connect(masters[1], right)
    return p.document(presentation=True)


def make_mix_master() -> dict[str, Any]:
    """Generated safety dynamics only; user tone shaping lives in vehicle_bus_eq~."""
    p = Patcher(920, 520)
    p.comment("GENERATED SAFETY MASTER — compressor, makeup, limiter and final ceiling", 25, 15, 720)
    control = inlet(p, 35, 60)
    left_in = inlet(p, 175, 60, signal=True)
    right_in = inlet(p, 285, 60, signal=True)
    names = (
        "compressor_threshold_db", "compressor_ratio", "compressor_attack_rate",
        "compressor_release_rate", "compressor_makeup_db", "compressor_bypass",
    )
    router = route(p, names, 35, 105, 790)
    p.connect(control, router)
    compressor = p.new("omx.comp~", 360, 270, 105, numinlets=2, numoutlets=4)
    defaults_bang = p.new("loadbang", 35, 155, 60, numinlets=1, numoutlets=1)
    defaults = p.message(
        "agcEnabled 1, agcThreshold -12., ratio 2., attack 85., release 35., "
        "smoothGain 35., range 0, channelCoupling 0, dualBandEnabled 0, "
        "limEnabled 0, ngEnabled 0, sidechainFilterEnabled 0, delay 0, "
        "progressiveRelease 0, bypass 0",
        105, 155, 650,
    )
    p.connect(defaults_bang, defaults)
    p.connect(defaults, compressor)
    p.connect(left_in, compressor, 0, 0)
    p.connect(right_in, compressor, 0, 1)
    specs = (
        ("clip -36. 0.", "prepend agcThreshold", -12.0),
        ("clip 1. 50.", "prepend ratio", 2.0),
        ("clip 0. 150.", "prepend attack", 85.0),
        ("clip 0. 150.", "prepend release", 35.0),
    )
    for index, (clip_text, prepend_text, default) in enumerate(specs):
        x = 35 + index * 200
        bounded = p.new(clip_text, x, 205, 95, numinlets=3, numoutlets=1)
        named = p.new(prepend_text, x, 240, 150, numinlets=1, numoutlets=1)
        initial = p.new(f"loadmess {default:g}", x, 275, 95, numinlets=1, numoutlets=1)
        p.connect(router, bounded, index)
        p.connect(initial, bounded)
        p.connect(bounded, named)
        p.connect(named, compressor)
    makeup_clip = p.new("clip -12. 12.", 35, 325, 85, numinlets=3, numoutlets=1)
    makeup_amp = p.new("expr pow(10.,$f1/20.)", 130, 325, 150, numinlets=1, numoutlets=1)
    makeup_pack = p.new("pack 0. 50", 290, 325, 85, numinlets=2, numoutlets=1)
    makeup_line = p.new("line~", 385, 325, 50, numinlets=2, numoutlets=2)
    makeup_initial = p.new("loadmess 0.", 35, 360, 85, numinlets=1, numoutlets=1)
    p.connect(router, makeup_clip, 4)
    p.connect(makeup_initial, makeup_clip)
    p.connect(makeup_clip, makeup_amp)
    p.connect(makeup_amp, makeup_pack)
    p.connect(makeup_pack, makeup_line)
    bypass_clip = p.new("clip 0 1", 500, 325, 65, numinlets=3, numoutlets=1)
    bypass_named = p.new("prepend bypass", 575, 325, 100, numinlets=1, numoutlets=1)
    bypass_initial = p.new("loadmess 0", 685, 325, 80, numinlets=1, numoutlets=1)
    p.connect(router, bypass_clip, 5)
    p.connect(bypass_initial, bypass_clip)
    p.connect(bypass_clip, bypass_named)
    p.connect(bypass_named, compressor)
    gains = []
    for channel, x in ((0, 285), (1, 535)):
        gain = p.new("*~", x, 370, 40, numinlets=2, numoutlets=1)
        p.connect(compressor, gain, channel, 0)
        p.connect(makeup_line, gain, 0, 1)
        gains.append(gain)
    limiter = p.new("omx.peaklim~", 360, 410, 105, numinlets=2, numoutlets=4)
    clip_l = p.new("clip~ -0.891 0.891", 235, 450, 130, numinlets=3, numoutlets=1)
    clip_r = p.new("clip~ -0.891 0.891", 510, 450, 130, numinlets=3, numoutlets=1)
    left = outlet(p, 360, 490, signal=True)
    right = outlet(p, 555, 490, signal=True)
    p.connect(gains[0], limiter, 0, 0)
    p.connect(gains[1], limiter, 0, 1)
    p.connect(limiter, clip_l, 0, 0)
    p.connect(limiter, clip_r, 1, 0)
    p.connect(clip_l, left)
    p.connect(clip_r, right)
    return p.document()


def make_profile_powertrain(profile: str) -> dict[str, Any]:
    """Render one profile only; inactive powertrains are absent, not gain-muted."""
    p = Patcher(1080, 660)
    p.comment(f"{profile.upper()} dedicated powertrain — procedural continuous synthesis", 25, 15, 760)
    control = inlet(p, 35, 65)
    tonal_names = (
        ("rpm", "throttle", "load", "aggression", "brightness", "body", "texture")
        if profile == "ev"
        else ("rpm", "throttle", "load", "accel", "aggression", "brightness", "body", "texture")
    )
    fuel_names = ("engine_running", "combustion_gain", "shift_cut") if profile != "ev" else ()
    common_realism_names = (
        "air_detail", "cycle_irregularity", "stereo_width",
        "throttle_loudness_depth", "saturation",
    )
    profile_names = (
        ("torque_ripple_level", "gear_mesh_level", "electrical_detail")
        if profile == "ev"
        else ("combustion_pulse", "intake_detail", "exhaust_detail", "residual_detail")
    )
    names = tonal_names + fuel_names + common_realism_names + profile_names + ("powertrain_level_db",)
    router = route(p, names, 35, 105, 860)
    p.connect(control, router)
    gen = p.new(
        f"gen~ @gen ../gen/{profile}_powertrain.gendsp",
        300,
        330,
        270,
        numinlets=1,
        numoutlets=2,
    )

    bounds = {
        "rpm": (0.0, 10000.0),
        "throttle": (0.0, 1.0),
        "load": (-1.0, 1.0),
        "accel": (-1.0, 1.0),
        "aggression": (0.0, 1.0),
        "brightness": (0.0, 1.0),
        "body": (0.0, 1.0),
        "texture": (0.0, 1.0),
    }
    for index, name in enumerate(tonal_names):
        low, high = bounds[name]
        x = 35 + index * 140
        bounded = p.new(f"clip {low:g} {high:g}", x, 165, 90, numinlets=3, numoutlets=1)
        named = p.message(f"{name} $1", x, 205, 105)
        p.connect(router, bounded, index)
        p.connect(bounded, named)
        p.connect(named, gen)

    for offset, name in enumerate(fuel_names):
        x = 550 + offset * 155
        bounded = p.new("clip 0. 1.", x, 250, 75, numinlets=3, numoutlets=1)
        named = p.message(f"{name} $1", x, 285, 125)
        p.connect(router, bounded, len(tonal_names) + offset)
        p.connect(bounded, named)
        p.connect(named, gen)

    realism_bounds = {
        **{name: (0.0, 1.0) for name in common_realism_names + profile_names},
        "throttle_loudness_depth": (0.0, 8.0),
    }
    realism_start = len(tonal_names) + len(fuel_names)
    for offset, name in enumerate(common_realism_names + profile_names):
        low, high = realism_bounds[name]
        x = 35 + (offset % 6) * 170
        y = 335 + (offset // 6) * 80
        bounded = p.new(f"clip {low:g} {high:g}", x, y, 90, numinlets=3, numoutlets=1)
        named = p.new(f"prepend {name}", x, y + 35, 145, numinlets=1, numoutlets=1)
        p.connect(router, bounded, realism_start + offset)
        p.connect(bounded, named)
        p.connect(named, gen)

    # Every profile's continuous vehicle core remains procedural. The optional
    # shared cinematic Soundscape is composed one layer higher so the same
    # editable BEAP patcher can be used by EV, V10, and V12.
    mixed_l = gen
    mixed_r = gen
    mixed_l_out = 0
    mixed_r_out = 1
    stem_level = add_db_gain_control(p, router, len(names) - 1, 790, 375, -3.0)
    trim_l = p.new("*~", 360, 535, 40, numinlets=2, numoutlets=1)
    trim_r = p.new("*~", 580, 535, 40, numinlets=2, numoutlets=1)
    left = outlet(p, 360, 585, signal=True)
    right = outlet(p, 580, 585, signal=True)
    p.connect(mixed_l, trim_l, mixed_l_out, 0)
    p.connect(mixed_r, trim_r, mixed_r_out, 0)
    p.connect(stem_level, trim_l, 0, 1)
    p.connect(stem_level, trim_r, 0, 1)
    p.connect(trim_l, left)
    p.connect(trim_r, right)
    return p.document()


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
        p.new("gen~ @gen ../gen/ev_powertrain.gendsp", 220, 395, 250, numinlets=1, numoutlets=2),
        p.new("gen~ @gen ../gen/v12_powertrain.gendsp", 510, 395, 260, numinlets=1, numoutlets=2),
        p.new("gen~ @gen ../gen/v10_powertrain.gendsp", 800, 395, 260, numinlets=1, numoutlets=2),
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
    tonal_controls: dict[str, str] = {}
    for index, name in enumerate(tonal_names):
        low, high = bounds[name]
        x = 35 + index * 160
        bounded = p.new(f"clip {low:g} {high:g}", x, 175, 90, numinlets=3, numoutlets=1)
        tonal_controls[name] = bounded
        named = p.message(f"{name} $1", x, 220, 105)
        p.connect(router, bounded, index)
        p.connect(bounded, named)
        for gen in gens:
            p.connect(named, gen)
        if name in {"rpm", "throttle"}:
            p.connect(named, ev_pad)

    fuel_cutoff = p.new(
        "expr 2600.+5200.*max(0.,min(1.,($f1-800.)/8200.))+600.*$f2",
        430,
        255,
        390,
        numinlets=2,
        numoutlets=1,
    )
    fuel_cutoff_pack = p.new("pack 0. 80", 835, 255, 85, numinlets=2, numoutlets=1)
    fuel_cutoff_line = p.new("line~", 935, 255, 50, numinlets=2, numoutlets=2)
    fuel_cutoff_default = p.new("loadmess 3000", 1000, 255, 105, numinlets=1, numoutlets=1)
    p.connect(tonal_controls["rpm"], fuel_cutoff, 0, 0)
    p.connect(tonal_controls["brightness"], fuel_cutoff, 0, 1)
    p.connect(fuel_cutoff, fuel_cutoff_pack)
    p.connect(fuel_cutoff_pack, fuel_cutoff_line)
    p.connect(fuel_cutoff_default, fuel_cutoff_pack)

    fuel_filtered: dict[int, list[str]] = {}
    for gen_index in (1, 2):
        filtered_channels: list[str] = []
        for channel in (0, 1):
            fuel_filter = p.new(
                "svf~ 3000 0.65",
                465 + gen_index * 285 + channel * 100,
                435,
                105,
                numinlets=3,
                numoutlets=4,
            )
            p.connect(gens[gen_index], fuel_filter, channel, 0)
            p.connect(fuel_cutoff_line, fuel_filter, 0, 1)
            filtered_channels.append(fuel_filter)
        fuel_filtered[gen_index] = filtered_channels

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
            p.connect(fuel_filtered[index][0], left_mult, 0, 0)
            p.connect(fuel_filtered[index][1], right_mult, 0, 0)
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


def _sum_signal_chain(
    patch: Patcher, sources: list[tuple[str, int]], x: float, y: float
) -> str:
    """Return a binary +~ chain for a non-empty list of signal outlets."""
    if not sources:
        raise ValueError("signal chain needs at least one source")
    current, outlet_index = sources[0]
    if len(sources) == 1 and outlet_index == 0:
        return current
    for index, (source, source_outlet) in enumerate(sources[1:]):
        add = patch.new("+~", x + (index % 5) * 58, y + (index // 5) * 35, 35, numinlets=2, numoutlets=1)
        patch.connect(current, add, outlet_index, 0)
        patch.connect(source, add, source_outlet, 1)
        current, outlet_index = add, 0
    return current


def make_tracked_texture_renderer(profile: str) -> dict[str, Any]:
    """Render one low-cost CC0 anchor bank without any local Ferrari dependency."""
    p = Patcher(1500, 780)
    p.comment(f"{profile.upper()} tracked CC0 texture fallback — six asynchronous firing-rate anchors", 25, 15, 900)
    control = inlet(p, 35, 65)
    names = (
        "rpm", "throttle", "engine_running", "reference_texture_level_db", "reference_texture_mute"
    )
    router = route(p, names, 35, 105, 575)
    p.connect(control, router)
    rpm = p.new("clip 0. 10000.", 35, 155, 105, numinlets=3, numoutlets=1)
    throttle = p.new("clip 0. 1.", 155, 155, 75, numinlets=3, numoutlets=1)
    cylinders_per_rev = 5.0 if profile == "v10" else 6.0
    firing = p.new(f"expr max(30.,min(850.,($f1/60.)*{cylinders_per_rev:g}))", 245, 155, 285, numinlets=1, numoutlets=1)
    p.connect(router, rpm, 0)
    p.connect(router, throttle, 1)
    p.connect(rpm, firing)

    anchors = (("065", 65.0, 45.0), ("110", 110.0, 70.0), ("180", 180.0, 85.0),
               ("260", 260.0, 120.0), ("380", 380.0, 150.0), ("520", 520.0, 170.0))
    channels: list[list[tuple[str, int]]] = [[], []]
    for index, (name, anchor, width) in enumerate(anchors):
        x = 35 + (index % 3) * 470
        y = 235 + (index // 3) * 220
        buffer = p.new(f"buffer~ cc0_{profile}_{name} ../media/engine_texture_{name}_a.wav", x, y, 350, numinlets=2, numoutlets=2)
        speed = p.new(f"expr max(.9,min(1.1,$f1/{anchor:g}.))", x, y + 35, 220, numinlets=1, numoutlets=1)
        speed_pack = p.new("pack 0. 100", x, y + 70, 90, numinlets=2, numoutlets=1)
        speed_line = p.new("line~", x + 105, y + 70, 50, numinlets=2, numoutlets=2)
        groove = p.new(f"groove~ cc0_{profile}_{name} 2 @loop 1", x, y + 105, 245, numinlets=3, numoutlets=3)
        weight = p.new(f"expr sqrt(max(0.,1.-abs($f1-{anchor:g})/{width:g}))", x + 250, y + 35, 210, numinlets=1, numoutlets=1)
        weight_pack = p.new("pack 0. 100", x + 250, y + 70, 90, numinlets=2, numoutlets=1)
        weight_line = p.new("line~", x + 355, y + 70, 50, numinlets=2, numoutlets=2)
        p.connect(firing, speed)
        p.connect(speed, speed_pack)
        p.connect(speed_pack, speed_line)
        p.connect(speed_line, groove)
        p.connect(firing, weight)
        p.connect(weight, weight_pack)
        p.connect(weight_pack, weight_line)
        for channel in (0, 1):
            gain = p.new("*~", x + channel * 70, y + 150, 40, numinlets=2, numoutlets=1)
            p.connect(groove, gain, channel, 0)
            p.connect(weight_line, gain, 0, 1)
            channels[channel].append((gain, 0))

    sums = [
        _sum_signal_chain(p, channels[0], 420, 650),
        _sum_signal_chain(p, channels[1], 790, 650),
    ]
    running = p.new("clip 0. 1.", 650, 155, 75, numinlets=3, numoutlets=1)
    load_gain = p.new("expr 0.72+0.45*$f1", 740, 155, 145, numinlets=1, numoutlets=1)
    combined = p.new("* 1.", 900, 155, 45, numinlets=2, numoutlets=1)
    gate_pack = p.new("pack 0. 100", 950, 155, 90, numinlets=2, numoutlets=1)
    gate_line = p.new("line~", 1055, 155, 50, numinlets=2, numoutlets=2)
    p.connect(router, running, 2)
    p.connect(throttle, load_gain)
    p.connect(running, combined, 0, 0)
    p.connect(load_gain, combined, 0, 1)
    p.connect(combined, gate_pack)
    p.connect(gate_pack, gate_line)
    level = add_db_gain_control(p, router, 3, 1120, 155, -12.0)
    mute = p.new("clip 0 1", 1300, 155, 65, numinlets=3, numoutlets=1)
    mute_gain = p.new("expr 1-$i1", 1375, 155, 80, numinlets=1, numoutlets=1)
    mute_pack = p.new("pack 0. 40", 1300, 195, 85, numinlets=2, numoutlets=1)
    mute_line = p.new("line~", 1400, 195, 50, numinlets=2, numoutlets=2)
    mute_default = p.new("loadmess 0", 1300, 235, 80, numinlets=1, numoutlets=1)
    p.connect(router, mute, 4)
    p.connect(mute_default, mute)
    p.connect(mute, mute_gain)
    p.connect(mute_gain, mute_pack)
    p.connect(mute_pack, mute_line)
    outputs: list[str] = []
    for channel, source in enumerate(sums):
        x = 570 + channel * 300
        gate_gain = p.new("*~", x, 690, 40, numinlets=2, numoutlets=1)
        level_gain = p.new("*~", x + 55, 690, 40, numinlets=2, numoutlets=1)
        mute_stage = p.new("*~", x + 110, 690, 40, numinlets=2, numoutlets=1)
        p.connect(source, gate_gain)
        p.connect(gate_line, gate_gain, 0, 1)
        p.connect(gate_gain, level_gain)
        p.connect(level, level_gain, 0, 1)
        p.connect(level_gain, mute_stage)
        p.connect(mute_line, mute_stage, 0, 1)
        outputs.append(mute_stage)
    left = outlet(p, 650, 745, signal=True)
    right = outlet(p, 950, 745, signal=True)
    p.connect(outputs[0], left)
    p.connect(outputs[1], right)
    return p.document()


def make_v10_state_renderer() -> dict[str, Any]:
    """State/RPM-index the local V10 atlas and equal-power fallback to tracked CC0."""
    p = Patcher(2680, 1350)
    p.comment("V10 local state atlas — steady/accel/decel, six RPM anchors, optional clean-checkout fallback", 25, 15, 1100)
    control = inlet(p, 35, 65)
    names = ("rpm", "accel", "throttle", "engine_running", "reference_texture_level_db", "reference_texture_mute")
    router = route(p, names, 35, 105, 650)
    p.connect(control, router)
    rpm = p.new("clip 0. 10000.", 35, 155, 105, numinlets=3, numoutlets=1)
    firing = p.new("expr max(30.,min(850.,$f1/12.))", 155, 155, 220, numinlets=1, numoutlets=1)
    accel = p.new("clip -1. 1.", 395, 155, 85, numinlets=3, numoutlets=1)
    accel_default = p.new("loadmess 0.", 395, 195, 85, numinlets=1, numoutlets=1)
    p.connect(router, rpm, 0)
    p.connect(rpm, firing)
    p.connect(router, accel, 1)
    p.connect(accel_default, accel)

    state_exprs = {
        "steady": "expr sqrt(max(0.,1.-abs($f1)))",
        "accel": "expr sqrt(max(0.,$f1))",
        "decel": "expr sqrt(max(0.,-$f1))",
    }
    state_lines: dict[str, str] = {}
    for index, state in enumerate(("steady", "accel", "decel")):
        x = 505 + index * 245
        expression = p.new(state_exprs[state], x, 155, 205, numinlets=1, numoutlets=1)
        packed = p.new("pack 0. 120", x, 195, 90, numinlets=2, numoutlets=1)
        line = p.new("line~", x + 105, 195, 50, numinlets=2, numoutlets=2)
        p.connect(accel, expression)
        p.connect(expression, packed)
        p.connect(packed, line)
        state_lines[state] = line

    local_loaded = p.message("1", 2380, 105, 30)
    local_timer = p.new("qmetro 100", 1260, 105, 80, numinlets=2, numoutlets=1)
    local_timer_on = p.new("loadmess 1", 1260, 145, 80, numinlets=1, numoutlets=1)
    local_counter = p.new("counter 0 30", 1350, 145, 90, numinlets=5, numoutlets=4)
    local_timeout = p.new("sel 30", 1450, 145, 50, numinlets=1, numoutlets=2)
    readiness = p.new("pak " + " ".join("0" for _ in range(18)), 1930, 210, 330, numinlets=18, numoutlets=1)
    readiness_sum = p.new("zl sum", 2275, 210, 55, numinlets=2, numoutlets=2)
    local_ready = p.new("sel 18", 2345, 210, 50, numinlets=1, numoutlets=2)
    local_timer_off = p.message("0", 1510, 145, 30)
    local_gain_expr = p.new("expr sqrt(max(0.,min(1.,$f1)))", 2415, 105, 220, numinlets=1, numoutlets=1)
    fallback_gain_expr = p.new("expr sqrt(max(0.,min(1.,1.-$f1)))", 2415, 145, 235, numinlets=1, numoutlets=1)
    local_gain_line = p.new("sig~ 0.", 2530, 105, 60, numinlets=1, numoutlets=1)
    fallback_gain_line = p.new("sig~ 1.", 2530, 145, 60, numinlets=1, numoutlets=1)
    fallback_default = p.new("loadmess 0.", 2415, 180, 85, numinlets=1, numoutlets=1)
    p.connect(local_timer_on, local_timer)
    p.connect(local_timer, local_counter)
    p.connect(local_counter, local_timeout)
    p.connect(local_timeout, local_timer_off, 0)
    for index, state in enumerate(("steady", "accel", "decel")):
        for anchor_index, anchor in enumerate((65, 110, 180, 260, 380, 520)):
            item_index = index * 6 + anchor_index
            x = 1435 + anchor_index * 190
            y = 35 + index * 55
            info = p.new(
                f"info~ v10_{state}_{anchor:03d}", x, y, 165,
                numinlets=1, numoutlets=10,
            )
            present = p.new("expr $f1>500.", x, y + 28, 105, numinlets=1, numoutlets=1)
            p.connect(local_timer, info)
            p.connect(info, present, 6, 0)
            p.connect(present, readiness, 0, item_index)
    p.connect(readiness, readiness_sum)
    p.connect(readiness_sum, local_ready)
    p.connect(local_ready, local_loaded, 0)
    p.connect(local_ready, local_timer_off, 0)
    p.connect(local_timer_off, local_timer)
    p.connect(local_loaded, local_gain_expr)
    p.connect(local_loaded, fallback_gain_expr)
    p.connect(local_gain_expr, local_gain_line)
    p.connect(fallback_gain_expr, fallback_gain_line)
    p.connect(fallback_default, fallback_gain_expr)

    anchors = ((65, 45.0), (110, 70.0), (180, 85.0), (260, 120.0), (380, 150.0), (520, 170.0))
    state_channels: dict[str, list[list[tuple[str, int]]]] = {
        state: [[], []] for state in ("steady", "accel", "decel")
    }
    for state_index, state in enumerate(("steady", "accel", "decel")):
        for anchor_index, (anchor, width) in enumerate(anchors):
            x = 35 + anchor_index * 380
            y = 270 + state_index * 260
            buffer_name = f"v10_{state}_{anchor:03d}"
            filename = f"../media/local/ferrari_v10_{state}_{anchor:03d}.wav"
            p.new(f"buffer~ {buffer_name} {filename}", x, y, 355, numinlets=2, numoutlets=2)
            speed = p.new(f"expr max(.88,min(1.12,$f1/{anchor:g}.))", x, y + 40, 235, numinlets=1, numoutlets=1)
            speed_pack = p.new("pack 0. 100", x, y + 75, 90, numinlets=2, numoutlets=1)
            speed_line = p.new("line~", x + 105, y + 75, 50, numinlets=2, numoutlets=2)
            groove = p.new(f"groove~ {buffer_name} 2 @loop 1", x, y + 110, 225, numinlets=3, numoutlets=3)
            weight = p.new(f"expr sqrt(max(0.,1.-abs($f1-{anchor:g})/{width:g}))", x, y + 150, 260, numinlets=1, numoutlets=1)
            weight_pack = p.new("pack 0. 100", x + 270, y + 150, 90, numinlets=2, numoutlets=1)
            weight_line = p.new("line~", x + 270, y + 185, 50, numinlets=2, numoutlets=2)
            p.connect(firing, speed)
            p.connect(speed, speed_pack)
            p.connect(speed_pack, speed_line)
            p.connect(speed_line, groove)
            p.connect(firing, weight)
            p.connect(weight, weight_pack)
            p.connect(weight_pack, weight_line)
            for channel in (0, 1):
                anchor_gain = p.new("*~", x + channel * 70, y + 210, 40, numinlets=2, numoutlets=1)
                p.connect(groove, anchor_gain, channel, 0)
                p.connect(weight_line, anchor_gain, 0, 1)
                state_channels[state][channel].append((anchor_gain, 0))

    state_sums: dict[str, list[str]] = {}
    for state_index, state in enumerate(("steady", "accel", "decel")):
        state_sums[state] = []
        for channel in (0, 1):
            summed = _sum_signal_chain(p, state_channels[state][channel], 420 + channel * 500, 1060 + state_index * 35)
            weighted = p.new("*~", 1180 + state_index * 100 + channel * 360, 1040, 40, numinlets=2, numoutlets=1)
            p.connect(summed, weighted)
            p.connect(state_lines[state], weighted, 0, 1)
            state_sums[state].append(weighted)

    local_sums = []
    for channel in (0, 1):
        local_sums.append(
            _sum_signal_chain(
                p,
                [(state_sums[state][channel], 0) for state in ("steady", "accel", "decel")],
                1450 + channel * 250,
                1110,
            )
        )
    throttle = p.new("clip 0. 1.", 35, 1125, 75, numinlets=3, numoutlets=1)
    running = p.new("clip 0. 1.", 125, 1125, 75, numinlets=3, numoutlets=1)
    load_gain = p.new("expr 0.74+0.42*$f1", 215, 1125, 145, numinlets=1, numoutlets=1)
    gate_product = p.new("* 1.", 375, 1125, 45, numinlets=2, numoutlets=1)
    gate_pack = p.new("pack 0. 100", 425, 1125, 90, numinlets=2, numoutlets=1)
    gate_line = p.new("line~", 530, 1125, 50, numinlets=2, numoutlets=2)
    p.connect(router, throttle, 2)
    p.connect(router, running, 3)
    p.connect(throttle, load_gain)
    p.connect(running, gate_product, 0, 0)
    p.connect(load_gain, gate_product, 0, 1)
    p.connect(gate_product, gate_pack)
    p.connect(gate_pack, gate_line)
    level = add_db_gain_control(p, router, 4, 1760, 1120, -6.0)
    mute = p.new("clip 0 1", 1950, 1120, 65, numinlets=3, numoutlets=1)
    mute_gain = p.new("expr 1-$i1", 2025, 1120, 80, numinlets=1, numoutlets=1)
    mute_pack = p.new("pack 0. 40", 2115, 1120, 85, numinlets=2, numoutlets=1)
    mute_line = p.new("line~", 2215, 1120, 50, numinlets=2, numoutlets=2)
    mute_default = p.new("loadmess 0", 1950, 1160, 80, numinlets=1, numoutlets=1)
    p.connect(router, mute, 5)
    p.connect(mute_default, mute)
    p.connect(mute, mute_gain)
    p.connect(mute_gain, mute_pack)
    p.connect(mute_pack, mute_line)
    shaped_local: list[str] = []
    for channel, source in enumerate(local_sums):
        x = 1240 + channel * 300
        gate_stage = p.new("*~", x, 1160, 40, numinlets=2, numoutlets=1)
        level_stage = p.new("*~", x + 55, 1160, 40, numinlets=2, numoutlets=1)
        mute_stage = p.new("*~", x + 110, 1160, 40, numinlets=2, numoutlets=1)
        p.connect(source, gate_stage)
        p.connect(gate_line, gate_stage, 0, 1)
        p.connect(gate_stage, level_stage)
        p.connect(level, level_stage, 0, 1)
        p.connect(level_stage, mute_stage)
        p.connect(mute_line, mute_stage, 0, 1)
        shaped_local.append(mute_stage)
    fallback = p.new("v10_fallback_renderer~", 35, 1170, 170, numinlets=1, numoutlets=2)
    p.connect(control, fallback)
    final_sources: list[str] = []
    for channel in (0, 1):
        x = 610 + channel * 420
        local_stage = p.new("*~", x, 1190, 40, numinlets=2, numoutlets=1)
        fallback_stage = p.new("*~", x + 90, 1190, 40, numinlets=2, numoutlets=1)
        total = p.new("+~", x + 45, 1240, 40, numinlets=2, numoutlets=1)
        p.connect(shaped_local[channel], local_stage)
        p.connect(local_gain_line, local_stage, 0, 1)
        p.connect(fallback, fallback_stage, channel, 0)
        p.connect(fallback_gain_line, fallback_stage, 0, 1)
        p.connect(local_stage, total, 0, 0)
        p.connect(fallback_stage, total, 0, 1)
        final_sources.append(total)
    left = outlet(p, 700, 1305, signal=True)
    right = outlet(p, 1120, 1305, signal=True)
    p.connect(final_sources[0], left)
    p.connect(final_sources[1], right)
    return p.document()


def make_reference_texture() -> dict[str, Any]:
    """Build the superseded V4 reference renderer for offline comparison only."""
    p = Patcher(2300, 1080)
    p.comment("OFFLINE V4 ARCHIVE — never declared or loaded by a V5 runtime", 25, 15, 1050)
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
    gate_product = p.new("* 1.", 1340, 155, 45, numinlets=2, numoutlets=1)
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

    level = add_db_gain_control(p, router, 4, 1570, 155, -18.0)
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
        buffer_a = p.new(f"buffer~ tex_{name}_a ../media/engine_texture_{name}_a.wav", x, 245, 330, numinlets=2, numoutlets=2)
        buffer_b = p.new(f"buffer~ tex_{name}_b ../media/engine_texture_{name}_b.wav", x, 280, 330, numinlets=2, numoutlets=2)
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

    local_buffer = p.new(
        "buffer~ ferrari_idle_body ../media/local/ferrari_sf90_idle_body.wav",
        35,
        700,
        390,
        numinlets=2,
        numoutlets=2,
    )
    local_speed = p.new(
        "expr max(.85,min(2.93,$f1/61.5))",
        445,
        700,
        225,
        numinlets=1,
        numoutlets=1,
    )
    local_speed_pack = p.new("pack 0. 120", 685, 700, 90, numinlets=2, numoutlets=1)
    local_speed_line = p.new("line~", 790, 700, 50, numinlets=2, numoutlets=2)
    local_groove = p.new(
        "groove~ ferrari_idle_body 2 @loop 1",
        855,
        700,
        245,
        numinlets=3,
        numoutlets=3,
    )
    local_weight = p.new(
        "expr sqrt(max(0.,min(1.,(180.-$f1)/80.)))",
        1120,
        700,
        280,
        numinlets=1,
        numoutlets=1,
    )
    local_weight_pack = p.new("pack 0. 120", 1415, 700, 90, numinlets=2, numoutlets=1)
    local_weight_line = p.new("line~", 1520, 700, 50, numinlets=2, numoutlets=2)
    p.connect(firing, local_speed)
    p.connect(local_speed, local_speed_pack)
    p.connect(local_speed_pack, local_speed_line)
    p.connect(local_speed_line, local_groove)
    p.connect(firing, local_weight)
    p.connect(local_weight, local_weight_pack)
    p.connect(local_weight_pack, local_weight_line)

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
        local_gain = p.new("*~", x + 150, 805, 40, numinlets=2, numoutlets=1)
        local_trim = p.new("*~ 1.4", x + 205, 805, 65, numinlets=2, numoutlets=1)
        texture_sum = p.new("+~", x + 285, 840, 40, numinlets=2, numoutlets=1)
        load_gain = p.new("*~", x + 340, 840, 40, numinlets=2, numoutlets=1)
        life_gain = p.new("*~", x + 395, 840, 40, numinlets=2, numoutlets=1)
        level_gain = p.new("*~", x + 450, 840, 40, numinlets=2, numoutlets=1)
        mute_stage = p.new("*~", x + 505, 840, 40, numinlets=2, numoutlets=1)
        p.connect(layer_sum, bank_trim)
        p.connect(local_groove, local_gain, channel, 0)
        p.connect(local_weight_line, local_gain, 0, 1)
        p.connect(local_gain, local_trim)
        p.connect(bank_trim, texture_sum, 0, 0)
        p.connect(local_trim, texture_sum, 0, 1)
        p.connect(texture_sum, load_gain, 0, 0)
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


def make_engine_start_beap() -> dict[str, Any]:
    """Seed one editable crank/first-fire/catch voice with a Max-safe envelope."""
    p = Patcher(2050, 790)
    p.comment(
        "USER-TUNABLE CINEMATIC ENGINE START — crank / first fire / catch; preserved on rebuild",
        25, 15, 1100,
    )
    pitch = inlet(p, 45, 65, signal=True)
    gate = inlet(p, 145, 65, signal=True)
    timbre = inlet(p, 245, 65, signal=True)

    p.comment("CRANK MOTOR — filtered pressure pulses; no starter sample", 25, 110, 650)
    noise = add_beap_module(p, "Random/bp.Noise.maxpat", 25, 145, "Start_Noise")
    osc = add_beap_module(
        p, "Oscillator/bp.Oscillator.maxpat", 300, 145, "Start_Osc",
        initial={"Waveform": 0},
    )
    mixer = add_beap_module(
        p, "Mixers/bp.Audio Mixer.maxpat", 625, 145, "Start_Mixer",
        initial={"in1": -8, "in2": -24},
    )
    start_filter = add_beap_module(
        p, "Filter/bp.MMF.maxpat", 845, 145, "Start_Filter",
        initial={"Freq": 900, "Res": 4, "FilterType": 0, "power[1]": 1},
    )
    envelope = add_beap_module(
        p, "Envelope/bp.AD.maxpat", 1120, 145, "Start_AD",
        initial={"Attack": 4, "Decay": 1050},
    )
    vca = add_beap_module(p, "Level/bp.VCA.maxpat", 1320, 145, "Start_VCA")
    native_env = p.new("*~ 0.55", 1135, 360, 65, numinlets=2, numoutlets=1)

    # The visible BEAP Mixer/MMF is the authoritative tone source. A simple
    # signal-rate crank envelope bypasses only BEAP AD/VCA timing because some
    # supported Max 8.6.x revisions miss a gate delivered on the first unmute
    # vector. This guarantees audibility without hiding a second oscillator.
    crank_rate = p.new("scale~ -1.5 0.75 8. 23.", 35, 400, 165, numinlets=6, numoutlets=1)
    crank_phase = p.new("phasor~", 210, 400, 60, numinlets=2, numoutlets=1)
    crank_edge = p.new(">~ 0.54", 280, 400, 65, numinlets=2, numoutlets=1)
    crank_pulse = p.new("onepole~ 95", 355, 400, 95, numinlets=2, numoutlets=1)
    gate_normal = p.new("*~ 0.2", 460, 400, 65, numinlets=2, numoutlets=1)
    gate_clip = p.new("clip~ 0. 1.", 535, 400, 85, numinlets=3, numoutlets=1)
    pulse_env = p.new("*~", 630, 400, 40, numinlets=2, numoutlets=1)
    crank_source = p.new("*~", 680, 400, 40, numinlets=2, numoutlets=1)
    crank_body = p.new("lores~ 620 0.68", 730, 400, 115, numinlets=3, numoutlets=1)
    crank_mode = p.new("reson~ 3.2 92 3.8", 855, 400, 120, numinlets=4, numoutlets=1)
    crank_sum = p.new("+~", 985, 400, 40, numinlets=2, numoutlets=1)

    p.comment("FIRST FIRE / CATCH — broad exhaust bloom, restrained crack", 25, 485, 720)
    catch_filter = p.new("svf~ 1050 0.72", 355, 520, 110, numinlets=3, numoutlets=4)
    catch_colour = p.new("*~ 0.035", 475, 520, 70, numinlets=2, numoutlets=1)
    catch_colour_clip = p.new("clip~ 0. 0.2", 555, 520, 100, numinlets=3, numoutlets=1)
    catch_gate = p.new("*~", 665, 520, 40, numinlets=2, numoutlets=1)
    catch_vca = p.new("*~", 715, 520, 40, numinlets=2, numoutlets=1)
    native_sum = p.new("+~", 1040, 430, 40, numinlets=2, numoutlets=1)
    body_catch_sum = p.new("+~", 1090, 450, 40, numinlets=2, numoutlets=1)

    p.comment("OUTPUT — soft pressure saturation; bass centered below 160 Hz", 1050, 485, 760)
    drive = p.new("*~ 1.8", 1160, 540, 65, numinlets=2, numoutlets=1)
    soft_clip = p.new("tanh~", 1235, 540, 50, numinlets=1, numoutlets=1)
    split = p.new("svf~ 160 0.7", 1295, 540, 100, numinlets=3, numoutlets=4)
    left_air = p.new("lores~ 3600 0.58", 1410, 525, 120, numinlets=3, numoutlets=1)
    right_air = p.new("lores~ 4100 0.54", 1410, 580, 120, numinlets=3, numoutlets=1)
    left_mix = p.new("+~", 1540, 525, 40, numinlets=2, numoutlets=1)
    right_mix = p.new("+~", 1540, 580, 40, numinlets=2, numoutlets=1)
    left = outlet(p, 1610, 525, signal=True)
    right = outlet(p, 1610, 580, signal=True)

    p.connect(noise, mixer, 0, 0)
    p.connect(pitch, osc, 0, 0)
    p.connect(osc, mixer, 0, 1)
    p.connect(mixer, start_filter, 0, 0)
    p.connect(timbre, start_filter, 0, 1)
    p.connect(gate, envelope, 0, 0)
    p.connect(envelope, native_env)
    p.connect(start_filter, vca, 0, 0)
    p.connect(native_env, vca, 0, 1)

    p.connect(pitch, crank_rate)
    p.connect(crank_rate, crank_phase)
    p.connect(crank_phase, crank_edge)
    p.connect(crank_edge, crank_pulse)
    p.connect(gate, gate_normal)
    p.connect(gate_normal, gate_clip)
    p.connect(crank_pulse, pulse_env, 0, 0)
    p.connect(gate_clip, pulse_env, 0, 1)
    p.connect(start_filter, crank_source, 0, 0)
    p.connect(pulse_env, crank_source, 0, 1)
    p.connect(crank_source, crank_body)
    p.connect(crank_source, crank_mode)
    p.connect(crank_body, crank_sum, 0, 0)
    p.connect(crank_mode, crank_sum, 0, 1)

    p.connect(start_filter, catch_filter, 0, 0)
    p.connect(timbre, catch_colour)
    p.connect(catch_colour, catch_colour_clip)
    p.connect(catch_filter, catch_gate, 2, 0)
    p.connect(gate_clip, catch_gate, 0, 1)
    p.connect(catch_gate, catch_vca, 0, 0)
    p.connect(catch_colour_clip, catch_vca, 0, 1)
    p.connect(vca, native_sum, 0, 0)
    p.connect(crank_sum, native_sum, 0, 1)
    p.connect(native_sum, body_catch_sum, 0, 0)
    p.connect(catch_vca, body_catch_sum, 0, 1)
    p.connect(body_catch_sum, drive)
    p.connect(drive, soft_clip)
    p.connect(soft_clip, split)
    p.connect(split, left_mix, 0, 0)
    p.connect(split, right_mix, 0, 0)
    p.connect(split, left_air, 1, 0)
    p.connect(split, right_air, 1, 0)
    p.connect(left_air, left_mix, 0, 1)
    p.connect(right_air, right_mix, 0, 1)
    p.connect(left_mix, left)
    p.connect(right_mix, right)
    return p.document()


def make_engine_start_voice() -> dict[str, Any]:
    p = Patcher(620, 360)
    p.comment("Cinematic starter poly voice — host suspends DSP after the cue", 20, 15, 500)
    pitch = p.new("in~ 1", 35, 65, 45, numinlets=0, numoutlets=1)
    gate_cv = p.new("in~ 2", 125, 65, 45, numinlets=0, numoutlets=1)
    timbre = p.new("in~ 3", 215, 65, 45, numinlets=0, numoutlets=1)
    beap = p.new("engine_start_beap~", 120, 135, 150, numinlets=3, numoutlets=2)
    p.new("thispoly~", 390, 135, 70, numinlets=2, numoutlets=3)
    left = p.new("out~ 1", 90, 265, 50, numinlets=1, numoutlets=0)
    right = p.new("out~ 2", 260, 265, 50, numinlets=1, numoutlets=0)
    p.connect(pitch, beap, 0, 0)
    p.connect(gate_cv, beap, 0, 1)
    p.connect(timbre, beap, 0, 2)
    p.connect(beap, left, 0)
    p.connect(beap, right, 1)
    return p.document()


def make_engine_start_core() -> dict[str, Any]:
    """Always-audible procedural crank and first-fire core behind the start seam."""
    p = Patcher(1120, 650)
    p.comment(
        "ENGINE START CORE — generated crank pressure / first fire; tone layer remains in BEAP",
        20, 15, 820,
    )
    pitch = inlet(p, 35, 65, signal=True)
    gate = inlet(p, 125, 65, signal=True)
    timbre = inlet(p, 215, 65, signal=True)
    rate = p.new("scale~ -1.5 0.75 8. 23.", 35, 115, 165, numinlets=6, numoutlets=1)
    phase = p.new("phasor~", 210, 115, 60, numinlets=2, numoutlets=1)
    edge = p.new(">~ 0.54", 280, 115, 65, numinlets=2, numoutlets=1)
    pulse = p.new("onepole~ 95", 355, 115, 95, numinlets=2, numoutlets=1)
    gate_clip = p.new("clip~ 0. 1.", 535, 115, 85, numinlets=3, numoutlets=1)
    pulse_env = p.new("*~", 630, 115, 40, numinlets=2, numoutlets=1)
    pulse_depth = p.new("*~ 0.65", 680, 115, 65, numinlets=2, numoutlets=1)
    gate_base = p.new("*~ 0.35", 755, 115, 65, numinlets=2, numoutlets=1)
    start_env = p.new("+~", 830, 115, 40, numinlets=2, numoutlets=1)
    noise = p.new("noise~", 35, 180, 55, numinlets=1, numoutlets=1)
    pressure = p.new("*~", 100, 180, 40, numinlets=2, numoutlets=1)
    body = p.new("lores~ 620 0.68", 150, 180, 115, numinlets=3, numoutlets=1)
    chamber = p.new("reson~ 3.2 92 3.8", 275, 180, 120, numinlets=4, numoutlets=1)
    body_sum = p.new("+~", 405, 180, 40, numinlets=2, numoutlets=1)
    catch_filter = p.new("svf~ 1050 0.72", 150, 235, 110, numinlets=3, numoutlets=4)
    catch_colour = p.new("*~ 0.032", 275, 235, 70, numinlets=2, numoutlets=1)
    catch_clip = p.new("clip~ 0. 0.18", 355, 235, 105, numinlets=3, numoutlets=1)
    catch_gate = p.new("*~", 470, 235, 40, numinlets=2, numoutlets=1)
    catch_vca = p.new("*~", 520, 235, 40, numinlets=2, numoutlets=1)
    start_sum = p.new("+~", 570, 200, 40, numinlets=2, numoutlets=1)
    drive = p.new("*~ 2.1", 620, 200, 65, numinlets=2, numoutlets=1)
    soft_clip = p.new("tanh~", 695, 200, 50, numinlets=1, numoutlets=1)
    infra_cut = p.new("svf~ 28 0.7", 755, 160, 95, numinlets=3, numoutlets=4)
    split = p.new("svf~ 160 0.7", 755, 200, 100, numinlets=3, numoutlets=4)
    left_air = p.new("lores~ 3400 0.58", 870, 185, 120, numinlets=3, numoutlets=1)
    right_air = p.new("lores~ 3900 0.54", 870, 240, 120, numinlets=3, numoutlets=1)
    left_mix = p.new("+~", 1000, 185, 40, numinlets=2, numoutlets=1)
    right_mix = p.new("+~", 1000, 240, 40, numinlets=2, numoutlets=1)
    left = outlet(p, 1060, 185, signal=True)
    right = outlet(p, 1060, 240, signal=True)
    p.connect(pitch, rate)
    p.connect(rate, phase)
    p.connect(phase, edge)
    p.connect(edge, pulse)
    p.connect(gate, gate_clip)
    p.connect(pulse, pulse_env, 0, 0)
    p.connect(gate_clip, pulse_env, 0, 1)
    p.connect(pulse_env, pulse_depth)
    p.connect(gate_clip, gate_base)
    p.connect(pulse_depth, start_env, 0, 0)
    p.connect(gate_base, start_env, 0, 1)
    p.connect(noise, pressure, 0, 0)
    p.connect(start_env, pressure, 0, 1)
    p.connect(pressure, body)
    p.connect(pressure, chamber)
    p.connect(body, body_sum, 0, 0)
    p.connect(chamber, body_sum, 0, 1)
    p.connect(pressure, catch_filter)
    p.connect(timbre, catch_colour)
    p.connect(catch_colour, catch_clip)
    p.connect(catch_filter, catch_gate, 2, 0)
    p.connect(gate_clip, catch_gate, 0, 1)
    p.connect(catch_gate, catch_vca, 0, 0)
    p.connect(catch_clip, catch_vca, 0, 1)
    p.connect(body_sum, start_sum, 0, 0)
    p.connect(catch_vca, start_sum, 0, 1)
    p.connect(start_sum, drive)
    p.connect(drive, soft_clip)
    p.connect(soft_clip, infra_cut)
    p.connect(infra_cut, split, 1, 0)
    p.connect(split, left_mix, 0, 0)
    p.connect(split, right_mix, 0, 0)
    p.connect(split, left_air, 1, 0)
    p.connect(split, right_air, 1, 0)
    p.connect(left_air, left_mix, 0, 1)
    p.connect(right_air, right_mix, 0, 1)
    p.connect(left_mix, left)
    p.connect(right_mix, right)
    return p.document()


def make_profile_transient(profile: str) -> dict[str, Any]:
    """Choose cinematic/realistic start and procedural profile event synthesis."""
    p = Patcher(1320, 760)
    p.comment(f"{profile.upper()} transient host — cinematic BEAP default; realistic starter option for ICE", 25, 15, 820)
    control = inlet(p, 35, 65)
    router = route(p, ("starter", "start_style"), 35, 105, 245)
    event_renderer = p.new(
        "transient~" if profile == "ev" else f"{profile}_backfire_host~",
        35, 555, 180 if profile != "ev" else 90, numinlets=1, numoutlets=2,
    )
    p.connect(control, router)
    p.connect(router, event_renderer, 2)

    starter = p.new("sel 1 0", 35, 155, 55, numinlets=1, numoutlets=3)
    style_select = p.new("sel cinematic realistic", 120, 155, 170, numinlets=1, numoutlets=3)
    style_store = p.new("int 1", 310, 155, 50, numinlets=2, numoutlets=1)
    cinematic_value = p.message("1", 120, 195, 30)
    realistic_value = p.message("2", 160, 195, 30)
    default_style = p.new("loadmess cinematic", 200, 195, 125, numinlets=1, numoutlets=1)
    start_style_gate = p.new("sel 1 2", 310, 195, 55, numinlets=1, numoutlets=3)
    p.connect(router, starter, 0)
    p.connect(router, style_select, 1)
    p.connect(default_style, style_select)
    p.connect(style_select, cinematic_value, 0)
    p.connect(style_select, realistic_value, 1)
    p.connect(cinematic_value, style_store, 0, 1)
    p.connect(realistic_value, style_store, 0, 1)
    p.connect(starter, style_store, 0)
    p.connect(style_store, start_style_gate)
    p.comment("starter state directly owns the procedural gate; style gain prevents cross-mode residue", 365, 155, 520)
    starter_state_clip = p.new("clip 0. 1.", 835, 155, 75, numinlets=3, numoutlets=1)
    starter_state_signal = p.new(
        "sig~ 0.", 920, 155, 60, numinlets=1, numoutlets=1,
        varname="starter_state_gate",
    )
    starter_state_smooth = p.new("rampsmooth~ 64 256", 990, 155, 125, numinlets=3, numoutlets=1)
    p.connect(router, starter_state_clip, 0)
    p.connect(starter_state_clip, starter_state_signal)
    p.connect(starter_state_signal, starter_state_smooth)
    cinematic_gain_value = p.message("1. 15", 365, 180, 45)
    realistic_gain_value = p.message("0. 15", 415, 180, 45)
    start_cinematic_gain = p.new(
        "line~ 1.", 465, 180, 65, numinlets=2, numoutlets=2,
        varname="start_cinematic_gain",
    )
    p.connect(cinematic_value, cinematic_gain_value)
    p.connect(realistic_value, realistic_gain_value)
    p.connect(cinematic_gain_value, start_cinematic_gain)
    p.connect(realistic_gain_value, start_cinematic_gain)

    voice = p.new("poly~ engine_start_voice 1", 390, 250, 190, numinlets=3, numoutlets=2)
    unmute = p.message("mute 1 0", 390, 195, 65)
    initial_suspend = p.new("loadmess mute 1 1", 625, 195, 125, numinlets=1, numoutlets=1)
    cinematic_order = p.new("t b b", 330, 195, 50, numinlets=1, numoutlets=2)
    envelope_delay = p.new("delay 5", 330, 225, 55, numinlets=2, numoutlets=1)
    suspend_delay = p.new("delay 1600", 465, 195, 80, numinlets=2, numoutlets=1)
    suspend = p.message("mute 1 1", 555, 195, 65)
    pitch_message = p.message("-1.25 0, 0.55 180, -0.35 850", 390, 295, 210)
    pitch_line = p.new("line~ -1.25", 390, 335, 75, numinlets=2, numoutlets=2)
    gate_message = p.message("5. 0, 0. 1000", 460, 335, 105)
    gate_line = p.new("line~", 460, 375, 50, numinlets=2, numoutlets=2)
    timbre_message = p.message("4.2 0, 1.1 900", 530, 375, 115)
    timbre_line = p.new("line~ 4.2", 530, 415, 70, numinlets=2, numoutlets=2)
    cinema_tone_l = p.new("*~ 0.18", 390, 465, 65, numinlets=2, numoutlets=1)
    cinema_tone_r = p.new("*~ 0.18", 475, 465, 65, numinlets=2, numoutlets=1)
    p.connect(start_style_gate, cinematic_order, 0)
    p.connect(cinematic_order, unmute, 1)
    p.connect(unmute, voice)
    p.connect(initial_suspend, voice)
    p.connect(cinematic_order, envelope_delay, 0)
    p.connect(envelope_delay, suspend_delay)
    p.connect(suspend_delay, suspend)
    p.connect(suspend, voice)
    for destination in (pitch_message, gate_message, timbre_message):
        p.connect(envelope_delay, destination)
    p.connect(pitch_message, pitch_line)
    p.connect(gate_message, gate_line)
    p.connect(timbre_message, timbre_line)
    p.connect(pitch_line, voice, 0, 0)
    p.connect(gate_line, voice, 0, 1)
    p.connect(timbre_line, voice, 0, 2)
    p.connect(voice, cinema_tone_l, 0, 0)
    p.connect(voice, cinema_tone_r, 1, 0)
    start_core = p.new("engine_start_core~", 390, 425, 145, numinlets=3, numoutlets=2)
    core_l = p.new("*~ 0.55", 550, 445, 65, numinlets=2, numoutlets=1)
    core_r = p.new("*~ 0.55", 550, 475, 65, numinlets=2, numoutlets=1)
    core_style_l = p.new("*~", 625, 400, 40, numinlets=2, numoutlets=1)
    core_style_r = p.new("*~", 675, 400, 40, numinlets=2, numoutlets=1)
    cinema_l = p.new("+~", 625, 445, 40, numinlets=2, numoutlets=1)
    cinema_r = p.new("+~", 625, 475, 40, numinlets=2, numoutlets=1)
    p.connect(pitch_line, start_core, 0, 0)
    p.connect(starter_state_smooth, start_core, 0, 1)
    p.connect(timbre_line, start_core, 0, 2)
    p.connect(start_core, core_l, 0, 0)
    p.connect(start_core, core_r, 1, 0)
    p.connect(core_l, core_style_l, 0, 0)
    p.connect(core_r, core_style_r, 0, 0)
    p.connect(start_cinematic_gain, core_style_l, 0, 1)
    p.connect(start_cinematic_gain, core_style_r, 0, 1)
    p.connect(cinema_tone_l, cinema_l, 0, 0)
    p.connect(core_style_l, cinema_l, 0, 1)
    p.connect(cinema_tone_r, cinema_r, 0, 0)
    p.connect(core_style_r, cinema_r, 0, 1)

    sample_l = p.new("sig~ 0.", 670, 465, 55, numinlets=1, numoutlets=1)
    sample_r = p.new("sig~ 0.", 755, 465, 55, numinlets=1, numoutlets=1)
    if profile != "ev":
        fallback_name = f"starter_{profile}"
        p.new(f"buffer~ {fallback_name} ../media/{fallback_name}.wav", 660, 250, 255, numinlets=1, numoutlets=2)
        fallback_start = p.message("start", 660, 290, 45)
        fallback_player = p.new(f"play~ {fallback_name} 1", 660, 330, 165, numinlets=1, numoutlets=2)
        fallback_filter = p.new("lores~ 1800 0.65", 660, 370, 115, numinlets=3, numoutlets=1)
        fallback_gain = p.new("*~ 0.75", 660, 415, 65, numinlets=2, numoutlets=1)
        p.connect(start_style_gate, fallback_start, 1)
        p.connect(fallback_start, fallback_player)
        p.connect(fallback_player, fallback_filter)
        p.connect(fallback_filter, fallback_gain)
        sample_l = fallback_gain
        sample_r = fallback_gain
        if profile == "v10":
            startup_check_load = p.new("loadbang", 1080, 205, 70, numinlets=1, numoutlets=1)
            startup_check_delay = p.new("delay 200", 1160, 205, 70, numinlets=2, numoutlets=1)
            startup_info = p.new("info~ ferrari_startup", 1080, 235, 145, numinlets=1, numoutlets=10)
            startup_exists = p.new("expr $f1>500.", 1080, 270, 105, numinlets=1, numoutlets=1)
            local_available_pack = p.new("pack 0. 20", 1080, 270, 85, numinlets=2, numoutlets=1)
            local_available_line = p.new("line~", 1180, 270, 50, numinlets=2, numoutlets=2)
            fallback_available = p.new("expr 1.-$f1", 1080, 305, 100, numinlets=1, numoutlets=1)
            fallback_available_pack = p.new("pack 0. 20", 1190, 305, 85, numinlets=2, numoutlets=1)
            fallback_available_line = p.new("line~", 1190, 340, 50, numinlets=2, numoutlets=2)
            fallback_selected = p.new("*~", 745, 415, 40, numinlets=2, numoutlets=1)
            p.connect(startup_check_load, startup_check_delay)
            p.connect(startup_check_delay, startup_info)
            p.connect(startup_info, startup_exists, 6)
            p.connect(startup_exists, local_available_pack)
            p.connect(local_available_pack, local_available_line)
            p.connect(startup_exists, fallback_available)
            p.connect(fallback_available, fallback_available_pack)
            p.connect(fallback_available_pack, fallback_available_line)
            p.connect(fallback_gain, fallback_selected)
            p.connect(fallback_available_line, fallback_selected, 0, 1)
            local_buffer = p.new("buffer~ ferrari_startup ../media/local/ferrari_sf90_startup.wav", 900, 250, 410, numinlets=2, numoutlets=2)
            p.connect(local_buffer, startup_info, 1)
            local_start = p.message("start", 900, 290, 45)
            local_player = p.new("play~ ferrari_startup 2", 900, 330, 175, numinlets=1, numoutlets=3)
            local_l = p.new("*~ 0.65", 900, 375, 65, numinlets=2, numoutlets=1)
            local_r = p.new("*~ 0.65", 985, 375, 65, numinlets=2, numoutlets=1)
            p.connect(start_style_gate, local_start, 1)
            p.connect(local_start, local_player)
            p.connect(local_player, local_l, 0, 0)
            p.connect(local_player, local_r, 1, 0)
            local_l_selected = p.new("*~", 900, 415, 40, numinlets=2, numoutlets=1)
            local_r_selected = p.new("*~", 985, 415, 40, numinlets=2, numoutlets=1)
            p.connect(local_l, local_l_selected)
            p.connect(local_r, local_r_selected)
            p.connect(local_available_line, local_l_selected, 0, 1)
            p.connect(local_available_line, local_r_selected, 0, 1)
            sample_l_sum = p.new("+~", 805, 465, 40, numinlets=2, numoutlets=1)
            sample_r_sum = p.new("+~", 900, 465, 40, numinlets=2, numoutlets=1)
            p.connect(fallback_selected, sample_l_sum, 0, 0)
            p.connect(local_l_selected, sample_l_sum, 0, 1)
            p.connect(fallback_selected, sample_r_sum, 0, 0)
            p.connect(local_r_selected, sample_r_sum, 0, 1)
            sample_l = sample_l_sum
            sample_r = sample_r_sum

    stop_gate = p.message("0. 150", 35, 195, 55)
    p.connect(starter, stop_gate, 1)
    p.connect(stop_gate, gate_line)
    sum_start_l = p.new("+~", 390, 515, 40, numinlets=2, numoutlets=1)
    sum_start_r = p.new("+~", 540, 515, 40, numinlets=2, numoutlets=1)
    p.connect(cinema_l, sum_start_l, 0, 0)
    p.connect(sample_l, sum_start_l, 0, 1)
    p.connect(cinema_r, sum_start_r, 0, 0)
    p.connect(sample_r, sum_start_r, 0, 1)
    sum_l = p.new("+~", 390, 610, 40, numinlets=2, numoutlets=1)
    sum_r = p.new("+~", 540, 610, 40, numinlets=2, numoutlets=1)
    left = outlet(p, 390, 680, signal=True)
    right = outlet(p, 540, 680, signal=True)
    p.connect(event_renderer, sum_l, 0, 0)
    p.connect(sum_start_l, sum_l, 0, 1)
    p.connect(event_renderer, sum_r, 1, 0)
    p.connect(sum_start_r, sum_r, 0, 1)
    p.connect(sum_l, left)
    p.connect(sum_r, right)
    return p.document()


def make_legacy_transient() -> dict[str, Any]:
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
    starter_fade_in = p.message("1. 20", 240, 155, 55)
    starter_fade_out = p.message("0. 350", 305, 155, 60)
    starter_envelope = p.new("line~", 375, 155, 50, numinlets=2, numoutlets=2)
    starter_stop_delay = p.new("delay 400", 240, 195, 70, numinlets=2, numoutlets=1)
    starter_stop = p.message("stop", 325, 195, 45)
    p.connect(starter_sel, starter_fade_in, 0)
    p.connect(starter_sel, starter_fade_out, 1)
    p.connect(starter_sel, starter_stop_delay, 1)
    p.connect(starter_fade_in, starter_envelope)
    p.connect(starter_fade_out, starter_envelope)
    p.connect(starter_stop_delay, starter_stop)
    p.connect(router, profile_sel, 10)
    for outlet_index, value in ((0, 0), (1, 1), (2, 2)):
        message = p.message(str(value), 105 + outlet_index * 45, 195, 30)
        p.connect(profile_sel, message, outlet_index)
        p.connect(message, profile_gate, 0, 0)

    for index, (name, gate_outlet) in enumerate((("starter_v12", 0), ("starter_v10", 1))):
        x = 35 + index * 300
        p.new(f"buffer~ {name} ../media/{name}.wav", x, 245, 235, numinlets=1, numoutlets=2)
        start = p.message("start", x, 285, 45)
        player = p.new(f"play~ {name} 1", x, 325, 145, numinlets=1, numoutlets=2)
        gain = p.new("*~ 0.08", x, 365, 65, numinlets=2, numoutlets=1)
        p.connect(profile_gate, start, gate_outlet)
        p.connect(start, player)
        p.connect(starter_stop, player)
        p.connect(player, gain)
        players.append(gain)

    local_buffer = p.new(
        "buffer~ ferrari_startup ../media/local/ferrari_sf90_startup.wav",
        635,
        245,
        370,
        numinlets=2,
        numoutlets=2,
    )
    local_info = p.new(
        "info~ ferrari_startup", 1020, 245, 155, numinlets=1, numoutlets=10
    )
    local_query_load = p.new("loadbang", 1020, 205, 70, numinlets=1, numoutlets=1)
    local_query_delay = p.new("delay 250", 1100, 205, 70, numinlets=2, numoutlets=1)
    local_available = p.new(
        "expr $f1>1000.", 1020, 285, 115, numinlets=1, numoutlets=1
    )
    local_available_pack = p.new(
        "pack 0. 20", 1020, 325, 85, numinlets=2, numoutlets=1
    )
    local_available_line = p.new(
        "line~", 1020, 365, 50, numinlets=2, numoutlets=2
    )
    fallback_available = p.new(
        "expr 1.-$f1", 1145, 285, 100, numinlets=1, numoutlets=1
    )
    fallback_available_pack = p.new(
        "pack 0. 20", 1145, 325, 85, numinlets=2, numoutlets=1
    )
    fallback_available_line = p.new(
        "line~", 1145, 365, 50, numinlets=2, numoutlets=2
    )
    fallback_default = p.new(
        "loadmess 1.", 1235, 325, 85, numinlets=1, numoutlets=1
    )
    p.connect(local_buffer, local_info, 1)
    p.connect(local_query_load, local_query_delay)
    p.connect(local_query_delay, local_info)
    p.connect(local_info, local_available, 6)
    p.connect(local_available, local_available_pack)
    p.connect(local_available_pack, local_available_line)
    p.connect(local_available, fallback_available)
    p.connect(fallback_available, fallback_available_pack)
    p.connect(fallback_available_pack, fallback_available_line)
    p.connect(fallback_default, fallback_available_pack)
    local_start = p.message("start", 635, 285, 45)
    local_player = p.new(
        "play~ ferrari_startup 2", 635, 325, 175, numinlets=1, numoutlets=3
    )
    local_left_gain = p.new("*~ 0.35", 635, 365, 65, numinlets=2, numoutlets=1)
    local_right_gain = p.new("*~ 0.35", 715, 365, 65, numinlets=2, numoutlets=1)
    local_left_envelope = p.new("*~", 635, 400, 40, numinlets=2, numoutlets=1)
    local_right_envelope = p.new("*~", 715, 400, 40, numinlets=2, numoutlets=1)
    p.connect(profile_gate, local_start, 0)
    p.connect(profile_gate, local_start, 1)
    p.connect(local_start, local_player)
    p.connect(starter_stop, local_player)
    p.connect(local_player, local_left_gain, 0, 0)
    p.connect(local_player, local_right_gain, 1, 0)
    p.connect(local_available_line, local_left_gain, 0, 1)
    p.connect(local_available_line, local_right_gain, 0, 1)
    p.connect(local_left_gain, local_left_envelope, 0, 0)
    p.connect(local_right_gain, local_right_envelope, 0, 0)
    p.connect(starter_envelope, local_left_envelope, 0, 1)
    p.connect(starter_envelope, local_right_envelope, 0, 1)

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
            p.new(f"buffer~ {name} ../media/{name}.wav", px, y + 82, 210, numinlets=1, numoutlets=2)
            start = p.message("start", px, y + 122, 45)
            player = p.new(f"play~ {name} 1", px, y + 162, 155, numinlets=1, numoutlets=2)
            gain = p.new(f"*~ {gain_value:.2f}", px, y + 202, 65, numinlets=2, numoutlets=1)
            p.connect(selector, start, index)
            p.connect(start, player)
            p.connect(player, gain)
            players.append(gain)

    add_family(tuple(f"shift_up_{index:02d}" for index in range(1, 4)), 0.21, 35, 440, ((shift_up_gate, 0),))
    add_family(tuple(f"shift_down_{index:02d}" for index in range(1, 4)), 0.24, 650, 440, ((shift_down_gate, 0),))
    add_family(tuple(f"intake_backfire_{index:02d}" for index in range(1, 4)), 0.34, 1265, 440, ((intake_gate, 0),))
    add_family(tuple(f"exhaust_pop_{index:02d}" for index in range(1, 5)), 0.30, 35, 740, ((exhaust_gate, 0),))
    add_family(tuple(f"exhaust_crackle_{index:02d}" for index in range(1, 4)), 0.18, 830, 740, ((crackle_gate, 0),))

    p.new("buffer~ mechanical_click ../media/mechanical_click.wav", 1445, 740, 255, numinlets=1, numoutlets=2)
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
            "svf~ 1600 0.7", 35 + index * 300, 1040, 105,
            numinlets=3, numoutlets=4,
        )
        starter_fade = p.new(
            "*~", 155 + index * 300, 1040, 40,
            numinlets=2, numoutlets=1,
        )
        fallback_select = p.new(
            "*~", 205 + index * 300, 1040, 40,
            numinlets=2, numoutlets=1,
        )
        p.connect(players[index], starter_lowpass)
        p.connect(starter_lowpass, starter_fade)
        p.connect(starter_envelope, starter_fade, 0, 1)
        p.connect(starter_fade, fallback_select)
        p.connect(fallback_available_line, fallback_select, 0, 1)
        players[index] = fallback_select

    mixed = players[0]
    for index, player in enumerate(players[1:]):
        add = p.new("+~", 240 + (index % 8) * 105, 1080 + (index // 8) * 45, 35, numinlets=2, numoutlets=1)
        p.connect(mixed, add, 0, 0)
        p.connect(player, add, 0, 1)
        mixed = add
    master = p.new("*~", 920, 1220, 40, numinlets=2, numoutlets=1)
    texture_master = p.new("*~", 920, 1255, 40, numinlets=2, numoutlets=1)
    left_source = p.new("+~", 820, 1255, 40, numinlets=2, numoutlets=1)
    right_source = p.new("+~", 980, 1255, 40, numinlets=2, numoutlets=1)
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
    p.connect(texture_master, left_source, 0, 0)
    p.connect(local_left_envelope, left_source, 0, 1)
    p.connect(texture_master, right_source, 0, 0)
    p.connect(local_right_envelope, right_source, 0, 1)
    p.connect(left_source, left_gain)
    p.connect(right_source, right_gain)
    p.connect(left_gain, trim_l)
    p.connect(right_gain, trim_r)
    p.connect(stem_level, trim_l, 0, 1)
    p.connect(stem_level, trim_r, 0, 1)
    p.connect(trim_l, left)
    p.connect(trim_r, right)
    p.connect(control, router)
    return p.document()


def make_transient() -> dict[str, Any]:
    """Compatibility seam for EV: shift/decel motion now stays in continuous DSP."""
    p = Patcher(620, 300)
    p.comment("V5 procedural event seam — no runtime shift/pop/crackle sample players", 25, 15, 560)
    control = inlet(p, 35, 65)
    names = (
        "starter", "shift", "shift_dir", "pop", "intake_backfire",
        "exhaust_pop", "crackle", "click", "aggression", "texture",
        "engine_type", "engine_running", "transient_level_db",
    )
    router = route(p, names, 35, 105, 540)
    silence_l = p.new("sig~ 0.", 180, 190, 55, numinlets=1, numoutlets=1)
    silence_r = p.new("sig~ 0.", 330, 190, 55, numinlets=1, numoutlets=1)
    left = outlet(p, 180, 255, signal=True)
    right = outlet(p, 330, 255, signal=True)
    p.connect(control, router)
    p.connect(silence_l, left)
    p.connect(silence_r, right)
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
    p.new("buffer~ cabin_ir_l ../media/cabin_ir_l.wav", 25, 740, 265, numinlets=2, numoutlets=2)
    p.new("buffer~ cabin_ir_r ../media/cabin_ir_r.wav", 25, 780, 265, numinlets=2, numoutlets=2)
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


def make_profile_drive_simulator(profile: str) -> dict[str, Any]:
    """Adapt the deterministic control-rate drivetrain to a Max message seam."""
    p = Patcher(720, 360)
    p.comment(
        f"{profile.upper()} drivetrain — one 20 ms clock; throttle stores state and never advances time",
        25,
        15,
        650,
    )
    control = inlet(p, 35, 70)
    model = p.new(
        f"js ../code/drive_model.js {profile}",
        225,
        155,
        220,
        numinlets=1,
        numoutlets=1,
    )
    tick = p.new("qmetro 20", 35, 155, 75, numinlets=2, numoutlets=1)
    tick_on = p.new("loadmess 1", 35, 115, 80, numinlets=1, numoutlets=1)
    output = outlet(p, 500, 255)
    p.connect(control, model)
    p.connect(tick_on, tick)
    p.connect(tick, model)
    p.connect(model, output)
    return p.document()


def make_legacy_profile_drive_simulator(profile: str) -> dict[str, Any]:
    """Small fixed-profile drive model with deterministic start reset and flare."""
    config = PROFILE_CONFIG[profile]
    flare = 650.0 if profile == "ev" else (1050.0 if profile == "v10" else 1100.0)
    idle = config["idle_rpm"]
    p = Patcher(1260, 780)
    p.comment(
        f"{profile.upper()} fixed drive model — manual/auto, 2 s post-start guard, start catch {flare:g}->{idle:g} RPM",
        25, 15, 880,
    )
    control = inlet(p, 35, 65)
    split = p.new("t l l", 35, 105, 55, numinlets=1, numoutlets=2)
    router = route(p, ("throttle", "brake", "auto", "ignition", "start"), 120, 105, 430)
    output = outlet(p, 585, 730)
    p.connect(control, split)
    p.connect(split, output, 0)
    p.connect(split, router, 1)

    throttle = p.new("clip 0. 1.", 35, 165, 75, numinlets=3, numoutlets=1)
    brake = p.new("clip 0. 1.", 125, 165, 75, numinlets=3, numoutlets=1)
    auto = p.new("clip 0 1", 215, 165, 65, numinlets=3, numoutlets=1)
    ignition = p.new("clip 0 1", 295, 165, 65, numinlets=3, numoutlets=1)
    start = p.new("clip 0 1", 375, 165, 65, numinlets=3, numoutlets=1)
    for outlet_index, destination in enumerate((throttle, brake, auto, ignition, start)):
        p.connect(router, destination, outlet_index)
    for index, destination in enumerate((throttle, brake, auto, ignition, start)):
        initial = p.new("loadmess 0", 35 + index * 90, 205, 80, numinlets=1, numoutlets=1)
        p.connect(initial, destination)

    tick = p.new("qmetro 50", 520, 105, 75, numinlets=2, numoutlets=1)
    tick_on = p.new("loadmess 1", 520, 65, 80, numinlets=1, numoutlets=1)
    tick_order = p.new("t b b b", 520, 145, 70, numinlets=1, numoutlets=3)
    counter = p.new("counter 0 399", 520, 185, 95, numinlets=5, numoutlets=4)
    p.connect(tick_on, tick)
    p.connect(tick, tick_order)
    p.connect(tick_order, counter, 2)

    running = p.new("int 0", 650, 165, 50, numinlets=2, numoutlets=1)
    start_edge = p.new("sel 1", 375, 245, 45, numinlets=1, numoutlets=2)
    start_trigger = p.new("t b b b b b", 375, 285, 95, numinlets=1, numoutlets=5)
    running_on = p.message("1", 485, 285, 30)
    running_off = p.message("0", 650, 205, 30)
    ignition_off = p.new("sel 0", 295, 245, 45, numinlets=1, numoutlets=2)
    counter_reset = p.message("set 0", 520, 245, 45)
    speed_reset = p.message("0.", 575, 245, 35)
    gear_reset = p.message("gear 1", 620, 245, 50)
    p.connect(start, start_edge)
    p.connect(start_edge, start_trigger, 0)
    p.connect(start_trigger, running_on, 4)
    p.connect(running_on, running, 0, 0)
    p.connect(start_trigger, counter_reset, 3)
    p.connect(counter_reset, counter)
    p.connect(start_trigger, speed_reset, 2)
    p.connect(start_trigger, gear_reset, 1)
    p.connect(gear_reset, output)
    p.connect(ignition, ignition_off)
    p.connect(ignition_off, running_off, 0)
    p.connect(running_off, running, 0, 0)

    throttle_state = p.new("pak 0. 0 0 0", 35, 335, 110, numinlets=4, numoutlets=1)
    effective_throttle = p.new(
        "expr ($i4!=0)*(($i2==0)*$f1+($i2!=0)*($i3>=40)*(0.16+0.78*min(1.,($i3-40.)/120.)))",
        35, 375, 600, numinlets=4, numoutlets=1,
    )
    p.connect(throttle, throttle_state, 0, 0)
    p.connect(auto, throttle_state, 0, 1)
    p.connect(counter, throttle_state, 0, 2)
    p.connect(running, throttle_state, 0, 3)
    p.connect(throttle_state, effective_throttle)

    speed_store = p.new("f 0.", 520, 335, 50, numinlets=2, numoutlets=1)
    speed_state = p.new("pak 0. 0. 0.", 520, 375, 105, numinlets=3, numoutlets=1)
    speed_integrator = p.new(
        "expr max(0.,min(300.,$f1+0.05*($f2*(34.-0.07*$f1)-(0.5+0.00012*$f1*$f1)-$f3*55.)))",
        520, 415, 620, numinlets=3, numoutlets=1,
    )
    speed_split = p.new("t f f f", 520, 455, 70, numinlets=1, numoutlets=3)
    p.connect(tick_order, speed_store, 0)
    p.connect(speed_store, speed_state, 0, 0)
    p.connect(effective_throttle, speed_state, 0, 1)
    p.connect(brake, speed_state, 0, 2)
    p.connect(speed_state, speed_integrator)
    p.connect(speed_integrator, speed_split)
    p.connect(speed_split, speed_store, 2, 1)
    p.connect(speed_reset, speed_store, 0, 1)

    gear_store = p.new("int 1", 690, 495, 50, numinlets=2, numoutlets=1)
    gear_default = p.new("loadmess 1", 750, 495, 80, numinlets=1, numoutlets=1)
    gear_restart = p.message("1", 840, 495, 30)
    gear_change = p.new("change", 690, 535, 55, numinlets=1, numoutlets=1)
    gear_named = p.new("prepend gear", 755, 535, 90, numinlets=1, numoutlets=1)
    rpm_state = p.new("pak 0. 0. 1", 520, 495, 100, numinlets=3, numoutlets=1)
    if profile == "ev":
        rpm_expr = f"expr min(10000.,{idle:g}+$f1*31.+$f2*1400.)"
    else:
        ratios = (
            "107.+($i3==2)*-33.5+($i3==3)*-51.1+($i3==4)*-62.5+($i3==5)*-71.4+($i3==6)*-78.+($i3==7)*-82.8"
            if profile == "v12"
            else "114.2+($i3==2)*-37.5+($i3==3)*-58.7+($i3==4)*-70.4+($i3==5)*-79.9+($i3==6)*-86.5+($i3==7)*-91.6"
        )
        rpm_expr = f"expr max({idle:g},$f1*({ratios})+$f2*520.)"
    normal_rpm = p.new(rpm_expr, 520, 535, 620, numinlets=3, numoutlets=1)
    normal_rpm_pack = p.new("pack 0. 120", 520, 570, 90, numinlets=2, numoutlets=1)
    normal_rpm_line = p.new("line 0.", 625, 570, 60, numinlets=2, numoutlets=2)
    p.connect(tick_order, gear_store, 1)
    p.connect(gear_default, gear_store, 0, 0)
    p.connect(start_trigger, gear_restart, 1)
    p.connect(gear_restart, gear_store, 0, 0)
    p.connect(gear_store, gear_change)
    p.connect(gear_change, gear_named)
    p.connect(gear_named, output)
    p.connect(speed_split, rpm_state, 1, 0)
    p.connect(effective_throttle, rpm_state, 0, 1)
    p.connect(gear_store, rpm_state, 0, 2)
    p.connect(rpm_state, normal_rpm)
    p.connect(normal_rpm, normal_rpm_pack)
    p.connect(normal_rpm_pack, normal_rpm_line)

    if profile != "ev":
        shift_state = p.new("pak 0. 1 0.", 875, 495, 95, numinlets=3, numoutlets=1)
        if profile == "v12":
            shift_expr = "expr (($f1>6200.+2600.*$f3)*($i2<7))-(($f1<2200.+1600.*$f3)*($i2>1))"
        else:
            shift_expr = "expr (($f1>5800.+2500.*$f3)*($i2<7))-(($f1<2100.+1500.*$f3)*($i2>1))"
        shift_decision = p.new(shift_expr, 875, 535, 375, numinlets=3, numoutlets=1)
        shift_nonzero = p.new("sel 0", 875, 575, 45, numinlets=1, numoutlets=2)
        shift_lockout = p.new("speedlim 350", 930, 575, 85, numinlets=2, numoutlets=1)
        shift_direction = p.new("sel -1 1", 1025, 575, 60, numinlets=1, numoutlets=3)
        down_value = p.message("-1", 875, 615, 30)
        up_value = p.message("1", 915, 615, 30)
        down_event = p.message("shift_dir -1, shift 1", 955, 615, 145)
        up_event = p.message("shift_dir 1, shift 1", 1110, 615, 140)
        gear_state = p.new("pak 0 1", 875, 655, 70, numinlets=2, numoutlets=1)
        gear_next = p.new("expr $i1+$i2", 955, 655, 95, numinlets=2, numoutlets=1)
        gear_clip = p.new("clip 1 7", 1060, 655, 65, numinlets=3, numoutlets=1)
        gear_update = p.new("t i i", 1135, 655, 55, numinlets=1, numoutlets=2)
        p.connect(normal_rpm, shift_state, 0, 0)
        p.connect(gear_store, shift_state, 0, 1)
        p.connect(effective_throttle, shift_state, 0, 2)
        p.connect(shift_state, shift_decision)
        p.connect(shift_decision, shift_nonzero)
        p.connect(shift_nonzero, shift_lockout, 1)
        p.connect(shift_lockout, shift_direction)
        p.connect(shift_direction, down_value, 0)
        p.connect(shift_direction, down_event, 0)
        p.connect(shift_direction, up_value, 1)
        p.connect(shift_direction, up_event, 1)
        p.connect(gear_store, gear_state, 0, 1)
        p.connect(down_value, gear_state, 0, 0)
        p.connect(up_value, gear_state, 0, 0)
        p.connect(gear_state, gear_next)
        p.connect(gear_next, gear_clip)
        p.connect(gear_clip, gear_update)
        p.connect(gear_update, gear_store, 1, 1)
        p.connect(down_event, output)
        p.connect(up_event, output)

    rpm_switch = p.new("switch 2", 520, 610, 75, numinlets=3, numoutlets=1)
    normal_select = p.message("1", 455, 590, 30)
    flare_select = p.message("2", 415, 325, 30)
    flare_line = p.new("line 0. 10", 375, 365, 75, numinlets=3, numoutlets=2)
    flare_message = p.message(f"{flare:.1f} 0, {idle:.1f} 850", 375, 405, 155)
    flare_done = p.new("delay 900", 375, 445, 70, numinlets=2, numoutlets=1)
    p.connect(normal_rpm_line, rpm_switch, 0, 1)
    p.connect(normal_select, rpm_switch, 0, 0)
    p.connect(start_trigger, flare_select, 0)
    p.connect(flare_select, rpm_switch, 0, 0)
    p.connect(start_trigger, flare_message, 0)
    p.connect(flare_message, flare_line)
    p.connect(flare_line, rpm_switch, 0, 2)
    p.connect(start_trigger, flare_done, 0)
    p.connect(flare_done, normal_select)

    named_sources = (
        (speed_split, 0, "prepend speed_kph"),
        (rpm_switch, 0, "prepend rpm"),
        (effective_throttle, 0, "prepend throttle"),
        (brake, 0, "prepend brake"),
        (effective_throttle, 0, "prepend load"),
    )
    for index, (source_box, source_outlet, text_value) in enumerate(named_sources):
        named = p.new(text_value, 35 + (index % 3) * 170, 515 + (index // 3) * 45, 130, numinlets=1, numoutlets=1)
        p.connect(source_box, named, source_outlet)
        p.connect(named, output)
    accel_expr = p.new("expr max(-1.,min(1.,$f1*2.-$f2*2.))", 35, 620, 250, numinlets=2, numoutlets=1)
    accel_named = p.new("prepend accel", 300, 620, 95, numinlets=1, numoutlets=1)
    p.connect(effective_throttle, accel_expr, 0, 0)
    p.connect(brake, accel_expr, 0, 1)
    p.connect(accel_expr, accel_named)
    p.connect(accel_named, output)
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


def make_launcher() -> dict[str, Any]:
    """Build a DSP-free project switchboard for the three independent demos."""
    p = Patcher(720, 390)
    p.comment("VehicleSoundSynth V5 — choose one independent runtime", 30, 25, 520)
    p.comment(
        "The launcher owns no audio objects. Selecting a profile closes the previous runtime before opening one instance.",
        30,
        58,
        650,
        40,
    )
    controller = p.new("pcontrol", 570, 175, 70, numinlets=1, numoutlets=0)
    selection = p.new("s vss.runtime.select", 360, 285, 145, numinlets=1, numoutlets=0)
    for index, profile in enumerate(("ev", "v10", "v12")):
        config = PROFILE_CONFIG[profile]
        y = 120 + index * 68
        p.comment(config["title"], 45, y, 210)
        button = p.message(f"Open {config['title']}", 270, y, 190)
        order = p.new("t b b", 470, y, 50, numinlets=1, numoutlets=2)
        select_message = p.message(profile, 360, y + 30, 55)
        open_delay = p.new("delay 40", 530, y + 30, 65, numinlets=2, numoutlets=1)
        open_message = p.message(f"loadunique {config['runtime']}", 270, y + 30, 260)
        p.connect(button, order)
        p.connect(order, select_message, 1)
        p.connect(select_message, selection)
        p.connect(order, open_delay, 0)
        p.connect(open_delay, open_message)
        p.connect(open_message, controller)
    close_all = p.message("Close active runtime", 510, 285, 145)
    close_symbol = p.message("none", 510, 315, 55)
    p.connect(close_all, close_symbol)
    p.connect(close_symbol, selection)
    p.comment("Tip: save intentional BEAP edits before switching profiles or closing the active runtime.", 30, 350, 650)
    return p.document()


def make_keyboard_drive_ws() -> dict[str, Any]:
    """Build a focus-aware binary W/S pedal adapter for Manual mode."""
    p = Patcher(720, 430)
    p.comment(
        "Keyboard adapter — W is immediate full throttle; S is immediate fixed service brake; releases return to zero",
        20,
        15,
        650,
    )
    manual = inlet(p, 25, 55)
    p.comment("Manual enabled (0/1)", 65, 58, 150)
    key_down = p.new("key", 25, 105, 45, numinlets=0, numoutlets=1)
    key_up = p.new("keyup", 85, 105, 55, numinlets=0, numoutlets=1)
    down_select = p.new("sel 119 87 115 83", 25, 145, 125, numinlets=1, numoutlets=5)
    up_select = p.new("sel 119 87 115 83", 165, 145, 125, numinlets=1, numoutlets=5)
    w_gate = p.new("gate 1", 25, 220, 55, numinlets=2, numoutlets=1)
    s_gate = p.new("gate 1", 165, 220, 55, numinlets=2, numoutlets=1)
    w_pressed = p.message("1", 25, 185, 30)
    w_released = p.message("0", 65, 185, 30)
    s_pressed = p.message("1", 165, 185, 30)
    s_released = p.message("0", 205, 185, 30)
    manual_off = p.new("sel 0", 315, 105, 45, numinlets=1, numoutlets=2)
    disable_order = p.new("t b b", 375, 105, 50, numinlets=1, numoutlets=2)
    reset_key_state = p.message("set 0", 435, 92, 45)
    hard_zero = p.message("0.", 435, 120, 35)
    default_off = p.new("loadmess 0", 490, 105, 80, numinlets=1, numoutlets=1)
    w_change = p.new("change", 25, 260, 55, numinlets=1, numoutlets=3)
    s_change = p.new("change", 165, 260, 55, numinlets=1, numoutlets=3)
    w_state = p.new("sel 1 0", 25, 300, 55, numinlets=1, numoutlets=3)
    s_state = p.new("sel 1 0", 165, 300, 55, numinlets=1, numoutlets=3)
    throttle_up = p.message("1.", 25, 340, 35)
    throttle_off = p.message("0.", 70, 340, 35)
    brake_on = p.message("0.65", 165, 340, 45)
    brake_off = p.message("0.", 220, 340, 35)
    throttle_line = p.new("line 0.", 320, 340, 60, numinlets=2, numoutlets=2)
    brake_line = p.new("line 0.", 410, 340, 60, numinlets=2, numoutlets=2)
    throttle_out = outlet(p, 320, 385)
    brake_out = outlet(p, 410, 385)

    p.connect(key_down, down_select)
    p.connect(key_up, up_select)
    for outlet_index in (0, 1):
        p.connect(down_select, w_pressed, outlet_index)
        p.connect(up_select, w_released, outlet_index)
    for outlet_index in (2, 3):
        p.connect(down_select, s_pressed, outlet_index)
        p.connect(up_select, s_released, outlet_index)
    p.connect(manual, w_gate, 0, 0)
    p.connect(manual, s_gate, 0, 0)
    p.connect(manual, manual_off)
    p.connect(default_off, w_gate, 0, 0)
    p.connect(default_off, s_gate, 0, 0)
    p.connect(default_off, manual_off)
    p.connect(w_pressed, w_gate, 0, 1)
    p.connect(w_released, w_gate, 0, 1)
    p.connect(s_pressed, s_gate, 0, 1)
    p.connect(s_released, s_gate, 0, 1)
    p.connect(manual_off, disable_order, 0)
    p.connect(disable_order, reset_key_state, 1)
    p.connect(reset_key_state, w_change)
    p.connect(reset_key_state, s_change)
    p.connect(disable_order, hard_zero, 0)
    p.connect(hard_zero, throttle_line)
    p.connect(hard_zero, brake_line)
    p.connect(w_gate, w_change)
    p.connect(s_gate, s_change)
    p.connect(w_change, w_state)
    p.connect(s_change, s_state)
    p.connect(w_state, throttle_up, 0)
    p.connect(w_state, throttle_off, 1)
    p.connect(s_state, brake_on, 0)
    p.connect(s_state, brake_off, 1)
    p.connect(throttle_up, throttle_line)
    p.connect(throttle_off, throttle_line)
    p.connect(brake_on, brake_line)
    p.connect(brake_off, brake_line)
    p.connect(throttle_line, throttle_out)
    p.connect(brake_line, brake_out)
    return p.document()


def make_manual_input() -> dict[str, Any]:
    """Unify keyboard and fixed LT/RT gamepad pedals behind one small seam."""
    p = Patcher(1000, 500)
    p.comment(
        "MANUAL INPUT — Keyboard W/S or Gamepad LT/RT; every source/mode change releases both pedals",
        20, 15, 760,
    )
    manual = inlet(p, 20, 45)
    throttle_out = outlet(p, 850, 450)
    brake_out = outlet(p, 920, 450)

    p.comment("Input Source: Keyboard / Gamepad", 20, 48, 230)
    source_menu = p.add(
        "umenu", None, 20, 72, 125, numinlets=1, numoutlets=3,
        items=["Keyboard", ",", "Gamepad"],
    )
    source_default = p.new("loadmess 0", 152, 72, 80, numinlets=1, numoutlets=1)
    source_trigger = p.new("t i i", 240, 72, 50, numinlets=1, numoutlets=2)
    source_select = p.new("sel 0 1", 298, 72, 55, numinlets=1, numoutlets=3)
    source_keyboard = p.message("source keyboard", 360, 62, 110)
    source_gamepad = p.message("source gamepad", 360, 88, 110)

    p.comment("Gamepad: fixed LT throttle / RT brake — use DS4 Wireless Controller Bluetooth mode", 490, 48, 480)
    p.comment("Detected", 490, 72, 68)
    detected = p.add("toggle", None, 490, 94, 22, 22, numinlets=1, numoutlets=1)
    p.comment("Analog warning", 525, 72, 100)
    analog_warning = p.add("toggle", None, 525, 94, 22, 22, numinlets=1, numoutlets=1)
    device_name_set = p.new("prepend set", 565, 94, 82, numinlets=1, numoutlets=1)
    device_name = p.message("No gamepad detected", 655, 94, 170)
    device_type_set = p.new("prepend set", 835, 94, 82, numinlets=1, numoutlets=1)
    device_type = p.message("unknown", 925, 94, 70)

    debug_specs = (
        ("LT Throttle Raw", 20),
        ("Throttle Norm", 145),
        ("RT Brake Raw", 270),
        ("Brake Norm", 395),
    )
    debug_numbers: list[str] = []
    for label, x in debug_specs:
        p.comment(label, x, 125, 110)
        debug_numbers.append(p.add("flonum", None, x, 148, 82, numinlets=1, numoutlets=2))

    p.comment("Dead Zone", 535, 125, 78)
    dead_zone = p.add("flonum", None, 535, 148, 62, numinlets=1, numoutlets=2)
    dead_zone_default = p.new("loadmess 0.02", 603, 148, 100, numinlets=1, numoutlets=1)
    dead_zone_clip = p.new("clip 0. 0.25", 710, 148, 90, numinlets=3, numoutlets=1)
    dead_zone_named = p.new("prepend dead_zone", 807, 148, 120, numinlets=1, numoutlets=1)
    p.comment("Smoothing ms", 535, 182, 95)
    smoothing = p.add("flonum", None, 535, 205, 62, numinlets=1, numoutlets=2)
    smoothing_default = p.new("loadmess 30.", 603, 205, 92, numinlets=1, numoutlets=1)
    smoothing_clip = p.new("clip 0. 100.", 710, 205, 88, numinlets=3, numoutlets=1)
    smoothing_named = p.new("prepend smoothing_ms", 807, 205, 145, numinlets=1, numoutlets=1)

    manual_clip = p.new("clip 0 1", 20, 245, 65, numinlets=3, numoutlets=1)
    manual_trigger = p.new("t i i", 92, 245, 50, numinlets=1, numoutlets=2)
    manual_named = p.new("prepend manual", 150, 245, 100, numinlets=1, numoutlets=1)
    source_state = p.new("pak 0 0", 260, 245, 70, numinlets=2, numoutlets=1)
    keyboard_enabled = p.new("expr $i1*($i2==0)", 340, 233, 145, numinlets=2, numoutlets=1)
    gamepad_enabled = p.new("expr $i1*($i2==1)", 340, 259, 145, numinlets=2, numoutlets=1)
    keyboard = p.add(
        "bpatcher", None, 500, 245, 190, 40, numinlets=1, numoutlets=2,
        name="Patcher:/patchers/keyboard_drive_ws.maxpat",
    )
    keyboard_throttle = p.new("prepend keyboard_throttle", 700, 240, 175, numinlets=1, numoutlets=1)
    keyboard_brake = p.new("prepend keyboard_brake", 700, 270, 165, numinlets=1, numoutlets=1)

    gamepad = p.new("gamepad", 20, 315, 75, numinlets=1, numoutlets=3)
    device_info = p.new("prepend device_info", 105, 335, 130, numinlets=1, numoutlets=1)
    gamepad_status = p.new("prepend gamepad_status", 105, 365, 145, numinlets=1, numoutlets=1)
    clock = p.new("qmetro 10", 260, 315, 72, numinlets=2, numoutlets=1)
    clock_off = p.new("loadmess 0", 260, 345, 80, numinlets=1, numoutlets=1)
    model = p.new("js Patcher:/code/manual_input.js", 355, 315, 220, numinlets=1, numoutlets=3)
    debug_route_names = (
        "detected", "device_name", "device_type", "analog_warning",
        "throttle_raw", "throttle_normalized", "brake_raw", "brake_normalized",
    )
    debug_route = route(p, debug_route_names, 585, 315, 390)

    p.connect(manual, manual_clip)
    p.connect(manual_clip, manual_trigger)
    p.connect(manual_trigger, manual_named, 1)
    p.connect(manual_named, model)
    p.connect(manual_trigger, source_state, 0, 0)
    p.connect(source_default, source_menu)
    p.connect(source_menu, source_trigger)
    p.connect(source_trigger, source_select, 1)
    p.connect(source_trigger, source_state, 0, 1)
    p.connect(source_select, source_keyboard, 0)
    p.connect(source_select, source_gamepad, 1)
    p.connect(source_keyboard, model)
    p.connect(source_gamepad, model)
    p.connect(source_state, keyboard_enabled)
    p.connect(source_state, gamepad_enabled)
    p.connect(keyboard_enabled, keyboard)
    p.connect(keyboard, keyboard_throttle, 0, 0)
    p.connect(keyboard, keyboard_brake, 1, 0)
    p.connect(keyboard_throttle, model)
    p.connect(keyboard_brake, model)

    p.connect(gamepad, model, 0, 0)
    p.connect(gamepad, device_info, 1, 0)
    p.connect(device_info, model)
    p.connect(gamepad, gamepad_status, 2, 0)
    p.connect(gamepad_status, model)
    p.connect(gamepad_enabled, clock)
    p.connect(clock_off, clock)
    p.connect(clock, model)
    p.connect(dead_zone_default, dead_zone)
    p.connect(dead_zone, dead_zone_clip)
    p.connect(dead_zone_clip, dead_zone_named)
    p.connect(dead_zone_named, model)
    p.connect(smoothing_default, smoothing)
    p.connect(smoothing, smoothing_clip)
    p.connect(smoothing_clip, smoothing_named)
    p.connect(smoothing_named, model)

    p.connect(model, throttle_out, 0, 0)
    p.connect(model, brake_out, 1, 0)
    p.connect(model, debug_route, 2, 0)
    debug_targets = (
        detected, device_name_set, device_type_set, analog_warning,
        debug_numbers[0], debug_numbers[1], debug_numbers[2], debug_numbers[3],
    )
    for index, target in enumerate(debug_targets):
        p.connect(debug_route, target, index)
    p.connect(device_name_set, device_name)
    p.connect(device_type_set, device_type)
    return p.document()


def make_profile_main(profile: str, root: Path | None = None) -> dict[str, Any]:
    """Build one self-contained, profile-fixed runnable patcher."""
    config = PROFILE_CONFIG[profile]
    p = Patcher(1500, 1080)
    p.comment(f"VehicleSoundSynth V5 — {config['title']} independent runtime", 25, 18, 720)
    p.comment("Audio starts OFF. This patch contains only this profile's DSP graph.", 25, 48, 620)
    active_profile = p.new("r vss.runtime.select", 850, 25, 145, numinlets=0, numoutlets=1)
    active_match = p.new(f"sel {profile}", 850, 60, 65, numinlets=1, numoutlets=2)
    save_then_close = p.new("t b b", 930, 95, 50, numinlets=1, numoutlets=2)
    save_message = p.message("write", 990, 70, 45)
    close_delay = p.new("delay 20", 990, 105, 65, numinlets=2, numoutlets=1)
    close_message = p.message("wclose", 1070, 105, 55)
    patcher_control = p.new("thispatcher", 1070, 140, 85, numinlets=1, numoutlets=2)
    close_save = p.new("closebang", 850, 140, 65, numinlets=0, numoutlets=1)
    eq_save = p.new("s vehicle_bus_eq.save", 925, 140, 145, numinlets=1, numoutlets=0)
    p.connect(active_profile, active_match)
    p.connect(active_match, save_then_close, 1)
    p.connect(save_then_close, save_message, 1)
    p.connect(save_message, patcher_control)
    p.connect(save_then_close, close_delay, 0)
    p.connect(close_delay, close_message)
    p.connect(close_message, patcher_control)
    p.connect(close_save, eq_save)

    drive = p.add(
        "bpatcher", None, 1210, 330, 210, 55, numinlets=1, numoutlets=1,
        name=f"Patcher:/patchers/{config['drive']}.maxpat",
    )
    external = p.new(f"r vss.{profile}.input", 1210, 395, 130, numinlets=0, numoutlets=1)
    source = p.new("switch 2", 1210, 430, 75, numinlets=3, numoutlets=1)
    source_default = p.new("loadmess 1", 1300, 430, 80, numinlets=1, numoutlets=1)
    engine = p.add(
        "bpatcher", None, 1210, 470, 220, 55, numinlets=1, numoutlets=2,
        name=f"Patcher:/patchers/{config['engine']}.maxpat",
    )
    p.connect(source_default, source, 0, 0)
    p.connect(drive, source, 0, 1)
    p.connect(external, source, 0, 2)
    p.connect(source, engine)

    p.comment("Lifecycle", 25, 105, 120)
    ignition_on = p.message("ignition 1", 25, 135, 75)
    start = p.message("start 1", 115, 135, 60)
    stop = p.message("ignition 0", 190, 135, 75)
    for message in (ignition_on, start, stop):
        p.connect(message, drive)

    p.comment("Drive source", 300, 105, 120)
    source_menu = p.add(
        "umenu",
        None,
        300,
        135,
        155,
        numinlets=1,
        numoutlets=3,
        items=["Internal Manual", ",", "Internal Auto", ",", f"External vss.{profile}.input"],
    )
    source_select = p.new("expr 1+($i1==2)", 470, 135, 120, numinlets=1, numoutlets=1)
    auto_select = p.new("== 1", 470, 170, 45, numinlets=2, numoutlets=1)
    auto_named = p.new("prepend auto", 525, 170, 95, numinlets=1, numoutlets=1)
    source_load = p.new("loadmess 0", 600, 135, 80, numinlets=1, numoutlets=1)
    manual_select = p.new("== 0", 630, 170, 45, numinlets=2, numoutlets=1)
    p.connect(source_load, source_menu)
    p.connect(source_menu, source_select)
    p.connect(source_select, source, 0, 0)
    p.connect(source_menu, auto_select)
    p.connect(auto_select, auto_named)
    p.connect(auto_named, drive)
    p.connect(source_menu, manual_select)

    pedal_numbers: dict[str, str] = {}
    for index, (label, name, default) in enumerate(
        (("Throttle", "throttle", 0.0), ("Brake", "brake", 0.0))
    ):
        x = 25 + index * 150
        p.comment(label, x, 205, 100)
        number = p.add("flonum", None, x, 232, 75, numinlets=1, numoutlets=2)
        clip = p.new("clip 0. 1.", x, 266, 75, numinlets=3, numoutlets=1)
        named = p.new(f"prepend {name}", x, 300, 110, numinlets=1, numoutlets=1)
        initial = p.new(f"loadmess {default:g}", x + 80, 232, 80, numinlets=1, numoutlets=1)
        p.connect(number, clip)
        p.connect(clip, named)
        p.connect(named, drive)
        p.connect(initial, number)
        pedal_numbers[name] = number

    manual_input = p.add(
        "bpatcher", None, 25, 430, 1000, 430, numinlets=1, numoutlets=2,
        name="Patcher:/patchers/manual_input.maxpat",
    )
    p.connect(manual_select, manual_input)
    p.connect(manual_input, pedal_numbers["throttle"], 0, 0)
    p.connect(manual_input, pedal_numbers["brake"], 1, 0)

    p.comment("Cinematic Soundscape (shared editable BEAP core)", 330, 205, 310)
    p.comment("Soundscape Enable", 330, 230, 115)
    soundscape_enable = p.add("toggle", None, 330, 253, 24, 24, numinlets=1, numoutlets=1)
    soundscape_enable_named = p.new("prepend soundscape_enable", 360, 253, 175, numinlets=1, numoutlets=1)
    soundscape_enable_default = p.new("loadmess 0", 360, 280, 80, numinlets=1, numoutlets=1)
    p.connect(soundscape_enable, soundscape_enable_named)
    p.connect(soundscape_enable_named, engine)
    p.connect(soundscape_enable_default, soundscape_enable)

    soundscape_specs = (
        ("Soundscape dB", "soundscape_level_db", -14.0 if profile != "v12" else -15.0, -60.0, 6.0, 550),
        ("Motion", "soundscape_motion", {"ev": 0.62, "v10": 0.52, "v12": 0.42}[profile], 0.0, 1.0, 690),
        ("Space", "soundscape_space", {"ev": 0.42, "v10": 0.38, "v12": 0.52}[profile], 0.0, 1.0, 810),
    )
    for label, name, default, low, high, x in soundscape_specs:
        p.comment(label, x, 230, 105)
        number = p.add("flonum", None, x, 253, 70, numinlets=1, numoutlets=2)
        bounded = p.new(f"clip {low:g} {high:g}", x, 280, 85, numinlets=3, numoutlets=1)
        named = p.new(f"prepend {name}", x + 90, 253, 170, numinlets=1, numoutlets=1)
        initial = p.new(f"loadmess {default:g}", x + 90, 280, 95, numinlets=1, numoutlets=1)
        p.connect(number, bounded)
        p.connect(bounded, named)
        p.connect(named, engine)
        p.connect(initial, number)
    p.comment("Soundscape Solo", 960, 230, 115)
    soundscape_solo = p.add("toggle", None, 960, 253, 24, 24, numinlets=1, numoutlets=1)
    soundscape_solo_named = p.new("prepend soundscape_solo", 990, 253, 170, numinlets=1, numoutlets=1)
    soundscape_solo_default = p.new("loadmess 0", 990, 280, 80, numinlets=1, numoutlets=1)
    p.connect(soundscape_solo, soundscape_solo_named)
    p.connect(soundscape_solo_named, engine)
    p.connect(soundscape_solo_default, soundscape_solo)
    open_dna = p.message("Open Sound DNA", 1180, 230, 125)
    open_dna_instance = p.new(
        f"s open.{profile}.sound_dna", 1180, 260, 180,
        numinlets=1, numoutlets=0,
    )
    p.comment("Sound DNA Solo", 1180, 290, 115)
    dna_solo = p.add("toggle", None, 1180, 315, 24, 24, numinlets=1, numoutlets=1)
    dna_solo_named = p.new("prepend dna_solo", 1210, 315, 140, numinlets=1, numoutlets=1)
    dna_solo_default = p.new("loadmess 0", 1210, 342, 80, numinlets=1, numoutlets=1)
    p.connect(dna_solo, dna_solo_named)
    p.connect(dna_solo_named, engine)
    p.connect(dna_solo_default, dna_solo)
    design_windows = p.new("pcontrol", 1410, 400, 70, numinlets=1, numoutlets=0)
    open_soundscape = p.message("Open Soundscape BEAP", 1180, 370, 160)
    open_soundscape_file = p.message(
        "loadunique Patcher:/patchers/cinematic_soundscape_beap~.maxpat",
        1180, 400, 260,
    )
    p.connect(open_dna, open_dna_instance)
    p.connect(open_soundscape, open_soundscape_file)
    p.connect(open_soundscape_file, design_windows)

    if profile == "ev":
        p.comment("Legacy EV macro preset", 330, 315, 150)
        mode = p.add(
            "umenu", None, 330, 340, 145, numinlets=1, numoutlets=3,
            items=["Relax", ",", "Expressive", ",", "Sport"],
        )
        mode_messages = (
            p.message("ev_mode relax", 485, 330, 105),
            p.message("ev_mode expressive", 485, 355, 135),
            p.message("ev_mode sport", 625, 355, 105),
        )
        selector = p.new("sel 0 1 2", 740, 340, 70, numinlets=1, numoutlets=4)
        mode_default = p.new("loadmess 0", 820, 340, 80, numinlets=1, numoutlets=1)
        p.connect(mode_default, mode)
        p.connect(mode, selector)
        for index, message in enumerate(mode_messages):
            p.connect(selector, message, index)
            p.connect(message, engine)
    else:
        p.comment("Start sound", 330, 315, 120)
        style = p.add(
            "umenu", None, 330, 340, 145, numinlets=1, numoutlets=3,
            items=["Cinematic BEAP", ",", "Realistic Sample"],
        )
        style_selector = p.new("sel 0 1", 485, 340, 55, numinlets=1, numoutlets=3)
        cinematic = p.message("start_style cinematic", 550, 330, 145)
        realistic = p.message("start_style realistic", 550, 355, 135)
        style_default = p.new("loadmess 0", 700, 340, 80, numinlets=1, numoutlets=1)
        p.connect(style_default, style)
        p.connect(style, style_selector)
        p.connect(style_selector, cinematic, 0)
        p.connect(style_selector, realistic, 1)
        p.connect(cinematic, engine)
        p.connect(realistic, engine)

        p.comment("Backfire Enable / Intensity", 25, 315, 185)
        backfire_enable = p.add("toggle", None, 25, 340, 24, 24, numinlets=1, numoutlets=1)
        backfire_enable_named = p.new("prepend backfire_enable", 60, 340, 155, numinlets=1, numoutlets=1)
        backfire_enable_default = p.new("loadmess 1", 225, 340, 80, numinlets=1, numoutlets=1)
        backfire_intensity = p.add("flonum", None, 25, 375, 70, numinlets=1, numoutlets=2)
        backfire_intensity_clip = p.new("clip 0. 1.", 105, 375, 75, numinlets=3, numoutlets=1)
        backfire_intensity_named = p.new("prepend backfire_intensity", 190, 375, 175, numinlets=1, numoutlets=1)
        backfire_intensity_default = p.new(
            f"loadmess {0.82 if profile == 'v10' else 0.55:g}",
            375, 375, 100, numinlets=1, numoutlets=1,
        )
        p.connect(backfire_enable, backfire_enable_named)
        p.connect(backfire_enable_named, engine)
        p.connect(backfire_enable_default, backfire_enable)
        p.connect(backfire_intensity, backfire_intensity_clip)
        p.connect(backfire_intensity_clip, backfire_intensity_named)
        p.connect(backfire_intensity_named, engine)
        p.connect(backfire_intensity_default, backfire_intensity)

        p.comment("Backfire Solo / Test Pop", 500, 315, 175)
        backfire_solo = p.add("toggle", None, 500, 340, 24, 24, numinlets=1, numoutlets=1)
        backfire_solo_named = p.new("prepend backfire_solo", 535, 340, 150, numinlets=1, numoutlets=1)
        backfire_solo_default = p.new("loadmess 0", 695, 340, 80, numinlets=1, numoutlets=1)
        backfire_test = p.add("button", None, 500, 375, 24, 24, numinlets=1, numoutlets=1)
        backfire_test_message = p.message("backfire_test 1", 535, 375, 105)
        p.connect(backfire_solo, backfire_solo_named)
        p.connect(backfire_solo_named, engine)
        p.connect(backfire_solo_default, backfire_solo)
        p.connect(backfire_test, backfire_test_message)
        p.connect(backfire_test_message, engine)
        open_pop = p.message("Open Pop Designer", 800, 340, 130)
        open_pop_instance = p.new(
            f"s open.{profile}.backfire", 800, 375, 180,
            numinlets=1, numoutlets=0,
        )
        p.connect(open_pop, open_pop_instance)

    p.comment("Audio + Output", 760, 105, 120)
    audio_toggle = p.add("toggle", None, 760, 135, 24, 24, numinlets=1, numoutlets=1)
    audio_off = p.new("loadmess 0", 795, 135, 80, numinlets=1, numoutlets=1)
    audio_pack = p.new("pack 0. 60", 760, 175, 85, numinlets=2, numoutlets=1)
    audio_line = p.new("line~", 760, 210, 50, numinlets=2, numoutlets=2)
    gain_l = p.new("*~", 1060, 540, 40, numinlets=2, numoutlets=1)
    gain_r = p.new("*~", 1175, 540, 40, numinlets=2, numoutlets=1)
    dac = p.new("ezdac~", 1115, 635, 65, numinlets=2, numoutlets=0)
    meter_l = p.add("meter~", None, 1035, 585, 18, 80, numinlets=1, numoutlets=1)
    meter_r = p.add("meter~", None, 1225, 585, 18, 80, numinlets=1, numoutlets=1)
    spectrum_l = p.new("spectroscope~", 1260, 540, 220, numinlets=2, numoutlets=0)
    spectrum_r = p.new("spectroscope~", 1260, 680, 220, numinlets=2, numoutlets=0)
    p.connect(audio_off, audio_toggle)
    p.connect(audio_toggle, audio_pack)
    p.connect(audio_toggle, dac)
    p.connect(audio_pack, audio_line)
    p.connect(engine, gain_l, 0, 0)
    p.connect(engine, gain_r, 1, 0)
    p.connect(audio_line, gain_l, 0, 1)
    p.connect(audio_line, gain_r, 0, 1)
    p.connect(gain_l, dac, 0, 0)
    p.connect(gain_r, dac, 0, 1)
    p.connect(gain_l, meter_l)
    p.connect(gain_r, meter_r)
    p.connect(gain_l, spectrum_l)
    p.connect(gain_r, spectrum_r)

    p.comment("Master compressor (attack/release are OMX rates: higher = faster)", 25, 900, 620)
    compressor_ui = (
        ("Threshold dB", "compressor_threshold_db", -12.0, -36.0, 0.0),
        ("Ratio", "compressor_ratio", 2.0, 1.0, 50.0),
        ("Attack rate", "compressor_attack_rate", 85.0, 0.0, 150.0),
        ("Release rate", "compressor_release_rate", 35.0, 0.0, 150.0),
        ("Makeup dB", "compressor_makeup_db", 0.0, -12.0, 12.0),
    )
    for index, (label, name, default, low, high) in enumerate(compressor_ui):
        x = 25 + index * 180
        p.comment(label, x, 928, 130)
        number = p.add("flonum", None, x, 952, 75, numinlets=1, numoutlets=2)
        bounded = p.new(f"clip {low:g} {high:g}", x, 984, 90, numinlets=3, numoutlets=1)
        named = p.new(f"prepend {name}", x, 1016, 155, numinlets=1, numoutlets=1)
        initial = p.new(f"loadmess {default:g}", x + 82, 952, 85, numinlets=1, numoutlets=1)
        p.connect(number, bounded)
        p.connect(initial, number)
        p.connect(bounded, named)
        p.connect(named, engine)
    p.comment("Bypass", 930, 928, 70)
    compressor_bypass = p.add("toggle", None, 930, 952, 24, 24, numinlets=1, numoutlets=1)
    compressor_bypass_named = p.new("prepend compressor_bypass", 965, 952, 175, numinlets=1, numoutlets=1)
    compressor_bypass_default = p.new("loadmess 0", 930, 984, 80, numinlets=1, numoutlets=1)
    p.connect(compressor_bypass_default, compressor_bypass)
    p.connect(compressor_bypass, compressor_bypass_named)
    p.connect(compressor_bypass_named, engine)
    p.comment(f"External control: send named messages to vss.{profile}.input", 650, 900, 480)
    return p.document()


def make_legacy_main() -> dict[str, Any]:
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
        "engine_type ev, ev_weight 1., v12_weight 0., v10_weight 0., aggression 0.25, brightness 0.72, body 0.34, texture 0.20, cabin_width 0.90, cabin_rumble 0., exhaust_boom 0., structure_vibration 0., cabin_ir_mix 0.10, powertrain_level_db -2., transient_level_db -9., road_level_db -14., rumble_level_db -60., pad_level_db -9., pad_mute 0, pad_solo 0, reference_texture_level_db -20., reference_texture_mute 0, master_trim_db -8.",
        "engine_type v12, ev_weight 0., v12_weight 1., v10_weight 0., aggression 0.62, brightness 0.78, body 0.72, texture 0.52, cabin_width 0.82, cabin_rumble 0.90, exhaust_boom 0.62, structure_vibration 0.58, cabin_ir_mix 0.20, powertrain_level_db -3., transient_level_db -7., road_level_db -16., rumble_level_db -5., pad_level_db -3., pad_mute 0, pad_solo 0, reference_texture_level_db -18., reference_texture_mute 0, master_trim_db -8.",
        "engine_type v10, ev_weight 0., v12_weight 0., v10_weight 1., aggression 0.90, brightness 0.66, body 0.84, texture 0.86, cabin_width 0.78, cabin_rumble 0.92, exhaust_boom 0.74, structure_vibration 0.72, cabin_ir_mix 0.18, powertrain_level_db -3., transient_level_db -6., road_level_db -16., rumble_level_db -4., pad_level_db -3., pad_mute 0, pad_solo 0, reference_texture_level_db -18., reference_texture_mute 0, master_trim_db -8.",
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
        p, "EV Pad dB", "pad_level_db", -9.0, 730, 635, engine
    )
    ui_targets["reference_texture_level_db"] = add_labeled_db_number(
        p, "Engine Texture dB", "reference_texture_level_db", -18.0, 930, 635, engine
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
    "ev_powertrain": """// Procedural EV motor: RPM owns pitch; pedal owns bounded torque loudness.
Param rpm(650, min=0, max=10000);
Param throttle(0, min=0, max=1);
Param load(0, min=-1, max=1);
Param aggression(0.25, min=0, max=1);
Param brightness(0.72, min=0, max=1);
Param body(0.34, min=0, max=1);
Param texture(0.2, min=0, max=1);
Param air_detail(0.58, min=0, max=1);
Param cycle_irregularity(0.18, min=0, max=1);
Param stereo_width(0.68, min=0, max=1);
Param throttle_loudness_depth(4.5, min=0, max=8);
Param saturation(0.2, min=0, max=1);
Param torque_ripple_level(0.48, min=0, max=1);
Param gear_mesh_level(0.42, min=0, max=1);
Param electrical_detail(0.64, min=0, max=1);
r = slide(clamp(rpm, 0, 10000), 1200, 1800);
t = slide(clamp(throttle, 0, 1), 700, 1400);
l = abs(clamp(load, -1, 1));
f = clamp(55 + r * 0.052, 55, 760);
throttle_gain = pow(10, (t * throttle_loudness_depth) / 20);
tone_t = 0.62 + t * 0.38;
body_t = 1 - t * 0.12;
a = clamp((0.045 + l * 0.028) * throttle_gain, 0, 0.16);
slow_motion = cycle(clamp(r / 240, 0.35, 30)) * cycle_irregularity;
electrical_motion = 0.985 + slow_motion * 0.018;
aggression_colour = 0.6 + aggression * 1.6;
aggression_air = 0.8 + aggression * 0.8;
torque_ripple = cycle(clamp(f * 0.5, 27.5, 380)) * (0.035 + l * 0.035) * torque_ripple_level * aggression_colour;
gear_l = cycle(clamp(f * 1.49, 82, 1140)) * 0.045 + cycle(clamp(f * 2.23, 124, 1710)) * 0.026;
gear_r = cycle(clamp(f * 1.53, 84, 1160)) * 0.045 + cycle(clamp(f * 2.29, 126, 1750)) * 0.026;
coherent_low = cycle(f) * (0.58 + body * 0.18);
h2 = cycle(clamp(f * 2, 110, 1520)) * (0.08 + body * 0.05);
h3_l = cycle(clamp(f * 3.03, 165, 2320)) * (0.035 + texture * 0.055);
h3_r = cycle(clamp(f * 2.97, 165, 2260)) * (0.035 + texture * 0.055);
inverter_l = cycle(clamp(f * (2.65 + brightness + aggression * 0.64), 150, 4400)) * (0.08 + electrical_detail * 0.16) * tone_t;
inverter_r = cycle(clamp(f * (2.77 + brightness + aggression * 0.64), 155, 4600)) * (0.08 + electrical_detail * 0.16) * tone_t;
air_l = (cycle(clamp(f * 5.37, 300, 7800)) + cycle(clamp(f * 7.11, 420, 11200)) * 0.55) * air_detail * 0.035 * tone_t;
air_r = (cycle(clamp(f * 5.61, 320, 8100)) + cycle(clamp(f * 6.83, 400, 10800)) * 0.55) * air_detail * 0.035 * tone_t;
shared = (coherent_low + torque_ripple + h2) * body_t;
side_l = (h3_l * (0.82 + t * 0.18) + gear_l * gear_mesh_level * (0.76 + t * 0.24)) * aggression_colour + (inverter_l + air_l) * aggression_air;
side_r = (h3_r * (0.82 + t * 0.18) + gear_r * gear_mesh_level * (0.76 + t * 0.24)) * aggression_colour + (inverter_r + air_r) * aggression_air;
left_drive = (shared + side_l * (0.45 + stereo_width * 0.55)) * electrical_motion * a;
right_drive = (shared + side_r * (0.45 + stereo_width * 0.55)) * electrical_motion * a;
sat_drive = 1 + saturation * 0.85;
out1 = tanh(left_drive * sat_drive) / sat_drive;
out2 = tanh(right_drive * sat_drive) / sat_drive;""",
    "v10_powertrain": """// Procedural V10: independent five-cylinder banks, bounded pedal loudness and intake/exhaust colour.
Param rpm(740, min=0, max=10000);
Param throttle(0, min=0, max=1);
Param load(0, min=-1, max=1);
Param accel(0, min=-1, max=1);
Param aggression(0.9, min=0, max=1);
Param brightness(0.66, min=0, max=1);
Param body(0.84, min=0, max=1);
Param texture(0.86, min=0, max=1);
Param engine_running(0, min=0, max=1);
Param combustion_gain(0, min=0, max=1);
Param shift_cut(1, min=0, max=1);
Param air_detail(0.74, min=0, max=1);
Param cycle_irregularity(0.52, min=0, max=1);
Param stereo_width(0.72, min=0, max=1);
Param throttle_loudness_depth(4.5, min=0, max=8);
Param saturation(0.36, min=0, max=1);
Param combustion_pulse(0.88, min=0, max=1);
Param intake_detail(0.82, min=0, max=1);
Param exhaust_detail(0.72, min=0, max=1);
Param residual_detail(0.78, min=0, max=1);
r = slide(clamp(rpm, 0, 10000), 620, 980);
t = slide(clamp(throttle, 0, 1), 360, 760);
l = max(clamp(load, -1, 1), 0);
motion = slide(clamp(accel, -1, 1), 280, 820);
accel_drive = max(motion, 0);
decel_drive = max(-motion, 0);
run = slide(clamp(engine_running * combustion_gain * shift_cut, 0, 1), 420, 1650);
speedmix = clamp((r - 740) / 7560, 0, 1);
idle_weight = 1 - clamp((r - 740) / 1650, 0, 1);
crank = clamp(r / 60, 6, 170);
cycle_variation = cycle(crank * 0.5) * (0.006 + cycle_irregularity * 0.022) + cycle(crank * 2.5) * cycle_irregularity * 0.008;
bank_fire = clamp(crank * 2.5 * (1 + cycle_variation), 16, 450);
fire = bank_fire * 2;
phase_l = phasor(bank_fire);
phase_r = phase_l + 0.5;
phase_r = phase_r - floor(phase_r);
pulse_l = pow(0.5 + 0.5 * cos(phase_l * 6.283185307179586), 4) - 0.2734375;
pulse_r = pow(0.5 + 0.5 * cos(phase_r * 6.283185307179586), 4) - 0.2734375;
throttle_gain = pow(10, (t * throttle_loudness_depth) / 20);
tone_t = 0.58 + t * 0.42;
body_t = 1 - t * 0.16;
a = clamp((0.22 + body * 0.055 + l * 0.045 + accel_drive * 0.025 - decel_drive * 0.020) * throttle_gain, 0, 0.58) * run;
cylinder_l = 0.95 + cycle(crank * 0.5) * (0.025 + cycle_irregularity * 0.040) + cycle(crank * 2.5) * 0.018;
cylinder_r = 0.95 + cycle(crank * 0.53) * (0.025 + cycle_irregularity * 0.040) + cycle(crank * 2.47) * 0.018;
idle_body = (cycle(clamp(crank * 2.55, 28, 260)) * 0.052 + cycle(clamp(crank * 3.65, 38, 430)) * 0.030) * body * idle_weight;
crankcase_body = idle_body;
manifold_l = cycle(clamp(fire * 0.38, 32, 980)) * (0.022 + l * 0.026) * (0.68 + idle_weight * 0.32);
manifold_r = cycle(clamp(fire * 0.405, 34, 1030)) * (0.022 + l * 0.026) * (0.68 + idle_weight * 0.32);
manifold = (manifold_l + manifold_r) * 0.5;
shared_low = cycle(clamp(fire * 0.5, 24, 460)) * (0.075 + body * 0.060) * (1-speedmix*0.50) + idle_body;
brightness_colour = 0.25 + brightness * 1.13636;
orders_l = cycle(fire) * 0.18 + cycle(clamp(fire * 1.5, 45, 1800)) * 0.072 * (0.65 + brightness * 0.53) + cycle(clamp(fire * 2.5, 65, 5200)) * (0.025 + texture * 0.070 + brightness * 0.060);
orders_r = cycle(fire) * 0.17 + cycle(clamp(fire * 1.5, 45, 1800)) * 0.076 * (0.65 + brightness * 0.53) + cycle(clamp(fire * 2.5, 65, 5200)) * (0.021 + texture * 0.074 + brightness * 0.060);
bright_l = (cycle(clamp(fire * 3.17, 90, 7200)) * 0.055 + cycle(clamp(fire * 5.13, 140, 11800)) * 0.032) * air_detail * (0.35 + speedmix * 0.65) * tone_t * brightness_colour;
bright_r = (cycle(clamp(fire * 3.31, 95, 7500)) * 0.055 + cycle(clamp(fire * 4.87, 135, 11500)) * 0.032) * air_detail * (0.35 + speedmix * 0.65) * tone_t * brightness_colour;
intake_l = cycle(clamp(fire * 1.23, 45, 2700)) * intake_detail * (0.020 + t * 0.030 + accel_drive * 0.038);
intake_r = cycle(clamp(fire * 1.29, 45, 2800)) * intake_detail * (0.020 + t * 0.030 + accel_drive * 0.038);
exhaust_l = cycle(clamp(fire * 0.67, 32, 1500)) * exhaust_detail * (t * 0.030 + accel_drive * 0.032 + decel_drive * 0.032);
exhaust_r = cycle(clamp(fire * 0.71, 34, 1580)) * exhaust_detail * (t * 0.030 + accel_drive * 0.032 + decel_drive * 0.032);
residual_l = (cycle(clamp(fire * 1.37, 40, 2300)) * 0.050 + cycle(clamp(fire * 2.23, 65, 4300)) * 0.032) * abs(pulse_l) * residual_detail;
residual_r = (cycle(clamp(fire * 1.43, 42, 2400)) * 0.050 + cycle(clamp(fire * 2.17, 65, 4200)) * 0.032) * abs(pulse_r) * residual_detail;
bank_l = pulse_l * cylinder_l * (0.42 + combustion_pulse * 0.24);
bank_r = pulse_r * cylinder_r * (0.42 + combustion_pulse * 0.24);
bank_mid = (bank_l + bank_r) * 0.5;
bank_side = (bank_l - bank_r) * 0.5;
bank_spread = 0.28 + stereo_width * 0.32;
side_gain = 0.35 + stereo_width * 0.40;
left_drive = ((shared_low + bank_mid) * body_t + bank_side * bank_spread + (manifold_l + orders_l + bright_l + intake_l + exhaust_l + residual_l) * side_gain) * a * (0.88 + aggression * 0.12);
right_drive = ((shared_low + bank_mid) * body_t - bank_side * bank_spread + (manifold_r + orders_r + bright_r + intake_r + exhaust_r + residual_r) * side_gain) * a * (0.88 + aggression * 0.12);
sat_drive = 1 + saturation * 0.95;
out1 = tanh(left_drive * sat_drive) / sat_drive;
out2 = tanh(right_drive * sat_drive) / sat_drive;""",
    "v12_powertrain": """// Procedural V12: smooth independent six-cylinder banks with high-order air.
Param rpm(780, min=0, max=10000);
Param throttle(0, min=0, max=1);
Param load(0, min=-1, max=1);
Param accel(0, min=-1, max=1);
Param aggression(0.62, min=0, max=1);
Param brightness(0.78, min=0, max=1);
Param body(0.72, min=0, max=1);
Param texture(0.52, min=0, max=1);
Param engine_running(0, min=0, max=1);
Param combustion_gain(0, min=0, max=1);
Param shift_cut(1, min=0, max=1);
Param air_detail(0.68, min=0, max=1);
Param cycle_irregularity(0.34, min=0, max=1);
Param stereo_width(0.64, min=0, max=1);
Param throttle_loudness_depth(4.5, min=0, max=8);
Param saturation(0.28, min=0, max=1);
Param combustion_pulse(0.80, min=0, max=1);
Param intake_detail(0.68, min=0, max=1);
Param exhaust_detail(0.62, min=0, max=1);
Param residual_detail(0.64, min=0, max=1);
r = slide(clamp(rpm, 0, 10000), 700, 1100);
t = slide(clamp(throttle, 0, 1), 420, 850);
l = max(clamp(load, -1, 1), 0);
motion = slide(clamp(accel, -1, 1), 320, 900);
accel_drive = max(motion, 0);
decel_drive = max(-motion, 0);
run = slide(clamp(engine_running * combustion_gain * shift_cut, 0, 1), 480, 1900);
speedmix = clamp((r - 780) / 8220, 0, 1);
idle_weight = 1 - clamp((r - 780) / 1800, 0, 1);
crank = clamp(r / 60, 6, 170);
cycle_variation = cycle(crank * 0.5) * (0.004 + cycle_irregularity * 0.016) + cycle(crank * 1.5) * cycle_irregularity * 0.006;
bank_fire = clamp(crank * 3 * (1 + cycle_variation), 18, 525);
fire = bank_fire * 2;
phase_l = phasor(bank_fire);
phase_r = phase_l + 0.5;
phase_r = phase_r - floor(phase_r);
pulse_l = pow(0.5 + 0.5 * cos(phase_l * 6.283185307179586), 4) - 0.2734375;
pulse_r = pow(0.5 + 0.5 * cos(phase_r * 6.283185307179586), 4) - 0.2734375;
throttle_gain = pow(10, (t * throttle_loudness_depth) / 20);
tone_t = 0.62 + t * 0.38;
body_t = 1 - t * 0.14;
a = clamp((0.205 + body * 0.050 + l * 0.040 + accel_drive * 0.022 - decel_drive * 0.016) * throttle_gain, 0, 0.54) * run;
cylinder_l = 0.97 + cycle(crank * 0.5) * (0.018 + cycle_irregularity * 0.030) + cycle(crank * 1.5) * 0.012;
cylinder_r = 0.97 + cycle(crank * 0.48) * (0.018 + cycle_irregularity * 0.030) + cycle(crank * 1.53) * 0.012;
idle_body = (cycle(clamp(crank * 2.6, 28, 260)) * 0.040 + cycle(clamp(crank * 3.8, 38, 420)) * 0.024) * body * idle_weight;
crankcase_body = idle_body;
manifold_l = cycle(clamp(fire * 0.42, 32, 950)) * (0.018 + l * 0.020) * (0.65 + idle_weight * 0.35);
manifold_r = cycle(clamp(fire * 0.445, 34, 1000)) * (0.018 + l * 0.020) * (0.65 + idle_weight * 0.35);
manifold = (manifold_l + manifold_r) * 0.5;
shared_low = cycle(clamp(fire * 0.5, 24, 520)) * (0.062 + body * 0.050) * (1-speedmix*0.55) + idle_body;
orders_l = cycle(fire) * 0.17 + cycle(clamp(fire * 2.0, 45, 3200)) * (0.10 + brightness * 0.10) + cycle(clamp(fire * 3.0, 55, 5200)) * (0.06 + texture * 0.07);
orders_r = cycle(fire) * 0.165 + cycle(clamp(fire * 2.0, 45, 3200)) * (0.096 + brightness * 0.104) + cycle(clamp(fire * 3.0, 55, 5200)) * (0.064 + texture * 0.066);
bright_l = (cycle(clamp(fire * 4.11, 90, 8000)) * 0.050 + cycle(clamp(fire * 6.17, 130, 12000)) * 0.026) * air_detail * (0.30 + speedmix * 0.70) * tone_t;
bright_r = (cycle(clamp(fire * 3.89, 85, 7700)) * 0.050 + cycle(clamp(fire * 5.83, 125, 11800)) * 0.026) * air_detail * (0.30 + speedmix * 0.70) * tone_t;
intake_l = cycle(clamp(fire * 1.49, 45, 2500)) * intake_detail * (0.016 + t * 0.024 + accel_drive * 0.030);
intake_r = cycle(clamp(fire * 1.53, 45, 2600)) * intake_detail * (0.016 + t * 0.024 + accel_drive * 0.030);
exhaust_l = cycle(clamp(fire * 0.73, 32, 1300)) * exhaust_detail * (t * 0.024 + accel_drive * 0.026 + decel_drive * 0.026);
exhaust_r = cycle(clamp(fire * 0.77, 34, 1380)) * exhaust_detail * (t * 0.024 + accel_drive * 0.026 + decel_drive * 0.026);
residual_l = (cycle(clamp(fire * 1.33, 40, 2200)) * 0.042 + cycle(clamp(fire * 2.17, 65, 4200)) * 0.026) * abs(pulse_l) * residual_detail;
residual_r = (cycle(clamp(fire * 1.39, 42, 2300)) * 0.042 + cycle(clamp(fire * 2.11, 65, 4100)) * 0.026) * abs(pulse_r) * residual_detail;
bank_l = pulse_l * cylinder_l * (0.40 + combustion_pulse * 0.22);
bank_r = pulse_r * cylinder_r * (0.40 + combustion_pulse * 0.22);
bank_mid = (bank_l + bank_r) * 0.5;
bank_side = (bank_l - bank_r) * 0.5;
bank_spread = 0.26 + stereo_width * 0.30;
side_gain = 0.34 + stereo_width * 0.38;
left_drive = ((shared_low + bank_mid) * body_t + bank_side * bank_spread + (manifold_l + orders_l + bright_l + intake_l + exhaust_l + residual_l) * side_gain) * a * (0.86 + aggression * 0.14);
right_drive = ((shared_low + bank_mid) * body_t - bank_side * bank_spread + (manifold_r + orders_r + bright_r + intake_r + exhaust_r + residual_r) * side_gain) * a * (0.86 + aggression * 0.14);
sat_drive = 1 + saturation * 0.85;
out1 = tanh(left_drive * sat_drive) / sat_drive;
out2 = tanh(right_drive * sat_drive) / sat_drive;""",
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
        "reference_texture_level_db": -18.0,
        "reference_texture_mute": 0.0,
        "ev_weight": 0.0,
        "texture": 0.86,
        "air_detail": 0.74,
        "cycle_irregularity": 0.52,
        "stereo_width": 0.72,
        "throttle_loudness_depth": 4.5,
        "saturation": 0.36,
        "combustion_pulse": 0.88,
        "intake_detail": 0.82,
        "exhaust_detail": 0.72,
        "residual_detail": 0.78,
        "v10_weight": 1.0,
        "v12_weight": 0.0,
        "master_trim_db": -8.0,
        "compressor_threshold_db": -12.0,
        "compressor_ratio": 2.0,
        "compressor_attack_rate": 85.0,
        "compressor_release_rate": 35.0,
        "compressor_makeup_db": 0.0,
        "compressor_bypass": 0.0,
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
        "pad_level_db": -9.0,
        "pad_mute": 0.0,
        "pad_solo": 0.0,
        "reference_texture_level_db": -20.0,
        "reference_texture_mute": 0.0,
        "ev_weight": 1.0,
        "texture": 0.20,
        "air_detail": 0.58,
        "cycle_irregularity": 0.18,
        "stereo_width": 0.68,
        "throttle_loudness_depth": 4.5,
        "saturation": 0.20,
        "torque_ripple_level": 0.48,
        "gear_mesh_level": 0.42,
        "electrical_detail": 0.64,
        "v10_weight": 0.0,
        "v12_weight": 0.0,
        "master_trim_db": -8.0,
        "compressor_threshold_db": -12.0,
        "compressor_ratio": 2.0,
        "compressor_attack_rate": 85.0,
        "compressor_release_rate": 35.0,
        "compressor_makeup_db": 0.0,
        "compressor_bypass": 0.0,
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
        "reference_texture_level_db": -18.0,
        "reference_texture_mute": 0.0,
        "ev_weight": 0.0,
        "texture": 0.52,
        "air_detail": 0.68,
        "cycle_irregularity": 0.34,
        "stereo_width": 0.64,
        "throttle_loudness_depth": 4.5,
        "saturation": 0.28,
        "combustion_pulse": 0.80,
        "intake_detail": 0.68,
        "exhaust_detail": 0.62,
        "residual_detail": 0.64,
        "v10_weight": 0.0,
        "v12_weight": 1.0,
        "master_trim_db": -8.0,
        "compressor_threshold_db": -12.0,
        "compressor_ratio": 2.0,
        "compressor_attack_rate": 85.0,
        "compressor_release_rate": 35.0,
        "compressor_makeup_db": 0.0,
        "compressor_bypass": 0.0,
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
        "VehicleSoundSynth-EV.maxpat",
        "VehicleSoundSynth-V10.maxpat",
        "VehicleSoundSynth-V12.maxpat",
        "patchers/ev_powertrain~.maxpat",
        "patchers/v10_powertrain~.maxpat",
        "patchers/v12_powertrain~.maxpat",
        "patchers/vehicle_bus_eq~.maxpat",
        "patchers/cinematic_soundscape_beap~.maxpat",
        "patchers/cinematic_soundscape_voice.maxpat",
        "patchers/cabin_rumble~.maxpat",
        "patchers/transient~.maxpat",
        "patchers/transient_ev~.maxpat",
        "patchers/transient_v10~.maxpat",
        "patchers/transient_v12~.maxpat",
        "patchers/engine_start_beap~.maxpat",
        "patchers/engine_start_core~.maxpat",
        "patchers/engine_start_voice.maxpat",
        "patchers/backfire_burst_scheduler.maxpat",
        "patchers/road_air~.maxpat",
        "patchers/cabin_master~.maxpat",
        "patchers/mix_master~.maxpat",
        "patchers/keyboard_drive_ws.maxpat",
        "patchers/manual_input.maxpat",
    ]
    for profile in ("ev", "v10", "v12"):
        patchers.extend(
            (
                f"patchers/{profile}_sound_dna~.maxpat",
                f"patchers/vehicle_engine_{profile}~.maxpat",
                f"patchers/engine_controller_{profile}.maxpat",
                f"patchers/drive_simulator_{profile}.maxpat",
                f"patchers/{profile}_cinematic_soundscape_host~.maxpat",
            )
        )
    for profile in ("v10", "v12"):
        patchers.extend(
            (
                f"patchers/{profile}_backfire_beap~.maxpat",
                f"patchers/{profile}_backfire_host~.maxpat",
            )
        )
    for name in patchers:
        contents["patchers"][name] = {"kind": "patcher", "local": 1}
    for name in GEN_CODE:
        contents["code"][f"gen/{name}.gendsp"] = {"kind": "gendsp", "local": 1}
    contents["code"]["code/drive_model.js"] = {"kind": "javascript", "local": 1}
    contents["code"]["code/manual_input.js"] = {"kind": "javascript", "local": 1}
    contents["code"]["code/eq_state_path.js"] = {"kind": "javascript", "local": 1}
    contents["code"]["code/dna_state_path.js"] = {"kind": "javascript", "local": 1}
    contents["code"]["code/backfire_burst.js"] = {"kind": "javascript", "local": 1}
    for name in MEDIA_FRAMES:
        if name.startswith(("cabin_ir_", "starter_")):
            contents["media"][f"media/{name}.wav"] = {"kind": "mediafile", "local": 1}
    contents["data"]["presets/sound_dna.json"] = {"kind": "data", "local": 1}
    contents["data"]["presets/vehicle_bus_eq_default.json"] = {"kind": "data", "local": 1}
    contents["data"]["assets/ferrari_sf90_acoustic_target.json"] = {"kind": "data", "local": 1}
    contents["data"]["assets/ferrari_v10_lifecycle_targets.json"] = {"kind": "data", "local": 1}
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
    root = root.resolve()
    (root / "presets" / "local").mkdir(parents=True, exist_ok=True)
    stale_signal_independent_rumble = root / "gen" / "cabin_rumble.gendsp"
    if stale_signal_independent_rumble.is_file():
        stale_signal_independent_rumble.unlink()
    outputs = {
        "main.maxpat": make_launcher(),
        "VehicleSoundSynth-EV.maxpat": make_profile_main("ev", root),
        "VehicleSoundSynth-V10.maxpat": make_profile_main("v10", root),
        "VehicleSoundSynth-V12.maxpat": make_profile_main("v12", root),
        "patchers/vehicle_engine~.maxpat": make_engine(),
        "patchers/engine_controller.maxpat": make_engine_controller(),
        "patchers/powertrain~.maxpat": make_powertrain(),
        "patchers/ev_powertrain~.maxpat": make_profile_powertrain("ev"),
        "patchers/v10_powertrain~.maxpat": make_profile_powertrain("v10"),
        "patchers/v12_powertrain~.maxpat": make_profile_powertrain("v12"),
        "patchers/ev_pad_driver~.maxpat": make_ev_pad_driver(),
        "patchers/ev_soundscape_host~.maxpat": make_ev_soundscape_host(),
        "patchers/ev_relax_voice.maxpat": make_ev_mode_voice("relax"),
        "patchers/ev_expressive_voice.maxpat": make_ev_mode_voice("expressive"),
        "patchers/ev_sport_voice.maxpat": make_ev_mode_voice("sport"),
        "patchers/cinematic_soundscape_voice.maxpat": make_cinematic_soundscape_voice(),
        "patchers/reference_texture~.maxpat": make_reference_texture(),
        "patchers/cabin_rumble~.maxpat": make_cabin_rumble(),
        "patchers/transient~.maxpat": make_transient(),
        "patchers/transient_ev~.maxpat": make_profile_transient("ev"),
        "patchers/transient_v10~.maxpat": make_profile_transient("v10"),
        "patchers/transient_v12~.maxpat": make_profile_transient("v12"),
        "patchers/engine_start_core~.maxpat": make_engine_start_core(),
        "patchers/engine_start_voice.maxpat": make_engine_start_voice(),
        "patchers/backfire_burst_scheduler.maxpat": make_backfire_burst_scheduler(),
        "patchers/road_air~.maxpat": make_road_air(),
        "patchers/cabin_master~.maxpat": make_cabin_master(),
        "patchers/mix_master~.maxpat": make_mix_master(),
        "patchers/drive_simulator.maxpat": make_drive_simulator(),
        "patchers/keyboard_drive_ws.maxpat": make_keyboard_drive_ws(),
        "patchers/manual_input.maxpat": make_manual_input(),
        "presets/sound_dna.json": PRESETS,
        "presets/vehicle_bus_eq_default.json": VEHICLE_BUS_EQ_DEFAULT,
        PROJECT_FILENAME: project_file(),
    }
    for profile in ("v10", "v12"):
        outputs[f"patchers/{profile}_pad_voice.maxpat"] = make_ice_pad_voice(profile)
        outputs[f"patchers/{profile}_pad_host~.maxpat"] = make_ice_pad_host(profile)
        outputs[f"patchers/{profile}_backfire_host~.maxpat"] = make_ice_backfire_host(profile)
    for profile in ("ev", "v10", "v12"):
        outputs[f"patchers/{profile}_cinematic_soundscape_host~.maxpat"] = make_cinematic_soundscape_host(profile)
        outputs[f"patchers/vehicle_engine_{profile}~.maxpat"] = make_profile_engine(profile)
        outputs[f"patchers/engine_controller_{profile}.maxpat"] = make_profile_controller(profile)
        outputs[f"patchers/drive_simulator_{profile}.maxpat"] = make_profile_drive_simulator(profile)
    resource_roots = {
        "../gen/": "Patcher:/gen/",
        "../code/": "Patcher:/code/",
        "../media/local/": "Patcher:/media/local/",
        "../media/": "Patcher:/media/",
    }
    for relative_path, value in outputs.items():
        if relative_path.endswith(".maxpat"):
            for item in value["patcher"]["boxes"]:
                text = item["box"].get("text")
                if text:
                    for source, resolved in resource_roots.items():
                        text = text.replace(source, resolved)
                    item["box"]["text"] = text
        write_json(root / relative_path, value)
    user_pad = root / "patchers" / "ev_pad_beap~.maxpat"
    if not user_pad.exists():
        write_json(user_pad, make_ev_pad_beap())
    for mode in ("expressive", "sport"):
        user_mode = root / "patchers" / f"ev_{mode}_beap~.maxpat"
        if not user_mode.exists():
            write_json(user_mode, make_ev_mode_beap(mode))
    user_start = root / "patchers" / "engine_start_beap~.maxpat"
    if not user_start.exists():
        write_json(user_start, make_engine_start_beap())
    shared_soundscape = root / "patchers" / "cinematic_soundscape_beap~.maxpat"
    if not shared_soundscape.exists():
        write_json(shared_soundscape, make_cinematic_soundscape_beap())
    user_eq = root / "patchers" / "vehicle_bus_eq~.maxpat"
    if not user_eq.exists():
        write_json(user_eq, make_vehicle_bus_eq())
    for profile in ("ev", "v10", "v12"):
        user_dna = root / "patchers" / f"{profile}_sound_dna~.maxpat"
        if not user_dna.exists():
            write_json(user_dna, make_sound_dna(profile))
    for profile in ("v10", "v12"):
        user_pad = root / "patchers" / f"{profile}_pad_beap~.maxpat"
        if not user_pad.exists():
            write_json(user_pad, make_ice_pad_beap(profile))
        user_backfire = root / "patchers" / f"{profile}_backfire_beap~.maxpat"
        if not user_backfire.exists():
            write_json(user_backfire, make_ice_backfire_beap(profile))
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
