/* VehicleSoundSynth manual pedal input mapping.
 *
 * Max 8.6.5's built-in gamepad object emits named controller events. This
 * module keeps the fixed LT/RT mapping, normalization, smoothing, source
 * exclusivity, and fail-safe releases out of the drivetrain model.
 */

inlets = 1;
outlets = 3;

function clamp(value, low, high) {
    return Math.max(low, Math.min(high, value));
}

function normalizeTrigger(raw, deadZone, signedRange) {
    var normalized = Number(raw);
    if (signedRange) {
        normalized = (normalized + 1.0) * 0.5;
    }
    normalized = clamp(normalized, 0.0, 1.0);
    deadZone = clamp(Number(deadZone) || 0.0, 0.0, 0.25);
    if (normalized <= deadZone) {
        return 0.0;
    }
    return clamp((normalized - deadZone) / (1.0 - deadZone), 0.0, 1.0);
}

function ManualInputModel() {
    this.manual = 0;
    this.source = "keyboard";
    this.throttle = 0.0;
    this.brake = 0.0;
    this.throttleTarget = 0.0;
    this.brakeTarget = 0.0;
    this.keyboardThrottle = 0.0;
    this.keyboardBrake = 0.0;
    this.deadZone = 0.02;
    this.smoothingMs = 30.0;
    this.leftTriggerSigned = 0;
    this.rightTriggerSigned = 0;
    this.connected = 0;
    this.deviceInstance = -1;
    this.deviceName = "No gamepad detected";
    this.deviceType = "unknown";
}

ManualInputModel.prototype.release = function () {
    this.throttle = 0.0;
    this.brake = 0.0;
    this.throttleTarget = 0.0;
    this.brakeTarget = 0.0;
    this.keyboardThrottle = 0.0;
    this.keyboardBrake = 0.0;
    return [["throttle", 0.0], ["brake", 0.0]];
};

ManualInputModel.prototype.applyKeyboardPedals = function () {
    this.brake = this.keyboardBrake;
    this.throttle = this.brake > 0.0 ? 0.0 : this.keyboardThrottle;
    this.throttleTarget = this.throttle;
    this.brakeTarget = this.brake;
    return [["throttle", this.throttle], ["brake", this.brake]];
};

ManualInputModel.prototype.deviceEvents = function () {
    var identity = (this.deviceName + " " + this.deviceType).toLowerCase();
    var analogWarning = identity.indexOf("pro controller") >= 0 ||
        identity.indexOf("switch_pro") >= 0;
    return [
        ["detected", this.connected],
        ["device_name", this.deviceName],
        ["device_type", this.deviceType],
        ["analog_warning", analogWarning ? 1 : 0]
    ];
};

ManualInputModel.prototype.handle = function (name, args) {
    var value = args.length ? args[0] : 0;
    var pedal;
    var signedProperty;
    var rawTrigger;
    var normalizedTrigger;
    var events;
    var nextInstance;
    var status;
    if (name === "manual") {
        this.manual = Number(value) ? 1 : 0;
        if (!this.manual) {
            return this.release();
        }
    } else if (name === "source") {
        value = String(value).toLowerCase();
        if (value !== "keyboard" && value !== "gamepad") {
            value = "keyboard";
        }
        if (value !== this.source) {
            this.source = value;
            return this.release();
        }
    } else if (name === "keyboard_throttle" && this.manual && this.source === "keyboard") {
        this.keyboardThrottle = clamp(Number(value) || 0.0, 0.0, 1.0);
        return this.applyKeyboardPedals();
    } else if (name === "keyboard_brake" && this.manual && this.source === "keyboard") {
        this.keyboardBrake = clamp(Number(value) || 0.0, 0.0, 1.0);
        return this.applyKeyboardPedals();
    } else if (name === "dead_zone") {
        this.deadZone = clamp(Number(value) || 0.0, 0.0, 0.25);
    } else if (name === "smoothing_ms") {
        this.smoothingMs = clamp(Number(value) || 0.0, 0.0, 100.0);
    } else if (name === "device_info") {
        // Max 8.6.5 gamepad outlet 2: instance_id, device_index, name, type.
        // Track the instance, not the reusable HID device index, so a hot swap
        // cannot inherit a held pedal from the controller it replaced.
        nextInstance = args.length ? Number(args[0]) : -1;
        events = nextInstance !== this.deviceInstance && this.source === "gamepad" ?
            this.release() : [];
        this.connected = 1;
        this.deviceInstance = nextInstance;
        this.deviceName = args.length > 3 ? args.slice(2, args.length - 1).join(" ") :
            (args.length > 2 ? String(args[2]) : "Gamepad");
        this.deviceType = args.length > 3 ? String(args[args.length - 1]) : "unknown";
        return events.concat(this.deviceEvents());
    } else if (name === "gamepad_status") {
        status = args.join(" ").toLowerCase();
        if (status.indexOf("remove") >= 0 || status.indexOf("disconnect") >= 0) {
            events = this.source === "gamepad" ? this.release() : [];
            this.connected = 0;
            this.deviceInstance = -1;
            this.deviceName = "No gamepad detected";
            this.deviceType = "unknown";
            this.leftTriggerSigned = 0;
            this.rightTriggerSigned = 0;
            return events.concat(this.deviceEvents());
        }
    } else if (name === "axis_left_trigger" || name === "axis_right_trigger") {
        pedal = name === "axis_left_trigger" ? "throttle" : "brake";
        signedProperty = pedal === "throttle" ? "leftTriggerSigned" : "rightTriggerSigned";
        rawTrigger = Number(value);
        events = [[pedal + "_raw", rawTrigger], ["detected", 1]];
        this.connected = 1;
        if (rawTrigger < -0.000001) {
            this[signedProperty] = 1;
        }
        normalizedTrigger = normalizeTrigger(rawTrigger, this.deadZone, this[signedProperty]);
        if (this.manual && this.source === "gamepad") {
            if (pedal === "throttle") {
                this.throttleTarget = normalizedTrigger;
            } else {
                this.brakeTarget = normalizedTrigger;
            }
            events.push([pedal + "_normalized", normalizedTrigger]);
            if (this.smoothingMs <= 0.0) {
                this[pedal] = normalizedTrigger;
                events.push([pedal, normalizedTrigger]);
            }
        }
        return events;
    }
    return [];
};

ManualInputModel.prototype.tick = function (dt) {
    var alpha;
    if (!this.manual || this.source !== "gamepad") {
        return [];
    }
    dt = clamp(Number(dt) || 0.01, 0.001, 0.1);
    alpha = this.smoothingMs <= 0.0 ? 1.0 :
        1.0 - Math.exp(-(dt * 1000.0) / this.smoothingMs);
    this.throttle += (this.throttleTarget - this.throttle) * alpha;
    this.brake += (this.brakeTarget - this.brake) * alpha;
    if (Math.abs(this.throttleTarget - this.throttle) < 0.000001) {
        this.throttle = this.throttleTarget;
    }
    if (Math.abs(this.brakeTarget - this.brake) < 0.000001) {
        this.brake = this.brakeTarget;
    }
    return [["throttle", this.throttle], ["brake", this.brake]];
};

ManualInputModel.prototype.snapshot = function () {
    return {
        manual: this.manual,
        source: this.source,
        throttle: this.throttle,
        brake: this.brake,
        throttleTarget: this.throttleTarget,
        brakeTarget: this.brakeTarget,
        connected: this.connected,
        deviceInstance: this.deviceInstance,
        deviceName: this.deviceName,
        deviceType: this.deviceType
    };
};

function outputEvents(events) {
    var index;
    var event;
    if (typeof outlet === "undefined") {
        return;
    }
    for (index = 0; index < events.length; index += 1) {
        event = events[index];
        if (event[0] === "throttle") {
            outlet(0, event[1]);
        } else if (event[0] === "brake") {
            outlet(1, event[1]);
        } else {
            outlet(2, event);
        }
    }
}

var maxModel = new ManualInputModel();

function loadbang() {
    outputEvents(maxModel.release());
}

function bang() {
    outputEvents(maxModel.tick(0.01));
}

function anything() {
    var args = typeof arrayfromargs === "undefined" ? [] : arrayfromargs(arguments);
    outputEvents(maxModel.handle(String(messagename), args));
}

if (typeof module !== "undefined" && module.exports) {
    module.exports = {
        clamp: clamp,
        normalizeTrigger: normalizeTrigger,
        ManualInputModel: ManualInputModel
    };
}
