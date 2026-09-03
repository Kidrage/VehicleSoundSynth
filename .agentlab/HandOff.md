# VehicleSoundSynth V6 Repository HandOff

## Repository Identity

- Canonical remote: `git@github.com:Kidrage/VehicleSoundSynth.git`
- Target runtime: Max 8.6.5 on macOS.
- Canonical branch: `main`.
- V6 audio baseline source: `3708c086a5d414665ee533db7ed8067bdeafc68b`.
- Release tag: `v6.0.0`.

## Delivered Change

### V6 system cleanup (2026-09-03)

- Branch `codex/v6-system-cleanup` keeps the accepted `v6.0.0` timbre intact.
  No Gen/BEAP synthesis algorithm, Soundscape factory preset, audio asset, EQ
  default or module gain default was retuned.
- `main.maxpat` is now the sole common console. Its tabbed Drive, Mix/EQ and
  Sound Design pages drive one selected runtime through profile-scoped command
  and feedback buses. The four profile patchers are thin mode-only adapters.
- `profile_runtime_host_<profile>.maxpat` is materialized from one shared
  drivetrain, engine, input, seven-stem mixer, EQ, output and diagnostic
  topology. Literal profile binding avoids Max interpreting a dynamic class
  name as an object; public `vss.<profile>.input` messages remain supported.
- Every Sound DNA control now has a bilingual name, unit, listening context and
  help text. Existing panels remain seed-once user property and are never
  auto-migrated on rebuild. IONIQ6N now uses Main's seven-stem Mixer as the sole
  DNA output-gain authority; the duplicate DNA fader was removed while its six
  embedded BEAP modules retained hash
  `292e7072a4f924e10ba5b6350ac9e6757269c44806e69fc183808e05c860c939`.
- Main reads the active profile's saved four-band EQ state back into its visible
  controls on open, save, reload and reset, so a value from the previous profile
  cannot masquerade as the active setting.
- Drivetrain calibration adds high-speed full-throttle reserve, a temporary
  abrupt-lift brake/RPM response and faster service braking. Gradual pedal
  release still coasts; EV and IONIQ6N with N e-Shift off remain speed-coupled.
- All 197 tests pass. Two post-fix generator runs produced the same 114-file
  patch/project/Gen/preset digest `8d371799786bd85cece6679e41893dfd30b8f6ec93e5f8ed75cd561434aa02d7`.
  Max 8.6.5 opened Main with EV, V10, V12 and IONIQ6N from a correctly named,
  exact runtime-tree `git archive` copy after the last EQ-feedback/gain-authority
  cleanup. Every top-level patcher recorded `savedserialnumber=0`; the new log
  has no missing-object, Gen, patchcord, JavaScript-function or project-category
  blocker. Optional local Ferrari one-shot and read-only object-database messages
  remain expected environment diagnostics. Five earlier empty task processes
  were force-terminated after explicit user authorization. The final smoke PID
  exited normally after all runtime, Main, Project and Console windows closed;
  pre-existing user PID `65075` and its four original probe windows are preserved.

- Renames the project/runtime identity to V6 without changing synthesis,
  factory presets, audio routing, controls, or drivetrain behavior.
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
- V6-baseline Max serialization saves are archived under
  `/Users/saintpeter/Downloads/.VehicleSoundSynth-Backups/20260903-v6-baseline/`
  and excluded from Git after their SHA-256 values were verified.
- Never commit or sync the supplied MP3, Ferrari material, local presets,
  recovery files or temporary renders.
