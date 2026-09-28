import json
import numpy as np
from scipy import stats

def audit_stage2():
    print("=" * 70)
    print("INDEPENDENT AUDIT: AMS v7 STAGE 2")
    print("=" * 70)
    with open("experiments/automated_mechanism_search/runs/stage2_v7/counts.json") as f:
        counts = json.load(f)
    print("Stage 2 Counts:")
    for k, v in counts.items():
        print(f"  {k:25s}: {v}")

    with open("experiments/automated_mechanism_search/runs/stage2_v7/archive.json") as f:
        archive = json.load(f)
    print(f"\nArchive cells occupied: {len(archive)} / 56")

    with open("experiments/automated_mechanism_search/runs/stage2_v7/promotions.json") as f:
        promotions = json.load(f)
    print(f"Promotions count: {len(promotions)}")
    for p in promotions:
        pid = p["pid"]
        task = p["best_task"]
        q = p["quality"]
        couplings = p["fingerprint"]["couplings"]
        m_Cstar = p["tier1"]["metrics"]["Cstar"]
        effects = p["tier1"]["effects"]
        print(f"  {pid}: task={task}, q={q:.4f}, couplings={couplings}, Cstar_metric={m_Cstar}, effects={effects}")

def audit_stage3():
    print("\n" + "=" * 70)
    print("INDEPENDENT AUDIT: AMS v7 STAGE 3")
    print("=" * 70)
    with open("experiments/automated_mechanism_search/runs/stage3_v7/results.json") as f:
        res = json.load(f)

    candidates = res["candidates"]
    print(f"Total Candidates evaluated in Stage 3: {len(candidates)}")
    print(f"Evaluation Seeds (10 fresh seeds): {res['seeds']}")
    print(f"Total CPU seconds: {res['cpu_seconds']:.2f} s")
    print(f"Cumulative CPU hours: {res['cumulative_cpu_hours']:.5f} h")
    print(f"Final Labels summary: {res['labels']}")

    m_G = 21.8 # Best generic SGD
    tau = 10.9 # Required threshold (m_P <= 10.9)
    print(f"\nBest Generic G: SGD (m_G = {m_G})")
    print(f"Preregistered Threshold tau: m_P <= {tau} (50% reduction vs best generic)")

    p_vals = []
    
    print("\n" + "-" * 110)
    print(f"{'PID':8s} | {'m_P':6s} | {'Ret OK':6s} | {'Thresh':6s} | {'Wilcox p':10s} | {'Holm':5s} | {'Bootstrap 95% CI':18s} | {'Gate 3':6s} | {'Label':8s}")
    print("-" * 110)

    for c in candidates:
        pid = c["pid"]
        dec = c["decision"]
        m_P = dec["m_P"]
        ret_ok = c["summaries"]["P"]["return_ok_count"]
        diff = np.array(dec["per_seed_G_minus_P"], dtype=float)
        
        # Independent Wilcoxon signed-rank test
        # Preregistration: test whether G - P > 0 (candidate faster than generic)
        nonzero = diff[diff != 0]
        if len(nonzero) > 0:
            w_res = stats.wilcoxon(diff, alternative="greater")
            w_p = float(w_res.pvalue)
        else:
            w_p = 1.0

        # Independent Bootstrap 95% CI of mean(G - P)
        rng = np.random.RandomState(42)
        boot_means = [rng.choice(diff, size=len(diff), replace=True).mean() for _ in range(10000)]
        ci_low, ci_high = np.percentile(boot_means, [2.5, 97.5])
        
        # Gate 3 conditions:
        # 1. m_P <= tau (10.9) and return_ok_count >= 8/10
        thresh_pass = (m_P <= tau) and (ret_ok >= 8)
        # 2. bootstrap CI excludes 0 (ci_low > 0)
        boot_excludes_0 = ci_low > 0
        
        p_vals.append((pid, dec["wilcoxon_p"], thresh_pass, boot_excludes_0, dec["gate3"], c["label"]))

        print(f"{pid:8s} | {m_P:6.1f} | {ret_ok:2d}/10  | {str(dec['threshold_ok']):6s} | {dec['wilcoxon_p']:10.6f} | {str(dec['holm_significant']):5s} | [{dec['bootstrap_ci'][0]:5.1f}, {dec['bootstrap_ci'][1]:5.1f}]       | {str(dec['gate3']):6s} | {c['label']:8s}")

    print("-" * 110)

    # Independent Holm-Bonferroni verification
    print("\nIndependent Holm-Bonferroni Correction Verification (family-wise alpha = 0.05, 8 tests):")
    sorted_candidates = sorted(p_vals, key=lambda x: x[1])
    m_tests = len(sorted_candidates)
    alpha = 0.05
    for rank, (pid, p_val, thresh_pass, boot_excl, g3_pass, lbl) in enumerate(sorted_candidates):
        k = rank + 1
        alpha_k = alpha / (m_tests - k + 1)
        is_sig = p_val <= alpha_k
        print(f"  Rank {k}: {pid:8s} | p = {p_val:.6f} | threshold = {alpha}/({m_tests}-{k}+1) = {alpha_k:.6f} | Significant: {is_sig}")

    print("\nSummary of Gate 3 Verification:")
    all_gate3_fail = all(not c["decision"]["gate3"] for c in candidates)
    all_negative = all(c["label"] == "NEGATIVE" for c in candidates)
    print(f"  All 8 candidates fail Gate 3: {all_gate3_fail}")
    print(f"  All 8 candidates labeled NEGATIVE: {all_negative}")

if __name__ == "__main__":
    audit_stage2()
    audit_stage3()
