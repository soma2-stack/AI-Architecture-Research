"""Known algebraic representations, with explicit storage and reconstruction."""
import time
import numpy as np
import torch
import core as c

def factor(matrix,tolerance=None):
    tolerance=c.CFG['factor_internal_relative_tolerance'] if tolerance is None else tolerance
    u,s,v=torch.linalg.svd(matrix,full_matrices=False)
    total=float(torch.linalg.vector_norm(s))
    rank=0
    while rank<len(s) and float(torch.linalg.vector_norm(s[rank:]))>tolerance*max(total,1e-30):rank+=1
    return u[:,:rank]*s[:rank],v[:rank],s

def rank_info(matrix):
    values=torch.linalg.svdvals(matrix)
    maximum=float(values[0]) if len(values) else 0.
    return {'singular_values':values.tolist(),
            'ranks':{str(t):int(torch.count_nonzero(values>maximum*t)) if maximum else 0 for t in c.CFG['numerical_rank_relative_thresholds']}}

def support(model,S):
    result={'exact_nonzero':int(torch.count_nonzero(S)),
            'thresholds':{str(t):{'count':int(torch.count_nonzero(S.abs()>t)),
                                'fraction':float((S.abs()>t).double().mean())} for t in c.CFG['support_thresholds']},
            **rank_info(S),'blocks':[]}
    for state_layer in range(model.depth):
        for parameter_layer in range(model.depth):
            cols=[i for g in model.groups if g['layer']==parameter_layer for i in range(g['start'],g['end'])]
            block=S[state_layer*model.n:(state_layer+1)*model.n,cols]
            result['blocks'].append({'state_layer':state_layer+1,'parameter_layer':parameter_layer+1,
                                     'size':block.numel(),'nonzero':int(torch.count_nonzero(block)),
                                     'threshold_counts':{str(t):int(torch.count_nonzero(block.abs()>t)) for t in c.CFG['support_thresholds']},
                                     **rank_info(block)})
    return result

def probe_gradient(model,h,q,y,S):
    cot,direct=model.terminal(h,q,y);return cot@S+direct

def compression(model,S,h,q,y,reference_gradient):
    probes=[]
    L,R,s=factor(S)
    candidates=[('matrix_minimum_rank',L,R)]
    u,sv,v=torch.linalg.svd(S,full_matrices=False)
    for rank in (1,2,4):
        rank=min(rank,len(sv));candidates.append((f'matrix_rank{rank}',u[:,:rank]*sv[:rank],v[:rank]))
    for name,left,right in candidates:
        reconstructed=left@right;groups=c.grouped(model,probe_gradient(model,h,q,y,reconstructed),reference_gradient)
        error=c.metric(reconstructed,S)
        probes.append({'name':name,'rank':left.shape[1],
                       'stored_values':left.numel()+right.numel(),'reconstruction':error,
                       'groups':groups,'passes':c.passes(error) and all(c.passes(g) for g in groups),
                       'scope':'offline snapshot; source full matrix and SVD scratch also required; no online-cheap claim'})
    # S_W columns ordered owner,input. Rearranged SVD yields an exact Kronecker sum.
    compressed=S.clone();values=0;terms=[];rank1=S.clone();rank1_values=0;owner_slices=[]
    for g in model.groups:
        if g['name']!='W':
            values+=model.N*(g['end']-g['start']);rank1_values+=model.N*(g['end']-g['start']);continue
        tensor=S[:,g['start']:g['end']].reshape(model.N,model.n,model.n)
        rearranged=tensor.reshape(model.N*model.n,model.n)
        l,r,sv=factor(rearranged)
        compressed[:,g['start']:g['end']]=(l@r).reshape(model.N,model.n*model.n)
        values+=l.numel()+r.numel()
        u,sval,v=torch.linalg.svd(rearranged,full_matrices=False)
        rank1[:,g['start']:g['end']]=((u[:,:1]*sval[:1])@v[:1]).reshape(model.N,model.n*model.n)
        rank1_values+=model.N*model.n+model.n
        terms.append({'layer':g['layer']+1,'terms':l.shape[1],'values':l.numel()+r.numel(),'singular_values':sv.tolist()})
        owner_slices.append({'layer':g['layer']+1,'ranks':[rank_info(tensor[:,owner,:])['ranks'] for owner in range(model.n)]})
    for name,reconstruction,stored in [('kronecker_minimum_sum',compressed,values),('kronecker_one_term',rank1,rank1_values)]:
        groups=c.grouped(model,probe_gradient(model,h,q,y,reconstruction),reference_gradient);error=c.metric(reconstruction,S)
        probes.append({'name':name,'stored_values':stored,'reconstruction':error,'groups':groups,
                       'passes':c.passes(error) and all(c.passes(g) for g in groups),
                       'terms':terms if name.endswith('sum') else None,'owner_slices':owner_slices,
                       'scope':'offline rearrangement; non-W groups explicit, no online-cheap claim'})
    return probes

def factor_run(model,x,q,y):
    start=time.perf_counter();cpu=time.process_time();h=torch.zeros(model.N);L=torch.zeros(model.N,0);R=torch.zeros(0,model.P)
    trajectory=[];derivative=0.;ranks=[];max_stored=0;peak=0
    for xt in x:
        before=time.perf_counter();h,A,B,workspace=c.partials(model,h,xt)
        S=A@(L@R)+B
        L,R,singular_values=factor(S);ranks.append(L.shape[1]);max_stored=max(max_stored,L.numel()+R.numel())
        # Fresh contiguous copies prevent retained views from hiding discarded SVD factors.
        L=L.clone();R=R.clone()
        peak=max(peak,workspace+5*model.N*model.P+4*(L.numel()+R.numel())+model.N*model.N)
        del A,B,S,singular_values
        derivative+=time.perf_counter()-before;trajectory.append(h)
    before=time.perf_counter();S=L@R;cot,direct=model.terminal(h,q,y);g=cot@S+direct;derivative+=time.perf_counter()-before
    return {'gradient':g,'trajectory':torch.stack(trajectory),'S':S,'seconds':time.perf_counter()-start,
            'cpu_seconds':time.process_time()-cpu,'derivative_seconds':derivative,
            'stored_derivative_scalars':L.numel()+R.numel(),'peak_stored_derivative_scalars':max_stored,
            'derivative_bytes':8*(L.numel()+R.numel()),'index_bytes':0,'ranks_over_time':ranks,
            'peak_derivative_scratch_bound_scalars':peak,'terminal_query_scalars':model.N*model.P+model.N+2*model.P,
            'scratch_scope':'full temporary matrix and SVD scratch; no full persistent backup or history'}

def kronecker_sum_run(model,x,q,y):
    assert model.depth==1
    start=time.perf_counter();cpu=time.process_time();n=model.n;h=torch.zeros(n);terms=[];trajectory=[];derivative=0.
    wg=model.layer_groups[0]['W'];other_cols=torch.tensor([i for i in range(model.P) if not wg['start']<=i<wg['end']],dtype=torch.int64)
    remainder=torch.zeros(n,len(other_cols));workspace=0
    for xt in x:
        before=time.perf_counter();h,A,B,workspace=c.partials(model,h,xt)
        # One W contribution each time. Exact deterministic sum, no stochastic merge.
        gain=torch.ones(n) if model.linear_shared else 1-h**2
        terms=[(A@left,right) for left,right in terms]
        terms.append((torch.diag(gain),xt.clone()))
        remainder=A@remainder+B[:,other_cols]
        del A,B
        derivative+=time.perf_counter()-before;trajectory.append(h)
    before=time.perf_counter();S=torch.zeros(n,model.P);S[:,other_cols]=remainder
    for left,right in terms:S[:,wg['start']:wg['end']]+=torch.einsum('ij,k->ijk',left,right).reshape(n,n*n)
    cot,direct=model.terminal(h,q,y);g=cot@S+direct;derivative+=time.perf_counter()-before
    entries=remainder.numel()+sum(left.numel()+right.numel() for left,right in terms)
    metadata=other_cols.numel()*8
    return {'gradient':g,'trajectory':torch.stack(trajectory),'S':S,'seconds':time.perf_counter()-start,
            'cpu_seconds':time.process_time()-cpu,'derivative_seconds':derivative,
            'stored_derivative_scalars':entries,'derivative_bytes':entries*8+metadata,'index_bytes':metadata,
            'kronecker_terms':len(terms),'terminal_query_scalars':n*model.P+n+2*model.P,
            'peak_derivative_scratch_bound_scalars':3*entries+workspace+n*model.P,
            'scratch_scope':'exact unfused sum retains every factor; O(T) factor history explicitly counted'}
