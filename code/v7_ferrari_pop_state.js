/* Three saved controls only; never read or overwrite the previous Pop preset. */
autowatch = 1;
outlets = 1;
var pending = null;
var profile = typeof jsarguments !== 'undefined' && /^(ev|v10|v12|ioniq6n)$/.test(jsarguments[1])
    ? String(jsarguments[1]) : 'ferrari';
function statePath() {
    var path = String(this.patcher.filepath || '');
    var directory = path.slice(0, path.lastIndexOf('/')).replace(/\/patchers$/, '');
    return directory + '/presets/local/v7_' + profile + '_pop_v' + (profile === 'ferrari' ? '3' : '4') + '.json';
}
function save() {
    if (pending) { pending.cancel(); pending = null; }
    outlet(0, 'store', 1);
    outlet(0, 'write', statePath());
}
function restore() {
    if (pending) pending.cancel();
    var file = new File(v7ReadPath(statePath()), 'read');
    if (!file.isopen) return; // the visible defaults remain authoritative
    file.close();
    outlet(0, 'read', v7ReadPath(statePath()));
    pending = new Task(function () { outlet(0, 1); }, this);
    pending.schedule(50);
}
function notifydeleted() { if (pending) pending.cancel(); }

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
