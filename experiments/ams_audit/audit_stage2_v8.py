import json
import numpy as np

def audit_v8():
    print("=" * 80)
    print("INDEPENDENT AUDIT: AMS v8 STAGE 2 & CONFIRMATION FUNNEL")
    print("=" * 80)

    # 1. Stage 2 Counts
    with open("experiments/automated_mechanism_search/runs/stage2_v8/counts.json") as f:
        counts = json.load(f)
    print("\n[1] Official Stage 2 Counts:")
    for k, v in counts.items():
        print(f"  {k:25s}: {v}")

    with open("experiments/automated_mechanism_search/runs/stage2_v8/archive.json") as f:
        archive = json.load(f)
    print(f"\nArchive cells occupied: {len(archive)} / 56")

    # 2. Fast Tier-1 Baselines (seeds 5000-5002)
    with open("experiments/automated_mechanism_search/runs/stage2_v8/baselines_tier1.json") as f:
        base_fast = json.load(f)
    print("\n[2] Fast Tier-1 Baselines (seeds 5000-5002):")
    for t in ["B", "Cstar", "F"]:
        bg = base_fast["best_generic"][t]
        aw = base_fast["adamw"][t]
        print(f"  Task {t:5s}: Best Generic = {bg['method']:5s} (metric = {bg['metric']:.4f}), AdamW mean = {aw['mean']:.4f}, sd = {aw['sd']:.4f}")

    # 3. Confirmation Baselines (seeds 6000-6007)
    with open("experiments/automated_mechanism_search/runs/stage2_v8_confirm/baselines_confirm.json") as f:
        base_conf = json.load(f)
    print("\n[3] Confirmation Baselines (seeds 6000-6007):")
    for t in ["B", "Cstar", "F"]:
        bg = base_conf["best_generic"][t]
        aw = base_conf["adamw"][t]
        print(f"  Task {t:5s}: Best Generic = {bg['method']:5s} (metric = {bg['metric']:.4f})")
        print(f"               AdamW mean = {aw['mean']:.4f}, sd = {aw['sd']:.4f}, 2*sd = {2*aw['sd']:.4f}, 2-sigma threshold = {aw['mean'] - 2*aw['sd']:.4f}")

    # 4. Confirmation Records Audit
    with open("experiments/automated_mechanism_search/runs/stage2_v8_confirm/confirmation.json") as f:
        conf = json.load(f)

    records = conf["records"]
    print(f"\n[4] Confirmation Funnel Records ({len(records)} elites evaluated):")
    print(f"  Total Candidates in Confirmation: {conf['n_candidates']}")
    print(f"  Total Eligible for Promotion:     {conf['n_eligible']}")
    print(f"  Promoted List:                    {conf['promoted']}")

    # Failure mode tallies
    fail_constraint = 0
    fail_adamw = 0
    fail_wins = 0
    fail_q = 0

    print("\n" + "-" * 125)
    print(f"{'PID':8s} | {'Cell':10s} | {'Task':5s} | {'q_fast':8s} | {'q_conf':8s} | {'m_P':7s} | {'m_G':7s} | {'Wins':5s} | {'Ret/Cons':8s} | {'AdamW 2s':8s} | {'Eligible':8s} | {'Fail Reasons'}")
    print("-" * 125)

    cstar_elites = []

    for r in records:
        pid = r["pid"]
        cell = str(r["cell"])
        task = r["task"]
        q_fast = r["q_fast"]
        q_conf = r["q_confirm"]
        m_P = r["m_P"]
        m_G = r["m_G"]
        wins = r["paired_wins"]
        cons_ok = r["constraint_ok"]
        adamw_ok = r["adamw_gate"]
        elig = r["eligible"]

        reasons = []
        if not cons_ok:
            fail_constraint += 1
            reasons.append("constraint")
        if not adamw_ok:
            fail_adamw += 1
            reasons.append("AdamW_2s")
        if wins < 6:
            fail_wins += 1
            reasons.append(f"wins({wins}<6)")
        if q_conf < 0.15:
            fail_q += 1
            reasons.append(f"q({q_conf:.3f}<0.15)")

        ret_str = ""
        if task == "Cstar":
            ret_ok_cnt = r.get("return_ok_count", "N/A")
            ret_str = f"{ret_ok_cnt}/8"
            cstar_elites.append(r)
        else:
            ret_str = "PASS" if cons_ok else "FAIL"

        print(f"{pid:8s} | {cell:10s} | {task:5s} | {q_fast:8.4f} | {q_conf:8.4f} | {m_P:7.4f} | {m_G:7.4f} | {wins:2d}/8  | {ret_str:8s} | {str(adamw_ok):8s} | {str(elig):8s} | {', '.join(reasons)}")

    print("-" * 125)
    print(f"\nFailure Breakdown across 42 Elites:")
    print(f"  Failed task constraint:     {fail_constraint} / 42")
    print(f"  Failed AdamW 2-sigma gate:  {fail_adamw} / 42")
    print(f"  Failed >= 6/8 paired wins:  {fail_wins} / 42")
    print(f"  Failed q_confirm >= 0.15:   {fail_q} / 42 (100.0%)")

    # 5. Deep-dive into Task C* Elites
    print("\n" + "=" * 80)
    print("[5] Deep-Dive: Task C* Elites in Confirmation Funnel")
    print("=" * 80)
    cstar_elites.sort(key=lambda x: -x["q_fast"])
    for r in cstar_elites:
        pid = r["pid"]
        print(f"\nCandidate {pid}:")
        print(f"  Cell: {r['cell']}, Descriptor: {r['descriptor']}")
        print(f"  Fast Tier-1 (3 seeds): q_fast = {r['q_fast']:.4f}")
        print(f"  Confirmation (8 seeds):")
        print(f"    P seed metrics (AULC): {r['seed_metric']}")
        print(f"    G seed metrics (SGD):  {r['G_seed_metric']}")
        print(f"    Mean AULC: m_P = {r['m_P']:.4f}, m_G = {r['m_G']:.4f}")
        uncapped_e = (r['m_G'] - r['m_P']) / r['m_G']
        print(f"    Uncapped effect vs G:   {uncapped_e:.4f}")
        print(f"    Return count (R0):      {r['return_ok_count']} / 8 (need >= 6)")
        print(f"    Capped effect e_conf:   {r['e_confirm']:.4f}")
        print(f"    Cost penalty:           {r['penalty']:.4f}")
        print(f"    q_confirm:              {r['q_confirm']:.4f}")
        print(f"    Paired wins vs SGD:     {r['paired_wins']} / 8")
        print(f"    AdamW 2-sigma check:    {r['adamw_gate']}")
        print(f"    Final Eligible:         {r['eligible']}")

if __name__ == "__main__":
    audit_v8()
