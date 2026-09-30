import itertools
import time
import numpy as np
import torch
from torch import nn
from common import Classifier, rng, tensor, digest, state_bytes

def dataset(seed):
    cores=np.array(list(itertools.product((0,1),repeat=6)),dtype=np.float32).reshape(-1,3,2)
    shared=np.array(list(itertools.product((0,1),repeat=3)),dtype=np.float32)
    core=np.repeat(cores,8,axis=0); scene=np.tile(shared,(64,1))
    x=np.concatenate((core,np.repeat(scene[:,None,:],3,axis=1)),axis=2)
    y=np.any(np.all(core==1,axis=2),axis=1).astype(np.float32)
    env=[np.flatnonzero(scene[:,j]==y) for j in range(3)]
    test=x.copy(); order=rng(seed,1,1)
    for row in test: order.shuffle(row,axis=0)
    return x,y,env,test

def rules(x):
    out=[]; descriptions=[]
    for size in (1,2):
        for fields in itertools.combinations(range(5),size):
            for vals in itertools.product((0,1),repeat=size):
                pred=np.any(np.all(x[:,:,fields]==np.array(vals),axis=2),axis=1)
                out.append(pred); descriptions.append((fields,vals))
    return np.array(out),descriptions

def rule_control(seed):
    x,y,env,test=dataset(seed); table,desc=rules(x); test_table,_=rules(test)
    union=np.concatenate(env); errors=np.sum(table[:,union] != y[union],axis=1)
    best=np.flatnonzero(errors==errors.min()); i=int(best[0])
    distinct={table[j].tobytes() for j in best}
    stages=[]
    for end in range(1,4):
        idx=np.concatenate(env[:end]); e=np.sum(table[:,idx]!=y[idx],axis=1)
        j=int(np.argmin(e)); stages.append(float(np.mean(test_table[j]==y)))
    return {'seed':seed,'model':'propositional_enumeration','accuracy':float(np.mean(test_table[i]==y)),
            'joint_cumulative_gap_pp':0,'zero_error_distinct_rules':len(distinct),
            'selected_rule':desc[i],'stage_accuracy':stages,'parameters':0,
            'persistent_bytes':len(desc)*8,'approx_comparisons':len(desc)*len(union),
            'training_examples':len(union),'dataset_sha256':digest(x,y,union,test)}

@torch.no_grad()
def metrics(model,x,y,env,test):
    logits=model(tensor(test)); pred=(logits>=0).numpy(); union=np.concatenate(env)
    train=model(tensor(x[union])); labels=tensor(y[union])
    # All eight counterfactual shared vectors are paired within each core case.
    p=pred.reshape(64,8); flips=np.mean(p[:,1:]!=p[:,:1])
    return {'accuracy':float(np.mean(pred==y)),
            'environment_accuracy':[float(np.mean((model(tensor(x[ix]))>=0).numpy()==y[ix])) for ix in env],
            'union_accuracy':float(np.mean((train>=0).numpy()==y[union])),
            'union_bce':float(nn.functional.binary_cross_entropy_with_logits(train,labels)),
            'counterfactual_flip_rate':float(flips)}

def train(seed,kind,schedule,control,lr,config,meter):
    start=time.perf_counter(); cpu=time.process_time()
    x,y,env,test=dataset(seed); union=np.concatenate(env)
    torch.manual_seed(seed); model=Classifier(kind,control=='layernorm').cpu()
    torch.manual_seed(seed+7); fresh=Classifier(kind,control=='layernorm').cpu().state_dict()
    initial={k:v.detach().clone() for k,v in model.state_dict().items()}
    def optimizer():
        if control=='sgd': return torch.optim.SGD(model.parameters(),lr=lr)
        return torch.optim.AdamW(model.parameters(),lr=lr,weight_decay=.001 if control=='weight_decay' else 0)
    opt=optimizer(); data_rng=rng(seed,1,2); final_rng=rng(seed,1,3)
    order=list(np.roll(np.arange(3),seed%3))
    if schedule=='shuffled_cumulative': order=order[::-1]
    steps=3*config['stage_steps']+config['final_steps']; transition_metrics=[]
    counts=0; linear=[m for m in model.modules() if isinstance(m,nn.Linear)]
    utilities=[torch.zeros(m.out_features) for m in linear[:-1]]; ages=0
    def reset_stage(final=False):
        nonlocal opt
        if control=='optimizer_reset': opt=optimizer()
        if control=='shrink_perturb':
            with torch.no_grad():
                for k,v in model.state_dict().items(): v.copy_(.9*v+.01*fresh[k])
        if control=='fresh_union' and final:
            model.load_state_dict(initial); opt=optimizer()
    for step in range(steps):
        if step%100==0: meter.check()
        if step in (config['stage_steps'],2*config['stage_steps'],3*config['stage_steps']):
            transition_metrics.append(metrics(model,x,y,env,test)); reset_stage(step==3*config['stage_steps'])
        if step>=3*config['stage_steps']:
            idx=final_rng.choice(union,config['batch']); local=step-3*config['stage_steps']; span=config['final_steps']
        else:
            stage=step//config['stage_steps']; local=step%config['stage_steps']; span=config['stage_steps']
            pool=union if schedule=='joint' else env[order[stage]] if schedule=='sequential' else np.concatenate([env[k] for k in order[:stage+1]])
            idx=data_rng.choice(pool,config['batch'])
        if control=='lr_restart':
            for g in opt.param_groups: g['lr']=lr*(.1+.9*.5*(1+np.cos(np.pi*local/span)))
        xb=tensor(x[idx]); yb=tensor(y[idx]); opt.zero_grad(set_to_none=True)
        loss=nn.functional.binary_cross_entropy_with_logits(model(xb),yb)
        if not torch.isfinite(loss): raise RuntimeError('Nonfinite T1 loss')
        loss.backward(); nn.utils.clip_grad_norm_(model.parameters(),config['gradient_clip']); opt.step()
        if control=='feature_replacement':
            ages+=1
            with torch.no_grad():
                h=xb.flatten(1)
                for j in range(len(linear)-1):
                    h=torch.relu(linear[j](h)); utilities[j].mul_(.99).add_(h.abs().mean(0),alpha=.01)
                if ages>=100:
                    counts+=32*.001
                    if counts>=1:
                        counts-=1
                        for j,u in enumerate(utilities):
                            k=int(u.argmin()); key=f'net.{2*j}.weight'
                            linear[j].weight[k].copy_(initial[key][k]); linear[j].bias[k].zero_()
                            linear[j+1].weight[:,k].zero_(); u[k]=0
                            # Reset the affected Adam entries along the same slices.
                            for param,axis in ((linear[j].weight,0),(linear[j].bias,0),(linear[j+1].weight,1)):
                                for val in opt.state.get(param,{}).values():
                                    if torch.is_tensor(val) and val.shape==param.shape:
                                        if axis==0: val[k]=0
                                        else: val[:,k]=0
    result=metrics(model,x,y,env,test)
    parameters=sum(p.numel() for p in model.parameters())
    result.update(seed=seed,model=kind,schedule=schedule,control=control,lr=lr,
                  transition_metrics=transition_metrics,parameters=parameters,
                  persistent_bytes=state_bytes(model,opt)+sum(u.numel()*u.element_size() for u in utilities)+16,
                  steps=steps,training_examples=steps*config['batch'],
                  approximate_dense_training_flops=6*parameters*steps*config['batch'],
                  flop_note='Dense parameter proxy; Transformer attention/nonlinear overhead not included; CPU measured separately',
                  cpu_seconds=time.process_time()-cpu,wall_seconds=time.perf_counter()-start,
                  dataset_sha256=digest(x,y,union,test))
    return result
