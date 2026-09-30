from common import nn,torch

class Predictor(nn.Module):
    def __init__(self,depth,width=128,normalization=False,sieve=False):
        super().__init__(); self.depth=depth; self.blocks=nn.ModuleList()
        for i in range(depth):
            self.blocks.append(nn.Sequential(nn.Linear(64 if i==0 else width,width),
                *([nn.LayerNorm(width)] if normalization else []),nn.ReLU()))
        self.head=nn.Linear(width if depth else 64,1)
        self.aux=nn.Linear(width,1) if sieve and depth else None
    def hidden(self,x):
        h=[]
        for block in self.blocks: x=block(x); h.append(x)
        return h
    def forward(self,x):
        h=self.hidden(x); return self.head(h[-1] if h else x).flatten()

def build(seed,kind,control,c):
    torch.manual_seed(seed); return Predictor(c['models'][kind],c['width'],control=='layernorm',control=='feature_sieve').cpu()

def optimizer(model,control,lr,phase,c):
    params=[p for p in model.parameters() if p.requires_grad]
    if control=='sgdm': return torch.optim.SGD(params,lr=lr,momentum=c['momentum'])
    if control=='lbfgs' and phase!='A': return torch.optim.LBFGS(params,lr=lr,max_iter=1,history_size=10,line_search_fn=None)
    return torch.optim.AdamW(params,lr=.003 if control=='lbfgs' and phase=='A' else lr,weight_decay=c['weight_decay_control'] if control=='weight_decay' else 0)

def repair(model,initial,control):
    if control=='head_reset': model.head.load_state_dict(initial.head.state_dict())
    if control.startswith('reinit_'): model.blocks[int(control.split('_')[1])].load_state_dict(initial.blocks[int(control.split('_')[1])].state_dict())
    if control=='last_layer':
        for block in model.blocks:
            for p in block.parameters(): p.requires_grad=False
