/* Explicit V3 persistence. Never write V1/V2 files or import changed-meaning macros. */
autowatch = 1;
outlets = 1;
var profile = typeof jsarguments !== 'undefined' ? String(jsarguments[1]) : 'ferrari';
var pending = null;
var compatible = ['aggression','brightness','body','texture','air_detail',
    'cycle_irregularity','stereo_width','throttle_loudness_depth','saturation',
    'combustion_pulse','intake_detail','exhaust_detail','residual_detail',
    'idle_level','idle_body','idle_metal','idle_irregularity','idle_air','idle_width'];

function paths(p, patchPath) {
    var directory = String(patchPath).replace(/\/[^/]*$/, '').replace(/\/patchers$/, '');
    return {local:directory+'/presets/local/'+p+'_sound_dna_v3.json',
        factory:directory+'/presets/'+p+'_sound_dna_v3_factory.json',
        legacy:directory+'/presets/local/'+p+'_sound_dna_v2.json'};
}
function exists(path) {
    var file = new File(path,'read'), found = file.isopen;
    if (found) file.close();
    return found;
}
function migrate(data) {
    var result = {};
    for (var i=0;i<compatible.length;i++) {
        var name=compatible[i], value=data['dna_'+name];
        if (value && value.length && isFinite(Number(value[0]))) {
            result['legacy_'+name] = Math.max(0,Math.min(name==='throttle_loudness_depth'?8:1,Number(value[0])));
        }
    }
    return result;
}
function legacyValues(path) {
    var file=new File(path,'read'), text='';
    if (!file.isopen) return {};
    while(file.position<file.eof) text+=file.readline();
    file.close();
    try { return migrate(JSON.parse(text).pattrstorage.slots['1'].data); }
    catch(error) { post('DNA V3: invalid legacy state, keeping factory\n'); return {}; }
}
function cancel() { if(pending) {pending.cancel(); pending=null;} }
function save() {
    cancel();
    outlet(0,'store',1);
    outlet(0,'delete',99);
    outlet(0,'write',paths(profile,this.patcher.filepath).local);
}
function readState(resetFactory) {
    cancel();
    var all=paths(profile,this.patcher.filepath);
    var local=!resetFactory && exists(all.local);
    var path=local?all.local:all.factory;
    if(!exists(path)) {post('DNA V3: missing state '+path+'\n'); return;}
    // New recipes always begin at V3 factory. Migrate only unchanged legacy
    // controls on the preserved ICE idle path, never the new V3 sound groups.
    var values=!local && !resetFactory && profile!=='ferrari'?legacyValues(all.legacy):{};
    outlet(0,'read',path);
    pending=new Task(function(){
        pending=null;
        outlet(0,local?1:99);
        if(!local) {
            outlet(0,'store',1);
            for(var key in values) if(values.hasOwnProperty(key)) outlet(0,'setstoredvalue',key,1,values[key]);
            outlet(0,1);
        }
        if(resetFactory) save();
    },this);
    pending.schedule(80);
}
function restore() { readState.call(this,false); }
function reset() { readState.call(this,true); }
function notifydeleted() {cancel();}
if(typeof module!=='undefined' && module.exports) module.exports={paths:paths,migrate:migrate};
