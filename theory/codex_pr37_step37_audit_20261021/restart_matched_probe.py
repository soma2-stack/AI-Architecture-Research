"""PR37 actual operator: preregistered schedule ablation, with feasibility checks.
This is NOT a matched forcing/budget comparison; differences are explicitly reported.
"""
import sys,json,pathlib
sys.path.insert(0,r'E:\AI-Architecture-Research-PR37-step37-audit\theory\codex_pr37_step37_audit_20261021')
from legal_class import simulate
out=[]
for K,rho,top in [(1,3,.2),(0,3,.2),(1,2,.2),(1,4,.2)]:
 try:
  r=simulate(n=8192,kind='stair',K=K,rho=rho,top=top,settle=.02,warm=30,level=1.)
  out.append({'config':{'K':K,'rho':rho,'top':top},'status':'PASS','T':r['T'],'mT':r['mT'],'peak_forcing':r['max_Delta_phi'],'population_gain':r['readout_over_max_phi'],'legal_query_gain':r['legal_retainer_readout_over_A_max_phi'],'legal_query_abs':r['legal_one_step_retainer_component_optimum'],'full_query_abs':abs(r['legal_same_query_full_selected_readout']),'forcing_error':r['forcing_match_max_error'],'max_input':r['max_input'],'endpoint_gap':r['endpoint_ret_pair_difference']})
 except Exception as e:out.append({'config':{'K':K,'rho':rho,'top':top},'status':'FAIL','error':str(e)})
p=pathlib.Path(__file__).with_name('probe_results.json');p.write_text(json.dumps(out,indent=2))
for x in out:print(x)
print('NOTE: schedule ablation, not matched control; compare T, mT and forcing explicitly.')
