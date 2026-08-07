# VehicleSoundSynth V3 Repository Guide

## Purpose

Max 8.6.5 vehicle-sound V3 with isolated EV and combustion lifecycles, credible
V12/V10 archetypes, a seven-speed DCT event model, a dedicated in-cabin rumble
module, and a global master EQ. The project is generator-owned and uses only
built-in Max/MSP/Gen objects.

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
python3 tools/audio_metrics.py render.wav --max-peak-dbfs -1 --min-rms-dbfs -45 --min-rumble-ratio 0.55 --max-subsonic-ratio 0.05 --max-high-ratio 0.10
```

Regenerate twice and compare hashes when generator determinism matters. Never
hand-edit generated `.maxpat`, `.gendsp`, or `.wav` files.

Runtime smoke-check the generated project in Max 8.6.5 after structural tests.
On macOS, Max writes load diagnostics to
`~/Library/Application Support/Cycling '74/Max 8/Logs/Max.log`; treat
`invalid category`, `No such object`, `function ... not found`, and
`patchcord outlet out of range` as release-blocking.

## Runtime Design

- V3 starts from the verified V2 release commit `b8cefa5`.
- Intended flow: lifecycle/state controller → powertrain/transient/road/rumble
  layers → cabin low-frequency centering → four-band master EQ → one final
  limiter/clip stage.
- `tools/build_runtime_probe.py` builds a self-contained, monitor-muted Max
  recording bundle under `/private/tmp` for objective V12/V10 checks.
- Open the project first and main second in the same Max instance; opening both
  files simultaneously can race project search-path registration.

## Repository State

- Branch: `codex/vehicle-sound-v3`; V2 commit `b8cefa5` is the baseline.
- Remote: none.
- Avoid cache files such as `tests/__pycache__/`.
- Never edit the sibling V1 or V2 repositories while implementing V3.
