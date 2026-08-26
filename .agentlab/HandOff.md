# VehicleSoundSynth V5 Repository HandOff

## Repository Identity

- Canonical remote: `git@github.com:Kidrage/VehicleSoundSynth.git`
- Target runtime: Max 8.6.5 on macOS
- Canonical branch: `main`.
- Start/Pop implementation fixed point: `b990974`, with later handoff-only
  descendants resolved from canonical `main`.

## Delivered Change

- Default Cinematic start is now a hybrid procedural voice: a generated
  crank/first-fire pressure core guarantees the transient is audible, while the
  existing seed-once `engine_start_beap~` remains the editable colour layer.
  Realistic start remains the tracked starter one-shot (or optional ignored
  local V10 derivative with fallback); continuous ICE remains procedural.
- V10/V12 Test Pop now has an explicit audition route that can sound with the
  engine off. Normal lift-off/shift backfire still requires Backfire Enable,
  ignition and engine-running state.
- The Pop voice is no longer a bare click/resonator. It uses distinct pressure
  body and exhaust-crack envelopes, profile-specific filters, two soft wall
  reflections, stereo differentiation, saturation and a higher usable level.

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

- The two current user Max saves were backed up byte-for-byte before final
  consolidation under the hidden single archive
  `/Users/saintpeter/Downloads/.VehicleSoundSynth-Backups/20260826-start-pop/`.
  V10 SHA-256 is `c1198af...`; V12 is `4386770...`.

## Validation

- 144/144 unit tests pass; deterministic generation, seed-once preservation and
  `git diff --check` pass.
- Real Max 8.6.5 renders are non-silent and unclipped. Cinematic starts measured
  V10 -4.83/-16.98 dBFS peak/RMS and V12 -4.41/-16.85; the controller-driven
  start path measured -4.58/-25.79. Test Pop measured V10 -3.91/-25.70 and V12
  -6.29/-29.03, with profile-distinct stereo tails and zero clipping.
- Final project plus EV/V10/V12 smoke found no missing-object, Gen outlet,
  invalid-category, patchcord or project blocker. Direct-open search-path
  warnings and the optional local Ferrari starter miss are fallback-safe.
- All task-opened windows were saved/closed and the temporary recovery setting
  was restored to `Ask`. Max rejected normal Quit/TERM only after all windows
  were closed and files saved; the user explicitly authorized terminating exact
  PIDs 9109, 9300 and 44294. Final AppleScript state is `Max = false`.
