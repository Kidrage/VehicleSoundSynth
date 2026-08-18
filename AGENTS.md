# VehicleSoundSynth V4 Repository Instructions

- Target Max 8.6.5 using built-in objects only.
- Treat `main.maxpat` as a DSP-free launcher. The runnable demos are `VehicleSoundSynth-EV.maxpat`, `VehicleSoundSynth-V10.maxpat`, and `VehicleSoundSynth-V12.maxpat`; open only one at a time. Their public seams are `patchers/vehicle_engine_{ev,v10,v12}~.maxpat`.
- Regenerate patchers/Gen/presets with `python3 tools/build_project.py`; process curated media with `python3 tools/process_assets.py`. Do not hand-edit generated `.maxpat`, `.gendsp`, or `.wav` files. The seed-once user-owned exceptions are `patchers/engine_start_beap~.maxpat`, `patchers/ev_pad_beap~.maxpat`, `patchers/ev_expressive_beap~.maxpat`, and `patchers/ev_sport_beap~.maxpat`.
- Run `python3 -m unittest discover -s tests -v` after changes.
- After generator or project-schema changes, open `VehicleSoundSynth-V4.maxproj` in Max 8.6.5 and check the Max log for project-category, missing-object, Gen outlet, and patchcord errors; JSON-only tests are not a runtime smoke test.
- Keep DSP muted on load and protect stereo output against peaks.
- Keep the low-frequency system lifecycle-gated and high-passed near 28 Hz. Center deep bass after the cabin IR with the 120 Hz crossover; stereo phase shaping and early reflections belong only above that crossover.
- Never commit or sync `media/local/` or `/Users/saintpeter/Desktop/Ferrari.wav`. Optional local-only V10 startup/idle/state-atlas runtime layers may be generated only by `tools/prepare_local_reference.py`; processing must be deterministic and hash-reported, V12 must remain independent, a clean checkout must fall back to the tracked CC0 starter/texture bank, and no local source or derivative may be distributed.
- When runtime-checking in Max, save intentional patch edits, close every patcher and Project window opened by the task, and quit the task-owned Max instance before reporting completion.
- Treat `assets/asset_manifest.json` and `ASSET_LICENSES.md` as the provenance authority for distributable assets. Distributable runtime field recordings must remain CC0/CC BY, hash-verified, DC-cleaned, faded, and normalized. User-supplied local-only references must be deterministically processed, hash-reported, ignored by Git, and never synced or redistributed.
- Preserve every sibling V1/V2/V3 repository; all V4 implementation work belongs in this repository.
