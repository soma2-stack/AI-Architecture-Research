"""Post-freeze comparison and exact downstream audit; never imports old engines."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import gzip,hashlib,itertools,json,time
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext,ROUND_CEILING,ROUND_FLOOR
import numpy as np
import psutil
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OLD=ROOT/'experiments/rebalanced_7d_section_20261001'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def diff(new,old):
    a=np.array(new,dtype=float);b=np.array(old,dtype=float)
    delta=np.abs(a-b); nz=np.abs(b)>1e-300
    rel=np.zeros_like(delta);rel[nz]=delta[nz]/np.abs(b[nz])
    ix=np.unravel_index(int(np.argmax(rel)),rel.shape) if rel.ndim else ()
    return {'shape':a.shape,'entries':a.size,'max_absolute':float(delta.max()),
            'max_relative_nonzero':float(rel.max()),'max_relative_index':[int(j) for j in ix],
            'reference_at_index':float(b[ix]),'new_at_index':float(a[ix]),
            'exact_zero_pattern_equal':bool(np.array_equal(a==0,b==0)),
            'passed':bool(np.all(delta<=1e-14+1e-10*np.abs(b)))}
def decimal_query(c,i):
    """Separate Decimal path: exact rational ell and independently rounded sqrt."""
    K=[[F(x) for x in row] for row in c['K_selected']]
    L=[[F(x) for x in row] for row in c['L']]
    a=F(c['a'][i]);dr=[F(x) for x in c['model_parameters'][:4]]
    ell=[sum(K[i][j]*L[j][p] for j in range(7))/a for p in range(24)]
    norm2=sum(x*x/(dr[p//6]**2) for p,x in enumerate(ell))
    square=4*max(F(1),sum(x*x for x in dr))*norm2
    with localcontext() as ctx:
        ctx.prec=100;ctx.rounding=ROUND_CEILING
        x=Decimal(square.numerator)/Decimal(square.denominator)
        root=x.sqrt().next_plus()
        ctx.rounding=ROUND_FLOOR
        mu=(Decimal(7)/8)/root
    return F(mu),square

def main():
    start=time.perf_counter();cpu=time.process_time();checks=[]
    def check(name,ok):
        checks.append({'name':name,'passed':bool(ok)})
        if not ok: raise RuntimeError('comparison/check failed: '+name)
    freeze=json.loads((HERE/'METHOD_FROZEN.json').read_text(encoding='utf-8'))
    ofreeze=json.loads((HERE/'REPLAY_OUTPUT_FROZEN.json').read_text(encoding='utf-8'))
    check('method_sources_preserved',all(sha(HERE/k)==v for k,v in freeze['method_hashes'].items()))
    check('independent_outputs_frozen_before_comparison',all(sha(HERE/k)==v for k,v in ofreeze['sha256'].items()))
    check('all_original_outputs_and_sources_unchanged',all(sha(ROOT/k)==v for k,v in freeze['original_preservation'].items()))
    old=json.loads((OLD/'result.json').read_text(encoding='utf-8'))
    comparisons={};newresults={}
    names=('HH','HH3','HS','HS3','y2','y3','fixed3','selected3')
    scalar_fields={'eta_h':'eta_hidden','forcing':'hidden_forcing_upper','domain':'radius',
                   'center_rows':'center_rows_upper','M3':'M3_upper','mu':'mu_tilde','beta':'beta3',
                   'Eh':'hidden_residual_upper','Gamma':'normal_first_derivative_upper'}
    for bits in (192,256):
        new=json.loads((HERE/f'result_{bits}.json').read_text(encoding='utf-8'));newresults[bits]=new
        ref=next(a['certificate'] for a in old['attempts'] if a['precision']==bits)
        n=np.load(HERE/f'bounds_{bits}.npz');o=np.load(OLD/f'bounds_{bits}.npz')
        check(f'{bits}_array_names',tuple(n.files)==names and set(o.files)==set(names))
        ar={k:diff(n[k],o[k]) for k in names}
        for k,v in ar.items(): check(f'{bits}_all_entries_{k}',v['passed'] and v['exact_zero_pattern_equal'])
        def to_floats(a):
            if isinstance(a,list): return [to_floats(x) for x in a]
            return float(F(a))
        sc={k:diff(to_floats(new[k]),to_floats(ref[v])) for k,v in scalar_fields.items()}
        for k,v in sc.items(): check(f'{bits}_scalar_{k}',v['passed'])
        check(f'{bits}_decision',new['decision']=='PASS' and ref['valid'] and ref['all_antipodal_faces_pass'])
        comparisons[str(bits)]={'arrays':ar,'scalars':sc}
    check('192_256_binary64_bound_summaries_identical',all(np.array_equal(np.load(HERE/'bounds_192.npz')[k],np.load(HERE/'bounds_256.npz')[k]) for k in names))
    precision_difference={k:max(abs(F(a)-F(b)) for a,b in zip(newresults[192][k],newresults[256][k])) for k in ('beta','M3','mu','forcing','center_rows')}
    check('higher_precision_margin_agreement',precision_difference['beta']<F(1,10**50))
    c=json.loads((HERE/'frozen_candidate.json').read_text(encoding='utf-8'))
    with gzip.open(HERE/'exact_bounds_256.json.gz','rt',encoding='utf-8') as f: raw=json.load(f)
    T=np.array([F(v) for v in raw['selected3']['values']],dtype=object).reshape(raw['selected3']['shape'])
    amps=[F(v) for v in c['a']];K=[[F(x) for x in row] for row in c['K_selected']]
    cubic=[sum(T[(j,)+ix]*amps[ix[0]]*amps[ix[1]]*amps[ix[2]] for ix in itertools.product(range(7),repeat=3)) for j in range(7)]
    rows=[]
    for i in range(7):
        M=sum(abs(K[i][j])*cubic[j] for j in range(7))/amps[i]
        bound=F(newresults[256]['M3'][i]);check(f'face{i+1}_exact_M3_contraction_enclosed',M<=bound)
        dm,square=decimal_query(c,i);mu=F(newresults[256]['mu'][i])
        check(f'face{i+1}_query_mu_valid_exact_squared',mu*mu*square<=F(49,64))
        check(f'face{i+1}_Decimal_query_crosscheck',abs(mu-dm)<F(1,10**60))
        er=F(newresults[256]['center_rows'][i]);exact_beta=mu*(1-er-bound/6)
        beta=F(newresults[256]['beta'][i])
        check(f'face{i+1}_beta_rounds_outward',beta<=exact_beta and exact_beta-beta<F(1,10**70))
        check(f'face{i+1}_strict_separation',2*beta>F(1,500))
        rows.append({'face':i+1,'M3':float(bound),'exact_M3_upper_rounding_excess':str(bound-M),
            'mu':float(mu),'Decimal_mu_lower':str(dm),'center_row_upper':float(er),
            'third_penalty':float(mu*bound/6),'beta':float(beta),'separation':float(2*beta),
            'M3_failure_multiplier':float(6*(1-er-F(1,1000)/mu)/bound)})
    # Sensitive entries identified in the independent hostile review.
    targets=[('HH3',(1,0,0,0)),('HS',(11,0,0))]
    sensitive=[]
    for name,ix in targets:
        new=np.load(HERE/'bounds_256.npz')[name][ix];oldv=np.load(OLD/'bounds_256.npz')[name][ix]
        sensitive.append({'array':name,'index':ix,'new':float(new),'reference':float(oldv),
                          'relative_difference':float(abs(new-oldv)/abs(oldv))})
    counts=sum(v['entries'] for v in comparisons['256']['arrays'].values())
    resources={'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.perf_counter()-start,
        'peak_ram_bytes':getattr(psutil.Process().memory_info(),'peak_wset',psutil.Process().memory_info().rss),'gpu_seconds':0}
    report={'classification':'SECOND INTERVAL IMPLEMENTATION AGREES','checks':checks,
            'compared_entries_per_precision':counts,'comparisons':comparisons,
            'precision_max_differences':{k:str(v) for k,v in precision_difference.items()},
            'faces':rows,'sensitive_entries':sensitive,'resources':resources}
    (HERE/'comparison.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'classification':report['classification'],'checks':len(checks),'entries':counts,
        'max_array_relative_difference':max(v['max_relative_nonzero'] for v in comparisons['256']['arrays'].values()),
        'max_beta_precision_difference':float(precision_difference['beta']),'faces':rows,'resources':resources},indent=2))

if __name__=='__main__': main()
