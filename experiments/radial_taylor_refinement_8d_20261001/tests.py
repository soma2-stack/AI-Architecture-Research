import time
CPU=time.process_time();WALL=time.perf_counter()
import common as c
from fractions import Fraction as Q
import numpy as np
from exact_gate import roots,evaluate,POLYS,gate_majorants
checks=[];I=c.ref.I
def check(n,ok):
    checks.append({'name':n,'passed':bool(ok)})
    assert ok,n
if __name__=='__main__':
    d=c.candidate()
    check('candidate_byte_exact',c.sha(c.ROOT/'candidate.json')==c.sha(c.REPO/'experiments/third_order_antipodal_8d_20261001/candidate.json'))
    for bits in (192,256):
        I.precision(bits)
        for j,rr in enumerate(roots()):
            derivative=[(i+1)*v for i,v in enumerate(POLYS[j][1:])]
            check(f'{bits}_complete_polynomial_roots_{j+1}',all(evaluate(derivative,x).lo<=0<=evaluate(derivative,x).hi for x in rr))
        for l,u in ((Q(-3,4),Q(3,4)),(Q(1,4),Q(1,2)),(Q(-7,8),Q(-3,4))):
            x=I(l).lo;y=I(u).hi;bounds=gate_majorants([I(x,y,True)])
            for j in range(4):
                points=[l+(u-l)*k/128 for k in range(129)]
                exact=[abs(sum(Q(v)*p**i for i,v in enumerate(POLYS[j]))) for p in points]
                check(f'{bits}_gate_{j+1}_rational_samples_{l}_{u}',Q(float(bounds[j][0]))>=max(exact))
    weights=[((1-Q(j,8))**3-(1-Q(j+1,8))**3)/3 for j in range(8)]
    check('radial_weights_positive_and_sum',all(w>0 for w in weights) and sum(weights)==Q(1,3))
    check('constant_radial_bound_recovers_one_sixth',sum(w*Q(7,5)/2 for w in weights)==Q(7,30))
    B=np.array([[float(Q(v)) for v in row] for row in d['B']])
    check('prefix_normals_zero',np.all(B[:-4,:4]==0) and np.array_equal(B[-4:,:4],np.eye(4)))
    c.sys.path.insert(0,str(c.REPO/'experiments/independent_dimension_feasibility_20261001'))
    import numerics as n
    m=n.Model();a=np.array([float(Q(v)) for v in d['a']]);ah=float(Q(d['ah']));sec=n.Section(m,B,a,ah)
    errors=[]
    for z in (np.zeros(8),np.linspace(-.25,.25,8),np.linspace(.25,-.25,8)):
        s,valid,y=sec.points(z);t=a*z;w=np.r_[y[0],t]
        h2,s2,_,_=m.forward(w,B)
        check('fixed_h_identity_'+str(len(errors)),bool(valid[0]) and max(abs(h2-m.h0))<1e-12)
        errors.append(float(max(abs(s[0]-s2))))
        h=np.zeros(4);S=np.zeros(24)
        for step,x0 in enumerate(m.X[:-1]):
            x=x0+B[4*step:4*step+4]@w*n.SD
            hn=np.tanh(m.R*h+m.W@x+m.b);g=1-hn**2
            S=g[m.owner]*(m.rd*S+m.inject(h,x));h=hn
        x=(np.arctanh(m.h0)-m.R*h-m.b)@m.Winv.T
        reconstructed=(1-m.h0**2)[m.owner]*(m.rd*S+m.inject(h,x))*m.sw
        check('last_step_RTRL_elimination_'+str(len(errors)),max(abs(reconstructed-s2))<1e-12)
    check('direct_frozen_RTRL_section_parity',max(errors)<1e-12)
    hardware=c.ref.a.c.hardware();check('CPU_only',c.ref.a.c.torch.ones(1).device.type=='cpu')
    for p in c.ROOT.glob('*.py'):compile(p.read_text(),str(p),'exec')
    check('all_sources_compile',True)
    c.write('tests.json',{'checks':checks,'passed':len(checks),'CPU_seconds':time.process_time()-CPU,
      'wall_seconds':time.perf_counter()-WALL,'section_RTRL_errors':errors,'hardware':hardware})
    print('PASS',len(checks),'synthetic checks')
