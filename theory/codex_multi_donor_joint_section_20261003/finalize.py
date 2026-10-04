"""Provenance and additive notebook/index preparation; no numerical work."""
import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
NOTE='Codex_Research.md'
STAGE=HERE.relative_to(ROOT).as_posix()+'/'
MARKER=b'### Private renewal Gamma resume'
ENTRY=(HERE/'RESUME_ENTRY.md').read_bytes()
TITLE=ENTRY.splitlines()[0]

def git(*args,data=None):
    return subprocess.run(['git',*args],cwd=ROOT,input=data,
        stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True).stdout

def verify():
    frozen=json.loads((HERE/'SOURCE_HASHES.json').read_text(encoding='utf-8-sig'))
    records=[]
    for item in frozen['sources']:
        actual=hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()
        if actual!=item['sha256']:
            raise RuntimeError('Frozen source changed: '+item['path'])
        records.append(dict(path=item['path'],sha256=actual,unchanged=True))
    result=json.loads((HERE/'checks_result.json').read_text())
    script_hash=hashlib.sha256((HERE/'checks.py').read_bytes()).hexdigest()
    if result['status']!='PASS' or not all(x['passed'] for x in result['checks']):
        raise RuntimeError('Numerical checks not all PASS')
    if result['script_sha256']!=script_hash:
        raise RuntimeError('Checked numerical script changed')
    if result['peak_observed_process_threads']>8 or result['gpu_cuda_calls']!=0:
        raise RuntimeError('Resource audit failed')
    return frozen,records,result

def append():
    path=ROOT/NOTE
    old=path.read_bytes()
    if TITLE not in old:
        if MARKER not in old:
            raise RuntimeError('Notebook insertion marker missing')
        new=old.replace(MARKER,ENTRY+b'\n'+MARKER,1)
        path.write_bytes(new)
        # Existing bytes are preserved exactly around the insertion.
        if new.replace(ENTRY+b'\n',b'',1)!=old:
            raise RuntimeError('Non-additive notebook edit')
    else:
        new=old
        if ENTRY not in new:
            raise RuntimeError('Notebook entry differs from frozen entry')
    return dict(before_sha256=hashlib.sha256(old).hexdigest(),
        after_sha256=hashlib.sha256(new).hexdigest(),
        method='byte insertion; existing working-tree content preserved')

def stage_note():
    staged=git('diff','--cached','--name-only').decode().splitlines()
    if any(not (x==NOTE or x.startswith(STAGE)) for x in staged):
        raise RuntimeError('Unrelated staged changes; leave them untouched')
    head=git('show','HEAD:'+NOTE)
    if TITLE in head:
        raise RuntimeError('Entry already in HEAD')
    if MARKER not in head:
        raise RuntimeError('HEAD notebook marker missing')
    desired=head.replace(MARKER,ENTRY+b'\n'+MARKER,1)
    blob=git('hash-object','-w','--stdin',data=desired).decode().strip()
    git('update-index','--cacheinfo','100644',blob,NOTE)
    if git('show',':'+NOTE)!=desired:
        raise RuntimeError('Index notebook mismatch')
    if desired.replace(ENTRY+b'\n',b'',1)!=head:
        raise RuntimeError('Non-additive staged notebook')
    print('Only the new notebook entry staged; unrelated working edits retained.')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--append-note',action='store_true')
    p.add_argument('--stage-note',action='store_true')
    p.add_argument('--audit',action='store_true')
    args=p.parse_args()
    frozen,records,result=verify()
    note=append() if args.append_note else None
    if args.audit:
        files=[]
        for path in sorted(HERE.iterdir()):
            if path.is_file() and path.name!='FINAL_AUDIT.json':
                files.append(dict(path=path.name,
                    sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
        audit=dict(completed_utc=datetime.now(timezone.utc).isoformat(),
            source_commit=frozen['source_commit'],
            pre_commit_head=git('rev-parse','HEAD').decode().strip(),
            frozen_sources=records,new_file_hashes=files,
            checks_passed=len(result['checks']),
            resources={key:result[key] for key in (
                'cpu_seconds','wall_seconds','peak_observed_process_threads',
                'peak_observed_working_set_bytes','gpu_cuda_calls','workers')},
            notebook=note,scope='new research folder plus additive Codex resume only',
            theorem_status='internally checked; new independent review pending',
            accepted_global_threshold_bracket='unchanged [1/4,3/4]',
            complete_corridor_closed=False,new_superlinear_section=False)
        (HERE/'FINAL_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n')
    if args.stage_note:
        stage_note()
    print('Frozen source hashes and numerical-script hash verified.')
