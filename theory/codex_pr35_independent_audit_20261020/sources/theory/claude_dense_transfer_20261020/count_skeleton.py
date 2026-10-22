"""Combined listing count for Corollary 9.3 (skeleton-coded section; exact rational certificate).

Same listing count as PR #34 count_certificate.py (m = 3, T = n/2, all-query Theorem 4 listing):
  |Phi| + |Psi| <= P_C(u) = alpha0 + alpha1 u + alpha2 u^2, u = ln n (imported unchanged).
The skeleton section has D = floor(N3/2400) >= e^(u/3)/2400 - 2 (N3 = floor(n^(1/3))). With
  g(u) := e^(u/3)/2400 - 2 - P_C(u),
g(u_1) > 0, g'(u_1) > 0, g''(u_1) > 0 at a rational u_1 <= ln n_1 give g > 0 for all u >= u_1, since
g'' = e^(u/3)/21600 - 2 alpha2 is increasing. The skeleton theorem needs n >= 1e16, which holds here.
Run: python -I count_skeleton.py   (writes count_skeleton_result.json)
"""
import importlib.util, json, os
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "claude_lemma_m_three_memory_20261019", "count_certificate.py")
spec = importlib.util.spec_from_file_location("cc", SRC); cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)


def certify(C, u1):
    a0, a1, a2 = cc.poly_coeffs(*C)
    E = cc.exp_lower(F(u1) / 3)
    g = E / 2400 - 2 - (a0 + a1 * u1 + a2 * u1 ** 2)
    g1 = E / 7200 - (a1 + 2 * a2 * u1)
    g2 = E / 21600 - 2 * a2
    return g > 0 and g1 > 0 and g2 > 0


def main():
    cc.side_checks()
    LN10_LO = F("2.302585")
    assert cc.exp_upper_small(LN10_LO / 4) ** 4 <= 10
    rows = []
    for C in ((0, 0, 0), (10 ** 6, 10 ** 6, 10 ** 6), (10 ** 12, 10 ** 12, 10 ** 12), (10 ** 18, 10 ** 18, 10 ** 18)):
        e = next(e for e in range(16, 400) if certify(C, e * LN10_LO))
        rows.append({"C0,C1,C2": list(C), "Lemma M fails for all n >= 10^e, e =": e}); print(json.dumps(rows[-1]))
    json.dump({"thresholds": rows}, open(os.path.join(HERE, "count_skeleton_result.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
