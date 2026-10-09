# V7 Codex engineering handoff

## Repository binding and no-guess start gate

Canonical repository: `Kidrage/VehicleSoundSynth` — `https://github.com/Kidrage/VehicleSoundSynth`, private.
Default branch: `main`; verified before task at `ac2b37d8639027d79934a2023cf8d1d37d3b2f96`.
Target branch: **EV-Engine-V7**. R2 audited start commit: **e979b0cf261004cc60cd70de1cb5dbd747812092** (existing branch, no reset). Fixed V6 source checkpoint: **fed2b78ecfabc84d673207b3a5f714b89f76720f**.
Ioniq accepted source checkpoint: `739c9d9a19432ac693e1a10a7ecd0cbb6b283dc8`.
The actual V7 delivery commit is written into the delivered release manifest after publication; bind to that exact SHA, never a synthetic container baseline commit. No production/main merge authorized.

Before editing run `git remote -v`, `git status --short`, `git branch --show-current`, `git rev-parse HEAD`, `git log -1`. Verify canonical remote, EV-Engine-V7, delivered SHA, and clean worktree. If user changes exist, record/commit them on a user-approved isolated branch before any generator; never stash/reset them silently. Re-fetch and inspect any remote changes before continuing; no force push.

Read in order: AGENTS.md; .codex/REPO_GUIDE.md and .codex/MAINLINE.md; PROJECT_HANDOFF.md; SOUND_DESIGN_GUIDE.md; V7_MANUAL.md; this handoff; assets/v7/resource_map.json; assets/v7/generated_sha256.json; assets/v7/parameter_contracts.json.

## Current implementation and exact active modules

Project `EV-Engine-V7.maxproj`; launcher `main.maxpat` (DSP-free). Five adapters `EV-Engine-V7-{EV,V10,V12,IONIQ6N,Ferrari}.maxpat`; each owns one `patchers/v7_profile_runtime_host_{ev,v10,v12,ioniq6n,ferrari}.maxpat`.

Drive: `code/v7_drive_model.js`, recipe `tools/v7/drive.py`. Ioniq threshold strategy7800WOT, Coast/Brake no pedal-induced upshift, predictive downshift gate, cut/sweep/engage, legacy strategy A/B. No spoofed CAN.

Source: `gen/v7_ev_powertrain.gendsp`, `v7_v10_dna_source_v3.gendsp`, `v7_v12_dna_source_v3.gendsp`, `v7_ioniq6n_powertrain_v4.gendsp`, `v7_ferrari_dna_source_v5.gendsp`; recipe `tools/v7/kernels.py`. Core controls actual leading partial; Ioniq high-RPM pitch compression relief and running drive span; sample-rate-independent throttle/load envelopes. Original source files remain byte-identical.

Mass: `gen/v7_mass_<profile>.gendsp`. Same DNA fader/solo/lifecycle. Fixed/slow LF multi-partials; no gear-dependent pitch migration. Do not excite the old cabin_rumble from this bed. Balance: `gen/v7_balance.gendsp` on DNA+SC continuous sum only. Dynamics: `gen/v7_dynamics.gendsp` and `patchers/v7_mix_master~.maxpat`, actual dB/ms RMS linked comp, no auto makeup; legacy peaklim then counted emergency sample clip.

UI: `patchers/v7_runtime_console.maxpat`, `v7_tone_console.maxpat`, `v7_response_console.maxpat`, `v7_lab_console.maxpat` (sixth tab) plus versioned existing Drive/Mix/Design. Parameters/hints share `tools/v7/schema.py` + `helptext.py`; R2 routing/diagnostics/save receipts in `tools/v7/review.py`. Never change a UI max without shader/state/contract/endpoint tests.

State: `code/v7_profile_state.js`; native `v7_*state*.js`; isolated local paths. `tools/v7_bind_profile.py` validates all 8 owner snapshots before publishing binding. A saved numeric state is not a successful atomic full native save; check all owners and reopening. Start/Pop file schema differences require actual Max verification. Bound presets only load when local owner missing; writes stay local.

## What is evidence, what is not

User reported pitch plateau/early repeated upshifts, lift loudness collapse, 200–400Hz domination and absent LF at speed. Source/control formulas support plausible causes; this task has no new recorded car WAV, CAN, room IR or speaker measurement.

Numeric/scalar tests cover control traces, bypass math, finite outputs at44.1/48/96k, fixed LF register, actualEQ endpoints, compression curve, clipping counter and JavaScript VM state I/O. The C++ harness is a scalar approximation, NOT vendor-exported Gen and NOT full BEAP runtime. Do not use its output to claim native sound/CPU acceptance.

The previous strict legacy run exposed unavailable Max/BEAP, macOS afconvert and archive-missing history. Portable validation reports those as skips, not passes. V6 inventory/launcher tests now explicitly protect the retained V6 fixture; V7 has its own inventory/active UI tests.

## Next execution order and permitted scope

**Phase N1 — native load and routing, no timbre tuning.** Open new Max project. Check all5 sequentially, Console/Gen objects/project categories, non-silence, monoLF/mutes, no duplicateDSP, correct V7 slider routing/readback. Audio OFF on load. Change each numerical endpoint, verify it reaches the audible instance. Run source exports via actual Gen if feasible; compare to scalar without pretending equivalence. Correct native incompatibilities in V7 recipes only.

**Phase N2 — saving and clean reopen, no spectral retuning.** Set clearly distinguishable V7 values and one nativeDesigner control perowner/profile, Save, inspect all8 JSON, close/reopenMax, compare values/audio traces. Test engine switching, invalid JSON/backup, factory→save, publish binding to clean worktree, local override precedence. Block any release if values revert or leak across profiles.

**Phase N3 — controls and mix calibration.** Recorded/internal fixed trajectories: ready, low/medium/full load, pedal taps, lift, repeated shift, braking, eshift mode toggle. Log speed/gear/vehicleRPM/renderRPM/root/pedal/state/shift_reason/GR/clip. No driving beyond road-safe limits; use replay. Existing source controls, new core/mass/balance/envelopes may be tuned perengine; no blanket recoding of five identities or changes to licensed Start/Pop assets.

**Phase N4 — car verification.** Same captured signal through realtime vs music playback, matched gain, main/Sub routing, low-level seat measurements, at least main and adjacent seat. No assumedLFE+10dB, no high-SPL sustainedsines, no claims of physicalspeaker protection. Per-car global render-side correction can be a later separate phase; current priorities1/2 are source/control, not full-carcalibration.

## Initial parameter and mixing direction

Use schema/factories, not duplicated literals. Ioniq core−2dB, oldweight−6dB, sub−18dB, fixedfoundation−22dB, cavity−2dB, relief.7, sourceattack65ms/release280ms, internalrunningdrive span6dB. Values are conservative candidates, not measuredcar targets. Other4 values are separately stored in factoryJSON.

Single harmonic/line must not unintentionally dominate; do not equalize all harmonics to the same loudness. Solo DNA/SC/combined first. Reduce core/repeatedbody before addingLF; inspect2–6k relative120–600; preserveengineidentity. Tool `tools/v7_audio_audit.py` analyzes ACTUAL exportedWAV, flags narrow-line concentration and band energies without inferringcomponentstems.

## Automated and manual acceptance

Run `python tools/build_v7.py --check`; `python -m unittest tests.test_v7 tests.test_v7_r2 -v`; strict `python -m unittest discover -s tests -v`. Only explicitly use portable validation on a machine missing known dependencies, report skips. No test removal to hide sound/routing defects.

Native acceptance: no missing/invalidobjects; all5 non-silent whileRunning, quietOff; noNaN/unboundedfeedback; selected controls affect onlyselectedengine; sourcegainmutes newbed; repeatedengineopen/close noDSPleak; 42 focused gates retained; savedtonesloadsamevalues and matchedcaptures; startupstatecannotstartaudio.

Audio acceptance: same documented drive trace, same sample rate/outputgain; capture stems and final without perclipnormalization. No emergencyclip during intendednormaloperation, no continuous excessiveGR to compensatewrongbalance; LF quality persists beyondthirdgear; no unexplained dominant200–400Hzline. A/B at matchedloudness, userIoniqidentityaccepted, othersindividuallyevaluated. Record actual limits and tradeoffs, not“allfixed”.

## Git and rollback

No main write/merge/default-branchchange. Source/DesignerV6files protected bySHAmanifest; do not overwrite userV7seededits withgenerator. Scopepatches byphase and keepcoherentcommits. Exportreports/PCM toqaoutsideGitunlessintentionallysanitized. No local/referenceaudio/credentials inartifacts.

For complete rollback, closeMax and create a SEPARATE worktree at fixedfed2b78 checkpoint; don't hardreset a dirtyworktree. `v7_enable=0` compares thisiteration'ssource/strategy only, safetytrimstillactive. Old top-leveladapters remainfor fullV6 A/B oneatatime. Bind andsaveworkingtones before switching; preservecurrentlocalstate separately.

## R2 delta and native checks that must not be skipped

- Four new profile parameters default to neutral0: order2/order3 −12..+3dB, speed mass0..+6dB, speed edge−6..0dB. Gains act at source partials / independent LF / continuous-bus shelf respectively. Speed blend60–140km/h, 0.8s smoothing; not gear-pitch remapping. Upper harmonics still use nativeDNA controls.
- Ferrari SF90 `sf_effort` now consumes the V7 audio envelope; its own layer envelopes remain cascaded. ICE negative load is not positive traction. Verify pedal onset/lift by actual captured audio, not just internal envelope taps.
- Drive strategy hysteresis changes no raw telemetry: drive0.16/0.08, brake0.06/0.02. No off-state shifts. All old source/strategy bypass gates preserved.
- IONIQ gen gets read-only outputs5/6 for actual renderRPM/root; outer powertrain wrapper still has4 audio outlets. Never route diagnostics into an audio summing bus or telemetry authority.
- `v7_meter.gendsp` has4 overlapping constant-peak bandpass RMS monitors60/170/300/3500Hz. Only continuousDNA+SC post-balance, not stem isolation/brickwall/acousticSPL. Max UI capture still required.
- Save primes verifier before native fanout. Eight owners require valid physicalslot1/name/number checks plus observedwrite notifications; no missing ACK is counted successful. Test the installedMax version's actual `write` outlet message including filename and successflag. Unknown/no notification must remain unconfirmed. Rapid overlapping saves are not an atomic transaction and are not release-certified.
- Numeric schema revision2 accepts complete old18-param V7 documents with new4 default0; corrupted partial/wrong-range documents fall back to last valid physicalbackup before publishedbinding. Nativeowner backup recovery has NOT been generalized. File name and pattrstorage identity are checked by bindingCLI. Never call completeJSON or VM tests native save acceptance.

R2 first rollback target is e979b0c on a separate worktree; older V6 remains a separate fullsound A/B. Final commit is the release manifest SHA. No main updates and no leftover temporary publishing files are allowed in final tree.
