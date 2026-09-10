/* Running-DNA V2 state. Never rewrite a legacy preset or revive its dead knobs. */
autowatch = 1;
outlets = 1;

var profile = String(jsarguments.length > 1 ? jsarguments[1] : "v10");
var legacyAudible = ["aggression", "brightness", "body", "texture", "air_detail",
    "cycle_irregularity", "stereo_width", "throttle_loudness_depth", "saturation",
    "combustion_pulse", "intake_detail", "exhaust_detail", "residual_detail"];

function statePath(legacy) {
    var patchPath = String(this.patcher.filepath || "");
    var separator = patchPath.lastIndexOf("/");
    var directory = separator >= 0 ? patchPath.slice(0, separator) : patchPath;
    if (/\/patchers$/.test(directory)) directory = directory.slice(0, -9);
    return directory + "/presets/local/" + profile + "_sound_dna" + (legacy ? "" : "_v2") + ".json";
}

function exists(path) {
    var file = new File(path, "read");
    var found = file.isopen;
    if (found) file.close();
    return found;
}

function save() {
    outlet(0, "store", 1);
    outlet(0, "write", statePath.call(this, false));
}

function restore() {
    var path = statePath.call(this, false);
    if (exists(path)) {
        outlet(0, "read", path);
        return;
    }
    var file = new File(statePath.call(this, true), "read");
    if (!file.isopen) return; // Keep graph defaults without missing-file dialogs.
    var source = "";
    while (file.position < file.eof) source += file.readline();
    file.close();
    var payload;
    try { payload = JSON.parse(source); }
    catch (error) { post("DNA V2: invalid legacy state; preserving factory state\n"); return; }
    var slots = payload && payload.pattrstorage && payload.pattrstorage.slots;
    var data = slots && slots["1"] && slots["1"].data;
    if (!data) return;
    // Capture initialized V2 defaults, then migrate ONLY formerly audible
    // controls into slot1. Six old idle knobs were disconnected in V1; their
    // stored UI values must not change the accepted idle on the first V2 load.
    // Max's documented syntax is: setstoredvalue client preset data.
    outlet(0, "store", 1);
    for (var index = 0; index < legacyAudible.length; index += 1) {
        var key = "dna_" + legacyAudible[index];
        var value = data[key];
        if (value && value.length && isFinite(Number(value[0]))) {
            outlet(0, "setstoredvalue", key, 1, Number(value[0]));
        }
    }
}
