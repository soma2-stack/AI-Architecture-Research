"""Post-checkpoint comparison with unmodified pinned GPT-6 source plus explicit
PUBLIC preparation/reset harmonization. No changes to historical GPT-6 folders.
"""
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1')
import json,time,types,hashlib
from pathlib import Path
import numpy as np
import private_echo as astra
import competitor_snapshot as original
ROOT=Path(__file__).resolve().parent
src=(ROOT/'competitor_snapshot.py').read_text()
old="    tau=np.zeros(m);live=np.zeros(m);gates=[];dgs=[];baselines=[];taus=[]"
new="    for ix,ss in zip(np.r_[3*S+np.arange(m),6*S+np.arange(m)],np.r_[np.ones(m),-np.ones(m)]):hd[int(ix)]=float(ss*math.sqrt(1-gh)-u)\n"+old
assert src.count(old)==1;src=src.replace(old,new)
old="            ids=np.r_[3*S+np.arange(m)+t,6*S+np.arange(m)+t]"
new="            if t==N:gs=np.full(m,1-math.tanh(BIAS)**2)\n"+old
assert src.count(old)==1;src=src.replace(old,new)
gpt=types.ModuleType('gpt_public_matched');exec(compile(src,'<two-explicit-public-matching-edits>','exec'),gpt.__dict__)

def save(data):
    p=ROOT/'comparison_results.json';tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(data,indent=2,allow_nan=False));os.replace(tmp,p)

def make(n,m,R,W,L,variant,raw=False):
    y=np.random.default_rng(812).choice([-1.,1.],(R,m));zero=np.zeros((R,m));extra={}
    if variant.startswith('astra'):
        mode='weak_echo' if 'weak' in variant else 'echo'
        if variant=='astra_weak_equal_contrast':extra['eta_override']=1e-4/( (1-n**-2)*np.exp(-.0025/R))
        if variant=='astra_echo_active_half':
            mask=np.array([[(i&(st+1)).bit_count()%2 for i in range(m)] for st in range(R)])
            y=y*mask
        p=astra.history(n,m,R,W,zero,L,survivor_controls=y,mode=mode,**extra)
        q=astra.history(n,m,R,W,zero,L,survivor_controls=-y,mode=mode,**extra)
        controls=m*R//2 if variant=='astra_echo_active_half' else m*R
        dose=2*p['echo_center']*np.sinh(p['echo_contrast'])
    else:
        lib=original if raw else gpt
        if variant=='gpt_capture':
            kw=lambda v:dict(private_capture=v,hold_survivors=True);word=y;controls=m*R//2;dose=1e-4
        elif variant=='gpt_interior_independent':
            word=np.random.default_rng(812).choice([-1.,1.],(R,m,W-1));controls=word.size;dose=(W-1)*.5e-4
            kw=lambda v:dict(private_interior=v,hold_survivors=True)
        else:
            amp=min(1.,4/(W-1)) if variant=='gpt_interior_equal_dose' else 1.
            word=np.repeat((amp*y)[:,:,None],W-1,axis=2);controls=m*R;dose=(W-1)*.5e-4*amp
            kw=lambda v:dict(private_interior=v,hold_survivors=True)
        p=lib.history(n,m,R,W,zero,L,**kw(word));q=lib.history(n,m,R,W,zero,L,**kw(-word))
    assert astra.endpoint_error(p,q)<1e-10
    return p,q,controls,float(dose)

def measure(n,m,R,W,L,variant,large=False,raw=False):
    tic=time.time();p,q,controls,dose=make(n,m,R,W,L,variant,raw)
    out=dict(n=n,m=m,R=R,W=W,L=L,N=p['N'],variant=variant,raw_competitor=raw,
        active_private_controls=controls,variable_gate_half_excursion_sum_per_stage_site=dose,
        strong_geometry=p['strong_geometry'],endpoint=astra.endpoint_error(p,q),maxtrace=p['maxtrace'],
        max_input=max(p['maxinput'],q['maxinput']),mN=m*p['N'],queries=[])
    for horizon in ([1] if large else [1,2,4,8]):
        qr,_=astra.query_probe(p,q,horizon,2,1);out['queries'].append(qr)
    out['seconds']=time.time()-tic
    return out

def main():
    p=ROOT/'comparison_results.json';d=json.loads(p.read_text()) if p.exists() else dict(cases=[])
    variants=['astra_echo','astra_weak_echo','astra_weak_equal_contrast','astra_echo_active_half',
        'gpt_capture','gpt_interior_tied','gpt_interior_equal_dose','gpt_interior_independent']
    plan=[(n,m,R,W,L,v,False,False) for n,m,R,W,L in [(16384,4,2,16,128),(32768,8,4,16,256),(32768,8,4,64,256)] for v in variants]
    plan += [(32768,8,4,16,256,v,False,True) for v in ['gpt_capture','gpt_interior_tied']]
    plan += [(1048576,8,4,16,2048,v,True,False) for v in ['astra_echo','astra_weak_echo','gpt_capture','gpt_interior_tied']]
    for n,m,R,W,L,v,large,raw in plan:
        if any((x['n'],x['m'],x['R'],x['W'],x['L'],x['variant'],x['raw_competitor'])==(n,m,R,W,L,v,raw) for x in d['cases']):continue
        print('START',n,W,v,raw,flush=True)
        x=measure(n,m,R,W,L,v,large,raw);d['cases'].append(x);save(d)
        print('DONE',n,W,v,max(q['best_M'] for q in x['queries']),x['seconds'],flush=True)
    print('COMPARISON COMPLETE',flush=True)

if __name__=='__main__':main()
