# Project Handoff

> Deterministically generated repository/project memory for cross-agent handoff.
> Update after every material project change and before final reporting.

## Repository Identity

- Repository ID: `VehicleSoundSynth-V4-f1d8c907be6f`
- Working root: `.`
- Repository name: `VehicleSoundSynth-V4`
- Git repository: `true`
- Generated at: `2026-08-18T08:11:35.113093+00:00`

## Current State

- Branch: `codex/vehicle-sound-v4`
- HEAD: `5024087`
- Indexed paths: 118
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
| `patchers` | 39 |
| `media` | 35 |
| `.` | 16 |
| `assets` | 10 |
| `tools` | 10 |
| `assets/raw` | 7 |
| `.codex` | 3 |
| `gen` | 3 |
| `presets` | 1 |
| `tests` | 1 |

## Data and File Structure

### Categories

- audio: 41 files, 103833150 bytes
- code: 11 files, 544512 bytes
- literature: 14 files, 580770 bytes
- other: 48 files, 8489997 bytes
- structured_data: 4 files, 24133 bytes

### Common Extensions

- `.maxpat`: 43
- `.wav`: 41
- `.py`: 11
- `.md`: 6
- `.docx`: 5
- `.json`: 4
- `.gendsp`: 3
- `.txt`: 2
- `[no extension]`: 1
- `.maxproj`: 1
- `.pdf`: 1

### Schema / Model / Interface Candidates

- None detected.

## Key Entrypoints and Guides

- `AGENTS.md`
- `README.md`
- `assets/raw/README.md`

## Change History

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
- `c36ebb0 2026-08-12 docs: refresh V4 integrity handoff`
- `e6ac257 2026-08-12 docs: align V4 acoustic guidance`
- `2d654bf 2026-08-12 docs: refresh V4 repository handoff`
- `6b4ddd7 2026-08-12 docs: record final V4 acoustic evidence`
- `0637838 2026-08-12 fix: resolve transient media from project path`
- `72ba1d3 2026-08-12 test: enforce upper-band stereo safety`
- `a26e162 2026-08-12 fix: improve cabin mono compatibility`
- `cdcc641 2026-08-12 fix: harden V4 runtime probe setup`
- `6814cc4 2026-08-12 fix: expose Gen parameters to Max runtime`
- `660866e 2026-08-12 docs: refresh V4 handoff`

## Current Changes

- `## codex/vehicle-sound-v4`
- `M  .codex/REPO_GUIDE.md`
- `M  .codex/repo_files.txt`
- `M  .codex/source_index.txt`
- ` M PROJECT_HANDOFF.md`
- `M  README.md`
- `M  VehicleSoundSynth-EV.maxpat`
- `M  VehicleSoundSynth-V10.maxpat`
- `M  VehicleSoundSynth-V12.maxpat`
- `M  VehicleSoundSynth-V4.maxproj`
- `A  patchers/keyboard_drive_ws.maxpat`
- `M  tests/test_project.py`
- `M  tools/build_project.py`

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
- `presets/sound_dna.json`

## Validation and Risks

- This inventory records paths and metadata, not semantic correctness.
- Binary/media payloads and secrets were not read.
- Validate current branch, tests, and interfaces before modifying files.

## Agent Notes

<!-- AGENT_NOTES_START -->
- 2026-08-18 top-level silence/W-S repair: the profile `Output` toggle had only driven a 60 ms gain ramp and never enabled `ezdac~`, while every runtime deliberately loaded both DSP and gain off; ignition/start therefore remained silent unless the small DAC object was separately clicked. Each profile now exposes one `Audio + Output` toggle wired to both DSP and the gain ramp. New generated `patchers/keyboard_drive_ws.maxpat` provides Manual-only W throttle and S brake ramps, handles upper/lowercase keycodes and key-up, collapses repeat events, and forces both pedals to zero when leaving Manual. The exact structural regression test failed before the fix and passes afterward; all 85 tests pass. Final Max 8.6.5 EV/V10/V12 loads resolved the keyboard abstraction with no missing-object, patchcord, outlet, or Gen errors. All task-opened Max instances and the pre-existing V4-only instance were closed; final Max process count was zero.
- 2026-08-18 three-runtime rebuild: `main.maxpat` is now a DSP-free launcher for independent `VehicleSoundSynth-EV.maxpat`, `VehicleSoundSynth-V10.maxpat`, and `VehicleSoundSynth-V12.maxpat` runtimes. Each fixed profile owns one controller, drive model, one Gen powertrain, transient host, and public `vehicle_engine_<profile>~` seam; inactive profiles are absent rather than gain-muted. V10 catch settles 1050->740 RPM, V12 1100->780 RPM, and automatic throttle waits two seconds after start.
- V10 is now sample-led by an ignored deterministic 18-loop Ferrari atlas (steady/accel/decel x six firing-rate anchors) with a source/processor/hash manifest, offline cadence alignment to the declared 65/110/180/260/380/520 Hz anchors, a 0.88-1.12 runtime playback clamp, state/RPM crossfades, and a -18 dB/500 Hz procedural underlay. V12 remains independent and uses tracked CC0 texture. All 18 V10 buffers must report loaded before local selection; any partial/missing atlas retains the tracked CC0 fallback through persistent `sig~` values.
- Cadence warping renders an extra continuation and re-closes each loop after resampling. Across the final 18 local loops, the largest wrap step is 0.0413 FS and 0.653x its channel's 99.9th-percentile ordinary adjacent-sample step; the test suite enforces that every seam remains within 1.5x that baseline.
- Critical Max fix: the three continuous texture lifecycle gates used integer `*`, truncating `1 * 0.72/0.74` to zero. They now use float `* 1.`, restoring the V10 atlas and both tracked fallbacks. A fresh Max 8.6.5 48 kHz V10 pre-cabin render changed from procedural-only -41.76 dBFS/79 Hz centroid/16 peaks to sample-led -31.32 dBFS/133 Hz centroid/62 peaks, with zero clipping. Experimental resonant post-atlas filters were rejected and removed because they increased the 2-6 kHz ratio.
- Engine start defaults to the seed-once user-tunable `engine_start_beap~` cinematic voice, with realistic sample option for ICE and voice suspension after 1.2 s. EV adds seed-once Relax/Expressive/Sport BEAP graphs; a 250 ms host crossfade then suspends inactive `poly~` voices.
- The DSP-free launcher now broadcasts a profile selection, lets the active top-level runtime execute `write`/`wclose`, and then uses `loadunique` for one replacement. This makes the one-profile CPU contract enforceable instead of relying only on operator discipline.
- Validation: 84 Python tests pass; generator determinism, provenance hashes, full-atlas gating, and patchcord checks pass; `git diff --check` is clean; and no `media/local/` files are tracked. Runtime probes now pass all controls through the fixed drive simulator and controller, so start-to-idle checks exercise the 1050->740 / 1100->780 flare path without injecting `engine_running` or `combustion_gain`. High-RPM probes route drive RPM through a test switch, wait 1000 ms for catch, then lock the requested 3500/4200 RPM before recording so drive ticks cannot overwrite the spectral target. Final Max 8.6.5 EV/V10/V12 profile loads produced no object, Gen, patchcord, outlet, or missing-media errors after the clean 15:22 log baseline; each runtime received `write`/`wclose` before the next, and the final Max process count was zero.
- 2026-08-18 Ferrari-body repair: V12/V10 discontinuous exponential bank pulses were replaced by zero-wrap raised-cosine fourth-power pulses, idle saturation was reduced, and the fuel path now opens an MSP low-pass from roughly 3.0 kHz at idle toward 8.4 kHz at high RPM. Default V10/V12 reference texture moved to -18 dB. EV and the sibling V3 repository were not changed.
- `tools/prepare_local_reference.py --bundle` now creates ignored 48 kHz stereo `ferrari_sf90_startup.wav` (0-1.2 s, -14 dBFS RMS, 3 kHz low-pass) and `ferrari_sf90_idle_body.wav` (2.5-5.5 s, -15.5 dBFS RMS, 4 kHz low-pass, 300 ms cyclic seam). Runtime uses the local startup at 0.35 gain with a 350 ms catch fade, retains a 0.08/1.6 kHz-filtered CC0 fallback, and equal-power fades the local idle body out from 100-180 Hz while retaining the CC0 bank.
- Max buffer arguments use bare filenames so the real project can resolve ignored media through its recursive `media` search path. The standalone runtime probe also mirrors local-only media at its bundle root; this was verified after an initial diagnostic render correctly exposed `can't open` errors for the former abstraction-relative `media/local/...` arguments.
- Final Max 8.6.5 start-to-idle renders were unclipped and were evaluated with five windows distributed across the whole file. V12 measured harmonic slope -7.063 dB/oct, upper-harmonic ratio 0.000366, 2-6 kHz ratio 0.000896, >6 kHz ratio 0.00000470, low-mid ratio 0.9666, centroid 93.5 Hz, and sample-edge ratio 0.1366. V10 measured -8.092, 0.000101, 0.000215, 0.00000131, 0.9786, 83.4 Hz, and 0.0678 respectively. The same generated high-RPM path measured sample-edge ratios 0.168 (V12 3500 RPM) and 0.213 (V10 4200 RPM), with zero clipping. Separate fresh-process 2.5 s probes produced different hashes for local-present and local-missing cases; both were non-silent, proving the `info~`-driven 20 ms local/fallback selection.
- 2026-08-17 harshness repair: V12/V10 continuous combustion returned to the known-good V3.1 phase-locked two-bank model, with the discontinuous full-firing-rate stochastic reset removed and bank pulse level reduced slightly to preserve tonal body. Combustion texture defaults moved from -6 dB to -24 dB. Starter playback now uses a 3.5 kHz low-pass and 0.16 gain instead of the former unfiltered 0.26 path. `audio_metrics.py` now reports/enforces the 2-6 kHz `harsh_ratio`; README and repository guide define separate start and post-start gates.
- Real Max 8.6.5 NonRealTime final renders passed the new post-start gates with zero clipping. V12 idle measured 2-6 kHz 0.02920, >6 kHz 0.000515, low-mid 0.86408, and rumble 0.81644. V10 idle measured 0.003405, 0.000114, 0.95623, and 0.93203 respectively. The installed NonRealTime driver again rendered at 44.1 kHz despite the requested 48 kHz, so sample-rate conformance remains a separate open validation issue. All 74 Python tests pass and `git diff --check` is clean.
- 2026-08-14 V4 acoustic rebuild: V10/V12 now use event-by-event stochastic energy/timing variation instead of periodic cycle/cylinder AM, with only three bounded phase-stable harmonic orders. The former 0.25/0.5 s local texture and +12 dB high layer were removed from runtime.
- Runtime V10/V12 texture is a tracked CC0 bank of twelve normalized 48 kHz stereo loops: six firing-rate anchors (65/110/180/260/380/520 Hz), two asynchronous >4 s variants per anchor, exactly -18 dBFS RMS, 250 ms cyclic seam closure, and playback clamped to 0.9-1.1x. Every loop now has approximately 0.10 full-band Side energy ratio / 0.80 L/R correlation, zero-sample wrap discontinuity, bounded slow-envelope cycling, and a mono-exact Mid reconstruction. The 520 Hz layer remains nonzero through the full firing-rate range. `/Users/saintpeter/Desktop/Ferrari.wav` is analysis-only and never loaded or distributed.
- V10/V12 combustion uses separate left/right stochastic event gain and timing while retaining a coherent low-frequency center. The cabin renderer centers bass below 120 Hz and retains fold-safe upper-band Side/reflections. The final 48 kHz V12 3500 RPM render measured low/mid/high correlation 0.990/0.527/0.386, full-band mono-fold loss 1.15 dB, modulation peak ratio 0.126, envelope autocorrelation 0.164, and zero clipping.
- EV Pad defaults use triangle/sine pairs instead of saw waves, no post-sum +3 dB makeup, -3 dB stem default, and 3x stronger BEAP VCA CV. Current 48 kHz renders measured Pad Off -47.57 dBFS, Pad On -40.89 dBFS, and Pad Solo -41.66 dBFS, proving the ignition gate, independent stem, mute, and solo paths are audible. The core EV generator retains exact phase-coherent low orders and contains no near-unison beating oscillator.
- The visible four-band EQ now converts UI dB to filtergraph power gain with `10^(dB/10)` and suppresses duplicate default RTPC messages when a probe/user override is present. A 3800 Hz 48 kHz NonRealTime probe measured -33.023 dBFS flat and -45.024 dBFS at -12 dB: an exact -12.001 dB delta.
- Validation: 74 Python tests pass; generator determinism and `git diff --check` pass. Max 8.6.5 rendered V12/V10 idle/high, EV Pad On/Off/Solo, shift-up, final V12 high-RPM, and EQ probes at 48 kHz. All new probe instances were individually terminated; the pre-existing Max PID 9674 was not closed.
- V4 is an independent full copy of V3 commit `81e1345` in `/Users/saintpeter/Downloads/VehicleSoundSynth-V4`; its public project is `VehicleSoundSynth-V4.maxproj` on branch `codex/vehicle-sound-v4`. The sibling V3 directory was not modified.
- V4 implements RPM-adaptive three-band cabin stereo: strict mono below 120 Hz, a bounded 120–2000 Hz Side path, and a bounded >2 kHz Side/reflection path. V10/V12 cylinder banks use explicit Mid/Side with bank Side gain decreasing from 0.30 at idle to 0.12 at high RPM.
- The local-only SF90 texture is now two normalized layers: a 250 ms idle residual from 1.0 s and a 500 ms high-RPM residual from 22.75 s. Their SHA-256 values are recorded in `assets/asset_manifest.json`; they crossfade equal-power from 1800–3000 RPM and never leave ignored `media/local/`.
- Future EV defaults `pad_level_db` to +6 dB and the generated driver adds fixed +3 dB post-BEAP makeup while preserving strict low-frequency centering and the user-owned `ev_pad_beap~` patcher.
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
