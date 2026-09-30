import core as c
import unittest
from fractions import Fraction as Q
import numpy as np
import mpmath as mp
import torch
from interval import I,certify

class Tests(unittest.TestCase):
    def test_RTRL_BPTT_endpoint_J(self):
        for case in ('dense','independent','shared_linear','deep'):
            m=c.Model(case);X=c.inputs(c.CFG['development_seed'],3);before=m.serialize()
            F,J,S=c.jets(m,X);f,j=c.autograd(m,X)
            self.assertLess(c.relative(F,f),1e-12);self.assertLess(c.relative(J,j),1e-12)
            self.assertEqual(before,m.serialize())
    def test_deterministic(self):
        self.assertEqual(c.inputs(9,5),c.inputs(9,5));self.assertNotEqual(c.inputs(9,5),c.inputs(10,5))
        self.assertNotIn(c.CFG['development_seed'],c.CFG['seeds'])
        self.assertEqual(c.Model('dense').serialize(),c.Model('dense').serialize())
    def test_counting_structural_zeros(self):
        for case in c.CFG['cases']:
            m=c.Model(case);cfg=c.CFG['cases'][case]
            self.assertEqual(m.P,cfg['P']);self.assertEqual(m.dimension,cfg['endpoint_dimension'])
            self.assertEqual(cfg['T'],(m.dimension+1)//2)
            _,_,S=c.jets(m,c.inputs(1,3))
            self.assertTrue(all(S[i,p]==0 for i in range(m.N) for p in range(m.P) if (i,p) not in m.support))
    def test_shared_exact_factors(self):
        m=c.Model('shared_linear');X=c.inputs(3,5);F,J,S=c.jets(m,X)
        ex=np.zeros(2);eh=np.zeros(2);h=np.zeros(2)
        W=np.array([[.5,.125],[-.0625,.4375]]);b=np.array([1/64,-2/64])
        for row in X:
            ex=.35*ex+np.array(row,dtype=float);eh=.35*eh+h
            h=.35*h+W@np.array(row,dtype=float)+b
        self.assertLess(c.relative(F[:2],W@ex+b*sum(.35**i for i in range(5))),1e-12)
        eb=sum(.35**i for i in range(5))
        for p,(layer,owner,name,j) in enumerate(m.meta):
            expected=eb if name=='b' else eh[owner] if name=='R' else ex[j]
            self.assertAlmostEqual(S[owner,p],expected)
        self.assertEqual(np.linalg.matrix_rank(J,tol=1e-10),4)
    def test_independent_compact_rule(self):
        m=c.Model('independent');X=c.inputs(c.CFG['development_seed'],5)
        h=np.zeros(2);eligibility=np.zeros(m.P)
        for row in X:
            x=np.array(row,dtype=float);old=h.copy();z=np.zeros(2)
            for p,(_,owner,name,j) in enumerate(m.meta):
                z[owner]+=float(m.params[p])*(old[j] if name=='R' else x[j] if name=='W' else 1)
            h=np.tanh(z)
            for p,(_,owner,name,j) in enumerate(m.meta):
                r=float(m.params[owner]);direct=old[j] if name=='R' else x[j] if name=='W' else 1
                eligibility[p]=(1-h[owner]**2)*(r*eligibility[p]+direct)
        F,_,S=c.jets(m,X)
        self.assertLess(c.relative(h,F[:2]),1e-12)
        for p,(_,owner,_,_) in enumerate(m.meta):self.assertAlmostEqual(eligibility[p],S[owner,p])
    def test_saved_certificate_rejection(self):
        import json,copy
        from verify import verify
        paths=sorted(c.ROOT.glob('certificate_shared_linear_*.json'))
        if not paths:self.skipTest('Official certificates not collected yet')
        path=paths[0]
        data=json.loads(path.read_text());self.assertTrue(verify(data)['verified'])
        broken=copy.deepcopy(data);broken['preconditioner']=[['0']*4 for _ in range(4)]
        with self.assertRaises(AssertionError):verify(broken)
    def test_high_precision(self):
        mp.mp.dps=100;m=c.Model('dense');X=c.inputs(8,3)
        f,j,_=c.jets(m,X);F,J,_=c.jets(m,X,'mp')
        self.assertLess(c.relative(j,J),1e-12);self.assertLess(c.relative(f,F),1e-12)
    def test_endpoint_finite_difference(self):
        m=c.Model('dense');X=c.inputs(8,3);F,J,_=c.jets(m,X);eps=Q(1,100000)
        for k in range(6):
            xp=[r.copy() for r in X];xm=[r.copy() for r in X];xp[k//2][k%2]+=eps;xm[k//2][k%2]-=eps
            fp=c.jets(m,xp)[0];fm=c.jets(m,xm)[0]
            self.assertLess(c.relative((np.array(fp)-np.array(fm))/(2*float(eps)),J[:,k]),1e-8)
    def test_interval_arithmetic(self):
        I.precision(128)
        for a in (Q(1,3),Q(-2,7),Q(3,2)):
            for b in (Q(-1,5),Q(7,9)):
                self.assertTrue((I(a)+I(b)).contains(a+b));self.assertTrue((I(a)*I(b)).contains(a*b))
                self.assertTrue((I(a)/I(b)).contains(a/b))
    def test_interval_exp_tanh(self):
        mp.mp.dps=100;I.precision(256)
        for q in (Q(-2),Q(-1,3),Q(0),Q(2)):
            value=mp.mpf(q.numerator)/q.denominator
            self.assertTrue(I(q).exp().contains(Q(mp.nstr(mp.exp(value),95))))
            self.assertTrue(I(q).tanh().contains(Q(mp.nstr(mp.tanh(value),95))))
    def test_interval_jet_enclosures(self):
        mp.mp.dps=100;I.precision(256);m=c.Model('dense');X=c.inputs(8,3)
        _,j,_=c.jets(m,X,'mp');_,J,_=c.jets(m,X,'interval')
        for a,b in zip(j.flat,J.flat):self.assertTrue(I.cast(b).contains(Q(mp.nstr(a,95))))
    def test_certification_and_rejection(self):
        I.precision(128);scale=I.scale
        matrix=[[I(2),I(1)],[I(1),I(1)]];M=[[scale,-scale],[-scale,2*scale]]
        self.assertTrue(certify(matrix,M)['verified'])
        self.assertFalse(certify([[I(1),I(2)],[I(2),I(4)]],[[scale,0],[0,scale]])['verified'])
    def test_CPU(self):
        h=c.hardware();self.assertIsNone(torch.version.cuda);self.assertEqual(h['device'],'cpu')
        self.assertEqual(torch.get_default_dtype(),torch.float64)
    def test_augmented_step_determinant_factorization(self):
        for n in (2,3):
            m=c.Model('dense',n);R=torch.zeros(n,n);W=torch.zeros(n,n);b=torch.zeros(n)
            for p,(_,i,name,j) in enumerate(m.meta):
                if name=='R':R[i,j]=float(m.params[p])
                if name=='W':W[i,j]=float(m.params[p])
                if name=='b':b[i]=float(m.params[p])
            x=torch.tensor([.1]*n);z=torch.linspace(-.1,.1,m.dimension)
            def step(zz):
                h=zz[:n];S=zz[n:].reshape(n,m.P);new=torch.tanh(R@h+W@x+b)
                G=torch.diag(1-new**2);direct=torch.zeros(n,m.P)
                for p,(_,i,name,j) in enumerate(m.meta):direct[i,p]=h[j] if name=='R' else x[j] if name=='W' else 1
                return torch.cat([new,(G@(R@S+direct)).reshape(-1)])
            A=torch.diag(1-torch.tanh(R@z[:n]+W@x+b)**2)@R
            actual=torch.linalg.det(torch.autograd.functional.jacobian(step,z));expected=torch.linalg.det(A)**(m.P+1)
            self.assertLess(abs(float(actual/expected-1)),1e-12)
    def test_width_counts_and_cross_structure(self):
        for n in (2,3,4):
            for case in ('dense','deep','independent','shared_linear'):
                m=c.Model(case,n);p=2*n*n+n
                if case=='dense':self.assertEqual((m.P,m.dimension),(p,n*(p+1)))
                elif case=='deep':self.assertEqual((m.P,m.dimension),(2*p,2*n+3*n*p))
                else:self.assertEqual((m.P,m.dimension),(n*n+2*n,n*n+3*n))
                _,_,S=c.jets(m,c.inputs(c.CFG['development_seed'],3,n))
                self.assertTrue(all(S[i,p]==0 for i in range(m.N) for p in range(m.P) if (i,p) not in m.support))
    def test_wider_AD_and_high_precision(self):
        for n in (3,4):
            for case in ('dense','deep'):
                m=c.Model(case,n);X=c.inputs(c.CFG['development_seed'],3,n);before=m.serialize()
                F,J,_=c.jets(m,X);f,j=c.autograd(m,X)
                self.assertLess(c.relative(F,f),1e-12);self.assertLess(c.relative(J,j),1e-12)
                mp.mp.dps=100;mf,mj,_=c.jets(m,X,'mp')
                self.assertLess(c.relative(J,mj),1e-12);self.assertEqual(m.serialize(),before)
    def test_wider_shared_factor_ceiling(self):
        for n in (3,4):
            m=c.Model('shared_linear',n);X=c.inputs(c.CFG['development_seed'],n+3,n)
            F,J,S=c.jets(m,X);ex=np.zeros(n);eh=np.zeros(n);h=np.zeros(n)
            W=np.zeros((n,n));b=np.zeros(n)
            for p,(_,i,name,j) in enumerate(m.meta):
                if name=='W':W[i,j]=float(m.params[p])
                if name=='b':b[i]=float(m.params[p])
            for row in X:
                x=np.array(row,dtype=float);ex=.35*ex+x;eh=.35*eh+h;h=.35*h+W@x+b
            eb=sum(.35**i for i in range(len(X)))
            for p,(_,i,name,j) in enumerate(m.meta):
                expected=eb if name=='b' else eh[i] if name=='R' else ex[j]
                self.assertAlmostEqual(S[i,p],expected)
            self.assertEqual(np.linalg.matrix_rank(J,tol=1e-10),2*n)

if __name__=='__main__':
    meter=c.Meter('Endpoint development unit checks')
    try:unittest.main(verbosity=2)
    finally:meter.finish()
