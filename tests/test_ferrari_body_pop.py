"""Ferrari-only acoustic changes; public stem and event boundaries stay fixed."""
import json
import subprocess
import hashlib
import wave
import array
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FerrariBodyPopTests(unittest.TestCase):
    def test_one_short_mono_pop_matches_provenance_and_has_safe_edges(self):
        path = ROOT/'media/ferrari_pop_v3.wav'
        manifest = json.loads((ROOT/'assets/asset_manifest.json').read_text())
        entry = next(output for asset in manifest['assets'] for output in asset.get('outputs', []) if output['path'] == 'media/ferrari_pop_v3.wav')
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), entry['processed_sha256'])
        with wave.open(str(path)) as handle:
            self.assertEqual((handle.getnchannels(), handle.getsampwidth(), handle.getframerate(), handle.getnframes()), (1,2,48000,11520))
            samples = array.array('h',handle.readframes(handle.getnframes()))
        self.assertEqual(samples[0], 0)
        self.assertEqual(samples[-1], 0)
        self.assertLess(abs(sum(samples)/len(samples)), 1.)
        self.assertLessEqual(max(map(abs,samples)), 16424)
        rms=math.sqrt(sum(x*x for x in samples)/len(samples))
        self.assertGreater(20*math.log10(max(map(abs,samples))/rms), 8.)

    def test_live_pop_has_two_players_and_no_legacy_synthesis_layer(self):
        host = (ROOT/'patchers/ferrari_backfire_host~.maxpat').read_text()
        self.assertIn('ferrari_pop_v3~',host)
        self.assertNotIn('ferrari_backfire_v2_beap~',host)
        p=json.loads((ROOT/'patchers/ferrari_pop_v3~.maxpat').read_text())['patcher']
        texts=[x['box'].get('text','') for x in p['boxes']]
        self.assertEqual(len([x for x in texts if x.startswith('buffer~ ')]),1)
        self.assertIn('replace Patcher:/media/ferrari_pop_v3.wav', texts)
        self.assertEqual(len([x for x in texts if x.startswith('poly~ ferrari_pop_sample_voice~ 2 ')]),1)
        for forbidden in ('noise~','cycle~','tanh~','bp.Reverb'):
            self.assertFalse(any(forbidden in x for x in texts))
        voice=(ROOT/'patchers/ferrari_pop_sample_voice~.maxpat').read_text()
        self.assertIn('thispoly~',voice)
        self.assertIn('loadmess mute 1',voice)

    def test_pop_preserves_physical_events_preview_and_cancellation(self):
        script = r'''
const {PopControl} = require(process.argv[1]);
const output = [];
const c = new PopControl((port, msg) => output.push([port, msg]));
const send = (key, ...args) => c.handle(key, args);
send('pop', 1);
if(output.length) throw Error('engine-off automatic pop');
send('loaded', 1); send('ignition', 1); send('engine_running', 1);
send('overrun', 0.7);
if(JSON.stringify(output.pop()) !== JSON.stringify([1,['burst',0.7]])) throw Error('burst changed');
send('shift', 1); send('pop', 1);
const hits = output.filter(x => x[1][0] === 'play').map(x => x[1]);
if(hits.length !== 2 || hits[0][2] >= hits[1][2]) throw Error('shift strength lost');
const voices = output.filter(x => x[1][0] === 'target').map(x => x[1][1]);
if(JSON.stringify(voices) !== '[1,2]') throw Error('more than two voices');
send('engine_running', 0);
if(JSON.stringify(output.slice(-3)) !== JSON.stringify([[1,['stop']],[0,['target',0]],[0,['stop']]])) throw Error('shutdown left a tail/burst running');
output.length=0; send('overrun',1); send('pop',1);
if(output.length) throw Error('off events escaped');
send('audition');
if(output.length !== 2) throw Error('preview gate changed');
output.length=0; send('loaded',0); send('audition');
if(output.length) throw Error('missing sample fallback');
console.log('ok');
'''
        result = subprocess.run(['node', '-e', script, str(ROOT/'code/ferrari_pop_control.js')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_soundscape_has_a_gated_direct_body_path_independent_of_space(self):
        path = ROOT / 'patchers/ferrari_soundscape_v6_beap~.maxpat'
        self.assertTrue(path.exists(), 'V6 must preserve V5 and add a separate dry-body voice')
        p = json.loads(path.read_text())['patcher']
        boxes = {x['box']['id']: x['box'] for x in p['boxes']}
        self.assertTrue(any(b.get('text') == 'autopattr @autorestore 0' for b in boxes.values()), 'The new plain UI must register with the parent storage, not only BEAP parameters')
        edges = {}
        for item in p['lines']:
            line = item['patchline']
            edges.setdefault(line['source'][0], []).append(line['destination'][0])
        def reaches(start, end, blocked=()):
            pending, visited = [start], set(blocked)
            while pending:
                node = pending.pop()
                if node in visited:
                    continue
                if node == end:
                    return True
                visited.add(node)
                pending.extend(edges.get(node, []))
            return False
        vca = next(i for i,b in boxes.items() if b.get('varname') == 'Ferrari_Output_VCA')
        direct = next(i for i,b in boxes.items() if b.get('varname') == 'Direct_Body')
        space = [i for i,b in boxes.items() if b.get('varname') in ('Bank_Reflection', 'Roadside_Space')]
        outputs = [i for i,b in boxes.items() if b['maxclass'] == 'outlet' and b.get('comment') == 'signal']
        self.assertTrue(reaches(vca, direct, space))
        self.assertEqual(len(outputs), 2)
        for output in outputs:
            self.assertTrue(reaches(direct, output, space))


if __name__ == '__main__':
    unittest.main()
