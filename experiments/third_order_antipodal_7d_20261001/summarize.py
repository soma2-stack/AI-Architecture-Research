"""Post-result diagnostics from frozen artifacts only; no candidate evaluations."""
import sys,time
sys.dont_write_bytecode=True
CPU=time.process_time(); WALL=time.perf_counter()
import common as c
Q=c.Q
r=c.json.loads((c.ROOT/'result.json').read_text())
check=c.json.loads((c.ROOT/'checks.json').read_text())
dec=c.json.loads((c.ROOT/'remainder_decomposition_256.json').read_text())['M3_components']
o=r['attempts'][-1]['certificate']; candidate=c.json.loads((c.ROOT/'candidate.json').read_text())
faces=[v for v in check['faces'] if v['precision']==256]
for i,v in enumerate(faces):
    v['M3_components']={name:vals[i] for name,vals in dec.items()}
    v['M3_component_fractions']={name:vals[i]/sum(x[i] for x in dec.values()) for name,vals in dec.items()}
    v['relative_reduction_required_in_M3']=(float(Q(o['mu_tilde'][i]))*(1-o['center_rows_upper'][i])-1e-3)/v['third_order_penalty']
# Above is the permitted M3 fraction, not a demonstrated achievable tightening.
s=c.json.loads((c.ROOT/'search_summary.json').read_text())
resource_files=['tests.json','bootstrap_resources.json','selection_resources.json','checks.json']
other=[c.json.loads((c.ROOT/p).read_text()) for p in resource_files]
peak=max([r['peak_working_set_bytes'],s['parent_peak_working_set_bytes']]+[x['peak_working_set_bytes'] for x in other]+[x['peak_working_set_bytes'] for x in s['results']])
worker_peaks=sorted([x['peak_working_set_bytes'] for x in s['results']],reverse=True)
tot=r['total_cpu_seconds']+check['cpu_seconds']
wall=r['wall_seconds']+s['wall_seconds']+sum(x['wall_seconds'] for x in other)
out={'status':r['status'],'first_failed_face':next(x['face'] for x in faces if not x['passes']),
    'weakest_face':min(faces,key=lambda x:x['beta'])['face'],'faces':faces,
    'eta_hidden':o['eta_hidden'],'radius':float(Q(o['radius'])),
    'hidden_forcing_upper':o['hidden_forcing_upper'],
    'hidden_inclusion_limit':float((1-Q(o['eta_hidden']))*Q(candidate['ah'])),
    'normal_half_width':float(Q(candidate['ah'])),'tangent_half_widths':[float(Q(x)) for x in candidate['a']],
    'search_evaluations':sum(x['evals'] for x in s['results']),
    'invalid_search_evaluations':sum(x['invalid'] for x in s['results']),
    'cpu_seconds_before_summary':tot,'summed_phase_wall_seconds':wall,
    'largest_measured_process_peak_bytes':peak,
    'conservative_concurrent_peak_sum_bytes':s['parent_peak_working_set_bytes']+sum(worker_peaks[:2]),
    '8d_diagnostic':c.json.loads((c.ROOT/'8d_numerical_diagnostic.json').read_text())['attempts'],
    'candidate_sha256':c.sha(c.ROOT/'candidate.json'),'accepted_kernel_sha256':c.sha(c.ACCEPTED/'kernel.py'),
    'gpu_seconds':0,'gpu_used':False}
out['summary_cpu_seconds']=time.process_time()-CPU
out['measured_cpu_seconds']=tot+out['summary_cpu_seconds']
out['separate_development_allowance_cpu_seconds']=5
c.write('diagnostics.json',out)
print(c.json.dumps(out,indent=2))
