import sys,json,pathlib,math
sys.path.insert(0,r'E:\AI-Architecture-Research-PR37-step37-audit\theory\codex_pr37_step37_audit_20261021')
from legal_class import simulate
rows=[]
for K in [0,1]:
 for rho in ([3] if K==0 else [2,3,4,5,6]):
  for top in [.08,.12,.16,.20,.24,.28,.32]:
   try:
    x=simulate(n=8192,kind='stair',K=K,rho=rho,top=top,settle=.02,warm=30,level=1.)
    rows.append(dict(K=K,rho=rho,top=top,T=x['T'],mT=x['mT'],m=max(x['m_plus_minus']),gain=x['readout_over_max_phi'],full=abs(x['legal_same_query_full_selected_readout']),ret=abs(x['legal_one_step_retainer_component_optimum']),forcing=x['max_Delta_phi'],error=x['forcing_match_max_error'],maxinput=x['max_input'],endpoint=x['endpoint_ret_pair_difference']))
   except Exception as e:rows.append(dict(K=K,rho=rho,top=top,error_message=str(e)))
pairs=[]
for a in rows:
 if a.get('K')!=0 or 'mT' not in a:continue
 for b in rows:
  if b.get('K')!=1 or 'mT' not in b:continue
  budget=abs(a['mT']-b['mT'])/max(a['mT'],b['mT'])
  horizon=abs(a['T']-b['T'])/max(a['T'],b['T'])
  pairs.append(dict(budget_diff=budget,horizon_diff=horizon,control=a,stair=b))
pairs.sort(key=lambda p:p['budget_diff']+p['horizon_diff'])
p=pathlib.Path(__file__).with_name('budget_sweep_results.json')
p.write_text(json.dumps(dict(rows=rows,closest_pairs=pairs[:12]),indent=2))
print('cases',len(rows),'legal',sum('mT' in r for r in rows))
for pair in pairs[:5]:
 a,b=pair['control'],pair['stair']
 print('budget_diff',round(pair['budget_diff'],4),'T_diff',round(pair['horizon_diff'],4),'one_stage',a['top'],a['T'],a['mT'],round(a['gain'],6),'stair',b['rho'],b['top'],b['T'],b['mT'],round(b['gain'],6))
print('No pair is called matched unless T and mT are identical.')
