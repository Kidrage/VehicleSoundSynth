#!/usr/bin/env python3
"""Convert, crop, clean, normalize, and hash licensed source recordings."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
import subprocess
import tempfile
import wave
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_pcm16(path: Path) -> tuple[int, int, list[list[float]]]:
    with wave.open(str(path), "rb") as handle:
        if handle.getsampwidth() != 2:
            raise ValueError(f"{path}: expected PCM16 after conversion")
        channels = handle.getnchannels()
        sample_rate = handle.getframerate()
        payload = handle.readframes(handle.getnframes())
    values = struct.unpack(f"<{len(payload) // 2}h", payload)
    separated = [[] for _ in range(channels)]
    for index, value in enumerate(values):
        separated[index % channels].append(value / 32768.0)
    return sample_rate, channels, separated


def process_pcm16_wav(
    source: Path,
    destination: Path,
    *,
    start_seconds: float,
    duration_seconds: float,
    channel: str = "mix",
    peak_dbfs: float = -3.0,
    fade_ms: float = 5.0,
    max_frames: int | None = None,
) -> dict[str, int | float | str]:
    sample_rate, channel_count, separated = _read_pcm16(source)
    if sample_rate != 48000:
        raise ValueError(f"{source}: expected 48 kHz, got {sample_rate}")
    start = max(0, round(start_seconds * sample_rate))
    stop = min(len(separated[0]), start + round(duration_seconds * sample_rate))
    if max_frames is not None:
        stop = min(stop, start + max_frames)
    if stop <= start:
        raise ValueError(f"{source}: empty crop")
    if channel == "left":
        samples = separated[0][start:stop]
    elif channel == "right":
        samples = separated[min(1, channel_count - 1)][start:stop]
    elif channel == "mix":
        samples = [
            sum(separated[item][index] for item in range(channel_count)) / channel_count
            for index in range(start, stop)
        ]
    else:
        raise ValueError(f"unsupported channel selection: {channel}")

    dc = sum(samples) / len(samples)
    samples = [value - dc for value in samples]
    peak = max(abs(value) for value in samples)
    target = 10.0 ** (peak_dbfs / 20.0)
    scale = target / peak if peak > 1e-9 else 1.0
    samples = [value * scale for value in samples]
    fade_frames = min(round(fade_ms * sample_rate / 1000.0), len(samples) // 2)
    for index in range(fade_frames):
        factor = index / max(1, fade_frames - 1)
        samples[index] *= factor
        samples[-1 - index] *= factor

    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = b"".join(
        struct.pack("<h", max(-32768, min(32767, round(value * 32767.0))))
        for value in samples
    )
    with wave.open(str(destination), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        handle.writeframes(payload)
    rms = math.sqrt(sum(value * value for value in samples) / len(samples))
    return {
        "path": str(destination),
        "frames": len(samples),
        "sample_rate": sample_rate,
        "peak_dbfs": 20.0 * math.log10(max(max(abs(value) for value in samples), 1e-12)),
        "rms_dbfs": 20.0 * math.log10(max(rms, 1e-12)),
        "sha256": sha256(destination),
    }


def convert_to_pcm16_48k(source: Path, destination: Path) -> None:
    # afconvert truncates some short PCM files when format conversion and SRC
    # are requested in the same pass on macOS. Convert sample format first,
    # then perform deterministic PCM rate conversion ourselves.
    with tempfile.TemporaryDirectory() as directory:
        native = Path(directory) / "native_rate_pcm16.wav"
        subprocess.run(
            ["/usr/bin/afconvert", "-f", "WAVE", "-d", "LEI16", str(source), str(native)],
            check=True,
            capture_output=True,
            text=True,
        )
        with wave.open(str(native), "rb") as handle:
            channels = handle.getnchannels()
            source_rate = handle.getframerate()
            payload = handle.readframes(handle.getnframes())
        if source_rate != 48000:
            values = struct.unpack(f"<{len(payload) // 2}h", payload)
            source_frames = len(values) // channels
            output_frames = max(1, round(source_frames * 48000 / source_rate))
            resampled: list[int] = []
            for output_index in range(output_frames):
                source_position = output_index * source_rate / 48000
                left_index = min(int(source_position), source_frames - 1)
                right_index = min(left_index + 1, source_frames - 1)
                fraction = source_position - left_index
                for channel_index in range(channels):
                    left = values[left_index * channels + channel_index]
                    right = values[right_index * channels + channel_index]
                    resampled.append(round(left + (right - left) * fraction))
            payload = struct.pack(f"<{len(resampled)}h", *resampled)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with wave.open(str(destination), "wb") as handle:
            handle.setnchannels(channels)
            handle.setsampwidth(2)
            handle.setframerate(48000)
            handle.writeframes(payload)


def process_manifest(root: Path, manifest_path: Path) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for asset in manifest["assets"]:
        raw = root / asset["raw_path"]
        outputs = asset.get("outputs", [])
        if not raw.is_file() or not outputs:
            continue
        asset["raw_sha256"] = sha256(raw)
        with tempfile.TemporaryDirectory() as directory:
            converted = Path(directory) / "converted.wav"
            convert_to_pcm16_48k(raw, converted)
            for output in outputs:
                result = process_pcm16_wav(
                    converted,
                    root / output["path"],
                    start_seconds=output["start_seconds"],
                    duration_seconds=output["duration_seconds"],
                    channel=output.get("channel", "mix"),
                    peak_dbfs=output.get("peak_dbfs", -3.0),
                    fade_ms=output.get("fade_ms", 5.0),
                    max_frames=output.get("max_frames"),
                )
                output["processed_sha256"] = result["sha256"]
                output["frames"] = result["frames"]
                output["sample_rate"] = result["sample_rate"]
        asset["status"] = "processed"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = args.manifest or root / "assets" / "asset_manifest.json"
    process_manifest(root, manifest)


if __name__ == "__main__":
    main()
