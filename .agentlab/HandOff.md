# VehicleSoundSynth V5 Repository HandOff

## Repository Identity

- Canonical remote: `git@github.com:Kidrage/VehicleSoundSynth.git`
- Target runtime: Max 8.6.5 on macOS
- Canonical branch: `main`.
- Low/heavy randomized Pop implementation fixed point: `fe50c57`, with later handoff-only
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
- Fast lift-off and Test Pop now schedule 1--5 decaying hits with random
  140--200 ms spacing. The pitch contour falls overall with small per-hit jitter;
  shift/explicit events remain one hit and rapid retrigger cancels stale hits.

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
  `/Users/saintpeter/Downloads/.VehicleSoundSynth-Backups/20260826-pop-low-burst/`.
  V10 SHA-256 is `faf699ce...`; V12 host is `9fba2059...`.

## Validation

- 149/149 unit tests pass; deterministic generation, seed-once preservation and
  `git diff --check` pass.
- Real Max 8.6.5 renders are non-silent and unclipped. Cinematic starts measured
  V10 -4.83/-16.98 dBFS peak/RMS and V12 -4.41/-16.85; the controller-driven
  start path measured -4.58/-25.79. Test Pop measured V10 -3.91/-25.70 and V12
  -6.29/-29.03, with profile-distinct stereo tails and zero clipping.
- Final Pop-only Max renders are unclipped. V10 measured -4.44/-25.05 dBFS
  peak/RMS, 430 Hz centroid and 0.520 rumble ratio; V12 measured
  -5.03/-25.88 dBFS, 241 Hz centroid and 0.577 rumble ratio. Both expose a
  0.16-second burst-envelope period; physical overrun renders are also non-silent
  and unclipped.
- Final project plus EV/V10/V12 smoke found no missing-object, Gen outlet,
  invalid-category, patchcord or project blocker. Direct-open search-path
  warnings and the optional local Ferrari starter miss are fallback-safe.
- All final-smoke EV/V10/V12 runtime windows and the Project window were saved
  and closed in sequence. The temporary recovery setting was restored to `Ask`,
  the task-owned Max instance quit normally, and final AppleScript state is
  `Max = false`.
