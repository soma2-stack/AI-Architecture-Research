"""Small width-extension witnesses, with real-tanh interval certificates."""
import core as c
import json,hashlib,subprocess,time
import numpy as np
import scipy.linalg as la
import mpmath as mp
from fractions import Fraction as Q
from interval import I,certify

def save_row(row):
    with (c.ROOT/'raw.jsonl').open('a') as f:f.write(json.dumps(row,allow_nan=False)+'\n')

def point(case,n,seed,meter):
    meter.check();m=c.Model(case,n);T=(m.dimension+n-1)//n;X=c.inputs(seed,T,n)
    before=m.serialize();start=time.process_time();F,J,_=c.jets(m,X);f,j=c.autograd(m,X)
    assert c.relative(F,f)<1e-8 and c.relative(J,j)<1e-10 and before==m.serialize()
    assert np.isfinite(J).all();s=la.svdvals(J)
    row={'case':case,'width':n,'depth':m.depth,'P':m.P,'N':m.N,'T':T,'input_dimension':n,
         'dimension':m.dimension,'maximum_possible_rank':min(n*T,m.dimension),'seed':seed,
         'parameters':before,'inputs':[[str(x) for x in r] for r in X],
         'F_AD_relative':c.relative(F,f),'J_AD_relative':c.relative(J,j),
         'F_AD_max_absolute':float(np.max(np.abs(np.array(F)-f))),
         'J_AD_max_absolute':float(np.max(np.abs(J-j))),
         'float64_singular_values':s.tolist(),'float64_ranks':{str(t):int(np.count_nonzero(s>s[0]*t)) for t in (1e-6,1e-8,1e-10,1e-12,1e-14)},
         'attempts':[],'certificates':[]}
    targets=[('full',list(range(m.dimension)),list(range(n*T)))]
    if case=='shared_linear':
        _,_,r=la.qr(J.T,mode='economic',pivoting=True);rr=list(map(int,r[:2*n]))
        _,_,p=la.qr(J[rr],mode='economic',pivoting=True);targets=[('rank_control',rr,list(map(int,p[:2*n])))]
    if case=='deep':
        base=list(range(m.N))+[m.N+k for k,(state,p) in enumerate(m.support) if state//n==m.meta[p][0]]
        _,_,p=la.qr(J[base],mode='economic',pivoting=True)
        targets.append(('local_base',base,list(map(int,p[:len(base)]))))
        row['base_dimension']=len(base);row['cross_dimension']=n*(2*n*n+n)
    for digits in c.CFG['mp_digits']:
        meter.check();mp.mp.dps=digits;mf,mj,_=c.jets(m,X,'mp')
        assert c.relative(J,mj)<1e-10
        for label,rr,cols in targets:
            if any(a['label']==label for a in row['certificates']):continue
            matrix=mp.matrix([[mj[i,k] for k in cols] for i in rr]);det=mp.det(matrix)
            entry={'label':label,'digits':digits,'size':len(rr),'determinant':mp.nstr(det,70)}
            try:inverse=matrix**-1
            except ZeroDivisionError:
                entry['singular_at_precision']=True;row['attempts'].append(entry);continue
            for bits in c.CFG['interval_bits']:
                meter.check();I.precision(bits);_,ivj,_=c.jets(m,X,'interval')
                minor=[[I.cast(ivj[i,k]) for k in cols] for i in rr]
                M=[[int(mp.nint(inverse[i,k]*I.scale)) for k in range(len(rr))] for i in range(len(rr))]
                proof=certify(minor,M);entry.update({'bits':bits,'verified':proof['verified'],
                         'residual_bound':str(Q(int(proof['residual_infinity_numerator']),I.scale))})
                row['attempts'].append(entry.copy())
                if proof['verified']:
                    cert={'model':case,'width':n,'seed':seed,'T':T,'params':before,'X':row['inputs'],
                          'label':label,'rows':rr,'columns':cols,'bits':bits,'mp_digits':digits,'mp_determinant':mp.nstr(det,90),
                          'preconditioner':[[str(v) for v in r] for r in M],
                          'J_intervals':[[[str(v.lo),str(v.hi)] for v in r] for r in minor],'proof':proof}
                    path=c.ROOT/f'certificate_{case}_n{n}_{seed}_{label}.json';path.write_text(json.dumps(cert))
                    row['certificates'].append({'label':label,'size':len(rr),'path':path.name,**entry})
                    print('CERTIFIED',case,n,label,len(rr),'CPU',time.process_time(),flush=True)
                    break
        if len(row['certificates'])==len(targets):
            if case in ('dense','deep'):
                meter.check()
                # High-precision spectral conditioning, diagnostic only.
                full=mp.matrix(mj.tolist());sv=mp.svd_r(full,compute_uv=False)
                row['mp_conditioning']={'digits':digits,'smallest_singular_value':mp.nstr(sv[len(sv)-1,0],70),
                    'largest_singular_value':mp.nstr(sv[0,0],70),'condition_number':mp.nstr(sv[0,0]/sv[len(sv)-1,0],70)}
            break
    row['cpu_seconds']=time.process_time()-start;save_row(row)
    print(json.dumps({k:row[k] for k in ('case','width','dimension','certificates','cpu_seconds')}),flush=True)
    return row

def main():
    meter=c.Meter('Official width scaling witnesses and interval certification');c.ACTIVE_METER=meter
    try:
        assert not (c.ROOT/'raw.jsonl').exists(),'Do not overwrite results'
        replay=json.loads((c.ROOT/'previous_replay.json').read_text());assert len(replay['certificates'])==5
        commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=c.ROOT.parents[1],text=True).strip()
        (c.ROOT/'provenance.json').write_text(json.dumps({'commit':commit,'hardware':c.hardware(),
          'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in c.ROOT.iterdir() if p.suffix in ('.py','.json','.md') and p.name not in ('provenance.json','previous_replay.json')}}))
        records=[];ok=True
        for n in (3,4):
            found=False
            for seed in c.CFG['seeds']:
                r=point('dense',n,seed,meter);records.append(r)
                if any(a['size']==r['dimension'] for a in r['certificates']):found=True;break
            ok &= found
        for n in (2,4):
            for case in ('independent','shared_linear'):
                records.append(point(case,n,c.CFG['seeds'][0],meter))
        if ok and meter.prior+time.process_time()<c.CFG['depth2_start_cpu_cutoff_seconds']:
            records.append(point('deep',3,c.CFG['seeds'][0],meter))
        result={'classification':'WIDTH SCALING — MULTI-WIDTH EVIDENCE FOUND' if ok else 'WIDTH SCALING — INCONCLUSIVE',
                'points':len(records),'arbitrary_width_proof':False,'stop':'No Stage C or AMS v10'}
        (c.ROOT/'result.json').write_text(json.dumps(result,indent=2))
    except Exception as exc:
        (c.ROOT/'failure.json').write_text(json.dumps({'error':repr(exc),'cpu_seconds':time.process_time()}));raise
    finally:meter.finish()

if __name__=='__main__':main()
