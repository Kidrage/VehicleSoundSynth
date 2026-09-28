/* V7 explicit per-engine snapshot. No driving/solo/audio values are persisted.
 * File writes are verified by reopening; the last valid snapshot is kept as .bak.
 * Other native pattrstorage owners remain independently versioned (v7_ prefix).
 */
autowatch=1;
outlets=2;
var profile=typeof jsarguments!=='undefined' ? String(jsarguments[1]) : 'ev';
var SCHEMA = {"v7_enable": {"min": 0, "max": 1, "default": 1, "label": "V7 处理 / Enable", "help": "0=旧源曲线与旧驾驶策略；1=V7。切换前停车并静音；输出安全保护始终保留。", "owner": "all"}, "v7_core_db": {"min": -12, "max": 3, "default": -3, "label": "主阶次 / Core trim (dB)", "help": "只调主阶次/压力核心，不是总音量。0=原比例；负值给其他层让位；不要强制所有谐波等响。", "owner": "source"}, "v7_pitch_relief": {"min": 0, "max": 1, "default": 0.7, "label": "IONIQ 拉转 / Pitch relief", "help": "仅 IONIQ：0=原高转速压缩曲线；1=解除高段压缩。启动/低转区不变；不改遥测 RPM。", "owner": "ioniq-source"}, "v7_attack_ms": {"min": 10, "max": 180, "default": 65, "label": "负载渐入 / Attack τ (ms)", "help": "音频负载一阶包络时间常数；约 2.2τ 为10–90%上升时间。不会延迟真实油门/车速数据。", "owner": "source"}, "v7_release_ms": {"min": 80, "max": 800, "default": 280, "label": "收油延续 / Release τ (ms)", "help": "音频主体释放时间常数；不是刹车减速度。过大则拖尾，过小则点按突兀。", "owner": "source"}, "v7_lift_range_db": {"min": 3, "max": 12, "default": 6, "label": "IONIQ 牵引跨度 / Load span (dB)", "help": "仅 IONIQ：运行区内部驱动增益的稳态牵引/滑行跨度；不是整车响度保证。怠速保持旧曲线。", "owner": "ioniq-source"}, "v7_sub_db": {"min": -60, "max": 0, "default": -18, "label": "深低频 / Sub source (dB)", "help": "独立约35–85 Hz声源，不随档位上移；-60=精确关闭。随DNA推子/solo/运行门控；不是独立LFE输出。", "owner": "bed"}, "v7_foundation_db": {"min": -60, "max": 0, "default": -20, "label": "固定重量 / Foundation (dB)", "help": "独立约90–190 Hz重量。-60=关闭；与随RPM走的Body不同。先削重复结构，再少量增加。", "owner": "bed"}, "v7_weight_trim_db": {"min": -12, "max": 0, "default": -6, "label": "IONIQ 旧底床 / Old weight (dB)", "help": "仅 IONIQ：削减旧DNA与Soundscape两处新增中低频底床；0=不削减。避免重复填满200–400Hz。", "owner": "ioniq-weight"}, "v7_body_db": {"min": -9, "max": 6, "default": 0, "label": "主体平衡 / 90–200 Hz (dB)", "help": "连续DNA+Soundscape总线的宽频段增益，不改变振荡器频率；0=旁通该段。", "owner": "balance"}, "v7_cavity_db": {"min": -12, "max": 3, "default": -2, "label": "腔体平衡 / 200–450 Hz (dB)", "help": "声源总线宽频段整理，非实车测量校正。过满先下调，勿一口气削光音色主根频。", "owner": "balance"}, "v7_mechanical_db": {"min": -9, "max": 6, "default": 0, "label": "纹理平衡 / 450–2000 Hz (dB)", "help": "连续声源机械/存在感宽频段；不是精确部件stem。其他层太强时先降低它们。", "owner": "balance"}, "v7_brightness_db": {"min": -12, "max": 6, "default": 0, "label": "亮度增益 / >2 kHz (dB)", "help": "明确的高频宽架增益；+6≈2倍幅值，-6≈半幅。不能生成原本不存在的高频；不同于旧Brightness 0–1形状。", "owner": "balance"}, "v7_comp_threshold_db": {"min": -36, "max": -6, "default": -18, "label": "总线阈值 / Threshold (dBFS)", "help": "V7立体声联动RMS压缩阈值；只有超过软拐点才压缩。不是响度目标，不是硬件保护阈值。", "owner": "dynamics"}, "v7_comp_ratio": {"min": 1, "max": 6, "default": 2, "label": "压缩比 / Ratio (:1)", "help": "1=不压缩；2=阈值以上每增加2dB仅输出1dB。默认不补偿增益，避免越压越响。", "owner": "dynamics"}, "v7_comp_attack_ms": {"min": 2, "max": 100, "default": 20, "label": "压缩进入 / Attack τ (ms)", "help": "V7增益衰减时间常数，毫秒；与旧OMX对数rate不同。太短可能磨平冲击。", "owner": "dynamics"}, "v7_comp_release_ms": {"min": 50, "max": 800, "default": 180, "label": "压缩释放 / Release τ (ms)", "help": "V7增益恢复时间常数；过短抽吸，过长使后续声层暂时被压低。", "owner": "dynamics"}, "v7_output_trim_db": {"min": -18, "max": 0, "default": -3, "label": "V7 余量 / Output trim (dB)", "help": "在原Main Master之外的候选版本安全余量；上限0，不靠大补偿增益救混音。", "owner": "dynamics"}};
var state={}, initialized=false, pending=null, verifyTask=null;
function root(path){return String(path||'').replace(/\\/g,'/').replace(/\/[^/]*$/,'').replace(/\/patchers$/,'');}
function paths(p,path){var r=root(path);return {local:r+'/presets/local/v7_'+p+'_profile.json',factory:r+'/presets/v7_factories/'+p+'_profile.json'};}
function bounded(values,defaults){
    var result={}, k, v;
    for(k in SCHEMA)if(Object.prototype.hasOwnProperty.call(SCHEMA,k)){
        v=values && values[k];
        if(typeof v!=='number'||!isFinite(v))v=defaults[k];
        if(typeof v!=='number'||!isFinite(v))v=SCHEMA[k].default;
        result[k]=Math.max(SCHEMA[k].min,Math.min(SCHEMA[k].max,v));
        if(k==='v7_enable')result[k]=result[k]>=0.5?1:0;
    }
    return result;
}
function validDocument(doc,p){return doc && doc.schema_version===7 && doc.profile===p && doc.values && typeof doc.values==='object' && !Array.isArray(doc.values);}
function read(path){
    var f=new File(v7ReadPath(path), 'read'),s='';if(!f.isopen)return null;
    while(f.position<f.eof)s+=f.readstring(65536);f.close();
    try{return JSON.parse(s);}catch(e){return null;}
}
function write(path,doc){
    var f=new File(path,'write','TEXT');if(!f.isopen)throw new Error('Cannot write '+path);
    f.eof=0;f.writestring(JSON.stringify(doc,null,2));f.close();
    var check=read(path);if(JSON.stringify(check)!==JSON.stringify(doc))throw new Error('Readback differs '+path);
}
function status(text){if(typeof outlet!=='undefined')outlet(1,'v7_status',text);}
function emit(){for(var k in state)if(Object.prototype.hasOwnProperty.call(state,k)){
    outlet(0,k,state[k]);outlet(1,k,state[k]);
}}
function restore(){
    var p=paths(profile,this.patcher.filepath),factory=read(p.factory);
    if(!validDocument(factory,profile)){status('ERROR: V7 factory missing/invalid; audio remains user-controlled OFF');return;}
    var local=read(p.local),backup=read(p.local+'.bak');
    var chosen=validDocument(local,profile)?local:validDocument(backup,profile)?backup:factory;
    state=bounded(chosen.values,factory.values);initialized=true;emit();
    status(chosen===factory?'V7 factory loaded / 出厂候选':chosen===backup?'Recovered V7 backup / 已恢复备份':'V7 profile loaded / 已载入本车设置');
}
function save(){
    if(!initialized){status('Save blocked: profile not initialized');return;}
    var p=paths(profile,this.patcher.filepath),old=read(p.local);
    var doc={schema_version:7,profile:profile,base_commit:'fed2b78ecfabc84d673207b3a5f714b89f76720f',values:bounded(state,state)};
    try{
        if(validDocument(old,profile))write(p.local+'.bak',old);
        write(p.local,doc);
        status('V7 parameters saved + verified / V7参数已写入校验；模块保存已另行请求');
    }catch(e){status('SAVE ERROR: '+String(e));}
}
function reset(){
    var p=paths(profile,this.patcher.filepath),factory=read(p.factory);
    if(!validDocument(factory,profile)){status('RESET ERROR: factory missing');return;}
    state=bounded(factory.values,{});initialized=true;emit();
    status('Factory recalled; Save to bind / 已恢复出厂，保存后绑定');
}
function loadbang(){
    if(pending)pending.cancel();
    pending=new Task(function(){pending=null;restore.call(this);},this);pending.schedule(450);
}
function anything(){
    var n=String(messagename),a=typeof arrayfromargs==='undefined'?[]:arrayfromargs(arguments);
    if(n==='save_profile_sound')return save.call(this);
    if(n==='reload_profile_sound')return restore.call(this);
    if(n==='reset_profile_sound')return reset.call(this);
    if(n==='v7_query'){if(initialized)emit();return;}
    if(!Object.prototype.hasOwnProperty.call(SCHEMA,n))return;
    if(!initialized){status('Please wait for V7 factory/local restore');return;}
    if(SCHEMA[n].owner.indexOf('ioniq')===0 && profile!=='ioniq6n'){status('This control applies only to IONIQ / 仅IONIQ生效');return;}
    var v=Number(a[0]);if(!isFinite(v)){status('Rejected non-finite parameter');return;}
    var one={};one[n]=v;state=bounded(one,state);
    outlet(0,n,state[n]);outlet(1,n,state[n]);status('Modified; Save to bind / 已修改，保存绑定此发动机');
}
function notifydeleted(){if(pending)pending.cancel();if(verifyTask)verifyTask.cancel();}
if(typeof module!=='undefined' && module.exports)module.exports={bounded:bounded,paths:paths,validDocument:validDocument,schema:SCHEMA};

/* Read-only published tone binding fallback. Writes always remain presets/local/v7_*.
 * No V6 local file is imported. Native pattrstorage client paths remain unchanged.
 */
function v7PhysicalExists(path){var f=new File(path,'read'),found=f.isopen;if(found)f.close();return found;}
function v7ReadPath(path){
    path=String(path);
    if(path.indexOf('/presets/local/v7_')>=0 && !v7PhysicalExists(path)){
        var binding=path.replace('/presets/local/v7_','/presets/v7_bindings/');
        if(v7PhysicalExists(binding))return binding;
    }
    return path;
}
