"""Reachable fixed-feature numerical diagnostic. No training or certificates."""
import os
for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[key] = '4'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
import argparse
import hashlib
import importlib.util
import json
import math
import threading
import time
from pathlib import Path
import numpy as np
import scipy.linalg as la
import psutil

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
CFG = json.loads((ROOT/'config.json').read_text())
OLD = REPO/'experiments/aperiodic_gate_spectrum_20261001'
spec = importlib.util.spec_from_file_location('archived_diagnostic', OLD/'run.py')
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)


def save_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Resources:
    def __init__(self):
        self.cpu = time.process_time()
        self.wall = time.perf_counter()
        self.peak = 0
        self.done = threading.Event()
        threading.Thread(target=self.monitor, daemon=True).start()

    def monitor(self):
        while not self.done.wait(.2):
            self.peak = max(self.peak, psutil.Process().memory_info().rss)

    def snapshot(self):
        self.peak = max(self.peak, psutil.Process().memory_info().rss)
        return dict(cpu_seconds=time.process_time()-self.cpu,
                    wall_seconds=time.perf_counter()-self.wall,
                    peak_rss_bytes=self.peak, gpu_seconds=0, device='cpu')

    def check(self):
        z = self.snapshot()
        if (z['cpu_seconds'] > CFG['process_cpu_cap_seconds']-90 or
            z['wall_seconds'] > CFG['wall_cap_seconds']-45 or
            z['peak_rss_bytes'] > CFG['rss_cap_bytes'] or
            psutil.virtual_memory().available < 4*1024**3):
            raise RuntimeError('RESOURCE STOP '+str(z))


def family(n, development=False):
    F = old.family(n)
    if not development:
        z = np.load(OLD/f'results/model_n{n}.npz')
        for key in ('R', 'R0', 'O'):
            if not np.allclose(F[key], z[key], rtol=0, atol=1e-14):
                raise RuntimeError('Archived model mismatch')
            F[key] = z[key].copy()
    F['r'] = F['k']-1
    F['idx'] = np.arange(1, F['k'])
    F['E'] = np.eye(n)[:, F['idx']]
    F['Hsrc'] = CFG['source_amplitude']*np.ones(F['l'])
    F['beta'] = max(1., la.norm(F['R'], 'fro'))
    F['wR'] = la.norm(F['R'], 'fro')/n
    F['kappa'] = F['a']/F['beta']
    F['scale'] = F['wR']*la.norm(F['Hsrc'])
    lo, hi = 1/math.cosh(.5)**2, 1/math.cosh(.25)**2
    mid, sg = (lo+hi)/2, (hi-lo)/2
    F['lo'], F['hi'] = lo, hi
    F['Q'] = F['R'].T@(sg*sg*np.eye(n)+mid*mid*np.ones((n,n)))@F['R']/(F['beta']**2*n)
    qe = F['E'].T@F['Q']@F['E']
    vals, vecs = la.eigh(qe)
    F['root'] = (vecs*np.sqrt(np.maximum(vals, 0)))@vecs.T*F['scale']
    return F


def realize(F, hs):
    if np.max(np.abs(hs)) >= 1:
        return None
    return np.arctanh(hs[1:])-hs[:-1]@F['R'].T-.05


def admissible(F, hs):
    xs = realize(F, hs)
    return xs is not None and np.max(np.abs(xs)) < .5


def generate(F, strategy, seed):
    rng = np.random.default_rng(np.random.SeedSequence([seed, F['n'], ['random','sparse','dense'].index(strategy)]))
    H, r = F['H'], F['r']
    mem = np.zeros((H, r))
    if strategy == 'random':
        mem = rng.uniform(-CFG['random_amplitude'], CFG['random_amplitude'], (H, r))
    elif strategy == 'sparse':
        active = rng.uniform(size=H)<.5
        coords = rng.integers(r, size=H)
        mem[np.arange(H), coords] = active*CFG['pulse_amplitude']*rng.uniform(.5,1,H)*rng.choice([-1.,1.],H)
    else:
        mem = CFG['dense_amplitude']*rng.uniform(.1,1,(H,r))*rng.uniform(.4,1,(H,1))
    hs = np.zeros((H+2,F['n']))
    hs[1:-1,F['k']:] = F['Hsrc']
    hs[1:-1, F['idx']] = mem
    return shrink(F, hs)


def shrink(F, hs):
    hs = hs.copy()
    shrink = 1.
    for _ in range(100):
        xs = realize(F, hs)
        if xs is not None and np.max(np.abs(xs)) <= CFG['generation_input_cap']:
            return hs, shrink
        hs[1:-1,F['idx']] *= CFG['generation_shrink']
        shrink *= CFG['generation_shrink']
    raise RuntimeError('Generator failed admissibility')


def history_info(F, hs):
    xs = realize(F, hs)
    gates = 1-hs[1:-1,F['idx']]**2
    words = [np.round(g,14).tobytes() for g in gates]
    prefix = np.zeros(len(words), dtype=int)
    for t in range(1,len(words)):
        p = prefix[t-1]
        while p and words[t]!=words[p]:
            p = prefix[p-1]
        if words[t]==words[p]:
            p += 1
        prefix[t] = p
    period = len(words)-int(prefix[-1])
    spread = float(np.max(np.ptp(gates,axis=1)))
    comm = max(la.norm(g[:,None]*F['O'][1:,1:]-F['O'][1:,1:]*g[None,:],'fro') for g in gates)
    if period <= len(words)//2 or spread <= 1e-12 or comm <= 1e-12:
        raise RuntimeError('History is not aperiodic/non-scalar/noncommuting')
    h = np.zeros(F['n'])
    for x in xs:
        h = np.tanh(F['R']@h+x+.05)
    if la.norm(h)>1e-10 or not np.array_equal(hs[-1],np.zeros(F['n'])):
        raise RuntimeError('Fixed-h realization failed')
    return dict(max_abs_input=float(np.max(np.abs(xs))), endpoint_roundoff=float(la.norm(h)),
                minimum_word_period=period, gate_spread=spread, gate_rotation_commutator=float(comm),
                mean_gate_damage=float(np.mean(1-gates)),
                history_sha256=hashlib.sha256(hs.tobytes()).hexdigest())


def operator(F, hs, trajectory=False):
    B = np.zeros((F['n'],F['r']))
    states = [B.copy()] if trajectory else None
    for t in range(1,len(hs)):
        B = (1-hs[t]**2)[:,None]*(F['R']@B+(F['E'] if t>=2 else 0))
        if trajectory:
            states.append(B.copy())
    return np.array(states) if trajectory else B


def metric(F, D, seed=1):
    # Numerical permitted-corner LOWER, analytic all-continuation UPPER.
    Y = F['scale']*F['R']@D/(F['beta']*math.sqrt(F['n']))
    gram = Y@Y.T
    rng = np.random.default_rng(seed)
    best, best_g = -1., None
    for restart in range(CFG['query_restarts']):
        g = (np.full(F['n'], F['hi']) if restart==0 else np.full(F['n'],F['lo']) if restart==1
             else np.where(rng.integers(2,size=F['n']),F['hi'],F['lo']))
        product = gram@g
        for _ in range(10):
            changes = 0
            for j in range(F['n']):
                target = F['hi'] if g[j]==F['lo'] else F['lo']
                diff = target-g[j]
                if 2*diff*product[j]+diff*diff*gram[j,j]>1e-24:
                    product += diff*gram[:,j]
                    g[j] = target
                    changes += 1
            if not changes:
                break
        value = max(float(g@gram@g),0)
        if value>best:
            best,best_g=value,g.copy()
    rms = F['scale']*math.sqrt(max(float(np.trace(D.T@F['Q']@D)),0))
    upper = F['kappa']*F['scale']*la.svdvals(D)[0]
    lower = math.sqrt(best)
    if lower>upper*(1+1e-9)+1e-12:
        raise RuntimeError('Query envelope violated')
    return dict(box_search_lower=lower,box_rms_lower=rms,all_future_upper=float(upper)),best_g


def input_cholesky(F, hs):
    H,r,idx=F['H'],F['r'],F['idx']
    D=1/(1-hs[1:-1,idx]**2)
    RE=F['R'][:,idx]
    diagR=RE.T@RE
    Rmem=RE[idx]
    bw=2*r-1
    band=np.zeros((bw+1,H*r))
    for t in range(H):
        block=diagR+np.diag(D[t]**2)
        for j in range(r):
            band[:r-j,t*r+j]=block[j:,j]
        if t<H-1:
            cross=-D[t+1,:,None]*Rmem
            for j in range(r):
                offsets=r+np.arange(r)-j
                band[offsets,t*r+j]=cross[:,j]
    return la.cholesky_banded(band,lower=True),bw


def transpose_band(L,bw):
    ans=np.zeros_like(L)
    for b in range(bw+1):
        ans[bw-b,b:]=L[b,:L.shape[1]-b]
    return ans


def history_direction(L,bw,v,F):
    return la.solve_banded((0,bw),transpose_band(L,bw),v).reshape(F['H'],F['r'])


def jacobian(F,hs):
    states=operator(F,hs,True)
    H,r,idx=F['H'],F['r'],F['idx']
    J=np.empty((r*r,H*r),order='F')
    tail=np.eye(F['n'])
    outside=np.setdiff1d(np.arange(F['n']),idx)
    leakage_squared=0.
    for t in range(H+1,0,-1):
        if t<=H:
            V=F['R']@states[t-1]+(F['E'] if t>=2 else 0)
            right=-2*hs[t,idx,None]*V[idx]
            left=tail[np.ix_(idx,idx)]
            block=np.einsum('ai,ib->abi',left,right).reshape(r*r,r)
            J[:,(t-1)*r:t*r]=block
            leakage_squared += float(np.sum(np.sum(tail[np.ix_(outside,idx)]**2,axis=0)*np.sum(right**2,axis=1)))
        tail=(tail*(1-hs[t]**2)[None,:])@F['R']
    return J, math.sqrt(leakage_squared), states[-1]


def spectrum(F,hs,case,outdir,res):
    start=time.process_time()
    J,leak,B=jacobian(F,hs)
    L,bw=input_cholesky(F,hs)
    J=la.solve_banded((bw,0),L,J.T,overwrite_b=False,check_finite=False).T.copy(order='C')
    res.check()
    gram=J@J.T
    vu,uu=la.eigh(gram,driver='evd',check_finite=False)
    raw=np.sqrt(np.maximum(vu[::-1],0))
    uu=uu[:,::-1]
    r=F['r']
    qgram=np.einsum('ai,ijkl,bk->ajbl',F['root'],gram.reshape(r,r,r,r),F['root'],optimize=True).reshape(r*r,r*r)
    vq,uq=la.eigh(qgram,driver='evd',check_finite=False)
    sq=np.sqrt(np.maximum(vq[::-1],0));uq=uq[:,::-1]
    upper=raw*F['kappa']*F['scale']
    leak_bound=F['kappa']*F['scale']*F['n']*leak
    count=int(np.sum(sq-leak_bound>CFG['epsilon']))
    upper_count=int(np.sum(upper+leak_bound>CFG['epsilon']))
    cap=min(CFG['finite_axis_cap'],2*F['n'],len(sq))
    modes=[]
    for j in range(cap):
        y=(F['root'].T@uq[:,j].reshape(r,r)).ravel()
        v=J.T@y/max(sq[j],1e-300)
        modes.append(history_direction(L,bw,v,F))
    upper_modes=[]
    for j in range(min(8,len(raw))):
        v=J.T@uu[:,j]/max(raw[j],1e-300)
        upper_modes.append(history_direction(L,bw,v,F))
    eigen_roundoff=max(0.,float(-min(vu[0],vq[0])))
    info=history_info(F,hs)
    info.update(case=case,n=F['n'],r=r,H=F['H'],T=F['T'],
                lower_tangent_count=count,upper_envelope_count=upper_count,
                count_over_n=count/F['n'],count_over_nlogn=count/(F['n']*math.log(F['n'])),
                count_over_n15=count/F['n']**1.5,count_over_n2=count/F['n']**2,
                lower_radius005_count=int(np.sum(.05*(sq-leak_bound)>CFG['epsilon'])),
                lower_radius025_count=int(np.sum(.25*(sq-leak_bound)>CFG['epsilon'])),
                ranking_score=float(np.log1p((sq/CFG['epsilon'])**2).sum()),
                leading_lower=float(sq[0]),leading_upper=float(upper[0]),
                stable_rank=float((sq@sq)/max(sq[0]**2,1e-300)),
                tangent_leakage_query_bound=leak_bound,gram_negative_eigenvalue=eigen_roundoff,
                below_epsilon_energy=float(np.sum(sq[sq<=CFG['epsilon']]**2)/max(sq@sq,1e-300)),
                cpu_seconds=time.process_time()-start)
    # Keep full spectra, selected tangent charts, actual operator and inputs.
    np.savez_compressed(outdir/f'{case}.npz',hs=hs,xs=realize(F,hs),B=B,
                        lower_spectrum=sq,upper_spectrum=upper,
                        modes=np.array(modes),upper_modes=np.array(upper_modes))
    save_json(outdir/f'{case}.json',info)
    print(json.dumps(info),flush=True)
    return info,B


def novelty(F,bases,res):
    best_score=-1;winner=None
    traces=[]
    def score(hs):
        B=operator(F,hs)
        return min(F['scale']*math.sqrt(max(float(np.trace((B-b).T@F['Q']@(B-b))),0)) for b in bases)
    for j in range(CFG['novelty_candidates']):
        res.check()
        hs,sh=generate(F,CFG['strategies'][j%3],CFG['novelty_seed']+j)
        s=score(hs)
        traces.append(dict(stage='pool',index=j,score=s,shrink=sh))
        if s>best_score:
            best_score,winner=s,hs
    rng=np.random.default_rng(np.random.SeedSequence([CFG['novelty_seed'],F['n'],111]))
    for j in range(CFG['novelty_mutations']):
        res.check()
        candidate=winner.copy()
        if j%2:
            other,_=generate(F,CFG['strategies'][j%3],CFG['novelty_seed']+1000+j)
            candidate[1:-1,F['idx']]=.7*candidate[1:-1,F['idx']]+.3*other[1:-1,F['idx']]
        else:
            i=int(rng.integers(F['r']));begin=int(rng.integers(1,F['H']+1))
            end=min(F['H']+1,begin+int(rng.integers(1,max(2,F['n']))))
            candidate[begin:end,F['idx'][i]]=rng.uniform(-.22,.22)
        candidate,sh=shrink(F,candidate)
        s=score(candidate)
        traces.append(dict(stage='mutation',index=j,score=s,shrink=sh))
        if s>best_score:
            best_score,winner=s,candidate
    return winner,traces


def finite_check(F,row,outdir,res):
    z=np.load(outdir/f"{row['case']}.npz")
    hs=z['hs'];B=z['B'];modes=z['modes'];upper_modes=z['upper_modes']
    records=[];queries=[]
    def check(dh,radius,kind,index):
        hp=hs.copy();hm=hs.copy()
        hp[1:-1,F['idx']]+=radius*dh
        hm[1:-1,F['idx']]-=radius*dh
        rec=dict(kind=kind,index=index,radius=radius,admissible=admissible(F,hp) and admissible(F,hm))
        if not rec['admissible']:
            return rec
        dp=operator(F,hp);dm=operator(F,hm)
        met,g=metric(F,dp-dm,CFG['novelty_seed']+index)
        rec.update(met)
        rec['passes_numerically']=met['box_search_lower']>2*CFG['epsilon']
        rec['fails_even_envelope']=met['all_future_upper']<=2*CFG['epsilon']
        rec['physical_antipode_input_distance']=float(la.norm(realize(F,hp)-realize(F,hm)))
        linear=2*radius*dh
        # Operator curvature diagnostic through symmetric secant midpoint.
        rec['midpoint_nonlinearity_ratio']=float(la.norm(dp+dm-2*B,'fro')/max(la.norm(dp-dm,'fro'),1e-300))
        queries.append(g)
        return rec
    for radius in CFG['finite_radii']:
        for kind,bank in [('lower_axis',modes),('upper_axis',upper_modes)]:
            for j,dh in enumerate(bank):
                res.check();records.append(check(dh,radius,kind,j))
        size=min(row['lower_tangent_count'],32,len(modes))
        if size:
            rng=np.random.default_rng(np.random.SeedSequence([CFG['novelty_seed'],F['n'],int(radius*1000)]))
            for j in range(CFG['joint_samples']):
                res.check()
                coef=rng.normal(size=size);coef/=la.norm(coef)
                records.append(check(np.einsum('i,itj->tj',coef,modes[:size]),radius,'joint_sphere',j))
    save_json(outdir/f"finite_{F['n']}.json",dict(selected_case=row['case'],joint_dimension_tested=min(row['lower_tangent_count'],32),records=records))
    np.savez_compressed(outdir/f"finite_queries_{F['n']}.npz",gates=np.array(queries))
    return dict(n=F['n'],selected_case=row['case'],radii=[dict(radius=a,
                lower_axes_tested=sum(x['kind']=='lower_axis' and x['radius']==a for x in records),
                admissible_axes=sum(x['kind']=='lower_axis' and x['radius']==a and x['admissible'] for x in records),
                passing_axes=sum(x['kind']=='lower_axis' and x['radius']==a and x.get('passes_numerically',False) for x in records),
                envelope_failing_axes=sum(x['kind']=='lower_axis' and x['radius']==a and x.get('fails_even_envelope',False) for x in records),
                sampled_joint_min=min([x['box_search_lower'] for x in records if x['kind']=='joint_sphere' and x['radius']==a and x['admissible']] or [0]),
                sampled_joint_admissible=sum(x['kind']=='joint_sphere' and x['radius']==a and x['admissible'] for x in records)) for a in CFG['finite_radii']])


def development():
    F=family(8,True);F['H']=12;F['T']=13
    hs,_=generate(F,'random',CFG['development_seed'])
    J,leak,B=jacobian(F,hs);L,bw=input_cholesky(F,hs)
    rng=np.random.default_rng(CFG['development_seed'])
    v=rng.normal(size=F['H']*F['r']);v/=la.norm(v)
    dh=history_direction(L,bw,v,F)
    xp=hs.copy();xm=hs.copy();xp[1:-1,F['idx']]+=1e-6*dh;xm[1:-1,F['idx']]-=1e-6*dh
    fd=(operator(F,xp)-operator(F,xm))/(2e-6)
    analytic=(J@dh.ravel()).reshape(F['r'],F['r'])
    ferr=float(la.norm(fd[F['idx']]-analytic)/max(la.norm(analytic),1e-15))
    dx=(realize(F,xp)-realize(F,xm))/(2e-6)
    input_norm=float(la.norm(dx))
    import torch
    torch.set_num_threads(1);torch.set_default_dtype(torch.float64)
    R=torch.tensor(F['R'],requires_grad=True);before=R.detach().clone()
    h=torch.zeros(F['n'])
    for x in realize(F,hs):
        h=torch.tanh(R@h+torch.tensor(x)+.05)
    cq=rng.normal(size=F['n'])
    grad=torch.autograd.grad(torch.tensor(cq)@h,R)[0].detach().numpy()
    selected=grad[np.ix_(F['idx'],np.arange(F['k'],F['n']))]
    predicted=np.outer(B.T@cq,F['Hsrc'])
    berr=float(la.norm(selected-predicted)/max(la.norm(predicted),1e-15))
    met,g=metric(F,fd)
    passed=ferr<1e-7 and abs(input_norm-1)<1e-8 and berr<1e-11 and torch.equal(before,R.detach()) and not R.is_cuda
    record=dict(development_only=True,fd_relative_error=ferr,input_tangent_norm=input_norm,
                selected_BPTT_relative_error=berr,forward_endpoint_norm=float(h.detach().norm()),
                query_bounds=met,parameters_unchanged=torch.equal(before,R.detach()),cpu_only=not R.is_cuda,passed=passed)
    save_json(ROOT/'development_validation.json',record)
    if not passed:
        raise RuntimeError('Development validity failed '+str(record))
    print(json.dumps(record),flush=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--development',action='store_true');args=ap.parse_args()
    if args.development:
        development();return
    manifest=json.loads((ROOT/'FROZEN.json').read_text())
    for name,value in manifest['inputs'].items():
        if sha(REPO/name)!=value:
            raise RuntimeError('Frozen source changed '+name)
    outdir=ROOT/'results';outdir.mkdir(exist_ok=False)
    res=Resources();rows=[];finite=[];status='RUNNING'
    try:
        for n in CFG['widths']:
            F=family(n);bases=[];width_rows=[]
            for strategy in CFG['strategies']:
                for seed in CFG['seeds']:
                    res.check();hs,sh=generate(F,strategy,seed)
                    case=f'n{n}_{strategy}_{seed}'
                    info,B=spectrum(F,hs,case,outdir,res)
                    info.update(strategy=strategy,seed=seed,generator_shrink=sh)
                    rows.append(info);width_rows.append(info);bases.append(B)
                    save_json(outdir/'summary.json',dict(status=status,rows=rows,finite=finite,resources=res.snapshot()))
            hs,traces=novelty(F,bases,res)
            save_json(outdir/f'novelty_n{n}.json',traces)
            info,B=spectrum(F,hs,f'n{n}_novelty',outdir,res)
            info.update(strategy='novelty',seed=CFG['novelty_seed'])
            rows.append(info);width_rows.append(info)
            selected=sorted(width_rows,key=lambda x:(-x['lower_tangent_count'],-x['ranking_score'],x['case']))[0]
            save_json(outdir/f'finite_selection_n{n}.json',dict(selected=selected['case'],history_sha256=selected['history_sha256'],rule='lower count, log score, lexical'))
            finite.append(finite_check(F,selected,outdir,res))
            save_json(outdir/'summary.json',dict(status=status,rows=rows,finite=finite,resources=res.snapshot()))
        status='COMPLETE'
    except Exception as exc:
        status='STOPPED';save_json(outdir/'stop.json',dict(error=repr(exc),resources=res.snapshot()))
        raise
    finally:
        save_json(outdir/'summary.json',dict(status=status,rows=rows,finite=finite,resources=res.snapshot()))
        res.done.set()


if __name__=='__main__':
    main()
