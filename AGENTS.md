# VehicleSoundSynth V3 Repository Instructions

- Target Max 8.6.5 using built-in objects only.
- Treat `main.maxpat` as the runnable demo and `patchers/vehicle_engine~.maxpat` as the public sound-engine interface.
- Regenerate patchers and media with `python3 tools/build_project.py`; do not hand-edit generated `.maxpat`, `.gendsp`, or `.wav` files.
- Run `python3 -m unittest discover -s tests -v` after changes.
- After generator or project-schema changes, open `VehicleSoundSynth-V3.maxproj` in Max 8.6.5 and check the Max log for project-category, missing-object, Gen outlet, and patchcord errors; JSON-only tests are not a runtime smoke test.
- Keep DSP muted on load and protect stereo output against peaks.
- Keep the low-frequency system lifecycle-gated, centered below 120 Hz, and high-passed near 28 Hz.
- Preserve `/Users/saintpeter/Downloads/VehicleSoundSynth` and `/Users/saintpeter/Downloads/VehicleSoundSynth-V2`; all V3 implementation work belongs in this repository.
