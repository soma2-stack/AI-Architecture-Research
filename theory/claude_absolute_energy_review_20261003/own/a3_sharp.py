import mpmath as mp
mp.mp.dps=50
b0=mp.mpf(1)/20
def S(n):
    n=mp.mpf(n); k=mp.floor(n/2); l=n-k; a=1-1/n; lam=1/(100*n); en=4/(10**8*n**2)
    cstar=mp.sqrt(k)-1/(mp.sqrt(k)-1)
    mem=max(mp.mpf(0),b0*cstar-a)
    return mp.sqrt(l*(b0-lam)**2+mem**2)-en*mp.sqrt(n)
def L(n):
    n=mp.mpf(n); l=n-mp.floor(n/2); return (b0-1/(100*n))*mp.sqrt(l)-4/(10**8*n**2)*mp.sqrt(n)
worst=(None,mp.inf)
ns=list(range(200,20001))+[int(mp.mpf(10)**(e/4)) for e in range(17,121)]
for n in ns:
    m=S(n)-(b0*mp.sqrt(n)-mp.mpf('0.709'))
    if m<worst[1]: worst=(n,m)
print("min over n of S_n-(b0 sqrt n-0.709):",worst[0],mp.nstr(worst[1],8))
print("first n with memory term>0:",next(n for n in range(200,2000) if S(n)>L(n)+mp.mpf('1e-30')))
# sharp threshold vs claimed, for several R
for R in [0.5,1,2,10,100,1000]:
    first=next((n for n in range(200,10**9) if S(n)>R),None) if R<=10 else None
    lo=400*R**2; up=min(mp.mpf(200000000)/249001*R**2, 400*(R+mp.mpf('0.709'))**2)
    print(f"R={R}: nonempty for 200<=n<={float(lo):.1f}; empty for n>={float(max(200,up)):.1f} (claimed 803.21R^2={803.2096256641539*R**2:.1f})" + (f"; first n with S_n>R: {first}" if first else ""))
