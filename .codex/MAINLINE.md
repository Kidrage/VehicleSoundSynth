# VehicleSoundSynth V5 Mainline

Base: frozen V4 tag `v4.0.0` (`6aa49d0`).

1. Rename project/runtime identity to V5 without changing the three-runtime architecture.
2. Replace runtime shift/pop/crackle samples with continuous powertrain/cabin motion and BEAP physical transients.
3. Improve continuous EV, V10, and V12 realism while preserving smooth throttle-driven RPM and the V10 Ferrari lifecycle analysis gates.
4. Add editable V10/V12 cinematic pad and backfire BEAP patchers with top-level controls and suspendable DSP.
5. Add one shared persistent four-band vehicle-bus EQ state with load/save/reload/reset and safe fallback.
6. Validate structure, deterministic generation, audio metrics, CPU behavior, and real Max 8.6.5 loading; save, close, and quit Max.
7. Add a switchable Keyboard/macOS HID Manual Input module with configurable
   axes, Learn/debug, normalized pedal mapping, and safe source release without
   changing the 20 ms drivetrain model.
