"""Operator sound controls must work with the driving stream held or deselected."""
import json
import unittest
from pathlib import Path
from tools import build_project as builder

ROOT = Path(__file__).resolve().parents[1]


def destinations(profile, selector, patch=None):
    """Follow control messages to engine/drive, excluding stateful driving gates.

    Model only Max's selector-preserving/stripping routers and prepend objects.
    In particular, never pretend that a driver output can cross a closed gate
    or an unselected Internal/External switch. Object IDs are not an API.
    """
    if patch is None:
        patch = json.loads((ROOT / 'patchers' / f'profile_runtime_host_{profile}.maxpat').read_text())['patcher']
    boxes = {x['box']['id']: x['box'] for x in patch['boxes']}
    wires = {}
    for item in patch['lines']:
        line = item['patchline']
        wires.setdefault(tuple(line['source']), []).append(tuple(line['destination']))
    source = next(i for i, b in boxes.items() if b.get('text') == f'r vss.runtime.control.{profile}')
    pending = [(target, inlet, selector) for target, inlet in wires.get((source, 0), [])]
    reached = []
    while pending:
        ident, inlet, message = pending.pop()
        tokens = boxes[ident].get('text', '').split()
        if not tokens:
            continue
        kind = tokens[0]
        if kind in (f'vehicle_engine_{profile}~', f'drive_simulator_{profile}'):
            reached.append((kind, message))
            continue
        if kind in ('route', 'routepass'):
            choices = tokens[1:]
            outlet = choices.index(message) if message in choices else len(choices)
            if kind == 'route' and outlet < len(choices):
                message = ''  # Remaining numeric arguments have no selector.
        elif kind == 'prepend':
            outlet, message = 0, tokens[1]
        else:
            continue
        pending.extend((target, inlet, message) for target, inlet in wires.get((ident, outlet), []))
    return reached


class RuntimeDesignRoutingTests(unittest.TestCase):
    def test_eq_dynamics_and_designer_actions_bypass_driving_gates(self):
        for profile in ('ev', 'v10', 'v12', 'ioniq6n', 'ferrari'):
            names = ['eq_low', 'eq_lowmid', 'eq_highmid', 'eq_high', 'eq_bypass',
                     'compressor_threshold_db', 'compressor_ratio', 'compressor_attack_rate',
                     'compressor_release_rate', 'compressor_makeup_db', 'compressor_bypass',
                     'start_open', 'start_audition', 'start_save', 'start_reload', 'start_reset']
            names += ['n_sound_mode'] if profile == 'ioniq6n' else ['ev_mode'] if profile == 'ev' else []
            for name in names:
                with self.subTest(profile=profile, selector=name):
                    self.assertEqual([(f'vehicle_engine_{profile}~', name)],
                                     destinations(profile, name, builder.make_profile_runtime_host(profile)['patcher']))

    def test_shared_page_exposes_pop_and_noise_actions_for_every_profile(self):
        patch = builder.make_sound_design_console()['patcher']
        boxes = {x['box']['id']: x['box'] for x in patch['boxes']}
        edges = {}
        for item in patch['lines']:
            line = item['patchline']
            edges.setdefault(tuple(line['source']), []).append(tuple(line['destination']))
        controls = {b.get('varname'): i for i,b in boxes.items()}
        for name in ('pop_open', 'pop_audition', 'noise_open', 'noise_solo'):
            self.assertIn(name, controls, name + ' must be visible in shared Sound Design')
            self.assertEqual(boxes[controls[name]]['presentation'], 1)

        # Exercise the actual generated console's message/selector/gate seam.
        for profile in ('ev', 'v10', 'v12', 'ioniq6n', 'ferrari'):
            state, emitted = {}, []
            def deliver(ident, incoming, inlet=0):
                b = boxes[ident]
                tokens = b.get('text', '').split()
                kind = b['maxclass']
                outgoing = []
                if kind == 'outlet':
                    emitted.append(incoming)
                    return
                if kind == 'message':
                    if incoming and incoming[0] == 'set':
                        return
                    outgoing = [(0, tokens)]
                elif kind == 'toggle':
                    if incoming and incoming[0] == 'set':
                        state[ident] = incoming[1]
                        return
                    outgoing = [(0, incoming)]
                elif kind == 'newobj' and tokens:
                    if tokens[0] == 'route':
                        matched = incoming[0] in tokens[1:]
                        index = tokens[1:].index(incoming[0]) if matched else len(tokens)-1
                        outgoing = [(index, incoming[1:] or ['bang'])] if matched else [(index, incoming)]
                    elif tokens[0] == 'sel':
                        matched = incoming[0] in tokens[1:]
                        index = tokens[1:].index(incoming[0]) if matched else len(tokens)-1
                        outgoing = [(index, ['bang'] if matched else incoming)]
                    elif tokens[0] in ('prepend', 'loadmess'):
                        outgoing = [(0, tokens[1:] + (incoming if tokens[0] == 'prepend' else []))]
                    elif tokens[:2] == ['t', 'b']:
                        outgoing = [(0, ['bang'])]
                    elif tokens[0] == 'gate':
                        if inlet == 0:
                            state[ident] = int(incoming[0])
                        elif state.get(ident, 0):
                            outgoing = [(state[ident]-1, incoming)]
                for port, message in outgoing:
                    for target, target_inlet in edges.get((ident, port), []):
                        deliver(target, message, target_inlet)
            feedback = next(i for i,b in boxes.items() if b['maxclass'] == 'inlet')
            for target, target_inlet in edges.get((feedback,0), []):
                deliver(target, ['profile',profile], target_inlet)
            expected = {
                'pop_open': ['event_open' if profile == 'ioniq6n' else 'backfire_open'],
                'pop_audition': ['event_audition'] if profile == 'ioniq6n' else ['backfire_test','1'],
                'noise_open': ['noise_open'], 'noise_solo': ['noise_solo','1'],
            }
            for name, command in expected.items():
                emitted.clear()
                deliver(controls[name], ['1'] if name == 'noise_solo' else ['bang'])
                self.assertEqual(emitted, [command], (profile, name))
                self.assertEqual([(f'vehicle_engine_{profile}~', command[0])],
                                 destinations(profile, command[0], builder.make_profile_runtime_host(profile)['patcher']))

    def test_sound_controls_reach_engine_once_even_when_drive_is_held_or_external(self):
        for profile in ('ev', 'v10', 'v12', 'ioniq6n', 'ferrari'):
            for selector in (
                'soundscape_enable', 'soundscape_solo', 'soundscape_motion',
                'soundscape_space', 'soundscape_pitch_follow', 'soundscape_transpose',
                'soundscape_brightness', 'soundscape_open', 'soundscape_save',
                'soundscape_reload', 'soundscape_reset', 'dna_solo',
            ):
                with self.subTest(profile=profile, selector=selector):
                    self.assertEqual([(f'vehicle_engine_{profile}~', selector)], destinations(profile, selector))

    def test_pedals_and_lifecycle_still_use_the_original_drive_model(self):
        for profile in ('ev', 'v10', 'v12', 'ioniq6n', 'ferrari'):
            for selector in ('throttle', 'brake', 'ignition', 'start', 'auto'):
                with self.subTest(profile=profile, selector=selector):
                    self.assertEqual([(f'drive_simulator_{profile}', selector)], destinations(profile, selector))


if __name__ == '__main__':
    unittest.main()
