# VehicleSoundSynth V4 Repository Guide

## Purpose

Max 8.6.5 vehicle-sound V4 with isolated EV and combustion lifecycles, credible
V12/V10 hybrid archetypes, a seven-speed DCT event model, a dedicated in-cabin rumble
module, a six-anchor CC0 stereo engine-texture bank, optional local Ferrari startup/idle-body layers, licensed event assets, a short cabin IR, and a global
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
- `tools/prepare_local_reference.py` — builds ignored, non-distributable Ferrari startup/idle-body runtime layers plus comparison residuals.
- `assets/asset_manifest.json` / `ASSET_LICENSES.md` — runtime-audio provenance authority.
- `main.maxpat` — runnable demo UI; DSP must start muted.
- `patchers/vehicle_engine~.maxpat` — public engine seam: one message inlet, two signal outlets.
- `patchers/ev_pad_driver~.maxpat` — generated vehicle-message to BEAP-CV adapter and safety trim.
- `patchers/ev_pad_beap~.maxpat` — embedded dual-channel BEAP pad; user tuning is preserved on rebuild.
- `patchers/reference_texture~.maxpat` — V10/V12 six-anchor CC0 bank plus low-RPM local idle-body renderer.
- `patchers/`, `gen/`, `media/`, `presets/` — generated runtime resources.
- `tests/` — deterministic structural and resource checks.

## Commands

```sh
python3 tools/build_project.py --output-root .
python3 tools/process_assets.py --root .
python3 tools/prepare_engine_texture.py assets/raw/biholao_370278_ferrari_acceleration.wav media --metadata assets/engine_texture_bank.json
python3 tools/prepare_local_reference.py /Users/saintpeter/Desktop/Ferrari.wav media/local --bundle
python3 -m unittest discover -s tests -v
python3 tools/audio_metrics.py idle_v12.wav --expected-fundamental-hz 78 --max-harsh-ratio 0.001 --max-high-ratio 0.00001 --min-low-mid-ratio 0.96 --min-rumble-ratio 0.90 --max-spectral-centroid-hz 100 --max-rolloff-95-hz 160 --max-sample-delta-peak-over-rms 0.15 --max-upper-harmonic-ratio 0.001 --max-harmonic-slope-db-per-octave -7 --max-clipped-sample-ratio 0
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
- V10/V12 Gen pulses are wrap-continuous raised cosines. A dynamic low-pass
  opens from roughly 3 kHz at idle toward 8.4 kHz at high RPM; saturation drive
  is deliberately mild at idle. Local Ferrari idle texture follows firing rate
  only below 180 Hz, and the local startup layer fades for 350 ms after catch.
- `tools/build_mix_probe.py` provides 48 kHz NonRealTime measured EQ/trim/bypass checks.
- `tools/build_runtime_probe.py` builds a self-contained, monitor-muted Max
  recording bundle under `/private/tmp` for objective V12/V10 checks. Use unique
  probe names and only one isolated probe instance at a time on macOS.
- Open the project first and main second in the same Max instance; opening both
  files simultaneously can race project search-path registration.

## Repository State

- Branch: `codex/vehicle-sound-v4`; acoustic-rebuild fixed point is `f138ccb`.
- Remote: none.
- `media/local/` is ignored and must never be committed or mirrored; missing
  Ferrari layers intentionally fall back to the tracked CC0 paths.
- Avoid cache files such as `tests/__pycache__/`.
- Never edit sibling V1, V2, or V3 repositories while implementing V4.
