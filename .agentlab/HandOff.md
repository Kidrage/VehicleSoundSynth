# VehicleSoundSynth V6 Repository HandOff

## Repository Identity

- Canonical remote: `git@github.com:Kidrage/VehicleSoundSynth.git`
- Target runtime: Max 8.6.5 on macOS.
- Canonical branch: `main`.
- V6 audio baseline source: `3708c086a5d414665ee533db7ed8067bdeafc68b`.
- Release tag: `v6.0.0`.

## Delivered Change

### Isolated control / DNA V3 candidate (2026-09-14)

The active task is now `codex/v6-control-dna-v3`, based on accepted `cff9d08`,
in `Downloads/VehicleSoundSynth-V6-Candidate/VehicleSoundSynth-V6`. The production
Downloads V6 folder and private state are unchanged. User approved the local
20260911 package: IONIQ control repair, Main tone routing, Ferrari/V10/V12 DNA V3
and independent Ferrari Noise V2, not a Soundscape/Start/Pop/FX rewrite.

Read `V6_CANDIDATE_GUIDE.md` and `.agentlab/V6_CONTROL_DNA_V3.md` first for this
candidate. Previous release/QA entries below remain historical. Whole-runtime
and listening acceptance are separate from source tests; do not promote the
candidate before acceptance. On 2026-09-14 the user explicitly authorized
uploading only `codex/v6-control-dna-v3` ahead of acceptance, superseding its
earlier local-only gate. No main merge/push or production replacement.

Implementation/review fixes are saved in local commit `1b670bb`. On 2026-09-14
07:07 UTC the user-authorized termination of task Max PID 24644 succeeded with
SIGTERM; no SIGKILL, remaining Max process or new test session. The disk-state
backup and unsaved test-UI limitation are recorded in the candidate report.
Native runtime/listening acceptance is still incomplete.


### Accepted snapshot / release handoff (2026-09-10)

The user accepted the current sound and authorized pushing the feature branch
`codex/v6-layering-dna-pad-pop`, not main. No audio, factory, drive or routing
changes are made in this release task. `V6_RELEASE_HANDOFF.md` is the current
release/rollback/QA authority; `V6_USER_GUIDE.md` is the Chinese operator guide.
The following 2026-09-09 record remains a historical test record: user acceptance
does not turn unfinished automated native Max checks into passes.

### Running beds / Noise / shared Pop (2026-09-09 historical implementation)

Implementation is on `codex/v6-layering-dna-pad-pop`, based on `b609e8b`.
At the time of that record, no new commit or push existed. Source/structure and protection checks pass, but
native Max acceptance remains incomplete. The stuck task Max was subsequently
force-exited with explicit user authorization and a recovery backup; the user's
original Max was preserved and no new test instance started. See
`V6_LAYERING_2026-09-09.md` for the exact pending compile/save-dialog issue,
protected user files, test evidence and resumption steps. Do not treat the
historical completed-task records below as acceptance of this implementation.

### Ferrari-only body return and sample Pop (2026-09-08)

- Branch `codex/v6-ferrari-body-pop-sampler`, based on `93accba`; local-only
  delivery, no main merge or GitHub push. User-owned Main changes are excluded.
- Soundscape V6 adds one -9 dB factory dry-body return to the preserved V5
  graph, with separate state. DNA/start, other four sounds, all common controls,
  drivetrain, Mixer/EQ and dynamics are unchanged. 227 protected resources plus
  Main match the pre-task hash inventory; original local presets are untouched.
- Pop V3 uses one tracked CC0 240 ms one-shot, two idle-muted players and three
  controls. Existing burst timing and physical/preview gates remain. Explicit
  Save/Reload/Factory Reset and the actual live designer Open path work in Max.
- 211 tests pass; two fresh 163-file generations match. Actual 48 kHz Max
  recordings verify audible body reinforcement and unclipped Pop/output.
  The sustained factory SC harshness ratio is 0.000870, mono loss 0.011 dB.
  Coarse local Max CPU readings favor the new player; see the audit for limits.
- Test files were saved and task Max exited normally; user PID 36547 remains.
  Backup hashes, reproduction details and tuning: `FERRARI_BODY_POP_2026-09-08.md`.

### Soundscape control repair without retuning (2026-09-08)

- Active repair branch: `codex/v6-soundscape-control-repair`, based on
  `adca388`. The accepted Ferrari realism branch remains recoverable.
- Main's Soundscape and DNA Solo commands previously passed through the
  Internal/External drive switch and held-context gate. One shared-host router
  now delivers those commands directly to each existing engine; no synthesis,
  factory/local preset or pedal/lifecycle behavior is retuned.
- Actual Main/Ferrari Max recordings reproduce the prior held-Load Enable
  failure and verify the repair, independent Solo behavior and Save/Reload.
  Three valid 44.1 kHz recordings have zero clipped samples. 207 tests pass;
  two fresh 158-file generations match. 182 non-host runtime resources and
  all original local presets match the frozen baseline.
- Max loaded all five adapters and both live Ferrari designers, with no new
  missing-object, Gen, patchcord/outlet or project-category error. Task windows
  were saved/closed and task Max exited; pre-existing user PID 38515 is preserved.
- Main's local-only console path was repaired from generator authority while
  preserving the user's other saved properties. That user-owned Main diff
  is not part of the commit; its committed counterpart was already portable.
- V10/V12 acceleration texture is diagnosis-only: idle-body fade, reduced
  relative low-mid support and increasing fixed-ratio upper tones are candidates
  for future level-matched investigation. See
  `SOUNDSCAPE_CONTROL_AUDIT_2026-09-08.md` for the detailed evidence and boundaries.

### Fifth Ferrari V10 acoustic interpretation (2026-09-04)

- Accepted V6 is frozen and pushed as annotated tag
  `v6-accepted-2026-09-04-672ad62` at
  `672ad6204841440462225008e6ea8be643f6483f`. Feature work is isolated on
  `codex/v6-ferrari-v10`; it does not replace or retune the four accepted
  profiles.
- `VehicleSoundSynth-Ferrari.maxpat` is a fifth complete runtime on the shared
  Main/runtime-host/Mixer/EQ/input/persistence topology, with its own
  controller, drive config, public `vss.ferrari.input`, Sound DNA, Soundscape
  V4, procedural Start and procedural Backfire.
- The sound is an analysis-envelope-derived V10 acoustic interpretation, not a
  physical SF90 engine model. Continuous synthesis uses `rpm/12` cadence and
  independent 120--250, 250--600, 600--1200, 1200--2000 and 2000--6000 Hz
  controls. Load opens those bands by different bounded amounts; lift-off
  drops high edge faster while retaining body/cavity mass.
- Ferrari Soundscape remains a separate stem and parameter namespace. Its
  exterior body, cavity projection, mechanical halo and air/reflection layers
  follow RPM for root pitch and load for colour/density. Final Max renders
  show nine high-load structure peaks, `0.000277` harshness, zero clipping and
  `0.082 dB` mono-fold loss. Low/high-load files have distinct hashes while the
  dominant root remains stable.
- `assets/ferrari_sf90_v10_interpretation_targets.json` contains numeric targets
  only. No supplied reference audio/path, continuous derivative, local preset,
  recovery file or test render is tracked or synchronized.
- All 201 tests pass. Two clean generator roots are byte-identical with combined
  digest `1ab8cf78938d72a1c4e915bfccd82a74a98c55d3a21427d525a528be69965297`.
  Max 8.6.5 rendered controller start, stable idle, Soundscape low/high load and
  backfire with no project/object/Gen/patchcord blocker. All task-owned Max
  processes exited; pre-existing user PID `38515` remained untouched.

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
