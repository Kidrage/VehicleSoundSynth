# VehicleSoundSynth V6

使用入口：[V6 中文使用说明](V6_USER_GUIDE.md)。
维护交接：[V6 发布交接](V6_RELEASE_HANDOFF.md)。
2026-09-10 用户认可当前声音，发布目标是 `codex/v6-layering-dna-pad-pop`，不是 `main`；本次发布不再调整音色。

Max/MSP 8.6.5 vehicle-sound project with five independent runtimes:

- `VehicleSoundSynth-EV.maxpat`
- `VehicleSoundSynth-V10.maxpat`
- `VehicleSoundSynth-V12.maxpat`
- `VehicleSoundSynth-IONIQ6N.maxpat`
- `VehicleSoundSynth-Ferrari.maxpat`

`main.maxpat` is the DSP-free launcher and the only common control surface. Its
three pages own Drive, Mix + EQ, and Sound Design for the selected runtime; it
does not contain an engine or keep inactive profiles running. Each profile
window is now a thin adapter containing only its profile-specific modes. All
five hosts are materialized from one shared runtime topology as
`patchers/profile_runtime_host_<profile>.maxpat`; they differ only in literal
profile binding required by Max, while drive, persistence, monitoring, output
and command/feedback structure stays identical.

## Quick start

Before opening Max, keep the project file inside a folder named
`VehicleSoundSynth-V6`; Max 8.6.5 uses that name to resolve the project search
paths reliably.

1. Open `VehicleSoundSynth-V6.maxproj` and wait for the Project window. Directly
   opening one of the five runtime `.maxpat` files is also supported: their
   root-level abstractions use explicit `patchers/` paths.
2. Open `main.maxpat`, then click one profile. On Main's `Drive / 驾驶` page,
   choose the input source and use `Ignition On`, `Start`, and `Audio On`.
   Audio always starts off; ignition/start alone never enable monitoring.
3. In the V10/V12 profile window, choose `Cinematic BEAP` or `Realistic Sample`.
   Start catch settles to 740 RPM for V10 and
   780 RPM for V12; it no longer enters a high-rev default after ignition.
4. In EV, choose Relax, Expressive, or Sport, then enable ignition/start when
   the selected BEAP layer should sound.
5. In IONIQ6N, select Ignition, Evolution, or Lightspeed. Evolution is the
   default. N e-Shift starts enabled with eight virtual ratios; disable it for
   continuous EV pitch without virtual shifts. Its Sound DNA, three
   Soundscapes and activation remain procedural and independent of V10;
   N events now use the shared short Pop sample with the original mode gates.
6. In Ferrari, startup, continuous V10 interpretation and Soundscape V7
   remain procedural; Pop uses one licensed 240 ms sample. This profile is analysis-informed rather than a
   claim to model the physical SF90 powertrain, and it has no runtime reference-audio dependency.
7. On Main's Drive page, use Internal Manual for direct throttle/brake control, Internal Auto for the
   guarded drive cycle, or send messages to `vss.ev.input`, `vss.v10.input`, or
   `vss.v12.input` in External mode. IONIQ6N uses `vss.ioniq6n.input`; Ferrari
   uses `vss.ferrari.input`.
8. After lowering the monitoring level, enable Main's single `Audio On`
   toggle. It opens the output ramp and Max DSP together; ignition/start alone
   intentionally do not enable monitoring.
9. On Main's Sound Design page use `Open Sound DNA` plus `Solo` to tune the
   procedural engine, or use Soundscape `Enable`, macros, `Open Designer` and
   `Solo`. In the V10/V12/Ferrari profile window use `Open Pop Designer`, Backfire
   Solo, and `Test Pop` to tune the
   active Pop voice without driving the car. These buttons open the audible
   instances; use the matching `Save` control, or `Save Profile Sound` for the
   Mixer, Soundscape and EQ together, after an edit. Main also exposes the shared
   Pop Open/Audition and Noise Open/Solo controls for all five profiles.
10. On Main's Mix + EQ page balance the seven audible modules: Sound DNA, Start,
   Pop/Event, Soundscape, Noise (机械·路噪), Cabin Rumble, and Master. Noise
   starts at -60 dB (exactly off): raise its fader before using its Solo or
   component controls. Each profile
   restores its own local mixer and four-band EQ state automatically. The DNA
   output fader lives here as the sole output-gain authority; it is not duplicated
   inside a Sound DNA designer.
11. Save intentional BEAP subpatcher edits. The launcher saves/closes the active
   top-level runtime when switching; when finished, close the runtime and Project
   windows and quit Max.

## Runtime design

Each public profile patcher has one message inlet and stereo signal outlets:

- `patchers/vehicle_engine_ev~.maxpat`
- `patchers/vehicle_engine_v10~.maxpat`
- `patchers/vehicle_engine_v12~.maxpat`
- `patchers/vehicle_engine_ioniq6n~.maxpat`
- `patchers/vehicle_engine_ferrari~.maxpat`

Each profile owns exactly one user-editable Sound DNA wrapper around one Gen powertrain. There are no runtime profile
weights and no hidden V10/V12/EV generators muted behind gain objects.

IONIQ6N is a fourth profile, not a V10 retune. Its procedural Sound DNA fills
the motor-order, low-mid body/cavity and mechanical-texture bands without
loading the supplied road-test recording. Its Soundscape is a separate stem
with three crossfaded, seed-once BEAP instruments: Ignition emphasizes
activation pressure and restrained bubbles, Evolution uses cinematic harmonic
motion plus dramatic transients, and Lightspeed adds velocity pressure and an
upper shimmer ceiling. RPM alone owns the tonal root; load/throttle reveal
layers and colour, while speed only increases air and space. Activation and
N-event buses are separately tunable, persistent and lifecycle-gated.

Ferrari is a fifth, separately persisted V10 acoustic interpretation derived
from analysis envelopes only. The live realism-V2 Sound DNA uses an exact
four-stroke `rpm/12`
cadence with independently tunable body (120--250 Hz), cavity (250--600 Hz),
mechanical (600--1200 Hz), presence (1.2--2 kHz) and edge (2--6 kHz) bands.
Its output uses a dedicated 1.35 kHz presence ceiling after band summing, so
high load keeps combustion texture without exposing a broad square-like edge.
Its Soundscape V7 keeps the accepted V6 pressure/body/cavity and dry-body return,
but disconnects the independent mechanical-halo and air returns. Noise used
inside the combustion-pressure exciter is deliberately retained. No reference
recording or continuous derivative is loaded. The short Pop sample is a licensed
CC0 exhaust event, not a Ferrari reference-recording derivative.

V10 and V12 continuous sound is procedural. No idle, acceleration, deceleration,
or shift-recovery recording is loaded or looped. Both engines use phase-locked
four-stroke cylinder banks, low-order body resonances, bounded combustion
residuals, and soft saturation instead of saw/square oscillators. V10 is tuned
against offline Ferrari lifecycle targets; V12 remains an independent, smoother
high-rev model. Their new DNA V2 keeps the original output at or below 1200 RPM
and smoothly introduces the running body/cavity/HF-softness path from 1200 to
3000 RPM. Running Body, Running Cavity, HF Softness and Release Mass expose the
new design without retuning the accepted idle.

EV/V10/V12 Soundscape V5 supplies an independent running low-mid bed: excitation
feeds body/cavity resonators, load changes contour and density, and fast edge /
slow mass envelopes separate pedal release from a simple volume fade. EV uses
rounded electromagnetic excitation; ICE beds use RPM-coherent pressure. The
existing BEAP colour filters, Chorus/Reverb and cabin processing remain in place.
Ferrari retains its accepted body design; IONIQ's V2 mode beds remove only the
standalone speed/transient hiss. IONIQ's already RPM-shaped native texture is
retained as part of its accepted high-load identity, not treated as constant hiss.

V6 adds visible per-profile `Open Sound DNA` panels, low-order crankcase/manifold motion to the ICE models and torque-ripple/
gear-mesh motion to the EV model. These remain phase-continuous and are driven by
RPM, load, acceleration and throttle; no saw/square oscillator or lifecycle loop
is used. The stronger idle signature is deliberately concentrated in the body
and rumble bands, while the existing RPM-adaptive low-pass still restrains the
plastic high-frequency edge.

All five Pop/Event renderers now share one 240 ms CC0 exhaust sample and at most
two idle-muted players, followed by Tone and Level. Only voicing differs by
profile. The existing ICE burst scheduler and physical conditions remain;
IONIQ keeps its mode/eShift event gates and EV does not gain automatic combustion
events. Legacy Pop synthesizers are retained for rollback, never layered with
the current player. Starts and DCT pitch/torque motion are unchanged.

Every runtime host owns one generated `patchers/module_mixer.maxpat`; Main's
Mix + EQ page is its remote control surface. It does not synthesize sound: it
converts the seven labelled values to the existing public dB messages. The six stem
faders cover Sound DNA, Start, Pop/Event, Soundscape, Noise and Cabin Rumble;
Master is the final bus trim. Values auto-save per profile under the ignored
`presets/local/` directory, so all five profiles keep independent balances.
Changing profile does not copy or merge saved values.

The signal path per runtime is:

```text
fixed drive/controller -> one editable profile Sound DNA -> one Gen powertrain
                       + optional shared Soundscape
                       + sample Pop/Event + independent mechanical/road Noise
                       -> powertrain-excited cabin/body
                       -> editable four-band stereo EQ
                       -> generated compressor -> limiter/clip -> output
```

See `SOUND_DESIGN_GUIDE.md` for the exact sound-design controls, the files that
are safe to edit, plastic-tone troubleshooting, EQ ranges, and the BEAP/MSP
division inside the cinematic Soundscape.

In `Internal Manual`, keep a Max patcher window focused. `W` is a binary pedal: key-down
sends full throttle (`1.0`) and key-up releases it (`0.0`). `S` applies a fixed
strong service-brake pedal (`0.85`) and has priority if both keys are
held; releasing `S` resumes `W` if it is still down. Keyboard pedals are
disabled, and both are released, when leaving Manual mode. These immediate
pedal commands still enter the same 20 ms physical integrator, so vehicle speed
and RPM cannot jump. EV is single-speed. V10 uses a faster DCT cut / RPM
sweep / clutch re-engagement, while V12 uses longer, smoother phases. Both keep
RPM continuous through a shift and produce one bounded torque dip rather than a
reset or threshold jump.

## Gamepad Manual Control

V6 keeps W/S and adds a fixed, deliberately small gamepad adapter in the
independent `patchers/manual_input.maxpat` subpatcher. It uses Max 8.6.5's
built-in [`gamepad`](https://docs.cycling74.com/max8/refpages/gamepad) object;
there is no external package, HID element learning, or device-specific axis
number.

1. Pair the controller in macOS Bluetooth settings, open one runtime, and set
   `Drive source` to `Internal Manual`.
2. In the large `MANUAL INPUT` panel choose `Input Source: Gamepad`.
3. LT/L2 is the accelerator and RT/R2 is the brake. Their physical travel is
   mapped directly to `throttle 0..1` and `brake 0..1`; half travel is about
   half pedal, rather than a per-frame accumulator.
4. Confirm `Detected`, the device name/type, `LT Throttle Raw/Norm`, and
   `RT Brake Raw/Norm` change. A 0.02 dead zone and 30 ms smoothing suppress
   Bluetooth jitter while retaining an immediate response.

Only the selected input source is active. Keyboard gives brake priority to `S`;
Gamepad keeps LT and RT as independent analog pedals, so partial accelerator and
brake overlap is possible. Changing the source, changing/disconnecting a
controller, or leaving `Internal Manual`
synchronously sends `throttle 0` and `brake 0`, so a held or lost trigger cannot
leave the drivetrain accelerating. The gamepad adapter changes pedal inputs
only: the unchanged 20 ms drivetrain still integrates speed, drag, RPM, and
seven-speed DCT state.

With a gradual 1--2 second pedal release, V6 uses the shared progressive coast
law: low speed settles more decisively while highway speed retains noticeably
more inertia. A fast release from meaningful throttle adds a short engine-brake
impulse and faster ICE RPM drop; EV and IONIQ6N with e-Shift disabled remain
strictly speed-coupled. Full-throttle high-speed drive is roughly 15--25%
stronger than the V6 audio baseline. The public throttle/brake range remains
linear `0..1`.

For GameSir Nova 2 Lite, use the manufacturer's macOS-compatible
[`Wireless Controller`/DS4 Bluetooth mode](https://gamesir.com/pages/tutorials-how-to-connect-nova-2-lite)
when analog trigger travel is required. A `Pro Controller`/Switch-mode HID
descriptor may expose LT/RT as digital buttons; the panel raises `Analog
warning` in that case. The mapping remains based on the semantic
`axis_left_trigger` and `axis_right_trigger` events, never a guessed axis index.

## Engine start

V10/V12 expose:

```text
start_style cinematic
start_style realistic
```

`cinematic` is the default. Each profile owns a directly embedded, seed-once
V3 Start Designer: `ev_engine_start_v3_beap~`, `v10_engine_start_v3_beap~`, or
`v12_engine_start_v3_beap~`; Ferrari owns
`ferrari_engine_start_v3_beap~`. Their Activation/Crank Body, Catch Bloom, Metal, Air,
Tail and Level controls drive the audible instance and persist independently.
V10 catches into its 60--67 Hz firing cadence, V12 catches faster and more
smoothly, and EV uses a ready chime plus harmonic activation instead of a fake
crank. `realistic` remains the mutually exclusive ICE sample alternative; V10
selects the optional local processed Ferrari startup when available. The sample
and procedural starter are never layered.
Ferrari's start path exposes only its procedural option and never routes to
`buffer~` or `play~`; the short Pop renderer is the separate sample exception.

## User-editable BEAP patchers

These files are seeded only when absent and are not overwritten by project
regeneration:

- `patchers/{ev,v10,v12,ferrari}_engine_start_v3_beap~.maxpat` — independent current cinematic starts
- `patchers/{ev,v10,v12}_soundscape_v5_beap~.maxpat` — current independent running beds
- `patchers/ferrari_soundscape_v7_beap~.maxpat` — accepted body with separate hiss returns removed
- `patchers/ioniq6n_soundscape_{ignition,evolution,lightspeed}_bed_v2_beap~.maxpat` — accepted N modes with the standalone hiss return removed
- `patchers/ioniq6n_activation_beap~.maxpat` — unchanged procedural ready activation
- `patchers/{v10,v12}_sound_dna_v2~.maxpat` — current running-only DNA upgrades
- `patchers/vehicle_noise_{ev,v10,v12,ioniq6n,ferrari}~.maxpat` — independent Noise designers
- `patchers/{ev,v10,v12,ioniq6n}_pop_v4~.maxpat` / `patchers/ferrari_pop_v3~.maxpat` — current short-sample Pop designers
- `patchers/ev_pad_beap~.maxpat` — EV Relax
- `patchers/ev_expressive_beap~.maxpat` — EV Expressive
- `patchers/ev_sport_beap~.maxpat` — EV Sport
- `patchers/v10_pad_beap~.maxpat` / `patchers/v12_pad_beap~.maxpat` — cinematic ICE pads
- Older Soundscape, DNA and backfire files remain available for rollback; do not
  open them as though they were the active designer.

Sound DNA and Soundscape meet only at the engine stem sum; no DNA audio enters
the Soundscape. For V5 beds, tune Body → Cavity → Contour → Load Response /
Release Mass, then the BEAP filters. RPM owns periodic excitation; pedal/load
changes body and edge envelopes. ICE cadence stays tied to RPM: Pitch Follow
and Transpose move modal placement, not the physical engine clock. Bass below
120 Hz remains centred; existing spatial processing is upper-band only.

EV/V10/V12 use `<profile>_soundscape_v5_factory.json` and local
`<profile>_soundscape_v5.json`. Only compatible spatial/pitch controls migrate
from V4; old source settings cannot overwrite the new bed. Ferrari uses V7
files and migrates the accepted V6 state with only namespace changes.
`Factory Reset` targets the matching versioned authority; old files remain.
`Soundscape Enable`, dB, `Motion`, `Space`,
`Pitch Follow`, `Transpose`, `Brightness`, and `Solo` are exposed on every
runtime. `Open Designer` fronts the exact embedded instance feeding that
runtime—there is no detached editor or `poly~` copy. For EV, V10 and V12,
`Save` writes the active profile to its ignored versioned file under
`presets/local/`. All four have independent graph topologies, factory states
and local user states.

IONIQ6N instead persists all three mode graphs through
`presets/ioniq6n_soundscape_modes_v2_factory.json` and the ignored local
`presets/local/ioniq6n_soundscape_modes_v2.json`. All old mode/tone/FX settings
migrate by namespace only. Switching `n_sound_mode` uses a
150 ms crossfade; it never copies parameters between instruments. The separate
N-event renderer now uses the shared Pop V4 designer while retaining the host's gates.

Noise is independent of Soundscape Enable and starts off. Raise Main's Noise
fader, then use Noise Solo while running. Mechanical and Intake follow RPM /
load; Tire and Air follow road speed and are silent while parked. Component
levels are -60..0 dB, Color is 0..1; the visible BEAP ceiling is in the live path.
Use the Noise Designer's own Save/Reload/Factory Reset. Noise does not audition
with ignition off. `road_level_db` remains the compatible stem message.

## Public control messages

All fixed runtimes accept the common controls below. Do not send `engine_type`
or profile-weight messages to a fixed runtime.

```text
ignition 0|1
start 1
speed_kph 0..300
rpm 0..10000
throttle 0..1
brake 0..1
load -1..1
accel -1..1
gear 1..7
shift 0|1
shift_dir -1|1
overrun 0..1
intake_backfire 0|1
exhaust_pop 0|1
pop 0|1
click 0|1
cabin_rumble 0..1
exhaust_boom 0..1
structure_vibration 0..1
cabin_ir_mix 0..1
powertrain_level_db -60..6
start_level_db -60..6
transient_level_db -60..6
road_level_db -60..6
noise_open
noise_solo 0|1
noise_save
noise_reload
noise_reset
noise_mechanical_db -60..0
noise_intake_db -60..0
noise_tire_db -60..0
noise_air_db -60..0
noise_color 0..1
rumble_level_db -60..6
soundscape_enable 0|1
soundscape_level_db -60..6
soundscape_motion 0..1
soundscape_space 0..1
soundscape_pitch_follow 0..1
soundscape_transpose -12..12
soundscape_brightness 0..1
soundscape_open
soundscape_save
soundscape_reload
soundscape_reset
soundscape_solo 0|1
dna_solo 0|1
backfire_solo 0|1
reference_texture_level_db -60..6
reference_texture_mute 0|1
eq_low <frequency_hz> <gain_db>
eq_lowmid <frequency_hz> <gain_db> <q>
eq_highmid <frequency_hz> <gain_db> <q>
eq_high <frequency_hz> <gain_db>
eq_bypass 0|1
master_trim_db -24..0
compressor_threshold_db -36..0
compressor_ratio 1..50
compressor_attack_rate 0..150
compressor_release_rate 0..150
compressor_makeup_db -12..12
compressor_bypass 0|1
```

IONIQ6N additionally accepts:

```text
n_sound_mode ignition|evolution|lightspeed
eshift_enable 0|1
event_enable 0|1
event_intensity 0..1
event_open
event_save
event_reload
event_reset
event_audition
event_solo 0|1
```

OMX attack/release values are rates, not milliseconds: larger values are
faster. Defaults are -12 dB, 2:1, attack 85, release 35, and 0 dB makeup. The
peak limiter and -1 dBFS clip guard remain active after the compressor.

Legacy aliases remain accepted for saved controller mappings:

```text
ev_mode relax|expressive|sport
ev_soundscape_level_db -60..6
ev_soundscape_mute 0|1
pad_level_db -60..6
pad_mute 0|1
pad_solo 0|1
```

V10/V12 additionally accept `start_style cinematic|realistic`.
They also accept:

```text
backfire_enable 0|1
backfire_intensity 0..1
backfire_solo 0|1
backfire_test 1
```

The V10 defaults are more active and sharper; V12 defaults are rarer and
rounder. A physical lift-off event is armed only after at least 0.12 seconds of
loaded running above roughly 1600 RPM and throttle 0.35. Releasing at least 0.35
of pedal to 0.18 or below within 0.18 seconds produces a randomized 1--5 hit
pressure-release burst. Adjacent hits are 140--200 ms apart with small per-hit
pitch variation; slow release, low RPM, brake-only motion, EV, ignition-off,
and engine-off states do not trigger it. The internal `overrun 0..1` message
carries that event strength from the drivetrain to the backfire host.

Both ICE runtime pages expose Backfire enable/intensity, `Backfire Solo`,
`Test Pop`, and `Open Pop Designer`. For an isolated audition, enable Audio, turn on Backfire Solo,
and click Test Pop; it plays the same randomized burst and deliberately bypasses
ignition and running-state gates. Automatic lift-off/shift events still require
Backfire Enable, ignition and a running engine. Gear-shift events remain one hit.
Turn Solo off before normal driving.
`Backfire Intensity` scales event strength; Pitch and Tone now own the sample's
colour. It no longer opens layers of the legacy pressure synthesizer.

Use `Open Pop Designer` so edits target the active audible instance in the
supported one-runtime-at-a-time workflow. Opening two copies of the same profile
is a diagnostic-only case; their profile-local control buses intentionally move
both copies together. Current designers expose Pitch (-6..3 semitones, next
hit), Tone (1200..8000 Hz) and Level (-24..0 dB), plus audition and persistence.
Factory voicings are Ferrari 0 st / 4200 Hz / 0 dB; V10 -1 / 3800 / -3;
V12 -2 / 3200 / -3; EV +1 / 5000 / -3; IONIQ 0 / 4200 / -3.
Only two short players are available; inactive players mute, and shutdown or
profile deactivation cancels pending events/tails. Do not edit generated
`*_backfire_host~.maxpat` JSON.

Click `Save Pop` after tuning. Ferrari keeps
`presets/local/ferrari_pop_v3.json`; the other four write
`presets/local/<profile>_pop_v4.json`. Old Pop presets are not imported into
the new sample design. `Pop / Event` in Main remains the final whole-stem
balance; the designer Level is not a second replacement for that fader.
EV audition is explicit only; IONIQ keeps N-mode/eShift conditions. Old BEAP
Pop controls describe rollback files, not the current audible sample renderer.

Keyboard Manual uses binary pedals: W sends full `throttle 1` while held and S
sends the fixed service-brake command. The `keyboard_drive_ws` adapter owns the
key-state gates; `manual_input` only selects Keyboard versus Gamepad and forwards
normalized pedals into the existing 20 ms drive integration.

## Persistent module mixer

Main's `MODULE MIXER` is the single common balance surface. Move a fader in dB;
its value is sent immediately and written after a short debounce to
`presets/local/<profile>_module_mixer_noise_v1.json` (Ferrari uses prefix
`ferrari_realism_v2`). On first migration, the old mixer file is preserved and
all other faders retain their values; only Noise starts at -60 dB. The state
is profile-specific and ignored by Git. `Reload` restores the last saved values,
`Reset` returns to the shipped profile balance, and closing/switching a runtime
saves once more synchronously. Edit `tools/build_project.py` rather than the
generated `patchers/module_mixer.maxpat` if the mixer interface itself changes.

## Persistent profile sound

`Save Profile Sound` commits the active profile's Module Mixer, Soundscape and
four-band vehicle-bus EQ. Their ignored state files are respectively
the versioned mixer path above, the current versioned Soundscape path, and
`<profile>_vehicle_bus_eq.json` under `presets/local/`.
`Reload Profile Sound` recalls all three. Each panel also retains its own Save,
Reload and Reset controls. A legacy `presets/local/vehicle_bus_eq.json` is read
once as a migration fallback when a profile EQ file does not yet exist; the
next save writes the new profile-local path. Closing or switching a runtime
saves the active profile before the window closes.

## Offline Ferrari V10 lifecycle analysis

`/Users/saintpeter/Desktop/Ferrari.wav` is a user-supplied V10 acoustic
reference. Continuous engine audio never loads it or any derivative. Regenerate
the tracked, non-audio lifecycle target table with:

```sh
python3 tools/analyze_reference_lifecycle.py \
  /Users/saintpeter/Desktop/Ferrari.wav \
  assets/ferrari_v10_lifecycle_targets.json
```

The table covers 14 windows across startup catch, cold/warm idle, low/mid/full
acceleration attacks, loaded holds, shift recovery, and overrun/deceleration.
Each node records cadence and direction, level/crest, centroid/rolloff, low-mid,
rumble, harsh-band, and air-band ratios. These measurements constrain synthesis
and render QA without embedding the source recording. Gate actual synthesized
V10 role renders against those reference-derived envelopes with:

```sh
python3 tools/bind_drive_render.py v10_v10-lifecycle-drive_on_final.wav
python3 tools/validate_v10_lifecycle.py \
  --drive-lifecycle-wav v10_v10-lifecycle-drive_on_final.wav \
  idle=v10_v10-lifecycle-idle_on_final.wav \
  acceleration=v10_v10-lifecycle-acceleration_on_final.wav \
  loaded_hold=v10_v10-lifecycle-loaded-hold_on_final.wav \
  shift_recovery=v10_v10-lifecycle-shift-recovery_on_final.wav \
  deceleration=v10_v10-lifecycle-deceleration_on_final.wav
```

The production gate requires the target table's 48 kHz sample rate and rejects
clipping, weak low/mid body, insufficient rumble, excessive 2-6 kHz or >6 kHz
energy, excessive centroid/roll-off, out-of-envelope RMS/crest, missing shift
events, and wrong firing-cadence direction/range. The matching
`v10_v10-lifecycle-*.lifecycle.json` sidecars are generated by the five
`v10-lifecycle-*` runtime-probe scenarios. All five roles are mandatory unless
the explicitly diagnostic `--allow-partial-lifecycle` flag is used.
The additional 24 s `v10-lifecycle-drive` probe does not inject RPM, accel, or
shift messages: it sends ignition/start/auto only, renders the same Max chain,
and records a deterministic trace from the exact `code/drive_model.js` used by
the runtime. The gate verifies throttle-driven RPM growth, startup catch,
ordered automatic gears 2-7, paired shift events, bounded 20 ms RPM steps, and
brake/deceleration before accepting its audio metrics. The binding step records
the completed Max WAV hash, frame count, sample rate, and probe hash in the
sidecar; validation rejects a trace copied from another render.
`--allow-non-target-sample-rate` likewise exists only for CoreAudio diagnostics
when Max ignores a requested 48 kHz rate.

For the optional `Realistic Sample` startup choice only, build the ignored local
bundle with:

```sh
python3 tools/prepare_local_reference.py /Users/saintpeter/Desktop/Ferrari.wav media/local --bundle
```

The deterministic processor creates:

- a 1.2 s startup layer;
- legacy idle-body and 18 atlas loops retained for offline comparison only;
- `ferrari_v10_atlas.json`, containing source and processor hashes, cadence/RPM
  anchors, source ranges, loop metadata, levels, confidence, and derivative
  hashes.

Only the 1.2 s startup one-shot is reachable from a runtime, and only when
`start_style realistic` is chosen. `media/local/` is ignored by Git and must
never be committed, synced, or redistributed. A clean checkout uses the tracked
CC0 starter. V12 never loads a Ferrari-derived file.

Distributable audio provenance remains governed by `ASSET_LICENSES.md` and
`assets/asset_manifest.json`.

## Regeneration and validation

Generated `.maxpat`, `.gendsp`, preset, and fallback media are owned by
`tools/build_project.py`. The shared bus EQ, five Sound DNA panels, and the
seed-once BEAP patchers documented in `SOUND_DESIGN_GUIDE.md` are user-owned and
preserved by normal regeneration.

```sh
python3 tools/build_project.py --output-root .
python3 -m unittest discover -s tests -v
git diff --check
```

For objective WAV checks:

```sh
python3 tools/audio_metrics.py render.wav --require-sample-rate 48000 \
  --max-clipped-sample-ratio 0 --max-harsh-ratio 0.001
```

The metrics tool averages up to five evenly spaced Hann windows. A harsh
high-frequency defect appearing only after startup therefore cannot hide behind
the first analysis window.
