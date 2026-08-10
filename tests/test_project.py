import hashlib
import json
import struct
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

    def test_v3_project_identity_and_public_entrypoint(self):
        project_path = ROOT / "VehicleSoundSynth-V3.maxproj"
        self.assertTrue(project_path.is_file())
        project = self.load_json("VehicleSoundSynth-V3.maxproj")
        self.assertEqual("VehicleSoundSynth-V3", project["name"])
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

    def test_v3_public_engine_contract_exposes_cabin_rumble_controls(self):
        engine = self.load_json("patchers/vehicle_engine~.maxpat")
        text = "\n".join(item["box"].get("text", "") for item in engine["patcher"]["boxes"])
        for name in ("cabin_rumble", "exhaust_boom", "structure_vibration"):
            self.assertIn(name, text)

    def test_v3_exposes_independent_db_trim_for_every_audio_stem(self):
        stem_contract = {
            "patchers/powertrain~.maxpat": "powertrain_level_db",
            "patchers/transient~.maxpat": "transient_level_db",
            "patchers/road_air~.maxpat": "road_level_db",
            "patchers/cabin_rumble~.maxpat": "rumble_level_db",
        }
        engine = self.load_json("patchers/vehicle_engine~.maxpat")
        engine_text = "\n".join(
            item["box"].get("text", "") for item in engine["patcher"]["boxes"]
        )
        for relative_path, parameter in stem_contract.items():
            patch = self.load_json(relative_path)["patcher"]
            text = "\n".join(item["box"].get("text", "") for item in patch["boxes"])
            self.assertIn(parameter, engine_text)
            self.assertIn(parameter, text)
            self.assertIn("clip -60. 6.", text)
            self.assertIn("expr pow(10., $f1/20.)", text)
            self.assertIn("pack 0. 50", text)

        presets = self.load_json("presets/sound_dna.json")
        expected = {
            "Future EV": (-2.0, -9.0, -14.0, -60.0),
            "High-Rev V12": (-3.0, -7.0, -16.0, -5.0),
            "Aggressive V10": (-3.0, -6.0, -16.0, -4.0),
        }
        for name, levels in expected.items():
            self.assertEqual(
                levels,
                tuple(
                    presets[name][parameter]
                    for parameter in stem_contract.values()
                ),
            )

    def test_cabin_ir_has_bounded_wet_dry_mix_and_stereo_4096_tap_filters(self):
        engine = self.load_json("patchers/vehicle_engine~.maxpat")
        engine_text = "\n".join(
            item["box"].get("text", "") for item in engine["patcher"]["boxes"]
        )
        self.assertIn("cabin_ir_mix", engine_text)
        cabin = self.load_json("patchers/cabin_master~.maxpat")["patcher"]
        text = "\n".join(item["box"].get("text", "") for item in cabin["boxes"])
        for token in (
            "cabin_ir_mix", "buffer~ cabin_ir_l cabin_ir_l.wav",
            "buffer~ cabin_ir_r cabin_ir_r.wav", "buffir~ cabin_ir_l 0 4096",
            "buffir~ cabin_ir_r 0 4096", "expr sqrt(1.-$f1)", "expr sqrt($f1)",
        ):
            self.assertIn(token, text)
        self.assertGreaterEqual(text.count("svf~ 120 0.7"), 2)
        self.assertEqual(4, text.count("svf~ 180 0.5"))
        for name in ("cabin_ir_l.wav", "cabin_ir_r.wav"):
            with wave.open(str(ROOT / "media" / name), "rb") as handle:
                self.assertEqual(48000, handle.getframerate())
                self.assertEqual(1, handle.getnchannels())
                self.assertEqual(4096, handle.getnframes())

        expected = {"Future EV": 0.10, "High-Rev V12": 0.20, "Aggressive V10": 0.18}
        presets = self.load_json("presets/sound_dna.json")
        for name, value in expected.items():
            self.assertEqual(value, presets[name]["cabin_ir_mix"])

    def test_v3_cabin_rumble_module_is_declared_and_runnable(self):
        project = self.load_json("VehicleSoundSynth-V3.maxproj")
        declared = {
            relative_path
            for category in project["contents"].values()
            for relative_path in category
        }
        required = {"patchers/cabin_rumble~.maxpat"}
        self.assertTrue(required.issubset(declared))
        self.assertTrue(all((ROOT / path).is_file() for path in required))
        self.assertNotIn("gen/cabin_rumble.gendsp", declared)

        rumble = self.load_json("patchers/cabin_rumble~.maxpat")["patcher"]
        boxes = [item["box"] for item in rumble["boxes"]]
        self.assertEqual(3, sum(box["maxclass"] == "inlet" for box in boxes))
        self.assertEqual(2, sum(box["maxclass"] == "outlet" for box in boxes))
        text = "\n".join(box.get("text", "") for box in boxes)
        self.assertNotIn("gen~ @gen cabin_rumble", text)
        self.assertIn("Powertrain-driven cabin modes", text)
        for frequency in (48, 68, 92, 118):
            self.assertIn(f"svf~ {frequency} ", text)
        self.assertIn("svf~ 28 0.7", text)

        engine = self.load_json("patchers/vehicle_engine~.maxpat")["patcher"]
        engine_boxes = {item["box"]["id"]: item["box"] for item in engine["boxes"]}
        power = next(box_id for box_id, box in engine_boxes.items() if box.get("text") == "powertrain~")
        rumble_id = next(box_id for box_id, box in engine_boxes.items() if box.get("text") == "cabin_rumble~")
        cords = {
            (tuple(line["patchline"]["source"]), tuple(line["patchline"]["destination"]))
            for line in engine["lines"]
        }
        self.assertIn(((power, 0), (rumble_id, 1)), cords)
        self.assertIn(((power, 1), (rumble_id, 2)), cords)

    def test_v3_engine_routes_rumble_before_cabin_and_centers_low_frequencies(self):
        engine = self.load_json("patchers/vehicle_engine~.maxpat")["patcher"]
        boxes = {item["box"]["id"]: item["box"] for item in engine["boxes"]}
        rumble = next(box_id for box_id, box in boxes.items() if box.get("text") == "cabin_rumble~")
        cabin = next(box_id for box_id, box in boxes.items() if box.get("text") == "cabin_master~")
        edges = {}
        for item in engine["lines"]:
            source = item["patchline"]["source"][0]
            destination = item["patchline"]["destination"][0]
            edges.setdefault(source, set()).add(destination)

        reachable = {rumble}
        frontier = [rumble]
        while frontier:
            current = frontier.pop()
            for destination in edges.get(current, set()):
                if destination not in reachable:
                    reachable.add(destination)
                    frontier.append(destination)
        self.assertIn(cabin, reachable)

        cabin_patch = self.load_json("patchers/cabin_master~.maxpat")
        cabin_text = "\n".join(
            item["box"].get("text", "") for item in cabin_patch["patcher"]["boxes"]
        )
        self.assertIn("svf~ 120 0.7", cabin_text)

    def test_v3_presets_and_demo_expose_strong_profile_specific_rumble(self):
        presets = self.load_json("presets/sound_dna.json")
        expected = {
            "Future EV": (0.0, 0.0, 0.0),
            "High-Rev V12": (0.90, 0.62, 0.58),
            "Aggressive V10": (0.92, 0.74, 0.72),
        }
        for name, values in expected.items():
            preset = presets[name]
            actual = (
                preset["cabin_rumble"],
                preset["exhaust_boom"],
                preset["structure_vibration"],
            )
            self.assertEqual(values, actual)

        main = self.load_json("main.maxpat")
        text = "\n".join(item["box"].get("text", "") for item in main["patcher"]["boxes"])
        for token in (
            "VehicleSoundSynth V3",
            "Cabin Rumble",
            "Exhaust Boom",
            "Structure Vibration",
            "prepend cabin_rumble",
            "prepend exhaust_boom",
            "prepend structure_vibration",
        ):
            self.assertIn(token, text)

    def test_v2_engine_routes_through_lifecycle_and_final_mix_modules(self):
        engine = self.load_json("patchers/vehicle_engine~.maxpat")
        text = "\n".join(item["box"].get("text", "") for item in engine["patcher"]["boxes"])
        self.assertIn("engine_controller", text)
        self.assertIn("mix_master~", text)
        self.assertTrue((ROOT / "patchers" / "engine_controller.maxpat").is_file())
        self.assertTrue((ROOT / "patchers" / "mix_master~.maxpat").is_file())

    def test_v2_fuel_generators_expose_running_and_shift_envelopes(self):
        for name, events_per_revolution in (("v12_powertrain", 6), ("v10_powertrain", 5)):
            patcher = self.load_json(f"gen/{name}.gendsp")["patcher"]
            code = "\n".join(item["box"].get("code", "") for item in patcher["boxes"])
            for parameter in ("engine_running", "combustion_gain", "shift_cut"):
                self.assertIn(f"Param {parameter}", code)
            self.assertIn(f"events = {events_per_revolution}", code)
            self.assertIn("phasor(", code)
            self.assertIn("pulse = exp(", code)
            self.assertIn("noise()", code)
            self.assertIn("tanh(", code)
            self.assertGreaterEqual(code.count("cycle("), 8)
            self.assertIn("sideband_low", code)
            self.assertIn("sideband_high", code)
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
            "gate 1",
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
        self.assertIn("pack 0 0 0 1", controller_text)
        self.assertIn("expr $i1*$i2*$i3*$i4", controller_text)
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
        transient_boxes = {item["box"]["id"]: item["box"] for item in transient["patcher"]["boxes"]}
        starter_stop_id = next(
            box_id for box_id, box in transient_boxes.items()
            if box.get("maxclass") == "message" and box.get("text") == "stop"
        )
        starter_player_ids = {
            box_id for box_id, box in transient_boxes.items()
            if box.get("text") in {"play~ starter_v12 1", "play~ starter_v10 1"}
        }
        stopped_players = {
            line["patchline"]["destination"][0]
            for line in transient["patcher"]["lines"]
            if line["patchline"]["source"][0] == starter_stop_id
        }
        self.assertEqual(starter_player_ids, stopped_players)

    def test_runnable_project_has_public_engine_interface(self):
        required = [
            "VehicleSoundSynth-V3.maxproj",
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
            "brightness", "body", "texture", "cabin_width", "cabin_rumble",
            "exhaust_boom", "structure_vibration", "master_trim_db",
            "cabin_ir_mix",
            "powertrain_level_db", "transient_level_db", "road_level_db",
            "rumble_level_db",
        }
        for values in presets.values():
            self.assertEqual(expected, set(values))
            self.assertIn(values["engine_type"], {"ev", "v12", "v10"})
            db_parameters = {
                "master_trim_db", "powertrain_level_db", "transient_level_db",
                "road_level_db", "rumble_level_db",
            }
            bounded = {key: value for key, value in values.items() if key not in {"engine_type", *db_parameters}}
            self.assertTrue(all(0.0 <= value <= 1.0 for value in bounded.values()))
            self.assertTrue(-24.0 <= values["master_trim_db"] <= 0.0)
            self.assertTrue(all(-60.0 <= values[key] <= 6.0 for key in db_parameters - {"master_trim_db"}))

    def test_engine_accepts_the_documented_state_and_macro_messages(self):
        engine = self.load_json("patchers/vehicle_engine~.maxpat")
        texts = "\n".join(item["box"].get("text", "") for item in engine["patcher"]["boxes"])
        for name in ("speed_kph", "rpm", "throttle", "brake", "load", "accel", "gear", "shift"):
            self.assertIn(name, texts)
        for name in ("ev_weight", "v12_weight", "v10_weight", "aggression", "brightness", "body", "texture", "cabin_width"):
            self.assertIn(name, texts)

    def test_transient_media_are_bounded_48khz_mono_wave_files(self):
        import wave

        for name in ("shift_thump.wav", "exhaust_pop.wav", "mechanical_click.wav"):
            path = ROOT / "media" / name
            self.assertTrue(path.is_file(), name)
            with wave.open(str(path), "rb") as wav:
                self.assertEqual(1, wav.getnchannels())
                self.assertEqual(48000, wav.getframerate())
                self.assertLess(wav.getnframes(), 48000)

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

    def test_eq_parameter_lists_drive_filtergraph_coefficient_inlets(self):
        """Each EQ band's [frequency, linear gain, Q] list must recalculate coefficients."""
        mix = self.load_json("patchers/mix_master~.maxpat")["patcher"]
        boxes = {item["box"]["id"]: item["box"] for item in mix["boxes"]}
        lines = [item["patchline"] for item in mix["lines"]]
        graphs = {
            box_id for box_id, box in boxes.items()
            if box["maxclass"] == "filtergraph~"
        }
        parameter_paks = {
            box_id for box_id, box in boxes.items()
            if box.get("text", "").startswith("pak ")
        }
        self.assertEqual(4, len(graphs))
        for graph in graphs:
            coefficient_inputs = [
                line for line in lines
                if line["destination"] == [graph, 5]
                and line["source"][0] in parameter_paks
            ]
            self.assertEqual(1, len(coefficient_inputs), graph)
        self.assertFalse(
            any(box.get("text", "").startswith("prepend lowshelf") for box in boxes.values())
        )
        self.assertFalse(
            any(box.get("text", "").startswith("prepend peaknotch") for box in boxes.values())
        )
        self.assertFalse(
            any(box.get("text", "").startswith("prepend highshelf") for box in boxes.values())
        )

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

    def test_every_public_continuous_control_reaches_a_signal_outlet(self):
        contracts = {
            "patchers/powertrain~.maxpat": (
                "rpm", "throttle", "load", "aggression", "brightness", "body",
                "texture", "ev_weight", "v12_weight", "v10_weight", "powertrain_level_db",
            ),
            "patchers/transient~.maxpat": ("aggression", "texture", "transient_level_db"),
            "patchers/road_air~.maxpat": (
                "speed_kph", "brightness", "texture", "cabin_width", "road_level_db",
            ),
            "patchers/cabin_rumble~.maxpat": (
                "cabin_rumble", "exhaust_boom", "structure_vibration", "body",
                "aggression", "rumble_level_db",
            ),
            "patchers/cabin_master~.maxpat": (
                "aggression", "brightness", "body", "texture", "cabin_width", "cabin_ir_mix",
            ),
        }
        for relative_path, parameters in contracts.items():
            patch = self.load_json(relative_path)["patcher"]
            boxes = {item["box"]["id"]: item["box"] for item in patch["boxes"]}
            router_id, router_box = next(
                (box_id, box) for box_id, box in boxes.items()
                if box.get("text", "").startswith("route ")
            )
            route_names = router_box["text"].split()[1:]
            edges = {}
            for item in patch["lines"]:
                line = item["patchline"]
                edges.setdefault((line["source"][0], line["source"][1]), set()).add(
                    line["destination"][0]
                )
                edges.setdefault((line["source"][0], None), set()).add(line["destination"][0])
            signal_outlets = {
                box_id for box_id, box in boxes.items()
                if box["maxclass"] == "outlet" and box.get("comment") == "signal"
            }
            for parameter in parameters:
                start = (router_id, route_names.index(parameter))
                reachable = set(edges.get(start, set()))
                frontier = list(reachable)
                while frontier:
                    current = frontier.pop()
                    for destination in edges.get((current, None), set()):
                        if destination not in reachable:
                            reachable.add(destination)
                            frontier.append(destination)
                self.assertTrue(
                    reachable & signal_outlets,
                    f"{relative_path}: {parameter} has no audible signal path",
                )

    def test_expr_objects_stay_below_max_argument_truncation_limit(self):
        patchers = list(ROOT.glob("*.maxpat")) + list((ROOT / "patchers").glob("*.maxpat"))
        for path in patchers:
            for item in self.load_json(path.relative_to(ROOT))["patcher"]["boxes"]:
                text = item["box"].get("text", "")
                if text.startswith("expr "):
                    self.assertLess(len(text), 240, f"{path.name}: {text}")

    def test_gen_patchers_expose_bounded_required_parameters(self):
        gen_paths = sorted((ROOT / "gen").glob("*.gendsp"))
        self.assertEqual(3, len(gen_paths))
        for path in gen_paths:
            patcher = self.load_json(path.relative_to(ROOT))["patcher"]
            code = "\n".join(
                item["box"].get("code", item["box"].get("text", ""))
                for item in patcher["boxes"]
            )
            required = {"rpm", "throttle", "load", "aggression", "body"}
            required |= {"brightness", "texture"}
            if path.name != "ev_powertrain.gendsp":
                required |= {"engine_running", "combustion_gain", "shift_cut"}
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
        project = self.load_json("VehicleSoundSynth-V3.maxproj")
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
        self.assertIn("pow($f1/300., 0.8)", text)
        self.assertIn("pow($f1/300., 1.7)", text)
        self.assertIn("pink~", text)
        self.assertIn("Tire: 70-900 Hz", text)
        self.assertIn("Wind: 400-4000 Hz", text)
        self.assertIn("svf~ 70 0.65", text)
        self.assertIn("lores~ 900 0.45", text)
        self.assertIn("svf~ 400 0.7", text)
        self.assertIn("expr 1400.+2600.*$f1", text)
        self.assertIn("texture", text)
        self.assertIn("cabin_width", text)
        self.assertNotIn("pow($f1/300., 0.7) * 0.12", text)

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

    def test_manual_mode_keyboard_has_linear_throttle_and_fast_brake_envelopes(self):
        patcher = self.load_json("main.maxpat")["patcher"]
        boxes = {item["box"]["id"]: item["box"] for item in patcher["boxes"]}
        text_to_ids = {}
        for box_id, box in boxes.items():
            text_to_ids.setdefault(box.get("text", ""), set()).add(box_id)

        for text in (
            "key",
            "keyup",
            "sel 119 87 115 83",
            "== 0",
            "sel 1 0",
            "1. 2500",
            "0. 1400",
            "1. 120",
            "Manual keyboard: hold W = throttle up; release W = throttle down; hold S = fast brake; release S = brake off",
        ):
            self.assertIn(text, text_to_ids)

        lines = [line["patchline"] for line in patcher["lines"]]
        mode_id = next(
            box_id for box_id, box in boxes.items()
            if box["maxclass"] == "umenu" and "Internal Manual" in box.get("items", [])
        )
        manual_gate_id = next(iter(text_to_ids["== 0"]))
        self.assertTrue(any(
            line["source"][0] == mode_id and line["destination"][0] == manual_gate_id
            for line in lines
        ))

        throttle_id = next(
            box_id for box_id, box in boxes.items()
            if box["maxclass"] == "flonum" and box.get("patching_rect", [None])[0] == 25.0
            and box.get("patching_rect", [None, None])[1] == 270.0
        )
        brake_id = next(
            box_id for box_id, box in boxes.items()
            if box["maxclass"] == "flonum" and box.get("patching_rect", [None])[0] == 150.0
            and box.get("patching_rect", [None, None])[1] == 270.0
        )
        line_ids = {
            box_id for box_id, box in boxes.items() if box.get("text") == "line 0."
        }
        self.assertEqual(2, len(line_ids))
        self.assertTrue(any(
            line["source"][0] in line_ids and line["destination"][0] == throttle_id
            for line in lines
        ))
        self.assertTrue(any(
            line["source"][0] in line_ids and line["destination"][0] == brake_id
            for line in lines
        ))

    def test_preset_messages_refresh_visible_macro_and_gain_controls(self):
        main = self.load_json("main.maxpat")["patcher"]
        boxes = {item["box"]["id"]: item["box"] for item in main["boxes"]}
        text = "\n".join(box.get("text", "") for box in boxes.values())
        self.assertIn("Preset/UI state synchronizer", text)
        sync = next(
            box_id for box_id, box in boxes.items()
            if box.get("text", "").startswith("route ev_weight v12_weight v10_weight")
        )
        visible_parameters = (
            "ev_weight", "v12_weight", "v10_weight", "aggression", "brightness",
            "body", "texture", "cabin_width", "cabin_rumble", "exhaust_boom",
            "structure_vibration", "cabin_ir_mix", "powertrain_level_db", "transient_level_db",
            "road_level_db", "rumble_level_db", "master_trim_db",
        )
        self.assertTrue(all(parameter in boxes[sync]["text"] for parameter in visible_parameters))
        destinations = {
            line["patchline"]["destination"][0]
            for line in main["lines"]
            if line["patchline"]["source"][0] == sync
        }
        self.assertGreaterEqual(
            sum(boxes[destination]["maxclass"] == "flonum" for destination in destinations),
            len(visible_parameters),
        )

    def test_v3_demo_exposes_lifecycle_dct_rumble_and_global_eq_controls(self):
        main = self.load_json("main.maxpat")
        text = "\n".join(item["box"].get("text", "") for item in main["patcher"]["boxes"])
        for token in (
            "VehicleSoundSynth V3",
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
                "runtime_probe_v12_idle_on.maxpat",
                "vehicle_engine~.maxpat",
                "engine_controller.maxpat",
                "cabin_rumble~.maxpat",
                "v12_powertrain.gendsp",
                "media/starter_v12.wav",
            ):
                self.assertTrue((bundle / relative_path).is_file(), relative_path)
            with (bundle / "runtime_probe_v12_idle_on.maxpat").open(encoding="utf-8") as handle:
                probe = json.load(handle)
            text = "\n".join(item["box"].get("text", "") for item in probe["patcher"]["boxes"])
            self.assertIn("cabin_rumble~", text)
            self.assertIn("cabin_rumble 0.9", text)
            self.assertIn(";\rdsp setdriver NonRealTime", text)
            self.assertIn("dsptime~", text)
            self.assertIn("past 4000", text)

    def test_mix_runtime_probe_builder_exposes_eq_trim_and_bypass_scenarios(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "build_mix_probe.py"),
                    "--bundle-root", directory,
                    "--frequency", "250",
                    "--eq-message", "eq_lowmid 250. -12. 0.8",
                    "--trim-db", "-8",
                    "--bypass", "0",
                ],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            bundle = Path(directory)
            probe_path = bundle / "mix_probe_mix_probe.maxpat"
            self.assertTrue(probe_path.is_file())
            self.assertTrue((bundle / "mix_master~.maxpat").is_file())
            patch = json.loads(probe_path.read_text(encoding="utf-8"))
            text = "\n".join(item["box"].get("text", "") for item in patch["patcher"]["boxes"])
            self.assertIn("cycle~ 250", text)
            self.assertIn("eq_lowmid 250. -12. 0.8", text)
            self.assertIn("master_trim_db -8", text)
            self.assertIn("eq_bypass 0", text)

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
        self.assertGreater(low["rumble_ratio"], 0.99)
        self.assertLess(low["subsonic_ratio"], 0.01)
        self.assertLess(low["high_ratio"], 0.01)
        self.assertGreater(high["high_ratio"], 0.99)

    def test_audio_metrics_measure_low_frequency_stereo_side_energy(self):
        import math
        import struct

        sys.path.insert(0, str(ROOT / "tools"))
        from audio_metrics import analyze

        def write_stereo(path, right_polarity):
            sample_rate = 48000
            payload = []
            for index in range(sample_rate):
                value = round(0.25 * math.sin(2.0 * math.pi * 80.0 * index / sample_rate) * 32767.0)
                payload.append(struct.pack("<hh", value, round(value * right_polarity)))
            with wave.open(str(path), "wb") as handle:
                handle.setnchannels(2)
                handle.setsampwidth(2)
                handle.setframerate(sample_rate)
                handle.writeframes(b"".join(payload))

        with tempfile.TemporaryDirectory() as directory:
            centered_path = Path(directory) / "centered.wav"
            side_path = Path(directory) / "side.wav"
            write_stereo(centered_path, 1.0)
            write_stereo(side_path, -1.0)
            centered = analyze(centered_path)
            side = analyze(side_path)
        self.assertLess(centered["low_side_ratio"], 0.001)
        self.assertGreater(side["low_side_ratio"], 0.99)
        self.assertAlmostEqual(centered["peak_dbfs"], side["peak_dbfs"], places=3)
        self.assertAlmostEqual(centered["rms_dbfs"], side["rms_dbfs"], places=3)

    def test_audio_metrics_detect_harmonic_complexity_and_single_tone_dominance(self):
        import math
        import struct

        sys.path.insert(0, str(ROOT / "tools"))
        from audio_metrics import analyze

        def write_tones(path, frequencies):
            payload = []
            amplitude = 0.45 / len(frequencies)
            for index in range(48000):
                value = sum(
                    amplitude * math.sin(2 * math.pi * frequency * index / 48000)
                    for frequency in frequencies
                )
                payload.append(struct.pack("<h", round(value * 32767)))
            with wave.open(str(path), "wb") as handle:
                handle.setnchannels(1)
                handle.setsampwidth(2)
                handle.setframerate(48000)
                handle.writeframes(b"".join(payload))

        with tempfile.TemporaryDirectory() as directory:
            pure_path = Path(directory) / "pure.wav"
            rich_path = Path(directory) / "rich.wav"
            write_tones(pure_path, [440])
            write_tones(rich_path, [110, 220, 330, 440, 660, 880, 1320])
            pure = analyze(pure_path)
            rich = analyze(rich_path)
        self.assertLessEqual(pure["spectral_peak_count_80_6000"], 2)
        self.assertGreater(pure["dominant_peak_ratio_80_6000"], 0.70)
        self.assertGreaterEqual(rich["spectral_peak_count_80_6000"], 6)
        self.assertLess(rich["dominant_peak_ratio_80_6000"], 0.25)

    def test_generated_combustion_transients_are_not_high_frequency_dominated(self):
        sys.path.insert(0, str(ROOT / "tools"))
        from audio_metrics import analyze

        patterns = ("starter_*.wav", "intake_backfire_*.wav", "exhaust_pop_*.wav", "exhaust_crackle_*.wav")
        for pattern in patterns:
            for path in (ROOT / "media").glob(pattern):
                metrics = analyze(path)
                self.assertLess(metrics["high_ratio"], 0.20, path.name)

    def test_asset_manifest_allows_only_approved_licenses_and_labels_fallbacks(self):
        manifest = self.load_json("assets/asset_manifest.json")
        self.assertEqual(48000, manifest["sample_rate"])
        allowed = set(manifest["license_policy"])
        self.assertEqual({"CC0-1.0", "CC-BY-3.0", "CC-BY-4.0"}, allowed)
        self.assertTrue(manifest["assets"])
        for asset in manifest["assets"]:
            self.assertIn(asset["source"]["license"], allowed)
            self.assertTrue(asset["source"]["url"].startswith("https://"))
            self.assertIn(asset["status"], {"pending_download", "downloaded", "processed"})
            if asset["status"] == "processed":
                self.assertRegex(asset["raw_sha256"], r"^[0-9a-f]{64}$")
                for output in asset["outputs"]:
                    self.assertRegex(output["processed_sha256"], r"^[0-9a-f]{64}$")
        self.assertIn("fallback-only", manifest["fallback_media"]["policy"])
        self.assertTrue((ROOT / "ASSET_LICENSES.md").is_file())

    def test_all_runtime_foley_and_ir_are_processed_licensed_assets(self):
        manifest = self.load_json("assets/asset_manifest.json")
        processed = {}
        for asset in manifest["assets"]:
            for output in asset["outputs"]:
                processed[output["path"]] = output
        required = {
            f"media/{name}" for name in manifest["fallback_media"]["files"]
        } | {"media/cabin_ir_l.wav", "media/cabin_ir_r.wav", "media/starter_v12.wav", "media/starter_v10.wav"}
        self.assertTrue(required.issubset(processed))
        for relative_path in sorted(required):
            output = processed[relative_path]
            path = ROOT / relative_path
            self.assertEqual(
                output["processed_sha256"], hashlib.sha256(path.read_bytes()).hexdigest()
            )
            with wave.open(str(path), "rb") as handle:
                self.assertEqual(1, handle.getnchannels())
                self.assertEqual(48000, handle.getframerate())
                payload = struct.unpack(
                    f"<{handle.getnframes()}h", handle.readframes(handle.getnframes())
                )
            self.assertLessEqual(max(abs(value) for value in payload), 32767)
            self.assertLess(abs(sum(payload) / len(payload) / 32768.0), 0.002)

    def test_asset_processor_removes_dc_fades_and_normalizes_deterministically(self):
        import math
        import struct

        sys.path.insert(0, str(ROOT / "tools"))
        from process_assets import process_pcm16_wav

        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.wav"
            first = Path(directory) / "first.wav"
            second = Path(directory) / "second.wav"
            values = [
                round((0.20 + 0.15 * math.sin(2 * math.pi * 180 * index / 48000)) * 32767)
                for index in range(48000)
            ]
            with wave.open(str(source), "wb") as handle:
                handle.setnchannels(1)
                handle.setsampwidth(2)
                handle.setframerate(48000)
                handle.writeframes(b"".join(struct.pack("<h", value) for value in values))
            kwargs = dict(
                start_seconds=0.1, duration_seconds=0.25, channel="mix",
                peak_dbfs=-6.0, fade_ms=5.0,
            )
            result = process_pcm16_wav(source, first, **kwargs)
            process_pcm16_wav(source, second, **kwargs)
            self.assertEqual(hashlib.sha256(first.read_bytes()).hexdigest(), hashlib.sha256(second.read_bytes()).hexdigest())
            self.assertAlmostEqual(-6.0, result["peak_dbfs"], delta=0.08)
            with wave.open(str(first), "rb") as handle:
                payload = struct.unpack(f"<{handle.getnframes()}h", handle.readframes(handle.getnframes()))
            normalized = [value / 32768.0 for value in payload]
            self.assertLess(abs(sum(normalized) / len(normalized)), 0.001)
            self.assertEqual(0, payload[0])
            self.assertEqual(0, payload[-1])

    def test_asset_converter_resamples_without_changing_duration(self):
        import math

        sys.path.insert(0, str(ROOT / "tools"))
        from process_assets import convert_to_pcm16_48k

        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source_44100.wav"
            destination = Path(directory) / "destination_48000.wav"
            with wave.open(str(source), "wb") as handle:
                handle.setnchannels(1)
                handle.setsampwidth(2)
                handle.setframerate(44100)
                handle.writeframes(
                    b"".join(
                        struct.pack(
                            "<h",
                            round(0.25 * math.sin(2 * math.pi * 220 * index / 44100) * 32767),
                        )
                        for index in range(44100)
                    )
                )
            convert_to_pcm16_48k(source, destination)
            with wave.open(str(destination), "rb") as handle:
                self.assertEqual(48000, handle.getframerate())
                self.assertEqual(48000, handle.getnframes())
                self.assertEqual(2, handle.getsampwidth())

    def test_generator_never_overwrites_existing_curated_media(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            subprocess.run(
                [sys.executable, str(ROOT / "tools" / "build_project.py"), "--output-root", str(destination)],
                check=True, cwd=ROOT, capture_output=True, text=True,
            )
            protected = destination / "media" / "starter_v12.wav"
            protected.write_bytes(b"curated-audio-sentinel")
            subprocess.run(
                [sys.executable, str(ROOT / "tools" / "build_project.py"), "--output-root", str(destination)],
                check=True, cwd=ROOT, capture_output=True, text=True,
            )
            self.assertEqual(b"curated-audio-sentinel", protected.read_bytes())


if __name__ == "__main__":
    unittest.main()
