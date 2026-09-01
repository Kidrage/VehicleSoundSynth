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


def envelope_modulation_metrics(
    samples: list[float], sample_rate: int
) -> dict[str, float]:
    """Measure slow envelope cycling without mistaking steady tones for AM."""
    window = max(1, round(sample_rate * 0.10))
    hop = max(1, round(sample_rate * 0.02))
    envelope = [
        math.sqrt(sum(value * value for value in samples[index:index + window]) / window)
        for index in range(0, len(samples) - window + 1, hop)
    ]
    if len(envelope) < 4:
        return {
            "modulation_peak_hz": 0.0,
            "modulation_peak_ratio_0_5_20_hz": 0.0,
            "envelope_autocorrelation_period_seconds": 0.0,
            "envelope_autocorrelation_peak": 0.0,
        }
    mean = sum(envelope) / len(envelope)
    normalized = [value / max(mean, 1e-12) - 1.0 for value in envelope]
    energy = sum(value * value for value in normalized)
    if energy / len(normalized) < 1e-4:
        return {
            "modulation_peak_hz": 0.0,
            "modulation_peak_ratio_0_5_20_hz": 0.0,
            "envelope_autocorrelation_period_seconds": 0.0,
            "envelope_autocorrelation_peak": 0.0,
        }

    envelope_rate = sample_rate / hop
    spectrum: list[tuple[float, float]] = []
    for bin_index in range(1, len(normalized) // 2 + 1):
        frequency = bin_index * envelope_rate / len(normalized)
        if frequency > 20.0:
            break
        if frequency < 0.5:
            continue
        value = sum(
            sample
            * (0.5 - 0.5 * math.cos(2.0 * math.pi * index / (len(normalized) - 1)))
            * cmath.exp(-2j * math.pi * bin_index * index / len(normalized))
            for index, sample in enumerate(normalized)
        )
        spectrum.append((abs(value) ** 2, frequency))
    modulation_power = sum(power for power, _ in spectrum)
    peak_power, peak_frequency = max(spectrum, default=(0.0, 0.0))

    correlations: list[tuple[float, float]] = []
    minimum_lag = max(1, round(0.15 * envelope_rate))
    maximum_lag = min(len(normalized) - 2, round(2.5 * envelope_rate))
    for lag in range(minimum_lag, maximum_lag + 1):
        first = normalized[:-lag]
        second = normalized[lag:]
        numerator = sum(left * right for left, right in zip(first, second))
        denominator = math.sqrt(
            sum(value * value for value in first)
            * sum(value * value for value in second)
        )
        correlations.append((numerator / max(denominator, 1e-30), lag / envelope_rate))
    autocorrelation, period = max(correlations, default=(0.0, 0.0))
    return {
        "modulation_peak_hz": peak_frequency,
        "modulation_peak_ratio_0_5_20_hz": peak_power / max(modulation_power, 1e-30),
        "envelope_autocorrelation_period_seconds": period,
        "envelope_autocorrelation_peak": autocorrelation,
    }


def impact_metrics(samples: list[float], sample_rate: int) -> dict[str, float]:
    """Measure the first impact attack and its short-tail decay independently."""
    peak = max((abs(value) for value in samples), default=0.0)
    onset_threshold = peak * 0.08
    onset = next(
        (index for index, value in enumerate(samples) if abs(value) >= onset_threshold),
        0,
    )

    def attack(duration_ms: float) -> dict[str, float]:
        frame_count = max(16, round(sample_rate * duration_ms / 1000.0))
        segment = samples[onset:onset + frame_count]
        if len(segment) < frame_count:
            segment = segment + [0.0] * (frame_count - len(segment))
        windowed = [
            complex(
                value
                * (0.5 - 0.5 * math.cos(2.0 * math.pi * index / (frame_count - 1)))
            )
            for index, value in enumerate(segment)
        ]
        fft_size = 1
        while fft_size < frame_count:
            fft_size *= 2
        windowed.extend([0j] * (fft_size - frame_count))
        power = [abs(value) ** 2 for value in fft(windowed)[: fft_size // 2]]

        def band(low: float, high: float) -> float:
            return sum(
                value
                for index, value in enumerate(power)
                if low <= index * sample_rate / fft_size < high
            )

        audible = max(band(20.0, min(12000.0, sample_rate / 2.0)), 1e-30)
        bins = [
            index for index in range(1, len(power))
            if 20.0 <= index * sample_rate / fft_size < min(12000.0, sample_rate / 2.0)
        ]
        centroid = sum(
            index * sample_rate / fft_size * power[index] for index in bins
        ) / audible
        return {
            "centroid_hz": centroid,
            "low_20_180_ratio": band(20.0, 180.0) / audible,
            "snare_1200_6000_ratio": band(1200.0, 6000.0) / audible,
        }

    block = max(1, round(sample_rate * 0.005))
    envelope = [
        math.sqrt(sum(value * value for value in samples[index:index + block]) / block)
        for index in range(onset, len(samples) - block + 1, block)
    ]
    envelope_peak = max(envelope, default=0.0)
    tail_threshold = envelope_peak * 0.1
    last_active = max(
        (index for index, value in enumerate(envelope) if value >= tail_threshold),
        default=0,
    )
    tail_ms = (last_active + 1) * block * 1000.0 / sample_rate
    short = attack(23.0)
    medium = attack(46.0)
    return {
        "impact_onset_ms": onset * 1000.0 / sample_rate,
        "attack_23ms_centroid_hz": short["centroid_hz"],
        "attack_23ms_low_20_180_ratio": short["low_20_180_ratio"],
        "attack_23ms_snare_1200_6000_ratio": short["snare_1200_6000_ratio"],
        "attack_46ms_centroid_hz": medium["centroid_hz"],
        "attack_46ms_low_20_180_ratio": medium["low_20_180_ratio"],
        "attack_46ms_snare_1200_6000_ratio": medium["snare_1200_6000_ratio"],
        "impact_tail_20db_ms": tail_ms,
    }


def analyze(
    path: Path,
    fft_size: int = 32768,
    expected_fundamental_hz: float | None = None,
) -> dict[str, float | int | str]:
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
    near_peak_sample_ratio = (
        sum(abs(value) >= peak * 0.90 for value in level_samples) / len(level_samples)
        if peak > 1e-9 else 0.0
    )
    size = min(fft_size, 1 << (len(samples).bit_length() - 1))
    left_samples = [mid + side for mid, side in zip(samples, side_samples)]
    right_samples = [mid - side for mid, side in zip(samples, side_samples)]
    window_count = min(5, max(1, math.ceil(len(samples) / size)))
    last_start = len(samples) - size
    starts = (
        [0]
        if window_count == 1
        else [round(index * last_start / (window_count - 1)) for index in range(window_count)]
    )
    hann = [
        0.5 - 0.5 * math.cos(2.0 * math.pi * index / (size - 1))
        for index in range(size)
    ]

    def window_spectrum(signal: list[float], start: int) -> list[complex]:
        return fft([
            complex(signal[start + index] * hann[index])
            for index in range(size)
        ])[: size // 2]

    power = [0.0] * (size // 2)
    side_power = [0.0] * (size // 2)
    left_power = [0.0] * (size // 2)
    right_power = [0.0] * (size // 2)
    cross_power = [0.0] * (size // 2)
    for start in starts:
        mid_spectrum = window_spectrum(samples, start)
        side_spectrum = window_spectrum(side_samples, start)
        left_spectrum = window_spectrum(left_samples, start)
        right_spectrum = window_spectrum(right_samples, start)
        for index in range(size // 2):
            power[index] += abs(mid_spectrum[index]) ** 2
            side_power[index] += abs(side_spectrum[index]) ** 2
            left_power[index] += abs(left_spectrum[index]) ** 2
            right_power[index] += abs(right_spectrum[index]) ** 2
            cross_power[index] += (
                left_spectrum[index] * right_spectrum[index].conjugate()
            ).real
    scale = 1.0 / len(starts)
    power = [value * scale for value in power]
    side_power = [value * scale for value in side_power]
    left_power = [value * scale for value in left_power]
    right_power = [value * scale for value in right_power]
    cross_power = [value * scale for value in cross_power]

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
    harsh = band_energy(2000.0, 6000.0) / audible
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
            index for index in range(len(left_power))
            if low <= index * sample_rate / size < high
        ]
        left_energy = sum(left_power[index] for index in bins)
        right_energy = sum(right_power[index] for index in bins)
        cross = sum(cross_power[index] for index in bins)
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
    spectral_limit = min(12000.0, sample_rate / 2.0)
    spectral_bins = [
        index for index in range(1, len(power))
        if 20.0 <= index * sample_rate / size < spectral_limit
    ]
    spectral_total = max(sum(power[index] for index in spectral_bins), 1e-30)
    spectral_centroid = sum(
        index * sample_rate / size * power[index] for index in spectral_bins
    ) / spectral_total
    cumulative = 0.0
    spectral_rolloff = 0.0
    for index in spectral_bins:
        cumulative += power[index]
        if cumulative >= spectral_total * 0.95:
            spectral_rolloff = index * sample_rate / size
            break
    sample_deltas = [samples[index] - samples[index - 1] for index in range(1, len(samples))]
    sample_delta_peak = max((abs(value) for value in sample_deltas), default=0.0)

    upper_harmonic_ratio = 0.0
    harmonic_slope = 0.0
    if expected_fundamental_hz is not None:
        if expected_fundamental_hz <= 0.0:
            raise ValueError("expected fundamental must be positive")
        harmonic_energies: list[tuple[int, float]] = []
        harmonic_count = min(96, int((spectral_limit - 1.0) / expected_fundamental_hz))
        for harmonic in range(1, harmonic_count + 1):
            center = round(harmonic * expected_fundamental_hz * size / sample_rate)
            energy = sum(
                power[index]
                for index in range(max(0, center - 2), min(len(power), center + 3))
            )
            harmonic_energies.append((harmonic, energy))
        harmonic_total = max(sum(energy for _, energy in harmonic_energies), 1e-30)
        upper_harmonic_ratio = sum(
            energy for harmonic, energy in harmonic_energies if harmonic >= 16
        ) / harmonic_total
        maximum_harmonic_energy = max(
            (energy for _, energy in harmonic_energies), default=0.0
        )
        fit = [
            (math.log2(harmonic), 10.0 * math.log10(max(energy, 1e-30)))
            for harmonic, energy in harmonic_energies
            if 2 <= harmonic <= 48 and energy > maximum_harmonic_energy * 1e-8
        ]
        if len(fit) >= 2:
            mean_x = sum(x for x, _ in fit) / len(fit)
            mean_y = sum(y for _, y in fit) / len(fit)
            harmonic_slope = sum(
                (x - mean_x) * (y - mean_y) for x, y in fit
            ) / max(sum((x - mean_x) ** 2 for x, _ in fit), 1e-30)
    return {
        "file": str(path),
        "sample_rate": sample_rate,
        "frames": len(samples),
        "peak_dbfs": 20.0 * math.log10(max(peak, 1e-12)),
        "rms_dbfs": 20.0 * math.log10(max(rms, 1e-12)),
        "crest_db": 20.0 * math.log10(max(peak / max(rms, 1e-12), 1e-12)),
        "envelope_spread_db": envelope_spread_db,
        "clipped_sample_ratio": clipped_ratio,
        "near_peak_sample_ratio": near_peak_sample_ratio,
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
        "harsh_ratio": harsh,
        "high_ratio": high,
        "spectral_peak_count_80_6000": len(peak_bins),
        "dominant_peak_ratio_80_6000": dominant_neighborhood / band_total,
        "spectral_centroid_hz": spectral_centroid,
        "spectral_rolloff_95_hz": spectral_rolloff,
        "sample_delta_peak_over_rms": sample_delta_peak / max(mono_rms, 1e-12),
        "upper_harmonic_ratio": upper_harmonic_ratio,
        "harmonic_slope_db_per_octave": harmonic_slope,
        **envelope_modulation_metrics(samples, sample_rate),
        **impact_metrics(samples, sample_rate),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wav", type=Path)
    parser.add_argument("--max-peak-dbfs", type=float)
    parser.add_argument("--min-rms-dbfs", type=float)
    parser.add_argument("--max-harsh-ratio", type=float)
    parser.add_argument("--max-high-ratio", type=float)
    parser.add_argument("--min-low-mid-ratio", type=float)
    parser.add_argument("--min-rumble-ratio", type=float)
    parser.add_argument("--max-subsonic-ratio", type=float)
    parser.add_argument("--max-low-side-ratio", type=float)
    parser.add_argument("--min-low-band-correlation", type=float)
    parser.add_argument("--max-mid-side-ratio", type=float)
    parser.add_argument("--min-mid-band-correlation", type=float)
    parser.add_argument("--max-mid-band-mono-fold-rms-loss-db", type=float)
    parser.add_argument("--max-high-side-ratio", type=float)
    parser.add_argument("--min-high-band-correlation", type=float)
    parser.add_argument("--max-high-band-mono-fold-rms-loss-db", type=float)
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
    parser.add_argument("--max-near-peak-sample-ratio", type=float)
    parser.add_argument("--require-sample-rate", type=int)
    parser.add_argument("--expected-fundamental-hz", type=float)
    parser.add_argument("--max-spectral-centroid-hz", type=float)
    parser.add_argument("--max-rolloff-95-hz", type=float)
    parser.add_argument("--max-sample-delta-peak-over-rms", type=float)
    parser.add_argument("--max-upper-harmonic-ratio", type=float)
    parser.add_argument("--max-harmonic-slope-db-per-octave", type=float)
    parser.add_argument("--max-attack-23ms-centroid-hz", type=float)
    parser.add_argument("--min-attack-23ms-low-ratio", type=float)
    parser.add_argument("--max-attack-23ms-snare-ratio", type=float)
    parser.add_argument("--max-impact-tail-20db-ms", type=float)
    args = parser.parse_args()
    metrics = analyze(
        args.wav, expected_fundamental_hz=args.expected_fundamental_hz
    )
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
    if args.max_harsh_ratio is not None and metrics["harsh_ratio"] > args.max_harsh_ratio:
        failures.append("harsh_ratio")
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
    for band in ("mid", "high"):
        side_limit = getattr(args, f"max_{band}_side_ratio")
        correlation_limit = getattr(args, f"min_{band}_band_correlation")
        mono_limit = getattr(args, f"max_{band}_band_mono_fold_rms_loss_db")
        if side_limit is not None and metrics[f"{band}_band_side_ratio"] > side_limit:
            failures.append(f"{band}_band_side_ratio")
        if correlation_limit is not None and metrics[f"{band}_band_correlation"] < correlation_limit:
            failures.append(f"{band}_band_correlation")
        if mono_limit is not None and metrics[f"{band}_band_mono_fold_rms_loss_db"] > mono_limit:
            failures.append(f"{band}_band_mono_fold_rms_loss_db")
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
    if (
        args.max_near_peak_sample_ratio is not None
        and metrics["near_peak_sample_ratio"] > args.max_near_peak_sample_ratio
    ):
        failures.append("near_peak_sample_ratio")
    if (
        args.max_spectral_centroid_hz is not None
        and metrics["spectral_centroid_hz"] > args.max_spectral_centroid_hz
    ):
        failures.append("spectral_centroid_hz")
    if (
        args.max_rolloff_95_hz is not None
        and metrics["spectral_rolloff_95_hz"] > args.max_rolloff_95_hz
    ):
        failures.append("spectral_rolloff_95_hz")
    if (
        args.max_sample_delta_peak_over_rms is not None
        and metrics["sample_delta_peak_over_rms"] > args.max_sample_delta_peak_over_rms
    ):
        failures.append("sample_delta_peak_over_rms")
    if args.max_upper_harmonic_ratio is not None:
        if args.expected_fundamental_hz is None:
            parser.error("--max-upper-harmonic-ratio requires --expected-fundamental-hz")
        if metrics["upper_harmonic_ratio"] > args.max_upper_harmonic_ratio:
            failures.append("upper_harmonic_ratio")
    if args.max_harmonic_slope_db_per_octave is not None:
        if args.expected_fundamental_hz is None:
            parser.error(
                "--max-harmonic-slope-db-per-octave requires --expected-fundamental-hz"
            )
        if (
            metrics["harmonic_slope_db_per_octave"]
            > args.max_harmonic_slope_db_per_octave
        ):
            failures.append("harmonic_slope_db_per_octave")
    if (
        args.max_attack_23ms_centroid_hz is not None
        and metrics["attack_23ms_centroid_hz"] > args.max_attack_23ms_centroid_hz
    ):
        failures.append("attack_23ms_centroid_hz")
    if (
        args.min_attack_23ms_low_ratio is not None
        and metrics["attack_23ms_low_20_180_ratio"] < args.min_attack_23ms_low_ratio
    ):
        failures.append("attack_23ms_low_20_180_ratio")
    if (
        args.max_attack_23ms_snare_ratio is not None
        and metrics["attack_23ms_snare_1200_6000_ratio"] > args.max_attack_23ms_snare_ratio
    ):
        failures.append("attack_23ms_snare_1200_6000_ratio")
    if (
        args.max_impact_tail_20db_ms is not None
        and metrics["impact_tail_20db_ms"] > args.max_impact_tail_20db_ms
    ):
        failures.append("impact_tail_20db_ms")
    if failures:
        print("Acceptance failed: " + ", ".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
