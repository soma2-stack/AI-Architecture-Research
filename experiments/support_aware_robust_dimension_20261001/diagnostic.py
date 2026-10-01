"""Numerical packing slopes inside selected CERTIFIED products, CPU only."""
from resources import ROOT,CFG,Monitor
import core as k
import json,itertools
import numpy as np
from scipy.stats import qmc
from fractions import Fraction as Q

def numerical_model(case):
 m=k.model(case);n=m.n;P=m.P
 R=np.zeros((n,n));W=R.copy();b=np.zeros(n);ER=np.zeros((n,P,n));EW=ER.copy();Eb=np.zeros((n,P))
 for p,(_,i,g,j) in enumerate(m.meta):
  if g=='R':R[i,j]=float(m.params[p]);ER[i,p,j]=1
  elif g=='W':W[i,j]=float(m.params[p]);EW[i,p,j]=1
  else:b[i]=float(m.params[p]);Eb[i,p]=1
 scales={g:np.sqrt(float(sum(m.params[p]**2 for p,(_,_,name,_) in enumerate(m.meta) if name==g)/sum(name==g for _,_,name,_ in m.meta))) for g in ['R','W','b']}
 weights=np.array([scales[g] for _,_,g,_ in m.meta])
 return {'n':n,'P':P,'R':R,'W':W,'b':b,'ER':ER,'EW':EW,'Eb':Eb,'weights':weights,'support':m.support,'case':case['case']}
def jets(m,X,B):
 count,T,n=X.shape;d=B.shape[1];P=m['P'];R,W=m['R'],m['W']
 h=np.zeros((count,n));S=np.zeros((count,n,P));hx=np.zeros((count,n,d));SJ=np.zeros((count,n,P,d))
 for t in range(T):
  u=B[t*n:(t+1)*n]
  ap=np.einsum('ij,bjp->bip',R,S)+np.einsum('ipj,bj->bip',m['ER'],h)+np.einsum('ipj,bj->bip',m['EW'],X[:,t])+m['Eb']
  ax=np.einsum('ij,bjd->bid',R,hx)+W@u
  apx=np.einsum('ij,bjpd->bipd',R,SJ)+np.einsum('ipj,bjd->bipd',m['ER'],hx)+np.einsum('ipj,jd->ipd',m['EW'],u)
  h=np.tanh(h@R.T+X[:,t]@W.T+m['b']);g=1-h*h
  SJ=g[:,:,None,None]*apx-2*(h*g)[:,:,None,None]*ap[:,:,:,None]*ax[:,:,None,:]
  S=g[:,:,None]*ap;hx=g[:,:,None]*ax
 ii,pp=zip(*m['support']);s=S[:,ii,pp]*m['weights'][list(pp)]
 J=SJ[:,ii,pp]*m['weights'][list(pp)][None,:,None]
 return h,S*m['weights'][None,None,:],hx,s,J

def distances(m,S):
 n=m['n'];beta=max(1,np.linalg.norm(m['R']));hi=1/np.cosh(.25)**2;lo=1/np.cosh(.75)**2
 gates=np.array(list(itertools.product([lo,hi],repeat=n))) if m['case']=='dense' else np.full((1,n),hi)
 C=gates@m['R']/(np.sqrt(n)*beta);F=np.einsum('vn,bnp->bvp',C,S);N=len(S);D=np.zeros((N,N))
 for start in range(0,N,32):
  B=F[start:start+32];part=np.zeros((len(B),N))
  for v in range(len(C)):part=np.maximum(part,np.linalg.norm(B[:,v,None,:]-F[None,:,v,:],axis=-1))
  D[start:start+32]=part
 return D

def greedy(D,spacing,start):
 ids=[start];nearest=D[start].copy();nearest[start]=-1
 while nearest.max()>spacing:
  j=int(nearest.argmax());ids.append(j);nearest=np.minimum(nearest,D[j]);nearest[ids]=-1
 return ids

def main():
 meter=Monitor('CPU numerical same-section scale diagnostics');rows=[]
 try:
  for result in json.loads((ROOT/'results.json').read_text()):
   meter.check();case=next(c for c in k.INPUT['cases'] if c['name']==result['case']);cert=result['certificate'];n=case['n'];r=cert['r']
   dim=result['dimension'];ids=dim['retained_indices'];q=len(ids)
   if not q:rows.append({'case':case['name'],'dimension':0,'skipped':'no epsilon-essential axes'});continue
   m=numerical_model(case);X0=np.array([[float(Q(v)) for v in row] for row in case['X']])
   B=np.array([[float(Q(v)) for v in row[:n+r]] for row in result['frame']['B']])*np.sqrt(3/32)
   L=np.array([[float(Q(v)) for v in row] for row in cert['selected_projection']]);rho=np.array([float(Q(v)) for v in cert['rho_i']])
   z=np.r_[2*qmc.Sobol(q,scramble=True,seed=CFG['diagnostic_seed']+n).random_base2(9)[:CFG['diagnostic_samples']]-1,np.array(list(itertools.product([-1.,1.],repeat=q)))]
   targets=np.zeros((len(z),r));targets[:,ids]=z*rho[ids]
   center=jets(m,X0[None],B);origin=np.r_[center[0][0],L@center[3][0]]
   goal=origin[None]+np.c_[np.zeros((len(z),n)),targets];y=np.zeros((len(z),n+r))
   for _ in range(18):
    meter.check();X=X0[None]+(y@B.T).reshape(len(y),*X0.shape);h,S,H,s,J=jets(m,X,B)
    F=np.c_[h,s@L.T];G=np.concatenate([H,np.einsum('rd,bdj->brj',L,J)],axis=1);res=F-goal
    if np.max(abs(res))<2e-12:break
    y-=np.linalg.solve(G,res[:,:,None])[:,:,0]
   assert np.max(abs(res))<2e-12
   amps=np.r_[np.full(n,float(Q(cert['a0'])*Q(cert['hidden_factor']))),[float(Q(v)) for v in cert['a_i']]]
   assert np.max(abs(y)/amps)<1+1e-10
   D=distances(m,S);ez=np.linalg.norm(z[:,None]-z[None,:],axis=-1);nz=ez>1e-12
   foundmin=np.min(D[nz]/ez[nz]);foundmax=np.max(D[nz]/ez[nz])
   assert foundmin>=float(Q(dim['m_Euclidean_lower']))*(1-1e-9)
   assert foundmax<=float(Q(dim['M_Euclidean_upper']))*(1+1e-9)
   counts=[];bestids={}
   for factor in CFG['separation_factors']:
    spacing=2*float(k.EPS)*factor;sets=[greedy(D,spacing,start) for start in [0,len(z)//2,len(z)-1]]
    selected=max(sets,key=len);counts.append(len(selected));bestids[str(factor)]=selected
   slopes=[float(np.log(counts[i]/counts[i+1])/np.log(2)) for i in range(3)]
   row={'case':case['name'],'certified_r':q,'sample_count':len(z),'factors':CFG['separation_factors'],'states':counts,'bits':[float(np.log2(x)) for x in counts],
     'adjacent_loglog_slopes':slopes,'slope_mean':float(np.mean(slopes)),'saturated_at_smallest_spacing':counts[0]==len(z),
     'actual_pair_ratio_min':float(foundmin),'actual_pair_ratio_max':float(foundmax),'certified_m':float(Q(dim['m_Euclidean_lower'])),'certified_M':float(Q(dim['M_Euclidean_upper'])),
     'fixed_h_projection_residual':float(np.max(abs(res))),'maximum_box_use_fraction':float(np.max(abs(y)/amps)),
     'label':'NUMERICAL finite sampling/greedy diagnostic; slopes are not a dimension proof'}
   np.savez_compressed(ROOT/f"scale_{case['name']}.npz",z=z,y=y,X=X,S=S,D=D,**{'ids_'+key.replace('.','_'):val for key,val in bestids.items()})
   rows.append(row);print(case['name'],'r',q,'counts',counts,'slopes',slopes,flush=True)
  (ROOT/'scale_diagnostics.json').write_text(json.dumps(rows,indent=2)+'\n')
 finally:meter.finish()
if __name__=='__main__':main()
