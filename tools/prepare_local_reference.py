#!/usr/bin/env python3
"""Prepare normalized local-only Ferrari idle/high-RPM residuals for V4."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
import wave
from pathlib import Path


SAMPLE_RATE = 48000
LOOP_FRAMES = 12000
FADE_FRAMES = 960


def _read_pcm16_stereo(path: Path) -> list[list[float]]:
    with wave.open(str(path), "rb") as handle:
        if handle.getsampwidth() != 2 or handle.getframerate() != SAMPLE_RATE:
            raise ValueError("reference must be 48 kHz PCM16 WAV")
        channels = handle.getnchannels()
        if channels not in (1, 2):
            raise ValueError("reference must be mono or stereo")
        frames = handle.getnframes()
        values = struct.unpack(f"<{frames * channels}h", handle.readframes(frames))
    if channels == 1:
        mono = [value / 32768.0 for value in values]
        return [mono[:], mono[:]]
    return [
        [values[index * 2 + channel] / 32768.0 for index in range(frames)]
        for channel in range(2)
    ]


def _biquad(samples: list[float], coeffs: tuple[float, float, float, float, float]) -> list[float]:
    b0, b1, b2, a1, a2 = coeffs
    x1 = x2 = y1 = y2 = 0.0
    output: list[float] = []
    for sample in samples:
        value = b0 * sample + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
        output.append(value)
        x2, x1 = x1, sample
        y2, y1 = y1, value
    return output


def _rbj(kind: str, frequency: float, q_value: float = 0.707) -> tuple[float, float, float, float, float]:
    omega = 2.0 * math.pi * frequency / SAMPLE_RATE
    cosine = math.cos(omega)
    alpha = math.sin(omega) / (2.0 * q_value)
    if kind == "highpass":
        b0, b1, b2 = (1 + cosine) / 2, -(1 + cosine), (1 + cosine) / 2
    elif kind == "lowpass":
        b0, b1, b2 = (1 - cosine) / 2, 1 - cosine, (1 - cosine) / 2
    elif kind == "notch":
        b0, b1, b2 = 1.0, -2.0 * cosine, 1.0
    else:
        raise ValueError(kind)
    a0, a1, a2 = 1 + alpha, -2.0 * cosine, 1 - alpha
    return b0 / a0, b1 / a0, b2 / a0, a1 / a0, a2 / a0


def _residual_filter(
    samples: list[float], *, cadence_hz: float = 61.5, highpass_hz: float = 90.0,
    lowpass_hz: float = 4000.0,
) -> list[float]:
    mean = sum(samples) / max(1, len(samples))
    output = [sample - mean for sample in samples]
    output = _biquad(output, _rbj("highpass", highpass_hz))
    for multiple in range(1, 17):
        frequency = cadence_hz * multiple
        if frequency >= lowpass_hz:
            break
        output = _biquad(output, _rbj("notch", frequency, 18.0))
    return _biquad(output, _rbj("lowpass", lowpass_hz))


def prepare_reference(
    source: Path,
    destination: Path,
    *,
    start_seconds: float = 1.0,
    loop_frames: int = LOOP_FRAMES,
    cadence_hz: float = 61.5,
    highpass_hz: float = 90.0,
    lowpass_hz: float = 4000.0,
) -> dict[str, float | str]:
    channels = _read_pcm16_stereo(source)
    start = round(start_seconds * SAMPLE_RATE)
    required = loop_frames + FADE_FRAMES
    if start < 0 or start + required > len(channels[0]):
        raise ValueError("reference window is outside the source WAV")
    processed: list[list[float]] = []
    for channel in channels:
        # Give the steep 61.5 Hz cadence notch enough real source history to
        # settle before taking the loop window; otherwise its startup transient
        # leaks the very cadence the residual is meant to remove.
        preroll = min(start, SAMPLE_RATE * 2)
        filtered_with_history = _residual_filter(
            channel[start - preroll : start + required], cadence_hz=cadence_hz,
            highpass_hz=highpass_hz, lowpass_hz=lowpass_hz,
        )
        filtered = filtered_with_history[preroll : preroll + required]
        loop = filtered[:loop_frames]
        continuation = filtered[loop_frames : loop_frames + FADE_FRAMES]
        for index in range(FADE_FRAMES):
            phase = index / max(1, FADE_FRAMES - 1) * math.pi / 2.0
            # Overlap the post-loop continuation into the beginning. The file
            # seam remains source[N-1] -> source[N], while the overlap exits
            # into source[fade] without a second discontinuity.
            loop[index] = continuation[index] * math.cos(phase) + loop[index] * math.sin(phase)
        processed.append(loop)

    flat = [sample for channel in processed for sample in channel]
    rms = math.sqrt(sum(sample * sample for sample in flat) / len(flat))
    if rms <= 1e-12:
        raise ValueError("reference window is silent after residual filtering")
    target_rms = 10.0 ** (-18.0 / 20.0)
    peak = max(abs(sample) for sample in flat)
    gain = min(target_rms / rms, (10.0 ** (-3.0 / 20.0)) / peak)
    processed = [[max(-1.0, min(1.0, sample * gain)) for sample in channel] for channel in processed]

    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = b"".join(
        struct.pack("<hh", round(processed[0][index] * 32767.0), round(processed[1][index] * 32767.0))
        for index in range(loop_frames)
    )
    with wave.open(str(destination), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(SAMPLE_RATE)
        handle.writeframes(payload)

    flat = [sample for channel in processed for sample in channel]
    rms = math.sqrt(sum(sample * sample for sample in flat) / len(flat))
    peak = max(abs(sample) for sample in flat)
    return {
        "source": str(source),
        "destination": str(destination),
        "duration_seconds": loop_frames / SAMPLE_RATE,
        "rms_dbfs": 20.0 * math.log10(max(rms, 1e-12)),
        "peak_dbfs": 20.0 * math.log10(max(peak, 1e-12)),
        "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
    }


def prepare_reference_bundle(source: Path, destination_dir: Path) -> dict[str, dict[str, float | str]]:
    """Create the two normalized local layers used by the V4 RPM crossfade."""
    return {
        "idle": prepare_reference(
            source, destination_dir / "ferrari_sf90_idle_residual.wav",
            start_seconds=1.0, loop_frames=12000, cadence_hz=61.5,
            highpass_hz=90.0, lowpass_hz=4000.0,
        ),
        "high": prepare_reference(
            source, destination_dir / "ferrari_sf90_high_residual.wav",
            start_seconds=22.75, loop_frames=24000, cadence_hz=345.7,
            highpass_hz=180.0, lowpass_hz=12000.0,
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--start-seconds", type=float, default=1.0)
    parser.add_argument("--bundle", action="store_true")
    args = parser.parse_args()
    result = (
        prepare_reference_bundle(args.source, args.destination)
        if args.bundle
        else prepare_reference(args.source, args.destination, start_seconds=args.start_seconds)
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
