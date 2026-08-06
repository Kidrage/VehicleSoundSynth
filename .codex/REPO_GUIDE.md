# VehicleSoundSynth Repository Guide

## Purpose

Max 8.6.5 vehicle-sound MVP with three continuously morphable archetypes. The
project is generator-owned and uses built-in Max/MSP/Gen objects only.

## First Reads

- `AGENTS.md` — repository constraints and validation command.
- `PROJECT_HANDOFF.md` — current state and cross-agent notes.
- `README.md` — user-facing interface and message contract.
- `tests/test_project.py` — structural acceptance contract.

## Layout

- `tools/build_project.py` — sole writer for generated patchers, Gen DSP, and WAVs.
- `main.maxpat` — runnable demo UI; DSP must start muted.
- `patchers/vehicle_engine~.maxpat` — public engine seam: one message inlet, two signal outlets.
- `patchers/`, `gen/`, `media/`, `presets/` — generated runtime resources.
- `tests/` — deterministic structural and resource checks.

## Commands

```sh
python3 tools/build_project.py
python3 -m unittest discover -s tests -v
```

Regenerate twice and compare hashes when generator determinism matters. Never
hand-edit generated `.maxpat`, `.gendsp`, or `.wav` files.

## Repository State

- Branch: `codex/vehicle-sound-mvp`; initial MVP commit is the local baseline.
- Remote: none.
- Avoid cache files such as `tests/__pycache__/`.
