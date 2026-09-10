import unittest
from tools import build_project as b


class FerrariNoiseSplitTests(unittest.TestCase):
    def test_only_independent_mechanical_air_returns_are_removed(self):
        old=b.make_ferrari_soundscape_v5_beap(6)['patcher']
        new=b.make_ferrari_soundscape_v5_beap(7)['patcher']
        removed=[e for e in old['lines'] if e not in new['lines']]
        self.assertEqual(len(removed),2)
        noncomments=lambda p:[i for i in p['boxes'] if i['box']['maxclass']!='comment']
        self.assertEqual(noncomments(old),noncomments(new),'Body, cavity, direct body and all FX must remain unchanged')
        boxes={i['box']['id']:i['box'] for i in old['boxes']}
        self.assertEqual({boxes[e['patchline']['source'][0]]['patching_rect'][0] for e in removed},{1510.,2225.})
        self.assertEqual(len(new['lines']),len(old['lines'])-2)
        old_data=b.make_ferrari_soundscape_v5_factory(6)['pattrstorage']['slots']['99']['data']
        new_data=b.make_ferrari_soundscape_v5_factory(7)['pattrstorage']['slots']['99']['data']
        self.assertEqual({k.replace('_v6_','_v7_'):v for k,v in old_data.items()},new_data)
