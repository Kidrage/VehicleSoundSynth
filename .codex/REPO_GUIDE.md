# VehicleSoundSynth V5 Repository Guide

## Purpose

Max 8.6.5 vehicle-sound V5, forked from stable V4 tag `v4.0.0`, with three independent fixed-profile runtimes. V10
and V12 continuous audio are procedural; Ferrari.wav is a V10 lifecycle-analysis
target and may supply only the optional ignored realistic-start one-shot. EV has
three suspendable, user-editable BEAP soundscapes. The project also contains a
start-relative single-speed/seven-speed drivetrain, cabin rumble, licensed
events, short cabin IR, adjustable stereo compression, EQ, and peak protection.

## First Reads

- `AGENTS.md` — repository constraints and validation command.
- `PROJECT_HANDOFF.md` — current state and cross-agent notes.
- `README.md` — user-facing interface and message contract.
- `tests/test_project.py` — structural acceptance contract.

## Layout

- `tools/build_project.py` — sole writer for patchers, Gen DSP, presets, and fallback WAVs.
- `tools/process_assets.py` — deterministic curated-audio crop, resample, DC removal, fade, normalization, and hashing.
- `tools/prepare_engine_texture.py` — CC0 stereo residual filtering, envelope stabilization, Side decorrelation, cyclic seam closure, normalization, and hashing.
- `tools/prepare_local_reference.py` — builds the ignored Ferrari startup one-shot plus analysis-only legacy derivatives and hash manifests.
- `tools/analyze_reference_lifecycle.py` / `tools/validate_v10_lifecycle.py` — build the tracked 14-node target table and gate five synthesized roles plus the throttle-only full-drive render.
- `code/drive_model.js` — exact deterministic 20 ms EV/V10/V12 drivetrain used by Max and Node regression traces.
- `code/manual_input.js` — ES5/Node-testable HID normalization, curve,
  smoothing, Learn, source exclusivity, and safe pedal-release state.
- `assets/asset_manifest.json` / `ASSET_LICENSES.md` — runtime-audio provenance authority.
- `main.maxpat` — DSP-free launcher; it must never instantiate an engine.
- `VehicleSoundSynth-{EV,V10,V12}.maxpat` — independent runnable UIs; the
  single `Audio + Output` toggle enables both DSP and the output ramp.
- `patchers/keyboard_drive_ws.maxpat` — focus-aware Manual-mode W/S throttle
  and brake ramps with forced release when leaving Manual.
- `patchers/manual_input.maxpat` — generated deep module that selects the
  keyboard adapter or Max's built-in macOS `hi` adapter and exposes only
  normalized throttle/brake to the existing drivetrain.
- `patchers/vehicle_engine_{ev,v10,v12}~.maxpat` — fixed public seams.
- `patchers/{ev,v10,v12}_powertrain~.maxpat` — exactly one Gen per profile.
- `patchers/ev_soundscape_host~.maxpat` — mode crossfade plus cancellable inactive-voice suspension.
- `patchers/engine_start_beap~.maxpat`, `patchers/ev_*beap~.maxpat`, and V5's `patchers/{v10,v12}_{pad,backfire}_beap~.maxpat` — seed-once, user-tunable BEAP graphs.
- `patchers/`, `gen/`, `media/`, `presets/` — generated runtime resources.
- `tests/` — deterministic structural and resource checks.

## Commands

```sh
python3 tools/build_project.py --output-root .
python3 tools/process_assets.py --root .
python3 tools/prepare_engine_texture.py assets/raw/biholao_370278_ferrari_acceleration.wav media --metadata assets/engine_texture_bank.json
python3 tools/prepare_local_reference.py /Users/saintpeter/Desktop/Ferrari.wav media/local --bundle
python3 -m unittest discover -s tests -v
python3 tools/bind_drive_render.py v10_v10-lifecycle-drive_on_final.wav
python3 tools/validate_v10_lifecycle.py --drive-lifecycle-wav v10_v10-lifecycle-drive_on_final.wav idle=idle.wav acceleration=acceleration.wav loaded_hold=loaded.wav shift_recovery=shift.wav deceleration=deceleration.wav
```

Regenerate twice and compare hashes when generator determinism matters. Never
hand-edit generated `.maxpat`, `.gendsp`, or `.wav` files except the eight
seed-once BEAP patchers named above (engine start, three EV voices, two ICE
pads, and two ICE backfires). The project generator preserves those files
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
- V10 uses phase-continuous raised-cosine firing pulses and bounded harmonic,
  intake, load, acceleration, and overrun terms calibrated against the Ferrari
  lifecycle target table. V12 remains an independent procedural model; neither
  continuous runtime loads Ferrari/atlas/idle loops.
- `tools/build_mix_probe.py` provides 48 kHz NonRealTime measured EQ/trim/bypass checks.
- `tools/build_runtime_probe.py` builds a self-contained, monitor-muted Max
  recording bundle under `/private/tmp` for objective V12/V10 checks. Use unique
  probe names and only one isolated probe instance at a time on macOS.
- Open the project first and launcher second in the same Max instance. Launcher
  selection writes/closes the prior top-level runtime before opening one unique
  replacement. In Internal Manual, choose Keyboard and focus the runtime for
  W/S, or choose Gamepad and use HID Learn/configuration for RT/LT. Both adapters
  feed only throttle/brake into the unchanged drive model. Save user-tuned BEAP
  subpatchers, close every task-opened
  patcher, and quit Max after a smoke test.

## V5 Mainline

- Remove runtime shift/pop/crackle sample playback; keep only licensed starter one-shots.
- Deepen EV/V10/V12 idle and acceleration realism without discontinuous pitch or plastic high-frequency oscillators.
- Add physically triggered, seed-once BEAP backfire voices for V10/V12.
- Add independent, top-level-controlled, seed-once cinematic BEAP pads for V10/V12.
- Persist one shared vehicle-bus four-band EQ across all three runtimes with safe default fallback.
- Keep `main.maxpat` DSP-free and maintain one-runtime-at-a-time CPU behavior.
- Keep Keyboard and configurable macOS HID gamepad pedals mutually exclusive,
  with immediate zero release on source or Manual-mode exit.

## Repository State

- Branch: `codex/vehicle-sound-v5`; base is V4 stable tag `v4.0.0` at `6aa49d0`.
- Remote initially points to the local V4 clone and must be replaced by the private GitHub origin after publication.
- `media/local/` is ignored and must never be committed or mirrored; missing
  Ferrari layers intentionally fall back to the tracked CC0 paths.
- Avoid cache files such as `tests/__pycache__/`.
- Never edit sibling V1, V2, V3, or frozen V4 while implementing V5.
