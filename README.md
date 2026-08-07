# VehicleSoundSynth V2

Max/MSP 8.6.5 vehicle-acoustics project with an EV profile plus lifecycle-gated
V12 and V10 combustion profiles. V2 adds ignition/start/idle behavior, a
profile-aware seven-speed DCT, causal shift and backfire events, quieter road
noise, and a final four-band stereo EQ.

Open `VehicleSoundSynth-V2.maxproj` first, wait for its Project window to load,
then open `main.maxpat` from that same Max instance. Audio starts muted.

完整中文操作说明见
[`VehicleSoundSynthV2_完整使用手册.docx`](VehicleSoundSynthV2_完整使用手册.docx)。
V2 目录内保留的 `VehicleSoundSynth_完整使用手册.docx` 是 V1 参考文档。

## Quick start

1. Lower monitoring level and open `VehicleSoundSynth-V2.maxproj`.
2. Open `main.maxpat` from the loaded project.
3. Select `High-Rev V12` or `Aggressive V10`.
4. Enable `Ignition`, click `Engine Start`, and confirm idle reaches the meters.
5. Enable `Audio`; use `Internal Auto` to audition the seven-speed DCT.

Future EV does not require the combustion ignition/start lifecycle.

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
python3 tools/audio_metrics.py render.wav --max-peak-dbfs -1 --min-rms-dbfs -60 --max-high-ratio 0.20
```

The signal ends in `mix_master~`: four serial stereo EQ bands, click-safe
dry/wet bypass, master trim, `omx.peaklim~`, and `clip~ -0.891 0.891`.
