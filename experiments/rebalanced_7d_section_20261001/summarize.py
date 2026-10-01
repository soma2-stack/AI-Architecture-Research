"""Post-result reporting from saved artifacts only; no new candidate evaluation."""
import sys,time
sys.dont_write_bytecode=True
CPU=time.process_time();WALL=time.perf_counter()
import common as c
c.verify();Q=c.Q
r=c.json.loads((c.ROOT/'result.json').read_text());d=c.json.loads((c.ROOT/'candidate.json').read_text())
old=c.json.loads((c.CONTROL/'candidate.json').read_text());out=r['attempts'][-1]['certificate']
check=c.json.loads((c.ROOT/'checks.json').read_text());audit=c.json.loads((c.ROOT/'final_audit.json').read_text())
s=c.json.loads((c.ROOT/'search_summary.json').read_text());faces=[]
for i in range(7):
    beta=Q(out['beta3'][i]);mu=Q(out['mu_tilde'][i]);er=Q(out['center_rows_upper'][i]);M3=Q(out['M3_upper'][i])
    faces.append({'face':i+1,'a':float(Q(d['a'][i])),'a_historical':float(Q(old['a'][i])),
        'amplitude_factor':float(Q(d['a'][i])/Q(old['a'][i])),
        'beta':float(beta),'antipodal_separation_lower':float(2*beta),'epsilon_slack':float(beta-Q(1,1000)),
        'linear_query_margin':float(mu*(1-er)),'mu':float(mu),'center_row':float(er),
        'M3':float(M3),'M3_over_6':float(M3/6),'third_order_penalty':float(mu*M3/6)})
lim=(1-Q(out['eta_hidden']))*Q(d['ah']);maxforcing=max(map(Q,out['hidden_forcing_upper']))
constraints={'hidden_self_mapping':float(maxforcing/lim),'hidden_eta_over_cap':out['eta_hidden']/.75,
    'raw_history_domain':float(Q(out['radius'])),'epsilon_over_weakest_beta':float(Q(1,1000)/min(map(Q,out['beta3'])))}
peak=max([r['peak_working_set_bytes'],s['parent_peak_working_set_bytes'],check['peak_working_set_bytes'],audit['peak_working_set_bytes']]+[v['peak_working_set_bytes'] for v in s['results']])
peak_sum=s['parent_peak_working_set_bytes']+sum(sorted((v['peak_working_set_bytes'] for v in s['results']),reverse=True)[:2])
dec=c.json.loads((c.ROOT/'remainder_decomposition_256.json').read_text())
for i,face in enumerate(faces):face['M3_component_majorants']={name:values[i] for name,values in dec['M3_components'].items()}
resources={'cpu_seconds_before_summary':r['total_cpu_seconds']+check['cpu_seconds']+audit['cpu_seconds'],
    'largest_process_peak_bytes':peak,'conservative_concurrent_peak_sum_bytes':peak_sum,'gpu_seconds':0,'gpu_used':False}
resources['summary_cpu_seconds']=time.process_time()-CPU
resources['measured_cpu_seconds']=resources['cpu_seconds_before_summary']+resources['summary_cpu_seconds']
resources['separate_administrative_allowance_seconds']=5
resources['summed_phase_wall_seconds_excluding_summary']=r['wall_seconds']+s['wall_seconds']+check['wall_seconds']+audit['wall_seconds']+sum(c.json.loads((c.ROOT/p).read_text())['wall_seconds'] for p in ('tests.json','bootstrap_resources.json','selection_resources.json'))
report={'status':r['status'],'certified_dimension':out.get('certified_dimension'),
    'candidate_sha256':c.sha(c.ROOT/'candidate.json'),'kernel_sha256':c.sha(c.ROOT/'kernel.py'),
    'historical_control_sha256':c.sha(c.CONTROL/'candidate.json'),'faces':faces,
    'eta_hidden':out['eta_hidden'],'ah':float(Q(d['ah'])),'hidden_limit':float(lim),
    'hidden_forcing_upper':out['hidden_forcing_upper'],'constraint_ratios':constraints,
    'closest_to_active_constraint':max(constraints,key=constraints.get),
    'search_evaluations':sum(v['evals'] for v in s['results']),'invalid_numerical_proposals':sum(v['invalid'] for v in s['results']),
    'weakest_face':min(faces,key=lambda f:f['beta'])['face'],
    'max_192_256_beta_difference':max(check['beta_precision_differences']),
    'resources':resources,'numerical_faces':c.json.loads((c.ROOT/'numerical_faces.json').read_text())}
c.write('summary.json',report);print(c.json.dumps(report,indent=2))
