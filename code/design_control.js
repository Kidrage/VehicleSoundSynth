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
    "v3_aggression","v3_body","v3_character","v3_softness","v3_release_mass","v3_width","v3_load_response","v3_pressure_blend",
    "backfire_open","backfire_test","backfire_enable","backfire_solo",
    "backfire_save","backfire_reload","backfire_reset","backfire_intensity",
    "event_open","event_audition","event_enable","event_solo",
    "event_save","event_reload","event_reset","event_intensity",
    "start_open","start_audition","start_save","start_reload","start_reset","start_style",
    "eq_save","eq_reload","eq_reset"
  ],
  "contract_defaults": {
    "profiles": ["ev","v10","v12","ioniq6n","ferrari"],
    "bypass_drive_gate": true,
    "readback": "owner/UI state; not a measured DSP acknowledgement",
    "save": "not persisted",
    "context": "selected running profile; audio requires DSP on"
  },
  "contracts": [
    {"selectors":"eq_low eq_lowmid eq_highmid eq_high eq_bypass",
     "owner":"vehicle_bus_eq~", "payload":"ordered Hz/dB/Q tuple (bounds below); bypass 0/1",
     "readback":"bounded payload after synchronous engine application; saved state on reopen/actions",
     "save":"selected profile bus EQ namespace", "context":"EQ must not be bypassed; sustained diagnostic input"},
    {"selectors":"eq_save eq_reload eq_reset", "owner":"vehicle_bus_eq~",
     "payload":"action, no arguments", "save":"selected profile bus EQ namespace"},
    {"selectors":"compressor_threshold_db compressor_ratio compressor_attack_rate compressor_release_rate compressor_makeup_db compressor_bypass",
     "owner":"mix_master~", "payload":"one number (bounds below); rate is not milliseconds",
     "readback":"bounded payload after synchronous engine application; defaults on reopen",
     "context":"bypass off and signal above threshold; measure gain reduction, not just RMS"},
    {"selectors":"powertrain_level_db start_level_db transient_level_db soundscape_level_db road_level_db rumble_level_db",
     "owner":"module_mixer; one gain in destination stem", "payload":"one dB value, -60..6",
     "save":"<profile namespace>_module_mixer_noise_v1.json",
     "context":"active stem required; Noise -60 is exact mute, other -60 values are 0.001 gain; Rumble is DNA-fed"},
    {"selectors":"master_trim_db", "owner":"module_mixer; mix_master~ applies gain",
     "payload":"one dB value, -24..0", "save":"<profile namespace>_module_mixer_noise_v1.json"},
    {"selectors":"soundscape_enable soundscape_motion soundscape_space soundscape_pitch_follow soundscape_brightness",
     "owner":"profile cinematic_soundscape_host~", "payload":"one normalized number 0..1",
     "save":"existing profile Soundscape namespace, unchanged",
     "context":"SC enabled and lifecycle running; does not enable Noise; Space depends on preserved graph"},
    {"selectors":"soundscape_transpose", "owner":"profile cinematic_soundscape_host~",
     "payload":"one semitone value, -12..12", "save":"existing profile Soundscape namespace, unchanged"},
    {"selectors":"soundscape_open soundscape_save soundscape_reload soundscape_reset",
     "owner":"profile cinematic_soundscape_host~", "payload":"action, no arguments",
     "save":"existing profile Soundscape namespace, unchanged", "context":"opens actual live instrument; wait for reset before save/reload"},
    {"selectors":"soundscape_solo dna_solo noise_solo backfire_solo event_solo pad_solo",
     "owner":"vehicle_engine solo state", "payload":"one boolean 0/1",
     "context":"solo is not a gain or lifecycle override; Noise still needs its Main fader above -60"},
    {"selectors":"pad_mute", "owner":"legacy pad compatibility adapter",
     "payload":"one boolean 0/1", "context":"legacy alias; prefer soundscape_enable"},
    {"selectors":"pad_level_db", "owner":"legacy pad compatibility adapter",
     "payload":"one dB value", "context":"legacy alias; prefer Main soundscape_level_db; not an extra new gain"},
    {"selectors":"noise_open noise_save noise_reload noise_reset", "owner":"vehicle_noise_<profile>~",
     "payload":"action, no arguments", "save":"Ferrari noise_v2; other profiles noise_v1",
     "context":"live Noise designer; no save or automatic opening of Main road_level_db"},
    {"selectors":"noise_mechanical_db noise_intake_db", "owner":"noise_control",
     "payload":"one dB value, -60..0; -60 exact off", "save":"Ferrari noise_v2; others noise_v1",
     "context":"ignition + engine_running; Main Noise above -60; RPM/load dependent"},
    {"selectors":"noise_tire_db noise_air_db", "owner":"noise_control",
     "payload":"one dB value, -60..0; -60 exact off", "save":"Ferrari noise_v2; others noise_v1",
     "context":"speed > 0, running, Main Noise above -60; stationary silence is intended"},
    {"selectors":"noise_color", "owner":"noise_control", "payload":"one number 0..1",
     "save":"Ferrari noise_v2; others noise_v1", "context":"Noise enabled; shifts spectral centres, not DNA pitch"},
    {"selectors":"noise_combustion_db", "owner":"Ferrari Noise V2 raw residual return",
     "profiles":["ferrari"], "payload":"one dB value, -60..0; -60 exact off", "save":"ferrari_noise_v2.json",
     "context":"same pressure clock as DNA; independent of Main DNA gain; Main Noise above -60"},
    {"selectors":"dna_open", "owner":"profile runtime host", "payload":"action, no arguments",
     "context":"opens currently sounding DNA designer, not a second instrument"},
    {"selectors":"dna_save dna_reload dna_reset", "owner":"dna_v3_state",
     "profiles":["v10","v12","ferrari"], "payload":"action, no arguments", "save":"<profile>_sound_dna_v3.json"},
    {"selectors":"dna_group", "owner":"DNA V3 designer", "profiles":["v10","v12","ferrari"],
     "payload":"integer 0..4: all/core/body/character/upper", "context":"audition excludes old ICE idle; 0 restores ordinary blend"},
    {"selectors":"v3_aggression v3_body v3_character v3_softness v3_load_response v3_pressure_blend",
     "owner":"DNA V3 source", "profiles":["v10","v12","ferrari"], "payload":"one number 0..1",
     "save":"<profile>_sound_dna_v3.json", "context":"ICE: V3 fades in 1200..3000 RPM; Ferrari: all running RPM; body is spectral morph, pressure is separate blend"},
    {"selectors":"v3_release_mass", "owner":"DNA V3 source", "profiles":["v10","v12","ferrari"],
     "payload":"one number 0..1", "save":"<profile>_sound_dna_v3.json", "context":"test load release envelope, not steady-state RMS; ICE blend as above"},
    {"selectors":"v3_width", "owner":"dna_v3_output", "profiles":["v10","v12","ferrari"],
     "payload":"one number 0..1", "save":"<profile>_sound_dna_v3.json", "context":"V3 Side high-passed at 120 Hz; 0 mono; protected old ICE idle stereo unchanged"},
    {"selectors":"backfire_open backfire_save backfire_reload backfire_reset event_open event_save event_reload event_reset",
     "owner":"profile Pop designer / event adapter", "payload":"action, no arguments",
     "save":"existing Pop V3/V4 namespace, unchanged", "context":"IONIQ uses event_*; others backfire_*"},
    {"selectors":"backfire_test", "owner":"profile backfire adapter", "payload":"one intensity number 0..1",
     "context":"explicit preview; EV never gains automatic combustion events"},
    {"selectors":"event_audition", "owner":"IONIQ event adapter", "profiles":["ioniq6n"],
     "payload":"action, no arguments", "context":"explicit preview; driving event gates unchanged"},
    {"selectors":"backfire_enable event_enable backfire_intensity event_intensity",
     "owner":"profile Pop/event adapter", "payload":"one number 0..1",
     "context":"physical events retain lifecycle/mode gates; enable is not manual audition"},
    {"selectors":"start_open start_audition start_save start_reload start_reset",
     "owner":"profile Start Designer", "payload":"action, no arguments",
     "save":"existing profile Start namespace, unchanged", "context":"Open/Audition bypass driving gates; sound still needs DSP"},
    {"selectors":"start_style", "owner":"profile transient host", "payload":"cinematic or realistic",
     "context":"Ferrari remains procedural; V10 real one-shot is exclusive; no second starter"},
    {"selectors":"ev_mode", "owner":"EV sound-mode adapter", "profiles":["ev"],
     "payload":"relax / expressive / sport", "context":"pure sound mode, no drive integration"},
    {"selectors":"n_sound_mode", "owner":"IONIQ sound-mode adapter", "profiles":["ioniq6n"],
     "payload":"ignition / evolution / lightspeed", "context":"pure sound mode, no drive integration"},
    {"selectors":"eshift_enable", "owner":"DriveModel; engine receives notification only",
     "profiles":["ioniq6n"], "payload":"one boolean 0/1", "bypass_drive_gate":false,
     "readback":"actual model state; single notification bypasses audio driving gate",
     "context":"duplicate state idempotent; on redline 8000, off 9950; 300 ms mode transition"},
    {"selectors":"audio_enable drive_source tuning_context", "owner":"profile runtime host",
     "payload":"audio 0/1; source 0=manual, 1=auto, 2=external; context live/idle/cruise/load/lift/high_rpm",
     "context":"Held freezes driving input, never sound-design commands"},
    {"selectors":"save_profile_sound reload_profile_sound reset_profile_sound", "owner":"profile runtime host",
     "payload":"action, no arguments", "save":"Mixer + SC + EQ only; no compressor, DNA, Noise, Start or Pop"}
  ]
};
/* REGISTRY_JSON_END */
var designProfile = typeof jsarguments !== 'undefined' ? String(jsarguments[1]) : 'ev';

// Read-only contract query for audit tools. Never handles control messages or
// invents a second owner/readback/persistence path in the audio runtime.
function describe(name) {
    var i, key, entry, result;
    for (i = 0; i < DESIGN_REGISTRY.contracts.length; i += 1) {
        entry = DESIGN_REGISTRY.contracts[i];
        if (entry.selectors.split(' ').indexOf(name) < 0) continue;
        result = {};
        for (key in DESIGN_REGISTRY.contract_defaults) result[key] = DESIGN_REGISTRY.contract_defaults[key];
        for (key in entry) if (key !== 'selectors') result[key] = entry[key];
        if (DESIGN_REGISTRY.normalized[name]) result.bounds = DESIGN_REGISTRY.normalized[name];
        return result;
    }
    return null;
}

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
    module.exports = {normalize: normalize, describe: describe, registry: DESIGN_REGISTRY};
}
