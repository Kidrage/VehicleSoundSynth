autowatch = 1;
outlets = 1;
var profile = String(jsarguments.length > 1 ? jsarguments[1] : "engine");
function statePath() {
    var path = String(this.patcher.filepath || "");
    var directory = path.slice(0, path.lastIndexOf("/"));
    if (/\/patchers$/.test(directory)) directory = directory.slice(0, -9);
    return directory + "/presets/local/" + profile + "_pop_v2.json";
}
function save() { outlet(0, "store", 1); outlet(0, "write", statePath()); }
function restore() { outlet(0, "read", statePath()); }
