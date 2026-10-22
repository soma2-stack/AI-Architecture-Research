"""Separate scalar nonlinear leakage tests and independent class-recurrence reproduction."""
from pathlib import Path
import json
import mpmath as mp
import e7_independent as e7
mp.mp.dps=70
HERE=Path(__file__).resolve().parent

def main():
    scalar=[]; a=1-mp.mpf(1)/65536; s=mp.mpf('.052')
    field=mp.atanh(s)-a*s; beta=mp.tanh(field)
    for R in (16,64,256,1024):
        vals={}
        for mode in ('zero','symmetric'):
            y=mp.mpf(0) if mode=='zero' else -beta*R/2
            deficit=mp.mpf(0); log_ret=mp.mpf(0); error=mp.mpf(0)
            for r in range(R):
                deficit+=y*y; log_ret+=mp.log(1-y*y)
                yn=mp.tanh(a*y+field)
                step_err=abs(yn-y-beta)
                bound=(1-a)*abs(y)+a*abs(y)*(a*abs(y)+abs(field))**2
                assert step_err<=bound+mp.mpf('1e-60')
                error=max(error,step_err); y=yn
            vals[mode]={'exact_mean_gate_deficit':str(deficit/R),'log_local_retention_per_period':str(log_ret),'largest_drift_linearization_error':str(error),'final_y':str(y)}
        scalar.append({'R':R,'zero':vals['zero'],'symmetric':vals['symmetric'],'deficit_ratio_zero_over_symmetric':str(mp.mpf(vals['zero']['exact_mean_gate_deficit'])/mp.mpf(vals['symmetric']['exact_mean_gate_deficit']))})
    # Author's published beta is used only as an input parameter; propagation/readout is independent.
    pub=json.loads((HERE.parents[0]/'claude_remaining_channels_20261020'/'exp_resets_result.json').read_text())
    beta_target=pub['beta']; rows=[]
    for kind in ('hold','reset64','symmetric64','symmetric256','symmetric1024'):
        result=e7.run(65536,2048,kind,beta_target=beta_target)
        R=int(kind[len('symmetric'):]) if kind.startswith('symmetric') else 64 if kind=='reset64' else 1
        target='sym' if kind.startswith('symmetric') else 'zero'
        expected=next(x for x in pub['rows'] if x['mode']==('hold' if kind=='hold' else 'stag') and x['R']==R and x['target']==target)
        err=abs(result['centered_one_column_box_optimum']-expected['readout'])
        assert err<1e-8
        assert result['peak_actual_width_m']==expected['peak width m']
        rows.append({'kind':kind,'independent_readout':result['centered_one_column_box_optimum'],'author_saved_readout':expected['readout'],'absolute_error':err,'m':result['peak_actual_width_m'],'mT':result['mT'],'E_from_warmup':result['cumulative_max_gate_deficit_E'],'E_from_source_pulse':result['E_from_source_pulse_to_T'],'max_input':result['max_abs_actual_input']})
    out={'scalar_steady_bath':{'n':65536,'s':str(s),'field_beta_prime':str(field),'actual_beta':str(beta),'rows':scalar},'network_reproduction':rows,'note':'No universal symmetric-reset or resource exponent theorem inferred from finite tests.'}
    (HERE/'reset_law_results.json').write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
if __name__=='__main__':main()
