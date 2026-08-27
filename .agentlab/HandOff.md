# VehicleSoundSynth V5 Repository HandOff

## Repository Identity

- Canonical remote: `git@github.com:Kidrage/VehicleSoundSynth.git`
- Target runtime: Max 8.6.5 on macOS
- Canonical branch: `main`.
- Authoritative keyboard, seven-module mixer, and kick-impact Pop implementation
  fixed point: `f85c1ca`, contained in canonical `main`; later descendants are
  handoff-only.

## Delivered Change

- The keyboard adapter now follows the installed Max 8.6.5 `gate` reference:
  Internal Manual enable enters control inlet 0, while W/S key state enters data
  inlet 1. W is immediate full throttle and S remains the fixed 0.65 service
  brake; Gamepad LT/RT, `drive_model.js`, and the normalized public pedal seam
  are unchanged.
- Every EV/V10/V12 main runtime embeds one generated `MODULE MIXER` with seven
  dB faders: Sound DNA, Start, Pop/Event, Soundscape, Road/Air, Cabin Rumble,
  and Master. Each profile auto-saves to its own ignored
  `presets/local/<profile>_module_mixer.json`; Save/Reload/Reset are explicit.
  Start is now independently trimmed before the shared transient/Event level,
  and Pop/Event is the post-voice total gain requested for all Pop layers.
- V10/V12 Pop defaults are a low, short pressure impact rather than a snare:
  Global Pitch `-5/-6`, Low Pressure `1.0/1.0`, Body `1.30/1.35`, Crack
  `0.008/0.006`, and Decay `0.75/0.62`. The generated host adds a 600/520 Hz
  air ceiling after its 28 Hz subsonic high-pass. The editable Pop Designer
  remains authoritative over pitch, drop, body/crack tuning, decay and levels.
- `Audition One Hit` remains the repeatable tone check. `Test Pop` and physical
  loaded lift-off retain the seeded 1--5 hit, 140--200 ms descending schedule;
  shift/explicit events remain one hit, and physical events still require
  Backfire Enable, ignition and engine-running state.
- Sound DNA, cinematic start, shared Soundscape, public throttle/brake values,
  and fixed 20 ms speed/RPM/shift integration are otherwise unchanged.

## Repository Rules

- Edit generated Max JSON only through `tools/build_project.py`.
- Seed-once Sound DNA, Soundscape, start and backfire BEAP graphs are user-owned
  and must not be overwritten by regeneration.
- V10/V12 continuous sound remains procedural; local Ferrari media is not a
  distributable continuous-runtime source.
- Before delivery run deterministic regeneration, all tests, audio probes,
  `git diff --check`, real Max smoke/save/close, and confirm Max is fully exited.

## Local Save Archive

- The two intentionally reseeded Pop Designer panels were backed up before
  replacement at
  `/Users/saintpeter/Downloads/.VehicleSoundSynth-Backups/20260827-keyboard-pop-mixer/`.

## Validation

- 161/161 unit tests pass; `git diff --check` passes. Fifteen builder-owned
  generated outputs and both intentionally reseeded Pop panels are byte-identical
  to an independent fresh generator build. V4 remains clean and `drive_model.js`
  has no diff.
- Fresh real-Max single-hit renders are non-silent and unclipped. V10 measured
  peak `-5.34` dBFS, 23 ms attack centroid `149` Hz, 20--180 Hz energy `0.803`,
  snare-band energy `0.000376`, and a `180` ms -20 dB tail. V12 measured
  `-3.76`, `91` Hz, `0.942`, `0.000143`, and `170` ms respectively.
- Seeded 1--5-hit burst renders are also unclipped: V10/V12 peak at
  `-1.69/-2.47` dBFS and retain the 140--200 ms schedule. The installed
  NonRealTime driver again wrote 44.1 kHz, so the metrics are comparative/audio
  safety evidence rather than a 48 kHz delivery claim.
- Final headless Max 8.6.5 loads covered the project and EV/V10/V12 separately.
  Current and rotated logs contain zero missing-object, Gen/function,
  invalid-category, or patchcord-range blocker matches. The direct-open
  search-path notices remain warning-only; abstractions loaded, and all three
  ignored per-profile module-mixer JSON states were written with expected
  defaults.
- The official `crashrecovery` preference was backed up, temporarily changed
  from Ask to Never for headless smoke, and restored byte-for-byte to Ask. Every
  task-owned process had zero windows before exact termination. The user also
  authorized closing former PID 25676; final process inspection and AppleScript
  both report no Max instance running.
