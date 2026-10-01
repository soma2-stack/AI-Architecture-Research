"""Exact rational inequality replay, array comparison, provenance, report."""
import time
CPU=time.process_time();WALL=time.perf_counter()
import common as c
import numpy as np
from fractions import Fraction as Q
k=c.k;checks=[]
def check(name,ok):
    checks.append({'name':name,'passed':bool(ok)})
    assert ok,name
if __name__=='__main__':
    f=c.verify();d=c.candidate();res=c.json.loads((c.ROOT/'result.json').read_text())
    check('frozen_methods_candidate_and_historical_evidence_preserved',bool(f))
    check('both_requested_precisions', [x['precision'] for x in res['attempts']]==[192,256])
    certificates=[x['certificate'] for x in res['attempts']]
    table=[];exact=[]
    for bits,v in zip((192,256),certificates):
        check(f'{bits}_valid_certificate_geometry',v['valid'])
        check(f'{bits}_physical_domain',Q(v['radius'])<=1)
        eta=Q(v['eta_hidden']);ah=Q(d['ah']);limit=(1-eta)*ah
        check(f'{bits}_hidden_contraction',eta<Q(3,4))
        check(f'{bits}_all_hidden_forcing_inclusion',all(Q(x)<=limit for x in v['hidden_forcing_upper']))
        beta=list(map(Q,v['beta3']));mu=list(map(Q,v['mu_tilde']))
        replay=[u*(1-Q(e)-Q(m)/6) for u,e,m in zip(mu,v['center_rows_upper'],v['M3_upper'])]
        check(f'{bits}_exact_eight_margin_replay',len(beta)==8 and beta==replay)
        check(f'{bits}_reported_decision_consistent',v['all_antipodal_faces_pass']==all(b>Q(1,1000) for b in beta))
        exact.append({'bits':bits,'hidden_limit':str(limit),'beta':list(map(str,beta)),
                      'separations':list(map(lambda z:str(2*z),beta)),
                      'cubic_penalties':list(map(lambda z:str(z),[u*Q(m)/6 for u,m in zip(mu,v['M3_upper'])]))})
    differences=[abs(Q(a)-Q(b)) for a,b in zip(certificates[0]['beta3'],certificates[1]['beta3'])]
    check('beta_precision_agreement',max(differences)<Q(1,10**10))
    ar=[np.load(c.ROOT/f'bounds_{bits}.npz') for bits in (192,256)]
    check('same_complete_derivative_array_keys',set(ar[0].files)==set(ar[1].files)=={'HH','HH3','HS','HS3','y2','y3','fixed3','selected3'})
    comparisons={}
    for name in ar[0].files:
        x,y=ar[0][name],ar[1][name]
        check(name+'_complete_finite_nonnegative',x.shape==y.shape and np.all(np.isfinite(x)) and np.all(np.isfinite(y)) and np.all(x>=0) and np.all(y>=0))
        check(name+'_precision_agreement',np.allclose(x,y,rtol=1e-11,atol=1e-280))
        comparisons[name]={'shape':list(x.shape),'entries':x.size,'bitwise_identical':bool(np.array_equal(x,y)),
                          'maximum_absolute_difference':float(np.max(abs(x-y)))}
    check('overall_decision_consistent',res['status']==('PASS' if all(v['all_antipodal_faces_pass'] for v in certificates) else 'FAIL'))
    check('CPU_only',res['gpu_used']==False and k.a.c.torch.ones(1).device.type=='cpu')
    cfg=c.json.loads((c.ROOT/'config.json').read_text())
    total=res['total_cpu_seconds']+time.process_time()-CPU
    check('CPU_budget',total<cfg['cpu_limit_seconds'])
    peak=max(res['peak_ram_bytes'],k.a.c.psutil.Process().memory_info().peak_wset)
    check('RAM_budget',peak<cfg['ram_limit_bytes'])
    measured=total-res['failed_test_CPU_charge']
    out={'checks':checks,'passed':len(checks),'arrays':comparisons,'exact':exact,
         'max_beta_difference':str(max(differences)),'max_beta_difference_float':float(max(differences)),
         'cpu_seconds':time.process_time()-CPU,'wall_seconds':time.perf_counter()-WALL,
         'total_cpu_seconds':total,'measured_cpu_seconds':measured,'failed_test_CPU_charge':res['failed_test_CPU_charge'],
         'peak_ram_bytes':peak,'gpu_seconds':0}
    c.write('checks.json',out)
    v=certificates[1];beta=list(map(Q,v['beta3']));mu=list(map(Q,v['mu_tilde']))
    rows='\n'.join(f'| {i+1} | {float(2*b):.15g} | {float(b/Q(1,1000)):.12g} | {float(mu[i]*Q(v["M3_upper"][i])/6):.12g} | {v["M3_upper"][i]:.12g} |'
                  for i,b in enumerate(beta))
    weak=min(range(8),key=lambda i:beta[i]);passed=res['status']=='PASS'
    status='8D RIGOROUSLY CERTIFIED — INDEPENDENT REVIEW REQUIRED' if passed else 'FAIL FOR THE FROZEN 8D SECTION'
    conclusion=('Under the accepted cube-boundary antipodal theorem, any continuous no-replay encoder satisfying the unchanged permitted gradient-query contract needs k>=8 real coordinates on this section. This is not eight bits or 256 mutually separated grid states.' if passed else 'At least one uniform lower face bound does not exceed 2epsilon. This is failure of this candidate certificate, not a proof that the endpoint lacks an 8D robust section.')
    report=f'''# Frozen 8D rigorous third-order antipodal certificate

## Result

**{status}** at BOTH 192 and 256 bits. Same independent width-4
confirmation endpoint/T37/P24, epsilon=1/1000, parameter-RMS/input-SD
normalization, support-aware permitted queries, fixed-h and continuous encoder
contract. No candidate tuning, new history, 9D/10D, architecture or GAS-0 work.

{conclusion}

## Guaranteed face separations (256-bit run)

Every entry below is a WHOLE-FACE outward lower bound, not a midpoint sample.
Required strict separation is >0.002. The cubic penalty is subtracted from
beta; guaranteed separation is twice beta.

| Face | Guaranteed 2beta | Ratio to 2epsilon | Cubic penalty mu*M3/6 | M3 upper |
|---|---:|---:|---:|---:|
{rows}

Weakest face: {weak+1}; separation {float(2*beta[weak]):.16g};
absolute slack {float(2*beta[weak]-Q(1,500)):.16g}; relative slack
{float(beta[weak]/Q(1,1000)-1)*100:.10g}%.

## Exact hidden section

Equal normal half-widths ah={float(Q(d['ah'])):.16g}.
Hidden contraction eta_h={v['eta_hidden']:.16g}, strictly below 3/4.
Forcing upper vector {v['hidden_forcing_upper']}.
Common forcing limit (1-eta_h)*ah={float(Q(exact[1]['hidden_limit'])):.16g}.
Local raw-history radius upper {float(Q(v['radius'])):.16g} <=1.
Frozen rational K_hidden and K_selected are independently inverted; center
residuals are included. Uniform self-map/contraction gives the exact curved
fixed-h lift throughout the simultaneous eight-axis box.

## Frozen candidate and accepted method

Primary numerical screen c057e4e, dimension_8.json / query_svd / proxy,
not its larger direct-geometry winner. Candidate SHA256
{res['candidate_sha256']}.
Pre-certification freeze commit {res['freeze_commit']}.
Amplitudes and all chart entries retain their exact binary64 rational values;
no 20-bit rounding or normal-amplitude inflation. Numerical chart() output L
is frozen with identity K_selected, and numerical inverse K_hidden is frozen.
Rigorous center residuals account for their inexactness.

The local reviewed_kernel.py is byte-identical to the accepted affine-tightened
kernel. Both W*B and W*x affine refinements, actual parameter injections,
all HH/HH3/HS/HS3 mixed terms, y^(2)/y^(3) and s_y*y^(3) are retained. The original
kernel's hard-coded '6D' reason is preserved in raw metadata and overridden
only in the new human-readable label; the generic r equations are unchanged.
Accepted proof and affine formulas are referenced by frozen source hashes;
no theorem or proof mathematics changed.

## Precision, arithmetic and checks

Fresh interval endpoint/box regeneration at 192 and 256 bits, with no reused
curvature outputs. Exact rational downstream replay; maximum beta precision
difference {float(max(differences)):.6g}. All eight complete derivative arrays
compared, {sum(z['entries'] for z in comparisons.values())} entries per precision.
Arrays bitwise identical: {all(z['bitwise_identical'] for z in comparisons.values())}.
Dyadic/transcendental intervals have the declared precision; positive tensor
majorants deliberately use the independently reviewed elementary upward
binary64 arithmetic. They are not 256-bit tensors or ordinary GPU estimates.

All {len(checks)} final checks pass; tests.json contains the synthetic tests.
Frozen inputs, numerical screen and previous 7D evidence remain unchanged.
There was no retuning, restart or fallback after official bounds.

## Resources and scope

One CPU thread. Measured CPU for setup, passed pre-official tests,
official runs and final checks: {measured:.6f}s ({measured/60:.6f}min).
Separately charge {res['failed_test_CPU_charge']} CPU-s for the failed pre-official
test/import process (conservative allowance, not a measurement). Budget-accounted
total is {total:.6f}s. The synthetic tensor-shape typo and pre-official repair
are preserved in preofficial_repair.json/FROZEN_INITIAL.json; frozen candidate
and reviewed kernel never changed.
Official wall time {res['wall_seconds']:.6f}s; complete timing components in
setup_resources.json/tests.json/result.json/checks.json. Peak process RAM
{peak/2**20:.6f}MiB. GPU/CUDA/own VRAM zero. Budget 1200 CPU-s, RAM 2GiB.

## Stop / next step

STOP. No 9D, 10D or architecture work. The strongest remaining uncertainty is
independent review of this new 8D candidate and its whole-box margin; the
result does not identify the model's maximum robust dimension. Recommend a
bounded independent hostile audit/replay before authorizing further work.
'''
    (c.ROOT/'REPORT.md').write_text(report,encoding='utf-8')
    c.write('OUTPUT_MANIFEST.json',{'sha256':{p.name:c.sha(p) for p in c.ROOT.iterdir() if p.is_file() and p.name!='OUTPUT_MANIFEST.json'}})
    print(c.json.dumps({'status':res['status'],'weakest_face':weak+1,'weakest_separation':float(2*beta[weak]),
      'slack_percent':float(beta[weak]/Q(1,1000)-1)*100,'checks':len(checks),'total_CPU_seconds':total,
      'peak_RAM_MiB':peak/2**20,'max_beta_precision_difference':float(max(differences))},indent=2))
