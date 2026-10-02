"""Independent autograd and direct-SVD cross-checks; no new official histories."""
import full_history as fh
import run as core
import torch
import numpy as np
import scipy.linalg as la
import time
import json
import psutil

def main():
    start_c,start_w=time.process_time(),time.perf_counter()
    torch.set_num_threads(1)
    torch.set_default_dtype(torch.float64)
    # Tiny development-only graph: independently differentiate BPTT twice.
    F=core.family(8); F.update(H=6,T=7)
    hs,_,_=core.histories(F,'random_pulse',11003)
    K,Q,chols,subs=fh.full_chart(F,hs)
    n,H=F['n'],F['H']; P=2*n*n+n
    weights=torch.tensor([F['wR']]*(n*n)+[F['wW']]*(n*n)+[F['wb']]*n)
    theta=torch.tensor(np.concatenate([F['R'].ravel(),np.eye(n).ravel(),np.full(n,.05)]),requires_grad=True)
    physical_R=torch.tensor(F['R']); qroot=torch.tensor(Q)
    def endpoint_sensitivity(free):
        allh=torch.cat([torch.zeros((1,n)),free.reshape(H,n),torch.zeros((1,n))])
        xs=torch.atanh(allh[1:])-allh[:-1]@physical_R.T-.05
        def forward(th):
            R=th[:n*n].reshape(n,n); W=th[n*n:2*n*n].reshape(n,n); b=th[2*n*n:]
            h=torch.zeros(n)
            for x in xs: h=torch.tanh(R@h+W@x+b)
            return h
        S=torch.autograd.functional.jacobian(forward,theta,create_graph=True,vectorize=True)*weights
        return (qroot@S).ravel()
    free=torch.tensor(hs[1:-1].ravel(),requires_grad=True)
    independent=torch.autograd.functional.jacobian(endpoint_sensitivity,free,vectorize=True).detach().numpy()
    L=np.zeros((n*H,n*H))
    for t in range(H):
        L[t*n:(t+1)*n,t*n:(t+1)*n]=chols[t]
        if t: L[t*n:(t+1)*n,(t-1)*n:t*n]=subs[t]
    raw=K@L.T
    relative=float(la.norm(raw-independent)/la.norm(independent))
    absolute=float(np.max(np.abs(raw-independent)))
    if relative>1e-9: raise RuntimeError('Independent nested-autograd Jacobian disagreement')
    # Recompute one saved complete case; compare direct singular values to Gram.
    record=json.loads((fh.ROOT/'full_history_results/n012_diffuse_s73101.json').read_text())
    history=np.load(fh.ROOT/'full_history_results/n012_diffuse_s73101_history.npz')['hidden_states']
    model=core.family(12)
    matrix,_,_,_=fh.full_chart(model,history)
    direct=la.svdvals(matrix)
    saved=np.load(fh.ROOT/'full_history_results/n012_diffuse_s73101_spectra.npz')['box_rms']
    above=direct>.001
    diff=float(np.max(np.abs(direct[above]-saved[above])))
    if int(np.count_nonzero(above))!=record['visible_count'] or diff>1e-9:
        raise RuntimeError('Direct SVD threshold/count disagreement')
    result=dict(autograd_development_n=8,autograd_development_H=6,autograd_seed=11003,
                nested_BPTT_endpoint_jacobian_relative_error=relative,max_absolute_error=absolute,
                complete_n12_direct_svd_visible_count=int(np.count_nonzero(above)),
                complete_n12_direct_svd_max_above_epsilon_difference=diff,
                cpu_only=theta.device.type=='cpu' and free.device.type=='cpu',
                torch_version=torch.__version__,cuda_runtime=torch.version.cuda,gpu_seconds=0,
                cpu_seconds=time.process_time()-start_c,wall_seconds=time.perf_counter()-start_w,
                peak_working_set_bytes=psutil.Process().memory_info().peak_wset)
    destination=fh.ROOT/'analysis/independent_numerical_checks.json'
    if destination.exists(): raise RuntimeError('Refusing to overwrite checks')
    destination.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
