/* V7 explicit per-engine snapshot. No driving/solo/audio values are persisted.
 * File writes are verified by reopening; the last valid snapshot is kept as .bak.
 * Other native pattrstorage owners remain independently versioned (v7_ prefix).
 */
autowatch=1;
outlets=2;
var profile=typeof jsarguments!=='undefined' ? String(jsarguments[1]) : 'ev';
var SCHEMA = {"v7_enable": {"min": 0, "max": 1, "default": 1, "label": "V7 处理 / Enable", "help": "0=旧源曲线与旧驾驶策略；1=V7。切换前停车并静音；输出安全保护始终保留。", "owner": "all"}, "v7_core_db": {"min": -12, "max": 3, "default": -3, "label": "主阶次 / Core trim (dB)", "help": "只调主阶次/压力核心，不是总音量。0=原比例；负值给其他层让位；不要强制所有谐波等响。", "owner": "source"}, "v7_pitch_relief": {"min": 0, "max": 1, "default": 0.7, "label": "IONIQ 拉转 / Pitch relief", "help": "仅 IONIQ：0=原高转速压缩曲线；1=解除高段压缩。启动/低转区不变；不改遥测 RPM。", "owner": "ioniq-source"}, "v7_attack_ms": {"min": 10, "max": 180, "default": 65, "label": "负载渐入 / Attack τ (ms)", "help": "音频负载一阶包络时间常数；约 2.2τ 为10–90%上升时间。不会延迟真实油门/车速数据。", "owner": "source"}, "v7_release_ms": {"min": 80, "max": 800, "default": 280, "label": "收油延续 / Release τ (ms)", "help": "音频主体释放时间常数；不是刹车减速度。过大则拖尾，过小则点按突兀。", "owner": "source"}, "v7_lift_range_db": {"min": 3, "max": 12, "default": 6, "label": "IONIQ 牵引跨度 / Load span (dB)", "help": "仅 IONIQ：运行区内部驱动增益的稳态牵引/滑行跨度；不是整车响度保证。怠速保持旧曲线。", "owner": "ioniq-source"}, "v7_sub_db": {"min": -60, "max": 0, "default": -18, "label": "深低频 / Sub source (dB)", "help": "独立约35–85 Hz声源，不随档位上移；-60=精确关闭。随DNA推子/solo/运行门控；不是独立LFE输出。", "owner": "bed"}, "v7_foundation_db": {"min": -60, "max": 0, "default": -20, "label": "固定重量 / Foundation (dB)", "help": "独立约90–190 Hz重量。-60=关闭；与随RPM走的Body不同。先削重复结构，再少量增加。", "owner": "bed"}, "v7_weight_trim_db": {"min": -12, "max": 0, "default": -6, "label": "IONIQ 旧底床 / Old weight (dB)", "help": "仅 IONIQ：削减旧DNA与Soundscape两处新增中低频底床；0=不削减。避免重复填满200–400Hz。", "owner": "ioniq-weight"}, "v7_body_db": {"min": -9, "max": 6, "default": 0, "label": "主体平衡 / 90–200 Hz (dB)", "help": "连续DNA+Soundscape总线的宽频段增益，不改变振荡器频率；0=旁通该段。", "owner": "balance"}, "v7_cavity_db": {"min": -12, "max": 3, "default": -2, "label": "腔体平衡 / 200–450 Hz (dB)", "help": "声源总线宽频段整理，非实车测量校正。过满先下调，勿一口气削光音色主根频。", "owner": "balance"}, "v7_mechanical_db": {"min": -9, "max": 6, "default": 0, "label": "纹理平衡 / 450–2000 Hz (dB)", "help": "连续声源机械/存在感宽频段；不是精确部件stem。其他层太强时先降低它们。", "owner": "balance"}, "v7_brightness_db": {"min": -12, "max": 6, "default": 0, "label": "亮度增益 / >2 kHz (dB)", "help": "明确的高频宽架增益；+6≈2倍幅值，-6≈半幅。不能生成原本不存在的高频；不同于旧Brightness 0–1形状。", "owner": "balance"}, "v7_comp_threshold_db": {"min": -36, "max": -6, "default": -18, "label": "总线阈值 / Threshold (dBFS)", "help": "V7立体声联动RMS压缩阈值；只有超过软拐点才压缩。不是响度目标，不是硬件保护阈值。", "owner": "dynamics"}, "v7_comp_ratio": {"min": 1, "max": 6, "default": 2, "label": "压缩比 / Ratio (:1)", "help": "1=不压缩；2=阈值以上每增加2dB仅输出1dB。默认不补偿增益，避免越压越响。", "owner": "dynamics"}, "v7_comp_attack_ms": {"min": 2, "max": 100, "default": 20, "label": "压缩进入 / Attack τ (ms)", "help": "V7增益衰减时间常数，毫秒；与旧OMX对数rate不同。太短可能磨平冲击。", "owner": "dynamics"}, "v7_comp_release_ms": {"min": 50, "max": 800, "default": 180, "label": "压缩释放 / Release τ (ms)", "help": "V7增益恢复时间常数；过短抽吸，过长使后续声层暂时被压低。", "owner": "dynamics"}, "v7_output_trim_db": {"min": -18, "max": 0, "default": -3, "label": "V7 余量 / Output trim (dB)", "help": "在原Main Master之外的候选版本安全余量；上限0，不靠大补偿增益救混音。", "owner": "dynamics"}, "v7_order2_db": {"min": -12, "max": 3, "default": 0, "label": "次阶次 A / Order A (dB)", "help": "0=原比例；-6约半幅。EV为2f，V10/V12/Ferrari为h2，IONIQ为1.5×root；不是总线EQ。", "owner": "source", "introduced_in": 2}, "v7_order3_db": {"min": -12, "max": 3, "default": 0, "label": "次阶次 B / Order B (dB)", "help": "0=原比例；-6约半幅。EV为约3f双侧分量，V10/V12/Ferrari为h3，IONIQ为2.25×root。", "owner": "source", "introduced_in": 2}, "v7_speed_weight_db": {"min": 0, "max": 6, "default": 0, "label": "高速重量保持 / Speed mass (dB)", "help": "只提升独立Sub+Foundation。60km/h以下0；60–140平滑增长；140以上为设定dB。0=不额外补偿。", "owner": "bed", "introduced_in": 2}, "v7_speed_edge_db": {"min": -6, "max": 0, "default": 0, "label": "高速高频约束 / Speed edge (dB)", "help": "连续DNA+SC的2kHz高架附加量。60–140km/h渐进；0=不补偿，-6=高速最多约半幅。", "owner": "balance", "introduced_in": 2}};
var OWNER_CONTRACTS = {"ev": [{"file": "ev_profile.json", "storage": null, "owner": "V7"}, {"file": "ev_module_mixer_noise_v1.json", "storage": "module_mixer_ev", "owner": "Mix"}, {"file": "ev_vehicle_bus_eq.json", "storage": "vehicle_bus_eq_ev", "owner": "EQ"}, {"file": "ev_start_v3.json", "storage": "start_ev_v3", "owner": "Start"}, {"file": "ev_noise_v1.json", "storage": "noise_ev_v1", "owner": "Noise"}, {"file": "ev_sound_dna.json", "storage": "ev_sound_dna", "owner": "DNA"}, {"file": "ev_soundscape_v5.json", "storage": "soundscape_ev_v5", "owner": "Soundscape"}, {"file": "ev_pop_v4.json", "storage": "ev_pop_v4", "owner": "Pop"}], "v10": [{"file": "v10_profile.json", "storage": null, "owner": "V7"}, {"file": "v10_module_mixer_noise_v1.json", "storage": "module_mixer_v10", "owner": "Mix"}, {"file": "v10_vehicle_bus_eq.json", "storage": "vehicle_bus_eq_v10", "owner": "EQ"}, {"file": "v10_start_v3.json", "storage": "start_v10_v3", "owner": "Start"}, {"file": "v10_noise_v1.json", "storage": "noise_v10_v1", "owner": "Noise"}, {"file": "v10_sound_dna_v3.json", "storage": "v10_sound_dna_v3", "owner": "DNA"}, {"file": "v10_soundscape_v5.json", "storage": "soundscape_v10_v5", "owner": "Soundscape"}, {"file": "v10_pop_v4.json", "storage": "v10_pop_v4", "owner": "Pop"}], "v12": [{"file": "v12_profile.json", "storage": null, "owner": "V7"}, {"file": "v12_module_mixer_noise_v1.json", "storage": "module_mixer_v12", "owner": "Mix"}, {"file": "v12_vehicle_bus_eq.json", "storage": "vehicle_bus_eq_v12", "owner": "EQ"}, {"file": "v12_start_v3.json", "storage": "start_v12_v3", "owner": "Start"}, {"file": "v12_noise_v1.json", "storage": "noise_v12_v1", "owner": "Noise"}, {"file": "v12_sound_dna_v3.json", "storage": "v12_sound_dna_v3", "owner": "DNA"}, {"file": "v12_soundscape_v5.json", "storage": "soundscape_v12_v5", "owner": "Soundscape"}, {"file": "v12_pop_v4.json", "storage": "v12_pop_v4", "owner": "Pop"}], "ioniq6n": [{"file": "ioniq6n_profile.json", "storage": null, "owner": "V7"}, {"file": "ioniq6n_module_mixer_noise_v1.json", "storage": "module_mixer_ioniq6n", "owner": "Mix"}, {"file": "ioniq6n_vehicle_bus_eq.json", "storage": "vehicle_bus_eq_ioniq6n", "owner": "EQ"}, {"file": "ioniq6n_start_v3.json", "storage": "start_ioniq6n_v3", "owner": "Start"}, {"file": "ioniq6n_noise_v1.json", "storage": "noise_ioniq6n_v1", "owner": "Noise"}, {"file": "ioniq6n_sound_dna_v4.json", "storage": "ioniq6n_sound_dna_v4", "owner": "DNA"}, {"file": "ioniq6n_soundscape_modes_v3.json", "storage": "soundscape_ioniq6n_modes_v3", "owner": "Soundscape"}, {"file": "ioniq6n_pop_v4.json", "storage": "ioniq6n_pop_v4", "owner": "Pop"}], "ferrari": [{"file": "ferrari_profile.json", "storage": null, "owner": "V7"}, {"file": "ferrari_realism_v2_module_mixer_noise_v1.json", "storage": "module_mixer_ferrari", "owner": "Mix"}, {"file": "ferrari_vehicle_bus_eq.json", "storage": "vehicle_bus_eq_ferrari", "owner": "EQ"}, {"file": "ferrari_start_v3.json", "storage": "start_ferrari_v3", "owner": "Start"}, {"file": "ferrari_noise_v2.json", "storage": "noise_ferrari_v2", "owner": "Noise"}, {"file": "ferrari_sound_dna_v5.json", "storage": "ferrari_sound_dna_v5", "owner": "DNA"}, {"file": "ferrari_soundscape_v7.json", "storage": "soundscape_ferrari_v7", "owner": "Soundscape"}, {"file": "ferrari_pop_v3.json", "storage": "ferrari_pop_v3", "owner": "Pop"}]};
var state={}, initialized=false, pending=null, verifyTask=null;
var saveRequested=false, receipts={}, numericSaved=false;
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
function validDocument(doc,p){
    if(!doc || doc.schema_version!==7 || doc.profile!==p || !doc.values || typeof doc.values!=='object' || Array.isArray(doc.values))return false;
    if(doc.schema_revision!==undefined && doc.schema_revision!==1 && doc.schema_revision!==2)return false;
    var k,v,revision=doc.schema_revision||1;
    for(k in doc.values)if(Object.prototype.hasOwnProperty.call(doc.values,k) && !Object.prototype.hasOwnProperty.call(SCHEMA,k))return false;
    for(k in SCHEMA)if(Object.prototype.hasOwnProperty.call(SCHEMA,k)){
        if(!Object.prototype.hasOwnProperty.call(doc.values,k)){
            if(revision===1 && SCHEMA[k].introduced_in===2)continue;
            return false;
        }
        v=doc.values[k];
        if(typeof v!=='number'||!isFinite(v)||v<SCHEMA[k].min||v>SCHEMA[k].max)return false;
        if(k==='v7_enable' && v!==0 && v!==1)return false;
    }
    return true;
}
function validTree(x){
    if(typeof x==='number')return isFinite(x);
    if(!x || typeof x!=='object')return true;
    for(var k in x)if(Object.prototype.hasOwnProperty.call(x,k) && !validTree(x[k]))return false;
    return true;
}
function validOwner(doc,c){
    if(c.storage===null)return validDocument(doc,profile);
    var ps=doc && doc.pattrstorage, slot=ps && ps.slots && ps.slots['1'], data=slot && slot.data;
    if(!ps || ps.name!==c.storage || !data || typeof data!=='object' || Array.isArray(data) || !validTree(data))return false;
    for(var k in data)if(Object.prototype.hasOwnProperty.call(data,k))return true;
    return false;
}
function read(path){
    var f=new File(v7ReadPath(path), 'read'),s='';if(!f.isopen)return null;
    while(f.position<f.eof)s+=f.readstring(65536);f.close();
    try{return JSON.parse(s);}catch(e){return null;}
}
function write(path,doc){
    var f=new File(path,'write','TEXT');if(!f.isopen)throw new Error('Cannot write '+path);
    f.eof=0;f.writestring(JSON.stringify(doc,null,2));f.close();
    var check=v7ReadPhysical(path);if(JSON.stringify(check)!==JSON.stringify(doc))throw new Error('Readback differs '+path);
}
function status(text){if(typeof outlet!=='undefined')outlet(1,'v7_status',text);}
function emit(){for(var k in state)if(Object.prototype.hasOwnProperty.call(state,k)){
    outlet(0,k,state[k]);outlet(1,k,state[k]);
}}
function restore(){
    var p=paths(profile,this.patcher.filepath),factory=read(p.factory);
    if(!validDocument(factory,profile)){status('ERROR: V7 factory missing/invalid; audio remains user-controlled OFF');return;}
    var local=v7ReadPhysical(p.local),backup=v7ReadPhysical(p.local+'.bak');
    var binding=v7ReadPhysical(p.local.replace('/presets/local/v7_','/presets/v7_bindings/'));
    var chosen=validDocument(local,profile)?local:validDocument(backup,profile)?backup:validDocument(binding,profile)?binding:factory;
    state=bounded(chosen.values,factory.values);initialized=true;emit();
    status(chosen===factory?'V7 factory loaded / 出厂候选':chosen===backup?'Recovered V7 backup / 已恢复备份':chosen===binding?'Published binding loaded / 已载入发布音色':'V7 profile loaded / 已载入本车设置');
}
function saveStatus(text){if(typeof outlet!=='undefined')outlet(1,'v7_save_status',text);}
function verifyOwners(){
    var c=OWNER_CONTRACTS[profile]||[],r=root(this.patcher.filepath),valid=0,confirmed=0,missing=[],unconfirmed=[],i,d;
    for(i=0;i<c.length;i++){
        d=v7ReadPhysical(r+'/presets/local/v7_'+c[i].file);
        if(validOwner(d,c[i])){
            valid++;
            if(saveRequested && (i===0?numericSaved:receipts[c[i].storage]))confirmed++;
            else unconfirmed.push(c[i].owner);
        }else missing.push(c[i].owner);
    }
    var complete=c.length===8 && confirmed===8 && valid===8;
    saveStatus(complete?'8/8 文件有效，收到本次保存回执；仍需 Max 关闭重开听评。':
        '有效文件 '+valid+'/8；本次回执 '+confirmed+'/8'+(missing.length?'；缺失/无效 '+missing.join(','):'')+
        (unconfirmed.length?'；未确认 '+unconfirmed.join(','):'')+'。不是完整保存确认。');
    return {valid:valid,confirmed:confirmed,complete:complete,missing:missing,unconfirmed:unconfirmed};
}
function storageNotice(args){
    if(!saveRequested || !args.length)return;
    var name=String(args[0]),c=OWNER_CONTRACTS[profile]||[],i;
    for(i=1;i<c.length;i++)if(c[i].storage===name){
        // Message shape varies by Max version. Explicit failure is never success.
        // A notice only counts together with a valid physical slot-1 file.
        for(var j=1;j<args.length;j++){
            if(typeof args[j]==='number' && args[j]===0){receipts[name]=false;return;}
            if(typeof args[j]==='string' && /\.json$/i.test(args[j]) && String(args[j]).replace(/\\/g,'/').split('/').pop()!=='v7_'+c[i].file){receipts[name]=false;return;}
        }
        receipts[name]=true;return;
    }
}
function save(){
    saveRequested=true;receipts={};numericSaved=false;
    if(verifyTask)verifyTask.cancel();
    if(!initialized){status('Save blocked: profile not initialized');return;}
    var p=paths(profile,this.patcher.filepath),old=v7ReadPhysical(p.local);
    var doc={schema_version:7,schema_revision:2,profile:profile,base_commit:'fed2b78ecfabc84d673207b3a5f714b89f76720f',values:bounded(state,state)};
    try{
        if(validDocument(old,profile))write(p.local+'.bak',old);
        write(p.local,doc);numericSaved=true;
        status('V7 numeric snapshot verified / 数值已校验；请看 Mix Lab 的8项保存核验');
        saveStatus('正在收集模块回执；尚未确认完整音色保存。');
        verifyTask=new Task(function(){verifyTask=null;verifyOwners.call(this);},this);verifyTask.schedule(1200);
    }catch(e){status('SAVE ERROR: '+String(e));saveStatus('数值保存失败；不得当作完整保存。');}
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
    if(n==='verify_profile_sound')return verifyOwners.call(this);
    if(n==='v7_storage_notice')return storageNotice(a);
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

// Physical-only JSON read: appended AFTER fallback rewriting by the generator.
// Verification and last-good backup must never resolve to a published binding.
function v7ReadPhysical(path){
    var f=new File(path,'read'),s='';if(!f.isopen)return null;
    if(f.eof>4194304){f.close();return null;}
    while(f.position<f.eof){var part=f.readstring(65536);if(!part.length){f.close();return null;}s+=part;}
    f.close();try{return JSON.parse(s);}catch(e){return null;}
}
