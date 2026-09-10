"""V5 running beds: replace source seam, retain the exact V4 filter/FX graph.

No DNA audio input, standalone noise source, or free-running amplitude LFO.
The stateful exciter owns periodic pressure; editable BEAP owns colour/space.
"""
from copy import deepcopy

BED_CONTROLS = (
    ('body', 'Body / 80–250 Hz', 0., 1., .78),
    ('cavity', 'Cavity / 200–650 Hz', 0., 1., .70),
    ('contour', 'Contour / 柔和轮廓', 0., 1., .42),
    ('load_response', 'Load Response / 负载开度', 0., 1., .72),
    ('release_mass', 'Release Mass / 收油惯性', 0., 1., .65),
)


def bed_code(profile):
    ev = profile == 'ev'
    ratio = {'ev': .60, 'v10': .25, 'v12': .20}[profile]
    formants = {'ev': (118, 230, 390), 'v10': (142, 275, 470), 'v12': (108, 205, 360)}[profile]
    code = '''Param body(.78, min=0, max=1);
Param cavity(.70, min=0, max=1);
Param contour(.42, min=0, max=1);
Param load_response(.72, min=0, max=1);
Param release_mass(.65, min=0, max=1);
History slowload(0); History fastload(0); History life(0);
History m1a(0); History m1b(0); History m2a(0); History m2b(0); History m3a(0); History m3b(0);
History subdc(0); History top(0); History top2(0);
History previousPhase(0); History cycleIndex(0); History cycleWeight(1);
// Inputs: pitch octaves / run gate / colour / motion / cadence / idle / load / event.
hz = clamp(261.625565*pow(2,in1),28,520);
loadval = clamp(in7,0,1);
fastcoef = exp(-1/(samplerate*.045));
slowcoef = exp(-1/(samplerate*(loadval > slowload ? .09 : .18+.72*release_mass)));
fastload = loadval+(fastload-loadval)*fastcoef;
slowload = loadval+(slowload-loadval)*slowcoef;
lifecoef = exp(-1/(samplerate*.05));
life = clamp(in2/5,0,1)+(life-clamp(in2/5,0,1))*lifecoef;
release = max(0,slowload-fastload)*release_mass;
colour = clamp(in3,0,1);
motion = clamp(in4,0,1);
idle = clamp(in6,0,1);
event = clamp(in8,0,1);
'''
    if ev:
        code += '''// Two coherent electromagnetic phase shapers: odd body + even cavity.
// Bounded depth keeps the fundamental present while exciting 118/230/390 Hz
// structure even at ready/low RPM; pedal changes colour, never the clock.
fund = hz*.60;
phase = phasor(fund);
wave = sin(phase*twopi);
pressure = sin(wave*(2.70+.24*fastload*load_response));
bank = sin(phase*twopi*2);
exciter = pressure*.72 + sin(bank*(1.40+.20*contour))*.28;
mass = .16+.04*idle+.30*slowload*load_response;
'''
    else:
        code += f'''// Both banks share one RPM clock; rounded pressure, never an audible comparator.
fund = max(18,abs(in5)*{ratio});
phase = phasor(fund);
cycleIndex = lt(phase, previousPhase) ? cycleIndex+1 : cycleIndex;
cycleWeight = lt(phase, previousPhase) ? 1+sin(cycleIndex*2.399963)*{'.055' if profile == 'v10' else '.025'} : cycleWeight;
previousPhase = phase;
// Noninteger pulse shape + tiny cycle-energy variation creates pressure texture,
// never a separate white/mechanical noise source or left/right detuning.
pulse = pow(.5+.5*cos(phase*twopi),3.15+1.65*contour+.25*fastload);
bank = pow(.5+.5*cos((phase+.47)*twopi),2.35+.70*contour);
rawpressure = pulse*.74+bank*{'.30' if profile == 'v10' else '.52'};
subdc = rawpressure+(subdc-rawpressure)*exp(-twopi*20/samplerate);
exciter = (rawpressure-subdc)*cycleWeight;
mass = .34+.04*idle+.30*slowload*load_response+.16*release;
'''
    code += '''// Contour changes pulse shape and filter opening, not cadence or mean amplitude.
exciter = exciter*(1+.12*contour*fastload);
sub = sin(phase*twopi)*.18 + sin(phase*twopi*2)*.07;
'''
    for index, center in enumerate(formants, 1):
        code += f'''f{index} = clamp({center}+hz*{.10+index*.09:.2f}+colour*{12+index*8},70,850);
w{index} = twopi*f{index}/samplerate;
r{index} = exp(-pi*f{index}/({2.0+index*.35}*samplerate));
m{index} = 2*(1-r{index})*sin(w{index})*exciter + 2*r{index}*cos(w{index})*m{index}a-r{index}*r{index}*m{index}b;
m{index}b=m{index}a; m{index}a=m{index};
'''
    code += '''// Independent fast edge / slow mass: lift sheds brightness first.
ceilfreq = 580+colour*220+fastload*120+contour*160;
lpcoef = exp(-twopi*ceilfreq/samplerate);
top = exciter+(top-exciter)*lpcoef;
top2 = top+(top2-top)*lpcoef;
out1 = (m1*.90+sub*.36)*mass*body*life;
out2 = (m2*.65+m3*.42)*(.25+.38*slowload*load_response)*cavity*life;
out3 = top2*(.035+.11*fastload*load_response)*contour*life;
out4 = m1*(release*.32+event*.065)*body*life;
'''
    return code


def make_soundscape_bed(profile):
    try:
        from . import build_project as b
    except ImportError:
        import build_project as b
    old = b.make_soundscape_v4_beap(profile)['patcher']
    modules = b.SOUNDSCAPE_V4_MODULES[profile]
    boxes = {item['box']['id']: item['box'] for item in old['boxes']}
    mixer = next(k for k,v in boxes.items() if v.get('varname') == modules['mixer'])
    split = next(k for k,v in boxes.items() if v.get('text') == 'svf~ 120 0.7')
    spatial = next(e['patchline']['source'][0] for e in old['lines'] if e['patchline']['destination'] == [split,0])
    # Cut ONLY the four source inputs and the independent post-VCA noise input.
    lines = [e for e in old['lines'] if e['patchline']['destination'][0] != mixer and e['patchline']['destination'] != [spatial,1]]
    roots = {k for k,v in boxes.items() if v['maxclass'] in ('inlet','outlet') or v.get('text') == 'thispatcher'}
    keep = set(roots)
    changed = True
    while changed:
        before = len(keep)
        keep.update(e['patchline']['source'][0] for e in lines if e['patchline']['destination'][0] in keep)
        changed = len(keep) != before
    p = b.Patcher(3240,1120)
    p._next_id = max(int(k.split('-')[-1]) for k in boxes)+1
    p.boxes = [deepcopy(item) for item in old['boxes'] if item['box']['id'] in keep]
    p.lines = [deepcopy(e) for e in lines if e['patchline']['source'][0] in keep and e['patchline']['destination'][0] in keep]
    p.parameters = {k:deepcopy(v) for k,v in old.get('parameters',{}).items() if k.split('::')[0] in keep}
    inputs = sorted((v for v in boxes.values() if v['maxclass']=='inlet'), key=lambda v:v['patching_rect'][0])
    gen = p.new(f'gen~ Patcher:/gen/{profile}_soundscape_bed.gendsp',25,460,350,numinlets=8,numoutlets=4)
    for target, original in enumerate((0,1,2,3,5,6,7,9)):
        p.connect(inputs[original]['id'],gen,0,target)
    for channel in range(4): p.connect(gen,mixer,channel,channel)
    p.new('autopattr @autorestore 0',25,120,170,numoutlets=4)
    p.comment(f'{profile.upper()} RUNNING BED V5 — 独立铺底，不读取 DNA 音频；机械/白噪声由 Noise 控制',25,15,1200)
    p.comment('调参顺序：Body / Cavity → Contour → Load Response / Release Mass → BEAP Filter → 原空间效果。所有旋钮 0..1。',25,45,1240)
    p.comment('持续 RPM 控制声源周期；负载决定密度与滤波；收油高频先退、低中频后退。低于 120 Hz 居中。',25,390,1050)
    p.comment('BEAP Layers: 1 Body 80–250 / 2 Cavity 200–650 / 3 Contour / 4 Shift + Lift Recovery',25,420,1120)
    for index,(name,label,lo,hi,default) in enumerate(BED_CONTROLS):
        x=25+index*245
        p.comment(label,x,190,230)
        ui=p.add('flonum',None,x,222,85,numoutlets=2,varname='bed_'+name,minimum=lo,maximum=hi)
        init=p.new(f'loadmess {default}',x,255,115)
        clip=p.new(f'clip {lo} {hi}',x,290,100,numinlets=3)
        message=p.new('prepend '+name,x,325,185)
        p.connect(init,ui); p.connect(ui,clip); p.connect(clip,message); p.connect(message,gen)
    return p.document()


def make_bed_factory(profile):
    try:
        from . import build_project as b
    except ImportError:
        import build_project as b
    doc=b.make_soundscape_factory(profile,version=4)
    storage=doc['pattrstorage']; storage['name']=f'soundscape_{profile}_v5'
    modules=b.SOUNDSCAPE_V4_MODULES[profile]
    removed={modules[k] for k in ('osc_a','osc_b','osc_c','noise')}
    data=storage['slots']['99']['data']
    data={k.replace('_soundscape_v4_beap~','_soundscape_v5_beap~'):v for k,v in data.items() if not any('::'+m+'::' in k for m in removed)}
    prefix=f'{profile}_soundscape_v5_beap~::'
    for i,db in enumerate((-3.,-5.,-10.,-9.),1): data[prefix+modules['mixer']+f'::in{i}']=[db]
    # Body output remains within the inherited colour and safety filters.
    data[prefix+modules['ladder']+'::Freq']=[850.]
    data[prefix+modules['mmf']+'::Freq']=[1050.]
    for name,_,_,_,default in BED_CONTROLS: data[prefix+'bed_'+name]=[default]
    storage['slots']['99']['data']=data
    return doc
