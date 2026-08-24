# Project Handoff

> Deterministically generated repository/project memory for cross-agent handoff.
> Update after every material project change and before final reporting.

## Repository Identity

- Repository ID: `VehicleSoundSynth-V5-8de441799e7b`
- Working root: `.`
- Repository name: `VehicleSoundSynth-V5`
- Git repository: `true`
- Generated at: `2026-08-24T06:14:05Z`

## Current State

- Branch: `main`
- HEAD: resolve `main` dynamically with `git rev-parse HEAD`; the consolidation
  record starts at `942cd3f`, immediately after V5 feature head `cf4c970`.
- Indexed paths: 145
- Inventory truncated: `false`
- Inaccessible paths: 0
- Scan mode: complete path/metadata inventory; no bulk content read; no symlink traversal.

## Project Progress Dashboard

- Current progress: derive from branch, HEAD, current changes, and manual Agent Notes below.
- Work already changed: see Change History and Current Changes.
- Active work: any dirty Git status entries listed under Current Changes.
- Remaining work / ETA: maintain in Agent Notes when it cannot be inferred deterministically.
- Pending decisions: maintain in Agent Notes and refresh before final reporting.
- Pending files / plans / acceptance artifacts: maintain in Agent Notes and task run ledgers.
- Fast reporting source: this canonical root file; use the shared mirror only when explicitly written.

## Active Work and Pending Items

- In progress: inspect Current Changes and Agent Notes.
- Pending decisions: record durable choices in Agent Notes before handoff.
- Pending files to modify: record intended paths in Agent Notes before dispatch.
- Pending plans to confirm: link task/run plans in Agent Notes.
- Pending acceptance artifacts: link deliverables and validation evidence in Agent Notes.
- Next safe entry point: run `./agentlab.sh repository-handoff --repo <path>` before deep work.

## Directory Routes

| Route | Files |
|---|---:|
| `patchers` | 55 |
| `media` | 35 |
| `.` | 16 |
| `tools` | 13 |
| `assets` | 11 |
| `assets/raw` | 7 |
| `.codex` | 4 |
| `code` | 3 |
| `gen` | 3 |
| `presets` | 3 |
| `tests` | 2 |
| `presets/local` | 1 |

## Data and File Structure

### Categories

- audio: 41 files, 103833150 bytes
- code: 18 files, 688992 bytes
- literature: 15 files, 596902 bytes
- other: 60 files, 12992034 bytes
- structured_data: 6 files, 33194 bytes

### Common Extensions

- `.maxpat`: 59
- `.wav`: 41
- `.py`: 15
- `.md`: 7
- `.json`: 6
- `.docx`: 5
- `.js`: 3
- `.gendsp`: 3
- `.txt`: 2
- `[no extension]`: 2
- `.maxproj`: 1
- `.pdf`: 1

### Schema / Model / Interface Candidates

- `code/drive_model.js`

## Key Entrypoints and Guides

- `AGENTS.md`
- `README.md`
- `assets/raw/README.md`

## Change History

- `0fccd1f 2026-08-24 feat: tune speed-dependent natural coasting`
- `4c206bd 2026-08-24 fix: isolate gamepad state and soundscape solo`
- `9f066e4 2026-08-24 feat: add fixed gamepad pedals and cinematic soundscape`
- `942cd3f 2026-08-21 docs: record V5 mainline consolidation`
- `cf4c970 2026-08-21 feat: add switchable gamepad manual throttle control`
- `1738ef6 2026-08-20 docs: refresh V5 repository handoff`
- `4a3d892 2026-08-20 fix: gate backfire by engine state`
- `4580cb7 2026-08-20 fix: close V5 review gaps`
- `6ecfd6a 2026-08-20 feat: start VehicleSoundSynth V5 realism pass`
- `6aa49d0 2026-08-20 Refresh repository handoff`
- `aaf3508 2026-08-20 Rebuild procedural vehicle lifecycle runtimes`
- `dc8d175 2026-08-19 fix: restore profile throttle and stabilize runtime audio`
- `2970e9d 2026-08-18 docs: refresh V4 silence-fix handoff`
- `17c8e14 2026-08-18 fix: enable runtime audio and restore W S driving`
- `5024087 2026-08-18 docs: refresh V4 project handoff`
- `aff305f 2026-08-18 feat: split V4 runtimes and restore sample-led V10`
- `68af5db 2026-08-18 fix: soften V10 V12 combustion with local Ferrari body`
- `3a678eb 2026-08-17 docs: refresh V4 repair handoff`
- `8cf0f1e 2026-08-17 fix: remove full-rate combustion reset harshness`
- `745207c 2026-08-14 fix: rebuild V4 engine realism and stereo field`
- `f138ccb 2026-08-12 docs: seal V4 integrity audit`
- `32bc86d 2026-08-12 docs: complete V4 Ferrari validation guide`
- `32873f8 2026-08-12 docs: finalize V4 integrity record`
- `613d929 2026-08-12 docs: correct V4 manual identity`

## Current Changes

- User-owned local Max saves remain modified in `VehicleSoundSynth-EV.maxpat`
  and `VehicleSoundSynth-V10.maxpat`; they predate the coast task, are archived
  under the Codex export namespace, and are intentionally excluded from commits.
- Canonical delivery is `main...origin/main`; always verify with
  `git status -sb` and `git rev-parse HEAD` instead of a stored ahead count.

## Related Repositories

### Remotes

- `origin github.com:Kidrage/VehicleSoundSynth.git (fetch)`
- `origin github.com:Kidrage/VehicleSoundSynth.git (push)`

### Submodules

- None detected.

## Media and Literature Routes

### literature

- `.codex/MAINLINE.md`
- `.codex/REPO_GUIDE.md`
- `.codex/repo_files.txt`
- `.codex/source_index.txt`
- `AGENTS.md`
- `ASSET_LICENSES.md`
- `PROJECT_HANDOFF.md`
- `README.md`
- `VehicleSoundSynthV2_完整使用手册.docx`
- `VehicleSoundSynthV3_完整使用手册.docx`
- `VehicleSoundSynthV3_车机RTPC_DSP链路技术说明.docx`
- `VehicleSoundSynthV3_车机RTPC_DSP链路技术说明.pdf`
- `VehicleSoundSynthV4_完整使用手册.docx`
- `VehicleSoundSynth_完整使用手册.docx`
- `assets/raw/README.md`

### image

- None detected.

### audio

- `assets/raw/biholao_370278_ferrari_acceleration.wav`
- `assets/raw/grasopt_479351_car_starter.wav`
- `assets/raw/jamespeacock4616_555787_mini_car_ir.wav`
- `assets/raw/microman502_818294_mechanical_gear_shift.wav`
- `assets/raw/richwise_478756_sports_car_revs_pops.wav`
- `assets/raw/thelittlecrow_669623_engine_block_contact.wav`
- `media/cabin_ir_l.wav`
- `media/cabin_ir_r.wav`
- `media/engine_texture_065_a.wav`
- `media/engine_texture_065_b.wav`
- `media/engine_texture_110_a.wav`
- `media/engine_texture_110_b.wav`
- `media/engine_texture_180_a.wav`
- `media/engine_texture_180_b.wav`
- `media/engine_texture_260_a.wav`
- `media/engine_texture_260_b.wav`
- `media/engine_texture_380_a.wav`
- `media/engine_texture_380_b.wav`
- `media/engine_texture_520_a.wav`
- `media/engine_texture_520_b.wav`

### video

- None detected.

### structured_data

- `assets/asset_manifest.json`
- `assets/engine_texture_bank.json`
- `assets/ferrari_sf90_acoustic_target.json`
- `assets/ferrari_v10_lifecycle_targets.json`
- `presets/sound_dna.json`
- `presets/vehicle_bus_eq_default.json`

## Validation and Risks

- This inventory records paths and metadata, not semantic correctness.
- Binary/media payloads and secrets were not read.
- Validate current branch, tests, and interfaces before modifying files.

## Agent Notes

<!-- AGENT_NOTES_START -->
- 2026-08-24 balanced natural coast: the unchanged public throttle/brake seam
  now keeps the original powered aero drag from 0.08 throttle upward and uses
  a smooth released-pedal curve that is stronger near rest and weaker at high
  speed. Public DriveModel traces measure 20->0 km/h in 10.40 s, 100->80 in
  23.84 s, and 200->180 in 29.04 s; the pre-change full-throttle 8 s speed is
  preserved exactly for EV/V10/V12, and active-brake stop-time gates still pass.
  The clean commit passed 126/126 tests in an isolated worktree and
  `git diff --check`. Clean EV/V10/V12 Max 8.6.5 loads after their per-profile
  timestamps had no missing-object, Gen/function, bad-outlet, or patchcord-range
  blocker; direct CLI loading retains the documented search-path warnings. Max
  ignored Quit only after windows had closed, so the exact task-owned PIDs were
  ended and final `application "Max" is running` is false. The pre-existing
  user-owned EV/V10 top-level saves were not rewritten (their before/after SHA
  values match), were excluded from clean validation and remain uncommitted;
  direct loading of the local EV save separately exposed its existing Max
  patchcord-deletion errors, so it must not be treated as canonical delivery.
- 2026-08-24 fixed gamepad pedals and shared cinematic Soundscape: all three
  runtimes retain the generated `manual_input.maxpat` deep module and now use
  Max 8.6.5's built-in `gamepad` semantic events with fixed LT/L2 throttle and
  RT/R2 brake; there is no Learn, axis index, inversion, or throttle curve.
  Triggers are absolute 0..1 pedals with 0.02 dead zone and 30 ms smoothing.
  Source/manual changes synchronously clear both pedals; active-Gamepad device
  replacement/disconnect also clears them, while inactive Gamepad events cannot
  interrupt a held Keyboard pedal. Device identity follows Max's documented
  instance ID rather than its reusable HID index. Keyboard W/S remains exclusive
  and Auto/External remain isolated. The 20 ms
  RPM/shift integration is unchanged; only service-brake force is now a
  progressive `31*brake^1.35` law, with full/keyboard/half-pedal regression
  stop times of 3-4/5-7/6-9 seconds from 100 km/h. EV/V10/V12 now share one
  declared, seed-once `cinematic_soundscape_beap~` Prophet-style analog core
  (triangle/pulse/noise, ladder, ADSR, LFO, chorus, reverb and bounded
  post-filtering), with generated per-profile RPM/load/throttle hosts and common
  Enable/dB/Motion/Space/Solo controls. Legacy pad files are preserved but
  undeclared. Soundscape Solo gates powertrain, transient, road and rumble on
  both channels and also removes the rumble excitation bypass, so it isolates
  the shared Pad for tuning. Six finalized Max NonRealTime on/off renders were each 122880
  stereo frames at the installed driver's 44.1 kHz, had distinct hashes, zero
  clipped samples and large audible RMS deltas: EV -40.53/-54.80 dBFS, V10
  -40.41/-43.99, V12 -40.40/-41.63; on-state centroids were 106.5/144.1/186.9
  Hz and harsh ratios remained below 3e-7. All 124 tests pass after the final
  deterministic regeneration and `git diff --check` is clean. A real Max 8.6.5
  pass loaded EV, V10 and V12 with no missing object, invalid category, bad
  outlet/function, or patchcord-range blocker; direct CLI opens retained the
  already documented project-association search-path warning. Each top-level
  runtime received its own `write -> delay 20 -> wclose` transition. After
  Max ignored its visible Quit command and TERM despite generated documents
  already being saved and no UI edits being made, so each task-owned sole PID
  was terminated exactly; final
  `application "Max" is running` is false. No local media, EQ state, user
  preset, or temporary probe file is part of the repository diff.
- 2026-08-21 V5 mainline consolidation: remote V2, V3, and V4 histories were verified as strict ancestors of `cf4c970`; no divergent core branch required a content merge. The local working copy fast-forwarded to the latest switchable-Gamepad V5 commit, then local `main` fast-forwarded from frozen V4 `6aa49d0` to the same V5 head. Three pre-update top-level Max runtime saves contained no Gamepad input layer and were excluded from the mainline as obsolete runtime/UI state; no local audio, EQ state, preset, or media was committed. `tools/build_project.py --output-root .` was deterministic against the committed outputs, all 119 unit tests passed, and `git diff --check` was clean. Fresh Max 8.6.5 instances loaded the project with EV, V10, and V12; project-path, missing-object, Gen, and patchcord blocker patterns were absent. Max continued to emit its known application-level read-only object-database warnings and informational HID-disposal messages. All smoke-test instances and the pre-existing windowless Max process were closed through normal Max quit handling; final `application "Max" is running` was false.
- 2026-08-21 switchable Manual Input (historical, superseded by the fixed-semantic
  2026-08-24 design above): the first V5 pass used configurable `hi` elements,
  range/invert/curve controls and Learn. That interface is intentionally no
  longer present; do not restore its axis-learning contract.
- 2026-08-20 V5 fork: V4 is frozen unchanged at tag `v4.0.0` (`6aa49d0`). V5 keeps the three independent fixed-profile runtimes and DSP-free launcher. Runtime shift/up/down, near-zero deceleration, pop, crackle, intake-backfire, and mechanical-click sample players are removed; only realistic starter one-shots and the cabin IR remain declared runtime recordings. V10/V12 now use seed-once user-owned BEAP backfire voices driven by actual overrun/shift state, with V10 more active and V12 rounder; the event gate additionally requires ignition and engine-running state, and fresh Max off-state renders were exactly silent. Each ICE runtime adds a separately editable/suspendable cinematic BEAP pad with top-level level/mute controls. The continuous engines add bounded crankcase/manifold (ICE) or torque-ripple/gear-mesh (EV) motion without saw/square waveforms; both EV channels contain the new continuous layers. The visible four-band bus EQ uses one shared ignored `presets/local/vehicle_bus_eq.json`, explicit Save/Reload/Reset controls, tracked safe defaults, a tracked empty local-state directory, and a portable runtime path helper. All 107 Python tests pass and `git diff --check` is clean. Fresh Max 8.6.5 NonRealTime renders covered EV Pad on/off, V10/V12 idle/high RPM, both BEAP backfires, both backfire ignition-off gates, and both V10/V12 Pad on/off; every enabled WAV was non-silent and unclipped, Pad/event pairs had different hashes, and the installed driver again rendered at 44.1 kHz. A V10 close wrote the shared EQ file synchronously; a subsequent V12 reopen/close preserved the exact file SHA-256, proving cross-profile persistence. The three final runtimes were then opened one at a time, sent their built-in `write -> delay 20 -> wclose` path, and Max was confirmed fully exited. No project object/Gen/patchcord/attribute/missing-file errors remained; Max's separate read-only object-database `sqlite_exec` warning persists at application level.
- 2026-08-20 procedural lifecycle rebuild: EV/V10/V12 are three independent runtimes with W/S manual drive, continuous RPM laws, start-relative ignition clocks, smoothed EV single-speed/V10-V12 seven-speed drivetrains, and adjustable stereo compression before limiting. V10/V12 continuous audio is synthesized; Ferrari.wav supplies only a tracked 14-node analysis target plus the optional ignored V10 startup one-shot. Five role-specific V10 Max renders and one 24 s throttle-only/automatic-DCT Max render pass the lifecycle gate for cadence direction/range, RMS/crest, low-mid/rumble, harsh/air energy, centroid/roll-off, clipping, ordered gears 2-7, paired shifts, RPM continuity, and deceleration. The full-drive trace is bound to the exact probe and WAV hashes. CoreAudio rendered diagnostics at 44.1 kHz, so production acceptance still separately requires 48 kHz. All 98 Python tests pass, `git diff --check` is clean, final review found no high/medium issues, and Max is fully exited.
- 2026-08-18 top-level silence/W-S repair: the profile `Output` toggle had only driven a 60 ms gain ramp and never enabled `ezdac~`, while every runtime deliberately loaded both DSP and gain off; ignition/start therefore remained silent unless the small DAC object was separately clicked. Each profile now exposes one `Audio + Output` toggle wired to both DSP and the gain ramp. New generated `patchers/keyboard_drive_ws.maxpat` provides Manual-only W throttle and S brake ramps, handles upper/lowercase keycodes and key-up, collapses repeat events, and forces both pedals to zero when leaving Manual. The exact structural regression test failed before the fix and passes afterward; all 85 tests pass. Final Max 8.6.5 EV/V10/V12 loads resolved the keyboard abstraction with no missing-object, patchcord, outlet, or Gen errors. All task-opened Max instances and the pre-existing V4-only instance were closed; final Max process count was zero.
- 2026-08-18 three-runtime rebuild: `main.maxpat` is now a DSP-free launcher for independent `VehicleSoundSynth-EV.maxpat`, `VehicleSoundSynth-V10.maxpat`, and `VehicleSoundSynth-V12.maxpat` runtimes. Each fixed profile owns one controller, drive model, one Gen powertrain, transient host, and public `vehicle_engine_<profile>~` seam; inactive profiles are absent rather than gain-muted. V10 catch settles 1050->740 RPM, V12 1100->780 RPM, and automatic throttle waits two seconds after start.
- Current V10 continuous audio is fully procedural: RPM/load/acceleration drive a phase-continuous raised-cosine firing model calibrated from the tracked Ferrari lifecycle target table. No idle, acceleration, deceleration, atlas, residual, CC0 texture loop, or Ferrari lifecycle sample is loaded by V10/V12 continuous runtime. V12 remains independently synthesized. Only V10's optional `start_style realistic` one-shot may load the ignored local Ferrari startup derivative.
- The 18-loop Ferrari atlas and its seam/cadence tests are retained only as superseded offline analysis tooling. They are never runtime inputs. `tools/validate_v10_lifecycle.py` now reads the tracked 14-node target table and gates real synthesized role renders for low/mid body, rumble, harsh/air energy, centroid, roll-off, sample rate, clipping, and level.
- Historical note (superseded): an earlier build used continuous local/CC0 texture players and fixed an integer lifecycle gate. Those players and their sample-led validation figures do not describe the current runtime.
- Engine start defaults to the seed-once user-tunable `engine_start_beap~` cinematic voice, with realistic sample option for ICE and voice suspension after 1.2 s. EV adds seed-once Relax/Expressive/Sport BEAP graphs; a 250 ms host crossfade then suspends inactive `poly~` voices.
- The DSP-free launcher now broadcasts a profile selection, lets the active top-level runtime execute `write`/`wclose`, and then uses `loadunique` for one replacement. This makes the one-profile CPU contract enforceable instead of relying only on operator discipline.
- Validation: 84 Python tests pass; generator determinism, provenance hashes, full-atlas gating, and patchcord checks pass; `git diff --check` is clean; and no `media/local/` files are tracked. Runtime probes now pass all controls through the fixed drive simulator and controller, so start-to-idle checks exercise the 1050->740 / 1100->780 flare path without injecting `engine_running` or `combustion_gain`. High-RPM probes route drive RPM through a test switch, wait 1000 ms for catch, then lock the requested 3500/4200 RPM before recording so drive ticks cannot overwrite the spectral target. Final Max 8.6.5 EV/V10/V12 profile loads produced no object, Gen, patchcord, outlet, or missing-media errors after the clean 15:22 log baseline; each runtime received `write`/`wclose` before the next, and the final Max process count was zero.
- 2026-08-18 Ferrari-body repair: V12/V10 discontinuous exponential bank pulses were replaced by zero-wrap raised-cosine fourth-power pulses, idle saturation was reduced, and the fuel path now opens an MSP low-pass from roughly 3.0 kHz at idle toward 8.4 kHz at high RPM. Default V10/V12 reference texture moved to -18 dB. EV and the sibling V3 repository were not changed.
- `tools/prepare_local_reference.py --bundle` creates an ignored 48 kHz startup one-shot plus legacy idle/atlas derivatives for offline comparison. Runtime may use only the startup one-shot, at a bounded gain with tracked CC0 starter fallback; the idle body and atlas cannot enter continuous synthesis.
- Generated Max file references use `Patcher:/...` project-relative paths, so clean checkouts and runtime-probe bundles remain portable across clone locations. The probe builder resolves those references while constructing its self-contained temporary bundle.
- Final Max 8.6.5 start-to-idle renders were unclipped and were evaluated with five windows distributed across the whole file. V12 measured harmonic slope -7.063 dB/oct, upper-harmonic ratio 0.000366, 2-6 kHz ratio 0.000896, >6 kHz ratio 0.00000470, low-mid ratio 0.9666, centroid 93.5 Hz, and sample-edge ratio 0.1366. V10 measured -8.092, 0.000101, 0.000215, 0.00000131, 0.9786, 83.4 Hz, and 0.0678 respectively. The same generated high-RPM path measured sample-edge ratios 0.168 (V12 3500 RPM) and 0.213 (V10 4200 RPM), with zero clipping. Separate fresh-process 2.5 s probes produced different hashes for local-present and local-missing cases; both were non-silent, proving the `info~`-driven 20 ms local/fallback selection.
- 2026-08-17 harshness repair: V12/V10 continuous combustion returned to the known-good V3.1 phase-locked two-bank model, with the discontinuous full-firing-rate stochastic reset removed and bank pulse level reduced slightly to preserve tonal body. Combustion texture defaults moved from -6 dB to -24 dB. Starter playback now uses a 3.5 kHz low-pass and 0.16 gain instead of the former unfiltered 0.26 path. `audio_metrics.py` now reports/enforces the 2-6 kHz `harsh_ratio`; README and repository guide define separate start and post-start gates.
- Real Max 8.6.5 NonRealTime final renders passed the new post-start gates with zero clipping. V12 idle measured 2-6 kHz 0.02920, >6 kHz 0.000515, low-mid 0.86408, and rumble 0.81644. V10 idle measured 0.003405, 0.000114, 0.95623, and 0.93203 respectively. The installed NonRealTime driver again rendered at 44.1 kHz despite the requested 48 kHz, so sample-rate conformance remains a separate open validation issue. All 74 Python tests pass and `git diff --check` is clean.
- 2026-08-14 V4 acoustic rebuild: V10/V12 now use event-by-event stochastic energy/timing variation instead of periodic cycle/cylinder AM, with only three bounded phase-stable harmonic orders. The former 0.25/0.5 s local texture and +12 dB high layer were removed from runtime.
- Historical baseline (superseded): an older V4 used tracked CC0 continuous texture loops. The current V10/V12 continuous engines do not load those loops; Ferrari.wav remains analysis-only except for the explicitly local V10 startup one-shot.
- V10/V12 combustion uses separate left/right stochastic event gain and timing while retaining a coherent low-frequency center. The cabin renderer centers bass below 120 Hz and retains fold-safe upper-band Side/reflections. The final 48 kHz V12 3500 RPM render measured low/mid/high correlation 0.990/0.527/0.386, full-band mono-fold loss 1.15 dB, modulation peak ratio 0.126, envelope autocorrelation 0.164, and zero clipping.
- EV Pad defaults use triangle/sine pairs instead of saw waves, no post-sum +3 dB makeup, -3 dB stem default, and 3x stronger BEAP VCA CV. Current 48 kHz renders measured Pad Off -47.57 dBFS, Pad On -40.89 dBFS, and Pad Solo -41.66 dBFS, proving the ignition gate, independent stem, mute, and solo paths are audible. The core EV generator retains exact phase-coherent low orders and contains no near-unison beating oscillator.
- The visible four-band EQ now converts UI dB to filtergraph power gain with `10^(dB/10)` and suppresses duplicate default RTPC messages when a probe/user override is present. A 3800 Hz 48 kHz NonRealTime probe measured -33.023 dBFS flat and -45.024 dBFS at -12 dB: an exact -12.001 dB delta.
- Validation: 74 Python tests pass; generator determinism and `git diff --check` pass. Max 8.6.5 rendered V12/V10 idle/high, EV Pad On/Off/Solo, shift-up, final V12 high-RPM, and EQ probes at 48 kHz. All new probe instances were individually terminated; the pre-existing Max PID 9674 was not closed.
- V4 is an independent full copy of V3 commit `81e1345` in `/Users/saintpeter/Downloads/VehicleSoundSynth-V4`; its public project is `VehicleSoundSynth-V4.maxproj` on branch `codex/vehicle-sound-v4`. The sibling V3 directory was not modified.
- V4 implements RPM-adaptive three-band cabin stereo: strict mono below 120 Hz, a bounded 120–2000 Hz Side path, and a bounded >2 kHz Side/reflection path. V10/V12 cylinder banks use explicit Mid/Side with bank Side gain decreasing from 0.30 at idle to 0.12 at high RPM.
- Historical baseline (superseded): local SF90 idle/high residual layers were once auditioned. They are no longer runtime-reachable; their records remain analysis provenance only.
- EV now uses one continuous RPM pitch law for both motor and BEAP soundscape, with three seed-once user-editable BEAP modes. A shared cancellable 260 ms suspension timer prevents rapid mode changes from muting the newly selected voice.
- Validation on the final source: 71 Python tests pass; generated artifacts are deterministic across two rebuilds; `git diff --check` is clean. After reducing high-band Side safety to 0.42 and cross-reflections to 0.04, the latest Max NonRealTime V12 idle render measured low Side 0.00060/correlation 0.99884, mid Side 0.20804/correlation 0.58705/mono loss 1.01296 dB, high Side 0.36953/correlation 0.27271/mono loss 2.00333 dB, total mono loss 0.09483 dB, and zero clipping. The installed NonRealTime driver still wrote 44.1 kHz even after the probe sent the documented global `dsp sr 48000` command, so the render is diagnostic only and the required 48 kHz full scenario/stem/EQ/event matrix remains open; `audio_metrics.py --require-sample-rate 48000` treats any other rate as failure.
- The three generated Gen patchers expose every codebox `Param` through a bounded top-level `param` object. A fresh Max 8.6.5 probe no longer logged `doesn't understand` for `rpm`, `combustion_gain`, `shift_cut`, or the other engine controls. Transient buffers now resolve bare filenames through the project media search path instead of embedding `media/` in abstraction-relative arguments; a fresh shift-up probe rendered non-silent, unclipped output, though the complete event matrix and clean-console audit remain open.
- V4 operator documentation is `VehicleSoundSynthV4_完整使用手册.docx`; the prior V3 RTPC/DSP DOCX/PDF are retained as baseline documentation rather than represented as V4 validation evidence.
- V3 is an independent clone of committed V2 and uses `VehicleSoundSynth-V3.maxproj`; the sibling V1/V2 folders and their manuals remain unchanged.
- V3.1 rebuilds V12/V10 as phase-locked left/right cylinder banks at half the total firing-event rate, with bounded cycle variation, pulse-gated narrowband residuals, exact +35% h2/+25% h3 lifts from the fixed point, automatic seven-speed DCT events, intake backfire, exhaust pops/crackle, and a powertrain-excited cabin-rumble stage using damped 48/68/92/118 Hz modes.
- Starter playback now stops on the controller's 500 ms catch transition and ignition-off path; a start lock prevents retriggering while the engine is already running, with explicit patchcord regression coverage.
- Internal Manual now supports uppercase/lowercase W/S keyboard pedals: W ramps throttle up over 2.5 s and releases over 1.4 s; S applies brake over 120 ms and releases immediately. Key repeat is collapsed, controls reset when leaving Manual, and the keyboard envelopes stay synchronized with the existing flonums.
- EV low-frequency synthesis now shares one phase-coherent fundamental between channels; the former 1.007x/1.013x near-unison layers were replaced by locked second/third harmonics, separated high-order sheen, lower drive gain, and soft saturation.
- EV includes an ignition-gated, RPM/throttle-following dual BEAP pad. `ev_pad_driver~` contains CV mapping and independent dB/mute/solo control, centers Pad energy below 120 Hz, and applies only an 82/18 crossmix above 120 Hz; `ev_pad_beap~` remains user-tunable and is never overwritten by regeneration.
- Repaired the four-band global EQ so one visible four-node `filtergraph~` recalculates one shared coefficient list for stereo `cascade~ 4`; numeric editing, public `eq_*` messages, reset, bypass, master trim, limiter, and clip protection share the same downstream path. Shelf messages do not require Q; peak bands do.
- Installed six documented CC0 source recordings under `assets/raw/`; deterministic processing creates normalized 48 kHz PCM16 transient/fallback media without overwriting curated output. User-supplied Ferrari analysis derivatives remain ignored, uncommitted, unsynced, and undistributed; only the explicitly documented V10 startup one-shot is runtime-reachable.
- Reduced the white-noise impression by separating centered band-limited tire noise from restrained stereo wind, lowering mechanical-noise contributions, and centering low-frequency cabin/IR content before the final master chain.
- Validation: all 63 Python tests pass, generator determinism and patchcord ports pass, DOCX ZIP/OOXML audit passes, and `git diff --check` is clean. Max 8.6.5 loaded the project then `main.maxpat`; the recent system log contained no category, missing-object, Gen-outlet, or patchcord errors. Earlier real Max EQ probes measured -6.03 dB at the -12 dB shelf corner and -16.00 dB for a -16 dB trim delta (both within ±1 dB). The newest render matrix is not claimed complete: an attempted current probe produced a zero-byte WAV because other live Max instances held incompatible audio-driver state.
- `tools/audio_metrics.py` reports per-band Side ratio/correlation/mono fold loss, fullband mono loss, 1/3-octave similarity, comparison gain tolerance, and independently enforceable mid/high stereo-safety thresholds.
- Primary operator documentation is `VehicleSoundSynthV3_完整使用手册.docx`; V1/V2 manuals remain byte-for-byte unchanged. The V3 DOCX passed deterministic OOXML/ZIP audits and QuickLook cover inspection; full multi-page PDF/image QA is unavailable because LibreOffice is not installed.
- Added `VehicleSoundSynthV3_车机RTPC_DSP链路技术说明.docx` and its 12-page PDF companion. They document the current V3 signal chain, all 43 public RTPC messages, internal lifecycle/event mappings, EV/V12/V10 synthesis equations, event/sample normalization, cabin rumble/IR/M-S, four-band EQ, output protection, and Float32/fixed-point porting forms. The DOCX passed OOXML/content audits; every PDF page was rasterized and visually checked. Reproducible builders are `tools/build_rtpc_dsp_spec.py` and `tools/render_rtpc_spec_pdf.py`.
- Remaining realism boundary: event and cabin-IR layers use recordings, while continuous V12/V10 operation is still procedural rather than a measured multi-load, multi-microphone engine corpus. No Git remote or CI is configured for this repository.
<!-- AGENT_NOTES_END -->

## Mandatory Update Rule

Refresh canonical PROJECT_HANDOFF.md after branch, commit, file, directory, schema, interface,
related-repository, or material project-state changes, and before final handoff.
