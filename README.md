# VehicleSoundSynth V4

Max/MSP 8.6.5 vehicle-acoustics project derived as an independent V4 archive from V3. V4 adds an EV profile plus lifecycle-gated
V12 and V10 combustion profiles. V4 uses crank-related combustion events,
bounded per-ignition timing/energy variation, three stable low/mid orders, and a
normalized six-anchor stereo residual bank instead of periodic AM, a dominant
pure sine, or a saw-like high-order stack. The EV low fundamental is
phase-coherent between channels and feeds
an EV-only, dual-channel BEAP pad. Its in-cabin low-frequency system is excited by the real powertrain
signal and adds engine half-order structure vibration, damped cabin/body modes,
and load-dependent exhaust boom. The seven-speed DCT, licensed CC0 transients,
short cabin IR, and final four-band stereo EQ complete the path.

Open `VehicleSoundSynth-V4.maxproj` first, wait for its Project window to load,
then open `main.maxpat` from that same Max instance. Audio starts muted.

完整中文操作说明见
[`VehicleSoundSynthV4_完整使用手册.docx`](VehicleSoundSynthV4_完整使用手册.docx)。
V4 目录保留旧手册作为参考，V3 原目录未被覆盖。

## Quick start

1. Lower monitoring level and open `VehicleSoundSynth-V4.maxproj`.
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
tuned in isolation. Below 120 Hz the two Pad outputs are folded to one centered
Mid signal; above 120 Hz an 82/18 crossmix keeps useful stereo width without the
previous near-antiphase mono loss.

V4 uses RPM-adaptive three-band cabin stereo: below 120 Hz is strict mono,
120–2000 Hz preserves a fold-safe Mid/Side field, and above 2 kHz keeps bounded
mechanical space and short asymmetric reflections. High RPM no longer collapses
the mid band toward mono.

The V12/V10 profiles are hybrid sound-design archetypes built from four-stroke
firing events, load envelopes, bounded harmonics, and real residual texture;
they are not measurement-matched replicas of a specific production vehicle.

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
`master_trim_db` affects every stem. The filtergraph power-gain parameter is
converted with `10^(dB/10)`, so a requested EQ change in dB matches the measured
center-frequency change instead of producing half the requested amount.

## Audio sources and noise

The EV motor remains procedural. V10/V12 are hybrid: phase-locked cylinder-bank synthesis
supplies firing order and load response, while twelve normalized stereo residual
loops from a CC0 Ferrari acceleration recording supply irregular intake,
mechanical, and exhaust texture. Runtime events and the cabin IR are also
processed CC0 field recordings, not generated Foley. See
`ASSET_LICENSES.md` and `assets/asset_manifest.json` for provenance, crops,
normalization targets, and hashes.

Broadband noise is deliberately limited to a centered `pink~` tire bed
(70-900 Hz) and a restrained stereo `noise~` wind layer (400-4000 Hz). The
V10/V12 generators no longer inject white noise. Reduce remaining road/air noise
with `Road Level`, `Brightness`, `Texture`, the High-Mid/High Shelf EQ, or by
lowering `road_air~` in the mix; do not use the limiter as an EQ.

## Engine texture bank and local Ferrari target

Rebuild the distributable CC0 residual bank with:

```sh
python3 tools/prepare_engine_texture.py assets/raw/biholao_370278_ferrari_acceleration.wav media --metadata assets/engine_texture_bank.json
```

The bank contains six firing-frequency anchors (65–520 Hz), each with two
asynchronous stereo loops longer than four seconds. The processor removes DC and
dominant cadence, stabilizes slow source-level rides, adds mono-compatible
upper-band Side microstructure, closes each loop with a 250 ms cyclic seam ease,
and normalizes every output to -18 dBFS RMS. Runtime pitch ratios are clamped to 0.9–1.1 and adjacent anchors
crossfade continuously. V10/V12 enable this bank; EV gates it off.

The user-supplied `/Users/saintpeter/Desktop/Ferrari.wav` remains local-only and
is used only as an acoustic comparison target. It is never loaded, committed,
synced, or redistributed. Its measured non-audio targets are stored in
`assets/ferrari_sf90_acoustic_target.json`.

## Regeneration and validation

Generated `.maxpat`, `.gendsp`, preset, and media files are owned by
`tools/build_project.py` and should not be hand-edited. The exception is
`patchers/ev_pad_beap~.maxpat`, which is seeded only when absent and is the
supported place for user Pad tuning.

```sh
python3 tools/build_project.py --output-root .
python3 -m unittest discover -s tests -v
python3 tools/audio_metrics.py steady_render.wav --max-harsh-ratio 0.03 --max-high-ratio 0.001 --min-low-mid-ratio 0.85 --min-rumble-ratio 0.80 --max-clipped-sample-ratio 0
python3 tools/audio_metrics.py start_render.wav --max-harsh-ratio 0.35 --max-high-ratio 0.03 --max-clipped-sample-ratio 0
python3 tools/audio_metrics.py high_rpm.wav --compare-wav ferrari_window.wav --min-third-octave-similarity-left 0.85 --min-third-octave-similarity-right 0.85 --min-third-octave-similarity 0.87 --max-third-octave-similarity-lr-delta 0.05
python3 tools/audio_metrics.py eq_cut.wav --compare-wav eq_flat.wav --expected-gain-db -12 --gain-tolerance-db 0.25
```

For the steady-state gate, trim the first second so the starter transient is not
measured as continuous combustion. The separate start gate keeps that transient
audible while preventing it from becoming a high-frequency fault burst.

The rumble layer is high-passed near 28 Hz. After the cabin IR, `cross~ 120`
centers deep bass while asymmetric short all-pass/early-reflection paths widen
only the upper body and mechanical detail. The mid band uses a 0.24 Side safety
trim; the high band uses 0.26 plus 0.04 cross-reflections. This keeps the default
fold-down near the target without removing stereo phase detail.
The full signal then ends
in `mix_master~`: one visible four-node graph driving stereo `cascade~`, click-safe dry/wet bypass,
master trim, `omx.peaklim~`, and `clip~ -0.891 0.891`.
