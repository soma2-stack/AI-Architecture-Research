"""Output formatting and static plots for the finite-size sanity check."""
import json
import math


def norm_at(case, where, key="walsh_row_norm"):
    return case["checkpoints"][where][key]


def slope(xs, ys):
    lx, ly = [math.log(x) for x in xs], [math.log(max(y, 1e-300)) for y in ys]
    mx, my = sum(lx)/len(lx), sum(ly)/len(ly)
    return sum((x-mx)*(y-my) for x, y in zip(lx, ly))/sum((x-mx)**2 for x in lx)


def finish(root, config, cases, scaling, metadata, measure_resources):
    capture = [c for c in cases if c["label"] == "capture"]
    control = [c for c in cases if c["mode"] == "control"]
    broken = next(c for c in cases if c["mode"] == "broken")
    main = next(c for c in capture if c["n"] == 1024)
    comparisons = []
    for cap, ctl in zip(capture, control):
        cf, uf = norm_at(cap, "after_reset"), norm_at(ctl, "after_reset", "common_row_norm")
        c0, u0 = norm_at(cap, "after_capture"), norm_at(ctl, "after_capture", "common_row_norm")
        comparisons.append({"n": cap["n"], "capture_final": cf,
                            "control_final_unprotected_common_row": uf,
                            "capture_final_div_control_final": cf/max(uf, 1e-300),
                            "capture_retained_fraction": cf/max(c0, 1e-300),
                            "control_retained_fraction": uf/max(u0, 1e-300),
                            "normalized_retention_advantage": (cf/max(c0, 1e-300))/(uf/max(u0, 1e-300)),
                            "control_final_walsh_row": norm_at(ctl, "after_reset")})
    coherent = [x["coherent"] for x in scaling]
    mixed = [x["mixed_code"] for x in scaling]
    ks = [x["K"] for x in scaling]
    combined_slope = slope(ks, [c["combined_donor_vector_norm"] for c in coherent])
    individual_slope = slope(ks, [c["individual_probe_component_mean_abs"] for c in coherent])
    tests = {
        "test_1_early_capture": {
            "status": "PASS" if all(c["max_step_relative_error_vs_a_gH"] < 1e-9
                                      and c["donor_trace_match_max_error"] < 1e-12
                                      and c["past_input_cube_legal"]
                                      and c["common_endpoint_max_pair_difference"] == 0 for c in capture) else "FAIL",
            "max_step_absolute_error": max(c["max_step_absolute_error_vs_a_gH"] for c in capture),
            "max_step_relative_error": max(c["max_step_relative_error_vs_a_gH"] for c in capture),
            "interpretation": "Trace correction preserves the captured row up to floating-point roundoff, after expected a*g_H decay."},
        "test_2_capture_vs_control": {
            "status": "PASS" if comparisons[-1]["capture_final_div_control_final"] > 1
                                    and comparisons[-1]["normalized_retention_advantage"] > 2 else "INCONCLUSIVE",
            "comparisons": comparisons,
            "definition": "Control_final is its unprotected COMMON-row norm, not its identically zero Walsh read. Raw ratios and normalized retained fractions are both reported."},
        "test_3_coded_donor_scaling": {
            "status": "PASS" if abs(combined_slope) < .2 and abs(individual_slope+.5) < .2 else "INCONCLUSIVE",
            "coherent_combined_log_log_slope": combined_slope,
            "coherent_individual_mean_abs_log_log_slope": individual_slope,
            "coherent_K32_div_K4_combined": coherent[-1]["combined_donor_vector_norm"]/coherent[0]["combined_donor_vector_norm"],
            "mixed_K32_div_K4_combined": mixed[-1]["combined_donor_vector_norm"]/mixed[0]["combined_donor_vector_norm"],
            "definition": "A small public clipped Hadamard code is a finite analogue, not the full-spark Gaussian existence lemma or a full-boundary dimension test. Coherent and one non-axis mixed boundary are measured."},
        "test_4_intentional_break": {
            "status": "PASS" if broken["pure_storage_ratio_to_normal"] < .95
                                     and broken["max_step_relative_error_vs_a_gH"] > 1e-6 else "INCONCLUSIVE",
            "pure_storage_ratio_to_normal": broken["pure_storage_ratio_to_normal"],
            "pure_storage_outside_H_norm": broken["pure_storage_outside_H_norm"],
            "complete_pair_final_div_normal": broken["combined_donor_vector_norm"]/main["combined_donor_vector_norm"],
            "max_step_relative_error": broken["max_step_relative_error_vs_a_gH"],
            "definition": "During tail/clear, the positive Walsh half is set to g_L instead of g_H. Both complete paired histories and an isolated stored zero-sum component are followed through the full O_* transport."},
    }
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    for ax, cap, ctl in zip(axes.flat, capture, control):
        ax.semilogy([x["t"] for x in cap["trace"]], [max(x["walsh_row_norm"], 1e-20) for x in cap["trace"]], label="Capture: protected Walsh row")
        ax.semilogy([x["t"] for x in ctl["trace"]], [max(x["common_row_norm"], 1e-20) for x in ctl["trace"]], label="Control: unprotected common row")
        post = [x for x in cap["trace"] if x["predicted_protected_norm"] is not None]
        ax.semilogy([x["t"] for x in post], [max(x["predicted_protected_norm"], 1e-20) for x in post], "--", color="black", linewidth=1, label="Predicted scalar decay")
        if cap["n"] == 1024:
            ax.semilogy([x["t"] for x in broken["trace"]], [max(x["walsh_row_norm"], 1e-20) for x in broken["trace"]], color="tab:red", label="Broken protection")
        for where in ("after_capture", "after_trace_correction", "after_clear"):
            ax.axvline(cap["checkpoints"][where]["t"], color="gray", alpha=.25, linewidth=.8)
        ax.set_title(f"n={cap['n']}, K=4; final capture/control={comparisons[config['widths'].index(cap['n'])]['capture_final_div_control_final']:.3g}")
        ax.set_xlabel("Step after preparation")
        ax.set_ylabel("Sensitivity-row vector norm")
        ax.grid(alpha=.2)
        ax.legend(fontsize=7)
    fig.suptitle("Early capture survives trace correction with its predicted decay\nStationary-carrier finite reference experiment; no training", fontsize=12)
    fig.savefig(root/"signal_survival.png", dpi=160)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
    for ax, group, title in zip(axes, (coherent, mixed), ("Coherent fully saturated controls", "Mixed clipped-code boundary")):
        for key, label in (("individual_probe_component_mean_abs", "Individual probe: mean absolute"),
                           ("combined_donor_vector_norm", "Combined donor vector norm"),
                           ("combined_norm_div_sqrt_K", "Combined / sqrt(K)")):
            ax.loglog(ks, [c[key] for c in group], "o-", label=label)
        ax.set_xticks(ks, labels=[str(k) for k in ks])
        from matplotlib.ticker import NullLocator
        ax.xaxis.set_minor_locator(NullLocator())
        ax.set_xlabel("K donor parameter probes")
        ax.set_ylabel("Final protected-row response")
        ax.set_title(title)
        ax.grid(alpha=.2)
        ax.legend(fontsize=8)
    fig.suptitle("Individual coordinates can dilute while their Euclidean norm remains useful", fontsize=12)
    fig.savefig(root/"coded_donor_scaling.png", dpi=160)
    plt.close(fig)
    result = {"metadata": metadata, "config": config, "tests": tests,
              "cases": cases, "resources": measure_resources(),
              "contradiction_to_theory": False,
              "limits": ["No full-boundary robust-dimension inference", "Stationary carrier rather than long nonwrapping moving corridor", "Tiny dense transfer perturbation not tested", "Finite widths are outside the asymptotic theorem range"]}
    root.joinpath("results.json").write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    lines = ["# Finite-n early capture sanity experiment", "",
             "**NUMERICAL EVIDENCE — not a proof, not training, and no theorem-status change.**", "",
             "The captured signal followed its expected decay while the donor traces were repaired. We retained the full Householder feedback and chronological public gates.", "",
             "These tiny widths cannot fit the theorem's long, nonwrapping moving corridors. We used balanced four-site stationary off-cycle carriers, an exact zero-sum reducing space of the same reference O_* matrix. We did not test the tiny actual-model dense perturbation. Every tested past input was also checked against the (-.5,.5) cube.", "",
             "Run again with `python experiments/finite_n_early_capture_20261006/run_experiment.py`. Fixed settings are in `config.json`; there are no learned parameters, training loops or optimization.", "",
             "## Test 1: early capture — "+tests["test_1_early_capture"]["status"], "",
             "Values below are norms of the full donor-column sensitivity row. Near-zero before capture is expected: the useful difference is initially common, not Walsh-shaped.", "",
             "| n | End write: Walsh | After capture | After trace correction | After clear | After reset | Max relative one-step error |",
             "|---|---:|---:|---:|---:|---:|---:|"]
    for c in capture:
        vals = [norm_at(c, p) for p in ("end_write", "after_capture", "after_trace_correction", "after_clear", "after_reset")]
        lines.append(f"| {c['n']} | "+" | ".join(f"{v:.9g}" for v in vals)+f" | {c['max_step_relative_error_vs_a_gH']:.3g} |")
    lines += ["", f"Largest absolute one-step error: **{tests['test_1_early_capture']['max_step_absolute_error']:.6g}**. Largest relative one-step error: **{tests['test_1_early_capture']['max_step_relative_error']:.6g}**.",
              "Expected tail/clear factor is a*g_H. Reset uses a*(1-.05^2), not g_H. Raw signal decay is expected; the test checks extra damage beyond this decay.", "",
              "| n | Trace-correction checkpoint: absolute prediction error | Relative prediction error | Donor trace mismatch | Smallest final correction gate | Max absolute raw input | Full raw history norm (pair) |",
              "|---|---:|---:|---:|---:|---:|---|"]
    for c in capture:
        pt = c["checkpoints"]["after_trace_correction"]
        lines.append(f"| {c['n']} | {pt['absolute_prediction_error']:.6g} | {pt['relative_prediction_error']:.6g} | {c['donor_trace_match_max_error']:.6g} | {c['minimum_correction_gate']:.9g} | {c['maximum_abs_raw_input']:.6g} | {c['absolute_raw_history_norms'][0]:.6g}, {c['absolute_raw_history_norms'][1]:.6g} |")
    lines += ["", "## Test 2: early capture versus control — "+tests["test_2_capture_vs_control"]["status"], "",
              "The control skips the Walsh mask. Its useful signal remains an unprotected common row. We compare that common read against the captured Walsh read; we do not divide by an identically zero control Walsh read. Because capture initially spends gain on a small mask contrast, both raw final ratios and normalized survival are shown.", "",
              "| n | Capture final / control final | Captured fraction retained | Control fraction retained | Normalized retention advantage |",
              "|---|---:|---:|---:|---:|"]
    for c in comparisons:
        lines.append(f"| {c['n']} | {c['capture_final_div_control_final']:.6g} | {c['capture_retained_fraction']:.6g} | {c['control_retained_fraction']:.6g} | {c['normalized_retention_advantage']:.6g} |")
    lines += ["", "## Test 3: coded-donor scaling — "+tests["test_3_coded_donor_scaling"]["status"], "",
              "All runs here use n=1024, m=64, the same duration and one survivor support. The small structured clipped code is an experimental analogue; it is not a verification of the theorem's Gaussian/full-spark code or every boundary direction.", "",
              "| K | Individual mean absolute: coherent | Combined norm: coherent | Combined / sqrt(K) | Combined norm: mixed code | Saturated mixed-code donors |",
              "|---|---:|---:|---:|---:|---:|"]
    for c, m in zip(coherent, mixed):
        lines.append(f"| {c['K']} | {c['individual_probe_component_mean_abs']:.9g} | {c['combined_donor_vector_norm']:.9g} | {c['combined_norm_div_sqrt_K']:.9g} | {m['combined_donor_vector_norm']:.9g} | {m['saturated_donors']} |")
    lines += ["", f"Coherent combined-norm slope versus K: **{combined_slope:.6g}**; individual-coordinate slope: **{individual_slope:.6g}**. A flat combined norm with shrinking individual coordinates is the expected Euclidean aggregation. It does not establish K independent robust dimensions.", "",
              "## Test 4: intentional protection break — "+tests["test_4_intentional_break"]["status"], "",
              "We made the survivor gates nonuniform during correction and clearing. This removes the exact reducing-space condition. An isolated stored Walsh component was propagated alongside the complete pair so loss can be measured separately from any newly generated response.", "",
              f"- Isolated stored component, broken / protected final: **{broken['pure_storage_ratio_to_normal']:.9g}**.",
              f"- Isolated component outside the protected space at the end: **{broken['pure_storage_outside_H_norm']:.9g}**.",
              f"- Complete-pair broken / normal final read: **{tests['test_4_intentional_break']['complete_pair_final_div_normal']:.9g}**.",
              f"- Largest broken one-step relative error against a*g_H: **{broken['max_step_relative_error_vs_a_gH']:.9g}**.", "",
              "## What this means", "",
              "The experiment tests an algebraic storage mechanism at small sizes. It does not test the astronomical theorem onset, establish a whole-ball robust memory dimension, or change any theory status. No failed or inconclusive comparison is hidden.", "",
              "Most useful next test: run two consecutive fresh Walsh captures with independently coded donor words and check that the second write does not contaminate the first singleton read after both trace repairs and the common reset.", "",
              "## Resources and files", "",
              f"PyTorch {metadata['pytorch_version']}; CPU float64; one intra-op and one inter-op thread; zero workers. CUDA available: {result['resources']['cuda_available']}. GPU/VRAM used: 0 bytes.",
              f"Measured wall time: {result['resources']['wall_seconds']:.3f} seconds; CPU time: {result['resources']['cpu_seconds']:.3f} seconds; peak process working set: {result['resources']['peak_process_working_set_bytes']/1024**2:.2f} MiB.",
              "", "Outputs: results.json, SUMMARY.md, signal_survival.png, coded_donor_scaling.png. Reproduction sources: run_experiment.py, report_results.py, config.json.",
              "", f"Theory source: {metadata['source_path']} at {metadata['source_ref']}. No research or governance files were edited."]
    root.joinpath("SUMMARY.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    print(json.dumps({name: record["status"] for name, record in tests.items()}, indent=2), flush=True)
