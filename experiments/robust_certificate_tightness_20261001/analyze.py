from pathlib import Path
import json,math,hashlib,statistics
from fractions import Fraction as Q
import numpy as np
ROOT=Path(__file__).parent;REPO=ROOT.parents[1]
def read(f):return json.loads((ROOT/f).read_text())
def save(f,obj):(ROOT/f).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
def main():
  rows=read('results.json');same={v['name']:v for v in read('same_product_results.json')}
  hp={v['name']:v for v in read('high_precision_checks.json')}
  assert len(rows)==len(same)==len(hp)==8
  for row in rows:
    for check in hp[row['name']]['checks']:
      assert check['passes_2epsilon'],check
      if 'fixed_h_gap' in check:assert float(check['fixed_h_gap'])<1e-50
      if 'absolute_difference' in check:assert check['absolute_difference']<1e-10
  freeze=read('FROZEN_SETUP.json')
  assert all(hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==v for f,v in freeze['sha256'].items())
  preserve=read('preservation_manifest.json')
  assert all(hashlib.sha256((REPO/f).read_bytes()).hexdigest()==v for f,v in preserve.items())
  gains={g:statistics.median(row['products']['best']['r']-row['certified_bits'] for row in rows if row['case']==g) for g in ['dense','independent']}
  query={g:statistics.median(row['accepted_grid']['query_slack_ratio'] for row in rows if row['case']==g) for g in ['dense','independent']}
  large=sum(row['products']['best']['r']>=6 and row['products']['best']['r']>=row['certified_dimension']+3 for row in rows)
  if gains['independent']-gains['dense']>=2 and query['independent']>=2*query['dense']:
    classification='MODEL-DEPENDENT CERTIFICATE BIAS FOUND'
  elif large>=2:
    classification='CERTIFICATES ARE HIGHLY CONSERVATIVE — MANY MORE ROBUST DIRECTIONS APPEAR NUMERICALLY'
  elif any(row['products']['best']['r']>row['certified_dimension'] for row in rows):
    classification='CERTIFICATES ARE MODERATELY CONSERVATIVE'
  else:classification='NO USEFUL CONCLUSION — UPPER/LOWER GAP REMAINS TOO LARGE'
  table=[]
  for row in rows:
    name=row['name'];old_states=2**row['certified_bits'];same_row=same[name]
    table.append({'name':name,'old_certified_dimension':row['certified_dimension'],'old_certified_bits':row['certified_bits'],
      'numerical_binary_grid_dimension':row['products']['best']['r'],
      'numerical_binary_grid_states':row['products']['best']['points'],
      'numerical_binary_grid_bits':float(row['products']['best']['r']),
      'same_product_numerical_states':same_row['states'],'same_product_numerical_bits':same_row['bits'],
      'raw_curvature_actual_over_majorant':row['curvature']['raw_ratio_max'],
      'projected_curvature_actual_over_majorant':row['curvature']['projected_curvature_ratio_max'],
      'old_query_dual_over_actual_closest_distance':1/row['accepted_grid']['query_slack_ratio'],
      'same_product_old_count_over_numerical_count':old_states/same_row['states'],
      'old_bits_over_same_product_numerical_bits':row['certified_bits']/same_row['bits'],
      'numeric_upper_evidence':'failed finite grids only; no global impossibility conclusion',
      'rigorous_cover_bits_upper':read(f'upper_{name}.json')['bits_upper']})
  summary={'classification':classification,'architecture_gate':'MORE ROBUST-DIMENSION WORK NEEDED',
    'epsilon':'1/1000','comparison':table,'median_grid_bit_gains':gains,'median_query_slack':query,
    'intrinsic_robust_dimension':'NOT DETERMINED; binary-grid coding dimension is not a certified continuous dimension',
    'upper_bound_conclusion':'NO USEFUL UPPER BOUND FOUND','preserved_prior_files':len(preserve),
    'closest_pair_high_precision_checks':sum(len(v['checks']) for v in hp.values()),'primary_code_hashes_verified':True}
  save('summary.json',summary)
  save('PRIMARY_FROZEN.json',{'epsilon':'1/1000','summary_sha256':hashlib.sha256((ROOT/'summary.json').read_bytes()).hexdigest(),'classification':classification,'no_secondary_epsilon_used':True})
  # Coupled slack factors are diagnostics, never factorial causal estimates.
  slack=[]
  inputs={v['name']:v for v in read('inputs.json')['cases']}
  for row in rows:
    case=inputs[row['name']];cert=case['certificate'];curv=row['curvature'];amp=row['products']['best']['amplitude']
    eta=cert['eta_sensitivity'];actual=curv['actual_preconditioned_jacobian_variation']
    entry={'name':row['name'],
      'A_tangent_spectrum':'full archived or frozen winner spectrum; center values in axis_slack.json',
      'B_hidden_compensation_actual_normal_halfwidth_use':curv['actual_normal_halfwidth_use_fraction'],
      'C_D_raw_majorant_over_sampled_max':1/curv['raw_ratio_max'],
      'D_projected_majorant_over_sampled_max':1/curv['projected_curvature_ratio_max'],
      'E_certified_eta':eta,'E_observed_actual_jacobian_eta':actual,
      'E_slack_1_minus_eta_ratio':(1-actual)/(1-eta),
      'E_contraction_cap':.75,'E_box_target_fraction':.9,'E_target_fraction_loss':1/.9,
      'F_larger_domain_amplitude_over_old':amp/float(Q(cert['a0'])),
      'F_warning':'domain enlargement is not solely certificate conservatism',
      'G_actual_query_over_old_dual':row['accepted_grid']['query_slack_ratio'],
      'H_17_over8_versus_collision_2_factor':17/16,
      'I_old_selected_r':cert['r'],'I_numeric_sampled_prefix':16,
      'I_uncertified_unsampled_directions':max(0,(case['n']*(2*case['n']**2+case['n']) if case['case']=='dense' else case['n']**2+2*case['n'])-16),
      'J_interval_precision':next(v for v in read('interval_inflation.json') if v['name']==row['name']),
      'K_basis_and_greedy_limits':'rotated grids can encode many binary choices through fewer strong dimensions; cap512, no upper',
      'scope':'observed ratios; sampled maxima are lower estimates of true suprema; components are coupled'}
    slack.append(entry)
  save('slack_decomposition.json',slack)
  resources=[json.loads(v) for v in (ROOT/'resources.jsonl').read_text().splitlines()]
  resource={'cpu_seconds':sum(v['cpu_seconds'] for v in resources),'cpu_minutes':sum(v['cpu_seconds'] for v in resources)/60,
    'gpu_active_wall_upper_seconds':sum(v['gpu_wall_upper_seconds'] for v in resources),
    'summed_post_import_job_wall_seconds':sum(v['wall_seconds'] for v in resources),
    'peak_RAM_bytes':max(v['peak_ram_bytes'] for v in resources),
    'peak_global_VRAM_bytes':max(v['peak_global_vram_bytes'] for v in resources),
    'peak_own_GPU_pool_bytes':max(v['peak_our_gpu_pool_bytes'] for v in resources),
    'peak_GPU_temperature_c':max(v['peak_temperature_c'] for v in resources),
    'includes_failed_attempts':True,'administrative_CPU_estimate_seconds':60,
    'notes':'GPU-active wall upper bound, not kernel-only time; global VRAM includes existing contexts; own pool excludes driver/library overhead'}
  save('resource_summary.json',resource)
  checks={'passed':True,'old_files_unchanged':len(preserve),'frozen_primary_unchanged':True,
    'eight_primary_endpoints':True,'high_precision_pairs_passed':True,'raw_history_search_only':True,
    'axis_diagonal_test_passed':read('axis_test.json')['passed'],'development_tests':read('tests.json')['tests']}
  save('final_checks.json',checks)
  print(classification);print(resource)
if __name__=='__main__':main()
