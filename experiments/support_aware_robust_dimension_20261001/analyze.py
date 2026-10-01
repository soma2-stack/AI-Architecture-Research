from resources import ROOT,CFG
import core as k
import json,math,hashlib
from fractions import Fraction as Q
from collections import Counter

def main():
 rows=json.loads((ROOT/'results.json').read_text());scale=json.loads((ROOT/'scale_diagnostics.json').read_text());records=[]
 for row in rows:
  name=row['case'];d=row['dimension'];old=row['accepted_dimension'];good=d['retained_indices'];b=list(map(Q,d['b_i']))
  extra=math.prod(math.ceil(b[i]/k.EPS) for i in good)
  historical=next(c['certificate'] for c in k.INPUT['cases'] if c['name']==name)
  trials=json.loads((ROOT/f'trials_{name}.json').read_text())
  byprefix={str(r):max((v['dimension']['epsilon_essential_dimension'] for v in trials if v['r']==r and v['valid']),default=0) for r in CFG['prefixes']}
  newstates=max(int(d['states']),extra)
  beststates=max(int(old['states']),newstates)
  sectioncover=math.ceil(2*Q(d['M_Euclidean_upper'])*Q(k.e.I(len(good)).sqrt().hi,k.e.I.scale)/(2*k.EPS))**len(good)
  records.append({'case':name,'n':historical['n'],'T':len(next(c['X'] for c in k.INPUT['cases'] if c['name']==name)),
   'historical_states':int(historical['states']),'accepted_support_aware_states':int(old['states']),
   'accepted_continuous_lower':old['epsilon_essential_dimension'],'continuous_lower':d['epsilon_essential_dimension'],
   'selected_section_states_17over8':int(d['states']),'selected_section_states_strict_entropy':extra,'selected_section_states_lower':newstates,
   'best_known_states_lower':beststates,'best_known_bits_lower':math.log2(beststates),
   'm':float(Q(d['m_Euclidean_lower'])),'M':float(Q(d['M_Euclidean_upper'])),
   'antipodal_half_margin':float(Q(d['antipodal_half_margin_lower'])),'r_chart':row['certificate']['r'],
   'amplitude':row['certificate']['a0'],'profile':row['certificate']['profile'],'source':row['source'],
   'prefix_best_continuous_lower':byprefix,'failure_counts':dict(Counter('valid' if v['valid'] else v['reason'] for v in trials)),
   'section_only_states_upper':str(sectioncover),'section_only_upper_bits':math.log2(sectioncover),
   'ambient_structural_upper':63 if name.startswith('dense_n3') else 144 if name.startswith('dense_n4') else 15 if name.startswith('independent_n3') else 24,
   'scale_diagnostic':next(v for v in scale if v['case']==name)})
 q=max(v['continuous_lower'] for v in records)
 classification='ROBUST CONTINUOUS DIMENSION REMAINS VERY SMALL' if q<=3 else 'MODERATE ROBUST CONTINUOUS DIMENSION CERTIFIED' if q<=8 else 'LARGE ROBUST CONTINUOUS DIMENSION CERTIFIED'
 obj={'classification':classification,'architecture_gate':'MORE ROBUST-DIMENSION WORK NEEDED','epsilon':'1/1000','records':records,
  'upper_bound_status':'NO USEFUL ROBUST-DIMENSION UPPER BOUND FOUND','rigorous':'whole-section residual-safe Lipschitz bounds, epsilon-essential coordinate lower bounds and integer product packing; section-specific entropy upper/lower only',
  'numerical':'sampled packing slopes/greedy counts and actual pair ratios','limitation':'maximum true dimension unresolved; failed prefixes cannot prove a ceiling; no architecture comparison'}
 (ROOT/'summary.json').write_text(json.dumps(obj,indent=2)+'\n')
 resources=[json.loads(x) for x in (ROOT/'resources.jsonl').read_text().splitlines()]
 (ROOT/'resource_summary.json').write_text(json.dumps({'measured_cpu_seconds':sum(v['cpu_seconds'] for v in resources),'measured_wall_sum_seconds':sum(v['wall_seconds'] for v in resources),'peak_RAM_bytes':max(v['peak_ram_bytes'] for v in resources),'GPU_seconds':0,'own_VRAM_bytes':0,'GPU_temperature_c':None,'GPU_CUDA_unused':True,'administrative_cpu_estimate_seconds':30,'workers':1},indent=2)+'\n')
 print(classification)
if __name__=='__main__':main()
