#!/usr/bin/env python3
"""Build normalized, loop-safe stereo engine residual anchors from licensed audio."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
import tempfile
import wave
from pathlib import Path
from typing import Any

from prepare_local_reference import SAMPLE_RATE, _biquad, _rbj
from process_assets import convert_to_pcm16_48k


DEFAULT_SPECS = (
    {"id": "065", "anchor_hz": 65.0, "variants": ((149.5, 4.10), (0.5, 4.70))},
    {"id": "110", "anchor_hz": 110.0, "variants": ((54.5, 4.10), (34.5, 4.70))},
    {"id": "180", "anchor_hz": 180.0, "variants": ((119.5, 4.10), (124.5, 4.70))},
    {"id": "260", "anchor_hz": 260.0, "variants": ((154.5, 4.10), (159.5, 4.70))},
    {"id": "380", "anchor_hz": 380.0, "variants": ((144.5, 4.10), (174.5, 4.70))},
    {"id": "520", "anchor_hz": 520.0, "variants": ((9.5, 4.10), (144.5, 4.70))},
)


def _read_stereo(path: Path) -> list[list[float]]:
    with wave.open(str(path), "rb") as handle:
        if handle.getsampwidth() != 2 or handle.getframerate() != SAMPLE_RATE:
            raise ValueError("texture source must be 48 kHz PCM16 WAV")
        channels = handle.getnchannels()
        if channels not in (1, 2):
            raise ValueError("texture source must be mono or stereo")
        frames = handle.getnframes()
        values = struct.unpack(f"<{frames * channels}h", handle.readframes(frames))
    if channels == 1:
        mono = [value / 32768.0 for value in values]
        return [mono[:], mono[:]]
    return [
        [values[index * 2 + channel] / 32768.0 for index in range(frames)]
        for channel in range(2)
    ]


def _filter_residual(samples: list[float], anchor_hz: float) -> list[float]:
    mean = sum(samples) / max(1, len(samples))
    output = [sample - mean for sample in samples]
    output = _biquad(output, _rbj("highpass", max(80.0, min(260.0, anchor_hz * 0.62))))
    for multiple in (1, 2, 3):
        frequency = anchor_hz * multiple
        if frequency < 8000.0:
            output = _biquad(output, _rbj("notch", frequency, 10.0))
    return _biquad(output, _rbj("lowpass", 9000.0, 0.707))


def _make_loop(
    channel: list[float], start: int, frames: int, crossfade_frames: int, anchor_hz: float,
) -> list[float]:
    preroll = min(start, SAMPLE_RATE)
    stop = start + frames
    if start < 0 or stop > len(channel):
        raise ValueError("texture window is outside the source WAV")
    filtered = _filter_residual(channel[start - preroll : stop], anchor_hz)[preroll:]
    loop = filtered[:frames]
    return loop


def _stabilize_envelope(channels: list[list[float]]) -> list[list[float]]:
    """Remove slow source-level rides without inventing periodic modulation."""
    mid = [(left + right) * 0.5 for left, right in zip(*channels)]
    block = round(SAMPLE_RATE * 0.10)
    levels = [
        math.sqrt(sum(value * value for value in mid[index:index + block]) / block)
        for index in range(0, len(mid), block)
        if len(mid[index:index + block]) == block
    ]
    if not levels:
        return channels
    target = sorted(levels)[len(levels) // 2]
    gains = [max(0.55, min(1.8, target / max(level, 1e-9))) for level in levels]
    gains = [gains[0]] + [
        gains[index - 1] * 0.25 + gains[index] * 0.75
        for index in range(1, len(gains))
    ]
    output = [[], []]
    for index in range(len(mid)):
        position = index / block
        low = min(int(position), len(gains) - 1)
        high = min(low + 1, len(gains) - 1)
        blend = position - int(position)
        gain = gains[low] * (1.0 - blend) + gains[high] * blend
        output[0].append(channels[0][index] * gain)
        output[1].append(channels[1][index] * gain)
    return output


def _enhance_stereo(channels: list[list[float]]) -> list[list[float]]:
    """Add band-limited, mono-compatible microstructure when the source is narrow."""
    mid = [(left + right) * 0.5 for left, right in zip(*channels)]
    source_side = [(left - right) * 0.5 for left, right in zip(*channels)]
    delayed = [
        0.55 * mid[max(0, index - 17)]
        - 0.35 * mid[max(0, index - 43)]
        + 0.25 * mid[max(0, index - 79)]
        for index in range(len(mid))
    ]
    decorrelated = _biquad(delayed, _rbj("highpass", 180.0, 0.707))
    side = [source + decor for source, decor in zip(source_side, decorrelated)]
    projection = sum(m * s for m, s in zip(mid, side)) / max(
        sum(value * value for value in mid), 1e-30
    )
    side = [s - projection * m for m, s in zip(mid, side)]
    mid_rms = math.sqrt(sum(value * value for value in mid) / max(1, len(mid)))
    side_rms = math.sqrt(sum(value * value for value in side) / max(1, len(side)))
    side_gain = 0.34 * mid_rms / max(side_rms, 1e-30)
    side = [value * side_gain for value in side]
    return [
        [m + s for m, s in zip(mid, side)],
        [m - s for m, s in zip(mid, side)],
    ]


def _close_loop_seam(channels: list[list[float]], crossfade_frames: int) -> list[list[float]]:
    """Ease each tail exactly onto its first sample so groove~ cannot click."""
    frames = len(channels[0])
    fade = min(crossfade_frames, frames // 4)
    for channel in channels:
        correction = channel[0] - channel[-1]
        for index in range(fade):
            weight = 0.5 - 0.5 * math.cos(math.pi * (index + 1) / fade)
            channel[frames - fade + index] += correction * weight
        channel[-1] = channel[0]
    return channels


def _write_normalized(
    channels: list[list[float]], destination: Path, target_rms_dbfs: float,
) -> dict[str, Any]:
    flat = [sample for channel in channels for sample in channel]
    rms = math.sqrt(sum(sample * sample for sample in flat) / max(1, len(flat)))
    peak = max((abs(sample) for sample in flat), default=0.0)
    if rms <= 1e-12 or peak <= 1e-12:
        raise ValueError("texture window is silent after residual filtering")
    target_rms = 10.0 ** (target_rms_dbfs / 20.0)
    ceiling = 10.0 ** (-3.0 / 20.0)

    def render(gain: float) -> list[list[float]]:
        return [
            [ceiling * math.tanh(value * gain / ceiling) for value in channel]
            for channel in channels
        ]

    low, high = 0.0, max(1.0, target_rms / rms * 4.0)
    for _ in range(48):
        gain = (low + high) * 0.5
        candidate = render(gain)
        candidate_rms = math.sqrt(
            sum(value * value for channel in candidate for value in channel)
            / max(1, len(flat))
        )
        if candidate_rms < target_rms:
            low = gain
        else:
            high = gain
    normalized = render((low + high) * 0.5)
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = b"".join(
        struct.pack("<hh", round(normalized[0][index] * 32767), round(normalized[1][index] * 32767))
        for index in range(len(normalized[0]))
    )
    with wave.open(str(destination), "wb") as handle:
        handle.setnchannels(2)
        handle.setsampwidth(2)
        handle.setframerate(SAMPLE_RATE)
        handle.writeframes(payload)
    flat = [sample for channel in normalized for sample in channel]
    final_rms = math.sqrt(sum(sample * sample for sample in flat) / len(flat))
    final_peak = max(abs(sample) for sample in flat)
    return {
        "path": str(destination),
        "frames": len(normalized[0]),
        "sample_rate": SAMPLE_RATE,
        "rms_dbfs": 20.0 * math.log10(max(final_rms, 1e-12)),
        "peak_dbfs": 20.0 * math.log10(max(final_peak, 1e-12)),
        "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
    }


def prepare_texture_bank(
    source: Path,
    destination: Path,
    *,
    specs: tuple[dict[str, Any], ...] = DEFAULT_SPECS,
    target_rms_dbfs: float = -18.0,
    crossfade_seconds: float = 0.25,
) -> dict[str, Any]:
    channels = _read_stereo(source)
    outputs: list[dict[str, Any]] = []
    for spec in specs:
        for variant_index, (start_seconds, duration_seconds) in enumerate(spec["variants"]):
            frames = round(duration_seconds * SAMPLE_RATE)
            start = round(start_seconds * SAMPLE_RATE)
            processed = [
                _make_loop(channel, start, frames, round(crossfade_seconds * SAMPLE_RATE), spec["anchor_hz"])
                for channel in channels
            ]
            processed = _stabilize_envelope(processed)
            processed = _enhance_stereo(processed)
            processed = _close_loop_seam(processed, round(crossfade_seconds * SAMPLE_RATE))
            suffix = "a" if variant_index == 0 else "b"
            output = destination / f"engine_texture_{spec['id']}_{suffix}.wav"
            metadata = _write_normalized(processed, output, target_rms_dbfs)
            metadata.update({"anchor_hz": spec["anchor_hz"], "variant": suffix})
            outputs.append(metadata)
    return {
        "source": str(source),
        "target_rms_dbfs": target_rms_dbfs,
        "crossfade_seconds": crossfade_seconds,
        "outputs": outputs,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--metadata", type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as directory:
        converted = Path(directory) / "source_pcm16.wav"
        convert_to_pcm16_48k(args.source, converted)
        result = prepare_texture_bank(converted, args.destination)
    result["source"] = str(args.source)
    result["source_sha256"] = hashlib.sha256(args.source.read_bytes()).hexdigest()
    if args.metadata:
        args.metadata.parent.mkdir(parents=True, exist_ok=True)
        args.metadata.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
