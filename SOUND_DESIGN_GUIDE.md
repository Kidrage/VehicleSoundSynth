# V5 Sound Design Guide

This guide separates the files that are safe to tune by ear from the generated
routing that should normally be left alone.

## Open the editable modules

Open a runtime and use the design controls beside the Soundscape section:

- `Open Sound DNA` opens the active profile's procedural engine panel.
- `Sound DNA Solo` removes Soundscape, transient, road and rumble stems while
  leaving the active procedural powertrain audible.
- Soundscape `Open Designer` fronts the exact cinematic pad instance feeding
  the active profile; it no longer opens a detached file or `poly~` copy.
- V10/V12 `Open Pop Designer` opens the active backfire voice in the supported
  one-runtime-at-a-time workflow, not a detached duplicate patcher. Two copies
  of one profile share its tuning bus and are not a supported tuning setup.

The visible four-node EQ embedded at the bottom of each engine window uses the
same `patchers/vehicle_bus_eq~.maxpat` design, but its values are stored per
profile. Save the patcher itself after changing its layout or objects. Use its
`Save EQ` button to save the active EV/V10/V12 values for the next launch.

## Human-maintained sound-design modules

| Module | Purpose | Persistence |
|---|---|---|
| `patchers/ev_sound_dna~.maxpat` | EV motor, inverter, gear and stereo character | Patcher is seed-once; `Save DNA` writes ignored local values |
| `patchers/v10_sound_dna~.maxpat` | V10 combustion, intake, exhaust and residual character | Same |
| `patchers/v12_sound_dna~.maxpat` | V12 bank, air and smooth high-rev character | Same |
| `patchers/vehicle_bus_eq~.maxpat` | Four-band output tone shaping | Patcher is seed-once; `Save EQ` writes ignored per-profile state |
| `patchers/cinematic_soundscape_beap~.maxpat` | Shared cinematic pad topology | Seed-once; the live host writes ignored per-profile state |
| `patchers/engine_start_beap~.maxpat` | Cinematic start effect | Seed-once |
| `patchers/v10_backfire_beap~.maxpat`, `v12_backfire_beap~.maxpat` | Physical pressure-release voices | Seed-once |

`patchers/module_mixer.maxpat` is generated routing/UI, not a synthesis patch.
Use its seven main-page faders to balance Sound DNA, Start, Pop/Event,
Soundscape, Road/Air, Cabin Rumble and Master. The values themselves are
human-owned per-profile state in ignored `presets/local/*_module_mixer.json`.

`patchers/{profile}_powertrain~.maxpat`, the matching `gen/*.gendsp`, the
Soundscape hosts, cabin, road, transient and `mix_master~` are generated bridge
or safety modules. Edit `tools/build_project.py` and regenerate when those
interfaces must change; do not tune their generated JSON directly.

## Backfire voice

The editable sound is in `patchers/v10_backfire_beap~.maxpat` and
`patchers/v12_backfire_beap~.maxpat`. The matching generated
`*_backfire_host~.maxpat` files are plumbing: they require ignition, a running
engine and Backfire Enable, scale event strength/intensity, consume the Pop
Designer controls, soft-saturate the combined voice, and route it into the
transient stem. Do not edit the generated host JSON.
`backfire_burst_scheduler.maxpat` is another generated bridge around
`code/backfire_burst.js`: a fast overrun or Test Pop becomes 1--5 decaying hits,
each 140--200 ms after the previous one, with an overall downward pitch contour
and small jitter. Shift and explicit physical events bypass the burst and remain
single hits.
The editable patch is split into labelled `PRESSURE BODY`, `EXHAUST CRACK`,
and `TAIL COLOR / OUTPUT` panels. The visible BEAP `Pressure_Mixer` feeds the
compatibility colour path. Its native MMF/AD/VCA branch can be very subtle or
silent under Max 8.6.5's short external gates, so it is not the authority for
the dominant Pop. The host also contains a `GENERATED PRESSURE CORE`:
a click creates smooth body/crack envelopes that excite broadband noise, not a
naked resonator, followed by two lower-level wall reflections. Its important
tone controls are now surfaced in the same Pop Designer, so the editable panel
is the sound-design authority instead of a colour-only side layer. This is why
turning an MMF or AD icon alone may still produce little change, while the
number controls at the top always affect the actual output.

The `HOST CORE CONTROLS` panel is the quickest complete tuning surface:

- `Global Pitch (semitones)` tunes both BEAP and Core. The shipped V10/V12
  defaults are `-5` / `-6`; move farther negative for an even lower boom. This
  is the main control when changing a BEAP oscillator alone appears not to move
  the dominant sound.
- `Core Presence` scales the guaranteed pressure core from `0.25` to `1.5`;
  `1` is unity. It deliberately has no zero/silent position.
- `Body Tune` and `Crack Tune` scale the Core resonant and crack bands without
  changing burst timing.
- `Decay Scale` lengthens or shortens both Core envelopes.
- `Low Pressure Level` controls the coherent low modes.
- `Core Body Level` and `Core Crack Level` set the two dominant Core layers.

The visible `Pressure_Mixer` is the dependable BEAP colour control. The native
`Pressure_Body`, `Pressure_AD`, `Exhaust_Crack`, and `Crack_AD` modules remain
available for experimentation but should not be used to judge whether the Pop
chain is working. Click `Save Pop` after tuning; the authoritative number values
and BEAP module state reload together from the ignored
`presets/local/{profile}_pop.json`. Factory values keep the first launch audible,
then the local saved slot wins after the complete graph has loaded. Closing the
runtime also saves the current Pop state.

The shipped balance deliberately favors a short kick-like pressure body:
V10/V12 Low Pressure are both `1.0`, Body Level `1.30` / `1.35`, Crack
Level only `0.008` / `0.006`, and Decay Scale `0.75` / `0.62`. A generated
600 / 520 Hz output air ceiling suppresses the former snare-like top without
removing the editable Crack layer. For tone work, set Global Pitch and the Core
Body/Crack balance first, then adjust Core Presence and the BEAP Pressure Mixer.
Raising Crack Tune or Crack Level moves back toward a short snare-like shell;
lowering them exposes more chamber boom. Treat native MMF/AD edits as optional
colour experiments. Audition low, default and high runtime Intensity.
Intensity morphs from a compact pressure
release through filtered crack to brighter colour and a second tail, rather
than merely scaling the same waveform. Use transient dB last for whole-stem
balance. Change `tools/build_project.py` only when the physical event, reflection
timing, host plumbing, compatibility layer, or safety contract must change.

For one repeatable hit, click `Audition One Hit` at the top of the active Pop
Designer. `Test Pop` remains the randomized 1--5-hit burst. After the timbre is
correct, use the main-page `Pop / Event` fader for total level; that fader is
post-voice and therefore does not change pitch, decay or Crack/Body balance.

To hear the voice alone, enable Audio, turn on `Backfire Solo`, and press
`Test Pop`; this randomized burst audition works even with the engine off. In
normal driving, `Backfire Enable`, ignition and engine-running state remain
mandatory. Hold enough throttle
to load the engine above roughly 1600 RPM, then release W/trigger quickly. The
drive model emits one strength-scaled `overrun` event and the host expands it to
the burst; slow lift-off, braking by itself, low RPM, EV, or an off engine is
intentionally silent. Save the BEAP
patcher after tone edits, then disable Solo and verify the full mix below the
final ceiling.

## Engine start

`Cinematic BEAP` is a hybrid procedural start, not sample playback. The
generated `patchers/engine_start_core~.maxpat` supplies the guaranteed crank and
first-fire pressure, and `patchers/engine_start_beap~.maxpat` is the seed-once
editable colour layer. The generated transient host gates the core directly
from the persistent `starter 0|1` state, avoiding a fragile bang-only envelope.
`Realistic Sample` is the alternate sample mode and uses the tracked CC0 starter
fallback, or the optional local-only V10 Ferrari startup when available.

## Sound DNA controls

RPM is the only master pitch/cadence input. Throttle does not directly tune an
oscillator: the drivetrain first integrates vehicle speed and RPM, while the
DNA applies a bounded 0–8 dB torque-loudness contour plus a smaller continuous
upper-order/intake/electrical colour contour. The default level depth is 4.5 dB,
so pedal motion cannot hide RPM motion behind a large volume jump, while a fixed-
RPM pedal change is still audibly more open rather than merely louder.

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

EV `Aggression` now drives torque-ripple/gear-mesh colour directly; V10
`Brightness` now drives upper firing orders and air directly. These two controls
were previously disconnected declarations and are now regression-tested.
Several other controls are deliberately state-dependent: Intake/Air are
clearest at high RPM and load, Exhaust Detail is clearest under pedal or
lift-off, Stereo Separation is easiest to judge in stereo, and Throttle
Loudness Depth has no effect while the pedal is at zero. Use `Sound DNA Solo`
before deciding that a control is inactive.

EV adds `Torque Ripple`, `Gear Mesh`, and `Electrical Detail`. V10/V12 add
`Combustion Pulse`, `Intake Detail`, `Exhaust Detail`, and `Residual Detail`.
Every DNA number is live. `Save DNA`, `Reload DNA`, and `Reset DNA` operate per profile in
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
`presets/local/{profile}_vehicle_bus_eq.json`. A legacy shared EQ file is only a
first-run migration fallback.

## Cinematic Soundscape

The pad is a BEAP/MSP hybrid. The large named modules are the sound-design
surface: two LFOs, three oscillators, Noise, Mixer, Ladder, MMF, ADSR, VCA,
Chorus and Reverb. Small MSP objects only scale CV, blend stereo, high-pass at
70 Hz and soft-bound the output. The generated profile host handles vehicle
mapping, smoothing, level and DSP suspension; do not tune that plumbing JSON.

The factory signal path is:

```text
root / perfect fifth / octave oscillators + very low noise
  -> Mixer -> Ladder -> MMF -> VCA
  -> parallel Chorus + Reverb -> stereo blend -> 70 Hz HP -> soft output
```

Osc A is the root triangle, Osc B is a quiet saw at `+0.5849625` octaves
(exact 3:2), and Osc C is a much quieter sine at `+1` octave. The two LFOs are
only `0.035` and `0.009` Hz. Their pitch depths are about 0.0005/0.0003 octave
before the Motion scaler, so they create slow drift rather than audible engine-
fault vibrato; only smooth sine/triangle outputs are connected. The Ladder and
MMF begin at 1.4/4.5 kHz with low resonance. The 1.2 s attack and 4.5 s release
avoid rhythmic pumping, while Chorus/Reverb supply width and tail.

Use the Main macros first:

- `Motion` 0.05–0.30: total drift depth. If the pad wobbles or sounds broken,
  lower this before touching oscillator pitch.
- `Pitch Follow` 0.35–0.70: how far RPM moves the chord; it never changes the
  root/fifth/octave relationship.
- `Transpose` ±12 semitones: move the whole voicing without retuning modules.
- `Brightness` 0.25–0.70: mapped filter colour. Lower it at the first sign of
  harshness or resonance during acceleration.
- `Space` 0.20–0.55: reverb send and long-tail depth. Excessive values smear
  throttle response; it is not an LFO speed.

For a warmer Prophet-style pad, keep the root triangle dominant, leave the saw
roughly 7–12 dB below it, keep Noise below 0.02, and use Chorus/Reverb for width.
For a darker ICE bed, set Motion around 0.10–0.18, Pitch Follow 0.45–0.60,
Brightness 0.35–0.50 and Space 0.28–0.42. Avoid high Ladder/MMF resonance and
large LFO-to-pitch depth: those are the main routes back to metallic whistle,
FM-like sidebands and cyclic amplitude beating.

Use `Soundscape Solo`, temporarily bring its mixer level up to about -10 dB,
and click `Open Designer`. Edits in that window affect the currently audible
instance immediately. `Save` writes
`presets/local/{profile}_soundscape.json`; `Reload` restores it and `Factory
Reset` recalls the shipped state. EV, V10 and V12 share the graph but not saved
values. `Save Profile Sound` also saves Soundscape, EQ and Mixer together.
After tuning, turn Solo off and return the shipped balance near -18 dB for EV
or -20 dB for V10/V12 before checking the final limiter.

## Acoustic A/B validation

`tools/build_runtime_probe.py` includes six `dna-*-throttle-low/high` scenarios.
They bypass the drive/controller only inside the monitor-muted diagnostic patch,
hold RPM/load/acceleration constant, and send the public DNA controls directly
to the same profile powertrain abstraction. Production runtimes and lifecycle
probes still use the unmodified drivetrain path.

The final Max 8.6.5 diagnostic renders used 0.10 versus 0.90 throttle. EV/V10/V12
gained 2.86/3.06/3.18 dB while spectral centroid moved 213→222, 342→353 and
508→524 Hz respectively. Clipped-sample ratio was zero for all six files; V10
and V12 full-band mono-fold loss stayed at 0.98–1.13 dB and 0.79–0.88 dB. The
installed NonRealTime driver wrote 44.1 kHz despite the 48 kHz request, so these
are comparative design diagnostics, not sample-rate delivery evidence.
