import copy,time
from common import np,torch,nn,tensor,rng,digest,state_bytes
from data import Generator,training_batches
from models import build,optimizer,repair

@torch.no_grad()
def logits(model,x):
    return torch.cat([model(tensor(x[i:i+1024])) for i in range(0,len(x),1024)])

@torch.no_grad()
def metric(model,datasets,evaluation):
    cf=logits(model,evaluation['cf']); anti=logits(model,evaluation['anti']); y=tensor(evaluation['y'])
    result={'cf_accuracy':float(((cf>=0)==y.bool()).float().mean()),'anti_accuracy':float(((anti>=0)==y.bool()).float().mean()),
        'bayes_relative_shortcut_reliance':float(((logits(model,evaluation['plus'])>=0)!=(logits(model,evaluation['minus'])>=0)).float().mean())}
    for name,(x,y,_,_) in datasets.items():
        z=logits(model,x); y=tensor(y)
        result['train_'+name+'_accuracy']=float(((z>=0)==y.bool()).float().mean()); result['train_'+name+'_bce']=float(nn.functional.binary_cross_entropy_with_logits(z,y))
    return result

def curve_metrics(curve,batch):
    a=np.array([r['cf_accuracy'] for r in curve]); steps=np.array([r['step'] for r in curve])
    auc=float(np.trapezoid(a,steps)/(steps[-1]-steps[0])); reached=next((i for i,v in enumerate(a) if v>.95),None)
    return {'correction_accuracy_auc':auc,'correction_error_aulc':1-auc,'samples_to_exceed_95_upper':None if reached is None else int(steps[reached]*batch),
        'samples_to_exceed_95_lower':None if reached is None else int(0 if reached==0 else steps[reached-1]*batch)}

def step(model,opt,x,y,control,index,c):
    if control=='feature_sieve' and model.aux is not None and (index+1)%c['sieve_interval']==0:
        for p in model.aux.parameters(): p.requires_grad=False
        opt.zero_grad(set_to_none=True); h=model.blocks[0](x); loss=nn.functional.binary_cross_entropy_with_logits(model.aux(h).flatten(),torch.full_like(y,.5))*c['sieve_forget_weight']
        loss.backward(); nn.utils.clip_grad_norm_(model.parameters(),5); opt.step()
        for p in model.aux.parameters(): p.requires_grad=True
        return float(loss.detach()),1
    def closure():
        opt.zero_grad(set_to_none=True); h=model.hidden(x); z=model.head(h[-1] if h else x).flatten(); loss=nn.functional.binary_cross_entropy_with_logits(z,y)
        if control=='spectral': loss=loss+.5*c['spectral_lambda']*z.square().mean()
        if model.aux is not None: loss=loss+c['sieve_aux_weight']*nn.functional.binary_cross_entropy_with_logits(model.aux(h[0].detach()).flatten(),y)
        if not torch.isfinite(loss): raise RuntimeError('Nonfinite training loss')
        loss.backward(); nn.utils.clip_grad_norm_(model.parameters(),5); return loss
    if isinstance(opt,torch.optim.LBFGS): loss=opt.step(closure)
    else: loss=closure(); opt.step()
    return float(loss.detach()),1

def run(seed,kind,control,lr,mode,c,meter,save=None):
    g=Generator(seed,c); datasets={p:g.phase(p) for p in ['A','B','C']}; evaluation=g.evaluation()
    initial=build(seed,kind,control,c); model=copy.deepcopy(initial); opt=None; snapshots=[]; steps_total=0; started=time.process_time()
    phases=['A','B','C'] if mode=='warm' else [mode]
    for phase in phases:
        if phase!='A' and mode=='warm': repair(model,initial,control)
        reset=opt is None or (phase!='A' and control in ('optimizer_reset','head_reset','last_layer','lbfgs')) or control.startswith('reinit_')
        if reset: opt=optimizer(model,control,lr,phase,c)
        budget=c['a_max_steps'] if phase in ('A','joint') else c['correction_steps']
        if phase=='joint':
            xs=np.concatenate([datasets[p][0] for p in ['A','B','C']]); ys=np.concatenate([datasets[p][1] for p in ['A','B','C']]); indices=training_batches(seed,phase,budget,c['batch'],c['examples'])
            # Fixed86/85/85 exact composition in every minibatch.
            indices=np.concatenate([indices[:,:86],indices[:,86:171]+c['examples'],indices[:,171:]+2*c['examples']],axis=1)
        else: xs,ys,_,_=datasets[phase]; indices=training_batches(seed,phase,budget,c['batch'],len(xs))
        curve=[{'step':0,'cf_accuracy':metric(model,datasets,evaluation)['cf_accuracy']}]
        closures=0
        for i,ix in enumerate(indices):
            if i%50==0: meter.check()
            _,n=step(model,opt,tensor(xs[ix]),tensor(ys[ix]),control,i,c); closures+=n
            if (i+1)%c['checkpoint_interval']==0:
                current=metric(model,datasets,evaluation); curve.append({'step':i+1,'cf_accuracy':current['cf_accuracy']})
                if phase=='A' and i+1>=c['a_min_steps'] and current['train_A_accuracy']>=c['a_train_stop_accuracy']: break
        actual=i+1; steps_total+=actual; r=metric(model,datasets,evaluation)
        r.update({'seed':seed,'model':kind,'control':control,'lr':lr,'mode':mode,'phase':phase,'updates':actual,'sample_exposures':actual*c['batch'],'closure_calls':closures,
            'curve':curve,**curve_metrics(curve,c['batch']),'parameters':sum(p.numel() for p in model.parameters()),'persistent_tensor_bytes':state_bytes(model,opt),
            'generator_sha256':g.hash,'training_sha256':{p:digest(datasets[p][0],datasets[p][1]) for p in datasets},'evaluation_sha256':digest(evaluation['cf'],evaluation['y']),
            'approx_dense_parameter_operations':6*sum(p.numel() for p in model.parameters())*actual*c['batch'],'operation_proxy_excludes_normalization_aux_extra_forward':True})
        if save:
            r['checkpoint']=save(seed,kind,control,lr,mode,phase,model)
        snapshots.append(r)
    return {'snapshots':snapshots,'cpu_seconds':time.process_time()-started,'updates':steps_total}

def probes(seed,model,g,c,meter):
    if not model.depth: return []
    (x,y),(test,ty)=g.probes()
    with torch.no_grad(): train_h=[h.detach() for h in model.hidden(tensor(x))]; test_h=[h.detach() for h in model.hidden(tensor(test))]
    result=[]
    for layer,(a,b) in enumerate(zip(train_h,test_h)):
        for nonlinear in (False,True):
            torch.manual_seed(seed+layer*10+int(nonlinear)); p=nn.Sequential(nn.Linear(a.shape[1],c['probe_width']),nn.ReLU(),nn.Linear(c['probe_width'],1)) if nonlinear else nn.Linear(a.shape[1],1)
            opt=torch.optim.AdamW(p.parameters(),lr=c['probe_lr'],weight_decay=0); random=rng(seed,4,400+layer*2+int(nonlinear))
            for step_index in range(c['probe_steps']):
                if step_index%50==0: meter.check()
                ix=random.integers(len(a),size=c['probe_batch']); opt.zero_grad(set_to_none=True); z=p(a[ix]).flatten(); loss=nn.functional.binary_cross_entropy_with_logits(z,tensor(y[ix])); loss.backward(); opt.step()
            with torch.no_grad(): accuracy=float(((p(b).flatten()>=0)==tensor(ty).bool()).float().mean())
            result.append({'layer':layer,'type':'nonlinear_32' if nonlinear else 'linear','test_accuracy':accuracy,'parameters':sum(v.numel() for v in p.parameters()),'updates':c['probe_steps'],'training_sha256':digest(x,y),'test_sha256':digest(test,ty)})
    return result

def kill_gate(pairs,c):
    checks=[]
    for seed,phases in sorted(pairs.items()):
        valid=len(phases)==2 and all(w['train_'+phase+'_accuracy']>=c['kill_training_min'] and max(0,s['cf_accuracy']-w['cf_accuracy'])<c['kill_gap_max'] for phase,(w,s) in phases.items())
        checks.append({'seed':seed,'passed':valid,'phases':{p:{'train_accuracy':w['train_'+p+'_accuracy'],'warm_cf':w['cf_accuracy'],'scratch_cf':s['cf_accuracy'],'gap_pp':100*(s['cf_accuracy']-w['cf_accuracy'])} for p,(w,s) in phases.items()}})
    return sum(r['passed'] for r in checks)>=c['kill_seeds'],checks
