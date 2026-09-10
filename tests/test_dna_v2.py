"""V10/V12 running DNA keeps the proven idle and a complete control seam."""
import unittest
import subprocess
from pathlib import Path

from tools import build_project as build
from tools import ice_dna_v2


class IceDnaV2Tests(unittest.TestCase):
    def test_state_upgrade_reads_old_values_once_but_never_writes_old_state(self):
        script = r'''
const fs = require('fs'), vm = require('vm');
const emitted = [], files = {};
const oldPath = '/project/presets/local/v10_sound_dna.json';
const newPath = '/project/presets/local/v10_sound_dna_v2.json';
files[oldPath] = JSON.stringify({pattrstorage: {slots: {'1': {data: {
    dna_body: [0.5], dna_air_detail: [0.61], dna_idle_level: [0.01], dna_idle_air: [0.99]
}}}}});
const context = {jsarguments: ['dna_v2_state_path.js', 'v10'],
    patcher: {filepath: '/project/patchers/v10_sound_dna_v2~.maxpat'},
    outlet: (...x) => emitted.push(x), post: () => {},
    File: function(path) {this.isopen = !!files[path]; this.position = 0;
        this.eof = String(files[path] || '').length; this.close = () => {};
        this.readline = () => {this.position = this.eof; return files[path];};}};
vm.createContext(context); vm.runInContext(fs.readFileSync(process.argv[1], 'utf8'), context);
context.restore();
if(JSON.stringify(emitted) !== JSON.stringify([[0, 'store', 1],
    [0, 'setstoredvalue', 'dna_body', 1, 0.5], [0, 'setstoredvalue', 'dna_air_detail', 1, 0.61]]))
    throw Error('audible values not migrated or previously dead idle knobs changed accepted idle');
context.save();
if(JSON.stringify(emitted.pop()) !== JSON.stringify([0, 'write', newPath])) throw Error('old state overwritten');
files[newPath] = true; context.restore();
if(JSON.stringify(emitted.pop()) !== JSON.stringify([0, 'read', newPath])) throw Error('V2 state not authoritative');
delete files[newPath]; delete files[oldPath]; emitted.length = 0; context.restore();
if(emitted.length) throw Error('missing local state should retain initialized defaults silently');
context.patcher.filepath = '/project/VehicleSoundSynth-V10.maxpat'; context.save();
if(JSON.stringify(emitted.pop()) !== JSON.stringify([0, 'write', newPath])) throw Error('embedded panel path escaped project');
'''
        path = Path(__file__).resolve().parents[1] / "code/dna_v2_state_path.js"
        result = subprocess.run(["node", "-e", script, str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_idle_program_is_preserved_and_running_upgrade_fades_in_smoothly(self):
        for profile in ("v10", "v12"):
            original = build.GEN_CODE[f"{profile}_powertrain"]
            upgraded = ice_dna_v2.make_running_gen(profile, original)
            # The entire original state/cadence and idle calculation remains;
            # no alternate oscillator, knob mapping or smoothing replaces it.
            retained = upgraded.split("// V2 RUNNING START")[0]
            retained = retained.split("// V2 PARAMETERS END\n", 1)[1]
            self.assertEqual(retained, original.split("out1 =")[0])
            self.assertIn("out1 = legacy_l + v2_blend * (v2_out_l - legacy_l);", upgraded)
            for rpm in (0, 740, 780, 1100, 1200, 2100, 3000, 6500):
                scope = {"r": rpm, "clamp": lambda x, lo, hi: min(max(x, lo), hi)}
                for line in upgraded.splitlines():
                    if line.startswith(("v2_progress =", "v2_blend =")):
                        name, expression = line.rstrip(";").split(" = ", 1)
                        scope[name] = eval(expression, {"__builtins__": {}}, scope)
                expected = 0 if rpm <= 1200 else 1 if rpm >= 3000 else 0.5
                self.assertEqual(scope["v2_blend"], expected)

    def test_versioned_adapter_routes_every_visible_macro_to_its_own_gen(self):
        for profile in ("v10", "v12"):
            with self.subTest(profile=profile):
                panel = build.make_sound_dna(profile, version=2)["patcher"]
                adapter = build.make_profile_powertrain(profile, version=2)["patcher"]
                texts = [item["box"].get("text", "") for item in adapter["boxes"]]
                routed = next(text for text in texts if text.startswith("route ")).split()[1:]
                knobs = [item["box"]["varname"][4:] for item in panel["boxes"]
                         if item["box"].get("varname", "").startswith("dna_")]
                self.assertTrue(set(knobs).issubset(routed), set(knobs) - set(routed))
                self.assertIn("running_body", knobs)
                self.assertIn(f"gen~ @gen ../gen/{profile}_powertrain_v2.gendsp", texts)
                self.assertEqual(sum(text.startswith("gen~") for text in texts), 1)
                boxes = {item["box"]["id"]: item["box"] for item in adapter["boxes"]}
                route_id = next(key for key, box in boxes.items() if box.get("text", "").startswith("route "))
                gen_id = next(key for key, box in boxes.items() if box.get("text", "").startswith("gen~"))
                lines = [item["patchline"] for item in adapter["lines"]]
                for knob in knobs:
                    pending = [tuple(line["destination"]) for line in lines
                               if line["source"] == [route_id, routed.index(knob)]]
                    seen = set()
                    while pending:
                        node, _port = pending.pop()
                        if node in seen:
                            continue
                        seen.add(node)
                        pending.extend(tuple(line["destination"]) for line in lines if line["source"][0] == node)
                    self.assertIn(gen_id, seen, f"{profile} {knob} is a dead visible control")
                panel_texts = [item["box"].get("text", "") for item in panel["boxes"]]
                self.assertIn(f"{profile}_powertrain_v2~", panel_texts)
                self.assertIn(f"js Patcher:/code/dna_v2_state_path.js {profile}", panel_texts)


if __name__ == "__main__":
    unittest.main()
