# VehicleSoundSynth V5 Repository HandOff

## Repository Identity

- Canonical remote: `git@github.com:Kidrage/VehicleSoundSynth.git`
- Target runtime: Max 8.6.5 on macOS.
- Feature branch: `codex/v5-soundscape-v4-rebuild`.
- Fixed point: `9a79128b3a39e9013dbdcc34386fef7071cbf050`.

## Delivered Change

- The audible shared Soundscape V3 core is replaced by three independent,
  seed-once V4 BEAP instruments: EV Evolution Score, V10 Ignition/cadence, and
  V12 Luxury Body/turbine-whine. Sound DNA audio and parameter namespaces do
  not enter these graphs; they share only controller-owned vehicle state.
- RPM is the only continuous root-pitch authority. Load/throttle blend tonal,
  structural and air layers; `speed_kph` changes upper-band texture and space.
  Bass below 120 Hz remains centred and the output rejects sub-28 Hz energy.
- Current procedural start voices use `{profile}_engine_start_v3_beap~`.
  Current ICE backfire voices use `{profile}_backfire_v2_beap~`. Older
  seed-once designers remain recoverable but are not on the audible path.
- The existing Main Soundscape controls and keyboard/gamepad/drive seams are
  unchanged. Direct acoustic probes now supply `engine_running 1`, matching
  the V4 host's controller-authoritative lifecycle gate.

## Repository Rules

- Edit generated Max JSON only through `tools/build_project.py`.
- Seed-once Sound DNA, Soundscape, start and backfire BEAP graphs are
  user-owned and must not be overwritten after creation.
- V10/V12 continuous sound remains procedural. Ferrari material is
  analysis-only except for the explicit ignored realistic V10 start option.
- Before delivery run deterministic regeneration, all tests, audio probes,
  `git diff --check`, real Max smoke/save/close, and scoped Max-process cleanup.

## Validation

- 184/184 unit tests pass, including keyboard/gamepad exclusivity, pedal
  release, lifecycle triggers, valid patchcords, current audible-instance
  routing, version-isolated persistence, and deterministic generation.
- Real Max 8.6.5 produced nine 48 kHz Soundscape Solo renders at fixed 1800 RPM:
  EV/V10/V12 low load, high load, and 180 km/h low load. Every render is
  non-silent, has zero clipped samples, subsonic ratio below 0.01, harshness
  below 0.001, and mono-fold loss below 3.1 dB.
- Fixed-RPM EV centroid moves 71.2 -> 119.9 Hz with load and 71.2 -> 80.9 Hz
  with speed. V10 moves 86.9 -> 131.9 / 127.2 Hz; V12 moves 103.7 -> 109.6 /
  108.0 Hz. This verifies timbre/space change without direct pitch jumps.
- All task-created probe patchers were generated/saved on disk and their exact
  Max PIDs were terminated after render finalization. Only pre-existing,
  windowless user Max PID `22230` remains; it was not touched.

## Safety Archive

- Pre-task dirty runtime saves and intermediate task-owned V4 seeds are stored
  under `/Users/saintpeter/Downloads/.VehicleSoundSynth-Backups/20260901-soundscape-v4-rebuild/`.
- No Ferrari source/continuous derivative, local preset, Max recovery file, or
  temporary WAV is part of the repository change.
