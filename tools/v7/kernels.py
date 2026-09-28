"""Native GenExpr source recipes. Numeric tests are not native Max acceptance."""
import re
from .schema import PARAMS

def declarations(names):
    return '\n'.join(f"Param {n}({PARAMS[n]['default']}, min={PARAMS[n]['min']}, max={PARAMS[n]['max']});" for n in names)+'\n'

SOURCE_PARAMS=['v7_enable','v7_core_db','v7_attack_ms','v7_release_ms','v7_pitch_relief','v7_lift_range_db','v7_weight_trim_db']

def source_kernel(code, profile):
    pre = declarations(SOURCE_PARAMS)+'''History v7_tenv(0); History v7_lenv(0);
v7_on = slide(v7_enable, samplerate*.04, samplerate*.04);
v7_tt = clamp(throttle,0,1);
v7_lt = abs(clamp(load,-1,1));
v7_tk = exp(-1/(samplerate*.001*(v7_tt>v7_tenv ? v7_attack_ms : v7_release_ms)));
v7_lk = exp(-1/(samplerate*.001*(v7_lt>v7_lenv ? v7_attack_ms : v7_release_ms)));
v7_tenv = v7_tt+(v7_tenv-v7_tt)*v7_tk;
v7_lenv = v7_lt+(v7_lenv-v7_lt)*v7_lk;
v7_core = pow(10,slide(v7_core_db,samplerate*.03,samplerate*.03)*v7_on/20);
'''
    # Hoist all original parameter declarations before the new audio envelope.
    # Ferrari appends versioned params late in its source, so insertion-at-last-Param
    # would otherwise make earlier expressions reference v7_on before assignment.
    declarations_old = re.findall(r"\bParam\s+\w+\([^;]+\);", code)
    code = re.sub(r"\bParam\s+\w+\([^;]+\);", "", code)
    code = "\n".join(declarations_old)+"\n"+pre+code
    def mod_line(var,expr):
        nonlocal code
        pattern=rf'(?m)^{re.escape(var)} = ([^;]+);'
        assert re.search(pattern,code),var
        code=re.sub(pattern,lambda m:f'{var} = ({m.group(1)})*(1-v7_on)+({expr})*v7_on;',code,count=1)
    if profile=='ioniq6n':
        for v in ('t_fast',):mod_line(v,'v7_tenv')
        for v in ('l_fast','l_slow'):mod_line(v,'v7_lenv')
        # Protect <2600RPM; decouple high-RPM compression strength from reference timbre repair.
        code=code.replace('repair_rpm = r-repair_mix*repair_compress;',
             'repair_rpm = r-repair_mix*repair_compress*(1-v7_on*v7_pitch_relief);')
        code=code.replace('order1 = cycle(root) *', 'order1 = v7_core * cycle(root) *')
        old='drive = clamp(0.11 + load_depth * (0.30*t_fast + 0.22*l_fast) + 0.10*l_slow, 0.08, 0.72);'
        assert old in code
        code=code.replace(old,old+'''
v7_runblend = clamp((r-1600)/1200,0,1);
v7_runblend = v7_on*v7_runblend*v7_runblend*(3-2*v7_runblend);
v7_drive_peak = clamp(.21+.52*load_depth,.08,.72);
v7_drive = v7_drive_peak*pow(10,-v7_lift_range_db*(1-clamp(.5*v7_tenv+.5*v7_lenv,0,1))/20);
drive = drive+(v7_drive-drive)*v7_runblend;''')
        code+='\nout3 = out3*pow(10,v7_weight_trim_db*v7_on/20);\nout4 = out4*pow(10,v7_weight_trim_db*v7_on/20);\n'
    elif profile=='ev':
        mod_line('t','v7_tenv');mod_line('l','v7_lenv')
        code=code.replace('coherent_low = cycle(f) *','coherent_low = v7_core * cycle(f) *')
    else:
        if re.search(r'(?m)^t = ',code):mod_line('t','v7_tenv')
        if re.search(r'(?m)^l = ',code):mod_line('l','v7_lenv')
        # Main new group response and preserved low-RPM path both receive sample-rate-independent envelope.
        if 'v3_effort =' in code:mod_line('v3_effort','max(v7_tenv,v7_lenv)')
        # Core trim is before editable Body/Cavity filters and old saturation output.
        # Attenuate the leading pressure partial, not the entire harmonic family.
        # Phase/timing remain intact; downstream Body and character retain their identity.
        pattern=r'(?m)^v3_h1 = ([^;]+);'
        assert re.search(pattern,code),profile
        code=re.sub(pattern,lambda m:'v3_h1 = ('+m.group(1)+')*v7_core;',code,count=1)
    return '// V7 VERSIONED SOURCE: original source is retained in gen/.\n'+code

BED_PARAMS=['v7_enable','v7_sub_db','v7_foundation_db','v7_attack_ms','v7_release_ms']
def bed(profile):
    f={'ev':(43,61,73,101,137,177),'v10':(46,63,78,108,146,182),'v12':(41,58,72,103,139,173),
       'ioniq6n':(45,62,76,105,143,179),'ferrari':(44,59,74,107,147,183)}[profile]
    return declarations(BED_PARAMS)+f'''
Param rpm(650,min=0,max=10000); Param throttle(0,min=0,max=1);
Param load(0,min=-1,max=1); Param engine_running(0,min=0,max=1);
Param shift_cut(1,min=0,max=1); Param powertrain_level_db(-4,min=-60,max=6);
History effort(0); History speed_env(0); History dc_x(0); History dc_y(0);
request = clamp(.6*throttle+.4*abs(load),0,1);
k = exp(-1/(samplerate*.001*(request>effort ? max(120,v7_attack_ms) : max(350,v7_release_ms))));
effort = request+(effort-request)*k;
speed_env = clamp(rpm/10000,0,1)+(speed_env-clamp(rpm/10000,0,1))*exp(-1/(samplerate*.8));
life = slide(engine_running,samplerate*.04,samplerate*.12);
enabled = slide(v7_enable,samplerate*.04,samplerate*.04);
// No oscillator follows the pitch CV. Small slow variation preserves LF at 3rd..8th gear.
modulation = .92+.08*cycle(4+effort*3);
sub = (cycle({f[0]}+effort*2+speed_env)*.50 + cycle({f[1]}+effort*2)*.30 + cycle({f[2]}+speed_env)*.20)*modulation;
body = cycle({f[3]}+effort*3)*.45+cycle({f[4]}+effort*2)*.32+cycle({f[5]}+speed_env*2)*.23;
subgain = slide(v7_sub_db<=-60 ? 0 : pow(10,v7_sub_db/20),samplerate*.03,samplerate*.03);
bodygain = slide(v7_foundation_db<=-60 ? 0 : pow(10,v7_foundation_db/20),samplerate*.03,samplerate*.03);
stemgain = slide(powertrain_level_db<=-60 ? 0 : pow(10,powertrain_level_db/20),samplerate*.035,samplerate*.035);
// Soft shift modulation retains mass rather than applying the full tonal torque dip twice.
raw = (sub*subgain+body*bodygain)*.20*(.45+.55*effort)*(.9+.1*shift_cut)*life*enabled*stemgain;
// First-order 28Hz high-pass; final car bass management is still external.
dc_y = raw-dc_x+exp(-6.283185307179586*28/samplerate)*dc_y;
dc_x = raw;
out1 = dc_y;
'''

BALANCE_PARAMS=['v7_enable','v7_body_db','v7_cavity_db','v7_mechanical_db','v7_brightness_db']
def balance():
    code=declarations(BALANCE_PARAMS)+'\nv7_on=slide(v7_enable,samplerate*.04,samplerate*.04);\n'
    inputs=['in1','in2']
    # Cookbook biquads, same coefficients on both channels. Gains are smoothed, never auto-normalized.
    for n,(param,freq,q,kind) in enumerate([
        ('v7_body_db',135,.7,'peak'),('v7_cavity_db',300,.8,'peak'),
        ('v7_mechanical_db',900,.65,'peak'),('v7_brightness_db',2000,1,'highshelf')]):
        s=f'b{n}'
        code+=f'{s}g=slide({param},samplerate*.035,samplerate*.035)*v7_on;\n{s}A=pow(10,{s}g/40);\n{s}w=6.283185307179586*{freq}/samplerate;\n{s}c=cos({s}w);\n{s}a=sin({s}w)/(2*{q});\n'
        if kind=='peak':
            code+=f'{s}a0=1+{s}a/{s}A;\n{s}b0=(1+{s}a*{s}A)/{s}a0;\n{s}b1=-2*{s}c/{s}a0;\n{s}b2=(1-{s}a*{s}A)/{s}a0;\n{s}a1={s}b1;\n{s}a2=(1-{s}a/{s}A)/{s}a0;\n'
        else:
            code+=f'''{s}alpha=sin({s}w)*sqrt(2)/2;
{s}beta=2*sqrt({s}A)*{s}alpha;
{s}a0=({s}A+1)-({s}A-1)*{s}c+{s}beta;
{s}b0={s}A*(({s}A+1)+({s}A-1)*{s}c+{s}beta)/{s}a0;
{s}b1=-2*{s}A*(({s}A-1)+({s}A+1)*{s}c)/{s}a0;
{s}b2={s}A*(({s}A+1)+({s}A-1)*{s}c-{s}beta)/{s}a0;
{s}a1=2*(({s}A-1)-({s}A+1)*{s}c)/{s}a0;
{s}a2=(({s}A+1)-({s}A-1)*{s}c-{s}beta)/{s}a0;
'''
        for ch in range(2):
            t=f'{s}ch{ch}'
            code+=f'''History {t}x1(0); History {t}x2(0); History {t}y1(0); History {t}y2(0);
{t}y={s}b0*{inputs[ch]}+{s}b1*{t}x1+{s}b2*{t}x2-{s}a1*{t}y1-{s}a2*{t}y2;
{t}x2={t}x1; {t}x1={inputs[ch]}; {t}y2={t}y1; {t}y1={t}y;
'''
            inputs[ch]=t+'y'
    return code+f'out1={inputs[0]};\nout2={inputs[1]};\n'

DYNAMICS_PARAMS=['v7_enable','v7_comp_threshold_db','v7_comp_ratio','v7_comp_attack_ms','v7_comp_release_ms','v7_output_trim_db']
def dynamics():
    return declarations(DYNAMICS_PARAMS)+'''
History power(0); History reduction(0);
// Feed-forward stereo-linked RMS detector (10ms power integration), 6dB soft knee.
p=max(in1*in1,in2*in2);
power=p+(power-p)*exp(-1/(samplerate*.010));
level=10*log10(max(power,1e-12));
over=level-v7_comp_threshold_db;
slope=1-1/max(v7_comp_ratio,1);
target=over<=-3 ? 0 : over>=3 ? slope*over : slope*(over+3)*(over+3)/12;
k=exp(-1/(samplerate*.001*(target>reduction ? v7_comp_attack_ms : v7_comp_release_ms)));
reduction=target+(reduction-target)*k;
on=slide(v7_enable,samplerate*.04,samplerate*.04);
trim=slide(v7_output_trim_db,samplerate*.04,samplerate*.04);
g=pow(10,(-min(reduction,36)*on+trim)/20);
out1=in1*g; out2=in2*g; out3=reduction*on;
'''

def clip_counter():
    return '''History clipped(0); History peak(0);
Param reset(0,min=0,max=1); History old_reset(0);
clipped=(reset>old_reset ? 0 : clipped)+((abs(in1)>.891 || abs(in2)>.891) ? 1 : 0);
old_reset=reset;
peak=max(max(abs(in1),abs(in2)),peak*.99995);
out1=clamp(in1,-.891,.891); out2=clamp(in2,-.891,.891);
out3=clipped; out4=peak;
'''
