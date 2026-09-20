"""Ferrari V5 structural contracts. Native Max/listening acceptance is separate."""
import copy
import json
import subprocess
import unittest
from pathlib import Path

from tools import build_project as b, ferrari_sf90_v5 as v5

ROOT = Path(__file__).resolve().parents[1]


def boxes(doc):
    return {x["box"]["id"]: x["box"] for x in doc["patcher"]["boxes"]}


class FerrariSf90V5Tests(unittest.TestCase):
    def test_source_is_v4_bypass_plus_deterministic_structure(self):
        old = b.GEN_CODE["ferrari_dna_source_v4"]
        new = b.GEN_CODE["ferrari_dna_source_v5"]
        self.assertIn("Param sf90_material(1", new)
        for hz in (123, 185, 214, 240, 620, 820, 1100):
            self.assertIn(f"*{hz}/samplerate", new)
        self.assertEqual(old.count("noise()"), new.count("noise()"))
        tail = new[new.index("// Ferrari V5:"):]
        self.assertNotIn("noise()", tail)
        for i in range(8, 11):
            old_line = next(x for x in old.splitlines() if x.startswith(f"out{i} ="))
            self.assertIn(old_line, new)
        for i in range(1, 5):
            self.assertIn(f"sf_old{i} =", new)
            self.assertIn(f"out{i} = sf_old{i}+sf_mix*", new)

    def test_reference_targets_are_traceable_not_runtime_audio(self):
        target = json.loads((ROOT / "assets/ferrari_sf90_acoustic_target.json").read_text())
        interp = json.loads((ROOT / "assets/ferrari_sf90_v10_interpretation_targets.json").read_text())
        self.assertAlmostEqual(target["idle_window_1_to_5_seconds"]["dominant_frequency_hz"], 61.5)
        self.assertGreater(target["idle_window_1_to_5_seconds"]["low_mid_ratio_40_to_500_hz"], .9)
        self.assertGreater(target["idle_window_1_to_5_seconds"]["rumble_ratio_40_to_160_hz"], .8)
        self.assertFalse(interp["source_policy"]["runtime_audio_dependency"])
        self.assertEqual(interp["dna_bands"]["body_hz"], [120.0, 250.0])
        self.assertEqual(interp["dna_bands"]["cavity_hz"], [250.0, 600.0])

    def test_acoustic_keeps_one_source_and_independent_noise(self):
        doc = v5.make_acoustic()
        bs = boxes(doc)
        gen = [x for x in bs.values() if x.get("text", "").startswith("gen~")]
        self.assertEqual(len(gen), 1)
        self.assertIn("ferrari_dna_source_v5.gendsp", gen[0]["text"])
        noise = next(x for x in bs.values() if x.get("text") == "vehicle_noise_ferrari_v2~")
        inputs = [x["patchline"]["source"] for x in doc["patcher"]["lines"]
                  if x["patchline"]["destination"][0] == noise["id"]]
        self.assertIn([gen[0]["id"], 7], inputs)
        self.assertIn([gen[0]["id"], 8], inputs)
        self.assertIn([gen[0]["id"], 9], inputs)

    def test_designer_has_v5_control_and_fresh_state(self):
        doc = v5.make_designer()
        bs = boxes(doc)
        self.assertEqual(bs["sf90-route"]["text"], "route sf90_material")
        self.assertEqual(bs["sf90-tag"]["text"], "prepend sf90_material")
        self.assertEqual(bs["sf90-value"]["varname"], "sf90_material")
        self.assertIn("ferrari_v5_state.js",
                      next(x.get("text", "") for x in bs.values()
                           if x.get("text", "").startswith("js ") and "state" in x.get("text", "")))
        storage = next(x["text"] for x in bs.values()
                       if x.get("text", "").startswith("pattrstorage "))
        self.assertIn("ferrari_sound_dna_v5", storage)
        self.assertNotIn("ferrari_sound_dna_v4 ", storage)

    def test_factory_uses_reference_aligned_defaults(self):
        data = v5.factory()["pattrstorage"]["slots"]["99"]["data"]
        for key, value in v5.FACTORY_MACROS.items():
            self.assertEqual(data[key], [value])
        self.assertEqual(v5.factory()["pattrstorage"]["name"], "ferrari_sound_dna_v5")

    def test_state_never_writes_v4(self):
        script = r"""
const s=require('./code/ferrari_v5_state.js');
const p=s.paths('/qa/patchers/ferrari_dna_v5_designer~.maxpat');
const f={v3_body:[.72],sf90_material:[1],reference_restore:[1]};
const m=s.merge(f,{v3_body:[.4],sf90_material:[.3],unknown:[1]});
console.log(JSON.stringify({p:p,m:m}));
"""
        result = json.loads(subprocess.check_output(["node", "-e", script], cwd=ROOT, text=True))
        self.assertTrue(result["p"]["local"].endswith("ferrari_sound_dna_v5.json"))
        self.assertNotIn("v4", result["p"]["local"])
        self.assertEqual(result["m"]["v3_body"], [.4])
        self.assertEqual(result["m"]["sf90_material"], [.3])
        source = (ROOT / "code/ferrari_v5_state.js").read_text()
        self.assertNotIn("ferrari_sound_dna_v4.json", source)

    def test_active_engine_changes_only_ferrari_voice_from_checkpoint(self):
        current = copy.deepcopy(b.make_profile_engine("ferrari"))
        old = json.loads(subprocess.check_output(
            ["git", "show", v5.BASELINE + ":patchers/vehicle_engine_ferrari~.maxpat"],
            cwd=ROOT))
        count = 0
        for box in boxes(current).values():
            if box.get("text") == "ferrari_acoustic_v5~":
                box["text"] = "ferrari_acoustic_v4~"
                count += 1
        self.assertEqual(count, 1)
        self.assertEqual(current, old)

    def test_ioniq_runtime_resources_are_byte_identical_to_checkpoint(self):
        names = subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", v5.BASELINE, "gen", "patchers", "presets", "code"],
            cwd=ROOT, text=True).splitlines()
        candidates = [n for n in names if "ioniq6n" in n or "ioniq_weight" in n]
        self.assertGreater(len(candidates), 15)
        for name in candidates:
            self.assertEqual((ROOT / name).read_bytes(),
                             subprocess.check_output(["git", "show", v5.BASELINE + ":" + name], cwd=ROOT),
                             name)

    def test_generation_is_deterministic(self):
        self.assertEqual(v5.outputs(), v5.outputs())


if __name__ == "__main__":
    unittest.main()
