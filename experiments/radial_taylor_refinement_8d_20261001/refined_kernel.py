"""Whole-box third derivatives: dyadic gates and positive upward tensor algebra."""
import os, sys, time
os.environ['CUDA_VISIBLE_DEVICES']='-1'
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'): os.environ[key]='1'
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
ROOT=Path(__file__).resolve().parent
OLD=ROOT.parent/'antipodal_robust_dimension_20261001'
sys.path.insert(0,str(OLD))
import antipodal_kernel as a
from antipodal_kernel import I,uq,upadd,upmul,upsum,left,abs_array,residual,inverse,matmul
from exact_gate import gate_majorants
CPU_START=None

def check_budget():
    if CPU_START is not None and time.process_time()-CPU_START>1200:
        raise RuntimeError('20 CPU-minute budget exhausted')

def plus(*terms):
    ans=terms[0]
    for term in terms[1:]: ans=upadd(ans,term)
    return ans

def times(*terms):
    ans=terms[0]
    for term in terms[1:]: ans=upmul(ans,term)
    return ans

def sym3(t2,t1):
    return plus(upmul(t2[..., :, :, None],t1[...,None,None,:]),
                upmul(t2[..., :, None, :],t1[...,None,:,None]),
                upmul(t2[..., None, :, :],t1[..., :,None,None]))

def third_majorants(base,r,amps):
    """Every mixed partial in normal+tangent variables, no sampling or BLAS."""
    check_budget(); m=base['model']; assert m.depth==1
    before=m.serialize(); n=m.n; P=m.P; s=n+r
    R=np.zeros((n,n)); W=np.zeros((n,n))
    RI=[[I(0) for _ in range(n)] for _ in range(n)]
    WI=[[I(0) for _ in range(n)] for _ in range(n)]
    for i,j,p in m.layers[0]['R']: R[i,j]=uq(abs(m.params[p])); RI[i][j]=I(m.params[p])
    for i,j,p in m.layers[0]['W']: W[i,j]=uq(abs(m.params[p])); WI[i][j]=I(m.params[p])
    b=[I(m.params[p]) for i,j,p in m.layers[0]['b']]
    history=[]
    for row in range(len(base['X'])*n):
        radius=sum((base['BI'][row][k].absq()*amps[k] for k in range(s)),Q(0))
        xx=base['X'][row//n][row%n]
        lo=(xx-radius)*I.scale; hi=(xx+radius)*I.scale
        history.append(I(lo.numerator//lo.denominator,-((-hi.numerator)//hi.denominator),True))
    hh=[I(0) for _ in range(n)]
    hx=np.zeros((n,s)); h2=np.zeros((n,s,s)); h3=np.zeros((n,s,s,s))
    S=np.zeros((n,P)); Sx=np.zeros((n,P,s))
    S2=np.zeros((n,P,s,s)); S3=np.zeros((n,P,s,s,s))
    for t in range(len(base['X'])):
        check_budget(); xx=history[t*n:(t+1)*n]
        u=np.array([[uq(base['BI'][t*n+i][k].absq()) for k in range(s)] for i in range(n)])
        # Exact signed affine input combination, before interval absolute values.
        affine=[[sum((WI[i][j]*base['BI'][t*n+j][k] for j in range(n)),I(0)) for k in range(s)] for i in range(n)]
        inputcenter=[sum((WI[i][j]*base['X'][t][j] for j in range(n)),I(0)) for i in range(n)]
        inputrad=[sum((v.absq()*amps[k] for k,v in enumerate(row)),Q(0)) for row in affine]
        pre=[sum((RI[i][j]*hh[j] for j in range(n)),b[i])+inputcenter[i]+I(-I(inputrad[i]).hi,I(inputrad[i]).hi,True) for i in range(n)]
        hn=[v.tanh() for v in pre]; gates=[I(1)-v.square() for v in hn]
        g,f2,f3,f4=gate_majorants(hn)
        ax=upadd(left(R,hx),np.array([[uq(v.absq()) for v in row] for row in affine])); ax2=left(R,h2); ax3=left(R,h3)
        p=left(R,S); px=left(R,Sx); p2=left(R,S2); p3=left(R,S3)
        for q,(_,i,name,j) in enumerate(m.meta):
            if name=='R':
                p[i,q]=upadd(p[i,q],uq(hh[j].absq()))
                px[i,q]=upadd(px[i,q],hx[j]); p2[i,q]=upadd(p2[i,q],h2[j]); p3[i,q]=upadd(p3[i,q],h3[j])
            elif name=='W':
                p[i,q]=upadd(p[i,q],uq(xx[j].absq())); px[i,q]=upadd(px[i,q],u[j])
            else: p[i,q]=upadd(p[i,q],1.)
        AX=ax[:,None,:]
        cube=times(AX[..., :,None,None],AX[...,None,:,None],AX[...,None,None,:])
        px_ax_ax=plus(times(px[..., :,None,None],AX[...,None,:,None],AX[...,None,None,:]),
                      times(AX[..., :,None,None],px[...,None,:,None],AX[...,None,None,:]),
                      times(AX[..., :,None,None],AX[...,None,:,None],px[...,None,None,:]))
        S3_new=plus(times(g[:,None,None,None,None],p3),
            times(f2[:,None,None,None,None],plus(times(p[:,:,None,None,None],ax3[:,None]),sym3(ax2[:,None],px),sym3(p2,AX))),
            times(f3[:,None,None,None,None],plus(times(p[:,:,None,None,None],sym3(ax2[:,None],AX)),px_ax_ax)),
            times(f4[:,None,None,None,None],p[:,:,None,None,None],cube))
        h3_new=plus(times(g[:,None,None,None],ax3),times(f2[:,None,None,None],sym3(ax2,ax)),
                    times(f3[:,None,None,None],ax[:,:,None,None],ax[:,None,:,None],ax[:,None,None,:]))
        S2_new=plus(times(g[:,None,None,None],p2),times(f3[:,None,None,None],p[:,:,None,None],AX[..., :,None],AX[...,None,:]),
                    times(f2[:,None,None,None],plus(times(p[:,:,None,None],ax2[:,None]),
                         times(px[..., :,None],AX[...,None,:]),times(px[...,None,:],AX[..., :,None]))))
        Sx_new=upadd(upmul(g[:,None,None],px),times(f2[:,None,None],p[:,:,None],AX))
        S_new=upmul(g[:,None],p)
        h2_new=upadd(upmul(g[:,None,None],ax2),times(f2[:,None,None],ax[:,:,None],ax[:,None,:]))
        hx_new=upmul(g[:,None],ax)
        S,Sx,S2,S3=S_new,Sx_new,S2_new,S3_new
        hx,h2,h3,hh=hx_new,h2_new,h3_new,hn
    HS=np.array([upmul(S2[i,p],uq(Q(base['scaleI'][m.meta[p][2]].hi,I.scale))) for i,p in m.support])
    HS3=np.array([upmul(S3[i,p],uq(Q(base['scaleI'][m.meta[p][2]].hi,I.scale))) for i,p in m.support])
    assert before==m.serialize()
    assert all(np.isfinite(x).all() and (x>=0).all() for x in (h2,h3,HS,HS3))
    return h2,h3,HS,HS3

def contract2(T,V):
    r=V.shape[1]; ans=np.zeros((T.shape[0],r,r))
    for k in range(V.shape[0]):
        for l in range(V.shape[0]):
            ans=upadd(ans,times(T[:,k,l,None,None],V[k][None,:,None],V[l][None,None,:]))
    return ans

def contract3(T,V):
    r=V.shape[1]; ans=np.zeros((T.shape[0],r,r,r))
    for k in range(V.shape[0]):
        for l in range(V.shape[0]):
            for m in range(V.shape[0]):
                ans=upadd(ans,times(T[:,k,l,m,None,None,None],V[k][None,:,None,None],
                                   V[l][None,None,:,None],V[m][None,None,None,:]))
    return ans

def mixed_chain(T,W2,V):
    r=V.shape[1]; ans=np.zeros((T.shape[0],r,r,r))
    for k in range(V.shape[0]):
        for l in range(V.shape[0]):
            ans=upadd(ans,upmul(T[:,k,l,None,None,None],sym3(W2[k][None],V[l][None])))
    return ans

def certify(base,aa,ah,L,Kh,K):
    """One fixed candidate; always returns (result,bounds), including failures."""
    check_budget(); n=base['n']; r=len(aa); amps=[ah]*n+aa
    radius=max(sum((v.absq()*amp for v,amp in zip(row,amps)),Q(0)) for row in base['BI'])
    out={'valid':False,'precision_bits':I.bits,'r':r,'radius':str(radius)}
    if radius>1: return dict(out,reason='local domain'),{}
    HH,HH3,HS,HS3=third_majorants(base,r,amps)
    bounds={'HH':HH,'HH3':HH3,'HS':HS,'HS3':HS3}
    J=[row[:n+r] for row in base['reduced']]
    H0=[row[:n] for row in J[:n]]; Ht=[row[n:] for row in J[:n]]
    # Independent exact inversion proves both frozen rational matrices nonsingular.
    inverse(Kh); inverse(K)
    cross=matmul([row[:n] for row in J[n:]],matmul(inverse(H0),Ht))
    C0=matmul([[I(v) for v in row] for row in L],[[J[n+i][n+j]-cross[i][j] for j in range(r)] for i in range(len(L[0]))])
    E0=residual(K,C0); Khabs=abs_array(Kh); au=np.array([uq(v) for v in aa]); ampu=np.array([uq(v) for v in amps])
    Eh=upadd(residual(Kh,H0),left(Khabs,upsum(upmul(HH[:,:n,:],ampu[None,None,:]),axis=2)))
    eta_h=float(max(upsum(Eh,axis=1))); out['eta_hidden']=eta_h
    if eta_h>=.75: return dict(out,reason='hidden contraction'),bounds
    force=upadd(upsum(upmul(abs_array(Ht),au[None,:]),axis=1),
                upmul(.5,upsum(upsum(times(HH[:,n:,n:],au[None,:,None],au[None,None,:]),axis=2),axis=1)))
    mapped=left(Khabs,force[:,None])[:,0]; out['hidden_forcing_upper']=mapped.tolist()
    if any(Q(float(v))>(1-Q(eta_h))*ah for v in mapped): return dict(out,reason='hidden self-mapping'),bounds
    Neumann=inverse([[Q(int(i==j))-Q(float(Eh[i,j])) for j in range(n)] for i in range(n)])
    assert all(v>=0 for row in Neumann for v in row)
    inv=np.array([[uq(sum(Neumann[i][k]*abs(Kh[k][j]) for k in range(n))) for j in range(n)] for i in range(n)])
    Htb=upadd(abs_array(Ht),upsum(upmul(HH[:,n:,:],ampu[None,None,:]),axis=2))
    Gamma=left(inv,Htb); V=np.vstack([Gamma,np.eye(r)])
    y2=left(inv,contract2(HH,V)); W2=np.vstack([y2,np.zeros((r,r,r))])
    y3=left(inv,upadd(contract3(HH3,V),mixed_chain(HH,W2,V)))
    Sn=upadd(abs_array([row[:n] for row in J[n:]]),upsum(upmul(HS[:,:n,:],ampu[None,None,:]),axis=2))
    fixed3=plus(contract3(HS3,V),mixed_chain(HS,W2,V),left(Sn,y3))
    selected3=left(abs_array(L),fixed3)
    cubic=upsum(upsum(upsum(times(selected3,au[None,:,None,None],au[None,None,:,None],au[None,None,None,:]),axis=3),axis=2),axis=1)
    M3=upmul(left(abs_array(K),cubic[:,None])[:,0],np.array([uq(1/v) for v in aa]))
    center_rows=upsum(upmul(E0,np.array([[uq(aa[j]/aa[i]) for j in range(r)] for i in range(r)])),axis=1)
    ell=[[sum(K[i][j]*L[j][d] for j in range(r))/aa[i] for d in range(len(L[0]))] for i in range(r)]
    mu=a.structured_query(base,ell); assert not isinstance(mu,tuple)
    beta=[v*(1-Q(float(er))-Q(float(m))/6) for v,er,m in zip(mu,center_rows,M3)]
    passed=all(v>Q(1,1000) for v in beta)
    out.update(valid=True,certified_dimension=r if passed else None,all_antipodal_faces_pass=passed,
        center_rows_upper=center_rows.tolist(),M3_upper=M3.tolist(),mu_tilde=[str(v) for v in mu],
        beta3=[str(v) for v in beta],weakest_beta=str(min(beta)),
        hidden_residual_upper=Eh.tolist(),normal_first_derivative_upper=Gamma.tolist(),
        reason='6D certified; antipodal pairs only' if passed else 'third-order face margin')
    bounds.update(y2=y2,y3=y3,fixed3=fixed3,selected3=selected3)
    assert all(np.isfinite(v).all() for v in bounds.values())
    return out,bounds
