"""Invertible embedding; only (x,y) crosses the predictor-training boundary."""
from common import np,rng,digest

def orthogonal(random,n):
    q,r=np.linalg.qr(random.normal(size=(n,n)))
    return q*np.where(np.diag(r)>=0,1,-1)[None,:]

class Generator:
    def __init__(self,seed,config):
        self.seed=seed; self.config=config; r=rng(seed,4,0)
        self.q=[orthogonal(r,63) for _ in range(3)]; self.mix=orthogonal(r,64)
        z,c=self.latent(config['calibration_core_samples'],1)
        core=self.embed(z); self.mean=core.mean(0)
        centered=core-self.mean; cov=centered.T@centered/len(core)
        eig,v=np.linalg.eigh(cov)
        if eig.min()<=1e-10: raise RuntimeError('Noninvertible covariance')
        self.white=(v*(eig**-.5))@v.T; self.unwhite=(v*(eig**.5))@v.T
        self.calibration_covariance=np.cov(self.observe(z,np.ones(len(z))).T,bias=True)
        # Paired signs ensure shortcut/core cross covariance exactly zero.
        paired=np.concatenate([self.observe(z,np.ones(len(z))),self.observe(z,-np.ones(len(z)))])
        self.calibration_covariance=np.cov(paired.T,bias=True)
        self.hash=digest(*self.q,self.mix,self.mean,self.white)
    def latent(self,n,stream):
        r=rng(self.seed,4,stream); c=np.concatenate([-np.ones(n//2),np.ones(n-n//2)]); r.shuffle(c)
        z=r.normal(size=(n,63)); z[:,0]=c*r.uniform(*self.config['core_margin'],size=n)
        return z,c
    def embed(self,z):
        x=z.copy()
        for q in self.q:
            x=x@q; x=np.where(x>=0,x,x*self.config['embedding_leaky_slope'])
        return x
    def observe(self,z,s):
        core=(self.embed(z)-self.mean)@self.white
        return np.concatenate([core,s[:,None]],1)@self.mix
    def inverse(self,x):
        x=x@self.mix.T; core=x[:,:63]@self.unwhite+self.mean
        for q in self.q[::-1]:
            core=np.where(core>=0,core,core/self.config['embedding_leaky_slope']); core=core@q.T
        return core,x[:,63]
    def phase(self,name):
        stream=10+['A','B','C'].index(name); n=self.config['examples']; z,c=self.latent(n,stream)
        correct=round(n*self.config['phase_agreement'][name]); flags=np.concatenate([np.ones(correct),-np.ones(n-correct)])
        rng(self.seed,4,stream+20).shuffle(flags); s=c*flags
        return self.observe(z,s).astype('float32'),((c+1)/2).astype('float32'),c,s
    def evaluation(self):
        n=self.config['eval_examples']; z,c=self.latent(n,50)
        s=rng(self.seed,4,51).choice([-1.,1.],size=n)
        return {'cf':self.observe(z,s).astype('float32'),'anti':self.observe(z,-c).astype('float32'),
            'plus':self.observe(z,np.ones(n)).astype('float32'),'minus':self.observe(z,-np.ones(n)).astype('float32'),
            'y':((c+1)/2).astype('float32')}
    def probes(self):
        out=[]
        for stream,n in [(60,self.config['probe_training_examples']),(61,self.config['probe_test_examples'])]:
            z,c=self.latent(n,stream); s=rng(self.seed,4,stream+10).choice([-1.,1.],size=n)
            out.append((self.observe(z,s).astype('float32'),((c+1)/2).astype('float32')))
        return out

def training_batches(seed,phase,steps,batch,n):
    # Independent of arm/model/LR/history; same corrective opportunities.
    return rng(seed,4,100+['A','B','C','joint'].index(phase)).integers(n,size=(steps,batch))
