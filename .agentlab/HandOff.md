# VehicleSoundSynth V5 Repository HandOff

## Repository Identity

- Canonical remote: `git@github.com:Kidrage/VehicleSoundSynth.git`
- Target runtime: Max 8.6.5 on macOS
- Canonical branch: `main`.
- Layered-backfire implementation: `9fffe195d9e3aa68678856ad880693ac6a5df63a`,
  with later handoff-only descendants resolved from canonical `main`.

## Delivered Change

- Keyboard W is immediate full throttle; S is a fixed 0.65 service brake with
  brake priority. Gamepad LT/RT remain independent analog pedals.
- V10/V12 DriveModel emits a bounded physical `overrun` event after a fast,
  loaded lift-off. Generated hosts turn it into a strength-scaled BEAP event;
  drivetrain thresholds and the public message seam are unchanged.
- Both ICE runtimes expose Backfire Solo and Test Pop for isolated audition.
- Seed-once V10/V12 voices expose Pressure Body, Exhaust Crack, and Tail
  Color/Output sections. Intensity morphs layer colour and tail density, not
  only gain. The Max-safe envelope is sourced from the visible BEAP Mixer/MMF
  outputs, so those tone controls remain authoritative.
- Public actuator inputs remain normalized `throttle 0..1` and `brake 0..1`;
  the fixed 20 ms speed/RPM/shift integration is unchanged.

## Repository Rules

- Edit generated Max JSON only through `tools/build_project.py`.
- Seed-once Sound DNA, Soundscape, start and backfire BEAP graphs are user-owned
  and must not be overwritten by regeneration.
- V10/V12 continuous sound remains procedural; local Ferrari media is not a
  distributable continuous-runtime source.
- Before delivery run deterministic regeneration, all tests, audio probes,
  `git diff --check`, real Max smoke/save/close, and confirm Max is fully exited.

## Local Save Archive

- Old-main Max saves, including the three pre-layered-Pop user saves, were
  backed up byte-for-byte to the single existing directory
  `/Users/saintpeter/Downloads/VehicleSoundSynth-Backups-20260825/VehicleSoundSynth-V5-MaxSaveBackup-20260825-pedal-backfire`
  before consolidation; no new top-level backup folder was created.

## Validation

- 139/139 unit tests pass; deterministic generator and seed-once preservation
  checks pass; `git diff --check` is clean.
- Real Max 8.6.5 Backfire Solo final renders are non-silent and unclipped:
  V10 peak/RMS -9.90/-41.52 dBFS, V12 -9.44/-43.41 dBFS. The profiles retain
  distinct final centroids of about 826 Hz and 703 Hz respectively.
- Final project plus EV/V10/V12 smoke found no missing-object, Gen outlet,
  invalid-category, or patchcord blocker. Direct-open search-path warnings and
  the optional local Ferrari starter miss are documented/fallback-safe.
- All task-opened windows are closed and every task Max PID is terminated. The
  user's pre-existing Max PID 44294 was deliberately preserved; the temporary
  recovery preference was restored to `Ask`.
