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
    return {local: directory + '/presets/local/' + profile + suffix + '.json',
        factory: directory + '/presets/' + profile + suffix + '_factory.json'};
}
function noiseRead(path, slot, persist, migration) {
    if (noisePending) noisePending.cancel();
    var file = new File(path, 'read');
    if (!file.isopen) return;
    file.close();
    outlet(0, 'read', path);
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
    var file = new File(paths.local, 'read');
    var exists = file.isopen;
    if (exists) file.close();
    var migration = null;
    if (!exists && noiseVersion === 2) {
        var oldFile = new File(noisePaths(noiseProfile, this.patcher.filepath, 1).local, 'read');
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
