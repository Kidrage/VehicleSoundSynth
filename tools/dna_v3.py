"""Versioned acoustic source recipes. No driver, event, SC or FX ownership.

Source outputs: Core, Body, Character, Upper, legacy L/R, V3 blend,
combustion residual, mechanical residual, intake residual. Only Ferrari uses
the last three. One source clock feeds both deterministic and residual stems.
"""
from __future__ import annotations

PROFILES = ('ferrari', 'v10', 'v12')
MACROS = (
    ('v3_aggression', 'Aggression / odd-even + local drive', .5),
    ('v3_body', 'Body Weight / deep → mid', .5),
    ('v3_character', 'Character / dual cavity depth', .5),
    ('v3_softness', 'Softness / upper spectral rolloff', .5),
    ('v3_release_mass', 'Release Mass / body release time', .5),
    ('v3_width', 'Width / Side above 120 Hz', .5),
    ('v3_load_response', 'Load Response / gain + spectral opening', .5),
    ('v3_pressure_blend', 'Body Pressure / excitation mix', .5),
)
LEVELS = {'ferrari': (0, -5, -9, -18), 'v10': (0, -6, -10, -19), 'v12': (0, -5, -9, -21)}
BODY = {'ferrari': (48, .018), 'v10': (60, .020), 'v12': (42, .014)}
# Core, Body, Upper: attack midpoint; release interval mapped by Release Mass.
ENVELOPES = {
    'ferrari': ((32.5, 90, 160), (70, 180, 300), (20, 40, 90)),
    'v10': ((20, 70, 140), (40, 120, 210), (15, 40, 80)),
    'v12': ((42.5, 130, 240), (77.5, 240, 420), (25, 80, 160)),
}


def source_code(profile, legacy=None):
    if profile not in PROFILES:
        raise ValueError(profile)
    headers = '\n'.join(f'Param {name}({default}, min=0, max=1);' for name, _, default in MACROS)
    histories = '\n'.join(f'History v3_env{i}(0);' for i in range(3))
    if profile == 'ferrari':
        original = '''Param rpm(740, min=0, max=10000);
Param throttle(0, min=0, max=1);
Param load(0, min=-1, max=1);
Param engine_running(0, min=0, max=1);
Param combustion_gain(0, min=0, max=1);
Param shift_cut(1, min=0, max=1);
r = slide(rpm, samplerate*0.013, samplerate*0.021);
v3_fire = r/12;
v3_quarter_phase = phasor(v3_fire*.25);
v3_phase = wrap(v3_quarter_phase*4,0,1);
v3_legacy_l = 0;
v3_legacy_r = 0;
v3_blend = 1;'''
    else:
        # Preserve the original program verbatim up to its output seam. Do not
        # rebuild the old idle out of new oscillators or reset its bank phase.
        seam = 'out1 = tanh(left_drive * sat_drive) / sat_drive;\nout2 = tanh(right_drive * sat_drive) / sat_drive;'
        if not legacy or not legacy.endswith(seam):
            raise ValueError('Accepted ICE output seam changed')
        original = legacy[:-len(seam)] + '''
v3_legacy_l = tanh(left_drive * sat_drive) / sat_drive;
v3_legacy_r = tanh(right_drive * sat_drive) / sat_drive;
v3_fire = bank_fire*2;
v3_phase = wrap(phase_l*2,0,1);
v3_progress = clamp((r-1200)/1800,0,1);
v3_blend = v3_progress*v3_progress*(3-2*v3_progress);'''
    code = headers + '\n' + histories + '\n' + original + '''
// Smooth parameter movement and asymmetric sample-rate-independent envelopes.
v3_effort = max(clamp(throttle,0,1),max(load,0));
v3_agg = slide(v3_aggression,samplerate*.025,samplerate*.025);
v3_mass = slide(v3_body,samplerate*.035,samplerate*.035);
v3_char = slide(v3_character,samplerate*.035,samplerate*.035);
v3_soft = slide(v3_softness,samplerate*.035,samplerate*.035);
v3_response = slide(v3_load_response,samplerate*.035,samplerate*.035);
v3_pressure_mix = slide(v3_pressure_blend,samplerate*.035,samplerate*.035);
v3_gate = slide(engine_running*combustion_gain*shift_cut,samplerate*.009,samplerate*.036);
'''
    for i, (attack, low, high) in enumerate(ENVELOPES[profile]):
        code += f'''v3_tau{i} = v3_effort > v3_env{i} ? {attack} : {low}+v3_release_mass*{high-low};
v3_k{i} = exp(-1/(samplerate*.001*v3_tau{i}));
v3_env{i} = v3_effort+(v3_env{i}-v3_effort)*v3_k{i};
'''
    # Finite partials: the clock never clamps to an unrelated high-frequency
    # drone. Each partial fades out at 0.40..0.45 fs instead.
    for n in range(1, 13):
        code += f'v3_h{n} = cos(v3_phase*6.283185307179586*{n})*clamp((samplerate*.45-v3_fire*{n})/(samplerate*.05),0,1);\n'
    if profile == 'ferrari':
        core = 'v3_h1*.4921875+v3_h2*(.12+.16125*v3_open)+v3_h3*.10546875*v3_open+v3_h4*.0234375*v3_open+v3_h5*.001953125*v3_open'
    elif profile == 'v10':
        core = 'v3_h1*.65+v3_h2*(.26-.13*v3_open)+v3_h3*(.08+.13*v3_open)+v3_h4*.045+v3_h5*.05*v3_open+v3_h7*.025*v3_open+v3_h9*.012*v3_open'
    else:
        core = '+'.join(f'v3_h{n}*{(.68/n**1.65):.8f}'+ ('*(.65+.35*v3_open)' if n%2 else '*(1-.25*v3_open)') for n in range(1,13))
    base, depth = BODY[profile]
    centers = {'ferrari': (320,700), 'v10': (420,800), 'v12': (335,750)}[profile]
    code += f'''v3_open = clamp(.12+.48*v3_agg+v3_env0*(.15+.25*v3_response),0,1);
v3_pressure = {core};
// Body has its OWN deterministic low-frequency carrier; filtering a 500-Hz
// pulse through a 150-Hz lowpass cannot create the missing fundamental.
v3_body_hz = {base}+r*{depth};
v3_body_phase = phasor(v3_body_hz);
v3_body_wave = cos(v3_body_phase*6.283185307179586)*(.85-.30*v3_mass)
 + cos(v3_body_phase*12.566370614359172)*(.08+.28*v3_mass)
 + cos(v3_body_phase*18.84955592153876)*(.02+.12*v3_mass);
v3_suborder = cycle(v3_fire*.5)*.18;
'''
    # Broad dual-formant spectral weights, not high-Q ringing or fixed sine
    # peaks. Character follows RPM orders inside these acoustic windows.
    terms = []
    for n in ((3,5,7,9) if profile == 'v10' else range(1,9)):
        harmonic = f'cos(phase_l*6.283185307179586*{n})' if profile == 'v10' else f'v3_h{n}'
        frequency = f'bank_fire*{n}' if profile == 'v10' else f'v3_fire*{n}'
        # Compact C1 bell windows avoid sixteen per-sample exponentials. RPM
        # and macros are already smoothed; no control-rate stepping is added.
        code += f'''v3_w{n}a = clamp(1-abs({frequency}-{centers[0]}-r*.012)/(240+120*v3_open+100*v3_char),0,1);
v3_w{n}b = clamp(1-abs({frequency}-{centers[1]}-r*.018)/(360+140*v3_open+100*v3_char),0,1);
'''
        terms.append(f'{harmonic}*(v3_w{n}a*v3_w{n}a*(3-2*v3_w{n}a)*.65+v3_w{n}b*v3_w{n}b*(3-2*v3_w{n}b)*.35)/{n**.7:.8f}')
    code += 'v3_cavity = ' + '+'.join(terms) + ';\n'
    if profile == 'ferrari':
        code += '''v3_pm_index = (.03+.12*v3_char)*(.4+.6*v3_open);
v3_pm1 = sin(v3_quarter_phase*6.283185307179586*6 + v3_pm_index*sin(v3_quarter_phase*6.283185307179586*2));
v3_pm2 = sin(v3_quarter_phase*6.283185307179586*9 + v3_pm_index*sin(v3_quarter_phase*6.283185307179586*3));
v3_cavity = v3_cavity + v3_pm1*.09 + v3_pm2*.065;
'''
    code += '''// Shallow, local midrange drive. No whole-bus square-wave saturation.
v3_local_drive = 1+v3_agg*.65;
v3_character_wave = tanh(v3_cavity*v3_local_drive)/v3_local_drive;
v3_upper_wave = (v3_h4*.48+v3_h5*.28+v3_h6*.16+v3_h8*.08)*(1-.82*v3_soft);
out1 = v3_pressure*.18*(.55+(.20+.5*v3_response)*v3_env0)*v3_gate;
out2 = (v3_body_wave+v3_suborder+v3_pressure*.20*v3_pressure_mix)*.18*(.45+(.25+.6*v3_response)*v3_env1)*v3_gate;
out3 = v3_character_wave*.20*(.35+(.30+.7*v3_response)*v3_env0)*(.5+v3_char)*v3_gate;
out4 = v3_upper_wave*.16*v3_env2*v3_gate;
out5 = v3_legacy_l;
out6 = v3_legacy_r;
out7 = v3_blend;
'''
    if profile == 'ferrari':
        code += '''// Random residuals split BEFORE any DNA mixing, gain or saturation.
// The shared cadence excites them; no second engine and no mixed-DNA tap.
v3_peak = pow(max(v3_pressure,0)/.905,2);
out8 = noise()*v3_peak*(.40+.60*v3_env1)*v3_gate;
out9 = noise()*v3_peak*(.3+.7*v3_env0)*v3_gate;
out10 = noise()*(.2+abs(v3_pressure))*(.15+.85*v3_env2)*v3_gate;'''
    else:
        code += 'out8 = 0;\nout9 = 0;\nout10 = 0;'
    return code


MIX_CODE = '''// V3 spatial protection, then exact original/V3 blend.
// in1: BEAP group sum; in2/3: untouched legacy; in4: running blend.
Param v3_width(0.5, min=0, max=1);
History v3_low(0);
History v3_last(0);
History v3_allpass(0);
History v3_ceiling(0);
History v3_infra(0);
v3_k = exp(-6.283185307179586*3500/samplerate);
v3_ceiling = in1*(1-v3_k)+v3_ceiling*v3_k;
v3_hi = exp(-6.283185307179586*28/samplerate);
v3_infra = v3_ceiling*(1-v3_hi)+v3_infra*v3_hi;
v3_mid = v3_ceiling-v3_infra;
v3_side_k = exp(-6.283185307179586*120/samplerate);
v3_low = v3_mid*(1-v3_side_k)+v3_low*v3_side_k;
v3_high = v3_mid-v3_low;
v3_ap = -.96*v3_high+v3_last+.96*v3_allpass;
v3_last = v3_high;
v3_allpass = v3_ap;
v3_side = (v3_ap-v3_high)*.22*slide(v3_width,samplerate*.035,samplerate*.035);
out1 = in2 + in4*(v3_mid+v3_side-in2);
out2 = in3 + in4*(v3_mid-v3_side-in3);'''


def builder():
    try:
        from . import build_project as b
    except ImportError:
        import build_project as b
    return b


def make_acoustic(profile):
    """One source; independent DNA and optional Noise processors. No feedback loop."""
    b = builder()
    p = b.Patcher(1050, 500)
    p.comment('V3 acoustic seam: ONE source → DNA groups / pre-mix residuals → independent outputs', 20, 15, 990)
    control = b.inlet(p, 20, 65)
    source = p.new(f'gen~ @gen Patcher:/gen/{profile}_dna_source_v3.gendsp', 20, 175, 425, numinlets=1, numoutlets=10)
    dna = p.new(f'{profile}_dna_v3_designer~', 20, 300, 240, numinlets=8, numoutlets=3)
    p.connect(control, dna)
    # Designer outlet 2 is bounded synthesis parameters/RTPC, never audio.
    p.connect(dna, source, 2)
    for i in range(7):
        p.connect(source, dna, i, i+1)
    for channel in range(2):
        out = b.outlet(p, 20+channel*120, 430, signal=True)
        p.connect(dna, out, channel)
    if profile == 'ferrari':
        noise = p.new('vehicle_noise_ferrari_v2~', 550, 300, 235, numinlets=4, numoutlets=2)
        p.connect(control, noise)
        for i in range(3):
            p.connect(source, noise, 7+i, 1+i)
        for channel in range(2):
            out = b.outlet(p, 550+channel*120, 430, signal=True)
            p.connect(noise, out, channel)
    return p.document()


def filter_defaults(profile):
    # Broad protective LPs, not resonators pretending to produce absent bass.
    return (('Core', 2700), ('Body', 850), ('Character', 2400), ('Upper', 3500))


def legacy_defaults(profile):
    b = builder()
    if profile == 'ferrari':
        return {}
    preset = b.PRESETS['Aggressive V10' if profile == 'v10' else 'High-Rev V12']
    return {name: preset[name] for name, *_ in b.DNA_PARAMETER_SPECS[profile]}


def factory(profile):
    data = {name: [default] for name, _, default in MACROS}
    data.update({f'legacy_{name}': [default] for name, default in legacy_defaults(profile).items()})
    data.update(beap_factory_data(make_designer(profile)))
    return {'pattrstorage': {'name': profile+'_sound_dna_v3', 'slots': {'99': {'id':99, 'data':data}}}}


def beap_factory_data(document):
    """Reset every live BEAP client, including mute/mode/CV, not just its dials."""
    data = {}
    for item in document['patcher']['boxes']:
        box = item['box']
        if box.get('maxclass') != 'bpatcher':
            continue
        for child in box['patcher']['boxes']:
            for key, value in child['box'].get('restore', {}).items():
                data[box['varname']+'::'+key] = value
    return data


def make_designer(profile):
    b = builder()
    p = b.Patcher(1860, 1650)

    def show(node, x, y, width, height=22):
        box = next(item['box'] for item in p.boxes if item['box']['id'] == node)
        box.update(presentation=1, presentation_rect=[x,y,width,height])
        return node

    show(p.comment(f'{profile.upper()} DNA V3 — Core / Body / Character / Upper',20,15,1400),20,15,1400)
    show(p.comment('1 Solo group → 2 BEAP group dB → 3 macros → 4 filters. Main DNA fader owns the whole stem. No SC / Noise input.',20,45,1450),20,45,1450)
    if profile != 'ferrari':
        show(p.comment('≤1200 RPM = original idle; 1200–3000 = smooth blend. V3 group audition excludes legacy idle; turn audition OFF for normal playback.',20,75,1500),20,75,1500)
    control = b.inlet(p,20,115)
    signals = [b.inlet(p,360+i*145,115,signal=True) for i in range(7)]
    outputs = [b.outlet(p,20+i*150,1580,signal=True) for i in range(2)]
    params_out = b.outlet(p,1700,1580)
    rtpc = ('rpm','throttle','load','accel','engine_running','combustion_gain','shift_cut')
    legacy = legacy_defaults(profile)
    names = tuple(name for name,_,_ in MACROS) + tuple(legacy) + rtpc + ('powertrain_level_db','dna_group','dna_save','dna_reload','dna_reset')
    router = b.route(p,names,20,155,1770)
    p.connect(control,router)
    load = p.new('loadbang',20,200,80)
    mix = p.new('gen~ @gen Patcher:/gen/dna_v3_output.gendsp',20,1200,390,numinlets=4,numoutlets=2)
    for index, (name,label,default) in enumerate(MACROS):
        x = 20+index*225
        show(p.comment(label,x,240,215),x,105,215,36)
        value = show(p.add('flonum',None,x,270,90,minimum=0,maximum=1,varname=name,numoutlets=2),x,145,90)
        initial = p.new(f'loadmess {default}',x,305,95)
        tag = p.new('prepend '+name,x,340,200)
        p.connect(router,value,index)
        p.connect(initial,value)
        p.connect(value,tag)
        p.connect(tag,params_out)
        if name == 'v3_width':
            p.connect(tag,mix)
    # The old cycle_irregularity is the inherited bank clock authority at ALL
    # RPM. Other legacy knobs affect only the old side of the <=3000 blend.
    for index,(name,default) in enumerate(legacy.items()):
        x,y = 20+(index%6)*275, 830+(index//6)*72
        high = 8 if name == 'throttle_loudness_depth' else 1
        label = 'Shared clock (all RPM) · '+name if name == 'cycle_irregularity' else 'Legacy ≤3000 · '+name
        show(p.comment(label,x,y,265),x,y,265)
        value = show(p.add('flonum',None,x,y+25,85,minimum=0,maximum=high,varname='legacy_'+name,numoutlets=2),x,y+25,85)
        initial = p.new(f'loadmess {default:g}',x+95,y+25,95)
        tag = p.new('prepend '+name,x+190,y+25,170)
        p.connect(router,value,len(MACROS)+index)
        p.connect(initial,value)
        p.connect(value,tag)
        p.connect(tag,params_out)
    for name in rtpc:
        # Unknown commands never reach Gen; public lifecycle values are bounded.
        if profile == 'ferrari' and name == 'accel':
            continue
        low = -1 if name in ('load','accel') else 0
        high = 10000 if name == 'rpm' else 1
        x = 20+rtpc.index(name)*230
        clip = p.new(f'clip {low} {high}',x,390,100)
        tag = p.new('prepend '+name,x,425,170)
        p.connect(router,clip,names.index(name))
        p.connect(clip,tag)
        p.connect(tag,params_out)
    audition = show(p.add('number',None,20,470,65,minimum=0,maximum=4,numoutlets=2),20,195,65)
    show(p.comment('Audition: 0 All · 1 Core · 2 Body · 3 Character · 4 Upper (not saved)',95,470,1000),95,195,1000)
    p.connect(router,audition,names.index('dna_group'))
    audition_init = p.new('loadmess 0',20,500,90)
    p.connect(audition_init,audition)
    mixer = b.add_beap_module(p,'Mixers/bp.Audio Mixer.maxpat',20,1010,'V3_Group_Mixer',initial={f'in{i+1}':v for i,v in enumerate(LEVELS[profile])})
    mb = next(x['box'] for x in p.boxes if x['box']['id']==mixer)
    show(mixer,20,590,mb['patching_rect'][2],mb['patching_rect'][3])
    show(p.comment('BEAP inputs 1 / 2 / 3 / 4 = Core / Body / Character / Upper. Start with factory ratios; recommended −30..0 dB.',460,1010,1160),460,590,1160)
    for i,(name,frequency) in enumerate(filter_defaults(profile)):
        x = 20+i*450
        select = p.new(f'expr ($i1==0)||($i1=={i+1})',x,540,210)
        ramp = p.new('pack 0. 35',x,575,105,numinlets=2)
        gain = p.new('line~',x,610,50,numinlets=2,numoutlets=2)
        gate = p.new('*~',x,645,45,numinlets=2)
        p.connect(audition,select)
        p.connect(select,ramp)
        p.connect(ramp,gain)
        p.connect(signals[i],gate)
        p.connect(gain,gate,0,1)
        node = b.add_beap_module(p,'Filter/bp.MMF.maxpat',x,690,'V3_'+name,initial={'Freq':frequency,'Res':.45,'FilterType':0,'power[1]':1})
        box = next(t['box'] for t in p.boxes if t['box']['id']==node)
        show(node,x,270,box['patching_rect'][2],box['patching_rect'][3])
        show(p.comment(name+' · LP; low resonance 0.3–0.8',x,665,425),x,235,425)
        p.connect(gate,node)
        p.connect(node,mixer,0,i)
    p.connect(mixer,mix)
    # Audition must not leak the legacy stem into a group being examined.
    normal = p.new('== 0',1450,1200,60)
    normal_ramp = p.new('pack 1. 35',1530,1200,100,numinlets=2)
    normal_line = p.new('line~',1650,1200,60,numinlets=2,numoutlets=2)
    p.connect(audition,normal)
    p.connect(normal,normal_ramp)
    p.connect(normal_ramp,normal_line)
    for i in range(2):
        gate = p.new('*~',500+i*150,1200,45,numinlets=2)
        p.connect(signals[4+i],gate)
        p.connect(normal_line,gate,0,1)
        p.connect(gate,mix,0,1+i)
    p.connect(signals[6],mix,0,3)
    level = b.add_db_gain_control(p,router,names.index('powertrain_level_db'),20,1300,-3)
    for i in range(2):
        gain = p.new('*~',20+i*150,1480,45,numinlets=2)
        p.connect(mix,gain,i)
        p.connect(level,gain,0,1)
        p.connect(gain,outputs[i])
    p.new('autopattr @autorestore 0',900,1300,190,numoutlets=4)
    storage = p.new(f'pattrstorage {profile}_sound_dna_v3 @autorestore 0 @savemode 0',900,1340,550,numoutlets=4)
    state = p.new(f'js Patcher:/code/dna_v3_state.js {profile}',900,1380,370)
    p.connect(state,storage)
    for index,(action,label) in enumerate((('save','Save DNA'),('restore','Reload DNA'),('reset','Factory Reset'))):
        button = show(p.message(label,900+index*230,1440,180),470+index*230,680,180)
        message = p.message(action,900+index*230,1480,90)
        p.connect(button,message)
        p.connect(router,message,names.index(('dna_save','dna_reload','dna_reset')[index]))
        p.connect(message,state)
        if action == 'restore':
            delay = p.new('delay 250',900,1520,85,numinlets=2)
            p.connect(load,delay)
            p.connect(delay,message)
    receive = p.new(f'r open.{profile}.sound_dna',1250,1340,260)
    front = p.message('front',1530,1340,60)
    window = p.new('thispatcher',1620,1340,100,numoutlets=2)
    p.connect(receive,front)
    p.connect(front,window)
    return p.document(presentation=True)
