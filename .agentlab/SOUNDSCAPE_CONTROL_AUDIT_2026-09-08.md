# Soundscape control repair and V10/V12 diagnosis

Base: `adca388` on `codex/v6-ferrari-realism-v2`.
Repair branch: `codex/v6-soundscape-control-repair`.

## Confirmed failure and minimal repair

Ferrari already mixes independent DNA and Soundscape stems additively. The
two `*~` pairs apply their own gains; neither multiplies one stem by the other.
The earlier proposed audio rewire was therefore rejected.

Main's sound-design commands were sent through the drive simulator, the
Internal/External source switch, and the live driving gate. Selecting an Idle,
Cruise, Load, Lift or High RPM audition context closes that gate. Enable, Solo,
Open, Save, Reload and Reset consequently stopped reaching the engine. External
drive selection similarly deselected the Internal command path. Module-mixer
level commands used a separate path and could still work, making the failure
look like inconsistent audio-layer behavior.

One selector-preserving router in the shared runtime-host generator now sends
Soundscape controls, DNA Solo and legacy Pad aliases directly to the existing
engine. The same fix is materialized into all five hosts. Pedals, lifecycle,
the drive source switch and held driving-state behavior retain their original
route. No public selector, sound algorithm, filter, envelope, gain default or
preset namespace changes.

The locally Max-saved Main had also replaced its project-qualified console name
with `runtime_console.maxpat`. This failed to resolve in an isolated project,
with bpatcher/patchcord errors. Only that property was regenerated from the
launcher authority; every other user-saved JSON property, including layout and
patchcord order, was preserved. The user's remaining Main changes are local and
excluded from the repair commit; the committed launcher already has the correct
qualified name.

## Actual Max evidence

The diagnostic copy opens Main and its real Ferrari adapter/runtime, drives the
actual Enable UI, and records separate DNA, Soundscape, Cabin Rumble and final
stereo taps in one eight-channel recording. Only diagnostic receivers/taps and
zero multipliers on hardware-output wires are added. The synthesizers are not
rebuilt into a substitute probe. Copied local presets are used; originals are
never written. Max 8.6.5 records at the driver's actual 44.1 kHz.

Left-channel RMS, dBFS; windows are relative to recording start:

| State/window | Before: DNA | After: DNA | Before: Soundscape | After: Soundscape |
| --- | ---: | ---: | ---: | ---: |
| Load, enabled, 1–3 s | -22.11 | -22.06 | -29.97 | -30.64 |
| Load, disabled, 8–10 s | -22.13 | -22.08 | -30.64 | -53.59 |
| Load, disabled after tail, 10–10.8 s | -21.97 | -22.21 | -31.73 | Digital silence |
| Load, re-enabled, 13–15 s | -22.06 | -22.14 | -30.27 | -30.39 |

Before repair, toggling Enable in Load never reached the engine. Returning to
Live restored delivery and attenuated Soundscape substantially. After repair,
the same held-context toggle reaches the engine and the stem reaches digital
silence after the existing tail/suspension interval. Tail duration is retained;
allow six seconds when judging the fully disabled state.

Noise and independently initialized oscillator phases mean different WAV hashes
alone do not establish audibility or regression safety. Compare isolated stems,
matched states, tail-settled windows and preserved graph/preset hashes instead.
The invalid first recording with an unresolved Main bpatcher is excluded.

An additional actual-UI Idle-context recording verifies the solo boundaries:
with DNA Solo selected, turning Soundscape off attenuates its raw stem from
-24.21 to -65.82 dBFS while raw DNA stays at -17.90/-17.88 dBFS. With Soundscape
Solo selected, DNA still exists at its raw tap but does not leak to the final
output: disabling Soundscape yields digital silence at the final output after
the tail. Save with Enable off, enable temporarily, and Reload returns the
isolated stem to its off state. The test restores and saves Enable on afterward.
All three valid recordings have zero clipped samples. These tests establish
control/stem separation, not a promise of perceptually identical random noise
across independently started sessions.

## Timbre boundaries and V10/V12 findings

DNA and Soundscape both intentionally contain low-mid body/cavity energy; Cabin
Rumble is a third independent source. Solo was also blocked in held contexts,
so a requested DNA-only audition could still contain those other sources. The
repair restores the control separation. Moving existing Ferrari body energy
between instruments would alter the accepted sound and was not attempted.

V10/V12 were inspected but not retuned. Their source supports these candidate
causes of the acceleration texture; they are not a newly measured listening
acceptance claim:

- V10's added idle structure fades to zero by 2390 RPM; V12's by 2580 RPM.
  The low component is further multiplied by `1-speedmix*0.50/0.55`, while
  full throttle reduces body weighting by 16%/14%. High-load tone therefore
  loses relative low-mid mass as it leaves the convincing idle range.
- High-frequency `bright_*` terms increase with RPM and throttle. Intake,
  exhaust and residual detail contain many fixed-ratio `cycle()` components,
  including non-integer orders and different left/right ratios. These can
  expose sustained synthetic whistles/sidebands instead of broad structural
  texture as the low-mid support recedes.
- There are already pressure pulses, cycle variation, acceleration/release
  terms and bounded `tanh` saturation. Calling the models "just square waves"
  or assuming clipping without measurements is inaccurate. Increasing noise,
  modulation or saturation blindly is not an approved remedy.
- A future tuning proposal should first compare level-matched DNA-only idle,
  fixed-RPM load sweeps and acceleration sweeps, then evaluate retained body
  support, upper-band balance and source texture independently. Ferrari/IONIQ
  use more explicitly separated body/cavity/mechanical shaping; their exact
  sound should not be copied into V10/V12 without separate approval.

## Preservation and regression checks

- Frozen committed tree plus actual local Main/presets are stored in the unified
  hidden Downloads backup directory, under `soundscape-audit-20260908.G6XDmc3y`.
  Archive SHA-256 values:
  `b3b523cc99932a70d45d94ad89a537dd2df1b525f475b65b4d3df03b4f9c32ef`
  and `11b9953b602ee25934ad2478ac3cfb83cabf303e21bdca019a251074e74974c0`.
- 182 tracked patcher/Gen/preset/media/JS resources, excluding the five changed
  control hosts, match the frozen base byte-for-byte. All original local presets
  match the archive. Main differs from the pre-task JSON only at its repaired
  console-name property.
- `python3 -B -m unittest tests.test_runtime_design_routing -v` reproduced 60
  failed profile/selector cases before the repair and passes afterward; pedals
  and lifecycle remain on the original drive path.
- `python3 -B -m unittest discover -s tests -v`: 207 tests pass.
- Two fresh full builds produce the same 158-file manifest. SHA-256 of the
  sorted `(relative_path, file_sha256)` manifest representation:
  `8de8fac1c0d819e5d4a70656c5d5ec5c6220bf9f6d7e8df008e4a6e29c2407af`.
  All five installed hosts match fresh generation. `git diff --check` passes.
- Reference media, local presets, diagnostic audio and Max recovery files are
  excluded from Git and from cross-agent synchronization.
- Final Max check opened Ferrari's actual V2 DNA and V5 Soundscape designers,
  exercised Factory Reset, and loaded EV/V10/V12/IONIQ6N with Audio Off. No new
  missing-object, Gen, patchcord/outlet or project-category error was reported.
  Known object-database read-only warnings and the optional local starter miss
  are environmental diagnostics. Test patchers were saved/closed and the task
  Max instance quit normally; only the pre-existing user PID 38515 remains.
