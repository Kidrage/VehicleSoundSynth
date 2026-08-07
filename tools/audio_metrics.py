#!/usr/bin/env python3
"""Report objective level and spectrum metrics for a rendered WAV file."""

from __future__ import annotations

import argparse
import cmath
import json
import math
import struct
import wave
from pathlib import Path


def read_mid_side(path: Path) -> tuple[int, list[float], list[float]]:
    with wave.open(str(path), "rb") as handle:
        channels = handle.getnchannels()
        width = handle.getsampwidth()
        sample_rate = handle.getframerate()
        frames = handle.readframes(handle.getnframes())
    if width != 2:
        raise ValueError(f"Only 16-bit PCM WAV is supported, got {width * 8}-bit")
    values = struct.unpack(f"<{len(frames) // 2}h", frames)
    mid: list[float] = []
    side: list[float] = []
    for index in range(0, len(values), channels):
        left = values[index] / 32768.0
        right = values[index + 1] / 32768.0 if channels > 1 else left
        mid.append((left + right) * 0.5)
        side.append((left - right) * 0.5)
    return sample_rate, mid, side


def fft(values: list[complex]) -> list[complex]:
    size = len(values)
    if size <= 1:
        return values
    even = fft(values[0::2])
    odd = fft(values[1::2])
    result = [0j] * size
    for index in range(size // 2):
        rotated = cmath.exp(-2j * math.pi * index / size) * odd[index]
        result[index] = even[index] + rotated
        result[index + size // 2] = even[index] - rotated
    return result


def analyze(path: Path, fft_size: int = 32768) -> dict[str, float | int | str]:
    sample_rate, samples, side_samples = read_mid_side(path)
    if not samples:
        raise ValueError("WAV contains no samples")
    peak = max(abs(value) for value in samples)
    rms = math.sqrt(sum(value * value for value in samples) / len(samples))
    size = min(fft_size, 1 << (len(samples).bit_length() - 1))
    windowed = [
        complex(samples[index] * (0.5 - 0.5 * math.cos(2.0 * math.pi * index / (size - 1))))
        for index in range(size)
    ]
    spectrum = fft(windowed)[: size // 2]
    power = [abs(value) ** 2 for value in spectrum]
    side_windowed = [
        complex(side_samples[index] * (0.5 - 0.5 * math.cos(2.0 * math.pi * index / (size - 1))))
        for index in range(size)
    ]
    side_power = [abs(value) ** 2 for value in fft(side_windowed)[: size // 2]]

    def band_energy(low: float, high: float) -> float:
        return sum(
            value
            for index, value in enumerate(power)
            if low <= index * sample_rate / size < high
        )

    audible = max(band_energy(20.0, min(20000.0, sample_rate / 2.0)), 1e-30)
    subsonic = band_energy(20.0, 30.0) / audible
    rumble = band_energy(30.0, 140.0) / audible
    low_mid = band_energy(40.0, 500.0) / audible
    high = band_energy(6000.0, min(20000.0, sample_rate / 2.0)) / audible
    low_mid_energy = band_energy(30.0, 120.0)
    low_side_energy = sum(
        value
        for index, value in enumerate(side_power)
        if 30.0 <= index * sample_rate / size < 120.0
    )
    low_side_ratio = low_side_energy / max(low_mid_energy + low_side_energy, 1e-30)
    return {
        "file": str(path),
        "sample_rate": sample_rate,
        "frames": len(samples),
        "peak_dbfs": 20.0 * math.log10(max(peak, 1e-12)),
        "rms_dbfs": 20.0 * math.log10(max(rms, 1e-12)),
        "crest_db": 20.0 * math.log10(max(peak / max(rms, 1e-12), 1e-12)),
        "subsonic_ratio": subsonic,
        "rumble_ratio": rumble,
        "low_mid_ratio": low_mid,
        "low_side_ratio": low_side_ratio,
        "high_ratio": high,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wav", type=Path)
    parser.add_argument("--max-peak-dbfs", type=float)
    parser.add_argument("--min-rms-dbfs", type=float)
    parser.add_argument("--max-high-ratio", type=float)
    parser.add_argument("--min-low-mid-ratio", type=float)
    parser.add_argument("--min-rumble-ratio", type=float)
    parser.add_argument("--max-subsonic-ratio", type=float)
    parser.add_argument("--max-low-side-ratio", type=float)
    args = parser.parse_args()
    metrics = analyze(args.wav)
    print(json.dumps(metrics, indent=2, sort_keys=True))
    failures = []
    if args.max_peak_dbfs is not None and metrics["peak_dbfs"] > args.max_peak_dbfs:
        failures.append("peak_dbfs")
    if args.min_rms_dbfs is not None and metrics["rms_dbfs"] < args.min_rms_dbfs:
        failures.append("rms_dbfs")
    if args.max_high_ratio is not None and metrics["high_ratio"] > args.max_high_ratio:
        failures.append("high_ratio")
    if args.min_low_mid_ratio is not None and metrics["low_mid_ratio"] < args.min_low_mid_ratio:
        failures.append("low_mid_ratio")
    if args.min_rumble_ratio is not None and metrics["rumble_ratio"] < args.min_rumble_ratio:
        failures.append("rumble_ratio")
    if args.max_subsonic_ratio is not None and metrics["subsonic_ratio"] > args.max_subsonic_ratio:
        failures.append("subsonic_ratio")
    if args.max_low_side_ratio is not None and metrics["low_side_ratio"] > args.max_low_side_ratio:
        failures.append("low_side_ratio")
    if failures:
        print("Acceptance failed: " + ", ".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
