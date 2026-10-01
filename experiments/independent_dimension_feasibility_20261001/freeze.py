"""Generate deterministic bases and freeze before the requested-dimensional screen."""
import numerics as n
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,time,subprocess
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    st=time.perf_counter();cpu=time.process_time();m=n.Model();bases,s=m.bases()
    # Validation is 7D calibration and analytic/numerical consistency only.
    B=m.oldB;_,_,Jh,Js=m.forward(np.zeros(11),B)
    A=Js[:,4:]-Js[:,:4]@np.linalg.solve(Jh[:,:4],Jh[:,4:])
    ch={'B':B,'Jh':Jh,'Js':Js,'Q':m.oldQ,'A':A}
    old=n.proxy(m,ch,n.vector(m.c['a']),float(F(m.c['ah'])))
    expected=json.loads((ROOT/'experiments/cleanroom_7d_interval_20261001/result_256.json').read_text(encoding='utf-8'))
    wanted=n.vector(expected['beta']);error=float(np.max(abs(np.array(old['beta'])-wanted)))
    if not old['valid'] or error>1e-10:raise RuntimeError('7D numerical aggregate calibration fails')
    section=n.Section(m,bases['extend7'][:,:11],n.vector(m.c['a']),1.)
    z=np.linspace(-.2,.2,7);s0,v,y,J=section.points(z,jac=True);step=1e-6
    Jfd=np.empty((24,7))
    for j in range(7):
        d=np.zeros(7);d[j]=step
        plus=section.points(z+d)[0];minus=section.points(z-d)[0]
        Jfd[:,j]=(plus[0]-minus[0])/(2*step)
    # Section.points Jacobian is wrt t, while z perturbs t=a*z.
    fd_err=float(np.max(abs(J[0]*section.a[None,:]-Jfd)))
    if fd_err>1e-8 or not v[0]:raise RuntimeError('numerical section Jacobian validation fails')
    H=m.Jh;null_errors={k:float(np.linalg.norm(H@b[:,4:],ord=np.inf)) for k,b in bases.items()}
    if max(null_errors.values())>1e-10:raise RuntimeError('tangent basis nullspace check fails')
    np.savez_compressed(HERE/'bases.npz',**bases)
    validation={'label':'NUMERICAL SANITY ONLY; no new dimension screened','7d_calibration_max_abs_beta_difference':error,
                'fixed_h_jacobian_finite_difference_max_abs_error':fd_err,'tangent_nullspace_errors':null_errors,
                'hidden_residual':section.max_residual,'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.perf_counter()-st}
    (HERE/'sanity.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8')
    methods=['PREREGISTRATION.md','config.json','numerics.py','run.py','freeze.py','endpoint.json','bases.npz']
    originals=list((ROOT/'experiments/cleanroom_7d_interval_20261001').glob('*'))+list((ROOT/'experiments/rebalanced_7d_section_20261001').glob('*'))
    freeze={'parent_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'method_hashes':{k:sha(HERE/k) for k in methods},
        'original_preservation':{str(p.relative_to(ROOT)):sha(p) for p in originals if p.is_file()},
        'prospective_status':'Sanity passed. No 8D–24D scores inspected; deterministic bases frozen.'}
    (HERE/'METHOD_FROZEN.json').write_text(json.dumps(freeze,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(validation))
if __name__=='__main__':main()
