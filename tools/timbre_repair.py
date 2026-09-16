"""Reversible IONIQ V3 / Ferrari V4 voicing. No drive, SC, Noise or FX owner.

Old generators and seed-once designers remain untouched. reference_restore=0
recovers the previous candidate SOURCE at identical RTPC/state, not its driver.
"""
from __future__ import annotations
import re

BASELINE = '467fd7243dc9f419b63e61d28f7d5ea06b309434'
SEEDS = ('patchers/ioniq6n_sound_dna_v3~.maxpat',
         'patchers/ferrari_dna_v4_designer~.maxpat')


def _replace(source: str, old: str, new: str) -> str:
    if source.count(old) != 1:
        raise ValueError('Protected source seam changed: '+old[:100])
    return source.replace(old, new, 1)


def acoustic_rpm(rpm: float, amount: float = 1.) -> float:
    """C1 monotone render-only map; 7600 -> 5500, <=2600 remains exact."""
    r = max(0., min(10000., rpm))
    d = max(r-2600., 0.)
    return r - max(0., min(1., amount))*.5*(d*d/3200. if d < 1600. else d-800.)


def ioniq_code(legacy: str) -> str:
    header = '''// V3 reference fit: render-only RPM, never published as vehicle telemetry.
Param reference_restore(1, min=0, max=1);
History repair_launch_env(0);
'''
    mapping = '''repair_mix = slide(clamp(reference_restore,0,1),samplerate*.080,samplerate*.080);
repair_d = max(r-2600,0);
repair_compress = .5*(repair_d < 1600 ? repair_d*repair_d/3200 : repair_d-800);
repair_rpm = r-repair_mix*repair_compress;
root = clamp(52 + repair_rpm * 0.047, 52, 522);
// Activation (1450) and ready/idle protected. Reuse existing two partials.
repair_up = clamp((r-1900)/700,0,1);
repair_down = clamp((4500-r)/1500,0,1);
repair_window = repair_up*repair_up*(3-2*repair_up)*repair_down*repair_down*(3-2*repair_down);
repair_launch_target = repair_window*sqrt(clamp(throttle,0,1)*clamp(load,0,1))*clamp(accel,0,1);
repair_tau = repair_launch_target > repair_launch_env ? .065 : .220;
repair_k = exp(-1/(samplerate*repair_tau));
repair_launch_env = repair_launch_target+(repair_launch_env-repair_launch_target)*repair_k;
repair_launch = repair_mix*repair_launch_env*repair_up*repair_up*(3-2*repair_up);'''
    code = _replace(legacy, 'root = clamp(52 + r * 0.047, 52, 522);', mapping)
    code = _replace(code, '*(1+.50*detail_amount);', '*(1+.50*detail_amount)*(1+.28*repair_launch);')
    code = _replace(code, '*(1+.80*detail_amount);', '*(1+.80*detail_amount)*(1+.40*repair_launch);')
    return header+code


def ferrari_code(legacy: str) -> str:
    """Restore differentiated deterministic material; residual taps unchanged.

    Retains one shared cadence. The V2 material ratios are artistic references,
    not physical intake/exhaust stems. No random noise returns to the DNA bus.
    """
    code = 'Param reference_restore(1, min=0, max=1);\nParam accel(0, min=-1, max=1);\n'+legacy
    for i in range(1,5):
        code, n = re.subn(rf'^out{i} = ', f'repair_old{i} = ', code, flags=re.M)
        if n != 1:
            raise ValueError('Ferrari output seam changed')
    code += '''
// Material restoration happens AFTER the protected residual calculation.
// Do not alter v3_pressure/v3_peak: Noise keeps identical cadence and gain.
repair_mix = slide(clamp(reference_restore,0,1),samplerate*.080,samplerate*.080);
repair_lift_fast = slide(max(-clamp(accel,-1,1),0),samplerate*.035,samplerate*.160);
repair_lift_slow = slide(max(-clamp(accel,-1,1),0),samplerate*.120,samplerate*.420);
repair_body_tail = 1+.22*repair_lift_slow*clamp(v3_release_mass,0,1);
repair_upper_release = 1-.55*repair_lift_fast;
// Fifth-power pressure family inherited from the V2 reference. Bounded finite
// partials reuse the SAME phase, with no pulse truncation and no clock jitter.
repair_pressure = v3_h1*.4921875+v3_h2*(.18+.10125*v3_open)
 +v3_h3*.10546875*(.50+.50*v3_open)+v3_h4*.0234375*v3_open
 +v3_h5*.001953125*v3_open;
repair_pulse_env = .35+.65*max(v3_h1,0);
// Non-integer material oscillators have continuous OWN phase accumulators;
// never multiply a wrapped engine phase by a non-integer (that makes clicks).
repair_cav_a_hz = v3_fire*1.37;
repair_cav_b_hz = v3_fire*1.43;
repair_int_a_hz = v3_fire*2.61;
repair_int_b_hz = v3_fire*2.73;
// Fixed/slow acoustic windows, not all layers moved in lockstep with RPM.
repair_wa = 1/(1+pow((repair_cav_a_hz-355)/250,2));
repair_wb = 1/(1+pow((repair_cav_b_hz-405)/280,2));
repair_wc = 1/(1+pow((repair_int_a_hz-820)/480,2));
repair_wd = 1/(1+pow((repair_int_b_hz-930)/520,2));
repair_cavity = (cycle(repair_cav_a_hz)*repair_wa*.42
 +cycle(repair_cav_b_hz)*repair_wb*.38)*repair_pulse_env;
repair_intake = (cycle(repair_int_a_hz)*repair_wc*.14
 +cycle(repair_int_b_hz)*repair_wd*.12)*repair_pulse_env;
// Reuse the existing independent Body carrier AND the half-order. Avoid a
// louder isolated bass drone; give the upper body harmonics a pressure shape.
repair_body = v3_body_wave*.82+v3_suborder*1.45
 +repair_pressure*(.18+.22*v3_pressure_mix);
repair_character = tanh((v3_cavity*.40+repair_cavity+repair_intake)
 *v3_local_drive)/v3_local_drive;
repair_new1 = repair_pressure*.18*(.55+(.20+.5*v3_response)*v3_env0)*v3_gate;
repair_new2 = repair_body*.18*(.45+(.25+.6*v3_response)*v3_env1)*repair_body_tail*v3_gate;
repair_new3 = repair_character*.20*(.35+(.30+.7*v3_response)*v3_env0)*(.5+v3_char)*v3_gate;
repair_new4 = v3_upper_wave*.16*v3_env2*repair_upper_release*v3_gate;
out1 = repair_old1+repair_mix*(repair_new1-repair_old1);
out2 = repair_old2+repair_mix*(repair_new2-repair_old2);
out3 = repair_old3+repair_mix*(repair_new3-repair_old3);
out4 = repair_old4+repair_mix*(repair_new4-repair_old4);
'''
    return code


def builder():
    try:
        from . import build_project as b
    except ImportError:
        import build_project as b
    return b


def _box(patch, **conditions):
    found = [x['box'] for x in patch['boxes'] if all(x['box'].get(k)==v for k,v in conditions.items())]
    if len(found) != 1:
        raise ValueError(f'Ambiguous graph seam: {conditions}')
    return found[0]


def _add(patch, ident, text=None, cls='newobj', **extra):
    box = dict(id=ident, maxclass=cls, patching_rect=[20.,1700.,240.,22.], numinlets=1,numoutlets=1)
    if text is not None:
        box['text'] = text
    box.update(extra)
    patch['boxes'].append({'box':box})
    return ident


def _connect(patch, src, dst, outlet=0, inlet=0):
    patch['lines'].append({'patchline':{'source':[src,outlet],'destination':[dst,inlet]}})


def _add_control(document, destination, varname=None):
    """Intercept only reference_restore; all existing routes keep their outlets."""
    patch = document['patcher']
    control = _box(patch,maxclass='inlet') if sum(x['box']['maxclass']=='inlet' for x in patch['boxes'])==1 else min(
        (x['box'] for x in patch['boxes'] if x['box']['maxclass']=='inlet'),key=lambda x:x['patching_rect'][0])
    outgoing = [x for x in patch['lines'] if x['patchline']['source']==[control['id'],0]]
    if len(outgoing) != 1:
        raise ValueError('Expected one protected inlet edge')
    route = _add(patch,'repair-route','route reference_restore',numoutlets=2)
    outgoing[0]['patchline']['source'] = [route,1]
    _connect(patch,control['id'],route)
    clip = _add(patch,'repair-clip','clip 0 1',numinlets=3)
    tag = _add(patch,'repair-tag','prepend reference_restore')
    _connect(patch,clip,tag)
    _connect(patch,tag,destination)
    if varname:
        bottom = max((x['box'].get('presentation_rect',[0,0,0,0])[1]+x['box'].get('presentation_rect',[0,0,0,0])[3]
                      for x in patch['boxes']), default=710)+24
        value = _add(patch,'repair-value',cls='flonum',varname=varname,minimum=0.,maximum=1.,numoutlets=2,
                     presentation=1,presentation_rect=[35.,bottom,90.,22.])
        _add(patch,'repair-label','Reference Restore: 0 = previous candidate; 1 = repaired voicing. Save DNA explicitly.',
             cls='comment',numoutlets=0,presentation=1,presentation_rect=[135.,bottom,1000.,34.])
        initial = _add(patch,'repair-initial','loadmess 1')
        _connect(patch,initial,value)
        _connect(patch,route,value)
        _connect(patch,value,clip)
        if 'rect' in patch:
            patch['rect'][3] = max(patch['rect'][3],bottom+90)
    else:
        _connect(patch,route,clip)
    return document


def _state(document, profile, old_namespace, new_namespace):
    patch = document['patcher']
    scripts = [x['box'] for x in patch['boxes'] if 'state' in x['box'].get('text','') and x['box'].get('text','').startswith('js ')]
    if len(scripts)!=1:
        raise ValueError('State seam ambiguous')
    scripts[0]['text'] = 'js Patcher:/code/timbre_repair_state.js '+profile
    storage = next(x['box'] for x in patch['boxes'] if x['box'].get('text','').startswith('pattrstorage '))
    if not storage['text'].startswith('pattrstorage '+old_namespace+' '):
        raise ValueError('Storage namespace changed')
    storage['text'] = f'pattrstorage {new_namespace} @autorestore 0 @savemode 0 @changemode 1 @greedy 1'
    return document


def make_ioniq_designer():
    b=builder()
    doc = b.make_sound_dna('ioniq6n',version=2)
    power = _box(doc['patcher'],text='ioniq6n_powertrain_v2~')
    power['text'] = 'ioniq6n_powertrain_v3~'
    _state(doc,'ioniq6n','ioniq6n_sound_dna_v2','ioniq6n_sound_dna_v3')
    return _add_control(doc,power['id'],'dna_reference_restore')


def make_ioniq_powertrain():
    doc=builder().make_ioniq6n_powertrain(version=2)
    gen=next(x['box'] for x in doc['patcher']['boxes'] if x['box'].get('text','').startswith('gen~ '))
    gen['text']='gen~ @gen ../gen/ioniq6n_powertrain_v3.gendsp'
    return _add_control(doc,gen['id'])


def make_ferrari_designer():
    b=builder()
    doc=b.dna_v3.make_designer('ferrari')
    patch=doc['patcher']
    tag=_box(patch,text='prepend v3_aggression')
    dest=next(x['patchline']['destination'][0] for x in patch['lines'] if x['patchline']['source']==[tag['id'],0])
    router=next(x['box'] for x in patch['boxes'] if x['box'].get('text','').startswith('route '))
    clip=_add(patch,'repair-accel-clip','clip -1 1',numinlets=3)
    accel_tag=_add(patch,'repair-accel-tag','prepend accel')
    _connect(patch,router['id'],clip,router['text'].split()[1:].index('accel'))
    _connect(patch,clip,accel_tag)
    _connect(patch,accel_tag,dest)
    for item in patch['boxes']:
        box=item['box']
        if box['maxclass']=='comment' and 'FERRARI DNA V3' in box.get('text',''):
            box['text']=box['text'].replace('FERRARI DNA V3','FERRARI DNA V4 / material restore')
    _state(doc,'ferrari','ferrari_sound_dna_v3','ferrari_sound_dna_v4')
    return _add_control(doc,dest,'reference_restore')


def make_ferrari_acoustic():
    doc=builder().dna_v3.make_acoustic('ferrari')
    p=doc['patcher']
    _box(p,text='gen~ @gen Patcher:/gen/ferrari_dna_source_v3.gendsp')['text']='gen~ @gen Patcher:/gen/ferrari_dna_source_v4.gendsp'
    _box(p,text='ferrari_dna_v3_designer~')['text']='ferrari_dna_v4_designer~'
    return doc


def factory(profile, document=None):
    b=builder()
    if profile=='ioniq6n':
        doc=document or make_ioniq_designer()
        result=b.ioniq_dna_v2.factory(doc)
        name='ioniq6n_sound_dna_v3'
        key='dna_reference_restore'
    elif profile=='ferrari':
        result=b.dna_v3.factory('ferrari')
        name='ferrari_sound_dna_v4'
        key='reference_restore'
    else:
        raise ValueError(profile)
    result['pattrstorage']['name']=name
    result['pattrstorage']['slots']['99']['data'][key]=[1.]
    return result


def register(contents):
    for name in (*SEEDS,'patchers/ioniq6n_powertrain_v3~.maxpat','patchers/ferrari_acoustic_v4~.maxpat'):
        contents['patchers'][name]={'kind':'patcher','local':1}
    for name in ('ioniq6n_sound_dna_v3','ferrari_sound_dna_v4'):
        contents['data']['presets/'+name+'_factory.json']={'kind':'data','local':1}
    contents['code']['code/timbre_repair_state.js']={'kind':'javascript','local':1}


def outputs():
    b=builder()
    i=make_ioniq_designer()
    return {
        SEEDS[0]:i,
        SEEDS[1]:make_ferrari_designer(),
        'patchers/ioniq6n_powertrain_v3~.maxpat':make_ioniq_powertrain(),
        'patchers/ferrari_acoustic_v4~.maxpat':make_ferrari_acoustic(),
        'presets/ioniq6n_sound_dna_v3_factory.json':factory('ioniq6n',i),
        'presets/ferrari_sound_dna_v4_factory.json':factory('ferrari'),
    }


def write_outputs(root):
    b=builder()
    for name,doc in outputs().items():
        if name in SEEDS and (root/name).exists():
            continue
        b.write_json(root/name,doc)
