"""Source preservation, result consistency and reproduction manifest. No experiments."""
import json,hashlib,subprocess,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
TARGET='1a8203e2ced0a68017f27e507c1a92c4fb9c91ad'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((HERE/n).read_text())
def main():
    assert git('rev-parse','HEAD')==TARGET and not git('diff','--name-only') and not git('diff','--cached','--name-only')
    own='theory/'+HERE.name
    assert all(x.endswith(own+'/') for x in git('status','--porcelain').split('?? ')[1:])
    sources={};previous=[]
    dirs=['theory/claude_remaining_channels_20261020']
    for nm,root in [('codex_pr37_independent_audit_20261020','E:/AI-Architecture-Research-PR37-audit'),
                    ('codex_pr37_step35_audit_20261020','E:/AI-Architecture-Research-PR37-step35-audit'),
                    ('codex_pr37_step36_audit_20261020','E:/AI-Architecture-Research-PR37-step36-audit')]:
        folder='theory/'+nm;dirs.append(folder);same=crlf=0
        files=git('ls-tree','-r','--name-only',TARGET,'--',folder).splitlines()
        for rel in files:
            p=ROOT/rel;q=Path(root)/rel;assert q.is_file(),str(q)
            a=p.read_bytes();b=q.read_bytes()
            if a==b:same+=1
            else:assert a.replace(b'\r\n',b'\n')==b.replace(b'\r\n',b'\n'),rel;crlf+=1
        previous.append({'folder':folder,'files':len(files),'byte_identical':same,'CRLF_only':crlf})
    for folder in dirs:
        for rel in git('ls-tree','-r','--name-only',TARGET,'--',folder).splitlines():sources[rel]=sha(ROOT/rel)
    for folder,name in [('claude_remaining_channels_20261020','filtered_check.py'),('claude_lemma_m_rest_20261016','colsim.py')]:
        assert sha(HERE/'author_comparison'/folder/name)==sha(ROOT/'theory'/folder/name)
    author=read('author_comparison/claude_remaining_channels_20261020/filtered_check_result.json')
    assert len(author['C_staircase'])==6 and author['E_kernel_pair']['endpoint_gap_max_abs']<1e-12
    op=read('operator_results.json');assert op['exact']['cases']==72 and len(op['interval_staircases'])==10
    kernels=read('kernel_results.json');cost=read('cost_results.json');stair=read('stair_results.json');val=read('full_crosscheck_results.json')
    assert len(kernels)==2 and len(cost)==4 and len(stair)==3 and len(val)==3
    ref=author['E_kernel_pair'];r=kernels[0]
    assert abs(r['kernel_difference_term']-ref['term_kernel'])<1e-8
    assert abs(r['raw_population_readout']-ref['readout_difference'])<1e-8
    for r in kernels+cost+stair:
        assert r['max_input']<.5 and r['endpoint_ret_pair_difference']==0
        assert r['row_recursion_error']<1e-12 and abs(r['split_error'])<1e-7
        assert r['mT']==max(r['m_plus_minus'])*r['T']
        assert r['P']+2<r['n']//4
    for r in stair:
        assert r['forcing_match_max_error']<1e-6 and r['source_gate_min']>0
        assert r['readout_over_max_phi']>2 and r['legal_retainer_readout_over_A_max_phi']>2
        assert r['Gamma']==0 and r['kernel_difference_term']==0
        assert abs(r['raw_population_readout'])<=r['variation_Delta_phi']+2*r['capture_difference_L1']
    assert all(cost[i]['Gamma_over_Zinf_inputL1']<cost[i+1]['Gamma_over_Zinf_inputL1'] for i in range(len(cost)-1))
    assert all(r['selected_query_error_allowing_complement_tie']<1e-9 for r in val)
    paths=[]
    for target in re.findall(r'\[[^\]\n]+\]\(([^)\s]+)\)',(HERE/'AUDIT.md').read_text(encoding='utf-8')):
        if target.startswith(('https://','http://','#')):continue
        assert (HERE/target.split('#')[0]).resolve().is_file(),target;paths.append(target)
    files={str(p.relative_to(HERE)).replace('\\','/'):sha(p) for p in HERE.rglob('*')
           if p.is_file() and '__pycache__' not in p.parts and p.name!='verification_manifest.json'}
    report={'target':TARGET,'tracked_diff':[],'previous_audits':previous,'source_SHA256':sources,'audit_SHA256':files,
            'relative_links_verified':paths,'independent_exact_cases':72,'independent_exact_steps':op['exact']['exact_steps'],
            'independent_kernel_operator_cases':40,'independent_interval_staircases':10,
            'independent_legal_histories_pairs':len(kernels)+len(cost)+len(stair),'full_vector_crosschecks':len(val),
            'independent_stair_seconds':sum(r['seconds'] for r in stair),'author_full_seconds':author['seconds'],
            'max_independent_legal_input':max(r['max_input'] for r in kernels+cost+stair),
            'max_independent_split_error':max(abs(r['split_error']) for r in kernels+cost+stair),
            'author_files_edited':False,'notebooks_or_AGENTS_edited':False,'GitHub_mutations':'none'}
    (HERE/'verification_manifest.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if 'SHA256' not in k and k!='relative_links_verified'},indent=2))
if __name__=='__main__':main()
