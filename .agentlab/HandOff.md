# VehicleSoundSynth V5 Repository HandOff

## Repository Identity

- Canonical remote: `git@github.com:Kidrage/VehicleSoundSynth.git`
- Target runtime: Max 8.6.5 on macOS.
- Delivery branch: `codex/soundscape-pitch-restore`.
- Soundscape pitch/voicing/persistence implementation fixed point: `fd21aa0`;
  later handoff-only descendants do not alter the implementation.
- Focused base: canonical `main` at `e8f89cd`.

## Delivered Change

- Restored the large continuous RPM-following Soundscape pitch laws without
  changing drivetrain or engine-DNA pitch: EV `55 + 0.032*rpm`, V10
  `36.7 + 0.014*rpm`, V12 `32.7 + 0.012*rpm`, smoothed over 90 ms.
- Removed hidden interval offsets. The visible BEAP Osc Offset controls now own
  each chord; profile factories are EV `0/+7/+12`, V10 `-5/0/+7`, and V12
  `0/+7/+12`, with distinct Motion/Space/Brightness voicings.
- Added tracked per-profile factory slot 99 files covering all 90 controllable
  clients. Local Save writes only slot 1; startup/Reload/Reset always re-prime
  the tracked factory so stale local slot 99 data cannot replace Factory Reset.
- The three oscillator Frequency dials are intentionally live RPM indicators.
  Tune harmonic intervals with Osc Offset, global motion with Pitch Follow and
  Transpose, and timbre with Motion/Space/Brightness plus the visible BEAP
  filters/envelopes.
- No drivetrain, manual input, engine DNA, Pop/backfire, EQ, continuous
  powertrain DSP, top-level runtime, or media file changed.

## Repository Rules

- Edit generated Max JSON only through `tools/build_project.py`.
- Preserve the seed-once shared `cinematic_soundscape_beap~.maxpat`; regeneration
  must never overwrite user tuning in an existing copy.
- V10/V12 continuous audio remains procedural. Ferrari continuous derivatives
  remain analysis-only; the optional ignored V10 starter has a tracked fallback.
- Before delivery run deterministic generation, the full tests, audio/persistence
  probes, `git diff --check`, real Max project smoke, and confirm Max is exited.

## Local Save Archive

- Task originals, failed probes and task-owned Max recovery records are under
  `/Users/saintpeter/Downloads/.VehicleSoundSynth-Backups/V5/20260829-094048-soundscape-restore/`.

## Validation

- 173/173 tests pass; two independent fresh generator roots are byte-identical;
  `git diff --check` passes.
- Fresh CoreAudio EV/V10/V12 persistence probes wrote slot-1 files with 90
  clients. All 87 static/tunable clients matched factory exactly; only Osc A/B/C
  Frequency differed because live RPM owns those indicators.
- Final EV/V10/V12 WAVs are non-silent, unclipped, profile-distinct and below
  the documented `0.001` harshness gate. The installed driver rendered 16 kHz,
  so these are diagnostic rather than 48 kHz production-acceptance renders.
- A complete isolated checkout named `VehicleSoundSynth-V5` was regenerated and
  opened through `VehicleSoundSynth-V5.maxproj` in Max 8.6.5. The 12:12 log has
  zero project-category, missing-object/JS, Gen outlet/function,
  patchcord-range, or feedback blockers. Only the expected absent ignored V10
  Ferrari starter was reported; the clean checkout uses the tracked fallback.
- Directly launched Max did not respond to its normal Quit/Cmd-Q command. Each
  zero-window task PID was therefore verified by exact command/start time and
  terminated; its workspace recovery record was archived. Max currently reports
  false. The remaining 09:10 editor stack log predates this task and is not an
  active workspace recovery file.
