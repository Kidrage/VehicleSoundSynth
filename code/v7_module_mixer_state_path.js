autowatch = 1;
outlets = 1;

var profile = typeof jsarguments !== "undefined" ? String(jsarguments.length > 1 ? jsarguments[1] : "ev") : "ev";
var stateNamespace = profile === "ferrari" ? "ferrari_realism_v2" : profile;

function statePath() {
    var patchPath = String(this.patcher.filepath || "");
    var separator = patchPath.lastIndexOf("/");
    var directory = separator >= 0 ? patchPath.slice(0, separator) : patchPath;
    if (/\/patchers$/.test(directory)) {
        directory = directory.slice(0, -9);
    }
    return directory + "/presets/local/v7_" + stateNamespace + "_module_mixer_noise_v1.json";
}

function save() {
    outlet(0, "store", 1);
    outlet(0, "write", statePath());
}

function restore() {
    var path = statePath();
    var file = new File(v7ReadPath(path), 'read');
    var exists = file.isopen;
    if (exists) {
        file.close();
        outlet(0, 'read', v7ReadPath(path));
    } else {
        var previous=path.replace('_module_mixer_noise_v1.json','_module_mixer.json');
        var old=new File(v7ReadPath(previous), 'read');
        if(old.isopen) {
            var content='';
            while(old.position<old.eof)content+=old.readstring(65536);
            old.close();
            try {
                var migrated=migrateNoiseDefault(JSON.parse(content));
                var target=new File(path,'write','TEXT');
                if(target.isopen) { target.writestring(JSON.stringify(migrated)); target.close(); outlet(0, 'read', v7ReadPath(path)); }
            } catch(error) { post('Noise mixer migration skipped: '+error+'\n'); }
        }
    }
}

function migrateNoiseDefault(document) {
    var copy=JSON.parse(JSON.stringify(document));
    var slots=copy.pattrstorage.slots;
    for(var key in slots) if(Object.prototype.hasOwnProperty.call(slots,key)) {
        // Slider units are tenths of dB above -60: zero is exact Noise off.
        slots[key].data.mix_road_level_db=[0.];
    }
    return copy;
}
if(typeof module!=='undefined')module.exports={migrateNoiseDefault:migrateNoiseDefault};

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
