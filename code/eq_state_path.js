autowatch = 1;
outlets = 1;

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
    return projectRoot() + "/presets/local/" + profile + "_vehicle_bus_eq.json";
}

function legacyPath() {
    return projectRoot() + "/presets/local/vehicle_bus_eq.json";
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
    outlet(0, "store", 1);
    outlet(0, "write", statePath());
}

function restore() {
    var profileState = statePath();
    if (fileExists(profileState)) {
        outlet(0, "read", profileState);
    } else if (fileExists(legacyPath())) {
        outlet(0, "read", legacyPath());
    }
}
