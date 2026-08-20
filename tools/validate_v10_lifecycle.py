#!/usr/bin/env python3
"""Gate synthesized V10 renders against Ferrari lifecycle spectral envelopes."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

try:
    from tools.audio_metrics import analyze
except ModuleNotFoundError:  # Direct `python3 tools/...` execution.
    from audio_metrics import analyze


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGETS = ROOT / "assets" / "ferrari_v10_lifecycle_targets.json"
REQUIRED_CONTINUOUS_ROLES = {
    "idle", "acceleration", "loaded_hold", "shift_recovery", "deceleration"
}


def validate_drive_trace(trace: dict[str, Any]) -> dict[str, Any]:
    """Validate throttle-driven RPM, DCT and deceleration from DriveModel output."""
    failures: list[str] = []
    model_path = ROOT / "code" / "drive_model.js"
    expected_sha = hashlib.sha256(model_path.read_bytes()).hexdigest()
    if trace.get("drive_model_sha256") != expected_sha:
        failures.append("drive_model_sha256")
    if trace.get("profile") != "v10":
        failures.append("profile")
    if trace.get("commands") != [["ignition", 1], ["start", 1], ["auto", 1]]:
        failures.append("drive_commands")
    snapshots = trace.get("snapshots", [])
    if len(snapshots) < 1000:
        failures.append("trace_duration")

    def at(seconds: float) -> dict[str, Any]:
        return min(snapshots, key=lambda item: abs(float(item["time"]) - seconds))

    if snapshots:
        first = snapshots[0]
        first_second = [item for item in snapshots if float(item["time"]) <= 1.0]
        if float(first["rpm"]) < 1000.0 or min(float(item["rpm"]) for item in first_second) > 780.0:
            failures.append("startup_catch")
        before_accel, after_accel = at(2.0), at(6.0)
        if not (
            float(after_accel["rpm"]) > float(before_accel["rpm"]) + 3000.0
            and float(after_accel["throttle"]) > float(before_accel["throttle"]) + 0.40
            and float(after_accel["accel"]) > 0.3
        ):
            failures.append("throttle_acceleration")
        before_decel, after_decel = at(19.0), at(23.0)
        if not (
            float(after_decel["rpm"]) < float(before_decel["rpm"]) - 1200.0
            and float(after_decel["accel"]) < -0.5
        ):
            failures.append("brake_deceleration")
        maximum_rpm_step = max(
            abs(float(right["rpm"]) - float(left["rpm"]))
            for left, right in zip(snapshots, snapshots[1:])
        )
        if maximum_rpm_step > 500.0:
            failures.append("rpm_continuity")
    else:
        maximum_rpm_step = 0.0

    messages = [item["message"] for item in trace.get("events", [])]
    shift_directions = [int(message[1]) for message in messages if message[0] == "shift_dir"]
    gears = [int(message[1]) for message in messages if message[0] == "gear" and int(message[1]) > 1]
    shift_starts = sum(message[0] == "shift" and int(message[1]) == 1 for message in messages)
    shift_ends = sum(message[0] == "shift" and int(message[1]) == 0 for message in messages)
    if len(shift_directions) < 5 or any(direction != 1 for direction in shift_directions):
        failures.append("automatic_shift_direction")
    if gears[:6] != [2, 3, 4, 5, 6, 7]:
        failures.append("seven_speed_gears")
    if shift_starts != shift_ends or shift_starts < 5:
        failures.append("shift_lifecycle")
    return {
        "passed": not failures,
        "failures": failures,
        "maximum_rpm_step_per_20ms": maximum_rpm_step,
        "shift_directions": shift_directions,
        "gears": gears,
        "start_firing_hz": float(snapshots[0]["rpm"]) / 12.0 if snapshots else 0.0,
        "peak_firing_hz": max(float(item["rpm"]) for item in snapshots) / 12.0 if snapshots else 0.0,
        "end_firing_hz": float(snapshots[-1]["rpm"]) / 12.0 if snapshots else 0.0,
    }


def validate_drive_lifecycle(
    wav: Path,
    targets: dict[str, Any],
    *,
    require_target_sample_rate: bool = True,
) -> dict[str, Any]:
    sidecar_path = wav.with_suffix(".drive.json")
    failures: list[str] = []
    if not sidecar_path.is_file():
        return {"wav": str(wav), "passed": False, "failures": ["drive_trace"]}
    trace = json.loads(sidecar_path.read_text(encoding="utf-8"))
    trace_report = validate_drive_trace(trace)
    failures.extend(trace_report["failures"])
    probe_path = sidecar_path.parent / str(trace.get("probe_file", ""))
    if not probe_path.is_file() or trace.get("probe_sha256") != hashlib.sha256(probe_path.read_bytes()).hexdigest():
        failures.append("probe_sha256")
    wav_sha256 = hashlib.sha256(wav.read_bytes()).hexdigest()
    if trace.get("wav_file") != wav.name or trace.get("wav_sha256") != wav_sha256:
        failures.append("wav_sha256")
    metrics = analyze(wav)
    if (
        trace.get("wav_sample_rate") != metrics["sample_rate"]
        or trace.get("wav_frames") != metrics["frames"]
    ):
        failures.append("wav_metadata")
    if require_target_sample_rate and metrics["sample_rate"] != targets["sample_rate_hz"]:
        failures.append("sample_rate")
    if metrics["rms_dbfs"] < -50.0:
        failures.append("rms_dbfs")
    if metrics["clipped_sample_ratio"] > 0.0:
        failures.append("clipped_sample_ratio")
    # The 24 s drive reaches ~8,000 RPM, where the physical V10 firing order is
    # above 500 Hz. Role-specific renders carry the stricter Ferrari low/mid
    # limits; this full-drive check only rejects a broadly thin lifecycle mix.
    if metrics["low_mid_ratio"] < 0.25:
        failures.append("low_mid_ratio")
    if metrics["harsh_ratio"] > 0.04:
        failures.append("harsh_ratio")
    if metrics["high_ratio"] > 0.01:
        failures.append("high_ratio")
    expected_frames = round(float(trace["render_ms"]) * float(metrics["sample_rate"]) / 1000.0)
    if abs(int(metrics["frames"]) - expected_frames) > int(metrics["sample_rate"]) // 5:
        failures.append("render_duration")
    return {
        "wav": str(wav),
        "metrics": metrics,
        "drive_trace": trace_report,
        "failures": failures,
        "passed": not failures,
    }


def target_envelope(targets: dict[str, Any], role: str) -> dict[str, float]:
    """Return intentionally broad, reference-derived limits for one lifecycle role."""
    nodes = [node for node in targets["nodes"] if node["role"] == role]
    if not nodes:
        raise ValueError(f"unknown lifecycle role: {role}")

    def lowest(name: str) -> float:
        return min(float(node[name]) for node in nodes)

    def highest(name: str) -> float:
        return max(float(node[name]) for node in nodes)

    # Ferrari.wav is a close-mic reference while the runtime render includes
    # cabin, road, stereo and master stages. These margins preserve that mix
    # freedom while still rejecting thin/noisy/saw-like regressions.
    return {
        "min_rms_dbfs": lowest("rms_dbfs") - 24.0,
        "max_rms_dbfs": highest("rms_dbfs") + 6.0,
        "min_crest_db": max(2.5, lowest("crest_db") - 7.0),
        "max_crest_db": highest("crest_db") + 10.0,
        "min_low_mid_ratio": max(0.50, lowest("low_mid_ratio_40_500") - 0.40),
        "min_rumble_ratio": max(0.005, lowest("rumble_ratio_30_140") - 0.45),
        "max_harsh_ratio": max(0.025, highest("harsh_ratio_2000_6000") * 3.0),
        "max_high_ratio": max(0.006, highest("air_ratio_6000_12000") * 4.0),
        "max_spectral_centroid_hz": max(
            900.0, highest("spectral_centroid_hz") * 3.0
        ),
        "max_spectral_rolloff_95_hz": max(
            2500.0, highest("spectral_rolloff_95_hz") * 3.5
        ),
    }


def validate_render(
    wav: Path,
    targets: dict[str, Any],
    role: str,
    *,
    require_target_sample_rate: bool = True,
    require_cadence_schedule: bool = False,
) -> dict[str, Any]:
    metrics = analyze(wav)
    limits = target_envelope(targets, role)
    failures: list[str] = []

    if require_target_sample_rate and metrics["sample_rate"] != targets["sample_rate_hz"]:
        failures.append("sample_rate")
    if metrics["peak_dbfs"] > -0.8:
        failures.append("peak_dbfs")
    if metrics["rms_dbfs"] < -50.0:
        failures.append("rms_dbfs")
    if metrics["clipped_sample_ratio"] > 0.0:
        failures.append("clipped_sample_ratio")
    comparisons = (
        ("rms_dbfs", "min_rms_dbfs", lambda value, limit: value < limit),
        ("rms_dbfs", "max_rms_dbfs", lambda value, limit: value > limit),
        ("crest_db", "min_crest_db", lambda value, limit: value < limit),
        ("crest_db", "max_crest_db", lambda value, limit: value > limit),
        ("low_mid_ratio", "min_low_mid_ratio", lambda value, limit: value < limit),
        ("rumble_ratio", "min_rumble_ratio", lambda value, limit: value < limit),
        ("harsh_ratio", "max_harsh_ratio", lambda value, limit: value > limit),
        ("high_ratio", "max_high_ratio", lambda value, limit: value > limit),
        (
            "spectral_centroid_hz",
            "max_spectral_centroid_hz",
            lambda value, limit: value > limit,
        ),
        (
            "spectral_rolloff_95_hz",
            "max_spectral_rolloff_95_hz",
            lambda value, limit: value > limit,
        ),
    )
    for metric_name, limit_name, failed in comparisons:
        if failed(float(metrics[metric_name]), limits[limit_name]):
            failures.append(f"{metric_name}:{limit_name}")

    schedule = None
    schedule_path = wav.with_suffix(".lifecycle.json")
    if schedule_path.is_file():
        schedule = json.loads(schedule_path.read_text(encoding="utf-8"))
    if require_cadence_schedule:
        if schedule is None:
            failures.append("cadence_schedule")
        else:
            if schedule.get("role") != role:
                failures.append("cadence_schedule_role")
            derivative = float(schedule["cadence_derivative_hz_s"])
            direction_ok = {
                "idle": abs(derivative) <= 1.0,
                "loaded_hold": abs(derivative) <= 1.0,
                "acceleration": derivative > 0.0,
                "shift_recovery": derivative < 0.0,
                "deceleration": derivative < 0.0,
            }[role]
            if not direction_ok:
                failures.append("cadence_direction")
            role_derivatives = [
                abs(float(node["cadence_derivative_hz_s"]))
                for node in targets["nodes"]
                if node["role"] == role and abs(float(node["cadence_derivative_hz_s"])) > 1.0
            ]
            if role in {"acceleration", "shift_recovery", "deceleration"} and role_derivatives and not (
                min(role_derivatives) * 0.20
                <= abs(derivative)
                <= max(role_derivatives) * 2.0
            ):
                failures.append("cadence_derivative_hz_s")
            target_cadences = [float(node["dominant_firing_hz"]) for node in targets["nodes"]]
            cadence_low = min(target_cadences) * 0.85
            cadence_high = max(target_cadences) * 1.15
            if not all(
                cadence_low <= float(schedule[name]) <= cadence_high
                for name in ("start_firing_hz", "end_firing_hz")
            ):
                failures.append("firing_cadence_range")
            if role == "shift_recovery" and not schedule.get("event"):
                failures.append("shift_event")
    return {
        "wav": str(wav),
        "role": role,
        "target_source_sha256": targets["source_sha256"],
        "limits": limits,
        "cadence_schedule": schedule,
        "metrics": metrics,
        "failures": failures,
        "passed": not failures,
    }


def parse_render(value: str) -> tuple[str, Path]:
    try:
        role, path = value.split("=", 1)
    except ValueError as error:
        raise argparse.ArgumentTypeError("expected ROLE=PATH") from error
    if not role or not path:
        raise argparse.ArgumentTypeError("expected ROLE=PATH")
    return role, Path(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "render",
        nargs="+",
        type=parse_render,
        metavar="ROLE=PATH",
        help="one or more synthesized lifecycle renders",
    )
    parser.add_argument(
        "--allow-partial-lifecycle",
        action="store_true",
        help="diagnostic only; production acceptance requires all five continuous roles",
    )
    parser.add_argument("--targets", type=Path, default=DEFAULT_TARGETS)
    parser.add_argument(
        "--drive-lifecycle-wav",
        type=Path,
        help="24 s throttle-only integrated V10 render with matching .drive.json trace",
    )
    parser.add_argument(
        "--allow-non-target-sample-rate",
        action="store_true",
        help="diagnostic only; production acceptance remains 48 kHz",
    )
    args = parser.parse_args()
    targets = json.loads(args.targets.read_text(encoding="utf-8"))
    reports = [
        validate_render(
            path,
            targets,
            role,
            require_target_sample_rate=not args.allow_non_target_sample_rate,
            require_cadence_schedule=True,
        )
        for role, path in args.render
    ]
    provided_roles = {role for role, _ in args.render}
    missing_roles = sorted(REQUIRED_CONTINUOUS_ROLES - provided_roles)
    complete = args.allow_partial_lifecycle or not missing_roles
    drive_report = None
    if args.drive_lifecycle_wav is not None:
        drive_report = validate_drive_lifecycle(
            args.drive_lifecycle_wav,
            targets,
            require_target_sample_rate=not args.allow_non_target_sample_rate,
        )
    drive_complete = args.allow_partial_lifecycle or drive_report is not None
    passed = (
        complete
        and drive_complete
        and all(report["passed"] for report in reports)
        and (drive_report is None or drive_report["passed"])
    )
    print(json.dumps({
        "renders": reports,
        "missing_roles": missing_roles,
        "complete_lifecycle": not missing_roles,
        "drive_lifecycle": drive_report,
        "passed": passed,
    }, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
