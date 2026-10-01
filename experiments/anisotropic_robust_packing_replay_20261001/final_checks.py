"""Post-replay comparison and an independent scalar mixed-curvature path."""
import replay as r
import mpmath as mp
import json, hashlib, itertools
from fractions import Fraction as Q
from pathlib import Path
import numpy as np

def main():
    meter=r.Meter('final independent cross-checks and artifact audit')
    try:
        A=json.loads((r.ROOT/'regenerated_certificate_192.json').read_text())
        B=json.loads((r.ROOT/'regenerated_certificate_256.json').read_text())
        original=json.loads((r.ROOT/'comparison_only.json').read_text())
        fields=('eta_hidden','eta_sensitivity','rho_i','mu_i','directional_curvature_F','projected_curvature',
                'scaled_jacobian_residual_upper','hidden_jacobian_residual_upper','hidden_forcing_upper',
                'normal_first_derivative_upper','K_hidden','K_selected','selected_projection','N_i','states','bits')
        comparisons={key:{'equal':A[key]==original[key]} for key in fields}
        assert all(x['equal'] for x in comparisons.values()),'Replay/original outward bounds differ; preserve and review'
        paired={key:A[key]==B[key] for key in fields}
        mu_difference=[str(Q(b)-Q(a)) for a,b in zip(A['mu_i'],B['mu_i'])]
        assert all(Q(x)>=0 for x in mu_difference)
        j1=json.loads((r.ROOT/'endpoint_jacobian_192.json').read_text())['J_intervals']
        j2=json.loads((r.ROOT/'endpoint_jacobian_256.json').read_text())['J_intervals']
        contained=0
        for row1,row2 in zip(j1,j2):
            for (lo1,hi1),(lo2,hi2) in zip(row1,row2):
                assert Q(int(lo1),2**192)<=Q(int(hi2),2**256) and Q(int(lo2),2**256)<=Q(int(hi1),2**192)
                contained+=Q(int(lo1),2**192)<=Q(int(lo2),2**256)<=Q(int(hi2),2**256)<=Q(int(hi1),2**192)
        raw1=json.loads((r.ROOT/'raw_curvature_192.json').read_text())
        raw2=json.loads((r.ROOT/'raw_curvature_256.json').read_text())
        assert raw1['hidden_mixed_upper']==raw2['hidden_mixed_upper']
        assert raw1['normalized_sensitivity_mixed_upper']==raw2['normalized_sensitivity_mixed_upper']
        mp.mp.dps=100
        model=r.model();theta=list(map(r.e.mpq,model.params))
        history=list(map(r.e.mpq,[Q(v) for row in r.INPUT['X'] for v in row]))
        basis=[[r.e.mpq(Q(v))*mp.sqrt(mp.mpf(3)/32) for v in row] for row in r.INPUT['B']]
        scales={g:mp.sqrt(sum(r.e.mpq(model.params[p])**2 for p,(_,_,name,_) in enumerate(model.meta) if name==g)/
                         sum(name==g for _,_,name,_ in model.meta)) for g in ('R','W','b')}
        def forward(th,hx):
            h=[mp.mpf(0)]*3
            for t in range(22):
                h=[mp.tanh(sum(th[3*i+j]*h[j]+th[9+3*i+j]*hx[3*t+j] for j in range(3))+th[18+i]) for i in range(3)]
            return h
        tests=[]
        for state,p,k,l in ((0,0,0,0),(1,10,0,3),(2,20,3,4),(0,9,4,4)):
            if k==l:
                def f(pp,z):
                    th=theta.copy();th[p]=pp
                    return forward(th,[x+b[k]*z for x,b in zip(history,basis)])[state]
                value=mp.diff(f,(theta[p],mp.mpf(0)),(1,2))
            else:
                def f(pp,y,z):
                    th=theta.copy();th[p]=pp
                    return forward(th,[x+b[k]*y+b[l]*z for x,b in zip(history,basis)])[state]
                value=mp.diff(f,(theta[p],mp.mpf(0),mp.mpf(0)),(1,1,1))
            value*=scales[model.meta[p][2]]
            upper=raw1['normalized_sensitivity_mixed_upper'][state*21+p][k][l]
            assert abs(value)<=mp.mpf(upper)
            tests.append({'state':state,'parameter':p,'axis_pair':[k,l],
                          'actual_center_value':mp.nstr(value,70),'complete_box_majorant':upper,
                          'method':'independent scalar forward recurrence + mpmath.diff at 100 digits; numerical supporting check'})
        manifest=json.loads((r.ROOT/'input_manifest.json').read_text());repository=r.ROOT.parents[1]
        unchanged={name:hashlib.sha256((repository/'experiments/anisotropic_robust_packing_20260930'/name).read_bytes()).hexdigest()==sha
                   for name,sha in manifest['original_directory_hashes'].items()}
        assert all(unchanged.values()),'Original evidence changed'
        for entry in manifest['sources']:
            assert hashlib.sha256((r.ROOT/entry['snapshot']).read_bytes()).hexdigest()==entry['sha256']
        checks={'original_192_comparison':comparisons,'precision_192_256_comparison':paired,
                'mu_256_minus_mu_192_exact':mu_difference,
                'endpoint_interval_count':66*66,'endpoint_intervals_256_contained_in_192':int(contained),
                'raw_HH_HS_exactly_equal_between_precisions':True,
                'independent_original_witness_mixed_curvature_checks':tests,
                'original_directory_unchanged':unchanged,'frozen_snapshots_hash_verified':True,
                'independence_scope':'New clean processes recompute all bounds; reviewed interval/jet/kernel source is shared, scalar differentiation cross-check is a separately written path.',
                'classification':'CLEAN REPLAY VERIFIED — TWO-AXIS CERTIFICATE REPRODUCED'}
        r.dump('final_checks.json',checks)
        print(json.dumps({'classification':checks['classification'],'all_192_fields_identical':True,
                          'contained_intervals':int(contained),'original_files_unchanged':len(unchanged),'scalar_mixed_checks':len(tests)}))
    finally:print(json.dumps(meter.finish()))

if __name__=='__main__':main()
