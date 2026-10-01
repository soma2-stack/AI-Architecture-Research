"""Fixed-history intervals and epsilon-essential continuous-section bounds."""
from resources import ROOT,CFG
import sys,json,hashlib,math
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
import mpmath as mp
REPO=ROOT.parents[1];OLD=REPO/'experiments/robust_witness_search_20261001'
sys.path.append(str(OLD))
import cpu_jets as c
import certificate_kernel as e
INPUT=json.loads((REPO/'experiments/robust_certificate_tightness_20261001/inputs.json').read_text())
EPS=Q(CFG['epsilon']);ORIGINAL_QUERY=e.query_margins

def model(case):
 m=c.Model(case['case'],case['n']);n=m.n;full=list(map(Q,INPUT['models']['dense_parameters'][str(n)]))
 m.params=full if case['case']=='dense' else [Q(6+3*i,20) for i in range(n)]+full[n*n:]
 return m

def structured_query(base,L):
 if not base['model'].diagonal:return ORIGINAL_QUERY(base,L)
 m=base['model'];n=m.n;diag=[m.params[p] for i,j,p in m.layers[0]['R']]
 R=[[diag[i]*int(i==j) for j in range(n)] for i in range(n)]
 W=[[Q(0) for _ in range(n)] for _ in range(n)]
 for i,j,p in m.layers[0]['W']:W[i][j]=m.params[p]
 e.inverse(W)
 factor=e.I(n*max(Q(1),sum(x*x for x in diag))).sqrt()
 margins=[]
 for ell in L:
  total=sum(Q(v)**2/diag[i]**2 for v,(i,p) in zip(ell,m.support))
  margins.append(Q((e.I(Q(7,8))/(factor*e.I(total).sqrt())).lo,e.I.scale))
 # 7/8 is a permitted gate; do not expose impossible residual coordinates.
 low=e.I(1)-e.I(Q(3,4)).tanh().square();high=e.I(1)-e.I(Q(1,4)).tanh().square()
 assert Q(low.hi,e.I.scale)<Q(7,8)<Q(high.lo,e.I.scale)
 return margins,R
e.query_margins=structured_query

def float_frame(case):
 m=model(case);n=m.n;X=[[Q(v) for v in row] for row in case['X']]
 _,J,_=c.jets(m,X,'float');H=J[:n]
 scales={g:np.sqrt(float(sum(m.params[p]**2 for p,(_,_,name,_) in enumerate(m.meta) if name==g)/sum(name==g for _,_,name,_ in m.meta))) for g in ['R','W','b']}
 S=J[n:]*np.array([scales[m.meta[p][2]] for i,p in m.support])[:,None]*np.sqrt(3/32)
 A=S-S@H.T@np.linalg.solve(H@H.T,H)
 U,s,V=np.linalg.svd(A,full_matrices=False);normal,_=np.linalg.qr(H.T,mode='reduced')
 B=np.c_[normal,V[:8].T]
 dy=lambda x:Q(round(float(x)*2**128),2**128)
 return {'B':[[str(dy(x)) for x in row] for row in B], 'U':[[str(dy(x)) for x in row] for row in U[:,:8].T], 'sigma':[str(dy(x)) for x in s[:8]]}

def projectors(base,r,rule):
 if rule=='frame':
  e.query_margins=ORIGINAL_QUERY
  try:return e.frame_projection(base,r)
  finally:e.query_margins=structured_query
 assert base['model'].diagonal and rule=='supported'
 m=base['model'];U=base['U'][:r];weight=[m.params[i]**2 for i,p in m.support]
 Gram=[[sum(U[i][d]*weight[d]*U[j][d] for d in range(len(weight))) for j in range(r)] for i in range(r)]
 inv=mp.matrix([[e.mpq(x) for x in row] for row in Gram])**-1
 return [[e.dyadic(e.mpq(weight[d])*sum(e.mpq(U[k][d])*inv[k,j] for k in range(r))) for d in range(len(weight))] for j in range(r)]

def base_for(case,frame,bits,meter=None,JI=None):
 mp.mp.dps=100;e.I.precision(bits);m=model(case);n=m.n
 c.ACTIVE_METER=meter;X=[[Q(v) for v in row] for row in case['X']]
 before=m.serialize()
 if JI is None:_,JI,_=c.jets(m,X,'interval')
 assert before==m.serialize()
 scales={g:e.I(sum(m.params[p]**2 for p,(_,_,name,_) in enumerate(m.meta) if name==g)/sum(name==g for _,_,name,_ in m.meta)).sqrt() for g in ['R','W','b']}
 B=[[Q(v) for v in row] for row in frame['B']];sd=e.I(Q(3,32)).sqrt()
 BI=[[e.I(x)*sd for x in row] for row in B]
 reduced=e.matmul(JI.tolist(),BI)
 for d,(i,p) in enumerate(m.support):reduced[n+d]=[v*scales[m.meta[p][2]] for v in reduced[n+d]]
 return {'n':n,'model':m,'X':X,'B':B,'BI':BI,'reduced':reduced,'JI':JI,'scaleI':scales,'U':[[Q(v) for v in row] for row in frame['U']],'sigma':list(map(Q,frame['sigma']))}

def upnorm(A):
 v=sum(Q(x)**2 for row in A for x in row)
 return Q(e.I(v).sqrt().hi,e.I.scale)

def dimension_bound(base,cert,HH,HS,fraction=Q(1)):
 """A continuous projection-coordinate section; all interval residuals included."""
 n=base['n'];r=cert['r'];m=base['model'];J=[row[:n+r] for row in base['reduced']]
 L=[list(map(Q,row)) for row in cert['selected_projection']]
 margins=structured_query(base,L)[0]
 rho=[Q(x)*fraction for x in cert['rho_i']]
 b=[x*y for x,y in zip(rho,margins)]
 kept=[i for i,x in enumerate(b) if x>EPS];q=len(kept)
 # Upper absolute derivative, including hidden compensation and projection inverse.
 amps=[Q(cert['a0'])*Q(cert['hidden_factor'])]*n+list(map(Q,cert['a_i']))
 SJ=[]
 for d,row in enumerate(J[n:]):
  SJ.append([row[j].absq()+sum(Q(float(HS[d,j,k]))*amps[k] for k in range(n+r)) for j in range(n+r)])
 Gamma=[[Q(float(x)) for x in row] for row in cert['normal_first_derivative_upper']]
 fixed=[[SJ[d][n+j]+sum(SJ[d][k]*Gamma[k][j] for k in range(n)) for j in range(r)] for d in range(len(m.support))]
 E=[[Q(float(x)) for x in row] for row in cert['scaled_jacobian_residual_upper']]
 neumann=e.inverse([[Q(int(i==j))-E[i][j] for j in range(r)] for i in range(r)])
 assert all(x>=0 for row in neumann for x in row)
 a=list(map(Q,cert['a_i']));K=[list(map(Q,row)) for row in cert['K_selected']]
 inverse_bound=[[a[i]*sum(neumann[i][k]*abs(K[k][j])/a[k] for k in range(r)) for j in range(r)] for i in range(r)]
 T=[[sum(fixed[d][k]*inverse_bound[k][j] for k in range(r))*rho[j] for j in kept] for d in range(len(fixed))]
 M=upnorm(T) if q else Q(0)
 minb=min((b[i] for i in kept),default=Q(0))
 mlower=Q((e.I(minb)/e.I(q).sqrt()).lo,e.I.scale) if q else Q(0)
 N=[int(2*x//(Q(17,8)*EPS))+1 for x in b];states=math.prod(N)
 out={'fraction':str(fraction),'geometric_dimension':r,'epsilon_essential_dimension':q,'retained_indices':kept,
   'b_i':[str(x) for x in b],'rho_i':[str(x) for x in rho],'mu_i':[str(x) for x in margins],
   'm_Euclidean_lower':str(mlower),'M_Euclidean_upper':str(M),'antipodal_half_margin_lower':str(minb),
   'coordinate_collision_scale_upper':str(2*EPS/mlower) if mlower else None,
   'states':str(states),'counts':N,'bits':math.log2(states),'label':'CERTIFIED on curved fixed-h lift; not maximum dimension',
   'query_upper_used':'D_C<=Frobenius normalized sensitivity difference',
   'discarded_axis_reasons':['observable half-range<=epsilon' if i not in kept else 'retained' for i in range(r)]}
 return out

def current_frame(case):
 r=case['certificate']['r']
 return {'B':[row[:case['n']+r] for row in case['B']],'U':case['U'][:r],'sigma':['1']*r}

def source_manifest():
 prior=REPO/'experiments/robust_certificate_tightness_20261001'
 files=[p for p in prior.iterdir() if p.is_file()]
 files.extend(p for p in OLD.iterdir() if p.is_file() and p.suffix in ['.py','.json','.md'])
 files.append(REPO/'AGENTS.md')
 return {p.relative_to(REPO).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
