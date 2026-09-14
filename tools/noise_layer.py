"""One optional, independently gated Noise designer shared by five profiles."""
from __future__ import annotations

CONTROL_SPECS = (
    ('noise_mechanical_db', 'Mechanical / 机械 dB', -10.0, -60.0, 0.0,
     'RPM cadence + moving 290–1360 Hz band; try at a steady 2000–5000 RPM.'),
    ('noise_intake_db', 'Intake / 进气 dB', -15.0, -60.0, 0.0,
     'Load + throttle pressure; compare light/full load at the same RPM.'),
    ('noise_tire_db', 'Tire / 路面 dB', -14.0, -60.0, 0.0,
     '70–900 Hz common-center road texture; speed only, silent while parked.'),
    ('noise_air_db', 'Air / 风噪 dB', -22.0, -60.0, 0.0,
     'Stereo air above 400 Hz; speed curve, not an always-on hiss.'),
    ('noise_color', 'Color / 色彩 0–1', 0.35, 0.0, 1.0,
     'Opens intake/wind filters, not engine pitch. Start at 0.2–0.5.'),
)
FILTER_DEFAULTS = {'Freq': 3400.0, 'Res': 0.45, 'FilterType': 0, 'power[1]': 1}
COMBUSTION_SPEC = ('noise_combustion_db', 'Combustion / 燃烧残差 dB', -10.0, -60.0, 0.0,
                   'Shared DNA cadence, PRE-DNA-gain random pressure. Main Noise fader still owns the stem.')


def make_vehicle_noise_factory(profile, version=1):
    specs = CONTROL_SPECS + ((COMBUSTION_SPEC,) if version == 2 else ())
    data = {name: [default] for name, _, default, *_ in specs}
    data.update({f'Noise_Ceiling::{name}': [value] for name, value in FILTER_DEFAULTS.items()})
    if version == 2:
        try:
            from .dna_v3 import beap_factory_data
        except ImportError:
            from dna_v3 import beap_factory_data
        data.update(beap_factory_data(make_vehicle_noise(profile, version=2)))
    return {'pattrstorage': {'name': f'noise_{profile}_v{version}', 'slots': {
        '99': {'id': 99, 'data': data}
    }}}


def make_vehicle_noise(profile, version=1):
    # Lazy import avoids a circular import when the authority calls this builder.
    try:
        from tools.build_project import Patcher, inlet, outlet, route, add_beap_module
    except ModuleNotFoundError:
        from build_project import Patcher, inlet, outlet, route, add_beap_module
    if profile not in ('ev', 'v10', 'v12', 'ioniq6n', 'ferrari'):
        raise ValueError(profile)
    if version not in (1, 2) or (version == 2 and profile != 'ferrari'):
        raise ValueError((profile, version))
    specs = CONTROL_SPECS + ((COMBUSTION_SPEC,) if version == 2 else ())
    p = Patcher(1580 if version == 2 else 1280, 1010)

    def present(box_id, x, y, w, h=22):
        box = next(item['box'] for item in p.boxes if item['box']['id'] == box_id)
        box.update(presentation=1, presentation_rect=[x, y, w, h])
        return box_id

    present(p.comment(f'{profile.upper()} NOISE — mechanical / intake / road / air', 20, 15, 1150), 20, 15, 1150)
    present(p.comment('1 Main Noise fader (−60 = OFF) → 2 Solo → 3 component dB → 4 Color / BEAP ceiling. No reverb.',
                      20, 42, 1160), 20, 45, 1160)
    present(p.comment('Run engine first. V2 residuals come from the shared pre-mix source, NEVER DNA output gain; SC is independent.' if version == 2 else 'Run the engine first. No ignition-independent audition. Sound DNA / Soundscape do not feed this module.',
                      20, 67, 1160), 20, 73, 1160)
    control = inlet(p, 20, 110)
    residuals = [inlet(p, 65+i*50, 70, signal=True) for i in range(3)] if version == 2 else []
    names = tuple(spec[0] for spec in specs) + ('noise_open', 'noise_save', 'noise_reload', 'noise_reset', 'noise_solo')
    router = route(p, names, 65, 110, 1110)
    p.connect(control, router)
    controller = p.new(f'js Patcher:/code/noise_control.js {profile}' + (' 2' if version == 2 else ''), 20, 335, 340)
    p.connect(router, controller, len(names))
    load = p.new('loadbang', 1070, 335, 70)
    p.connect(load, controller)
    for index, (name, label, default, low, high, hint) in enumerate(specs):
        x = 20 + index * 242
        present(p.comment(label, x, 155, 235), x, 115, 235)
        value = present(p.add('flonum', None, x, 187, 94, numoutlets=2,
                              minimum=low, maximum=high, varname=name), x, 145, 94)
        present(p.comment(hint, x, 222, 231, 62), x, 180, 231, 62)
        initial = p.new(f'loadmess {default:g}', x, 291, 100)
        tagged = p.new(f'prepend {name}', x, 315, 220)
        p.connect(router, value, index)
        p.connect(initial, value)
        p.connect(value, tagged)
        p.connect(tagged, controller)

    keys = ('active', 'stem', 'cadence', 'mechanical_hz', 'intake_hz', 'air_hz', 'mechanical', 'intake', 'tire', 'air')
    if version == 2:
        keys += ('combustion',)
    dsp_route = route(p, keys, 20, 375, 1150)
    p.connect(controller, dsp_route)
    signals = {}
    for index, key in enumerate(keys):
        x = 20 + index * 122
        pack = p.new('pack 0. 40', x, 412, 100, numinlets=2)
        line = p.new('line~', x, 445, 50, numinlets=2, numoutlets=2)
        p.connect(dsp_route, pack, index)
        p.connect(pack, line)
        signals[key] = line

    # One coherent, audio-rate cadence shapes mechanical texture. No slow LFO.
    noise = p.new('noise~', 20, 495, 60, numinlets=0)
    cadence = p.new('cycle~', 95, 495, 65, numinlets=2)
    pulse = p.new('*~ 0.35', 170, 495, 75, numinlets=2)
    offset = p.new('+~ 0.65', 255, 495, 75, numinlets=2)
    excited = p.new('*~', 340, 495, 40, numinlets=2)
    p.connect(signals['cadence'], cadence)
    p.connect(cadence, pulse)
    p.connect(pulse, offset)
    p.connect(noise, excited)
    p.connect(offset, excited, 0, 1)
    mechanical = p.new('svf~ 650 0.58', 20, 550, 115, numinlets=3, numoutlets=4)
    intake = p.new('svf~ 1000 0.45', 215, 550, 125, numinlets=3, numoutlets=4)
    p.connect(residuals[1] if version == 2 else excited, mechanical)
    p.connect(signals['mechanical_hz'], mechanical, 0, 1)
    p.connect(residuals[2] if version == 2 else noise, intake)
    p.connect(signals['intake_hz'], intake, 0, 1)
    branches = []
    for name, source, x in (('mechanical', mechanical, 20), ('intake', intake, 215)):
        gain = p.new('*~', x, 590, 40, numinlets=2)
        p.connect(source, gain, 2)
        p.connect(signals[name], gain, 0, 1)
        branches.append(gain)
    tire = p.new('pink~', 405, 495, 55, numinlets=0)
    tire_hp = p.new('svf~ 70 0.65', 405, 535, 110, numinlets=3, numoutlets=4)
    tire_lp = p.new('lores~ 900 0.25', 405, 575, 130, numinlets=3)
    tire_gain = p.new('*~', 405, 615, 40, numinlets=2)
    p.connect(tire, tire_hp)
    p.connect(tire_hp, tire_lp, 1)
    p.connect(tire_lp, tire_gain)
    p.connect(signals['tire'], tire_gain, 0, 1)
    main_sum = p.new('+~', 20, 635, 40, numinlets=2)
    road_sum = p.new('+~', 85, 635, 40, numinlets=2)
    p.connect(branches[0], main_sum)
    p.connect(branches[1], main_sum, 0, 1)
    p.connect(main_sum, road_sum)
    p.connect(tire_gain, road_sum, 0, 1)
    ceiling = add_beap_module(p, 'Filter/bp.MMF.maxpat', 20, 685, 'Noise_Ceiling', initial=FILTER_DEFAULTS)
    # Keep the native live BEAP controls exposed and saved; no unused decorative filter.
    template = next(item['box'] for item in p.boxes if item['box']['id'] == ceiling)
    present(ceiling, 20, 295, template['patching_rect'][2], template['patching_rect'][3])
    present(p.comment('BEAP ceiling: LP / 1800–4500 Hz / restrained resonance (0.3–0.8).', 370, 685, 800), 365, 302, 815)
    if version == 2:
        combustion_filter = p.new('svf~ 250 0.65', 1400, 540, 125, numinlets=3, numoutlets=4)
        # The band follows RPM, not speed, including a rev while parked.
        combustion_frequency = p.new('*~ 0.55', 1400, 500, 80, numinlets=2)
        combustion_gain = p.new('*~', 1400, 590, 45, numinlets=2)
        residual_sum = p.new('+~', 1400, 635, 45, numinlets=2)
        p.connect(signals['mechanical_hz'], combustion_frequency)
        p.connect(combustion_frequency, combustion_filter, 0, 1)
        p.connect(residuals[0], combustion_filter)
        p.connect(combustion_filter, combustion_gain, 2)
        p.connect(signals['combustion'], combustion_gain, 0, 1)
        p.connect(road_sum, residual_sum)
        p.connect(combustion_gain, residual_sum, 0, 1)
        p.connect(residual_sum, ceiling)
    else:
        p.connect(road_sum, ceiling)
    gate = p.new('*~', 540, 705, 40, numinlets=2)
    p.connect(signals['active'], gate)
    p.connect(signals['stem'], gate, 0, 1)
    for channel, x in enumerate((610, 915)):
        air = p.new('noise~', x, 495, 60, numinlets=0)
        air_side = p.new('*~ 0.25', x + 75, 495, 75, numinlets=2)
        air_common = p.new('+~', x + 160, 495, 40, numinlets=2)
        hp = p.new('svf~ 400 0.65', x, 535, 120, numinlets=3, numoutlets=4)
        lp = p.new('lores~ 2300 0.2', x, 575, 130, numinlets=3)
        amount = p.new('*~', x, 615, 40, numinlets=2)
        summed = p.new('+~', x, 660, 40, numinlets=2)
        infra = p.new('svf~ 28 0.7', x, 715, 110, numinlets=3, numoutlets=4)
        gain = p.new('*~', x, 755, 40, numinlets=2)
        output = outlet(p, x, 810, signal=True)
        # Mostly shared air preserves mono compatibility even with only Air enabled.
        p.connect(air, air_side)
        p.connect(noise, air_common)
        p.connect(air_side, air_common, 0, 1)
        p.connect(air_common, hp)
        p.connect(hp, lp, 1)
        p.connect(signals['air_hz'], lp, 0, 1)
        p.connect(lp, amount)
        p.connect(signals['air'], amount, 0, 1)
        p.connect(ceiling, summed)
        p.connect(amount, summed, 0, 1)
        p.connect(summed, infra)
        p.connect(infra, gain, 1)
        p.connect(gate, gain, 0, 1)
        p.connect(gain, output)
        meter = present(p.add('meter~', None, x + 60, 785, 150, 18, numoutlets=1), 370 + channel * 290, 365, 250, 20)
        p.connect(gain, meter)

    # Open the one currently sounding instance. Solo is a profile-scoped engine command.
    front_receive = p.new(f'r open.{profile}.noise', 20, 855, 180)
    front = p.message('front', 210, 855, 55)
    window = p.new('thispatcher', 275, 855, 90, numoutlets=2)
    p.connect(front_receive, front)
    p.connect(router, front, len(specs))
    p.connect(front, window)
    solo = present(p.add('toggle', None, 385, 855, 24), 960, 355, 24, 24)
    present(p.comment('Noise Solo', 420, 855, 105), 990, 356, 130)
    solo_message = p.new('prepend noise_solo', 385, 895, 145)
    solo_send = p.new(f's vss.runtime.control.{profile}', 535, 895, 220, numoutlets=0)
    solo_set = p.new('prepend set', 720, 895, 100)
    p.connect(router, solo_set, len(specs)+4)
    p.connect(solo_set, solo)
    p.connect(solo, solo_message)
    p.connect(solo_message, solo_send)
    p.new('autopattr @autorestore 0', 20, 895, 180, numoutlets=4)
    storage = p.new(f'pattrstorage noise_{profile}_v{version} @autorestore 0 @savemode 0', 20, 935, 420, numoutlets=4)
    state = p.new(f'js Patcher:/code/noise_state.js {profile}' + (' 2' if version == 2 else ''), 455, 935, 335)
    p.connect(state, storage)
    for index, (action, caption) in enumerate((('save', 'Save Noise'), ('restore', 'Reload Noise'), ('reset', 'Factory Reset'))):
        x = 365 + 190 * index
        button = present(p.message(caption, x, 975, 155), x, 420, 155)
        command = p.message(action, x, 1010, 65)
        p.connect(router, command, len(specs)+1 + index)
        p.connect(button, command)
        p.connect(command, state)
        if action == 'restore':
            delayed = p.new('delay 250', 1070, 895, 80, numinlets=2)
            p.connect(load, delayed)
            p.connect(delayed, command)
    return p.document(presentation=True)
