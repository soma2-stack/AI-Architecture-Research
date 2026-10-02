"""Append final byte hashes/resources; do not change any measured output."""
from pathlib import Path
import json
import hashlib
import subprocess

root=Path(__file__).resolve().parent
summary=json.loads((root/'analysis/summary.json').read_text())
checks=json.loads((root/'analysis/independent_numerical_checks.json').read_text())
resources=summary['resources']
final=dict(measured_cpu_seconds=resources['measurement_cpu_seconds']+summary['analysis_cpu_seconds']+checks['cpu_seconds'],
           active_measured_wall_seconds=resources['measurement_wall_seconds']+summary['analysis_wall_seconds']+checks['wall_seconds'],
           peak_measured_process_bytes=max(resources['peak_measurement_rss_bytes'],summary['analysis_peak_working_set_bytes'],checks['peak_working_set_bytes']),
           gpu_seconds=0,cuda_runtime=checks['cuda_runtime'],
           unmeasured_setup_repair_cpu_allowance_seconds=10,
           excluded='imports before timers, reasoning, shell/Git/tool latency; allowance is not a measurement')
dest=root/'analysis/final_resources.json'
if dest.exists(): raise RuntimeError('Refusing to replace final resource record')
dest.write_text(json.dumps(final,indent=2)+'\n')
files=sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='RESULTS_MANIFEST.json')
record=dict(head_before_result_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
            status='completed numerical diagnostic, no new theorem/certificate',
            primary_setup_commit='ff8aa58',secondary_setup_commit='9e22766',
            files={p.relative_to(root).as_posix():dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files})
dest=root/'RESULTS_MANIFEST.json'
if dest.exists(): raise RuntimeError('Refusing to replace manifest')
dest.write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(dict(resources=final,manifest_files=len(files)),indent=2))
