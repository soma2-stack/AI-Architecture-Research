"""Recompute all certificate bounds; never read archived numerical bounds."""
import os
os.environ['CUDA_VISIBLE_DEVICES']='-1'
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import json, time, hashlib, itertools, sys, traceback
from fractions import Fraction as Q
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import mpmath as mp
import psutil
import reviewed_kernel as e
import replay_jets as c

ROOT=Path(__file__).parent
INPUT=json.loads((ROOT/'inputs.json').read_text())
PREREG=json.loads((ROOT/'preregistration.json').read_text())

class Meter:
    def __init__(self,job):
        self.job=job;self.start=time.perf_counter();self.p=psutil.Process()
        self.prior=sum(row['cpu_seconds'] for row in rows())
    def check(self):
        assert self.prior+time.process_time()<PREREG['max_cpu_seconds'],'CPU safety stop'
        assert self.p.memory_info().rss<PREREG['rss_cap_bytes'],'RAM safety stop'
    def finish(self):
        m=self.p.memory_info()
        row={'job':self.job,'cpu_seconds':time.process_time(),'wall_seconds':time.perf_counter()-self.start,
             'peak_ram_bytes':max(m.rss,getattr(m,'peak_wset',m.rss)),
             'gpu_seconds':0,'gpu_used':False,'cuda_used':False,'peak_vram_bytes':0,'workers':1}
        with (ROOT/'cpu_ledger.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(row)+'\n')
        return row

def rows():
    p=ROOT/'cpu_ledger.jsonl'
    return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []

def dump(name,data):
    p=ROOT/name
    assert not p.exists(),'Preserve output: '+name
    p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')

def model():
    m=c.Model('dense',3)
    m.params=list(map(Q,INPUT['params']))
    assert m.P==21 and len(m.support)==63
    return m

def fresh_base(bits,meter,verify_basis=False):
    e.I.precision(bits);mp.mp.dps=100;c.ACTIVE_METER=meter
    m=model();X=[[Q(x) for x in row] for row in INPUT['X']]
    before=m.serialize()
    print('Regenerating endpoint mixed jets:',bits,flush=True)
    F,JI,_=c.jets(m,X,'interval')
    assert before==m.serialize()
    Bq=[[Q(x) for x in row] for row in INPUT['B']]
    sd=e.I(Q(3,32)).sqrt()
    BI=[[e.I(x)*sd for x in row] for row in Bq]
    scales={group:e.I(sum(m.params[p]**2 for p,(_,_,g,_) in enumerate(m.meta) if g==group)/
                     sum(g==group for _,_,g,_ in m.meta)).sqrt() for group in ('R','W','b')}
    reduced=e.matmul(JI.tolist(),BI)
    for j,(_,p) in enumerate(m.support):reduced[3+j]=[x*scales[m.meta[p][2]] for x in reduced[3+j]]
    base={'model':m,'X':X,'n':3,'D':63,'U':[[Q(x) for x in row] for row in INPUT['U']],
          'B':Bq,'BI':BI,'JI':JI.tolist(),'reduced':reduced,'scaleI':scales,
          'sigma':[e.dyadic(mp.mpf(x)) for x in INPUT['singular_values']]}
    dump(f'endpoint_jacobian_{bits}.json',{'bits':bits,'J_intervals':[[[str(x.lo),str(x.hi)] for x in row] for row in JI],
                                       'F_intervals':[[str(x.lo),str(x.hi)] for x in F]})
    if verify_basis:
        print('Rebuilding QR/SVD chart at 100 decimal digits',flush=True)
        FF,Jmp,_=c.jets(m,X,'mp');Jmp=mp.matrix(Jmp.tolist())
        for value,box in zip(FF,F):
            assert e.mpq(Q(box.lo,e.I.scale))<=value<=e.mpq(Q(box.hi,e.I.scale))
        differences=[]
        for i in range(66):
            for j in range(66):
                box=JI[i,j];v=Jmp[i,j]
                assert e.mpq(Q(box.lo,e.I.scale))<=v<=e.mpq(Q(box.hi,e.I.scale))
                differences.append(abs(v-e.mpq(box.midq())))
        QQ,_=mp.qr(Jmp[:3,:].T);N=QQ[:,3:]
        weights=[mp.sqrt(sum(e.mpq(m.params[p])**2 for p,(_,_,g,_) in enumerate(m.meta) if g==group)/
                         sum(g==group for _,_,g,_ in m.meta)) for group in ('R','W','b')]
        scale=dict(zip(('R','W','b'),weights));input_sd=mp.sqrt(mp.mpf(3)/32)
        Af=mp.matrix([[Jmp[3+i,j]*scale[m.meta[p][2]]*input_sd for j in range(66)] for i,(_,p) in enumerate(m.support)])*N
        U,s,V=mp.svd(Af);tangents=N*V.T
        proposed=[[e.dyadic(QQ[i,j] if j<3 else tangents[i,j-3]) for j in range(5)] for i in range(66)]
        proposedU=[[e.dyadic(U[j,i]) for j in range(63)] for i in range(2)]
        detail={'precision_digits':100,'max_mp_interval_midpoint_discrepancy':mp.nstr(max(differences),40),
                'full_spectrum':[mp.nstr(x,75) for x in s],
                'selected_history_axes_reproduced_exactly':proposed==Bq,
                'selected_left_axes_reproduced_exactly':proposedU==base['U'],
                'max_history_axis_difference':mp.nstr(max(abs(e.mpq(x-y)) for a,b in zip(proposed,Bq) for x,y in zip(a,b)),40)}
        dump('chart_reconstruction.json',detail)
        assert proposed==Bq and proposedU==base['U'],'Frozen axis reconstruction discrepancy; do not replace axes'
        # A separate scalar differentiation path, not the propagated jet recurrence.
        print('Independent mpmath nested differentiation cross-check',flush=True)
        def direct(theta,history):
            h=[mp.mpf(0)]*3
            for t in range(22):
                h=[mp.tanh(sum(theta[3*i+j]*h[j]+theta[9+3*i+j]*history[3*t+j] for j in range(3))+theta[18+i]) for i in range(3)]
            return h
        theta=list(map(e.mpq,m.params));history=list(map(e.mpq,[v for row in X for v in row]));cross=[]
        for state,p,k in ((0,0,0),(1,9,32),(2,20,65)):
            def scalar(pp,xx):
                th=theta.copy();hx=history.copy();th[p]=pp;hx[k]=xx
                return direct(th,hx)[state]
            value=mp.diff(scalar,(theta[p],history[k]),(1,1))
            expected=Jmp[3+state*21+p,k]
            assert abs(value-expected)<mp.mpf('1e-80')
            cross.append({'state':state,'parameter':p,'history_coordinate':k,'absolute_difference':mp.nstr(abs(value-expected),45)})
        dump('independent_scalar_cross_check.json',{'method':'mpmath.diff of separately written scalar forward recurrence','digits':100,'checks':cross})
    return base

def joint_replay(base,bits):
    projectors=[[Q(x) for x in row] for row in INPUT['selected_projection']]
    r=2;amps=[Q('1/8')]*5
    assert INPUT['a_i']==['1/8']*2 and INPUT['normal_half_widths']==['1/8']*3
    captured={};curvature=e.curvature
    def capture(*args):
        HH,HS=curvature(*args);captured.update(HH=HH,HS=HS)
        return HH,HS
    e.curvature=capture
    try:
        # Fixed K lookup supplied by reviewed_kernel. Only this one proposal.
        result=e.certify(base,2,Q('1/8'),'equal',Q(1),projectors,True)
    finally:e.curvature=curvature
    dump(f'raw_curvature_{bits}.json',{'precision_bits':bits,'direction_order':['normal0','normal1','normal2','tangent0','tangent1'],
                                    'hidden_mixed_upper':captured['HH'].tolist(),
                                    'normalized_sensitivity_mixed_upper':captured['HS'].tolist(),
                                    'sensitivity_row_order':base['model'].support,
                                    'rounding':'ordered binary64 upward majorants over complete simultaneous interval box'})
    dump(f'regenerated_certificate_{bits}.json',result)
    assert result['valid'],'First certificate inequality failed: '+result.get('reason','unknown')
    # The original rectangle and original margins, not newly proposed values.
    K=[[Q(x) for x in row] for row in INPUT['K_selected']]
    Kh=[[Q(x) for x in row] for row in INPUT['K_hidden']]
    rho=list(map(Q,INPUT['rho_i']));mu=list(map(Q,INPUT['mu_i']))
    eta=Q(result['eta_sensitivity']);eta_h=Q(result['eta_hidden'])
    assert eta_h<1 and eta<1
    hidden_slack=[(1-eta_h)*Q('1/8')-Q(x) for x in result['hidden_forcing_upper']]
    target_slack=[(1-eta)*Q('1/8')-sum(abs(K[j][i])*rho[i] for i in range(2)) for j in range(2)]
    assert all(x>=0 for x in hidden_slack),'First failed inequality: hidden self-map'
    assert all(x>=0 for x in target_slack),'First failed inequality: frozen target rectangle self-map'
    for old,new in zip(mu,result['mu_i']):assert old<=Q(new),'First failed inequality: frozen query margin'
    # Nonzero exact determinants: fixed point equations imply H=0 and target attainment.
    def determinant(A):
        if len(A)==2:return A[0][0]*A[1][1]-A[0][1]*A[1][0]
        return sum((-1)**j*A[0][j]*(A[1][(j+1)%3]*A[2][(j+2)%3]-A[1][(j+2)%3]*A[2][(j+1)%3])*(-1)**j for j in range(3))
    assert determinant(K)!=0 and determinant(Kh)!=0
    # Reconstruct the frozen output functionals from the query-aligned SVD frame.
    rebuilt=e.frame_projection(base,2)
    assert rebuilt==projectors,'Frozen projection reconstruction discrepancy'
    margins,C=e.query_margins(base,projectors);Ci=e.inverse(C)
    dual=[]
    for row in projectors:
        L=[row[i*21:(i+1)*21] for i in range(3)]
        coeff=[[sum(Ci[i][k]*L[k][p] for k in range(3)) for p in range(21)] for i in range(3)]
        assert [[sum(C[i][k]*coeff[k][p] for k in range(3)) for p in range(21)] for i in range(3)]==L
        dual.append([[str(x) for x in row] for row in coeff])
    eps=Q(INPUT['epsilon']);delta=[Q(17,8)*eps/m for m in mu]
    counts=[int((2*x)//d)+1 for x,d in zip(rho,delta)]
    assert counts==[2,2],'First failed inequality: original packing counts'
    grid=list(itertools.product(*[[-x+j*d for j in range(N)] for x,d,N in zip(rho,delta,counts)]))
    pair_checks=[]
    for a,b in itertools.combinations(grid,2):
        lower=max(m*abs(x-y) for m,x,y in zip(mu,a,b))
        assert lower>2*eps,'First failed inequality: strict packing separation'
        pair_checks.append({'point_a':list(map(str,a)),'point_b':list(map(str,b)),'query_distance_lower':str(lower)})
    audit={'valid':True,'precision_bits':bits,'eta_hidden':float(eta_h),'eta_sensitivity':float(eta),
           'frozen_rho':INPUT['rho_i'],'frozen_mu':INPUT['mu_i'],
           'hidden_self_map_slack':list(map(str,hidden_slack)),'target_box_slack':list(map(str,target_slack)),
           'K_hidden_det':str(determinant(Kh)),'K_selected_det':str(determinant(K)),
           'query_frame':[[str(x) for x in row] for row in C],'exact_dual_coefficients':dual,
           'query_inequality':'D_C >= max_i mu_i |Delta Psi_i| for arbitrary full Delta S; exact C B_i=L_i verified',
           'delta':list(map(str,delta)),'N_i':counts,'states':len(grid),'bits':2,
           'strict_pair_checks':pair_checks,'observable_half_ranges':[str(x*m) for x,m in zip(rho,mu)],
           'proposed_rho_matches_original':result['rho_i']==INPUT['rho_i'],
           'regenerated_mu_matches_original':result['mu_i']==INPUT['mu_i']}
    dump(f'consistency_{bits}.json',audit)
    return audit

def main(bits):
    meter=Meter(f'clean certificate replay {bits} bits')
    try:
        h=c.hardware();dump(f'hardware_{bits}.json',h)
        assert hashlib.sha256((ROOT/'inputs.json').read_bytes()).hexdigest()==json.loads((ROOT/'input_manifest.json').read_text())['inputs_sha256']
        base=fresh_base(bits,meter,verify_basis=bits==192)
        print('Regenerating complete mixed-curvature certificate',flush=True)
        answer=joint_replay(base,bits)
        print(json.dumps({k:answer[k] for k in ('eta_hidden','eta_sensitivity','N_i','states','bits')}),flush=True)
    except Exception:
        dump(f'FAILURE_{bits}.json',{'error':traceback.format_exc(),'policy':'stop; do not change constants, axes, box or tolerance'})
        raise
    finally:print(json.dumps(meter.finish()),flush=True)

if __name__=='__main__':main(int(sys.argv[1]))
