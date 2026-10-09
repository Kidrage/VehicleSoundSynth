autowatch = 1;
outlets = 1;
var profile = String(jsarguments.length > 1 ? jsarguments[1] : "ev");
function statePath() {
    var path = String(this.patcher.filepath || "");
    var directory = path.slice(0, path.lastIndexOf("/"));
    if (/\/patchers$/.test(directory)) directory = directory.slice(0, -9);
    return directory + "/presets/local/v7_" + profile + "_start_v3.json";
}
function save() { outlet(0, "store", 1); outlet(0, "write", statePath()); }
function restore() { outlet(0, 'read', v7ReadPath(statePath())); }

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
