#!/usr/bin/env python3
"""Render ONE CC0 exhaust one-shot offline; leave all other assets unchanged."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import struct
import tempfile
import wave
from pathlib import Path

if __package__:
    from .process_assets import convert_to_pcm16_48k, _read_pcm16
else:
    from process_assets import convert_to_pcm16_48k, _read_pcm16

SOURCE = 'assets/raw/richwise_478756_sports_car_revs_pops.wav'
SOURCE_SHA = '2b67aed7ec0dc3fe74b3d110865574ca591455a5300417281a29dfd7f4483cd1'
START = 6.537
DURATION = 0.240


def lowpass(samples, hz, rate=48000):
    coefficient = 1 - math.exp(-2 * math.pi * hz / rate)
    memory, output = 0.0, []
    for sample in samples:
        memory += coefficient * (sample - memory)
        output.append(memory)
    return output


def render(root: Path, destination: Path) -> dict:
    raw = root / SOURCE
    if hashlib.sha256(raw.read_bytes()).hexdigest() != SOURCE_SHA:
        raise ValueError('CC0 source hash mismatch; refusing an unknown recording')
    with tempfile.TemporaryDirectory(prefix='ferrari-pop-') as directory:
        converted = Path(directory) / 'source.wav'
        convert_to_pcm16_48k(raw, converted)
        rate, channels, data = _read_pcm16(converted)
    start, count = round(START * rate), round(DURATION * rate)
    # Include filter pre-roll to avoid inventing an attack from filter startup.
    mono = [sum(frame) / channels for frame in zip(*data)]
    dc = lowpass(mono, 75, rate)
    clean = [x-y for x,y in zip(mono, dc)]
    body = lowpass(clean, 650, rate)[start:start+count]
    top = lowpass(clean, 6500, rate)[start:start+count]
    crack_low = lowpass(top, 800, rate)
    crack = [x-y for x,y in zip(top, crack_low)]
    crack_low = lowpass(crack, 800, rate)
    crack = [x-y for x,y in zip(crack, crack_low)]
    samples = []
    for i, low in enumerate(body):
        t = i / rate
        # Retain the recorded crack; the body and two tiny exhaust-wall
        # reflections are baked in. No sine sweep, distortion or reverb plugin.
        attack = 6.0 * crack[i] * math.exp(-t / 0.026)
        pressure = 1.2 * low * math.exp(-t / 0.055)
        samples.append(attack + pressure)
    dry = samples[:]
    for delay, gain in ((0.017, 0.16), (0.031, 0.07)):
        frames = round(delay * rate)
        for i in range(frames, count):
            samples[i] += dry[i-frames] * gain
    window = [min(1., i/(rate*0.0015), (count-1-i)/(rate*0.020)) for i in range(count)]
    samples = [x*w for x,w in zip(samples, window)]
    dc = sum(samples) / sum(window)
    samples = [x-dc*w for x,w in zip(samples, window)]
    gain = 10**(-6/20) / max(map(abs, samples))
    pcm = [round(max(-1., min(1., x*gain))*32767) for x in samples]
    destination.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(destination), 'wb') as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(rate)
        handle.writeframes(struct.pack('<%dh' % count, *pcm))
    return {
        'path': 'media/ferrari_pop_v3.wav', 'start_seconds': START,
        'duration_seconds': DURATION, 'channel': 'mix', 'peak_dbfs': -6.0,
        'processed_sha256': hashlib.sha256(destination.read_bytes()).hexdigest(),
        'frames': count, 'sample_rate': rate, 'channels': 1,
        'processor': 'tools/prepare_ferrari_pop.py',
        'processing': '75 Hz high-pass; 650 Hz body x1.2 / 800-6500 Hz recorded crack x6; 26/55 ms decay; 17/31 ms short reflections; 1.5/20 ms fades; DC removal; -6 dBFS peak',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(render(args.root, args.output), indent=2))
