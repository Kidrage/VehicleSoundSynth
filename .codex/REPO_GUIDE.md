# VehicleSoundSynth V4 Repository Guide

## Purpose

Max 8.6.5 vehicle-sound V4 with isolated EV and combustion lifecycles, credible
V12/V10 hybrid archetypes, a seven-speed DCT event model, a dedicated in-cabin rumble
module, a six-anchor CC0 stereo engine-texture bank, licensed event assets, a short cabin IR, and a global
master EQ. The project uses only built-in Max/MSP/Gen objects.

## First Reads

- `AGENTS.md` — repository constraints and validation command.
- `PROJECT_HANDOFF.md` — current state and cross-agent notes.
- `README.md` — user-facing interface and message contract.
- `tests/test_project.py` — structural acceptance contract.

## Layout

- `tools/build_project.py` — sole writer for patchers, Gen DSP, presets, and fallback WAVs.
- `tools/process_assets.py` — deterministic curated-audio crop, resample, DC removal, fade, normalization, and hashing.
- `tools/prepare_engine_texture.py` — CC0 stereo residual filtering, envelope stabilization, Side decorrelation, cyclic seam closure, normalization, and hashing.
- `tools/prepare_local_reference.py` — retained analysis utility for the non-distributable local Ferrari target; not a runtime builder.
- `assets/asset_manifest.json` / `ASSET_LICENSES.md` — runtime-audio provenance authority.
- `main.maxpat` — runnable demo UI; DSP must start muted.
- `patchers/vehicle_engine~.maxpat` — public engine seam: one message inlet, two signal outlets.
- `patchers/ev_pad_driver~.maxpat` — generated vehicle-message to BEAP-CV adapter and safety trim.
- `patchers/ev_pad_beap~.maxpat` — embedded dual-channel BEAP pad; user tuning is preserved on rebuild.
- `patchers/reference_texture~.maxpat` — V10/V12-only six-anchor/twelve-loop stereo residual renderer.
- `patchers/`, `gen/`, `media/`, `presets/` — generated runtime resources.
- `tests/` — deterministic structural and resource checks.

## Commands

```sh
python3 tools/build_project.py --output-root .
python3 tools/process_assets.py --root .
python3 tools/prepare_engine_texture.py assets/raw/biholao_370278_ferrari_acceleration.wav media --metadata assets/engine_texture_bank.json
python3 -m unittest discover -s tests -v
python3 tools/audio_metrics.py render.wav --max-peak-dbfs -1 --min-rms-dbfs -45 --min-rumble-ratio 0.55 --max-subsonic-ratio 0.05 --max-low-side-ratio 0.05 --min-low-band-correlation 0.95 --max-mono-fold-rms-loss-db 1.5 --max-high-ratio 0.10 --min-spectral-peaks 6 --max-dominant-peak-ratio 0.50
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

- V4 is an independent full copy of V3 plus its saved documentation artifacts.
- Intended flow: lifecycle/state controller → powertrain/transient/road/rumble
  layers → RPM-adaptive three-band cabin field (120 Hz/2 kHz crossovers) →
  visible four-node master EQ → one final
  limiter/clip stage.
- `tools/build_mix_probe.py` provides 48 kHz NonRealTime measured EQ/trim/bypass checks.
- `tools/build_runtime_probe.py` builds a self-contained, monitor-muted Max
  recording bundle under `/private/tmp` for objective V12/V10 checks. Use unique
  probe names and only one isolated probe instance at a time on macOS.
- Open the project first and main second in the same Max instance; opening both
  files simultaneously can race project search-path registration.

## Repository State

- Branch: `codex/vehicle-sound-v4`; acoustic-rebuild fixed point is `f138ccb`.
- Remote: none.
- Avoid cache files such as `tests/__pycache__/`.
- Never edit sibling V1, V2, or V3 repositories while implementing V4.
