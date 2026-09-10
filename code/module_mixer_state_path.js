autowatch = 1;
outlets = 1;

var profile = typeof jsarguments !== "undefined" ? String(jsarguments.length > 1 ? jsarguments[1] : "ev") : "ev";
var stateNamespace = profile === "ferrari" ? "ferrari_realism_v2" : profile;

function statePath() {
    var patchPath = String(this.patcher.filepath || "");
    var separator = patchPath.lastIndexOf("/");
    var directory = separator >= 0 ? patchPath.slice(0, separator) : patchPath;
    if (/\/patchers$/.test(directory)) {
        directory = directory.slice(0, -9);
    }
    return directory + "/presets/local/" + stateNamespace + "_module_mixer_noise_v1.json";
}

function save() {
    outlet(0, "store", 1);
    outlet(0, "write", statePath());
}

function restore() {
    var path = statePath();
    var file = new File(path, "read");
    var exists = file.isopen;
    if (exists) {
        file.close();
        outlet(0, "read", path);
    } else {
        var previous=path.replace('_module_mixer_noise_v1.json','_module_mixer.json');
        var old=new File(previous,'read');
        if(old.isopen) {
            var content='';
            while(old.position<old.eof)content+=old.readstring(65536);
            old.close();
            try {
                var migrated=migrateNoiseDefault(JSON.parse(content));
                var target=new File(path,'write','TEXT');
                if(target.isopen) { target.writestring(JSON.stringify(migrated)); target.close(); outlet(0,'read',path); }
            } catch(error) { post('Noise mixer migration skipped: '+error+'\n'); }
        }
    }
}

function migrateNoiseDefault(document) {
    var copy=JSON.parse(JSON.stringify(document));
    var slots=copy.pattrstorage.slots;
    for(var key in slots) if(Object.prototype.hasOwnProperty.call(slots,key)) {
        // Slider units are tenths of dB above -60: zero is exact Noise off.
        slots[key].data.mix_road_level_db=[0.];
    }
    return copy;
}
if(typeof module!=='undefined')module.exports={migrateNoiseDefault:migrateNoiseDefault};
