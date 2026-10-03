"""Generate elementary exact-rational arithmetic supporting the written proof.

No model, histories, random numbers, framework, benchmark or GPU is involved.
The general analytic proof does not depend on a finite numerical rank check.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json
import time


def exponential_bracket(x, degree):
    lower = sum((x**j / factorial(j) for j in range(degree + 1)), F(0))
    # Every successive omitted-term ratio is <= x/(degree+2).
    tail_upper = (x**(degree + 1) / factorial(degree + 1)) / (1 - x / (degree + 2))
    return lower, lower + tail_upper


def rational_record(value):
    return {"numerator": str(value.numerator), "denominator": str(value.denominator)}


def main():
    cpu0, wall0 = time.process_time(), time.perf_counter()
    facts = []
    for name, x, degree, boundary, side in [
        ("log134_lt_4.90", F(49, 10), 24, F(134), "lower_gt"),
        ("log200_lt_5.30", F(53, 10), 24, F(200), "lower_gt"),
        ("log_1000_over87_gt_2.44", F(61, 25), 24, F(1000, 87), "upper_lt"),
    ]:
        lo, hi = exponential_bracket(x, degree)
        passed = lo > boundary if side == "lower_gt" else hi < boundary
        facts.append({"name": name, "x": rational_record(x), "degree": degree,
                      "exp_lower": rational_record(lo), "exp_upper": rational_record(hi),
                      "boundary": rational_record(boundary), "inequality": side,
                      "holds": passed})
    u_upper = (F(49, 10) + F(53, 20)) / F(61, 25) + 1
    prefix_error_upper = F(15, 1000) * F(41, 10) * F(51, 10) / (200 * 14)
    facts.extend([
        {"name": "u200_lt_4.1", "value": rational_record(u_upper),
         "boundary": rational_record(F(41, 10)), "holds": u_upper < F(41, 10)},
        {"name": "sqrt200_gt14", "holds": 200 > 14**2},
        {"name": "prefix_error_lt_0.000113",
         "value": rational_record(prefix_error_upper),
         "boundary": rational_record(F(113, 1000000)),
         "holds": prefix_error_upper < F(113, 1000000)},
        {"name": "0.000113_lt_epsilon_over8", "epsilon": "1/1000",
         "holds": F(113, 1000000) < F(1, 8000)},
        {"name": "normalized_u_bound_decreasing",
         "description": "u(n)>1 and 1/(2 log(1/.087))<25/122 for n>=200",
         "log_derivative_upper": rational_record(F(25, 122)*(1+F(1, 2))-F(3, 2)),
         "holds": F(25, 122)*(1+F(1, 2)) < F(3, 2)},
    ])
    peak = None
    try:
        import psutil
        info = psutil.Process().memory_info()
        peak = getattr(info, "peak_wset", None)
    except ImportError:
        pass
    result = {"purpose": "Exact scalar arithmetic only; supporting verification, not the general proof",
              "date": "2026-10-02", "method": "Python Fraction; finite exponential sums with rational geometric tail",
              "facts": facts, "all_inequalities_hold": all(f["holds"] for f in facts),
              "resources": {"cpu_seconds": time.process_time()-cpu0,
                            "wall_seconds": time.perf_counter()-wall0,
                            "peak_process_working_set_bytes": peak, "gpu_seconds": 0,
                            "cuda_used": False, "scope": "arithmetic calculation only; administration unprofiled"}}
    path = Path(__file__).with_name("ARITHMETIC.json")
    path.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"all_inequalities_hold": result["all_inequalities_hold"],
                      "facts": len(facts), "resources": result["resources"]}))
    if not result["all_inequalities_hold"]:
        raise SystemExit("A written scalar inequality failed; preserve evidence and repair the derivation.")


if __name__ == "__main__":
    main()
