# Asset licenses and provenance

VehicleSoundSynth V5 distributes only CC0 and attribution-compatible CC BY
source audio. NC, SA, and unknown-license material is excluded from the
repository and release. The machine-readable
record is `assets/asset_manifest.json`; its hashes and processing fields are the
release authority.

## Installed source recordings

| Purpose | Source | Author | License |
|---|---|---|---|
| Starter | [Car Starter](https://freesound.org/people/Grasopt/sounds/479351/) | Grasopt | CC0 1.0 |
| DCT shifts | [Engine block/chassis contact recording](https://freesound.org/people/TheLittleCrow/sounds/669623/) | TheLittleCrow | CC0 1.0 |
| Revs, pops, crackles | [Sports/Supercar Rev & Pops](https://freesound.org/people/richwise/sounds/478756/) | richwise | CC0 1.0 |
| Mechanical selector | [Mechanical gear shift](https://freesound.org/people/microman502/sounds/818294/) | microman502 | CC0 1.0 |
| Cabin IR | [Mini car impulse response](https://freesound.org/people/jamespeacock4616/sounds/555787/) | jamespeacock4616 | CC0 1.0 |
| Engine residual bank/reference | [Ferrari acceleration](https://freesound.org/people/biholao/sounds/370278/) | biholao | CC0 1.0 |

All six source files are installed under `assets/raw/` and are marked
`processed` in the manifest. V5 runtime audio uses only the processed starter
and stereo cabin IR. The processed shift, intake-backfire, exhaust-pop/crackle,
mechanical-click, shift-thump, and six-anchor residual files remain licensed
archive/offline-analysis artifacts and are not declared or loaded by a V5 runtime.
Every residual loop is 48 kHz stereo and normalized to -18 dBFS RMS; hashes are
recorded in `assets/engine_texture_bank.json`.

## V6 shared Pop sample exception

`media/ferrari_pop_v3.wav` is a 240 ms mono event made only from richwise's
CC0 **Supercar rev** recording above (source SHA verified). The author did not
identify the car: this is real exhaust material, not a Ferrari-specific recording
claim. `tools/prepare_ferrari_pop.py` deterministically isolates the event at
6.537 seconds, shapes its recorded body/crack and two short reflections offline,
removes DC, fades its edges and normalizes to -6 dBFS peak. The exact recipe and
output hash are in the manifest. It is the sole new runtime sample; the other
archived event files remain unused and no user-supplied reference is involved.
Ferrari Pop V3 and the other four profiles' Pop V4 share this same file with
profile-specific post-processing and at most two idle-muted players. EV only
exposes manual preview; IONIQ keeps its mode/eShift event conditions.

## User-supplied local-only reference (unchanged)

`/Users/saintpeter/Desktop/Ferrari.wav` is a user-supplied SF90 near-field
reference. No redistribution permission is asserted. Its tracked output is a
non-audio lifecycle measurement table used to tune and validate the procedural
V10 model. `tools/prepare_local_reference.py` may also derive an optional
local-only V10 realistic-start one-shot. Idle-body, residual, and atlas outputs
are offline comparison artifacts only and are never loaded for continuous
runtime sound. V12 never loads any Ferrari-derived file. A clean checkout uses
the tracked CC0 starter. The source and every local audio derivative are ignored
by Git and must never be committed, synced, uploaded, or released; the manifest
records the relevant source, processor, target-table, and derivative hashes.

`tools/process_assets.py` converts sources to PCM16, resamples processed material
to 48 kHz, removes DC, applies short edge fades, and peak-normalizes every
output. Targets are -3 dBFS for starters/IR, -5 dBFS for exhaust pops, -6 dBFS
for shifts/backfires/mechanical details, and -8 dBFS for crackles. Exact source
and processed SHA-256 hashes, crops, channel selection, frame counts, and peak
targets are recorded in `assets/asset_manifest.json`.

The project generator never overwrites an existing curated media file. Its
procedural WAV generation is only a deterministic fallback for a fresh build
that has no curated media yet.
