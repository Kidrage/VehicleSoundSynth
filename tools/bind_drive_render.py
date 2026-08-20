#!/usr/bin/env python3
"""Bind a completed Max drive-lifecycle WAV to its deterministic trace sidecar."""

from __future__ import annotations

import argparse
import hashlib
import json
import wave
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wav", type=Path)
    parser.add_argument("--sidecar", type=Path)
    args = parser.parse_args()
    wav = args.wav.resolve()
    sidecar = args.sidecar.resolve() if args.sidecar else wav.with_suffix(".drive.json")
    if not wav.is_file() or wav.is_symlink():
        raise SystemExit(f"WAV must be a regular file: {wav}")
    if not sidecar.is_file() or sidecar.is_symlink():
        raise SystemExit(f"sidecar must be a regular file: {sidecar}")
    trace = json.loads(sidecar.read_text(encoding="utf-8"))
    with wave.open(str(wav), "rb") as handle:
        trace.update({
            "wav_file": wav.name,
            "wav_sha256": hashlib.sha256(wav.read_bytes()).hexdigest(),
            "wav_frames": handle.getnframes(),
            "wav_sample_rate": handle.getframerate(),
        })
    temporary = sidecar.with_name(sidecar.name + ".tmp")
    temporary.write_text(json.dumps(trace, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(sidecar)
    print(sidecar)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
