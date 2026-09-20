/* Ferrari V5 owns only its fresh DNA namespace. V4 and older states are read-only. */
autowatch = 1;
outlets = 1;
var pending = null;

function paths(patchPath) {
    var root = String(patchPath).replace(/\/[^/]*$/, '').replace(/\/patchers$/, '');
    return {
        local: root + '/presets/local/ferrari_sound_dna_v5.json',
        factory: root + '/presets/ferrari_sound_dna_v5_factory.json'
    };
}
function readData(path, slot) {
    var file = new File(path, 'read'), text = '';
    if (!file.isopen) return null;
    while (file.position < file.eof) text += file.readline();
    file.close();
    try {
        var data = JSON.parse(text).pattrstorage.slots[String(slot)].data;
        return data && typeof data === 'object' && !Array.isArray(data) ? data : null;
    } catch (error) {
        post('Ferrari V5: invalid state ' + path + '\n');
        return null;
    }
}
function merge(factory, saved) {
    var result = {};
    for (var key in factory) if (factory.hasOwnProperty(key)) {
        var value = saved && saved[key];
        result[key] = Array.isArray(value) &&
            value.length === factory[key].length &&
            value.every(function (x) { return typeof x === 'number' && isFinite(x); })
            ? value.slice() : factory[key].slice();
        if (key.indexOf('v3_') === 0 || key === 'reference_restore' || key === 'sf90_material') {
            result[key][0] = Math.max(0, Math.min(1, result[key][0]));
        }
    }
    return result;
}
function cancel() {
    if (pending) { pending.cancel(); pending = null; }
}
function save() {
    cancel();
    outlet(0, 'store', 1);
    outlet(0, 'delete', 99);
    outlet(0, 'write', paths(this.patcher.filepath).local);
}
function readState(resetFactory) {
    cancel();
    var all = paths(this.patcher.filepath);
    var factory = readData(all.factory, 99);
    if (!factory) {
        post('Ferrari V5: missing factory; keeping current sound\n');
        return;
    }
    var saved = resetFactory ? null : readData(all.local, 1);
    var data = merge(factory, saved);
    outlet(0, 'read', all.factory);
    pending = new Task(function () {
        pending = null;
        for (var key in data) if (data.hasOwnProperty(key)) {
            outlet(0, 'setstoredvalue', key, 1, data[key]);
        }
        outlet(0, 1);
        if (resetFactory) save.call(this);
    }, this);
    pending.schedule(80);
}
function restore() { readState.call(this, false); }
function reset() { readState.call(this, true); }
function notifydeleted() { cancel(); }

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {paths: paths, merge: merge};
}
