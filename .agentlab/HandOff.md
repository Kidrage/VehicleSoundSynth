# VehicleSoundSynth V5 Repository HandOff

## Repository Identity

- Canonical remote: `git@github.com:Kidrage/VehicleSoundSynth.git`
- Target runtime: Max 8.6.5 on macOS
- Canonical branch: `main`.
- Authoritative Soundscape stabilization/persistence implementation fixed point:
  `973a2f2`, contained in canonical `main`; later descendants are handoff-only.

## Delivered Change

- Each runtime now embeds one directly audible Soundscape instance. Main-page
  controls and `Open Designer` address that same instance; there is no detached
  `poly~` copy. Live macro and BEAP edits save to ignored per-profile
  `<profile>_soundscape.json` state and reload on the next launch.
- `Save Profile Sound` and runtime close/switch save the module mixer,
  Soundscape, and per-profile vehicle-bus EQ together. Reload and factory reset
  are explicit. `pattrstorage` no longer feeds a periodic self-save loop.
- The shared seed-once Soundscape is retuned as a restrained root/fifth/octave
  pad: 0.035/0.009 Hz drift, very small pitch depth, lower filter resonance,
  slower chorus, long envelope/reverb, 70 Hz high-pass, and one portable
  saturation stage. EV/V10/V12 retain independent macro and EQ states.
- Direct Soundscape DSP suspends after disable to reduce idle CPU. Drivetrain,
  pedal, Pop-event, Sound DNA, and engine-generation behavior are unchanged.

## Repository Rules

- Edit generated Max JSON only through `tools/build_project.py`.
- Seed-once Sound DNA, Soundscape, start and backfire BEAP graphs are user-owned
  and must not be overwritten by regeneration.
- V10/V12 continuous sound remains procedural; local Ferrari media is not a
  distributable continuous-runtime source.
- Before delivery run deterministic regeneration, all tests, audio probes,
  `git diff --check`, real Max smoke/save/close, and confirm Max is fully exited.

## Local Save Archive

- The pre-existing V10 top-level Max save was preserved at
  `/private/tmp/vss-live-tuning-backup.1CYB1C/VehicleSoundSynth-V10.maxpat`
  (SHA-256 `41471bdc72545afac23774f2893c4c25461f42f95e400f05b4f5122437032689`).

## Validation

- 166/166 unit tests pass; `git diff --check` passes. All changed generated and
  seed outputs are byte-identical to an independent fresh generator build. V4
  remains clean at tag `v4.0.0`; `drive_model.js` is unchanged.
- Fresh final EV/V10/V12 Soundscape renders are non-silent and unclipped. Their
  spectral centroids are about 151/125/92 Hz and all measured harsh/high-band
  ratios remain far below the documented `0.001` safety gate. V10 and V12 long
  renders have only 1.37/1.51 dB envelope spread after the chorus reduction.
- Final Max 8.6.5 loads covered the project and EV/V10/V12 separately.
  Current and rotated logs contain zero missing-object, Gen/function,
  invalid-category, or patchcord-range blocker matches. The direct-open
  search-path notices remain warning-only; abstractions loaded, and all three
  ignored per-profile module-mixer, Soundscape, and EQ JSON states were written
  with complete expected state. A timed check proved the former periodic
  Soundscape state-file rewrite no longer occurs.
- The official `crashrecovery` preference was backed up, temporarily changed
  from Ask to Never for headless smoke, and restored byte-for-byte to Ask. Every
  task-owned process had zero windows before exact termination. Pre-existing
  zero-window Max PID `35660` (started at 13:38, before this task) was preserved;
  final AppleScript therefore reports Max running.
