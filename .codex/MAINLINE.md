# VehicleSoundSynth V6 Mainline

## IONIQ running-weight repair (2026-09-16, base 138a36d)

Current IONIQ: DNA V4 / mode beds V3. Read `.agentlab/IONIQ_WEIGHT_REPAIR_2026-09-16.md` first. Recipe `tools/ioniq_weight_balance.py`, scoped installer `tools/install_ioniq_weight.py`, state `code/ioniq_weight_state.js`, tests `tests/test_ioniq_weight.py`, source-only math `tools/check_ioniq_weight_math.py`. Preserve all previous version resources, other four profiles, drive, Start, Pop, Noise and private states. Weight Balance=0 bypasses this iteration, not the earlier Reference Restore. Native Max/listening remains a local acceptance gate. Older active-version statements below are historical where superseded.


## Current timbre repair (2026-09-16)

Target `codex/v6-ioniq-dna-accel-detail`, base `467fd72`. Read `.agentlab/V6_TIMBRE_REPAIR_2026-09-16.md`. Live IONIQ V3 / Ferrari V4; all previous version entries below are historical/rollback where superseded. Recipe `tools/timbre_repair.py`; installer `tools/install_timbre_repair.py`; state `code/timbre_repair_state.js`; contracts `tests/test_timbre_repair.py`; scalar-only checks `tools/check_timbre_repair_math.py`. New Designer seeds: `patchers/ioniq6n_sound_dna_v3~.maxpat`, `patchers/ferrari_dna_v4_designer~.maxpat`. Native Max and user listening remain required.


Active narrow follow-up (2026-09-14): local IONIQ DNA V2 acceleration detail
and full DNA state, from candidate d0df3b9. Preserve accepted Soundscape and
all driving/eShift behavior. See `.agentlab/V6_IONIQ_DNA_DETAIL.md` for pending
listening/full-project/reopen gates; test Max saved/exited, no promotion before acceptance.

Base: frozen V4 tag `v4.0.0` (`6aa49d0`).

1. Rename project/runtime identity to V6 without changing the original three-runtime architecture.
2. Replace runtime shift/pop/crackle samples with continuous powertrain/cabin motion and BEAP physical transients.
3. Improve continuous EV, V10, and V12 realism while preserving smooth throttle-driven RPM and the V10 Ferrari lifecycle analysis gates.
4. Add one editable EV/V10/V12 cinematic Soundscape plus V10/V12 backfire BEAP patchers with top-level controls and suspendable DSP.
5. Add one shared persistent four-band vehicle-bus EQ state with load/save/reload/reset and safe fallback.
6. Validate structure, deterministic generation, audio metrics, CPU behavior, and real Max 8.6.5 loading; save, close, and quit Max.
7. Add a switchable Keyboard/macOS gamepad Manual Input module with fixed
   semantic LT-throttle/RT-brake mapping, live debug, normalized pedals, and
   safe source release without changing the 20 ms drivetrain model.
8. Add IONIQ6N as an isolated fourth runtime: electric Sound DNA, optional
   eight-ratio N e-Shift, three decoupled N Sound BEAP instruments, independent
   ready activation and mode-aware N events. Preserve EV/V10/V12 acoustic files.
9. Consolidate four duplicated operator surfaces into one Main console and one
   profile-parameterized runtime host. Keep profile windows mode-only, document
   every Sound DNA control, restore IONIQ6N mixer/DNA parity, and do not retune
   any synthesis graph or factory preset.
10. Recalibrate only drivetrain response: add high-speed throttle reserve,
    distinguish abrupt lift braking from gradual coasting, and shorten service
    braking while preserving the public 0..1 throttle/brake contract.
11. Freeze the accepted V6 state, then add Ferrari as a fifth isolated,
    analysis-envelope-derived V10 acoustic interpretation with independent
    Sound DNA, Soundscape V4, procedural start and procedural backfire. Preserve
    the four accepted profiles byte-for-byte and keep all reference audio local.
12. Replace only Ferrari's live acoustic pair with versioned realism-V2 Sound
    DNA and Soundscape V5: soften square-like high-load energy, restore idle
    low-mid mass, expose the active Soundscape location/level in Main, and prove
    normal-mix audibility without changing the other four profile sounds.
13. Ferrari-only Soundscape V6 adds a polarity-aligned, gated 120–650 Hz dry
    body return. Pop V3 replaces only Ferrari's backfire renderer with one
    240 ms CC0 one-shot and two idle-muted players; existing event timing,
    Ferrari DNA/start, all other profile sounds and shared controls stay fixed.
14. Current implementation, user accepted 2026-09-10: on
    `codex/v6-layering-dna-pad-pop` from frozen `b609e8b`, separate an optional
    five-profile Noise stem (-60 dB exact off) from low-mid Soundscape beds;
    add EV/V10/V12 Soundscape V5, Ferrari V7's independent-hiss split and
    IONIQ mode-bed V2's one-return split. Upgrade V10/V12 DNA above 1200 RPM
    without changing the accepted idle. Share the existing 240 ms CC0 Pop
    player across five profiles while preserving event conditions. Preserve
    Ferrari/IONIQ DNA, starts, driving/input, FX, EQ and dynamics. Keep old
    versioned files/state, migrate only compatible settings, and validate
    actual Max playback/persistence when native QA resumes. The user authorized
    publishing this feature branch on 2026-09-10 without further retuning;
    no main merge. Unfinished automated native QA remains explicitly documented
    in `V6_RELEASE_HANDOFF.md` and is separate from user listening acceptance.
15. Isolated 2026-09-14 candidate on `codex/v6-control-dna-v3`, base `cff9d08`:
    repair IONIQ eShift without retuning its equal-RTPC audio or other drives;
    make pure sound commands independent of driving gates; add versioned
    Ferrari/V10/V12 four-group DNA and independent Ferrari Noise residuals.
    Preserve accepted SC/Start/Pop/FX, old files and private state. Track actual
    control semantics and complete factory defaults. Native matrix, CPU,
    persistence and two user listening rounds precede promotion. The user
    authorized uploading this candidate branch on 2026-09-14 before remaining
    acceptance; no main merge/push or production replacement.
