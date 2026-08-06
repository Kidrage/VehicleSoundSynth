# Project Handoff

> Deterministically generated repository/project memory for cross-agent handoff.
> Update after every material project change and before final reporting.

## Repository Identity

- Repository ID: `VehicleSoundSynth-529320b305be`
- Working root: `.`
- Repository name: `VehicleSoundSynth`
- Git repository: `true`
- Generated at: `2026-08-06T11:05:06.754166+00:00`

## Current State

- Branch: `codex/vehicle-sound-mvp`
- HEAD: `7dada34`
- Indexed paths: 27
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
| `.` | 8 |
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
- literature: 8 files, 111018 bytes
- other: 12 files, 167505 bytes
- structured_data: 1 files, 612 bytes

### Common Extensions

- `.maxpat`: 7
- `.md`: 5
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

- `7dada34 2026-08-06 fix: use Max-compatible project search path schema`
- `e1cc86c 2026-08-06 docs: refresh project handoff`
- `ed5201e 2026-08-06 docs: add complete VehicleSoundSynth user manual`
- `cfc59a0 2026-08-06 docs: refresh project handoff`
- `3f4ffcf 2026-08-06 feat: add Max vehicle sound synthesizer MVP`

## Current Changes

- `## codex/vehicle-sound-mvp`
- ` M .codex/REPO_GUIDE.md`
- ` M .codex/repo_files.txt`
- ` M .codex/source_index.txt`
- ` M AGENTS.md`
- ` M PROJECT_HANDOFF.md`
- ` M README.md`
- ` M VehicleSoundSynth.maxproj`
- ` M "VehicleSoundSynth_\345\256\214\346\225\264\344\275\277\347\224\250\346\211\213\345\206\214.docx"`
- ` M gen/ev_powertrain.gendsp`
- ` M gen/v10_powertrain.gendsp`
- ` M gen/v12_powertrain.gendsp`
- ` M main.maxpat`
- ` M patchers/drive_simulator.maxpat`
- ` M patchers/road_air~.maxpat`
- ` M tests/test_project.py`
- ` M tools/build_project.py`
- `?? "MaxMSP_\347\224\265\345\212\250\350\275\246\350\266\205\350\267\221\345\243\260\346\265\252\345\220\210\346\210\220\345\231\250\346\226\271\346\241\210.md"`

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
- `MaxMSP_电动车超跑声浪合成器方案.md`
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
- Complete Chinese operator and realism-tuning manual: `VehicleSoundSynth_完整使用手册.docx`.
- Rebuild the manual with `tools/build_user_manual.py` in an environment that provides `python-docx`.
- Manual validation completed: DOCX structural audit, 10-page render review, and all 12 project tests passed.
- `MaxMSP_电动车超跑声浪合成器方案.md` is user-owned, untracked source material; preserve it unless explicitly asked to add it.
- Runtime fix after HEAD `7dada34`: nested Max project categories plus explicit `./` search paths, Max-compatible `switch`/`svf~` and expressions, direct toggle-to-`ezdac~` control, valid `slide` arguments, and explicit Gen `out 1` / `out 2` ports.
- Verification: 13 Python tests pass; fresh Max 8.6.5 project load has zero errors/warnings; automated 48 kHz stereo recording measured non-zero engine output (`RMS=3713`, `Peak=18159`). Open the project first, then main in the same Max instance to avoid a search-path registration race.
<!-- AGENT_NOTES_END -->

## Mandatory Update Rule

Refresh canonical PROJECT_HANDOFF.md after branch, commit, file, directory, schema, interface,
related-repository, or material project-state changes, and before final handoff.
