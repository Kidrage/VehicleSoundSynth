# VehicleSoundSynth

A compact Max/MSP vehicle-acoustics prototype with three morphable sound identities:
Future EV, High-Rev V12, and Aggressive V10.

The project targets Max 8.6.5 and uses only built-in Max/MSP/Gen objects. Open
`VehicleSoundSynth.maxproj`, then open `main.maxpat`. Audio is deliberately off
at startup; click the speaker icon when your output level is safe.

完整的中文操作、参数与拟真调音说明见
[`VehicleSoundSynth_完整使用手册.docx`](VehicleSoundSynth_完整使用手册.docx)。

## Controls

- **State source**: Internal uses the built-in drive model; External listens on
  `vss.input` for named Max messages.
- **Throttle / Brake / Auto Drive**: drive the internal state generator.
- **Preset**: selects one of the three archetypes.
- **EV / V12 / V10 weights**: continuously blend identities.
- **Aggression / Brightness / Body / Texture / Cabin Width**: sound-design macros.

External state messages accepted by the engine:

```text
speed_kph 0..300
rpm 0..10000
throttle 0..1
brake 0..1
load -1..1
accel -1..1
gear 0..6
shift 0|1
pop 0|1
click 0|1
```

Regenerate generated assets and run validation:

```sh
python3 tools/build_project.py
python3 -m unittest discover -s tests -v
```
