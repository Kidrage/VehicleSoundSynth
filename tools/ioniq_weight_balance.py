"""IONIQ-only running weight repair: independent mass, not a moving EQ notch.

All previous Gen/BEAP/SC/drive files remain intact. New DNA V4 and SC beds V3
are seed-once. Balance=0 removes this iteration only (138a36d sound).
"""
from __future__ import annotations
import copy
import re
from pathlib import Path

BASELINE = '138a36dc71f119966796702c61b73f2ed1f97219'
MODES = ('ignition', 'evolution', 'lightspeed')
DNA_SEED = 'patchers/ioniq6n_sound_dna_v4~.maxpat'
SEEDS = (DNA_SEED, *(f'patchers/ioniq6n_soundscape_{m}_bed_v3_beap~.maxpat' for m in MODES))


def builder():
    try:
        from . import build_project as b
    except ImportError:
        import build_project as b
    return b


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError('Protected source seam changed: '+old[:100])
    return text.replace(old, new, 1)


def foundation_code(*, soundscape=False):
    """Two finite-harmonic pressure clocks feed three broad, slowly moving modes.

    No noise, audio sample, self-oscillating resonator or 1:1 vehicle-RPM clock.
    Finite Chebyshev partials give bounded harmonics below 500 Hz.
    f_body/f_cavity/f_upper are artistic structure modes, NOT measured cabin IR.
    """
    head = '''History wb_slow(0); History wb_fast(0); History wb_rslow(0); History wb_x1(0); History wb_x2(0);
History wb_a1(0); History wb_a2(0); History wb_b1(0); History wb_b2(0); History wb_c1(0); History wb_c2(0);
'''
    code = '''wb_load = clamp(WB_LOAD,0,1);
wb_kf = exp(-1/(samplerate*.055));
wb_ks = exp(-1/(samplerate*(wb_load>wb_slow ? .120 : .550)));
wb_fast = wb_load+(wb_fast-wb_load)*wb_kf;
wb_slow = wb_load+(wb_slow-wb_load)*wb_ks;
wb_rtarget = clamp((WB_RPM-1600)/6400,0,1);
wb_rslow = wb_rtarget+(wb_rslow-wb_rtarget)*exp(-1/(samplerate*.650));
// Small slow frequency movement: mass does not leave its register at high RPM.
wb_fa = WB_FA + 4*wb_slow + 2*wb_rslow;
wb_fb = WB_FB + 5*wb_slow + 3*wb_rslow;
wb_wa = cycle(wb_fa); wb_wb = cycle(wb_fb);
// Distributed finite pressure partials, not a loud pair of fundamental sines.
// Chebyshev polynomials reuse each continuous oscillator phase; no DC term.
wb_a_h2=2*wb_wa*wb_wa-1;
wb_a_h3=4*wb_wa*wb_wa*wb_wa-3*wb_wa;
wb_a_h4=8*pow(wb_wa,4)-8*wb_wa*wb_wa+1;
wb_a_h5=16*pow(wb_wa,5)-20*pow(wb_wa,3)+5*wb_wa;
wb_b_h2=2*wb_wb*wb_wb-1;
wb_b_h3=4*wb_wb*wb_wb*wb_wb-3*wb_wb;
wb_b_h4=8*pow(wb_wb,4)-8*wb_wb*wb_wb+1;
wb_b_h5=16*pow(wb_wb,5)-20*pow(wb_wb,3)+5*wb_wb;
wb_pa=.15*wb_wa+.24*wb_a_h2+.20*wb_a_h3+.14*wb_a_h4+.09*wb_a_h5;
wb_pb=.12*wb_wb+.22*wb_b_h2+.18*wb_b_h3+.14*wb_b_h4+.10*wb_b_h5;
wb_exciter = wb_pa*.62+wb_pb*.56;
wb_body_hz = WB_BODY + 5*wb_slow + 3*wb_rslow;
wb_cavity_hz = WB_CAVITY + 8*wb_slow + 5*wb_rslow;
wb_upper_hz = WB_UPPER + 10*wb_slow + 7*wb_rslow;
'''
    for key,hz,q in [('a','wb_body_hz',1.15),('b','wb_cavity_hz',1.3),('c','wb_upper_hz',1.25)]:
        code += f'''wb_{key}w = 6.283185307179586*{hz}/samplerate;
// Constant-peak bandpass biquad (RBJ): zeros at DC and Nyquist.
wb_{key}alpha = sin(wb_{key}w)/(2*{q});
wb_{key}norm = 1/(1+wb_{key}alpha);
wb_{key} = wb_{key}alpha*wb_{key}norm*(wb_exciter-wb_x2) + 2*cos(wb_{key}w)*wb_{key}norm*wb_{key}1-(1-wb_{key}alpha)*wb_{key}norm*wb_{key}2;
wb_{key}2 = wb_{key}1; wb_{key}1 = wb_{key};
'''
    code += '''wb_x2=wb_x1; wb_x1=wb_exciter;
wb_body_signal = (wb_a*.85+wb_b*.28)*(.24+.40*wb_slow);
wb_cavity_signal = (wb_b*.58+wb_c*.48)*(.16+.32*wb_slow+.08*wb_fast);
'''
    values = {'WB_LOAD': 'clamp((in2-.12)/.88,0,1)' if soundscape else '.45*t_fast+.55*l_slow',
              'WB_RPM':'wb_rpm' if soundscape else 'r',
              'WB_FA':'(mode<.5 ? 49 : mode<1.5 ? 43 : 53)' if soundscape else '61',
              'WB_FB':'(mode<.5 ? 79 : mode<1.5 ? 71 : 83)' if soundscape else '87',
              'WB_BODY':'(mode<.5 ? 148 : mode<1.5 ? 132 : 158)' if soundscape else '144',
              'WB_CAVITY':'(mode<.5 ? 272 : mode<1.5 ? 238 : 286)' if soundscape else '252',
              'WB_UPPER':'(mode<.5 ? 430 : mode<1.5 ? 382 : 454)' if soundscape else '404'}
    for key,value in values.items(): code=code.replace(key,value)
    return head,code


def dna_code(legacy):
    hist, bed = foundation_code()
    prefix='''// V4: balance the dominant root BEFORE common acoustic filtering.
Param weight_balance(1, min=0, max=1);
Param foundation(.70, min=0, max=1);
'''+hist
    gate='''wb_control = slide(clamp(weight_balance,0,1),samplerate*.08,samplerate*.08);
wb_progress = clamp((r-1600)/1200,0,1);
wb_active = wb_control*wb_progress*wb_progress*(3-2*wb_progress);
wb_foundation = slide(clamp(foundation,0,1),samplerate*.08,samplerate*.08);
order1 = cycle(root) * (0.50 + 0.20*motor_order)*(1-.62*wb_active);'''
    code=replace_once(legacy,'order1 = cycle(root) * (0.50 + 0.20*motor_order);',gate)
    # Append AFTER existing oscillators so the previous phase layout is preserved.
    code += '\n'+bed+'''
// Separate outputs enter the actual Body/Cavity filter inputs, not master EQ.
// Both get the SAME Main DNA gain, mixer mutes and VCA as the tonal paths.
wb_gain = wb_active*wb_foundation*run*(.82+.18*cut);
out3 = wb_body_signal*body_pressure*wb_gain*1.8;
out4 = wb_cavity_signal*cavity_structure*wb_gain*1.8;
'''
    return prefix+code


def sc_code():
    hist,bed=foundation_code(soundscape=True)
    return '''// Independent low-mid return. Inputs: lifecycle gate (0..5), effort (0..1).
Param rpm(650, min=0, max=10000);
Param mode(1, min=0, max=2);
Param weight_balance(1, min=0, max=1);
Param foundation(.70, min=0, max=1);
'''+hist+'''
wb_rpm = slide(clamp(rpm,0,10000),samplerate*.025,samplerate*.045);
wb_control = slide(clamp(weight_balance,0,1),samplerate*.08,samplerate*.08);
wb_foundation = slide(clamp(foundation,0,1),samplerate*.08,samplerate*.08);
wb_progress = clamp((wb_rpm-1600)/1200,0,1);
wb_active = wb_control*wb_progress*wb_progress*(3-2*wb_progress);
wb_life = slide(clamp(in1/5,0,1),samplerate*.04,samplerate*.09);
'''+bed+'''
// Dry mono mass bypasses ONLY spatial wet attenuation, NOT SC enable/fader.
// Source never references pitch CV, transpose, speed or vehicle gear ratios.
out1 = (wb_body_signal*.95+wb_cavity_signal*.85)*wb_active*wb_foundation*wb_life*1.7;
'''


def getbox(patch, **fields):
    matches=[e['box'] for e in patch['boxes'] if all(e['box'].get(k)==v for k,v in fields.items())]
    if len(matches)!=1:raise ValueError(f'Ambiguous graph seam: {fields}')
    return matches[0]


def add(p,ident,text=None,cls='newobj',**kw):
    if any(x['box']['id']==ident for x in p['boxes']):raise ValueError('Duplicate ID '+ident)
    obj={'id':ident,'maxclass':cls,'numinlets':1,'numoutlets':1,
         'patching_rect':[30.,1850.+len(p['boxes'])*24,260.,22.]}
    if text is not None:obj['text']=text
    obj.update(kw);p['boxes'].append({'box':obj});return ident


def wire(p,src,dst,outlet=0,inlet=0):
    p['lines'].append({'patchline':{'source':[src,outlet],'destination':[dst,inlet]}})


def controls(p,control,destination,*,ui=False,dna=False,raw_rpm=False):
    """One exact interception seam; preserve the old unmatched control route."""
    names=['weight_balance','foundation']+(['rpm'] if raw_rpm else [])
    old=[e['patchline'] for e in p['lines'] if e['patchline']['source']==[control,0]]
    if len(old)!=1:raise ValueError('Expected one inlet connection')
    router=add(p,'wb-route','route '+' '.join(names),numoutlets=len(names)+1)
    old[0]['source']=[router,len(names)];wire(p,control,router)
    bottom=max((x['box'].get('presentation_rect',[0,0,0,0])[1]+x['box'].get('presentation_rect',[0,0,0,0])[3] for x in p['boxes']),default=0)+28
    # SC originals are patching-view designers; do not switch their view mode.
    for i,name in enumerate(names):
        lo,hi=(0,10000) if name=='rpm' else (0,1)
        clip=add(p,'wb-clip-'+name,f'clip {lo} {hi}',numinlets=3)
        tag=add(p,'wb-tag-'+name,'prepend '+name);wire(p,clip,tag);wire(p,tag,destination)
        if ui and name!='rpm':
            default=1 if name=='weight_balance' else .7
            y=bottom+i*48
            value=add(p,'wb-value-'+name,cls='flonum',minimum=lo,maximum=hi,numoutlets=2,
                      varname=('dna_' if dna else 'bed_')+name,
                      presentation=1,presentation_rect=[35.,y,90.,22.],
                      patching_rect=[35.,960.+i*65,90.,22.])
            label='Weight Balance: 0 = 138a36d; 1 = running repair (idle protected)' if name=='weight_balance' else 'Foundation: slow 120–600 Hz pressure / independent of pitch-follow'
            add(p,'wb-label-'+name,label,cls='comment',numoutlets=0,presentation=1,
                presentation_rect=[145.,y,1000.,34.],patching_rect=[140.,960.+i*65,1100.,34.])
            init=add(p,'wb-init-'+name,f'loadmess {default:g}');wire(p,init,value)
            wire(p,router,value,i);wire(p,value,clip)
        else:wire(p,router,clip,i)
    p['rect'][3]=max(p['rect'][3],bottom+160,1190)


def make_powertrain():
    b=builder();doc=b.timbre_repair.make_ioniq_powertrain();p=doc['patcher']
    gen=next(x['box'] for x in p['boxes'] if x['box'].get('text','').startswith('gen~'))
    gen['text']='gen~ @gen Patcher:/gen/ioniq6n_powertrain_v4.gendsp';gen['numoutlets']=4;gen['outlettype']=['signal']*4
    # Reuse the actual, already wired stem gain. No new gain authority.
    trim=next(e['patchline']['destination'][0] for e in p['lines'] if e['patchline']['source']==[gen['id'],0])
    gain=next(e['patchline']['source'] for e in p['lines'] if e['patchline']['destination']==[trim,1])
    for ch in (2,3):
        newtrim=add(p,f'wb-trim{ch}','*~',numinlets=2)
        out=add(p,f'wb-out{ch}',cls='outlet',numoutlets=0,comment='signal',patching_rect=[900.+(ch-2)*230,625.,30.,22.])
        wire(p,gen['id'],newtrim,ch);wire(p,gain[0],newtrim,gain[1],1);wire(p,newtrim,out)
    inlet=getbox(p,maxclass='inlet')
    controls(p,inlet['id'],gen['id'])
    return doc


def make_dna():
    b=builder();doc=b.timbre_repair.make_ioniq_designer();p=doc['patcher']
    power=getbox(p,text='ioniq6n_powertrain_v3~');power['text']='ioniq6n_powertrain_v4~';power['numoutlets']=4;power['outlettype']=['signal']*4
    for ch,name in [(2,'DNA_Body_Modal'),(3,'DNA_Cavity')]:
        dest=getbox(p,varname=name)['id']
        edge=next(e['patchline'] for e in p['lines'] if e['patchline']['destination']==[dest,0])
        src=edge['source'];s=add(p,f'wb-band-sum{ch}','+~',numinlets=2)
        edge['source']=[s,0];wire(p,src[0],s,src[1]);wire(p,power['id'],s,ch,1)
    state=getbox(p,text='js Patcher:/code/timbre_repair_state.js ioniq6n')
    state['text']='js Patcher:/code/ioniq_weight_state.js dna'
    storage=next(e['box'] for e in p['boxes'] if e['box'].get('text','').startswith('pattrstorage '))
    storage['text']=storage['text'].replace('ioniq6n_sound_dna_v3','ioniq6n_sound_dna_v4')
    controls(p,getbox(p,maxclass='inlet')['id'],power['id'],ui=True,dna=True)
    return doc


def make_mode(mode):
    b=builder();doc=b.make_ioniq6n_soundscape_beap(mode,version=2);p=doc['patcher']
    inputs=sorted((e['box'] for e in p['boxes'] if e['box']['maxclass']=='inlet'),key=lambda o:o['patching_rect'][0])
    add(p,'wb-autopattr','autopattr @autorestore 0',numoutlets=4)
    gen=add(p,'wb-gen','gen~ @gen Patcher:/gen/ioniq6n_weight_bed.gendsp',numinlets=2,numoutlets=1,outlettype=['signal'])
    wire(p,inputs[1]['id'],gen,0,0);wire(p,inputs[5]['id'],gen,0,1)
    init=add(p,'wb-mode-init',f'loadmess mode {MODES.index(mode)}');wire(p,init,gen)
    controls(p,inputs[8]['id'],gen,ui=True,raw_rpm=True)
    # Sum AFTER wet/dry reconstruction but BEFORE original 28 Hz HP and trim.
    safe=[e['box'] for e in p['boxes'] if e['box'].get('text')=='svf~ 28 0.7']
    if len(safe)!=2:raise ValueError('SC final HP count changed')
    for ch,o in enumerate(safe):
        edge=next(e['patchline'] for e in p['lines'] if e['patchline']['destination']==[o['id'],0])
        src=edge['source'];s=add(p,f'wb-dry-sum{ch}','+~',numinlets=2)
        edge['source']=[s,0];wire(p,src[0],s,src[1]);wire(p,gen,s,0,1)
    return doc


def make_host():
    b=builder();doc=b.make_ioniq6n_soundscape_host();p=doc['patcher']
    rpm=getbox(p,text='clip 0. 10000.')['id']
    tag=add(p,'wb-rpm-tag','prepend rpm');wire(p,rpm,tag)
    for mode in MODES:
        o=getbox(p,text=f'ioniq6n_soundscape_{mode}_bed_v2_beap~')
        o['text']=o['text'].replace('_bed_v2_','_bed_v3_');wire(p,tag,o['id'],0,8)
    s=getbox(p,text='js Patcher:/code/ioniq6n_bed_state.js');s['text']='js Patcher:/code/ioniq_weight_state.js soundscape'
    st=next(e['box'] for e in p['boxes'] if e['box'].get('text','').startswith('pattrstorage '))
    st['text']=st['text'].replace('soundscape_ioniq6n_modes_v2','soundscape_ioniq6n_modes_v3')
    return doc


def factory(kind):
    b=builder()
    if kind=='dna':
        d=b.timbre_repair.factory('ioniq6n');data=d['pattrstorage']['slots']['99']['data']
        d['pattrstorage']['name']='ioniq6n_sound_dna_v4'
        data['dna_weight_balance']=[1.];data['dna_foundation']=[.70]
    elif kind=='soundscape':
        d=b.make_ioniq6n_soundscape_factory(version=2)
        data=d['pattrstorage']['slots']['99']['data']
        data={k.replace('_bed_v2_beap~','_bed_v3_beap~'):v for k,v in data.items()}
        for m in MODES:
            prefix=f'ioniq6n_soundscape_{m}_bed_v3_beap~::'
            for key,value in b.dna_v3.beap_factory_data(make_mode(m)).items():
                data.setdefault(prefix+key,value)
            data[prefix+'bed_weight_balance']=[1.];data[prefix+'bed_foundation']=[.70]
        d['pattrstorage']['slots']['99']['data']=data;d['pattrstorage']['name']='soundscape_ioniq6n_modes_v3'
    else:raise ValueError(kind)
    return d


def register(contents):
    for path in (*SEEDS,'patchers/ioniq6n_powertrain_v4~.maxpat','patchers/ioniq6n_cinematic_soundscape_host_v3~.maxpat'):
        contents['patchers'][path]={'kind':'patcher','local':1}
    for name in ('ioniq6n_sound_dna_v4','ioniq6n_soundscape_modes_v3'):
        contents['data'][f'presets/{name}_factory.json']={'kind':'data','local':1}
    contents['code']['code/ioniq_weight_state.js']={'kind':'javascript','local':1}


def outputs():
    return {DNA_SEED:make_dna(),
            **{f'patchers/ioniq6n_soundscape_{m}_bed_v3_beap~.maxpat':make_mode(m) for m in MODES},
            'patchers/ioniq6n_powertrain_v4~.maxpat':make_powertrain(),
            'patchers/ioniq6n_cinematic_soundscape_host_v3~.maxpat':make_host(),
            'presets/ioniq6n_sound_dna_v4_factory.json':factory('dna'),
            'presets/ioniq6n_soundscape_modes_v3_factory.json':factory('soundscape')}


def write_outputs(root):
    b=builder()
    for name,doc in outputs().items():
        if name not in SEEDS or not (root/name).exists():b.write_json(root/name,doc)
