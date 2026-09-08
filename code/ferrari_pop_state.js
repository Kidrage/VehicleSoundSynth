/* Three saved controls only; never read or overwrite the previous Pop preset. */
autowatch = 1;
outlets = 1;
var pending = null;
function statePath() {
    var path = String(this.patcher.filepath || '');
    var directory = path.slice(0, path.lastIndexOf('/')).replace(/\/patchers$/, '');
    return directory + '/presets/local/ferrari_pop_v3.json';
}
function save() {
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
