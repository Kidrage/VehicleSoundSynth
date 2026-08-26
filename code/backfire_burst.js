/* VehicleSoundSynth V10/V12 overrun burst scheduler.
 *
 * Max interface:
 *   bang       cancel/restart and emit one 1..5-hit burst
 *   stop       cancel pending hits
 *   seed <int> set a reproducible diagnostic seed
 *
 * Outlet list per hit:
 *   pitch_semitones gain zero_based_index total_count
 */

inlets = 1;
outlets = 1;

var HIT_GAINS = [1.0, 0.82, 0.70, 0.60, 0.52];

function clamp(value, low, high) {
    return Math.max(low, Math.min(high, value));
}

function BurstPlanner(seedValue) {
    this.setSeed(seedValue);
}

BurstPlanner.prototype.setSeed = function (seedValue) {
    var parsed = Number(seedValue);
    if (!isFinite(parsed)) {
        parsed = 1;
    }
    this.state = ((Math.floor(parsed) >>> 0) ^ 0x9e3779b9) >>> 0;
    if (!this.state) {
        this.state = 0x6d2b79f5;
    }
    /* Warm up small neighbouring seeds before their first bounded choice. */
    this.nextUint();
    this.nextUint();
};

BurstPlanner.prototype.nextUint = function () {
    var value = this.state >>> 0;
    value ^= value << 13;
    value ^= value >>> 17;
    value ^= value << 5;
    this.state = value >>> 0;
    return this.state;
};

BurstPlanner.prototype.nextFloat = function () {
    return this.nextUint() / 4294967296.0;
};

BurstPlanner.prototype.randomRange = function (low, high) {
    return low + (high - low) * this.nextFloat();
};

BurstPlanner.prototype.randomIntInclusive = function (low, high) {
    return low + Math.floor(this.nextFloat() * (high - low + 1));
};

BurstPlanner.prototype.createPlan = function () {
    var count = this.randomIntInclusive(1, 5);
    var plan = [];
    var index;
    var pitch;
    for (index = 0; index < count; index += 1) {
        if (index === 0) {
            pitch = this.randomRange(-0.4, 0.4);
        } else {
            pitch = clamp(
                -1.25 * index + this.randomRange(-0.65, 0.65),
                -6.0,
                0.5
            );
        }
        plan.push({
            pitchSemitones: pitch,
            gain: HIT_GAINS[index],
            index: index,
            count: count,
            delayMs: index === 0 ? 0 : this.randomIntInclusive(140, 200)
        });
    }
    return plan;
};

var planner = new BurstPlanner((new Date()).getTime());
var pendingTasks = [];
var generation = 0;

function cancelPending() {
    var index;
    generation += 1;
    for (index = 0; index < pendingTasks.length; index += 1) {
        pendingTasks[index].cancel();
    }
    pendingTasks = [];
}

function emitHit(hit, strength) {
    if (typeof outlet !== "undefined") {
        outlet(0, hit.pitchSemitones, hit.gain * strength, hit.index, hit.count);
    }
}

function scheduledEmitter(hit, strength, expectedGeneration) {
    return function () {
        if (generation === expectedGeneration) {
            emitHit(hit, strength);
        }
    };
}

function burst(strengthValue) {
    var plan;
    var index;
    var elapsed = 0;
    var expectedGeneration;
    var task;
    var strength = clamp(Number(strengthValue) || 0.0, 0.0, 1.0);
    cancelPending();
    expectedGeneration = generation;
    plan = planner.createPlan();
    emitHit(plan[0], strength);
    if (typeof Task === "undefined") {
        return;
    }
    for (index = 1; index < plan.length; index += 1) {
        elapsed += plan[index].delayMs;
        task = new Task(
            scheduledEmitter(plan[index], strength, expectedGeneration),
            this
        );
        task.schedule(elapsed);
        pendingTasks.push(task);
    }
}

function bang() {
    burst(1.0);
}

function stop() {
    cancelPending();
}

function seed(value) {
    cancelPending();
    planner.setSeed(value);
}

if (typeof module !== "undefined" && module.exports) {
    module.exports = {
        BurstPlanner: BurstPlanner,
        clamp: clamp,
        runBurst: burst,
        seed: seed,
        stop: stop
    };
}
