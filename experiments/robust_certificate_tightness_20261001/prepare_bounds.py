"""Read accepted bounds; regenerate only archived raw tensors needed for ratios."""
import sys,json,hashlib
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
ROOT=Path(__file__).parent;REPO=ROOT.parents[1]
OLD=REPO/'experiments/robust_witness_search_20261001'
sys.path.append(str(OLD))
import cpu_jets as c
import certificate_kernel as e
from resources import Monitor
def model(case):
    m=c.Model(case['case'],case['n']);saved=DATA['models']['dense_parameters'][str(case['n'])]
    full=list(map(Q,saved));n=case['n']
    m.params=full if case['case']=='dense' else [Q(6+3*i,20) for i in range(n)]+full[n*n:]
    return m
DATA=json.loads((ROOT/'inputs.json').read_text())
def main():
  meter=Monitor('CPU bounds and upper cover');e.I.precision(192)
  try:
    for case in DATA['cases']:
      meter.check();m=model(case);n=case['n'];cert=case['certificate'];r=cert['r']
      scales={g:e.I(sum(m.params[p]**2 for p,(_,_,name,_) in enumerate(m.meta) if name==g)/sum(name==g for _,_,name,_ in m.meta)).sqrt() for g in ['R','W','b']}
      X=[[Q(v) for v in row] for row in case['X']]
      BI=[[e.I(Q(v))*e.I(Q(3,32)).sqrt() for v in row[:n+r]] for row in case['B']]
      base={'n':n,'model':m,'X':X,'BI':BI,'scaleI':scales}
      if case['curvature_source']:
        source=np.load(REPO/case['curvature_source']);HH,HS=source['HH'],source['HS']
      else:
        aa=list(map(Q,cert['a_i']));amps=[Q(cert['a0'])*Q(cert['hidden_factor'])]*n+aa
        HH,HS=e.curvature(base,r,amps)
      np.savez_compressed(ROOT/f"bounds_{case['name']}.npz",HH=HH,HS=HS)
      # A conservative rigorous coordinate cover of the entire raw history cube.
      R=[[Q(0) for _ in range(n)] for _ in range(n)]
      for i,j,p in m.layers[0]['R']:R[i][j]=abs(m.params[p])
      S=[[Q(0) for _ in range(m.P)] for _ in range(n)]
      for xx in X:
        new=[[sum(R[i][j]*S[j][p] for j in range(n)) for p in range(m.P)] for i in range(n)]
        for p,(_,i,g,j) in enumerate(m.meta):new[i][p]+=1 if g!='W' else abs(xx[j])+1
        S=new
      sqrtD=Q(e.I(len(m.support)).sqrt().hi,e.I.scale)
      B=[S[i][p]*Q(scales[m.meta[p][2]].hi,e.I.scale) for i,p in m.support]
      counts=[max(1,(v*sqrtD/Q(1,1000)).__ceil__()) for v in B]
      states=int(np.prod(np.array(counts,dtype=object)))
      obj={'label':'RIGOROUS but loose covering upper bound','D':len(B),'counts':counts,
        'normalized_coordinate_bounds':[str(v) for v in B],'states_upper':str(states),
        'bits_upper':sum(np.log2(float(v)) for v in counts),'query_Lipschitz_upper':1,
        'proof':'|tanh|,|tanh_prime|<=1; positive sensitivity recurrence; normalized c norm<=1; coordinate cell side<=2epsilon/sqrt(D), query diameter<=2epsilon'}
      (ROOT/f"upper_{case['name']}.json").write_text(json.dumps(obj,indent=2)+'\n')
      print(case['name'],'upper bits',obj['bits_upper'],flush=True)
  finally:meter.finish()
if __name__=='__main__':main()
