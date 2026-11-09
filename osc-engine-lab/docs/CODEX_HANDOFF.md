# Codex handoff: OSC Engine Lab / P0

Canonical source: https://github.com/Kidrage/VehicleSoundSynth
Canonical default branch `main`: `ac2b37d8639027d79934a2023cf8d1d37d3b2f96` (V6); actual latest working V7 branch `EV-Engine-V7`: `d5fa73f323ba7686c364f3a180806da10ee003b7` (2026-10-09).
Target isolated branch: `research/osc-engine-lab-juce`; no main or V7 push, merge, reset, generator run, or change to IONIQ6N.

Before touching V7: read `AGENTS.md`, `.codex/REPO_GUIDE.md`, `.codex/MAINLINE.md`, `PROJECT_HANDOFF.md`, `SOUND_DESIGN_GUIDE.md`, `V7_MANUAL.md`, `V7_CODEX_HANDOFF.md`. Verify `git remote -v; git status --short; git branch --show-current; git rev-parse HEAD`. Preserve user uncommitted patches and `presets/local`.

Scope: first an independent C++ DSP core and JUCE desktop shell with no shared runtime names; fixed snapshots, matched-RPM/load replay, solo/bypass per layer; no sample fallback, no user-reference audio uploaded. Maintain source, tonal DNA, pressure/body, pad, turbulence, cabin transfer, drivetrain, events, and output safety as separable units. Validations: portable CMake/CTest, JUCE native device test, measured waveform and RTPC replay, CPU/MCPS benchmark, Max V7 independent A/B on target macOS.

**No YouTube download until user reviews source list** and license is verified. Do not label video-extracted mixed audio as an isolated exhaust stem. Audio analysis after approval must identify time codes, source QA, order-vs-RPM, 20–120, 120–250, 250–600, 600–1200, 1.2–2k, 2–6k, stereo and transient measures, with measured-vs-inferred confidence.

Accepted IONIQ6N identity and user local presets are protected. V7 regression hypotheses include active parameter routing and preset/factory state drift; no conclusion without captured, level-matched A/B and parameter diff. Rollback by retaining separate worktrees and reverting only research commits, never force pushing or resetting user changes.
