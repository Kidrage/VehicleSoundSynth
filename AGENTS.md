# VehicleSoundSynth V3 Repository Instructions

- Target Max 8.6.5 using built-in objects only.
- Treat `main.maxpat` as the runnable demo and `patchers/vehicle_engine~.maxpat` as the public sound-engine interface.
- Regenerate patchers/Gen/presets with `python3 tools/build_project.py`; process curated media with `python3 tools/process_assets.py`. Do not hand-edit generated `.maxpat`, `.gendsp`, or `.wav` files. The sole exception is `patchers/ev_pad_beap~.maxpat`: it is seeded once, intentionally user-tunable, and never overwritten by regeneration.
- Run `python3 -m unittest discover -s tests -v` after changes.
- After generator or project-schema changes, open `VehicleSoundSynth-V3.maxproj` in Max 8.6.5 and check the Max log for project-category, missing-object, Gen outlet, and patchcord errors; JSON-only tests are not a runtime smoke test.
- Keep DSP muted on load and protect stereo output against peaks.
- Keep the low-frequency system lifecycle-gated and high-passed near 28 Hz. Center deep bass after the cabin IR with the 120 Hz crossover; stereo phase shaping and early reflections belong only above that crossover.
- Never commit or sync `media/local/` or `/Users/saintpeter/Desktop/Ferrari.wav`; only the non-audio target JSON and deterministic fallback may be tracked.
- Treat `assets/asset_manifest.json` and `ASSET_LICENSES.md` as the provenance authority. Distributable runtime field recordings must remain CC0/CC BY, hash-verified, DC-cleaned, faded, and normalized. User-supplied local-only references are allowed only when separately hash-documented, ignored by Git, and never synced or redistributed.
- Preserve `/Users/saintpeter/Downloads/VehicleSoundSynth` and `/Users/saintpeter/Downloads/VehicleSoundSynth-V2`; all V3 implementation work belongs in this repository.
