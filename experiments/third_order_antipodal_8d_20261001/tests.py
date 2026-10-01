"""Pre-official synthetic arithmetic and immutable-selection tests."""
import time
CPU=time.process_time();WALL=time.perf_counter()
import common as c
import numpy as np
from fractions import Fraction as Q
k=c.k;I=k.I;checks=[]
def check(name,condition):
    checks.append({'name':name,'passed':bool(condition)})
    assert condition,name
if __name__=='__main__':
    c.verify();d=c.candidate();r=d['r'];B=c.rational_rows(d['B'])
    old=c.json.loads((c.REPO/'experiments/independent_dimension_feasibility_20261001/dimension_8.json').read_text())
    selected=next(v for v in old['cases'] if v['basis']=='query_svd' and v['style']=='proxy')
    check('candidate_amplitudes_exact_binary_values',[Q(v) for v in d['a']]==[Q(float(v)) for v in selected['a']])
    check('normal_amplitude_exact_binary_value',Q(d['ah'])==Q(float(selected['ah'])))
    check('eight_tangents_four_normals',r==8 and len(B)==148 and all(len(row)==12 for row in B))
    frozenB=np.load(c.REPO/'experiments/independent_dimension_feasibility_20261001/bases.npz')['query_svd'][:,:12]
    check('all_basis_entries_exact_unchanged',all(v==Q(float(frozenB[i,j])) for i,row in enumerate(B) for j,v in enumerate(row)))
    check('last_input_normal_chart',all(B[i][j]==int(i==144+j) for i in range(148) for j in range(4)))
    check('preconditioners_nonsingular',bool(k.inverse(c.rational_rows(d['K_hidden']))) and bool(k.inverse(c.rational_rows(d['K_selected']))))
    check('epsilon_unchanged',Q(d['epsilon'])==Q(1,1000))
    for bits in (192,256):
        I.precision(bits);x=I(Q(2,7));y=I(Q(-3,11))
        for name,v,target in [('sum',x+y,Q(2,7)-Q(3,11)),('product',x*y,-Q(6,77)),('inverse',1/x,Q(7,2))]:
            check(f'interval_{bits}_{name}',Q(v.lo,I.scale)<=target<=Q(v.hi,I.scale))
        q=I(Q(3,32)).sqrt();check(f'interval_{bits}_sqrt',Q(q.lo,I.scale)**2<=Q(3,32)<=Q(q.hi,I.scale)**2)
        check(f'interval_{bits}_tanh_zero',I(0).tanh().lo<=0<=I(0).tanh().hi)
    A=np.arange(8,dtype=float).reshape(1,2,2,2)/8;V=np.array([[1.,2.],[3.,4.]])
    t=k.contract3(A,V)
    exact=np.einsum('ijkl,ja,kb,lc->iabc',A,V,V,V)
    check('all_mixed_third_contractions_upward',np.all(t>=exact) and np.max(t-exact)<1e-9)
    hardware=k.a.c.hardware();check('CPU_execution',hardware is not None and k.a.c.torch.ones(1).device.type=='cpu')
    check('accepted_kernel_byte_identical',c.sha(c.ROOT/'reviewed_kernel.py')==c.sha(c.REPO/'experiments/rebalanced_7d_section_20261001/kernel.py'))
    check('all_frozen_sources_and_history_preserved',bool(c.verify()))
    c.write('tests.json',{'checks':checks,'passed':len(checks),'cpu_seconds':time.process_time()-CPU,
                          'wall_seconds':time.perf_counter()-WALL,'hardware':hardware,'gpu_used':False})
    print('PASS',len(checks),'checks')
