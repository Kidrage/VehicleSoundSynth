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


def read_mid_side(path: Path) -> tuple[int, list[float], list[float], list[float]]:
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
    level_samples: list[float] = []
    for index in range(0, len(values), channels):
        left = values[index] / 32768.0
        right = values[index + 1] / 32768.0 if channels > 1 else left
        mid.append((left + right) * 0.5)
        side.append((left - right) * 0.5)
        level_samples.append(left)
        if channels > 1:
            level_samples.append(right)
    return sample_rate, mid, side, level_samples


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
    sample_rate, samples, side_samples, level_samples = read_mid_side(path)
    if not samples:
        raise ValueError("WAV contains no samples")
    peak = max(abs(value) for value in level_samples)
    rms = math.sqrt(sum(value * value for value in level_samples) / len(level_samples))
    envelope_block_size = max(1, sample_rate // 5)
    envelope_blocks = [
        math.sqrt(
            sum(value * value for value in samples[index:index + envelope_block_size])
            / envelope_block_size
        )
        for index in range(0, len(samples) - envelope_block_size + 1, envelope_block_size)
    ]

    def percentile(values: list[float], fraction: float) -> float:
        ordered = sorted(values)
        if not ordered:
            return 0.0
        position = fraction * (len(ordered) - 1)
        low = math.floor(position)
        high = math.ceil(position)
        if low == high:
            return ordered[low]
        weight = position - low
        return ordered[low] * (1.0 - weight) + ordered[high] * weight

    envelope_low = percentile(envelope_blocks, 0.05)
    envelope_high = percentile(envelope_blocks, 0.95)
    envelope_spread_db = 20.0 * math.log10(
        max(envelope_high, 1e-12) / max(envelope_low, 1e-12)
    )
    clipped_ratio = sum(abs(value) >= 0.999 for value in level_samples) / len(level_samples)
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
    analysis_bins = [
        index for index in range(1, len(power) - 1)
        if 80.0 <= index * sample_rate / size < 6000.0
    ]
    band_peak = max((power[index] for index in analysis_bins), default=0.0)
    peak_bins = [
        index for index in analysis_bins
        if power[index] >= band_peak * 0.001
        and power[index] > power[index - 1]
        and power[index] >= power[index + 1]
    ]
    band_total = max(sum(power[index] for index in analysis_bins), 1e-30)
    dominant_index = max(analysis_bins, key=power.__getitem__) if analysis_bins else 0
    dominant_neighborhood = sum(
        power[index]
        for index in range(max(0, dominant_index - 2), min(len(power), dominant_index + 3))
    )
    return {
        "file": str(path),
        "sample_rate": sample_rate,
        "frames": len(samples),
        "peak_dbfs": 20.0 * math.log10(max(peak, 1e-12)),
        "rms_dbfs": 20.0 * math.log10(max(rms, 1e-12)),
        "crest_db": 20.0 * math.log10(max(peak / max(rms, 1e-12), 1e-12)),
        "envelope_spread_db": envelope_spread_db,
        "clipped_sample_ratio": clipped_ratio,
        "subsonic_ratio": subsonic,
        "rumble_ratio": rumble,
        "low_mid_ratio": low_mid,
        "low_side_ratio": low_side_ratio,
        "high_ratio": high,
        "spectral_peak_count_80_6000": len(peak_bins),
        "dominant_peak_ratio_80_6000": dominant_neighborhood / band_total,
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
    parser.add_argument("--min-spectral-peaks", type=int)
    parser.add_argument("--max-dominant-peak-ratio", type=float)
    parser.add_argument("--max-envelope-spread-db", type=float)
    parser.add_argument("--max-clipped-sample-ratio", type=float)
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
    if args.min_spectral_peaks is not None and metrics["spectral_peak_count_80_6000"] < args.min_spectral_peaks:
        failures.append("spectral_peak_count_80_6000")
    if args.max_dominant_peak_ratio is not None and metrics["dominant_peak_ratio_80_6000"] > args.max_dominant_peak_ratio:
        failures.append("dominant_peak_ratio_80_6000")
    if args.max_envelope_spread_db is not None and metrics["envelope_spread_db"] > args.max_envelope_spread_db:
        failures.append("envelope_spread_db")
    if args.max_clipped_sample_ratio is not None and metrics["clipped_sample_ratio"] > args.max_clipped_sample_ratio:
        failures.append("clipped_sample_ratio")
    if failures:
        print("Acceptance failed: " + ", ".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
