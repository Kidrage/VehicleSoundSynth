"""Independent running-bed contract; legacy FX remain byte-identical."""
import unittest
import math
import cmath
from tools import build_project as build


class SoundscapeBedTests(unittest.TestCase):
    def test_no_bare_comparison_with_identifier_in_gen_code(self):
        from tools.soundscape_bed import bed_code
        # Gen also has a '<p' (ltp) operator. Named lt() avoids interpreting
        # the first letter of previousPhase as part of that operator.
        for profile in ('ev', 'v10', 'v12'):
            code = '\n'.join(line.split('//', 1)[0] for line in bed_code(profile).splitlines())
            self.assertNotRegex(code, r'[<>][A-Za-z_]', profile)
            if profile != 'ev':
                self.assertEqual(code.count('lt(phase, previousPhase)'), 2)

    def test_ev_electromagnetic_exciter_fills_low_mids_without_pitch_drift(self):
        from tools.soundscape_bed import bed_code
        code = bed_code('ev')
        # Evaluate the actual emitted, memory-free phase-shaping equations.
        # Native Max still verifies the complete modal/filter/output chain.
        source_lines = [line for line in code.splitlines()
                        if line.startswith(('wave =', 'pressure =', 'bank =', 'exciter ='))]
        self.assertIn('fund = hz*.60;', code)
        count = 512
        for rpm in (650, 2000):
            fund = (55 + .032 * rpm) * .60
            for load in (.2, 1.):
                samples = []
                for index in range(count):
                    state = dict(phase=index / count, twopi=2 * math.pi, sin=math.sin,
                                 fastload=load, load_response=.72, contour=.42)
                    for line in source_lines:
                        name, expression = line.rstrip(';').split(' = ', 1)
                        state[name] = eval(expression, {'__builtins__': {}}, state)
                    samples.append(state['exciter'])
                coefficients = [sum(sample * cmath.exp(-2j * math.pi * harmonic * index / count)
                                    for index, sample in enumerate(samples)) / count
                                for harmonic in range(1, 17)]
                total = sum(abs(value) ** 2 for value in coefficients)
                body = sum(abs(value) ** 2 for harmonic, value in enumerate(coefficients, 1)
                           if 80 <= fund * harmonic <= 650)
                self.assertGreater(body / total, .25, (rpm, load, body / total))
                self.assertGreater(abs(coefficients[0]), max(map(abs, coefficients[1:])))
                self.assertLess(abs(sum(samples) / count), 1e-12)
                self.assertLess(max(map(abs, samples)), 1.2)

    def test_all_bed_knobs_are_exposed_to_the_gen_message_inlet(self):
        from tools.soundscape_bed import bed_code, BED_CONTROLS
        for profile in ('ev','v10','v12'):
            graph=build.make_gen(bed_code(profile),input_count=8)['patcher']
            names={box['box'].get('text','').split()[1] for box in graph['boxes'] if box['box'].get('text','').startswith('param ')}
            self.assertEqual(names,{row[0] for row in BED_CONTROLS})
            nodes=[box['box'] for box in graph['boxes'] if box['box'].get('text','').startswith('in ')]
            self.assertEqual(len(nodes),8)
            for i,node in enumerate(nodes):
                self.assertIn({'patchline':{'source':[node['id'],0],'destination':['obj-1',i]}},graph['lines'])

    def test_new_bed_has_stateful_source_and_preserves_spatial_modules(self):
        from tools.soundscape_bed import make_soundscape_bed
        for profile in ('ev', 'v10', 'v12'):
            old = build.make_soundscape_v4_beap(profile)['patcher']
            new = make_soundscape_bed(profile)['patcher']
            old_named = {b['box'].get('varname'): b['box'] for b in old['boxes']}
            new_named = {b['box'].get('varname'): b['box'] for b in new['boxes']}
            for key in ('chorus', 'reverb'):
                name = build.SOUNDSCAPE_V4_MODULES[profile][key]
                self.assertEqual(old_named[name]['patcher'], new_named[name]['patcher'])
            texts = [b['box'].get('text','') for b in new['boxes']]
            self.assertTrue(any(f'gen~ Patcher:/gen/{profile}_soundscape_bed.gendsp' == t for t in texts))
            self.assertFalse(any(b['box'].get('varname') == build.SOUNDSCAPE_V4_MODULES[profile]['noise'] for b in new['boxes']))
            for param in ('body', 'cavity', 'contour', 'load_response', 'release_mass'):
                self.assertIn('bed_' + param, new_named)


if __name__ == '__main__':
    unittest.main()
