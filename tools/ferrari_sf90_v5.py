"""Ferrari V5: SF90-reference-aligned deterministic pressure / structure model.

The user-supplied SF90 recording is analysis-only. No source/derivative audio is
loaded or committed. sf90_material=0 restores the exact Ferrari V4 source at
identical RTPC/state; 1 selects this version. Noise residual taps stay unchanged.
"""
from __future__ import annotations
import re

# QA trigger: integration is validated on macOS before this branch is handed to listening.\nBASELINE = "739c9d9a19432ac693e1a10a7ecd0cbb6b283dc8"
SEED = "patchers/ferrari_dna_v5_designer~.maxpat"
MODES = (
    ("b123", 123.0, 2.3),
    ("b185", 185.0, 3.2),
    ("b214", 214.0, 2.8),
    ("c240", 240.0, 2.6),
    ("c620", 620.0, 2.1),
    ("m820", 820.0, 1.8),
    ("m1100", 1100.0, 1.6),
)

FACTORY_MACROS = {
    "v3_aggression": .42,
    "v3_body": .72,
    "v3_character": .60,
    "v3_softness": .72,
    "v3_release_mass": .66,
    "v3_width": .34,
    "v3_load_response": .76,
    "v3_pressure_blend": .70,
    "reference_restore": 1.0,
    "sf90_material": 1.0,
}


def builder():
    try:
        from . import build_project as b
    except ImportError:
        import build_project as b
    return b


def _bp_history(name: str) -> str:
    return f"History sf_{name}_y1(0); History sf_{name}_y2(0);"


def _bp_code(name: str, hz: float, q: float) -> str:
    return f"""sf_{name}_w = 6.283185307179586*{hz:g}/samplerate;
sf_{name}_a = sin(sf_{name}_w)/(2*{q:g});
sf_{name}_n = 1/(1+sf_{name}_a);
sf_{name} = sf_{name}_a*sf_{name}_n*(sf_exc-sf_x2)
 +2*cos(sf_{name}_w)*sf_{name}_n*sf_{name}_y1
 -(1-sf_{name}_a)*sf_{name}_n*sf_{name}_y2;
sf_{name}_y2 = sf_{name}_y1; sf_{name}_y1 = sf_{name};
"""


def source_code(legacy: str) -> str:
    """Build V5 on V4 while keeping V4 as a sample-exact source bypass."""
    histories = [
        "History sf_prev_pressure(0);",
        "History sf_x1(0); History sf_x2(0);",
        "History sf_core_env(0); History sf_body_env(0);",
        "History sf_cavity_env(0); History sf_mech_env(0);",
    ]
    histories.extend(_bp_history(name) for name, _, _ in MODES)
    code = "Param sf90_material(1, min=0, max=1);\\n" + "\\n".join(histories) + "\\n" + legacy
    for i in range(1, 5):
        code, count = re.subn(rf"^out{i} = ", f"sf_old{i} = ", code, flags=re.M)
        if count != 1:
            raise ValueError(f"Ferrari V4 output seam {i} changed")

    filters = "\\n".join(_bp_code(*mode) for mode in MODES)
    code += """
// Ferrari V5: the V2-style pressure pulse remains the identity clock.
// Deterministic structure replaces V4's additional RPM-tracking cavity/intake
// oscillators. Random combustion/mechanical/intake residuals remain out8-10.
sf_mix = slide(clamp(sf90_material,0,1),samplerate*.080,samplerate*.080);
sf_effort = max(clamp(throttle,0,1),max(load,0));
sf_core_tau = sf_effort > sf_core_env ? .030 : .120;
sf_body_tau = sf_effort > sf_body_env ? .060 : .260;
sf_cavity_tau = sf_effort > sf_cavity_env ? .045 : .200;
sf_mech_tau = sf_effort > sf_mech_env ? .018 : .075;
sf_core_env = sf_effort+(sf_core_env-sf_effort)*exp(-1/(samplerate*sf_core_tau));
sf_body_env = sf_effort+(sf_body_env-sf_effort)*exp(-1/(samplerate*sf_body_tau));
sf_cavity_env = sf_effort+(sf_cavity_env-sf_effort)*exp(-1/(samplerate*sf_cavity_tau));
sf_mech_env = sf_effort+(sf_mech_env-sf_effort)*exp(-1/(samplerate*sf_mech_tau));

// Cycle-normalized pressure edge: deterministic and pulse-synchronous, but not
// a white-noise substitute. It excites fixed acoustic modes between firings.
sf_edge = tanh((repair_pressure-sf_prev_pressure)*samplerate/max(v3_fire,45)*.018);
sf_exc = repair_pressure*(.60+.25*v3_pressure_mix)
 + sf_edge*(.10+.22*v3_pressure_mix);
""" + filters + """
sf_prev_pressure = repair_pressure;
sf_x2 = sf_x1; sf_x1 = sf_exc;

// Reference-derived identity: idle pressure harmonics naturally land near
// 61/123/185 Hz; fixed modes keep the 120-600 Hz structure from becoming
// another proportional-pitch oscillator bank as RPM rises.
sf_core_gain = .58+.15*sf_core_env*(.45+.55*v3_response);
sf_body_gain = .42+.27*sf_body_env*(.45+.55*v3_response);
sf_cavity_gain = .32+.27*sf_cavity_env*(.45+.55*v3_response);
sf_mech_gain = .22+.11*sf_mech_env*(.50+.50*v3_response);

sf_body_tone = sf_b123*(.42+.25*v3_mass)
 + sf_b185*(.70+.15*v3_mass)
 + sf_b214*(.48-.12*v3_mass);
sf_character_tone = sf_c240*(.78-.20*v3_char)
 + sf_c620*(.34+.28*v3_char);
sf_mech_tone = sf_m820*(.50+.18*v3_agg)
 + sf_m1100*(.36+.18*v3_agg)*(1-.55*v3_soft);

// Fast lift removes edge first (~4-5 dB at full lift); Body/Cavity mass is
// governed by their slower envelopes rather than artificial resonator ringing.
sf_upper_release = 1-.42*repair_lift_fast;
sf_new1 = repair_pressure*.17*sf_core_gain*v3_gate;
sf_new2 = sf_body_tone*.42*sf_body_gain*v3_gate;
sf_new3 = sf_character_tone*.52*sf_cavity_gain*v3_gate;
sf_new4 = sf_mech_tone*.45*sf_mech_gain*sf_upper_release*v3_gate;

out1 = sf_old1+sf_mix*(sf_new1-sf_old1);
out2 = sf_old2+sf_mix*(sf_new2-sf_old2);
out3 = sf_old3+sf_mix*(sf_new3-sf_old3);
out4 = sf_old4+sf_mix*(sf_new4-sf_old4);
"""
    return code


def _getbox(patch, **fields):
    matches = [x["box"] for x in patch["boxes"]
               if all(x["box"].get(k) == v for k, v in fields.items())]
    if len(matches) != 1:
        raise ValueError(f"Ambiguous Ferrari V5 graph seam: {fields}")
    return matches[0]


def _add(patch, ident, text=None, cls="newobj", **kw):
    if any(x["box"]["id"] == ident for x in patch["boxes"]):
        raise ValueError("Duplicate Ferrari V5 ID " + ident)
    box = {"id": ident, "maxclass": cls, "numinlets": 1, "numoutlets": 1,
           "patching_rect": [30., 1900. + len(patch["boxes"]) * 24, 260., 22.]}
    if text is not None:
        box["text"] = text
    box.update(kw)
    patch["boxes"].append({"box": box})
    return ident


def _wire(patch, src, dst, outlet=0, inlet=0):
    patch["lines"].append({"patchline": {
        "source": [src, outlet], "destination": [dst, inlet]}})


def _add_sf90_control(document, destination):
    patch = document["patcher"]
    inlets = sorted(
        (x["box"] for x in patch["boxes"] if x["box"].get("maxclass") == "inlet"),
        key=lambda x: x["patching_rect"][0])
    if len(inlets) < 2:
        raise ValueError("Ferrari V5 designer inlet layout changed")
    inlet = inlets[0]
    old = [x["patchline"] for x in patch["lines"]
           if x["patchline"]["source"] == [inlet["id"], 0]]
    if len(old) != 1:
        raise ValueError("Expected one Ferrari designer control inlet edge")
    route = _add(patch, "sf90-route", "route sf90_material", numoutlets=2)
    old[0]["source"] = [route, 1]
    _wire(patch, inlet["id"], route)
    clip = _add(patch, "sf90-clip", "clip 0 1", numinlets=3)
    tag = _add(patch, "sf90-tag", "prepend sf90_material")
    _wire(patch, clip, tag)
    _wire(patch, tag, destination)

    bottom = max((x["box"].get("presentation_rect", [0, 0, 0, 0])[1]
                  + x["box"].get("presentation_rect", [0, 0, 0, 0])[3]
                  for x in patch["boxes"]), default=0) + 30
    value = _add(
        patch, "sf90-value", cls="flonum", minimum=0., maximum=1.,
        numoutlets=2, varname="sf90_material", presentation=1,
        presentation_rect=[35., bottom, 90., 22.],
        patching_rect=[35., 1030., 90., 22.])
    _add(
        patch, "sf90-label",
        "SF90 Material: 0 = Ferrari V4 source; 1 = pressure-driven fixed-structure V5",
        cls="comment", numoutlets=0, presentation=1,
        presentation_rect=[145., bottom, 1050., 34.],
        patching_rect=[140., 1030., 1080., 34.])
    init = _add(patch, "sf90-init", "loadmess 1")
    _wire(patch, init, value)
    _wire(patch, route, value)
    _wire(patch, value, clip)
    patch["rect"][3] = max(patch["rect"][3], bottom + 100)
    return document


def make_designer():
    b = builder()
    doc = b.timbre_repair.make_ferrari_designer()
    patch = doc["patcher"]
    params = next(x["patchline"]["destination"][0] for x in patch["lines"]
                  if x["patchline"]["source"] == ["repair-tag", 0])
    state = _getbox(patch, text="js Patcher:/code/timbre_repair_state.js ferrari")
    state["text"] = "js Patcher:/code/ferrari_v5_state.js"
    storage = next(x["box"] for x in patch["boxes"]
                   if x["box"].get("text", "").startswith("pattrstorage "))
    storage["text"] = storage["text"].replace(
        "ferrari_sound_dna_v4", "ferrari_sound_dna_v5")
    for item in patch["boxes"]:
        box = item["box"]
        if box.get("maxclass") == "comment" and "FERRARI DNA V4" in box.get("text", ""):
            box["text"] = box["text"].replace(
                "FERRARI DNA V4 / material restore",
                "FERRARI DNA V5 / SF90 pressure-structure")
    return _add_sf90_control(doc, params)


def make_acoustic():
    b = builder()
    doc = b.timbre_repair.make_ferrari_acoustic()
    patch = doc["patcher"]
    _getbox(
        patch,
        text="gen~ @gen Patcher:/gen/ferrari_dna_source_v4.gendsp"
    )["text"] = "gen~ @gen Patcher:/gen/ferrari_dna_source_v5.gendsp"
    _getbox(patch, text="ferrari_dna_v4_designer~")["text"] = "ferrari_dna_v5_designer~"
    return doc


def factory():
    b = builder()
    d = b.timbre_repair.factory("ferrari")
    data = d["pattrstorage"]["slots"]["99"]["data"]
    data.update({name: [value] for name, value in FACTORY_MACROS.items()})
    d["pattrstorage"]["name"] = "ferrari_sound_dna_v5"
    return d


def register(contents):
    for path in (SEED, "patchers/ferrari_acoustic_v5~.maxpat"):
        contents["patchers"][path] = {"kind": "patcher", "local": 1}
    contents["data"]["presets/ferrari_sound_dna_v5_factory.json"] = {
        "kind": "data", "local": 1}
    contents["code"]["code/ferrari_v5_state.js"] = {
        "kind": "javascript", "local": 1}


def outputs():
    return {
        SEED: make_designer(),
        "patchers/ferrari_acoustic_v5~.maxpat": make_acoustic(),
        "presets/ferrari_sound_dna_v5_factory.json": factory(),
    }


def write_outputs(root):
    b = builder()
    for name, doc in outputs().items():
        if name == SEED and (root / name).exists():
            continue
        b.write_json(root / name, doc)
