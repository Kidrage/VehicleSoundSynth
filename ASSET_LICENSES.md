# Asset licenses and provenance

VehicleSoundSynth V4 distributes only CC0 and attribution-compatible CC BY
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
`processed` in the manifest. The runtime starter, shift, intake backfire,
exhaust pop/crackle, mechanical click, shift thump, stereo cabin IR, and the
six-anchor/twelve-loop engine residual bank are processed from these recordings.
Every residual loop is 48 kHz stereo and normalized to -18 dBFS RMS; hashes are
recorded in `assets/engine_texture_bank.json`.

## User-supplied local-only reference

`/Users/saintpeter/Desktop/Ferrari.wav` is a user-supplied SF90 near-field
reference. No redistribution permission is asserted. In addition to analysis,
`tools/prepare_local_reference.py` may deterministically derive the optional
local-only V10 startup, idle body, and steady/accel/decel six-anchor state atlas
used on this machine. V12 never loads these files. A clean checkout instead uses
the tracked CC0 starter and texture bank. Both source and every local derivative
are ignored by Git and must never be committed, synced, uploaded, or released.
The source/processor hashes, direct derivative hashes, and the hash of
`media/local/ferrari_v10_atlas.json` (which records all 18 loop hashes and source
ranges) are authoritative under `local_only_references` in the manifest.

`tools/process_assets.py` converts sources to PCM16, resamples runtime material
to 48 kHz, removes DC, applies short edge fades, and peak-normalizes every
output. Targets are -3 dBFS for starters/IR, -5 dBFS for exhaust pops, -6 dBFS
for shifts/backfires/mechanical details, and -8 dBFS for crackles. Exact source
and processed SHA-256 hashes, crops, channel selection, frame counts, and peak
targets are recorded in `assets/asset_manifest.json`.

The project generator never overwrites an existing curated media file. Its
procedural WAV generation is only a deterministic fallback for a fresh build
that has no curated media yet.
