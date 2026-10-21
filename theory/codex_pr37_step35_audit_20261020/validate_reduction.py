"""Independent full-vector Householder/permutation reference for the class simulator."""
import os
for name in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS'):os.environ[name]='1'
import json,math
from pathlib import Path
import numpy as np
import e7_independent as reduced
HERE=Path(__file__).resolve().parent

def full(n,P,kind,H=60,warm=20,gap=80,source_pattern='single'):
    k=n//2; d=n//4; a=1-1/n; lam=1/(100*n); sk=math.sqrt(k); ga=1/(1-1/sk)
    w=-np.ones(k)/sk; w[0]+=1
    def U(x):return x-ga*np.multiply.outer(x@w,w) if x.ndim==2 else x-ga*w*float(w@x)
    def Op(x):
        z=U(x); v=z.copy(); v[...,1:d]=z[...,:d-1]; v[...,0]=z[...,d-1]
        return U(v)
    j=k-3; jp=k-2; ret=np.arange(d+1,d+1+P); assert ret[-1]<j
    T=warm+H+gap; release=warm+H; amp=math.tanh(.38)
    pulses=[(warm+H//2,0)] if source_pattern=='single' else [(warm+H//3,0),(warm+2*H//3,1)]
    h=np.zeros((2,k)); B=h.copy(); own=np.zeros(2); src=0.; sig=.05
    for _ in range(80):sig=math.tanh(lam*sig+.05)
    peak=0.; xmax=0.; width=total=0
    for t in range(1,T+1):
        pre=a*Op(h)+.05; hn=np.tanh(pre)
        mask,targets=reduced.controls(t,warm,release,T,kind,np.arange(P))
        rows=ret[mask]
        mnow=0
        if len(rows):
            x=np.arctanh(targets[mask])[None,:]-pre[:,rows]
            xmax=max(xmax,float(abs(x).max())); mnow+=int(np.count_nonzero(x[0])); hn[:,rows]=targets[mask]
        if warm<=t<release:
            target=np.zeros((2,2))
            for start,history in pulses:
                if start<=t<start+7:target[history]=[amp,-amp]
            x=np.arctanh(target)-pre[:,[j,jp]]
            xmax=max(xmax,float(abs(x).max())); mnow+=2; hn[:,[j,jp]]=target
        width=max(width,mnow); total+=mnow
        gates=1-hn*hn; c=src/sig
        nb=a*Op(B); nb[:,j]+=c; B=gates*nb
        own=gates[:,j]*(a*own+c)
        peak=max(peak,abs(float(own[0]-own[1])))
        h=hn; src=math.tanh(lam*src+.05)
    z=U(B[0]-B[1]); z[j]-=own[0]-own[1]; z[d-1]=0
    pz=z.copy(); pz[1:d]=z[:d-1]; pz[0]=z[d-1]
    coef=a*U(pz)
    read=max(abs(float(np.maximum(reduced.LO*coef,reduced.HI*coef).sum())),abs(float(np.minimum(reduced.LO*coef,reduced.HI*coef).sum())))
    return {'readout':read,'peak_own':peak,'max_input':xmax,'width':width,'total':total,'endpoint_gap':float(abs(h[0]-h[1]).max())}

def main():
    rows=[]
    for n,P,kind,pattern in ((4096,32,'hold','single'),(4096,32,'mixed','single'),(4096,32,'strong_targets','single'),(8192,48,'alternating','single'),(8192,48,'anti','single'),(8192,48,'anti','bipolar')):
        f=full(n,P,kind,source_pattern=pattern); r=reduced.run(n,P,kind,H=60,warm=20,gap=80,source_pattern=pattern)
        err=abs(f['readout']-r['centered_one_column_box_optimum'])
        assert err<1e-9 and abs(f['peak_own']-r['peak_abs_Delta_own_source'])<1e-9
        assert abs(f['max_input']-r['max_abs_actual_input'])<1e-10
        assert f['width']==r['peak_actual_width_m'] and f['total']==r['actual_additive_support']
        assert f['endpoint_gap']<1e-14
        rows.append({'n':n,'P':P,'family':kind,'source_pattern':pattern,'full':f,'class_readout':r['centered_one_column_box_optimum'],'readout_error':err})
    # Strong independent link to a previously executed, independently implemented full-vector run.
    control=reduced.run(65536,2048,'reset64')
    expected=json.loads((HERE.parents[0]/'codex_pr37_independent_audit_20261020'/'retention_resets.json').read_text())[0]
    assert abs(control['centered_one_column_box_optimum']-expected['centered_one_column_box_optimum'])<1e-8
    rows.append({'previous_full_vector_control':'n65536 P2048 reset64','class_readout':control['centered_one_column_box_optimum'],'previous_full_vector_readout':expected['centered_one_column_box_optimum'],'peak_m_matches':control['peak_actual_width_m']==expected['peak_actual_width_m']})
    (HERE/'reduction_validation.json').write_text(json.dumps(rows,indent=2)); print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
