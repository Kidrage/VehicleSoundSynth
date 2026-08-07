# Project Handoff

> Deterministically generated repository/project memory for cross-agent handoff.
> Update after every material project change and before final reporting.

## Repository Identity

- Repository ID: `VehicleSoundSynth-V2-e4c8994a8fe9`
- Working root: `.`
- Repository name: `VehicleSoundSynth-V2`
- Git repository: `true`
- Generated at: `2026-08-07T01:43:36.090956+00:00`

## Current State

- Branch: `codex/vehicle-sound-v2`
- HEAD: `594acd1`
- Indexed paths: 26
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
| `.` | 7 |
| `patchers` | 6 |
| `.codex` | 3 |
| `gen` | 3 |
| `media` | 3 |
| `tools` | 2 |
| `presets` | 1 |
| `tests` | 1 |

## Data and File Structure

### Categories

- audio: 3 files, 38532 bytes
- code: 3 files, 100086 bytes
- literature: 7 files, 68087 bytes
- other: 12 files, 167505 bytes
- structured_data: 1 files, 612 bytes

### Common Extensions

- `.maxpat`: 7
- `.md`: 4
- `.gendsp`: 3
- `.wav`: 3
- `.py`: 3
- `.txt`: 2
- `[no extension]`: 1
- `.maxproj`: 1
- `.docx`: 1
- `.json`: 1

### Schema / Model / Interface Candidates

- None detected.

## Key Entrypoints and Guides

- `AGENTS.md`
- `README.md`

## Change History

- `594acd1 2026-08-06 fix: make generated Max project produce audio`
- `7dada34 2026-08-06 fix: use Max-compatible project search path schema`
- `e1cc86c 2026-08-06 docs: refresh project handoff`
- `ed5201e 2026-08-06 docs: add complete VehicleSoundSynth user manual`
- `cfc59a0 2026-08-06 docs: refresh project handoff`
- `3f4ffcf 2026-08-06 feat: add Max vehicle sound synthesizer MVP`

## Current Changes

- `## codex/vehicle-sound-v2`
- ` M .codex/REPO_GUIDE.md`
- ` M .codex/source_index.txt`
- ` M AGENTS.md`

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
- `VehicleSoundSynth_完整使用手册.docx`

### image

- None detected.

### audio

- `media/exhaust_pop.wav`
- `media/mechanical_click.wav`
- `media/shift_thump.wav`

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
- V2 is independent from the sibling V1 repository and uses `VehicleSoundSynth-V2.maxproj`; the folder and project filename must match for Max 8.6.5.
- Implemented combustion lifecycle for V12/V10: ignition, starter, engine-running gate, idle body, load-dependent harmonics, and 90 ms DCT shift cut/recovery.
- Implemented profile-aware seven-speed DCT plus round-robin starter, up/down shift, intake backfire, exhaust pop, and crackle families. Combustion-only events are gated out of Future EV.
- Implemented quieter road/air noise and `mix_master~`: four-band stereo EQ, click-safe bypass, -24..0 dB trim, and the sole final limiter/clip stage.
- Primary operator documentation is `VehicleSoundSynthV2_完整使用手册.docx`; the V1 manual remains as a reference copy and is not overwritten.
- Validation: 26 Python tests pass; fresh Max 8.6.5 project and main loads produce zero Console errors/warnings. A monitor-muted V12 idle render measured peak -25.78 dBFS, RMS -35.33 dBFS, high-frequency ratio 0.000005%, and 40-500 Hz ratio 67.99%.
- The standard DOCX renderer could not run because LibreOffice/soffice is absent; the V2 manual passed its deterministic OOXML structural audit but still needs optional page-image QA on a host with LibreOffice.
<!-- AGENT_NOTES_END -->

## Mandatory Update Rule

Refresh canonical PROJECT_HANDOFF.md after branch, commit, file, directory, schema, interface,
related-repository, or material project-state changes, and before final handoff.
