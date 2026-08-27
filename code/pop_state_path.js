autowatch = 1;
outlets = 1;

var profile = String(jsarguments.length > 1 ? jsarguments[1] : "engine");

function statePath() {
    var patchPath = String(this.patcher.filepath || "");
    var separator = patchPath.lastIndexOf("/");
    var directory = separator >= 0 ? patchPath.slice(0, separator) : patchPath;
    if (/\/patchers$/.test(directory)) {
        directory = directory.slice(0, -9);
    }
    return directory + "/presets/local/" + profile + "_pop.json";
}

function save() {
    outlet(0, "store", 1);
    outlet(0, "write", statePath());
}

function restore() {
    outlet(0, "read", statePath());
}
