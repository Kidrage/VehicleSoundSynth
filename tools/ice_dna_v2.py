"""Running-only ICE DNA recipe; the version-one idle program is retained."""

RUNNING_SPECS = (
    ("running_body", "Running Body", 0.0, 1.0),
    ("running_cavity", "Running Cavity", 0.0, 1.0),
    ("hf_softness", "HF Softness", 0.0, 1.0),
    ("release_mass", "Release Mass", 0.0, 1.0),
)
RUNNING_DEFAULTS = {
    "v10": {"running_body": 0.78, "running_cavity": 0.70, "hf_softness": 0.82, "release_mass": 0.62},
    "v12": {"running_body": 0.88, "running_cavity": 0.66, "hf_softness": 0.88, "release_mass": 0.76},
}
RUNNING_METADATA = {
    "running_body": ("Running / 运转", "120–350 Hz 主体", "0..1", ">1200 RPM / 加速", "建议 0.5–0.9；燃烧激发主体，不改变原怠速"),
    "running_cavity": ("Running / 运转", "250–650 Hz 腔体", "0..1", ">1200 RPM / 负载", "建议 0.4–0.8；进排气腔体，不改变主音高"),
    "hf_softness": ("Running / 运转", "高频柔化", "0..1", ">1200 RPM / 高转", "建议 0.7–1；越大越柔和，不是总音量"),
    "release_mass": ("Running / 运转", "收油质量感", "0..1", ">1200 RPM / 收油", "建议 0.4–0.8；低中频缓释，高频先退"),
}


def make_running_gen(profile: str, legacy: str) -> str:
    """Extend, never rewrite, the accepted idle program at its audio seam.

    Four broad, stable two-pole pressure resonators supply body/cavity. Their
    excitation shares the existing bank clock and cylinder weighting; there
    is no free-running noise, sample, new detune, or effect. The original DSP
    continues unchanged so entering/leaving the 1200..3000 blend is click-free.
    """
    if profile not in RUNNING_DEFAULTS:
        raise ValueError(f"No running-only ICE upgrade for {profile}")
    original, outputs = legacy.rsplit("out1 =", 1)
    if outputs != " tanh(left_drive * sat_drive) / sat_drive;\nout2 = tanh(right_drive * sat_drive) / sat_drive;":
        raise ValueError("Legacy DNA output seam changed; re-audit idle before extending it")
    defaults = RUNNING_DEFAULTS[profile]
    params = "// V2 PARAMETERS START\n" + "\n".join(
        f"Param {name}({defaults[name]:g}, min=0, max=1);"
        for name, _label, _low, _high in RUNNING_SPECS
    )
    state_names = [f"v2_m{index}_{delay}" for index in range(4) for delay in (1, 2)]
    state_names += ["v2_exc_1", "v2_exc_2", "v2_side_low", "v2_hf_l1", "v2_hf_l2", "v2_hf_r1", "v2_hf_r2"]
    params += "\n" + "\n".join(f"History {name}(0);" for name in state_names)
    params += "\n// V2 PARAMETERS END\n"
    # Modest fixed-Q structure: V10 tighter/upper; V12 lower/wider. Frequency
    # drift follows only RPM. The firing cadence is still solely drivetrain RPM.
    modes = ((155, .012, 1.25), (245, .013, 1.4), (360, .016, 1.3), (530, .012, 1.15)) if profile == "v10" else (
        (130, .010, 1.10), (210, .012, 1.2), (325, .014, 1.15), (470, .012, 1.05))
    bank_weight = .58 if profile == "v10" else .525
    code = f"""// V2 RUNNING START
// Fixed-RPM pedal moves affect pressure, cavity and release, never cadence.
v2_progress = clamp((r - 1200) / 1800, 0, 1);
v2_blend = v2_progress * v2_progress * (3 - 2 * v2_progress);
v2_pedal = slide(clamp(throttle, 0, 1), 85, 190);
v2_load_fast = slide(l, 110, 290);
v2_body_env = slide(max(v2_pedal, v2_load_fast), 730, 1800 + release_mass * 12000);
v2_edge_env = slide(max(v2_pedal, v2_load_fast), 120, 580);
v2_lift = max(v2_body_env - v2_edge_env, 0);
v2_pressure = (pulse_l * cylinder_l * {bank_weight:g} + pulse_r * cylinder_r * {1-bank_weight:g}) * (0.75 + combustion_pulse * 0.80);
v2_pressure = v2_pressure * (0.86 + v2_load_fast * 0.14 + abs(pulse_l) * texture * 0.18);
v2_exc_diff = v2_pressure - v2_exc_2;
"""
    for index, (center, rpm_depth, q) in enumerate(modes):
        code += f"""v2_freq{index} = {center:g} + r * {rpm_depth:g};
v2_rad{index} = exp(-3.141592653589793 * v2_freq{index} / ({q:g} * samplerate));
v2_modal{index} = (1 - v2_rad{index}) * v2_exc_diff + 2 * v2_rad{index} * cos(6.283185307179586 * v2_freq{index} / samplerate) * v2_m{index}_1 - v2_rad{index} * v2_rad{index} * v2_m{index}_2;
v2_m{index}_2 = v2_m{index}_1;
v2_m{index}_1 = v2_modal{index};
"""
    code += f"""v2_exc_2 = v2_exc_1;
v2_exc_1 = v2_pressure;
v2_body = (v2_modal0 * 1.65 + v2_modal1 * 0.95) * running_body * (0.45 + body * 0.65) * (1 + v2_body_env * 0.48 + v2_lift * release_mass * 0.30);
v2_cavity = (v2_modal2 * 1.20 + v2_modal3 * 0.75) * running_cavity * (0.46 + v2_load_fast * 0.42 + intake_detail * v2_pedal * 0.22);
v2_bank_order = cos(phase_l * 6.283185307179586) * (0.075 + body * 0.045) + cos(phase_l * 12.566370614359172) * (0.060 + texture * 0.022);
v2_exhaust = v2_bank_order * exhaust_detail * (0.18 + v2_body_env * 0.13 + v2_lift * release_mass * 0.18);
v2_center = v2_body + v2_cavity + v2_bank_order + v2_exhaust + v2_pressure * {0.30 if profile == 'v10' else 0.24:g};
// Retain a controlled mechanical gloss; fixed noninteger sine pairs no longer
// dominate acceleration. This is intrinsic pulse structure, not a noise bed.
v2_gloss = cos(phase_l * 37.69911184307752) * air_detail * brightness * v2_edge_env * {0.010 if profile == 'v10' else 0.016:g};
v2_old_edge_l = (bright_l + intake_l * 0.35 + residual_l * 0.28) * (1 - hf_softness * 0.94) * (0.06 + v2_edge_env * 0.18);
v2_old_edge_r = (bright_r + intake_r * 0.35 + residual_r * 0.28) * (1 - hf_softness * 0.94) * (0.06 + v2_edge_env * 0.18);
v2_side_raw = bank_side * (0.12 + texture * 0.10);
v2_side_k = exp(-6.283185307179586 * 120 / samplerate);
v2_side_low = v2_side_raw * (1 - v2_side_k) + v2_side_low * v2_side_k;
v2_side = (v2_side_raw - v2_side_low) * stereo_width;
v2_l_raw = v2_center + v2_side + v2_gloss + v2_old_edge_l;
v2_r_raw = v2_center - v2_side + v2_gloss + v2_old_edge_r;
v2_ceiling = {1050 if profile == 'v10' else 950} + brightness * 1450 + v2_edge_env * 320;
v2_hf_k = exp(-6.283185307179586 * v2_ceiling / samplerate);
v2_hf_l1 = v2_l_raw * (1 - v2_hf_k) + v2_hf_l1 * v2_hf_k;
v2_hf_l2 = v2_hf_l1 * (1 - v2_hf_k) + v2_hf_l2 * v2_hf_k;
v2_hf_r1 = v2_r_raw * (1 - v2_hf_k) + v2_hf_r1 * v2_hf_k;
v2_hf_r2 = v2_hf_r1 * (1 - v2_hf_k) + v2_hf_r2 * v2_hf_k;
v2_left = (v2_l_raw + hf_softness * (v2_hf_l2 - v2_l_raw)) * a * (0.90 + aggression * 0.10) + idle_center + idle_side;
v2_right = (v2_r_raw + hf_softness * (v2_hf_r2 - v2_r_raw)) * a * (0.90 + aggression * 0.10) + idle_center - idle_side;
legacy_l = tanh(left_drive * sat_drive) / sat_drive;
legacy_r = tanh(right_drive * sat_drive) / sat_drive;
v2_out_l = tanh(v2_left * sat_drive) / sat_drive;
v2_out_r = tanh(v2_right * sat_drive) / sat_drive;
out1 = legacy_l + v2_blend * (v2_out_l - legacy_l);
out2 = legacy_r + v2_blend * (v2_out_r - legacy_r);"""
    return params + original + code
