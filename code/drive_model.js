/* VehicleSoundSynth deterministic control-rate drivetrain.
 *
 * The module is ES5-compatible for Max's built-in js object and can also be
 * required by Node for regression traces. One bang is exactly one 20 ms step;
 * control messages only update stored state and never integrate time.
 */

var DRIVE_CONFIG = {
    ev: {
        idle: 650.0,
        flare: 650.0,
        catchSeconds: 0.25,
        singleSpeedRatio: 31.0
    },
    v10: {
        idle: 740.0,
        flare: 1050.0,
        catchSeconds: 0.85,
        launchRpm: 2600.0,
        ratios: [114.2, 76.7, 55.5, 43.8, 34.3, 27.7, 22.6],
        upBase: 5800.0,
        upThrottle: 2500.0,
        downBase: 2100.0,
        downThrottle: 1500.0,
        shiftCutSeconds: 0.04,
        shiftSweepSeconds: 0.09,
        shiftEngageSeconds: 0.07,
        shiftFloor: 0.65,
        shiftLockSeconds: 0.45,
        overrunMinRpm: 1600.0,
        overrunArmThrottle: 0.35,
        overrunCloseThrottle: 0.18,
        overrunMinDrop: 0.35,
        overrunArmSeconds: 0.12,
        overrunWindowSeconds: 0.18,
        overrunCooldownSeconds: 0.30
    },
    ferrari: {
        idle: 740.0,
        flare: 1050.0,
        catchSeconds: 0.85,
        launchRpm: 2600.0,
        ratios: [114.2, 76.7, 55.5, 43.8, 34.3, 27.7, 22.6],
        upBase: 5800.0,
        upThrottle: 2500.0,
        downBase: 2100.0,
        downThrottle: 1500.0,
        shiftCutSeconds: 0.04,
        shiftSweepSeconds: 0.09,
        shiftEngageSeconds: 0.07,
        shiftFloor: 0.65,
        shiftLockSeconds: 0.45,
        overrunMinRpm: 1600.0,
        overrunArmThrottle: 0.35,
        overrunCloseThrottle: 0.18,
        overrunMinDrop: 0.35,
        overrunArmSeconds: 0.12,
        overrunWindowSeconds: 0.18,
        overrunCooldownSeconds: 0.30
    },
    v12: {
        idle: 780.0,
        flare: 1100.0,
        catchSeconds: 0.85,
        launchRpm: 2400.0,
        ratios: [107.0, 73.5, 55.9, 44.5, 35.6, 29.0, 24.2],
        upBase: 6200.0,
        upThrottle: 2400.0,
        downBase: 2200.0,
        downThrottle: 1600.0,
        shiftCutSeconds: 0.05,
        shiftSweepSeconds: 0.12,
        shiftEngageSeconds: 0.10,
        shiftFloor: 0.72,
        shiftLockSeconds: 0.55,
        overrunMinRpm: 1600.0,
        overrunArmThrottle: 0.35,
        overrunCloseThrottle: 0.18,
        overrunMinDrop: 0.35,
        overrunArmSeconds: 0.12,
        overrunWindowSeconds: 0.18,
        overrunCooldownSeconds: 0.30
    },
    ioniq6n: {
        idle: 650.0,
        flare: 1450.0,
        catchSeconds: 0.65,
        electric: true,
        singleSpeedRatio: 31.0,
        eShiftDefault: 1,
        maxGear: 8,
        launchRpm: 2600.0,
        virtualRedline: 8000.0,
        absoluteRpmLimit: 10000.0,
        modeTransitionSeconds: 0.30,
        ratios: [75 * 8000 / 6300, 58 * 8000 / 6300, 47 * 8000 / 6300,
            39 * 8000 / 6300, 33 * 8000 / 6300, 28 * 8000 / 6300,
            24 * 8000 / 6300, 21 * 8000 / 6300],
        upBase: 5000.0,
        upThrottle: 2600.0,
        downBase: 1750.0,
        downThrottle: 850.0,
        shiftCutSeconds: 0.04,
        shiftSweepSeconds: 0.04,
        shiftEngageSeconds: 0.18,
        shiftFloor: 0.62,
        shiftLockSeconds: 0.36
    }
};

function clamp(value, low, high) {
    return Math.max(low, Math.min(high, value));
}

function smoothstep(value) {
    var x = clamp(value, 0.0, 1.0);
    return x * x * (3.0 - 2.0 * x);
}

function drivetrainDrag(speed, throttle) {
    // Preserve the original powered aero load, but make a released vehicle
    // settle decisively near zero while retaining more high-speed inertia.
    var aero = 0.5 + 0.00012 * speed * speed;
    var coast = 0.65 + 1.45 / (1.0 + Math.pow(speed / 35.0, 2.0));
    var coastMix = 1.0 - smoothstep(throttle / 0.08);
    return aero + (coast - aero) * coastMix;
}

function DriveModel(profile) {
    if (!DRIVE_CONFIG[profile]) {
        throw new Error("Unsupported drive profile: " + profile);
    }
    this.profile = profile;
    this.config = DRIVE_CONFIG[profile];
    this.reset();
}

DriveModel.prototype.reset = function () {
    this.time = 0.0;
    this.ignition = 0;
    this.running = 0;
    this.auto = 0;
    this.manualThrottle = 0.0;
    this.manualBrake = 0.0;
    this.throttle = 0.0;
    this.brake = 0.0;
    this.speed = 0.0;
    this.rpm = this.config.idle;
    this.accel = 0.0;
    this.gear = 1;
    this.startElapsed = -1.0;
    this.shift = null;
    this.shiftCut = 1.0;
    this.eShiftEnabled = this.config.eShiftDefault ? 1 : 0;
    this.modeTransition = null;
    this.launchCoupled = false;
    this.lastShiftEnd = -999.0;
    this.overrunArmElapsed = 0.0;
    this.overrunArmed = 0;
    this.overrunReleaseElapsed = -1.0;
    this.overrunReleaseFrom = 0.0;
    this.overrunPeakThrottle = 0.0;
    this.overrunCooldown = 0.0;
    this.liftBrake = 0.0;
};

DriveModel.prototype.clearOverrun = function () {
    this.overrunArmElapsed = 0.0;
    this.overrunArmed = 0;
    this.overrunReleaseElapsed = -1.0;
    this.overrunReleaseFrom = 0.0;
    this.overrunPeakThrottle = 0.0;
};

DriveModel.prototype.handle = function (name, args) {
    var value = args.length ? Number(args[0]) : 0.0;
    var events = [];
    if (this.profile === "ioniq6n" &&
            /^(throttle|brake|auto|eshift_enable|gear|rpm|ignition|start)$/.test(name) &&
            !isFinite(value)) {
        return events;
    }
    if (name === "throttle") {
        this.manualThrottle = clamp(value, 0.0, 1.0);
    } else if (name === "brake") {
        this.manualBrake = clamp(value, 0.0, 1.0);
    } else if (name === "auto") {
        this.auto = value ? 1 : 0;
    } else if (name === "eshift_enable" && this.profile === "ioniq6n") {
        if (this.eShiftEnabled === (value ? 1 : 0)) {
            return [["eshift_enable", this.eShiftEnabled]];
        }
        this.eShiftEnabled = value ? 1 : 0;
        if (this.shift) {
            events.push(["shift", 0]);
        }
        this.shift = null;
        this.shiftCut = 1.0;
        this.gear = this.eShiftEnabled ? this.selectIoniqGear() : 1;
        this.launchCoupled = this.speed * this.config.ratios[this.gear - 1] >=
            this.config.idle + this.throttle * (this.config.launchRpm - this.config.idle);
        this.modeTransition = this.running && this.startElapsed >= this.config.catchSeconds ?
            {elapsed: 0.0, fromRpm: this.rpm} : null;
        this.lastShiftEnd = this.time;
        events.push(["eshift_enable", this.eShiftEnabled]);
        events.push(["shift_cut", 1.0]);
        events.push(["gear", this.gear]);
    } else if (this.profile === "ioniq6n" && (name === "gear" || name === "rpm")) {
        // External telemetry bypasses this integrator in the runtime host.
        // An Internal write is not a manual shift and must not publish a lie.
        events.push([name, name === "gear" ? this.gear : this.rpm]);
    } else if (name === "ignition") {
        this.ignition = value ? 1 : 0;
        events.push(["ignition", this.ignition]);
        if (!this.ignition) {
            this.running = 0;
            this.modeTransition = null;
            this.launchCoupled = false;
            this.throttle = 0.0;
            this.brake = 0.0;
            this.shift = null;
            this.shiftCut = 1.0;
            this.clearOverrun();
            this.overrunCooldown = 0.0;
            this.liftBrake = 0.0;
            events.push(["shift_cut", 1.0]);
        }
    } else if (name === "start" && value && this.ignition) {
        // qmetro may already have ticked for an arbitrary time while the
        // patcher was open. Every lifecycle curve must be relative to this
        // start edge, never to patch load time.
        this.time = 0.0;
        this.running = 1;
        this.speed = 0.0;
        this.rpm = this.config.flare;
        this.gear = 1;
        this.startElapsed = 0.0;
        this.modeTransition = null;
        this.launchCoupled = false;
        this.shift = null;
        this.shiftCut = 1.0;
        this.lastShiftEnd = -999.0;
        this.clearOverrun();
        this.overrunCooldown = 0.0;
        this.liftBrake = 0.0;
        events.push(["gear", 1]);
        events.push(["start", 1]);
    } else {
        events.push([name].concat(args));
    }
    return events;
};

DriveModel.prototype.effectivePedals = function () {
    if (!this.running) {
        return [0.0, 0.0];
    }
    if (this.startElapsed >= 0.0 && this.startElapsed < this.config.catchSeconds) {
        return [0.0, 0.0];
    }
    if (!this.auto) {
        return [this.manualThrottle, this.manualBrake];
    }
    var driveTime = Math.max(0.0, this.time - 2.0);
    if (driveTime < 6.0) {
        return [0.16 + 0.78 * smoothstep(driveTime / 6.0), 0.0];
    }
    if (driveTime < 14.0) {
        return [0.94, 0.0];
    }
    if (driveTime < 18.0) {
        return [0.20 * (1.0 - smoothstep((driveTime - 14.0) / 4.0)), 0.0];
    }
    return [0.0, 0.80];
};

DriveModel.prototype.normalIceTarget = function () {
    if (this.profile === "ioniq6n") {
        return this.ioniqTarget();
    }
    var coupled = Math.max(
        this.config.idle,
        this.speed * this.config.ratios[this.gear - 1]
    );
    var freeRev = this.config.idle +
        this.throttle * (this.config.launchRpm - this.config.idle);
    var clutch = smoothstep((this.speed - 4.0) / 20.0);
    return freeRev * (1.0 - clutch) + coupled * clutch;
};

DriveModel.prototype.selectIoniqGear = function () {
    var best = this.config.maxGear;
    var error = Infinity;
    var i, predicted, distance;
    for (i = 0; i < this.config.ratios.length; i += 1) {
        predicted = Math.max(this.config.idle, this.speed * this.config.ratios[i]);
        distance = Math.abs(predicted - this.rpm);
        if (predicted <= this.config.virtualRedline + 0.000001 && distance <= error) {
            best = i + 1;
            error = distance;
        }
    }
    return this.speed < 1.0 ? 1 : best;
};

DriveModel.prototype.ioniqTarget = function () {
    var coupled = clamp(this.speed * this.config.ratios[this.gear - 1],
        this.config.idle, this.config.virtualRedline);
    var free = this.config.idle + this.throttle *
        (this.config.launchRpm - this.config.idle);
    if (this.gear === 1 && this.speed < 1.0) {
        this.launchCoupled = false;
    }
    if (!this.launchCoupled && coupled >= free) {
        this.launchCoupled = true;
    }
    // Engagement occurs when wheel speed catches the free target, not via
    // a speed-only blend that drags a 5200 RPM flare down to 1800 RPM.
    return this.launchCoupled ? coupled : Math.max(coupled, free);
};

DriveModel.prototype.updateModeTransition = function (dt) {
    var transition = this.modeTransition;
    var target = this.eShiftEnabled ? this.ioniqTarget() :
        this.config.idle + this.speed * this.config.singleSpeedRatio;
    transition.elapsed += dt;
    this.rpm = clamp(transition.fromRpm + (target - transition.fromRpm) *
        smoothstep(transition.elapsed / this.config.modeTransitionSeconds),
        this.config.idle, this.config.absoluteRpmLimit);
    if (transition.elapsed >= this.config.modeTransitionSeconds) {
        this.modeTransition = null;
        this.lastShiftEnd = this.time;
    }
};

DriveModel.prototype.updateOverrun = function (dt, previousThrottle, events) {
    var drop;
    var dropStrength;
    var rpmStrength;
    var strength;
    if (this.profile === "ev" || this.config.electric || !this.running ||
            (this.startElapsed >= 0.0 && this.startElapsed < this.config.catchSeconds)) {
        this.clearOverrun();
        return;
    }

    this.overrunCooldown = Math.max(0.0, this.overrunCooldown - dt);
    if (!this.overrunArmed) {
        if (this.throttle >= this.config.overrunArmThrottle &&
                this.rpm >= this.config.overrunMinRpm) {
            this.overrunArmElapsed += dt;
            this.overrunPeakThrottle = Math.max(this.overrunPeakThrottle, this.throttle);
            if (this.overrunArmElapsed >= this.config.overrunArmSeconds) {
                this.overrunArmed = 1;
            }
        } else {
            this.overrunArmElapsed = 0.0;
            this.overrunPeakThrottle = this.throttle;
        }
        return;
    }

    this.overrunPeakThrottle = Math.max(this.overrunPeakThrottle, previousThrottle);
    if (this.overrunReleaseElapsed < 0.0 && previousThrottle - this.throttle >= 0.02) {
        this.overrunReleaseElapsed = 0.0;
        this.overrunReleaseFrom = Math.max(this.overrunPeakThrottle, previousThrottle);
    }
    if (this.overrunReleaseElapsed < 0.0) {
        return;
    }

    this.overrunReleaseElapsed += dt;
    drop = this.overrunReleaseFrom - this.throttle;
    if (this.throttle <= this.config.overrunCloseThrottle &&
            drop >= this.config.overrunMinDrop &&
            this.overrunReleaseElapsed <= this.config.overrunWindowSeconds &&
            this.rpm >= this.config.overrunMinRpm && this.overrunCooldown <= 0.0) {
        dropStrength = clamp(drop / 0.8, 0.0, 1.0);
        rpmStrength = clamp((this.rpm - this.config.overrunMinRpm) / 5000.0, 0.0, 1.0);
        strength = clamp(0.35 + 0.40 * dropStrength + 0.25 * rpmStrength, 0.0, 1.0);
        events.push(["overrun", strength]);
        this.clearOverrun();
        this.overrunCooldown = this.config.overrunCooldownSeconds;
    } else if (this.overrunReleaseElapsed > this.config.overrunWindowSeconds ||
            this.throttle > this.overrunReleaseFrom - 0.05) {
        this.clearOverrun();
    }
};

DriveModel.prototype.beginShift = function (direction, events) {
    var maxGear = this.config.maxGear || 7;
    var nextGear = clamp(this.gear + direction, 1, maxGear);
    if (nextGear === this.gear) {
        return;
    }
    if (this.profile === "ioniq6n" && (this.modeTransition || !this.launchCoupled ||
            this.speed * this.config.ratios[nextGear - 1] > this.config.virtualRedline + 0.000001)) {
        return;
    }
    this.shift = {
        elapsed: 0.0,
        direction: direction,
        fromRpm: this.rpm,
        nextGear: nextGear
    };
    this.gear = nextGear;
    events.push(["shift_dir", direction]);
    events.push(["shift", 1]);
    events.push(["gear", this.gear]);
};

DriveModel.prototype.updateShift = function (dt, events) {
    var cutEnd = this.config.shiftCutSeconds;
    var sweepEnd = cutEnd + this.config.shiftSweepSeconds;
    var total = sweepEnd + this.config.shiftEngageSeconds;
    var elapsed = this.shift.elapsed + dt;
    var target = Math.max(
        this.config.idle,
        this.speed * this.config.ratios[this.gear - 1]
    );
    if (this.profile === "ioniq6n") {
        target = Math.min(target, this.config.virtualRedline);
    }
    if (elapsed <= cutEnd) {
        this.shiftCut = 1.0 - (1.0 - this.config.shiftFloor) *
            smoothstep(elapsed / cutEnd);
    } else if (elapsed <= sweepEnd) {
        this.shiftCut = this.config.shiftFloor;
    } else {
        this.shiftCut = this.config.shiftFloor +
            (1.0 - this.config.shiftFloor) *
            smoothstep((elapsed - sweepEnd) / this.config.shiftEngageSeconds);
    }
    this.rpm = this.shift.fromRpm +
        (target - this.shift.fromRpm) * smoothstep(elapsed / total);
    this.shift.elapsed = elapsed;
    if (elapsed >= total) {
        this.rpm = target;
        this.shift = null;
        this.shiftCut = 1.0;
        this.lastShiftEnd = this.time;
        events.push(["shift", 0]);
    }
};

DriveModel.prototype.maybeShift = function (events) {
    if (this.shift || this.time - this.lastShiftEnd < this.config.shiftLockSeconds ||
            (this.profile === "ioniq6n" && (this.modeTransition || !this.launchCoupled))) {
        return;
    }
    var up = this.config.upBase + this.config.upThrottle * this.throttle;
    var down = this.config.downBase + this.config.downThrottle * this.throttle;
    if (this.rpm > up && this.gear < (this.config.maxGear || 7)) {
        this.beginShift(1, events);
    } else if (this.rpm < down && this.gear > 1) {
        this.beginShift(-1, events);
    }
};

DriveModel.prototype.tick = function (dt) {
    var events = [];
    var pedals;
    var force;
    var drag;
    var liftDrag;
    var serviceBrake;
    var target;
    var alpha;
    var previousThrottle;
    dt = clamp(Number(dt) || 0.02, 0.001, 0.1);
    this.time += dt;
    previousThrottle = this.throttle;
    pedals = this.effectivePedals();
    this.throttle = pedals[0];
    this.brake = pedals[1];
    if (this.running && this.speed >= 25.0 && this.brake < 0.05 &&
            previousThrottle >= 0.35 && previousThrottle - this.throttle >= 0.18) {
        // A fast pedal edge requests temporary engine braking. Progressive
        // trigger release arrives as small steps and therefore preserves the
        // existing natural coast curve.
        this.liftBrake = Math.max(
            this.liftBrake,
            clamp((previousThrottle - this.throttle) / 0.8, 0.0, 1.0)
        );
    } else {
        this.liftBrake = Math.max(0.0, this.liftBrake - dt / 0.8);
    }
    if (this.throttle > 0.25 || this.brake >= 0.05) {
        this.liftBrake = 0.0;
    }
    drag = drivetrainDrag(this.speed, this.throttle);
    serviceBrake = 33.0 * Math.pow(this.brake, 1.35);
    liftDrag = this.liftBrake * (5.0 + 0.055 * this.speed);
    force = this.throttle * (37.5 - 0.065 * this.speed) - drag - serviceBrake - liftDrag;
    if (this.running) {
        this.speed = clamp(this.speed + dt * force, 0.0, 300.0);
    } else {
        this.speed = clamp(this.speed - dt * (drag + serviceBrake), 0.0, 300.0);
    }
    this.accel = clamp(force / 37.5, -1.0, 1.0);

    if (this.startElapsed >= 0.0 && this.startElapsed < this.config.catchSeconds) {
        this.startElapsed += dt;
        this.rpm = this.config.flare +
            (this.config.idle - this.config.flare) *
            smoothstep(this.startElapsed / this.config.catchSeconds);
    } else if (this.profile === "ioniq6n" && this.modeTransition) {
        this.updateModeTransition(dt);
    } else if (this.profile === "ev" ||
            (this.profile === "ioniq6n" && !this.eShiftEnabled)) {
        target = this.config.idle + this.speed * this.config.singleSpeedRatio;
        this.rpm = clamp(target, this.config.idle, 10000.0);
    } else if (this.shift) {
        this.updateShift(dt, events);
    } else {
        target = this.normalIceTarget();
        if (this.liftBrake > 0.0 && this.profile !== "ioniq6n") {
            target = Math.max(
                this.config.idle,
                target * (1.0 - 0.18 * this.liftBrake)
            );
        }
        alpha = 1.0 - Math.exp(
            -dt / (target >= this.rpm ? 0.12 : (this.liftBrake > 0.0 ? 0.08 : 0.16))
        );
        this.rpm += (target - this.rpm) * alpha;
        this.rpm = clamp(this.rpm, this.config.idle,
            this.profile === "ioniq6n" ? this.config.virtualRedline : 10000.0);
        this.maybeShift(events);
    }

    this.updateOverrun(dt, previousThrottle, events);

    events.push(["speed_kph", this.speed]);
    events.push(["rpm", this.rpm]);
    events.push(["throttle", this.throttle]);
    events.push(["brake", this.brake]);
    events.push(["load", clamp(this.throttle - 0.35 * this.brake, -1.0, 1.0)]);
    events.push(["accel", this.accel]);
    events.push(["shift_cut", this.shiftCut]);
    return events;
};

DriveModel.prototype.snapshot = function () {
    var state = {
        time: this.time,
        speed: this.speed,
        rpm: this.rpm,
        throttle: this.throttle,
        brake: this.brake,
        accel: this.accel,
        gear: this.gear,
        shifting: this.shift ? 1 : 0,
        shiftCut: this.shiftCut,
        liftBrake: this.liftBrake
    };
    if (this.profile === "ioniq6n") {
        state.eShiftEnabled = this.eShiftEnabled;
    }
    return state;
};

function outputEvents(events) {
    var index;
    if (typeof outlet === "undefined") {
        return;
    }
    for (index = 0; index < events.length; index += 1) {
        outlet(0, events[index]);
    }
}

var maxProfile = "ev";
if (typeof jsarguments !== "undefined" && jsarguments.length > 1) {
    maxProfile = String(jsarguments[1]);
}
var maxModel = new DriveModel(maxProfile);

function loadbang() {
    outputEvents([["gear", 1], ["rpm", maxModel.config.idle], ["shift_cut", 1.0]]);
}

function bang() {
    outputEvents(maxModel.tick(0.02));
}

function anything() {
    var args = typeof arrayfromargs === "undefined" ? [] : arrayfromargs(arguments);
    outputEvents(maxModel.handle(String(messagename), args));
}

if (typeof module !== "undefined" && module.exports) {
    module.exports = {
        DRIVE_CONFIG: DRIVE_CONFIG,
        DriveModel: DriveModel,
        clamp: clamp,
        smoothstep: smoothstep
    };
}
