# VehicleSoundSynth V6 Repository Guide

## Purpose

Max 8.6.5 vehicle-sound V6, forked from stable V4 tag `v4.0.0`, with five independent fixed-profile runtimes. V10
and V12 continuous audio are procedural; Ferrari.wav is a V10 lifecycle-analysis
target and may supply only the optional ignored realistic-start one-shot. EV,
V10 and V12 use independent Soundscape V5 running beds. IONIQ6N is a
separate fourth electric profile with one Sound DNA, three crossfaded N Sound
BEAP instruments, a ready activation voice and a mode-aware N-event bus.
Ferrari is a fifth, analysis-envelope-derived V10 acoustic interpretation with
independent realism-V2 Sound DNA, Soundscape V7 and unchanged procedural start.
All five Pop renderers share one licensed 240 ms sample (two idle-muted players);
its live graphs use fresh local-state namespaces and it has no
runtime reference-audio dependency and is not a physical SF90 engine claim.
The project also contains a
start-relative single-speed/seven-speed drivetrain, cabin rumble, licensed
events, short cabin IR, adjustable stereo compression, EQ, and peak protection.

## First Reads

- `AGENTS.md` — repository constraints and validation command.
- `PROJECT_HANDOFF.md` — current state and cross-agent notes.
- `README.md` — user-facing interface and message contract.
- `V6_USER_GUIDE.md` — current Chinese operating, tuning and persistence guide.
- `V6_RELEASE_HANDOFF.md` — 2026-09-10 accepted snapshot, release scope and QA limits.
- `tests/test_project.py` — structural acceptance contract.

## Layout

- `tools/build_project.py` — sole writer for patchers, Gen DSP, presets, and fallback WAVs.
- `tools/ice_dna_v2.py`, `tools/soundscape_bed.py`, `tools/noise_layer.py` — scoped
  generator recipes for running-only ICE DNA, independent body beds and Noise.
- `tools/process_assets.py` — deterministic curated-audio crop, resample, DC removal, fade, normalization, and hashing.
- `tools/prepare_engine_texture.py` — CC0 stereo residual filtering, envelope stabilization, Side decorrelation, cyclic seam closure, normalization, and hashing.
- `tools/prepare_local_reference.py` — builds the ignored Ferrari startup one-shot plus analysis-only legacy derivatives and hash manifests.
- `tools/analyze_reference_lifecycle.py` / `tools/validate_v10_lifecycle.py` — build the tracked 14-node target table and gate five synthesized roles plus the throttle-only full-drive render.
- `code/drive_model.js` — exact deterministic 20 ms EV/V10/V12/IONIQ6N/Ferrari drivetrain used by Max and Node regression traces.
- `code/manual_input.js` — ES5/Node-testable fixed LT-throttle/RT-brake
  normalization, smoothing, source exclusivity, and safe pedal-release state.
- `assets/asset_manifest.json` / `ASSET_LICENSES.md` — runtime-audio provenance authority.
- `main.maxpat` — sole shared operator console and DSP-free launcher. It owns
  profile selection plus common Audio, Ignition, input, Mix/EQ and Sound Design
  controls, but never instantiates an engine.
- `patchers/runtime_console.maxpat`, `drive_console.maxpat`,
  `mix_eq_console.maxpat`, and `sound_design_console.maxpat` — the four tabbed
  Main pages. Their messages are scoped to the selected profile.
- `VehicleSoundSynth-{EV,V10,V12,IONIQ6N,Ferrari}.maxpat` — thin profile adapters that
  expose only profile-specific modes and embed one shared runtime host.
- `patchers/profile_runtime_host_<profile>.maxpat` — five Max-safe literal
  bindings materialized from one common engine, drivetrain, input, mixer, EQ,
  output and feedback topology. They accept profile-scoped Main commands and
  retain the public `vss.<profile>.input` seam.
- `patchers/keyboard_drive_ws.maxpat` — focus-aware Manual-mode binary W/S
  pedals with forced release when leaving Manual. Its Max `gate` control is
  inlet 0 and key-state data is inlet 1.
- `patchers/manual_input.maxpat` — generated deep module that selects the
  keyboard adapter or Max's built-in macOS `gamepad` adapter and exposes only
  normalized throttle/brake to the existing drivetrain.
- `patchers/vehicle_engine_{ev,v10,v12,ioniq6n,ferrari}~.maxpat` — fixed public seams.
- `patchers/{ev,ioniq6n}_sound_dna~.maxpat` — seed-once,
  user-editable profile sound-design panels that own synthesis macros and wrap
  one generated powertrain.
- `patchers/{v10,v12}_sound_dna_v2~.maxpat` / `*_powertrain_v2~.maxpat` /
  `gen/*_powertrain_v2.gendsp` — current ICE DNA, original output through
  1200 RPM and running extension blended over 1200–3000 RPM. V1 files remain.
- `patchers/ferrari_sound_dna_v2~.maxpat` — current Ferrari seed-once Sound DNA;
  it wraps the generated `gen/ferrari_exciter_v2.gendsp` with editable BEAP
  body/cavity/mechanical bands and uses the `ferrari_realism_v2` local state.
- `patchers/{ev,ioniq6n}_powertrain~.maxpat` — generated profile DSP;
  `patchers/{v10,v12,ferrari}_powertrain~.maxpat` is retained for V1
  rollback while the current Ferrari V2 path is described above.
- `patchers/vehicle_bus_eq~.maxpat` — seed-once, user-editable four-band EQ
  topology with per-profile ignored state; `patchers/mix_master~.maxpat`
  contains generated safety dynamics only. `code/eq_feedback_reader.js` reads
  the selected profile's saved state back into Main without owning or rewriting
  the EQ patch.
- `patchers/module_mixer.maxpat` — generated seven-stem main-page balance UI;
  per-profile ignored state is resolved by `code/module_mixer_state_path.js`.
  Its Sound DNA fader is the only profile output-gain authority, including for
  IONIQ6N. Road Air is now Noise; `road_level_db` remains the message. Migration
  to `<namespace>_module_mixer_noise_v1.json` preserves other faders and sets
  Noise to -60 dB, exact silence.
- `patchers/vehicle_noise_<profile>~.maxpat` / `code/noise_control.js` /
  `code/noise_state.js` — optional independent RPM/load mechanics/intake and
  speed-driven tire/air. Component levels, Color, live BEAP ceiling, Solo,
  meters and versioned `<profile>_noise_v1` state. It does not depend on SC
  Enable; Solo sends on `vss.runtime.control.<profile>` to bypass drive gates.
- `patchers/{ev,v10,v12,ferrari}_cinematic_soundscape_host~.maxpat` — generated profile
  mapping, persistence and cancellable DSP suspension around a direct embedded
  instance of the shared runtime Soundscape; there is no detached voice wrapper.
- `patchers/{ev,v10,v12}_soundscape_v5_beap~.maxpat` /
  `gen/{ev,v10,v12}_soundscape_bed.gendsp` — current stateful body/cavity beds;
  old BEAP colour/space/output graph retained. Their V5 factory/local namespace
  imports compatible spatial/pitch controls from V4, not old source settings.
- `presets/{ev,v10,v12}_soundscape_v5_factory.json` — current tracked slot-99
  authorities, via `code/soundscape_bed_state.js`; prior factories remain.
- `patchers/ioniq6n_cinematic_soundscape_host~.maxpat` — fourth-profile host;
  crossfades Ignition/Evolution/Lightspeed over 150 ms and never accepts Sound
  DNA audio or DNA parameter messages.
- `assets/ferrari_sf90_v10_interpretation_targets.json` — sanitized numeric
  cadence/band/envelope target; contains no source path, audio, or derivative.
- `patchers/ferrari_soundscape_v5_beap~.maxpat` — preserved Ferrari rollback
  Soundscape designer with its own V5 state and factory authority.
- `patchers/ferrari_soundscape_v6_beap~.maxpat` — accepted rollback Ferrari
  designer: V5 synthesis/wet path plus a polarity-aligned, enveloped dry body
  return. `direct_body_db` is -60..0 dB (-60 = off), factory -9 dB; all other
  synthesis constants are unchanged. V6 state/factory names never overwrite V5.
- `patchers/ferrari_soundscape_v7_beap~.maxpat` — current V6 body plus only a
  two-return independent mechanical/air split. Never mute its shared pressure
  noise source. `code/ferrari_bed_state.js` migrates accepted V6 settings to V7
  with prefix changes only; V6 remains untouched.
- `patchers/ferrari_pop_v3~.maxpat` — current seed-once Ferrari Pop Designer,
  opened by the existing `open.ferrari.backfire` bus. Pitch (-6..3 st, next hit),
  Tone (1200..8000 Hz) and Level (-24..0 dB) are the only tone controls.
  One buffer and two `ferrari_pop_sample_voice~` instances play a 240 ms CC0 WAV;
  short fade-before-reuse and `thispoly~` mute bound voice cost. The unchanged
  burst scheduler still owns 1..5-hit counts/spacing. The Ferrari compatibility adapter
  retains physical event gates and explicit ignition-independent preview.
  Missing media fails silent with a Max file error; there is no synth fallback.
- `patchers/{ev,v10,v12,ioniq6n}_pop_v4~.maxpat` — profile-voiced instances of
  the same short-sample player, using `code/ferrari_pop_control.js` and
  `code/ferrari_pop_state.js` with profile arguments. V4 local state does not
  import old synthesis knobs. EV is preview-only; IONIQ mode/eShift and ICE
  event/burst conditions remain in their hosts. Never layer old Pop synthesis.
- `patchers/ferrari_sound_dna~.maxpat`,
  `patchers/ferrari_soundscape_v4_beap~.maxpat`, and
  `patchers/ferrari_{engine_start_v3,backfire_v2}_beap~.maxpat` — preserved
  seed-once rollback/start/event designers; the start stays procedural and the
  old Ferrari backfire is retained but no longer instantiated by the live host.
- `patchers/ioniq6n_soundscape_<mode>_bed_v2_beap~.maxpat` — current N modes;
  only the standalone speed/transient hiss return is disconnected. Accepted
  RPM-shaped native texture, tones, mode switching and FX are retained. The
  old `*_beap~` files remain; `code/ioniq6n_bed_state.js` migrates all old mode
  settings to `ioniq6n_soundscape_modes_v2` by prefix only. Designer actions
  now reach the live host storage.
- `patchers/ioniq6n_activation_beap~.maxpat` — unchanged ready activation;
  `ioniq6n_n_event_beap~.maxpat` is rollback-only, while the N-event host now
  gates the Pop V4 renderer.
- `patchers/cinematic_soundscape_v3_beap~.maxpat`, three profile-specific
  `*_engine_start_beap~` designers, three legacy EV pads, two legacy ICE pads,
  and two backfire graphs are seed-once user-tunable files. The legacy pads and
  old shared start files are preserved but undeclared.
- `patchers/`, `gen/`, `media/`, `presets/` — generated runtime resources.
- `tests/` — deterministic structural and resource checks.

## Commands

```sh
python3 tools/build_project.py --output-root .
python3 tools/process_assets.py --root .
python3 tools/prepare_engine_texture.py assets/raw/biholao_370278_ferrari_acceleration.wav media --metadata assets/engine_texture_bank.json
python3 tools/prepare_local_reference.py /Users/saintpeter/Desktop/Ferrari.wav media/local --bundle
python3 -m unittest discover -s tests -v
python3 tools/bind_drive_render.py v10_v10-lifecycle-drive_on_final.wav
python3 tools/validate_v10_lifecycle.py --drive-lifecycle-wav v10_v10-lifecycle-drive_on_final.wav idle=idle.wav acceleration=acceleration.wav loaded_hold=loaded.wav shift_recovery=shift.wav deceleration=deceleration.wav
```

Regenerate twice and compare hashes when generator determinism matters. Never
hand-edit generated `.maxpat`, `.gendsp`, or `.wav` files. The five current
Sound DNA panels (including Ferrari V2), bus EQ, and seed-once BEAP patchers
named above are explicit
user-owned exceptions. The project generator preserves those files after their
first seed. The project generator
never overwrites curated runtime WAVs already present in `media/`.

Current Pop tuning is Pitch / Tone / Level plus audition, Save, Reload and
Factory Reset. Ferrari retains `ferrari_pop_v3.json`; the other four use
`<profile>_pop_v4.json`. Main's Pop/Event fader remains the whole-stem balance.
Pressure/Crack/Decay controls in old BEAP files belong to rollback renderers.
For continuous-engine tuning, open the active Sound DNA instance and use DNA
Solo; EV Aggression and V10 Brightness are explicitly connected to Gen DSP,
while several other controls are RPM/load/throttle-state dependent.
Soundscape `Open Designer` addresses the active version named above, never a
detached editor. V5 bed controls are Body, Cavity, Contour, Load Response and
Release Mass; separate fast edge / slow mass envelopes follow load release.
ICE cadence stays RPM-owned; Pitch Follow/Transpose move modal placement, not
the physical clock. No DNA audio is accepted. Existing spatial processing is
preserved. The launcher uses
profile-scoped `vss.runtime.control.<profile>` and
`vss.runtime.feedback.<profile>` buses selected by `vss.runtime.select`, so
runtime-close overlap cannot edit the old profile. Legacy Soundscape feedback
is bridged inside the shared host; do not instantiate DSP or a second
Soundscape in the launcher.

Runtime smoke-check the generated project in Max 8.6.5 after structural tests.
On macOS, Max writes load diagnostics to
`~/Library/Application Support/Cycling '74/Max 8/Logs/Max.log`; treat
`invalid category`, `No such object`, `function ... not found`, and
`patchcord outlet out of range` as release-blocking.

## Runtime Design

- V4 is an independent full copy of V3 plus its saved documentation artifacts.
- Intended flow: fixed lifecycle/state controller → one powertrain plus transient/road/rumble
  layers → RPM-adaptive three-band cabin field (120 Hz/2 kHz crossovers) →
  visible four-node master EQ → one final
  limiter/clip stage.
- V10 uses phase-continuous raised-cosine firing pulses and bounded harmonic,
  intake, load, acceleration, and overrun terms calibrated against the Ferrari
  lifecycle target table. V12 remains an independent procedural model; neither
  continuous runtime loads Ferrari/atlas/idle loops.
- `tools/build_mix_probe.py` provides 48 kHz NonRealTime measured EQ/trim/bypass checks.
- `tools/build_runtime_probe.py` builds a self-contained, monitor-muted Max
  recording bundle under `/private/tmp` for five-profile checks. It derives live
  abstraction/poly dependencies, resolves nested resource paths into the bundle
  and initializes direct V10/V12 V2 idle/run controls. No user presets or
  continuous reference samples are copied. Use unique probe names and only one
  isolated probe instance at a time on macOS.
- Open the project first and launcher second in the same Max instance. Launcher
  selection writes/closes the prior top-level runtime before opening one unique
  replacement. In Internal Manual, choose Keyboard and focus the runtime for
  W/S, or choose Gamepad for fixed LT throttle / RT brake. Keyboard W is an
  immediate 1/0 pedal and S is a 0.85 brake with brake priority; Gamepad keeps
  both pedals analog and permits overlap. Both adapters feed only
  throttle/brake into the existing fixed-step drivetrain interface. The V6
  calibration adds 15--25% high-speed full-throttle reserve, a stronger service
  brake and a short lift-brake state for abrupt pedal release; gradual release
  preserves the established coast feel. EV and IONIQ6N with N e-Shift disabled
  remain speed-coupled. The ICE drive model emits one bounded
  `overrun 0..1` event for a sufficiently fast loaded lift-off; generated hosts
  translate that event through `code/backfire_burst.js` into 1--5 decaying hits
  at random 140--200 ms intervals. Test Pop uses the same burst, while shifts
  remain single-hit. Those events now trigger the shared short-sample Pop
  renderer; Pitch/Tone/Level replace old synthesis-layer controls. Use the
  runtime Backfire Solo + Test Pop controls for ignition-independent audition;
  normal events remain engine-state gated. Save
  user-tuned BEAP
  subpatchers, close every task-opened
  patcher, and quit Max after a smoke test.

## Current Mainline

See `.codex/MAINLINE.md` for historical stages. The current implementation adds
Noise separation, running-body SC beds, V10/V12 running-only DNA and a shared
short-sample Pop renderer; final acceptance is tracked in `PROJECT_HANDOFF.md`.

- Preserve Ferrari/IONIQ DNA, all starts, driving/input, existing spatial FX, EQ and dynamics.
- Keep older seed-once graphs and preset namespaces; never revive previously dead idle knobs through migration.
- Keep `main.maxpat` DSP-free and maintain one-runtime-at-a-time CPU behavior.
- Keep Keyboard and fixed semantic macOS gamepad pedals mutually exclusive,
  with immediate zero release on source or Manual-mode exit. Keyboard is a
  binary full-throttle adapter with 0.85 brake priority; Gamepad pedals remain
  independent continuous 0..1 values.
- Keep natural coast inside the shared 20 ms drive model: released low-speed
  settling is stronger than high-speed coasting, blends to the original powered
  drag by 0.08 throttle, and must not alter the public throttle/brake interface.
- Keep N e-Shift optional and preserve event conditions. EV must not gain automatic combustion events.
- Keep the five profile windows mode-only over one shared host topology; common Open/Solo belongs in Main.

## Repository State

- Active branch: `codex/v6-layering-dna-pad-pop`, from frozen `b609e8b`.
  The user accepted the sound and authorized publication of this feature branch
  on 2026-09-10. Do not merge or push main. Verify the remote SHA at delivery;
  the existence of a remote alone does not establish publication.
- Canonical remote: `git@github.com:Kidrage/VehicleSoundSynth.git`; use
  the approved feature branch for this task. Historical V3/V4
  repositories remain read-only archives, not competing mainlines.
- `media/local/` is ignored and must never be committed or mirrored; missing
  Ferrari layers intentionally fall back to the tracked CC0 paths.
- Avoid cache files such as `tests/__pycache__/`.
- Never edit sibling V1, V2, V3, or frozen V4 while implementing V6.
- Preserve/exclude the pre-existing Main diff and user documentation moves into
  `docx/`. Generate into a fresh temporary root and install only scoped outputs;
  never blanket-regenerate production over user-owned seeds.
