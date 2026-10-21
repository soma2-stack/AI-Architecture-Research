"""Independent saturation and conditioning checks; no author imports."""
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
import mpmath as mp
import json
HERE=Path(__file__).resolve().parent
mp.mp.dps=90

def poly(roots):
    c=[F(1)]
    for root in roots:
        nxt=[F(0)]*(len(c)+1)
        for j,v in enumerate(c):nxt[j]-=root*v;nxt[j+1]+=v
        c=nxt
    return c

def main():
    rows=[]
    for D in [2,3,4]:
        r=2*D-1;nodes=[F(-1)+F(2*j,r-1) for j in range(r)]
        M=mp.matrix(r,D)
        for i,t in enumerate(nodes):
            x=mp.mpf(t.numerator)/t.denominator
            for j in range(D):M[i,j]=x**j
        smallest=mp.inf;singular_theta=None
        for I in combinations(range(r),D):
            det=F(1)
            for j in range(D):
                for k in range(j+1,D):det*=nodes[I[k]]-nodes[I[j]]
            assert det!=0
            sub=mp.matrix([[M[i,j] for j in range(D)] for i in I])
            vals,vecs=mp.eigsy(sub.T*sub)
            if vals[0]<smallest:
                smallest=vals[0];singular_theta=vecs[:,0]
        delta=mp.sqrt(smallest)/mp.sqrt(D);L=1/delta
        thetas=[singular_theta]
        for I in [tuple(range(D-1)),tuple(range(r-D+1,r))]:
            c=poly([nodes[j] for j in I]);v=mp.matrix([mp.mpf(a.numerator)/a.denominator for a in c]);v/=mp.norm(v);thetas.append(v)
        for j in range(D):thetas.append(mp.eye(D)[:,j])
        min_sat=r
        for theta in thetas:
            raw=L*M*theta
            z=[max(mp.mpf(-1),min(mp.mpf(1),a)) for a in raw]
            sat=sum(abs(a)==1 for a in z);min_sat=min(min_sat,sat)
            assert sat>=r-D+1
            zm=[max(mp.mpf(-1),min(mp.mpf(1),a)) for a in -raw]
            assert all(a==-b for a,b in zip(z,zm))
        rows.append({'D':D,'r':r,'L_90digit_numeric':mp.nstr(L,25),'min_saturated':min_sat,
                     'all_full_spark_determinants_exact_nonzero':True})
    # Rigorous lower bound on L at the minimum theorem size D=89, using ONE submatrix.
    D=89;roots=[F(-1)+F(j,D-1) for j in range(D-1)];c=poly(roots)
    p0=abs(c[0]);maxcoeff=max(abs(x) for x in c)
    # theta=c/||c||: first D-1 rows vanish and last row (node0) has |p0|/||c||.
    # sigma_min<=|p0|/||c||, L>=sqrt(D)||c||/|p0| >=maxcoeff/|p0|.
    lower=maxcoeff/p0
    decimal_power=0
    while F(10)**(decimal_power+1)<=lower:decimal_power+=1
    out={'finite_saturation_tests':rows,'conditioning_D89':{'L_lower_gt_10_power':decimal_power,
          'L_lower_exact':str(lower),'meaning':'rigorous conditioning lower bound, not a counterexample to exact-real code'}}
    (HERE/'independent_code_result.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
