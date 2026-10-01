from fractions import Fraction as Q
import numpy as np
import mpmath as mp
from replay_interval import I,matmul,inverse
from pathlib import Path
import json
CFG=json.loads((Path(__file__).parent/"inputs.json").read_text())["original_config"]
FROZEN=json.loads((Path(__file__).parent/"inputs.json").read_text())
def mpinverse(A):
    key="K_hidden" if len(A)==3 else "K_selected"
    return [[Q(x) for x in row] for row in FROZEN[key]]
def dyadic(v):
    return Q(int(mp.nint(v*mp.mpf(2)**CFG['basis_dyadic_bits'])),1<<CFG['basis_dyadic_bits'])

def mpq(v):
    v=Q(v);return mp.mpf(v.numerator)/v.denominator

def uq(v):
    """Upward binary64 conversion of an exact rational nonnegative bound."""
    v=Q(v);f=float(v)
    if Q(f)<v:f=np.nextafter(f,np.inf)
    return f

def upadd(x,y):return np.nextafter(np.asarray(x,dtype=float)+np.asarray(y,dtype=float),np.inf)

def upmul(x,y):
    x=np.asarray(x,dtype=float);y=np.asarray(y,dtype=float)
    z=np.nextafter(x*y,np.inf)
    return np.where((x==0)|(y==0),0.,z)

def upsum(x,axis=-1):
    x=np.moveaxis(x,axis,-1);v=np.zeros(x.shape[:-1])
    for j in range(x.shape[-1]):v=upadd(v,x[...,j])
    return v

def left(A,T):
    out=np.zeros((len(A),)+T.shape[1:])
    for k in range(T.shape[0]):out=upadd(out,upmul(np.asarray(A)[:,k].reshape((-1,)+(1,)*(T.ndim-1)),T[k]))
    return out

def abs_array(A):return np.array([[uq(x.absq() if isinstance(x,I) else abs(x)) for x in row] for row in A])

def residual(K,A):
    prod=matmul([[I(x) for x in row] for row in K],A)
    return abs_array([[I(int(i==j))-x for j,x in enumerate(row)] for i,row in enumerate(prod)])

def curvature(base,r,amplitudes):
    """Uniform directional h_yy and (S_phi)_yy majorants, including all mixed pairs.

    Values/gates are dyadic interval-enclosed on the entire history box.
    Positive derivative tensors use upward-rounded elementary binary64 ops.
    No BLAS/reassociation is used in these majorants.
    """
    model=base['model'];n=base['n'];P=model.P;s=n+r
    R=np.zeros((n,n));W=np.zeros((n,n))
    RI=[[I(0) for _ in range(n)] for _ in range(n)];WI=[[I(0) for _ in range(n)] for _ in range(n)]
    for i,j,p in model.layers[0]['R']:R[i,j]=uq(abs(model.params[p]));RI[i][j]=I(model.params[p])
    for i,j,p in model.layers[0]['W']:W[i,j]=uq(abs(model.params[p]));WI[i][j]=I(model.params[p])
    b=[I(model.params[p]) for i,j,p in model.layers[0]['b']]
    history_bounds=[]
    for row in range(len(base['X'])*n):
        radius=sum((base['BI'][row][k].absq()*amplitudes[k] for k in range(s)),Q(0))
        xx=base['X'][row//n][row%n]
        history_bounds.append(I((Q(xx)-radius)*I.scale//1,-((-(Q(xx)+radius)*I.scale)//1),True))
    hh=[I(0) for _ in range(n)]
    hx=np.zeros((n,s));hxx=np.zeros((n,s,s));S=np.zeros((n,P));Sx=np.zeros((n,P,s));Sxx=np.zeros((n,P,s,s))
    for t in range(len(base['X'])):
        xx=history_bounds[t*n:(t+1)*n]
        u=np.array([[uq(base['BI'][t*n+i][k].absq()) for k in range(s)] for i in range(n)])
        aa=[sum((RI[i][j]*hh[j]+WI[i][j]*xx[j] for j in range(n)),b[i]) for i in range(n)]
        newh=[x.tanh() for x in aa]
        gates=[I(1)-x.square() for x in newh]
        g=np.array([uq(Q(x.hi,I.scale)) for x in gates])
        f2=np.array([uq((2*newh[i]*gates[i]).absq()) for i in range(n)])
        f3=np.array([uq((-2*gates[i]*(I(1)-3*newh[i].square())).absq()) for i in range(n)])
        ax=upadd(left(R,hx),left(W,u));axx=left(R,hxx)
        ap=left(R,S);apx=left(R,Sx);apxx=left(R,Sxx)
        for p,(_,i,name,j) in enumerate(model.meta):
            if name=='R':
                ap[i,p]=upadd(ap[i,p],uq(hh[j].absq()))
                apx[i,p]=upadd(apx[i,p],hx[j]);apxx[i,p]=upadd(apxx[i,p],hxx[j])
            elif name=='W':
                ap[i,p]=upadd(ap[i,p],uq(xx[j].absq()));apx[i,p]=upadd(apx[i,p],u[j])
            else:ap[i,p]=upadd(ap[i,p],1.)
        Sxx=upadd(upmul(g[:,None,None,None],apxx),upmul(f3[:,None,None,None],
             upmul(ap[:,:,None,None],upmul(ax[:,None,:,None],ax[:,None,None,:]))))
        terms=upadd(upmul(ap[:,:,None,None],axx[:,None,:,:]),
              upadd(upmul(apx[:,:,:,None],ax[:,None,None,:]),upmul(apx[:,:,None,:],ax[:,None,:,None])))
        Sxx=upadd(Sxx,upmul(f2[:,None,None,None],terms))
        Sx=upadd(upmul(g[:,None,None],apx),upmul(f2[:,None,None],upmul(ap[:,:,None],ax[:,None,:])))
        S=upmul(g[:,None],ap)
        hxx=upadd(upmul(g[:,None,None],axx),upmul(f2[:,None,None],upmul(ax[:,:,None],ax[:,None,:])))
        hx=upmul(g[:,None],ax);hh=newh
    HS=np.array([upmul(Sxx[i,p],uq(Q(base['scaleI'][model.meta[p][2]].hi,I.scale))) for i,p in model.support])
    assert np.isfinite(HS).all() and np.isfinite(hxx).all()
    return hxx,HS

def query_margins(base,projectors):
    model=base['model'];n=base['n'];P=model.P
    R=[[Q(0) for _ in range(n)] for _ in range(n)]
    W=[[Q(0) for _ in range(n)] for _ in range(n)]
    for i,j,p in model.layers[0]['R']:R[i][j]=model.params[p]
    for i,j,p in model.layers[0]['W']:W[i][j]=model.params[p]
    inverse(W) # Required to realize each permitted gate vector at fixed h.
    Gamma=[[Q(1,4)*int(i==j)+Q(5,8) for j in range(n)] for i in range(n)]
    C=[[sum(R[k][i]*Gamma[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    Ci=inverse(C)
    beta2=max(Q(1),sum(x*x for row in R for x in row));factor=I(n*beta2).sqrt()
    margins=[]
    for row in projectors:
        U=[[Q(0) for _ in range(P)] for _ in range(n)]
        for value,(i,p) in zip(row,model.support):U[i][p]=value
        coeff=[[sum(Ci[i][k]*U[k][p] for k in range(n)) for p in range(P)] for i in range(n)]
        total=sum((I(sum(x*x for x in row)).sqrt() for row in coeff),I(0))
        margin=(I(1)/(factor*total)).lo
        margins.append(Q(margin,I.scale))
    # Positive-control inclusion in the exact accepted gate interval.
    low=(I(1)-I(Q(3,4)).tanh().square());high=(I(1)-I(Q(1,4)).tanh().square())
    assert Q(low.hi,I.scale)<Q(5,8)<Q(7,8)<Q(high.lo,I.scale)
    return margins,C

def frame_projection(base,r):
    """Secondary fixed-history axes, output dual matched to finite permitted queries."""
    n=base['n'];model=base['model'];P=model.P;UU=base['U'][:r]
    _,C=query_margins(base,UU)
    F=np.array(C,dtype=object);G=F@F.T
    tensors=[]
    for row in UU:
        U=np.zeros((n,P),dtype=object)
        for x,(i,p) in zip(row,model.support):U[i,p]=x
        tensors.append(U)
    Gram=[[sum(tensors[i][k,p]*G[k,l]*tensors[j][l,p] for k in range(n) for l in range(n) for p in range(P))
           for j in range(r)] for i in range(r)]
    M=mp.matrix([[mpq(x) for x in row] for row in Gram])**-1
    result=[]
    for j in range(r):
        T=sum((np.asarray([[mpq(x) for x in row] for row in tensors[k]],dtype=object)*M[k,j] for k in range(r)))
        GT=np.asarray([[sum(mpq(G[i,k])*T[k,p] for k in range(n)) for p in range(P)] for i in range(n)],dtype=object)
        result.append([dyadic(GT[i,p]) for i,p in model.support])
    return result

def certify(base,r,a0,profile,hidden_factor,projectors,detail=False):
    n=base['n'];sigma=base['sigma'][:r]
    aa=[a0 if profile=='equal' else a0*x/sigma[0] for x in sigma]
    amplitudes=[a0*hidden_factor]*n+aa
    HH,HS=curvature(base,r,amplitudes)
    J=[row[:n+r] for row in base['reduced']]
    H0=[row[:n] for row in J[:n]];Ht=[row[n:] for row in J[:n]]
    cache=base.setdefault('_center_cache',{})
    key=(I.bits,r,tuple(tuple(row) for row in projectors))
    if key not in cache:
        Kh=mpinverse(H0);Hinv0=inverse(H0)
        Jp=matmul([[I(x) for x in row] for row in projectors],J[n:])
        cross=matmul([row[:n] for row in Jp],matmul(Hinv0,Ht))
        C0=[[Jp[i][n+j]-cross[i][j] for j in range(r)] for i in range(r)]
        K=mpinverse(C0)
        cache[key]=(Kh,abs_array(Kh),residual(Kh,H0),K,residual(K,C0),query_margins(base,projectors)[0])
    Kh,Khabs,E0,K,Ecenter,mu=cache[key]
    variation=upsum(upmul(HH[:,:n,:],np.array([uq(x) for x in amplitudes])[None,None,:]),axis=2)
    Eh=upadd(E0,left(Khabs,variation));eta_h=float(np.max(upsum(Eh,axis=1)))
    if eta_h>=float(Q(CFG['contraction_cap'])):return {'valid':False,'reason':'hidden_jacobian_dominance','eta_h':eta_h}
    forcing=upadd(upsum(upmul(abs_array(Ht),np.array([uq(x) for x in aa])[None,:]),axis=1),
       upmul(.5,upsum(upsum(upmul(HH[:,n:,n:],upmul(np.array([uq(x) for x in aa])[None,:,None],
                  np.array([uq(x) for x in aa])[None,None,:])),axis=2),axis=1)))
    mapped=left(Khabs,forcing[:,None])[:,0]
    if any(Q(float(x))>(1-Q(eta_h))*amplitudes[i] for i,x in enumerate(mapped)):
        return {'valid':False,'reason':'hidden_section_box_inclusion','eta_h':eta_h}
    # Absolute inverse enclosure from a nonnegative Neumann series majorant.
    Neumann=inverse([[Q(int(i==j))-Q(float(Eh[i,j])) for j in range(n)] for i in range(n)])
    invbound=np.array([[uq(sum(Neumann[i][k]*abs(Kh[k][j]) for k in range(n))) for j in range(n)] for i in range(n)])
    Htbound=upadd(abs_array(Ht),upsum(upmul(HH[:,n:,:],np.array([uq(x) for x in amplitudes])[None,None,:]),axis=2))
    Gamma=left(invbound,Htbound)
    V=np.vstack([Gamma,np.eye(r)])
    def contract(T):
        ans=np.zeros((T.shape[0],r,r))
        for k in range(n+r):
            for l in range(n+r):ans=upadd(ans,upmul(T[:,k,l,None,None],upmul(V[k][None,:,None],V[l][None,None,:])))
        return ans
    hsecond=left(invbound,contract(HH))
    Snormal=upadd(abs_array([row[:n] for row in J[n:]]),
                upsum(upmul(HS[:,:n,:],np.array([uq(x) for x in amplitudes])[None,None,:]),axis=2))
    fixed_curvature=upadd(contract(HS),left(Snormal,hsecond))
    Pabs=abs_array(projectors);curv=left(Pabs,fixed_curvature)
    variation=upsum(upmul(curv,np.array([uq(x) for x in aa])[None,None,:]),axis=2)
    E=upadd(Ecenter,left(abs_array(K),variation))
    ratio=np.array([[uq(aa[k]/aa[j]) for k in range(r)] for j in range(r)])
    scaled=upmul(E,ratio);eta=float(np.max(upsum(scaled,axis=1)))
    if eta>=float(Q(CFG['contraction_cap'])):return {'valid':False,'reason':'mixed_sensitivity_curvature','eta_h':eta_h,'eta':eta}
    rho0=[sigma[i]*aa[i] for i in range(r)]
    factors=[(1-Q(eta))*aa[j]/sum(abs(K[j][i])*rho0[i] for i in range(r)) for j in range(r)]
    lam=min(Q(1),Q(CFG['target_fraction_of_contraction_slack'])*min(factors))
    rho=[lam*x for x in rho0]
    epsilon=Q(CFG['epsilon_primary']);spacing=Q(CFG['strict_spacing_epsilon_multiplier'])*epsilon
    counts=[int((2*x*m)//spacing)+1 for x,m in zip(rho,mu)]
    states=int(np.prod(np.array(counts,dtype=object)));robust=sum(x>1 for x in counts)
    out={'valid':True,'case':model_case(base),'n':n,'r':r,'a0':str(a0),'profile':profile,'hidden_factor':str(hidden_factor),
         'a_i':[str(x) for x in aa],'rho_i':[str(x) for x in rho],'mu_i':[str(x) for x in mu],
         'observable_half_ranges':[str(x*m) for x,m in zip(rho,mu)],'N_i':counts,'states':str(states),
         'bits':float(mp.log(states,2)),'robust_dimension':robust,'eta_hidden':eta_h,'eta_sensitivity':eta,
         'lambda':str(lam),'label':'CERTIFIED','chart':'curved fixed-h lift of an exact projection product'}
    if detail:
        out.update(directional_curvature_F=[[float(np.nextafter(np.sqrt(upsum(upmul(fixed_curvature[:,i,j],fixed_curvature[:,i,j]),axis=0)),np.inf))
                   for j in range(r)] for i in range(r)],
                   projected_curvature=curv.tolist(),
                   scaled_jacobian_residual_upper=scaled.tolist(),hidden_jacobian_residual_upper=Eh.tolist(),
                   hidden_forcing_upper=mapped.tolist(),normal_first_derivative_upper=Gamma.tolist(),
                   K_hidden=[[str(x) for x in row] for row in Kh],K_selected=[[str(x) for x in row] for row in K],
                   selected_projection=[[str(x) for x in row] for row in projectors],
                   preconditioner_condition=float(mp.cond(mp.matrix([[mpq(x) for x in row] for row in K]))))
    return out

def model_case(base):return 'independent' if base['model'].diagonal else 'dense'
