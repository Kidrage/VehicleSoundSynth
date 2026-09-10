/* A-only Noise split. Preserve all accepted IONIQ tone/mode/FX settings on migration. */
autowatch = 1;
outlets = 2;
var initialized = false;
var pending = null;
function projectRoot() {
    var path = String(this.patcher.filepath || '');
    return path.slice(0, path.lastIndexOf('/')).replace(/\/patchers$/, '');
}
function statePath() { return projectRoot() + '/presets/local/ioniq6n_soundscape_modes_v2.json'; }
function factoryPath() { return projectRoot() + '/presets/ioniq6n_soundscape_modes_v2_factory.json'; }
function exists(path) {
    var file = new File(path, 'read');
    var result = file.isopen;
    if (result) file.close();
    return result;
}
function readJSON(path) {
    var file = new File(path, 'read'), text = '';
    while (file.isopen && file.position < file.eof) text += file.readstring(65536);
    file.close();
    return JSON.parse(text);
}
function migrateModeData(previous) {
    var data = ((((previous || {}).pattrstorage || {}).slots || {})['1'] || {}).data || {};
    var migrated = {};
    for (var key in data) if (Object.prototype.hasOwnProperty.call(data, key)) {
        migrated[key.replace(/ioniq6n_soundscape_(ignition|evolution|lightspeed)_beap~/g,
            'ioniq6n_soundscape_$1_bed_v2_beap~')] = data[key];
    }
    return migrated;
}
function primeFactory() { outlet(0, 'read', factoryPath()); }
function recallLater(slot, persist) {
    if (pending) pending.cancel();
    pending = new Task(function () {
        outlet(0, slot);
        if (slot === 99) outlet(0, 'store', 1);
        if (persist) save();
    }, this);
    pending.schedule(50);
}
function save() {
    if (!initialized) return;
    if (pending) pending.cancel();
    outlet(0, 'store', 1);
    outlet(0, 'delete', 99);
    outlet(0, 'write', statePath());
    primeFactory();
    outlet(1, 'soundscape_status', 'Local Modes V2 Saved', 'ioniq6n');
}
function restore() {
    if (exists(statePath())) {
        outlet(0, 'read', statePath());
        recallLater(1, false);
        outlet(1, 'soundscape_status', 'Local Modes V2', 'ioniq6n');
        return;
    }
    var previous = projectRoot() + '/presets/local/ioniq6n_soundscape_modes.json';
    if (exists(previous)) {
        try {
            var data = migrateModeData(readJSON(previous));
            outlet(0, 'store', 1);
            for (var key in data) if (Object.prototype.hasOwnProperty.call(data, key)) {
                var values = data[key] instanceof Array ? data[key] : [data[key]];
                outlet.apply(null, [0, 'setstoredvalue', key, 1].concat(values));
            }
            recallLater(1, true);
            outlet(1, 'soundscape_status', 'Migrated Modes V2', 'ioniq6n');
            return;
        } catch (error) { post('IONIQ mode migration skipped: ' + error + '\n'); }
    }
    primeFactory();
    recallLater(99, false);
    outlet(1, 'soundscape_status', 'Factory Modes V2', 'ioniq6n');
}
function reset() {
    primeFactory();
    recallLater(99, true);
    outlet(1, 'soundscape_status', 'Factory Modes V2', 'ioniq6n');
}
function ready() {
    initialized = true;
    primeFactory();
    recallLater(99, false);
}
function notifydeleted() { if (pending) pending.cancel(); }
if (typeof module !== 'undefined' && module.exports) module.exports = {migrateModeData: migrateModeData};
