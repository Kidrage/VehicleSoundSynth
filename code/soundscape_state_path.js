autowatch = 1;
outlets = 2;

var profile = String(jsarguments.length > 1 ? jsarguments[1] : "ev");
var initialized = false;
var currentState = "Factory V3";

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
    return projectRoot() + "/presets/local/" + profile + "_soundscape_v3.json";
}

function factoryPath() {
    return projectRoot() + "/presets/" + profile + "_soundscape_v3_factory.json";
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
        outlet(1, "soundscape_status", "Factory V3", profile);
    }
}

function save() {
    if (!initialized) {
        outlet(1, "soundscape_status", "V3 Not Ready", profile);
        return;
    }
    var path = statePath();
    outlet(0, "store", 1);
    // Old local files may contain the former shared factory slot.  Strip it so
    // local persistence can never shadow the tracked, read-only factory state.
    outlet(0, "delete", 99);
    outlet(0, "write", path);
    // Re-read the tracked factory after writing the local-only file.
    primeFactorySlot(false);
    currentState = "Local V3";
    outlet(1, "soundscape_status", "Local V3 Saved", profile);
}

function factory() {
    currentState = "Factory V3";
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
        currentState = "Local V3";
        outlet(1, "soundscape_status", "Local V3", profile);
    } else {
        currentState = "Factory V3";
        outlet(1, "soundscape_status", "Factory V3", profile);
    }
}

function reset() {
    currentState = "Factory V3";
    primeFactorySlot(false);
    outlet(1, "soundscape_status", "Factory V3", profile);
}

function ready() {
    // Startup calls this only after the nested BEAP clients and the optional
    // V3 local slot have both been recalled.  Until then Save is rejected so
    // closing a loading patcher cannot replace a valid local state.
    initialized = true;
    primeFactorySlot(false);
    outlet(1, "soundscape_status", currentState, profile);
}
