/* Versioned, profile-local Noise state. The Main stem fader is not stored here. */
autowatch = 1;
outlets = 1;
var noiseProfile = typeof jsarguments !== 'undefined' && jsarguments.length > 1 ? String(jsarguments[1]) : 'ev';
var noisePending = null;
var noiseVersion = typeof jsarguments !== 'undefined' && Number(jsarguments[2]) === 2 ? 2 : 1;
function noisePaths(profile, patchPath, version) {
    var path = String(patchPath || '');
    var directory = path.slice(0, path.lastIndexOf('/')).replace(/\/patchers$/, '');
    var suffix = version === 2 ? '_noise_v2' : '_noise_v1';
    return {local: directory + '/presets/local/v7_' + profile + suffix + '.json',
        factory: directory + '/presets/v7_factories/' + profile + suffix + '_factory.json'};
}
function noiseRead(path, slot, persist, migration) {
    if (noisePending) noisePending.cancel();
    var file = new File(v7ReadPath(path), 'read');
    if (!file.isopen) return;
    file.close();
    outlet(0, 'read', v7ReadPath(path));
    noisePending = new Task(function () {
        outlet(0, slot);
        if (migration) {
            outlet(0, 'store', 1);
            for (var key in migration) if (migration.hasOwnProperty(key)) {
                outlet(0, 'setstoredvalue', key, 1, migration[key]);
            }
            outlet(0, 1);
        }
        if (persist) save();
    }, this);
    noisePending.schedule(50);
}
function save() {
    if (noisePending) noisePending.cancel();
    outlet(0, 'store', 1);
    outlet(0, 'delete', 99);
    outlet(0, 'write', noisePaths(noiseProfile, this.patcher.filepath, noiseVersion).local);
}
function restore() {
    var paths = noisePaths(noiseProfile, this.patcher.filepath, noiseVersion);
    var file = new File(v7ReadPath(paths.local), 'read');
    var exists = file.isopen;
    if (exists) file.close();
    var migration = null;
    if (!exists && noiseVersion === 2) {
        var oldFile = new File(v7ReadPath(noisePaths(noiseProfile, this.patcher.filepath, 1).local), 'read');
        if (oldFile.isopen) {
            var text = '';
            while (oldFile.position < oldFile.eof) text += oldFile.readline();
            oldFile.close();
            try {
                var data = JSON.parse(text).pattrstorage.slots['1'].data;
                migration = {};
                for (var key in data) if (data.hasOwnProperty(key) &&
                    (/^noise_(mechanical_db|intake_db|tire_db|air_db|color)$/.test(key) || /^Noise_Ceiling::/.test(key))) {
                    if (data[key] && data[key].length && isFinite(Number(data[key][0]))) migration[key] = data[key][0];
                }
            } catch (error) { post('Noise V2: invalid old state; keeping factory\n'); }
        }
    }
    noiseRead(exists ? paths.local : paths.factory, exists ? 1 : 99, false, migration);
}
function reset() { noiseRead(noisePaths(noiseProfile, this.patcher.filepath, noiseVersion).factory, 99, true); }
function notifydeleted() { if (noisePending) noisePending.cancel(); }
if (typeof module !== 'undefined' && module.exports) module.exports = {noisePaths: noisePaths};

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
