"""Collect face searches, confirmations and slack diagnostics into out/summary.json (no new model evaluations)."""
import json, math
from pathlib import Path

OUT = Path(__file__).resolve().parent / 'out'
EPS2 = 2e-3


def load(pattern):
    return [json.loads(p.read_text()) for p in sorted(OUT.glob(pattern))]


faces = {}
for d in load('face*_*.json'):
    f = faces.setdefault(d['face'], {'rounds': []})
    f['rounds'].append({k: d[k] for k in ('escalate', 'weakest_round', 'best_value', 'best_method', 'best_BD', 'best_C',
                                         'reliable_BD_vs_C', 'cpu_seconds')})
    if 'best' not in f or d['best_value'] < f['best']['best_value']:
        f['best'] = d
summary = {'faces': {}}
for face, f in sorted(faces.items()):
    b = f['best']; base = next((r for r in f['rounds'] if not r['escalate'] and not r['weakest_round']), None)
    extra = [r for r in f['rounds'] if r['escalate'] or r['weakest_round']]
    pre = min(r['best_value'] for r in f['rounds'] if not r['escalate'])
    esc = [r for r in extra if r['escalate']]
    reliable = base['reliable_BD_vs_C'] or (bool(esc) and all(r['best_value'] >= 0.99 * pre for r in esc))
    row = {'best_DC': b['best_value'], 'ratio_to_2eps': b['best_value'] / EPS2, 'certified_2beta': b['certified_2beta'],
           'ratio_to_2beta': b['ratio_to_2beta'], 'D78_at_best': b['D78_at_best'], 'best_z': b['best_z'],
           'reliable': reliable, 'rounds': f['rounds'], 'max_y_over_ah': max(d['stats']['max_y_over_ah'] for d in load(f'face{face}_*.json')),
           'max_lift_residual': max(d['stats']['max_lift_residual'] for d in load(f'face{face}_*.json')),
           'newton_failures': sum(d['stats']['newton_failures'] for d in load(f'face{face}_*.json'))}
    c = OUT / f'confirm_face{face}.json'
    if c.exists():
        cc = json.loads(c.read_text()); row.update(confirm_rel_diff=cc['rel_diff'], DC_mp50=cc['DC_mp50'], confirm_y_over_ah=cc['max_y_over_ah_mp'])
    k = OUT / f'curv_face{face}.json'
    if k.exists():
        kk = json.loads(k.read_text())
        row.update(slack_log_terms=kk['log_terms'], slack_log_total=kk['log_total'], G_ray=kk['G_ray'], M3=kk['M3'],
                   G_face_hat=kk['G_face_hat'], oracle_face_bound=kk['oracle_face_bound'], mu_min_dphi_face=kk['mu_min_dphi_face'],
                   odd_remainder_over_M3_third=kk['odd_remainder_over_M3_third'], mu_dphi_at_best=kk['mu_dphi'])
    summary['faces'][face] = row
rows = summary['faces']
if rows:
    m_face = min(rows, key=lambda f: rows[f]['best_DC']); m = rows[m_face]['best_DC']
    confirmed = all(r.get('confirm_rel_diff', 1) <= 1e-8 for r in rows.values())
    valid = all(r['newton_failures'] == 0 and r['max_y_over_ah'] <= 1 for r in rows.values())
    reliable = all(r['reliable'] for r in rows.values())
    if m <= EPS2 and valid and rows[m_face].get('confirm_rel_diff', 1) <= 1e-8:
        verdict = '7D SECTION LOOKS TOO WEAK AT EPSILON'
    elif m >= 1.05 * EPS2 and reliable and valid and confirmed and len(rows) == 7:
        verdict = '7D LOOKS REAL — CERTIFICATE IS TOO CONSERVATIVE'
    else:
        verdict = 'INCONCLUSIVE'
    summary.update(actual_weakest_face=m_face, min_DC=m, min_ratio_to_2eps=m / EPS2, all_reliable=reliable,
                   all_confirmed=confirmed, all_lifts_valid=valid, classification=verdict)
(OUT / 'summary.json').write_text(json.dumps(summary, indent=1))
print(json.dumps({k: v for k, v in summary.items() if k != 'faces'}, indent=1))
for f, r in rows.items():
    print(f"face {f}: D_C {r['best_DC']:.6e}  /2eps {r['ratio_to_2eps']:.4f}  /2beta {r['ratio_to_2beta']:.4f}  reliable {r['reliable']}"
          + (f"  conf {r['confirm_rel_diff']:.1e}" if 'confirm_rel_diff' in r else '')
          + (f"  slack {({k: round(v, 3) for k, v in r['slack_log_terms'].items()})}" if 'slack_log_terms' in r else ''))
