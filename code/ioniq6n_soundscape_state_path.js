autowatch = 1;
outlets = 2;

var initialized = false;
var currentState = "Factory Modes";

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
    return projectRoot() + "/presets/local/ioniq6n_soundscape_modes.json";
}

function factoryPath() {
    return projectRoot() + "/presets/ioniq6n_soundscape_modes_factory.json";
}

function fileExists(path) {
    var file = new File(path, "read");
    var exists = file.isopen;
    if (exists) file.close();
    return exists;
}

function primeFactory(reportStatus) {
    outlet(0, "read", factoryPath());
    if (reportStatus) outlet(1, "soundscape_status", "Factory Modes", "ioniq6n");
}

function save() {
    if (!initialized) {
        outlet(1, "soundscape_status", "Modes Not Ready", "ioniq6n");
        return;
    }
    outlet(0, "store", 1);
    outlet(0, "delete", 99);
    outlet(0, "write", statePath());
    primeFactory(false);
    currentState = "Local Modes";
    outlet(1, "soundscape_status", "Local Modes Saved", "ioniq6n");
}

function restore() {
    if (fileExists(statePath())) {
        outlet(0, "read", statePath());
        currentState = "Local Modes";
        outlet(1, "soundscape_status", currentState, "ioniq6n");
    } else {
        currentState = "Factory Modes";
        primeFactory(false);
        outlet(1, "soundscape_status", currentState, "ioniq6n");
    }
}

function reset() {
    currentState = "Factory Modes";
    primeFactory(true);
}

function ready() {
    initialized = true;
    primeFactory(false);
    outlet(1, "soundscape_status", currentState, "ioniq6n");
}
