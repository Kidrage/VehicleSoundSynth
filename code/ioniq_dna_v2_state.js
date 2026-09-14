/* Explicit IONIQ-only state. Never writes legacy DNA or any Soundscape file. */
autowatch = 1;
outlets = 1;
var pending = null;
function paths(patchPath) {
    var root = String(patchPath).replace(/\/[^/]*$/, '').replace(/\/patchers$/, '');
    return {local:root+'/presets/local/ioniq6n_sound_dna_v2.json',
        factory:root+'/presets/ioniq6n_sound_dna_v2_factory.json',
        legacy:root+'/presets/local/ioniq6n_sound_dna.json'};
}
function readData(path, slot) {
    var file = new File(path,'read'), text = '';
    if (!file.isopen) return null;
    while (file.position < file.eof) text += file.readline();
    file.close();
    try { return JSON.parse(text).pattrstorage.slots[String(slot)].data; }
    catch (error) { post('IONIQ DNA: invalid state '+path+'\n'); return null; }
}
function merge(factory, saved) {
    var result = {};
    for (var key in factory) if (factory.hasOwnProperty(key)) {
        var value = saved && saved[key];
        result[key] = Array.isArray(value) && value.length === factory[key].length && value.every(function(x) {
            return typeof x === 'number' && isFinite(x);
        }) ? value : factory[key];
        if (key.indexOf('dna_') === 0) result[key] = [Math.max(0,Math.min(1,result[key][0]))];
    }
    return result;
}
function cancel() { if (pending) {pending.cancel(); pending = null;} }
function save() {
    cancel();
    outlet(0,'store',1);
    outlet(0,'delete',99);
    outlet(0,'write',paths(this.patcher.filepath).local);
}
function readState(resetFactory) {
    cancel();
    var all = paths(this.patcher.filepath);
    var factory = readData(all.factory,99);
    if (!factory) {post('IONIQ DNA: missing factory; keeping current sound\n'); return;}
    var saved = resetFactory ? null : (readData(all.local,1) || readData(all.legacy,1));
    var data = merge(factory,saved);
    outlet(0,'read',all.factory);
    pending = new Task(function() {
        pending = null;
        for (var key in data) if (data.hasOwnProperty(key)) outlet(0,'setstoredvalue',key,1,data[key]);
        outlet(0,1);
        if (resetFactory) save.call(this);
    },this);
    pending.schedule(80);
}
function restore() {readState.call(this,false);}
function reset() {readState.call(this,true);}
function notifydeleted() {cancel();}
if (typeof module !== 'undefined' && module.exports) module.exports = {paths:paths,merge:merge};
