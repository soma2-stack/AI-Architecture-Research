import numpy as np
import torch
from torch import nn
from common import rng,tensor,digest,state_bytes

class Model(nn.Module):
    def __init__(self,kind):
        super().__init__(); self.kind=kind
        if kind=='head':
            self.heads=nn.ModuleList([nn.Linear(16,1) for _ in range(8)])
            for h in self.heads: nn.init.zeros_(h.weight); nn.init.zeros_(h.bias)
        elif kind.startswith('mlp'):
            w=int(kind[3:]); self.net=nn.Sequential(nn.Linear(24,w),nn.ReLU(),nn.Linear(w,w),nn.ReLU(),nn.Linear(w,1))
        elif kind=='gru': self.gru=nn.GRU(25,7,batch_first=True); self.out=nn.Linear(7,1)
        else:
            self.enc=nn.Linear(9,8); self.position=nn.Parameter(torch.zeros(16,8))
            self.attn=nn.TransformerEncoderLayer(8,2,16,dropout=0,batch_first=True); self.out=nn.Linear(8,1)
    def forward(self,x):
        if self.kind=='head':
            ctx=x[:,16:].argmax(1); out=torch.empty(len(x),device='cpu')
            for k in ctx.unique().tolist():
                mask=ctx==k; out[mask]=self.heads[k](x[mask,:16]).flatten()
            return out
        if self.kind.startswith('mlp'): return self.net(x).flatten()
        bits=x[:,:16].unsqueeze(2); ctx=x[:,None,16:].expand(-1,16,-1)
        if self.kind=='gru':
            pos=torch.eye(16,device='cpu')[None].expand(len(x),-1,-1)
            h,_=self.gru(torch.cat((bits,pos,ctx),2)); return self.out(h[:,-1]).flatten()
        h=self.enc(torch.cat((bits,ctx),2))+self.position
        return self.out(self.attn(h).mean(1)).flatten()

def data(seed,c):
    teacher=rng(seed,2,0).choice((-1,1),size=(8,16)); teacher[:,:4]=1
    order=rng(seed,2,1).permutation(8).tolist(); order+=order[::-1]
    gen=rng(seed,2,2); train=[]
    for task in order:
        bits=gen.choice((-1.,1.),size=(c['block_steps']*c['batch'],16)).astype(np.float32)
        x=np.concatenate((bits,np.repeat(np.eye(8,dtype=np.float32)[task][None],len(bits),axis=0)),axis=1)
        y=(bits@teacher[task]>=0).astype(np.float32); train.append((x,y))
    test=[]; gen=rng(seed,2,3)
    for task in range(8):
        bits=gen.choice((-1.,1.),size=(c['evaluation_examples_per_task'],16)).astype(np.float32)
        x=np.concatenate((bits,np.repeat(np.eye(8,dtype=np.float32)[task][None],len(bits),axis=0)),axis=1)
        test.append((tensor(x),tensor((bits@teacher[task]>=0).astype(np.float32))))
    return teacher,order,train,test

@torch.no_grad()
def evaluate(model,test):
    return [float(((model(x)>=0)==y.bool()).float().mean()) for x,y in test]

def run(seed,kind,arm,lr,c,meter):
    teacher,order,train,test=data(seed,c); torch.manual_seed(seed); model=Model(kind).cpu()
    initial={k:v.clone() for k,v in model.state_dict().items()}
    def opt():
        return torch.optim.SGD(model.parameters(),lr=lr) if kind=='head' else torch.optim.AdamW(model.parameters(),lr=lr,weight_decay=0)
    optimizer=opt(); history=[]; losses=[]; seen=set(); max_state=state_bytes(model,optimizer)
    if sum(p.numel() for p in model.parameters())>c['parameter_cap']: raise RuntimeError('Parameter cap')
    mapping={k:[] for k in range(8)}
    for b,k in enumerate(order): mapping[k].append(b)
    # A joint block is an accounting interval, not a task-boundary signal.
    for block,task in enumerate(order):
        if arm=='fresh': model.load_state_dict(initial); optimizer=opt()
        before=evaluate(model,test); checkpoints=[before[task]]
        for step in range(c['block_steps']):
            if step%32==0: meter.check()
            if arm=='joint':
                global_step=block*c['block_steps']+step; ctx=global_step%8; row=global_step//8
                b=mapping[ctx][row//c['block_steps']]; s=row%c['block_steps']
            else: b=block; s=step
            x,y=train[b]; ix=slice(s*c['batch'],(s+1)*c['batch']); optimizer.zero_grad(set_to_none=True)
            logits=model(tensor(x[ix])); loss=nn.functional.binary_cross_entropy_with_logits(logits,tensor(y[ix]))
            if not torch.isfinite(loss): raise RuntimeError('Nonfinite T2 loss')
            loss.backward(); nn.utils.clip_grad_norm_(model.parameters(),5); optimizer.step()
            if (step+1)%32==0:
                with torch.no_grad(): checkpoints.append(float(((model(test[task][0])>=0)==test[task][1].bool()).float().mean()))
        losses.append(float(loss)); after=evaluate(model,test)
        inactive=[k for k in seen if k!=task]
        history.append({'block':block,'context':task,'before':before,'after':after,
                        'active_checkpoints':checkpoints,'aulc':float(np.mean(1-np.array(checkpoints))),
                        'first_exposure':task not in seen,
                        'max_old_inactive_loss':max([0]+[before[k]-after[k] for k in inactive]),
                        'worst_seen_accuracy':min(after[k] for k in seen|{task})})
        seen.add(task); max_state=max(max_state,state_bytes(model,optimizer))
        if max_state>c['persistent_bytes_cap']: raise RuntimeError('Persistent state cap')
    parameters=sum(p.numel() for p in model.parameters())
    return {'seed':seed,'model':kind,'arm':arm,'lr':lr,'training_selection_loss':float(np.mean(losses)),
            'accuracy_by_task':history[-1]['after'],'mean_accuracy':float(np.mean(history[-1]['after'])),
            'history':history,'parameters':parameters,'persistent_bytes':max_state,
            'steps':16*c['block_steps'],'training_examples':16*c['block_steps']*c['batch'],
            'approximate_training_flops':6*parameters*16*c['block_steps']*c['batch']*(16 if kind in ('gru','transformer') else 1),
            'flop_note':'Dense parameter proxy; not a complete attention/nonlinear operation count',
            'teacher_sha256':digest(teacher),'dataset_sha256':digest(*[a for pair in train for a in pair]),
            'state_growth':False,'replay':False,'task_boundary_signal':False}
