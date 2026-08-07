# VehicleSoundSynth V3

Max/MSP 8.6.5 vehicle-acoustics project with an EV profile plus lifecycle-gated
V12 and V10 combustion profiles. V3 adds a dedicated in-cabin low-frequency
system: engine half-order structure vibration, cabin/body resonances, and
load-dependent exhaust boom. The seven-speed DCT, causal transient system,
and final four-band stereo EQ remain intact.

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
5. Enable `Audio`; use `Internal Auto` to audition the seven-speed DCT.
6. Shape the cabin with `Cabin Rumble`, `Exhaust Boom`, and `Structure Vibration`.

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

## Regeneration and validation

Generated `.maxpat`, `.gendsp`, preset, and media files are owned by
`tools/build_project.py` and should not be hand-edited.

```sh
python3 tools/build_project.py --output-root .
python3 -m unittest discover -s tests -v
python3 tools/audio_metrics.py render.wav --max-peak-dbfs -1 --min-rms-dbfs -45 --min-rumble-ratio 0.55 --max-subsonic-ratio 0.05 --max-low-side-ratio 0.10 --max-high-ratio 0.10
```

The rumble layer is high-passed near 28 Hz and the cabin side channel is
high-passed near 120 Hz so deep bass stays centered. The full signal then ends
in `mix_master~`: four serial stereo EQ bands, click-safe dry/wet bypass,
master trim, `omx.peaklim~`, and `clip~ -0.891 0.891`.
