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
        shiftLockSeconds: 0.45
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
        shiftLockSeconds: 0.55
    }
};

function clamp(value, low, high) {
    return Math.max(low, Math.min(high, value));
}

function smoothstep(value) {
    var x = clamp(value, 0.0, 1.0);
    return x * x * (3.0 - 2.0 * x);
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
    this.lastShiftEnd = -999.0;
};

DriveModel.prototype.handle = function (name, args) {
    var value = args.length ? Number(args[0]) : 0.0;
    var events = [];
    if (name === "throttle") {
        this.manualThrottle = clamp(value, 0.0, 1.0);
    } else if (name === "brake") {
        this.manualBrake = clamp(value, 0.0, 1.0);
    } else if (name === "auto") {
        this.auto = value ? 1 : 0;
    } else if (name === "ignition") {
        this.ignition = value ? 1 : 0;
        events.push(["ignition", this.ignition]);
        if (!this.ignition) {
            this.running = 0;
            this.throttle = 0.0;
            this.brake = 0.0;
            this.shift = null;
            this.shiftCut = 1.0;
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
        this.shift = null;
        this.shiftCut = 1.0;
        this.lastShiftEnd = -999.0;
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
    return [0.0, 0.42];
};

DriveModel.prototype.normalIceTarget = function () {
    var coupled = Math.max(
        this.config.idle,
        this.speed * this.config.ratios[this.gear - 1]
    );
    var freeRev = this.config.idle +
        this.throttle * (this.config.launchRpm - this.config.idle);
    var clutch = smoothstep((this.speed - 4.0) / 20.0);
    return freeRev * (1.0 - clutch) + coupled * clutch;
};

DriveModel.prototype.beginShift = function (direction, events) {
    var nextGear = clamp(this.gear + direction, 1, 7);
    if (nextGear === this.gear) {
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
    if (this.shift || this.time - this.lastShiftEnd < this.config.shiftLockSeconds) {
        return;
    }
    var up = this.config.upBase + this.config.upThrottle * this.throttle;
    var down = this.config.downBase + this.config.downThrottle * this.throttle;
    if (this.rpm > up && this.gear < 7) {
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
    var target;
    var alpha;
    dt = clamp(Number(dt) || 0.02, 0.001, 0.1);
    this.time += dt;
    pedals = this.effectivePedals();
    this.throttle = pedals[0];
    this.brake = pedals[1];
    drag = 0.5 + 0.00012 * this.speed * this.speed;
    force = this.throttle * (34.0 - 0.07 * this.speed) - drag - this.brake * 55.0;
    if (this.running) {
        this.speed = clamp(this.speed + dt * force, 0.0, 300.0);
    } else {
        this.speed = clamp(this.speed - dt * (drag + this.brake * 55.0), 0.0, 300.0);
    }
    this.accel = clamp(force / 34.0, -1.0, 1.0);

    if (this.startElapsed >= 0.0 && this.startElapsed < this.config.catchSeconds) {
        this.startElapsed += dt;
        this.rpm = this.config.flare +
            (this.config.idle - this.config.flare) *
            smoothstep(this.startElapsed / this.config.catchSeconds);
    } else if (this.profile === "ev") {
        target = this.config.idle + this.speed * this.config.singleSpeedRatio;
        this.rpm = clamp(target, this.config.idle, 10000.0);
    } else if (this.shift) {
        this.updateShift(dt, events);
    } else {
        target = this.normalIceTarget();
        alpha = 1.0 - Math.exp(-dt / (target >= this.rpm ? 0.12 : 0.16));
        this.rpm += (target - this.rpm) * alpha;
        this.rpm = clamp(this.rpm, this.config.idle, 10000.0);
        this.maybeShift(events);
    }

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
    return {
        time: this.time,
        speed: this.speed,
        rpm: this.rpm,
        throttle: this.throttle,
        brake: this.brake,
        accel: this.accel,
        gear: this.gear,
        shifting: this.shift ? 1 : 0,
        shiftCut: this.shiftCut
    };
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
