/* New source namespace; only the previous spatial controls migrate. */
autowatch = 1;
outlets = 2;
var profile = typeof jsarguments !== 'undefined' ? String(jsarguments[1]) : 'ev';
var initialized = false;
function projectRoot() {
    var directory=String(this.patcher.filepath || '').replace(/\/[^/]*$/, '');
    return directory.replace(/\/patchers$/, '');
}
function statePath() { return projectRoot()+'/presets/local/v7_'+profile+'_soundscape_v5.json'; }
function factoryPath() { return projectRoot()+'/presets/v7_factories/'+profile+'_soundscape_v5_factory.json'; }
function exists(path) { var f=new File(v7ReadPath(path), 'read'); var yes=f.isopen; if(yes)f.close(); return yes; }
function readJSON(path) { var f=new File(v7ReadPath(path), 'read'); var s=''; while(f.isopen && f.position<f.eof)s+=f.readstring(65536); f.close(); return JSON.parse(s); }
function spatialMigration(old, voice) {
    var data=((old.pattrstorage.slots['1']||{}).data)||{};
    var out={};
    for(var k in data) if(Object.prototype.hasOwnProperty.call(data,k)) {
        if(k==='soundscape_space_state' || k==='soundscape_motion_state' || k==='soundscape_pitch_follow_state' || k==='soundscape_transpose_state' || /::(Orbital_Motion|Wide_Banks|Bank_Space|.*Space.*|.*Reflection.*|.*Chorus.*|.*Reverb.*)::/.test(k))
            out[k.replace(/_soundscape_v4_beap~/g,'_soundscape_v5_beap~')]=data[k];
    }
    return out;
}
function primeFactorySlot() { outlet(0, 'read', v7ReadPath(factoryPath())); }
function factory() { primeFactorySlot(); }
function prime() { primeFactorySlot(); }
function save() {
    if(!initialized)return;
    outlet(0,'store',1); outlet(0,'delete',99); outlet(0,'write',statePath()); primeFactorySlot();
    outlet(1,'soundscape_status','Local Bed V5 Saved',profile);
}
function restore() {
    if(exists(statePath())) { outlet(0, 'read', v7ReadPath(statePath())); return; }
    var previous=projectRoot()+'/presets/local/v7_'+profile+'_soundscape_v4.json';
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
