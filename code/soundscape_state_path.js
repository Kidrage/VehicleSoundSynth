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

function factoryPath() {
    return projectRoot() + "/presets/" + profile + "_soundscape_factory.json";
}

function fileExists(path) {
    var file = new File(path, "read");
    var exists = file.isopen;
    if (exists) {
        file.close();
    }
    return exists;
}

function primeFactorySlot(reportStatus) {
    outlet(0, "read", factoryPath());
    if (reportStatus) {
        outlet(1, "soundscape_status", "factory", profile);
    }
}

function save() {
    var path = statePath();
    outlet(0, "store", 1);
    // Old local files may contain the former shared factory slot.  Strip it so
    // local persistence can never shadow the tracked, read-only factory state.
    outlet(0, "delete", 99);
    outlet(0, "write", path);
    // Re-read the tracked factory after writing the local-only file.
    primeFactorySlot(false);
    outlet(1, "soundscape_status", "saved", profile);
}

function factory() {
    primeFactorySlot(true);
}

function prime() {
    // A legacy local file may contain slot 99.  Re-prime after every local read
    // so Factory Reset always resolves to the tracked factory authority.
    primeFactorySlot(false);
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
    primeFactorySlot(false);
    outlet(1, "soundscape_status", "factory", profile);
}
