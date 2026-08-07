import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VehicleSoundProjectTests(unittest.TestCase):
    def load_json(self, relative_path):
        with (ROOT / relative_path).open(encoding="utf-8") as handle:
            return json.load(handle)

    def test_v2_project_identity_and_public_entrypoint(self):
        project_path = ROOT / "VehicleSoundSynth-V2.maxproj"
        self.assertTrue(project_path.is_file())
        project = self.load_json("VehicleSoundSynth-V2.maxproj")
        self.assertEqual("VehicleSoundSynth-V2", project["name"])
        self.assertTrue((ROOT / "main.maxpat").is_file())

    def test_v2_public_engine_contract_covers_lifecycle_events_and_master_eq(self):
        engine = self.load_json("patchers/vehicle_engine~.maxpat")
        text = "\n".join(item["box"].get("text", "") for item in engine["patcher"]["boxes"])
        for name in (
            "engine_type",
            "ignition",
            "start",
            "shift_dir",
            "intake_backfire",
            "exhaust_pop",
            "eq_low",
            "eq_lowmid",
            "eq_highmid",
            "eq_high",
            "eq_bypass",
            "master_trim_db",
        ):
            self.assertIn(name, text)

    def test_v2_engine_routes_through_lifecycle_and_final_mix_modules(self):
        engine = self.load_json("patchers/vehicle_engine~.maxpat")
        text = "\n".join(item["box"].get("text", "") for item in engine["patcher"]["boxes"])
        self.assertIn("engine_controller", text)
        self.assertIn("mix_master~", text)
        self.assertTrue((ROOT / "patchers" / "engine_controller.maxpat").is_file())
        self.assertTrue((ROOT / "patchers" / "mix_master~.maxpat").is_file())

    def test_v2_fuel_generators_expose_running_and_shift_envelopes(self):
        for name in ("v12_powertrain", "v10_powertrain"):
            patcher = self.load_json(f"gen/{name}.gendsp")["patcher"]
            code = "\n".join(item["box"].get("code", "") for item in patcher["boxes"])
            for parameter in ("engine_running", "combustion_gain", "shift_cut"):
                self.assertIn(f"Param {parameter}", code)
            self.assertIn("sub = cycle", code)
            self.assertIn("idle", code)

    def test_v2_internal_drive_model_exposes_seven_speed_dct_events(self):
        drive = self.load_json("patchers/drive_simulator.maxpat")
        text = "\n".join(item["box"].get("text", "") for item in drive["patcher"]["boxes"])
        for token in (
            "7-speed DCT",
            "engine_type",
            "ignition",
            "start",
            "Drive lifecycle gate",
            "clip 1 7",
            "shift_dir -1",
            "shift_dir 1",
            "3.10 2.13 1.62 1.29 1.03 0.84 0.70",
            "3.13 2.10 1.52 1.20 0.94 0.76 0.62",
        ):
            self.assertIn(token, text)
        self.assertIn("pack 0 1", text)
        self.assertNotIn("pak 0 1", text)
        self.assertNotIn("shift 1", text)

    def test_v2_generated_transient_families_have_deterministic_variants(self):
        expected_minimums = {
            "starter_*.wav": 2,
            "shift_up_*.wav": 3,
            "shift_down_*.wav": 3,
            "intake_backfire_*.wav": 3,
            "exhaust_pop_*.wav": 4,
            "exhaust_crackle_*.wav": 3,
        }
        for pattern, minimum in expected_minimums.items():
            self.assertGreaterEqual(len(list((ROOT / "media").glob(pattern))), minimum, pattern)
        transient = self.load_json("patchers/transient~.maxpat")
        text = "\n".join(item["box"].get("text", "") for item in transient["patcher"]["boxes"])
        for event in ("starter", "shift_dir", "intake_backfire", "exhaust_pop", "crackle"):
            self.assertIn(event, text)

    def test_v2_combustion_events_are_causal_and_profile_gated(self):
        drive = self.load_json("patchers/drive_simulator.maxpat")
        drive_text = "\n".join(item["box"].get("text", "") for item in drive["patcher"]["boxes"])
        self.assertIn("($f1>0.72)", drive_text)
        self.assertIn("($f2>2800.)", drive_text)
        self.assertIn("intake_backfire 1", drive_text)

        controller = self.load_json("patchers/engine_controller.maxpat")
        controller_text = "\n".join(item["box"].get("text", "") for item in controller["patcher"]["boxes"])
        self.assertIn("exhaust_pop 1", controller_text)
        self.assertIn("crackle 1", controller_text)
        self.assertIn("stop", controller_text)
        controller_boxes = {item["box"]["id"]: item["box"] for item in controller["patcher"]["boxes"]}
        exhaust_on_id = next(
            box_id for box_id, box in controller_boxes.items()
            if box.get("text") == "exhaust_pop 1"
        )
        exhaust_on_inputs = [
            line for line in controller["patcher"]["lines"]
            if line["patchline"]["destination"][0] == exhaust_on_id
        ]
        self.assertEqual(1, len(exhaust_on_inputs), "public pop/exhaust requests must not be duplicated")

        transient = self.load_json("patchers/transient~.maxpat")
        transient_text = "\n".join(item["box"].get("text", "") for item in transient["patcher"]["boxes"])
        self.assertGreaterEqual(transient_text.count("gate 1"), 5)
        self.assertIn("engine_running", transient_text)
        self.assertIn("expr $i1*$i2", transient_text)

    def test_runnable_project_has_public_engine_interface(self):
        required = [
            "VehicleSoundSynth-V2.maxproj",
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
        expected = {
            "engine_type", "ev_weight", "v12_weight", "v10_weight", "aggression",
            "brightness", "body", "texture", "cabin_width", "master_trim_db",
        }
        for values in presets.values():
            self.assertEqual(expected, set(values))
            self.assertIn(values["engine_type"], {"ev", "v12", "v10"})
            bounded = {key: value for key, value in values.items() if key not in {"engine_type", "master_trim_db"}}
            self.assertTrue(all(0.0 <= value <= 1.0 for value in bounded.values()))
            self.assertTrue(-24.0 <= values["master_trim_db"] <= 0.0)

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

    def test_output_chain_has_single_final_eq_and_peak_protection_stage(self):
        cabin = self.load_json("patchers/cabin_master~.maxpat")
        cabin_text = "\n".join(item["box"].get("text", "") for item in cabin["patcher"]["boxes"])
        self.assertNotIn("omx.peaklim~", cabin_text)
        self.assertNotIn("clip~ -0.891 0.891", cabin_text)

        mix = self.load_json("patchers/mix_master~.maxpat")
        mix_boxes = {item["box"]["id"]: item["box"] for item in mix["patcher"]["boxes"]}
        mix_text = "\n".join(box.get("text", "") for box in mix_boxes.values())
        self.assertEqual(4, sum(box["maxclass"] == "filtergraph~" for box in mix_boxes.values()))
        self.assertEqual(8, sum(box.get("text") == "biquad~" for box in mix_boxes.values()))
        for token in ("eq_low", "eq_lowmid", "eq_highmid", "eq_high", "eq_bypass", "master_trim_db"):
            self.assertIn(token, mix_text)
        limiter = next(box["id"] for box in mix_boxes.values() if box.get("text") == "omx.peaklim~")
        clippers = {box["id"] for box in mix_boxes.values() if box.get("text") == "clip~ -0.891 0.891"}
        outlets = {box["id"] for box in mix_boxes.values() if box["maxclass"] == "outlet"}
        mix_cords = {
            (line["patchline"]["source"][0], line["patchline"]["destination"][0])
            for line in mix["patcher"]["lines"]
        }
        self.assertEqual(2, len(clippers))
        self.assertTrue(all((limiter, clipper) in mix_cords for clipper in clippers))
        self.assertTrue(all(any((clipper, outlet) in mix_cords for outlet in outlets) for clipper in clippers))

    def test_demo_starts_muted(self):

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
            cords = [
                (
                    tuple(item["patchline"]["source"]),
                    tuple(item["patchline"]["destination"]),
                )
                for item in patcher["lines"]
            ]
            self.assertEqual(len(cords), len(set(cords)), f"{path.name}: duplicate patchcord")
            for item in patcher["lines"]:
                line = item["patchline"]
                source_id, source_outlet = line["source"]
                destination_id, destination_inlet = line["destination"]
                self.assertIn(source_id, boxes, f"{path.name}: {source_id}")
                self.assertIn(destination_id, boxes, f"{path.name}: {destination_id}")
                self.assertLess(source_outlet, boxes[source_id]["numoutlets"], path.name)
                self.assertLess(destination_inlet, boxes[destination_id]["numinlets"], path.name)

    def test_expr_objects_stay_below_max_argument_truncation_limit(self):
        patchers = list(ROOT.glob("*.maxpat")) + list((ROOT / "patchers").glob("*.maxpat"))
        for path in patchers:
            for item in self.load_json(path.relative_to(ROOT))["patcher"]["boxes"]:
                text = item["box"].get("text", "")
                if text.startswith("expr "):
                    self.assertLess(len(text), 240, f"{path.name}: {text}")

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
        project = self.load_json("VehicleSoundSynth-V2.maxproj")
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
            "patchers/engine_controller.maxpat",
            "patchers/powertrain~.maxpat",
            "patchers/transient~.maxpat",
            "patchers/road_air~.maxpat",
            "patchers/cabin_master~.maxpat",
            "patchers/mix_master~.maxpat",
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
        for abstraction in ("engine_controller", "powertrain~", "transient~", "road_air~", "cabin_master~", "mix_master~"):
            self.assertIn(abstraction, engine_text)

    def test_road_noise_is_subordinate_and_high_frequency_controlled(self):
        road = self.load_json("patchers/road_air~.maxpat")
        text = "\n".join(item["box"].get("text", "") for item in road["patcher"]["boxes"])
        self.assertIn("* 0.12", text)
        self.assertIn("500. + 3000.*", text)
        self.assertIn("lores~ 1800 0.35", text)

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

    def test_v2_demo_exposes_lifecycle_dct_and_global_eq_controls(self):
        main = self.load_json("main.maxpat")
        text = "\n".join(item["box"].get("text", "") for item in main["patcher"]["boxes"])
        for token in (
            "VehicleSoundSynth V2",
            "Ignition",
            "Engine Start",
            "prepend ignition",
            "prepend start",
            "7-speed DCT",
            "Low Shelf",
            "Low-Mid",
            "High-Mid",
            "High Shelf",
            "EQ Bypass",
            "Master Trim",
            "prepend eq_low",
            "prepend eq_lowmid",
            "prepend eq_highmid",
            "prepend eq_high",
            "prepend master_trim_db",
        ):
            self.assertIn(token, text)

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

    def test_runtime_probe_builder_creates_self_contained_temp_bundle(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "build_runtime_probe.py"),
                    "--bundle-root",
                    directory,
                ],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            bundle = Path(directory)
            for relative_path in (
                "runtime_probe.maxpat",
                "vehicle_engine~.maxpat",
                "engine_controller.maxpat",
                "v12_powertrain.gendsp",
                "media/starter_v12.wav",
            ):
                self.assertTrue((bundle / relative_path).is_file(), relative_path)

    def test_audio_metrics_distinguish_low_engine_energy_from_high_noise(self):
        sys.path.insert(0, str(ROOT / "tools"))
        from audio_metrics import analyze

        def write_tone(path, frequency):
            import math
            import struct

            sample_rate = 48000
            frames = sample_rate
            values = [
                round(0.25 * math.sin(2.0 * math.pi * frequency * index / sample_rate) * 32767.0)
                for index in range(frames)
            ]
            with wave.open(str(path), "wb") as handle:
                handle.setnchannels(1)
                handle.setsampwidth(2)
                handle.setframerate(sample_rate)
                handle.writeframes(b"".join(struct.pack("<h", value) for value in values))

        with tempfile.TemporaryDirectory() as directory:
            low_path = Path(directory) / "low.wav"
            high_path = Path(directory) / "high.wav"
            write_tone(low_path, 120.0)
            write_tone(high_path, 8000.0)
            low = analyze(low_path)
            high = analyze(high_path)
        self.assertGreater(low["low_mid_ratio"], 0.99)
        self.assertLess(low["high_ratio"], 0.01)
        self.assertGreater(high["high_ratio"], 0.99)

    def test_generated_combustion_transients_are_not_high_frequency_dominated(self):
        sys.path.insert(0, str(ROOT / "tools"))
        from audio_metrics import analyze

        patterns = ("starter_*.wav", "intake_backfire_*.wav", "exhaust_pop_*.wav", "exhaust_crackle_*.wav")
        for pattern in patterns:
            for path in (ROOT / "media").glob(pattern):
                metrics = analyze(path)
                self.assertLess(metrics["high_ratio"], 0.20, path.name)


if __name__ == "__main__":
    unittest.main()
