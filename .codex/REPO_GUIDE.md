# VehicleSoundSynth V5 Repository Guide

## Purpose

Max 8.6.5 vehicle-sound V5, forked from stable V4 tag `v4.0.0`, with three independent fixed-profile runtimes. V10
and V12 continuous audio are procedural; Ferrari.wav is a V10 lifecycle-analysis
target and may supply only the optional ignored realistic-start one-shot. All
three profiles share one suspendable, user-editable cinematic BEAP soundscape.
The project also contains a
start-relative single-speed/seven-speed drivetrain, cabin rumble, licensed
events, short cabin IR, adjustable stereo compression, EQ, and peak protection.

## First Reads

- `AGENTS.md` — repository constraints and validation command.
- `PROJECT_HANDOFF.md` — current state and cross-agent notes.
- `README.md` — user-facing interface and message contract.
- `tests/test_project.py` — structural acceptance contract.

## Layout

- `tools/build_project.py` — sole writer for patchers, Gen DSP, presets, and fallback WAVs.
- `tools/process_assets.py` — deterministic curated-audio crop, resample, DC removal, fade, normalization, and hashing.
- `tools/prepare_engine_texture.py` — CC0 stereo residual filtering, envelope stabilization, Side decorrelation, cyclic seam closure, normalization, and hashing.
- `tools/prepare_local_reference.py` — builds the ignored Ferrari startup one-shot plus analysis-only legacy derivatives and hash manifests.
- `tools/analyze_reference_lifecycle.py` / `tools/validate_v10_lifecycle.py` — build the tracked 14-node target table and gate five synthesized roles plus the throttle-only full-drive render.
- `code/drive_model.js` — exact deterministic 20 ms EV/V10/V12 drivetrain used by Max and Node regression traces.
- `code/manual_input.js` — ES5/Node-testable fixed LT-throttle/RT-brake
  normalization, smoothing, source exclusivity, and safe pedal-release state.
- `assets/asset_manifest.json` / `ASSET_LICENSES.md` — runtime-audio provenance authority.
- `main.maxpat` — DSP-free launcher; it must never instantiate an engine. Its
  Soundscape control is only a send/receive view of the selected runtime.
- `VehicleSoundSynth-{EV,V10,V12}.maxpat` — independent runnable UIs; the
  single `Audio + Output` toggle enables both DSP and the output ramp.
- `patchers/keyboard_drive_ws.maxpat` — focus-aware Manual-mode binary W/S
  pedals with forced release when leaving Manual. Its Max `gate` control is
  inlet 0 and key-state data is inlet 1.
- `patchers/manual_input.maxpat` — generated deep module that selects the
  keyboard adapter or Max's built-in macOS `gamepad` adapter and exposes only
  normalized throttle/brake to the existing drivetrain.
- `patchers/vehicle_engine_{ev,v10,v12}~.maxpat` — fixed public seams.
- `patchers/{ev,v10,v12}_sound_dna~.maxpat` — seed-once, user-editable profile
  sound-design panels that own synthesis macros and wrap one generated powertrain.
- `patchers/{ev,v10,v12}_powertrain~.maxpat` — exactly one Gen per profile.
- `patchers/vehicle_bus_eq~.maxpat` — seed-once, user-editable four-band EQ
  topology with per-profile ignored state; `patchers/mix_master~.maxpat`
  contains generated safety dynamics only.
- `patchers/module_mixer.maxpat` — generated seven-stem main-page balance UI;
  per-profile ignored state is resolved by `code/module_mixer_state_path.js`.
- `patchers/{ev,v10,v12}_cinematic_soundscape_host~.maxpat` — generated profile
  mapping, persistence and cancellable DSP suspension around a direct embedded
  instance of the shared runtime Soundscape; there is no detached voice wrapper.
- `presets/{ev,v10,v12}_soundscape_factory.json` — tracked profile-specific,
  complete 90-client Soundscape slot-99 authority. The state helper re-reads
  slot 99 after every local read; local Save deletes slot 99 before writing so
  ignored user files contain slot 1 only.
- `patchers/cinematic_soundscape_beap~.maxpat` plus the engine-start, three
  legacy EV, two legacy ICE-pad, and two backfire graphs — nine seed-once,
  user-tunable BEAP files. The legacy pads are preserved but undeclared.
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
hand-edit generated `.maxpat`, `.gendsp`, or `.wav` files. The three Sound DNA
panels, bus EQ, and nine seed-once BEAP patchers named above are explicit
user-owned exceptions. The project generator preserves those files after their
first seed. The project generator
never overwrites curated runtime WAVs already present in `media/`.

For V10/V12 Pop tuning, the top `AUTHORITATIVE POP CONTROLS` inside the
seed-once backfire patcher are the stable interface to the generated pressure
core. `Global Pitch`, Body/Crack Tune, Decay, layer levels, and nonzero Core
Presence all reach real audio through profile-local named buses. The visible
BEAP Pressure Mixer is optional colour; native BEAP MMF/AD/VCA response can be
subtle on short Max 8.6.5 gates and must not be treated as the audibility gate.
The shipped pressure-first defaults are Global Pitch -5/-6 semitones,
Low Pressure 1.0/1.0, Body 1.30/1.35, Crack 0.008/0.006 and Decay 0.75/0.62.
The generated host adds a 600/520 Hz air ceiling after subsonic protection. Use `Audition One
Hit` for repeatable timbre work, click `Save Pop` to persist the active controls
and BEAP state under ignored `presets/local/{profile}_pop.json`, then balance the whole result with the runtime
Module Mixer's `Pop / Event` fader.
For continuous-engine tuning, open the active Sound DNA instance and use DNA
Solo; EV Aggression and V10 Brightness are explicitly connected to Gen DSP,
while several other controls are RPM/load/throttle-state dependent.
Soundscape `Open Designer` addresses the active embedded instance; `Save`
persists profile-local state for the shared seed-once graph. The visible three
oscillator Offsets own the chord; EV/V10/V12 use separate tracked factory
voicings with no hidden interval adders. `Pitch Follow = 1` restores the exact
legacy full-travel RPM laws (`55+.032*rpm`, `36.7+.014*rpm`, and
`32.7+.012*rpm`) with 90 ms smoothing. Restrained sub-0.05 Hz LFO drift is
owned separately by Motion and scaled smoothly by throttle. The launcher uses
profile-scoped `vss.runtime.control.<profile>` and
`vss.soundscape.feedback.<profile>` buses selected by `vss.runtime.select`, so
runtime-close overlap cannot edit the old profile; do not instantiate DSP or a
second Soundscape in the launcher.

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
  recording bundle under `/private/tmp` for objective V12/V10 checks. Use unique
  probe names and only one isolated probe instance at a time on macOS.
- Open the project first and launcher second in the same Max instance. Launcher
  selection writes/closes the prior top-level runtime before opening one unique
  replacement. In Internal Manual, choose Keyboard and focus the runtime for
  W/S, or choose Gamepad for fixed LT throttle / RT brake. Keyboard W is an
  immediate 1/0 pedal and S is a 0.65 brake with brake priority; Gamepad keeps
  both pedals analog and permits overlap. Both adapters feed only
  throttle/brake into the existing fixed-step drivetrain interface;
  its 20 ms RPM/shift integration remains unchanged while V5 uses a gentler,
  progressive service-brake law. The ICE drive model emits one bounded
  `overrun 0..1` event for a sufficiently fast loaded lift-off; generated hosts
  translate that event through `code/backfire_burst.js` into 1--5 decaying hits
  at random 140--200 ms intervals. Test Pop uses the same burst, while shifts
  remain single-hit. Those events excite the seed-once BEAP backfire voices and
  their pressure/crack/reflection core. The editable voice has
  labelled Pressure Body, Exhaust Crack, and Tail Color/Output sections;
  intensity morphs layer colour and tail density, not only gain. Use the
  runtime Backfire Solo + Test Pop controls for ignition-independent audition;
  normal events remain engine-state gated. Save
  user-tuned BEAP
  subpatchers, close every task-opened
  patcher, and quit Max after a smoke test.

## V5 Mainline

- Remove runtime shift/pop/crackle sample playback; keep only licensed starter one-shots.
- Deepen EV/V10/V12 idle and acceleration realism without discontinuous pitch or plastic high-frequency oscillators.
- Add physically triggered, seed-once BEAP backfire voices for V10/V12.
- Add one shared, top-level-controlled, seed-once cinematic BEAP Soundscape for EV/V10/V12.
- Persist one shared vehicle-bus four-band EQ across all three runtimes with safe default fallback.
- Keep `main.maxpat` DSP-free and maintain one-runtime-at-a-time CPU behavior.
- Keep Keyboard and fixed semantic macOS gamepad pedals mutually exclusive,
  with immediate zero release on source or Manual-mode exit. Keyboard is a
  binary full-throttle adapter with 0.65 brake priority; Gamepad pedals remain
  independent continuous 0..1 values.
- Keep natural coast inside the shared 20 ms drive model: released low-speed
  settling is stronger than high-speed coasting, blends to the original powered
  drag by 0.08 throttle, and must not alter the public throttle/brake interface.

## Repository State

- Canonical branch: `main`; it contains the complete V5 history and is based on
  the frozen V4 stable tag `v4.0.0` at `6aa49d0`.
- Canonical remote: `git@github.com:Kidrage/VehicleSoundSynth.git`; use
  `origin/main` as the only operator/development entry point. Historical V3/V4
  repositories remain read-only archives, not competing mainlines.
- `media/local/` is ignored and must never be committed or mirrored; missing
  Ferrari layers intentionally fall back to the tracked CC0 paths.
- Avoid cache files such as `tests/__pycache__/`.
- Never edit sibling V1, V2, V3, or frozen V4 while implementing V5.
