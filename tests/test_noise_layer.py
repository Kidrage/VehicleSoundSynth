"""The replacement Noise stem is independent, lifecycle-safe and user-tunable."""
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class NoiseLayerTests(unittest.TestCase):
    def run_node(self, source):
        result = subprocess.run(
            ["node", "-e", source, str(ROOT / "code/noise_control.js")],
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_default_stem_is_exactly_silent_and_requires_running_lifecycle(self):
        self.run_node(r"""
const {NoiseControl} = require(process.argv[1]);
const output = {};
const c = new NoiseControl('ferrari', (name, value) => output[name] = value);
const send = (name, value) => c.handle(name, [value]);
c.update();
if (output.stem !== 0 || output.active !== 0) throw Error('unsafe boot');
send('ignition', 1); send('engine_running', 1); send('rpm', 3000);
if (output.stem !== 0) throw Error('-60 dB is not exact mute');
send('road_level_db', -12);
if (!(output.stem > 0 && output.active === 1)) throw Error('fader disconnected');
send('ignition', 0);
if (output.active !== 0) throw Error('off-state hiss');
send('ignition', 1); send('engine_running', 0);
if (output.active !== 0) throw Error('starter leaks noise');
""")

    def test_rpm_moves_mechanics_speed_moves_road_and_every_component_can_mute(self):
        self.run_node(r"""
const {NoiseControl} = require(process.argv[1]);
for (const profile of ['ev', 'v10', 'v12', 'ioniq6n', 'ferrari']) {
  const out = {};
  const c = new NoiseControl(profile, (n,v) => out[n]=v);
  const send = (n,v) => c.handle(n,[v]);
  send('rpm',800); send('load',.5); send('speed_kph',0);
  const low = {...out};
  send('rpm',6000);
  if (!(out.mechanical_hz > low.mechanical_hz && out.cadence > low.cadence)) throw Error('fixed noise spectrum');
  if (out.tire !== 0 || out.air !== 0) throw Error('road noise when parked');
  const cadence=out.cadence, mechanical=out.mechanical_hz;
  send('speed_kph',120);
  if (!(out.tire > 0 && out.air > 0)) throw Error('speed does not drive road');
  if (out.cadence !== cadence || out.mechanical_hz !== mechanical) throw Error('speed owns shaft frequency');
  send('throttle',1);
  if (out.cadence !== cadence) throw Error('throttle pitch shift');
  for (const name of ['mechanical','intake','tire','air']) {
    send('noise_'+name+'_db',-60);
    if (out[name] !== 0) throw Error(name+' mute disconnected');
    send('noise_'+name+'_db',0);
    if (!(out[name] > 0)) throw Error(name+' gain disconnected');
  }
  const old=out.intake_hz;
  send('noise_color',1);
  if (!(out.intake_hz > old)) throw Error('color disconnected');
  const saved=JSON.stringify(out);
  send('soundscape_enable',0); send('soundscape_solo',1);
  if (JSON.stringify(out) !== saved) throw Error('Noise depends on SC');
}
""")

    def test_generated_designer_has_independent_lifecycle_and_real_audio_controls(self):
        from tools.noise_layer import make_vehicle_noise, make_vehicle_noise_factory
        for profile in ('ev', 'v10', 'v12', 'ioniq6n', 'ferrari'):
            patch = make_vehicle_noise(profile)['patcher']
            boxes = {item['box']['id']: item['box'] for item in patch['boxes']}
            edges = {}
            for item in patch['lines']:
                wire = item['patchline']
                edges.setdefault(wire['source'][0], []).append(wire['destination'][0])
                self.assertLess(wire['source'][1], boxes[wire['source'][0]]['numoutlets'])
                self.assertLess(wire['destination'][1], boxes[wire['destination'][0]]['numinlets'])
            outputs = [key for key, value in boxes.items() if value['maxclass'] == 'outlet']
            self.assertEqual(len(outputs), 2)
            def reaches(start, end):
                todo, seen = [start], set()
                while todo:
                    key = todo.pop()
                    if key == end:
                        return True
                    if key not in seen:
                        seen.add(key)
                        todo.extend(edges.get(key, []))
                return False
            for name in ('noise_mechanical_db', 'noise_intake_db', 'noise_tire_db', 'noise_air_db', 'noise_color'):
                source = next(key for key, value in boxes.items() if value.get('varname') == name)
                self.assertTrue(all(reaches(source, target) for target in outputs), name)
            texts = [value.get('text', '') for value in boxes.values()]
            self.assertIn(f'r open.{profile}.noise', texts)
            self.assertIn(f's vss.runtime.control.{profile}', texts)
            self.assertNotIn(f's vss.{profile}.input', texts)
            self.assertNotIn('soundscape_enable', ' '.join(texts))
            self.assertFalse(any('Reverb' in text or 'Chorus' in text for text in texts))
            factory = make_vehicle_noise_factory(profile)['pattrstorage']['slots']['99']['data']
            self.assertNotIn('road_level_db', factory, 'Module Mixer is the only stem gain authority')
            self.assertEqual(factory['noise_color'], [0.35])

    def test_noise_designer_solo_bypasses_manual_external_and_held_driving_gates(self):
        from tools import build_project as builder
        from tools.noise_layer import make_vehicle_noise
        from tests.test_runtime_design_routing import destinations
        for profile in ('ev', 'v10', 'v12', 'ioniq6n', 'ferrari'):
            patch = make_vehicle_noise(profile)['patcher']
            texts = [item['box'].get('text', '') for item in patch['boxes']]
            self.assertIn(f's vss.runtime.control.{profile}', texts)
            # The routing model rejects every stateful drive switch/gate;
            # a successful path must reach the engine through design routing.
            self.assertEqual([(f'vehicle_engine_{profile}~', 'noise_solo')],
                             destinations(profile, 'noise_solo', builder.make_profile_runtime_host(profile)['patcher']))

    def test_save_reload_reset_are_versioned_and_do_not_write_the_mixer(self):
        script = r"""
const fs=require('fs'), vm=require('vm');
const source=fs.readFileSync(process.argv[1],'utf8');
for (const profile of ['ev','v10','v12','ioniq6n','ferrari']) {
  const messages=[], tasks=[], files=new Set();
  const context={jsarguments:['noise_state.js',profile],patcher:{filepath:'/project/patchers/noise.maxpat'},
    outlet:(...args)=>messages.push(args),
    File:function(path){this.isopen=files.has(path);this.close=()=>{};},
    Task:function(fn,owner){this.schedule=()=>tasks.push(()=>fn.call(owner));this.cancel=()=>{};}
  };
  vm.createContext(context);vm.runInContext(source,context);
  const local='/project/presets/local/'+profile+'_noise_v1.json';
  const factory='/project/presets/'+profile+'_noise_v1_factory.json';
  files.add(factory);context.restore();tasks.shift()();
  if(JSON.stringify(messages)!==JSON.stringify([[0,'read',factory],[0,99]])) throw Error('factory fallback');
  messages.length=0;files.add(local);context.restore();tasks.shift()();
  if(JSON.stringify(messages)!==JSON.stringify([[0,'read',local],[0,1]])) throw Error('local reopen');
  messages.length=0;context.save();
  if(JSON.stringify(messages)!==JSON.stringify([[0,'store',1],[0,'delete',99],[0,'write',local]])) throw Error('save path');
  messages.length=0;context.reset();tasks.shift()();
  if(JSON.stringify(messages)!==JSON.stringify([[0,'read',factory],[0,99],[0,'store',1],[0,'delete',99],[0,'write',local]])) throw Error('persistent factory reset');
}
"""
        result = subprocess.run(['node', '-e', script, str(ROOT / 'code/noise_state.js')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_new_state_namespaces_never_autosave_to_the_last_read_factory(self):
        from tools import build_project as builder
        from tools.noise_layer import make_vehicle_noise
        documents = [make_vehicle_noise(profile) for profile in ('ev', 'v10', 'v12', 'ioniq6n', 'ferrari')]
        documents += [builder.make_cinematic_soundscape_host(profile) for profile in ('ev', 'v10', 'v12', 'ferrari')]
        documents.append(builder.make_ioniq6n_soundscape_host())
        documents += [builder.make_sound_dna(profile, version=2) for profile in ('v10', 'v12')]
        for document in documents:
            boxes = [item['box'] for item in document['patcher']['boxes']]
            texts = [box.get('text', '') for box in boxes]
            storage = next(text for text in texts if text.startswith('pattrstorage '))
            # read(factory) sets Max's last-used filename. Mode 3 could silently
            # overwrite that tracked resource on close; only helper writes are allowed.
            self.assertIn('@savemode 0', storage, storage)
            self.assertIn('save', texts)
            self.assertIn('restore', texts)
        # This safeguard is deliberately limited to the new state namespaces.
        for profile in ('ev', 'v10', 'v12', 'ioniq6n', 'ferrari'):
            old = builder.make_sound_dna(profile)['patcher']
            storage = next(item['box']['text'] for item in old['boxes']
                           if item['box'].get('text', '').startswith('pattrstorage '))
            self.assertIn('@savemode 3', storage)

    def test_official_probe_uses_current_noise_and_ice_running_dna(self):
        from tools.build_runtime_probe import make_probe
        for profile in ('v10', 'v12'):
            patch = make_probe(Path('/probe/test.wav'), profile, direct_powertrain=True)['patcher']
            texts = [item['box'].get('text', '') for item in patch['boxes']]
            self.assertIn(f'{profile}_powertrain_v2~', texts)
            self.assertIn(f'vehicle_noise_{profile}~', texts)
            self.assertNotIn('road_air~', texts)
            self.assertIn('loadmess road_level_db -60', texts)
            for name in ('idle_level', 'idle_body', 'idle_metal', 'idle_irregularity', 'idle_air', 'idle_width', 'running_body'):
                self.assertTrue(any(text.startswith(f'loadmess {name} ') for text in texts), name)

    def test_probe_bundle_resolves_nested_resources_and_live_poly_dependencies(self):
        from tools.build_runtime_probe import rewrite_probe_resources, probe_patcher_dependencies
        with tempfile.TemporaryDirectory(prefix='vss probe ') as directory:
            bundle = Path(directory)
            nested = {'patcher': {'boxes': [{'box': {
                'maxclass': 'newobj', 'text': 'p nested', 'patcher': {'boxes': [
                    {'box': {'maxclass': 'newobj', 'text': 'js Patcher:/code/noise_control.js v10'}},
                    {'box': {'maxclass': 'message', 'text': 'replace Patcher:/media/ferrari_pop_v3.wav'}},
                    {'box': {'maxclass': 'newobj', 'text': 'gen~ @gen ../gen/v10_powertrain_v2.gendsp'}},
                    {'box': {'maxclass': 'newobj', 'text': 'poly~ ferrari_pop_sample_voice~ 2 @args example'}},
                ]}
            }}]}}
            rewrite_probe_resources(nested, ROOT, bundle)
            texts = [item['box']['text'] for item in nested['patcher']['boxes'][0]['box']['patcher']['boxes']]
            self.assertEqual(texts[0], f'js "{bundle}/noise_control.js" v10')
            self.assertEqual(texts[1], f'replace "{bundle}/media/ferrari_pop_v3.wav"')
            self.assertEqual(texts[2], f'gen~ @gen "{bundle}/v10_powertrain_v2.gendsp"')
            (bundle/'probe.maxpat').write_text(json.dumps(nested))
            (bundle/'ferrari_pop_sample_voice~.maxpat').write_text(json.dumps({'patcher': {'boxes': []}}))
            (bundle/'inactive_legacy.maxpat').write_text(json.dumps({'patcher': {'boxes': []}}))
            self.assertEqual(probe_patcher_dependencies(bundle, {'probe.maxpat'}), {'probe.maxpat', 'ferrari_pop_sample_voice~.maxpat'})


if __name__ == "__main__":
    unittest.main()
