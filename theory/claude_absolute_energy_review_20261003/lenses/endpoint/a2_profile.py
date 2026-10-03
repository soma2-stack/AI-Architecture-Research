import numpy as np
from model import build, fixed_point, B0
for n in (200, 800, 1600, 3200):
    M = build(n); R=M['R']; k=M['k']; d=M['d']; O=M['O']; a=M['a']
    h,res = fixed_point(R, B0*np.ones(n))
    hm=h[:k]
    pre = R@h + B0
    idx=[0,1,2,3,4,5,8,12,20,40,d//2,d-2,d-1,d,d+1,k-1]
    print(n, 'res',res, 'profile', [(i, round(hm[i],4)) for i in idx])
    # decomposition of preactivation of coords i>=2 in cycle: a*h_{i-1} + b0 + correction
    corr = pre[:k] - B0 - a*np.r_[0, hm[:-1]]
    print('   corr (pre_i - b0 - a h_{i-1}) for i=2..6 and d-1:', [round(corr[i],4) for i in (2,3,4,5,6,d-1)], ' non-cycle corr (pre_j - b0 - a h_j):', round(pre[d+1]-B0-a*hm[d+1],5))
    print('   sum mem/sqrt(k)=', round(hm.sum()/np.sqrt(k),4), ' pre_1=', round(pre[1],4), ' b0*sqrt(k)=', round(B0*np.sqrt(k),4), 'h1=',round(hm[1],4),'gate1=',round(1-hm[1]**2,4), '#|h|>.9', int(np.sum(abs(hm)>.9)))
