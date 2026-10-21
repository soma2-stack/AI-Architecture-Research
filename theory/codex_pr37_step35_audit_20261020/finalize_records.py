"""Preservation, source hashes, result consistency and local-link checks."""
import ast,hashlib,json,re,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
TARGET='c48640db6b677d52d109827d6d53bb0e2f005acf'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode().strip()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    assert git('rev-parse','HEAD')==TARGET
    assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
    source=[]
    dirs=['theory/claude_remaining_channels_20261020','theory/claude_lemma_m_bus_capacity_20261015','theory/claude_lemma_m_rest_20261016','theory/claude_dense_transfer_20261020']
    files=[ROOT/'AGENTS.md']
    for d in dirs:
        files.extend(p for p in (ROOT/d).iterdir() if p.is_file() and p.suffix in ('.md','.py','.json'))
    for p in files:
        rel=p.relative_to(ROOT).as_posix()
        original=subprocess.check_output(['git','show',TARGET+':'+rel],cwd=ROOT)
        same=original.replace(b'\r\n',b'\n')==p.read_bytes().replace(b'\r\n',b'\n')
        assert same,rel
        source.append({'path':rel,'commit':TARGET,'git_sha256':hashlib.sha256(original).hexdigest(),'working_sha256':digest(p),'unchanged_allowing_checkout_line_endings':same})
    snapshots=HERE/'sources'; snapshots.mkdir(exist_ok=True)
    older='c987408'; path='theory/claude_narrow_capture_hub_20261013/PROOF.md'
    data=subprocess.check_output(['git','show',older+':'+path],cwd=ROOT)
    saved=snapshots/'PR27_PROOF_c987408.md'; saved.write_bytes(data)
    source.append({'path':path,'commit':git('rev-parse',older),'saved_as':saved.relative_to(HERE).as_posix(),'sha256':digest(saved)})
    (HERE/'source_manifest.json').write_text(json.dumps(source,indent=2))
    copied=json.loads((HERE/'previous_audit_comparison.json').read_text())
    assert len(copied)==21 and all(r['matches_original_audit_allowing_checkout_line_endings'] for r in copied)
    records=[]
    for name in ('e7_finite.json','e7_contract.json','e7_bipolar.json','e7_controls.json'):
        records.extend(json.loads((HERE/name).read_text()))
    assert len(records)==66
    assert all(r['max_abs_actual_input']<.5 for r in records)
    assert all(r['mT']==r['T']*r['peak_actual_width_m'] for r in records)
    contract=json.loads((HERE/'e7_contract.json').read_text())
    assert all(r['within_H_n_width_source'] and r['within_small_budget'] for r in contract)
    assert all(r['cumulative_max_gate_deficit_E']>=r['E_from_source_pulse_to_T'] for r in records)
    for p in HERE.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    links=[]
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',(HERE/'AUDIT.md').read_text(encoding='utf-8')):
        if '://' in target:continue
        present=(HERE/target.split('#')[0]).exists(); links.append({'target':target,'exists':present}); assert present,target
    inventory=[]
    for p in sorted(HERE.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and p.name!='verification_manifest.json':
            inventory.append({'path':p.relative_to(HERE).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)})
    out={'target_commit':TARGET,'tracked_files_changed':False,'staged_files':[],'status':git('status','--short'),'previous_audit_files_unchanged':21,'source_records':len(source),'E7_runs':len(records),'E7_inside_H_and_small_budget':sum(r['within_H_n_width_source'] and r['within_small_budget'] for r in records),'E7_contract_series_runs':len(contract),'E7_elapsed_seconds_sum':sum(r['seconds'] for r in records),'max_actual_input':max(r['max_abs_actual_input'] for r in records),'all_actual_width_times_horizon_products_checked':True,'independent_validation':'six fresh full-vector cases plus previous full-vector reset control','independent_reset_reproductions':5,'BLAS_threads_per_process':1,'maximum_concurrent_BLAS_processes':2,'GPU_used':False,'subagents_used':False,'push_merge_or_author_branch_change':False,'syntax_AST_checks':'pass','markdown_links':links,'files':inventory}
    (HERE/'verification_manifest.json').write_text(json.dumps(out,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k not in ('files','markdown_links')},indent=2))
if __name__=='__main__':main()
