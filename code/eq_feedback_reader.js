autowatch = 1;
outlets = 1;

var inMax = typeof jsarguments !== "undefined";
var profile = String(inMax && jsarguments.length > 1 ? jsarguments[1] : "ev");
var BAND_NAMES = ["eq_low", "eq_lowmid", "eq_highmid", "eq_high"];
var DEFAULT_STATE = {
    eq_low: [90.0, 0.0],
    eq_lowmid: [250.0, 0.0, 0.8],
    eq_highmid: [3800.0, 0.0, 1.0],
    eq_high: [9000.0, 0.0],
    eq_bypass: [0]
};

function copyDefaults() {
    var result = {};
    var key;
    for (key in DEFAULT_STATE) {
        if (DEFAULT_STATE.hasOwnProperty(key)) {
            result[key] = DEFAULT_STATE[key].slice(0);
        }
    }
    return result;
}

function finiteNumber(value, fallback) {
    var number = Number(value);
    return isFinite(number) ? number : fallback;
}

function decodeEqState(payload) {
    var result = copyDefaults();
    var slots = payload && payload.pattrstorage && payload.pattrstorage.slots;
    var slot = slots && (slots["1"] || slots[1]);
    var data = slot && slot.data;
    var graph = data && data.vehicle_bus_eq_graph;
    var bypass = data && data.vehicle_bus_eq_bypass;
    var count;
    var stride;
    var index;
    var offset;
    var bandIndex;
    var linearGain;
    var gainDb;

    if (bypass && bypass.length) {
        result.eq_bypass = [finiteNumber(bypass[0], 0) ? 1 : 0];
    }
    if (!graph || graph.length < 9) {
        return result;
    }
    count = Math.max(0, Math.floor(finiteNumber(graph[0], 0)));
    stride = count ? Math.floor((graph.length - 1) / count) : 0;
    if (count < 1 || stride < 8) {
        return result;
    }
    for (index = 0; index < count; index += 1) {
        offset = 1 + index * stride;
        bandIndex = Math.floor(finiteNumber(graph[offset], -1));
        if (bandIndex < 0 || bandIndex >= BAND_NAMES.length) {
            continue;
        }
        linearGain = Math.max(finiteNumber(graph[offset + 6], 1.0), 0.000001);
        gainDb = 10.0 * Math.log(linearGain) / Math.LN10;
        if (bandIndex === 0 || bandIndex === 3) {
            result[BAND_NAMES[bandIndex]] = [
                finiteNumber(graph[offset + 5], result[BAND_NAMES[bandIndex]][0]),
                gainDb
            ];
        } else {
            result[BAND_NAMES[bandIndex]] = [
                finiteNumber(graph[offset + 5], result[BAND_NAMES[bandIndex]][0]),
                gainDb,
                finiteNumber(graph[offset + 7], result[BAND_NAMES[bandIndex]][2])
            ];
        }
    }
    return result;
}

function projectRoot() {
    var patchPath = String(this.patcher.filepath || "");
    var separator = patchPath.lastIndexOf("/");
    var directory = separator >= 0 ? patchPath.slice(0, separator) : patchPath;
    if (/\/patchers$/.test(directory)) {
        directory = directory.slice(0, -9);
    }
    return directory;
}

function fileExists(path) {
    var file = new File(path, "read");
    var exists = file.isopen;
    if (exists) {
        file.close();
    }
    return exists;
}

function readJson(path) {
    var file = new File(path, "read");
    var source = "";
    if (!file.isopen) {
        return null;
    }
    while (file.position < file.eof) {
        source += file.readline();
    }
    file.close();
    try {
        return JSON.parse(source);
    } catch (error) {
        post("eq_feedback_reader: invalid state file " + path + "\n");
        return null;
    }
}

function emitState(state) {
    outlet(0, "eq_low", state.eq_low[0], state.eq_low[1]);
    outlet(0, "eq_lowmid", state.eq_lowmid[0], state.eq_lowmid[1], state.eq_lowmid[2]);
    outlet(0, "eq_highmid", state.eq_highmid[0], state.eq_highmid[1], state.eq_highmid[2]);
    outlet(0, "eq_high", state.eq_high[0], state.eq_high[1]);
    outlet(0, "eq_bypass", state.eq_bypass[0]);
}

function bang() {
    var root = projectRoot.call(this);
    var profilePath = root + "/presets/local/" + profile + "_vehicle_bus_eq.json";
    var legacyPath = root + "/presets/local/vehicle_bus_eq.json";
    var payload = null;
    if (fileExists(profilePath)) {
        payload = readJson(profilePath);
    } else if (fileExists(legacyPath)) {
        payload = readJson(legacyPath);
    }
    emitState(decodeEqState(payload));
}

function reset() {
    emitState(copyDefaults());
}

if (typeof module !== "undefined" && module.exports) {
    module.exports = {
        DEFAULT_STATE: DEFAULT_STATE,
        decodeEqState: decodeEqState
    };
}
