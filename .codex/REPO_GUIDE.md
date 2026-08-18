# VehicleSoundSynth V4 Repository Guide

## Purpose

Max 8.6.5 vehicle-sound V4 with three independent fixed-profile runtimes. V10 is
sample-led by an optional local steady/accel/decel atlas, V12 uses an independent
procedural/CC0 hybrid, and EV has three suspendable BEAP soundscapes. The project
also contains a seven-speed DCT model, cabin rumble, licensed events, short cabin
IR, and global master EQ, using built-in Max/MSP/Gen/BEAP objects.

## First Reads

- `AGENTS.md` — repository constraints and validation command.
- `PROJECT_HANDOFF.md` — current state and cross-agent notes.
- `README.md` — user-facing interface and message contract.
- `tests/test_project.py` — structural acceptance contract.

## Layout

- `tools/build_project.py` — sole writer for patchers, Gen DSP, presets, and fallback WAVs.
- `tools/process_assets.py` — deterministic curated-audio crop, resample, DC removal, fade, normalization, and hashing.
- `tools/prepare_engine_texture.py` — CC0 stereo residual filtering, envelope stabilization, Side decorrelation, cyclic seam closure, normalization, and hashing.
- `tools/prepare_local_reference.py` — builds ignored, non-distributable Ferrari startup/idle-body layers and the 18-loop V10 state atlas with hash manifest.
- `assets/asset_manifest.json` / `ASSET_LICENSES.md` — runtime-audio provenance authority.
- `main.maxpat` — DSP-free launcher; it must never instantiate an engine.
- `VehicleSoundSynth-{EV,V10,V12}.maxpat` — independent runnable UIs; DSP starts muted.
- `patchers/vehicle_engine_{ev,v10,v12}~.maxpat` — fixed public seams.
- `patchers/{ev,v10,v12}_powertrain~.maxpat` — exactly one Gen per profile.
- `patchers/v10_state_renderer~.maxpat` — local atlas with mutually exclusive tracked fallback.
- `patchers/v12_texture_renderer~.maxpat` — tracked CC0 only; no local Ferrari dependency.
- `patchers/ev_soundscape_host~.maxpat` — 250 ms mode crossfade and inactive-voice suspension.
- `patchers/engine_start_beap~.maxpat` and `patchers/ev_*beap~.maxpat` — seed-once, user-tunable BEAP graphs.
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
hand-edit generated `.maxpat`, `.gendsp`, or `.wav` files except the four
seed-once BEAP patchers named above. The project generator preserves those files
after their first seed. The project generator
never overwrites curated runtime WAVs already present in `media/`.

Runtime smoke-check the generated project in Max 8.6.5 after structural tests.
On macOS, Max writes load diagnostics to
`~/Library/Application Support/Cycling '74/Max 8/Logs/Max.log`; treat
`invalid category`, `No such object`, `function ... not found`, and
`patchcord outlet out of range` as release-blocking.

## Runtime Design

- V4 is an independent full copy of V3 plus its saved documentation artifacts.
- Intended flow: fixed lifecycle/state controller → one powertrain plus transient/road/rumble
  layers → RPM-adaptive three-band cabin field (120 Hz/2 kHz crossovers) →
  visible four-node master EQ → one final
  limiter/clip stage.
- V10 atlas playback is clamped to 0.88-1.12x and crossfades steady/accel/decel
  states plus adjacent RPM anchors. Its procedural Gen is low-passed at 500 Hz
  and trimmed -18 dB. V12 is a separate procedural/CC0 hybrid.
- `tools/build_mix_probe.py` provides 48 kHz NonRealTime measured EQ/trim/bypass checks.
- `tools/build_runtime_probe.py` builds a self-contained, monitor-muted Max
  recording bundle under `/private/tmp` for objective V12/V10 checks. Use unique
  probe names and only one isolated probe instance at a time on macOS.
- Open the project first and launcher second in the same Max instance. Launcher
  selection writes/closes the prior top-level runtime before opening one unique
  replacement. Save user-tuned BEAP subpatchers, close every task-opened patcher,
  and quit Max after a smoke test.

## Repository State

- Branch: `codex/vehicle-sound-v4`; acoustic-rebuild fixed point is `f138ccb`.
- Remote: none.
- `media/local/` is ignored and must never be committed or mirrored; missing
  Ferrari layers intentionally fall back to the tracked CC0 paths.
- Avoid cache files such as `tests/__pycache__/`.
- Never edit sibling V1, V2, or V3 repositories while implementing V4.
