/* VehicleSoundSynth manual pedal input mapping.
 *
 * ES5-compatible for Max's js object and importable from Node regression
 * tests. HID values are mapped here; drivetrain integration remains in
 * drive_model.js.
 */

inlets = 1;
outlets = 3;

function clamp(value, low, high) {
    return Math.max(low, Math.min(high, value));
}

function normalizeAxis(raw, minimum, maximum, invert, deadZone, curve, gamma) {
    var low = Number(minimum);
    var high = Number(maximum);
    var span = high - low;
    var normalized;
    if (!isFinite(span) || Math.abs(span) < 0.000000001) {
        return 0.0;
    }
    normalized = clamp((Number(raw) - low) / span, 0.0, 1.0);
    if (invert) {
        normalized = 1.0 - normalized;
    }
    deadZone = clamp(Number(deadZone) || 0.0, 0.0, 0.95);
    if (normalized <= deadZone) {
        return 0.0;
    }
    normalized = (normalized - deadZone) / (1.0 - deadZone);
    if (String(curve).toLowerCase() === "progressive") {
        gamma = clamp(Number(gamma) || 1.5, 0.1, 5.0);
        normalized = Math.pow(normalized, gamma);
    }
    return normalized;
}

function ManualInputModel() {
    this.manual = 0;
    this.source = "keyboard";
    this.throttle = 0.0;
    this.brake = 0.0;
    this.throttleTarget = 0.0;
    this.brakeTarget = 0.0;
    this.throttleAxis = -1;
    this.brakeAxis = -1;
    this.throttleMin = 0.0;
    this.throttleMax = 1.0;
    this.brakeMin = 0.0;
    this.brakeMax = 1.0;
    this.throttleInvert = 0;
    this.brakeInvert = 0;
    this.deadZone = 0.02;
    this.curve = "linear";
    this.gamma = 1.5;
    this.smoothingMs = 35.0;
    this.learning = "";
    this.learnCandidates = {};
}

ManualInputModel.prototype.release = function () {
    this.throttle = 0.0;
    this.brake = 0.0;
    this.throttleTarget = 0.0;
    this.brakeTarget = 0.0;
    return [["throttle", 0.0], ["brake", 0.0]];
};

ManualInputModel.prototype.mapPedal = function (pedal, raw) {
    if (pedal === "throttle") {
        return normalizeAxis(
            raw, this.throttleMin, this.throttleMax, this.throttleInvert,
            this.deadZone, this.curve, this.gamma
        );
    }
    return normalizeAxis(
        raw, this.brakeMin, this.brakeMax, this.brakeInvert,
        this.deadZone, "linear", this.gamma
    );
};

ManualInputModel.prototype.handle = function (name, args) {
    var value = args.length ? args[0] : 0;
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
    } else if (name === "device") {
        return this.release().concat([["detected", 0]]);
    } else if (name === "keyboard_throttle" && this.manual && this.source === "keyboard") {
        this.throttle = clamp(Number(value) || 0.0, 0.0, 1.0);
        return [["throttle", this.throttle]];
    } else if (name === "keyboard_brake" && this.manual && this.source === "keyboard") {
        this.brake = clamp(Number(value) || 0.0, 0.0, 1.0);
        return [["brake", this.brake]];
    } else if (name === "throttle_axis") {
        this.throttleAxis = Math.round(Number(value));
    } else if (name === "brake_axis") {
        this.brakeAxis = Math.round(Number(value));
    } else if (name === "throttle_min") {
        this.throttleMin = Number(value);
    } else if (name === "throttle_max") {
        this.throttleMax = Number(value);
    } else if (name === "brake_min") {
        this.brakeMin = Number(value);
    } else if (name === "brake_max") {
        this.brakeMax = Number(value);
    } else if (name === "throttle_invert") {
        this.throttleInvert = Number(value) ? 1 : 0;
    } else if (name === "brake_invert") {
        this.brakeInvert = Number(value) ? 1 : 0;
    } else if (name === "dead_zone") {
        this.deadZone = clamp(Number(value) || 0.0, 0.0, 0.95);
    } else if (name === "curve") {
        this.curve = String(value).toLowerCase() === "progressive" ? "progressive" : "linear";
    } else if (name === "gamma") {
        this.gamma = clamp(Number(value) || 1.5, 0.1, 5.0);
    } else if (name === "smoothing_ms") {
        this.smoothingMs = clamp(Number(value) || 0.0, 0.0, 250.0);
    } else if (name === "learn_throttle" || name === "learn_brake") {
        this.learning = name === "learn_throttle" ? "throttle" : "brake";
        this.learnCandidates = {};
        return [["learn_status", this.learning]];
    } else if (name === "learn_commit") {
        var pedal = String(value).toLowerCase();
        var bestElement = -1;
        var bestMinimum = 0.0;
        var bestMaximum = 0.0;
        var bestSpan = 0.0;
        var candidateKey;
        var candidate;
        var candidateSpan;
        var learnedEvents = [];
        if (pedal === this.learning) {
            for (candidateKey in this.learnCandidates) {
                if (this.learnCandidates.hasOwnProperty(candidateKey)) {
                    candidate = this.learnCandidates[candidateKey];
                    candidateSpan = candidate.maximum - candidate.minimum;
                    if (candidateSpan > bestSpan) {
                        bestElement = Number(candidateKey);
                        bestMinimum = candidate.minimum;
                        bestMaximum = candidate.maximum;
                        bestSpan = candidateSpan;
                    }
                }
            }
        }
        if (bestElement >= 0 && bestSpan > 0.0) {
            if (pedal === "throttle") {
                this.throttleAxis = bestElement;
                this.throttleMin = bestMinimum;
                this.throttleMax = bestMaximum;
            } else {
                this.brakeAxis = bestElement;
                this.brakeMin = bestMinimum;
                this.brakeMax = bestMaximum;
            }
            learnedEvents.push([pedal + "_axis", bestElement]);
            learnedEvents.push([pedal + "_min", bestMinimum]);
            learnedEvents.push([pedal + "_max", bestMaximum]);
        }
        this.learning = "";
        this.learnCandidates = {};
        learnedEvents.push(["learn_status", "idle"]);
        return learnedEvents;
    } else if (name === "hid") {
        var element = Math.round(Number(args[0]));
        var raw = Number(args[1]);
        var events = [["detected", 1], ["last_element", element], ["last_raw", raw]];
        var key;
        if (this.learning) {
            key = String(element);
            if (!this.learnCandidates[key]) {
                this.learnCandidates[key] = {minimum: raw, maximum: raw};
            } else {
                this.learnCandidates[key].minimum = Math.min(this.learnCandidates[key].minimum, raw);
                this.learnCandidates[key].maximum = Math.max(this.learnCandidates[key].maximum, raw);
            }
        }
        if (this.manual && this.source === "gamepad" && element === this.throttleAxis) {
            this.throttleTarget = this.mapPedal("throttle", raw);
            events.push(["throttle_normalized", this.throttleTarget]);
            if (this.smoothingMs <= 0.0) {
                this.throttle = this.throttleTarget;
                events.push(["throttle", this.throttle]);
            }
        }
        if (this.manual && this.source === "gamepad" && element === this.brakeAxis) {
            this.brakeTarget = this.mapPedal("brake", raw);
            events.push(["brake_normalized", this.brakeTarget]);
            if (this.smoothingMs <= 0.0) {
                this.brake = this.brakeTarget;
                events.push(["brake", this.brake]);
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
        throttleAxis: this.throttleAxis,
        brakeAxis: this.brakeAxis,
        throttleMin: this.throttleMin,
        throttleMax: this.throttleMax,
        brakeMin: this.brakeMin,
        brakeMax: this.brakeMax,
        learning: this.learning
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
        normalizeAxis: normalizeAxis,
        ManualInputModel: ManualInputModel
    };
}
