# OSC Engine Lab (JUCE) — P0

New independent procedural sound-engine research under `VehicleSoundSynth` while preserving all V7 and IONIQ6N sound sources.

**Baseline:** `EV-Engine-V7` at `d5fa73f323ba7686c364f3a180806da10ee003b7`. **Research branch:** `research/osc-engine-lab-juce`.

Goal: a simple real-time JUCE UI (RPM, load, DNA, body, pad, turbulence, master, play/stop, RPM trajectory replay, 48 kHz WAV export), JUCE-free modular portable C++ DSP, fixed parameter snapshots and A/B tests. Targets: NA V8, NA V10, turbo flat-6, and an original sci-fi synthesizer DNA mode. No engine recording needs to be part of the running signal path.

**Approval gate:** review links in `docs/REFERENCE_CANDIDATES.md`; do not download recordings or run audio cleanup until user approves the actual sources and use rights are checked. At this stage no YouTube source audio has been downloaded, analyzed or redistributed.

Baseline architecture: phase-continuous firing exciter -> independent source partials and pressure contour -> fixed/slow modal structure + air/turbulence -> optional synth DNA pad -> loudness-controlled mix -> safety output. 911 Turbo S is a flat-six, not a V8/V10. Do not claim that an evenly spaced firing oscillator can exactly reconstruct cylinder timing, bank manifolds and microphone/cabin transfer.

GitHub tracking: https://github.com/Kidrage/VehicleSoundSynth/issues/1

Temporary standalone C++/JUCE source artifact is delivered in the initiating ChatGPT conversation as an independent downloadable ZIP. The archive is not a compiled JUCE application; its portable DSP CMake/CTest path has been run locally. Keep V7 generator and user patches untouched until review.
