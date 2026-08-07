# VehicleSoundSynth V2 Repository Guide

## Purpose

Max 8.6.5 vehicle-sound V2 with isolated EV and combustion lifecycles, credible
V12/V10 archetypes, a seven-speed DCT event model, and a global master EQ. The
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
python3 tools/build_project.py --output-root .
python3 -m unittest discover -s tests -v
python3 tools/audio_metrics.py render.wav --max-peak-dbfs -1 --min-rms-dbfs -60 --max-high-ratio 0.20
```

Regenerate twice and compare hashes when generator determinism matters. Never
hand-edit generated `.maxpat`, `.gendsp`, or `.wav` files.

Runtime smoke-check the generated project in Max 8.6.5 after structural tests.
On macOS, Max writes load diagnostics to
`~/Library/Application Support/Cycling '74/Max 8/Logs/Max.log`; treat
`invalid category`, `No such object`, `function ... not found`, and
`patchcord outlet out of range` as release-blocking.

## Runtime State

- V2 starts from the verified V1 runtime-fix commit `594acd1`.
- Implemented flow: lifecycle/state controller → continuous/event/road layers
  → cabin → four-band master EQ → one final limiter/clip stage.
- `tools/build_runtime_probe.py` builds a self-contained, monitor-muted Max
  recording bundle under `/private/tmp` for objective V12 idle checks.
- Latest Max 8.6.5 project/main load completed with zero Console errors. The
  monitor-muted V12 idle probe measured peak `-25.78 dBFS`, RMS `-35.33 dBFS`,
  and `67.99%` energy from 40–500 Hz.
- Open the project first and main second in the same Max instance; opening both
  files simultaneously can race project search-path registration.

## Repository State

- Branch: `codex/vehicle-sound-v2`; V1 commit `594acd1` is the local baseline.
- Remote: none.
- Avoid cache files such as `tests/__pycache__/`.
- Never edit the sibling V1 repository while implementing V2.
