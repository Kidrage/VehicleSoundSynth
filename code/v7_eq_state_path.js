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
    return projectRoot() + "/presets/local/v7_" + profile + "_vehicle_bus_eq.json";
}

function legacyPath() {
    return projectRoot() + "/presets/local/v7_vehicle_bus_eq.json";
}

function fileExists(path) {
    var file = new File(v7ReadPath(path), 'read');
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
        outlet(0, 'read', v7ReadPath(profileState));
    } else if (fileExists(legacyPath())) {
        outlet(0, 'read', v7ReadPath(legacyPath()));
    }
}

/* Read-only published tone binding fallback. Writes always remain presets/local/v7_*.
 * No V6 local file is imported. Native pattrstorage client paths remain unchanged.
 */
function v7PhysicalExists(path){var f=new File(path,'read'),found=f.isopen;if(found)f.close();return found;}
function v7ReadPath(path){
    path=String(path);
    if(path.indexOf('/presets/local/v7_')>=0 && !v7PhysicalExists(path)){
        var binding=path.replace('/presets/local/v7_','/presets/v7_bindings/');
        if(v7PhysicalExists(binding))return binding;
    }
    return path;
}
