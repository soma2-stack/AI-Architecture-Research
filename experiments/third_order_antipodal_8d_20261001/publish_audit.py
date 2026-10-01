"""Publication/provenance audit only. Does not compute or modify a certificate."""
import time
CPU=time.process_time();WALL=time.perf_counter()
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):(ROOT/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':
    f=json.loads((ROOT/'FROZEN.json').read_text())
    checks=[]
    def check(n,b):
        checks.append({'name':n,'passed':bool(b)})
        assert b,n
    check('frozen_local_files_unchanged',all(sha(ROOT/p)==h for p,h in f['local_hashes'].items()))
    check('dependency_chain_unchanged',all(sha(REPO/p)==h for p,h in f['source_hashes'].items()))
    check('all_239_historical_files_unchanged',len(f['historical_hashes'])==239 and all(sha(REPO/p)==h for p,h in f['historical_hashes'].items()))
    repair=json.loads((ROOT/'postofficial_export_repair.json').read_text())
    a=(ROOT/'finalize.py').read_text();b=(ROOT/'finalize_fixed.py').read_text()
    old='y'+chr(39)*2+'/y'+chr(39)*3+' and s_y*y'+chr(39)*3
    check('formatter_only_exact_documented_substitution',a.count(old)==1 and b==a.replace(old,'y^(2)/y^(3) and s_y*y^(3)'))
    check('formatter_hashes_preserved',sha(ROOT/'finalize.py')==repair['source_sha256'] and sha(ROOT/'finalize_fixed.py')==repair['repaired_sha256'])
    report=(ROOT/'REPORT.md').read_text()
    addition='''
## Publication repair disclosure

The first frozen finalize.py could not parse its report string because a
triple-prime formula closed a triple-single-quoted string. No audit code or
scientific computation ran in that failed export. The frozen original remains
byte-identical. finalize_fixed.py differs ONLY by replacing that report-text
notation with y^(2)/y^(3). It then completed all 36 checks. The repair and
hashes are preserved in postofficial_export_repair.json. Separately charge
1 CPU-s for that failed export. No candidate, kernel, bounds or proof changed.
FINAL_AUDIT.json records publication CPU time and aggregate budget usage.
'''
    assert '## Publication repair disclosure' not in report
    (ROOT/'REPORT.md').write_text(report+addition,encoding='utf-8')
    result=json.loads((ROOT/'result.json').read_text()); audit=json.loads((ROOT/'checks.json').read_text())
    seconds=time.process_time()-CPU
    total=audit['total_cpu_seconds']+repair['charged_CPU_seconds']+seconds
    check('accounted_budget_remains_below_1200_CPU_seconds',total<1200)
    write('FINAL_AUDIT.json',{'checks':checks,'passed':len(checks),'publication_cpu_seconds':seconds,
        'publication_wall_seconds':time.perf_counter()-WALL,'total_measured_CPU_seconds':audit['measured_cpu_seconds']+seconds,
        'failed_process_allowances_CPU_seconds':11,'total_accounted_CPU_seconds':total,
        'peak_ram_bytes':audit['peak_ram_bytes'],'GPU_seconds':0,'decision':result['status']})
    write('OUTPUT_MANIFEST.json',{'sha256':{p.name:sha(p) for p in ROOT.iterdir() if p.is_file() and p.name!='OUTPUT_MANIFEST.json'}})
    print(json.dumps({'checks':len(checks),'measured_CPU_seconds':audit['measured_cpu_seconds']+seconds,
                     'accounted_CPU_seconds':total,'decision':result['status']}))
