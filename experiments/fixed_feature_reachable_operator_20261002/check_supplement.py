"""Cross-check input-driven winners; no candidate generation."""
import importlib.util
import json
import time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent_check',ROOT/'crosscheck.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
r=c.r;np=c.np;la=c.la
cpu=time.process_time();wall=time.perf_counter();res=r.Resources()
records=[]
for n in (32,64,96):
    F=r.family(n)
    sel=json.loads((ROOT/f'supplement_results/finite_selection_n{n}.json').read_text())['selected']
    z=np.load(ROOT/f'supplement_results/{sel}.npz');hs=z['hs'];dh=z['modes'][0]
    expected=c.jvp(F,hs,dh)
    xp=hs.copy();xm=hs.copy();xp[1:-1,F['idx']]+=3e-6*dh;xm[1:-1,F['idx']]-=3e-6*dh
    fd=(r.operator(F,xp)-r.operator(F,xm))/(6e-6)
    err=float(la.norm(fd-expected)/max(la.norm(expected),1e-15))
    delta=np.zeros_like(hs);delta[1:-1,F['idx']]=dh
    dx=delta[1:]/(1-hs[1:]**2)-delta[:-1]@F['R'].T
    norm=float(la.norm(dx))
    cq=np.ones(n)/(n**.5*F['beta'])
    grad,endpoint=c.selected_gradient(F,hs,cq=cq)
    predicted=np.outer(z['B'].T@cq,F['Hsrc'])
    berr=float(la.norm(grad-predicted)/max(la.norm(predicted),1e-15))
    record=dict(n=n,case=sel,FD_relative_error=err,input_tangent_norm=norm,
                selected_BPTT_relative_error=berr,endpoint_roundoff=endpoint,
                passed=bool(err<1e-6 and abs(norm-1)<1e-8 and berr<1e-10))
    records.append(record)
    if not record['passed']:
        raise RuntimeError(str(record))
payload=dict(records=records,passed=all(x['passed'] for x in records),
             resources=res.snapshot(),cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-wall)
r.save_json(ROOT/'crosscheck_supplement.json',payload);res.done.set()
print(json.dumps(payload,indent=2))
