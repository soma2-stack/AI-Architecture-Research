"""Every SVD direction's CENTER diagnostics; no unmeasured supremum claims."""
import json,numpy as np,cupy as cp
import geometry as g
from resources import Monitor
def diagonal(m,X,B):
  X=cp.asarray(X);B=cp.asarray(B);T,n=X.shape;P=m['P'];d=B.shape[1]
  R,W,ER,EW,Eb=[cp.asarray(m[k]) for k in ['R','W','ER','EW','Eb']]
  h=cp.zeros(n);S=cp.zeros((n,P));hx=cp.zeros((n,d));Sx=cp.zeros((n,P,d))
  hdd=cp.zeros((n,d));Sdd=cp.zeros((n,P,d))
  for t in range(T):
    u=B[t*n:(t+1)*n]
    ap=R@S+cp.einsum('ipj,j->ip',ER,h)+cp.einsum('ipj,j->ip',EW,X[t])+Eb
    ax=R@hx+W@u;axx=R@hdd
    apx=cp.einsum('ij,jpd->ipd',R,Sx)+cp.einsum('ipj,jd->ipd',ER,hx)+cp.einsum('ipj,jd->ipd',EW,u)
    apdd=cp.einsum('ij,jpd->ipd',R,Sdd)+cp.einsum('ipj,jd->ipd',ER,hdd)
    h=cp.tanh(R@h+W@X[t]+cp.asarray(m['b']));gg=1-h*h;f2=-2*h*gg;f3=-2*gg*(1-3*h*h)
    Sdd=gg[:,None,None]*apdd+f3[:,None,None]*ap[:,:,None]*ax[:,None,:]**2+f2[:,None,None]*(ap[:,:,None]*axx[:,None,:]+2*apx*ax[:,None,:])
    hdd=gg[:,None]*axx+f2[:,None]*ax*ax
    Sx=gg[:,None,None]*apx+f2[:,None,None]*ap[:,:,None]*ax[:,None,:]
    S=gg[:,None]*ap;hx=gg[:,None]*ax
  ii=cp.asarray([i for i,p in m['support']]);pp=cp.asarray([p for i,p in m['support']])
  return cp.asnumpy(hdd),cp.asnumpy(Sdd[ii,pp]*cp.asarray(m['supported_weights'])[:,None])
def main():
  meter=Monitor('all-axis center slack diagnostics',True);outputs=[]
  try:
    # Development check against the previously tested full mixed-jet method.
    m=g.make({'n':3,'case':'dense'});rng=np.random.default_rng(9810002)
    X=rng.uniform(-.1,.1,(5,3));B=rng.normal(size=(15,4))*.1
    hh,ss=diagonal(m,X,B);check=g.jets(m,X[None],B,True)
    np.testing.assert_allclose(hh,cp.asnumpy(cp.diagonal(check['HH'][0],axis1=1,axis2=2)),atol=1e-12,rtol=1e-10)
    np.testing.assert_allclose(ss,cp.asnumpy(cp.diagonal(check['HS'][0],axis1=1,axis2=2)),atol=1e-12,rtol=1e-10)
    for case in g.DATA['cases']:
      meter.check();m=g.make(case);X=g.floats(case['X']);n=m['n'];D=len(m['support'])
      s,U,V,J=g.legacy.spectrum_batch(m,X[None],True);H=J[0,:n]
      normal=np.linalg.qr(H.T,mode='reduced')[0];tan=V[0,:D].T
      corrected=tan-normal@np.linalg.solve(H@normal,H@tan)
      B=corrected*g.SD;hh,ss=diagonal(m,X,B)
      Hnormal=H@normal*g.SD;Snormal=(J[0,n:]*m['supported_weights'][:,None])@normal*g.SD
      alpha_dd=-np.linalg.solve(Hnormal,hh);fixed=ss+Snormal@alpha_dd
      first=(J[0,n:]*m['supported_weights'][:,None])@B
      tensors=g.legacy.tensor_rows(m,first.T);second=g.legacy.tensor_rows(m,fixed.T)
      C=g.query_vectors(m)
      gain=np.linalg.norm(np.einsum('vi,dip->dvp',C,tensors),axis=2).max(axis=1)
      curve=np.linalg.norm(np.einsum('vi,dip->dvp',C,second),axis=2).max(axis=1)
      records=[]
      for i in range(D):
        records.append({'axis':i+1,'sigma_binary64':float(s[0,i]),'center_unit_query_gain':float(gain[i]),
          'center_query_curvature':float(curve[i]),'center_hidden_compensation_second_norm':float(np.max(np.abs(alpha_dd[:,i]))),
          'accepted_interval_axis':i<case['certificate']['r'],
          'extra_direction_sampled':i<16,'outside_declared_prefix_limit':i>=16,
          'failure_diagnostic':'I: not sampled beyond16' if i>=16 else 'A/G: center unit gain below2epsilon, not a global bound' if gain[i]<.002 else 'requires actual mixed-geometry/grid test',
          'scope':'CENTER ONLY; tiny binary64 spectral tails are numerically unresolved'})
      outputs.append({'name':case['name'],'directions':records,'center_diagnostics_not_certificates':True})
    (g.ROOT/'axis_slack.json').write_text(json.dumps(outputs,indent=2)+'\n')
    (g.ROOT/'axis_test.json').write_text(json.dumps({'passed':True,'signed_diagonal_vs_full_jet':True})+'\n')
  finally:meter.finish()
if __name__=='__main__':main()
