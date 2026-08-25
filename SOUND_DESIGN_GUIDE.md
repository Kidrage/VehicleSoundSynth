# V5 Sound Design Guide

This guide separates the files that are safe to tune by ear from the generated
routing that should normally be left alone.

## Open the editable modules

Open a runtime and use the two buttons beside the Soundscape controls:

- `Open Sound DNA` opens the active profile's procedural engine panel.
- `Open Soundscape BEAP` opens the shared cinematic pad graph.

The visible four-node EQ embedded at the bottom of each engine window is the
same shared `patchers/vehicle_bus_eq~.maxpat` module. Save the patcher itself
after changing its layout or objects. Use its `Save EQ` button to save band
values for the next launch.

## Human-maintained sound-design modules

| Module | Purpose | Persistence |
|---|---|---|
| `patchers/ev_sound_dna~.maxpat` | EV motor, inverter, gear and stereo character | Patcher is seed-once; `Save DNA` writes ignored local values |
| `patchers/v10_sound_dna~.maxpat` | V10 combustion, intake, exhaust and residual character | Same |
| `patchers/v12_sound_dna~.maxpat` | V12 bank, air and smooth high-rev character | Same |
| `patchers/vehicle_bus_eq~.maxpat` | Shared four-band output tone shaping | Patcher is seed-once; `Save EQ` writes one ignored shared state |
| `patchers/cinematic_soundscape_beap~.maxpat` | Shared cinematic pad | Seed-once; save the Max patcher after BEAP edits |
| `patchers/engine_start_beap~.maxpat` | Cinematic start effect | Seed-once |
| `patchers/v10_backfire_beap~.maxpat`, `v12_backfire_beap~.maxpat` | Physical pressure-release voices | Seed-once |

`patchers/{profile}_powertrain~.maxpat`, the matching `gen/*.gendsp`, the
Soundscape hosts, cabin, road, transient and `mix_master~` are generated bridge
or safety modules. Edit `tools/build_project.py` and regenerate when those
interfaces must change; do not tune their generated JSON directly.

## Sound DNA controls

RPM is the only master pitch/cadence input. Throttle does not directly tune an
oscillator: the drivetrain first integrates vehicle speed and RPM, while the
DNA applies only a bounded 0–8 dB torque-loudness contour. The default is
4.5 dB, so pedal motion can no longer hide RPM motion behind a large volume jump.

Common controls:

- `Aggression`: relative upper-order emphasis.
- `Brightness`: core harmonic balance; start here before using output EQ.
- `Body`: crankcase/sub/body energy and idle weight.
- `Texture`: non-integer orders and fine residual detail.
- `Air Detail`: high-order intake/electrical air. Raise slowly; excessive values
  recreate the brittle plastic edge.
- `Cycle Irregularity`: bounded cycle-to-cycle movement. Too little is sterile;
  too much sounds unstable.
- `Stereo / Bank Separation`: independent mid/high bank or inverter detail.
  Bass below 120 Hz is still centred later by the cabin module.
- `Throttle Loudness Depth dB`: fixed-RPM pedal level range. Keep roughly
  3.5–5.5 dB for a physical result.
- `Saturation`: Gen soft drive before the safety compressor. Keep below 0.5
  while judging high-frequency detail.

EV adds `Torque Ripple`, `Gear Mesh`, and `Electrical Detail`. V10/V12 add
`Combustion Pulse`, `Intake Detail`, `Exhaust Detail`, and `Residual Detail`.
`Save DNA`, `Reload DNA`, and `Reset DNA` operate per profile in
`presets/local/{profile}_sound_dna.json`; those local files are intentionally
ignored by Git.

The previous plastic quality mainly came from phase-locked sine orders, a large
throttle-to-level range, shared left/right resonances, and saturation plus final
compression masking small dynamics. V5 keeps the stable firing cadence but adds
different left/right non-integer orders, independent bank/intake/exhaust paths,
bounded air layers and adjustable irregularity. Continuous V10/V12 audio still
does not read Ferrari samples.

## Vehicle bus EQ

The editable EQ is now separate from `mix_master~`, which contains only the
compressor, makeup, limiter and final -1 dBFS ceiling. Its four bands are:

- low shelf: 30–400 Hz, default 90 Hz;
- low-mid peak: 120–1200 Hz, default 250 Hz;
- high-mid peak: 1–8 kHz, default 3.8 kHz;
- high shelf: 4–16 kHz, default 9 kHz.

For dull acceleration, first raise DNA `Air Detail` or `Intake Detail` by
0.05–0.15. Then try +1 to +2 dB around 3–5 kHz and no more than about +1.5 dB
at 9–11 kHz. If the result turns plastic, reduce `Saturation`, `Texture`, or the
3–5 kHz EQ before cutting the whole high band. `Save EQ` writes
`presets/local/vehicle_bus_eq.json`, shared by EV, V10 and V12.

## Cinematic Soundscape

The pad is a BEAP/MSP hybrid. The large named visual modules are the editable
sound design: two LFOs, three oscillators, Noise, Audio Mixer, Ladder, MMF,
ADSR, VCA, Chorus and Reverb. Small MSP objects only scale CV, blend stereo,
high-pass at 120 Hz and provide a safety clip.

The third oscillator supplies a fifth, the slow LFO adds long detune/formant
motion, and MMF adds a second colour stage after the Ladder. Use `Soundscape
Solo` while tuning, temporarily set the runtime Soundscape level near -8 dB,
then return it to a mix-safe value. Keep the 120 Hz high-pass so the pad does not
fight the centred vehicle body. The same BEAP core is shared by all profiles;
their hosts map RPM, throttle, load, acceleration, Motion and Space differently.

After tuning, save the BEAP patcher, turn Solo off, verify the final meters stay
below the ceiling, close every patcher window, and quit Max normally.
