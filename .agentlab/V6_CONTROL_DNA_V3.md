# V6 control + DNA V3 candidate — implementation in progress

Base: cff9d0872af7a7b14f07a35b7b8d37de3078b59f.
Branch: codex/v6-control-dna-v3. This separate candidate worktree must not replace
the accepted Downloads/VehicleSoundSynth-V6 until native QA and user listening acceptance.

Approved scope: IONIQ eShift state/range/launch repair (8000 virtual redline,
7600 full-throttle shift, off mode unchanged); five-profile design routing;
Ferrari shared deterministic/stochastic source with independent Noise V2;
Ferrari/V10/V12 DNA V3; versioned explicit persistence and parameter documentation.
Protect EV/IONIQ timbre at identical RTPC, all starts/Pop/SC/FX, other four drive traces.

Reference material (local only): Downloads/声浪设计V6/VehicleSoundSynth_V6_Handoff_20260911.
All 22 package checksums verified. Original red contract: 4 fail / 1 pass.
Diagnostic artifact: /private/tmp/vss-v6-handoff-review-mx4zo_y4.
User backup: Downloads/.VehicleSoundSynth-Backups/v6-control-dna-v3-20260914.FCY9yM/user-state.tgz.

No acceptance claim yet. Native Max tests must save intended edits, close every
task patcher/project and exit only the task-owned Max. Never operate the user's instance.

## Implemented candidate seams

- Stage A commit b887e87: IONIQ on=8000, off=9950; upshift threshold 5000+2600*t;
  scaled ratios; mode toggle chooses closest legal gear and blends 300 ms;
  duplicate enable is idempotent; launch stays uncoupled to 2600; no 18% locked
  RPM lift multiplier. Other four drive replays and IONIQ off are unchanged.
- Main direct-design registry covers EQ/comp/actions/modes without driving
  gates. Normalized application precedes bounded feedback. No comp persistence.
  IONIQ eShift notifications are split before Internal/External selection.
- New source seam: Core / Body / Character / Upper / old L / old R / blend /
  combustion residual / mechanical residual / intake residual. Ferrari has
  exactly one source; Noise V2 gets only raw residuals, never post-DNA gain.
- Source styles: Ferrari pressure + shallow dual PM; V10 odd/even harmonic
  morph and bank-phase odd character; V12 smooth 12-partial additive/formants.
  Independent body frequencies: 48+.018*rpm / 60+.020*rpm / 42+.014*rpm.
- BEAP four-group dB mixer and four visible filters; group audition; eight V3
  macros; sample-rate-independent new envelopes; protected old ICE output at
  <=1200, smooth complete V3 blend to 3000; Side above 120; mild 3500 ceiling.
- New DNA V3 and Ferrari Noise V2 state. Import unchanged V2 legacy knobs only
  into the old controls, not old running macros. `cycle_irregularity` explicitly
  remains the inherited all-RPM clock, not an idle-only control. Noise V2 imports compatible
  V1 component/filter values; Main Noise remains independently off if muted.
- All old SC/Start/Pop/EV/IONIQ audio resources and Noise V1 graph factories
  have explicit byte/equivalence regression tests. No continuous samples added.

## Verification status (not final acceptance)

QA root: `/private/tmp/vss-v3-qa.hUGBfM` (local only; no audio/presets synced).
Final exported-source report: `export_review/native_report.json`, **140/140**
at 44.1/48 kHz. Covers exact old ICE idle null, four groups, eight-macro seams,
Body morph versus gain-only, shared clock, release, width, lifecycle and sweep.
This is actual Max-exported C++, not a separate mathematical reimplementation.
It is not a full BEAP/Max runtime acceptance or full-profile CPU measurement.

Two fresh generations: **214 files identical**, digest
`99ec2a67ca6bca05fcb4891bb2d98e3fbc7deacd4daaf0d9d77923267fcffc7b`.
An earlier full 260-test suite passed. The next 261-test run found only an old
CLI-choice assertion for three taps; it was updated for the three added stem
taps, then all 14 targeted checks passed. Final full suite: **262 tests passed**
in 261.480 seconds (`unit-final-262.log`). A later documentation-only correction
to `drive_source` metadata (0 manual / 1 auto / 2 external) passed all five
registry tests again; no DSP or routing behavior changed. `git diff --check` passes.

Native Ferrari 4000 RPM/.7 throttle/.7 load diagnostic recordings at 48 kHz:
`matrix/v3qa_ferrari_{dna,soundscape,noise,dna-sc}.wav` have 385024 frames each.
DNA: peak -13.91 dBFS, RMS -23.40 dBFS, 2–6 kHz fraction .000040, mono loss
.087 dB, steady 200-ms RMS spread .01 dB. SC: RMS -19.12 dBFS, spread 2.79 dB;
SC is preserved, not retuned to conceal this measurement. Isolated Noise has
RMS -58.81 dBFS at Main -12 dB and a .057232 high-band fraction, as a noise-only
stem; do not apply the tonal-stem harshness claim to it. These four files have
zero clipped samples. Measurements exclude the first two seconds; originals
are fixed-gain, not normalized. No before/after listening acceptance implied.
Other matrix files may have incomplete/unfinalized headers: use only explicitly
verified files. Initial unlocked/44.1k captures are diagnostic-only, not 48k passes.

## Native Max incident / safe resumption

Task PIDs 6505 and 23732 saved/closed and exited normally. Task-only Max
**PID 24644** subsequently stalled; no production project was opened. Repeated
AX queries returned -25204. A one-second stack sample showed nested AppKit modal
loops with NonRealTime `sfrecord_dowrite` sleeping on the main thread. This is
not evidence of a Gen compile failure; native runtime acceptance remains incomplete.
All opened files are disposable QA copies; candidate source/patchers are saved.
The user's first delayed permission covered only PID 6505, already absent; it
was not applied to PID 24644. The user then explicitly authorized only PID 24644.

Rechecked at 2026-09-14 07:03 UTC: PID 24644 is the sole Max process, started
at 14:26:38 local time. Its disk-state backup is
`Downloads/.VehicleSoundSynth-Backups/max-v3-24644-20260914.VKdrg2/task-disk-state.tgz`,
SHA-256 `53f385ad49ed8a64500ac6ae8c59f42f83f2100c7374658abc102c8661a13753`.
It contains the disposable V10 probe, unfinished recording, matrix manifest,
stack sample and save-dialog screenshot. This does **not** save any unsaved
in-memory Max state.

At 2026-09-14 07:07 UTC, the executable path and original start time were checked
again and the backup SHA verified. SIGTERM was sent only to PID 24644 under the
new exact-instance authorization. It exited; SIGKILL was not needed. Process
checks confirmed PID 24644 absent and no remaining Max processes. No new Max
session was opened. This was authorized process termination, not a successful
in-application Save/Close; any unsaved disposable test UI state may be lost.
Candidate source and generated patchers remain saved in local commit `1b670bb`.
Exit cleanup is complete, but the native/listening gates below are still open.

V3 probe generation now deliberately has **no automatic wclose**. Save/close
once after recording, verify the finalized WAV header, and exit task Max before
opening another probe. Never loop Close or batch new documents through a Save
modal; unavailable AX windows are an error, not an empty window list. The full
30-case manifest remains `matrix/matrix.json`; it is not 30 completed tests.

Still required: all remaining stems/RTPC cases, original-versus-candidate equal-
level comparisons, native Save/Reload/Reset/reopen, five runtime GUI checks via
the actual maxproj, full-profile CPU comparison (10–15% is the package's suggested
budget, not a measured pass), and two user listening rounds. None authorizes
overwriting production early.

## Standards

Standards: no hard violations found; the all-RPM clock labeling finding is fixed.
The pre-delivery hash-guarded seed refresh exception is explicit in AGENTS.md.

## Spec

All four implementation findings fixed: full BEAP factory restore clients,
non-gain-only Body plus independent pressure mix, accurate shared-clock scope,
and contract/status export. Follow-up corrected transpose to -12..12 and reads
BEAP parameter ranges and exact V3/Noise namespaces. Five registry audit tests
passed. Native/listening gates above remain open; review did not certify them.

Review summary: Standards 1 original judgement finding fixed, 0 hard violations;
Spec 4 original + 2 follow-up implementation findings fixed; native gates open.

## Control documentation and remote

`code/design_control.js` documents 91 selectors. `controls/visible_controls.csv`
contains 1520 entries, including repeated Main/BEAP controls across profiles.
Every unmeasured UI item remains `native_unverified`; known static bounds and
message paths are included, not replaced by that status. User-facing meanings,
save scope and rollback: `V6_CANDIDATE_GUIDE.md`.

No candidate push or production replacement until acceptance. Existing accepted
branch remains cloud release; new implementation commits remain local for now.
Read-only GitHub check on 2026-09-14: accepted feature branch is still
`cff9d0872af7a7b14f07a35b7b8d37de3078b59f`; main is
`ac2b37d8639027d79934a2023cf8d1d37d3b2f96`. The V3 candidate branch does not
exist on origin. There is no remote candidate CI result to claim.
