"""Small Max graph construction utilities with explicit in/out port contracts."""
import copy,json

def patch(w=1120,h=610):
 return {'patcher':dict(fileversion=1,appversion={'major':8,'minor':6,'revision':5,'architecture':'x64','modernui':1},classnamespace='box',rect=[50.,50.,w,h],openinpresentation=1,default_fontname='Arial',default_fontsize=12.,boxes=[],lines=[])}
def add(p,ident,text=None,cls='newobj',ins=1,outs=1,rect=None,**attrs):
 assert not any(e['box']['id']==ident for e in p['boxes']),ident
 o={'id':ident,'maxclass':cls,'numinlets':ins,'numoutlets':outs,'patching_rect':rect or [20.,800.+len(p['boxes'])*24,200.,22.],**attrs}
 if text is not None:o['text']=text
 p['boxes'].append({'box':o});return ident

def wire(p,s,d,so=0,di=0):p['lines'].append({'patchline':{'source':[s,so],'destination':[d,di]}})
def boxes(p):return [e['box'] for e in p['boxes']]
def get(p,**kw):
 found=[b for b in boxes(p) if all(b.get(k)==v for k,v in kw.items())]
 if len(found)!=1:raise ValueError((kw,len(found)))
 return found[0]
def gen(code,inputs=1,outputs=2):
 d=patch(960,720);p=d['patcher'];p['classnamespace']='dsp.gen';p['openinpresentation']=0
 add(p,'code',cls='codebox',ins=inputs,outs=outputs,rect=[40.,40.,780.,580.],code=code)
 for i in range(inputs):
  add(p,f'in{i}',f'in {i+1}',ins=0,rect=[40.+i*95,10.,80.,22.]);wire(p,f'in{i}','code',di=i)
 for i in range(outputs):
  add(p,f'out{i}',f'out {i+1}',outs=0,rect=[40.+i*95,650.,80.,22.]);wire(p,'code',f'out{i}',so=i)
 return d

def receive(p,dest,names,profile='#1',prefix='v7'):
 r=add(p,prefix+'-recv',f'r vss.v7.params.{profile}',ins=0)
 route=add(p,prefix+'-route','routepass '+' '.join(names),outs=len(names)+1)
 wire(p,r,route)
 for i in range(len(names)):wire(p,route,dest,so=i)

def comment(p,ident,text,x,y,w,h=24,size=12):
 return add(p,ident,text,cls='comment',outs=0,rect=[x,y,w,h],presentation=1,presentation_rect=[x,y,w,h],fontsize=size,textcolor=[.86,.9,.96,1.],linecount=max(1,int(h/15)))

def control_page(params,schema,title,desc):
 d=patch();p=d['patcher'];p['bgcolor']=[.065,.085,.12,1.]
 inlet=add(p,'in',cls='inlet',ins=0,rect=[0,700,25,25]);out=add(p,'out',cls='outlet',outs=0,rect=[1090,700,25,25])
 comment(p,'title',title,16,10,1080,26,18)
 comment(p,'description',desc,16,38,1080,30,11)
 route=add(p,'readback','route '+' '.join(params)+ ' v7_status v7_gr_db v7_clip_samples profile',outs=len(params)+5);wire(p,inlet,route)
 for i,name in enumerate(params):
  s=schema[name];col=i%2;row=i//2;x=16+col*550;y=76+row*87
  add(p,'panel-'+name,cls='panel',ins=1,outs=0,rect=[x,y,536,81],presentation=1,presentation_rect=[x,y,536,81],bgcolor=[.11,.14,.19,1.],rounded=8)
  comment(p,'label-'+name,s['label'],x+10,y+4,403,23,13)
  add(p,name,cls='flonum',ins=1,outs=2,rect=[x+424,y+6,100,23],presentation=1,presentation_rect=[x+424,y+6,100,23],minimum=s['min'],maximum=s['max'],format=6,varname=name,hint=s['help'],annotation=s['help'],bgcolor=[.18,.23,.31,1.],textcolor=[.9,.96,1.,1.])
  tag=add(p,'tag-'+name,'prepend '+name);wire(p,name,tag);wire(p,tag,out)
  setn=add(p,'set-'+name,'prepend set');wire(p,route,setn,so=i);wire(p,setn,name)
  comment(p,'help-'+name,f"{s['min']:g}…{s['max']:g}  |  "+s['help'],x+10,y+31,514,44,11)
  if s['owner'].startswith('ioniq'):
   sel=add(p,'only-'+name,'sel ioniq6n',outs=2);wire(p,route,sel,so=len(params)+3)
   for j in range(2):
    m=add(p,f'active-{name}-{j}',f'ignoreclick {j}',cls='message',ins=2);wire(p,sel,m,so=j);wire(p,m,name)
 # Save commands have one owner at runtime; no user interaction writes audio/drive state.
 for i,(cmd,label) in enumerate([('save_profile_sound','保存当前发动机 / Save'),('reload_profile_sound','重载 / Reload'),('reset_profile_sound','恢复出厂 / Factory')]):
  b=add(p,'button'+str(i),label,cls='textbutton',outs=3,rect=[16+i*235,523,222,28],presentation=1,presentation_rect=[16+i*235,523,222,28],hint='作用于当前发动机的V7参数与DNA/SC/Noise/Start/Pop/EQ/Mix；不会存储音频开关/油门/solo。')
  m=add(p,'action'+str(i),cmd,cls='message',ins=2);wire(p,b,m);wire(p,m,out)
 comment(p,'status','等待发动机状态 / Select one engine; audio starts OFF',16,560,1080,28,12)
 s=add(p,'status-set','prepend set');wire(p,route,s,so=len(params));wire(p,s,'status')
 for j,(key,label) in enumerate([('v7_gr_db','RMS GR (dB)'),('v7_clip_samples','Emergency clip samples')]):
  comment(p,key+'-label',label,733,514+j*27,232,23,11)
  add(p,key,cls='flonum',outs=2,rect=[970,514+j*27,110,23],presentation=1,presentation_rect=[970,514+j*27,110,23],ignoreclick=1,format=6)
  s=add(p,key+'-set','prepend set');wire(p,route,s,so=len(params)+1+j);wire(p,s,key)
 return d
