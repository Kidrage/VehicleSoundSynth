/* Shared sample adapter; Ferrari V3 remains the default/compatibility interface.
 * ICE keeps the existing burst scheduler. IONIQ's host owns mode/eShift gates;
 * EV remains preview-only (its previous automatic event seam was silent).
 * Outlets: voice commands, existing burst scheduler commands.
 * No timers, audio synthesis, sample banks, or changes to the shared drivetrain.
 */
autowatch = 1;
inlets = 1;
outlets = 2;

function PopControl(emit, profile) {
    this.emit = emit;
    this.profile = /^(ev|v10|v12|ioniq6n|ferrari)$/.test(profile) ? profile : 'ferrari';
    this.enabled = 1;
    this.profileActive = 1;
    this.ignition = 0;
    this.running = 0;
    this.intensity = {v10: 0.82, v12: 0.55, ioniq6n: 0.72}[this.profile] || 0.65;
    this.stemDb = -6;
    this.pitch = {v10: -1, v12: -2, ev: 1}[this.profile] || 0;
    this.loaded = false;
    this.voice = 0;
    this.randomState = 9137;
}
function bounded(value, low, high) {
    value = Number(value);
    return isFinite(value) ? Math.max(low, Math.min(high, value)) : low;
}
PopControl.prototype.random = function () {
    this.randomState = (1664525 * this.randomState + 1013904223) >>> 0;
    return this.randomState / 4294967296;
};
PopControl.prototype.stop = function () {
    this.emit(1, ['stop']);
    this.emit(0, ['target', 0]);
    this.emit(0, ['stop']);
};
PopControl.prototype.hit = function (pitch, strength) {
    strength = bounded(strength, 0, 1);
    if (!this.loaded || strength === 0) return;
    // Do not reproduce the old octave impact sweep. Only subtle variation.
    var rate = Math.pow(2, (this.pitch + bounded(pitch, -6, 1) * 0.06
        + (this.random() - 0.5) * 0.24) / 12);
    var gain = strength * (0.35 + 0.65 * this.intensity)
        * (0.96 + 0.04 * this.random()) * Math.pow(10, this.stemDb / 20);
    this.voice = 1 + (this.voice % 2);
    this.emit(0, ['target', this.voice]);
    this.emit(0, ['play', 240 / rate, gain]);
};
PopControl.prototype.handle = function (name, args) {
    var value = args[0];
    if (name === 'loaded') { this.loaded = Number(value) > 0; return; }
    if (name === 'pitch') { this.pitch = bounded(value, -6, 3); return; }
    if (name === 'backfire_intensity' || name === 'event_intensity') { this.intensity = bounded(value, 0, 1); return; }
    if (name === 'transient_level_db') { this.stemDb = bounded(value, -60, 6); return; }
    if (name === 'backfire_seed') {
        this.randomState = (Number(value) >>> 0) || 9137;
        this.emit(1, ['seed', value]); return;
    }
    if (name === 'ignition' || name === 'engine_running' || name === 'backfire_enable' || name === 'event_enable' || name === 'profile_active') {
        var key = name === 'engine_running' ? 'running' : (name === 'profile_active' ? 'profileActive' :
            (name === 'backfire_enable' || name === 'event_enable' ? 'enabled' : 'ignition'));
        var previous = this[key];
        this[key] = Number(value) > 0 ? 1 : 0;
        if (previous && !this[key]) this.stop();
        return;
    }
    if (name === 'stop') { this.stop(); return; }
    if (name === 'hit') { this.hit(args[0], args[1]); return; }
    // Explicit preview retains the old ignition-independent audition contract.
    if (name === 'audition') { this.hit(0, 1); return; }
    if (name === 'backfire_test' && Number(value) === 1) {
        this.emit(1, ['burst', 1]); return;
    }
    if (!(this.enabled && this.ignition && this.running && this.profileActive)) return;
    if (name === 'event_hit' && this.profile === 'ioniq6n') {
        this.hit(0, bounded(value, 0, 1)); return;
    }
    if (this.profile === 'ev' || this.profile === 'ioniq6n') return;
    if (name === 'overrun' && Number(value) > 0) {
        this.emit(1, ['burst', bounded(value, 0, 1)]);
    } else if (Number(value) === 1 &&
        (name === 'shift' || name === 'intake_backfire' || name === 'exhaust_pop' || name === 'pop')) {
        this.hit(0, name === 'shift' ? 0.75 : 1);
    }
};
var controller = new PopControl(function (index, message) {
    if (typeof outlet !== 'undefined') outlet(index, message);
}, typeof jsarguments !== 'undefined' ? jsarguments[1] : 'ferrari');
function anything() { controller.handle(messagename, arrayfromargs(arguments)); }
function notifydeleted() { controller.stop(); }
if (typeof module !== 'undefined' && module.exports) module.exports = {PopControl: PopControl};
