/* Single registry for generated routing and applied tone-state validation.
 * This adapter owns no audio, drive integration or preset file. */
autowatch = 1;
outlets = 2;
/* REGISTRY_JSON_BEGIN */
var DESIGN_REGISTRY = {
  "normalized": {
    "eq_low": [[30,400],[-12,12]],
    "eq_lowmid": [[120,1200],[-12,12],[0.3,4]],
    "eq_highmid": [[1000,8000],[-12,12],[0.3,4]],
    "eq_high": [[4000,16000],[-12,12]],
    "eq_bypass": [[0,1]],
    "compressor_threshold_db": [[-36,0]],
    "compressor_ratio": [[1,50]],
    "compressor_attack_rate": [[0,150]],
    "compressor_release_rate": [[0,150]],
    "compressor_makeup_db": [[-12,12]],
    "compressor_bypass": [[0,1]]
  },
  "modes": {"ev":{"ev_mode":["relax","expressive","sport"]},
            "ioniq6n":{"n_sound_mode":["ignition","evolution","lightspeed"]}},
  "direct": [
    "soundscape_enable","soundscape_solo","soundscape_motion","soundscape_space",
    "soundscape_pitch_follow","soundscape_transpose","soundscape_brightness",
    "soundscape_open","soundscape_save","soundscape_reload","soundscape_reset","dna_solo",
    "pad_mute","pad_solo","pad_level_db",
    "noise_open","noise_save","noise_reload","noise_reset","noise_solo",
    "noise_mechanical_db","noise_intake_db","noise_tire_db","noise_air_db","noise_color","noise_combustion_db",
    "dna_save","dna_reload","dna_reset","dna_group",
    "v3_aggression","v3_body","v3_character","v3_softness","v3_release_mass","v3_width","v3_load_response",
    "backfire_open","backfire_test","backfire_enable","backfire_solo",
    "backfire_save","backfire_reload","backfire_reset","backfire_intensity",
    "event_open","event_audition","event_enable","event_solo",
    "event_save","event_reload","event_reset","event_intensity",
    "start_open","start_audition","start_save","start_reload","start_reset","start_style",
    "eq_save","eq_reload","eq_reset"
  ]
};
/* REGISTRY_JSON_END */
var designProfile = typeof jsarguments !== 'undefined' ? String(jsarguments[1]) : 'ev';

function normalize(profile, name, args) {
    var bounds = DESIGN_REGISTRY.normalized[name];
    var mode = (DESIGN_REGISTRY.modes[profile] || {})[name];
    var result = [name], i, value;
    if (mode) {
        if (args.length !== 1) return null;
        value = String(args[0]);
        if (mode.indexOf(value) < 0) return null;
        return [name, value];
    }
    if (!bounds || args.length !== bounds.length) return null;
    for (i = 0; i < bounds.length; i += 1) {
        value = Number(args[i]);
        if (!isFinite(value)) return null;
        value = Math.max(bounds[i][0], Math.min(bounds[i][1], value));
        if (name.indexOf('bypass') >= 0) value = Math.floor(value);
        result.push(value);
    }
    return result;
}
function anything() {
    var message = normalize(designProfile, String(messagename), arrayfromargs(arguments));
    if (!message) return;
    // Apply synchronously before publishing the bounded state. No request echo.
    outlet(0, message);
    outlet(1, message);
}
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {normalize: normalize, registry: DESIGN_REGISTRY};
}
