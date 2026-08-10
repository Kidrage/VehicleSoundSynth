# VehicleSoundSynth V3

Max/MSP 8.6.5 vehicle-acoustics project with an EV profile plus lifecycle-gated
V12 and V10 combustion profiles. V3 uses crank-related combustion pulses,
additive harmonics, FM/AM sidebands and non-integer orders instead of a dominant
pure sine. Its in-cabin low-frequency system is excited by the real powertrain
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

The preset also sets four independent stem trims. If a dB field seems inactive,
confirm the matching stem is actually sounding: `Rumble Level` cannot change
Future EV because that preset intentionally sets the rumble stem to -60 dB.

Future EV does not require the combustion ignition/start lifecycle.

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

EQ messages act on the complete stereo mix immediately before output trim and
protection. Runtime probes measured approximately -6.1 dB at 90 Hz for a
-12 dB low shelf, -12.0 dB at the centers of the 250 Hz and 3.8 kHz peak bands,
and -5.9 dB at 9 kHz for a -12 dB high shelf. `eq_bypass 1` crossfades to the
unprocessed signal; `master_trim_db` affects every stem.

## Audio sources and noise

The continuous EV/V12/V10 engines remain procedural. Runtime event samples and
the cabin IR are processed CC0 field recordings, not generated Foley. See
`ASSET_LICENSES.md` and `assets/asset_manifest.json` for provenance, crops,
normalization targets, and hashes.

Broadband noise is deliberately limited to a centered `pink~` tire bed
(70-900 Hz), a restrained stereo `noise~` wind layer (400-4000 Hz), and very
low-level smoothed mechanical texture inside the fuel generators. Reduce it
with `Road Level`, `Brightness`, `Texture`, the High-Mid/High Shelf EQ, or by
lowering `road_air~` in the mix; do not use the limiter as an EQ.

## Regeneration and validation

Generated `.maxpat`, `.gendsp`, preset, and media files are owned by
`tools/build_project.py` and should not be hand-edited.

```sh
python3 tools/build_project.py --output-root .
python3 -m unittest discover -s tests -v
python3 tools/audio_metrics.py render.wav --max-peak-dbfs -1 --min-rms-dbfs -45 --min-rumble-ratio 0.55 --max-subsonic-ratio 0.05 --max-low-side-ratio 0.10 --max-high-ratio 0.10
```

The rumble layer is high-passed near 28 Hz. Cabin side energy is narrowed before
the IR and again after IR wet/dry mixing; the final side path uses four 180 Hz
high-pass stages so deep bass stays centered. The full signal then ends
in `mix_master~`: four serial stereo EQ bands, click-safe dry/wet bypass,
master trim, `omx.peaklim~`, and `clip~ -0.891 0.891`.
