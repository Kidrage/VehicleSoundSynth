/* Three saved controls only; never read or overwrite the previous Pop preset. */
autowatch = 1;
outlets = 1;
var pending = null;
var profile = typeof jsarguments !== 'undefined' && /^(ev|v10|v12|ioniq6n)$/.test(jsarguments[1])
    ? String(jsarguments[1]) : 'ferrari';
function statePath() {
    var path = String(this.patcher.filepath || '');
    var directory = path.slice(0, path.lastIndexOf('/')).replace(/\/patchers$/, '');
    return directory + '/presets/local/' + profile + '_pop_v' + (profile === 'ferrari' ? '3' : '4') + '.json';
}
function save() {
    if (pending) { pending.cancel(); pending = null; }
    outlet(0, 'store', 1);
    outlet(0, 'write', statePath());
}
function restore() {
    if (pending) pending.cancel();
    var file = new File(statePath(), 'read');
    if (!file.isopen) return; // the visible defaults remain authoritative
    file.close();
    outlet(0, 'read', statePath());
    pending = new Task(function () { outlet(0, 1); }, this);
    pending.schedule(50);
}
function notifydeleted() { if (pending) pending.cancel(); }
