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


def read_channels(path: Path) -> tuple[int, list[float], list[float], list[float]]:
    """Return sample rate plus left, right, and Mid signals from PCM16 WAV."""
    sample_rate, mid, side, _ = read_mid_side(path)
    left = [mid_value + side_value for mid_value, side_value in zip(mid, side)]
    right = [mid_value - side_value for mid_value, side_value in zip(mid, side)]
    return sample_rate, left, right, mid


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


def _third_octave_profile(
    power: list[float], sample_rate: int, fft_size: int
) -> list[float]:
    """Return normalized 1/3-octave energy from 31.5 Hz through 8 kHz."""
    centers = [31.5 * 2.0 ** (index / 3.0) for index in range(25)]
    edge = 2.0 ** (1.0 / 6.0)
    energies = [
        sum(
            value
            for bin_index, value in enumerate(power)
            if center / edge <= bin_index * sample_rate / fft_size < center * edge
        )
        for center in centers
    ]
    norm = math.sqrt(sum(value * value for value in energies))
    return [value / max(norm, 1e-30) for value in energies]


def third_octave_similarity(first: Path, second: Path, fft_size: int = 32768) -> float:
    """Cosine similarity of normalized mono 1/3-octave energy profiles."""
    first_rate, first_mid, _, _ = read_mid_side(first)
    second_rate, second_mid, _, _ = read_mid_side(second)
    if first_rate != second_rate:
        raise ValueError("comparison WAV files must use the same sample rate")
    if not first_mid or not second_mid:
        raise ValueError("comparison WAV files contain no samples")
    size = min(
        fft_size,
        1 << (min(len(first_mid), len(second_mid)).bit_length() - 1),
    )
    if size < 2:
        raise ValueError("comparison WAV files are too short")

    def profile(samples: list[float]) -> list[float]:
        windowed = [
            complex(samples[index] * (0.5 - 0.5 * math.cos(2.0 * math.pi * index / (size - 1))))
            for index in range(size)
        ]
        power = [abs(value) ** 2 for value in fft(windowed)[: size // 2]]
        return _third_octave_profile(power, first_rate, size)

    return sum(left * right for left, right in zip(profile(first_mid), profile(second_mid)))


def third_octave_similarities(
    first: Path, second: Path, fft_size: int = 32768
) -> dict[str, float]:
    """Compare left, right, and Mid 1/3-octave profiles independently."""
    first_rate, *first_channels = read_channels(first)
    second_rate, *second_channels = read_channels(second)
    if first_rate != second_rate:
        raise ValueError("comparison WAV files must use the same sample rate")
    shortest = min(*(len(channel) for channel in first_channels + second_channels))
    if shortest < 2:
        raise ValueError("comparison WAV files are too short")
    size = min(fft_size, 1 << (shortest.bit_length() - 1))

    def profile(samples: list[float]) -> list[float]:
        windowed = [
            complex(samples[index] * (0.5 - 0.5 * math.cos(2.0 * math.pi * index / (size - 1))))
            for index in range(size)
        ]
        power = [abs(value) ** 2 for value in fft(windowed)[: size // 2]]
        return _third_octave_profile(power, first_rate, size)

    names = ("left", "right", "mid")
    return {
        name: sum(a * b for a, b in zip(profile(first_channel), profile(second_channel)))
        for name, first_channel, second_channel in zip(names, first_channels, second_channels)
    }


def stereo_delay_ms(path: Path, max_delay_ms: float = 5.0) -> float:
    """Estimate inter-channel delay; positive means the right channel is later."""
    sample_rate, left, right, _ = read_channels(path)
    count = min(len(left), len(right), 12000)
    left = left[:count]
    right = right[:count]
    max_lag = min(round(sample_rate * max_delay_ms / 1000.0), count - 2)

    def score(lag: int) -> float:
        if lag >= 0:
            first, second = left[: count - lag], right[lag:count]
        else:
            first, second = left[-lag:count], right[: count + lag]
        numerator = sum(a * b for a, b in zip(first, second))
        energy = math.sqrt(
            sum(a * a for a in first) * sum(b * b for b in second)
        )
        return numerator / max(energy, 1e-30)

    best = max(range(-max_lag, max_lag + 1), key=score)
    return best * 1000.0 / sample_rate


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
    left_samples = [mid + side for mid, side in zip(samples, side_samples)]
    right_samples = [mid - side for mid, side in zip(samples, side_samples)]
    left_spectrum = fft([
        complex(left_samples[index] * (0.5 - 0.5 * math.cos(2.0 * math.pi * index / (size - 1))))
        for index in range(size)
    ])[: size // 2]
    right_spectrum = fft([
        complex(right_samples[index] * (0.5 - 0.5 * math.cos(2.0 * math.pi * index / (size - 1))))
        for index in range(size)
    ])[: size // 2]

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
    def stereo_band(low: float, high: float) -> tuple[float, float, float]:
        bins = [
            index for index in range(len(left_spectrum))
            if low <= index * sample_rate / size < high
        ]
        left_energy = sum(abs(left_spectrum[index]) ** 2 for index in bins)
        right_energy = sum(abs(right_spectrum[index]) ** 2 for index in bins)
        cross = sum(
            (left_spectrum[index] * right_spectrum[index].conjugate()).real
            for index in bins
        )
        mid_energy = sum(power[index] for index in bins)
        side_energy = sum(side_power[index] for index in bins)
        correlation = cross / max(math.sqrt(left_energy * right_energy), 1e-30)
        side_ratio = side_energy / max(mid_energy + side_energy, 1e-30)
        stereo_energy = (left_energy + right_energy) * 0.5
        fold_loss = max(
            0.0,
            -10.0 * math.log10(max(mid_energy, 1e-30) / max(stereo_energy, 1e-30)),
        )
        return side_ratio, correlation, fold_loss

    low_band = stereo_band(30.0, 120.0)
    mid_band = stereo_band(120.0, 2000.0)
    high_band = stereo_band(2000.0, min(12000.0, sample_rate / 2.0))
    stereo_rms = math.sqrt(
        sum(left * left + right * right for left, right in zip(left_samples, right_samples))
        / max(1, 2 * len(left_samples))
    )
    mono_rms = math.sqrt(sum(value * value for value in samples) / len(samples))
    mono_fold_loss = max(
        0.0,
        -20.0 * math.log10(max(mono_rms, 1e-12) / max(stereo_rms, 1e-12)),
    )
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
        "low_band_side_ratio": low_band[0],
        "low_band_correlation": low_band[1],
        "low_band_mono_fold_rms_loss_db": low_band[2],
        "mid_band_side_ratio": mid_band[0],
        "mid_band_correlation": mid_band[1],
        "mid_band_mono_fold_rms_loss_db": mid_band[2],
        "high_band_side_ratio": high_band[0],
        "high_band_correlation": high_band[1],
        "high_band_mono_fold_rms_loss_db": high_band[2],
        "mono_fold_rms_loss_db": mono_fold_loss,
        "right_channel_delay_ms": stereo_delay_ms(path),
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
    parser.add_argument("--min-low-band-correlation", type=float)
    parser.add_argument("--max-mono-fold-rms-loss-db", type=float)
    parser.add_argument("--compare-wav", type=Path)
    parser.add_argument("--min-third-octave-similarity", type=float)
    parser.add_argument("--min-third-octave-similarity-left", type=float)
    parser.add_argument("--min-third-octave-similarity-right", type=float)
    parser.add_argument("--max-third-octave-similarity-lr-delta", type=float)
    parser.add_argument("--max-abs-right-delay-ms", type=float)
    parser.add_argument("--expected-gain-db", type=float)
    parser.add_argument("--gain-tolerance-db", type=float, default=1.0)
    parser.add_argument("--min-spectral-peaks", type=int)
    parser.add_argument("--max-dominant-peak-ratio", type=float)
    parser.add_argument("--max-envelope-spread-db", type=float)
    parser.add_argument("--max-clipped-sample-ratio", type=float)
    parser.add_argument("--require-sample-rate", type=int)
    args = parser.parse_args()
    metrics = analyze(args.wav)
    if args.compare_wav is not None:
        comparison = analyze(args.compare_wav)
        metrics["comparison_rms_delta_db"] = metrics["rms_dbfs"] - comparison["rms_dbfs"]
        similarities = third_octave_similarities(args.wav, args.compare_wav)
        metrics["third_octave_similarity"] = similarities["mid"]
        metrics.update({f"third_octave_similarity_{name}": value for name, value in similarities.items()})
        metrics["third_octave_similarity_lr_delta"] = abs(similarities["left"] - similarities["right"])
    print(json.dumps(metrics, indent=2, sort_keys=True))
    failures = []
    if args.require_sample_rate is not None and metrics["sample_rate"] != args.require_sample_rate:
        failures.append("sample_rate")
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
    if (
        args.min_low_band_correlation is not None
        and metrics["low_band_correlation"] < args.min_low_band_correlation
    ):
        failures.append("low_band_correlation")
    if (
        args.max_mono_fold_rms_loss_db is not None
        and metrics["mono_fold_rms_loss_db"] > args.max_mono_fold_rms_loss_db
    ):
        failures.append("mono_fold_rms_loss_db")
    if args.min_third_octave_similarity is not None:
        if args.compare_wav is None:
            parser.error("--min-third-octave-similarity requires --compare-wav")
        if metrics["third_octave_similarity"] < args.min_third_octave_similarity:
            failures.append("third_octave_similarity")
    for channel in ("left", "right"):
        threshold = getattr(args, f"min_third_octave_similarity_{channel}")
        if threshold is not None:
            if args.compare_wav is None:
                parser.error(f"--min-third-octave-similarity-{channel} requires --compare-wav")
            if metrics[f"third_octave_similarity_{channel}"] < threshold:
                failures.append(f"third_octave_similarity_{channel}")
    if args.max_third_octave_similarity_lr_delta is not None:
        if args.compare_wav is None:
            parser.error("--max-third-octave-similarity-lr-delta requires --compare-wav")
        if metrics["third_octave_similarity_lr_delta"] > args.max_third_octave_similarity_lr_delta:
            failures.append("third_octave_similarity_lr_delta")
    if (
        args.max_abs_right_delay_ms is not None
        and abs(metrics["right_channel_delay_ms"]) > args.max_abs_right_delay_ms
    ):
        failures.append("right_channel_delay_ms")
    if args.expected_gain_db is not None:
        if args.compare_wav is None:
            parser.error("--expected-gain-db requires --compare-wav")
        if abs(metrics["comparison_rms_delta_db"] - args.expected_gain_db) > args.gain_tolerance_db:
            failures.append("comparison_rms_delta_db")
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
