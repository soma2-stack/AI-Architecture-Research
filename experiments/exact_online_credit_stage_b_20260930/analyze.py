"""Post-run frozen-criterion analysis only; no forward/gradient experiments."""
import csv
import json
import statistics as st
import core as c

def median(values):return float(st.median(values))
def mean(values):return float(st.mean(values))
def method(row,name):return next(m for m in row['methods'] if m['method']==name)
def final(row):return row['checkpoints'][str(row['T'])]
def support_per_p(row,threshold):return final(row)['thresholds'][str(threshold)]['count']/row['P']
def write_csv(name,rows):
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with (c.ROOT/name).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)

def main():
    meter=c.Meter('Stage-B analysis')
    try:
        for phase in ('width8','width16','family'):assert json.loads((c.ROOT/f'status_{phase}.json').read_text())['valid']
        rows=[json.loads(l) for width in (8,16) for l in (c.ROOT/f'raw_width{width}.jsonl').read_text().splitlines()]
        families=[json.loads(l) for l in (c.ROOT/'family.jsonl').read_text().splitlines()]
        assert len(rows)==460 and len(families)==54
        exact_groups=[g for r in rows for m in r['methods'] if m['intended_exact'] for g in m['groups']]
        assert all(c.passes(g) for g in exact_groups)
        keys=['id','n','axis','family','interaction','depth','mode','T','seed','P','N','full_capacity']
        support_csv=[];runtime_csv=[];cross_csv=[];fill_csv=[];errors_csv=[];compression_csv=[]
        for r in rows:
            base={k:r[k] for k in keys}
            support_csv.append({**base,'significant':final(r)['thresholds']['1e-12']['count'],
                                'fraction':final(r)['thresholds']['1e-12']['fraction'],
                                'graph_closure_values':r['graph_closure_values'],
                                'exact_packed_values':method(r,'packed_exact')['stored_derivative_scalars'],
                                'exact_packed_all_numbers':method(r,'packed_exact')['all_stored_numbers'],
                                'exact_packed_index_bytes':method(r,'packed_exact')['index_bytes'],
                                'snapshot_matrix_factor_values':next(p['stored_values'] for p in r['compression'] if p['name']=='matrix_minimum_rank'),
                                'snapshot_kronecker_values':next(p['stored_values'] for p in r['compression'] if p['name']=='kronecker_minimum_sum')})
            for m in r['methods']:
                runtime_csv.append({**base,'method':m['method'],'exact_gate_passed':m['exact_gate_passed'],
                                    **{k:m.get(k) for k in ('stored_derivative_scalars','all_stored_numbers','derivative_bytes','index_bytes','seconds','cpu_seconds','derivative_seconds_per_step','derivative_to_inference_ratio','total_to_inference_ratio','estimated_contraction_operations_per_step')},
                                    'inference_seconds_per_step':r['inference_seconds_per_step'],'peak_process_rss':r['process_peak_rss_bytes']})
                for g in m['groups']:
                    if g['group']=='ALL':errors_csv.append({**base,'method':m['method'],**g})
            for step,check in r['checkpoints'].items():
                fill_csv.append({**base,'step':int(step),'exact_nonzero':check['exact_nonzero'],
                                 **{f'count_{t}':v['count'] for t,v in check['thresholds'].items()},
                                 **{f'rank_{t}':v for t,v in check['ranks'].items()}})
            for b in final(r)['blocks']:
                cross_csv.append({**base,'state_layer':b['state_layer'],'parameter_layer':b['parameter_layer'],'size':b['size'],
                                  **{f'count_{t}':v for t,v in b['threshold_counts'].items()},**{f'rank_{t}':v for t,v in b['ranks'].items()},
                                  'singular_values':json.dumps(b['singular_values'])})
            for p in r['compression']:
                compression_csv.append({**base,'representation':p['name'],'stored_values':p['stored_values'],'matrix_relative_error':p['reconstruction']['relative_error'],
                                        'maximum_group_relative_error':max(g['relative_error'] for g in p['groups']),'passes':p['passes'],'offline_only':True})
        for name,data in [('support_scaling.csv',support_csv),('runtime_scaling.csv',runtime_csv),('cross_layer.csv',cross_csv),('fill_in.csv',fill_csv),('compact_errors.csv',errors_csv),('compression.csv',compression_csv)]:write_csv(name,data)
        write_csv('family_dimension.csv',[{k:v for k,v in r.items() if k not in ('input_hashes','singular_values','ranks')}|{f'rank_{t}':v for t,v in r['ranks'].items()} for r in families])
        axis_tables={}
        for axis in ('block','lowrank'):
            table=[]
            for width in (8,16):
                interactions=sorted({r['interaction'] for r in rows if r['n']==width and r['axis']==axis})
                for interaction in interactions:
                    rr=[r for r in rows if r['n']==width and r['axis']==axis and r['interaction']==interaction and r['depth']==1]
                    table.append({'n':width,'interaction':interaction,'P':rr[0]['P'],'full_capacity':rr[0]['full_capacity'],
                                  'support_count_min':min(final(r)['thresholds']['1e-12']['count'] for r in rr),
                                  'support_count_max':max(final(r)['thresholds']['1e-12']['count'] for r in rr),
                                  'support_fraction_mean':mean(final(r)['thresholds']['1e-12']['fraction'] for r in rr),
                                  'packed_values':method(rr[0],'packed_exact')['stored_derivative_scalars'],
                                  'packed_all_numbers':method(rr[0],'packed_exact')['all_stored_numbers'],
                                  'matrix_rank':sorted({final(r)['ranks']['1e-10'] for r in rr}),
                                  'median_RTRL_total_to_inference':median(method(r,'RTRL')['total_to_inference_ratio'] for r in rr),
                                  'median_RTRL_derivative_to_inference':median(method(r,'RTRL')['derivative_to_inference_ratio'] for r in rr),
                                  'median_packed_total_to_inference':median(method(r,'packed_exact')['total_to_inference_ratio'] for r in rr)})
            axis_tables[axis]=table
        depth_table=[]
        for width in (8,16):
            for family,interaction in [('block',1),('block',width),('lowrank',1),('lowrank',8)]:
                depths=sorted({r['depth'] for r in rows if r['n']==width and r['axis']==family and r['interaction']==interaction})
                for depth in depths:
                    rr=[r for r in rows if r['n']==width and r['axis']==family and r['interaction']==interaction and r['depth']==depth]
                    earliest=[g['relative_error'] for r in rr for g in method(r,'local_block')['groups'] if g['group']=='ALL' and g['layer']==1]
                    depth_table.append({'n':width,'family':family,'interaction':interaction,'depth':depth,'P':rr[0]['P'],'N':rr[0]['N'],
                                        'full_capacity':rr[0]['full_capacity'],'packed_values':method(rr[0],'packed_exact')['stored_derivative_scalars'],
                                        'packed_all_numbers':method(rr[0],'packed_exact')['all_stored_numbers'],
                                        'earliest_local_error_min':min(earliest),'earliest_local_error_max':max(earliest)})
        mixing=[]
        for mode in c.CFG['mix_modes']:
            rr=[r for r in rows if r['axis']=='mix' and r['mode']==mode]
            mixing.append({'mode':mode,'P':rr[0]['P'],'full_capacity':rr[0]['full_capacity'],
                           'significant_count_min':min(final(r)['thresholds']['1e-12']['count'] for r in rr),
                           'significant_count_max':max(final(r)['thresholds']['1e-12']['count'] for r in rr),
                           'packed_values':method(rr[0],'packed_exact')['stored_derivative_scalars']})
        # Frozen evidence checks use paired seeds/T, not favorable aggregate selection.
        block_checks=[];rank_checks=[];depth_checks=[]
        for width in (8,16):
            kk=sorted({r['interaction'] for r in rows if r['n']==width and r['axis']=='block'})
            for threshold in c.CFG['support_thresholds']:
                for T in c.CFG['horizons']:
                    block_good=rank_good=0
                    for seed in c.CFG['seeds']:
                        series=[support_per_p(next(r for r in rows if r['n']==width and r['axis']=='block' and r['interaction']==k and r['depth']==1 and r['T']==T and r['seed']==seed),threshold) for k in kk]
                        block_good+=all(a<b for a,b in zip(series,series[1:]))
                        r0=next(r for r in rows if r['n']==width and r['axis']=='lowrank' and r['interaction']==0 and r['depth']==1 and r['T']==T and r['seed']==seed)
                        r1=next(r for r in rows if r['n']==width and r['axis']=='lowrank' and r['interaction']==1 and r['depth']==1 and r['T']==T and r['seed']==seed)
                        rank_good+=support_per_p(r1,threshold)>support_per_p(r0,threshold)
                    block_checks.append({'n':width,'T':T,'threshold':threshold,'seeds_with_strict_block_growth':block_good})
                    rank_checks.append({'n':width,'T':T,'threshold':threshold,'seeds_with_rank0_to1_growth':rank_good})
        cross_present=all(b['threshold_counts']['1e-12']>0 for r in rows if r['axis'] in ('block','lowrank') and r['depth']>1 for b in final(r)['blocks'] if b['parameter_layer']<b['state_layer'])
        rich=[r for r in rows if r['depth']==3 and ((r['axis']=='block' and r['interaction']==r['n']) or (r['axis']=='lowrank' and r['interaction'] in (1,8)))]
        widths=[]
        for family,interaction in [('block','full'),('lowrank',1),('lowrank',8)]:
            a=next(r for r in rich if r['n']==8 and r['axis']==family and r['interaction']==(8 if interaction=='full' else interaction))
            b=next(r for r in rich if r['n']==16 and r['axis']==family and r['interaction']==(16 if interaction=='full' else interaction))
            aa=method(a,'packed_exact')['all_stored_numbers']/a['P'];bb=method(b,'packed_exact')['all_stored_numbers']/b['P']
            widths.append({'family':family,'interaction':interaction,'width8_storage_per_P':aa,'width16_storage_per_P':bb,'growth_ratio':bb/aa})
        rich_exact_costs=[m['all_stored_numbers']/r['P'] for r in rich for m in r['methods'] if m['method'] not in ('BPTT','local_block','online_kronecker_sum') and m['exact_gate_passed']]
        local_failure=all(g['relative_error']>c.CFG['survival_early_local_error'] for r in rich for g in method(r,'local_block')['groups'] if g['layer']==1 and g['group']=='ALL')
        full_rank_unstable=sum(len(set(final(r)['ranks'].values()))>1 for r in rows)
        checkpoint_rank_unstable=sum(len(set(check['ranks'].values()))>1 for r in rows for check in r['checkpoints'].values())
        cross_rank_unstable=sum(len(set(b['ranks'].values()))>1 for r in rows for check in r['checkpoints'].values() for b in check['blocks'])
        owner_rank_unstable=sum(len(set(rank.values()))>1 for r in rows for probe in r['compression'] if probe['name']=='kronecker_minimum_sum' for layer in probe['owner_slices'] for rank in layer['ranks'])
        family_rank_unstable=sum(len(set(r['ranks'].values()))>1 for r in families)
        cheap_closer=None
        for name in ('packed_exact','SnAp1','SnAp2','online_svd_factor'):
            if all(any(m['method']==name and m['exact_gate_passed'] and m['all_stored_numbers']/r['P']<=c.CFG['kill_max_compact_storage_over_P'] and m['derivative_to_inference_ratio']<=c.CFG['kill_max_compact_derivative_to_inference_ratio'] for m in r['methods']) for r in rich):cheap_closer=name
        survived=(all(x['seeds_with_strict_block_growth']>=4 for x in block_checks) and all(x['seeds_with_rank0_to1_growth']>=4 for x in rank_checks)
                  and cross_present and local_failure and min(rich_exact_costs)>=c.CFG['survival_rich_min_storage_over_P']
                  and all(x['growth_ratio']>=c.CFG['survival_width16_sparse_growth_ratio'] for x in widths)
                  and full_rank_unstable+checkpoint_rank_unstable+cross_rank_unstable+owner_rank_unstable+family_rank_unstable==0)
        classification='STAGE B — KNOWN EXACT STRUCTURE CLOSES THE GAP' if cheap_closer else 'STAGE B — STRUCTURAL PARETO GAP SURVIVES' if survived else 'STAGE B — INCONCLUSIVE'
        snap={name:{'cases':sum(any(m['method']==name for m in r['methods']) for r in rows),
                    'exact_passes':sum(method(r,name)['exact_gate_passed'] for r in rows),
                    'maximum_group_relative_error':max(g['relative_error'] for r in rows for g in method(r,name)['groups'])} for name in ('SnAp1','SnAp2')}
        family_summary={'fixed_parameter_ranks':sorted({r['ranks']['1e-10'] for r in families if isinstance(r['seed'],int)}),
                        'pooled_ranks':sorted({r['ranks']['1e-10'] for r in families if not isinstance(r['seed'],int)}),
                        'fixed_parameter_cap':7,'pooled_cap':39,'cutoff_unstable_rows':sum(len(set(r['ranks'].values()))>1 for r in families)}
        fill_summary=[]
        for family,interaction in [('block',1),('block',8),('lowrank',0),('lowrank',1),('lowrank',8)]:
            rr=[r for r in rows if r['n']==8 and r['axis']==family and r['interaction']==interaction and r['depth']==1 and r['T']==128]
            fill_summary.append({'family':family,'interaction':interaction,'mean_significant_by_step':{step:mean(r['checkpoints'][step]['thresholds']['1e-12']['count'] for r in rr) for step in rr[0]['checkpoints']}})
        summary={'classification':classification,'cases':len(rows),'family_derivative_cases':360,'method_records':sum(len(r['methods']) for r in rows),
                 'maximum_exact_group_relative_error':max(g['relative_error'] for g in exact_groups),
                 'maximum_exact_group_absolute_error':max(g['maximum_absolute_error'] for g in exact_groups),
                 'maximum_exact_reconstruction_relative_error':max(m['reconstruction']['relative_error'] for r in rows for m in r['methods'] if m['intended_exact'] and m['reconstruction']),
                 'axes':axis_tables,'depth':depth_table,'mixing':mixing,'block_checks':block_checks,'rank_checks':rank_checks,'width_confirmation':widths,
                 'all_cross_layer_blocks_present':cross_present,'rich_minimum_online_exact_stored_numbers_over_P':min(rich_exact_costs),
                 'same_layer_only_local_failure':local_failure,'full_sensitivity_rank_cutoff_unstable_cases':full_rank_unstable,
                 'rank_cutoff_sensitivity':{'checkpoint_matrices':checkpoint_rank_unstable,'cross_layer_blocks':cross_rank_unstable,'W_owner_slices':owner_rank_unstable,'family_spans':family_rank_unstable},
                 'cheap_closer':cheap_closer,'snap':snap,'family_dimension':family_summary,'fill_in':fill_summary,
                 'snapshot_compression_passes':{name:sum(p['passes'] for r in rows for p in r['compression'] if p['name']==name) for name in {p['name'] for r in rows for p in r['compression']}},
                 'gpu_used':False,'parameter_updates':0,'uoro':'deferred, not implemented',
                 'recommendation':'owner review for Stage C' if survived and not cheap_closer else 'stop target' if cheap_closer else 'Stage B inconclusive'}
        meter.finish();ledger=[json.loads(l) for l in (c.ROOT/'cpu_ledger.jsonl').read_text().splitlines()]
        summary['resources']={'cpu_seconds':sum(r['cpu_seconds'] for r in ledger),'wall_seconds':sum(r['wall_seconds'] for r in ledger),
                              'peak_rss_bytes':max(r['peak_rss_bytes'] for r in ledger),'ledger':ledger}
        (c.ROOT/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
    finally:meter.finish()

if __name__=='__main__':main()
