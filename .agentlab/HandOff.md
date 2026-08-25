# VehicleSoundSynth V5 Repository HandOff

## Repository Identity

- Canonical remote: `git@github.com:Kidrage/VehicleSoundSynth.git`
- Target runtime: Max 8.6.5 on macOS
- Canonical branch: `main`.
- Pedal/backfire implementation: `136ca58511a733bd486774e38cd92e5ded73e3f8`,
  based on the latest modular Sound DNA line.

## Delivered Change

- Keyboard W is immediate full throttle; S is a fixed 0.65 service brake with
  brake priority. Gamepad LT/RT remain independent analog pedals.
- V10/V12 DriveModel emits a bounded physical `overrun` event after a fast,
  loaded lift-off. Generated hosts turn it into a strength-scaled BEAP event.
- Both ICE runtimes expose Backfire Solo and Test Pop for isolated audition.
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

- Five old-main Max saves were backed up byte-for-byte to
  `/Users/saintpeter/Downloads/VehicleSoundSynth-Backups-20260825/VehicleSoundSynth-V5-MaxSaveBackup-20260825-pedal-backfire`
  and mirrored to the Codex Truenas export namespace before consolidation.

## Validation

- 136/136 unit tests pass; deterministic generator and seed-once preservation
  checks pass; `git diff --check` is clean.
- Real Max 8.6.5 Backfire Solo final renders are non-silent and unclipped:
  V10 peak/RMS -16.79/-43.66 dBFS, V12 -17.39/-45.14 dBFS.
- Final project plus EV/V10/V12 smoke found no missing-object, Gen outlet,
  invalid-category, or patchcord blocker. Direct-open search-path warnings and
  the optional local Ferrari starter miss are documented/fallback-safe.
- All task windows are closed, Max is fully exited, and its temporary recovery
  preference was restored to `Ask`.
