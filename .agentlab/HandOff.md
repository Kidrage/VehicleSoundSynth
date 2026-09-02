# VehicleSoundSynth V5 Repository HandOff

## Repository Identity

- Canonical remote: `git@github.com:Kidrage/VehicleSoundSynth.git`
- Target runtime: Max 8.6.5 on macOS.
- Feature branch: `codex/v5-ioniq6n-profile`.
- Fixed point: `d3dbad6513e2c9b37076ca8959c8cf119bfee3bf`.
- Feature implementation: `ba830a854806c72a1a0be5b21fb12642c3c31d1b`.

## Delivered Change

- Adds `VehicleSoundSynth-IONIQ6N.maxpat` as a fourth independent runtime and
  launcher target. It does not replace or retune V10.
- Adds an electric IONIQ6N Sound DNA with independent motor-order, low-mid
  body/cavity, mechanical texture, high-edge, load/release and ready-bed
  controls. The user-supplied road-test MP3 is analysis-only and is not loaded,
  copied or committed.
- Adds three seed-once, crossfaded N Sound instruments: Ignition, Evolution and
  Lightspeed. RPM is the sole root-pitch authority, load/throttle controls the
  layer/filter mix, and speed changes only upper air/space. Soundscape audio and
  parameters remain completely outside the Sound DNA graph.
- Adds separate seed-once ready activation and N-event designers. Ignition
  arms the restrained release bubble, Evolution leaves both release effects
  disarmed, and Lightspeed arms the afterburner pop. Shift impacts follow the
  optional eight-ratio N e-Shift model, which defaults enabled and can be
  disabled for continuous EV pitch.
- Preserves the original EV/V10/V12 generated acoustic artifacts byte-for-byte
  relative to the fixed point. Keyboard/gamepad and public throttle/brake seams
  are reused unchanged.

## Persistence and Editing

- Soundscape factory: `presets/ioniq6n_soundscape_modes_factory.json`.
- N-event factory: `presets/ioniq6n_n_event_factory.json`.
- User state is written only under ignored `presets/local/`.
- Seed-once IONIQ6N Sound DNA, Soundscape, activation and event BEAP patchers
  are user-owned after their first generation.

## Validation

- All 192 tests pass, including structural, deterministic-generation,
  drivetrain, lifecycle, persistence and acoustic-probe regressions in
  `tests/test_project.py` and `tools/build_runtime_probe.py`.
- Max NonRealTime diagnostics cover activation, ready-state, all three modes at
  low/high load, low/high speed, N e-Shift on/off, and the three N-event paths.
  The installed driver may render at 44.1 kHz even when 48 kHz is requested;
  those files are diagnostic and are not tracked.
- Two consecutive project generations produced identical SHA-256 values for all
  212 filtered repository files. `git diff --check` is clean; the current Max
  log contains no missing-object, invalid-category, Gen or patchcord blocker.
  The known application database read-only warning remains unrelated.
- Three N Sound patchers have distinct SHA-256 values. Max diagnostics were
  non-clipping, remained below the `0.001` 2--6 kHz harshness gate, and kept
  mono-fold loss below 3 dB. All task-owned Max instances exited normally;
  pre-existing user PID `65075` was preserved.

## Safety

- The original dirty V10/V12 working tree is untouched and archived under
  `/Users/saintpeter/Downloads/.VehicleSoundSynth-Backups/20260902-ioniq6n-profile/`.
- Never commit or sync the supplied MP3, Ferrari material, local presets,
  recovery files or temporary renders.
