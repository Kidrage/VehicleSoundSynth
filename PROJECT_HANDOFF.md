# Project Handoff

> Deterministically generated repository/project memory for cross-agent handoff.
> Update after every material project change and before final reporting.

## Repository Identity

- Repository ID: `VehicleSoundSynth-V3-e69f9ccd340b`
- Working root: `.`
- Repository name: `VehicleSoundSynth-V3`
- Git repository: `true`
- Generated at: `2026-08-10T09:53:11.974032+00:00`

## Current State

- Branch: `codex/vehicle-sound-v3`
- HEAD: `1e811ab`
- Indexed paths: 64
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
| `media` | 23 |
| `.` | 10 |
| `patchers` | 9 |
| `assets` | 8 |
| `assets/raw` | 7 |
| `tools` | 6 |
| `.codex` | 3 |
| `gen` | 3 |
| `presets` | 1 |
| `tests` | 1 |

## Data and File Structure

### Categories

- audio: 29 files, 93695022 bytes
- code: 7 files, 250568 bytes
- literature: 11 files, 172602 bytes
- other: 15 files, 477380 bytes
- structured_data: 2 files, 14799 bytes

### Common Extensions

- `.wav`: 29
- `.maxpat`: 10
- `.py`: 7
- `.md`: 6
- `.docx`: 3
- `.gendsp`: 3
- `.txt`: 2
- `.json`: 2
- `[no extension]`: 1
- `.maxproj`: 1

### Schema / Model / Interface Candidates

- None detected.

## Key Entrypoints and Guides

- `AGENTS.md`
- `README.md`
- `assets/raw/README.md`

## Change History

- `1e811ab 2026-08-10 fix: synchronize Manual keyboard and pedal state`
- `5ff0aa0 2026-08-10 feat: add Manual mode W/S controls`
- `127d6fc 2026-08-10 docs: refresh V3 final handoff`
- `01a234e 2026-08-10 fix: stop starter on lifecycle transitions`
- `c3307f6 2026-08-10 feat: complete V3 vehicle sound realism overhaul`
- `4931e74 2026-08-07 docs: refresh final V3 handoff`
- `c015005 2026-08-07 fix: harden stereo level validation`
- `e9cd491 2026-08-07 feat: add combustion cabin rumble V3`
- `b8cefa5 2026-08-07 docs: refresh final V2 handoff state`
- `20332d0 2026-08-07 fix: reject start events before ignition`
- `9449ee8 2026-08-07 docs: record final V2 validation`
- `f5f2a4a 2026-08-07 fix: gate automatic drive and transient events`
- `e3562cf 2026-08-07 docs: refresh V2 project handoff`
- `ec29ab4 2026-08-07 fix: tighten lifecycle and DCT event causality`
- `99e87ba 2026-08-07 feat: build combustion-focused vehicle sound V2`
- `594acd1 2026-08-06 fix: make generated Max project produce audio`
- `7dada34 2026-08-06 fix: use Max-compatible project search path schema`
- `e1cc86c 2026-08-06 docs: refresh project handoff`
- `ed5201e 2026-08-06 docs: add complete VehicleSoundSynth user manual`
- `cfc59a0 2026-08-06 docs: refresh project handoff`

## Current Changes

- `## codex/vehicle-sound-v3`

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
- `presets/sound_dna.json`

## Validation and Risks

- This inventory records paths and metadata, not semantic correctness.
- Binary/media payloads and secrets were not read.
- Validate current branch, tests, and interfaces before modifying files.

## Agent Notes

<!-- AGENT_NOTES_START -->
- V3 is an independent clone of committed V2 and uses `VehicleSoundSynth-V3.maxproj`; the sibling V1/V2 folders and their manuals remain unchanged.
- Rebuilt the V12/V10 sources as differentiated multi-harmonic combustion models with AM/FM sidebands, load texture, lifecycle gating, automatic seven-speed DCT events, intake backfire, exhaust pops/crackle, and a powertrain-excited cabin-rumble stage using damped 48/68/92/118 Hz modes.
- Starter playback now stops on the controller's 500 ms catch transition and ignition-off path; a start lock prevents retriggering while the engine is already running, with explicit patchcord regression coverage.
- Internal Manual now supports uppercase/lowercase W/S keyboard pedals: W ramps throttle up over 2.5 s and releases over 1.4 s; S applies brake over 120 ms and releases immediately. Key repeat is collapsed, controls reset when leaving Manual, and the keyboard envelopes stay synchronized with the existing flonums.
- Repaired the four-band global EQ coefficient path and all master/stem dB controls. Public stem messages are `powertrain_level_db`, `transient_level_db`, `road_level_db`, and `rumble_level_db` (-60..+6 dB); `cabin_ir_mix`, master trim, bypass, limiter, and clip protection remain downstream.
- Installed six documented CC0 source recordings under `assets/raw/`; deterministic processing creates normalized 48 kHz PCM16 runtime media without overwriting curated output. The Ferrari acceleration file is preserved intentionally as the sixth downloaded listening reference and is not loaded at runtime.
- Reduced the white-noise impression by separating centered band-limited tire noise from restrained stereo wind, lowering mechanical-noise contributions, and centering low-frequency cabin/IR content before the final master chain.
- Validation: all 45 Python tests pass and `git diff --check` is clean. A post-change Max 8.6.5 project/main smoke check loaded with DSP muted and produced none of the blocking category, missing-object, Gen-outlet, or patchcord errors. Runtime component probes previously confirmed EQ turnover/peak response, master/stem gain response, and differentiated V12/V10 spectra; the last post-IR side-filter revision remains structurally covered rather than repeatedly rendered after Core Audio instance contention.
- Primary operator documentation is `VehicleSoundSynthV3_完整使用手册.docx`; V1/V2 manuals remain byte-for-byte unchanged. The V3 DOCX passed deterministic OOXML/ZIP audits and QuickLook cover inspection; full multi-page PDF/image QA is unavailable because LibreOffice is not installed.
- Remaining realism boundary: event and cabin-IR layers use recordings, while continuous V12/V10 operation is still procedural rather than a measured multi-load, multi-microphone engine corpus. No Git remote or CI is configured for this repository.
<!-- AGENT_NOTES_END -->

## Mandatory Update Rule

Refresh canonical PROJECT_HANDOFF.md after branch, commit, file, directory, schema, interface,
related-repository, or material project-state changes, and before final handoff.
