# VehicleSoundSynth V5 Repository HandOff

## Repository Identity

- Canonical remote: `git@github.com:Kidrage/VehicleSoundSynth.git`
- Target runtime: Max 8.6.5 on macOS
- Canonical branch: `main`.
- Authoritative live/persistent sound-module implementation fixed point:
  `dc84aad`, contained in canonical `main`; later descendants are handoff-only.

## Delivered Change

- Main-page module buttons now address the audible nested instances. DNA remains
  live and saves per-profile ignored JSON; Soundscape opens the active shared
  BEAP voice and `Save Soundscape` writes that seed-once graph; V10/V12 Pop gains
  `Save Pop`/`Reload Pop` backed by ignored `<profile>_pop.json` files.
- The shared Soundscape factory patch is restored to a restrained
  root/fifth/octave voicing with 0.07/0.02 Hz drift, lower pitch depth and filter
  resonance, controlled high-frequency detail, and slower pad envelopes.
  `Motion` is a maximum depth and throttle supplies its smooth 25--100% scaler.
- Stale ignored V10/V12 DNA states were reset to their tracked intended presets.
  The generated runtimes, public pedal seam, 20 ms drivetrain integration,
  Pop event schedule, and module mixer architecture are otherwise unchanged.

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

- 162/162 unit tests pass; `git diff --check` passes. The ten changed generated
  outputs are byte-identical to an independent fresh generator build. V4 remains
  clean and `drive_model.js` has no diff.
- Final Soundscape on/off renders for EV/V10/V12 are distinct, non-silent and
  unclipped. Their harshness ratios range from `5.35e-5` to `1.02e-4`, below the
  documented `0.001` safety gate. Final V10 Pop measures `-2.93` dBFS peak,
  `121.5` Hz attack centroid, `0.875` low-band energy, `0.000216` snare-band
  energy, and a `170` ms tail.
- Final headless Max 8.6.5 loads covered the project and EV/V10/V12 separately.
  Current and rotated logs contain zero missing-object, Gen/function,
  invalid-category, or patchcord-range blocker matches. The direct-open
  search-path notices remain warning-only; abstractions loaded, and all three
  ignored per-profile module-mixer JSON states were written with expected
  defaults.
- The official `crashrecovery` preference was backed up, temporarily changed
  from Ask to Never for headless smoke, and restored byte-for-byte to Ask. Every
  task-owned process had zero windows before exact termination. Pre-existing
  zero-window Max PID `35660` (started at 13:38, before this task) was preserved;
  final AppleScript therefore reports Max running.
