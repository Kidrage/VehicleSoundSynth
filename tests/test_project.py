import hashlib
import json
import math
import struct
import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path

from tools.prepare_local_reference import prepare_v10_atlas
from tools.validate_v10_lifecycle import validate_drive_trace, validate_render
from tools.build_project import DNA_PARAMETER_SPECS
from tools.build_runtime_probe import SCENARIOS


ROOT = Path(__file__).resolve().parents[1]


class VehicleSoundProjectTests(unittest.TestCase):
    def load_json(self, relative_path):
        with (ROOT / relative_path).open(encoding="utf-8") as handle:
            return json.load(handle)

    def run_drive_trace(self, profile, seconds=12.0):
        script = r"""
const modelModule = require(process.argv[1]);
const profile = process.argv[2];
const seconds = Number(process.argv[3]);
const model = new modelModule.DriveModel(profile);
model.handle("ignition", [1]);
model.handle("start", [1]);
const beforeThrottle = model.snapshot();
model.handle("throttle", [1]);
const afterThrottleBeforeTick = model.snapshot();
const trace = [];
for (let i = 0; i < Math.round(seconds / 0.02); i += 1) {
  model.tick(0.02);
  trace.push(model.snapshot());
}
process.stdout.write(JSON.stringify({beforeThrottle, afterThrottleBeforeTick, trace}));
"""
        result = subprocess.run(
            [
                "node",
                "-e",
                script,
                str(ROOT / "code" / "drive_model.js"),
                profile,
                str(seconds),
            ],
            check=True,
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        return json.loads(result.stdout)

    def test_v5_identity_and_frozen_v4_lineage(self):
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        self.assertEqual("VehicleSoundSynth-V5", project["name"])
        self.assertTrue((ROOT / ".codex" / "MAINLINE.md").is_file())
        self.assertIn("v4.0.0", (ROOT / ".codex" / "MAINLINE.md").read_text())

    def test_v5_runtime_events_are_procedural_and_never_play_shift_pop_samples(self):
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        declared_media = set(project["contents"]["media"])
        self.assertEqual(
            {
                "media/cabin_ir_l.wav",
                "media/cabin_ir_r.wav",
                "media/starter_v10.wav",
                "media/starter_v12.wav",
            },
            declared_media,
        )
        self.assertNotIn(
            "patchers/reference_texture~.maxpat",
            project["contents"]["patchers"],
        )
        forbidden_media = (
            "shift_up_", "shift_down_", "shift_thump", "exhaust_pop",
            "exhaust_crackle", "intake_backfire", "mechanical_click",
        )
        for path in declared_media:
            self.assertFalse(any(token in path for token in forbidden_media), path)
        for relative in (
            "patchers/transient~.maxpat",
            "patchers/transient_v10~.maxpat",
            "patchers/transient_v12~.maxpat",
        ):
            patcher = self.load_json(relative)["patcher"]
            text = "\n".join(
                item["box"].get("text", "") + " " + item["box"].get("name", "")
                for item in patcher["boxes"]
            ).lower()
            for token in forbidden_media:
                self.assertNotIn(f"buffer~ {token}", text)
                self.assertNotIn(f"play~ {token}", text)
                self.assertNotIn(f"groove~ {token}", text)

    def test_v5_ice_backfire_is_editable_beap_and_profile_tuned(self):
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        declared = set(project["contents"]["patchers"])
        for profile in ("v10", "v12"):
            beap_path = f"patchers/{profile}_backfire_beap~.maxpat"
            host_path = f"patchers/{profile}_backfire_host~.maxpat"
            self.assertIn(beap_path, declared)
            self.assertIn(host_path, declared)
            beap = self.load_json(beap_path)["patcher"]
            beap_text = "\n".join(
                item["box"].get("text", "") + " "
                + item["box"].get("name", "") + " "
                + item["box"].get("varname", "")
                for item in beap["boxes"]
            )
            for module in (
                "Pressure_Noise", "Pressure_Osc", "Pressure_Body",
                "Pressure_AD", "Pressure_VCA", "Exhaust_Crack",
                "Crack_AD", "Crack_VCA",
            ):
                self.assertIn(module, beap_text)
            self.assertIn("*~ 0.95", beap_text)
            self.assertIn("+~", beap_text)
            host = self.load_json(host_path)["patcher"]
            host_text = "\n".join(item["box"].get("text", "") for item in host["boxes"])
            for control in (
                "rpm", "throttle", "accel", "shift", "shift_dir",
                "intake_backfire", "exhaust_pop", "pop", "overrun",
                "ignition", "engine_running", "backfire_enable", "backfire_intensity",
                "backfire_test",
            ):
                self.assertIn(control, host_text)
            self.assertIn("pak 1 0 0", host_text)
            self.assertIn("($i1 != 0) && ($i2 != 0) && ($i3 != 0)", host_text)
            expected_gain = (
                "0.68*(0.60+0.85*$f1)*(0.55+0.45*$f2)"
                if profile == "v10"
                else "0.68*(0.66+0.94*$f1)*(0.55+0.45*$f2)"
            )
            self.assertIn(expected_gain, host_text)
            self.assertIn("noise~", host_text)
            self.assertIn("lores~", host_text)
            self.assertIn("click~", host_text)
            self.assertIn("onepole~", host_text)
            self.assertIn("GENERATED PRESSURE CORE", host_text)
            self.assertIn("LOW PRESSURE MODES — coherent below 120 Hz", host_text)
            self.assertIn("reson~", host_text)
            self.assertNotIn("($f1 < -0.18) && ($f2 > 1400.)", host_text)
            self.assertIn(f"{profile}_backfire_beap~", host_text)
            runtime = self.load_json(f"VehicleSoundSynth-{profile.upper()}.maxpat")["patcher"]
            runtime_text = "\n".join(item["box"].get("text", "") for item in runtime["boxes"])
            for token in ("Backfire Solo / Test Pop", "prepend backfire_solo", "backfire_test 1"):
                self.assertIn(token, runtime_text)
            engine = self.load_json(f"patchers/vehicle_engine_{profile}~.maxpat")["patcher"]
            engine_text = "\n".join(item["box"].get("text", "") for item in engine["boxes"])
            self.assertIn("route soundscape_solo pad_solo backfire_solo dna_solo", engine_text)
            self.assertIn("expr $i3+(1-$i3)*(1-max($i1,$i2))", engine_text)
            self.assertIn("expr (1-$i3)*(1-max($i1,$i2))", engine_text)
            self.assertIn("expr (1-$i3)*(1-$i1*(1-$i2))", engine_text)
            self.assertIn("expr (1-$i3)*(1-$i2)", engine_text)
        v10 = json.dumps(self.load_json("patchers/v10_backfire_beap~.maxpat"), sort_keys=True)
        v12 = json.dumps(self.load_json("patchers/v12_backfire_beap~.maxpat"), sort_keys=True)
        self.assertNotEqual(v10, v12)

    def test_backfire_intensity_drives_layered_pressure_crack_and_tail_colour(self):
        for profile in ("v10", "v12"):
            beap = self.load_json(f"patchers/{profile}_backfire_beap~.maxpat")["patcher"]
            beap_text = "\n".join(
                item["box"].get("text", "") + " "
                + item["box"].get("varname", "")
                for item in beap["boxes"]
            )
            for layer in ("PRESSURE BODY", "EXHAUST CRACK", "TAIL COLOR / OUTPUT"):
                self.assertIn(layer, beap_text)
            for module in ("Pressure_Body", "Pressure_AD", "Pressure_VCA",
                           "Exhaust_Crack", "Crack_AD", "Crack_VCA"):
                self.assertIn(module, beap_text)
            self.assertIn("tanh~", beap_text)

            boxes = {item["box"]["id"]: item["box"] for item in beap["boxes"]}
            self.assertFalse(any(box.get("text") == "noise~" for box in boxes.values()))
            sources_by_text = {}
            for line in beap["lines"]:
                patchline = line["patchline"]
                source_id = patchline["source"][0]
                dest_id = patchline["destination"][0]
                sources_by_text.setdefault(boxes[dest_id].get("text", ""), set()).add(
                    boxes[source_id].get("varname", "")
                )
            body_compat = next(text for text in sources_by_text if text.startswith("lores~"))
            crack_compat = next(text for text in sources_by_text if text.startswith("svf~") and "180 " not in text)
            self.assertIn("Pressure_Mixer", sources_by_text[body_compat])
            self.assertIn("Pressure_Mixer", sources_by_text[crack_compat])

            host = self.load_json(f"patchers/{profile}_backfire_host~.maxpat")["patcher"]
            host_text = "\n".join(item["box"].get("text", "") for item in host["boxes"])
            self.assertIn("max(0.,min(1.,($f1-0.35)/0.65))", host_text)
            expected_gain = (
                "0.68*(0.60+0.85*$f1)*(0.55+0.45*$f2)"
                if profile == "v10"
                else "0.68*(0.66+0.94*$f1)*(0.55+0.45*$f2)"
            )
            self.assertIn(expected_gain, host_text)
            self.assertIn("*~ 4.8", host_text)
            self.assertIn("onepole~", host_text)
            self.assertIn("*~ 8" if profile == "v10" else "*~ 6", host_text)
            self.assertIn(
                "onepole~ 28" if profile == "v10" else "onepole~ 24",
                host_text,
            )
            self.assertNotIn("*~ 58" if profile == "v10" else "*~ 44", host_text)
            self.assertNotIn("*~ 115" if profile == "v10" else "*~ 92", host_text)

    def test_pop_designer_controls_the_live_beap_and_dominant_pressure_core(self):
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        self.assertIn("code/pop_state_path.js", project["contents"]["code"])
        state_helper = (ROOT / "code" / "pop_state_path.js").read_text(
            encoding="utf-8"
        )
        self.assertIn('"/presets/local/" + profile + "_pop.json"', state_helper)
        self.assertIn('outlet(0, "store", 1)', state_helper)
        self.assertIn('outlet(0, "write", statePath())', state_helper)
        control_varnames = {
            "pop_global_pitch_semitones",
            "pop_impact_drop_octaves",
            "pop_core_presence",
            "pop_body_tune",
            "pop_crack_tune",
            "pop_decay_scale",
            "pop_low_pressure_level",
            "pop_body_level",
            "pop_crack_level",
        }
        for profile in ("v10", "v12"):
            runtime = json.dumps(self.load_json(f"VehicleSoundSynth-{profile.upper()}.maxpat"))
            address = f"open.{profile}.backfire"
            self.assertIn("Open Pop Designer", runtime)
            self.assertIn(f"s {address}", runtime)
            self.assertNotIn(
                f"loadunique Patcher:/patchers/{profile}_backfire_beap~.maxpat",
                runtime,
            )

            beap = self.load_json(f"patchers/{profile}_backfire_beap~.maxpat")["patcher"]
            beap_text = json.dumps(beap)
            self.assertIn(f"r {address}", beap_text)
            self.assertIn('"text": "front"', beap_text)
            self.assertIn('"text": "thispatcher"', beap_text)
            self.assertIn('"text": "Save Pop"', beap_text)
            self.assertIn('"text": "Reload Pop"', beap_text)
            self.assertIn('"text": "autopattr @autorestore 0"', beap_text)
            self.assertIn(f'"text": "pattrstorage {profile}_pop ', beap_text)
            self.assertIn(
                f'"text": "js Patcher:/code/pop_state_path.js {profile}"',
                beap_text,
            )
            self.assertIn(
                '"text": "delay 50"',
                beap_text,
                "saved Pop controls must emit after the host abstraction finishes loading",
            )
            varnames = {
                item["box"].get("varname")
                for item in beap["boxes"]
                if item["box"].get("varname")
            }
            self.assertTrue(control_varnames.issubset(varnames))
            expected_initials = {
                "v10": {
                    "pop_global_pitch_semitones": -5.0,
                    "pop_impact_drop_octaves": 0.85,
                    "pop_core_presence": 1.10,
                    "pop_body_tune": 1.0,
                    "pop_crack_tune": 1.0,
                    "pop_decay_scale": 0.75,
                    "pop_low_pressure_level": 1.0,
                    "pop_body_level": 1.30,
                    "pop_crack_level": 0.008,
                },
                "v12": {
                    "pop_global_pitch_semitones": -6.0,
                    "pop_impact_drop_octaves": 0.75,
                    "pop_core_presence": 1.15,
                    "pop_body_tune": 1.0,
                    "pop_crack_tune": 1.0,
                    "pop_decay_scale": 0.62,
                    "pop_low_pressure_level": 1.0,
                    "pop_body_level": 1.35,
                    "pop_crack_level": 0.006,
                },
            }[profile]
            for item in beap["boxes"]:
                box = item["box"]
                if box.get("varname") not in expected_initials:
                    continue
                self.assertEqual(1, box.get("parameter_enable"))
                self.assertEqual(
                    [expected_initials[box["varname"]]],
                    box["saved_attribute_attributes"]["valueof"]["parameter_initial"],
                )
                self.assertEqual(
                    1,
                    box["saved_attribute_attributes"]["valueof"][
                        "parameter_initial_enable"
                    ],
                    "factory values keep first launch audible before local recall",
                )
            self.assertEqual(
                2,
                sum(item["box"].get("maxclass") == "outlet" for item in beap["boxes"]),
            )
            ordered_outlets = [
                item["box"] for item in beap["boxes"]
                if item["box"].get("maxclass") == "outlet"
            ]
            self.assertEqual(
                ["signal", "signal"],
                [box.get("comment") for box in ordered_outlets[:2]],
                "the editable abstraction owns audio only; tuning uses named buses",
            )

            host = self.load_json(f"patchers/{profile}_backfire_host~.maxpat")["patcher"]
            host_boxes = [item["box"] for item in host["boxes"]]
            beap_host = next(
                box for box in host_boxes
                if box.get("text") == f"{profile}_backfire_beap~"
            )
            self.assertEqual(4, beap_host["numinlets"])
            self.assertEqual(2, beap_host["numoutlets"])
            beap_host_id = beap_host["id"]
            pressure_noise_id = next(
                box["id"] for box in host_boxes if box.get("text") == "noise~"
            )
            self.assertIn(
                (pressure_noise_id, 0, beap_host_id, 3),
                {
                    (
                        line["patchline"]["source"][0],
                        line["patchline"]["source"][1],
                        line["patchline"]["destination"][0],
                        line["patchline"]["destination"][1],
                    )
                    for line in host["lines"]
                },
            )
            host_text = "\n".join(box.get("text", "") for box in host_boxes)
            self.assertNotIn("pak 0. 0. 0.", host_text)
            self.assertNotIn("pak 0. 0.", host_text)
            for varname in control_varnames:
                control_name = varname.removeprefix("pop_")
                self.assertIn(f"s {profile}.pop.{control_name}", beap_text)
                self.assertIn(f"r {profile}.pop.{control_name}", host_text)
            for default_text in (
                "loadmess 0.85" if profile == "v10" else "loadmess 0.75",
                "loadmess 1",
                "loadmess 0.008" if profile == "v10" else "loadmess 0.006",
            ):
                self.assertIn(default_text, host_text)
            self.assertIn("line 1.", host_text)
            self.assertGreaterEqual(host_text.count("*~ 1."), 6)
            for token in (
                "pow(2.,($f1+$f2)/12.)",
                "clip 0.25 1.5",
                "expr 3.8/max(0.5,$f1)" if profile == "v10" else "expr 3.4/max(0.5,$f1)",
            ):
                self.assertIn(token, host_text)
            self.assertNotIn("sqrt(max(0.,2.*(1.-$f1)))", host_text)
            self.assertNotIn("sqrt(max(0.,2.*$f1))", host_text)

    def test_backfire_defaults_prioritize_low_pressure_body_over_bright_crack(self):
        expected = {
            "v10": {
                "mixer": {"in1": -20, "in2": -4},
                "body": {"Freq": 180, "Res": 6},
                "body_ad": {"Attack": 2, "Decay": 80},
                "crack": {"Freq": 420, "Res": 2},
                "crack_ad": {"Attack": 1, "Decay": 8},
                "host": ("lores~ 180 0.74", "lores~ 240 0.7", "svf~ 420 0.66", "svf~ 520 0.64", "lores~ 600 0.65"),
            },
            "v12": {
                "mixer": {"in1": -22, "in2": -5},
                "body": {"Freq": 150, "Res": 6},
                "body_ad": {"Attack": 5, "Decay": 90},
                "crack": {"Freq": 360, "Res": 2},
                "crack_ad": {"Attack": 2, "Decay": 10},
                "host": ("lores~ 150 0.76", "lores~ 210 0.72", "svf~ 360 0.68", "svf~ 450 0.66", "lores~ 520 0.67"),
            },
        }

        def restore_for(box):
            matches = []

            def visit(value):
                if isinstance(value, dict):
                    if isinstance(value.get("restore"), dict):
                        matches.append(value["restore"])
                    for child in value.values():
                        visit(child)
                elif isinstance(value, list):
                    for child in value:
                        visit(child)

            visit(box)
            self.assertEqual(1, len(matches))
            return {key: values[0] for key, values in matches[0].items()}

        for profile, values in expected.items():
            beap = self.load_json(f"patchers/{profile}_backfire_beap~.maxpat")["patcher"]
            modules = {
                item["box"].get("varname"): item["box"] for item in beap["boxes"]
            }
            for module, key in (
                ("Pressure_Mixer", "mixer"),
                ("Pressure_Body", "body"),
                ("Pressure_AD", "body_ad"),
                ("Exhaust_Crack", "crack"),
                ("Crack_AD", "crack_ad"),
            ):
                restored = restore_for(modules[module])
                for parameter, target in values[key].items():
                    self.assertEqual(target, restored[parameter])
            host_text = "\n".join(
                item["box"].get("text", "")
                for item in self.load_json(f"patchers/{profile}_backfire_host~.maxpat")["patcher"]["boxes"]
            )
            for token in values["host"]:
                self.assertIn(token, host_text)
            self.assertIn("LOW PRESSURE MODES — coherent below 120 Hz", host_text)

    def test_pop_uses_kick_pitch_drop_and_single_hit_audition(self):
        expected = {
            "v10": {
                "pitch": "52.+0.002*$f1",
                "sweep": "$1 0, $2 45",
                "gate": "110.*$f1",
                "mixer": {"in1": -20, "in2": -4},
                "filters": ("lores~ 180 0.74", "lores~ 240 0.7", "svf~ 420 0.66", "svf~ 520 0.64", "lores~ 600 0.65"),
                "drop": 0.85,
            },
            "v12": {
                "pitch": "46.5+0.0017*$f1",
                "sweep": "$1 0, $2 50",
                "gate": "125.*$f1",
                "mixer": {"in1": -22, "in2": -5},
                "filters": ("lores~ 150 0.76", "lores~ 210 0.72", "svf~ 360 0.68", "svf~ 450 0.66", "lores~ 520 0.67"),
                "drop": 0.75,
            },
        }

        def restore_for(box):
            matches = []

            def visit(value):
                if isinstance(value, dict):
                    if isinstance(value.get("restore"), dict):
                        matches.append(value["restore"])
                    for child in value.values():
                        visit(child)
                elif isinstance(value, list):
                    for child in value:
                        visit(child)

            visit(box)
            self.assertEqual(1, len(matches))
            return {key: values[0] for key, values in matches[0].items()}

        for profile, values in expected.items():
            beap = self.load_json(f"patchers/{profile}_backfire_beap~.maxpat")["patcher"]
            modules = {item["box"].get("varname"): item["box"] for item in beap["boxes"]}
            self.assertIn("pop_impact_drop_octaves", modules)
            self.assertEqual(
                [values["drop"]],
                modules["pop_impact_drop_octaves"]["saved_attribute_attributes"]["valueof"]["parameter_initial"],
            )
            self.assertEqual(values["mixer"], {
                name: restore_for(modules["Pressure_Mixer"])[name]
                for name in ("in1", "in2")
            })
            beap_text = "\n".join(item["box"].get("text", "") for item in beap["boxes"])
            self.assertIn(f"s {profile}.pop.impact_drop_octaves", beap_text)
            self.assertIn(f"s {profile}.pop.audition_one_hit", beap_text)
            self.assertIn("Audition One Hit", beap_text)

            host = self.load_json(f"patchers/{profile}_backfire_host~.maxpat")["patcher"]
            host_text = "\n".join(item["box"].get("text", "") for item in host["boxes"])
            self.assertIn(values["pitch"], host_text)
            self.assertIn(values["sweep"], host_text)
            self.assertIn(values["gate"], host_text)
            self.assertNotIn("48.+0.018*$f1", host_text)
            self.assertIn(f"r {profile}.pop.impact_drop_octaves", host_text)
            self.assertIn(f"r {profile}.pop.audition_one_hit", host_text)
            for token in values["filters"]:
                self.assertIn(token, host_text)

    def test_v5_all_profiles_share_one_editable_cinematic_soundscape_core(self):
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        declared = set(project["contents"]["patchers"])
        core_path = "patchers/cinematic_soundscape_beap~.maxpat"
        voice_path = "patchers/cinematic_soundscape_voice.maxpat"
        self.assertIn(core_path, declared)
        self.assertNotIn(voice_path, declared)
        core = self.load_json(core_path)["patcher"]
        core_text = "\n".join(item["box"].get("text", "") for item in core["boxes"])
        self.assertIn("USER-TUNABLE", core_text)
        for module in ("Osc_A", "Osc_B", "Noise", "Mixer", "Ladder", "LFO", "ADSR", "VCA", "Chorus", "Reverb"):
            self.assertIn(module, json.dumps(core))
        self.assertNotIn("saw~", core_text.lower())
        self.assertNotIn("rect~", core_text.lower())

        preset_names = {"ev": "Future EV", "v10": "Aggressive V10", "v12": "High-Rev V12"}
        for profile in ("ev", "v10", "v12"):
            host_path = f"patchers/{profile}_cinematic_soundscape_host~.maxpat"
            self.assertIn(host_path, declared)
            host = self.load_json(host_path)["patcher"]
            host_text = "\n".join(item["box"].get("text", "") for item in host["boxes"])
            for control in (
                "rpm", "throttle", "load", "accel", "shift", "ignition", "start",
                "soundscape_enable", "soundscape_level_db", "soundscape_motion", "soundscape_space",
                "pad_level_db", "pad_mute",
            ):
                self.assertIn(control, host_text)
            self.assertIn(f"cinematic_soundscape_beap~ {profile}", host_text)
            self.assertIn("mute~", host_text)
            engine = self.load_json(f"patchers/vehicle_engine_{profile}~.maxpat")["patcher"]
            engine_text = "\n".join(item["box"].get("text", "") for item in engine["boxes"])
            self.assertIn(f"{profile}_cinematic_soundscape_host~", engine_text)
            runtime = self.load_json(f"VehicleSoundSynth-{profile.upper()}.maxpat")["patcher"]
            self.assertTrue(any(
                item["box"].get("name") == "Patcher:/patchers/soundscape_control.maxpat"
                for item in runtime["boxes"]
            ))
            self.assertTrue(any(
                item["box"].get("name") == "Patcher:/patchers/module_mixer.maxpat"
                for item in runtime["boxes"]
            ))

    def test_v5_vehicle_bus_eq_has_profile_local_persistent_state(self):
        self.assertTrue((ROOT / "presets" / "local" / ".gitkeep").is_file())
        ignore_rules = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("presets/local/*", ignore_rules)
        self.assertIn("!presets/local/.gitkeep", ignore_rules)
        eq = self.load_json("patchers/vehicle_bus_eq~.maxpat")["patcher"]
        text = "\n".join(item["box"].get("text", "") for item in eq["boxes"])
        self.assertIn("autopattr", text)
        self.assertIn("pattrstorage vehicle_bus_eq_#1", text)
        self.assertIn("Patcher:/presets/vehicle_bus_eq_default.json", text)
        self.assertIn("js Patcher:/code/eq_state_path.js #1", text)
        self.assertIn("save", text)
        self.assertNotIn("r vehicle_bus_eq.save", text)
        self.assertNotIn("dict vehicle_bus_eq_defaults", text)
        self.assertNotIn("delay 20", text)
        self.assertIn("delay 30", text)
        for label in ("Save EQ", "Reload EQ", "Reset EQ"):
            self.assertIn(label, text)
        default = self.load_json("presets/vehicle_bus_eq_default.json")
        self.assertEqual(1, default["schema_version"])
        self.assertEqual(
            {"eq_low", "eq_lowmid", "eq_highmid", "eq_high", "eq_bypass"},
            set(default["bands"]),
        )
        for profile in ("ev", "v10", "v12"):
            runtime = self.load_json(
                f"VehicleSoundSynth-{profile.upper()}.maxpat"
            )["patcher"]
            runtime_text = "\n".join(item["box"].get("text", "") for item in runtime["boxes"])
            self.assertNotIn('"text": "write"', json.dumps(runtime))
            self.assertNotIn("s vehicle_bus_eq.save", runtime_text)
            engine = json.dumps(
                self.load_json(f"patchers/vehicle_engine_{profile}~.maxpat")
            )
            self.assertIn(f'"args": ["{profile}"]', engine)
        path_helper = (ROOT / "code" / "eq_state_path.js").read_text(encoding="utf-8")
        self.assertIn("this.patcher.filepath", path_helper)
        self.assertIn('profile + "_vehicle_bus_eq.json"', path_helper)
        self.assertIn("/presets/local/vehicle_bus_eq.json", path_helper)
        self.assertIn('outlet(0, "store", 1)', path_helper)

    def test_v5_generator_preserves_all_user_tuned_ice_beap_patchers(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            command = [
                sys.executable,
                str(ROOT / "tools" / "build_project.py"),
                "--output-root",
                str(destination),
            ]
            subprocess.run(command, check=True, cwd=ROOT, capture_output=True, text=True)
            for profile in ("v10", "v12"):
                for role in ("pad", "backfire"):
                    path = destination / "patchers" / f"{profile}_{role}_beap~.maxpat"
                    payload = self.load_json(path.relative_to(ROOT)) if False else json.loads(path.read_text())
                    payload["patcher"]["description"] = f"{profile}-{role}-user-tuning"
                    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
                    before = path.read_bytes()
                    subprocess.run(command, check=True, cwd=ROOT, capture_output=True, text=True)
                    self.assertEqual(before, path.read_bytes())

    def test_v5_generator_preserves_shared_cinematic_soundscape_tuning(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            command = [
                sys.executable,
                str(ROOT / "tools" / "build_project.py"),
                "--output-root",
                str(destination),
            ]
            subprocess.run(command, check=True, cwd=ROOT, capture_output=True, text=True)
            path = destination / "patchers" / "cinematic_soundscape_beap~.maxpat"
            payload = json.loads(path.read_text())
            payload["patcher"]["description"] = "shared-soundscape-user-tuning"
            path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
            before = path.read_bytes()
            subprocess.run(command, check=True, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(before, path.read_bytes())

    def test_v5_generator_preserves_user_tuned_engine_start_beap(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            command = [
                sys.executable,
                str(ROOT / "tools" / "build_project.py"),
                "--output-root",
                str(destination),
            ]
            subprocess.run(command, check=True, cwd=ROOT, capture_output=True, text=True)
            path = destination / "patchers" / "engine_start_beap~.maxpat"
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["patcher"]["description"] = "user-start-colour-tuning"
            path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
            before = path.read_bytes()
            subprocess.run(command, check=True, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(before, path.read_bytes())

    def test_sound_design_is_split_into_user_owned_dna_eq_and_soundscape_modules(self):
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        declared = set(project["contents"]["patchers"])
        self.assertIn("patchers/vehicle_bus_eq~.maxpat", declared)
        for profile in ("ev", "v10", "v12"):
            dna_path = f"patchers/{profile}_sound_dna~.maxpat"
            self.assertIn(dna_path, declared)
            dna = self.load_json(dna_path)["patcher"]
            dna_text = "\n".join(
                item["box"].get("text", "") + " " + item["box"].get("varname", "")
                for item in dna["boxes"]
            )
            self.assertIn("USER-TUNABLE SOUND DNA", dna_text)
            self.assertIn(f"{profile}_powertrain~", dna_text)
            self.assertIn(f"js Patcher:/code/dna_state_path.js {profile}", dna_text)
            for control in (
                "aggression", "brightness", "body", "texture", "air_detail",
                "cycle_irregularity", "stereo_width", "throttle_loudness_depth",
                "saturation",
            ):
                self.assertIn(control, dna_text)
            engine = self.load_json(f"patchers/vehicle_engine_{profile}~.maxpat")["patcher"]
            engine_text = "\n".join(
                item["box"].get("text", "") + " " + item["box"].get("name", "")
                for item in engine["boxes"]
            )
            self.assertIn(f"{profile}_sound_dna~", engine_text)
            self.assertNotIn(f"{profile}_powertrain~", engine_text)
            self.assertIn("vehicle_bus_eq~.maxpat", engine_text)

        mix = self.load_json("patchers/mix_master~.maxpat")["patcher"]
        mix_text = "\n".join(item["box"].get("text", "") for item in mix["boxes"])
        self.assertNotIn("filtergraph~", mix_text)
        self.assertNotIn("pattrstorage vehicle_bus_eq", mix_text)
        self.assertIn("omx.comp~", mix_text)
        self.assertIn("omx.peaklim~", mix_text)

        eq = self.load_json("patchers/vehicle_bus_eq~.maxpat")["patcher"]
        eq_text = "\n".join(
            item["box"].get("text", "") + " " + item["box"].get("maxclass", "")
            for item in eq["boxes"]
        )
        self.assertIn("USER-TUNABLE VEHICLE BUS EQ", eq_text)
        self.assertIn("filtergraph~", eq_text)
        self.assertIn("pattrstorage vehicle_bus_eq", eq_text)
        self.assertNotIn("omx.comp~", eq_text)
        self.assertNotIn("omx.peaklim~", eq_text)

    def test_generator_preserves_user_owned_sound_dna_and_bus_eq_tuning(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            command = [
                sys.executable,
                str(ROOT / "tools" / "build_project.py"),
                "--output-root",
                str(destination),
            ]
            subprocess.run(command, check=True, cwd=ROOT, capture_output=True, text=True)
            paths = [destination / "patchers" / "vehicle_bus_eq~.maxpat"]
            paths.extend(destination / "patchers" / f"{p}_sound_dna~.maxpat" for p in ("ev", "v10", "v12"))
            for path in paths:
                payload = json.loads(path.read_text())
                payload["patcher"]["description"] = "user-tuning-must-survive"
                path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
                before = path.read_bytes()
                subprocess.run(command, check=True, cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(before, path.read_bytes(), path.name)

    def test_sound_dna_exposes_realism_controls_without_direct_throttle_pitch(self):
        defaults = self.load_json("presets/sound_dna.json")
        preset_names = {"ev": "Future EV", "v10": "Aggressive V10", "v12": "High-Rev V12"}
        for profile in ("ev", "v10", "v12"):
            code = "\n".join(
                item["box"].get("code", "")
                for item in self.load_json(f"gen/{profile}_powertrain.gendsp")["patcher"]["boxes"]
            ).lower()
            for parameter in (
                "air_detail", "cycle_irregularity", "stereo_width",
                "throttle_loudness_depth", "saturation",
            ):
                self.assertIn(f"param {parameter}", code)
            self.assertIn("pow(10, (t * throttle_loudness_depth) / 20)", code)
            self.assertIn("tone_t =", code)
            self.assertRegex(code, r"tone_t\s*=.*\bt\s*\*")
            frequency_region = code.split("throttle_gain", 1)[0]
            self.assertNotRegex(frequency_region, r"\bt\s*\*")
            preset = defaults[preset_names[profile]]
            self.assertGreaterEqual(preset["throttle_loudness_depth"], 4.0)
            self.assertLessEqual(preset["throttle_loudness_depth"], 5.0)
            self.assertIn("stereo_width", code)
            if profile in ("v10", "v12"):
                # Both banks share one physical firing cadence. Stereo colour
                # comes from bank phase/amplitude and manifold modes, not
                # detuning the engine's dominant harmonic order.
                self.assertIn("orders_r = cycle(fire)", code)
                self.assertNotRegex(code, r"orders_r\s*=\s*cycle\(clamp\(fire\s*\*")

    def test_every_visible_sound_dna_control_reaches_the_generated_dsp(self):
        for profile in ("ev", "v10", "v12"):
            dna = self.load_json(f"patchers/{profile}_sound_dna~.maxpat")["patcher"]
            visible_controls = {
                item["box"]["varname"].removeprefix("dna_")
                for item in dna["boxes"]
                if item["box"].get("varname", "").startswith("dna_")
            }
            code = "\n".join(
                item["box"].get("code", "")
                for item in self.load_json(f"gen/{profile}_powertrain.gendsp")["patcher"]["boxes"]
            ).lower()
            for parameter in visible_controls:
                declaration = f"param {parameter}("
                self.assertIn(declaration, code)
                dsp_body = code.split(declaration, 1)[1].split(";", 1)[1]
                self.assertRegex(
                    dsp_body,
                    rf"\b{parameter}\b",
                    f"{profile} Sound DNA control {parameter} is declared but acoustically disconnected",
                )

    def test_runtime_open_sound_dna_targets_the_audible_instance(self):
        for profile in ("ev", "v10", "v12"):
            runtime = json.dumps(self.load_json(f"VehicleSoundSynth-{profile.upper()}.maxpat"))
            dna = json.dumps(self.load_json(f"patchers/{profile}_sound_dna~.maxpat"))
            address = f"open.{profile}.sound_dna"
            self.assertIn(f"s {address}", runtime)
            self.assertNotIn(f"loadunique Patcher:/patchers/{profile}_sound_dna~.maxpat", runtime)
            self.assertIn(f"r {address}", dna)
            self.assertIn('"text": "front"', dna)
            self.assertIn('"text": "thispatcher"', dna)

    def test_runtime_open_soundscape_targets_the_audible_live_instance(self):
        core = json.dumps(
            self.load_json("patchers/cinematic_soundscape_beap~.maxpat")
        )
        self.assertIn("route open save reload reset", core)
        self.assertIn('"text": "front"', core)
        self.assertIn('"text": "thispatcher"', core)
        self.assertIn('"text": "Save Parameters"', core)
        self.assertIn('"text": "Save Graph Layout"', core)
        self.assertNotIn("r open.cinematic_soundscape", core)
        for profile in ("ev", "v10", "v12"):
            runtime = json.dumps(
                self.load_json(f"VehicleSoundSynth-{profile.upper()}.maxpat")
            )
            self.assertIn("Patcher:/patchers/soundscape_control.maxpat", runtime)
            self.assertNotIn("s open.cinematic_soundscape", runtime)
            self.assertNotIn(
                "loadunique Patcher:/patchers/cinematic_soundscape_beap~.maxpat",
                runtime,
            )
            host = json.dumps(
                self.load_json(
                    f"patchers/{profile}_cinematic_soundscape_host~.maxpat"
                )
            )
            self.assertIn(f"cinematic_soundscape_beap~ {profile}", host)
            self.assertIn(
                "min(1.,max(0.,$f2*(0.25+0.75*$f1)))",
                host,
                "Motion must be the maximum depth and throttle its smooth scaler",
            )

    def test_soundscape_pitch_follow_restores_the_legacy_rpm_curve(self):
        legacy_frequency = {
            "ev": "55.+0.032*$f1",
            "v10": "36.7+0.014*$f1",
            "v12": "32.7+0.012*$f1",
        }
        for profile, frequency in legacy_frequency.items():
            host = json.dumps(
                self.load_json(
                    f"patchers/{profile}_cinematic_soundscape_host~.maxpat"
                )
            )
            self.assertIn(frequency, host)
            self.assertIn("loadmess 1", host)
            self.assertIn("pack 0. 90", host)
            self.assertNotIn("$f1*$f1*(3.-2.*$f1)", host)

    def test_launcher_soundscape_controls_the_selected_audible_runtime(self):
        launcher = self.load_json("main.maxpat")["patcher"]
        boxes = {item["box"]["id"]: item["box"] for item in launcher["boxes"]}
        lines = [item["patchline"] for item in launcher["lines"]]
        control_id = next(
            box_id for box_id, box in boxes.items()
            if box.get("name") == "Patcher:/patchers/soundscape_control.maxpat"
        )
        selection_map = next(
            box_id for box_id, box in boxes.items()
            if box.get("text") == "sel ev v10 v12 none"
        )
        command_gate = next(
            box_id for box_id, box in boxes.items()
            if box.get("text") == "gate 3"
        )
        feedback_selector = next(
            box_id for box_id, box in boxes.items()
            if box.get("text") == "switch 3"
        )
        command_buses = {
            profile: next(
                box_id for box_id, box in boxes.items()
                if box.get("text") == f"s vss.runtime.control.{profile}"
            )
            for profile in ("ev", "v10", "v12")
        }
        feedback_buses = {
            profile: next(
                box_id for box_id, box in boxes.items()
                if box.get("text") == f"r vss.soundscape.feedback.{profile}"
            )
            for profile in ("ev", "v10", "v12")
        }
        texts = {box.get("text") for box in boxes.values()}
        self.assertNotIn("s vss.runtime.control", texts)
        self.assertNotIn("r vss.soundscape.feedback", texts)
        self.assertIn(
            ((control_id, 0), (command_gate, 1)),
            {(tuple(line["source"]), tuple(line["destination"])) for line in lines},
        )
        self.assertIn(
            ((feedback_selector, 0), (control_id, 0)),
            {(tuple(line["source"]), tuple(line["destination"])) for line in lines},
        )
        cords = {
            (tuple(line["source"]), tuple(line["destination"])) for line in lines
        }
        for index, profile in enumerate(("ev", "v10", "v12"), start=1):
            index_message = next(
                box_id for box_id, box in boxes.items()
                if box.get("maxclass") == "message" and box.get("text") == str(index)
            )
            self.assertIn(((selection_map, index - 1), (index_message, 0)), cords)
            self.assertIn(((index_message, 0), (command_gate, 0)), cords)
            self.assertIn(((index_message, 0), (feedback_selector, 0)), cords)
            self.assertIn(((command_gate, index - 1), (command_buses[profile], 0)), cords)
            self.assertIn(((feedback_buses[profile], 0), (feedback_selector, index)), cords)
        selection_off = next(
            box_id for box_id, box in boxes.items()
            if box.get("maxclass") == "message" and box.get("text") == "0"
        )
        self.assertIn(((selection_map, 3), (selection_off, 0)), cords)
        self.assertIn(((selection_off, 0), (command_gate, 0)), cords)
        self.assertIn(((selection_off, 0), (feedback_selector, 0)), cords)
        self.assertTrue(
            any(tuple(line["destination"]) == (selection_map, 0) for line in lines),
            "Profile selection must also drive the Main control/feedback selector",
        )

        for profile in ("ev", "v10", "v12"):
            runtime = self.load_json(
                f"VehicleSoundSynth-{profile.upper()}.maxpat"
            )["patcher"]
            runtime_boxes = {
                item["box"]["id"]: item["box"] for item in runtime["boxes"]
            }
            runtime_lines = [item["patchline"] for item in runtime["lines"]]
            engine_id = next(
                box_id for box_id, box in runtime_boxes.items()
                if box.get("name", "").endswith(
                    f"/patchers/vehicle_engine_{profile}~.maxpat"
                )
            )
            command_receive = next(
                box_id for box_id, box in runtime_boxes.items()
                if box.get("text") == f"r vss.runtime.control.{profile}"
            )
            feedback_send = next(
                box_id for box_id, box in runtime_boxes.items()
                if box.get("text") == f"s vss.soundscape.feedback.{profile}"
            )
            runtime_texts = {box.get("text") for box in runtime_boxes.values()}
            self.assertNotIn("r vss.runtime.control", runtime_texts)
            self.assertNotIn("s vss.soundscape.feedback", runtime_texts)
            cords = {
                (tuple(line["source"]), tuple(line["destination"]))
                for line in runtime_lines
            }
            self.assertIn(((command_receive, 0), (engine_id, 0)), cords)
            self.assertIn(((engine_id, 2), (feedback_send, 0)), cords)

    def test_soundscape_live_instance_owns_profile_local_parameter_state(self):
        project = self.load_json("VehicleSoundSynth-V5.maxproj")["contents"]
        self.assertIn("code/soundscape_state_path.js", project["code"])
        self.assertNotIn(
            "patchers/cinematic_soundscape_voice.maxpat",
            project["patchers"],
        )

        core = json.dumps(
            self.load_json("patchers/cinematic_soundscape_beap~.maxpat")
        )
        self.assertIn("soundscape_action save", core)
        self.assertNotIn("r open.cinematic_soundscape", core)

        for profile in ("ev", "v10", "v12"):
            host = json.dumps(
                self.load_json(
                    f"patchers/{profile}_cinematic_soundscape_host~.maxpat"
                )
            )
            self.assertIn(
                f"cinematic_soundscape_beap~ {profile}", host,
                "the editable object must be the instance that feeds the runtime",
            )
            self.assertNotIn("poly~ cinematic_soundscape_voice", host)
            self.assertIn(f"pattrstorage soundscape_{profile}", host)
            self.assertIn(
                f"js Patcher:/code/soundscape_state_path.js {profile}", host
            )
            for command in (
                "soundscape_open", "soundscape_save",
                "soundscape_reload", "soundscape_reset",
            ):
                self.assertIn(command, host)
            patcher = self.load_json(
                f"patchers/{profile}_cinematic_soundscape_host~.maxpat"
            )["patcher"]
            storage_ids = {
                item["box"]["id"] for item in patcher["boxes"]
                if item["box"].get("text", "").startswith(
                    f"pattrstorage soundscape_{profile} "
                )
            }
            self.assertEqual(1, len(storage_ids))
            factory_storage_ids = {
                item["box"]["id"] for item in patcher["boxes"]
                if item["box"].get("text", "").startswith(
                    f"pattrstorage soundscape_{profile}_factory "
                )
            }
            self.assertEqual(
                0, len(factory_storage_ids),
                "a second greedy pattrstorage would create a feedback route",
            )
            state_path_id = next(
                item["box"]["id"] for item in patcher["boxes"]
                if item["box"].get("text")
                == f"js Patcher:/code/soundscape_state_path.js {profile}"
            )
            self.assertEqual(
                2,
                next(
                    item["box"]["numoutlets"] for item in patcher["boxes"]
                    if item["box"]["id"] == state_path_id
                ),
            )
            edges = [item["patchline"] for item in patcher["lines"]]
            local_storage_id = next(iter(storage_ids))
            self.assertIn(
                ([state_path_id, 0], [local_storage_id, 0]),
                [(edge["source"], edge["destination"]) for edge in edges],
            )
            self.assertFalse(
                any(
                    line["patchline"]["source"][0] in storage_ids
                    for line in patcher["lines"]
                ),
                "pattrstorage output must not feed its own save debounce loop",
            )
            text_by_id = {
                item["box"]["id"]: item["box"].get("text", "")
                for item in patcher["boxes"]
            }
            restore_ids = {
                box_id for box_id, text in text_by_id.items()
                if text == "restore"
            }
            restores_with_recall_delay = {
                edge["source"][0] for edge in edges
                if edge["source"][0] in restore_ids
                and text_by_id.get(edge["destination"][0], "").startswith("delay ")
            }
            self.assertEqual(
                restore_ids, restores_with_recall_delay,
                "every restore path, including manual reload, must recall after read",
            )
            recall_ids = {
                box_id for box_id, text in text_by_id.items() if text == "1"
            }
            self.assertTrue(any(
                edge["source"][0] in recall_ids
                and edge["destination"][0] in storage_ids
                for edge in edges
            ), "manual reload must recall slot 1 into live clients")

        helper = (ROOT / "code" / "soundscape_state_path.js").read_text(
            encoding="utf-8"
        )
        self.assertIn("/presets/local/", helper)
        self.assertIn("_soundscape.json", helper)
        self.assertIn('outlet(0, "delete", 99);', helper)
        self.assertIn('outlet(0, "read", factoryPath());', helper)
        self.assertNotIn("setstoredvalue", helper)
        self.assertNotIn("JSON.parse(text)", helper)
        self.assertIn("function prime()", helper)

    def test_soundscape_factory_is_audible_after_ignition_without_hidden_setup(self):
        for profile in ("ev", "v10", "v12"):
            host = self.load_json(
                f"patchers/{profile}_cinematic_soundscape_host~.maxpat"
            )["patcher"]
            boxes = {item["box"]["id"]: item["box"] for item in host["boxes"]}
            lines = [item["patchline"] for item in host["lines"]]
            enable_id = next(
                box_id for box_id, box in boxes.items()
                if box.get("varname") == "soundscape_enable_state"
            )
            incoming_defaults = {
                boxes[line["source"][0]].get("text")
                for line in lines
                if line["destination"] == [enable_id, 0]
                and boxes[line["source"][0]].get("text", "").startswith("loadmess ")
            }
            self.assertEqual(
                {"loadmess 1"}, incoming_defaults,
                "a fresh profile must sound after ignition without a hidden enable step",
            )
            host_text = "\n".join(box.get("text", "") for box in boxes.values())
            self.assertIn("expr $i1*$i2", host_text)

    def test_soundscape_control_is_a_view_of_persistent_profile_host_state(self):
        project = self.load_json("VehicleSoundSynth-V5.maxproj")["contents"]
        self.assertIn("patchers/soundscape_control.maxpat", project["patchers"])
        control = json.dumps(self.load_json("patchers/soundscape_control.maxpat"))
        for label in (
            "Enable", "Motion", "Space", "Pitch Follow", "Transpose",
            "Brightness", "Open Designer", "Save", "Reload", "Factory Reset",
        ):
            self.assertIn(label, control)
        for command in (
            "soundscape_enable", "soundscape_motion", "soundscape_space",
            "soundscape_pitch_follow", "soundscape_transpose",
            "soundscape_brightness", "soundscape_open", "soundscape_save",
            "soundscape_reload", "soundscape_reset",
        ):
            self.assertIn(command, control)

        for profile in ("ev", "v10", "v12"):
            host = self.load_json(
                f"patchers/{profile}_cinematic_soundscape_host~.maxpat"
            )["patcher"]
            host_json = json.dumps(host)
            self.assertIn(f"pattrstorage soundscape_{profile}", host_json)
            self.assertIn(
                f"js Patcher:/code/soundscape_state_path.js {profile}",
                host_json,
            )
            for varname in (
                "soundscape_enable_state", "soundscape_motion_state",
                "soundscape_space_state", "soundscape_pitch_follow_state",
                "soundscape_transpose_state", "soundscape_brightness_state",
            ):
                self.assertTrue(any(
                    item["box"].get("varname") == varname
                    for item in host["boxes"]
                ))

            runtime = self.load_json(
                f"VehicleSoundSynth-{profile.upper()}.maxpat"
            )["patcher"]
            control_box = next(
                item["box"] for item in runtime["boxes"]
                if item["box"].get("name")
                == "Patcher:/patchers/soundscape_control.maxpat"
            )
            self.assertEqual([profile], control_box.get("args"))
            self.assertNotIn("s open.cinematic_soundscape", json.dumps(runtime))

    def test_soundscape_solo_feedback_keeps_main_and_runtime_views_consistent(self):
        control_text = "\n".join(
            item["box"].get("text", "")
            for item in self.load_json(
                "patchers/soundscape_control.maxpat"
            )["patcher"]["boxes"]
        )
        self.assertIn(
            "route enable motion space pitch_follow transpose brightness solo",
            control_text,
        )
        self.assertIn("prepend soundscape_solo", control_text)

        for profile in ("ev", "v10", "v12"):
            engine = self.load_json(
                f"patchers/vehicle_engine_{profile}~.maxpat"
            )["patcher"]
            boxes = {item["box"]["id"]: item["box"] for item in engine["boxes"]}
            lines = [item["patchline"] for item in engine["lines"]]
            solo_clip = next(
                box_id for box_id, box in boxes.items()
                if box.get("text") == "clip 0 1"
                and any(
                    line["source"] == [box_id, 0]
                    and boxes[line["destination"][0]].get("text") == "pak 0 0 0"
                    and line["destination"][1] == 0
                    for line in lines
                )
            )
            feedback = next(
                box_id for box_id, box in boxes.items()
                if box.get("text") == "prepend soundscape_state solo"
            )
            state_out = next(
                box_id for box_id, box in boxes.items()
                if box.get("maxclass") == "outlet"
                and box.get("comment") == "messages"
            )
            cords = {
                (tuple(line["source"]), tuple(line["destination"]))
                for line in lines
            }
            self.assertIn(((solo_clip, 0), (feedback, 0)), cords)
            self.assertIn(((feedback, 0), (state_out, 0)), cords)

    def test_dna_solo_isolates_the_audible_powertrain_from_every_other_stem(self):
        for profile in ("ev", "v10", "v12"):
            runtime_text = json.dumps(
                self.load_json(f"VehicleSoundSynth-{profile.upper()}.maxpat")
            )
            self.assertIn("Sound DNA Solo", runtime_text)
            self.assertIn("prepend dna_solo", runtime_text)

            engine = self.load_json(f"patchers/vehicle_engine_{profile}~.maxpat")["patcher"]
            text = "\n".join(item["box"].get("text", "") for item in engine["boxes"])
            self.assertIn(
                "route soundscape_solo pad_solo backfire_solo dna_solo",
                text,
            )
            self.assertIn("$i3+(1-$i3)*(1-max($i1,$i2))", text)
            self.assertIn("(1-$i3)*(1-max($i1,$i2))", text)
            self.assertIn("(1-$i3)*(1-$i1*(1-$i2))", text)
            self.assertIn("(1-$i3)*(1-$i2)", text)

    def test_fixed_rpm_dna_probe_bypasses_drive_only_for_acoustic_ab(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(
                [
                    sys.executable, str(ROOT / "tools" / "build_runtime_probe.py"),
                    "--bundle-root", directory,
                    "--scenario", "dna-v10-throttle-high",
                    "--rumble", "off", "--tap", "pre-cabin",
                    "--render-ms", "1500", "--start", "off",
                ],
                check=True, cwd=ROOT, capture_output=True, text=True,
            )
            patch = json.loads(
                (Path(directory) / "runtime_probe_v10_dna-v10-throttle-high_off.maxpat").read_text()
            )["patcher"]
            boxes = {item["box"]["id"]: item["box"] for item in patch["boxes"]}
            controller = next(
                box_id for box_id, box in boxes.items()
                if box.get("text") == "engine_controller_v10"
            )
            powertrain = next(
                box_id for box_id, box in boxes.items()
                if box.get("text") == "v10_powertrain~"
            )
            cords = {
                (item["patchline"]["source"][0], item["patchline"]["destination"][0])
                for item in patch["lines"]
            }
            self.assertNotIn((controller, powertrain), cords)
            replay = next(
                box_id for box_id, box in boxes.items()
                if box.get("text", "").startswith("ignition 1, rpm 4200, throttle 0.9")
            )
            self.assertIn((replay, powertrain), cords)

    def test_fixed_state_probes_expose_low_high_pairs_for_repaired_dna_controls(self):
        source = (ROOT / "tools" / "build_runtime_probe.py").read_text(encoding="utf-8")
        for scenario, message in (
            ("dna-ev-aggression-low", "aggression 0"),
            ("dna-ev-aggression-high", "aggression 1"),
            ("dna-v10-brightness-low", "brightness 0"),
            ("dna-v10-brightness-high", "brightness 1"),
        ):
            self.assertIn(f'"{scenario}"', source)
            block = source.split(f'"{scenario}"', 1)[1].split("},", 1)[0]
            self.assertIn('"direct_powertrain": True', block)
            self.assertIn('"lock_rpm": True', block)
            self.assertIn(f'"{message}"', block)

    def test_pop_global_pitch_reaches_every_tonal_layer(self):
        expected = {
            "v10": ((180, 54, 120, 420, 650, 750), (54, 120)),
            "v12": ((150, 48, 105, 360, 550, 650), (48, 105)),
        }
        for profile, (editable_bases, host_bases) in expected.items():
            editable = json.dumps(
                self.load_json(f"patchers/{profile}_backfire_beap~.maxpat")
            )
            host = json.dumps(
                self.load_json(f"patchers/{profile}_backfire_host~.maxpat")
            )
            self.assertIn("expr pow(2.,$f1/12.)", editable)
            for base in editable_bases:
                self.assertIn(
                    f"expr {base}.*$f1*$f2", editable,
                    f"{profile} compatibility/tail layer at {base} Hz ignores Global Pitch",
                )
            for base in host_bases:
                self.assertIn(
                    f"expr {base}.*$f1*$f2", host,
                    f"{profile} low-pressure mode at {base} Hz ignores Global Pitch",
                )

    def test_pop_resonant_mode_tuning_targets_frequency_not_gain_inlet(self):
        expected = {
            "v10": ((54, 120), (54, 120)),
            "v12": ((48, 105), (48, 105)),
        }
        for profile, (editable_bases, host_bases) in expected.items():
            for relative, bases in (
                (f"patchers/{profile}_backfire_beap~.maxpat", editable_bases),
                (f"patchers/{profile}_backfire_host~.maxpat", host_bases),
            ):
                patcher = self.load_json(relative)["patcher"]
                boxes = {item["box"]["id"]: item["box"] for item in patcher["boxes"]}
                cords = {
                    (line["patchline"]["source"][0], line["patchline"]["destination"][0], line["patchline"]["destination"][1])
                    for line in patcher["lines"]
                }
                for base in bases:
                    source = next(
                        box_id for box_id, box in boxes.items()
                        if box.get("text") == f"expr {base}.*$f1*$f2"
                    )
                    destination = next(
                        box_id for box_id, box in boxes.items()
                        if box.get("text", "").startswith("reson~ ")
                        and f" {base} " in f" {box.get('text', '')} "
                    )
                    self.assertIn((source, destination, 2), cords)
                    self.assertNotIn((source, destination, 1), cords)

    def test_fixed_state_probe_matrix_covers_every_visible_dna_parameter(self):
        for profile, specs in DNA_PARAMETER_SPECS.items():
            for parameter, _label, low, high in specs:
                for suffix, value in (("low", low), ("high", high)):
                    scenario = f'dna-{profile}-{parameter}-{suffix}'
                    self.assertIn(scenario, SCENARIOS)
                    config = SCENARIOS[scenario]
                    self.assertTrue(config["direct_powertrain"])
                    self.assertTrue(config["lock_rpm"])
                    self.assertIn(f"{parameter} {value:g}", config["extra_messages"])
            for suffix, value_index in (("all-low", 2), ("all-high", 3)):
                aggregate = SCENARIOS[f"dna-{profile}-{suffix}"]
                for spec in specs:
                    self.assertIn(
                        f"{spec[0]} {spec[value_index]:g}",
                        aggregate["extra_messages"],
                    )

    def test_shared_beap_soundscape_has_three_voice_motion_and_formant_colour(self):
        core = self.load_json("patchers/cinematic_soundscape_beap~.maxpat")["patcher"]
        text = json.dumps(core)
        for token in ("LFO_Slow", "Osc_C", "MMF", "Mixer"):
            self.assertIn(token, text)
        plain = "\n".join(item["box"].get("text", "") for item in core["boxes"])
        self.assertIn("svf~ 70 0.7", plain)
        self.assertNotIn("+~ 0.5849625", plain)
        self.assertNotIn("+~ 1.", plain)
        self.assertNotIn("saw~", plain.lower())
        self.assertNotIn("rect~", plain.lower())

    def test_soundscape_factory_profiles_define_distinct_audible_voicings(self):
        expected = {
            "ev": {
                "soundscape_motion_state": 0.28,
                "soundscape_space_state": 0.46,
                "soundscape_brightness_state": 0.68,
                "Osc_A::Waveform": 1,
                "Osc_A::Offset": 0,
                "Osc_B::Waveform": 2,
                "Osc_B::Offset": 7,
                "Osc_C::Waveform": 0,
                "Osc_C::Offset": 12,
                "Mixer::in1": -6,
                "Mixer::in2": -14,
                "Mixer::in4": -18,
                "Ladder::Freq": 1900,
                "Chorus::Width": 18,
            },
            "v10": {
                "soundscape_motion_state": 0.10,
                "soundscape_space_state": 0.32,
                "soundscape_brightness_state": 0.38,
                "Osc_A::Waveform": 1,
                "Osc_A::Offset": -5,
                "Osc_B::Waveform": 2,
                "Osc_B::Offset": 0,
                "Osc_C::Waveform": 0,
                "Osc_C::Offset": 7,
                "Mixer::in1": -3,
                "Mixer::in2": -9,
                "Mixer::in4": -5,
                "Ladder::Freq": 1050,
                "Chorus::Width": 7,
            },
            "v12": {
                "soundscape_motion_state": 0.16,
                "soundscape_space_state": 0.46,
                "soundscape_brightness_state": 0.50,
                "Osc_A::Waveform": 0,
                "Osc_A::Offset": 0,
                "Osc_B::Waveform": 1,
                "Osc_B::Offset": 7,
                "Osc_C::Waveform": 0,
                "Osc_C::Offset": 12,
                "Mixer::in1": -5,
                "Mixer::in2": -8,
                "Mixer::in4": -13,
                "Ladder::Freq": 1450,
                "Chorus::Width": 15,
            },
        }
        for profile, values in expected.items():
            preset = self.load_json(
                f"presets/{profile}_soundscape_factory.json"
            )["pattrstorage"]
            self.assertEqual(f"soundscape_{profile}", preset["name"])
            data = preset["slots"]["99"]["data"]
            self.assertEqual(
                90, len(data),
                "Factory Reset must cover every host macro and nested BEAP client",
            )
            self.assertEqual([1.0], data["soundscape_pitch_follow_state"])
            for complete_key, complete_value in {
                "cinematic_soundscape_beap~::Osc_A::FreqMode": [1],
                "cinematic_soundscape_beap~::Osc_A::Freq": [0.6],
                "cinematic_soundscape_beap~::Osc_A::PW": [50],
                "cinematic_soundscape_beap~::Ladder::CV2": [0.0],
                "cinematic_soundscape_beap~::Ladder::power[1]": [0.0],
                "cinematic_soundscape_beap~::Mixer::Mute": [0.0],
                "cinematic_soundscape_beap~::Noise::manCVa": [0.0],
                "cinematic_soundscape_beap~::VCA::Response": [0.0],
            }.items():
                self.assertEqual(complete_value, data[complete_key])
            for key, value in values.items():
                storage_key = (
                    key if key.startswith("soundscape_")
                    else f"cinematic_soundscape_beap~::{key}"
                )
                self.assertEqual([value], data[storage_key])

    def test_soundscape_factory_loads_before_profile_local_override(self):
        state_helper = (
            ROOT / "code" / "soundscape_state_path.js"
        ).read_text(encoding="utf-8")
        self.assertIn("function factoryPath()", state_helper)
        self.assertIn('"/presets/" + profile + "_soundscape_factory.json"', state_helper)
        self.assertIn("function factory()", state_helper)
        for profile in ("ev", "v10", "v12"):
            host = self.load_json(
                f"patchers/{profile}_cinematic_soundscape_host~.maxpat"
            )["patcher"]
            boxes = {item["box"]["id"]: item["box"] for item in host["boxes"]}
            texts = [box.get("text") for box in boxes.values()]
            self.assertIn("factory", texts)
            self.assertIn("99", texts)
            self.assertIn("restore", texts)
            self.assertIn("1", texts)
            self.assertNotIn("store 99", texts)
            self.assertIn("delay 1200", texts)
            self.assertGreaterEqual(texts.count("delay 800"), 2)
            self.assertGreaterEqual(texts.count("delay 120"), 2)
            self.assertGreaterEqual(texts.count("prime"), 2)
            self.assertFalse(any(
                text.startswith(f"pattrstorage soundscape_{profile}_factory ")
                for text in texts if text
            ))
            edges = {
                (tuple(line["patchline"]["source"]), tuple(line["patchline"]["destination"]))
                for line in host["lines"]
            }
            reset_ids = {
                box_id for box_id, box in boxes.items() if box.get("text") == "reset"
            }
            reset_delay_ids = {
                destination[0] for source, destination in edges
                if source[0] in reset_ids
                and boxes[destination[0]].get("text") == "delay 800"
            }
            self.assertTrue(reset_delay_ids)
            reset_recall_ids = {
                destination[0] for source, destination in edges
                if source[0] in reset_delay_ids
                and boxes[destination[0]].get("text") == "99"
            }
            storage_id = next(
                box_id for box_id, box in boxes.items()
                if box.get("text", "").startswith(f"pattrstorage soundscape_{profile} ")
            )
            self.assertTrue(any(
                source[0] in reset_recall_ids and destination == (storage_id, 0)
                for source, destination in edges
            ), "Factory Reset must recall tracked slot 99 after its read completes")

    def test_soundscape_hosts_use_profile_specific_tone_maps_and_defaults(self):
        expected = {
            "ev": ("min(1.35", "0.22+0.72*$f1", ("0.28", "0.46", "0.68")),
            "v10": ("min(0.85", "0.12+0.36*$f1", ("0.1", "0.32", "0.38")),
            "v12": ("min(1.", "0.16+0.48*$f1", ("0.16", "0.46", "0.5")),
        }
        for profile, (ceiling, throttle, defaults) in expected.items():
            host = self.load_json(
                f"patchers/{profile}_cinematic_soundscape_host~.maxpat"
            )["patcher"]
            text = "\n".join(
                item["box"].get("text", "") for item in host["boxes"]
            )
            self.assertIn(ceiling, text)
            self.assertIn(throttle, text)
            for value in defaults:
                self.assertIn(f"loadmess {value}", text)

    def test_soundscape_factory_uses_smooth_modulation_and_one_soft_safety_stage(self):
        core = self.load_json("patchers/cinematic_soundscape_beap~.maxpat")["patcher"]
        boxes = {item["box"]["id"]: item["box"] for item in core["boxes"]}
        modules = {
            box.get("varname"): box for box in boxes.values()
            if box.get("varname")
        }

        def restore_for(box):
            matches = []

            def visit(value):
                if isinstance(value, dict):
                    if isinstance(value.get("restore"), dict):
                        matches.append(value["restore"])
                    for child in value.values():
                        visit(child)
                elif isinstance(value, list):
                    for child in value:
                        visit(child)

            visit(box)
            self.assertEqual(1, len(matches))
            return {key: values[0] for key, values in matches[0].items()}

        self.assertEqual(0.035, restore_for(modules["LFO"])["Frequency"])
        self.assertEqual(0.009, restore_for(modules["LFO_Slow"])["Frequency"])
        self.assertEqual(
            {"in1": -5, "in2": -12, "in3": -36, "in4": -26},
            {key: restore_for(modules["Mixer"])[key] for key in ("in1", "in2", "in3", "in4")},
        )
        self.assertEqual(1400, restore_for(modules["Ladder"])["Freq"])
        self.assertLessEqual(restore_for(modules["Ladder"])["Res"], 3)
        self.assertEqual(4500, restore_for(modules["MMF"])["Freq"])
        chorus = restore_for(modules["Chorus"])
        self.assertLessEqual(chorus["Rate"], 0.015)
        self.assertLessEqual(chorus["Regen"], 0.02)
        self.assertLessEqual(chorus["Width"], 10)

        lfo_ids = {modules["LFO"]["id"], modules["LFO_Slow"]["id"]}
        oscillator_ids = {modules["Osc_A"]["id"], modules["Osc_B"]["id"], modules["Osc_C"]["id"]}
        for item in core["lines"]:
            line = item["patchline"]
            source_id, source_outlet = line["source"]
            destination_id, destination_inlet = line["destination"]
            if source_id in lfo_ids:
                self.assertIn(source_outlet, (0, 3), "only sine/triangle LFO shapes are continuous")
                self.assertFalse(
                    destination_id in oscillator_ids and destination_inlet == 4,
                    "factory LFO must not drive oscillator PWM directly",
                )

        core_text = "\n".join(box.get("text", "") for box in boxes.values())
        self.assertNotIn("clip~ -0.8 0.8", core_text)
        self.assertEqual(2, core_text.count("tanh~"))
        self.assertNotIn("expr~", core_text)
        for profile in ("ev", "v10", "v12"):
            host_text = json.dumps(
                self.load_json(f"patchers/{profile}_cinematic_soundscape_host~.maxpat")
            )
            self.assertNotIn("clip~ -0.65 0.65", host_text)
            self.assertIn("0.92 35, 1. 300 35", host_text)

    def test_v5_continuous_models_add_load_and_idle_acoustic_identity_without_sawtooth(self):
        expected = {
            "ev": ("torque_ripple", "gear_mesh", "electrical_motion"),
            "v10": ("idle_weight", "crankcase_body", "manifold"),
            "v12": ("idle_weight", "crankcase_body", "manifold"),
        }
        for profile, tokens in expected.items():
            patcher = self.load_json(f"gen/{profile}_powertrain.gendsp")["patcher"]
            code = "\n".join(
                item["box"].get("code", "")
                for item in patcher["boxes"]
                if item["box"].get("maxclass") == "codebox"
            ).lower()
            for token in tokens:
                self.assertIn(token, code)
            if profile == "ev":
                right_side = code.split("side_r =", 1)[1].split(";", 1)[0]
                for token in ("h3_r", "gear_r", "inverter_r", "air_r"):
                    self.assertIn(token, right_side)
            for forbidden in ("saw", "square", "rect~"):
                self.assertNotIn(forbidden, code)

    def test_ice_continuous_powertrains_are_procedural_not_loop_players(self):
        """Idle/accel/decel must remain synthesized; samples are transient-only."""
        for profile in ("v10", "v12"):
            patcher = self.load_json(
                f"patchers/{profile}_powertrain~.maxpat"
            )["patcher"]
            text = "\n".join(
                item["box"].get("text", "") + " " + item["box"].get("name", "")
                for item in patcher["boxes"]
            )
            self.assertIn(
                f"gen~ @gen Patcher:/gen/{profile}_powertrain.gendsp",
                text,
            )
            for forbidden in (
                "groove~",
                "buffer~",
                "state_renderer~",
                "texture_renderer~",
                "engine_texture_",
                "ferrari_v10_",
            ):
                self.assertNotIn(forbidden, text.lower(), (profile, forbidden))

        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        declared = {
            path for category in project["contents"].values() for path in category
        }
        self.assertNotIn("patchers/v10_state_renderer~.maxpat", declared)
        self.assertNotIn("patchers/v10_fallback_renderer~.maxpat", declared)
        self.assertNotIn("patchers/v12_texture_renderer~.maxpat", declared)

    def test_ev_drive_model_has_no_direct_throttle_rpm_jump(self):
        result = self.run_drive_trace("ev", seconds=8.0)
        self.assertEqual(
            result["beforeThrottle"]["rpm"],
            result["afterThrottleBeforeTick"]["rpm"],
        )
        rpms = [item["rpm"] for item in result["trace"]]
        self.assertGreater(rpms[-1], rpms[100] + 1000.0)
        self.assertTrue(
            all(later + 1e-6 >= earlier for earlier, later in zip(rpms, rpms[1:])),
            "EV RPM must follow wheel speed continuously without threshold reversals",
        )
        self.assertLess(
            max(later - earlier for earlier, later in zip(rpms, rpms[1:])),
            100.0,
        )

    def test_profile_drive_patchers_use_one_control_clock(self):
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        self.assertIn("code/drive_model.js", project["contents"]["code"])
        for profile in ("ev", "v10", "v12"):
            patcher = self.load_json(
                f"patchers/drive_simulator_{profile}.maxpat"
            )["patcher"]
            text = "\n".join(
                item["box"].get("text", "") + " " + item["box"].get("name", "")
                for item in patcher["boxes"]
            )
            self.assertIn(
                f"js Patcher:/code/drive_model.js {profile}",
                text,
            )
            self.assertIn("qmetro 20", text)
            for forbidden in ("pak ", "*1400", "*520", "speedlim 350"):
                self.assertNotIn(forbidden, text)

    def test_drive_start_resets_auto_clock_after_arbitrary_patcher_wait(self):
        script = r"""
const {DriveModel} = require(process.argv[1]);
function snapshotAfter(preTicks) {
  const model = new DriveModel("v10");
  for (let index = 0; index < preTicks; index += 1) model.tick(0.02);
  model.handle("ignition", [1]);
  model.handle("start", [1]);
  model.handle("auto", [1]);
  for (let index = 0; index < 51; index += 1) model.tick(0.02);
  return model.snapshot();
}
process.stdout.write(JSON.stringify({immediate: snapshotAfter(0), delayed: snapshotAfter(300)}));
"""
        result = subprocess.run(
            ["node", "-e", script, str(ROOT / "code" / "drive_model.js")],
            check=True,
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        states = json.loads(result.stdout)
        self.assertAlmostEqual(states["immediate"]["rpm"], states["delayed"]["rpm"], places=9)
        self.assertAlmostEqual(
            states["immediate"]["throttle"], states["delayed"]["throttle"], places=9
        )
        self.assertLess(states["delayed"]["rpm"], 1100.0)

    def test_ice_drive_model_uses_ordered_smoothed_dct_shifts(self):
        for profile in ("v10", "v12"):
            result = self.run_drive_trace(profile, seconds=32.0)
            trace = result["trace"]
            changes = [
                later["gear"]
                for earlier, later in zip(trace, trace[1:])
                if later["gear"] != earlier["gear"]
            ]
            self.assertEqual([2, 3, 4, 5, 6, 7], changes, profile)
            self.assertTrue(
                all(
                    abs(later["rpm"] - earlier["rpm"]) < 400.0
                    for earlier, later in zip(trace[40:], trace[41:])
                ),
                f"{profile} must sweep RPM across a shift instead of resetting it",
            )
            shift_runs = []
            current = 0
            for item in trace:
                if item["shifting"]:
                    current += 1
                elif current:
                    shift_runs.append(current)
                    current = 0
            minimum_ticks = 9 if profile == "v10" else 12
            self.assertTrue(all(run >= minimum_ticks for run in shift_runs), shift_runs)

    def test_ev_beap_and_motor_share_one_continuous_pitch_law(self):
        host = self.load_json("patchers/ev_soundscape_host~.maxpat")["patcher"]
        text = "\n".join(
            item["box"].get("text", "") for item in host["boxes"]
        )
        self.assertIn("55.+$f1*.052", text)
        self.assertNotIn("80.+$f1*.02", text)
        self.assertNotIn("min(280.", text)
        self.assertIn("0.9+2.8*$f1+0.7*min(1.,$f2/10000.)", text)

    def test_ice_synthesis_reacts_to_lifecycle_state_without_audio_loops(self):
        for profile in ("v10", "v12"):
            powertrain = self.load_json(
                f"patchers/{profile}_powertrain~.maxpat"
            )["patcher"]
            patch_text = "\n".join(
                item["box"].get("text", "") for item in powertrain["boxes"]
            )
            self.assertIn("route rpm throttle load accel", patch_text)
            self.assertIn("accel $1", patch_text)

            gen = self.load_json(f"gen/{profile}_powertrain.gendsp")["patcher"]
            code = next(
                item["box"]["code"]
                for item in gen["boxes"]
                if item["box"].get("maxclass") == "codebox"
            )
            self.assertIn("Param accel(0, min=-1, max=1);", code)
            self.assertIn("accel_drive", code)
            self.assertIn("decel_drive", code)

        v10 = self.load_json("gen/v10_powertrain.gendsp")["patcher"]
        v10_code = next(
            item["box"]["code"]
            for item in v10["boxes"]
            if item["box"].get("maxclass") == "codebox"
        )
        self.assertIn("Param rpm(740", v10_code)
        self.assertIn("(r - 740) / 7560", v10_code)

    def test_ferrari_reference_is_an_analysis_only_lifecycle_target(self):
        target = self.load_json("assets/ferrari_v10_lifecycle_targets.json")
        self.assertEqual(1, target["schema_version"])
        self.assertEqual("analysis-only", target["runtime_usage"])
        self.assertRegex(target["source_sha256"], r"^[0-9a-f]{64}$")
        nodes = target["nodes"]
        self.assertGreaterEqual(len(nodes), 12)
        required_roles = {
            "startup_catch",
            "idle",
            "acceleration",
            "loaded_hold",
            "shift_recovery",
            "deceleration",
        }
        self.assertTrue(required_roles.issubset({node["role"] for node in nodes}))
        for node in nodes:
            self.assertGreater(node["end_seconds"], node["start_seconds"])
            self.assertGreater(node["dominant_firing_hz"], 0.0)
            self.assertGreaterEqual(node["low_mid_ratio_40_500"], 0.0)
            self.assertLessEqual(node["low_mid_ratio_40_500"], 1.0)
            self.assertGreaterEqual(node["harsh_ratio_2000_6000"], 0.0)
            self.assertLessEqual(node["harsh_ratio_2000_6000"], 1.0)
            self.assertGreater(node["spectral_rolloff_95_hz"], 0.0)

        project_text = json.dumps(self.load_json("VehicleSoundSynth-V5.maxproj"))
        self.assertIn("assets/ferrari_v10_lifecycle_targets.json", project_text)
        self.assertNotIn("media/local/ferrari_v10_", project_text)

    def test_v10_lifecycle_render_gate_uses_reference_envelope_and_rejects_plastic_highs(self):
        targets = self.load_json("assets/ferrari_v10_lifecycle_targets.json")
        with tempfile.TemporaryDirectory() as directory:
            low_path = Path(directory) / "v10_idle_low.wav"
            harsh_path = Path(directory) / "v10_idle_harsh.wav"
            for path, frequency in ((low_path, 80.0), (harsh_path, 4000.0)):
                with wave.open(str(path), "wb") as handle:
                    handle.setnchannels(2)
                    handle.setsampwidth(2)
                    handle.setframerate(48000)
                    payload = []
                    for index in range(48000):
                        value = round(7000 * math.sin(2.0 * math.pi * frequency * index / 48000))
                        payload.append(struct.pack("<hh", value, value))
                    handle.writeframes(b"".join(payload))

            good = validate_render(low_path, targets, "idle")
            bad = validate_render(harsh_path, targets, "idle")
            self.assertTrue(good["passed"], good)
            self.assertFalse(bad["passed"], bad)
            self.assertTrue(
                any(failure.startswith("harsh_ratio:") for failure in bad["failures"]),
                bad,
            )

            cadence_path = low_path.with_suffix(".lifecycle.json")
            cadence_path.write_text(json.dumps({
                "schema_version": 1,
                "role": "idle",
                "render_ms": 4000,
                "start_rpm": 740.0,
                "end_rpm": 740.0,
                "start_firing_hz": 740.0 / 12.0,
                "end_firing_hz": 740.0 / 12.0,
                "cadence_derivative_hz_s": 0.0,
                "event": None,
            }), encoding="utf-8")
            scheduled = validate_render(
                low_path, targets, "idle", require_cadence_schedule=True
            )
            self.assertTrue(scheduled["passed"], scheduled)

    def test_v10_lifecycle_probe_matrix_covers_all_continuous_roles_and_cadence(self):
        source = (ROOT / "tools" / "build_runtime_probe.py").read_text(encoding="utf-8")
        for role in ("idle", "acceleration", "loaded-hold", "shift-recovery", "deceleration"):
            self.assertIn(f'"v10-lifecycle-{role}"', source)
        for token in (
            '"start_firing_hz"', '"end_firing_hz"',
            '"cadence_derivative_hz_s"', '"lifecycle_role"',
        ):
            self.assertIn(token, source)

        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "build_runtime_probe.py"),
                    "--bundle-root", directory,
                    "--scenario", "v10-lifecycle-drive",
                    "--driver", "coreaudio",
                    "--render-ms", "24000",
                ],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            bundle = Path(directory)
            patch = json.loads(next(bundle.glob("runtime_probe*.maxpat")).read_text(encoding="utf-8"))
            text = "\n".join(
                item["box"].get("text", "") for item in patch["patcher"]["boxes"]
            )
            self.assertIn("auto 1", text)
            self.assertIn("ignition 1, start 1, auto 1", text)
            for bypass in ("loadmess rpm", "loadmess throttle", "line 0.", "shift_dir"):
                self.assertNotIn(bypass, text)
            trace = json.loads(next(bundle.glob("*.drive.json")).read_text(encoding="utf-8"))
            report = validate_drive_trace(trace)
            self.assertTrue(report["passed"], report)
            self.assertEqual([2, 3, 4, 5, 6, 7], report["gears"][:6])

    def test_master_has_adjustable_stereo_compressor_before_peak_limiter(self):
        master = self.load_json("patchers/mix_master~.maxpat")["patcher"]
        text = "\n".join(item["box"].get("text", "") for item in master["boxes"])
        for name in (
            "compressor_threshold_db",
            "compressor_ratio",
            "compressor_attack_rate",
            "compressor_release_rate",
            "compressor_makeup_db",
            "compressor_bypass",
        ):
            self.assertIn(name, text)
        self.assertIn("omx.comp~", text)
        self.assertIn("prepend agcThreshold", text)
        self.assertIn("prepend ratio", text)
        self.assertIn("prepend attack", text)
        self.assertIn("prepend release", text)
        self.assertIn("prepend bypass", text)
        for setting in (
            "channelCoupling 0",
            "dualBandEnabled 0",
            "limEnabled 0",
            "ngEnabled 0",
            "range 0",
        ):
            self.assertIn(setting, text)

        boxes = {item["box"]["id"]: item["box"].get("text", "") for item in master["boxes"]}
        lines = master["lines"]
        comp_id = next(identifier for identifier, value in boxes.items() if value == "omx.comp~")
        limiter_id = next(identifier for identifier, value in boxes.items() if value == "omx.peaklim~")
        makeup_ids = {
            line["patchline"]["destination"][0]
            for line in lines
            if line["patchline"]["source"][0] == comp_id
            and boxes[line["patchline"]["destination"][0]] == "*~"
        }
        self.assertEqual(2, len(makeup_ids))
        self.assertTrue(
            all(
                any(
                    line["patchline"]["source"][0] == makeup_id
                    and line["patchline"]["destination"][0] == limiter_id
                    for line in lines
                )
                for makeup_id in makeup_ids
            ),
            "compressor makeup stages must feed the final safety limiter",
        )

    def test_v4_has_three_independent_runtime_patchers_and_a_dsp_free_launcher(self):
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        declared = {
            path for category in project["contents"].values() for path in category
        }
        runtime_names = (
            "VehicleSoundSynth-EV.maxpat",
            "VehicleSoundSynth-V10.maxpat",
            "VehicleSoundSynth-V12.maxpat",
        )
        for name in runtime_names:
            self.assertIn(name, declared)
            patcher = self.load_json(name)["patcher"]
            text = "\n".join(
                item["box"].get("text", "") + " " + item["box"].get("name", "")
                for item in patcher["boxes"]
            )
            self.assertNotIn("engine_type", text)
            profile = name.removeprefix("VehicleSoundSynth-").removesuffix(".maxpat").lower()
            self.assertIn(f"drive_simulator_{profile}", text)
            self.assertIn(f"vehicle_engine_{profile}~", text)
            self.assertIn("manual_input", text)
            self.assertIn(f"patchers/drive_simulator_{profile}", text)
            self.assertIn(f"patchers/vehicle_engine_{profile}~", text)
            self.assertIn("patchers/manual_input", text)

        launcher = self.load_json("main.maxpat")["patcher"]
        launcher_text = "\n".join(
            item["box"].get("text", "") for item in launcher["boxes"]
        )
        for forbidden in ("dac~", "ezdac~", "gen~", "vehicle_engine~", "powertrain~"):
            self.assertNotIn(forbidden, launcher_text)
        for name in runtime_names:
            self.assertIn(f"loadunique {name}", launcher_text)
        self.assertIn("s vss.runtime.select", launcher_text)
        for profile in ("ev", "v10", "v12"):
            runtime_text = "\n".join(
                item["box"].get("text", "")
                for item in self.load_json(
                    f"VehicleSoundSynth-{profile.upper()}.maxpat"
                )["patcher"]["boxes"]
            )
            self.assertIn("r vss.runtime.select", runtime_text)
            self.assertIn(f"sel {profile}", runtime_text)
            self.assertIn("save_profile_sound", runtime_text)
            self.assertNotIn("write", runtime_text)
            self.assertIn("wclose", runtime_text)
            self.assertIn("thispatcher", runtime_text)

    def test_each_runtime_uses_only_its_own_powertrain_graph(self):
        expected = {
            profile: f"gen~ @gen Patcher:/gen/{profile}_powertrain.gendsp"
            for profile in ("ev", "v10", "v12")
        }
        for profile, own_gen in expected.items():
            patcher = self.load_json(
                f"patchers/{profile}_powertrain~.maxpat"
            )["patcher"]
            text = "\n".join(
                item["box"].get("text", "") for item in patcher["boxes"]
            )
            self.assertEqual(1, text.count("gen~ @gen"))
            self.assertIn(own_gen, text)
            self.assertNotIn("ev_weight", text)
            self.assertNotIn("v10_weight", text)
            self.assertNotIn("v12_weight", text)

    def test_nested_runtime_assets_resolve_from_the_generated_root(self):
        for profile in ("ev", "v10", "v12"):
            text = "\n".join(
                item["box"].get("text", "")
                for item in self.load_json(
                    f"patchers/{profile}_powertrain~.maxpat"
                )["patcher"]["boxes"]
            )
            self.assertIn(
                f"gen~ @gen Patcher:/gen/{profile}_powertrain.gendsp",
                text,
            )

        for relative in (
            "patchers/reference_texture~.maxpat",
            "patchers/cabin_master~.maxpat",
        ):
            text = "\n".join(
                item["box"].get("text", "")
                for item in self.load_json(relative)["patcher"]["boxes"]
            )
            self.assertIn("Patcher:/media/", text, relative)

    def test_profile_runtimes_have_fixed_controllers_and_startup_rpm_flares(self):
        expected = {
            "ev": (650, 650),
            "v10": (1050, 740),
            "v12": (1100, 780),
        }
        for profile, (flare, idle) in expected.items():
            for relative in (
                f"patchers/vehicle_engine_{profile}~.maxpat",
                f"patchers/engine_controller_{profile}.maxpat",
                f"patchers/drive_simulator_{profile}.maxpat",
            ):
                self.assertTrue((ROOT / relative).is_file(), relative)
                text = "\n".join(
                    item["box"].get("text", "")
                    for item in self.load_json(relative)["patcher"]["boxes"]
                )
                self.assertNotIn("engine_type", text)
            drive_text = "\n".join(
                item["box"].get("text", "")
                for item in self.load_json(
                    f"patchers/drive_simulator_{profile}.maxpat"
                )["patcher"]["boxes"]
            )
            self.assertIn(
                f"js Patcher:/code/drive_model.js {profile}",
                drive_text,
            )
            self.assertIn("qmetro 20", drive_text)
            code = (ROOT / "code" / "drive_model.js").read_text(encoding="utf-8")
            self.assertIn(f"idle: {idle:.1f}", code)
            self.assertIn(f"flare: {flare:.1f}", code)

    def test_profile_drive_throttle_runs_hot_and_ice_shifts_are_smoothed(self):
        for profile in ("ev", "v10", "v12"):
            drive = self.load_json(
                f"patchers/drive_simulator_{profile}.maxpat"
            )["patcher"]
            text = "\n".join(item["box"].get("text", "") for item in drive["boxes"])
            self.assertIn(
                f"js Patcher:/code/drive_model.js {profile}",
                text,
            )
            self.assertIn("qmetro 20", text)
            if profile == "ev":
                trace = self.run_drive_trace(profile, seconds=8.0)["trace"]
                self.assertTrue(all(item["gear"] == 1 for item in trace))
            else:
                trace = self.run_drive_trace(profile, seconds=32.0)["trace"]
                self.assertGreater(max(item["gear"] for item in trace), 1)
                self.assertLess(min(item["shiftCut"] for item in trace), 1.0)

        for profile in ("v10", "v12"):
            controller_text = "\n".join(
                item["box"].get("text", "")
                for item in self.load_json(
                    f"patchers/engine_controller_{profile}.maxpat"
                )["patcher"]["boxes"]
            )
            self.assertNotIn("shift_cut 0.72", controller_text)
            self.assertNotIn("shift_cut 0.22", controller_text)

        for profile in ("v10", "v12"):
            transient_text = "\n".join(
                item["box"].get("text", "")
                for item in self.load_json(
                    f"patchers/transient_{profile}~.maxpat"
                )["patcher"]["boxes"]
            )
            self.assertIn(f"{profile}_backfire_host~", transient_text)
            self.assertNotIn("play~ shift_", transient_text)

    def test_legacy_ev_modes_are_preserved_while_shared_soundscape_owns_runtime_dsp(self):
        expected = (
            "patchers/ev_pad_beap~.maxpat",
            "patchers/ev_expressive_beap~.maxpat",
            "patchers/ev_sport_beap~.maxpat",
        )
        for relative in expected:
            patcher = self.load_json(relative)["patcher"]
            text = "\n".join(
                item["box"].get("text", "") for item in patcher["boxes"]
            )
            self.assertIn("USER-TUNABLE", text)
            self.assertGreaterEqual(
                sum(item["box"]["maxclass"] == "bpatcher" for item in patcher["boxes"]),
                10,
            )
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        declared = set(project["contents"]["patchers"])
        self.assertNotIn("patchers/ev_soundscape_host~.maxpat", declared)
        host = self.load_json("patchers/ev_cinematic_soundscape_host~.maxpat")["patcher"]
        host_text = "\n".join(item["box"].get("text", "") for item in host["boxes"])
        self.assertIn("cinematic_soundscape_beap~ ev", host_text)
        self.assertIn("delay 5200", host_text)
        self.assertIn("delay 5600", host_text)
        self.assertIn("0. 300", host_text)
        self.assertIn("line~ 1.", host_text)
        self.assertIn("mute~", host_text)
        engine = self.load_json("patchers/vehicle_engine_ev~.maxpat")["patcher"]
        engine_text = "\n".join(item["box"].get("text", "") for item in engine["boxes"])
        self.assertIn("route soundscape_solo pad_solo backfire_solo dna_solo", engine_text)
        self.assertIn("expr (1-$i3)*(1-max($i1,$i2))", engine_text)

    def test_soundscape_solo_isolates_every_non_soundscape_stem(self):
        for profile in ("ev", "v10", "v12"):
            patcher = self.load_json(
                f"patchers/vehicle_engine_{profile}~.maxpat"
            )["patcher"]
            text_by_id = {
                item["box"]["id"]: item["box"].get("text", "")
                for item in patcher["boxes"]
            }
            edges = [item["patchline"] for item in patcher["lines"]]
            def line_after(expression):
                expression_id = next(
                    box_id for box_id, text in text_by_id.items() if text == expression
                )
                pack_id = next(
                    edge["destination"][0] for edge in edges
                    if edge["source"][0] == expression_id
                    and text_by_id[edge["destination"][0]] == "pack 0. 35"
                )
                return next(
                    edge["destination"][0] for edge in edges
                    if edge["source"][0] == pack_id
                    and text_by_id[edge["destination"][0]] == "line~"
                )

            core_line = line_after("expr $i3+(1-$i3)*(1-max($i1,$i2))")
            aux_line = line_after("expr (1-$i3)*(1-max($i1,$i2))")
            transient_line = line_after("expr (1-$i3)*(1-$i1*(1-$i2))")
            pad_line = line_after("expr (1-$i3)*(1-$i2)")
            core_gains = {
                edge["destination"][0]
                for edge in edges
                if edge["source"][0] == core_line
                and edge["destination"][1] == 1
                and text_by_id[edge["destination"][0]] == "*~"
            }
            aux_gains = {
                edge["destination"][0]
                for edge in edges
                if edge["source"][0] == aux_line
                and edge["destination"][1] == 1
                and text_by_id[edge["destination"][0]] == "*~"
            }
            transient_gains = {
                edge["destination"][0]
                for edge in edges
                if edge["source"][0] == transient_line
                and edge["destination"][1] == 1
                and text_by_id[edge["destination"][0]] == "*~"
            }
            pad_gains = {
                edge["destination"][0]
                for edge in edges
                if edge["source"][0] == pad_line
                and edge["destination"][1] == 1
                and text_by_id[edge["destination"][0]] == "*~"
            }
            self.assertEqual(2, len(core_gains), profile)
            self.assertEqual(4, len(aux_gains), profile)
            self.assertEqual(2, len(transient_gains), profile)
            self.assertEqual(2, len(pad_gains), profile)
            sources = (
                f"{profile}_sound_dna~",
                f"transient_{profile}~",
                "road_air~",
                "cabin_rumble~",
            )
            source_ids = {
                text: next(box_id for box_id, value in text_by_id.items() if value == text)
                for text in sources
            }
            for source_text, source_id in source_ids.items():
                if source_text.startswith("transient_"):
                    expected_gains = transient_gains
                elif source_text.endswith("_sound_dna~"):
                    expected_gains = core_gains
                else:
                    expected_gains = aux_gains
                for channel in (0, 1):
                    self.assertTrue(
                        any(
                            edge["source"] == [source_id, channel]
                            and edge["destination"][0] in expected_gains
                            and edge["destination"][1] == 0
                            for edge in edges
                        ),
                        f"{profile} solo does not gate {source_text} channel {channel}",
                    )
            rumble_id = source_ids["cabin_rumble~"]
            power_id = source_ids[f"{profile}_sound_dna~"]
            self.assertFalse(
                any(
                    edge["source"][0] == power_id
                    and edge["destination"][0] == rumble_id
                    and edge["destination"][1] in (1, 2)
                    for edge in edges
                ),
                f"{profile} solo bypasses the gate through rumble excitation",
            )


    def test_ice_start_defaults_to_cinematic_beap_with_realistic_sample_option(self):
        start_beap = self.load_json("patchers/engine_start_beap~.maxpat")["patcher"]
        start_text = "\n".join(
            item["box"].get("text", "") + " " + item["box"].get("varname", "")
            for item in start_beap["boxes"]
        )
        self.assertIn("USER-TUNABLE", start_text)
        for token in (
            "L_Mixer", "L_Ladder", "L_ADSR", "L_VCA",
            "R_Mixer", "R_Ladder", "R_ADSR", "R_VCA",
        ):
            self.assertIn(token, start_text)
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        self.assertIn("patchers/engine_start_core~.maxpat", project["contents"]["patchers"])
        for profile in ("v10", "v12"):
            transient = self.load_json(f"patchers/transient_{profile}~.maxpat")["patcher"]
            text = "\n".join(
                item["box"].get("text", "") + " " + item["box"].get("varname", "")
                for item in transient["boxes"]
            )
            self.assertIn("route starter start_style", text)
            self.assertIn("sel cinematic realistic", text)
            self.assertIn("loadmess cinematic", text)
            self.assertIn("poly~ engine_start_voice 1", text)
            self.assertIn("engine_start_core~", text)
            self.assertIn("start_cinematic_gain", text)
            self.assertIn("starter_state_gate", text)
            self.assertIn("rampsmooth~ 64 256", text)
            self.assertIn("mute 1 0", text)
            self.assertIn("mute 1 1", text)
            self.assertIn("t b b", text)
            self.assertIn("delay 5", text)
            self.assertIn("delay 1600", text)
            self.assertIn("*~ 0.55", text)
            self.assertIn("*~ 0.75", text)
            if profile == "v10":
                self.assertIn("*~ 0.65", text)
            self.assertIn("starter_", text)
        start_core = self.load_json("patchers/engine_start_core~.maxpat")["patcher"]
        start_core_text = "\n".join(
            item["box"].get("text", "") + " " + item["box"].get("varname", "")
            for item in start_core["boxes"]
        )
        self.assertEqual(
            3,
            sum(item["box"].get("maxclass") == "inlet" for item in start_core["boxes"]),
        )
        for token in ("phasor~", "tanh~", "svf~ 28 0.7"):
            self.assertIn(token, start_core_text)
        ev_text = "\n".join(
            item["box"].get("text", "")
            for item in self.load_json("patchers/transient_ev~.maxpat")["patcher"]["boxes"]
        )
        self.assertIn("poly~ engine_start_voice 1", ev_text)
        self.assertNotIn("play~ starter_", ev_text)

    def test_backfire_test_is_audition_only_while_physical_events_remain_gated(self):
        for profile in ("v10", "v12"):
            host = self.load_json(f"patchers/{profile}_backfire_host~.maxpat")["patcher"]
            boxes = {item["box"]["id"]: item["box"] for item in host["boxes"]}
            text = "\n".join(box.get("text", "") for box in boxes.values())
            self.assertIn("backfire_test", text)
            self.assertIn("AUDITION ONLY", text)
            test_edge = next(
                box_id for box_id, box in boxes.items()
                if box.get("varname") == "backfire_test_edge"
            )
            scheduler = next(
                box_id for box_id, box in boxes.items()
                if box.get("varname") == "overrun_test_burst_scheduler"
            )
            trigger_destinations = {
                line["patchline"]["destination"][0]
                for line in host["lines"]
                if line["patchline"]["source"][0] == test_edge
            }
            test_message = next(
                destination for destination in trigger_destinations
                if boxes[destination].get("text") == "burst 1."
            )
            test_message_destinations = {
                line["patchline"]["destination"][0]
                for line in host["lines"]
                if line["patchline"]["source"][0] == test_message
            }
            self.assertIn(scheduler, test_message_destinations)
            physical_burst_gates = [
                box_id for box_id, box in boxes.items()
                if box.get("text") == "gate 1" and scheduler in {
                    line["patchline"]["destination"][0]
                    for line in host["lines"]
                    if line["patchline"]["source"][0] == box_id
                }
            ]
            self.assertEqual(1, len(physical_burst_gates))
            runtime = self.load_json(f"VehicleSoundSynth-{profile.upper()}.maxpat")["patcher"]
            runtime_text = "\n".join(
                item["box"].get("text", "") for item in runtime["boxes"]
            )
            self.assertIn("backfire_test 1", runtime_text)

    def test_overrun_and_test_pop_use_burst_scheduler_while_shift_stays_single(self):
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        self.assertIn(
            "patchers/backfire_burst_scheduler.maxpat",
            project["contents"]["patchers"],
        )
        self.assertIn("code/backfire_burst.js", project["contents"]["code"])
        scheduler = self.load_json("patchers/backfire_burst_scheduler.maxpat")["patcher"]
        scheduler_text = "\n".join(
            item["box"].get("text", "") for item in scheduler["boxes"]
        )
        self.assertIn("js Patcher:/code/backfire_burst.js", scheduler_text)
        self.assertIn("pitch_semitones gain index count", scheduler_text)

        for profile in ("v10", "v12"):
            host = self.load_json(f"patchers/{profile}_backfire_host~.maxpat")["patcher"]
            boxes = {item["box"]["id"]: item["box"] for item in host["boxes"]}
            scheduler_id = next(
                box_id for box_id, box in boxes.items()
                if box.get("varname") == "overrun_test_burst_scheduler"
            )
            single_id = next(
                box_id for box_id, box in boxes.items()
                if box.get("varname") == "backfire_single_event_trigger"
            )
            test_edge = next(
                box_id for box_id, box in boxes.items()
                if box.get("varname") == "backfire_test_edge"
            )
            destinations = lambda source: {
                line["patchline"]["destination"][0]
                for line in host["lines"]
                if line["patchline"]["source"][0] == source
            }
            self.assertNotIn(single_id, destinations(test_edge))
            self.assertTrue(any(
                boxes[destination].get("text") == "burst 1."
                for destination in destinations(test_edge)
            ))
            self.assertIn("backfire_burst_scheduler", boxes[scheduler_id].get("text", ""))
            host_text = "\n".join(box.get("text", "") for box in boxes.values())
            self.assertIn("SHIFT / EXPLICIT EVENTS — one hit", host_text)
            self.assertIn("OVERRUN / TEST POP — 1..5 hit burst", host_text)
            self.assertIn("backfire_seed", host_text)
            self.assertIn("prepend seed", host_text)

    def test_local_reference_processor_builds_deterministic_v10_state_atlas(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "reference.wav"
            outputs = (base / "first", base / "second")
            frames = 8 * 48000
            with wave.open(str(source), "wb") as handle:
                handle.setnchannels(2)
                handle.setsampwidth(2)
                handle.setframerate(48000)
                payload = bytearray()
                phase = 0.0
                for index in range(frames):
                    progress = index / max(1, frames - 1)
                    cadence = 62.0 + 400.0 * abs(math.sin(progress * math.pi * 2.0))
                    phase += 2.0 * math.pi * cadence / 48000.0
                    amplitude = 0.18 + 0.10 * progress
                    left = int(32767 * amplitude * math.sin(phase))
                    right = int(32767 * amplitude * math.sin(phase + 0.03))
                    payload.extend(struct.pack("<hh", left, right))
                handle.writeframes(bytes(payload))
            hashes = []
            for output in outputs:
                report = prepare_v10_atlas(source, output)
                atlas_path = output / "ferrari_v10_atlas.json"
                self.assertTrue(atlas_path.is_file())
                atlas = json.loads(atlas_path.read_text(encoding="utf-8"))
                self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), atlas["source_sha256"])
                self.assertRegex(atlas["processor_sha256"], r"^[0-9a-f]{64}$")
                self.assertIn("global_gain_db", atlas)
                self.assertEqual({"steady", "accel", "decel"}, set(atlas["states"]))
                self.assertEqual(18, sum(len(items) for items in atlas["states"].values()))
                for items in atlas["states"].values():
                    self.assertEqual(6, len({item["sha256"] for item in items}))
                    for item in items:
                        self.assertEqual(
                            item["anchor_firing_hz"], item["rendered_cadence_hz"]
                        )
                        self.assertAlmostEqual(
                            item["anchor_firing_hz"] / item["source_cadence_hz"],
                            item["source_playback_ratio"],
                        )
                        with wave.open(str(output / item["file"]), "rb") as handle:
                            channels = handle.getnchannels()
                            values = struct.unpack(
                                f"<{handle.getnframes() * channels}h",
                                handle.readframes(handle.getnframes()),
                            )
                        for channel in range(channels):
                            samples = values[channel::channels]
                            seam_delta = abs(samples[0] - samples[-1]) / 32768.0
                            adjacent = sorted(
                                abs(samples[index] - samples[index - 1]) / 32768.0
                                for index in range(1, len(samples))
                            )
                            adjacent_p999 = adjacent[round(0.999 * (len(adjacent) - 1))]
                            self.assertLessEqual(
                                seam_delta, max(0.005, adjacent_p999 * 1.5), item["file"]
                            )
                self.assertEqual(atlas_path.as_posix(), report["manifest"])
                hashes.append(
                    {
                        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                        for path in sorted(output.glob("ferrari_v10_*.wav"))
                    }
                )
            self.assertEqual(hashes[0], hashes[1])

    def test_v10_uses_lifecycle_targets_while_v12_remains_independent(self):
        project = json.dumps(self.load_json("VehicleSoundSynth-V5.maxproj"))
        self.assertIn("ferrari_v10_lifecycle_targets.json", project)
        self.assertNotIn("v10_state_renderer", project)
        self.assertNotIn("v12_texture_renderer", project)
        for profile in ("v10", "v12"):
            power = "\n".join(
                item["box"].get("text", "")
                for item in self.load_json(f"patchers/{profile}_powertrain~.maxpat")["patcher"]["boxes"]
            )
            self.assertIn(
                f"gen~ @gen Patcher:/gen/{profile}_powertrain.gendsp",
                power,
            )
            self.assertNotIn("groove~", power)
            self.assertNotIn("ferrari", power.lower())

    def test_v31_public_contract_exposes_pad_and_reference_texture_controls(self):
        engine = self.load_json("patchers/vehicle_engine~.maxpat")
        text = "\n".join(
            item["box"].get("text", "") for item in engine["patcher"]["boxes"]
        )
        for name in (
            "pad_level_db",
            "pad_mute",
            "pad_solo",
            "reference_texture_level_db",
            "reference_texture_mute",
        ):
            self.assertIn(name, text)

    def test_v31_master_eq_is_one_visible_four_node_graph_before_stereo_cascade(self):
        eq = self.load_json("patchers/vehicle_bus_eq~.maxpat")["patcher"]
        boxes = [item["box"] for item in eq["boxes"]]
        graphs = [box for box in boxes if box["maxclass"] == "filtergraph~"]
        self.assertEqual(1, len(graphs))
        self.assertEqual(4, graphs[0]["nfilters"])
        self.assertEqual(1, graphs[0]["presentation"])
        self.assertEqual(2, sum(box.get("text") == "cascade~ 4" for box in boxes))
        self.assertEqual(1, eq["openinpresentation"])

        engine = self.load_json("patchers/vehicle_engine~.maxpat")["patcher"]
        engine_boxes = [item["box"] for item in engine["boxes"]]
        self.assertTrue(
            any(
                box["maxclass"] == "bpatcher"
                and box.get("name") == "mix_master~.maxpat"
                for box in engine_boxes
            )
        )
        for profile in ("ev", "v10", "v12"):
            main = self.load_json(f"VehicleSoundSynth-{profile.upper()}.maxpat")["patcher"]
            self.assertTrue(
                any(
                    item["box"].get("name", "").endswith(
                        f"/patchers/vehicle_engine_{profile}~.maxpat"
                    )
                    for item in main["boxes"]
                )
            )

    def test_v4_combustion_models_use_phase_stable_stereo_orders(self):
        for name, bank_events in (("v12_powertrain", "3"), ("v10_powertrain", "2.5")):
            patcher = self.load_json(f"gen/{name}.gendsp")["patcher"]
            code = "\n".join(item["box"].get("code", "") for item in patcher["boxes"])
            self.assertIn(f"bank_fire = clamp(crank * {bank_events} *", code)
            self.assertIn("phase_l = phasor(bank_fire)", code)
            self.assertIn("phase_r = phase_l + 0.5", code)
            self.assertIn("fire = bank_fire * 2", code)
            self.assertIn("orders_l = cycle(fire)", code)
            self.assertNotIn("raw_phase = phasor(fire)", code)
            self.assertNotIn("noise()", code)
            self.assertNotIn("0.5015", code)
            self.assertNotIn("0.503", code)

    def test_v31_cabin_field_centers_bass_and_widens_only_above_120_hz(self):
        patcher = self.load_json("patchers/cabin_master~.maxpat")["patcher"]
        text = "\n".join(item["box"].get("text", "") for item in patcher["boxes"])
        self.assertGreaterEqual(text.count("cross~ 120"), 2)

    def test_v4_combustion_banks_use_wrap_continuous_raised_cosine_pulses(self):
        for name in ("v10_powertrain.gendsp", "v12_powertrain.gendsp"):
            patcher = self.load_json(f"gen/{name}")["patcher"]
            code = "\n".join(item["box"].get("code", "") for item in patcher["boxes"])
            self.assertIn("cycle_variation", code)
            self.assertIn("cylinder_l =", code)
            self.assertIn("cylinder_r =", code)
            self.assertIn("pulse_l = pow(0.5 + 0.5 * cos(phase_l * 6.283185307179586), 4) - 0.2734375", code)
            self.assertIn("pulse_r = pow(0.5 + 0.5 * cos(phase_r * 6.283185307179586), 4) - 0.2734375", code)
            self.assertIn("bank_l =", code)
            self.assertIn("bank_r =", code)
            self.assertIn("shared_low =", code)
            self.assertNotIn("exp(-bank_phase", code)
            self.assertNotIn("event_trigger", code)
            self.assertNotIn("event_phase_l", code)
            self.assertNotIn("event_phase_r", code)

    def test_v4_cabin_field_uses_rpm_adaptive_three_band_side_control(self):
        patcher = self.load_json("patchers/cabin_master~.maxpat")["patcher"]
        text = "\n".join(item["box"].get("text", "") for item in patcher["boxes"])
        self.assertIn("rpm", text)
        self.assertIn("cross~ 2000", text)
        self.assertIn("expr 1.-0.1*min(1.,max(0.,($f1-1500.)/2500.))", text)
        self.assertIn("*~ 0.24", text)
        self.assertIn("*~ 0.26", text)
        self.assertIn("*~ 0.04", text)
        self.assertNotIn("*~ 0.12", text)

        engine = self.load_json("patchers/vehicle_engine~.maxpat")["patcher"]
        boxes = {item["box"]["id"]: item["box"] for item in engine["boxes"]}
        controller = next(box_id for box_id, box in boxes.items() if box.get("text") == "engine_controller")
        fan = next(box_id for box_id, box in boxes.items() if box.get("text") == "t l l l l l l l")
        cabin = next(box_id for box_id, box in boxes.items() if box.get("text") == "cabin_master~")
        self.assertTrue(any(
            line["patchline"]["source"][0] == controller
            and line["patchline"]["destination"][0] == fan
            for line in engine["lines"]
        ))
        self.assertTrue(any(
            line["patchline"]["source"][0] == fan
            and line["patchline"]["destination"][0] == cabin
            for line in engine["lines"]
        ))
        self.assertIn("allpass~ 8. 1.7 0.42", text)
        self.assertIn("allpass~ 8. 2.3 -0.36", text)
        self.assertIn("tapout~ 0.65", text)
        self.assertIn("tapout~ 1.35", text)
        self.assertIn("expr 0.6 + 1.2*$f1", text)
        self.assertNotIn("*~ 0.20", text)
        self.assertNotIn("*~ 0.42", text)
        self.assertNotIn("svf~ 180 0.5", text)

    def test_v31_pad_has_independent_level_mute_solo_and_safe_stereo_sum(self):
        driver = self.load_json("patchers/ev_pad_driver~.maxpat")["patcher"]
        driver_text = "\n".join(item["box"].get("text", "") for item in driver["boxes"])
        self.assertIn("pad_level_db", driver_text)
        self.assertIn("pad_mute", driver_text)
        self.assertIn("expr pow(10., $f1/20.)", driver_text)
        self.assertIn("*~ 0.18", driver_text)
        self.assertIn("*~ 0.5", driver_text)
        self.assertNotIn("*~ 1.412537545", driver_text)
        self.assertIn("loadmess -3", driver_text)
        self.assertNotIn("*~ 0.04", driver_text)

        boxes = {item["box"]["id"]: item["box"] for item in driver["boxes"]}
        lines = [item["patchline"] for item in driver["lines"]]
        low_mid = next(box_id for box_id, box in boxes.items() if box.get("text") == "*~ 0.5")
        stereo_sums = {
            line["destination"][0]
            for line in lines
            if line["source"][0] == low_mid
        }
        self.assertEqual(2, len(stereo_sums))

        pad = self.load_json("patchers/ev_pad_beap~.maxpat")["patcher"]
        pad_text = "\n".join(item["box"].get("text", "") for item in pad["boxes"])
        self.assertEqual(2, pad_text.splitlines().count("*~ 0.6"))
        self.assertNotIn("*~ 0.2", pad_text)

        power = self.load_json("patchers/powertrain~.maxpat")["patcher"]
        power_text = "\n".join(item["box"].get("text", "") for item in power["boxes"])
        self.assertIn("pad_solo", power_text)
        self.assertIn("reference_texture~", power_text)

    def test_v4_reference_texture_is_retained_only_as_an_undeclared_offline_archive(self):
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        declared = {
            path for category in project["contents"].values() for path in category
        }
        self.assertNotIn("patchers/reference_texture~.maxpat", declared)
        patcher = self.load_json("patchers/reference_texture~.maxpat")["patcher"]
        text = "\n".join(item["box"].get("text", "") for item in patcher["boxes"])
        self.assertIn("offline", text.lower())

    def test_v4_reference_texture_uses_normalized_multi_anchor_stereo_bank(self):
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        declared = {path for category in project["contents"].values() for path in category}
        patcher = self.load_json("patchers/reference_texture~.maxpat")["patcher"]
        text = "\n".join(item["box"].get("text", "") for item in patcher["boxes"])
        for anchor in ("065", "110", "180", "260", "380", "520"):
            for variant in ("a", "b"):
                filename = f"engine_texture_{anchor}_{variant}.wav"
                self.assertNotIn(f"media/{filename}", declared)
                self.assertIn(filename, text)
        self.assertIn("expr max(.9,min(1.1", text)
        self.assertNotIn("max(.25,min(4.", text)
        self.assertNotIn("*~ 3.981071706", text)

    def test_v4_engine_texture_bank_media_match_normalization_metadata(self):
        import math

        metadata = self.load_json("assets/engine_texture_bank.json")
        self.assertEqual(12, len(metadata["outputs"]))
        for output in metadata["outputs"]:
            path = ROOT / output["path"]
            self.assertEqual(output["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())
            with wave.open(str(path), "rb") as handle:
                self.assertEqual(2, handle.getnchannels())
                self.assertEqual(2, handle.getsampwidth())
                self.assertEqual(48000, handle.getframerate())
                self.assertGreaterEqual(handle.getnframes(), 4 * 48000)
                values = struct.unpack(
                    f"<{handle.getnframes() * 2}h", handle.readframes(handle.getnframes())
                )
            normalized = [value / 32768.0 for value in values]
            rms = math.sqrt(sum(value * value for value in normalized) / len(normalized))
            self.assertAlmostEqual(-18.0, 20.0 * math.log10(rms), delta=0.05)
            left = normalized[0::2]
            right = normalized[1::2]
            mid = [(left_value + right_value) * 0.5 for left_value, right_value in zip(left, right)]
            side = [(left_value - right_value) * 0.5 for left_value, right_value in zip(left, right)]
            mid_power = sum(value * value for value in mid)
            side_power = sum(value * value for value in side)
            side_ratio = side_power / max(mid_power + side_power, 1e-30)
            correlation = sum(a * b for a, b in zip(left, right)) / math.sqrt(
                sum(value * value for value in left) * sum(value * value for value in right)
            )
            self.assertGreaterEqual(side_ratio, 0.06)
            self.assertLessEqual(side_ratio, 0.16)
            self.assertLessEqual(correlation, 0.88)
            self.assertLessEqual(abs(left[-1] - left[0]), 2.0 / 32768.0)
            self.assertLessEqual(abs(right[-1] - right[0]), 2.0 / 32768.0)

            sys.path.insert(0, str(ROOT / "tools"))
            from audio_metrics import envelope_modulation_metrics

            modulation = envelope_modulation_metrics(mid, 48000)
            self.assertLessEqual(modulation["modulation_peak_ratio_0_5_20_hz"], 0.40)
            self.assertLessEqual(modulation["envelope_autocorrelation_peak"], 0.65)

    def test_v4_local_reference_bundle_normalizes_residual_and_body_layers(self):
        import math

        sys.path.insert(0, str(ROOT / "tools"))
        from prepare_local_reference import prepare_reference_bundle

        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.wav"
            output = Path(directory) / "local"
            frames = 24 * 48000
            with wave.open(str(source), "wb") as handle:
                handle.setnchannels(2)
                handle.setsampwidth(2)
                handle.setframerate(48000)
                payload = []
                for index in range(frames):
                    time = index / 48000
                    value = 0.35 * math.sin(2 * math.pi * 61.5 * time)
                    value += 0.12 * math.sin(2 * math.pi * 345.7 * time)
                    payload.append(struct.pack("<hh", round(value * 32767), round(value * 0.97 * 32767)))
                handle.writeframes(b"".join(payload))
            result = prepare_reference_bundle(source, output)
            self.assertEqual(0.25, result["idle"]["duration_seconds"])
            self.assertEqual(0.5, result["high"]["duration_seconds"])
            self.assertEqual(1.2, result["startup"]["duration_seconds"])
            self.assertEqual(3.0, result["idle_body"]["duration_seconds"])
            for name in ("idle", "high"):
                self.assertAlmostEqual(-18.0, result[name]["rms_dbfs"], delta=0.25)
                self.assertLessEqual(result[name]["peak_dbfs"], -3.0 + 0.05)
            self.assertAlmostEqual(-14.0, result["startup"]["rms_dbfs"], delta=0.25)
            self.assertAlmostEqual(-15.5, result["idle_body"]["rms_dbfs"], delta=0.25)
            self.assertLessEqual(result["startup"]["peak_dbfs"], -3.0 + 0.05)
            self.assertLessEqual(result["idle_body"]["peak_dbfs"], -3.0 + 0.05)

            idle_body = output / "ferrari_sf90_idle_body.wav"
            with wave.open(str(idle_body), "rb") as handle:
                self.assertEqual(2, handle.getnchannels())
                self.assertEqual(48000, handle.getframerate())
                self.assertEqual(144000, handle.getnframes())
                samples = struct.unpack("<288000h", handle.readframes(144000))
            left = [samples[index] / 32768.0 for index in range(0, len(samples), 2)]

            def projected_amplitude(frequency):
                cosine = sum(
                    value * math.cos(2 * math.pi * frequency * index / 48000)
                    for index, value in enumerate(left)
                )
                sine = sum(
                    value * math.sin(2 * math.pi * frequency * index / 48000)
                    for index, value in enumerate(left)
                )
                return 2.0 * math.hypot(cosine, sine) / len(left)

            self.assertGreater(projected_amplitude(61.5), projected_amplitude(345.7))

    def test_v31_local_reference_processor_writes_normalized_stereo_loop(self):
        import math

        sys.path.insert(0, str(ROOT / "tools"))
        from prepare_local_reference import prepare_reference

        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.wav"
            destination = Path(directory) / "residual.wav"
            frames = 6 * 48000
            with wave.open(str(source), "wb") as handle:
                handle.setnchannels(2)
                handle.setsampwidth(2)
                handle.setframerate(48000)
                payload = []
                for index in range(frames):
                    time = index / 48000
                    base = 0.45 * math.sin(2 * math.pi * 61.5 * time)
                    texture = 0.08 * math.sin(2 * math.pi * 347.0 * time)
                    payload.append(struct.pack("<hh", round((base + texture) * 32767), round((base + texture * 0.94) * 32767)))
                handle.writeframes(b"".join(payload))
            result = prepare_reference(source, destination, start_seconds=1.0)
            with wave.open(str(destination), "rb") as handle:
                self.assertEqual(2, handle.getnchannels())
                self.assertEqual(48000, handle.getframerate())
                self.assertEqual(12000, handle.getnframes())
                samples = struct.unpack("<24000h", handle.readframes(12000))
            self.assertLess(abs(samples[-2] - samples[0]) / 32768.0, 0.05)
            self.assertLess(abs(samples[-1] - samples[1]) / 32768.0, 0.05)
            self.assertAlmostEqual(-18.0, result["rms_dbfs"], delta=0.25)
            self.assertLessEqual(result["peak_dbfs"], -3.0 + 0.05)
            left = [samples[index] / 32768.0 for index in range(0, len(samples), 2)]

            def projected_amplitude(frequency):
                cosine = sum(
                    value * math.cos(2 * math.pi * frequency * index / 48000)
                    for index, value in enumerate(left)
                )
                sine = sum(
                    value * math.sin(2 * math.pi * frequency * index / 48000)
                    for index, value in enumerate(left)
                )
                return 2.0 * math.hypot(cosine, sine) / len(left)

            self.assertLess(projected_amplitude(61.5), projected_amplitude(347.0) * 0.10)

    def test_v4_banked_harmonic_body_preserves_low_orders_and_adds_independent_air(self):
        expected = {
            "v12_powertrain": (
                "orders_l = cycle(fire) * 0.17",
                "cycle(clamp(fire * 2.0, 45, 3200))",
                "cycle(clamp(fire * 3.0, 55, 5200))",
                "bright_l =",
                "bright_r =",
            ),
            "v10_powertrain": (
                "orders_l = cycle(fire) * 0.18",
                "cycle(clamp(fire * 1.5, 45, 1800))",
                "cycle(clamp(fire * 2.5, 65, 5200))",
                "bright_l =",
                "bright_r =",
            ),
        }
        for name, coefficients in expected.items():
            patcher = self.load_json(f"gen/{name}.gendsp")["patcher"]
            code = "\n".join(item["box"].get("code", "") for item in patcher["boxes"])
            for coefficient in coefficients:
                self.assertIn(coefficient, code)

    def test_v4_fuel_profiles_soften_idle_highs_without_flattening_high_rpm(self):
        powertrain = self.load_json("patchers/powertrain~.maxpat")["patcher"]
        powertrain_text = "\n".join(
            item["box"].get("text", "") for item in powertrain["boxes"]
        )
        self.assertIn(
            "expr 2600.+5200.*max(0.,min(1.,($f1-800.)/8200.))+600.*$f2",
            powertrain_text,
        )
        self.assertEqual(4, powertrain_text.count("svf~ 3000 0.65"))

        expected = {
            "v12_powertrain": "sat_drive = 1 + saturation * 0.85",
            "v10_powertrain": "sat_drive = 1 + saturation * 0.95",
        }
        for name, drive in expected.items():
            patcher = self.load_json(f"gen/{name}.gendsp")["patcher"]
            code = "\n".join(item["box"].get("code", "") for item in patcher["boxes"])
            self.assertIn(drive, code)
            self.assertIn("tanh(left_drive * sat_drive) / sat_drive", code)
            self.assertIn("tanh(right_drive * sat_drive) / sat_drive", code)
            self.assertNotIn("clamp(tanh", code)

    def test_v3_project_identity_and_public_entrypoint(self):
        project_path = ROOT / "VehicleSoundSynth-V5.maxproj"
        self.assertTrue(project_path.is_file())
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        self.assertEqual("VehicleSoundSynth-V5", project["name"])
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
            "Future EV": (-2.0, -14.0, -60.0),
            "High-Rev V12": (-3.0, -16.0, -5.0),
            "Aggressive V10": (-3.0, -16.0, -4.0),
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
            "cabin_ir_mix",
            "buffer~ cabin_ir_l Patcher:/media/cabin_ir_l.wav",
            "buffer~ cabin_ir_r Patcher:/media/cabin_ir_r.wav",
            "buffir~ cabin_ir_l 0 4096",
            "buffir~ cabin_ir_r 0 4096", "expr sqrt(1.-$f1)", "expr sqrt($f1)",
        ):
            self.assertIn(token, text)
        self.assertEqual(2, text.count("cross~ 120"))
        self.assertNotIn("svf~ 180 0.5", text)
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
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
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
        self.assertEqual(2, cabin_text.count("cross~ 120"))

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

        for profile in ("ev", "v10", "v12"):
            engine = self.load_json(f"patchers/vehicle_engine_{profile}~.maxpat")
            text = "\n".join(item["box"].get("text", "") for item in engine["patcher"]["boxes"])
            for token in ("cabin_rumble", "exhaust_boom", "structure_vibration"):
                self.assertIn(token, text)

    def test_v2_engine_routes_through_lifecycle_and_final_mix_modules(self):
        engine = self.load_json("patchers/vehicle_engine~.maxpat")
        text = "\n".join(item["box"].get("text", "") for item in engine["patcher"]["boxes"])
        self.assertIn("engine_controller", text)
        self.assertTrue(any(
            item["box"]["maxclass"] == "bpatcher"
            and item["box"].get("name") == "mix_master~.maxpat"
            for item in engine["patcher"]["boxes"]
        ))
        self.assertTrue((ROOT / "patchers" / "engine_controller.maxpat").is_file())
        self.assertTrue((ROOT / "patchers" / "mix_master~.maxpat").is_file())

    def test_v2_fuel_generators_expose_running_and_shift_envelopes(self):
        for name, bank_events in (("v12_powertrain", "3"), ("v10_powertrain", "2.5")):
            patcher = self.load_json(f"gen/{name}.gendsp")["patcher"]
            code = "\n".join(item["box"].get("code", "") for item in patcher["boxes"])
            for parameter in ("engine_running", "combustion_gain", "shift_cut"):
                self.assertIn(f"Param {parameter}", code)
            self.assertIn(f"bank_fire = clamp(crank * {bank_events} *", code)
            self.assertIn("phase_l = phasor(bank_fire)", code)
            self.assertIn("pulse_l = pow(0.5 + 0.5 * cos(phase_l", code)
            self.assertIn("pulse_r = pow(0.5 + 0.5 * cos(phase_r", code)
            self.assertNotIn("pulse_l = exp(-bank_phase_l", code)
            self.assertNotIn("pulse_r = exp(-bank_phase_r", code)
            self.assertIn("tanh(", code)
            self.assertGreaterEqual(code.count("cycle("), 12)
            self.assertIn("idle_weight", code)

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

        transient = self.load_json("patchers/v10_backfire_host~.maxpat")
        transient_text = "\n".join(item["box"].get("text", "") for item in transient["patcher"]["boxes"])
        self.assertIn("gate 1", transient_text)
        self.assertIn("engine_running", transient_text)
        self.assertIn("overrun", transient_text)
        self.assertNotIn("($f1 < -0.18) && ($f2 > 1400.)", transient_text)
        self.assertIn("backfire_intensity", transient_text)
        self.assertNotIn("play~", transient_text)

    def test_runnable_project_has_public_engine_interface(self):
        required = [
            "VehicleSoundSynth-V5.maxproj",
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
            "pad_level_db", "pad_mute", "pad_solo",
            "reference_texture_level_db", "reference_texture_mute",
            "compressor_threshold_db", "compressor_ratio",
            "compressor_attack_rate", "compressor_release_rate",
            "compressor_makeup_db", "compressor_bypass",
            "air_detail", "cycle_irregularity", "stereo_width",
            "throttle_loudness_depth", "saturation",
        }
        for values in presets.values():
            profile_specific = (
                {"torque_ripple_level", "gear_mesh_level", "electrical_detail"}
                if values["engine_type"] == "ev"
                else {"combustion_pulse", "intake_detail", "exhaust_detail", "residual_detail"}
            )
            self.assertEqual(expected | profile_specific, set(values))
            self.assertIn(values["engine_type"], {"ev", "v12", "v10"})
            db_parameters = {
                "master_trim_db", "powertrain_level_db", "transient_level_db",
                "road_level_db", "rumble_level_db", "pad_level_db",
                "reference_texture_level_db",
            }
            compressor_parameters = {
                "compressor_threshold_db", "compressor_ratio",
                "compressor_attack_rate", "compressor_release_rate",
                "compressor_makeup_db", "compressor_bypass",
            }
            bounded = {
                key: value for key, value in values.items()
                if key not in {"engine_type", "throttle_loudness_depth", *db_parameters, *compressor_parameters}
            }
            self.assertTrue(all(0.0 <= value <= 1.0 for value in bounded.values()))
            self.assertTrue(0.0 <= values["throttle_loudness_depth"] <= 8.0)
            self.assertTrue(-24.0 <= values["master_trim_db"] <= 0.0)
            self.assertTrue(all(-60.0 <= values[key] <= 6.0 for key in db_parameters - {"master_trim_db"}))
            self.assertTrue(-36.0 <= values["compressor_threshold_db"] <= 0.0)
            self.assertTrue(1.0 <= values["compressor_ratio"] <= 50.0)
            self.assertTrue(0.0 <= values["compressor_attack_rate"] <= 150.0)
            self.assertTrue(0.0 <= values["compressor_release_rate"] <= 150.0)
            self.assertTrue(-12.0 <= values["compressor_makeup_db"] <= 12.0)
            self.assertIn(values["compressor_bypass"], (0.0, 1.0))
        self.assertEqual(-18.0, presets["High-Rev V12"]["reference_texture_level_db"])
        self.assertEqual(-18.0, presets["Aggressive V10"]["reference_texture_level_db"])

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

        eq = self.load_json("patchers/vehicle_bus_eq~.maxpat")
        eq_boxes = {item["box"]["id"]: item["box"] for item in eq["patcher"]["boxes"]}
        eq_text = "\n".join(box.get("text", "") for box in eq_boxes.values())
        self.assertEqual(1, sum(box["maxclass"] == "filtergraph~" for box in eq_boxes.values()))
        self.assertEqual(2, sum(box.get("text") == "cascade~ 4" for box in eq_boxes.values()))
        for token in ("eq_low", "eq_lowmid", "eq_highmid", "eq_high", "eq_bypass", "master_trim_db"):
            self.assertIn(token, eq_text)

        mix = self.load_json("patchers/mix_master~.maxpat")
        mix_boxes = {item["box"]["id"]: item["box"] for item in mix["patcher"]["boxes"]}
        mix_text = "\n".join(box.get("text", "") for box in mix_boxes.values())
        self.assertNotIn("filtergraph~", mix_text)
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
        eq = self.load_json("patchers/vehicle_bus_eq~.maxpat")["patcher"]
        boxes = {item["box"]["id"]: item["box"] for item in eq["boxes"]}
        lines = [item["patchline"] for item in eq["lines"]]
        graphs = {
            box_id for box_id, box in boxes.items()
            if box["maxclass"] == "filtergraph~"
        }
        parameter_paks = {
            box_id for box_id, box in boxes.items()
            if box.get("text", "").startswith("pak ")
        }
        self.assertEqual(1, len(graphs))
        graph = next(iter(graphs))
        coefficient_inputs = [
            line for line in lines
            if line["destination"] == [graph, 5]
        ]
        trigger_texts = [boxes[line["source"][0]].get("text") for line in coefficient_inputs]
        self.assertEqual(4, trigger_texts.count("t b l b"))
        self.assertEqual(1, trigger_texts.count("t b l"))
        self.assertEqual(2, sum(box.get("text") == "unpack 0. 0." for box in boxes.values()))
        self.assertEqual(2, sum(box.get("text") == "unpack 0. 0. 0." for box in boxes.values()))
        self.assertFalse(
            any(box.get("text", "").startswith("prepend lowshelf") for box in boxes.values())
        )
        self.assertFalse(
            any(box.get("text", "").startswith("prepend peaknotch") for box in boxes.values())
        )
        self.assertFalse(
            any(box.get("text", "").startswith("prepend highshelf") for box in boxes.values())
        )
        # Max 8.6.5 escapes literal commas when it serializes an expr object.
        normalized_texts = [box.get("text", "").replace("\\,", ",") for box in boxes.values()]
        self.assertEqual(5, normalized_texts.count("expr pow(10., $f1/10.)"))
        self.assertTrue(
            "expr 10.*log(max($f1,0.000001))/log(10.)" in normalized_texts
        )

    def test_demo_starts_muted(self):
        for name in ("EV", "V10", "V12"):
            main = self.load_json(f"VehicleSoundSynth-{name}.maxpat")
            boxes = {item["box"]["id"]: item["box"] for item in main["patcher"]["boxes"]}
            text = "\n".join(box.get("text", "") for box in boxes.values())
            self.assertIn("Audio starts OFF", text)
            cords = {
                (line["patchline"]["source"][0], line["patchline"]["destination"][0])
                for line in main["patcher"]["lines"]
            }
            toggles = {box["id"] for box in boxes.values() if box["maxclass"] == "toggle"}
            loads = {box["id"] for box in boxes.values() if box.get("text") == "loadmess 0"}
            self.assertTrue(any((load, toggle) in cords for load in loads for toggle in toggles))
            self.assertTrue(
                any(
                    box.get("text") == "ezdac~" or box.get("maxclass") == "ezdac~"
                    for box in boxes.values()
                )
            )

    def test_profile_runtime_has_one_step_audio_enable_and_unified_manual_input(self):
        for name in ("EV", "V10", "V12"):
            main = self.load_json(f"VehicleSoundSynth-{name}.maxpat")["patcher"]
            boxes = {item["box"]["id"]: item["box"] for item in main["boxes"]}
            lines = [item["patchline"] for item in main["lines"]]

            dac_id = next(
                box_id
                for box_id, box in boxes.items()
                if box.get("text") == "ezdac~" or box.get("maxclass") == "ezdac~"
            )
            audio_pack_id = next(
                box_id
                for box_id, box in boxes.items()
                if box.get("text") == "pack 0. 60"
            )
            audio_toggle_id = next(
                line["source"][0]
                for line in lines
                if line["destination"] == [audio_pack_id, 0]
                and boxes[line["source"][0]].get("maxclass") == "toggle"
            )
            self.assertTrue(
                any(
                    line["source"][0] == audio_toggle_id
                    and line["destination"] == [dac_id, 0]
                    for line in lines
                ),
                f"{name} Audio toggle must enable both the output ramp and DSP",
            )

            manual_input_id = next(
                box_id
                for box_id, box in boxes.items()
                if box.get("name", "").endswith("/patchers/manual_input.maxpat")
            )
            throttle_number_id = next(
                box_id
                for box_id, box in boxes.items()
                if box.get("maxclass") == "flonum"
                and box.get("patching_rect", [None])[0] == 25
            )
            brake_number_id = next(
                box_id
                for box_id, box in boxes.items()
                if box.get("maxclass") == "flonum"
                and box.get("patching_rect", [None])[0] == 175
            )
            self.assertTrue(
                any(
                    line["source"] == [manual_input_id, 0]
                    and line["destination"] == [throttle_number_id, 0]
                    for line in lines
                )
            )
            self.assertTrue(
                any(
                    line["source"] == [manual_input_id, 1]
                    and line["destination"] == [brake_number_id, 0]
                    for line in lines
                )
            )

        keyboard = self.load_json("patchers/keyboard_drive_ws.maxpat")["patcher"]
        keyboard_text = "\n".join(
            item["box"].get("text", "") for item in keyboard["boxes"]
        )
        self.assertIn("key", keyboard_text)
        self.assertIn("keyup", keyboard_text)
        self.assertEqual(2, keyboard_text.count("sel 119 87 115 83"))

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

    def test_ev_low_frequency_output_is_phase_coherent_between_channels(self):
        patcher = self.load_json("gen/ev_powertrain.gendsp")["patcher"]
        code = "\n".join(
            item["box"].get("code", item["box"].get("text", ""))
            for item in patcher["boxes"]
        )
        for near_unison_ratio in ("1.007", "1.013"):
            self.assertNotIn(near_unison_ratio, code)
        self.assertIn("coherent_low", code)
        self.assertIn("out1 =", code)
        self.assertIn("out2 =", code)

    def test_ev_generator_source_has_no_obsolete_near_unison_model(self):
        source = (ROOT / "tools" / "build_project.py").read_text(encoding="utf-8")
        for near_unison_ratio in ("1.007", "1.013"):
            self.assertNotIn(near_unison_ratio, source)

    def test_ev_pad_uses_an_exact_three_to_two_fifth(self):
        patcher = self.load_json("patchers/ev_pad_beap~.maxpat")["patcher"]
        texts = {
            item["box"].get("text", "")
            for item in patcher["boxes"]
        }
        self.assertIn("+~ 1.5849625", texts)
        self.assertNotIn("+~ 1.583333", texts)

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
                self.assertTrue(any(
                    item["box"].get("text", "").startswith(f"param {name} ")
                    for item in patcher["boxes"]
                ), f"{path.name}: {name} is not exposed by a top-level Gen param")
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

    def test_shared_soundscape_replaces_legacy_ev_pad_in_declared_runtime(self):
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        declared = {
            relative_path
            for category in project["contents"].values()
            for relative_path in category
        }
        self.assertNotIn("patchers/ev_pad_driver~.maxpat", declared)
        self.assertNotIn("patchers/ev_pad_beap~.maxpat", declared)
        self.assertIn("patchers/ev_cinematic_soundscape_host~.maxpat", declared)
        self.assertNotIn("patchers/cinematic_soundscape_voice.maxpat", declared)
        self.assertIn("patchers/cinematic_soundscape_beap~.maxpat", declared)

        pad = self.load_json("patchers/cinematic_soundscape_beap~.maxpat")["patcher"]
        modules = [
            item["box"] for item in pad["boxes"]
            if item["box"].get("maxclass") == "bpatcher"
        ]
        self.assertGreaterEqual(len(modules), 10)
        self.assertEqual(len(modules), len({module.get("varname") for module in modules}))
        signal_inlets = [
            item for item in pad["boxes"]
            if item["box"].get("maxclass") == "inlet"
            and "signal" in item["box"].get("outlettype", [])
        ]
        signal_outlets = [
            item for item in pad["boxes"]
            if item["box"].get("maxclass") == "outlet"
            and item["box"].get("comment") == "signal"
        ]
        self.assertEqual(5, len(signal_inlets))
        self.assertEqual(2, len(signal_outlets))

    def test_seeded_beap_pad_restores_audible_pad_defaults(self):
        pad = self.load_json("patchers/ev_pad_beap~.maxpat")["patcher"]
        modules = {
            item["box"]["varname"]: item["box"]
            for item in pad["boxes"]
            if item["box"].get("maxclass") == "bpatcher"
        }

        def restored(module, parameter):
            values = []

            def visit(item):
                if isinstance(item, dict):
                    restore = item.get("restore", {})
                    if parameter in restore:
                        values.append(restore[parameter][0])
                    for child in item.values():
                        visit(child)
                elif isinstance(item, list):
                    for child in item:
                        visit(child)

            visit(module)
            self.assertEqual(1, len(values), f"{module['varname']}: {parameter}")
            return values[0]

        for channel in ("L", "R"):
            self.assertEqual(-15, restored(modules[f"{channel}_Mixer"], "in1"))
            self.assertEqual(-18, restored(modules[f"{channel}_Mixer"], "in2"))
            self.assertEqual(1200, restored(modules[f"{channel}_Ladder"], "Freq"))
            self.assertEqual(8, restored(modules[f"{channel}_Ladder"], "Res"))
            self.assertEqual(450, restored(modules[f"{channel}_ADSR"], "Attack"))
            self.assertEqual(1600, restored(modules[f"{channel}_ADSR"], "Release"))
        self.assertEqual(1, restored(modules["L_Osc_A"], "Waveform"))
        self.assertEqual(0, restored(modules["L_Osc_B"], "Waveform"))
        self.assertEqual(0, restored(modules["R_Osc_A"], "Waveform"))
        self.assertEqual(1, restored(modules["R_Osc_B"], "Waveform"))

        driver = self.load_json("patchers/ev_pad_driver~.maxpat")["patcher"]
        driver_text = "\n".join(item["box"].get("text", "") for item in driver["boxes"])
        self.assertNotIn("*~ 1.412537545", driver_text)
        self.assertIn("loadmess -3", driver_text)

    def test_project_search_path_schema_and_runtime_resources_are_declared(self):
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        # Max 8.6.x expects a dictionary here and can crash while opening a
        # project whose searchpath is encoded as an array. Explicit relative
        # paths avoid collisions with Max's own patchers/gen/media folders.
        self.assertEqual(
            {
                name: {"path": f"./{name}", "recursive": 1}
                for name in ("patchers", "gen", "code", "media", "presets")
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
            "patchers/transient~.maxpat",
            "patchers/road_air~.maxpat",
            "patchers/cabin_master~.maxpat",
            "patchers/mix_master~.maxpat",
            "patchers/vehicle_engine_ev~.maxpat",
            "patchers/vehicle_engine_v10~.maxpat",
            "patchers/vehicle_engine_v12~.maxpat",
            "patchers/drive_simulator_ev.maxpat",
            "patchers/drive_simulator_v10.maxpat",
            "patchers/drive_simulator_v12.maxpat",
            "gen/ev_powertrain.gendsp",
            "gen/v12_powertrain.gendsp",
            "gen/v10_powertrain.gendsp",
            "presets/sound_dna.json",
            "presets/vehicle_bus_eq_default.json",
        }
        self.assertTrue(required.issubset(declared))
        for relative_path in declared:
            self.assertTrue((ROOT / relative_path).is_file(), relative_path)

    def test_demo_ui_and_engine_deep_modules_cover_the_mvp(self):
        for profile, label in (("ev", "EV"), ("v10", "V10"), ("v12", "V12")):
            main = self.load_json(f"VehicleSoundSynth-{label}.maxpat")
            main_text = "\n".join(item["box"].get("text", "") for item in main["patcher"]["boxes"])
            main_boxes = [item["box"] for item in main["patcher"]["boxes"]]
            menu_items = [item for box in main_boxes for item in box.get("items", [])]
            self.assertIn("Internal Manual", menu_items)
            self.assertIn("Internal Auto", menu_items)
            self.assertIn(f"External vss.{profile}.input", menu_items)
            self.assertEqual(2, sum(box["maxclass"] == "meter~" for box in main_boxes))
            self.assertEqual(2, main_text.count("spectroscope~"))

            engine = self.load_json(f"patchers/vehicle_engine_{profile}~.maxpat")
            engine_text = "\n".join(item["box"].get("text", "") for item in engine["patcher"]["boxes"])
            for abstraction in (
                f"engine_controller_{profile}", f"{profile}_sound_dna~",
                f"transient_{profile}~", "road_air~", "cabin_master~",
            ):
                self.assertIn(abstraction, engine_text)
            self.assertTrue(any(
                item["box"]["maxclass"] == "bpatcher"
                and item["box"].get("name") == "vehicle_bus_eq~.maxpat"
                for item in engine["patcher"]["boxes"]
            ))

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
        for name in ("EV", "V10", "V12"):
            patcher = self.load_json(f"VehicleSoundSynth-{name}.maxpat")["patcher"]
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

    def test_manual_mode_keyboard_has_immediate_binary_pedal_messages(self):
        keyboard = self.load_json("patchers/keyboard_drive_ws.maxpat")["patcher"]
        keyboard_text = "\n".join(
            item["box"].get("text", "") for item in keyboard["boxes"]
        )
        for token in (
            "key", "keyup", "1.", "0.", "0.65",
            "t b b", "set 0", "0.",
        ):
            self.assertIn(token, keyboard_text)
        for removed in ("1. 1800", "0. 900", "0.65 280", "0. 240"):
            self.assertNotIn(removed, keyboard_text)
        boxes = {item["box"]["id"]: item["box"] for item in keyboard["boxes"]}
        edges = {
            (
                line["patchline"]["source"][0],
                line["patchline"]["source"][1],
                line["patchline"]["destination"][0],
                line["patchline"]["destination"][1],
            )
            for line in keyboard["lines"]
        }
        by_text = {}
        for box_id, box in boxes.items():
            by_text.setdefault(box.get("text", ""), []).append(box_id)
        disable = by_text["sel 0"][0]
        order = by_text["t b b"][0]
        reset = by_text["set 0"][0]
        hard_zero = by_text["0."][0]
        self.assertIn((disable, 0, order, 0), edges)
        for change in by_text["change"]:
            self.assertIn((reset, 0, change, 0), edges)
        for line in by_text["line 0."]:
            self.assertIn((hard_zero, 0, line, 0), edges)
        for profile in ("ev", "v10", "v12"):
            patcher = self.load_json(f"patchers/drive_simulator_{profile}.maxpat")["patcher"]
            text = "\n".join(item["box"].get("text", "") for item in patcher["boxes"])
            self.assertIn(
                f"js Patcher:/code/drive_model.js {profile}",
                text,
            )
            self.assertIn("qmetro 20", text)

    def test_preset_messages_refresh_visible_macro_and_gain_controls(self):
        applicable = (
            "aggression", "brightness", "body", "texture", "cabin_width",
            "cabin_rumble", "exhaust_boom", "structure_vibration", "cabin_ir_mix",
            "powertrain_level_db", "transient_level_db", "road_level_db",
            "rumble_level_db", "master_trim_db",
        )
        for profile in ("ev", "v10", "v12"):
            engine = self.load_json(f"patchers/vehicle_engine_{profile}~.maxpat")["patcher"]
            text = "\n".join(item["box"].get("text", "") for item in engine["boxes"])
            for parameter in applicable:
                self.assertIn(parameter, text)
            for removed in ("engine_type", "ev_weight", "v10_weight", "v12_weight"):
                self.assertNotIn(removed, text)

    def test_profile_runtimes_expose_persistent_seven_stem_module_mixer(self):
        project = self.load_json("VehicleSoundSynth-V5.maxproj")
        self.assertIn(
            "patchers/module_mixer.maxpat",
            project["contents"]["patchers"],
        )
        self.assertIn(
            "code/module_mixer_state_path.js",
            project["contents"]["code"],
        )
        mixer = self.load_json("patchers/module_mixer.maxpat")["patcher"]
        mixer_text = "\n".join(
            item["box"].get("text", "") for item in mixer["boxes"]
        )
        for label in (
            "Sound DNA", "Start", "Pop / Event", "Soundscape",
            "Road / Air", "Cabin Rumble", "Master",
        ):
            self.assertIn(label, mixer_text)
        for message in (
            "powertrain_level_db", "start_level_db", "transient_level_db",
            "soundscape_level_db", "road_level_db", "rumble_level_db",
            "master_trim_db",
        ):
            self.assertIn(f"prepend {message}", mixer_text)
        for token in (
            "pattrstorage module_mixer_#1", "autopattr @autorestore 0",
            "js Patcher:/code/module_mixer_state_path.js #1", "delay 250",
            "Save Mix", "Reload Mix", "Reset Defaults",
        ):
            self.assertIn(token, mixer_text)
        master_slider = next(
            item["box"] for item in mixer["boxes"]
            if item["box"].get("varname") == "mix_master_trim_db"
        )
        self.assertEqual(241, master_slider.get("size"))

        for profile in ("ev", "v10", "v12"):
            runtime = self.load_json(
                f"VehicleSoundSynth-{profile.upper()}.maxpat"
            )["patcher"]
            boxes = {item["box"]["id"]: item["box"] for item in runtime["boxes"]}
            mixer_box = next(
                box for box in boxes.values()
                if box.get("name") == "Patcher:/patchers/module_mixer.maxpat"
            )
            self.assertEqual([profile], mixer_box.get("args"))
            engine_box = next(
                box for box in boxes.values()
                if box.get("name", "").endswith(
                    f"/patchers/vehicle_engine_{profile}~.maxpat"
                )
            )
            edges = {
                (
                    line["patchline"]["source"][0],
                    line["patchline"]["source"][1],
                    line["patchline"]["destination"][0],
                    line["patchline"]["destination"][1],
                )
                for line in runtime["lines"]
            }
            self.assertIn((mixer_box["id"], 0, engine_box["id"], 0), edges)
            transient = self.load_json(
                f"patchers/transient_{profile}~.maxpat"
            )["patcher"]
            transient_text = "\n".join(
                item["box"].get("text", "") for item in transient["boxes"]
            )
            self.assertIn("start_level_db", transient_text)

    def test_profile_sound_save_orchestrates_mixer_soundscape_and_eq_without_writing_runtime(self):
        mixer = json.dumps(self.load_json("patchers/module_mixer.maxpat"))
        self.assertIn(
            "route save_profile_sound reload_profile_sound reset_profile_sound",
            mixer,
        )
        for profile in ("ev", "v10", "v12"):
            runtime = json.dumps(
                self.load_json(f"VehicleSoundSynth-{profile.upper()}.maxpat")
            )
            self.assertIn("Save Profile Sound", runtime)
            self.assertIn("Reload Profile Sound", runtime)
            self.assertNotIn('"text": "write"', runtime)
            engine = json.dumps(
                self.load_json(f"patchers/vehicle_engine_{profile}~.maxpat")
            )
            self.assertIn(
                "route save_profile_sound reload_profile_sound reset_profile_sound",
                engine,
            )
            for command in (
                "soundscape_save", "soundscape_reload", "soundscape_reset",
                "eq_save", "eq_reload", "eq_reset",
            ):
                self.assertIn(command, engine)

    def test_v3_demo_exposes_lifecycle_dct_rumble_and_global_eq_controls(self):
        for profile in ("ev", "v10", "v12"):
            engine = self.load_json(f"patchers/vehicle_engine_{profile}~.maxpat")["patcher"]
            text = "\n".join(item["box"].get("text", "") for item in engine["boxes"])
            for token in (
                "ignition", "start", "cabin_rumble", "exhaust_boom",
                "structure_vibration", "eq_low", "eq_lowmid", "eq_highmid",
                "eq_high", "eq_bypass", "master_trim_db",
            ):
                self.assertIn(token, text)
        eq = self.load_json("patchers/vehicle_bus_eq~.maxpat")["patcher"]
        self.assertTrue(any(item["box"]["maxclass"] == "filtergraph~" for item in eq["boxes"]))

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

    def test_project_rebuild_preserves_user_tuned_beap_pad(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            command = [
                sys.executable,
                str(ROOT / "tools" / "build_project.py"),
                "--output-root",
                str(destination),
            ]
            subprocess.run(command, check=True, cwd=ROOT, capture_output=True, text=True)
            pad_path = destination / "patchers" / "ev_pad_beap~.maxpat"
            pad = json.loads(pad_path.read_text(encoding="utf-8"))
            pad["patcher"]["description"] = "user tuning sentinel"
            pad_path.write_text(
                json.dumps(pad, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            tuned_bytes = pad_path.read_bytes()
            subprocess.run(command, check=True, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(tuned_bytes, pad_path.read_bytes())

    def test_project_rebuild_preserves_user_tuned_backfire_beap_voices(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            command = [
                sys.executable,
                str(ROOT / "tools" / "build_project.py"),
                "--output-root", str(destination),
            ]
            subprocess.run(command, check=True, cwd=ROOT, capture_output=True, text=True)
            for profile in ("v10", "v12"):
                voice_path = destination / "patchers" / f"{profile}_backfire_beap~.maxpat"
                voice = json.loads(voice_path.read_text(encoding="utf-8"))
                voice["patcher"]["description"] = f"{profile} user tuning sentinel"
                voice_path.write_text(
                    json.dumps(voice, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                tuned_bytes = voice_path.read_bytes()
                subprocess.run(command, check=True, cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(tuned_bytes, voice_path.read_bytes())

    def test_runtime_probe_builder_creates_self_contained_temp_bundle(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            bundle = base / "bundle"
            local_media = base / "local_media"
            local_media.mkdir()
            for name in ("ferrari_sf90_startup.wav", "ferrari_sf90_idle_body.wav"):
                (local_media / name).write_bytes((ROOT / "media" / "starter_v12.wav").read_bytes())
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "build_runtime_probe.py"),
                    "--bundle-root",
                    str(bundle),
                    "--local-media-dir",
                    str(local_media),
                ],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            for relative_path in (
                "runtime_probe_v12_idle_on.maxpat",
                f"{bundle.name}.maxproj",
                "engine_controller_v12.maxpat",
                "v12_powertrain~.maxpat",
                "cabin_rumble~.maxpat",
                "v12_powertrain.gendsp",
                "drive_model.js",
                "media/starter_v12.wav",
                "presets/vehicle_bus_eq_default.json",
                "presets/ev_soundscape_factory.json",
                "presets/v10_soundscape_factory.json",
                "presets/v12_soundscape_factory.json",
                "media/local/ferrari_sf90_startup.wav",
                "ferrari_sf90_startup.wav",
            ):
                self.assertTrue((bundle / relative_path).is_file(), relative_path)
            self.assertFalse((bundle / "media/local/ferrari_sf90_idle_body.wav").exists())
            self.assertFalse((bundle / "media/engine_texture_065_a.wav").exists())
            with (bundle / "runtime_probe_v12_idle_on.maxpat").open(encoding="utf-8") as handle:
                probe = json.load(handle)
            text = "\n".join(item["box"].get("text", "") for item in probe["patcher"]["boxes"])
            self.assertIn("drive_simulator_v12", text)
            self.assertIn("route rpm", text)
            self.assertIn("switch 2", text)
            self.assertNotIn("engine_running 1", text)
            self.assertNotIn("combustion_gain 1", text)
            self.assertIn("cabin_rumble~", text)
            self.assertIn("cabin_rumble 0.9", text)
            self.assertIn(";\rdsp setdriver NonRealTime", text)
            self.assertIn(";\rdsp sr 48000", text)
            self.assertIn("adstatus sr", text)
            self.assertIn("dsptime~", text)
            self.assertIn("past 4000", text)
            project = json.loads((bundle / f"{bundle.name}.maxproj").read_text(encoding="utf-8"))
            self.assertIn("v12_powertrain~.maxpat", project["contents"]["patchers"])
            self.assertNotIn("vehicle_engine~.maxpat", project["contents"]["patchers"])
            self.assertNotIn("reference_texture~.maxpat", project["contents"]["patchers"])
            self.assertIn("v12_powertrain.gendsp", project["contents"]["code"])
            self.assertIn("drive_model.js", project["contents"]["code"])
            self.assertIn(
                "presets/v12_soundscape_factory.json",
                project["contents"]["data"],
            )
            self.assertIn("media/starter_v12.wav", project["contents"]["media"])
            self.assertIn(
                "media/local/ferrari_sf90_startup.wav",
                project["contents"]["media"],
            )
            bundled_powertrain = json.loads(
                (bundle / "v12_powertrain~.maxpat").read_text(encoding="utf-8")
            )
            bundled_text = "\n".join(
                item["box"].get("text", "")
                for item in bundled_powertrain["patcher"]["boxes"]
            )
            self.assertIn("gen~ @gen v12_powertrain.gendsp", bundled_text)
            self.assertNotIn(ROOT.as_posix(), bundled_text)

            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "build_runtime_probe.py"),
                    "--bundle-root", str(bundle),
                    "--scenario", "high-v12-3500",
                    "--eq-message", "eq_highmid 3800. -15. 1.",
                ],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            eq_probe = json.loads(
                (bundle / "runtime_probe_v12_high-v12-3500_on.maxpat").read_text(
                    encoding="utf-8"
                )
            )
            eq_text = "\n".join(
                item["box"].get("text", "") for item in eq_probe["patcher"]["boxes"]
            )
            self.assertEqual(1, eq_text.count("loadmess eq_highmid"))
            self.assertIn("loadmess eq_highmid 3800. -15. 1.", eq_text)
            self.assertIn("delay 1000", eq_text)
            self.assertIn("3500", eq_text)

            boxes = {
                item["box"]["id"]: item["box"]
                for item in eq_probe["patcher"]["boxes"]
            }
            lines = [
                item["patchline"] for item in eq_probe["patcher"]["lines"]
            ]
            rpm_switch_id = next(
                box_id
                for box_id, box in boxes.items()
                if box.get("text") == "switch 2"
            )
            lock_select_id = next(
                line["source"][0]
                for line in lines
                if line["destination"] == [rpm_switch_id, 0]
                and boxes[line["source"][0]].get("text") == "2"
            )
            lock_value_id = next(
                line["source"][0]
                for line in lines
                if line["destination"] == [rpm_switch_id, 2]
                and boxes[line["source"][0]].get("text") == "3500"
            )
            lock_order_id = next(
                box_id
                for box_id, box in boxes.items()
                if box.get("text") == "t b b b"
                and {line["destination"][0] for line in lines if line["source"][0] == box_id}
                >= {lock_select_id, lock_value_id}
            )
            select_outlet = next(
                line["source"][1]
                for line in lines
                if line["source"][0] == lock_order_id
                and line["destination"][0] == lock_select_id
            )
            value_outlet = next(
                line["source"][1]
                for line in lines
                if line["source"][0] == lock_order_id
                and line["destination"][0] == lock_value_id
            )
            self.assertGreater(select_outlet, value_outlet)

            failed_rate = subprocess.run(
                [
                    sys.executable, str(ROOT / "tools" / "audio_metrics.py"),
                    str(bundle / "media" / "engine_texture_065_a.wav"),
                    "--require-sample-rate", "44100",
                ],
                cwd=ROOT, capture_output=True, text=True,
            )
            self.assertNotEqual(0, failed_rate.returncode)

    def test_v4_reference_texture_covers_full_firing_range(self):
        patcher = self.load_json("patchers/reference_texture~.maxpat")["patcher"]
        text = "\n".join(item["box"].get("text", "") for item in patcher["boxes"])
        self.assertIn("abs(min($f1,650.)-520.)/170.", text)
        self.assertIn("loadmess -18", text)
        self.assertNotIn("loadmess -6", text)

    def test_runtime_buffers_resolve_media_through_project_search_path(self):
        transients = [
            self.load_json(f"patchers/transient_{profile}~.maxpat")["patcher"]
            for profile in ("v10", "v12")
        ]
        reference = self.load_json("patchers/reference_texture~.maxpat")["patcher"]
        buffer_texts = [
            item["box"].get("text", "")
            for patcher in (*transients, reference)
            for item in patcher["boxes"]
            if item["box"].get("text", "").startswith("buffer~ ")
        ]
        self.assertTrue(buffer_texts)
        local_buffers = [text for text in buffer_texts if "ferrari_" in text]
        bundled_buffers = [text for text in buffer_texts if "ferrari_" not in text]
        self.assertEqual(
            {
                "buffer~ ferrari_startup Patcher:/media/local/ferrari_sf90_startup.wav",
                "buffer~ ferrari_idle_body Patcher:/media/local/ferrari_sf90_idle_body.wav",
            },
            set(local_buffers),
        )
        self.assertTrue(all(" Patcher:/media/" in text for text in buffer_texts))

    def test_v4_runtime_probe_exposes_full_acoustic_matrix_and_diagnostic_taps(self):
        source = (ROOT / "tools" / "build_runtime_probe.py").read_text(encoding="utf-8")
        for scenario in (
            "idle-v12", "idle-v10", "high-v12-3500", "high-v10-4200",
            "ev-soundscape-on", "ev-soundscape-off", "ev-soundscape-solo",
            "v10-soundscape-on", "v10-soundscape-off",
            "v12-soundscape-on", "v12-soundscape-off",
            "shift-up", "shift-down", "intake-backfire", "exhaust-pop",
            "v10-backfire-running", "v10-backfire-ignition-off",
            "v12-backfire-running", "v12-backfire-ignition-off",
        ):
            self.assertIn(f'"{scenario}"', source)
        self.assertIn('choices=("transient", "pre-cabin", "final")', source)
        engine = self.load_json("patchers/vehicle_engine~.maxpat")["patcher"]
        text = "\n".join(item["box"].get("text", "") for item in engine["boxes"])
        self.assertIn("send~ vss_pre_cabin_l", text)
        self.assertIn("send~ vss_pre_cabin_r", text)

    def test_audio_metrics_exposes_mid_and_high_stereo_safety_thresholds(self):
        source = (ROOT / "tools" / "audio_metrics.py").read_text(encoding="utf-8")
        for option in (
            "--max-mid-side-ratio", "--min-mid-band-correlation",
            "--max-mid-band-mono-fold-rms-loss-db", "--max-high-side-ratio",
            "--min-high-band-correlation", "--max-high-band-mono-fold-rms-loss-db",
            "--max-harsh-ratio",
            "--expected-fundamental-hz", "--max-spectral-centroid-hz",
            "--max-rolloff-95-hz", "--max-sample-delta-peak-over-rms",
            "--max-upper-harmonic-ratio", "--max-harmonic-slope-db-per-octave",
        ):
            self.assertIn(option, source)

    def test_runtime_probe_can_isolate_ev_motor_with_pad_gate_off(self):
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "tools" / "build_runtime_probe.py"),
                    "--bundle-root",
                    directory,
                    "--profile",
                    "ev",
                    "--rumble",
                    "off",
                    "--start",
                    "off",
                    "--ignition",
                    "off",
                    "--render-ms",
                    "8000",
                ],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            bundle = Path(directory)
            probe_path = bundle / "runtime_probe_ev_idle_off.maxpat"
            self.assertTrue(probe_path.is_file())
            self.assertTrue((bundle / "ev_cinematic_soundscape_host~.maxpat").is_file())
            self.assertFalse((bundle / "cinematic_soundscape_voice.maxpat").exists())
            self.assertTrue((bundle / "cinematic_soundscape_beap~.maxpat").is_file())
            patch = json.loads(probe_path.read_text(encoding="utf-8"))
            text = "\n".join(item["box"].get("text", "") for item in patch["patcher"]["boxes"])
            self.assertIn("engine_controller_ev", text)
            self.assertIn("ev_powertrain~", text)
            self.assertNotIn("engine_type", text)
            self.assertNotIn("ev_weight", text)
            self.assertIn("ignition 0", text)
            self.assertNotIn("start 1", text)

    def test_runtime_probe_can_exercise_backfire_running_state_gate(self):
        for profile in ("v10", "v12"):
            with tempfile.TemporaryDirectory() as directory:
                subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "tools" / "build_runtime_probe.py"),
                        "--bundle-root", directory,
                        "--scenario", f"{profile}-backfire-ignition-off",
                        "--render-ms", "1000",
                    ],
                    check=True,
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                probe_path = Path(directory) / (
                    f"runtime_probe_{profile}_{profile}-backfire-ignition-off_on.maxpat"
                )
                probe = json.loads(probe_path.read_text(encoding="utf-8"))["patcher"]
                text = "\n".join(item["box"].get("text", "") for item in probe["boxes"])
                self.assertIn("ignition 0", text)
                self.assertIn("exhaust_pop 1", text)

                subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "tools" / "build_runtime_probe.py"),
                        "--bundle-root", directory,
                        "--scenario", f"{profile}-backfire-overrun-solo",
                        "--render-ms", "1000",
                    ],
                    check=True,
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                solo_path = Path(directory) / (
                    f"runtime_probe_{profile}_{profile}-backfire-overrun-solo_on.maxpat"
                )
                solo = json.loads(solo_path.read_text(encoding="utf-8"))["patcher"]
                solo_text = "\n".join(
                    item["box"].get("text", "") for item in solo["boxes"]
                )
                self.assertIn("overrun 0.95", solo_text)
                self.assertIn("backfire_enable 1", solo_text)
                self.assertIn("backfire_intensity 1", solo_text)
                self.assertIn("backfire_solo 1", solo_text)
                self.assertIn("past 700", solo_text)
                self.assertNotIn("past 1800", solo_text)

    def test_runtime_probe_can_audition_one_isolated_pop_hit(self):
        for profile in ("v10", "v12"):
            with tempfile.TemporaryDirectory() as directory:
                subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "tools" / "build_runtime_probe.py"),
                        "--bundle-root", directory,
                        "--scenario", f"{profile}-backfire-single-solo",
                        "--render-ms", "1000",
                    ],
                    check=True,
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                probe_path = Path(directory) / (
                    f"runtime_probe_{profile}_{profile}-backfire-single-solo_on.maxpat"
                )
                probe = json.loads(probe_path.read_text(encoding="utf-8"))["patcher"]
                boxes = [item["box"] for item in probe["boxes"]]
                text = "\n".join(box.get("text", "") for box in boxes)
                self.assertIn("backfire_solo 1", text)
                self.assertIn(f"s {profile}.pop.audition_one_hit", text)
                self.assertIn("past 200", text)
                self.assertNotIn("backfire_test 1", text)

    def test_runtime_probe_exposes_low_default_and_high_backfire_intensity(self):
        expected = {
            "v10": {"low": 0.25, "default": 0.82, "high": 1.0},
            "v12": {"low": 0.25, "default": 0.55, "high": 1.0},
        }
        for profile, levels in expected.items():
            for label, intensity in levels.items():
                with self.subTest(profile=profile, label=label):
                    with tempfile.TemporaryDirectory() as directory:
                        subprocess.run(
                            [
                                sys.executable,
                                str(ROOT / "tools" / "build_runtime_probe.py"),
                                "--bundle-root", directory,
                                "--scenario", f"{profile}-backfire-solo-{label}",
                                "--render-ms", "1000",
                            ],
                            check=True,
                            cwd=ROOT,
                            capture_output=True,
                            text=True,
                        )
                        probe_path = Path(directory) / (
                            f"runtime_probe_{profile}_{profile}-backfire-solo-{label}_on.maxpat"
                        )
                        probe = json.loads(probe_path.read_text(encoding="utf-8"))["patcher"]
                        text = "\n".join(
                            item["box"].get("text", "") for item in probe["boxes"]
                        )
                        self.assertIn(f"backfire_intensity {intensity:g}", text)
                        self.assertIn("backfire_solo 1", text)
                        self.assertIn("overrun 0.95", text)

    def test_runtime_probe_exposes_both_auditionable_ice_start_styles(self):
        for profile in ("v10", "v12"):
            for style in ("cinematic", "realistic"):
                with self.subTest(profile=profile, style=style):
                    with tempfile.TemporaryDirectory() as directory:
                        subprocess.run(
                            [
                                sys.executable,
                                str(ROOT / "tools" / "build_runtime_probe.py"),
                                "--bundle-root", directory,
                                "--scenario", f"{profile}-start-{style}",
                                "--tap", "transient",
                                "--render-ms", "1800",
                            ],
                            check=True,
                            cwd=ROOT,
                            capture_output=True,
                            text=True,
                        )
                        probe_path = Path(directory) / (
                            f"runtime_probe_{profile}_{profile}-start-{style}_on.maxpat"
                        )
                        probe = json.loads(probe_path.read_text(encoding="utf-8"))["patcher"]
                        text = "\n".join(
                            item["box"].get("text", "") for item in probe["boxes"]
                        )
                        self.assertIn(f"start_style {style}", text)
                        self.assertIn("starter 1", text)
                        self.assertIn("past 200", text)

    def test_runtime_probe_exercises_controller_owned_start_lifecycle(self):
        for profile in ("v10", "v12"):
            with tempfile.TemporaryDirectory() as directory:
                subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "tools" / "build_runtime_probe.py"),
                        "--bundle-root", directory,
                        "--scenario", f"{profile}-start-controller-cinematic",
                        "--tap", "transient",
                        "--render-ms", "1800",
                    ],
                    check=True,
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                probe_path = Path(directory) / (
                    f"runtime_probe_{profile}_{profile}-start-controller-cinematic_on.maxpat"
                )
                probe = json.loads(probe_path.read_text(encoding="utf-8"))["patcher"]
                text = "\n".join(
                    item["box"].get("text", "") for item in probe["boxes"]
                )
                self.assertIn("start_style cinematic", text)
                self.assertIn("start 1", text)
                self.assertNotIn("starter 1", text)

    def test_runtime_probe_exposes_ignition_independent_backfire_test(self):
        for profile in ("v10", "v12"):
            with tempfile.TemporaryDirectory() as directory:
                subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "tools" / "build_runtime_probe.py"),
                        "--bundle-root", directory,
                        "--scenario", f"{profile}-backfire-test-solo",
                        "--tap", "transient",
                        "--render-ms", "1200",
                    ],
                    check=True,
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                probe_path = Path(directory) / (
                    f"runtime_probe_{profile}_{profile}-backfire-test-solo_on.maxpat"
                )
                probe = json.loads(probe_path.read_text(encoding="utf-8"))["patcher"]
                text = "\n".join(
                    item["box"].get("text", "") for item in probe["boxes"]
                )
                self.assertIn("backfire_test 1", text)
                self.assertIn("backfire_solo 1", text)
                self.assertIn("past 200", text)

    def test_runtime_probe_can_render_ice_soundscape_without_enabling_other_scenarios(self):
        for profile, level in (("v10", -8), ("v12", -9)):
            with tempfile.TemporaryDirectory() as directory:
                subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "tools" / "build_runtime_probe.py"),
                        "--bundle-root", directory,
                        "--scenario", f"{profile}-soundscape-on",
                        "--render-ms", "1000",
                    ],
                    check=True,
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                )
                probe_path = Path(directory) / f"runtime_probe_{profile}_{profile}-soundscape-on_on.maxpat"
                probe = json.loads(probe_path.read_text(encoding="utf-8"))["patcher"]
                text = "\n".join(item["box"].get("text", "") for item in probe["boxes"])
                self.assertIn(f"{profile}_cinematic_soundscape_host~", text)
                self.assertIn(f"soundscape_level_db {level}", text)
                self.assertIn("soundscape_enable 1", text)

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
            self.assertIn(";\rdsp setdriver NonRealTime", text)
            self.assertIn(";\rdsp sr 48000", text)
            self.assertIn("dsptime~", text)

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
            harsh_path = Path(directory) / "harsh.wav"
            write_tone(low_path, 120.0)
            write_tone(high_path, 8000.0)
            write_tone(harsh_path, 3500.0)
            low = analyze(low_path)
            high = analyze(high_path)
            harsh = analyze(harsh_path)
        self.assertGreater(low["low_mid_ratio"], 0.99)
        self.assertGreater(low["rumble_ratio"], 0.99)
        self.assertLess(low["subsonic_ratio"], 0.01)
        self.assertLess(low["high_ratio"], 0.01)
        self.assertGreater(high["high_ratio"], 0.99)
        self.assertGreater(harsh["harsh_ratio"], 0.99)
        self.assertLess(low["harsh_ratio"], 0.01)
        self.assertLess(high["harsh_ratio"], 0.01)

    def test_audio_metrics_distinguish_short_kick_impact_from_snare_attack(self):
        sys.path.insert(0, str(ROOT / "tools"))
        from audio_metrics import analyze

        def write_impact(path, snare):
            sample_rate = 48000
            phase = 0.0
            noise_state = 0x12345678
            payload = []
            for index in range(sample_rate):
                time = index / sample_rate
                elapsed = time - 0.10
                value = 0.0
                if elapsed >= 0.0:
                    if snare:
                        noise_state = (1664525 * noise_state + 1013904223) & 0xFFFFFFFF
                        noise = ((noise_state / 0xFFFFFFFF) * 2.0) - 1.0
                        value = 0.55 * noise * math.exp(-elapsed / 0.11)
                    else:
                        frequency = 56.0 + 72.0 * math.exp(-elapsed / 0.035)
                        phase += 2.0 * math.pi * frequency / sample_rate
                        value = 0.72 * math.sin(phase) * math.exp(-elapsed / 0.075)
                payload.append(struct.pack("<h", round(max(-1.0, min(1.0, value)) * 32767.0)))
            with wave.open(str(path), "wb") as handle:
                handle.setnchannels(1)
                handle.setsampwidth(2)
                handle.setframerate(sample_rate)
                handle.writeframes(b"".join(payload))

        with tempfile.TemporaryDirectory() as directory:
            kick_path = Path(directory) / "kick.wav"
            snare_path = Path(directory) / "snare.wav"
            write_impact(kick_path, False)
            write_impact(snare_path, True)
            kick = analyze(kick_path)
            snare = analyze(snare_path)

        self.assertLess(kick["attack_23ms_centroid_hz"], 250.0)
        self.assertGreater(kick["attack_23ms_low_20_180_ratio"], 0.65)
        self.assertLess(kick["attack_23ms_snare_1200_6000_ratio"], 0.02)
        self.assertLess(kick["impact_tail_20db_ms"], 240.0)
        self.assertGreater(
            snare["attack_23ms_centroid_hz"],
            kick["attack_23ms_centroid_hz"] * 4.0,
        )
        self.assertGreater(
            snare["attack_23ms_snare_1200_6000_ratio"],
            kick["attack_23ms_snare_1200_6000_ratio"] * 10.0,
        )

    def test_audio_metrics_detect_wrap_discontinuity_harmonic_comb(self):
        import math

        sys.path.insert(0, str(ROOT / "tools"))
        from audio_metrics import analyze

        def write_pulse(path, smooth):
            sample_rate = 48000
            frequency = 78.0
            payload = []
            sharpness = 9.8
            exponential_mean = (1.0 - math.exp(-sharpness)) / sharpness
            for index in range(sample_rate):
                phase = (index * frequency / sample_rate) % 1.0
                if smooth:
                    value = (0.5 + 0.5 * math.cos(2.0 * math.pi * phase)) ** 4
                    value -= 70.0 / 256.0
                else:
                    value = math.exp(-phase * sharpness) - exponential_mean
                payload.append(struct.pack("<h", round(value * 0.4 * 32767.0)))
            with wave.open(str(path), "wb") as handle:
                handle.setnchannels(1)
                handle.setsampwidth(2)
                handle.setframerate(sample_rate)
                handle.writeframes(b"".join(payload))

        with tempfile.TemporaryDirectory() as directory:
            saw_path = Path(directory) / "saw.wav"
            smooth_path = Path(directory) / "smooth.wav"
            write_pulse(saw_path, False)
            write_pulse(smooth_path, True)
            saw = analyze(saw_path, expected_fundamental_hz=78.0)
            smooth = analyze(smooth_path, expected_fundamental_hz=78.0)

        self.assertLess(smooth["spectral_centroid_hz"], saw["spectral_centroid_hz"])
        self.assertLess(smooth["spectral_rolloff_95_hz"], saw["spectral_rolloff_95_hz"])
        self.assertLess(
            smooth["sample_delta_peak_over_rms"],
            saw["sample_delta_peak_over_rms"] * 0.2,
        )
        self.assertLess(smooth["upper_harmonic_ratio"], 0.001)
        self.assertGreater(saw["upper_harmonic_ratio"], 0.01)

    def test_audio_metrics_scan_late_render_windows(self):
        import math

        sys.path.insert(0, str(ROOT / "tools"))
        from audio_metrics import analyze

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "late_fault.wav"
            sample_rate = 48000
            payload = []
            for index in range(sample_rate * 2):
                frequency = 80.0 if index < sample_rate else 8000.0
                value = round(
                    0.25
                    * math.sin(2.0 * math.pi * frequency * index / sample_rate)
                    * 32767.0
                )
                payload.append(struct.pack("<h", value))
            with wave.open(str(path), "wb") as handle:
                handle.setnchannels(1)
                handle.setsampwidth(2)
                handle.setframerate(sample_rate)
                handle.writeframes(b"".join(payload))
            metrics = analyze(path)

        self.assertGreater(metrics["high_ratio"], 0.25)
        self.assertGreater(metrics["spectral_centroid_hz"], 2000.0)
        self.assertGreater(metrics["spectral_rolloff_95_hz"], 6000.0)

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
        self.assertGreater(centered["low_band_correlation"], 0.999)
        self.assertLess(side["low_band_correlation"], -0.999)
        self.assertLess(centered["low_band_mono_fold_rms_loss_db"], 0.001)
        self.assertGreater(side["low_band_mono_fold_rms_loss_db"], 60.0)
        self.assertLess(centered["mono_fold_rms_loss_db"], 0.001)
        self.assertGreater(side["mono_fold_rms_loss_db"], 60.0)
        self.assertAlmostEqual(centered["peak_dbfs"], side["peak_dbfs"], places=3)
        self.assertAlmostEqual(centered["rms_dbfs"], side["rms_dbfs"], places=3)

    def test_audio_metrics_compare_third_octaves_and_expected_gain(self):
        import math

        sys.path.insert(0, str(ROOT / "tools"))
        from audio_metrics import analyze, third_octave_similarity

        def write_tones(path, gain, frequencies):
            payload = []
            for index in range(48000):
                value = gain * sum(
                    math.sin(2 * math.pi * frequency * index / 48000)
                    for frequency in frequencies
                ) / len(frequencies)
                sample = round(max(-0.99, min(0.99, value)) * 32767)
                payload.append(struct.pack("<hh", sample, sample))
            with wave.open(str(path), "wb") as handle:
                handle.setnchannels(2)
                handle.setsampwidth(2)
                handle.setframerate(48000)
                handle.writeframes(b"".join(payload))

        with tempfile.TemporaryDirectory() as directory:
            reference = Path(directory) / "reference.wav"
            quieter = Path(directory) / "quieter.wav"
            different = Path(directory) / "different.wav"
            write_tones(reference, 0.4, (80.0, 160.0, 320.0, 640.0))
            write_tones(quieter, 0.2, (80.0, 160.0, 320.0, 640.0))
            write_tones(different, 0.4, (2000.0, 4000.0, 8000.0))
            reference_metrics = analyze(reference)
            quiet_metrics = analyze(quieter)
            similarity = third_octave_similarity(reference, quieter)
            dissimilarity = third_octave_similarity(reference, different)
        self.assertAlmostEqual(-6.0206, quiet_metrics["rms_dbfs"] - reference_metrics["rms_dbfs"], delta=0.02)
        self.assertGreater(similarity, 0.999)
        self.assertLess(dissimilarity, 0.10)

    def test_v4_audio_metrics_compare_left_right_and_mid_profiles(self):
        import math

        sys.path.insert(0, str(ROOT / "tools"))
        from audio_metrics import third_octave_similarities

        def write_stereo(path, left_frequencies, right_frequencies):
            payload = []
            for index in range(48000):
                left = 0.35 * sum(
                    math.sin(2 * math.pi * frequency * index / 48000)
                    for frequency in left_frequencies
                ) / len(left_frequencies)
                right = 0.35 * sum(
                    math.sin(2 * math.pi * frequency * index / 48000)
                    for frequency in right_frequencies
                ) / len(right_frequencies)
                payload.append(struct.pack("<hh", round(left * 32767), round(right * 32767)))
            with wave.open(str(path), "wb") as handle:
                handle.setnchannels(2)
                handle.setsampwidth(2)
                handle.setframerate(48000)
                handle.writeframes(b"".join(payload))

        with tempfile.TemporaryDirectory() as directory:
            reference = Path(directory) / "reference.wav"
            matching = Path(directory) / "matching.wav"
            swapped = Path(directory) / "swapped.wav"
            write_stereo(reference, (80.0, 320.0), (160.0, 640.0))
            write_stereo(matching, (80.0, 320.0), (160.0, 640.0))
            write_stereo(swapped, (160.0, 640.0), (80.0, 320.0))
            exact = third_octave_similarities(reference, matching)
            channel_wrong = third_octave_similarities(reference, swapped)

        self.assertGreater(exact["left"], 0.999)
        self.assertGreater(exact["right"], 0.999)
        self.assertGreater(exact["mid"], 0.999)
        self.assertLess(channel_wrong["left"], 0.2)
        self.assertLess(channel_wrong["right"], 0.2)
        self.assertGreater(channel_wrong["mid"], 0.999)

    def test_v4_audio_metrics_report_right_channel_delay(self):
        import math

        sys.path.insert(0, str(ROOT / "tools"))
        from audio_metrics import stereo_delay_ms

        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "delayed.wav"
            delay = 12
            signal = [
                0.45 * math.sin(2 * math.pi * 313.0 * index / 48000)
                + 0.2 * math.sin(2 * math.pi * 877.0 * index / 48000)
                for index in range(12000)
            ]
            right = [0.0] * delay + signal[:-delay]
            with wave.open(str(target), "wb") as handle:
                handle.setnchannels(2)
                handle.setsampwidth(2)
                handle.setframerate(48000)
                handle.writeframes(b"".join(
                    struct.pack("<hh", round(left * 32767), round(r * 32767))
                    for left, r in zip(signal, right)
                ))
            measured = stereo_delay_ms(target)
        self.assertAlmostEqual(0.25, measured, delta=0.03)

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

    def test_audio_metrics_detect_slow_amplitude_beating(self):
        import math

        sys.path.insert(0, str(ROOT / "tools"))
        from audio_metrics import analyze

        def write_modulated_tone(path, modulation_depth):
            payload = []
            sample_rate = 48000
            for index in range(sample_rate * 4):
                time = index / sample_rate
                envelope = 1.0 - modulation_depth + modulation_depth * (
                    0.5 + 0.5 * math.sin(2 * math.pi * 0.62 * time)
                )
                value = 0.25 * envelope * math.sin(2 * math.pi * 88.8 * time)
                payload.append(struct.pack("<h", round(value * 32767)))
            with wave.open(str(path), "wb") as handle:
                handle.setnchannels(1)
                handle.setsampwidth(2)
                handle.setframerate(sample_rate)
                handle.writeframes(b"".join(payload))

        with tempfile.TemporaryDirectory() as directory:
            stable_path = Path(directory) / "stable.wav"
            beating_path = Path(directory) / "beating.wav"
            write_modulated_tone(stable_path, 0.0)
            write_modulated_tone(beating_path, 0.9)
            stable = analyze(stable_path)
            beating = analyze(beating_path)
        self.assertLess(stable["envelope_spread_db"], 0.2)
        self.assertGreater(beating["envelope_spread_db"], 10.0)
        self.assertLess(stable["modulation_peak_ratio_0_5_20_hz"], 0.10)
        self.assertAlmostEqual(0.62, beating["modulation_peak_hz"], delta=0.15)
        self.assertGreater(beating["modulation_peak_ratio_0_5_20_hz"], 0.25)
        self.assertGreater(beating["envelope_autocorrelation_peak"], 0.80)

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

    def test_local_reference_analysis_and_startup_are_hash_documented_but_never_distributed(self):
        manifest = self.load_json("assets/asset_manifest.json")
        references = manifest["local_only_references"]
        self.assertEqual(1, len(references))
        reference = references[0]
        self.assertIn("do not commit", reference["distribution"])
        self.assertRegex(reference["source_sha256"], r"^[0-9a-f]{64}$")
        self.assertEqual({
            "idle_residual", "high_rpm_residual", "v10_startup", "v10_idle_body"
        }, {
            output["role"] for output in reference["derived_outputs"]
        })
        for output in reference["derived_outputs"]:
            self.assertRegex(output["sha256"], r"^[0-9a-f]{64}$")
            if output["role"] == "v10_startup":
                self.assertIn("one-shot", output["runtime_usage"])
            else:
                self.assertEqual("analysis-only", output["runtime_usage"])
        self.assertIn("analysis-only", reference["usage"])
        self.assertEqual(["v10"], reference["comparison_profiles"])
        self.assertRegex(reference["processor_sha256"], r"^[0-9a-f]{64}$")
        atlas_record = reference["v10_state_atlas"]
        self.assertEqual(18, atlas_record["output_count"])
        self.assertRegex(atlas_record["manifest_sha256"], r"^[0-9a-f]{64}$")
        self.assertIn("never loaded", atlas_record["role"])
        target_record = reference["lifecycle_target_table"]
        target_path = ROOT / target_record["path"]
        self.assertEqual(
            target_record["sha256"], hashlib.sha256(target_path.read_bytes()).hexdigest()
        )
        self.assertEqual(14, target_record["node_count"])
        self.assertIn("media/local/", (ROOT / ".gitignore").read_text(encoding="utf-8"))
        for output in reference["derived_outputs"]:
            derived = ROOT / output["path"]
            if derived.is_file():
                self.assertEqual(output["sha256"], hashlib.sha256(derived.read_bytes()).hexdigest())
        atlas_path = ROOT / atlas_record["manifest_path"]
        if atlas_path.is_file():
            self.assertEqual(
                atlas_record["manifest_sha256"],
                hashlib.sha256(atlas_path.read_bytes()).hexdigest(),
            )
            atlas = json.loads(atlas_path.read_text(encoding="utf-8"))
            outputs = [item for items in atlas["states"].values() for item in items]
            self.assertEqual(18, len(outputs))
            for item in outputs:
                path = atlas_path.parent / item["file"]
                self.assertTrue(path.is_file())
                self.assertEqual(item["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())

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
