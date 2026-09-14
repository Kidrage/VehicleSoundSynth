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
- BEAP four-group dB mixer and four visible filters; group audition; seven V3
  macros; sample-rate-independent new envelopes; protected old ICE output at
  <=1200, smooth complete V3 blend to 3000; Side above 120; mild 3500 ceiling.
- New DNA V3 and Ferrari Noise V2 state. Import unchanged V2 idle knobs only
  into the old-idle controls, not old running macros. Noise V2 imports compatible
  V1 component/filter values; Main Noise remains independently off if muted.
- All old SC/Start/Pop/EV/IONIQ audio resources and Noise V1 graph factories
  have explicit byte/equivalence regression tests. No continuous samples added.

## Verification status (not final acceptance)

QA root: `/private/tmp/vss-v3-qa.hUGBfM` (local only).
Max task PID: 6505; no Max existed before launch. All opened windows are QA
patchers/projects in that root. Normal close/quit must be confirmed at delivery.

First full suite: 253 tests, 6 failures + 1 error were old V2/live-feedback
expectations; updated targeted contracts now pass. Full rerun pending.
Initial Max render was diagnostic-only: actual 44.1 kHz despite a 48k request,
and did not lock RPM. It must NOT be used to certify 4000-RPM or 48k acceptance.
Max-native export succeeded without object/Gen errors (console contains only
duplicate-media-name warnings inside the old probe bundle).
First exported-source run: 124 checks passed at 44.1/48 kHz, including exact
ICE old-idle null, four audible groups, macro endpoints, release, width, gate,
and 740–10000 sweep. Final optimized-source rerun is pending.

Still required: complete Max/BEAP stems and parameter Save/Reload/Reset/reopen,
full-profile CPU comparison <=15%, harshness/mono/pumping at real output,
five runtime GUI smoke checks, two level-matched listening rounds. These
remain release gates, not reasons to overwrite the accepted project early.

No candidate push or production replacement until acceptance. Existing accepted
branch remains cloud release; new implementation commits remain local for now.
