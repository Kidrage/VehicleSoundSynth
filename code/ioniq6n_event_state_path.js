autowatch = 1;
outlets = 1;

var initialized = false;

function projectRoot() {
    var path = String(this.patcher.filepath || "");
    var directory = path.slice(0, path.lastIndexOf("/"));
    if (/\/patchers$/.test(directory)) directory = directory.slice(0, -9);
    return directory;
}

function localPath() {
    return projectRoot() + "/presets/local/ioniq6n_n_event.json";
}

function factoryPath() {
    return projectRoot() + "/presets/ioniq6n_n_event_factory.json";
}

function fileExists(path) {
    var file = new File(path, "read");
    var exists = file.isopen;
    if (exists) file.close();
    return exists;
}

function save() {
    if (!initialized) return;
    outlet(0, "store", 1);
    outlet(0, "delete", 99);
    outlet(0, "write", localPath());
    outlet(0, "read", factoryPath());
}

function restore() {
    outlet(0, "read", fileExists(localPath()) ? localPath() : factoryPath());
}

function reset() {
    outlet(0, "read", factoryPath());
    outlet(0, 99);
}

function ready() {
    initialized = true;
    outlet(0, "read", factoryPath());
}
