# V6 Sound Design Guide

This guide separates the files that are safe to tune by ear from the generated
routing that should normally be left alone.

## Open the editable modules

Open `main.maxpat`, select a runtime, and use the live Soundscape strip in the
launcher or the matching strip inside the runtime. Both views address the same
audible instance and receive its current state:

- `Open Sound DNA` opens the active profile's procedural engine panel.
- `Sound DNA Solo` removes Soundscape, transient, road and rumble stems while
  leaving the active procedural powertrain audible.
- Soundscape `Open Designer` fronts the exact cinematic pad instance feeding
  the active profile; it no longer opens a detached file or `poly~` copy.
- V10/V12/Ferrari `Open Pop Designer` opens the active backfire voice in the supported
  one-runtime-at-a-time workflow, not a detached duplicate patcher. Two copies
  of one profile share its tuning bus and are not a supported tuning setup.
- IONIQ6N exposes `N Sound Mode`, `N e-Shift`, and a separate N Event Designer.
  Its Soundscape, Sound DNA, ready activation and N events are four independent
  tuning domains; changing one never writes parameters into another.

The visible four-node EQ embedded at the bottom of each engine window uses the
same `patchers/vehicle_bus_eq~.maxpat` design, but its values are stored per
profile. Save the patcher itself after changing its layout or objects. Use its
`Save EQ` button to save the active EV/V10/V12/IONIQ6N/Ferrari values for the next launch.

## Human-maintained sound-design modules

| Module | Purpose | Persistence |
|---|---|---|
| `patchers/ev_sound_dna~.maxpat` | EV motor, inverter, gear and stereo character | Patcher is seed-once; `Save DNA` writes ignored local values |
| `patchers/v10_sound_dna~.maxpat` | V10 combustion, intake, exhaust and residual character | Same |
| `patchers/v12_sound_dna~.maxpat` | V12 bank, air and smooth high-rev character | Same |
| `patchers/ioniq6n_sound_dna~.maxpat` | IONIQ6N motor order, body/cavity, mechanical texture and ready bed | Same |
| `patchers/ferrari_sound_dna~.maxpat` | Analysis-derived V10 order, five acoustic bands and lift-off mass | Same |
| `patchers/vehicle_bus_eq~.maxpat` | Four-band output tone shaping | Patcher is seed-once; `Save EQ` writes ignored per-profile state |
| `patchers/cinematic_soundscape_beap~.maxpat` | Shared four-layer Soundscape V2 topology | Seed-once; the live host writes ignored per-profile V2 state |
| `patchers/{ev,v10,v12}_engine_start_beap~.maxpat` | Independent cinematic starts | Seed-once; each profile has its own controls and ignored state |
| `patchers/v10_backfire_beap~.maxpat`, `v12_backfire_beap~.maxpat` | Physical pressure-release voices | Seed-once |
| `patchers/ioniq6n_soundscape_{ignition,evolution,lightspeed}_beap~.maxpat` | Three independent N Sound instruments | Seed-once; shared mode host writes ignored local state |
| `patchers/ioniq6n_activation_beap~.maxpat` | Ready activation/chime | Seed-once |
| `patchers/ioniq6n_n_event_beap~.maxpat` | N e-Shift impact, release bubble and afterburner pop | Seed-once; own ignored local state |
| `patchers/ferrari_soundscape_v4_beap~.maxpat` | Exterior body, cavity projection, mechanical halo and air/reflection | Seed-once; own ignored V4 state |
| `patchers/ferrari_engine_start_v3_beap~.maxpat` | Procedural-only V10 crank and catch | Seed-once; own ignored start state |
| `patchers/ferrari_backfire_v2_beap~.maxpat` | Procedural pressure release | Seed-once; own ignored backfire state |

`patchers/module_mixer.maxpat` is generated routing/UI, not a synthesis patch.
Use its seven main-page faders to balance Sound DNA, Start, Pop/Event,
Soundscape, Road/Air, Cabin Rumble and Master. The values themselves are
human-owned per-profile state in ignored `presets/local/*_module_mixer.json`.

`patchers/{profile}_powertrain~.maxpat`, the matching `gen/*.gendsp`, the
Soundscape hosts, cabin, road, transient and `mix_master~` are generated bridge
or safety modules. Edit `tools/build_project.py` and regenerate when those
interfaces must change; do not tune their generated JSON directly.

## Backfire voice

The editable sound is in the V10, V12 and Ferrari `*_backfire_v2_beap~.maxpat`
patchers. The matching generated
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

`Cinematic BEAP` is procedural, not sample playback. Open the active profile's
seed-once `ev_engine_start_beap~`, `v10_engine_start_beap~`, or
`v12_engine_start_beap~` designer and tune Activation/Crank Body, Catch Bloom,
Metal, Air, Tail and Level. Audition reaches that exact audible instance; Save,
Reload and Factory Reset persist under
`presets/local/{profile}_start_v2.json`. V10 uses a cranked 60--67 Hz catch,
V12 a quicker smoother twelve-cylinder catch, and EV a ready chime/harmonic
activation. `Realistic Sample` is the mutually exclusive ICE alternate and uses
the tracked CC0 fallback, or optional local-only V10 Ferrari startup.
Ferrari has its own `ferrari_engine_start_v3_beap~` and exposes no realistic
sample choice.

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
- `Idle Level`, `Idle Body`, `Idle Metal`, `Idle Irregularity`, `Idle Air`, and
  `Idle Width`: shape the low-RPM layer. On V10/V12 the exact firing cadence is
  shared by both channels and stereo comes from bank/modal detail, not detuning;
  the layer fades smoothly with RPM. On EV these controls shape only the quiet
  ready-state electromagnetic bed, never simulated combustion.

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

Ferrari instead exposes `Order Core`, `Body Band`, `Cavity Band`, `Mechanical
Band`, `Presence Band`, `Edge Band`, `Band Load Depth`, and `Lift Mass`, plus
intake/exhaust, irregularity, width, saturation and idle controls. Tune in that
order: establish 120--600 Hz mass first, add 600 Hz--2 kHz structure next, and
raise 2--6 kHz Edge last. Load opens all five bands by different bounded
amounts; Lift Mass deliberately releases body/cavity more slowly while dropping
the edge quickly. Soundscape is a separate stem and never receives these DNA
parameters.

## IONIQ6N independent profile

This fourth runtime is deliberately separate from V10. The reference road-test
MP3 informed target ranges only; no recording or derivative is loaded at
runtime. Use Sound DNA Solo first and tune in this order:

1. `Body Pressure` and `Cavity Structure` fill the low-mid mass without adding
   fake combustion.
2. `Motor Order` sets the phase-coherent electric core.
3. `Mechanical Texture` and `HF Edge` add inverter/gear definition; keep HF
   Edge restrained if acceleration becomes plastic.
4. `Load Depth` opens the timbre at fixed RPM, while `Release Mass` controls
   lift-off weight. `Ready Bed` is the quiet ignition-on floor.
5. Set `Stereo Width` and `Saturation` last. Bass centring and the final
   subsonic/peak guards remain downstream.

The Soundscape has three genuinely separate BEAP graphs selected with
`n_sound_mode ignition|evolution|lightspeed` and crossfaded over 150 ms:

- Ignition is pressure-led and restrained; release may excite a low bubble.
- Evolution is the default cinematic score voice, built from fixed-ratio
  harmonic motion and short dramatic transients.
- Lightspeed emphasizes velocity pressure, mechanical climb and a bounded high
  shimmer; release may excite the afterburner event.

RPM is the only root-pitch input. Load/throttle changes layer balance and
filter opening, and speed changes only upper air/space. To prove the separation,
hold RPM fixed, move throttle/load, then change speed: the first operation must
change density/colour, the second must change width/air, and neither should
step the root pitch.

`eshift_enable 1` is the default eight-ratio N e-Shift behaviour. Set it to `0`
for continuous EV pitch with no virtual shift events. The N Event Designer has
its own Enable, Intensity, Audition, Save, Reload and Factory Reset controls;
normal events still require ignition and engine-running state. Factory state is
tracked in `presets/ioniq6n_soundscape_modes_factory.json` and
`presets/ioniq6n_n_event_factory.json`; user state stays under ignored
`presets/local/`.
Every DNA number is live. `Save DNA`, `Reload DNA`, and `Reset DNA` operate per profile in
`presets/local/{profile}_sound_dna.json`; those local files are intentionally
ignored by Git.

The previous plastic quality mainly came from phase-locked sine orders, a large
throttle-to-level range, shared left/right resonances, and saturation plus final
compression masking small dynamics. V5 keeps the stable firing cadence but adds
different left/right non-integer orders, independent bank/intake/exhaust paths,
bounded air layers and adjustable irregularity. Continuous V10/V12 audio still
does not read Ferrari samples; the Ferrari interpretation is procedural too.

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

Soundscape V4 is a BEAP/MSP hybrid divided into Body/Modal, Harmonic/Macro,
Noise/Resonator and Air/Shimmer layers. The generated profile host handles vehicle
mapping, smoothing, level and DSP suspension; do not tune that plumbing JSON.

The signal path is:

```text
Body + Harmonic + Resonator + Air
  -> structure/filter -> dynamics
  -> high-band space and pan -> centred <120 Hz bass -> protected output
```

RPM continuously owns the root pitch, so Soundscape changes with speed through
the unchanged drive model. Throttle and load change layer balance,
filter opening and texture, not the root note. The two LFOs only add restrained
filter/waveform/high-band pan motion: they do not impose obvious volume pumping
or large pitch wander. Tune in the labelled order—source, structure/filter,
dynamics, space, output—and keep the low-frequency Body centred.

The V4 tracked factory files are `presets/{ev,v10,v12,ferrari}_soundscape_v4_factory.json`.
V1--V3 factories and local presets remain unchanged for compatibility but are
never loaded into V4. Firing/order oscillators feed filters and resonators; no
bare periodic waveform or full-mix waveshaper reaches the output. The profiles
deliberately use different palettes:

- EV: `0 / +7 / +12` voicing, brightest filters, wider chorus, restrained long
  space for a clean futuristic layer.
- V10: `-5 / 0 / +7`, root-heavy mixer, darker filters and narrow chorus for
  a compact mechanical low bed.
- V12: `0 / +7 / +12`, smoother harmonic blend, broad chorus and the longest
  release/reverb for a weightier orchestral pad.
- Ferrari: cadence-led exterior body, octave cavity projection, load-opened
  mechanical halo and upper-band roadside reflection; it is not a chord Pad.

The tracked JSON contains the complete V4 state. At load,
the helper reads slot 99 from that authority, waits for the nested BEAP clients,
recalls it, and then
applies the ignored `presets/local/{profile}_soundscape_v4.json` slot 1 when it
exists. After every local read it re-reads slot 99 from tracked JSON, so a legacy
local slot 99 cannot shadow a newer shipped voicing. `Factory Reset` recalls the
reloaded slot 99 and saves that complete result as the new local slot 1. Saving
deletes slot 99 before writing; the user file therefore contains only slot 1.
The three Osc `Freq` controls are then continuously owned by the runtime RPM
pitch law; tune chord intervals with `Offset`, and tune global travel with
`Pitch Follow`/`Transpose` rather than trying to hold those three dials fixed.

Use the Main macros first:

- `Motion` 0.05–0.30: analog drift depth. If the pad wobbles or sounds broken,
  lower this before touching oscillator pitch.
- `Pitch Follow` `1.0`: exactly restores the former large RPM travel. The root
  laws are EV `55 + 0.032*rpm`, V10 `36.7 + 0.014*rpm`, and V12
  `32.7 + 0.012*rpm`; Ferrari follows the V10 travel law. Values below 1 blend logarithmically toward the profile's
  stationary root; they do not alter the visible interval relationship.
- `Transpose` ±12 semitones: move the whole voicing without retuning modules.
- `Brightness` 0.25–0.70: mapped filter colour. Lower it at the first sign of
  harshness or resonance during acceleration.
- `Space` 0.20–0.55: reverb send and long-tail depth. Excessive values smear
  throttle response; it is not an LFO speed.

`Enable` defaults on in a fresh/factory profile but remains ignition-gated.
For V10/V12/Ferrari, the cadence-excited idle Body additionally requires a successful
`start 1`; `ignition 0` clears that latch. Thus opening the patch, enabling
Soundscape, or receiving RPM alone cannot passively start a combustion roar.
Changes from either Main or the runtime view are sent directly to the current
engine; feedback updates both views without reopening the patch. `Save` writes
only the selected profile, while `Reload` immediately recalls its saved state.
The Main link uses separate EV/V10/V12/Ferrari buses, so even the brief overlap while an
old runtime closes cannot receive the new profile's tuning or overwrite its
saved Soundscape.

For a warmer future bed, tune the Harmonic/Macro layer around the profile root,
keep Body dominant, keep Resonator/Air restrained, and add width only above the
bass split. For a darker
ICE bed, start with Motion `0.10–0.18`, Pitch Follow `1.0`, Brightness
`0.35–0.50`, and Space `0.28–0.46`. Avoid high Ladder/MMF resonance and large
LFO-to-pitch depth: those are the main routes back to metallic whistle, FM-like
sidebands and cyclic amplitude beating. If the pad is too low, raise oscillator
Offsets by 12 semitones before changing the RPM law; if it is too static, raise
Pitch Follow toward 1 before raising Motion.

Use `Soundscape Solo`, temporarily bring its mixer level up to about -10 dB,
and click `Open Designer`. Edits in that window affect the currently audible
instance immediately. `Save` writes
`presets/local/{profile}_soundscape_v3.json`; `Reload` restores it and `Factory
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
