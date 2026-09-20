#!/usr/bin/env python3
"""Ferrari V5 scalar SOURCE proxy; not native Max, BEAP, or listening QA."""
from pathlib import Path
import argparse
import json
import math
import shutil
import subprocess
import tempfile

try:
    from . import build_project as b
    from .check_timbre_repair_math import SUPPORT, translate
except ImportError:
    import build_project as b
    from check_timbre_repair_math import SUPPORT, translate


def run(output: Path):
    compiler = shutil.which("c++")
    if not compiler:
        raise RuntimeError("C++ compiler required")
    old = b.GEN_CODE["ferrari_dna_source_v4"]
    new = b.GEN_CODE["ferrari_dna_source_v5"]
    program = SUPPORT + translate("Old", old) + translate("New", new)
    cases = []
    for rate in (44100, 48000):
        for rpm in (740, 1600, 2600, 4200, 6500, 8000):
            for effort in (.05, .35, 1.0):
                cases.append((rate, rpm, effort))
    blocks = []
    for rate, rpm, effort in cases:
        blocks.append(f"""{{Old a; New z,n;
a.samplerate=z.samplerate=n.samplerate={rate};
a.rpm=z.rpm=n.rpm={rpm};
a.throttle=z.throttle=n.throttle={effort};
a.load=z.load=n.load={effort};
a.accel=z.accel=n.accel={effort};
a.engine_running=z.engine_running=n.engine_running=1;
a.combustion_gain=z.combustion_gain=n.combustion_gain=1;
a.reference_restore=z.reference_restore=n.reference_restore=1;
z.sf90_material=0; n.sf90_material=1;
double bypass=0,residual=0,peak=0,pow1=0,pow2=0,pow3=0,pow4=0;int count=0;bool finite=true;
for(int s=0;s<{rate}*2;s++){{auto x=a.step(),y=z.step(),v=n.step();
 for(int k=0;k<10;k++){{bypass=max(bypass,abs(x[k]-y[k]));finite=finite&&std::isfinite(v[k]);}}
 for(int k=7;k<10;k++)residual=max(residual,abs(x[k]-v[k]));
 for(int k=0;k<4;k++)peak=max(peak,abs(v[k]));
 if(s>{rate}){{pow1+=v[0]*v[0];pow2+=v[1]*v[1];pow3+=v[2]*v[2];pow4+=v[3]*v[3];count++;}}
}}
printf("{rate},{rpm},{effort},%.17g,%.17g,%.9g,%.9g,%.9g,%.9g,%.9g,%d\\n",
 bypass,residual,peak,sqrt(pow1/max(count,1)),sqrt(pow2/max(count,1)),
 sqrt(pow3/max(count,1)),sqrt(pow4/max(count,1)),finite);}}""")
    program += "int main(){\n" + "\n".join(blocks) + "\n}\n"
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ferrari-v5-") as tmp:
        src = Path(tmp) / "proxy.cpp"
        exe = Path(tmp) / "proxy"
        src.write_text(program)
        subprocess.run([compiler, "-O2", "-std=c++17", str(src), "-o", str(exe)],
                       check=True, capture_output=True, text=True)
        raw = subprocess.check_output([str(exe)], text=True)
    header = ("sample_rate,rpm,effort,bypass_max_abs,residual_max_abs,peak,"
              "core_rms,body_rms,character_rms,upper_rms,finite\n")
    (output / "source_metrics.csv").write_text(header + raw)
    rows = []
    failures = []
    for line in raw.splitlines():
        p = line.split(",")
        row = {
            "sample_rate": int(p[0]), "rpm": float(p[1]), "effort": float(p[2]),
            "bypass_max_abs": float(p[3]), "residual_max_abs": float(p[4]),
            "peak": float(p[5]), "core_rms": float(p[6]), "body_rms": float(p[7]),
            "character_rms": float(p[8]), "upper_rms": float(p[9]),
            "finite": int(float(p[10]))
        }
        rows.append(row)
        if row["bypass_max_abs"] != 0:
            failures.append(["v4_bypass", row])
        if row["residual_max_abs"] != 0:
            failures.append(["noise_residual_changed", row])
        if not row["finite"] or row["peak"] >= .95:
            failures.append(["finite_headroom", row])
    report = {
        "kind": "scalar GenExpr subset proxy; NOT native Max/BEAP/listening",
        "cases": len(rows),
        "failures": failures,
        "peak_max": max(r["peak"] for r in rows),
        "bypass_max_abs": max(r["bypass_max_abs"] for r in rows),
        "residual_max_abs": max(r["residual_max_abs"] for r in rows),
        "native_max_tested": False,
        "listening_tested": False,
    }
    (output / "source_report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    run(parser.parse_args().output)
