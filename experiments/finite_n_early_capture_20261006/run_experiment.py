"""Finite-size early-capture sanity check: no training or optimization.

The full reference O_* recurrence is used. Tiny widths use stationary
off-cycle carriers, not the astronomical theorem's nonwrapping corridors.
"""
import os
for key in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS",
            "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[key] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

import argparse
import hashlib
import json
import math
import subprocess
import time
from pathlib import Path

import torch
torch.set_num_threads(1)
torch.set_num_interop_threads(1)
torch.set_default_dtype(torch.float64)
torch.manual_seed(20261006)

ROOT = Path(__file__).resolve().parent
START = time.perf_counter()
CPU_START = time.process_time()
DEADLINE_SECONDS = 540
# Sequential tiny reductions are cheaper on CPU than CUDA kernel launches.
DEVICE = torch.device("cpu")
CONFIG = {
    "seed": 20261006, "widths": [128, 256, 512, 1024],
    "donor_counts": [4, 8, 16, 32], "dtype": "float64",
    "a": "1-1/n", "g_H": "1-1/n^2", "g_L": .995,
    "write_steps": "ceil(.4*n)", "clear_steps": "2*n",
    "trace_tail": "ceil(log((write_steps+1)/1e-3)/(-log(a*g_L)))+1",
    "reset_state": .05, "initial_tuple_beta": .04,
    "carrier": "four-site balanced stationary off-cycle tuples",
    "model": "complete frozen reference R0, including full selected Householder/cycle feedback",
    "dense_perturbation": "not included; this tests the full dense reference block O_*, not the tiny actual-model transfer correction",
    "cpu_intraop_threads": 1, "cpu_interop_threads": 1,
    "worker_processes": 0, "hard_guard_seconds": DEADLINE_SECONDS,
    "target_vram_bytes": 0,
    "no_training": True, "no_optimization": True,
}


def guard():
    if time.perf_counter()-START > DEADLINE_SECONDS:
        raise RuntimeError("STOP: finite experiment time guard reached")
    if DEVICE.type == "cuda" and torch.cuda.max_memory_allocated() > 2*1024**3:
        raise RuntimeError("STOP: conservative 2GB CUDA allocation guard")


class Model:
    def __init__(self, n, K):
        self.n, self.k, self.l = n, n//2, n-n//2
        self.r, self.d = self.k-1, n//4
        self.a, self.gh, self.gl = 1-1/n, 1-1/n**2, .995
        self.gamma = 1/(1-1/math.sqrt(self.k))
        self.c = self.gamma**2/self.k
        # Maximum four-site carrier allocation on the off-cycle sites.
        self.m = (self.k-self.d)//4
        self.m -= self.m % (2*K)
        if self.m < 2*K or self.m % 4:
            raise ValueError("Insufficient sites for donor groups and balanced Walsh labels")
        self.act = torch.arange(self.d-1, self.d-1+4*self.m, device=DEVICE)
        self.tuples = self.act.reshape(self.m, 4)
        self.donor_tuples, self.survivor_tuples = self.m//2, self.m//2
        self.surv = self.tuples[self.m//2:].reshape(-1)
        self.sign = torch.tensor([1., 1., -1., -1.], device=DEVICE)
        self.chi_tuple = torch.where(torch.arange(self.m//2, device=DEVICE) % 2 == 0, 1., -1.)
        self.chi = self.chi_tuple.repeat_interleave(4)
        self.xi = torch.zeros(self.r, device=DEVICE)
        self.xi[self.surv] = self.chi/math.sqrt(len(self.surv))
        self.common = torch.zeros(self.r, device=DEVICE)
        self.common[self.surv] = 1/math.sqrt(len(self.surv))
        comp_surv = self.tuples[self.m//2:, 2:].reshape(-1)
        ss = torch.zeros(self.r, device=DEVICE)
        ss[comp_surv] = 1/math.sqrt(len(comp_surv))
        donor_groups = self.tuples[:self.m//2].reshape(K, self.m//(2*K), 4)
        W = torch.zeros(self.r, K, device=DEVICE)
        for j in range(K):
            idx = donor_groups[j, :, 2:].reshape(-1)
            W[idx, j] = 1/math.sqrt(len(idx))
            W[:, j] -= ss/math.sqrt(K)
        P = torch.ones(K, K, device=DEVICE)/K
        H = torch.eye(K, device=DEVICE)-(1-1/math.sqrt(2))*P
        self.V = W@H
        self.A_witness = (torch.eye(K, device=DEVICE)+(math.sqrt(2)-1)*P)/math.sqrt(1+1/K)
        self.probe_orthogonality_error = float(torch.max(torch.abs(self.V.T@self.V-torch.eye(K, device=DEVICE))))
        self.write = math.ceil(.4*n)
        self.tail = math.ceil(math.log((self.write+1)/1e-3)/(-math.log(self.a*self.gl)))+1
        self.clear = 2*n
        self.total = self.write+1+self.tail+self.clear+1
        ratio = self.a*self.gl
        self.target = self.gl*(-math.expm1((self.write+1+self.tail)*math.log(ratio)))/(1-ratio)
        sig = .05
        for _ in range(20):
            sig = math.tanh(sig/(100*n)+.05)
        self.sigma = sig

    def O(self, x):
        """Exact C + 1u^T + e1v_H^T, including terminal and front feedback."""
        y = torch.empty_like(x)
        y[..., 0, :] = 0
        y[..., 1:self.d-1, :] = x[..., :self.d-2, :]
        y[..., self.d-1:, :] = x[..., self.d-1:, :]
        mass = x.sum(dim=-2)
        J = self.gamma/math.sqrt(self.k)*x[..., self.d-2, :]-self.c*mass
        B = self.gamma/math.sqrt(self.k)*mass
        y += J.unsqueeze(-2)
        y[..., 0, :] += B
        return y

    def public_schedule(self):
        # Pair-balanced active states have exactly zero total state sum.
        # Their off-cycle local predecessors cannot enter a nondriven row.
        h = torch.full((self.r,), math.tanh(.05), device=DEVICE)
        h[self.act] = 0
        gates, fields = [], []
        for step in range(self.total):
            mass = h.sum()
            J = self.gamma/math.sqrt(self.k)*h[self.d-2]-self.c*mass
            nxt = torch.tanh(self.a*self.O(h[:, None])[:, 0]+.05)
            gates.append(1-nxt*nxt)
            fields.append(J)
            nxt[self.act] = 0
            h = nxt
        return torch.stack(gates), torch.stack(fields), h


def phase_at(model, t):
    if t <= model.write:
        return "write"
    if t == model.write+1:
        return "capture"
    if t <= model.write+1+model.tail:
        return "trace_tail"
    if t < model.total:
        return "clear"
    return "reset"


@torch.no_grad()
def run_case(n, K, mode="capture", theta=None, label=None):
    guard()
    model = Model(n, K)
    theta = torch.ones(K, device=DEVICE) if theta is None else theta.to(DEVICE)
    assert theta.shape == (K,) and float(theta.abs().max()) <= 1
    pub_g, fields, pub_final = model.public_schedule()
    X = torch.zeros(2, model.r, K, device=DEVICE)
    Delta = torch.zeros(model.r, K, device=DEVICE)
    tau = torch.zeros(2, K, device=DEVICE)
    beta0 = CONFIG["initial_tuple_beta"]
    h_prev = (beta0*model.sign).repeat(model.m).expand(2, -1).clone()
    raw_energy = ((torch.atanh(h_prev)-.05)**2).sum(dim=1)
    raw_energy += model.l*(model.sigma/(100*n))**2
    max_raw = float((torch.atanh(h_prev)-.05).abs().max())
    correction_gates = None
    capture_row, predicted_row = None, None
    max_step_abs, max_step_rel, max_closed_abs = 0., 0., 0.
    direct_difference_discrepancy = 0.
    trace_match_error = None
    pure = model.xi[:, None].clone()
    pure_uniform = pure.clone()
    checkpoints, trace = {}, []
    sample_stride = max(1, model.total//350)
    checkpoints_at = {
        model.write: "end_write", model.write+1: "after_capture",
        model.write+1+model.tail: "after_trace_correction",
        model.total-1: "after_clear", model.total: "after_reset",
    }
    for t in range(1, model.total+1):
        if t % 128 == 0:
            guard()
        phase = phase_at(model, t)
        donor_g = torch.full((2, K), model.gl, device=DEVICE)
        if phase == "write":
            donor_g = model.gl+(torch.stack([theta, -theta])+1)*(model.gh-model.gl)/2
        elif t == model.write+1+model.tail:
            donor_g = model.target/(1+model.a*tau)
            correction_gates = donor_g.detach().cpu().tolist()
        tuple_g = torch.full((2, model.m), model.gh, device=DEVICE)
        tuple_g[:, :model.m//2] = donor_g.repeat_interleave(model.m//(2*K), dim=1)
        if phase == "capture" and mode != "control":
            tuple_g[:, model.m//2:] = torch.where(model.chi_tuple > 0, model.gh, model.gl)
        if mode == "broken" and phase in ("trace_tail", "clear"):
            # Reverse the public sign-dependent filter during correction.
            tuple_g[:, model.m//2:] = torch.where(model.chi_tuple > 0, model.gl, model.gh)
        G = pub_g[t-1].expand(2, -1).clone()
        G[:, model.act] = tuple_g.repeat_interleave(4, dim=1)
        if phase == "reset":
            G[:, model.act] = 1-CONFIG["reset_state"]**2
            h_next = torch.full_like(h_prev, CONFIG["reset_state"])
        else:
            h_next = (torch.sqrt(1-tuple_g)[:, :, None]*model.sign).reshape(2, -1)
        raw = torch.atanh(h_next)-model.a*(h_prev+fields[t-1])-.05
        raw_energy += (raw*raw).sum(dim=1)
        max_raw = max(max_raw, float(raw.abs().max()))
        h_prev = h_next

        old_row = model.xi@Delta
        baseB = model.a*model.O(X[1])+model.V
        # Exact difference Duhamel form avoids subtracting two large responses.
        Delta = G[0, :, None]*(model.a*model.O(Delta))+(G[0]-G[1])[:, None]*baseB
        X = G[:, :, None]*(model.a*model.O(X)+model.V)
        tau_g = (1-CONFIG["reset_state"]**2) if phase == "reset" else donor_g
        tau = tau_g*(1+model.a*tau)
        row = model.xi@Delta
        common_row = model.common@Delta
        if phase == "capture":
            capture_row = row.clone()
            predicted_row = row.clone()
        elif phase in ("trace_tail", "clear", "reset"):
            factor = model.a*(1-CONFIG["reset_state"]**2 if phase == "reset" else model.gh)
            expected_step = factor*old_row
            step_abs = float(torch.linalg.vector_norm(row-expected_step))
            scale = max(float(torch.linalg.vector_norm(expected_step)), 1e-300)
            max_step_abs = max(max_step_abs, step_abs)
            max_step_rel = max(max_step_rel, step_abs/scale)
            predicted_row *= factor
            max_closed_abs = max(max_closed_abs, float(torch.linalg.vector_norm(row-predicted_row)))
            pure_g = G[0]
            pure = pure_g[:, None]*model.a*model.O(pure)
            normal_g = pure_g.clone()
            normal_g[model.surv] = (1-CONFIG["reset_state"]**2 if phase == "reset" else model.gh)
            pure_uniform = normal_g[:, None]*model.a*model.O(pure_uniform)
        if t == model.write+1+model.tail:
            trace_match_error = float((tau[0]-tau[1]).abs().max())
        if t % sample_stride == 0 or t in checkpoints_at:
            norm = float(torch.linalg.vector_norm(row))
            prednorm = float(torch.linalg.vector_norm(predicted_row)) if predicted_row is not None else None
            entry = {"t": t, "phase": phase, "walsh_row_norm": norm,
                     "common_row_norm": float(torch.linalg.vector_norm(common_row)),
                     "predicted_protected_norm": prednorm}
            trace.append(entry)
            if t in checkpoints_at:
                discrepancy = float((X[0]-X[1]-Delta).abs().max())
                direct_difference_discrepancy = max(direct_difference_discrepancy, discrepancy)
                entry = dict(entry)
                entry["walsh_row_components"] = row.detach().cpu().tolist()
                entry["absolute_prediction_error"] = (float(torch.linalg.vector_norm(row-predicted_row))
                                                     if predicted_row is not None else None)
                entry["relative_prediction_error"] = (entry["absolute_prediction_error"]/max(prednorm, 1e-300)
                                                     if prednorm is not None else None)
                checkpoints[checkpoints_at[t]] = entry
    final_row = model.xi@Delta
    component_abs = final_row.abs()
    combined = float(torch.linalg.vector_norm(final_row))
    witnesses = final_row@model.A_witness
    pure_H = pure[model.surv]-pure[model.surv].mean(dim=0)
    pure_outside = pure.clone()
    pure_outside[model.surv] -= pure_H
    protected_pure_final = float(torch.abs(model.xi@pure_uniform))
    broken_pure_final = float(torch.abs(model.xi@pure))
    sg = ((1/math.cosh(.25))**2-(1/math.cosh(.75))**2)/2
    query_lower = model.sigma*math.sqrt(model.l)*model.a*sg*math.sqrt(len(model.surv))/(n*math.sqrt(n))*combined
    result = {
        "n": n, "K": K, "mode": mode, "label": label or mode,
        "m": model.m, "survivor_physical_sites": len(model.surv),
        "write_steps": model.write, "trace_tail_steps": model.tail,
        "clear_steps": model.clear, "total_steps_after_preparation": model.total,
        "mT": model.m*(model.total-1), "theta": theta.detach().cpu().tolist(),
        "saturated_donors": int((theta.abs() >= 1-1e-12).sum()),
        "probe_orthogonality_max_error": model.probe_orthogonality_error,
        "checkpoints": checkpoints, "trace": trace,
        "max_step_absolute_error_vs_a_gH": max_step_abs,
        "max_step_relative_error_vs_a_gH": max_step_rel,
        "max_closed_form_absolute_error": max_closed_abs,
        "direct_pair_vs_stable_difference_max_discrepancy": direct_difference_discrepancy,
        "donor_trace_match_max_error": trace_match_error,
        "final_donor_trace_match_max_error": float((tau[0]-tau[1]).abs().max()),
        "donor_correction_gates": correction_gates,
        "minimum_correction_gate": min(min(row) for row in correction_gates),
        "maximum_abs_raw_input": max_raw,
        "past_input_cube_legal": max_raw < .5,
        "absolute_raw_history_norms": torch.sqrt(raw_energy).detach().cpu().tolist(),
        "common_endpoint_max_pair_difference": float((h_prev[0]-h_prev[1]).abs().max()),
        "individual_probe_component_mean_abs": float(component_abs.mean()),
        "individual_probe_component_rms": combined/math.sqrt(K),
        "individual_probe_component_abs": component_abs.detach().cpu().tolist(),
        "unit_donor_witness_abs": witnesses.abs().detach().cpu().tolist(),
        "combined_donor_vector_norm": combined,
        "combined_norm_div_sqrt_K": combined/math.sqrt(K),
        "reference_one_step_query_lower": query_lower,
        "pure_storage_normal_final": protected_pure_final,
        "pure_storage_test_final": broken_pure_final,
        "pure_storage_ratio_to_normal": broken_pure_final/max(protected_pure_final, 1e-300),
        "pure_storage_outside_H_norm": float(torch.linalg.vector_norm(pure_outside)),
        "finite_reference_scope_only": True,
    }
    assert torch.isfinite(X).all() and torch.isfinite(Delta).all(), "STOP: NaN/Inf"
    print(f"n={n} K={K} {label or mode}: final Walsh={combined:.8g}; trace error={trace_match_error:.3g}; raw max={max_raw:.4g}", flush=True)
    return result


def hadamard(n):
    h = torch.ones(1, 1, device=DEVICE)
    while len(h) < n:
        h = torch.cat([torch.cat([h, h], dim=1), torch.cat([h, -h], dim=1)], dim=0)
    return h


def resources():
    import ctypes
    from ctypes import wintypes as w
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    class Memory(ctypes.Structure):
        _fields_ = [("cb", w.DWORD), ("faults", w.DWORD)] + [
            (key, ctypes.c_size_t) for key in ("peak_ws", "ws", "peak_paged", "paged", "peak_nonpaged", "nonpaged", "pagefile", "peak_pagefile")]
    kernel.GetCurrentProcess.restype = w.HANDLE
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    psapi.GetProcessMemoryInfo.argtypes = [w.HANDLE, ctypes.POINTER(Memory), w.DWORD]
    memory = Memory(); memory.cb = ctypes.sizeof(memory)
    assert psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(memory), memory.cb)
    return {"peak_process_working_set_bytes": memory.peak_ws,
            "cpu_seconds": time.process_time()-CPU_START, "wall_seconds": time.perf_counter()-START,
            "cuda_available": torch.cuda.is_available(), "device_used": str(DEVICE),
            "peak_cuda_allocated_bytes": 0 if DEVICE.type == "cpu" else torch.cuda.max_memory_allocated(),
            "torch_intraop_threads": torch.get_num_threads(), "torch_interop_threads": torch.get_num_interop_threads(),
            "worker_processes": 0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    if args.smoke:
        case = run_case(128, 4)
        print(json.dumps({k: case[k] for k in ("max_step_absolute_error_vs_a_gH", "max_step_relative_error_vs_a_gH", "maximum_abs_raw_input", "combined_donor_vector_norm")}, indent=2))
        return
    ROOT.joinpath("config.json").write_text(json.dumps(CONFIG, indent=2)+"\n", encoding="utf-8")
    cases = []
    for n in CONFIG["widths"]:
        cases.append(run_case(n, 4, "capture"))
        cases.append(run_case(n, 4, "control"))
    cases.append(run_case(1024, 4, "broken", label="nonuniform survivor gates during tail/clear"))
    scaling = []
    for K in CONFIG["donor_counts"]:
        coherent = next((c for c in cases if c["n"] == 1024 and c["K"] == K and c["mode"] == "capture"), None)
        if coherent is None:
            coherent = run_case(1024, K, "capture", label="coherent full-donor boundary")
            cases.append(coherent)
        q = max(2, K//4)
        B = hadamard(K)[:, :q]
        y = torch.arange(1, q+1, device=DEVICE, dtype=torch.float64)
        y[1::2] *= -1
        y /= torch.linalg.vector_norm(y)
        theta = torch.clamp(B@y, -1, 1)
        coded = run_case(1024, K, "capture", theta=theta, label="mixed clipped Hadamard boundary")
        cases.append(coded)
        scaling.append({"K": K, "q": q, "coherent": coherent, "mixed_code": coded})
    # Plotting and summary are separated from the numerical recurrence.
    from report_results import finish
    source = subprocess.check_output(["git", "show", "codex/linear-dimension-frontier-20261006:theory/codex_linear_dimension_frontier_20261006/PROOF.md"], cwd=ROOT.parents[1])
    metadata = {"source_ref": "e841ecb2f2f164f61f94c91485c8983618c6a558",
                "source_path": "theory/codex_linear_dimension_frontier_20261006/PROOF.md",
                "source_git_text_sha256": hashlib.sha256(source).hexdigest(),
                "pytorch_version": torch.__version__,
                "interpretation": "NUMERICAL EVIDENCE only; no theorem status change"}
    finish(ROOT, CONFIG, cases, scaling, metadata, resources)
    print(json.dumps(resources(), indent=2), flush=True)


if __name__ == "__main__":
    main()
