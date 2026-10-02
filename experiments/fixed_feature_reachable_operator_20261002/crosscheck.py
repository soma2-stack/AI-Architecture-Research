"""Independent numerical validation of frozen histories; not new candidates."""
import importlib.util
import json
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('runner',ROOT/'run.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
import torch
torch.set_num_threads(1)
torch.set_default_dtype(torch.float64)
np=r.np;la=r.la


def jvp(F,hs,dh):
    B=np.zeros((F['n'],F['r']));dB=np.zeros_like(B)
    for t in range(1,len(hs)):
        G=1-hs[t]**2
        pre=F['R']@B+(F['E'] if t>=2 else 0)
        perturb=np.zeros(F['n'])
        if t<=F['H']:
            perturb[F['idx']]=dh[t-1]
        dB=G[:,None]*(F['R']@dB)+(-2*hs[t]*perturb)[:,None]*pre
        B=G[:,None]*pre
    return dB


def selected_gradient(F,hs,vfuture=None,cq=None):
    R=torch.tensor(F['R'],requires_grad=True);initial=R.detach().clone()
    h=torch.zeros(F['n'])
    for x in r.realize(F,hs):
        h=torch.tanh(R@h+torch.tensor(x)+.05)
    endpoint=float(h.detach().norm())
    if vfuture is not None:
        h=torch.tanh(R@h+torch.tensor(vfuture)+.05)
        loss=h.sum()/(F['beta']*r.math.sqrt(F['n']))
    else:
        loss=torch.tensor(cq)@h
    grad=torch.autograd.grad(loss,R)[0].detach().numpy()
    assert torch.equal(initial,R.detach()) and not R.is_cuda
    return grad[np.ix_(F['idx'],np.arange(F['k'],F['n']))],endpoint


def main():
    cpu=time.process_time();wall=time.perf_counter();resources=r.Resources()
    rows=[]
    for n in r.CFG['widths']:
        F=r.family(n)
        selection=json.loads((ROOT/f'results/finite_selection_n{n}.json').read_text())
        z=np.load(ROOT/f"results/{selection['selected']}.npz")
        hs=z['hs'];dh=z['modes'][0]
        actual=jvp(F,hs,dh)
        errors=[]
        for step in (1e-5,3e-6):
            hp=hs.copy();hm=hs.copy();hp[1:-1,F['idx']]+=step*dh;hm[1:-1,F['idx']]-=step*dh
            fd=(r.operator(F,hp)-r.operator(F,hm))/(2*step)
            errors.append(float(la.norm(fd-actual)/max(la.norm(actual),1e-15)))
        delta=np.zeros_like(hs);delta[1:-1,F['idx']]=dh
        dx=delta[1:]/(1-hs[1:]**2)-delta[:-1]@F['R'].T
        whiten=float(la.norm(dx))
        projected=actual[F['idx']]
        score=float(la.norm(F['root']@projected,'fro'))
        spectrum=float(z['lower_spectrum'][0])
        metric_replay=abs(score-spectrum)/max(spectrum,1e-15)
        cq=np.ones(n)/(n**.5*F['beta'])
        grad,endpoint=selected_gradient(F,hs,cq=cq)
        prediction=np.outer(z['B'].T@cq,F['Hsrc'])
        bptt=float(la.norm(grad-prediction)/max(la.norm(prediction),1e-15))
        # Direct actual future loss at a noninfinitesimal fixed-h pair.
        hp=hs.copy();hm=hs.copy();hp[1:-1,F['idx']]+=.05*dh;hm[1:-1,F['idx']]-=.05*dh
        assert r.admissible(F,hp) and r.admissible(F,hm)
        D=r.operator(F,hp)-r.operator(F,hm)
        met,g=r.metric(F,D,n)
        vf=np.arccosh(1/np.sqrt(g))-.05
        gp,ep=selected_gradient(F,hp,vfuture=vf);gm,em=selected_gradient(F,hm,vfuture=vf)
        observed=F['wR']*la.norm(gp-gm,'fro')
        future_error=abs(observed-met['box_search_lower'])/max(observed,1e-15)
        record=dict(n=n,case=selection['selected'],fd_relative_errors=errors,
                    physical_input_tangent_norm=whiten,spectrum_replay_relative_error=metric_replay,
                    selected_BPTT_relative_error=bptt,actual_future_gradient_distance=float(observed),
                    future_query_replay_relative_error=float(future_error),
                    future_input_min=float(vf.min()),future_input_max=float(vf.max()),
                    endpoint_roundoff=max(endpoint,ep,em))
        record['passed']=bool(max(errors)<1e-6 and abs(whiten-1)<1e-8 and metric_replay<1e-8 and bptt<1e-10 and future_error<1e-9)
        rows.append(record)
        print(json.dumps(record),flush=True)
        if not record['passed']:
            raise RuntimeError('Crosscheck failure')
    manifest=json.loads((ROOT/'FROZEN.json').read_text())
    unchanged=all(r.sha(r.REPO/name)==value for name,value in manifest['inputs'].items())
    payload=dict(rows=rows,frozen_inputs_unchanged=unchanged,resources=resources.snapshot(),
                 cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall,passed=unchanged and all(x['passed'] for x in rows))
    r.save_json(ROOT/'crosscheck.json',payload);resources.done.set()


if __name__=='__main__':
    main()
