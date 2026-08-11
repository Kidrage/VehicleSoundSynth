# VehicleSoundSynth V3 Repository Guide

## Purpose

Max 8.6.5 vehicle-sound V3 with isolated EV and combustion lifecycles, credible
V12/V10 archetypes, a seven-speed DCT event model, a dedicated in-cabin rumble
module, licensed field-recorded event assets, a short cabin IR, and a global
master EQ. The project uses only built-in Max/MSP/Gen objects.

## First Reads

- `AGENTS.md` — repository constraints and validation command.
- `PROJECT_HANDOFF.md` — current state and cross-agent notes.
- `README.md` — user-facing interface and message contract.
- `tests/test_project.py` — structural acceptance contract.

## Layout

- `tools/build_project.py` — sole writer for patchers, Gen DSP, presets, and fallback WAVs.
- `tools/process_assets.py` — deterministic curated-audio crop, resample, DC removal, fade, normalization, and hashing.
- `assets/asset_manifest.json` / `ASSET_LICENSES.md` — runtime-audio provenance authority.
- `main.maxpat` — runnable demo UI; DSP must start muted.
- `patchers/vehicle_engine~.maxpat` — public engine seam: one message inlet, two signal outlets.
- `patchers/ev_pad_driver~.maxpat` — generated vehicle-message to BEAP-CV adapter and safety trim.
- `patchers/ev_pad_beap~.maxpat` — embedded dual-channel BEAP pad; user tuning is preserved on rebuild.
- `patchers/`, `gen/`, `media/`, `presets/` — generated runtime resources.
- `tests/` — deterministic structural and resource checks.

## Commands

```sh
python3 tools/build_project.py --output-root .
python3 tools/process_assets.py --root .
python3 -m unittest discover -s tests -v
python3 tools/audio_metrics.py render.wav --max-peak-dbfs -1 --min-rms-dbfs -45 --min-rumble-ratio 0.55 --max-subsonic-ratio 0.05 --max-high-ratio 0.10 --min-spectral-peaks 6 --max-dominant-peak-ratio 0.50
```

Regenerate twice and compare hashes when generator determinism matters. Never
hand-edit generated `.maxpat`, `.gendsp`, or `.wav` files except the explicitly
user-tunable `patchers/ev_pad_beap~.maxpat`. The project generator preserves that
file after its first seed. The project generator
never overwrites curated runtime WAVs already present in `media/`.

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
- `tools/build_mix_probe.py` provides measured EQ/trim/bypass checks.
- `tools/build_runtime_probe.py` builds a self-contained, monitor-muted Max
  recording bundle under `/private/tmp` for objective V12/V10 checks. Use unique
  probe names and one Core Audio instance at a time on macOS.
- Open the project first and main second in the same Max instance; opening both
  files simultaneously can race project search-path registration.

## Repository State

- Branch: `codex/vehicle-sound-v3`; V2 commit `b8cefa5` is the baseline.
- Remote: none.
- Avoid cache files such as `tests/__pycache__/`.
- Never edit the sibling V1 or V2 repositories while implementing V3.
