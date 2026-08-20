#!/usr/bin/env python3
"""Extract non-audio V10 lifecycle targets from a local Ferrari reference.

The output is safe to track: it contains window locations and aggregate acoustic
measurements, never source samples or a resynthesizable residual/loop bank.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

try:
    from tools.audio_metrics import fft
    from tools.prepare_local_reference import SAMPLE_RATE, _cadence_track, _read_pcm16_stereo
except ModuleNotFoundError:  # Direct `python3 tools/...` invocation.
    from audio_metrics import fft
    from prepare_local_reference import SAMPLE_RATE, _cadence_track, _read_pcm16_stereo


NODE_SPECS = (
    ("startup_catch", "startup_catch", 0.25, 1.00),
    ("idle_settle", "idle", 2.50, 3.25),
    ("idle_warm", "idle", 7.00, 7.75),
    ("blip_attack_low", "acceleration", 10.25, 11.00),
    ("blip_recovery_low", "shift_recovery", 11.25, 12.00),
    ("blip_attack_mid", "acceleration", 12.25, 13.00),
    ("blip_loaded_mid", "loaded_hold", 13.00, 13.75),
    ("overrun_mid", "deceleration", 14.75, 15.50),
    ("loaded_hold_upper", "loaded_hold", 19.50, 20.25),
    ("shift_recovery_upper", "shift_recovery", 23.25, 24.00),
    ("overrun_upper", "deceleration", 23.75, 24.50),
    ("full_attack", "acceleration", 28.00, 28.75),
    ("full_release", "deceleration", 28.75, 29.50),
    ("high_loaded_hold", "loaded_hold", 31.75, 32.50),
)


def _window_metrics(
    channels: list[list[float]], cadence: list[dict[str, float | str]],
    start_seconds: float, end_seconds: float,
) -> dict[str, float]:
    start = round(start_seconds * SAMPLE_RATE)
    end = min(len(channels[0]), round(end_seconds * SAMPLE_RATE))
    left = channels[0][start:end]
    right = channels[1][start:end]
    mid = [(a + b) * 0.5 for a, b in zip(left, right)]
    levels = left + right
    if len(mid) < 2048:
        raise ValueError("lifecycle analysis window is too short")

    fft_size = min(16384, 1 << (len(mid).bit_length() - 1))
    offset = max(0, (len(mid) - fft_size) // 2)
    windowed = [
        complex(
            mid[offset + index]
            * (0.5 - 0.5 * math.cos(2.0 * math.pi * index / (fft_size - 1)))
        )
        for index in range(fft_size)
    ]
    power = [abs(value) ** 2 for value in fft(windowed)[: fft_size // 2]]

    def band(low: float, high: float) -> float:
        return sum(
            value for index, value in enumerate(power)
            if low <= index * SAMPLE_RATE / fft_size < high
        )

    audible = max(band(20.0, 20000.0), 1e-30)
    spectral_bins = [
        index for index in range(1, len(power))
        if 20.0 <= index * SAMPLE_RATE / fft_size < 12000.0
    ]
    spectral_total = max(sum(power[index] for index in spectral_bins), 1e-30)
    centroid = sum(
        index * SAMPLE_RATE / fft_size * power[index] for index in spectral_bins
    ) / spectral_total
    accumulated = 0.0
    rolloff = 0.0
    for index in spectral_bins:
        accumulated += power[index]
        if accumulated >= spectral_total * 0.95:
            rolloff = index * SAMPLE_RATE / fft_size
            break

    center_frame = (start + end) * 0.5
    cadence_point = min(
        cadence, key=lambda point: abs(float(point["center_frame"]) - center_frame)
    )
    rms = math.sqrt(sum(value * value for value in levels) / max(1, len(levels)))
    peak = max(abs(value) for value in levels)
    return {
        "rms_dbfs": round(20.0 * math.log10(max(rms, 1e-12)), 3),
        "peak_dbfs": round(20.0 * math.log10(max(peak, 1e-12)), 3),
        "crest_db": round(20.0 * math.log10(max(peak / max(rms, 1e-12), 1e-12)), 3),
        "dominant_firing_hz": round(float(cadence_point["cadence_hz"]), 3),
        "cadence_derivative_hz_s": round(float(cadence_point["cadence_derivative_hz_s"]), 3),
        "spectral_centroid_hz": round(centroid, 3),
        "spectral_rolloff_95_hz": round(rolloff, 3),
        "rumble_ratio_30_140": round(band(30.0, 140.0) / audible, 6),
        "low_mid_ratio_40_500": round(band(40.0, 500.0) / audible, 6),
        "harsh_ratio_2000_6000": round(band(2000.0, 6000.0) / audible, 6),
        "air_ratio_6000_12000": round(band(6000.0, 12000.0) / audible, 6),
    }


def analyze_lifecycle(source: Path) -> dict[str, object]:
    channels = _read_pcm16_stereo(source)
    cadence = _cadence_track(channels)
    if not cadence:
        raise ValueError("reference is too short to analyse")
    nodes = []
    for identifier, role, start, end in NODE_SPECS:
        nodes.append(
            {
                "id": identifier,
                "role": role,
                "start_seconds": start,
                "end_seconds": end,
                **_window_metrics(channels, cadence, start, end),
            }
        )
    return {
        "schema_version": 1,
        "runtime_usage": "analysis-only",
        "description": "Ferrari V10 lifecycle acoustic targets; no source audio is loaded by a runtime patcher",
        "source_file": source.name,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "processor_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "sample_rate_hz": SAMPLE_RATE,
        "nodes": nodes,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    result = analyze_lifecycle(args.source)
    args.destination.parent.mkdir(parents=True, exist_ok=True)
    args.destination.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"destination": str(args.destination), "nodes": len(result["nodes"])}))


if __name__ == "__main__":
    main()
