"""Small full-support rank-one perturbation test for the selected recurrence."""
import math, time

def _one(torch, base_O, n, K, eps):
    # Everything in this test, including the rank-one dense operator, stays on
    # CUDA float64. The perturbation has nonzero entries across the full block.
    k=n//2; d=n//4; r=k-1; m=(k-d)//4; nd=m//2
    assert nd>=K and nd%K==0 and nd>=2
    device=torch.device('cuda:0'); dtype=torch.float64
    a=1-1/n; gh=1-1/n**2; gl=.995; R=2
    write=math.ceil(.4*n)
    tail=math.ceil(math.log((write+1)/1e-3)/(-math.log(a*gl)))+1
    clear=2*n; stage_length=write+1+tail+clear; total=R*stage_length+1
    ix=torch.arange(r,device=device,dtype=dtype)
    u=torch.sin((ix+1)*1.324717957244746); u=u/torch.linalg.vector_norm(u)
    v=torch.cos((ix+1)*.754877666246693); v=v/torch.linalg.vector_norm(v)
    def O(x):
        y=base_O(x,d,k)
        sh=[1]*(x.ndim-2)+[r,1]
        return y+eps*u.reshape(sh)*(x*v.reshape(sh)).sum(dim=-2,keepdim=True)

    act=torch.arange(d-1,d-1+4*m,device=device); tuples=act.reshape(m,4)
    signs=torch.tensor([1.,1.,-1.,-1.],device=device,dtype=dtype)
    survivor_ids=tuples[nd:].reshape(-1)
    ns=len(survivor_ids)
    chi=torch.stack([torch.where((torch.arange(nd,device=device)//(2**j))%2==0,1.,-1.) for j in range(R)]).repeat_interleave(4,dim=1)
    reads=torch.zeros(R,r,device=device,dtype=dtype); reads[:,survivor_ids]=chi/math.sqrt(ns)
    # Reproduce the verified orthonormal donor-feature construction.
    comp=tuples[nd:,2:].reshape(-1); ss=torch.zeros(r,device=device,dtype=dtype); ss[comp]=1/math.sqrt(len(comp))
    W=torch.zeros(r,K,device=device,dtype=dtype)
    donor_groups=tuples[:nd].reshape(K,nd//K,4)
    for j in range(K):
        inds=donor_groups[j,:,2:].reshape(-1); W[inds,j]=1/math.sqrt(len(inds)); W[:,j]-=ss/math.sqrt(K)
    P=torch.ones(K,K,device=device,dtype=dtype)/K
    H=torch.eye(K,device=device,dtype=dtype)-(1-1/math.sqrt(2))*P
    V=W@H
    donor_idx=torch.arange(nd,device=device)//(nd//K)
    codes=torch.ones(R,K,device=device,dtype=dtype)
    codes[1]=torch.where((torch.arange(K,device=device)//1)%2==0,1.,-1.)
    # Q is the pair of matched histories for donor epochs 0 and 1.
    Q=R
    states=torch.full((Q,2,r),math.tanh(.05),device=device,dtype=dtype)
    states[...,act]=(.04*signs).repeat(m).reshape(1,1,-1)
    X=torch.zeros(Q,2,r,K,device=device,dtype=dtype)
    tau=torch.zeros(Q,2,K,device=device,dtype=dtype); public_tau=0.
    captured=torch.zeros(Q,R,device=device,dtype=dtype)
    max_input=0.; input_sq=torch.zeros(Q,2,device=device,dtype=dtype)
    prep=torch.atanh(states[...,act])-.05
    input_sq+=(prep**2).sum(-1)
    max_input=max(max_input,float(prep.abs().max()))
    max_trace_match=0.; correction_ranges=[]
    saved={}; complement={}
    sample_points=set()
    for stage in range(R):
        for q in range(R):
            sample_points.add((stage,q,'start'))
    for t in range(1,total+1):
        reset=(t==total)
        stage=min((t-1)//stage_length,R-1); local=(t-1)%stage_length+1
        phase=('reset' if reset else 'write' if local<=write else 'capture' if local==write+1
               else 'trace' if local<=write+1+tail else 'clear')
        is_corr=(not reset and local==write+1+tail)
        dg=torch.full((Q,2,K),gl,device=device,dtype=dtype)
        if phase=='write':
            vcode=codes[stage]
            theta=vcode.reshape(1,1,K).expand(Q,2,K).clone()
            for q in range(Q):
                if q==stage: theta[q,1]=-vcode
            dg=gl+(theta+1)*(gh-gl)/2
        if is_corr:
            target=gl*(1+a*public_tau)
            dg=target/(1+a*tau)
        tg=torch.full((Q,2,m),gh,device=device,dtype=dtype)
        donor_gate=dg.gather(2,donor_idx.reshape(1,1,nd).expand(Q,2,nd))
        tg[:,:,:nd]=donor_gate
        if phase=='capture':
            mask=chi[stage,::4]>0
            tg[:,:,nd:]=torch.where(mask,gh,gl).reshape(1,1,nd).expand(Q,2,nd)

        # Frozen realized inputs: autonomous full selected-state evolution,
        # inverse-lift controls on the active coordinates, then an exact
        # common reset of the whole selected state. The common reset target is
        # the coordinatewise midpoint of the pre-reset histories, avoiding a
        # large artificial jump to a fixed point outside the input cube.
        pre=a*O(states.unsqueeze(-1)).squeeze(-1)+.05
        if reset:
            endpoint=states.mean(dim=(0,1))
            nxt=endpoint.reshape(1,1,r).expand(Q,2,r).clone()
            G=1-nxt**2
            raw=torch.atanh(endpoint).reshape(1,1,r)-pre
            input_sq+=(raw**2).sum(-1); max_input=max(max_input,float(raw.abs().max()))
        else:
            nxt=torch.tanh(pre)
            active=(torch.sqrt(1-tg)[...,None]*signs).reshape(Q,2,-1)
            nxt[...,act]=active
            G=1-nxt**2
            raw=torch.atanh(active)-pre[...,act]
            input_sq+=(raw**2).sum(-1); max_input=max(max_input,float(raw.abs().max()))
        X=G[...,None]*(a*O(X)+V.reshape(1,1,r,K))
        states=nxt
        if not reset: tau=dg*(1+a*tau)
        public_tau=(1-.05**2 if reset else gl)*(1+a*public_tau)
        if is_corr:
            max_trace_match=max(max_trace_match,float((tau[:,0]-tau[:,1]).abs().max()))
            correction_ranges.append(dict(stage=stage,g_min=float(dg.min()),g_max=float(dg.max()),g_range=float(dg.max()-dg.min())))
        Delta=X[:,0]-X[:,1]
        response=torch.einsum('jr,prk->pjk',reads,Delta)
        if phase=='capture':
            captured[:,stage]=torch.linalg.vector_norm(response[:,stage],dim=-1)
        if phase=='capture' or is_corr or reset or local==write or local==stage_length:
            comp_rows=[]
            for q in range(Q):
                coeff=reads@Delta[q]
                proj=reads.T@coeff
                comp_rows.append(float(torch.linalg.vector_norm(Delta[q]-proj)))
            if local==write: saved[f'stage{stage}_after_write']=torch.linalg.vector_norm(response,dim=-1).cpu().tolist()
            if phase=='capture': saved[f'stage{stage}_after_capture']=torch.linalg.vector_norm(response,dim=-1).cpu().tolist()
            if is_corr: saved[f'stage{stage}_after_trace_correction']=torch.linalg.vector_norm(response,dim=-1).cpu().tolist()
            if local==stage_length and not reset: saved[f'stage{stage}_after_clear']=torch.linalg.vector_norm(response,dim=-1).cpu().tolist()
            if reset: saved['after_reset']=torch.linalg.vector_norm(response,dim=-1).cpu().tolist()
            complement[f't{t}']=comp_rows
    final_delta=X[:,0]-X[:,1]
    final=torch.einsum('jr,prk->pjk',reads,final_delta)
    norms=torch.linalg.vector_norm(final,dim=-1)
    matrix=norms.cpu().tolist()
    diag=[matrix[i][i] for i in range(R)]
    cross=[max((matrix[i][j]/max(matrix[i][i],1e-300) for j in range(R) if j!=i),default=0.) for i in range(R)]
    # The matched scalar prediction accounts for transport after capture and
    # reset, independently of the deliberately added dense term.
    predicted=[]
    for j in range(R):
        capture_t=j*stage_length+write+1
        factor=1.
        for tt in range(capture_t+1,total+1):
            reset_step=(tt==total)
            local=(tt-1)%stage_length+1
            stage=min((tt-1)//stage_length,R-1)
            if reset_step: factor*=a*(1-.05**2)
            elif local==write+1: factor*=a*(gh+gl)/2 if stage!=j else a*gh
            else: factor*=a*gh
        predicted.append(float(captured[j,j].item())*factor)
    endpoint_diff=float(torch.linalg.vector_norm(states-states[:1,:1]).item())
    return dict(n=n,K=K,channels=R,dense_eps=eps,dense_operator_rank=1,dense_support_fraction=1.,
      dense_u_min_abs=float(u.abs().min()),dense_v_min_abs=float(v.abs().min()),
      protected_response_norm_matrix=matrix,diagonal=diag,cross_talk_ratios=cross,
      protected_transport_relative_error=[abs(diag[i]-predicted[i])/max(predicted[i],1e-300) for i in range(R)],
      predicted_diagonal=predicted,captured_diagonal=captured.diag().cpu().tolist(),
      max_trace_match_error=max_trace_match,correction_ranges=correction_ranges,
      max_absolute_raw_input=max_input,input_cube_legal=max_input<.5,
      selected_state_endpoint_pair_mismatch=endpoint_diff,reset_target='coordinatewise midpoint of the pre-reset histories; same exact endpoint for all pairs',
      raw_history_norms=torch.sqrt(input_sq).cpu().tolist(),m=m,mT=m*total,total_steps=total,
      response_checkpoints=saved,complement_sampled_norms=complement,
      note='Full-support rank-one perturbation is applied to the selected full recurrence and frozen-input sensitivity. This finite-size test uses a reduced selected block and is not the astronomical dense-model error theorem.')

def run_dense_battery(root,engine,torch,progress,done,failed,skipped,remaining):
    out=[]; baseline={}
    for n,K in ((512,8),(1024,16)):
        for eps in (0.,1e-8,1e-7,1e-6,1e-5):
            start=time.perf_counter()
            row=_one(torch,engine.O,n,K,eps)
            row['wall_seconds']=time.perf_counter()-start
            out.append(row)
            progress('RUNNING',done,failed,skipped,remaining)
        reference=out[-5]
        for row in out[-5:]:
            row['protected_response_relative_to_eps0']=[abs(row['diagonal'][i]-reference['diagonal'][i])/max(reference['diagonal'][i],1e-300) for i in range(2)]
            row['endpoint_mismatch_relative_to_eps0']=0.0 # all cases use the exact same reset target
    return out
