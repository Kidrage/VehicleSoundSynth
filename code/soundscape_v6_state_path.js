autowatch = 1;
outlets = 2;

var profile = String(jsarguments.length > 1 ? jsarguments[1] : "ferrari");
var initialized = false;
var currentState = "Factory V6";

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
    return projectRoot() + "/presets/local/ferrari_soundscape_v6.json";
}

function factoryPath() {
    return projectRoot() + "/presets/ferrari_soundscape_v6_factory.json";
}

function fileExists(path) {
    var file = new File(path, "read");
    var exists = file.isopen;
    if (exists) file.close();
    return exists;
}

function primeFactorySlot(reportStatus) {
    outlet(0, "read", factoryPath());
    if (reportStatus) outlet(1, "soundscape_status", "Factory V6", profile);
}

function save() {
    if (!initialized) {
        outlet(1, "soundscape_status", "V6 Not Ready", profile);
        return;
    }
    outlet(0, "store", 1);
    outlet(0, "delete", 99);
    outlet(0, "write", statePath());
    primeFactorySlot(false);
    currentState = "Local V6";
    outlet(1, "soundscape_status", "Local V6 Saved", profile);
}

function factory() {
    currentState = "Factory V6";
    primeFactorySlot(true);
}

function prime() { primeFactorySlot(false); }

function restore() {
    if (fileExists(statePath())) {
        outlet(0, "read", statePath());
        currentState = "Local V6";
        outlet(1, "soundscape_status", "Local V6", profile);
    } else {
        currentState = "Factory V6";
        outlet(1, "soundscape_status", "Factory V6", profile);
    }
}

function reset() {
    currentState = "Factory V6";
    primeFactorySlot(false);
    outlet(1, "soundscape_status", "Factory V6", profile);
}

function ready() {
    initialized = true;
    primeFactorySlot(false);
    outlet(1, "soundscape_status", currentState, profile);
}
