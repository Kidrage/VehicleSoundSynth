# VehicleSoundSynth V3

Max/MSP 8.6.5 vehicle-acoustics project with an EV profile plus lifecycle-gated
V12 and V10 combustion profiles. V3 uses crank-related combustion pulses,
phase-locked left/right cylinder banks, additive harmonics, bounded cycle variation,
and pulse-gated narrowband residuals instead of a dominant pure sine or broadband
noise. The EV low fundamental is phase-coherent between channels and feeds
an EV-only, dual-channel BEAP pad. Its in-cabin low-frequency system is excited by the real powertrain
signal and adds engine half-order structure vibration, damped cabin/body modes,
and load-dependent exhaust boom. The seven-speed DCT, licensed CC0 transients,
short cabin IR, and final four-band stereo EQ complete the path.

Open `VehicleSoundSynth-V3.maxproj` first, wait for its Project window to load,
then open `main.maxpat` from that same Max instance. Audio starts muted.

完整中文操作说明见
[`VehicleSoundSynthV3_完整使用手册.docx`](VehicleSoundSynthV3_完整使用手册.docx)。
V3 目录同时保留 V1 与 V2 手册作为参考，不会覆盖旧版本。

## Quick start

1. Lower monitoring level and open `VehicleSoundSynth-V3.maxproj`.
2. Open `main.maxpat` from the loaded project.
3. Select `High-Rev V12` or `Aggressive V10`.
4. Enable `Ignition`, click `Engine Start`, and confirm idle reaches the meters.
5. In `Internal Manual`, hold `W` to ramp throttle to 1 over 2.5 s; release it
   to ramp throttle back to 0 over 1.4 s. Hold `S` for a fast 120 ms brake
   application and release it to remove the brake immediately. Key repeat is
   suppressed, and leaving Manual mode releases both controls.
6. Enable `Audio`; use `Internal Auto` to audition the seven-speed DCT.
7. Shape the cabin with `Cabin Rumble`, `Exhaust Boom`, and `Structure Vibration`.
8. Drag the four nodes in the visible master EQ immediately before the meters/DAC.

The preset also sets four independent stem trims. If a dB field seems inactive,
confirm the matching stem is actually sounding: `Rumble Level` cannot change
Future EV because that preset intentionally sets the rumble stem to -60 dB.

Future EV's base motor does not require the combustion ignition/start lifecycle.
Its BEAP pad is intentionally gated by Ignition, so enable Ignition when you
want to hear the pad layer; Engine Start remains specific to V12/V10.

## EV BEAP pad tuning

Open `patchers/ev_pad_beap~.maxpat` to edit the two independent signal chains.
Each side contains two BEAP oscillators, an Audio Mixer, Ladder filter, ADSR,
and VCA. RPM supplies common 1V/oct pitch CV, throttle opens the filters and
raises the VCA control level, and Ignition supplies the gate. The
default voices sit +12 and +19.0196 semitones above the EV fundamental. The
second interval is an exact 3:2 fifth rather than an equal-tempered near match,
and neither voice uses micro-detuning, so the former slow beating is not recreated.

Save this patcher normally after adjusting it. Project regeneration deliberately
preserves the file; all surrounding routing and level containment remain generated.

`EV Pad dB` is the Pad's independent stem level. `Pad Mute` silences only the
Pad, while `Pad Solo` silences only the EV motor so the two Pad chains can be
tuned in isolation. The post-BEAP 82/18 crossmix keeps the stereo width useful
without the previous near-antiphase mono loss.

The V12/V10 profiles are procedural sound-design archetypes built from
four-stroke firing orders, load envelopes, and resonant harmonic layers; they
are not measurement-matched replicas of a specific production vehicle.

## Public control messages

```text
engine_type ev|v12|v10
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
pad_level_db -60..6
pad_mute 0|1
pad_solo 0|1
reference_texture_level_db -60..6
reference_texture_mute 0|1
```

Global EQ and output controls:

```text
eq_low <frequency_hz> <gain_db>
eq_lowmid <frequency_hz> <gain_db> <q>
eq_highmid <frequency_hz> <gain_db> <q>
eq_high <frequency_hz> <gain_db>
eq_bypass 0|1
master_trim_db -24..0
```

EQ messages and graph edits control the same four-filter `filtergraph~`/
stereo-`cascade~` system immediately before output trim and protection.
Select node 0–3 beside the graph for synchronized frequency, gain, and Q/S
editing. `eq_bypass 1` crossfades to the unprocessed signal;
`master_trim_db` affects every stem.

## Audio sources and noise

The continuous EV/V12/V10 engines remain procedural. Runtime event samples and
the cabin IR are processed CC0 field recordings, not generated Foley. See
`ASSET_LICENSES.md` and `assets/asset_manifest.json` for provenance, crops,
normalization targets, and hashes.

Broadband noise is deliberately limited to a centered `pink~` tire bed
(70-900 Hz) and a restrained stereo `noise~` wind layer (400-4000 Hz). The
V10/V12 generators no longer inject white noise. Reduce remaining road/air noise
with `Road Level`, `Brightness`, `Texture`, the High-Mid/High Shelf EQ, or by
lowering `road_air~` in the mix; do not use the limiter as an EQ.

## Local Ferrari reference texture

The optional SF90 reference remains local and is never committed. Prepare it with:

```sh
python3 tools/prepare_local_reference.py /Users/saintpeter/Desktop/Ferrari.wav media/local/ferrari_sf90_residual.wav
```

The tool removes DC, high-passes at 90 Hz, notches the 61.5 Hz V8 cadence and
its harmonics, low-passes at 4 kHz, builds a 250 ms equal-power stereo loop,
and normalizes it to -18 dBFS RMS with a -3 dBFS peak ceiling. V10/V12 load it
quietly at -24 to -20 dB; EV gates it off. If the local file is absent, a
deterministic stereo residual prevents missing-buffer errors. Measured targets,
without copyrighted audio, are stored in `assets/ferrari_sf90_acoustic_target.json`.

## Regeneration and validation

Generated `.maxpat`, `.gendsp`, preset, and media files are owned by
`tools/build_project.py` and should not be hand-edited. The exception is
`patchers/ev_pad_beap~.maxpat`, which is seeded only when absent and is the
supported place for user Pad tuning.

```sh
python3 tools/build_project.py --output-root .
python3 -m unittest discover -s tests -v
python3 tools/audio_metrics.py render.wav --max-peak-dbfs -1 --min-rms-dbfs -45 --min-rumble-ratio 0.55 --max-subsonic-ratio 0.05 --max-low-side-ratio 0.10 --max-high-ratio 0.10
```

The rumble layer is high-passed near 28 Hz. After the cabin IR, `cross~ 120`
centers deep bass while asymmetric short all-pass/early-reflection paths widen
only the upper body and mechanical detail. The full signal then ends
in `mix_master~`: one visible four-node graph driving stereo `cascade~`, click-safe dry/wet bypass,
master trim, `omx.peaklim~`, and `clip~ -0.891 0.891`.
