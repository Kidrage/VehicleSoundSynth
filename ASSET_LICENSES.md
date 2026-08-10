# Asset licenses and provenance

VehicleSoundSynth V3 accepts only CC0 and attribution-compatible CC BY source
audio. NC, SA, and unknown-license material is excluded. The machine-readable
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
| Reference recording | [Ferrari acceleration](https://freesound.org/people/biholao/sounds/370278/) | biholao | CC0 1.0 |

All six source files are installed under `assets/raw/` and are marked
`processed` in the manifest. The runtime starter, shift, intake backfire,
exhaust pop/crackle, mechanical click, shift thump, and stereo cabin IR files
are cropped from these recordings. The Ferrari acceleration file is retained
as a listening reference and is not played by the runtime patch.

`tools/process_assets.py` converts sources to PCM16, resamples runtime material
to 48 kHz, removes DC, applies short edge fades, and peak-normalizes every
output. Targets are -3 dBFS for starters/IR, -5 dBFS for exhaust pops, -6 dBFS
for shifts/backfires/mechanical details, and -8 dBFS for crackles. Exact source
and processed SHA-256 hashes, crops, channel selection, frame counts, and peak
targets are recorded in `assets/asset_manifest.json`.

The project generator never overwrites an existing curated media file. Its
procedural WAV generation is only a deterministic fallback for a fresh build
that has no curated media yet.
