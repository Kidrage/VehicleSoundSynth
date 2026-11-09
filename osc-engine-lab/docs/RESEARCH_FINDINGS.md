# Procedural Vehicle Sound — research evidence (2026-11-09)

**Status: literature/metadata study only; NO approved source recordings downloaded, decoded, or measured.**

## Is pure OSC viable?
Few phase-locked sine orders are inadequate for convincing engine identity through start/idle/RPM/load/lift/shift, but fully procedural audio with phase-continuous pressure pulse excitation, correct firing-event timing, dynamic order gains, stochastic turbulence, fixed/slow structural resonance and optional user-authored wavetable DNA is a technically defensible route. Specific-car indistinguishability remains an untested listening requirement.

Four-stroke **even-fire event cadence**, not necessarily the observed spectral F0:
`f_events = RPM * cylinders / 120`.
At 6000RPM: V8 400 events/sec; V10 500; flat-6 300. Actual audible orders depend on firing order, exhaust bank geometry, turbo/NA, pulse asymmetry and transfer functions. 911 Turbo S = twin-turbo flat-six.

## Research leads

- S. Baldan et al., [Physically informed car engine sound synthesis](https://ieeexplore.ieee.org/abstract/document/7361287), IEEE SIVE 2015: procedural/physically informed model.
- R. Doerfler & L. Wyse, [Differentiable Pulse-Train Synthesis](https://arxiv.org/abs/2603.09391), 2026: pressure pulses/exhaust resonators, reports 21% harmonic reconstruction improvement relative to their harmonic+noise baseline (study-specific).
- R. Doerfler et al., [EONE parametric engine sound](https://rdoerfler.github.io/eone-model-page/), AES Automotive Audio 2026: learnable RPM/torque-conditioned harmonic gain and noise-bank representation oriented to embedded resynthesis.
- [AES Design of an Engine Sound Synthesis System for Flexible Sound Design](https://aes.org/publications/elibrary-page/?id=22623): additive, granular and Fourier synthesis for real and sci-fi voices.
- [BMW IconicSounds Electric](https://faq.bmwusa.com/s/article/BMW-iX-from-112021-BMW-iX-from-032025-Driving-experience-BMW-IconicSounds-Electric-MY22MY26-d37Xg): BMW confirms Hans Zimmer collaboration and mode-dependent sound.

## Production-oriented hypotheses

Keep one DSP instance/preset namespace per voice. Split RTPC/state -> firing/source/DNA -> body/cavity -> pad -> stochastic mechanical/HF -> scene/cabin/IR -> output safety. Include bypass/solo/multi-stem traces. Fixed modes must remain in fixed/slow bands, RPM-related oscillators must not arbitrarily plateau or drift by gear. Limit high-frequency growth relative to low-mid load growth; **do not claim a numerical target before real measurement**.

**Validation protocol:** user-approved legitimately usable reference files -> source QA and license/SHA -> time-coded state selection -> measurements per band (20-120, 120-250, 250-600, 600-1200, 1.2-2k, 2-6k), order tracking, stereo correlation, event dynamics -> matched-control/level A/B with legacy V7 -> Mac/Windows JUCE realtime tests and measured target MCPS. No inference of CAN/RPM authority or physical IR from video audio.

Keep IONIQ6N accepted sound snapshots read-only. The research-branch source code can be delivered in a downloadable package; JUCE native compilation and listening are not verified by these notes.