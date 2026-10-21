"""Read-only preservation/link checks; writes only this audit's verification manifest."""
from pathlib import Path
import hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def main():
    links=[]
    for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',(HERE/'AUDIT.md').read_text(encoding='utf-8')):
        if '://' in link:continue
        p=HERE/link.split('#')[0]; links.append({'target':link,'exists':p.exists()})
    assert all(r['exists'] for r in links)
    allruns=[]
    for f in ('retention_results.json','retention_large.json','retention_resets.json'):
        allruns+=json.loads((HERE/f).read_text())
    assert len(allruns)==19
    assert max(r['max_abs_actual_input'] for r in allruns)<.5
    assert all(r['mT']==r['peak_actual_width_m']*r['T'] for r in allruns)
    assert all(r['gap_integral_s_squared']>6 for r in allruns)
    assert git('rev-parse','HEAD')=='ac759bb3561fe0de6cf2553282d8ebee04018226'
    assert git('diff','--name-only')==''
    assert git('diff','--cached','--name-only')==''
    sources=json.loads((HERE/'source_manifest.json').read_text())
    assert all(s.get('unchanged_allowing_checkout_line_endings',True) for s in sources)
    records=[]
    for p in sorted(HERE.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts and p.name!='verification_manifest.json':
            records.append({'path':p.relative_to(HERE).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    manifest={'target_commit':git('rev-parse','HEAD'),'tracked_files_changed':False,'staged_files':[],'audit_status':git('status','--short'),'source_records':len(sources),'local_markdown_links':links,'E4_runs':len(allruns),'E4_elapsed_seconds_sum':sum(r['seconds'] for r in allruns),'max_input':max(r['max_abs_actual_input'] for r in allruns),'max_centered_over_peak':max(r['centered_over_peak'] for r in allruns),'all_mT_products_verified':True,'BLAS_threads_per_process':1,'maximum_concurrent_BLAS_processes':3,'GPU_used':False,'subagents_used':False,'push_or_merge':False,'syntax_check':'in-memory compile of all three independent verification scripts passed; each script executed successfully','bytecode_cache_note':'An optional py_compile cache rename returned Windows access denied; switched to compile() without cache writes. This did not affect executed mathematical checks.','files':records}
    (HERE/'verification_manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps({k:v for k,v in manifest.items() if k not in ('files','local_markdown_links')},indent=2))
if __name__=='__main__':main()
