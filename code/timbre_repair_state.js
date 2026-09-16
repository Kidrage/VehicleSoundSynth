/* Versioned repair state; no writes to previous DNA, SC, Start, Mixer or Noise. */
autowatch = 1;
outlets = 1;
var profile = typeof jsarguments !== 'undefined' ? String(jsarguments[1]) : 'ioniq6n';
var pending = null;
function paths(p, patchPath) {
    var root = String(patchPath).replace(/\/[^/]*$/, '').replace(/\/patchers$/, '');
    if (p !== 'ioniq6n' && p !== 'ferrari') throw new Error('Unsupported repair profile');
    var name = p === 'ioniq6n' ? 'ioniq6n_sound_dna_v3' : 'ferrari_sound_dna_v4';
    return {local:root+'/presets/local/'+name+'.json', factory:root+'/presets/'+name+'_factory.json',
        previous:p === 'ioniq6n' ? [root+'/presets/local/ioniq6n_sound_dna_v2.json',root+'/presets/local/ioniq6n_sound_dna.json'] :
            [root+'/presets/local/ferrari_sound_dna_v3.json']};
}
function merge(factory, saved) {
    var result = {};
    for (var key in factory) if (factory.hasOwnProperty(key)) {
        var value = saved && saved[key];
        result[key] = Array.isArray(value) && value.length === factory[key].length && value.every(function(x) {
            return typeof x === 'number' && isFinite(x);
        }) ? value.slice() : factory[key].slice();
        if (key.indexOf('dna_') === 0 || key.indexOf('v3_') === 0 || key === 'reference_restore') {
            result[key][0] = Math.max(0,Math.min(1,result[key][0]));
        }
    }
    return result;
}
function readData(path, slot) {
    var f=new File(path,'read'), text='';
    if (!f.isopen) return null;
    while(f.position<f.eof) text+=f.readline();
    f.close();
    try {
        var data=JSON.parse(text).pattrstorage.slots[String(slot)].data;
        return data && typeof data==='object' && !Array.isArray(data) ? data : null;
    } catch(e) {post('Timbre repair: invalid state '+path+'\n'); return null;}
}
function cancel() {if(pending){pending.cancel();pending=null;}}
function save() {
    cancel();
    outlet(0,'store',1);
    outlet(0,'delete',99);
    outlet(0,'write',paths(profile,this.patcher.filepath).local);
}
function readState(resetFactory) {
    cancel();
    var all=paths(profile,this.patcher.filepath), factory=readData(all.factory,99);
    if(!factory){post('Timbre repair: missing factory; keeping current sound\n');return;}
    var saved=resetFactory?null:readData(all.local,1);
    if(!resetFactory && !saved) {
        for(var i=0;i<all.previous.length && !saved;i++) saved=readData(all.previous[i],1);
    }
    var data=merge(factory,saved);
    outlet(0,'read',all.factory);
    pending=new Task(function(){
        pending=null;
        for(var key in data) if(data.hasOwnProperty(key)) outlet(0,'setstoredvalue',key,1,data[key]);
        outlet(0,1);
        if(resetFactory) save.call(this);
    },this);
    pending.schedule(80);
}
function restore(){readState.call(this,false);}
function reset(){readState.call(this,true);}
function notifydeleted(){cancel();}
if(typeof module!=='undefined' && module.exports) module.exports={paths:paths,merge:merge};
