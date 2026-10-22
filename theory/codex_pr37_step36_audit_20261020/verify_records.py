"""Read-only provenance, outcome, source-preservation and link verification.
Writes only this audit's final manifest. No experiments.
"""
import json,hashlib,subprocess,re
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
TARGET='18f80054576df5e9c760fb4712c8591bd3e0422e'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    assert git('rev-parse','HEAD')==TARGET
    assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
    folders=['theory/claude_remaining_channels_20261020','theory/codex_pr37_independent_audit_20261020',
             'theory/codex_pr37_step35_audit_20261020']
    sources={}
    for folder in folders:
        for rel in git('ls-tree','-r','--name-only',TARGET,'--',folder).splitlines():
            sources[rel]=sha(ROOT/rel)
    previous=[]
    for name,oldroot in [('codex_pr37_independent_audit_20261020',Path('E:/AI-Architecture-Research-PR37-audit')),
                         ('codex_pr37_step35_audit_20261020',Path('E:/AI-Architecture-Research-PR37-step35-audit'))]:
        identical=normalized=0
        rels=git('ls-tree','-r','--name-only',TARGET,'--','theory/'+name).splitlines()
        for rel in rels:
            a=ROOT/rel;b=oldroot/rel
            assert b.is_file(),str(b)
            if a.read_bytes()==b.read_bytes():identical+=1
            else:
                assert a.read_bytes().replace(b'\r\n',b'\n')==b.read_bytes().replace(b'\r\n',b'\n'),rel
                normalized+=1
        previous.append({'folder':name,'files':len(rels),'byte_identical':identical,'CRLF_only':normalized})
    for script in ('repairs2_check.py','phase2_check.py'):
        assert sha(HERE/'author_comparison'/script)==sha(ROOT/'theory/claude_remaining_channels_20261020'/script)
    rows=json.loads((HERE/'b6_legal_results.json').read_text());valid=json.loads((HERE/'b6_validation.json').read_text())
    assert len(rows)==27 and len(valid)==6
    assert all(r['max_input']<.5 and r['row_recursion_error']<1e-10 and r['forced_capture_decomposition_error']<1e-10 for r in rows)
    assert all(r['within_H'] and r['small_budget'] for r in rows if r['n']>=10**8)
    auto=[r for r in rows if r['source']=='autonomous'];assert len(auto)==3
    for r in auto:
        dd=r['diagnostics'][0]
        assert r['peak_actual_width_m']==0 and dd['initial_is_zero']
        assert dd['P_Psi_star']>dd['C1_scale_using_min_bath']+dd['absolute_capture_input_budget']
    algebra=json.loads((HERE/'algebra_results.json').read_text())
    assert max(algebra['initial_vector_bounds']['worst_ratios_a_b_c'])<1
    op=json.loads((HERE/'switching_adjoint_results.json').read_text());assert len(op['cases'])==27
    doc=(HERE/'AUDIT.md').read_text(encoding='utf-8');links=[]
    for label,target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',doc):
        if target.startswith(('https://','http://','#')):continue
        f=(HERE/target.split('#')[0]).resolve();assert f.is_file(),(label,target)
        links.append(target)
    files={str(p.relative_to(HERE)).replace('\\','/'):sha(p) for p in HERE.rglob('*')
           if p.is_file() and '__pycache__' not in p.parts and p.name!='verification_manifest.json'}
    result={'target':TARGET,'tracked_diffs':[],'source_SHA256':sources,'old_audit_comparison':previous,
            'audit_files_SHA256':files,'verified_relative_links':links,
            'legal_cases':len(rows),'legal_H_and_small_budget_cases':sum(r['within_H'] and r['small_budget'] for r in rows),
            'legal_simulation_seconds':sum(r['seconds'] for r in rows),'operator_cases':len(op['cases']),
            'full_vector_cases':len(valid),'max_legal_input':max(r['max_input'] for r in rows),
            'max_recurrence_error':max(r['row_recursion_error'] for r in rows),
            'max_forced_capture_decomposition_error':max(r['forced_capture_decomposition_error'] for r in rows),
            'max_full_query_error':max(r['readout_error'] for r in valid),'GitHub_actions':'none'}
    (HERE/'verification_manifest.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if 'SHA256' not in k and k!='verified_relative_links'},indent=2))
if __name__=='__main__':main()
