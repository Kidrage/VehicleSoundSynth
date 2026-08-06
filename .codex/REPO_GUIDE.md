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

Runtime smoke-check the generated project in Max 8.6.5 after structural tests.
On macOS, Max writes load diagnostics to
`~/Library/Application Support/Cycling '74/Max 8/Logs/Max.log`; treat
`invalid category`, `No such object`, `function ... not found`, and
`patchcord outlet out of range` as release-blocking.

## Runtime State

- The working tree fixes the Max 8.6.5 load failures from HEAD `7dada34`:
  project categories/search paths, unsupported expressions/objects, DSP control,
  `slide` arguments, and explicit Gen `out 1` / `out 2` ports.
- A fresh Max 8.6.5 project load completes with zero errors and zero warnings.
- An automated two-channel engine recording measured non-zero output
  (`RMS=3713`, `Peak=18159` at 48 kHz).
- Open the project first and main second in the same Max instance; opening both
  files simultaneously can race project search-path registration.

## Repository State

- Branch: `codex/vehicle-sound-mvp`; initial MVP commit is the local baseline.
- Remote: none.
- Avoid cache files such as `tests/__pycache__/`.
