# Project Handoff

> Deterministically generated repository/project memory for cross-agent handoff.
> Update after every material project change and before final reporting.

## Repository Identity

- Repository ID: `VehicleSoundSynth-V4-f1d8c907be6f`
- Working root: `.`
- Repository name: `VehicleSoundSynth-V4`
- Git repository: `true`
- Generated at: `2026-08-12T02:47:21.944374+00:00`

## Current State

- Branch: `codex/vehicle-sound-v4`
- HEAD: `6b4ddd7`
- Indexed paths: 76
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
| `media` | 24 |
| `.` | 13 |
| `patchers` | 12 |
| `assets` | 9 |
| `tools` | 9 |
| `assets/raw` | 7 |
| `.codex` | 3 |
| `gen` | 3 |
| `code` | 1 |
| `presets` | 1 |
| `tests` | 1 |

## Data and File Structure

### Categories

- audio: 30 files, 93743066 bytes
- code: 11 files, 400491 bytes
- literature: 14 files, 568819 bytes
- other: 18 files, 2398851 bytes
- structured_data: 3 files, 18325 bytes

### Common Extensions

- `.wav`: 30
- `.maxpat`: 13
- `.py`: 10
- `.md`: 6
- `.docx`: 5
- `.json`: 3
- `.gendsp`: 3
- `.txt`: 2
- `[no extension]`: 1
- `.maxproj`: 1
- `.pdf`: 1
- `.js`: 1

### Schema / Model / Interface Candidates

- None detected.

## Key Entrypoints and Guides

- `AGENTS.md`
- `README.md`
- `assets/raw/README.md`

## Change History

- `6b4ddd7 2026-08-12 docs: record final V4 acoustic evidence`
- `0637838 2026-08-12 fix: resolve transient media from project path`
- `72ba1d3 2026-08-12 test: enforce upper-band stereo safety`
- `a26e162 2026-08-12 fix: improve cabin mono compatibility`
- `cdcc641 2026-08-12 fix: harden V4 runtime probe setup`
- `6814cc4 2026-08-12 fix: expose Gen parameters to Max runtime`
- `660866e 2026-08-12 docs: refresh V4 handoff`
- `cb5ce78 2026-08-12 feat: create V4 acoustic repair archive`
- `81e1345 2026-08-11 docs: refresh V3.1 handoff`
- `9066183 2026-08-11 fix: harden V3.1 stereo EQ and reference processing`
- `22bb3f1 2026-08-11 feat: add V3.1 cinematic engine mix`
- `030708f 2026-08-11 docs: refresh project handoff`
- `2f73f2b 2026-08-11 feat: stabilize EV and add dual BEAP pad`
- `99b6895 2026-08-10 docs: refresh Manual keyboard handoff`
- `1e811ab 2026-08-10 fix: synchronize Manual keyboard and pedal state`
- `5ff0aa0 2026-08-10 feat: add Manual mode W/S controls`
- `127d6fc 2026-08-10 docs: refresh V3 final handoff`
- `01a234e 2026-08-10 fix: stop starter on lifecycle transitions`
- `c3307f6 2026-08-10 feat: complete V3 vehicle sound realism overhaul`
- `4931e74 2026-08-07 docs: refresh final V3 handoff`

## Current Changes

- `## codex/vehicle-sound-v4`

## Related Repositories

### Remotes

- None detected.

### Submodules

- None detected.

## Media and Literature Routes

### literature

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
- `media/exhaust_crackle_01.wav`
- `media/exhaust_crackle_02.wav`
- `media/exhaust_crackle_03.wav`
- `media/exhaust_pop.wav`
- `media/exhaust_pop_01.wav`
- `media/exhaust_pop_02.wav`
- `media/exhaust_pop_03.wav`
- `media/exhaust_pop_04.wav`
- `media/intake_backfire_01.wav`
- `media/intake_backfire_02.wav`
- `media/intake_backfire_03.wav`
- `media/mechanical_click.wav`

### video

- None detected.

### structured_data

- `assets/asset_manifest.json`
- `assets/ferrari_sf90_acoustic_target.json`
- `presets/sound_dna.json`

## Validation and Risks

- This inventory records paths and metadata, not semantic correctness.
- Binary/media payloads and secrets were not read.
- Validate current branch, tests, and interfaces before modifying files.

## Agent Notes

<!-- AGENT_NOTES_START -->
- V4 is an independent full copy of V3 commit `81e1345` in `/Users/saintpeter/Downloads/VehicleSoundSynth-V4`; its public project is `VehicleSoundSynth-V4.maxproj` on branch `codex/vehicle-sound-v4`. The sibling V3 directory was not modified.
- V4 implements RPM-adaptive three-band cabin stereo: strict mono below 120 Hz, a bounded 120–2000 Hz Side path, and a bounded >2 kHz Side/reflection path. V10/V12 cylinder banks use explicit Mid/Side with bank Side gain decreasing from 0.30 at idle to 0.12 at high RPM.
- The local-only SF90 texture is now two normalized layers: a 250 ms idle residual from 1.0 s and a 500 ms high-RPM residual from 22.75 s. Their SHA-256 values are recorded in `assets/asset_manifest.json`; they crossfade equal-power from 1800–3000 RPM and never leave ignored `media/local/`.
- Future EV defaults `pad_level_db` to +6 dB and the generated driver adds fixed +3 dB post-BEAP makeup while preserving strict low-frequency centering and the user-owned `ev_pad_beap~` patcher.
- Validation on the final source: 70 Python tests pass; generated artifacts are deterministic across two rebuilds; `git diff --check` is clean. After reducing high-band Side safety to 0.42 and cross-reflections to 0.04, the latest Max NonRealTime V12 idle render measured low Side 0.00060/correlation 0.99884, mid Side 0.20804/correlation 0.58705/mono loss 1.01296 dB, high Side 0.36953/correlation 0.27271/mono loss 2.00333 dB, total mono loss 0.09483 dB, and zero clipping. The installed NonRealTime driver still wrote 44.1 kHz even after the probe sent the documented global `dsp sr 48000` command, so the render is diagnostic only and the required 48 kHz full scenario/stem/EQ/event matrix remains open; `audio_metrics.py --require-sample-rate 48000` treats any other rate as failure.
- The three generated Gen patchers expose every codebox `Param` through a bounded top-level `param` object. A fresh Max 8.6.5 probe no longer logged `doesn't understand` for `rpm`, `combustion_gain`, `shift_cut`, or the other engine controls. Transient buffers now resolve bare filenames through the project media search path instead of embedding `media/` in abstraction-relative arguments; a fresh shift-up probe rendered non-silent, unclipped output, though the complete event matrix and clean-console audit remain open.
- V4 operator documentation is `VehicleSoundSynthV4_完整使用手册.docx`; the prior V3 RTPC/DSP DOCX/PDF are retained as baseline documentation rather than represented as V4 validation evidence.
- V3 is an independent clone of committed V2 and uses `VehicleSoundSynth-V3.maxproj`; the sibling V1/V2 folders and their manuals remain unchanged.
- V3.1 rebuilds V12/V10 as phase-locked left/right cylinder banks at half the total firing-event rate, with bounded cycle variation, pulse-gated narrowband residuals, exact +35% h2/+25% h3 lifts from the fixed point, automatic seven-speed DCT events, intake backfire, exhaust pops/crackle, and a powertrain-excited cabin-rumble stage using damped 48/68/92/118 Hz modes.
- Starter playback now stops on the controller's 500 ms catch transition and ignition-off path; a start lock prevents retriggering while the engine is already running, with explicit patchcord regression coverage.
- Internal Manual now supports uppercase/lowercase W/S keyboard pedals: W ramps throttle up over 2.5 s and releases over 1.4 s; S applies brake over 120 ms and releases immediately. Key repeat is collapsed, controls reset when leaving Manual, and the keyboard envelopes stay synchronized with the existing flonums.
- EV low-frequency synthesis now shares one phase-coherent fundamental between channels; the former 1.007x/1.013x near-unison layers were replaced by locked second/third harmonics, separated high-order sheen, lower drive gain, and soft saturation.
- EV includes an ignition-gated, RPM/throttle-following dual BEAP pad. `ev_pad_driver~` contains CV mapping and independent dB/mute/solo control, centers Pad energy below 120 Hz, and applies only an 82/18 crossmix above 120 Hz; `ev_pad_beap~` remains user-tunable and is never overwritten by regeneration.
- Repaired the four-band global EQ so one visible four-node `filtergraph~` recalculates one shared coefficient list for stereo `cascade~ 4`; numeric editing, public `eq_*` messages, reset, bypass, master trim, limiter, and clip protection share the same downstream path. Shelf messages do not require Q; peak bands do.
- Installed six documented CC0 source recordings under `assets/raw/`; deterministic processing creates normalized 48 kHz PCM16 runtime media without overwriting curated output. A separate user-supplied SF90 file may create an ignored local V10/V12 residual: it now notches 61.5 Hz and its harmonics after filter preroll, loops for 250 ms, normalizes to -18 dBFS RMS, and is hash-documented but never committed, synced, or redistributed.
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
