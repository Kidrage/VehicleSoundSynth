# Project Handoff

> Deterministically generated repository/project memory for cross-agent handoff.
> Update after every material project change and before final reporting.

## Soundscape held-context control repair (2026-09-08)

Branch `codex/v6-soundscape-control-repair` starts at `adca388` and preserves
all five accepted sounds. Actual Main/Ferrari recordings reproduced Enable and
Solo being swallowed by the held audition driving gate. The shared host now
routes Soundscape design commands and DNA Solo directly to the existing engine;
pedals/lifecycle retain the original drive path. The fix also makes these
operator controls independent of Internal/External source selection.

DNA/Soundscape were already additive stems. No acoustic rewiring or retuning was
needed: 182 non-host patcher/Gen/preset/media/JS files and all original local
presets match the frozen baseline. The local Main console's unqualified name was
repaired from generator authority while preserving its other user-saved fields;
those pre-existing Main changes are excluded from the repair commit.

All 207 tests pass; two fresh 158-file builds match. Max 8.6.5 actual-runtime
A/B and Solo recordings at 44.1 kHz are unclipped. In held Load, Soundscape Off
previously remained at -31.73 dBFS; the repaired path reaches digital silence
after its existing tail. Raw DNA remains stable; Soundscape Solo Off produces
final-output silence. Save/Reload was exercised on copied local state.
All five adapters were loaded in Max; both Ferrari live designers and Factory
Reset were checked. All task windows/processes were closed; pre-existing user
Max PID 38515 remains untouched.
See `.agentlab/SOUNDSCAPE_CONTROL_AUDIT_2026-09-08.md` for evidence, backup hashes
and the V10/V12 analysis. V10/V12 timbres were not changed.

## Ferrari realism V2 / Soundscape V5 repair (2026-09-04)

Branch `codex/v6-ferrari-realism-v2` starts from Ferrari V1 commit `38bcf10`
and preserves the accepted V6 rollback tag
`v6-accepted-2026-09-04-672ad62`. Only Ferrari's live continuous/Soundscape
pair is version-switched: `ferrari_sound_dna_v2~` wraps
`ferrari_exciter_v2.gendsp`, while the independent exterior stem uses
`ferrari_soundscape_v5_beap~`. EV, V10, V12 and IONIQ6N synthesis graphs,
factories and profile runtimes remain byte-identical to `38bcf10`.

The V2 exciter keeps the exact `rpm/12` four-stroke cadence but replaces the
narrow eighth-power pressure spike with a broader fifth-power pulse, removes
most half-order oscillator reinforcement, reduces factory Presence/Edge, and
adds a stereo-matched 1.35 kHz output presence ceiling. The audible result is
pressure/body first instead of a bright periodic block. V5 Soundscape is not a
chord pad: one quiet sine reinforcement and the shared pressure cadence excite
body/cavity resonators; load/throttle reveal mechanical air, speed expands only
the upper reflection field, and sub-120 Hz energy stays centred. Its state lives
in fresh `ferrari_soundscape_v5` files, and Main visibly reports the active
profile/version/location plus a -12 dB factory stem level.

All 205 Python tests pass, including Ferrari-specific live-instance,
Open/Save/Reload/Reset, default-enable, no-sample and normal-mix probe contracts.
Real Max 8.6.5 diagnostic renders are unclipped. At the installed driver's
actual 44.1 kHz, DNA idle measures 91.9% low-mid energy, 91.5% rumble,
`0.000422` harshness and 11 spectral peaks; high-load DNA measures `0.002685`
harshness, a 1.00 kHz 95% rolloff and 21 peaks. Soundscape Solo high-load is
non-silent with `0.000431` harshness. In the normal high-load A/B, enabling
Soundscape changes the SHA-256, raises low-mid ratio from 65.4% to 93.7%,
raises rumble from 0.2% to 69.5%, and remains unclipped with 0.43 dB mono-fold
loss. The probes request 48 kHz, but this installed NonRealTime driver again
writes 44.1 kHz; metrics therefore report the actual rate rather than claiming
a 48 kHz acceptance render.

Post-fix verification generated two fresh 158-file project trees with identical
combined SHA-256
`ed7cef14842ae29fc33361d1e9773a71e22419518e5f4aa19f239f4de6c59679`;
the checked-in Ferrari V2 DNA, V5 Soundscape and V2 Gen seeds match that clean
generator output byte-for-byte. A final isolated Max 8.6.5 project launch closed
the crash-restored Ferrari window, reopened Ferrari through Main, confirmed the
active `ferrari` binding and visible `"Local V5" ferrari` / `-12 dB` state, then
opened the live `[ferrari_soundscape_v5_beap~]` and
`[ferrari_sound_dna_v2~]` instances. The project-qualified
`Patcher:/gen/ferrari_exciter_v2.gendsp` lookup produced no Gen-missing,
patchcord/outlet or rejected-parameter errors. Only the known Max read-only
object-database warnings and the optional untracked startup one-shot miss remain.
All task-owned Max windows/processes were exited; pre-existing user PID `38515`
was preserved.

## Independent Ferrari V10 acoustic interpretation (2026-09-04)

Accepted V6 is frozen at annotated tag `v6-accepted-2026-09-04-672ad62`
(`672ad6204841440462225008e6ea8be643f6483f`). Branch
`codex/v6-ferrari-v10` adds a fifth runtime,
`VehicleSoundSynth-Ferrari.maxpat`, without replacing or retuning EV, V10, V12
or IONIQ6N. The existing four profiles' seed-once sound files remain absent
from the baseline diff.

Ferrari is explicitly an analysis-envelope-derived V10 acoustic
interpretation, not a physical SF90 powertrain claim. Its continuous Sound DNA
uses an independent four-stroke `rpm/12` cadence and tunable body, cavity,
mechanical, presence and edge bands. Load envelopes add 4/5/3.5/2/1.5 dB by
band, fast lift-off removes 4.5 dB of edge energy, and slower low/mid release
retains mass. The separate Soundscape V4 instrument owns exterior body, cavity
projection, mechanical halo and air/reflection layers; load changes their
blend and filter colour while RPM remains the only root-pitch authority. The
final factory balance keeps the 124 Hz order centered but exposes nine measured
high-load structure peaks instead of the initial single-tone result. Start and
backfire use independent seed-once BEAP designers and are procedural-only.

`assets/ferrari_sf90_v10_interpretation_targets.json` contains sanitized
numeric targets only. No source path, reference audio, continuous derivative,
local preset, recovery file or temporary render is declared by the project or
tracked by Git. All five profiles share the existing generated runtime-host,
Main, Mixer/EQ, keyboard/gamepad and persistence topology; Ferrari adds its own
literal profile gates, state namespace and `vss.ferrari.input` bus.

All 201 Python tests pass. Two clean generator roots are byte-identical with
combined SHA-256 `1ab8cf78938d72a1c4e915bfccd82a74a98c55d3a21427d525a528be69965297`.
Max 8.6.5 rendered Ferrari controller start, stable idle, low/high-load
Soundscape Solo and backfire Solo at 48 kHz. Every render is non-silent and
unclipped, 2--6 kHz harshness stays below `0.001`, and mono-fold loss stays
below 3 dB. The final high-load Soundscape reports peak `-3.44 dBFS`, harshness
`0.000277`, nine spectral peaks and `0.082 dB` mono-fold loss; low/high-load
WAV hashes differ while their dominant root remains unchanged. The Max log has
no missing-object, Gen, patchcord/outlet or project-category blocker. Every
task-owned Max process was exited after rendering; pre-existing user PID
`38515` was left untouched.

## V6 system cleanup (2026-09-03)

Branch `codex/v6-system-cleanup` centralizes the four runtimes without changing
their accepted sound design. `main.maxpat` is now the only shared operator
surface for Audio, Ignition, input, module balance, master EQ and Sound Design.
Each vehicle patcher is a thin profile/mode adapter over a
`patchers/profile_runtime_host_<profile>.maxpat` file materialized from the same
generator topology. Literal profile binding is required because Max resolves
object class names before abstraction arguments; the common host owns the
engine, drivetrain, input, mixer, EQ, output and diagnostics chain. Profile-scoped
command/feedback buses prevent a closing runtime from receiving the newly
selected profile's controls, while `vss.<profile>.input` remains available.

Sound DNA panels received bilingual parameter names, units, audible-context
guidance and help text. The generator treats every existing Sound DNA panel as
seed-once user property and never migrates or overwrites it. IONIQ6N now uses
Main's seven-stem Mixer as the sole DNA output-gain authority; its duplicate DNA
fader was removed while the six embedded BEAP module hash stayed exactly
`292e7072a4f924e10ba5b6350ac9e6757269c44806e69fc183808e05c860c939`.
Main also reads the active profile's persisted four-band EQ state back into the
visible controls on open/save/reload/reset. No Gen/BEAP synthesis algorithm,
Soundscape factory preset, audio asset, EQ default or module-gain default was
retuned.

The public throttle/brake range remains 0..1. Full throttle now retains
15--25% more high-speed drive reserve, abrupt release creates a short lift-brake
and faster ICE RPM fall, gradual release preserves coasting, and the service
brake is stronger. EV and IONIQ6N with N e-Shift disabled remain strictly
speed-coupled. All 197 tests pass. Two post-fix generator runs produced the same
114-file patch/project/Gen/preset digest
`8d371799786bd85cece6679e41893dfd30b8f6ec93e5f8ed75cd561434aa02d7`.

Max 8.6.5 opened Main with EV, V10, V12 and IONIQ6N from a correctly named,
exact runtime-tree `git archive` copy after the final EQ-feedback/gain-authority
cleanup. Each top-level patcher recorded `savedserialnumber=0`, and the new log
contains no missing-object, Gen, patchcord, JavaScript-function or
project-category blocker. Optional local Ferrari one-shot misses and Max's
known read-only object-database warning remain environment diagnostics. The
five earlier empty task processes were force-terminated after explicit user
authorization; the final smoke process exited normally after every runtime,
Main, Project and Console window was closed. Pre-existing user PID `65075` and
its four original probe windows remain untouched.

## V6 audio baseline (2026-09-03)

The accepted four-profile sound at `3708c08` is promoted to the V6 line through
a version-only project rename to `VehicleSoundSynth-V6.maxproj`. No synthesis,
BEAP graph, factory preset, audio routing, control mapping, or drivetrain value
changes in this release commit. Two locally re-saved top-level Max patchers were
SHA-verified and archived outside Git before restoring the portable generated
versions. The clean baseline passes all 192 tests and deterministic double
generation.

## Independent IONIQ 6 N profile (2026-09-02)

Branch `codex/v5-ioniq6n-profile` adds a fourth fixed runtime,
`VehicleSoundSynth-IONIQ6N.maxpat`, from fixed point `d3dbad6`. This is not a
V10 rebuild: the committed EV, V10 and V12 acoustic artifacts remain unchanged.
The implementation commit is `ba830a8827b001e8f88b9751909e4e36fc9f9bec`.
The launcher opens only one of the four runtimes, and the IONIQ profile reuses
the verified keyboard/gamepad throttle and brake seam.

IONIQ6N owns a sample-free electric Sound DNA with separately tunable
motor-order, low-mid body/cavity, mechanical texture, high-edge, load/release
and ready-bed components. Its Soundscape is a different stem and parameter
namespace containing three seed-once BEAP instruments: Ignition, Evolution and
Lightspeed. Mode changes crossfade over 150 ms. RPM alone controls their tonal
root; load/throttle opens layers and filter colour, while speed affects only
upper air and space. The supplied road-test MP3 is analysis-only and is never a
runtime resource or tracked artifact.

Ready activation and N events are separate seed-once BEAP buses. Ignition mode
arms a restrained release bubble, Evolution arms neither release effect, and
Lightspeed arms an afterburner pop; shift impacts follow actual N e-Shift state.
The eight-ratio N e-Shift model defaults on and can be disabled with
`eshift_enable 0` for continuous EV pitch. Each tunable subsystem has its own
tracked factory state and ignored local user state.

Final verification passed all 192 tests and two consecutive generator runs
matched across 212 filtered files. The three N Sound patchers have distinct
hashes; Max NonRealTime diagnostics were non-clipping, below the `0.001`
2--6 kHz harshness threshold and within the 3 dB mono-fold limit. The recent
Max log has no new missing-object, invalid-category, Gen or patchcord blocker;
only the known application-level read-only object-database warning remains.
All task-owned project/probe instances were saved and exited. Pre-existing user
Max PID `65075` was deliberately preserved.

## Soundscape V4 rebuild (2026-09-01)

The active feature branch replaces the shared Soundscape V3 runtime with three
seed-once profile instruments: `ev_soundscape_v4_beap~`,
`v10_soundscape_v4_beap~`, and `v12_soundscape_v4_beap~`. The public Main-page
controls are unchanged. Each host consumes the controller's real
`engine_running` state and `speed_kph`; it no longer creates its own running
latch. RPM maps root pitch, speed maps only upper-band air/space, and
load/throttle map layer blend and colour.

The EV graph is a cinematic Evolution score/energy/transient design; V10 is an
exact `rpm/12` cadence plus a continuous Ignition-style order climb; V12 is an
exact `rpm/10` heavy body/exhaust-cavity design with a restrained load-driven
turbine/mechanical band. All three keep bass below 120 Hz mono-compatible.

Current start designers use `{profile}_engine_start_v3_beap~`; current ICE
backfire designers use `{profile}_backfire_v2_beap~`. Older seed-once files and
V1--V3 preset namespaces remain recoverable but are not in the audible path.

Final verification passed 184/184 tests, including keyboard/gamepad trigger
exclusivity and lifecycle gating. Nine Max 8.6.5 48 kHz Soundscape Solo renders
covered EV/V10/V12 at fixed 1800 RPM under low load, high load and 180 km/h.
All were non-silent and unclipped, with harshness below `0.001`, subsonic ratio
below `0.01`, and mono-fold loss below `3.1` dB. Fixed-RPM centroid movement was
EV `71.2 -> 119.9 / 80.9` Hz, V10 `86.9 -> 131.9 / 127.2` Hz, and V12
`103.7 -> 109.6 / 108.0` Hz (high-load / high-speed), proving that load and
speed change timbre/space without direct root-pitch jumps. All task-owned Max
probe instances exited; pre-existing windowless PID `22230` was preserved.

## Repository Identity

- Repository ID: `VehicleSoundSynth-V6-8de441799e7b`
- Working root: `.`
- Repository name: `VehicleSoundSynth-V6`
- Git repository: `true`
- Generated at: `2026-08-29T07:30:16.928757+00:00`

## Current State

- Branch: `codex/v5-ioniq6n-profile`
- Base HEAD: `d3dbad6`
- Indexed paths: 169
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
| `patchers` | 65 |
| `media` | 35 |
| `.` | 17 |
| `tools` | 13 |
| `assets` | 11 |
| `code` | 9 |
| `presets` | 9 |
| `assets/raw` | 7 |
| `.codex` | 4 |
| `gen` | 3 |
| `tests` | 3 |
| `presets/local` | 1 |

## Data and File Structure

### Categories

- audio: 41 files, 103833150 bytes
- code: 25 files, 954979 bytes
- literature: 16 files, 647208 bytes
- other: 75 files, 17424846 bytes
- structured_data: 12 files, 80989 bytes

### Common Extensions

- `.maxpat`: 69
- `.wav`: 41
- `.py`: 16
- `.json`: 12
- `.js`: 9
- `.md`: 8
- `.docx`: 5
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

- `decf0d2 2026-08-29 feat: deepen idle start and soundscape design`
- `058c2da 2026-08-29 docs: preserve legacy handoff alias`
- `ecd2cbb 2026-08-29 docs: record soundscape pitch restoration handoff`
- `fd21aa0 2026-08-29 feat: restore profile soundscape pitch and persistence`
- `e8f89cd 2026-08-28 docs: record scoped soundscape control review`
- `168a7bb 2026-08-28 fix: scope main soundscape controls by profile`
- `67ce425 2026-08-28 docs: record main soundscape control handoff`
- `0d600c8 2026-08-28 fix: expose live soundscape controls in main`
- `ad975b0 2026-08-28 docs: close soundscape stabilization review`
- `cfc65aa 2026-08-28 fix: recall soundscape state and preserve tails`
- `3b14b3a 2026-08-28 docs: record soundscape stabilization handoff`
- `973a2f2 2026-08-28 fix: stabilize live soundscape tuning and persistence`
- `1f668eb 2026-08-27 docs: preserve pre-existing Max process record`
- `0deaf5f 2026-08-27 docs: record live sound tuning validation`
- `dc84aad 2026-08-27 fix: make sound modules live and persistent`
- `857da2b 2026-08-27 docs: record keyboard pop and mixer validation`
- `f85c1ca 2026-08-27 feat: add persistent module mixer and impact pop`
- `a754277 2026-08-26 docs: record keyboard and pop pressure repair`
- `82fca86 2026-08-26 fix: restore keyboard pedals and deepen pop pressure`
- `4e22b6a 2026-08-26 docs: close pop and DNA authority handoff`

## Current Changes

- `## codex/v5-idle-start-soundscape-v2`

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
- `SOUND_DESIGN_GUIDE.md`
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
- `presets/ev_soundscape_factory.json`
- `presets/ev_soundscape_v2_factory.json`
- `presets/sound_dna.json`
- `presets/v10_soundscape_factory.json`
- `presets/v10_soundscape_v2_factory.json`
- `presets/v12_soundscape_factory.json`
- `presets/v12_soundscape_v2_factory.json`
- `presets/vehicle_bus_eq_default.json`

## Validation and Risks

- This inventory records paths and metadata, not semantic correctness.
- Binary/media payloads and secrets were not read.
- Validate current branch, tests, and interfaces before modifying files.

## Agent Notes

<!-- AGENT_NOTES_START -->
- 2026-09-01 Soundscape V3 acceptance repair:
  replaced the active V2 graph with a new V3-only state namespace and four-layer
  mechanical-resonance core. RPM remains the continuous speed-derived root;
  throttle/load change colour rather than pitch. V10/V12 idle cadence is latched
  only by Start and cleared by Ignition Off, so Soundscape cannot passively create
  combustion. V3 factories use only sine/triangle oscillator families, remove
  full-mix waveshaping, centre bass below 120 Hz and bound the structure/air
  paths. Existing V2 local/factory files remain untouched and are ignored by V3.
  Final 48 kHz isolated renders: EV Ready peak -8.98/RMS -17.32/crest 8.33 dB,
  V10 idle -2.57/-12.37/9.80 dB and V12 idle -3.37/-13.70/10.33 dB. All have
  zero clipping, harshness below 0.001 and mono-fold loss below 3 dB. The final
  179-test suite and deterministic double generation pass; drive, keyboard,
  gamepad/manual input, Mixer, Gen and public vehicle seams remain unchanged.
  Max 8.6.5 loaded all three runtimes without missing-object, Gen, category or
  patchcord blockers. Every test patcher was saved, its Project closed, and Max
  was confirmed fully exited before delivery.
- 2026-08-29 V5 idle/start/Soundscape V2 branch: added six persistent idle DNA
  controls and distinct EV/V10/V12 low-RPM layers; EV remains a ready-state
  electromagnetic bed while V10/V12 share exact bank cadence and fade smoothly
  above idle. Replaced the shared start colour path with three seed-once live
  Start Designers and kept realistic ICE samples mutually exclusive. The shared
  Soundscape now has Body/Modal, Harmonic/Macro, Noise/Resonator and Air/Shimmer
  layers, centred bass below 120 Hz, V2-only factory/local state files, and
  throttle/load timbre mapping independent of root pitch. Max exposed and the
  generator fixed a Gen parameter/local-name collision. Corrected fixed-state
  probes prove unchanged low/high-load main peaks (EV 103.629 Hz, V10 56.525 Hz,
  V12 49.796 Hz), distinct hashes/timbres, zero clipping, harshness below 0.001,
  and mono-fold loss below 3 dB. All 175 tests and deterministic double generation
  pass. Task Max instances were removed; pre-existing PID 68025 was preserved.
- 2026-08-27 keyboard/module-mixer/impact-Pop repair: the prior keyboard patch
  still had Max `gate` ports reversed. `f85c1ca` now follows the installed
  Max 8.6.5 reference exactly: inlet 0 controls the gate and inlet 1 receives
  W/S key data. Every runtime adds one persistent profile-local seven-module
  mixer, with separate Start and Pop/Event gains and a bounded non-boosting
  Master. V10/V12 Pop is now a short pressure impact: Crack is 0.008/0.006,
  Decay 0.75/0.62, and a 600/520 Hz output ceiling removes the former snare top.
  Real-Max single hits peak at -5.34/-3.76 dBFS, have 149/91 Hz attack
  centroids, 180/170 ms tails and zero clipping; randomized bursts also remain
  unclipped. All 161 tests pass, generated output matches a fresh build, the
  project/runtime blocker audit is clean, Max preferences were restored exactly,
  and all Max instances including user-authorized PID 25676 are exited.
- 2026-08-26 Pop/DNA authority repair: V10 Brightness and EV Aggression were
  confirmed dead declarations and now directly reach Gen colour paths. Pop had
  three concrete control faults: the dominant generated core bypassed most BEAP
  edits, saved flonums did not initialize reliably, and integer `line 1` objects
  truncated fractional 0--1 layer levels to zero. V10/V12 Pop Designer now
  fronts the supported live instance and exposes eight persistent authoritative
  controls over profile-local buses. Global Pitch plus Body/Crack Tune now reach
  every core, compatibility, low-pressure and tail-air tonal filter. Native BEAP
  MMF/AD/VCA remains optional short-gate colour, not the chain-health authority.
  A low/high fixed-state probe pair is generated for every visible DNA control;
  complete-profile real Max A/Bs changed RMS by 8.77 dB (EV), 14.26 dB (V10)
  and 14.74 dB (V12), with zero clipped samples. Review then found four computed
  resonant frequencies wired to `reson~` gain inlet 1; `e1e0286` moves them to
  frequency inlet 2 and locks this with a patchcord regression. Fresh final Pop
  renders are non-silent and unclipped: V10 -4.16/-25.16 dBFS peak/RMS and V12
  -4.81/-26.89 dBFS. All 156 tests pass, deterministic
  generation and `git diff --check` pass. Canonical promotion and final
  project/runtime smoke are complete; every task-owned Max PID was closed after
  reaching zero windows. The protected pre-existing background PID 25676 also
  has zero windows and was not force-closed.
- 2026-08-26 low/heavy randomized Pop: V10/V12 pressure bodies and coherent
  low modes were retuned below the former bright crack emphasis. A generated
  `backfire_burst_scheduler` around `code/backfire_burst.js` expands physical
  overrun and Test Pop into 1--5 hits, with random 140--200 ms gaps, decaying
  gain and an overall downward pitch contour plus small jitter. Shift/explicit
  events remain one hit, and retriggering cancels pending hits. `drive_model.js`
  and its physical lift-off thresholds are unchanged. Final Max Test Pop renders
  were unclipped: V10 peak/RMS -4.44/-25.05 dBFS, centroid 430 Hz, rumble ratio
  0.520; V12 -5.03/-25.88 dBFS, centroid 241 Hz, rumble ratio 0.577. Both showed
  a 0.16-second burst-envelope period. Physical overrun renders were also
  non-silent and unclipped. All 149 tests pass, generated output matches a fresh
  build, and `git diff --check` is clean. Final EV/V10/V12 and Project windows
  were saved/closed in sequence; crash recovery was restored to Ask and Max is
  fully exited.
- 2026-08-26 audible start and layered Pop: the generated transient host now
  drives a persistent starter-state gate into `engine_start_core~`, removing the
  fragile short-event seam that made Cinematic start digitally silent. The core
  models crank pulses, first-fire pressure and body modes, includes a 28 Hz
  high-pass, and layers with the unchanged seed-once BEAP colour graph. Realistic
  still selects the starter recording/fallback and continuous engines remain
  synthesized. `backfire_test 1` is audition-only and bypasses engine state;
  normal overrun/shift events still require enable, ignition and running. Pop now
  separates a longer pressure body from a short exhaust crack, adds two softer
  wall reflections, stereo differentiation and saturation; V10 is brighter and
  V12 rounder. Real Max renders were all unclipped: Cinematic start V10/V12
  peak/RMS -4.83/-16.98 and -4.41/-16.85 dBFS, controller lifecycle
  -4.58/-25.79, Test Pop V10/V12 -3.91/-25.70 and -6.29/-29.03. Final project
  smoke found no missing-object, Gen-outlet, patchcord, invalid-category or
  project blocker. All smoke windows were saved/closed and recovery preference
  restored to Ask. All 144 tests pass; generator determinism, seed-once
  preservation and `git diff --check` pass. Max rejected normal Quit/TERM only
  after every window was closed and every task file was saved; with explicit
  user authorization, exact PIDs 9109, 9300 and 44294 were then terminated.
  Final AppleScript state is `application "Max" is running = false`.
- 2026-08-25 layered procedural backfire voice: V10/V12 retain the existing
  physical `overrun` trigger and public control seam, while their seed-once BEAP
  voices are expanded into labelled Pressure Body, Exhaust Crack, and Tail
  Color/Output sections. Runtime Intensity now morphs layer colour and tail
  density as well as level. V10 is shorter/brighter; V12 is lower/rounder. The
  generated host owns only engine-state gating, event/tail scheduling, soft
  saturation, and a roughly -15 dB compatibility click. No sample or Ferrari
  runtime audio is used. Final Max NonRealTime default Solo renders were
  non-silent and unclipped: V10 peak/RMS -9.90/-41.52 dBFS and V12
  -9.44/-43.41 dBFS, with zero clipped-sample ratio. After the review fix, the
  Max-safe envelope is sourced from the visible BEAP Mixer/MMF outputs instead
  of an independent noise path; their final default centroids measured about
  826 Hz (V10) and 703 Hz (V12). Low/default/high probes
  were monotonic and spectrally distinct; the installed driver again produced
  44.1 kHz. All 139 tests pass, generator determinism and seed-once preservation
  pass, and `git diff --check` is clean. A fresh Max 8.6.5 project smoke and
  separate EV/V10/V12 loads found no new missing-object, Gen-outlet, invalid
  category, or patchcord blockers. Direct runtime loads retain the known
  search-path warning; the optional local Ferrari starter cleanly falls back.
  All task windows reached zero; Max ignored normal Quit/TERM, so exact task
  PIDs 49806, 49928, 49996, and 50085 were ended only after closure. Final
  authority-check render PIDs 51587 and 51670 likewise reached zero windows
  before exact termination. The
  pre-existing user Max PID 44294 was preserved. Crash recovery was restored
  from the temporary probe setting to `Ask`.
- 2026-08-25 realistic pedals and audible overrun backfire: Keyboard Manual now
  sends immediate W=1/0 throttle and S=0.65/0 brake with brake priority, while
  Gamepad LT/RT remain independent analog pedals. Source/Manual exit still
  releases both values synchronously and the 20 ms speed/RPM/shift integrator is
  unchanged. The shared ICE DriveModel arms only after loaded operation above
  1600 RPM and emits one bounded `overrun 0..1` event for a sufficiently fast
  lift; EV, slow/low-RPM/brake-only/off-state paths remain silent. V10/V12 hosts
  map event strength to the seed-once BEAP voice, a band-limited pressure layer,
  and a deterministic click/resonator main pop with two decaying tail impulses.
  Both ICE pages now provide Backfire Solo and Test Pop. Real Max 8.6.5 final
  Solo renders were non-silent and unclipped: V10 final peak/RMS -16.79/-43.66
  dBFS and V12 -17.39/-45.14 dBFS, with 0 clipped-sample ratio. The installed
  NonRealTime driver again wrote 44.1 kHz. All 136 tests pass, regeneration is
  deterministic, seed-once BEAP hashes are unchanged, and `git diff --check` is
  clean. The project and EV/V10/V12 runtimes loaded without missing-object, Gen
  outlet, invalid category, or patchcord blockers; direct runtime opens retain
  known search-path warnings and the optional local V10 starter falls back when
  absent. No intentional GUI edits were made; generated files had already been
  saved before the smoke. All task windows were closed. Max ignored normal Quit
  and TERM only after window count reached zero, so exact task PID 31832 was
  ended; `application "Max" is running` is false. The temporary crash-recovery
  preference used to suppress automated probe restoration was restored to Ask.
- 2026-08-25 sound-design modularization: EV/V10/V12 now route continuous
  synthesis through separate seed-once `*_sound_dna~` modules with persistent
  profile-local controls for air/detail, irregularity, stereo width, saturation,
  throttle loudness depth and profile-specific motor/combustion voices. RPM alone
  owns cadence/pitch; throttle applies a bounded dB gain and timbre/load response,
  eliminating the accidental loudness-only control seam. Independent non-integer
  upper banks and decorrelated high-frequency paths add real stereo detail without
  sample loops, saws or squares. The visible seed-once `vehicle_bus_eq~` is now
  separate from the generated compressor/limiter and saves one ignored local EQ
  state. The shared editable BEAP Soundscape adds a third oscillator, slow motion,
  multimode/formant colour, ladder filtering and deeper stereo effects; main UI
  buttons open DNA and Soundscape directly. `SOUND_DESIGN_GUIDE.md` distinguishes
  human tuning modules from generated routing/safety modules and documents every
  public control. Review follow-up removed detuned dominant ICE orders and added
  a fixed-RPM direct-powertrain A/B matrix: throttle now changes bounded spectral
  colour as well as level while both banks retain one firing cadence. Final Max
  diagnostics measured EV/V10/V12 low-to-high-throttle gain of 2.86/3.06/3.18
  dB and centroid movement of 213->222/342->353/508->524 Hz, with zero clipped
  samples. ICE mono-fold loss is 0.79-1.13 dB instead of the reviewed 2.2-2.4 dB.
  The installed NonRealTime driver produced 44.1 kHz despite a 48 kHz request,
  so this proves comparative timbre/stereo behavior, not sample-rate delivery.
  Full validation passed 132/132 tests and `git diff --check`.
  Fresh Max 8.6.5 smoke opened all three runtimes plus DNA/EQ/Soundscape modules;
  missing-object, missing-function, invalid-category, bad-outlet and patchcord-range
  blocker counts were zero. All eight task windows were explicitly saved and
  closed. Final review smoke loaded the project, three runtimes, three DNA panels,
  shared EQ and Soundscape with zero specified blocker patterns. All GUI windows
  closed; 21 probe/smoke processes accepted TERM and the last two ignored it only
  after their window count reached zero, so exact PIDs 7963 and 10984 were ended.
  Final process inspection found no Max executable and `application "Max" is
  running` was false.
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
