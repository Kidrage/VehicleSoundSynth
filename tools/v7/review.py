"""V7 R2 inspectable routing, save receipts and compact Mix Lab UI.

Generated signal taps are read-only. They do not enter source audio or CAN.
Filter-bank readings are broad-band estimates, not brick-wall STEM meters.
"""
import json
from pathlib import Path
from . import graph as g
from .schema import PARAMS, PROFILES

LAB_PARAMS = ['v7_order2_db','v7_order3_db','v7_speed_weight_db','v7_speed_edge_db']
BANDS = [('v7_meter_sub_db',60,.7,'60 Hz / LF'),
         ('v7_meter_body_db',170,.8,'170 Hz / Body'),
         ('v7_meter_cavity_db',300,1.4,'300 Hz / Cavity'),
         ('v7_meter_edge_db',3500,.9,'3.5 kHz / Edge')]

def meter_code():
    code='// Monitor only: four constant-peak bandpasses, stereo-mean power, 250ms RMS.\n'
    for i,(_,hz,q,_) in enumerate(BANDS):
        a=f'm{i}'
        code+=f'{a}w=6.283185307179586*{hz}/samplerate; {a}alpha=sin({a}w)/(2*{q}); {a}norm=1/(1+{a}alpha);\n'
        for ch in (1,2):
            s=a+str(ch)
            code+=f'''History {s}x1(0); History {s}x2(0); History {s}y1(0); History {s}y2(0);
{s}y={a}alpha*{a}norm*(in{ch}-{s}x2)+2*cos({a}w)*{a}norm*{s}y1-(1-{a}alpha)*{a}norm*{s}y2;
{s}x2={s}x1; {s}x1=in{ch}; {s}y2={s}y1; {s}y1={s}y;
'''
        code+=f'''History {a}power(0);
{a}p=({a}1y*{a}1y+{a}2y*{a}2y)*.5;
{a}power={a}p+({a}power-{a}p)*exp(-1/(samplerate*.250));
out{i+1}=10*log10(max({a}power,1e-12));
'''
    return code

def state_contracts(owners):
    out={}
    for p in PROFILES:
        names=[None, 'module_mixer_'+p, 'vehicle_bus_eq_'+p, 'start_'+p+'_v3',
               'noise_'+p+('_v2' if p=='ferrari' else '_v1'),
               'ioniq6n_sound_dna_v4' if p=='ioniq6n' else 'ferrari_sound_dna_v5' if p=='ferrari' else 'ev_sound_dna' if p=='ev' else p+'_sound_dna_v3',
               'soundscape_ioniq6n_modes_v3' if p=='ioniq6n' else 'soundscape_ferrari_v7' if p=='ferrari' else 'soundscape_'+p+'_v5',
               p+('_pop_v3' if p=='ferrari' else '_pop_v4')]
        out[p]=[dict(file=f, storage=n, owner=o) for f,n,o in zip(owners[p],names,('V7','Mix','EQ','Start','Noise','DNA','Soundscape','Pop'))]
    return out

def snapshot(p, source, port, name, sender, ident):
    s=g.add(p,ident+'-snapshot','snapshot~ 100',ins=2)
    t=g.add(p,ident+'-tag','prepend '+name)
    g.wire(p,source,s,so=port);g.wire(p,s,t);g.wire(p,t,sender)

def lab():
    d=g.control_page(LAB_PARAMS,PARAMS,'V7 MIX LAB | 阶次比例 · 高速保持 · 核验',
                     '先减突出的单音，再补固定低频。高速补偿默认0；只在确认有余量后增加，随当前发动机保存。')
    p=d['patcher']
    g.comment(p,'meter-note','连续 DNA + SC 的数字输出观察（EQ后／事件与车内处理前），250ms RMS，重叠宽带估计；不是座舱声压。',16,257,1080,34,12)
    keys=[x[0] for x in BANDS]+['drive_state','shift_reason','v7_render_rpm','v7_root_hz','v7_save_status']
    router=g.add(p,'lab-meter-route','route '+' '.join(keys),outs=len(keys)+1);g.wire(p,'in',router)
    for i,(key,hz,q,label) in enumerate(BANDS):
        x=16+i*274
        g.comment(p,key+'-title',label+' / dBFS',x,302,260,26,13)
        box=g.add(p,key,cls='flonum',outs=2,rect=[x,333,253,28],presentation=1,presentation_rect=[x,333,253,28],ignoreclick=1,format=6,hint=f'Bandpass {hz} Hz, Q={q}; overlap with adjacent meters; digital RMS, not acoustic SPL.')
        setter=g.add(p,key+'-readback','prepend set');g.wire(p,router,setter,so=i);g.wire(p,setter,box)
    g.comment(p,'meter-meaning','不要把四个读数调成一样：它们的带宽不同。比较同一驾驶轨迹的 A/B；谐波能量占比用导出的 WAV 审核。',16,372,1080,35,12)
    for i,(key,title,x,w) in enumerate([('drive_state','内部驾驶状态',16,252),('shift_reason','最近一次换挡原因',290,252),('v7_render_rpm','IONIQ 发声RPM',565,252),('v7_root_hz','IONIQ root / Hz',840,252)]):
        g.comment(p,key+'-title',title,x,415,w,24,12)
        g.comment(p,key,'—',x,440,w,28,13)
        setter=g.add(p,key+'-setter','prepend set');g.wire(p,router,setter,so=4+i);g.wire(p,setter,key)
    g.comment(p,'save-status','保存回执：尚未请求；关闭窗口前请完成核验。',16,480,780,32,11)
    ss=g.add(p,'save-status-set','prepend set');g.wire(p,router,ss,so=8);g.wire(p,ss,'save-status')
    b=g.add(p,'verify-save','核验保存 / Verify',cls='textbutton',outs=3,rect=[832,480,260,30],presentation=1,presentation_rect=[832,480,260,30])
    m=g.add(p,'verify-command','verify_profile_sound',cls='message',ins=2);g.wire(p,b,m);g.wire(p,m,'out')
    # Clear profile-specific readouts when another engine is selected.
    r=g.add(p,'lab-profile','route profile',outs=2);g.wire(p,'in',r)
    clear=g.add(p,'lab-clear','set —',cls='message',ins=2);g.wire(p,r,clear)
    for key in ('drive_state','shift_reason','v7_render_rpm','v7_root_hz'):g.wire(p,clear,key)
    return d

def extend_console(d):
    p=d['patcher'];g.get(p,maxclass='tab')['tabs'].append('Mix Lab / 核验')
    select=g.get(p,text='sel 0 1 2 3 4');select.update(text='sel 0 1 2 3 4 5',numoutlets=7)
    bp=g.add(p,'v7-lab-page',cls='bpatcher',name='Patcher:/patchers/v7_lab_console.maxpat',varname='v7_lab_page',rect=[20,95,1120,590],presentation=1,presentation_rect=[20,55,1120,590],hidden=1)
    g.wire(p,g.get(p,maxclass='inlet')['id'],bp);g.wire(p,bp,g.get(p,maxclass='outlet')['id'])
    pages=['drive_page','mix_page','design_page','v7_tone_page','v7_response_page','v7_lab_page']
    for b in g.boxes(p):
        text=b.get('text','')
        if b['maxclass']=='message' and text.startswith('script sendbox drive_page hidden '):
            b['text']+=', script sendbox v7_lab_page hidden 1'
    m=g.add(p,'v7-lab-tab',', '.join(f'script sendbox {v} hidden {int(i!=5)}' for i,v in enumerate(pages)),cls='message',ins=2)
    g.wire(p,select['id'],m,so=5);g.wire(p,m,g.get(p,text='thispatcher')['id'])
    return d

def add_storage_receipts(d):
    p=d['patcher']
    for i,b in enumerate(list(g.boxes(p))):
        if not b.get('text','').startswith('pattrstorage '):continue
        name=b['text'].split()[1]
        route=g.add(p,'v7-write-route'+str(i),'route write',outs=2)
        tag=g.add(p,'v7-write-tag'+str(i),'prepend v7_storage_notice '+name)
        send=g.add(p,'v7-write-send'+str(i),'s vss.v7.storage.notice',outs=0)
        g.wire(p,b['id'],route);g.wire(p,route,tag);g.wire(p,tag,send)
    return d

def finalize(outputs, root, expose_params):
    def read(rel):return json.loads(outputs[rel])
    def store(rel,doc):outputs[rel]=json.dumps(doc,ensure_ascii=False,indent=2)+'\n'
    owners=json.loads(outputs['assets/v7/state_owners.json'])
    contracts=state_contracts(owners)
    store('assets/v7/state_contracts.json',contracts)
    # Single generated contract also reaches the ES5 save verifier.
    js=outputs['code/v7_profile_state.js']
    js=js.replace('var OWNER_CONTRACTS = {}; // generated', 'var OWNER_CONTRACTS = '+json.dumps(contracts,ensure_ascii=False)+';')
    outputs['code/v7_profile_state.js']=js
    store('gen/v7_meter.gendsp',expose_params(g.gen(meter_code(),2,4)))
    store('patchers/v7_lab_console.maxpat',lab())
    store('patchers/v7_runtime_console.maxpat',extend_console(read('patchers/v7_runtime_console.maxpat')))
    for profile in PROFILES:
        rel=f'patchers/v7_vehicle_engine_{profile}~.maxpat';d=read(rel);p=d['patcher']
        ctrl=next(b['id'] for b in g.boxes(p) if b.get('text','').startswith('v7_engine_controller_'))
        speed=g.add(p,'v7-speed-route','routepass speed_kph',outs=2);g.wire(p,ctrl,speed)
        g.wire(p,speed,'v7-mass');g.wire(p,speed,'v7-balance')
        meter=g.add(p,'v7-meter','gen~ @gen Patcher:/gen/v7_meter.gendsp',ins=2,outs=4)
        for ch in (0,1):g.wire(p,'v7-balance',meter,so=ch,di=ch)
        send=g.add(p,'v7-meter-feedback',f's vss.runtime.feedback.{profile}',outs=0)
        for i,(key,*_) in enumerate(BANDS):snapshot(p,meter,i,key,send,'v7-meter-'+str(i))
        store(rel,d)
        rel=f'patchers/v7_profile_runtime_host_{profile}.maxpat';d=read(rel);p=d['patcher']
        receiver=g.add(p,'v7-receipts','r vss.v7.storage.notice',ins=0);g.wire(p,receiver,'v7-state')
        # Prime save tracking before the same command fans out to native owners.
        for i,src in enumerate([b['id'] for b in g.boxes(p) if b['maxclass']=='inlet' or b.get('text')==f'r vss.runtime.control.{profile}' or b.get('text','').startswith('audio_enable 0, throttle 0.')]):
            old=[e['patchline'] for e in p['lines'] if e['patchline']['source']==[src,0]]
            p['lines']=[e for e in p['lines'] if e['patchline']['source']!=[src,0]]
            t=g.add(p,'v7-command-order'+str(i),'t l l',outs=2);g.wire(p,src,t);g.wire(p,t,'v7-state',so=1)
            for e in old:
                if e['destination'][0]!='v7-state':g.wire(p,t,e['destination'][0],di=e['destination'][1])
        filt=g.get(p,id='v7-filter');old_last=filt['numoutlets']-1
        for e in p['lines']:
            if e['patchline']['source']==[filt['id'],old_last]:e['patchline']['source'][1]+=1
        filt['text']+=' verify_profile_sound';filt['numoutlets']+=1
        store(rel,d)
    # Audio-rate telemetry for IONIQ: do not calculate a second competing pitch in JS.
    rel='gen/v7_ioniq6n_powertrain_v4.gendsp';d=read(rel);p=d['patcher']
    cb=next(b for b in g.boxes(p) if b['maxclass']=='codebox');cb['code']+='\nout5=repair_rpm; out6=root; // read-only renderer telemetry\n';cb['numoutlets']=6;cb['outlettype']=['']*6
    for i in (4,5):
        ident=g.add(p,'v7-monitor-out'+str(i),f'out {i+1}',outs=0,rect=[700+(i-4)*100,650,90,22]);g.wire(p,cb['id'],ident,so=i)
    store(rel,d)
    rel='patchers/v7_ioniq6n_powertrain_v4~.maxpat';d=read(rel);p=d['patcher']
    gen=next(b for b in g.boxes(p) if b.get('text','').startswith('gen~'))
    gen.update(numoutlets=6,outlettype=['signal']*6)
    send=g.add(p,'v7-pitch-feedback','s vss.runtime.feedback.ioniq6n',outs=0)
    snapshot(p,gen['id'],4,'v7_render_rpm',send,'v7-render');snapshot(p,gen['id'],5,'v7_root_hz',send,'v7-root')
    store(rel,d)
    for rel in list(outputs):
        if rel.startswith('patchers/v7_') and rel.endswith('.maxpat'):store(rel,add_storage_receipts(read(rel)))
    project=read('EV-Engine-V7.maxproj')
    project['contents']['code']['gen/v7_meter.gendsp']={'kind':'gendsp','local':1}
    project['contents']['patchers']['patchers/v7_lab_console.maxpat']={'kind':'patcher','local':1}
    project['contents']['data']['assets/v7/state_contracts.json']={'kind':'data','local':1}
    store('EV-Engine-V7.maxproj',project)
    return outputs
