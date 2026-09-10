/* Versioned, profile-local Noise state. The Main stem fader is not stored here. */
autowatch = 1;
outlets = 1;
var noiseProfile = typeof jsarguments !== 'undefined' && jsarguments.length > 1 ? String(jsarguments[1]) : 'ev';
var noisePending = null;
function noisePaths(profile, patchPath) {
    var path = String(patchPath || '');
    var directory = path.slice(0, path.lastIndexOf('/')).replace(/\/patchers$/, '');
    return {local: directory + '/presets/local/' + profile + '_noise_v1.json',
        factory: directory + '/presets/' + profile + '_noise_v1_factory.json'};
}
function noiseRead(path, slot, persist) {
    if (noisePending) noisePending.cancel();
    var file = new File(path, 'read');
    if (!file.isopen) return;
    file.close();
    outlet(0, 'read', path);
    noisePending = new Task(function () {
        outlet(0, slot);
        if (persist) save();
    }, this);
    noisePending.schedule(50);
}
function save() {
    if (noisePending) noisePending.cancel();
    outlet(0, 'store', 1);
    outlet(0, 'delete', 99);
    outlet(0, 'write', noisePaths(noiseProfile, this.patcher.filepath).local);
}
function restore() {
    var paths = noisePaths(noiseProfile, this.patcher.filepath);
    var file = new File(paths.local, 'read');
    var exists = file.isopen;
    if (exists) file.close();
    noiseRead(exists ? paths.local : paths.factory, exists ? 1 : 99, false);
}
function reset() { noiseRead(noisePaths(noiseProfile, this.patcher.filepath).factory, 99, true); }
function notifydeleted() { if (noisePending) noisePending.cancel(); }
if (typeof module !== 'undefined' && module.exports) module.exports = {noisePaths: noisePaths};
