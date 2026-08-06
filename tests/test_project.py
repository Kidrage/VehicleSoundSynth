import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VehicleSoundProjectTests(unittest.TestCase):
    def load_json(self, relative_path):
        with (ROOT / relative_path).open(encoding="utf-8") as handle:
            return json.load(handle)

    def test_runnable_project_has_public_engine_interface(self):
        required = [
            "VehicleSoundSynth.maxproj",
            "main.maxpat",
            "patchers/vehicle_engine~.maxpat",
        ]
        for relative_path in required:
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)

        engine = self.load_json("patchers/vehicle_engine~.maxpat")
        boxes = [item["box"] for item in engine["patcher"]["boxes"]]
        self.assertEqual(1, sum(box.get("maxclass") == "inlet" for box in boxes))
        self.assertEqual(2, sum(box.get("maxclass") == "outlet" for box in boxes))

    def test_all_generated_patchers_are_valid_max_json(self):
        patchers = list(ROOT.glob("*.maxpat")) + list((ROOT / "patchers").glob("*.maxpat"))
        self.assertGreaterEqual(len(patchers), 7)
        for path in patchers:
            data = self.load_json(path.relative_to(ROOT))
            self.assertEqual(1, data["patcher"]["fileversion"], path.name)
            self.assertIn("boxes", data["patcher"], path.name)
            self.assertIn("lines", data["patcher"], path.name)

    def test_three_distinct_presets_and_macro_contract(self):
        presets = self.load_json("presets/sound_dna.json")
        self.assertEqual({"Future EV", "High-Rev V12", "Aggressive V10"}, set(presets))
        expected = {"ev_weight", "v12_weight", "v10_weight", "aggression", "brightness", "body", "texture", "cabin_width"}
        for values in presets.values():
            self.assertEqual(expected, set(values))
            self.assertTrue(all(0.0 <= value <= 1.0 for value in values.values()))

    def test_engine_accepts_the_documented_state_and_macro_messages(self):
        engine = self.load_json("patchers/vehicle_engine~.maxpat")
        texts = "\n".join(item["box"].get("text", "") for item in engine["patcher"]["boxes"])
        for name in ("speed_kph", "rpm", "throttle", "brake", "load", "accel", "gear", "shift"):
            self.assertIn(name, texts)
        for name in ("ev_weight", "v12_weight", "v10_weight", "aggression", "brightness", "body", "texture", "cabin_width"):
            self.assertIn(name, texts)

    def test_transient_media_are_small_48khz_mono_wave_files(self):
        import wave

        for name in ("shift_thump.wav", "exhaust_pop.wav", "mechanical_click.wav"):
            path = ROOT / "media" / name
            self.assertTrue(path.is_file(), name)
            with wave.open(str(path), "rb") as wav:
                self.assertEqual(1, wav.getnchannels())
                self.assertEqual(48000, wav.getframerate())
                self.assertLess(wav.getnframes(), 24000)

    def test_output_chain_contains_peak_protection_and_starts_muted(self):
        cabin = self.load_json("patchers/cabin_master~.maxpat")
        cabin_boxes = {item["box"]["id"]: item["box"] for item in cabin["patcher"]["boxes"]}
        cabin_text = "\n".join(box.get("text", "") for box in cabin_boxes.values())
        self.assertIn("omx.peaklim~", cabin_text)
        self.assertIn("clip~ -0.891 0.891", cabin_text)
        cabin_cords = {
            (line["patchline"]["source"][0], line["patchline"]["destination"][0])
            for line in cabin["patcher"]["lines"]
        }
        limiter = next(box["id"] for box in cabin_boxes.values() if box.get("text") == "omx.peaklim~")
        clippers = {box["id"] for box in cabin_boxes.values() if box.get("text") == "clip~ -0.891 0.891"}
        outlets = {box["id"] for box in cabin_boxes.values() if box["maxclass"] == "outlet"}
        self.assertEqual(2, len(clippers))
        self.assertTrue(all((limiter, clipper) in cabin_cords for clipper in clippers))
        self.assertTrue(all(any((clipper, outlet) in cabin_cords for outlet in outlets) for clipper in clippers))

        main = self.load_json("main.maxpat")
        main_boxes = {item["box"]["id"]: item["box"] for item in main["patcher"]["boxes"]}
        main_text = "\n".join(box.get("text", "") for box in main_boxes.values())
        self.assertIn("Audio starts OFF", main_text)
        main_cords = {
            (line["patchline"]["source"][0], line["patchline"]["destination"][0])
            for line in main["patcher"]["lines"]
        }
        toggles = {box["id"] for box in main_boxes.values() if box["maxclass"] == "toggle"}
        loads = {box["id"] for box in main_boxes.values() if box.get("text") == "loadmess 0"}
        dacs = {box["id"] for box in main_boxes.values() if box["maxclass"] == "ezdac~"}
        self.assertTrue(any((load, toggle) in main_cords for load in loads for toggle in toggles))
        self.assertTrue(any((toggle, dac) in main_cords for toggle in toggles for dac in dacs))

    def test_generated_patchers_use_max_compatible_objects_and_syntax(self):
        patchers = list(ROOT.glob("*.maxpat")) + list((ROOT / "patchers").glob("*.maxpat"))
        for path in patchers:
            boxes = [item["box"] for item in self.load_json(path.relative_to(ROOT))["patcher"]["boxes"]]
            texts = [box.get("text", "") for box in boxes]
            object_names = {text.split(" ", 1)[0] for text in texts if text}
            self.assertNotIn("selector", object_names, path.name)
            self.assertNotIn("hip~", object_names, path.name)
            self.assertFalse(any(text.startswith("expr if(") for text in texts), path.name)
            self.assertNotIn("; dsp $1", texts, path.name)
            self.assertNotIn("slide 0. 3 12", texts, path.name)

    def test_patch_cords_reference_real_boxes_and_valid_ports(self):
        patchers = list(ROOT.glob("*.maxpat")) + list((ROOT / "patchers").glob("*.maxpat"))
        for path in patchers:
            patcher = self.load_json(path.relative_to(ROOT))["patcher"]
            boxes = {item["box"]["id"]: item["box"] for item in patcher["boxes"]}
            self.assertEqual(len(patcher["boxes"]), len(boxes), path.name)
            for item in patcher["lines"]:
                line = item["patchline"]
                source_id, source_outlet = line["source"]
                destination_id, destination_inlet = line["destination"]
                self.assertIn(source_id, boxes, f"{path.name}: {source_id}")
                self.assertIn(destination_id, boxes, f"{path.name}: {destination_id}")
                self.assertLess(source_outlet, boxes[source_id]["numoutlets"], path.name)
                self.assertLess(destination_inlet, boxes[destination_id]["numinlets"], path.name)

    def test_gen_patchers_expose_bounded_required_parameters(self):
        required = {"rpm", "throttle", "load", "aggression", "brightness", "body", "texture"}
        gen_paths = sorted((ROOT / "gen").glob("*.gendsp"))
        self.assertEqual(3, len(gen_paths))
        for path in gen_paths:
            patcher = self.load_json(path.relative_to(ROOT))["patcher"]
            code = "\n".join(
                item["box"].get("code", item["box"].get("text", ""))
                for item in patcher["boxes"]
            )
            for name in required:
                self.assertIn(f"Param {name}", code, path.name)
            self.assertIn("clamp(", code, path.name)
            self.assertIn("cycle(", code, path.name)

            boxes = {item["box"]["id"]: item["box"] for item in patcher["boxes"]}
            output_ids = {
                box_id for box_id, box in boxes.items()
                if box.get("text") in {"out 1", "out 2"}
            }
            self.assertEqual(2, len(output_ids), path.name)
            destinations = {
                line["patchline"]["destination"][0]
                for line in patcher["lines"]
            }
            self.assertTrue(output_ids.issubset(destinations), path.name)

    def test_project_search_path_schema_and_runtime_resources_are_declared(self):
        project = self.load_json("VehicleSoundSynth.maxproj")
        # Max 8.6.x expects a dictionary here and can crash while opening a
        # project whose searchpath is encoded as an array. Explicit relative
        # paths avoid collisions with Max's own patchers/gen/media folders.
        self.assertEqual(
            {
                name: {"path": f"./{name}", "recursive": 1}
                for name in ("patchers", "gen", "media", "presets")
            },
            project["searchpath"],
        )
        self.assertEqual({"patchers", "code", "media", "data"}, set(project["contents"]))
        declared = {
            relative_path
            for category in project["contents"].values()
            for relative_path in category
        }
        required = {
            "main.maxpat",
            "patchers/vehicle_engine~.maxpat",
            "patchers/powertrain~.maxpat",
            "patchers/transient~.maxpat",
            "patchers/road_air~.maxpat",
            "patchers/cabin_master~.maxpat",
            "patchers/drive_simulator.maxpat",
            "gen/ev_powertrain.gendsp",
            "gen/v12_powertrain.gendsp",
            "gen/v10_powertrain.gendsp",
            "media/shift_thump.wav",
            "media/exhaust_pop.wav",
            "media/mechanical_click.wav",
            "presets/sound_dna.json",
        }
        self.assertTrue(required.issubset(declared))
        for relative_path in declared:
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_demo_ui_and_engine_deep_modules_cover_the_mvp(self):
        main = self.load_json("main.maxpat")
        main_text = "\n".join(item["box"].get("text", "") for item in main["patcher"]["boxes"])
        for text in (
            "Internal Manual",
            "Internal Auto",
            "External vss.input",
            "Future EV",
            "High-Rev V12",
            "Aggressive V10",
            "Aggression",
            "Brightness",
            "Body",
            "Texture",
            "Cabin Width",
            "meter~",
            "spectroscope~",
        ):
            self.assertIn(text, main_text)

        engine = self.load_json("patchers/vehicle_engine~.maxpat")
        engine_text = "\n".join(item["box"].get("text", "") for item in engine["patcher"]["boxes"])
        for abstraction in ("powertrain~", "transient~", "road_air~", "cabin_master~"):
            self.assertIn(abstraction, engine_text)

    def test_demo_opens_with_visible_controls_and_internal_source_selected(self):
        patcher = self.load_json("main.maxpat")["patcher"]
        self.assertEqual(0, patcher["openinpresentation"])
        boxes = {item["box"]["id"]: item["box"] for item in patcher["boxes"]}
        mode = next(
            box for box in boxes.values()
            if box["maxclass"] == "umenu" and "Internal Manual" in box.get("items", [])
        )
        incoming = [
            line["patchline"]["source"][0]
            for line in patcher["lines"]
            if line["patchline"]["destination"][0] == mode["id"]
        ]
        self.assertTrue(any(boxes[source].get("text") == "loadmess 0" for source in incoming))

    def test_generator_is_deterministic(self):
        def build_and_hash(destination):
            subprocess.run(
                [sys.executable, str(ROOT / "tools" / "build_project.py"), "--output-root", str(destination)],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            hashes = {}
            for path in sorted(item for item in destination.rglob("*") if item.is_file()):
                hashes[str(path.relative_to(destination))] = hashlib.sha256(path.read_bytes()).hexdigest()
            return hashes

        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_hashes = build_and_hash(Path(first))
            second_hashes = build_and_hash(Path(second))
        self.assertEqual(first_hashes, second_hashes)
        self.assertIn("main.maxpat", first_hashes)


if __name__ == "__main__":
    unittest.main()
