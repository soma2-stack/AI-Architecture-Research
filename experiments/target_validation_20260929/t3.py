import itertools,json,sys,time,math
from collections import Counter,deque
from common import ROOT,rng,digest,tensor,torch,nn,state_bytes
sys.path.insert(0,str(ROOT/'vendor'))
from aalpy.learning_algs import run_RPNI

PERMS=list(itertools.permutations(range(3)))
ALPHABET={'parity':2,'addition':100,'permutation':6,'modsum':5}

def transition(task,state,x):
    if task=='parity': s=state^x; return s,s
    if task=='addition': v=x//10+x%10+state; return v//10,v%10
    if task=='modsum': s=(state+x)%5; return s,s
    p,q=PERMS[x],PERMS[state]; s=PERMS.index(tuple(p[q[i]] for i in range(3))); return s,s

def labels(task,word):
    state=0; out=[]
    for x in word: state,y=transition(task,state,int(x)); out.append(y)
    return out

def data(seed,task,c):
    k=c['tasks'].index(task); r=rng(seed,3,100+k); e=rng(seed,3,200+k)
    def word(random,length):
        w=random.integers(ALPHABET[task],size=length).tolist()
        if task=='addition': w[-1]=0
        return w
    train=[word(r,int(r.integers(c['train_min_length'],c['train_max_length']+1))) for _ in range(c['train_words'])]
    tests={l:[word(e,l) for _ in range(c['test_words_per_length'])] for l in range(4,c['test_max_length']+1)}
    counts=Counter()
    for w in train:
        s=0
        for x in w: counts[s,x]+=1; s,_=transition(task,s,x)
    states=2 if task in ('parity','addition') else ALPHABET[task]
    minimum=min(counts[s,x] for s in range(states) for x in range(ALPHABET[task]))
    h=lambda words:digest(*[__import__('numpy').array(w,dtype='int16') for w in words])
    return train,tests,{'training_sha256':h(train),'test_sha256':h([w for ws in tests.values() for w in ws]),'minimum_transition_count':minimum}

def infer(train,outputs):
    # Only observed inputs/outputs cross this learner boundary.
    observations={tuple(w[:i+1]):y for w,ys in zip(train,outputs) for i,y in enumerate(ys)}
    return run_RPNI(list(observations.items()),'mealy',algorithm='gsm',input_completeness=None,print_info=False)

def exact_audit(model,task):
    todo=deque([(model.initial_state,0)]); seen=set()
    while todo:
        node,s=todo.popleft()
        if (node.state_id,s) in seen: continue
        seen.add((node.state_id,s))
        for x in range(ALPHABET[task]):
            ns,y=transition(task,s,x)
            if x not in node.transitions or node.output_fun[x]!=y: return False
            todo.append((node.transitions[x],ns))
    return True

def graph(model):
    return {s.state_id:{str(x):[s.transitions[x].state_id,s.output_fun[x]] for x in s.transitions} for s in model.states}

def evaluate(model,task,tests):
    result={}
    for length,words in tests.items():
        good=0
        for w in words:
            model.reset_to_initial()
            try: predicted=[model.step(x) for x in w]
            except KeyError: predicted=[]
            good+=predicted==labels(task,w)
        result[str(length)]=good/len(words)
    return result

class SequenceModel(nn.Module):
    def __init__(self,kind):
        super().__init__(); self.kind=kind; self.emb=nn.Embedding(100,16); self.out=nn.Linear(16,10)
        if kind in ('gru','lstm'): self.core=(nn.GRU if kind=='gru' else nn.LSTM)(16,16,batch_first=True)
        else: self.core=nn.TransformerEncoderLayer(16,2,32,dropout=0,batch_first=True)
    def forward(self,x):
        h=self.emb(x); length=x.shape[1]
        if self.kind in ('gru','lstm'): return self.out(self.core(h)[0])
        p=torch.arange(length,device='cpu'); mask=torch.full((length,length),float('-inf'),device='cpu').triu(1)
        if self.kind=='relative': mask=mask-(p[:,None]-p[None,:]).clamp(min=0)*.1
        else:
            div=torch.exp(torch.arange(0,16,2,device='cpu')*(-math.log(10000)/16)); pos=torch.zeros(length,16)
            pos[:,0::2]=torch.sin(p[:,None]*div); pos[:,1::2]=torch.cos(p[:,None]*div); h=h+pos
        for _ in range(4 if self.kind=='universal' else 1): h=self.core(h,src_mask=mask)
        return self.out(h)

def neural(seed,task,kind,lr,c,meter):
    train,tests,hashes=data(seed,task,c); torch.manual_seed(seed+c['tasks'].index(task)); model=SequenceModel(kind)
    opt=torch.optim.AdamW(model.parameters(),lr=lr,weight_decay=0); r=rng(seed,3,300+c['tasks'].index(task))
    bylength={l:[w for w in train if len(w)==l] for l in range(4,17)}; count=0
    for step in range(c['neural_steps']):
        if step%32==0: meter.check()
        length=int(r.integers(4,17)); pool=bylength[length]; words=[pool[int(i)] for i in r.integers(len(pool),size=c['batch'])]
        x=tensor(words,torch.long); y=tensor([labels(task,w) for w in words],torch.long)
        opt.zero_grad(set_to_none=True); loss=nn.functional.cross_entropy(model(x).flatten(0,1),y.flatten()); loss.backward(); nn.utils.clip_grad_norm_(model.parameters(),5); opt.step(); count+=length*c['batch']
    model.eval()
    def accuracy(words):
        with torch.no_grad():
            x=tensor(words,torch.long); y=tensor([labels(task,w) for w in words],torch.long); z=model(x)
            return float((z.argmax(-1)==y).all(1).float().mean()),float(nn.functional.cross_entropy(z.flatten(0,1),y.flatten()))
    training_loss=sum(accuracy(ws)[1]*len(ws) for ws in bylength.values())/len(train)
    training_exact=sum(accuracy(ws)[0]*len(ws) for ws in bylength.values())/len(train)
    scores={str(l):accuracy(ws)[0] for l,ws in tests.items()}
    return {'seed':seed,'task':task,'model':kind,'lr':lr,'training_loss':training_loss,'training_exact':training_exact,'exact_by_length':scores,'parameters':sum(p.numel() for p in model.parameters()),'persistent_tensor_bytes':state_bytes(model,opt),'updates':c['neural_steps'],'examples':c['neural_steps']*c['batch'],'token_updates':count,'approx_dense_parameter_operations':6*count*sum(p.numel() for p in model.parameters()),'operation_estimate_excludes_attention_quadratic_term':True,**hashes}
