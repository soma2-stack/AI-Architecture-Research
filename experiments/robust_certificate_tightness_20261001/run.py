"""Official Level-B/C analysis. Every output remains explicitly numerical."""
import json,itertools,math,time
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
import cupy as cp
from scipy.stats import qmc
import geometry as g
from resources import Monitor
ROOT=g.ROOT;CFG=g.CFG
def save(name,obj):(ROOT/name).write_text(json.dumps(obj,indent=2,default=lambda v:v.item())+'\n',encoding='utf-8')
def chunks(total,size=64):return range(0,total,size)
def section_chunks(m,X,B,beta,meter):
    rows=[]
    for start in chunks(len(beta)):
      meter.check();row=g.section(m,X,B,beta[start:start+64]);row.pop('out')
      row['S']=cp.asnumpy(row['S']);rows.append(row)
    return {k:np.concatenate([row[k] for row in rows]) for k in rows[0]}
def curvature(case,meter):
    m=g.make(case);n=m['n'];cert=case['certificate'];r=cert['r']
    B=g.floats(case['B'])[:,:n+r]*g.SD;X=g.floats(case['X'])
    amp=np.r_[np.full(n,float(Q(cert['a0']))*float(Q(cert['hidden_factor']))),[float(Q(v)) for v in cert['a_i']]]
    bound=np.load(ROOT/f"bounds_{case['name']}.npz");HH,HS=bound['HH'],bound['HS']
    actualH=np.zeros_like(HH);actualS=np.zeros_like(HS)
    def assess(z):
      ratios=[]
      for start in chunks(len(z)):
        meter.check();zz=z[start:start+64]*amp
        XX=X[None]+(zz@B.T).reshape(len(zz),*X.shape)
        out=g.jets(m,XX,B,True)
        ah=cp.asnumpy(cp.max(cp.abs(out['HH']),axis=0));ass=cp.asnumpy(cp.max(cp.abs(out['HS']),axis=0))
        np.maximum(actualH,ah,out=actualH);np.maximum(actualS,ass,out=actualS)
        rh=cp.max(cp.abs(out['HH'])/cp.asarray(np.maximum(HH,1e-300))[None],axis=(1,2,3))
        rs=cp.max(cp.abs(out['HS'])/cp.asarray(np.maximum(HS,1e-300))[None],axis=(1,2,3))
        ratios.extend(cp.asnumpy(cp.maximum(rh,rs)).tolist())
      return np.array(ratios)
    rng=np.random.default_rng(CFG['seed']+n+(m['case']=='independent')+10*(case['kind']=='confirmation'))
    sob=qmc.Sobol(n+r,scramble=True,seed=int(rng.integers(2**31))).random_base2(9)*2-1
    corners=np.array(list(itertools.product([-1.,1.],repeat=n+r))) if n+r<=8 else rng.choice([-1.,1.],(128,n+r))
    points=np.r_[np.zeros((1,n+r)),sob,corners];scores=assess(points)
    order=np.argsort(-scores)[:6];current=points[order].copy();bestz=points[np.argmax(scores)].copy();best=float(scores.max())
    for iteration in range(24):
      signs=rng.choice([-1.,1.],current.shape);plus=np.clip(current+.025*signs,-1,1);minus=np.clip(current-.025*signs,-1,1)
      score=assess(np.r_[plus,minus]);grad=((score[:6]-score[6:])/.05)[:,None]*signs
      grad/=np.maximum(np.linalg.norm(grad,axis=1),1e-12)[:,None]
      current=np.clip(current+.06*grad,-1,1);sc=assess(current)
      j=int(np.argmax(sc))
      if sc[j]>best:best=float(sc[j]);bestz=current[j].copy()
    np.savez_compressed(ROOT/f"curvature_ratios_{case['name']}.npz",bound_HH=HH,bound_HS=HS,
        actual_max_HH=actualH,actual_max_HS=actualS,ratio_HH=actualH/np.maximum(HH,1e-300),ratio_HS=actualS/np.maximum(HS,1e-300))
    # Actual implicit section curvature and preconditioned Jacobian variation.
    beta=sob[:128,n:]*amp[n:];sec=section_chunks(m,X,B/g.SD,beta,meter)
    L=g.floats(cert['selected_projection']);Kh=g.floats(cert['K_hidden']);K=g.floats(cert['K_selected'])
    center=g.jets(m,X[None],B,True,np);H0=center['H'][0,:,:n];Ht=center['H'][0,:,n:]
    C0=L@(center['J'][0,:,n:]-center['J'][0,:,:n]@np.linalg.solve(H0,Ht))
    maxcurv=np.zeros((r,r,r));etamax=0.;alpharatio=0.;allratio=[]
    for start in chunks(len(beta)):
      valid=sec['valid'][start:start+64]
      if not valid.any():continue
      out=g.jets(m,sec['X'][start:start+64][valid],B,True)
      H0p=out['H'][:,:,:n];Ht=out['H'][:,:,n:];Az=-cp.linalg.solve(H0p,Ht)
      V=cp.concatenate([Az,cp.broadcast_to(cp.eye(r),(len(Az),r,r))],axis=1)
      hz2=cp.einsum('bqkl,bki,blj->bqij',out['HH'],V,V)
      Az2=-cp.linalg.solve(H0p,hz2.reshape(len(Az),n,-1)).reshape(len(Az),n,r,r)
      sj2=cp.einsum('bqkl,bki,blj->bqij',out['HS'],V,V)+cp.einsum('bqk,bkij->bqij',out['J'][:,:,:n],Az2)
      projected=cp.einsum('rq,bqij->brij',cp.asarray(L),sj2)
      np.maximum(maxcurv,cp.asnumpy(cp.max(cp.abs(projected),axis=0)),out=maxcurv)
      C=cp.einsum('rq,bqj->brj',cp.asarray(L),out['J'][:,:,n:]+out['J'][:,:,:n]@Az)
      E=cp.abs(cp.asarray(K)@(C-cp.asarray(C0)))
      aa=amp[n:];eta=cp.max(cp.sum(E*cp.asarray(aa)[None,None,:]/cp.asarray(aa)[None,:,None],axis=2))
      etamax=max(etamax,float(eta))
      alpharatio=max(alpharatio,float(np.max(np.abs(sec['y'][start:start+64][valid,:n])/amp[:n])))
    projected_bound=np.array(cert['projected_curvature'])
    ratios=maxcurv/np.maximum(projected_bound,1e-300)
    return {'label':'NUMERICAL sampled/adversarial maxima, not upper bounds','raw_ratio_max':best,
      'raw_hessian_ratio_HH_max':float(np.max(actualH/np.maximum(HH,1e-300))),
      'raw_hessian_ratio_HS_max':float(np.max(actualS/np.maximum(HS,1e-300))),
      'raw_ratio_median_nonzero':float(np.median((actualS/np.maximum(HS,1e-300))[HS>1e-20])),
      'worst_normalized_box_point':bestz.tolist(),'amplitudes':amp.tolist(),
      'fixed_section_projected_curvature_actual_max':maxcurv.tolist(),
      'fixed_section_projected_curvature_ratio':ratios.tolist(),
      'projected_curvature_ratio_max':float(ratios.max()),
      'actual_preconditioned_jacobian_variation':etamax,'certified_eta':cert['eta_sensitivity'],
      'actual_normal_halfwidth_use_fraction':alpharatio,'fixed_section_success_fraction':float(sec['valid'].mean())}
def product_trials(case,meter):
    m=g.make(case);n=m['n'];X=g.floats(case['X']);frames=g.bases(m,X)
    trials=[];best=None;best_data=None
    for name,full in frames.items():
      rmax=min(10,full.shape[1]-n)
      for r in range(1,rmax+1):
        B=full[:,:n+r];corners=np.array(list(itertools.product([-1.,1.],repeat=r)))
        for amp in CFG['amplitudes']:
          sec=section_chunks(m,X,B,corners*amp,meter)
          row={'basis':name,'r':r,'amplitude':amp,'points':len(corners),
            'valid_fraction':float(sec['valid'].mean()),'residual_max':float(sec['residual'].max()),'success':False}
          if sec['valid'].all():
            sep,pair=g.min_distance(m,cp.asarray(sec['S']));row.update(min_query=sep,closest_pair=pair)
            row['success']=sep>CFG['strict_numerical_separation']
            row['failure']='query_collision' if not row['success'] else None
          else:row['failure']='fixed_h_solve_or_declared_domain'
          trials.append(row)
          if row['success'] and (best is None or (r,row['min_query'])>(best['r'],best['min_query'])):
            best=row.copy();best_data={**sec,'B':B,'beta':corners*amp}
        print(case['name'],name,'r',r,'success',any(v['success'] for v in trials if v['basis']==name and v['r']==r),flush=True)
      # Selected extension, only after a complete ten-dimensional success.
      prior=[v for v in trials if v['basis']==name and v['r']==10 and v['success']]
      if prior:
        amp=max(prior,key=lambda v:v['min_query'])['amplitude']
        for r in [11,12]:
          if r>full.shape[1]-n:continue
          B=full[:,:n+r];corners=np.array(list(itertools.product([-1.,1.],repeat=r)))
          sec=section_chunks(m,X,B,corners*amp,meter);row={'basis':name,'r':r,'amplitude':amp,'points':len(corners),'valid_fraction':float(sec['valid'].mean()),'success':False}
          if sec['valid'].all():
            sep,pair=g.min_distance(m,cp.asarray(sec['S']));row.update(min_query=sep,closest_pair=pair,success=sep>CFG['strict_numerical_separation'])
          trials.append(row)
          if row['success'] and (best is None or (r,row['min_query'])>(best['r'],best['min_query'])):best=row.copy();best_data={**sec,'B':B,'beta':corners*amp}
    if best_data is not None:
      np.savez_compressed(ROOT/f"product_{case['name']}.npz",**{k:v for k,v in best_data.items() if k!='out'})
    return {'label':'NUMERICAL complete finite vertex grids, not continuous product certificates','best':best,'trials':trials}
def pack(case,products,meter):
    m=g.make(case);X=g.floats(case['X']);full=g.bases(m,X)['svd'];r=full.shape[1]-m['n']
    sob=qmc.Sobol(r,scramble=True,seed=CFG['seed']+m['n']).random_base2(11)*2-1
    beta=np.concatenate([sob[j*512:(j+1)*512]*amp for j,amp in enumerate(CFG['amplitudes'])])
    sec=section_chunks(m,X,full,beta,meter);ok=sec['valid'];SS=sec['S'][ok];XX=sec['X'][ok]
    if products['best']:
      grid=np.load(ROOT/f"product_{case['name']}.npz")
      SS=np.concatenate([SS,grid['S']]);XX=np.concatenate([XX,grid['X']])
    D=g.pair_distances(m,cp.asarray(SS));N=len(SS)
    rng=np.random.default_rng(CFG['seed']);runs=[]
    for start in [0,*rng.integers(0,N,size=2).tolist()]:
      chosen=[int(start)];mind=D[start].copy()
      while len(chosen)<CFG['greedy_states_cap']:
        meter.check();j=int(np.argmax(mind))
        if mind[j]<=CFG['strict_numerical_separation']:break
        chosen.append(j);mind=np.minimum(mind,D[j])
      runs.append(chosen)
    chosen=max(runs,key=len);dist=D[np.ix_(chosen,chosen)].copy();np.fill_diagonal(dist,np.inf)
    pair=np.unravel_index(np.argmin(dist),dist.shape);selectedX=XX[chosen]
    np.savez_compressed(ROOT/f"packing_{case['name']}.npz",X=selectedX,S=SS[chosen],distances=dist)
    return {'label':'NUMERICAL LOWER ESTIMATE, not maximum','states':len(chosen),'bits':math.log2(len(chosen)),
      'closest_pair':pair,'min_query':float(dist[pair]),'cap_reached':len(chosen)==CFG['greedy_states_cap'],
      'valid_sobol_fraction':float(ok.mean()),'greedy_restart_counts':[len(v) for v in runs],
      'candidate_points':N,'chart_r':r}
def main():
    assert not (ROOT/'results.json').exists();meter=Monitor('official nonlinear geometry',True);results=[]
    try:
      for case in g.DATA['cases']:
        meter.check();print('BEGIN',case['name'],flush=True)
        same=g.frozen_product(case);np.savez_compressed(ROOT/f"accepted_grid_{case['name']}.npz",**{k:v for k,v in same.items() if isinstance(v,np.ndarray)})
        same={k:v for k,v in same.items() if not isinstance(v,np.ndarray)}
        curv=curvature(case,meter);products=product_trials(case,meter);packing=pack(case,products,meter)
        row={'name':case['name'],'n':case['n'],'case':case['case'],'kind':case['kind'],
          'certified_dimension':case['certificate']['robust_dimension'],'certified_bits':case['certificate']['bits'],
          'accepted_grid':same,'curvature':curv,'products':products,'packing':packing}
        save(f"result_{case['name']}.json",row);results.append(row)
        print('DONE',case['name'],products['best'],packing['states'],flush=True)
      save('results.json',results)
    except Exception:
      import traceback
      save('FAILURE.json',{'traceback':traceback.format_exc(),'partial_results':results});raise
    finally:meter.finish()
if __name__=='__main__':main()
