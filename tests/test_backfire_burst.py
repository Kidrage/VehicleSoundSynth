import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BURST_JS = ROOT / "code" / "backfire_burst.js"


def run_node(script: str) -> dict:
    completed = subprocess.run(
        ["node", "-e", script, str(BURST_JS)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


class BackfireBurstTests(unittest.TestCase):
    def test_seeded_plans_keep_count_spacing_pitch_and_gain_in_contract(self):
        result = run_node(
            r"""
const burst = require(process.argv[1]);
const counts = {};
const plans = [];
for (let seed = 1; seed <= 200; seed += 1) {
  const plan = new burst.BurstPlanner(seed).createPlan();
  counts[plan.length] = (counts[plan.length] || 0) + 1;
  plans.push(plan);
}
console.log(JSON.stringify({counts, plans}));
"""
        )
        self.assertEqual({"1", "2", "3", "4", "5"}, set(result["counts"]))
        expected_gains = (1.0, 0.82, 0.70, 0.60, 0.52)
        for plan in result["plans"]:
            self.assertGreaterEqual(len(plan), 1)
            self.assertLessEqual(len(plan), 5)
            self.assertGreaterEqual(plan[0]["pitchSemitones"], -0.4)
            self.assertLessEqual(plan[0]["pitchSemitones"], 0.4)
            self.assertEqual(0, plan[0]["delayMs"])
            for index, hit in enumerate(plan):
                self.assertEqual(index, hit["index"])
                self.assertEqual(len(plan), hit["count"])
                self.assertAlmostEqual(expected_gains[index], hit["gain"], places=9)
                if index:
                    self.assertGreaterEqual(hit["delayMs"], 140)
                    self.assertLessEqual(hit["delayMs"], 200)
                    base = -1.25 * index
                    self.assertGreaterEqual(hit["pitchSemitones"], max(-6.0, base - 0.65))
                    self.assertLessEqual(hit["pitchSemitones"], min(0.5, base + 0.65))

    def test_same_seed_is_reproducible_but_seeds_change_the_plan(self):
        result = run_node(
            r"""
const burst = require(process.argv[1]);
const first = new burst.BurstPlanner(1219).createPlan();
const repeated = new burst.BurstPlanner(1219).createPlan();
const different = new burst.BurstPlanner(1017).createPlan();
console.log(JSON.stringify({first, repeated, different}));
"""
        )
        self.assertEqual(result["first"], result["repeated"])
        self.assertNotEqual(result["first"], result["different"])

    def test_retrigger_cancels_every_pending_hit_from_the_old_burst(self):
        result = run_node(
            r"""
const created = [];
global.outlet = function () {};
global.Task = function (callback) {
  this.callback = callback;
  this.cancelled = false;
  this.schedule = function (delay) { this.delay = delay; created.push(this); };
  this.cancel = function () { this.cancelled = true; };
};
const burst = require(process.argv[1]);
burst.seed(1219);
burst.runBurst(1.0);
const oldTasks = created.slice();
burst.runBurst(1.0);
console.log(JSON.stringify({
  oldCount: oldTasks.length,
  allCancelled: oldTasks.every(task => task.cancelled),
  newCount: created.length - oldTasks.length
}));
"""
        )
        self.assertGreater(result["oldCount"], 0)
        self.assertTrue(result["allCancelled"])
        self.assertGreaterEqual(result["newCount"], 0)


if __name__ == "__main__":
    unittest.main()
