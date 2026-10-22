"""Rerun small author checks in a disposable audit copy, preserving source snapshots."""
from pathlib import Path
import subprocess,sys,os,shutil,json,time,importlib.util
ROOT=Path(__file__).resolve().parent
SRC=ROOT/'sources/theory/claude_lemma_m_three_memory_20261019'
RUN=ROOT/'author_runs'
RUN.mkdir(exist_ok=True)
for p in SRC.rglob('*.py'):
    out=RUN/p.relative_to(SRC);out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,out)
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
commands=[('constants_seq.py',[]),('constants_so.py',[]),('exp_exact_checks.py',[]),('exp_verify_probe.py',[]),('external_20261018/lemma_m_three_memory_probe.py',[]),('exp_S_check.py',['16384','700','5'])]
results=[]
for script,args in commands:
    t=time.perf_counter()
    p=subprocess.run([sys.executable,'-I',str(RUN/script),*args],cwd=RUN,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=120)
    tag=Path(script).stem
    (RUN/(tag+'_stdout.txt')).write_text(p.stdout)
    (RUN/(tag+'_stderr.txt')).write_text(p.stderr)
    rec={'script':script,'args':args,'returncode':p.returncode,'seconds':time.perf_counter()-t}
    print(json.dumps(rec),flush=True);results.append(rec)
spec=importlib.util.spec_from_file_location('author_so',RUN/'constants_so.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
adversarial=[]
for n in ('1e18','1e40','1e160','1e164','1e165','1e166','1e168','1e180'):
    try:
        v=mod.coeffs(n);adversarial.append({'n':n,'epsSO':v['eps_SO'],'e':v['e'],'valid':v['eps_SO']<=.5})
    except Exception as exc:adversarial.append({'n':n,'exception':type(exc).__name__,'message':str(exc)})
(ROOT/'author_run_results.json').write_text(json.dumps({'runs':results,'adversarial':adversarial},indent=2))
print(json.dumps(adversarial,indent=2),flush=True)
