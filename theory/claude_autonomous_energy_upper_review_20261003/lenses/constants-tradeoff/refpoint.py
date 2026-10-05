# Reference (R0) autonomous fixed point, numerical sanity only (not a certificate).
import numpy as np, time, sys
def rotate(v, n):
    k, d = n//2, n//4
    tau = 1/np.sqrt(k)
    w = -np.full(k,tau); w[0] += 1
    gamma = 1/(1-tau)
    u = v-gamma*w*(w@v)
    u[:d] = np.roll(u[:d],1)
    return u-gamma*w*(w@u)
for n in [int(x) for x in sys.argv[1:]]:
    t0=time.time(); k=n//2; a=1-1/n
    h=np.zeros(n); it=0
    while True:
        nxt=np.empty(n)
        nxt[:k]=np.tanh(a*rotate(h[:k],n)+.05)
        nxt[k:]=np.tanh(h[k:]/(100*n)+.05)
        res=np.linalg.norm(nxt-h); h=nxt; it+=1
        if res<1e-11 or it>200000: break
    i=np.argmin(h)
    print(f"n={n}: iters={it} res={res:.2e} min={h.min():.10f} at idx {i} (d={n//4},k={k}); selected-min={h[1:k].min():.8f}; h0={h[0]:.6f}; median sel={np.median(h[1:k]):.6f}; time {time.time()-t0:.1f}s", flush=True)
