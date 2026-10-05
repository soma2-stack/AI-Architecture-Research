"""Provenance and additive Codex-note/index update. No numerical libraries."""
import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent; ROOT=HERE.parent.parent
NOTE='Codex_Research.md'; STAGE=HERE.relative_to(ROOT).as_posix()+'/'
MARKER=b'### Multi-donor joint-section resume'
ENTRY=(HERE/'RESUME_ENTRY.md').read_bytes(); TITLE=ENTRY.splitlines()[0]

def git(*args,data=None):
    return subprocess.run(['git',*args],cwd=ROOT,input=data,stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,check=True).stdout

def verify():
    frozen=json.loads((HERE/'SOURCE_HASHES.json').read_text(encoding='utf-8-sig'))
    records=[]
    for item in frozen['sources']:
        actual=hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()
        if actual!=item['sha256']: raise RuntimeError('Changed historical source '+item['path'])
        records.append(dict(path=item['path'],sha256=actual,unchanged=True))
    checks=json.loads((HERE/'checks_result.json').read_text())
    if checks['status']!='PASS' or not all(x['passed'] for x in checks['checks']):
        raise RuntimeError('Checks failed')
    if checks['script_sha256']!=hashlib.sha256((HERE/'checks.py').read_bytes()).hexdigest():
        raise RuntimeError('Checked script changed')
    if checks['peak_observed_process_threads']>8 or checks['gpu_cuda_calls']:
        raise RuntimeError('Resource violation')
    return frozen,records,checks

def note():
    path=ROOT/NOTE; old=path.read_bytes()
    if TITLE in old:
        if ENTRY not in old: raise RuntimeError('Resume conflict')
        return dict(method='already inserted exactly')
    if MARKER not in old: raise RuntimeError('Missing marker')
    new=old.replace(MARKER,ENTRY+b'\n'+MARKER,1)
    if new.replace(ENTRY+b'\n',b'',1)!=old: raise RuntimeError('Non-additive edit')
    path.write_bytes(new)
    return dict(method='byte insertion only',before_sha256=hashlib.sha256(old).hexdigest(),
                after_sha256=hashlib.sha256(new).hexdigest())

def stage_note():
    staged=git('diff','--cached','--name-only').decode().splitlines()
    if any(not (x==NOTE or x.startswith(STAGE)) for x in staged):
        raise RuntimeError('Unrelated staged changes; preserve')
    head=git('show','HEAD:'+NOTE)
    if TITLE in head or MARKER not in head: raise RuntimeError('Unexpected HEAD resume')
    desired=head.replace(MARKER,ENTRY+b'\n'+MARKER,1)
    blob=git('hash-object','-w','--stdin',data=desired).decode().strip()
    git('update-index','--cacheinfo','100644',blob,NOTE)
    if git('show',':'+NOTE)!=desired: raise RuntimeError('Index mismatch')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--append-note',action='store_true')
    parser.add_argument('--audit',action='store_true')
    parser.add_argument('--stage-note',action='store_true')
    args=parser.parse_args(); frozen,records,checks=verify()
    change=note() if args.append_note else None
    if args.audit:
        entries=[]
        for path in sorted(HERE.iterdir()):
            if path.is_file() and path.name!='FINAL_AUDIT.json':
                entries.append(dict(path=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
        audit=dict(completed_utc=datetime.now(timezone.utc).isoformat(),
            source_commit=frozen['source_commit'],pre_commit_head=git('rev-parse','HEAD').decode().strip(),
            frozen_sources=records,new_files=entries,notebook=change,
            checked_script_unchanged=True,checks_passed=len(checks['checks']),
            resources={key:checks[key] for key in ('cpu_seconds','wall_seconds',
                'peak_observed_process_threads','peak_observed_rss_bytes','gpu_cuda_calls','workers')},
            theorem_status='new derivation internally checked; independent hostile review pending',
            latest_Claude_conditional_document='not located; exact hypothesis requested',
            uniform_one_over_survivors_bound='refuted under the literal entry formulation',
            superlinear_section_proved=False,complete_corridor_closed=False,
            global_bracket='unchanged [1/4,3/4]',scope='new folder and additive Codex resume only')
        (HERE/'FINAL_AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n')
    if args.stage_note: stage_note()
    print('Historical hashes unchanged; checked script exact; scope/resource audit PASS.')
