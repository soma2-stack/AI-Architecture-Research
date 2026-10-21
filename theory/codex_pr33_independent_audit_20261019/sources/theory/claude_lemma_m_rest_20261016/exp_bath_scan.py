"""Free bath level versus n (PROOF.md section 3): why experiments here use n >= 16384.

With no drives, the bath s_t (state of a never-driven off-cycle row) is recorded at t = 200, 800,
1500. For small n the front term gamma^2 M/k (row 1's chain) pushes the bath toward 0. The theorem
regime of PR #27 (n >= 1e8) has s in [.025, .1009].
Run: python -I exp_bath_scan.py
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import colsim


def main():
    out = []
    for n in (2048, 16384, 65536, 262144):
        k = n // 2
        r = colsim.hist(n, 1500, [k - 3], lambda t: {})
        b = r["bath"]
        rec = {"n": n, "s_200": float(b[200]), "s_800": float(b[800]), "s_1500": float(b[1500])}
        print(json.dumps(rec)); out.append(rec)
    with open(os.path.join(HERE, "exp_bath_scan_result.json"), "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
