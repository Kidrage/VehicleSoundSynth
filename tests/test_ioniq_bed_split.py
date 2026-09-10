"""IONIQ A-only split: preserve accepted tones, RPM texture, and spatial state."""
import json
import subprocess
import unittest
from pathlib import Path
from tools import build_project as build

ROOT = Path(__file__).resolve().parents[1]


class IoniqBedSplitTests(unittest.TestCase):
    def test_v2_only_disconnects_the_standalone_speed_transient_noise_return(self):
        for mode, spec in build.IONIQ6N_SOUNDSCAPE_MODES.items():
            old = build.make_ioniq6n_soundscape_beap(mode)['patcher']
            new = build.make_ioniq6n_soundscape_beap(mode, version=2)['patcher']
            self.assertEqual(new['boxes'][:len(old['boxes'])], old['boxes'])
            mixer = next(item['box']['id'] for item in old['boxes'] if item['box'].get('varname') == spec['modules']['mixer'])
            removed = [item for item in old['lines'] if item not in new['lines']]
            self.assertEqual(len(removed), 1)
            self.assertEqual(removed[0]['patchline']['destination'], [mixer, 3])
            self.assertEqual(len(new['lines']), len(old['lines']) - 1)
        self.assertEqual(build.make_ioniq6n_soundscape_factory(), json.loads((ROOT/'presets/ioniq6n_soundscape_modes_factory.json').read_text()))
        old = build.make_ioniq6n_soundscape_factory()['pattrstorage']['slots']['99']['data']
        new = build.make_ioniq6n_soundscape_factory(version=2)['pattrstorage']['slots']['99']['data']
        renamed = {key.replace('_beap~::', '_bed_v2_beap~::'): value for key,value in old.items()}
        self.assertEqual(new, renamed)

    def test_live_host_opens_v2_and_designer_actions_reach_the_same_state(self):
        patch = build.make_ioniq6n_soundscape_host()['patcher']
        boxes = {item['box']['id']: item['box'] for item in patch['boxes']}
        state = next(key for key,value in boxes.items() if value.get('text') == 'js Patcher:/code/ioniq6n_bed_state.js')
        edges = {}
        for item in patch['lines']:
            line = item['patchline']
            edges.setdefault(line['source'][0], []).append(line['destination'][0])
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
        for mode in build.IONIQ6N_SOUNDSCAPE_MODES:
            voice = next(key for key,value in boxes.items() if value.get('text') == f'ioniq6n_soundscape_{mode}_bed_v2_beap~')
            self.assertTrue(any(item['patchline']['source'] == [voice,2] for item in patch['lines']))
            self.assertTrue(reaches(voice, state), 'Designer Save must address the sounding instance')

    def test_full_old_slot_migrates_without_retuning_or_writing_the_original(self):
        source = r"""
const fs=require('fs'),vm=require('vm');
const script=fs.readFileSync(process.argv[1],'utf8');
const data={n_sound_mode_state:['lightspeed'],soundscape_space_state:[.91],
 'ioniq6n_soundscape_ignition_beap~::Ignition_Space::Decay':[38],
 'ioniq6n_soundscape_evolution_beap~::Evolution_Harmonics::Offset':[.12],
 'ioniq6n_soundscape_lightspeed_beap~::Lightspeed_Layer_Mixer::in3':[-8.5]};
const previous={pattrstorage:{slots:{'1':{data}}}};
const frozen=JSON.stringify(previous), messages=[],tasks=[];
const files={'/project/presets/local/ioniq6n_soundscape_modes.json':JSON.stringify(previous),
 '/project/presets/ioniq6n_soundscape_modes_v2_factory.json':'{}'};
const context={patcher:{filepath:'/project/patchers/host.maxpat'},post:()=>{},
 outlet:(...args)=>messages.push(args),File:function(path){this.isopen=path in files;this.position=0;this.eof=(files[path]||'').length;this.close=()=>{};this.readstring=()=>{this.position=this.eof;return files[path]||'';};},
 Task:function(fn,owner){this.cancelled=false;this.cancel=()=>this.cancelled=true;this.schedule=()=>tasks.push(()=>{if(!this.cancelled)fn.call(owner);});}
};
vm.createContext(context);vm.runInContext(script,context);
const migrated=context.migrateModeData(previous);
if(JSON.stringify(previous)!==frozen)throw Error('mutated old data');
if(migrated['ioniq6n_soundscape_ignition_bed_v2_beap~::Ignition_Space::Decay'][0]!==38)throw Error('FX setting lost');
if(migrated['ioniq6n_soundscape_evolution_bed_v2_beap~::Evolution_Harmonics::Offset'][0]!==.12)throw Error('tone changed');
if(Object.keys(migrated).length!==Object.keys(data).length)throw Error('partial migration');
context.ready();while(tasks.length)tasks.shift()();messages.length=0;
context.restore();while(tasks.length)tasks.shift()();
if(!messages.some(m=>m[1]==='setstoredvalue'&&m[2]==='soundscape_space_state'&&m[4]===.91))throw Error('overlay not applied');
if(!messages.some(m=>m[1]==='write'&&m[2]==='/project/presets/local/ioniq6n_soundscape_modes_v2.json'))throw Error('migration not saved');
if(messages.some(m=>m[1]==='write'&&m[2]==='/project/presets/local/ioniq6n_soundscape_modes.json'))throw Error('old preset overwritten');
messages.length=0;context.reset();while(tasks.length)tasks.shift()();
if(!messages.some(m=>m[0]===0&&m[1]===99))throw Error('factory not recalled');
if(!messages.some(m=>m[1]==='write'))throw Error('reset does not persist across reopen');
"""
        result = subprocess.run(['node','-e',source,str(ROOT/'code/ioniq6n_bed_state.js')],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)


if __name__ == '__main__':
    unittest.main()
