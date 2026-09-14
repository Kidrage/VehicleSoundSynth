# IONIQ DNA acceleration detail — 2026-09-14

## Scope / acceptance contract

Local-only branch `codex/v6-ioniq-dna-accel-detail`, frozen at `d0df3b9`.
Only modest acceleration-order detail and IONIQ DNA persistence are changed.
Preserve candidate Soundscape (all three modes, factories and private states),
other four voices, Start/Pop/Noise/EQ/FX, Main controls and N e-Shift/drive model.
No production replacement or GitHub push before listening acceptance.

Approved DSP contract: reuse existing 1.5x / 2.25x partials; no new oscillator,
noise, distortion or reverb. `Accel Orders` 0..1, default .30, 0 disables the
enhancement. Maximum amplitude multipliers 1.50 / 1.80. Positive accel,
throttle and positive load multiply a smooth 1200–3000 RPM window. Envelope
80 ms attack / 180 ms release, sample-rate-independent. Original phase,
root/RPM mapping, Body, HF Edge and default BEAP mix remain unchanged.
Do not widen old macro mappings without full-chain audio evidence and a clear
safety benefit. Preserve default sound; any future widening <=50% first pass.

## Implementation / use

Launch the candidate `VehicleSoundSynth-V6.maxproj`, Main → IONIQ6N → DNA Open.
The sounding file is `patchers/ioniq6n_sound_dna_v2~.maxpat` (seed-once), backed
by `ioniq6n_powertrain_v2~` and its versioned Gen. Old resources remain intact.
Start with Accel Orders .30; compare 0 / .30 / 1 while accelerating above
3000 RPM. This is spectral detail, not a master gain or a new Soundscape.

Save DNA explicitly after tuning. Reload DNA restores saved macros and BEAP
controls. Factory Reset restores AND saves the whole factory, including filter
mode/CV, Mixer mute/gains and VCA mode. No automatic closebang overwrite.
State: `presets/local/ioniq6n_sound_dna_v2.json`; factory slot 99. On first load,
compatible V1 macro/BEAP values are overlaid on a complete factory. V1 state and
every Soundscape state are read-only/protected; no Soundscape migration occurs.

The ten old mappings remain unchanged: measured full-BEAP endpoint spectral
differences show they are connected. Mechanical Texture (~2.2%) and HF Edge
(~0.86%) are intentionally subtle under the existing filtered mix, not broken
wires. Ready Bed must be tested at idle; Release Mass on negative acceleration;
Width is mostly Side and is difficult to hear on a mono/low-frequency monitor.
Avoid boosting upper-edge gain merely to make the knob conspicuous.

## Evidence / limits

- Actual Max-exported C++: 74/74 source checks at 44.1 and 48 kHz. Zero-enhancement
  null is bit-identical at 650/1200/2000/4000/6500/8000 RPM. Idle and inactive
  positive-acceleration gates null. No clipping; mono fold <=3 dB.
- Actual monitor-muted BEAP recording: 48 kHz, ~57.5 seconds, all ten macro
  endpoint pairs plus enhancement 0/.30/1. Peak ~0.793. At 4000 RPM/full effort,
  default enhancement raises 1.5x/2.25x-to-root ratios ~1.31/~1.95 dB. 2–6 kHz
  mean-square power ~1.27e-6 (<.001); mono fold ~.0001 dB in those samples.
- Live Max nested-state checks: initial factory, Save→Reload, full Factory
  Reset and subsequent Reload all pass for macro, BEAP filter and Mixer.
  Actual application-close/reopen persistence still requires final acceptance.
- QA directory `/private/tmp/vss-ioniq-detail.ehjEsh`. Source report
  `native_report.json`; full-chain `runtime2/beap.wav`; state `state/state-report.json`.
  Media/exported vendor code are temporary and never committed or synced.
- Initial inline QA had an invalid factory path; file-backed QA corrected it.
  Console also contains transient QA path lookup/zero-length state-only recorder
  errors. They are not a clean full-project smoke result; do not claim one.
- Unit suite and final review status are recorded below after completion.
- Task Max PID 37846 stopped recording and DSP. Normal save was issued for the
  front QA patcher; further normal quit/window queries were denied by the tool
  approval service (model capacity), not Max. User has been asked to save/quit.
  **Exit of all patchers is not yet confirmed. No force-exit authorized or used.**

## Rollback / resources

Accepted source folder `/Users/saintpeter/Downloads/VehicleSoundSynth-V6` untouched.
Candidate backup: `Downloads/.VehicleSoundSynth-Backups/ioniq-dna-detail-20260914.GWMJK0/candidate-state.tgz`
SHA256 `4288eeb08797c2d60f0de17f117e4605e8a14911e3a9c0fbf73f045b1b4ddf16`.
This local snapshot includes private presets, excludes media and Git, and must
not be uploaded. Published prior branch `codex/v6-control-dna-v3` stays at d0df3b9.
For exact rollback use that branch in a separate worktree after closing Max;
do not overwrite active/private files or reset the user's production worktree.

Source seams: `tools/ioniq_dna_v2.py`, bounded V2 paths in `build_project.py`,
`code/ioniq_dna_v2_state.js`. Install only with `tools/install_ioniq_detail.py`.
QA: `build_ioniq_detail_export.py`, `check_ioniq_detail_native.py`,
`build_ioniq_detail_runtime.py`, `ioniq_detail_state_probe.js`.
