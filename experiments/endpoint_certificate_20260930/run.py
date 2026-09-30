"""Endpoint mixed-derivative audit and exact rational interval certificates."""
import core as c
import hashlib
import json
import subprocess
import time
from fractions import Fraction as Q
import numpy as np
import scipy.linalg as la
import mpmath as mp
from interval import I,certify

def append(row):
    with (c.ROOT/'raw.jsonl').open('a') as f:f.write(json.dumps(row,allow_nan=False)+'\n')
def submatrix(J,rows,cols):return [[J[i,j] for j in cols] for i in rows]
def indices(matrix,size):
    _,_,r=la.qr(matrix.T,mode='economic',pivoting=True);rows=list(map(int,r[:size]))
    _,_,p=la.qr(matrix[rows],mode='economic',pivoting=True);cols=list(map(int,p[:size]))
    return rows,cols

def point(case,seed,meter):
    meter.check();model=c.Model(case);cfg=c.CFG['cases'][case];T=cfg['T'];X=c.inputs(seed,T)
    before=model.serialize();start=time.process_time();F,J,S=c.jets(model,X)
    f,j=c.autograd(model,X);assert c.relative(F,f)<1e-8 and c.relative(J,j)<1e-10
    assert np.isfinite(J).all() and model.serialize()==before
    singular=la.svdvals(J)
    ranks={str(t):int(np.count_nonzero(singular>singular[0]*t)) for t in c.CFG['float_rank_cutoffs']}
    row={'case':case,'seed':seed,'width':2,'depth':model.depth,'P':model.P,'input_dimension':2,'T':T,
         'dimension':model.dimension,'input_history_dimension':2*T,'maximum_possible_rank':min(2*T,model.dimension),
         'params':model.serialize(),'inputs':[[str(v) for v in r] for r in X],
         'RTRL_BPTT_endpoint_relative':c.relative(F,f),'endpoint_J_autograd_relative':c.relative(J,j),
         'float64_singular_values':singular.tolist(),'float64_ranks':ranks,'attempts':[],'certificates':[]}
    targets=[('full',list(range(model.dimension)),list(range(2*T)))]
    if case=='shared_linear':
        rows,cols=indices(J,4);targets=[('shared_rank4',rows,cols)]
    if case=='deep':
        base_rows=list(range(model.N))+[model.N+i for i,(state,p) in enumerate(model.support) if state//2==model.meta[p][0]]
        _,_,permutation=la.qr(J[base_rows],mode='economic',pivoting=True)
        targets.append(('local_base',base_rows,list(map(int,permutation[:len(base_rows)]))))
        row['base_dimension']=len(base_rows);row['cross_coordinates']=20
    for digits in c.CFG['mp_digits']:
        meter.check();mp.mp.dps=digits;mpF,mpJ,_=c.jets(model,X,'mp')
        assert c.relative(J,mpJ)<1e-10
        for label,rows,cols in targets:
            if any(cert['label']==label for cert in row['certificates']):continue
            matrix=mp.matrix(submatrix(mpJ,rows,cols));det=mp.det(matrix)
            entry={'label':label,'decimal_digits':digits,'minor_size':len(rows),'determinant':mp.nstr(det,50)}
            try:inverse=matrix**-1
            except ZeroDivisionError:
                entry['inverse_failed']=True;row['attempts'].append(entry);continue
            for bits in c.CFG['interval_bits']:
                meter.check();I.precision(bits);_,ivJ,_=c.jets(model,X,'interval');minor=submatrix(ivJ,rows,cols)
                pre=[[int(mp.nint(inverse[i,k]*I.scale)) for k in range(len(rows))] for i in range(len(rows))]
                proof=certify(minor,pre)
                entry['interval_bits']=bits;entry['residual_infinity_bound']=str(Q(int(proof['residual_infinity_numerator']),I.scale))
                entry['verified']=proof['verified'];row['attempts'].append(entry.copy())
                if proof['verified']:
                    certificate={'model':case,'seed':seed,'T':T,'params':before,'X':row['inputs'],'label':label,'rows':rows,'columns':cols,
                                 'bits':bits,'mp_digits':digits,'mp_determinant':mp.nstr(det,70),
                                 'preconditioner':[[str(v) for v in rr] for rr in pre],
                                 'J_intervals':[[[str(I.cast(v).lo),str(I.cast(v).hi)] for v in rr] for rr in minor],
                                 'proof':proof,'mathematical_conclusion':f'Selected {len(rows)} by {len(rows)} minor is nonzero'}
                    path=c.ROOT/f'certificate_{case}_{seed}_{label}.json';path.write_text(json.dumps(certificate,indent=2))
                    row['certificates'].append({'label':label,'size':len(rows),'path':path.name,'bits':bits,'mp_digits':digits,
                                                'residual_bound':entry['residual_infinity_bound']})
                    break
        if len(row['certificates'])==len(targets):break
    row['cpu_seconds']=time.process_time()-start;append(row);print(json.dumps({k:row[k] for k in ('case','seed','dimension','float64_ranks','certificates','cpu_seconds')}),flush=True)
    return row

def main():
    meter=c.Meter('Endpoint official witnesses and interval certification')
    try:
        assert not (c.ROOT/'raw.jsonl').exists(),'Refuse overwrite'
        hardware=c.hardware();commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=c.ROOT.parents[1],text=True).strip()
        (c.ROOT/'provenance.json').write_text(json.dumps({'hardware':hardware,'commit':commit,
          'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in c.ROOT.glob('*.py')},
          'config_sha256':hashlib.sha256((c.ROOT/'config.json').read_bytes()).hexdigest()},indent=2))
        rows=[point(case,c.CFG['seeds'][0],meter) for case in ('independent','shared_linear')]
        assert any(cert['size']==10 for cert in rows[0]['certificates']),'Independent positive control did not certify'
        assert any(cert['size']==4 for cert in rows[1]['certificates']),'Shared-linear positive control did not certify'
        witness=False
        for seed in c.CFG['seeds']:
            r=point('dense',seed,meter);rows.append(r)
            if any(cert['size']==22 for cert in r['certificates']):witness=True;break
        if witness:
            for seed in c.CFG['seeds']:
                r=point('deep',seed,meter);rows.append(r)
                if any(cert['size']==64 for cert in r['certificates']):break
        classification='ENDPOINT CERTIFICATE — FULL-DIMENSION WITNESS FOUND' if witness else 'ENDPOINT CERTIFICATE — INCONCLUSIVE'
        (c.ROOT/'result.json').write_text(json.dumps({'classification':classification,'dense_witness':witness,'points':len(rows),
                                                   'controls_valid':True,'stop':'No Stage C or AMS v10'},indent=2))
    except Exception as exc:
        (c.ROOT/'failure.json').write_text(json.dumps({'error':repr(exc),'classification':'ENDPOINT CERTIFICATE — INCONCLUSIVE'}));raise
    finally:meter.finish()

if __name__=='__main__':main()
