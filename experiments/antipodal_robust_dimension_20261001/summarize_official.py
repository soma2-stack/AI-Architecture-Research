"""Per-endpoint summary of official stage-1 results (192 + 256 certified only)."""
import json, glob, math
from fractions import Fraction as Q
from pathlib import Path
ROOT = Path(__file__).parent
prior = {'independent_n4_confirmation': 4, 'independent_n4_archived': 2, 'independent_n3_confirmation': 3, 'independent_n3_archived': 3,
         'dense_n4_confirmation': 3, 'dense_n4_archived': 1, 'dense_n3_confirmation': 3, 'dense_n3_archived': 2}
rows = [json.load(open(f)) for f in glob.glob(str(ROOT/'results/*.json')) if 'queue' not in f]
out = {'certified_candidates': sum(1 for d in rows if d.get('certified_dimension')), 'total_candidates': len(rows), 'endpoints': {}}
for name in prior:
    mine = [d for d in rows if d['candidate']['name'] == name]
    cert = [d for d in mine if d.get('certified_dimension')]
    best = max(cert, key=lambda d: (d['certified_dimension'], Q(d['result_256']['weakest_beta'])), default=None)
    rec = {'prior_certified_dimension': prior[name], 'attempted': len(mine),
           'failures': {k: sum(1 for d in mine if not d.get('certified_dimension') and (d['result_192'].get('reason') or 'face<=eps') == k) for k in ('hidden_section_box_inclusion', 'hidden_jacobian_dominance', 'outside fixed local domain', 'face<=eps')}}
    if best:
        r192, r256 = best['result_192'], best['result_256']
        rec.update(antipodal_certified_dimension=best['certified_dimension'], best_id=best['id'],
                   weakest_beta_192=r192['weakest_beta'], weakest_beta_256=r256['weakest_beta'],
                   weakest_beta_over_eps=float(Q(r256['weakest_beta'])*1000), beta_i_256=[float(Q(x)) for x in r256['beta_i']],
                   eta_hidden=r192['eta_hidden'], row_sums=r192['row_sums_upper'], max_raw_history_radius=float(Q(r192['max_raw_history_radius'])),
                   a_i=best['candidate']['a'], a_hidden=best['candidate']['ah'], basis=best['candidate']['basis'], corner_states=2**best['certified_dimension'])
    rec['strongest_lower_bound'] = max(prior[name], rec.get('antipodal_certified_dimension', 0))
    out['endpoints'][name] = rec
(ROOT/'summary.json').write_text(json.dumps(out, indent=1)+'\n')
for k, v in out['endpoints'].items():
    print(f"{k:28s} prior {v['prior_certified_dimension']} -> antipodal {v.get('antipodal_certified_dimension','-')} strongest {v['strongest_lower_bound']}  weakest beta/eps {v.get('weakest_beta_over_eps','-')}  radius {v.get('max_raw_history_radius','-')}")
