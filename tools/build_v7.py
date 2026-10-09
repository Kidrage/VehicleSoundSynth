#!/usr/bin/env python3
"""Build isolated V7 resources from preserved V6 seeds; never rewrite original designers.
Run in EV-Engine-V7 only. V7 copies are seed-protected after the first build unless
--refresh-generated is explicitly given and their previous hashes still match.
"""
from __future__ import annotations
import argparse,copy,hashlib,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from tools.v7 import graph as g, kernels, drive, review
from tools.v7.schema import PARAMS,PROFILES,defaults
from tools.v7.helptext import explain

BASE='fed2b78ecfabc84d673207b3a5f714b89f76720f'
ROOT_NAMES={'ev':'EV','v10':'V10','v12':'V12','ioniq6n':'IONIQ6N','ferrari':'Ferrari'}
SOURCE_NAMES={'ev':'ev_powertrain','v10':'v10_dna_source_v3','v12':'v12_dna_source_v3','ioniq6n':'ioniq6n_powertrain_v4','ferrari':'ferrari_dna_source_v5'}

def load(path):return json.loads((ROOT/path).read_text())
def canonical(doc):return json.dumps(doc,ensure_ascii=False,indent=2)+'\n'
def sha(text):return hashlib.sha256(text.encode()).hexdigest()
def walk_boxes(p):
 for b in g.boxes(p):
  yield b
  if 'patcher' in b:yield from walk_boxes(b['patcher'])

def refs(doc):
 out=set()
 for b in walk_boxes(doc['patcher']):
  text=b.get('text','');name=b.get('name','')
  if b.get('maxclass')=='bpatcher':
   short=name.split('/')[-1]
   if (ROOT/'patchers'/short).is_file():out.add('patchers/'+short)
  for typ,fn in re.findall(r'Patcher:/(patchers|code|gen)/([^\s"\,]+)',text+' '+name):
   rel=f'{typ}/{fn}'
   if (ROOT/rel).is_file():out.add(rel)
  if b.get('maxclass')=='newobj' and text:
   first=text.split()[0];fn=first if first.endswith('.maxpat') else first+'.maxpat'
   if (ROOT/'patchers'/fn).is_file():out.add('patchers/'+fn)
 return out

def closure():
 queue=[f'VehicleSoundSynth-{n}.maxpat' for n in ROOT_NAMES.values()]+['patchers/runtime_console.maxpat']
 found=set()
 while queue:
  rel=queue.pop()
  if rel in found:continue
  found.add(rel)
  if rel.endswith('.maxpat'):queue.extend(refs(load(rel))-found)
 return found

def outpath(rel):
 p=Path(rel)
 if len(p.parts)==1:return f'EV-Engine-V7-{p.stem.replace("VehicleSoundSynth-","")}.maxpat'
 return str(p.parent/('v7_'+p.name))

def rename_doc(doc,mapping):
 d=copy.deepcopy(doc)
 for b in walk_boxes(d['patcher']):
  for key in ('text','name'):
   if key not in b:continue
   text=b[key]
   for src,dst in mapping.items():
    text=text.replace('Patcher:/'+src,'Patcher:/'+dst)
   if key=='text' and b.get('maxclass')=='newobj' and text:
    parts=text.split(' ',1);token=parts[0];rel='patchers/'+(token if token.endswith('.maxpat') else token+'.maxpat')
    if rel in mapping:
     b.setdefault('varname',Path(rel).stem)
     parts[0]=Path(mapping[rel]).name if token.endswith('.maxpat') else Path(mapping[rel]).stem
     text=' '.join(parts)
   elif key=='name' and b.get('maxclass')=='bpatcher':
    short=b[key].split('/')[-1]
    if 'patchers/'+short in mapping:text='Patcher:/'+mapping['patchers/'+short]
    # Stable pattrstorage client paths must not change when an abstraction file is versioned.
    old=b[key].split('/')[-1]
    if old.endswith('.maxpat'):b.setdefault('varname',old[:-7])
   if key=='text' and re.fullmatch(r'expr pow\(10\.,\s*\$f1\s*/\s*20\.\)',text):
    text='expr ($f1 > -60.) * pow(10., $f1/20.)'
   b[key]=text
  # Read-only deep annotations; normalized shape controls are not fake physical dB.
  if b.get('presentation') and b.get('maxclass') not in ('comment','panel','bpatcher'):
   name=b.get('varname','');base=name.replace('legacy_','').replace('dna_','')
   if 'brightness' in name:
    helptext=('Legacy Brightness 0–1：只影响旧源混合分支，V10/V12在高转区可能几乎无效；用Main V7亮度dB调实际高频。' if name.startswith('legacy_') else
              'Brightness 0–1 是该源的归一化音色形状，不是音量；EV还改变逆变器阶次位置。Main V7亮度dB才是明确的高架增益。')
   elif name:
    bounds=f"{b.get('minimum','见标注')}…{b.get('maximum','见标注')}"
    helptext=f'{name} | 范围 {bounds}。改变此模块而非整车总音量；需对应声层启用。保存当前发动机写入V7隔离状态。'
   else:
    helptext=b.get('text','操作/显示')+'：作用于当前选择的发动机。音频默认关闭；状态只读反馈不会重新触发控制。'
   b['hint']=explain(name,b) or helptext;b['annotation']=b['hint']
 # Trace unlabeled numeric controls to the actual outgoing selector.
 p=d['patcher'];by={b['id']:b for b in g.boxes(p)}
 for b in g.boxes(p):
  if b.get('presentation') and b.get('maxclass') in ('flonum','number','slider','dial','toggle'):
   todo=[(b['id'],0)];seen=set();helptext=explain(b.get('varname',''),b)
   while todo and not helptext:
    ident,depth=todo.pop(0)
    if ident in seen or depth>7:continue
    seen.add(ident);t=by[ident].get('text','')
    if t.startswith('prepend '):helptext=explain(t.split()[1],b)
    if not helptext:
     todo.extend((e['patchline']['destination'][0],depth+1) for e in p['lines'] if e['patchline']['source'][0]==ident)
   if helptext:b['hint']=helptext;b['annotation']=helptext
 return d

def inject_actions(p,dest,state_id=None):
 inlet=next(b['id'] for b in g.boxes(p) if b['maxclass']=='inlet')
 router=g.add(p,'v7-owner-actions','route dna_save dna_reload dna_reset',outs=4)
 for edge in p['lines']:
  if edge['patchline']['source']==[inlet,0]:edge['patchline']['source']=[router,3]
 g.wire(p,inlet,router)
 for i,action in enumerate(('save','restore','reset')):
  msg=g.add(p,'v7-owner-'+action,action,cls='message',ins=2);g.wire(p,router,msg,so=i);g.wire(p,msg,dest)

def replace_source_wrappers(doc,rel):
 p=doc['patcher']
 for b in list(g.boxes(p)):
  text=b.get('text','')
  for profile,stem in SOURCE_NAMES.items():
   if text==f'gen~ @gen Patcher:/gen/v7_{stem}.gendsp':
    g.receive(p,b['id'],kernels.SOURCE_PARAMS,profile,prefix='v7-source')
  if 'gen~ @gen Patcher:/gen/v7_ioniq6n_weight_bed.gendsp'==text:
   g.receive(p,b['id'],['v7_enable','v7_weight_trim_db'],'ioniq6n',prefix='v7-old-weight')
 if rel in ('patchers/ev_sound_dna~.maxpat','patchers/ioniq6n_sound_dna_v4~.maxpat'):
  state=next(b['id'] for b in g.boxes(p) if b.get('text','').startswith('js ') and 'state' in b['text'])
  # Existing IONIQ may already have dna_reset only; duplicate reset has no audible effect,
  # but avoid multiple writers by deleting the old single action route for these selectors.
  existing=[b for b in g.boxes(p) if b.get('text','')=='route dna_save dna_reload dna_reset']
  if not existing:inject_actions(p,state)
 return doc

def add_owner_fanout(p):
 inlet=next(b['id'] for b in g.boxes(p) if b['maxclass']=='inlet')
 router=g.add(p,'v7-all-owner-actions','route save_profile_sound reload_profile_sound reset_profile_sound',outs=4);g.wire(p,inlet,router)
 # Route into controller exactly once; SC/EQ already owned by original action fanout.
 controller=next(b['id'] for b in g.boxes(p) if b.get('text','').startswith('v7_engine_controller_'))
 for i,action in enumerate(('save','reload','reset')):
  msg=g.add(p,'v7-owner-fanout-'+action,', '.join(f'{stem}_{action}' for stem in ('dna','noise','start','backfire','event')),cls='message',ins=2)
  g.wire(p,router,msg,so=i);g.wire(p,msg,controller)

def engine(doc,profile):
 p=doc['patcher'];add_owner_fanout(p)
 # One new mass voice per engine, following the existing Main DNA fader and same solo gate.
 dna=next(b for b in g.boxes(p) if b.get('text','') in
  [f'v7_{profile}_sound_dna~',f'v7_{profile}_sound_dna_v3~','v7_ioniq6n_sound_dna_v4~','v7_ferrari_acoustic_v5~'])
 bed=g.add(p,'v7-mass',f'gen~ @gen Patcher:/gen/v7_mass_{profile}.gendsp',outs=1)
 g.receive(p,bed,kernels.BED_PARAMS,profile,prefix='v7-mass-controls')
 ctrl=next(b['id'] for b in g.boxes(p) if b.get('text','').startswith('v7_engine_controller_'))
 state_names=['rpm','throttle','load','engine_running','shift_cut','powertrain_level_db']
 router=g.add(p,'v7-mass-state','routepass '+' '.join(state_names),outs=len(state_names)+1);g.wire(p,ctrl,router)
 for i in range(len(state_names)):g.wire(p,router,bed,so=i)
 # Route independent mass into the continuous sum only, not back into legacy cabin_rumble.
 # It shares the DNA solo coefficient but does not excite a second rumble generator.
 solos=[]
 for ch in (0,1):
  edge=next(e['patchline'] for e in p['lines'] if e['patchline']['source']==[dna['id'],ch])
  solo=edge['destination'][0];assert g.get(p,id=solo).get('text')=='*~';solos.append(solo)
 solo_ctrl=next(e['patchline']['source'] for e in p['lines'] if e['patchline']['destination']==[solos[0],1])
 bedsolo=g.add(p,'v7-mass-solo','*~',ins=2);g.wire(p,bed,bedsolo);g.wire(p,solo_ctrl[0],bedsolo,so=solo_ctrl[1],di=1)
 for ch,solo in enumerate(solos):
  edges=[e['patchline'] for e in p['lines'] if e['patchline']['source']==[solo,0] and
         g.get(p,id=e['patchline']['destination'][0]).get('text')=='+~']
  assert len(edges)==1,(profile,'continuous sum')
  target=edges[0]['destination'];summ=g.add(p,f'v7-mass-sum{ch}','+~',ins=2)
  edges[0]['destination']=[summ,0];g.wire(p,bedsolo,summ,di=1);g.wire(p,summ,target[0],di=target[1])
 # Balance acts only on continuous DNA+SC, before starts/Pop/noise/cabin FX.
 sc=next(b for b in g.boxes(p) if 'cinematic_soundscape_host' in b.get('text',''))
 sums=[]
 for ch in (0,1):
  first=next(e['patchline']['destination'][0] for e in p['lines'] if e['patchline']['source']==[sc['id'],ch])
  second=next(e['patchline']['destination'][0] for e in p['lines'] if e['patchline']['source']==[first,0])
  assert g.get(p,id=second).get('text')=='+~';sums.append(second)
 bal=g.add(p,'v7-balance','gen~ @gen Patcher:/gen/v7_balance.gendsp',ins=2,outs=2)
 g.receive(p,bal,kernels.BALANCE_PARAMS,profile,prefix='v7-balance-controls')
 for ch,src in enumerate(sums):
  edges=[e['patchline'] for e in p['lines'] if e['patchline']['source']==[src,0]]
  assert len(edges)==1;edges[0]['source']=[bal,ch];g.wire(p,src,bal,di=ch)
 # The new dynamics abstraction ignores old OMX UI rates, which are hidden in V7 Mix.
 master=next(b for b in g.boxes(p) if b.get('text')=='v7_mix_master~')
 master['text']='v7_mix_master~ '+profile
 return doc

def master():
 d=g.patch(1000,720);p=d['patcher'];p['openinpresentation']=0
 for i in range(3):g.add(p,f'in{i}',cls='inlet',ins=0,rect=[40+i*120,40,30,22])
 comp=g.add(p,'comp','gen~ @gen Patcher:/gen/v7_dynamics.gendsp',ins=2,outs=3)
 g.wire(p,'in1',comp);g.wire(p,'in2',comp,di=1);g.receive(p,comp,kernels.DYNAMICS_PARAMS,prefix='v7-comp')
 lim=g.add(p,'lim','omx.peaklim~',ins=2,outs=4);g.wire(p,comp,lim);g.wire(p,comp,lim,so=1,di=1)
 guard=g.add(p,'guard','gen~ @gen Patcher:/gen/v7_clip_counter.gendsp',ins=2,outs=4)
 g.wire(p,lim,guard);g.wire(p,lim,guard,so=1,di=1)
 for ch in (0,1):
  o=g.add(p,f'out{ch}',cls='outlet',outs=0,rect=[100+ch*300,600,30,22]);g.wire(p,guard,o,so=ch)
 sender=g.add(p,'feedback','s vss.runtime.feedback.#1',outs=0)
 for ident,src,port,key in [('gr',comp,2,'v7_gr_db'),('clips',guard,2,'v7_clip_samples')]:
  snap=g.add(p,ident+'snap','snapshot~ 100',ins=2);tag=g.add(p,ident+'tag','prepend '+key)
  g.wire(p,src,snap,so=port);g.wire(p,snap,tag);g.wire(p,tag,sender)
 g.comment(p,'note','V7 RMS dB/ms compressor → preserved peak limiter → emergency clip counter. NOT true-peak or physical speaker protection.',30,15,930,35)
 return d

def host(doc,profile):
 p=doc['patcher']
 state=g.add(p,'v7-state',f'js Patcher:/code/v7_profile_state.js {profile}',outs=2)
 sender=g.add(p,'v7-params',f's vss.v7.params.{profile}',outs=0)
 g.wire(p,state,sender)
 feedback=next(b['id'] for b in g.boxes(p) if b.get('text')==f's vss.runtime.feedback.{profile}')
 g.wire(p,state,feedback,so=1)
 # Listen to the same command inlet without reinjecting drive/GUI readback into it.
 inlet=next(b['id'] for b in g.boxes(p) if b['maxclass']=='inlet')
 rx=next(b['id'] for b in g.boxes(p) if b.get('text')==f'r vss.runtime.control.{profile}')
 g.wire(p,inlet,state);g.wire(p,rx,state)
 # Close/select auto-save also reaches the isolated V7 state owner (not telemetry).
 for b in list(g.boxes(p)):
  if b.get('text','').startswith('audio_enable 0, throttle 0.'):
   g.wire(p,b['id'],state)
 # Prevent unknown V7 controls from leaking into engine/drivetrain and Gen objects.
 old=next(b for b in g.boxes(p) if b.get('text','').startswith('route audio_enable '))
 filterid=g.add(p,'v7-filter','routepass '+' '.join(PARAMS)+' v7_query',outs=len(PARAMS)+2)
 incoming=[e['patchline'] for e in p['lines'] if e['patchline']['destination']==[old['id'],0]]
 for edge in incoming:edge['destination']=[filterid,0]
 g.wire(p,filterid,old['id'],so=len(PARAMS)+1)
 # v7_enable reaches model directly regardless of held/external audio context.
 route=g.add(p,'v7-driver-param','routepass v7_enable',outs=2);g.wire(p,state,route)
 driver=next(b['id'] for b in g.boxes(p) if b.get('text')==f'v7_drive_simulator_{profile}')
 g.wire(p,route,driver)
 # Startup loadbang is explicit because js loadbang support must not be inferred.
 lb=next(b['id'] for b in g.boxes(p) if b.get('text')=='loadbang')
 msg=g.add(p,'v7-initialize','loadbang',cls='message',ins=2);g.wire(p,lb,msg);g.wire(p,msg,state)
 return doc

def console(doc):
 p=doc['patcher'];tab=g.get(p,maxclass='tab');tab['tabs']+=['V7 Tone / 频段定稿','V7 Response / 动态']
 tab['presentation_rect'][2]=1080;tab['patching_rect'][2]=1080
 sel=g.get(p,text='sel 0 1 2');sel['text']='sel 0 1 2 3 4';sel['numoutlets']=6
 inlet=g.get(p,maxclass='inlet')['id'];outlet=g.get(p,maxclass='outlet')['id'];tp=g.get(p,text='thispatcher')['id']
 pages=['drive_page','mix_page','design_page','v7_tone_page','v7_response_page']
 for i,(var,fn) in enumerate(zip(pages[3:],['v7_tone_console.maxpat','v7_response_console.maxpat'])):
  ident=g.add(p,'v7-page'+str(i),cls='bpatcher',name='Patcher:/patchers/'+fn,varname=var,rect=[20,95,1120,590],presentation=1,presentation_rect=[20,55,1120,590],hidden=1)
  g.wire(p,inlet,ident);g.wire(p,ident,outlet)
 for i in range(5):
  text=', '.join(f'script sendbox {page} hidden {int(j!=i)}' for j,page in enumerate(pages))
  if i<3:g.get(p,id=f'obj-{11+i}')['text']=text
  else:
   msg=g.add(p,'v7-tab'+str(i),text,cls='message',ins=2);g.wire(p,sel['id'],msg,so=i);g.wire(p,msg,tp)
 p['bgcolor']=[.065,.085,.12,1.];g.get(p,id='obj-1')['text']='EV-ENGINE V7 | DRIVE · MIX · DESIGN · TONE · RESPONSE'
 return doc

def style_console(doc):
 p=doc['patcher'];p['bgcolor']=[.065,.085,.12,1.]
 for b in g.boxes(p):
  if not b.get('presentation'):continue
  if b['maxclass']=='comment':b['textcolor']=[.84,.9,.97,1.]
  elif b['maxclass'] in ('number','flonum','message','textbutton','umenu'):
   b['bgcolor']=[.15,.20,.28,1.];b['textcolor']=[.93,.97,1.,1.]
 return doc

def mixpage(doc):
 p=doc['patcher']
 # Keep original mix/EQ controls, but remove the misleading, inactive legacy compressor panel.
 for b in g.boxes(p):
  # Original compressor presentation occupies y=350..470; its only live authority was OMX.
  rect=b.get('presentation_rect',[])
  if b.get('presentation') and rect and rect[1]>=350 and rect[1]<490:
   b['hidden']=1
 g.get(p,id='obj-25')['text']='Noise / 独立噪声层 [dB]'
 g.get(p,id='obj-128')['text']='Factory / 恢复出厂'
 g.comment(p,'v7-comp-note','V7 动态已移至 Response 页：阈值 dBFS / 压缩比 / attack-release 毫秒。旧 OMX rate 不再作为 V7 控件。',20,368,1060,46,14)
 g.comment(p,'v7-mix-note','混音次序：先减 Core 或 200–450 Hz 过强部分 → 调独立 Sub / Foundation → 最后设 Master 与压缩。-60 dB DNA/Noise = 关闭。',20,425,1060,48,13)
 return doc

def main(doc,mapping):
 d=rename_doc(doc,mapping);p=d['patcher']
 for b in g.boxes(p):
  text=b.get('text','')
  for suffix in ROOT_NAMES.values():text=text.replace(f'loadunique VehicleSoundSynth-{suffix}.maxpat',f'loadunique EV-Engine-V7-{suffix}.maxpat')
  if 'text' in b:b['text']=text
  if b['maxclass']=='comment':b['textcolor']=[.82,.88,.95,1.]
  if b['maxclass']=='textbutton':b['bgcolor']=[.16,.22,.30,1.];b['textcolor']=[.91,.97,1.,1.]
 g.get(p,id='obj-1')['text']='EV-ENGINE-V7  |  声音设计 · 驾驶响应 · 混音定稿'
 g.get(p,id='obj-1')['fontsize']=23
 g.get(p,id='obj-1').update(presentation=1,presentation_rect=[30,12,1180,33])
 g.get(p,id='obj-2')['text']='五款独立发动机 · 当前音色保存绑定本车 · V7 Tone / Response 可直接调音 · 音频启动默认 OFF'
 g.get(p,id='obj-2').update(presentation=1,presentation_rect=[30,48,1180,31])
 for i,ident in enumerate(['obj-7','obj-13','obj-19','obj-25','obj-31','obj-36']):
  b=g.get(p,id=ident);b.update(presentation_rect=[30+(i%3)*395,90+(i//3)*39,380,30],bgcolor=[.16,.22,.30,1.],textcolor=[.92,.97,1.,1.],fontsize=14)
 g.get(p,id='obj-31')['text']='Open Ferrari SF90 / 声学演绎'
 bp=g.get(p,id='obj-38');bp['presentation_rect']=[30,178,1180,660]
 g.get(p,id='obj-58')['text']='候选版本：本机 Max 与实车听评尚待验收。仅开启一个发动机；请先低音量试听。唯一操作说明：V7_MANUAL.md'
 g.get(p,id='obj-58').update(presentation=1,presentation_rect=[30,850,1180,44])
 p['bgcolor']=[.04,.055,.085,1.];p['rect']=[50,50,1240,910]
 return d

def with_bindings(text):
 # Only read operations may resolve into tracked bindings. No broad path-rewrite on write.
 text=re.sub(r"new File\(([^;\n]+?),\s*(['\"])read\2\)",lambda m:"new File(v7ReadPath("+m[1]+"), 'read')",text)
 text=re.sub(r"outlet\(0,\s*(['\"])read\1,\s*([^;\n]+)\);",lambda m:"outlet(0, 'read', v7ReadPath("+m[2]+"));",text)
 return text+(ROOT/'tools/v7/binding_helpers.js.template').read_text()

def expose_params(doc):
 p=doc['patcher'];code='\n'.join(b.get('code','') for b in g.boxes(p))
 known={b['text'].split()[1] for b in g.boxes(p) if b.get('text','').startswith('param ')}
 for name,args in re.findall(r'\bParam (\w+)\(([^;]+)\);',code):
  if name in known:continue
  fields=[x.strip() for x in args.split(',')];text='param '+name+' '+fields[0]
  for v in fields[1:]:
   k,val=v.split('=');text+=' @'+k.strip()+' '+val.strip()
  g.add(p,'v7-param-'+name,text,ins=0,rect=[900,20+len(known)*24,320,22]);known.add(name)
 return doc

def build():
 needed=closure();mapping={rel:outpath(rel) for rel in sorted(needed)};outputs={}
 # Factories are fresh copies; no original local preset is automatically imported.
 for f in sorted((ROOT/'presets').glob('*.json')):
  outputs['presets/v7_factories/'+f.name]=f.read_text()
 for profile in PROFILES:
  outputs[f'presets/v7_factories/{profile}_profile.json']=canonical({'schema_version':7,'schema_revision':2,'profile':profile,'base_commit':BASE,'values':defaults(profile)})
 for rel in sorted(needed):
  dst=mapping[rel]
  if rel.endswith('.js'):
   text=(ROOT/rel).read_text()
   # Fresh namespace for every owner. Factory directories also carry V7 bindings.
   text=text.replace('/presets/local/','/__V7_LOCAL__/').replace('/presets/','/presets/v7_factories/').replace('/__V7_LOCAL__/','/presets/local/v7_')
   if rel=='code/drive_model.js':text=drive.build((ROOT/rel).read_text())
   outputs[dst]=text
  elif rel.endswith('.maxpat'):
   doc=rename_doc(load(rel),mapping)
   doc=replace_source_wrappers(doc,rel)
   for profile in PROFILES:
    if rel==f'patchers/vehicle_engine_{profile}~.maxpat':doc=engine(doc,profile)
    if rel==f'patchers/profile_runtime_host_{profile}.maxpat':doc=host(doc,profile)
   if rel=='patchers/runtime_console.maxpat':doc=console(doc)
   if rel=='patchers/mix_eq_console.maxpat':doc=mixpage(doc)
   if rel.endswith(('_console.maxpat','/soundscape_control.maxpat')):doc=style_console(doc)
   if rel!='patchers/mix_master~.maxpat':outputs[dst]=canonical(doc)
  elif rel.endswith('.gendsp'):
   doc=load(rel)
   for profile,stem in SOURCE_NAMES.items():
    if rel==f'gen/{stem}.gendsp':
     b=next(b for b in walk_boxes(doc['patcher']) if b.get('maxclass')=='codebox')
     b['code']=kernels.source_kernel(b['code'],profile)
   if rel=='gen/ioniq6n_weight_bed.gendsp':
    b=next(b for b in walk_boxes(doc['patcher']) if b.get('maxclass')=='codebox')
    b['code']=kernels.declarations(['v7_enable','v7_weight_trim_db'])+b['code']+'\nout1=out1*pow(10,v7_weight_trim_db*slide(v7_enable,samplerate*.04,samplerate*.04)/20);\n'
   outputs[dst]=canonical(doc)
 # EV primitive state had no reset/factory. Add a factory based on tracked source defaults.
 evcode=next(b['code'] for b in walk_boxes(load('gen/ev_powertrain.gendsp')['patcher']) if b.get('maxclass')=='codebox')
 evparams={m[0]:float(m[1]) for m in re.findall(r'Param (\w+)\(([-.\d]+)',evcode)}
 evdata={b['varname']:[evparams[b['varname'][4:]]] for b in walk_boxes(load('patchers/ev_sound_dna~.maxpat')['patcher']) if b.get('varname','').startswith('dna_')}
 outputs['presets/v7_factories/ev_sound_dna_factory.json']=canonical({'pattrstorage':{'name':'ev_sound_dna','slots':{'99':{'data':evdata}}}})
 # Override only the primitive EV state, with explicit recall after the native read completion delay.
 outputs['code/v7_dna_state_path.js']=(ROOT/'tools/v7/simple_dna_state.js.template').read_text()
 outputs['code/v7_profile_state.js']=(ROOT/'tools/v7/profile_state.js.template').read_text().replace('var SCHEMA = {}; // generated from tools/v7/schema.py','var SCHEMA = '+json.dumps(PARAMS,ensure_ascii=False)+';')
 for profile in PROFILES:outputs[f'gen/v7_mass_{profile}.gendsp']=canonical(g.gen(kernels.bed(profile),1,1))
 outputs['gen/v7_balance.gendsp']=canonical(g.gen(kernels.balance(),2,2))
 outputs['gen/v7_dynamics.gendsp']=canonical(g.gen(kernels.dynamics(),2,3))
 outputs['gen/v7_clip_counter.gendsp']=canonical(g.gen(kernels.clip_counter(),2,4))
 outputs['patchers/v7_mix_master~.maxpat']=canonical(master())
 tone=['v7_enable','v7_core_db','v7_pitch_relief','v7_weight_trim_db','v7_sub_db','v7_foundation_db','v7_body_db','v7_cavity_db','v7_mechanical_db','v7_brightness_db']
 response=[n for n in PARAMS if n not in tone and n not in review.LAB_PARAMS]
 outputs['patchers/v7_tone_console.maxpat']=canonical(g.control_page(tone,PARAMS,'V7 TONE | 音色身份与频段平衡','先减过强主阶次与重复腔体，再补低频。新参数按发动机保存；这些是宽频段工程起点，不是实车自动校准。'))
 outputs['patchers/v7_response_console.maxpat']=canonical(g.control_page(response,PARAMS,'V7 RESPONSE | 负载包络与总线动态','毫秒为时间常数 τ，不是旧OMX rate。负载包络不修改CAN/驾驶遥测；V7=0仅回退源/驾驶策略，安全链仍保留。'))
 outputs['main.maxpat']=canonical(main(load('assets/v7/main_v6_template.json'),mapping))
 outputs['assets/v7/parameter_contracts.json']=canonical({'schema_version':7,'parameters':PARAMS,'profile_defaults':{p:defaults(p) for p in PROFILES}})
 project=load('VehicleSoundSynth-V6.maxproj');project['name']='EV-Engine-V7'
 for category,entries in project['contents'].items():
  for key in list(entries):
   if key.endswith(('.docx','.pdf')) or key in ('V6_USER_GUIDE.md','V6_CANDIDATE_GUIDE.md','V6_RELEASE_HANDOFF.md'):del entries[key]
 for rel in outputs:
  if rel.endswith('.maxpat'):project['contents']['patchers'][rel]={'kind':'patcher','local':1}
  elif rel.endswith('.gendsp'):project['contents']['code'][rel]={'kind':'gendsp','local':1}
  elif rel.startswith('code/') and rel.endswith('.js'):project['contents']['code'][rel]={'kind':'javascript','local':1}
  elif rel.startswith('presets/') and rel.endswith('.json'):project['contents']['data'][rel]={'kind':'data','local':1}
 outputs['EV-Engine-V7.maxproj']=canonical(project)
 # Every V7 owner can load a published bound snapshot only when its local file is absent.
 for rel in list(outputs):
  if rel.startswith('code/') and '/presets/local/v7_' in outputs[rel]:outputs[rel]=with_bindings(outputs[rel])
  if rel.endswith('.gendsp'):outputs[rel]=canonical(expose_params(json.loads(outputs[rel])))
 owners={}
 for p in PROFILES:
  owners[p]=[p+'_profile.json',('ferrari_realism_v2' if p=='ferrari' else p)+'_module_mixer_noise_v1.json',
    p+'_vehicle_bus_eq.json',p+'_start_v3.json',p+('_noise_v2.json' if p=='ferrari' else '_noise_v1.json'),
    ('ioniq6n_sound_dna_v4.json' if p=='ioniq6n' else 'ferrari_sound_dna_v5.json' if p=='ferrari' else 'ev_sound_dna.json' if p=='ev' else p+'_sound_dna_v3.json'),
    ('ioniq6n_soundscape_modes_v3.json' if p=='ioniq6n' else 'ferrari_soundscape_v7.json' if p=='ferrari' else p+'_soundscape_v5.json'),
    p+('_pop_v3.json' if p=='ferrari' else '_pop_v4.json')]
 outputs['assets/v7/state_owners.json']=canonical(owners)
 # Clone manifest is reproducibility/protected-seed evidence, NOT a native runtime certificate.
 outputs['assets/v7/resource_map.json']=canonical({'base_commit':BASE,'mapping':mapping,'protected_seed_sha256':{rel:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() for rel in sorted(needed)},'active_entries':['main.maxpat']+[f'EV-Engine-V7-{n}.maxpat' for n in ROOT_NAMES.values()]})
 return review.finalize(outputs,ROOT,expose_params)

def main_cli():
 parser=argparse.ArgumentParser();parser.add_argument('--refresh-generated',action='store_true');parser.add_argument('--check',action='store_true');a=parser.parse_args()
 outputs=build();index=ROOT/'assets/v7/generated_sha256.json';previous=json.loads(index.read_text()) if index.exists() else {}
 conflicts=[]
 for rel,text in outputs.items():
  f=ROOT/rel
  if f.exists() and rel in previous and hashlib.sha256(f.read_bytes()).hexdigest()!=previous[rel] and f.read_text()!=text:conflicts.append(rel)
 if conflicts:raise SystemExit('Preserve user edits; reconcile before regeneration: '+', '.join(conflicts))
 if a.check:
  diff=[rel for rel,text in outputs.items() if not (ROOT/rel).exists() or (ROOT/rel).read_text()!=text]
  if diff:raise SystemExit('Generated resources differ: '+', '.join(diff))
  print('V7 reproducibility OK:',len(outputs));return
 if previous and not a.refresh_generated:raise SystemExit('Use --check or explicit --refresh-generated (still hash-guards local edits).')
 for rel,text in outputs.items():
  f=ROOT/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(text)
 index.write_text(canonical({rel:sha(text) for rel,text in outputs.items()}))
 print('Generated',len(outputs),'V7 resources; preserved',len(closure()),'V6 source seeds.')
if __name__=='__main__':main_cli()
