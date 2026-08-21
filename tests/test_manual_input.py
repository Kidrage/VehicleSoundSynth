import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUAL_INPUT_JS = ROOT / "code" / "manual_input.js"
DRIVE_MODEL_JS = ROOT / "code" / "drive_model.js"


def run_node(script: str, *paths: Path) -> dict:
    module_paths = paths or (MANUAL_INPUT_JS,)
    completed = subprocess.run(
        ["node", "-e", script, *(str(path) for path in module_paths)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


class ManualInputTests(unittest.TestCase):
    def test_axis_normalization_uses_configured_range_and_clamps(self):
        result = run_node(
            """
const input = require(process.argv[1]);
console.log(JSON.stringify({
  low: input.normalizeAxis(-100, 0, 255, false, 0, 'linear', 1.5),
  middle: input.normalizeAxis(127.5, 0, 255, false, 0, 'linear', 1.5),
  high: input.normalizeAxis(999, 0, 255, false, 0, 'linear', 1.5)
}));
"""
        )
        self.assertEqual(0.0, result["low"])
        self.assertAlmostEqual(0.5, result["middle"], places=9)
        self.assertEqual(1.0, result["high"])

    def test_inverted_axis_and_dead_zone_preserve_full_travel(self):
        result = run_node(
            """
const input = require(process.argv[1]);
console.log(JSON.stringify({
  invertedRest: input.normalizeAxis(255, 0, 255, true, 0.02, 'linear', 1.5),
  invertedFull: input.normalizeAxis(0, 0, 255, true, 0.02, 'linear', 1.5),
  jitter: input.normalizeAxis(3, 0, 255, false, 0.02, 'linear', 1.5),
  middle: input.normalizeAxis(127.5, 0, 255, false, 0.02, 'linear', 1.5)
}));
"""
        )
        self.assertEqual(0.0, result["invertedRest"])
        self.assertEqual(1.0, result["invertedFull"])
        self.assertEqual(0.0, result["jitter"])
        self.assertAlmostEqual((0.5 - 0.02) / 0.98, result["middle"], places=9)

    def test_progressive_curve_uses_adjustable_gamma(self):
        result = run_node(
            """
const input = require(process.argv[1]);
console.log(JSON.stringify({
  linear: input.normalizeAxis(0.5, 0, 1, false, 0, 'linear', 1.5),
  progressive: input.normalizeAxis(0.5, 0, 1, false, 0, 'progressive', 1.5),
  full: input.normalizeAxis(1, 0, 1, false, 0, 'progressive', 2.5)
}));
"""
        )
        self.assertAlmostEqual(0.5, result["linear"], places=9)
        self.assertAlmostEqual(0.5**1.5, result["progressive"], places=9)
        self.assertEqual(1.0, result["full"])

    def test_switching_input_source_immediately_clears_both_pedals(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('manual', [1]);
model.handle('keyboard_throttle', [0.75]);
model.handle('keyboard_brake', [0.25]);
const before = model.snapshot();
const events = model.handle('source', ['gamepad']);
console.log(JSON.stringify({before, after: model.snapshot(), events}));
"""
        )
        self.assertEqual(0.75, result["before"]["throttle"])
        self.assertEqual(0.25, result["before"]["brake"])
        self.assertEqual(0.0, result["after"]["throttle"])
        self.assertEqual(0.0, result["after"]["brake"])
        self.assertIn(["throttle", 0], result["events"])
        self.assertIn(["brake", 0], result["events"])

    def test_selected_gamepad_axes_map_to_pedals_and_other_elements_are_ignored(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('manual', [1]);
model.handle('source', ['gamepad']);
model.handle('throttle_axis', [7]);
model.handle('throttle_min', [0]);
model.handle('throttle_max', [255]);
model.handle('brake_axis', [9]);
model.handle('brake_min', [-32768]);
model.handle('brake_max', [32767]);
model.handle('dead_zone', [0]);
model.handle('smoothing_ms', [0]);
model.handle('hid', [6, 255]);
const ignored = model.snapshot();
model.handle('hid', [7, 127.5]);
model.handle('hid', [9, 0]);
console.log(JSON.stringify({ignored, mapped: model.snapshot()}));
"""
        )
        self.assertEqual(0.0, result["ignored"]["throttle"])
        self.assertEqual(0.0, result["ignored"]["brake"])
        self.assertAlmostEqual(0.5, result["mapped"]["throttle"], places=9)
        self.assertAlmostEqual(32768 / 65535, result["mapped"]["brake"], places=9)

    def test_progressive_curve_is_throttle_only_and_debug_separates_both_pedals(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('manual', [1]);
model.handle('source', ['gamepad']);
model.handle('throttle_axis', [4]);
model.handle('brake_axis', [5]);
model.handle('dead_zone', [0]);
model.handle('curve', ['progressive']);
model.handle('gamma', [2]);
model.handle('smoothing_ms', [0]);
const throttleEvents = model.handle('hid', [4, 0.5]);
const brakeEvents = model.handle('hid', [5, 0.5]);
console.log(JSON.stringify({throttleEvents, brakeEvents, state: model.snapshot()}));
"""
        )
        self.assertAlmostEqual(0.25, result["state"]["throttle"], places=9)
        self.assertAlmostEqual(0.5, result["state"]["brake"], places=9)
        self.assertIn(["throttle_normalized", 0.25], result["throttleEvents"])
        self.assertIn(["brake_normalized", 0.5], result["brakeEvents"])

    def test_gamepad_smoothing_is_fast_but_does_not_jump(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('manual', [1]);
model.handle('source', ['gamepad']);
model.handle('throttle_axis', [4]);
model.handle('dead_zone', [0]);
model.handle('smoothing_ms', [40]);
model.handle('hid', [4, 1]);
const before = model.snapshot().throttle;
model.tick(0.01);
const first = model.snapshot().throttle;
for (let i = 0; i < 40; i += 1) model.tick(0.01);
console.log(JSON.stringify({before, first, settled: model.snapshot().throttle}));
"""
        )
        self.assertEqual(0.0, result["before"])
        self.assertGreater(result["first"], 0.20)
        self.assertLess(result["first"], 0.30)
        self.assertGreater(result["settled"], 0.999)

    def test_leaving_manual_mode_releases_and_ignores_gamepad_input(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('manual', [1]);
model.handle('source', ['gamepad']);
model.handle('throttle_axis', [4]);
model.handle('smoothing_ms', [0]);
model.handle('hid', [4, 1]);
const active = model.snapshot();
const release = model.handle('manual', [0]);
model.handle('hid', [4, 1]);
model.tick(0.01);
console.log(JSON.stringify({active, release, inactive: model.snapshot()}));
"""
        )
        self.assertEqual(1.0, result["active"]["throttle"])
        self.assertIn(["throttle", 0], result["release"])
        self.assertIn(["brake", 0], result["release"])
        self.assertEqual(0.0, result["inactive"]["throttle"])
        self.assertEqual(0.0, result["inactive"]["brake"])

    def test_learn_selects_the_axis_with_the_largest_observed_travel(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('learn_throttle', [1]);
model.handle('hid', [4, 0]);
model.handle('hid', [7, 100]);
model.handle('hid', [4, 255]);
model.handle('hid', [7, 120]);
const events = model.handle('learn_commit', ['throttle']);
console.log(JSON.stringify({events, learned: model.snapshot()}));
"""
        )
        self.assertEqual(4, result["learned"]["throttleAxis"])
        self.assertEqual(0, result["learned"]["throttleMin"])
        self.assertEqual(255, result["learned"]["throttleMax"])
        self.assertIn(["throttle_axis", 4], result["events"])

    def test_gamepad_activity_cannot_change_internal_auto_drive_behavior(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const drive = require(process.argv[2]);
function trace(withGamepadNoise) {
  const model = new drive.DriveModel('v10');
  const manual = new input.ManualInputModel();
  model.handle('ignition', [1]);
  model.handle('start', [1]);
  model.handle('auto', [1]);
  manual.handle('source', ['gamepad']);
  manual.handle('throttle_axis', [4]);
  for (let index = 0; index < 600; index += 1) {
    if (withGamepadNoise) {
      manual.handle('hid', [4, index % 2]);
      for (const event of manual.tick(0.01)) {
        if (event[0] === 'throttle' || event[0] === 'brake') {
          model.handle(event[0], [event[1]]);
        }
      }
    }
    model.tick(0.02);
  }
  return model.snapshot();
}
console.log(JSON.stringify({baseline: trace(false), noisy: trace(true)}));
""",
            MANUAL_INPUT_JS,
            DRIVE_MODEL_JS,
        )
        self.assertEqual(result["baseline"], result["noisy"])

    def test_keyboard_fallback_remains_exclusive_to_keyboard_source(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('manual', [1]);
model.handle('keyboard_throttle', [0.6]);
const keyboard = model.snapshot();
model.handle('source', ['gamepad']);
model.handle('keyboard_throttle', [1]);
const gamepad = model.snapshot();
model.handle('source', ['keyboard']);
model.handle('keyboard_throttle', [0.4]);
console.log(JSON.stringify({keyboard, gamepad, restored: model.snapshot()}));
"""
        )
        self.assertEqual(0.6, result["keyboard"]["throttle"])
        self.assertEqual(0.0, result["gamepad"]["throttle"])
        self.assertEqual(0.4, result["restored"]["throttle"])

    def test_generated_manual_input_is_the_only_manual_pedal_adapter(self):
        source = MANUAL_INPUT_JS.read_text()
        self.assertIn("inlets = 1;\noutlets = 3;", source)
        self.assertNotIn("if (typeof inlets", source)

        manual = json.loads((ROOT / "patchers" / "manual_input.maxpat").read_text())["patcher"]
        manual_text = "\n".join(item["box"].get("text", "") for item in manual["boxes"])
        manual_names = [item["box"].get("name", "") for item in manual["boxes"]]
        for token in (
            "hi",
            "js Patcher:/code/manual_input.js",
            "Keyboard",
            "Gamepad",
            "Learn Throttle",
            "Throttle Axis",
            "Brake Axis",
            "Throttle Norm",
            "Brake Norm",
            "Dead Zone",
            "Smoothing ms",
            "Progressive",
        ):
            self.assertIn(token, manual_text)
        self.assertTrue(any(name.endswith("/patchers/keyboard_drive_ws.maxpat") for name in manual_names))

        for label in ("EV", "V10", "V12"):
            runtime = json.loads((ROOT / f"VehicleSoundSynth-{label}.maxpat").read_text())["patcher"]
            names = [item["box"].get("name", "") for item in runtime["boxes"]]
            self.assertTrue(any(name.endswith("/patchers/manual_input.maxpat") for name in names))
            self.assertFalse(any(name.endswith("/patchers/keyboard_drive_ws.maxpat") for name in names))

        project = json.loads((ROOT / "VehicleSoundSynth-V5.maxproj").read_text())
        self.assertIn("patchers/manual_input.maxpat", project["contents"]["patchers"])
        self.assertIn("code/manual_input.js", project["contents"]["code"])


if __name__ == "__main__":
    unittest.main()
