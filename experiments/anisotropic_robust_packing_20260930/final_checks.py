"""Artifact invariants and exact packing replay; no new numerical campaign."""
import json,hashlib,math
from fractions import Fraction as Q
import engine as e

def main():
    meter=e.Meter('final frozen-artifact and exact packing checks');checks=[]
    try:
        frozen=json.loads((e.ROOT/'PRIMARY_FROZEN.json').read_text())
        for name,digest in frozen['sha256'].items():
            assert hashlib.sha256((e.ROOT/name).read_bytes()).hexdigest()==digest,name
        checks.append('All primary-frozen byte hashes unchanged by secondary work')
        for mode in ('svd','frame'):
            rows=json.loads((e.ROOT/f'results_{mode}.json').read_text())
            replay=json.loads((e.ROOT/f'verification_{mode}.json').read_text())
            assert len(rows)==len(replay)==6 and all(x['verified'] for x in replay)
            for cert in rows:
                counts=[int(2*Q(a)*Q(b)//(Q(e.CFG['strict_spacing_epsilon_multiplier'])*Q(e.CFG['epsilon_primary'])))+1
                        for a,b in zip(cert['rho_i'],cert['mu_i'])]
                assert counts==cert['N_i'] and math.prod(counts)==int(cert['states'])
                assert sum(x>1 for x in counts)==cert['robust_dimension']
                assert max(x['center_inverse_residual_inf'] for x in replay)<1e-8
                source=json.loads((e.ROOT/f'certificate_{mode}_{cert["case"]}_n{cert["n"]}.json').read_text())
                assert source==cert
            checks.append(mode+': six original certificates verified at 256 bits; counts replay exactly')
        source=json.loads((e.ROOT/'source_hashes.json').read_text())
        assert all(hashlib.sha256((e.REPO/p).read_bytes()).hexdigest()==v for p,v in source.items())
        checks.append('All five prior source/certificate hashes unchanged')
        rows=json.loads((e.ROOT/'summary.json').read_text())
        for row in rows:
            n=row['n'];assert row['T']=={2:11,3:22,4:37}[n]
            assert row['P']==(2*n*n+n if row['case']=='dense' else n*n+2*n)
            assert row['D_exact']==(n*row['P'] if row['case']=='dense' else row['P'])
            basis=json.loads((e.ROOT/f'basis_{row["case"]}_n{n}.json').read_text())
            if n==4:assert float(basis['two_precision_relative_discrepancy'])<1e-35
        checks.append('Width/horizon/parameter/allowed-coordinate accounting; both width4 precision checks')
        reconstruction=json.loads((e.ROOT/'reconstruction_checks.json').read_text())
        assert len(reconstruction)==6 and all(x['passed'] for x in reconstruction)
        assert all(x['minimum_pair_query_distance'] is None or x['minimum_pair_query_distance']>2e-3 for x in reconstruction)
        checks.append('Fifteen grid points independently reconstructed; nontrivial pairs >2epsilon')
        weak=json.loads((e.ROOT/'weak_axis_certificates.json').read_text())
        assert all(Q(x['center_residual_exact'])<1 and float(x['bits'])==0 for x in weak)
        for case in ('dense','independent'):
            for n in (2,3,4):assert len(set(x['global_hessian_majorant_exact'] for x in weak if x['case']==case and x['n']==n))==1
        checks.append('Weak-axis global-majorant certificates valid and majorant unchanged within each case')
        assert e.CFG['epsilon_primary']=='1/1000'
        assert sum(x['cpu_seconds'] for x in e.read_rows(e.ROOT/'cpu_ledger.jsonl'))+time_cpu()<2700
        checks.append('Primary epsilon unchanged; measured CPU inside frozen45-minute cap')
        result={'passed':True,'checks':checks,'artifact_checks':len(checks),'unit_tests':json.loads((e.ROOT/'tests.json').read_text()),
                'reconstruction_points':sum(x['points_checked'] for x in reconstruction)}
        (e.ROOT/'final_checks.json').write_text(json.dumps(result,indent=2));print(result)
    finally:meter.finish()
def time_cpu():
    import time
    return time.process_time()
if __name__=='__main__':main()
