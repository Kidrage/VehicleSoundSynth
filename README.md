# VehicleSoundSynth V4

Max/MSP 8.6.5 vehicle-sound project with three independent runtimes:

- `VehicleSoundSynth-EV.maxpat`
- `VehicleSoundSynth-V10.maxpat`
- `VehicleSoundSynth-V12.maxpat`

`main.maxpat` is a DSP-free launcher. It does not contain the three engines and
does not keep inactive profiles running. Selecting another profile first sends
`write` and closes the active runtime, then opens one unique replacement; this
is the supported low-CPU workflow.

## Quick start

1. Open `VehicleSoundSynth-V4.maxproj` and wait for the Project window. Directly
   opening one of the three runtime `.maxpat` files is also supported: their
   root-level abstractions use explicit `patchers/` paths.
2. Open `main.maxpat` from the Project window, then click one profile. Audio
   starts off.
3. In V10/V12, choose `Cinematic BEAP` or `Realistic Sample`, click
   `ignition 1`, then `start 1`. Start catch settles to 740 RPM for V10 and
   780 RPM for V12; it no longer enters a high-rev default after ignition.
4. In EV, choose Relax, Expressive, or Sport, then enable ignition/start when
   the selected BEAP layer should sound.
5. Use Internal Manual for direct throttle/brake control, Internal Auto for the
   guarded drive cycle, or send messages to `vss.ev.input`, `vss.v10.input`, or
   `vss.v12.input` in External mode.
6. After lowering the monitoring level, enable the single `Audio + Output`
   toggle. It opens the output ramp and Max DSP together; ignition/start alone
   intentionally do not enable monitoring.
7. Save intentional BEAP subpatcher edits. The launcher saves/closes the active
   top-level runtime when switching; when finished, close the runtime and Project
   windows and quit Max.

## Runtime design

Each public profile patcher has one message inlet and stereo signal outlets:

- `patchers/vehicle_engine_ev~.maxpat`
- `patchers/vehicle_engine_v10~.maxpat`
- `patchers/vehicle_engine_v12~.maxpat`

Each profile owns exactly one Gen powertrain. There are no runtime profile
weights and no hidden V10/V12/EV generators muted behind gain objects.

V10 and V12 continuous sound is procedural. No idle, acceleration, deceleration,
or shift-recovery recording is loaded or looped. Both engines use phase-locked
four-stroke cylinder banks, low-order body resonances, bounded combustion
residuals, and soft saturation instead of saw/square oscillators. V10 is tuned
against offline Ferrari lifecycle targets; V12 remains an independent, smoother
high-rev model. EV combines a procedural motor with one
of three suspendable BEAP soundscapes. The motor remains the speed-tracking
fundamental; the BEAP layer uses the same continuous pitch law and is high-passed
at 320 Hz, so it behaves as a cinematic layer instead of cancelling or replacing
the motor body. Its default level is -9 dB.

The signal path per runtime is:

```text
fixed drive/controller -> one profile powertrain + transient + road
                       -> powertrain-excited cabin/body
                       -> four-band stereo EQ -> compressor -> limiter/clip -> output
```

In `Internal Manual`, focus the runtime window and hold `W` to ramp throttle
toward 1.0 or `S` to apply the brake. Releasing either key ramps that pedal back
to zero. Keyboard pedals are disabled, and both are released, when leaving
Manual mode. Throttle enters one 20 ms physical integrator and cannot change RPM
without elapsed vehicle time. EV is single-speed. V10 uses a faster DCT cut / RPM
sweep / clutch re-engagement, while V12 uses longer, smoother phases. Both keep
RPM continuous through a shift and produce one bounded torque dip rather than a
reset or threshold jump.

## Engine start

V10/V12 expose:

```text
start_style cinematic
start_style realistic
```

`cinematic` is the default and triggers the user-editable
`patchers/engine_start_beap~.maxpat`. Its `poly~` voice is suspended 1.2 seconds
after the event. `realistic` uses the tracked starter fallback; V10 selects the
local processed Ferrari startup when available. Local and fallback starters are
mutually exclusive, with a 20 ms selection ramp.

## User-editable BEAP patchers

These files are seeded only when absent and are not overwritten by project
regeneration:

- `patchers/engine_start_beap~.maxpat` — cinematic engine start
- `patchers/ev_pad_beap~.maxpat` — EV Relax
- `patchers/ev_expressive_beap~.maxpat` — EV Expressive
- `patchers/ev_sport_beap~.maxpat` — EV Sport

The EV host crossfades modes over 250 ms and then sends `mute 1 1` to inactive
`poly~` voices, so only the selected BEAP graph remains on DSP. Legacy
`pad_level_db` and `pad_mute` controls map to the same host controls, while
`pad_solo 1` really mutes the procedural motor core for BEAP-only editing.

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
intake_backfire 0|1
exhaust_pop 0|1
pop 0|1
click 0|1
cabin_rumble 0..1
exhaust_boom 0..1
structure_vibration 0..1
cabin_ir_mix 0..1
powertrain_level_db -60..6
transient_level_db -60..6
road_level_db -60..6
rumble_level_db -60..6
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

OMX attack/release values are rates, not milliseconds: larger values are
faster. Defaults are -12 dB, 2:1, attack 85, release 35, and 0 dB makeup. The
peak limiter and -1 dBFS clip guard remain active after the compressor.

EV additionally accepts:

```text
ev_mode relax|expressive|sport
ev_soundscape_level_db -60..6
ev_soundscape_mute 0|1
pad_level_db -60..6
pad_mute 0|1
pad_solo 0|1
```

V10/V12 additionally accept `start_style cinematic|realistic`.

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
`tools/build_project.py`. Only the four BEAP patchers listed above are
user-owned.

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
