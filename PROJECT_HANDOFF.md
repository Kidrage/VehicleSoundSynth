# Project Handoff

> Deterministically generated repository/project memory for cross-agent handoff.
> Update after every material project change and before final reporting.

## Repository Identity

- Repository ID: `VehicleSoundSynth-V3-e69f9ccd340b`
- Working root: `.`
- Repository name: `VehicleSoundSynth-V3`
- Git repository: `true`
- Generated at: `2026-08-07T08:01:19.741582+00:00`

## Current State

- Branch: `codex/vehicle-sound-v3`
- HEAD: `e9cd491`
- Indexed paths: 52
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
| `media` | 21 |
| `.` | 9 |
| `patchers` | 9 |
| `gen` | 4 |
| `tools` | 4 |
| `.codex` | 3 |
| `presets` | 1 |
| `tests` | 1 |

## Data and File Structure

### Categories

- audio: 21 files, 411324 bytes
- code: 5 files, 179063 bytes
- literature: 9 files, 162635 bytes
- other: 16 files, 404364 bytes
- structured_data: 1 files, 1024 bytes

### Common Extensions

- `.wav`: 21
- `.maxpat`: 10
- `.py`: 5
- `.md`: 4
- `.gendsp`: 4
- `.docx`: 3
- `.txt`: 2
- `[no extension]`: 1
- `.maxproj`: 1
- `.json`: 1

### Schema / Model / Interface Candidates

- None detected.

## Key Entrypoints and Guides

- `AGENTS.md`
- `README.md`

## Change History

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
- `3f4ffcf 2026-08-06 feat: add Max vehicle sound synthesizer MVP`

## Current Changes

- `## codex/vehicle-sound-v3`
- ` M .codex/repo_files.txt`
- ` M .codex/source_index.txt`
- ` M PROJECT_HANDOFF.md`

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
- `PROJECT_HANDOFF.md`
- `README.md`
- `VehicleSoundSynthV2_完整使用手册.docx`
- `VehicleSoundSynthV3_完整使用手册.docx`
- `VehicleSoundSynth_完整使用手册.docx`

### image

- None detected.

### audio

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
- `media/shift_down_01.wav`
- `media/shift_down_02.wav`
- `media/shift_down_03.wav`
- `media/shift_thump.wav`
- `media/shift_up_01.wav`
- `media/shift_up_02.wav`
- `media/shift_up_03.wav`
- `media/starter_v10.wav`

### video

- None detected.

### structured_data

- `presets/sound_dna.json`

## Validation and Risks

- This inventory records paths and metadata, not semantic correctness.
- Binary/media payloads and secrets were not read.
- Validate current branch, tests, and interfaces before modifying files.

## Agent Notes

<!-- AGENT_NOTES_START -->
- V3 is an independent clone of committed V2 and uses `VehicleSoundSynth-V3.maxproj`; the sibling V1/V2 folders and their manuals remain unchanged.
- Added `cabin_rumble~` before `cabin_master~` and `mix_master~`: four-stroke half/main orders, 48/68/92/118 Hz cabin modes, load-responsive exhaust boom, and structure vibration, all gated by the combustion lifecycle and DCT shift envelope.
- The three public macros are `cabin_rumble`, `exhaust_boom`, and `structure_vibration`. Future EV keeps them at zero; V12/V10 ship with profile-specific strong defaults. Frequencies below 120 Hz remain centered before the existing global EQ, trim, limiter, and clip protection.
- Validation: 32 Python tests pass; fresh Max 8.6.5 project/main loads produce no new Console errors. Monitor-muted V12/V10 idle renders passed peak, RMS, high-frequency, subsonic, rumble-band, and low-side-energy gates. V12 rumble-on is approximately 4.0 dB stronger in 30-140 Hz than the rumble-off control.
- Primary operator documentation is `VehicleSoundSynthV3_完整使用手册.docx`; the V1/V2 manuals are retained byte-for-byte. The V3 DOCX passed deterministic OOXML/ZIP structural audits, but optional page-image QA remains unavailable because LibreOffice/pdf2image are absent on this host.
<!-- AGENT_NOTES_END -->

## Mandatory Update Rule

Refresh canonical PROJECT_HANDOFF.md after branch, commit, file, directory, schema, interface,
related-repository, or material project-state changes, and before final handoff.
