/* Optional Noise stem only. No Sound DNA, Soundscape, or driving-state writes. */
autowatch = 1;
inlets = 1;
outlets = 1;

function noiseBound(value, low, high) {
    value = Number(value);
    return isFinite(value) ? Math.max(low, Math.min(high, value)) : low;
}
function noiseGain(db) { return db <= -60 ? 0 : Math.pow(10, db / 20); }

function NoiseControl(profile, emit) {
    this.profile = profile;
    this.emit = emit;
    this.last = {};
    this.state = {ignition: 0, engine_running: 0, rpm: 0, load: 0, throttle: 0, speed_kph: 0};
    this.params = {road_level_db: -60, noise_mechanical_db: -10, noise_intake_db: -15,
        noise_tire_db: -14, noise_air_db: -22, noise_color: 0.35};
}
NoiseControl.prototype.update = function () {
    var s = this.state, p = this.params;
    var electric = this.profile === 'ev' || this.profile === 'ioniq6n';
    var r = s.rpm / 8000, speed = s.speed_kph / 300;
    var effort = 0.72 * s.load + 0.28 * s.throttle;
    var values = {
        active: s.ignition && s.engine_running ? 1 : 0,
        stem: noiseGain(p.road_level_db),
        cadence: Math.max(12, s.rpm / (electric ? 20 : this.profile === 'v12' ? 10 : 12)),
        mechanical_hz: (electric ? 420 : this.profile === 'v12' ? 290 : 340) + s.rpm * 0.085,
        intake_hz: 510 + s.rpm * 0.105 + effort * 320 + p.noise_color * 700,
        air_hz: 1200 + p.noise_color * 2200 + speed * 500,
        mechanical: (0.035 + 0.08 * r + 0.09 * effort) * noiseGain(p.noise_mechanical_db),
        intake: (electric ? 0.35 : 1) * (0.005 + 0.18 * effort * effort) * noiseGain(p.noise_intake_db),
        tire: 0.11 * Math.pow(speed, 0.9) * noiseGain(p.noise_tire_db),
        air: 0.09 * Math.pow(speed, 1.65) * noiseGain(p.noise_air_db)
    };
    for (var key in values) if (Object.prototype.hasOwnProperty.call(values, key) && this.last[key] !== values[key]) {
        this.last[key] = values[key];
        this.emit(key, values[key]);
    }
};
NoiseControl.prototype.handle = function (name, args) {
    if(name === 'profile_active' && !Number(args[0])) {
        this.state.ignition=0; this.state.engine_running=0; this.update(); return;
    }
    if (Object.prototype.hasOwnProperty.call(this.state, name)) {
        this.state[name] = noiseBound(args[0], 0, name === 'rpm' ? 12000 : name === 'speed_kph' ? 300 : 1);
    } else if (Object.prototype.hasOwnProperty.call(this.params, name)) {
        this.params[name] = name === 'noise_color' ? noiseBound(args[0], 0, 1) :
            noiseBound(args[0], -60, name === 'road_level_db' ? 6 : 0);
    } else return;
    this.update();
};

var noiseController = new NoiseControl(
    typeof jsarguments !== 'undefined' && jsarguments.length > 1 ? String(jsarguments[1]) : 'ev',
    function (name, value) { if (typeof outlet !== 'undefined') outlet(0, name, value); }
);
function anything() { noiseController.handle(messagename, arrayfromargs(arguments)); }
function bang() { noiseController.update(); }
if (typeof module !== 'undefined' && module.exports) module.exports = {NoiseControl: NoiseControl};
