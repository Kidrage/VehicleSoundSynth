# VehicleSoundSynth V5 Repository HandOff

## Repository Identity

- Canonical remote: `git@github.com:Kidrage/VehicleSoundSynth.git`
- Target runtime: Max 8.6.5 on macOS
- Canonical branch: `main`.
- Authoritative Pop/Sound-DNA control implementation fixed point: `d80ce18`,
  currently on `codex/pop-dna-authority` pending final promotion to canonical
  `main` after Max smoke and review closure.

## Delivered Change

- Pop Designer now opens the active audible V10/V12 backfire instance and
  exposes a persistent authoritative control surface for Global Pitch, Core
  Presence, Body/Crack Tune, Decay, Low Pressure, Body Level and Crack Level.
  Profile-local named control buses keep the editable patcher separate from the
  generated host, and parent defaults plus floating-point message ramps prevent
  silent loads or 0--1 values being truncated to integers.
- `Global Pitch` reaches both randomized per-hit pitch and the generated
  pressure-core filters. Core Presence is deliberately bounded to 0.25--1.5 so
  it cannot become a hidden mute. The visible BEAP Pressure Mixer remains an
  optional colour source; the top controls are the audibility/tone authority.
- EV Aggression and V10 Brightness were repaired from declared-but-unused Sound
  DNA values into direct Gen colour paths. All three runtimes now expose DNA
  Solo so the live procedural powertrain can be judged without pad, transient,
  road or rumble masking.

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
- Seed-once V10/V12 voices expose Pressure Body, Exhaust Crack, Tail
  Color/Output, and the authoritative top control panel. Intensity morphs layer
  colour and tail density, not only gain. Max-safe pressure/core controls remain
  audible even when native BEAP MMF/AD/VCA response is subtle on short gates.
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

- 155/155 unit tests pass; deterministic generation, seed-once preservation and
  `git diff --check` pass.
- Fixed-state real Max low/high DNA renders cover the complete visible control
  set as aggregate A/Bs for EV/V10/V12. Low-to-high RMS changes were 8.77,
  14.26 and 14.74 dB respectively; all six renders were non-silent and had zero
  clipped samples. Per-control low/high probe scenarios are generated from the
  same authority as each editable DNA panel.
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
