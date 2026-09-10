/* New source namespace; only the previous spatial controls migrate. */
autowatch = 1;
outlets = 2;
var profile = typeof jsarguments !== 'undefined' ? String(jsarguments[1]) : 'ev';
var initialized = false;
function projectRoot() {
    var directory=String(this.patcher.filepath || '').replace(/\/[^/]*$/, '');
    return directory.replace(/\/patchers$/, '');
}
function statePath() { return projectRoot()+'/presets/local/'+profile+'_soundscape_v5.json'; }
function factoryPath() { return projectRoot()+'/presets/'+profile+'_soundscape_v5_factory.json'; }
function exists(path) { var f=new File(path,'read'); var yes=f.isopen; if(yes)f.close(); return yes; }
function readJSON(path) { var f=new File(path,'read'); var s=''; while(f.isopen && f.position<f.eof)s+=f.readstring(65536); f.close(); return JSON.parse(s); }
function spatialMigration(old, voice) {
    var data=((old.pattrstorage.slots['1']||{}).data)||{};
    var out={};
    for(var k in data) if(Object.prototype.hasOwnProperty.call(data,k)) {
        if(k==='soundscape_space_state' || k==='soundscape_motion_state' || k==='soundscape_pitch_follow_state' || k==='soundscape_transpose_state' || /::(Orbital_Motion|Wide_Banks|Bank_Space|.*Space.*|.*Reflection.*|.*Chorus.*|.*Reverb.*)::/.test(k))
            out[k.replace(/_soundscape_v4_beap~/g,'_soundscape_v5_beap~')]=data[k];
    }
    return out;
}
function primeFactorySlot() { outlet(0,'read',factoryPath()); }
function factory() { primeFactorySlot(); }
function prime() { primeFactorySlot(); }
function save() {
    if(!initialized)return;
    outlet(0,'store',1); outlet(0,'delete',99); outlet(0,'write',statePath()); primeFactorySlot();
    outlet(1,'soundscape_status','Local Bed V5 Saved',profile);
}
function restore() {
    if(exists(statePath())) { outlet(0,'read',statePath()); return; }
    var previous=projectRoot()+'/presets/local/'+profile+'_soundscape_v4.json';
    if(exists(previous)) {
        try {
            var migrated=spatialMigration(readJSON(previous),profile);
            // A slot-1 overlay on current factory, never overwrite the old file.
            outlet(0,'store',1);
            for(var key in migrated) if(Object.prototype.hasOwnProperty.call(migrated,key))
                outlet(0,'setstoredvalue',key,1,migrated[key]);
        } catch(error) { post('Soundscape spatial migration skipped: '+error+'\n'); }
    }
}
function reset() { primeFactorySlot(); }
function ready() { initialized=true; primeFactorySlot(); outlet(1,'soundscape_status','Running Bed V5',profile); }
if(typeof module!=='undefined')module.exports={spatialMigration:spatialMigration};
