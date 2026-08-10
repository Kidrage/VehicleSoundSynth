# VehicleSoundSynth V3 Repository Instructions

- Target Max 8.6.5 using built-in objects only.
- Treat `main.maxpat` as the runnable demo and `patchers/vehicle_engine~.maxpat` as the public sound-engine interface.
- Regenerate patchers/Gen/presets with `python3 tools/build_project.py`; process curated media with `python3 tools/process_assets.py`. Do not hand-edit generated `.maxpat`, `.gendsp`, or `.wav` files.
- Run `python3 -m unittest discover -s tests -v` after changes.
- After generator or project-schema changes, open `VehicleSoundSynth-V3.maxproj` in Max 8.6.5 and check the Max log for project-category, missing-object, Gen outlet, and patchcord errors; JSON-only tests are not a runtime smoke test.
- Keep DSP muted on load and protect stereo output against peaks.
- Keep the low-frequency system lifecycle-gated and high-passed near 28 Hz. Center deep bass after the cabin IR; the final Side path is four-stage high-passed at 180 Hz.
- Treat `assets/asset_manifest.json` and `ASSET_LICENSES.md` as the provenance authority. Runtime field recordings must remain CC0/CC BY, hash-verified, DC-cleaned, faded, and normalized.
- Preserve `/Users/saintpeter/Downloads/VehicleSoundSynth` and `/Users/saintpeter/Downloads/VehicleSoundSynth-V2`; all V3 implementation work belongs in this repository.
