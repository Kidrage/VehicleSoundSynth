# Ferrari-only body return and lightweight Pop

## Scope and rollback

Branch: `codex/v6-ferrari-body-pop-sampler`, based on `93accba116b88be1b80508905aa1f22a85dd1c9d`.
No merge or GitHub push is part of this delivery. The existing user-owned
`main.maxpat` diff is excluded from the commit and unchanged by this task.

Before editing, committed files plus working Main/local presets were archived to:
`/Users/saintpeter/Downloads/.VehicleSoundSynth-Backups/ferrari-body-pop-20260908.XSZyoHiF`.

- `committed-93accba.tar`: SHA-256 `2f95750cf0cd1527f68e5d37f52068122ffd4ce5953bd00e7c1e8957b9ab63af`
- `working-main-and-local-presets.tar`: SHA-256 `13f98518d65548383be85b45c3241df7599ec269b6e5c5788a113655ff9df15c`
- `file-sha256.json`: pre-task working-file hash inventory.

227 original Gen/patcher/code/media/preset files outside the two dedicated
Ferrari hosts remain byte-identical, including original ignored local presets.
Main is the 228th protected file. Ferrari DNA/start, the other four sounds,
all five shared runtime hosts, input/drivetrain, Mixer/EQ/dynamics remain intact.
The Ferrari adapter changes only its version/location comment.

## Diagnosis and minimal enhancement

The preceding control repair did not retune Ferrari's DNA or Soundscape source
or its effective synthesis presets. Older and current local Mixer balances do
differ, but the available recordings do **not** establish one definitive cause
for the reported subjective loss of weight. This task does not rewrite that
history or reset the user's Mixer.

Soundscape V6 retains V5's synthesis, cadence, filters and spatial graph and
adds one enveloped dry-body return from its own `Ferrari_Output_VCA`, never
from DNA. It is high-passed at 120 Hz, low-passed at 650 Hz, polarity-aligned
with the existing parallel return, and mixed before the existing output safety
filters/trim. Main's existing Enable/Solo and lifecycle suspension still govern
the whole stem. Space no longer has sole responsibility for conveying body.

`Direct Body` is the only added control: -60..0 dB, factory -9 dB; -60 disables
the addition. Start around -12..-6 dB. Raising it is an audible tonal change,
not a claim of a bit-identical full mix. The V5 graph, factory and local file
are preserved. V6 uses `ferrari_soundscape_v6` state; this installation seeds
that ignored file from the user's V5 values with only the new return added.
Fresh checkouts use the tracked V6 factory.

## Pop V3

One mono 48 kHz / 240 ms PCM16 CC0 exhaust one-shot, approximately 23 KB,
replaces the live Ferrari BEAP impact synthesis. Source: the already-curated
richwise sports-car rev/pop recording; it is **not** claimed to be a Ferrari
recording. See `ASSET_LICENSES.md` and the asset manifest for source attribution.

Offline processing keeps the recorded attack, adds short body pressure and two
small reflections, removes DC and fades both edges. No new recording library,
runtime reverb/convolution, oscillator bank or synthetic fallback was added.
`tools/prepare_ferrari_pop.py` verifies the raw hash before rendering; regeneration
matches `cf63aab2c16eee3efcf3e94c07baf3a3a1a5c04a5509009174c46559bb49133a`.

The live path is one buffer -> two round-robin `play~` voices -> shared tone
filter -> level -> existing Pop stem. Idle voices mute their DSP. Reuse/shutdown
fade over 3 ms. The unchanged burst scheduler still owns hit counts and timing;
automatic shift/overrun/event gates and ignition-independent previews remain.
The old Ferrari Pop graph is retained but no longer instantiated by the host.

The actual designer opens through the existing Pop Open bus and exposes only:

- Pitch: -6..+3 semitones, applied to the next hit.
- Tone: 1200..8000 Hz, factory 4200 Hz.
- Level: -24..0 dB, factory 0 dB, in addition to the unchanged stem balance.

Audition One/Burst, explicit Save/Reload and Factory Reset are included.
State uses `presets/local/ferrari_pop_v3.json`; it never reads old Pop presets.
Use Save to retain manual changes. Missing WAV fails silent with a file error;
the designer reports sample readiness after the explicit buffer read completes.

## Verification

- `python3 -m unittest discover -s tests -v`: **211 passed**, 207.019 s.
- Two fresh generator roots: **163 files identical**; combined sorted
  `path + space + sha256 + newline` digest:
  `9e62f764c11c1a9030a0979c4ad90161ba5d60f2d9d60eb36c8010067a8a8ef9`.
  Installed new Ferrari graphs/project/factory match that output.
- `git diff --check` passes. Re-rendered sample matches the tracked hash.
- New tests cover the real dedicated graph, two-player limit, sample provenance
  and edges, physical gates/preview/cancellation, direct-body reachability and
  its registration with persistence. Actual Max testing caught and fixed an
  initially missing plain-control `autopattr` registration and unreliable
  constructor-time sample-ready notification before delivery.

Max 8.6.5 was exercised in isolated project copies with hardware output muted.
The final Main/Ferrari test wrote eight channels at an actual 48 kHz. In held
Load / Soundscape Solo, representative two-second windows were:

| State | SC L RMS dBFS | Final L RMS dBFS | SC 2–6 kHz energy ratio | Mono loss |
|---|---:|---:|---:|---:|
| New dry return off | -23.69 | -34.41 | 0.002026 | 0.039 dB |
| Dry return -6 dB | -17.43 | -27.09 | 0.000501 | 0.008 dB |
| Factory reset (-9 dB) | -19.02 | -29.11 | 0.000870 | 0.011 dB |

These sequential windows contain the existing stochastic layers; they are
audibility/body evidence, not phase-identical null tests or subjective acceptance.
The final recording has no clipped samples: SC peak <0.831, Pop peak <0.161,
final peak <0.288. The sustained factory SC passes the 0.001 harshness target;
the deliberately transient Pop attack is not evaluated as a sustained pad.

Actual -6 dB Save -> change to -60 -> Reload restored -6; Factory Reset and
reopening restored -9. Pop lower-pitch playback lengthened to approximately
339 ms, -12 dB Level reduced the recorded event accordingly, Reload retained
it and Factory Reset restored the defaults. Burst/preview/shutdown and automatic
repeated hits played; stopped output returned to digital silence. Both live
designer windows opened through their existing control paths.

The isolated same-driver Pop comparison used 160 ms automatic hit spacing.
New Pop recorded peak 0.163 with a silent final second. Max's **integer-percent**
CPU telemetry averaged old/new: idle 1.40/0.00, active 0.97/0.16, tail 1.44/0.02.
This is a coarse local observation, not a calibrated CPU savings percentage;
0 means below the meter's resolution, not zero computation.

Early diagnostic runs with auto-restored duplicate windows or an incorrectly
qualified standalone probe object were rejected. The final single-runtime load
and playback produced no new missing-object/Gen/patchcord/project-category errors.
Known baseline optional local startup-file and readonly Max database warnings
were not repaired outside scope. Temporary instrumentation exists only under
`/private/tmp/vss-ferrari-body-pop.fx9PhKKz`, not in delivered graphs.

All intentional generated edits are saved on disk. The task's temporary Max
save prompt was resolved, and task PID 60550 exited normally. Only pre-existing
user Max PID 36547 remained; it was not modified or quit. No raw reference,
ignored preset, backup archive, test recording or recovery file is committed or
synced; the Codex relay receives text-only delivery notes.
