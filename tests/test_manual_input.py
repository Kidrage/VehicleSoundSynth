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
    def test_gamepad_trigger_normalization_clamps_and_rescales_dead_zone(self):
        result = run_node(
            """
const input = require(process.argv[1]);
console.log(JSON.stringify({
  low: input.normalizeTrigger(-100, 0.02, false),
  jitter: input.normalizeTrigger(0.01, 0.02, false),
  middle: input.normalizeTrigger(0.51, 0.02, false),
  high: input.normalizeTrigger(999, 0.02, false),
  signedRest: input.normalizeTrigger(-1, 0.02, true),
  signedFull: input.normalizeTrigger(1, 0.02, true)
}));
"""
        )
        self.assertEqual(0.0, result["low"])
        self.assertEqual(0.0, result["jitter"])
        self.assertAlmostEqual(0.5, result["middle"], places=9)
        self.assertEqual(1.0, result["high"])
        self.assertEqual(0.0, result["signedRest"])
        self.assertEqual(1.0, result["signedFull"])

    def test_signed_trigger_range_is_detected_without_axis_learning(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('manual', [1]);
model.handle('source', ['gamepad']);
model.handle('dead_zone', [0]);
model.handle('smoothing_ms', [0]);
model.handle('axis_left_trigger', [-1]);
const rest = model.snapshot().throttle;
model.handle('axis_left_trigger', [0]);
const middle = model.snapshot().throttle;
model.handle('axis_left_trigger', [1]);
console.log(JSON.stringify({rest, middle, full: model.snapshot().throttle}));
"""
        )
        self.assertEqual(0.0, result["rest"])
        self.assertEqual(0.5, result["middle"])
        self.assertEqual(1.0, result["full"])

    def test_trigger_pedal_is_absolute_and_linear_not_frame_accumulated(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('manual', [1]);
model.handle('source', ['gamepad']);
model.handle('dead_zone', [0]);
model.handle('smoothing_ms', [0]);
model.handle('axis_left_trigger', [0.4]);
for (let i = 0; i < 100; i += 1) model.tick(0.01);
console.log(JSON.stringify(model.snapshot()));
"""
        )
        self.assertAlmostEqual(0.4, result["throttle"], places=9)
        self.assertAlmostEqual(0.4, result["throttleTarget"], places=9)

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
        self.assertEqual(0.0, result["before"]["throttle"])
        self.assertEqual(0.25, result["before"]["brake"])
        self.assertEqual(0.0, result["after"]["throttle"])
        self.assertEqual(0.0, result["after"]["brake"])
        self.assertIn(["throttle", 0], result["events"])
        self.assertIn(["brake", 0], result["events"])

    def test_fixed_left_and_right_triggers_map_directly_to_throttle_and_brake(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('manual', [1]);
model.handle('source', ['gamepad']);
model.handle('dead_zone', [0]);
model.handle('smoothing_ms', [0]);
model.handle('axis_left_x', [1]);
const ignored = model.snapshot();
const leftEvents = model.handle('axis_left_trigger', [0.5]);
const rightEvents = model.handle('axis_right_trigger', [0.75]);
console.log(JSON.stringify({ignored, leftEvents, rightEvents, mapped: model.snapshot()}));
"""
        )
        self.assertEqual(0.0, result["ignored"]["throttle"])
        self.assertEqual(0.0, result["ignored"]["brake"])
        self.assertAlmostEqual(0.5, result["mapped"]["throttle"], places=9)
        self.assertAlmostEqual(0.75, result["mapped"]["brake"], places=9)
        self.assertIn(["throttle_normalized", 0.5], result["leftEvents"])
        self.assertIn(["brake_normalized", 0.75], result["rightEvents"])

    def test_gamepad_debug_keeps_raw_and_normalized_pedals_separate(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('manual', [1]);
model.handle('source', ['gamepad']);
model.handle('dead_zone', [0]);
model.handle('smoothing_ms', [0]);
const throttleEvents = model.handle('axis_left_trigger', [0.5]);
const brakeEvents = model.handle('axis_right_trigger', [0.75]);
console.log(JSON.stringify({throttleEvents, brakeEvents, state: model.snapshot()}));
"""
        )
        self.assertAlmostEqual(0.5, result["state"]["throttle"], places=9)
        self.assertAlmostEqual(0.75, result["state"]["brake"], places=9)
        self.assertIn(["throttle_raw", 0.5], result["throttleEvents"])
        self.assertIn(["throttle_normalized", 0.5], result["throttleEvents"])
        self.assertIn(["brake_raw", 0.75], result["brakeEvents"])
        self.assertIn(["brake_normalized", 0.75], result["brakeEvents"])

    def test_gamepad_smoothing_is_fast_but_does_not_jump(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('manual', [1]);
model.handle('source', ['gamepad']);
model.handle('dead_zone', [0]);
model.handle('smoothing_ms', [30]);
model.handle('axis_left_trigger', [1]);
const before = model.snapshot().throttle;
model.tick(0.01);
const first = model.snapshot().throttle;
for (let i = 0; i < 40; i += 1) model.tick(0.01);
console.log(JSON.stringify({before, first, settled: model.snapshot().throttle}));
"""
        )
        self.assertEqual(0.0, result["before"])
        self.assertGreater(result["first"], 0.28)
        self.assertLess(result["first"], 0.29)
        self.assertGreater(result["settled"], 0.999)

    def test_leaving_manual_mode_releases_and_ignores_gamepad_input(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('manual', [1]);
model.handle('source', ['gamepad']);
model.handle('smoothing_ms', [0]);
model.handle('axis_left_trigger', [1]);
const active = model.snapshot();
const release = model.handle('manual', [0]);
model.handle('axis_left_trigger', [1]);
model.tick(0.01);
console.log(JSON.stringify({active, release, inactive: model.snapshot()}));
"""
        )
        self.assertEqual(1.0, result["active"]["throttle"])
        self.assertIn(["throttle", 0], result["release"])
        self.assertIn(["brake", 0], result["release"])
        self.assertEqual(0.0, result["inactive"]["throttle"])
        self.assertEqual(0.0, result["inactive"]["brake"])

    def test_gamepad_device_status_reports_analog_capability_and_disconnect_releases(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('manual', [1]);
model.handle('source', ['gamepad']);
model.handle('smoothing_ms', [0]);
const ds4 = model.handle('device_info', [91, 0, 'Wireless Controller', 'ps4']);
model.handle('axis_left_trigger', [1]);
const active = model.snapshot();
const disconnected = model.handle('gamepad_status', ['device_removed', 91]);
const pro = model.handle('device_info', [92, 0, 'Pro Controller', 'switch_pro']);
console.log(JSON.stringify({ds4, active, disconnected, pro, final: model.snapshot()}));
"""
        )
        self.assertIn(["detected", 1], result["ds4"])
        self.assertIn(["analog_warning", 0], result["ds4"])
        self.assertEqual(1.0, result["active"]["throttle"])
        self.assertIn(["throttle", 0], result["disconnected"])
        self.assertIn(["brake", 0], result["disconnected"])
        self.assertIn(["detected", 0], result["disconnected"])
        self.assertIn(["analog_warning", 1], result["pro"])
        self.assertEqual(0.0, result["final"]["throttle"])

    def test_inactive_gamepad_device_changes_cannot_release_keyboard_pedals(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('manual', [1]);
model.handle('keyboard_throttle', [0.8]);
const connected = model.handle('device_info', [91, 0, 'Wireless Controller', 'ps4']);
const afterConnect = model.snapshot();
const disconnected = model.handle('gamepad_status', ['device_removed', 91]);
console.log(JSON.stringify({connected, afterConnect, disconnected, final: model.snapshot()}));
"""
        )
        self.assertEqual(0.8, result["afterConnect"]["throttle"])
        self.assertEqual(0.8, result["final"]["throttle"])
        self.assertNotIn(["throttle", 0], result["connected"])
        self.assertNotIn(["throttle", 0], result["disconnected"])

    def test_gamepad_instance_hot_swap_releases_even_when_device_index_is_reused(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('manual', [1]);
model.handle('source', ['gamepad']);
model.handle('smoothing_ms', [0]);
model.handle('device_info', [91, 0, 'Wireless Controller', 'ps4']);
model.handle('axis_left_trigger', [1]);
const before = model.snapshot();
const events = model.handle('device_info', [92, 0, 'Replacement Controller', 'xbox']);
console.log(JSON.stringify({before, events, after: model.snapshot()}));
"""
        )
        self.assertEqual(1.0, result["before"]["throttle"])
        self.assertIn(["throttle", 0], result["events"])
        self.assertIn(["brake", 0], result["events"])
        self.assertEqual(0.0, result["after"]["throttle"])
        self.assertEqual(92, result["after"]["deviceInstance"])

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
  for (let index = 0; index < 600; index += 1) {
    if (withGamepadNoise) {
      manual.handle('axis_left_trigger', [index % 2]);
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

    def test_keyboard_pedals_are_immediate_and_brake_has_priority(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const model = new input.ManualInputModel();
model.handle('manual', [1]);
model.handle('keyboard_throttle', [1]);
const throttle = model.snapshot();
model.handle('keyboard_brake', [0.65]);
const overlap = model.snapshot();
model.handle('keyboard_brake', [0]);
const resumed = model.snapshot();
model.handle('keyboard_throttle', [0]);
console.log(JSON.stringify({throttle, overlap, resumed, released: model.snapshot()}));
"""
        )
        self.assertEqual(1.0, result["throttle"]["throttle"])
        self.assertEqual(0.0, result["overlap"]["throttle"])
        self.assertEqual(0.65, result["overlap"]["brake"])
        self.assertEqual(1.0, result["resumed"]["throttle"])
        self.assertEqual(0.0, result["released"]["throttle"])
        self.assertEqual(0.0, result["released"]["brake"])

    def test_fast_loaded_lift_off_emits_one_bounded_overrun_event(self):
        result = run_node(
            """
const drive = require(process.argv[1]);
function trace(profile) {
  const model = new drive.DriveModel(profile);
  model.handle('ignition', [1]);
  model.handle('start', [1]);
  for (let i = 0; i < 60; i += 1) model.tick(0.02);
  model.speed = 70;
  model.rpm = 4200;
  model.gear = profile === 'ev' ? 1 : 2;
  model.handle('throttle', [1]);
  let events = [];
  for (let i = 0; i < 20; i += 1) events.push(...model.tick(0.02));
  model.handle('throttle', [0]);
  for (let i = 0; i < 20; i += 1) events.push(...model.tick(0.02));
  return events.filter(event => event[0] === 'overrun');
}
console.log(JSON.stringify({v10: trace('v10'), v12: trace('v12'), ev: trace('ev')}));
""",
            DRIVE_MODEL_JS,
        )
        for profile in ("v10", "v12"):
            self.assertEqual(1, len(result[profile]))
            self.assertGreaterEqual(result[profile][0][1], 0.35)
            self.assertLessEqual(result[profile][0][1], 1.0)
        self.assertEqual([], result["ev"])

    def test_overrun_rejects_slow_release_low_rpm_and_brake_only(self):
        result = run_node(
            """
const drive = require(process.argv[1]);
function prepared() {
  const model = new drive.DriveModel('v10');
  model.handle('ignition', [1]);
  model.handle('start', [1]);
  for (let i = 0; i < 60; i += 1) model.tick(0.02);
  model.speed = 70;
  model.rpm = 4200;
  model.gear = 2;
  model.handle('throttle', [1]);
  for (let i = 0; i < 20; i += 1) model.tick(0.02);
  return model;
}
function overruns(events) { return events.filter(event => event[0] === 'overrun'); }
let slow = prepared();
let slowEvents = [];
for (let i = 19; i >= 0; i -= 1) {
  slow.handle('throttle', [i / 20]);
  slowEvents.push(...slow.tick(0.02));
}
let low = prepared();
low.speed = 0;
low.gear = 1;
low.rpm = 1300;
low.handle('throttle', [0]);
let lowEvents = low.tick(0.02);
let braking = prepared();
braking.handle('brake', [0.65]);
let brakeEvents = braking.tick(0.02);
console.log(JSON.stringify({
  slow: overruns(slowEvents),
  low: overruns(lowEvents),
  braking: overruns(brakeEvents)
}));
""",
            DRIVE_MODEL_JS,
        )
        self.assertEqual([], result["slow"])
        self.assertEqual([], result["low"])
        self.assertEqual([], result["braking"])

    def test_smoothed_gamepad_lift_off_reaches_the_same_overrun_seam(self):
        result = run_node(
            """
const input = require(process.argv[1]);
const drive = require(process.argv[2]);
const manual = new input.ManualInputModel();
const model = new drive.DriveModel('v10');
model.handle('ignition', [1]);
model.handle('start', [1]);
for (let i = 0; i < 60; i += 1) model.tick(0.02);
model.speed = 70;
model.rpm = 4200;
model.gear = 2;
manual.handle('manual', [1]);
manual.handle('source', ['gamepad']);
manual.handle('dead_zone', [0]);
manual.handle('smoothing_ms', [30]);
function step(events) {
  for (let j = 0; j < 2; j += 1) {
    for (const event of manual.tick(0.01)) {
      if (event[0] === 'throttle' || event[0] === 'brake') {
        model.handle(event[0], [event[1]]);
      }
    }
  }
  events.push(...model.tick(0.02));
}
let events = [];
manual.handle('axis_left_trigger', [1]);
for (let i = 0; i < 50; i += 1) step(events);
manual.handle('axis_left_trigger', [0]);
for (let i = 0; i < 15; i += 1) step(events);
console.log(JSON.stringify(events.filter(event => event[0] === 'overrun')));
""",
            MANUAL_INPUT_JS,
            DRIVE_MODEL_JS,
        )
        self.assertEqual(1, len(result))
        self.assertGreaterEqual(result[0][1], 0.35)

    def test_progressive_service_brake_has_realistic_monotonic_stop_times(self):
        result = run_node(
            """
const drive = require(process.argv[1]);
function stopTime(brake) {
  const model = new drive.DriveModel('v10');
  model.handle('ignition', [1]);
  model.handle('start', [1]);
  for (let i = 0; i < 60; i += 1) model.tick(0.02);
  model.handle('throttle', [1]);
  for (let i = 0; i < 20000 && model.snapshot().speed < 100; i += 1) model.tick(0.02);
  model.handle('throttle', [0]);
  model.handle('brake', [brake]);
  let ticks = 0;
  while (model.snapshot().speed > 0 && ticks < 2000) {
    model.tick(0.02);
    ticks += 1;
  }
  return ticks * 0.02;
}
console.log(JSON.stringify({full: stopTime(1), half: stopTime(0.5), keyboard: stopTime(0.65)}));
""",
            DRIVE_MODEL_JS,
        )
        self.assertGreaterEqual(result["full"], 3.0)
        self.assertLessEqual(result["full"], 4.0)
        self.assertGreaterEqual(result["half"], 6.0)
        self.assertLessEqual(result["half"], 9.0)
        self.assertGreaterEqual(result["keyboard"], 5.0)
        self.assertLessEqual(result["keyboard"], 7.0)
        self.assertGreater(result["half"], result["keyboard"])
        self.assertGreater(result["keyboard"], result["full"])

    def test_natural_coast_settles_low_speed_but_preserves_high_speed_inertia(self):
        result = run_node(
            """
const drive = require(process.argv[1]);
function coastTime(fromSpeed, toSpeed) {
  const model = new drive.DriveModel('ev');
  model.handle('ignition', [1]);
  model.handle('start', [1]);
  for (let i = 0; i < 20; i += 1) model.tick(0.02);
  model.handle('throttle', [1]);
  for (let i = 0; i < 30000 && model.snapshot().speed < fromSpeed; i += 1) {
    model.tick(0.02);
  }
  model.handle('throttle', [0]);
  let ticks = 0;
  while (model.snapshot().speed > toSpeed && ticks < 10000) {
    model.tick(0.02);
    ticks += 1;
  }
  return ticks * 0.02;
}
console.log(JSON.stringify({
  low: coastTime(20, 0),
  high: coastTime(100, 80),
  veryHigh: coastTime(200, 180)
}));
""",
            DRIVE_MODEL_JS,
        )
        self.assertGreaterEqual(result["low"], 10.0)
        self.assertLessEqual(result["low"], 14.0)
        self.assertGreaterEqual(result["high"], 22.0)
        self.assertLessEqual(result["high"], 28.0)
        self.assertGreaterEqual(result["veryHigh"], 27.0)
        self.assertLessEqual(result["veryHigh"], 32.0)
        self.assertGreater(result["veryHigh"], result["high"])
        self.assertGreater(result["high"], result["low"])

    def test_natural_coast_curve_does_not_change_full_throttle_acceleration(self):
        result = run_node(
            """
const drive = require(process.argv[1]);
const speeds = {};
for (const profile of ['ev', 'v10', 'v12']) {
  const model = new drive.DriveModel(profile);
  model.handle('ignition', [1]);
  model.handle('start', [1]);
  for (let i = 0; i < 60; i += 1) model.tick(0.02);
  model.handle('throttle', [1]);
  for (let i = 0; i < 400; i += 1) model.tick(0.02);
  speeds[profile] = model.snapshot().speed;
}
console.log(JSON.stringify(speeds));
""",
            DRIVE_MODEL_JS,
        )
        for profile in ("ev", "v10", "v12"):
            self.assertAlmostEqual(192.99922998164607, result[profile], places=9)

    def test_generated_manual_input_is_the_only_manual_pedal_adapter(self):
        source = MANUAL_INPUT_JS.read_text()
        self.assertIn("inlets = 1;\noutlets = 3;", source)
        self.assertNotIn("if (typeof inlets", source)

        manual = json.loads((ROOT / "patchers" / "manual_input.maxpat").read_text())["patcher"]
        manual_text = "\n".join(item["box"].get("text", "") for item in manual["boxes"])
        manual_names = [item["box"].get("name", "") for item in manual["boxes"]]
        for token in (
            "gamepad",
            "js Patcher:/code/manual_input.js",
            "Keyboard",
            "Gamepad",
            "LT Throttle Raw",
            "RT Brake Raw",
            "Throttle Norm",
            "Brake Norm",
            "Dead Zone",
            "Smoothing ms",
            "Wireless Controller",
        ):
            self.assertIn(token, manual_text)
        for removed in ("\nhi\n", "Learn", " Axis", "Progressive", "Gamma", "Raw Min", "Raw Max"):
            self.assertNotIn(removed, manual_text)
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
