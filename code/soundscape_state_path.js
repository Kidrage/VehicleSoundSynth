autowatch = 1;
outlets = 2;

var profile = String(jsarguments.length > 1 ? jsarguments[1] : "ev");

function projectRoot() {
    var patchPath = String(this.patcher.filepath || "");
    var separator = patchPath.lastIndexOf("/");
    var directory = separator >= 0 ? patchPath.slice(0, separator) : patchPath;
    if (/\/patchers$/.test(directory)) {
        directory = directory.slice(0, -9);
    }
    return directory;
}

function statePath() {
    return projectRoot() + "/presets/local/" + profile + "_soundscape.json";
}

function fileExists(path) {
    var file = new File(path, "read");
    var exists = file.isopen;
    if (exists) {
        file.close();
    }
    return exists;
}

function save() {
    var path = statePath();
    outlet(0, "store", 1);
    outlet(0, "write", path);
    outlet(1, "soundscape_status", "saved", profile);
}

function restore() {
    var path = statePath();
    if (fileExists(path)) {
        outlet(0, "read", path);
        outlet(1, "soundscape_status", "loaded", profile);
    } else {
        outlet(1, "soundscape_status", "factory", profile);
    }
}

function reset() {
    outlet(0, 99);
    outlet(1, "soundscape_status", "factory", profile);
}
