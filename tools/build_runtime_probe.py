#!/usr/bin/env python3
"""Build a monitor-muted Max patch for EV/V12/V10 runtime renders."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

try:
    from .build_project import DNA_PARAMETER_SPECS, Patcher, write_json
except ImportError:  # Direct script execution from tools/.
    from build_project import DNA_PARAMETER_SPECS, Patcher, write_json


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
    "ioniq6n": {
        "rpm": 650.0,
        "weights": (1.0, 0.0, 0.0),
        "rumble": (0.0, 0.0, 0.0),
        "ir_mix": 0.08,
    },
    "ferrari": {
        "rpm": 740.0,
        "weights": (0.0, 0.0, 1.0),
        "rumble": (0.92, 0.74, 0.72),
        "ir_mix": 0.18,
    },
}

DSP_SETTLE_MS = 6000

def backfire_solo_scenario(profile: str, intensity: float) -> dict:
    message = (
        "ignition 1, engine_running 1, backfire_enable 1, "
        f"backfire_intensity {intensity:g}, overrun 0.95"
    )
    return {
        "profile": profile, "rpm": 4200.0, "lock_rpm": True,
        "event": message,
        "direct_event_to_transient": True,
        "extra_messages": (
            "backfire_enable 1", f"backfire_intensity {intensity:g}",
            "backfire_solo 1", "backfire_seed 1017" if profile == "v10" else "backfire_seed 1219",
        ),
    }


def start_scenario(profile: str, style: str) -> dict:
    return {
        "profile": profile,
        "event": "starter 1",
        "event_at_ms": 200,
        "direct_event_to_transient": True,
        "extra_messages": (f"start_style {style}",),
    }


def controller_start_scenario(profile: str, style: str) -> dict:
    return {
        "profile": profile,
        "event": "start 1",
        "event_at_ms": 200,
        "start_enabled": False,
        "extra_messages": (f"engine_type {profile}", f"start_style {style}"),
    }


def backfire_test_scenario(profile: str) -> dict:
    return {
        "profile": profile,
        "rpm": 1800.0,
        "lock_rpm": True,
        "event": "backfire_test 1",
        "event_at_ms": 200,
        "direct_event_to_transient": True,
        "ignition_enabled": False,
        "extra_messages": (
            "backfire_intensity 0.82" if profile == "v10" else "backfire_intensity 0.55",
            "backfire_solo 1", "backfire_seed 1017" if profile == "v10" else "backfire_seed 1219",
        ),
    }


def backfire_single_scenario(profile: str) -> dict:
    """Render one host-audition hit without the physical burst scheduler."""
    return {
        "profile": profile,
        "rpm": 1800.0,
        "lock_rpm": True,
        "global_event_address": f"{profile}.pop.audition_one_hit",
        "event_at_ms": 200,
        "start_enabled": False,
        "ignition_enabled": False,
        "extra_messages": (
            "backfire_solo 1",
            "transient_level_db -7" if profile == "v10" else "transient_level_db -8",
        ),
    }


SCENARIOS = {
    "idle-v12": {"profile": "v12", "rpm": 780.0},
    "idle-v10": {"profile": "v10", "rpm": 740.0},
    "high-v12-3500": {"profile": "v12", "rpm": 3500.0, "throttle": 0.72, "load": 0.65, "lock_rpm": True},
    "high-v10-4200": {"profile": "v10", "rpm": 4200.0, "throttle": 0.78, "load": 0.70, "lock_rpm": True},
    "v10-backfire-single-solo": backfire_single_scenario("v10"),
    "v12-backfire-single-solo": backfire_single_scenario("v12"),
    # Fixed-state acoustic A/B probes: throttle may change level and spectral
    # colour, but the locked RPM keeps every engine-order frequency unchanged.
    "dna-ev-throttle-low": {
        "profile": "ev", "rpm": 3200.0, "throttle": 0.10, "load": 0.55,
        "lock_rpm": True, "direct_powertrain": True,
        "extra_messages": ("accel 0", "speed_kph 0"),
    },
    "dna-ev-throttle-high": {
        "profile": "ev", "rpm": 3200.0, "throttle": 0.90, "load": 0.55,
        "lock_rpm": True, "direct_powertrain": True,
        "extra_messages": ("accel 0", "speed_kph 0"),
    },
    "dna-ev-aggression-low": {
        "profile": "ev", "rpm": 3200.0, "throttle": 0.65, "load": 0.55,
        "lock_rpm": True, "direct_powertrain": True,
        "extra_messages": ("accel 0", "speed_kph 0", "aggression 0"),
    },
    "dna-ev-aggression-high": {
        "profile": "ev", "rpm": 3200.0, "throttle": 0.65, "load": 0.55,
        "lock_rpm": True, "direct_powertrain": True,
        "extra_messages": ("accel 0", "speed_kph 0", "aggression 1"),
    },
    "dna-v10-throttle-low": {
        "profile": "v10", "rpm": 4200.0, "throttle": 0.10, "load": 0.65,
        "lock_rpm": True, "direct_powertrain": True, "extra_messages": (
            "accel 0", "speed_kph 0", "engine_running 1",
            "combustion_gain 1", "shift_cut 1", "starter 0",
        ),
    },
    "dna-v10-throttle-high": {
        "profile": "v10", "rpm": 4200.0, "throttle": 0.90, "load": 0.65,
        "lock_rpm": True, "direct_powertrain": True, "extra_messages": (
            "accel 0", "speed_kph 0", "engine_running 1",
            "combustion_gain 1", "shift_cut 1", "starter 0",
        ),
    },
    "dna-v10-brightness-low": {
        "profile": "v10", "rpm": 4200.0, "throttle": 0.65, "load": 0.65,
        "lock_rpm": True, "direct_powertrain": True, "extra_messages": (
            "accel 0", "speed_kph 0", "engine_running 1", "brightness 0",
            "combustion_gain 1", "shift_cut 1", "starter 0",
        ),
    },
    "dna-v10-brightness-high": {
        "profile": "v10", "rpm": 4200.0, "throttle": 0.65, "load": 0.65,
        "lock_rpm": True, "direct_powertrain": True, "extra_messages": (
            "accel 0", "speed_kph 0", "engine_running 1", "brightness 1",
            "combustion_gain 1", "shift_cut 1", "starter 0",
        ),
    },
    "dna-v12-throttle-low": {
        "profile": "v12", "rpm": 4500.0, "throttle": 0.10, "load": 0.65,
        "lock_rpm": True, "direct_powertrain": True, "extra_messages": (
            "accel 0", "speed_kph 0", "engine_running 1",
            "combustion_gain 1", "shift_cut 1", "starter 0",
        ),
    },
    "dna-v12-throttle-high": {
        "profile": "v12", "rpm": 4500.0, "throttle": 0.90, "load": 0.65,
        "lock_rpm": True, "direct_powertrain": True, "extra_messages": (
            "accel 0", "speed_kph 0", "engine_running 1",
            "combustion_gain 1", "shift_cut 1", "starter 0",
        ),
    },
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
    "ev-soundscape-solo-low-load": {
        "profile": "ev", "rpm": 1800.0, "throttle": 0.10, "load": 0.10,
        "lock_rpm": True, "direct_soundscape_state": True, "soundscape_enable": 1,
        "soundscape_level_db": -3.0, "soundscape_solo": 1,
    },
    "ev-soundscape-solo-idle": {
        "profile": "ev", "rpm": 0.0, "throttle": 0.0, "load": 0.0,
        "lock_rpm": True, "direct_soundscape_state": True, "soundscape_enable": 1,
        "soundscape_level_db": -3.0, "soundscape_solo": 1,
    },
    "ev-soundscape-solo-high-load": {
        "profile": "ev", "rpm": 1800.0, "throttle": 0.90, "load": 0.85,
        "lock_rpm": True, "direct_soundscape_state": True, "soundscape_enable": 1,
        "soundscape_level_db": -3.0, "soundscape_solo": 1,
    },
    "v10-soundscape-on": {
        "profile": "v10", "rpm": 1800.0, "throttle": 0.35, "lock_rpm": True,
        "soundscape_level_db": -8.0, "soundscape_enable": 1,
    },
    "v10-soundscape-off": {
        "profile": "v10", "rpm": 1800.0, "throttle": 0.35, "lock_rpm": True,
        "soundscape_enable": 0,
    },
    "v10-soundscape-solo-low-load": {
        "profile": "v10", "rpm": 1800.0, "throttle": 0.10, "load": 0.10,
        "lock_rpm": True, "direct_soundscape_state": True, "soundscape_enable": 1,
        "soundscape_level_db": -6.0, "soundscape_solo": 1,
    },
    "v10-soundscape-solo-high-load": {
        "profile": "v10", "rpm": 1800.0, "throttle": 0.90, "load": 0.85,
        "lock_rpm": True, "direct_soundscape_state": True, "soundscape_enable": 1,
        "soundscape_level_db": -6.0, "soundscape_solo": 1,
    },
    "v10-soundscape-solo-idle": {
        "profile": "v10", "rpm": 740.0, "throttle": 0.04, "load": 0.12,
        "lock_rpm": True, "direct_soundscape_state": True, "soundscape_enable": 1,
        "soundscape_level_db": -6.0, "soundscape_solo": 1,
    },
    "v10-soundscape-prestart": {
        "profile": "v10", "rpm": 740.0, "throttle": 0.0, "load": 0.0,
        "lock_rpm": True, "direct_soundscape_state": True, "soundscape_enable": 1,
        "soundscape_level_db": -6.0, "soundscape_solo": 1,
        "extra_messages": ("start 0",),
    },
    "v10-soundscape-start-gate": {
        "profile": "v10", "rpm": 740.0, "throttle": 0.0, "load": 0.0,
        "lock_rpm": True, "direct_soundscape_state": True, "soundscape_enable": 1,
        "soundscape_level_db": -6.0, "soundscape_solo": 1,
        "extra_messages": ("start 0",), "event": "start 1", "event_at_ms": 3000,
    },
    "v12-soundscape-on": {
        "profile": "v12", "rpm": 1800.0, "throttle": 0.35, "lock_rpm": True,
        "soundscape_level_db": -9.0, "soundscape_enable": 1,
    },
    "v12-soundscape-off": {
        "profile": "v12", "rpm": 1800.0, "throttle": 0.35, "lock_rpm": True,
        "soundscape_enable": 0,
    },
    "v12-soundscape-solo-low-load": {
        "profile": "v12", "rpm": 1800.0, "throttle": 0.10, "load": 0.10,
        "lock_rpm": True, "direct_soundscape_state": True, "soundscape_enable": 1,
        "soundscape_level_db": -7.0, "soundscape_solo": 1,
    },
    "v12-soundscape-solo-high-load": {
        "profile": "v12", "rpm": 1800.0, "throttle": 0.90, "load": 0.85,
        "lock_rpm": True, "direct_soundscape_state": True, "soundscape_enable": 1,
        "soundscape_level_db": -7.0, "soundscape_solo": 1,
    },
    "v12-soundscape-solo-idle": {
        "profile": "v12", "rpm": 780.0, "throttle": 0.04, "load": 0.12,
        "lock_rpm": True, "direct_soundscape_state": True, "soundscape_enable": 1,
        "soundscape_level_db": -7.0, "soundscape_solo": 1,
    },
    "ferrari-soundscape-solo-low-load": {
        "profile": "ferrari", "rpm": 1800.0, "throttle": 0.10, "load": 0.10,
        "lock_rpm": True, "direct_soundscape_state": True, "soundscape_enable": 1,
        "soundscape_level_db": -6.0, "soundscape_solo": 1,
    },
    "ferrari-soundscape-solo-high-load": {
        "profile": "ferrari", "rpm": 1800.0, "throttle": 0.90, "load": 0.85,
        "lock_rpm": True, "direct_soundscape_state": True, "soundscape_enable": 1,
        "soundscape_level_db": -6.0, "soundscape_solo": 1,
    },
    "ferrari-soundscape-solo-idle": {
        "profile": "ferrari", "rpm": 740.0, "throttle": 0.04, "load": 0.12,
        "lock_rpm": True, "direct_soundscape_state": True, "soundscape_enable": 1,
        "soundscape_level_db": -6.0, "soundscape_solo": 1,
    },
    "ferrari-start-cinematic": start_scenario("ferrari", "cinematic"),
    "ferrari-start-controller-cinematic": controller_start_scenario("ferrari", "cinematic"),
    "ferrari-backfire-solo": backfire_solo_scenario("ferrari", 0.65),
    "ferrari-idle": {
        "profile": "ferrari", "rpm": 740.0, "throttle": 0.04, "load": 0.12,
        "lock_rpm": True, "extra_messages": ("accel 0",),
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
    "v10-backfire-overrun-solo": {
        "profile": "v10", "rpm": 4200.0, "lock_rpm": True,
        "event": (
            "ignition 1, engine_running 1, backfire_enable 1, "
            "backfire_intensity 1, overrun 0.95"
        ),
        "direct_event_to_transient": True,
        "extra_messages": ("backfire_enable 1", "backfire_intensity 1", "backfire_solo 1"),
    },
    "v12-backfire-overrun-solo": {
        "profile": "v12", "rpm": 4200.0, "lock_rpm": True,
        "event": (
            "ignition 1, engine_running 1, backfire_enable 1, "
            "backfire_intensity 1, overrun 0.95"
        ),
        "direct_event_to_transient": True,
        "extra_messages": ("backfire_enable 1", "backfire_intensity 1", "backfire_solo 1"),
    },
    "v10-backfire-solo-low": backfire_solo_scenario("v10", 0.25),
    "v10-backfire-solo-default": backfire_solo_scenario("v10", 0.82),
    "v10-backfire-solo-high": backfire_solo_scenario("v10", 1.0),
    "v12-backfire-solo-low": backfire_solo_scenario("v12", 0.25),
    "v12-backfire-solo-default": backfire_solo_scenario("v12", 0.55),
    "v12-backfire-solo-high": backfire_solo_scenario("v12", 1.0),
    "v10-backfire-test-solo": backfire_test_scenario("v10"),
    "v12-backfire-test-solo": backfire_test_scenario("v12"),
    "v10-start-cinematic": start_scenario("v10", "cinematic"),
    "v10-start-realistic": start_scenario("v10", "realistic"),
    "v12-start-cinematic": start_scenario("v12", "cinematic"),
    "v12-start-realistic": start_scenario("v12", "realistic"),
    "ev-start-cinematic": start_scenario("ev", "cinematic"),
    "v10-start-controller-cinematic": controller_start_scenario("v10", "cinematic"),
    "v12-start-controller-cinematic": controller_start_scenario("v12", "cinematic"),
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
    "ioniq6n-activation": {
        "profile": "ioniq6n", "rpm": 650.0, "start_enabled": False,
        "lock_rpm": True,
        "event": "start 1", "event_at_ms": 250,
        "direct_event_to_transient": True,
        "extra_messages": ("ignition 1", "start_level_db -7"),
    },
    "ioniq6n-ready": {
        "profile": "ioniq6n", "rpm": 650.0, "throttle": 0.0, "load": 0.0,
        "lock_rpm": True,
        "extra_messages": ("engine_running 1", "shift_cut 1", "n_sound_mode evolution"),
    },
    "ioniq6n-ignition-low-load": {
        "profile": "ioniq6n", "rpm": 3600.0, "throttle": 0.12, "load": 0.12,
        "lock_rpm": True, "direct_soundscape_state": True,
        "soundscape_enable": 1, "soundscape_level_db": -6.0, "soundscape_solo": 1,
        "extra_messages": ("n_sound_mode ignition", "speed_kph 80", "engine_running 1"),
    },
    "ioniq6n-ignition-high-load": {
        "profile": "ioniq6n", "rpm": 3600.0, "throttle": 0.90, "load": 0.88,
        "lock_rpm": True, "direct_soundscape_state": True,
        "soundscape_enable": 1, "soundscape_level_db": -6.0, "soundscape_solo": 1,
        "extra_messages": ("n_sound_mode ignition", "speed_kph 80", "engine_running 1"),
    },
    "ioniq6n-evolution-low-load": {
        "profile": "ioniq6n", "rpm": 3600.0, "throttle": 0.12, "load": 0.12,
        "lock_rpm": True, "direct_soundscape_state": True,
        "soundscape_enable": 1, "soundscape_level_db": -6.0, "soundscape_solo": 1,
        "extra_messages": ("n_sound_mode evolution", "speed_kph 80", "engine_running 1"),
    },
    "ioniq6n-evolution-high-load": {
        "profile": "ioniq6n", "rpm": 3600.0, "throttle": 0.90, "load": 0.88,
        "lock_rpm": True, "direct_soundscape_state": True,
        "soundscape_enable": 1, "soundscape_level_db": -6.0, "soundscape_solo": 1,
        "extra_messages": ("n_sound_mode evolution", "speed_kph 80", "engine_running 1"),
    },
    "ioniq6n-lightspeed-low-load": {
        "profile": "ioniq6n", "rpm": 3600.0, "throttle": 0.12, "load": 0.12,
        "lock_rpm": True, "direct_soundscape_state": True,
        "soundscape_enable": 1, "soundscape_level_db": -6.0, "soundscape_solo": 1,
        "extra_messages": ("n_sound_mode lightspeed", "speed_kph 80", "engine_running 1"),
    },
    "ioniq6n-lightspeed-high-load": {
        "profile": "ioniq6n", "rpm": 3600.0, "throttle": 0.90, "load": 0.88,
        "lock_rpm": True, "direct_soundscape_state": True,
        "soundscape_enable": 1, "soundscape_level_db": -6.0, "soundscape_solo": 1,
        "extra_messages": ("n_sound_mode lightspeed", "speed_kph 80", "engine_running 1"),
    },
    "ioniq6n-evolution-low-speed": {
        "profile": "ioniq6n", "rpm": 3600.0, "throttle": 0.55, "load": 0.55,
        "lock_rpm": True, "direct_soundscape_state": True,
        "soundscape_enable": 1, "soundscape_level_db": -6.0, "soundscape_solo": 1,
        "extra_messages": ("n_sound_mode evolution", "speed_kph 15", "engine_running 1"),
    },
    "ioniq6n-evolution-high-speed": {
        "profile": "ioniq6n", "rpm": 3600.0, "throttle": 0.55, "load": 0.55,
        "lock_rpm": True, "direct_soundscape_state": True,
        "soundscape_enable": 1, "soundscape_level_db": -6.0, "soundscape_solo": 1,
        "extra_messages": ("n_sound_mode evolution", "speed_kph 220", "engine_running 1"),
    },
    "ioniq6n-eshift-on": {
        "profile": "ioniq6n", "drive_lifecycle": True,
        "extra_messages": ("auto 1", "eshift_enable 1", "n_sound_mode evolution"),
    },
    "ioniq6n-eshift-off": {
        "profile": "ioniq6n", "drive_lifecycle": True,
        "extra_messages": ("auto 1", "eshift_enable 0", "n_sound_mode evolution"),
    },
    "ioniq6n-event-upshift": {
        "profile": "ioniq6n", "rpm": 4200.0, "lock_rpm": True,
        "event": "eshift_enable 1, event_enable 1, shift 1", "event_at_ms": 300,
        "direct_event_to_transient": True,
        "extra_messages": ("engine_running 1", "event_intensity 0.72", "event_solo 1"),
    },
    "ioniq6n-event-bubble": {
        "profile": "ioniq6n", "rpm": 3600.0, "lock_rpm": True,
        "event": "n_sound_mode ignition, event_enable 1, overrun 0.9", "event_at_ms": 300,
        "direct_event_to_transient": True,
        "extra_messages": ("engine_running 1", "event_intensity 0.72", "event_solo 1"),
    },
    "ioniq6n-event-afterburner": {
        "profile": "ioniq6n", "rpm": 3600.0, "lock_rpm": True,
        "event": "n_sound_mode lightspeed, event_enable 1, pop 1", "event_at_ms": 300,
        "direct_event_to_transient": True,
        "extra_messages": ("engine_running 1", "event_intensity 0.72", "event_solo 1"),
    },
}


def dna_parameter_scenario(profile: str, parameter: str, value: float) -> dict:
    """Hold the acoustic state fixed while changing exactly one DNA control."""
    if profile == "ev":
        rpm = 3200.0
        state = ("accel 0", "speed_kph 0")
    elif profile == "ioniq6n":
        rpm = 3200.0
        state = (
            "accel 0", "speed_kph 0", "engine_running 1", "shift_cut 1"
        )
    else:
        rpm = 4200.0 if profile == "v10" else 4500.0
        state = (
            "accel 0", "speed_kph 0", "engine_running 1",
            "combustion_gain 1", "shift_cut 1", "starter 0",
        )
    return {
        "profile": profile,
        "rpm": rpm,
        "throttle": 0.65,
        "load": 0.55 if profile in {"ev", "ioniq6n"} else 0.65,
        "lock_rpm": True,
        "direct_powertrain": True,
        "extra_messages": (*state, f"{parameter} {value:g}"),
    }


# One low/high fixed-state pair per visible control. These probes are deliberately
# generated from the same authority as the editable panels, so adding a knob
# without an acoustic A/B scenario is a test failure rather than a silent UI bug.
for _profile, _specs in DNA_PARAMETER_SPECS.items():
    for _parameter, _label, _low, _high in _specs:
        SCENARIOS[f"dna-{_profile}-{_parameter}-low"] = dna_parameter_scenario(
            _profile, _parameter, _low
        )
        SCENARIOS[f"dna-{_profile}-{_parameter}-high"] = dna_parameter_scenario(
            _profile, _parameter, _high
        )
    for _suffix, _value_index in (("all-low", 2), ("all-high", 3)):
        _aggregate = dna_parameter_scenario(_profile, _specs[0][0], _specs[0][_value_index])
        _aggregate["extra_messages"] = (
            *_aggregate["extra_messages"][:-1],
            *(f"{item[0]} {item[_value_index]:g}" for item in _specs),
        )
        SCENARIOS[f"dna-{_profile}-{_suffix}"] = _aggregate


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
    global_event_address: str | None = None,
    event_at_ms: int | None = None,
    direct_event_to_transient: bool = False,
    drive_lifecycle: bool = False,
    direct_powertrain: bool = False,
    direct_soundscape_state: bool = False,
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
    if not direct_powertrain:
        p.connect(controller, powertrain, 0, 0)
    for controlled in (transient, road, rumble, cabin, mix):
        p.connect(controller, controlled, 0, 0)
    if not direct_soundscape_state:
        p.connect(controller, soundscape, 0, 0)
    solo_router = p.new("route soundscape_solo pad_solo backfire_solo dna_solo", 620, 300, 390, numinlets=1, numoutlets=5)
    soundscape_solo_clip = p.new("clip 0 1", 620, 335, 65, numinlets=3, numoutlets=1)
    backfire_solo_clip = p.new("clip 0 1", 695, 335, 65, numinlets=3, numoutlets=1)
    dna_solo_clip = p.new("clip 0 1", 770, 335, 65, numinlets=3, numoutlets=1)
    solo_state = p.new("pak 0 0 0", 845, 335, 85, numinlets=3, numoutlets=1)
    core_solo_gain = p.new("expr $i3+(1-$i3)*(1-max($i1,$i2))", 855, 275, 250, numinlets=3, numoutlets=1)
    aux_solo_gain = p.new("expr (1-$i3)*(1-max($i1,$i2))", 855, 305, 220, numinlets=3, numoutlets=1)
    transient_solo_gain = p.new("expr (1-$i3)*(1-$i1*(1-$i2))", 855, 335, 230, numinlets=3, numoutlets=1)
    pad_solo_gain = p.new("expr (1-$i3)*(1-$i2)", 855, 365, 150, numinlets=3, numoutlets=1)

    def make_solo_line(source: str, x: float, y: float) -> str:
        packed = p.new("pack 0. 35", x, y, 80, numinlets=2, numoutlets=1)
        line = p.new("line~", x + 85, y, 50, numinlets=2, numoutlets=2)
        p.connect(source, packed)
        p.connect(packed, line)
        return line

    core_solo_line = make_solo_line(core_solo_gain, 620, 400)
    aux_solo_line = make_solo_line(aux_solo_gain, 620, 430)
    transient_solo_line = make_solo_line(transient_solo_gain, 755, 400)
    pad_solo_line = make_solo_line(pad_solo_gain, 890, 400)
    solo_default = p.new("loadmess 0", 660, 370, 80, numinlets=1, numoutlets=1)
    core_l = p.new("*~", 300, 345, 40, numinlets=2, numoutlets=1)
    core_r = p.new("*~", 430, 345, 40, numinlets=2, numoutlets=1)
    transient_gate_l = p.new("*~", 160, 365, 40, numinlets=2, numoutlets=1)
    transient_gate_r = p.new("*~", 205, 365, 40, numinlets=2, numoutlets=1)
    road_gate_l = p.new("*~", 70, 365, 40, numinlets=2, numoutlets=1)
    road_gate_r = p.new("*~", 115, 365, 40, numinlets=2, numoutlets=1)
    rumble_gate_l = p.new("*~", 555, 365, 40, numinlets=2, numoutlets=1)
    rumble_gate_r = p.new("*~", 600, 365, 40, numinlets=2, numoutlets=1)
    pad_gate_l = p.new("*~", 205, 350, 40, numinlets=2, numoutlets=1)
    pad_gate_r = p.new("*~", 525, 350, 40, numinlets=2, numoutlets=1)
    p.connect(controller, solo_router)
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
    p.connect(powertrain, core_l, 0, 0)
    p.connect(powertrain, core_r, 1, 0)
    p.connect(transient, transient_gate_l, 0, 0)
    p.connect(transient, transient_gate_r, 1, 0)
    p.connect(road, road_gate_l, 0, 0)
    p.connect(road, road_gate_r, 1, 0)
    p.connect(rumble, rumble_gate_l, 0, 0)
    p.connect(rumble, rumble_gate_r, 1, 0)
    for stem_gain in (core_l, core_r):
        p.connect(core_solo_line, stem_gain, 0, 1)
    for stem_gain in (road_gate_l, road_gate_r, rumble_gate_l, rumble_gate_r):
        p.connect(aux_solo_line, stem_gain, 0, 1)
    for stem_gain in (transient_gate_l, transient_gate_r):
        p.connect(transient_solo_line, stem_gain, 0, 1)
    p.connect(soundscape, pad_gate_l, 0, 0)
    p.connect(soundscape, pad_gate_r, 1, 0)
    p.connect(pad_solo_line, pad_gate_l, 0, 1)
    p.connect(pad_solo_line, pad_gate_r, 0, 1)
    p.connect(core_l, add_l, 0, 0)
    p.connect(transient_gate_l, add_l, 0, 1)
    p.connect(core_l, rumble, 0, 1)
    road_l = p.new("+~", 250, 395, 40, numinlets=2, numoutlets=1)
    sum_l = p.new("+~", 300, 420, 40, numinlets=2, numoutlets=1)
    pad_sum_l = p.new("+~", 205, 375, 40, numinlets=2, numoutlets=1)
    p.connect(add_l, pad_sum_l, 0, 0)
    p.connect(pad_gate_l, pad_sum_l, 0, 1)
    engine_l = pad_sum_l
    p.connect(engine_l, road_l, 0, 0)
    p.connect(road_gate_l, road_l, 0, 1)
    p.connect(road_l, sum_l, 0, 0)
    p.connect(rumble_gate_l, sum_l, 0, 1)
    p.connect(core_r, add_r, 0, 0)
    p.connect(transient_gate_r, add_r, 0, 1)
    p.connect(core_r, rumble, 0, 2)
    road_r = p.new("+~", 480, 395, 40, numinlets=2, numoutlets=1)
    sum_r = p.new("+~", 430, 420, 40, numinlets=2, numoutlets=1)
    pad_sum_r = p.new("+~", 525, 375, 40, numinlets=2, numoutlets=1)
    p.connect(add_r, pad_sum_r, 0, 0)
    p.connect(pad_gate_r, pad_sum_r, 0, 1)
    engine_r = pad_sum_r
    p.connect(engine_r, road_r, 0, 0)
    p.connect(road_gate_r, road_r, 0, 1)
    p.connect(road_r, sum_r, 0, 0)
    p.connect(rumble_gate_r, sum_r, 0, 1)
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
    if direct_soundscape_state:
        # The V4 host consumes lifecycle truth; direct probes bypass the
        # controller and therefore must provide its authoritative run state.
        default_messages += ("engine_running 1", "start 1")
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
        p.connect(initial, powertrain if direct_powertrain else drive)
        if direct_soundscape_state:
            p.connect(initial, soundscape)

    load = p.new("loadbang", 500, 110, 65, numinlets=1, numoutlets=1)
    start_delay = p.new("delay 100", 500, 150, 70, numinlets=2, numoutlets=1)
    record_start = p.message("1", 590, 190, 30)
    record_stop = p.message("0", 680, 190, 30)
    p.connect(load, start_delay)
    event = None
    if event_message is not None and global_event_address is not None:
        raise ValueError("a probe event must use either a message or a global send")
    if event_message is not None:
        event = p.message(event_message, 790, 190, 190)
        event_target = (
            transient if direct_event_to_transient
            else soundscape if direct_soundscape_state
            else drive
        )
        p.connect(event, event_target)
    elif global_event_address is not None:
        event = p.new(
            f"s {global_event_address}", 790, 190, 190,
            numinlets=1, numoutlets=0,
        )
    if event is not None and driver_mode == "coreaudio":
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
    if tap == "transient":
        record_left, record_right = transient, transient
        record_left_outlet, record_right_outlet = 0, 1
    elif tap == "pre-cabin":
        record_left, record_right = sum_l, sum_r
        record_left_outlet, record_right_outlet = 0, 0
    else:
        record_left, record_right = mix, mix
        record_left_outlet, record_right_outlet = 0, 1
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
        delayed_start_messages: tuple[str, ...] = ()
        if start_enabled and ignition_enabled:
            # The load-time start occurs while DSP is stopped, so signal-rate
            # line~ gates cannot advance. Reset the lifecycle lock, but defer
            # the actual one-shot until the audio driver has entered its first
            # active vectors instead of sharing the ezdac~ scheduler tick.
            delayed_start_messages = ("ignition 0", "ignition 1", "start 1")
        elif start_enabled:
            delayed_start_messages = ("start 1",)
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
        p.connect(runtime_replay, powertrain if direct_powertrain else drive)
        if direct_soundscape_state:
            p.connect(runtime_replay, soundscape)
        if delayed_start_messages:
            delayed_start = p.new("delay 250", 770, 530, 70, numinlets=2, numoutlets=1)
            delayed_start_message = p.message(
                ", ".join(delayed_start_messages), 850, 530, 210,
            )
            p.connect(start_trigger, delayed_start, 2, 0)
            p.connect(delayed_start, delayed_start_message)
            p.connect(delayed_start_message, drive)
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
            # Keep a deterministic tail inside short diagnostic renders. Locked
            # RPM probes begin recording only after the one-second catch, so
            # this remains safely behind engine_running while never falling
            # beyond the recording stop as the previous fixed 1800 ms did.
            event_at_ms = (
                max(100, min(event_at_ms, render_ms - 300))
                if event_at_ms is not None
                else max(100, min(1800, render_ms - 300))
            )
            event_at = p.new(
                f"past {event_at_ms}", 825, 700, 75,
                numinlets=1, numoutlets=1,
            )
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
    parser.add_argument(
        "--tap", choices=("transient", "pre-cabin", "final"), default="final"
    )
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
    for profile_name in ("ev", "v10", "v12"):
        for suffix in (
            "soundscape_factory", "soundscape_v2_factory", "soundscape_v3_factory",
            "soundscape_v4_factory",
        ):
            factory_name = f"{profile_name}_{suffix}.json"
            shutil.copy2(root / "presets" / factory_name, presets / factory_name)
    shutil.copy2(
        root / "presets" / "ferrari_soundscape_v4_factory.json",
        presets / "ferrari_soundscape_v4_factory.json",
    )
    for factory_name in (
        "ioniq6n_soundscape_modes_factory.json", "ioniq6n_n_event_factory.json",
    ):
        shutil.copy2(root / "presets" / factory_name, presets / factory_name)
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
            start_enabled=bool(scenario.get("start_enabled", args.start == "on")),
            ignition_enabled=bool(scenario.get("ignition_enabled", args.ignition == "on")),
            tap=args.tap,
            extra_messages=tuple(extra_messages),
            event_message=scenario.get("event"),
            global_event_address=scenario.get("global_event_address"),
            event_at_ms=scenario.get("event_at_ms"),
            direct_event_to_transient=bool(
                scenario.get("direct_event_to_transient", False)
            ),
            drive_lifecycle=bool(scenario.get("drive_lifecycle", False)),
            direct_powertrain=bool(scenario.get("direct_powertrain", False)),
            direct_soundscape_state=bool(
                scenario.get("direct_soundscape_state", False)
            ),
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
        "backfire_burst_scheduler.maxpat",
    }
    required_patchers.update({
        f"{profile}_cinematic_soundscape_host~.maxpat",
    })
    if profile == "ioniq6n":
        required_patchers.update({
            "ioniq6n_activation_beap~.maxpat",
            "ioniq6n_n_event_beap~.maxpat",
            "ioniq6n_n_event_host~.maxpat",
            "ioniq6n_soundscape_ignition_beap~.maxpat",
            "ioniq6n_soundscape_evolution_beap~.maxpat",
            "ioniq6n_soundscape_lightspeed_beap~.maxpat",
        })
    else:
        required_patchers.update({
            f"{profile}_engine_start_beap~.maxpat",
            "cinematic_soundscape_v3_beap~.maxpat",
        })
    if profile not in {"ev", "ioniq6n"}:
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
        path.relative_to(bundle).as_posix(): {"kind": "data", "local": 1}
        for path in sorted(presets.glob("*.json"))
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
