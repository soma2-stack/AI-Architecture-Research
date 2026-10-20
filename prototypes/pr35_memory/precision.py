"""Cheap algebraic/precision diagnostics, separate from trainable recall evidence."""
from __future__ import annotations
import itertools
import math
import torch
from fractions import Fraction

@torch.no_grad()
def diagnostics():
    output = {"scope": "small finite numerical tests; not a new proof or theorem-scale run", "codes": [], "rounding": []}
    for d in (2, 3, 4, 6):
        r = 2*d - 1
        nodes = torch.linspace(-1, 1, r, dtype=torch.float64)
        matrix = nodes[:, None] ** torch.arange(d, dtype=torch.float64)[None, :]
        delta = min(float(torch.linalg.svdvals(matrix[list(rows)])[-1])
                    for rows in itertools.combinations(range(r), d)) / math.sqrt(d)
        gen = torch.Generator().manual_seed(35+d)
        theta = torch.randn(256, d, generator=gen, dtype=torch.float64)
        theta = theta / theta.norm(dim=1, keepdim=True)
        _, _, vh = torch.linalg.svd(matrix[:d-1], full_matrices=True)
        theta = torch.cat((theta, vh[-1:]), dim=0)
        rows = {}
        for name in ("float64", "float32", "bfloat16"):
            dtype = getattr(torch, name)
            raw = (theta.to(dtype) @ matrix.to(dtype).T) / delta
            z = raw.clamp(-1, 1)
            rows[name] = {"minimum_saturated": int((z.abs() >= 1).sum(-1).min()),
                          "fraction_zero_clip_derivative": float((raw.abs() > 1).float().mean()),
                          "code_max_abs_gap_vs_float64": float((z.double()-((theta@matrix.T)/delta).clamp(-1,1)).abs().max())}
        output["codes"].append({"D": d, "r": r, "delta_svd_estimate": delta,
                                 "L_svd_estimate": 1/delta, "samples": len(theta), "precision": rows})
    for n in (32, 1024, 65536, 10**8, 10**16):
        for name in ("float32", "float64", "bfloat16"):
            dtype = getattr(torch, name)
            one = torch.tensor(1., dtype=dtype)
            a = torch.tensor(1-1/n, dtype=dtype)
            eta = 1e-8 / n**2
            shift = torch.tensor(.05, dtype=dtype) + eta * .05
            output["rounding"].append({"n": n, "dtype": name, "a_equals_one": bool(a==one),
                                        "contract_field_visible_at_bias": bool(shift!=torch.tensor(.05,dtype=dtype)),
                                        "eta": eta})
    # Exact rational conditioning obstruction from the audit: D=89 full-spark code.
    d=89
    coefficients=[Fraction(1)]
    for i in range(d-1):
        root=Fraction(-1)+Fraction(i,d-1)
        new=[Fraction(0)]*(len(coefficients)+1)
        for j,c in enumerate(coefficients):
            new[j]-=root*c;new[j+1]+=c
        coefficients=new
    ratio=max(abs(c) for c in coefficients)/abs(coefficients[0])
    output["D89_exact_gain_lower_bound"]={"greater_than_1e50":ratio>10**50,
                                         "lower_bound_float_summary":float(ratio),
                                         "scope":"exact coefficient ratio lower bound; no SVD at D89"}
    matrix=torch.tensor([[1.,-1.],[1.,0.],[1.,1.]],dtype=torch.float64)
    gain=1/min(float(torch.linalg.svdvals(matrix[list(i)])[-1]) for i in itertools.combinations(range(3),2))*math.sqrt(2)
    a=torch.tensor([1.,0.],dtype=torch.float64)
    b=torch.tensor([99/101,20/101],dtype=torch.float64)
    output["noninjective_code_collision"]={"distinct_inputs":bool(torch.any(a!=b)),
        "identical_clipped_code":bool(torch.equal((gain*(matrix@a)).clamp(-1,1),(gain*(matrix@b)).clamp(-1,1)))}
    return output
