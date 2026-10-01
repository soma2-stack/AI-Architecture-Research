import itertools,json,math
from fractions import Fraction as Q
import numpy as np,cupy as cp
import geometry as g
from resources import Monitor
def main():
  assert not (g.ROOT/'same_product_results.json').exists()
  meter=Monitor('same accepted product numerical packing',True);rows=[]
  try:
    for case in g.DATA['cases']:
      m=g.make(case);n=m['n'];cert=case['certificate'];r=cert['r'];meter.check()
      assert r<=3
      levels={1:65,2:33,3:17}[r]
      B=g.floats(case['B'])[:,:n+r]*g.SD;L=cp.asarray(g.floats(cert['selected_projection']))
      X0=g.floats(case['X']);rho=np.array([float(Q(v)) for v in cert['rho_i']])
      targets=np.array(list(itertools.product(np.linspace(-1,1,levels),repeat=r)))*rho
      base=g.jets(m,X0[None],B);origin=cp.concatenate([base['h'][0],L@base['s'][0]])
      allX=[];allS=[];valid=[];allY=[]
      amp=np.r_[np.full(n,float(Q(cert['a0']))*float(Q(cert['hidden_factor']))),[float(Q(v)) for v in cert['a_i']]]
      for start in range(0,len(targets),64):
        meter.check();target=targets[start:start+64];goal=origin[None]+cp.asarray(np.c_[np.zeros((len(target),n)),target])
        y=cp.zeros((len(target),n+r))
        for _ in range(18):
          X=cp.asarray(X0)[None]+(y@cp.asarray(B).T).reshape(len(y),*X0.shape);out=g.jets(m,X,B)
          F=cp.concatenate([out['h'],out['s']@L.T],axis=1);res=F-goal
          if float(cp.max(cp.abs(res)))<2e-12:break
          J=cp.concatenate([out['H'],cp.einsum('rd,bdj->brj',L,out['J'])],axis=1)
          y-=cp.linalg.solve(J,res[:,:,None])[:,:,0]
        good=(cp.max(cp.abs(res),axis=1)<2e-12)&cp.all(cp.abs(y)<=cp.asarray(amp)[None]+1e-10,axis=1)
        allX.extend(cp.asnumpy(X));allS.extend(cp.asnumpy(out['S']));allY.extend(cp.asnumpy(y));valid.extend(cp.asnumpy(good))
      valid=np.array(valid);X=np.array(allX)[valid];S=np.array(allS)[valid];y=np.array(allY)[valid]
      D=g.pair_distances(m,cp.asarray(S));runs=[];rng=np.random.default_rng(g.CFG['seed'])
      for start in [0,*rng.integers(0,len(S),size=2).tolist()]:
        chosen=[int(start)];nearest=D[start].copy()
        while len(chosen)<512:
          j=int(np.argmax(nearest))
          if nearest[j]<=.00205:break
          chosen.append(j);nearest=np.minimum(nearest,D[j])
        runs.append(chosen)
      chosen=max(runs,key=len);dist=D[np.ix_(chosen,chosen)].copy();np.fill_diagonal(dist,np.inf)
      pair=tuple(map(int,np.unravel_index(np.argmin(dist),dist.shape)))
      np.savez_compressed(g.ROOT/f"same_product_{case['name']}.npz",X=X[chosen],S=S[chosen],y=y[chosen],distances=dist)
      row={'name':case['name'],'r':r,'levels_per_coordinate':levels,'evaluated_points':len(valid),
        'valid_fraction':float(valid.mean()),'states':len(chosen),'bits':math.log2(len(chosen)),
        'min_query':float(dist[pair]),'closest_pair':pair,'certified_states':int(cert['states']),
        'state_ratio':len(chosen)/int(cert['states']),'label':'NUMERICAL packing on SAME accepted product'}
      rows.append(row);print(row,flush=True)
    (g.ROOT/'same_product_results.json').write_text(json.dumps(rows,indent=2)+'\n')
  finally:meter.finish()
if __name__=='__main__':main()
