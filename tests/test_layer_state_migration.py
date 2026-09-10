import json
import subprocess
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class LayerStateTests(unittest.TestCase):
    def test_noise_upgrade_mutes_only_new_noise_and_preserves_old_file_values(self):
        result=subprocess.run(['node','-e',r'''
const {migrateNoiseDefault}=require('./code/module_mixer_state_path.js');
const d={pattrstorage:{slots:{'1':{data:{mix_road_level_db:[440],mix_powertrain_level_db:[570],mix_master_trim_db:[160]}}}}};
const out=migrateNoiseDefault(d);
if(d.pattrstorage.slots['1'].data.mix_road_level_db[0]!==440)throw Error('mutated legacy');
if(out.pattrstorage.slots['1'].data.mix_road_level_db[0]!==0)throw Error('noise not muted');
if(out.pattrstorage.slots['1'].data.mix_powertrain_level_db[0]!==570 || out.pattrstorage.slots['1'].data.mix_master_trim_db[0]!==160)throw Error('other stems changed');
'''],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_bed_migration_preserves_all_spatial_parameters_only(self):
        from tools import build_project as b
        for profile in ('ev','v10','v12'):
            data=b.make_soundscape_factory(profile,version=4)['pattrstorage']['slots']['99']['data']
            result=subprocess.run(['node','-e',r'''
const {spatialMigration}=require('./code/soundscape_bed_state.js');
const d=JSON.parse(process.argv[1]);
console.log(JSON.stringify(spatialMigration({pattrstorage:{slots:{'1':{data:d}}}})));
''',json.dumps(data)],cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            output=json.loads(result.stdout)
            for key,value in data.items():
                if any('::'+b.SOUNDSCAPE_V4_MODULES[profile][part]+'::' in key for part in ('chorus','reverb')):
                    self.assertEqual(output[key.replace('_v4_beap','_v5_beap')],value)
            self.assertFalse(any('::Freq' in k or '::in1' in k for k in output))
