"""Separate CPU mpmath path for frozen models, roots and critical queries."""
import os
os.environ['CUDA_VISIBLE_DEVICES']='-1'
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
from pathlib import Path
import json,itertools,time
from fractions import Fraction as Q
import numpy as np
import mpmath as mp
from resources import Monitor
ROOT=Path(__file__).parent;DATA=json.loads((ROOT/'inputs.json').read_text())
def q(v):
  x=Q(v);return mp.mpf(x.numerator)/x.denominator
def model(case):
  n=case['n'];params=list(map(q,DATA['models']['dense_parameters'][str(n)]))
  R=mp.matrix(n,n);W=mp.matrix(n,n);b=mp.matrix(n,1)
  for i in range(n):
    for j in range(n):R[i,j]=params[i*n+j] if case['case']=='dense' else q(Q(6+3*i,20)) if i==j else mp.mpf(0)
    for j in range(n):W[i,j]=params[n*n+i*n+j]
    b[i]=params[2*n*n+i]
  meta=[];values=[]
  for g,A in [('R',R),('W',W),('b',b)]:
    for i in range(n):
      for j in range(A.cols):
        if g=='R' and case['case']=='independent' and i!=j:continue
        meta.append((i,g,j));values.append(A[i,j])
  scale={g:mp.sqrt(sum(v*v for v,(_,name,_) in zip(values,meta) if name==g)/sum(name==g for _,name,_ in meta)) for g in ['R','W','b']}
  weights=[scale[g] for i,g,j in meta];beta=max(mp.mpf(1),mp.sqrt(sum(x*x for x in R)))
  return n,R,W,b,meta,weights,beta
def forward(m,X,B=None):
  n,R,W,b,meta,weights,beta=m;P=len(meta);h=mp.matrix(n,1);S=mp.matrix(n,P)
  d=0 if B is None else B.cols;hx=mp.matrix(n,d)
  for t,xx in enumerate(X):
    u=mp.matrix(xx);a=R*h+W*u+b;ap=R*S
    for p,(i,g,j) in enumerate(meta):ap[i,p]+=h[j] if g=='R' else u[j] if g=='W' else 1
    ax=R*hx+(W*B[t*n:(t+1)*n,:] if B is not None else mp.matrix(n,0))
    h=mp.matrix([mp.tanh(v) for v in a]);G=mp.diag([1-v*v for v in h]);S=G*ap;hx=G*ax
  return h,mp.matrix([[S[i,p]*weights[p] for p in range(P)] for i in range(n)]),hx
def exact_queries(m,Delta):
  n,R,_,_,_,_,beta=m;low=1/mp.cosh(q(Q(3,4)))**2;high=1/mp.cosh(q(Q(1,4)))**2
  values=[mp.norm(Delta.T*(R.T*mp.matrix(gates))/(mp.sqrt(n)*beta)) for gates in itertools.product([low,high],repeat=n)]
  return max(values)
def refine(case,X):
  m=model(case);n=m[0];B=mp.matrix([[q(v)*mp.sqrt(q(Q(3,32))) for v in row[:n]] for row in case['B']])
  X=[[q(float(v)) for v in row] for row in X];origin=[[q(v) for v in row] for row in case['X']]
  target=forward(m,origin)[0];alpha=mp.matrix(n,1)
  for _ in range(8):
    now=[[X[t][j]+sum(B[t*n+j,k]*alpha[k] for k in range(n)) for j in range(n)] for t in range(len(X))]
    h,S,H=forward(m,now,B);res=h-target
    if mp.norm(res,mp.inf)<mp.mpf('1e-55'):return h,S,alpha
    alpha-=mp.lu_solve(H,res)
  raise AssertionError('High-precision fixed-h correction failed')
def curvature_check(case,row):
  """Independent scalar mixed differentiation at the adversarial worst point."""
  cert=case['certificate'];n=case['n'];r=cert['r'];d=n+r;m=model(case)
  B=np.array([[float(Q(v)) for v in line[:d]] for line in case['B']])*np.sqrt(3/32)
  X=np.array([[float(Q(v)) for v in line] for line in case['X']])
  y=np.array(row['curvature']['worst_normalized_box_point'])*np.array(row['curvature']['amplitudes'])
  bounds=np.load(ROOT/f"bounds_{case['name']}.npz")
  # Avoid CuPy in this CPU path. The elementwise sampled maxima select one
  # candidate entry, evaluated at the stored adversarial point.
  found=np.load(ROOT/f"curvature_ratios_{case['name']}.npz")
  ih=np.unravel_index(np.argmax(found['ratio_HH']),found['ratio_HH'].shape)
  iss=np.unravel_index(np.argmax(found['ratio_HS']),found['ratio_HS'].shape)
  family='HS' if found['ratio_HS'][iss]>=found['ratio_HH'][ih] else 'HH'
  index=iss if family=='HS' else ih;out,j,k=index
  BB=mp.matrix([[q(v)*mp.sqrt(q(Q(3,32))) for v in line[:d]] for line in case['B']])
  yy=mp.matrix([q(float(v)) for v in y]);xx=[[q(v) for v in line] for line in case['X']]
  def value(a,b):
    delta=yy.copy();delta[j]+=a;delta[k]+=b
    now=[[xx[t][i]+sum(BB[t*n+i,l]*delta[l] for l in range(d)) for i in range(n)] for t in range(len(xx))]
    h,S,_=forward(m,now)
    if family=='HH':return h[out]
    support=[(i,p) for i in range(n) for p,(owner,_,_) in enumerate(m[4]) if case['case']=='dense' or owner==i]
    i,p=support[out];return S[i,p]
  if j==k:actual=mp.diff(lambda a:value(a,mp.mpf(0)),mp.mpf(0),2)
  else:actual=mp.diff(value,(mp.mpf(0),mp.mpf(0)),(1,1))
  upper=q(float(bounds[family][index]))
  return {'family':family,'entry':list(map(int,index)),'digits':mp.mp.dps,
    'actual_scalar_mixed_derivative':mp.nstr(actual,65),'certified_raw_upper':mp.nstr(upper,65),
    'actual_over_bound':float(abs(actual)/upper),'scope':'one entry at frozen adversarial point; sampled global maximum may use another point'}
def main():
  meter=Monitor('CPU high precision geometry crosschecks');mp.mp.dps=60;rows=[]
  try:
    for case in DATA['cases']:
      meter.check();row=json.loads((ROOT/f"result_{case['name']}.json").read_text());checks=[]
      for kind in ['accepted_grid','product','packing']:
        if kind=='product' and row['products']['best'] is None:continue
        fname={'accepted_grid':'accepted_grid','product':'product','packing':'packing'}[kind]
        archive=np.load(ROOT/f"{fname}_{case['name']}.npz")
        pair=row['accepted_grid']['closest_pair'] if kind=='accepted_grid' else row['products']['best']['closest_pair'] if kind=='product' else row['packing']['closest_pair']
        hs=[];ss=[];alphas=[]
        for index in pair:
          h,S,a=refine(case,archive['X'][index]);hs.append(h);ss.append(S);alphas.append(mp.norm(a,mp.inf))
        dist=exact_queries(model(case),ss[0]-ss[1]);forwardgap=mp.norm(hs[0]-hs[1],mp.inf)
        mid=row['accepted_grid']['min_query'] if kind=='accepted_grid' else row['products']['best']['min_query'] if kind=='product' else row['packing']['min_query']
        checks.append({'kind':kind,'digits':60,'query_distance':mp.nstr(dist,65),'binary64_distance':mid,
          'absolute_difference':float(abs(dist-mid)),'fixed_h_gap':mp.nstr(forwardgap,65),
          'max_normal_refinement':mp.nstr(max(alphas),65),'passes_2epsilon':dist>mp.mpf('.002')})
      # One separate 100-digit pass at the primary product's closest pair.
      if row['products']['best']:
        mp.mp.dps=100;archive=np.load(ROOT/f"product_{case['name']}.npz");pair=row['products']['best']['closest_pair']
        one=refine(case,archive['X'][pair[0]])[1];two=refine(case,archive['X'][pair[1]])[1]
        higher=exact_queries(model(case),one-two)
        checks.append({'kind':'product_100_digit','digits':100,'query_distance':mp.nstr(higher,105),
          'passes_2epsilon':higher>mp.mpf('.002')});mp.mp.dps=60
      curvature=curvature_check(case,row)
      rows.append({'name':case['name'],'checks':checks,'curvature_crosscheck':curvature})
      print(case['name'],[(v['kind'],v['passes_2epsilon']) for v in checks],flush=True)
    (ROOT/'high_precision_checks.json').write_text(json.dumps(rows,indent=2)+'\n')
  finally:meter.finish()
if __name__=='__main__':main()
