"""Post-run aggregation only; never invokes a model or gradient method."""
import json
import statistics
import audit as a

def main():
    meter=a.Meter('post-run aggregation')
    try:
        rows=[json.loads(line) for line in (a.ROOT/'raw.jsonl').read_text().splitlines()]
        assert json.loads((a.ROOT/'status.json').read_text())['valid']
        assert len(rows)==150
        all_exact=[g for r in rows if r['method'] in ('G1','G2') for g in r['groups']]
        assert all(a.passes(g) for g in all_exact)
        layers=[]
        for depth in (2,3):
            for layer in range(1,depth+1):
                groups=[g for r in rows if r['method']=='G3' and r['depth']==depth
                        for g in r['groups'] if g['layer']==layer and g['parameter']=='ALL']
                layers.append({'depth':depth,'layer':layer,
                               'relative_error_min':min(g['relative_error'] for g in groups),
                               'relative_error_mean':statistics.mean(g['relative_error'] for g in groups),
                               'relative_error_max':max(g['relative_error'] for g in groups),
                               'maximum_absolute_error':max(g['maximum_absolute_error'] for g in groups),
                               'gradient_norm_min':min(g['gradient_norm'] for g in groups),
                               'gradient_norm_max':max(g['gradient_norm'] for g in groups),
                               'cosine_min':min(g['cosine_similarity'] for g in groups),
                               'cases_exceeding_1e_4':sum(g['relative_error']>1e-4 for g in groups)})
        tables=[]
        for kind in ('dense','independent'):
            for depth in (1,2,3):
                subset=[r for r in rows if r['kind']==kind and r['depth']==depth]
                for method in sorted({r['method'] for r in subset}):
                    rr=[r for r in subset if r['method']==method]
                    tables.append({'kind':kind,'depth':depth,'method':method,'P':rr[0]['P'],
                                   'state_width':rr[0]['recurrent_state_width'],
                                   'persistent_derivative_scalars_min':min(r['persistent_derivative_scalars'] for r in rr),
                                   'persistent_derivative_scalars_max':max(r['persistent_derivative_scalars'] for r in rr),
                                   'peak_explicit_derivative_scalars_max':max(r['peak_explicit_derivative_scalars'] for r in rr),
                                   'median_inference_microseconds_per_step':statistics.median(r['inference_seconds_per_step'] for r in rr)*1e6,
                                   'median_gradient_microseconds_per_step':statistics.median(r['gradient_seconds_per_step'] for r in rr)*1e6,
                                   'median_gradient_to_inference_ratio':statistics.median(r['gradient_to_inference_ratio'] for r in rr),
                                   'median_total_to_inference_ratio':statistics.median(r['total_to_inference_ratio'] for r in rr)})
        supports=[]
        for depth in (1,2,3):
            rr=[r for r in rows if r['method']=='G1' and r['kind']=='independent' and r['depth']==depth]
            supports.append({'depth':depth,'nonzero_counts':sorted({r['sensitivity_support']['nonzero_above_threshold'] for r in rr}),
                             'fraction_min':min(r['sensitivity_support']['fraction_above_threshold'] for r in rr),
                             'fraction_max':max(r['sensitivity_support']['fraction_above_threshold'] for r in rr),
                             'lower_to_upper_nonzero_every_case':all(b['nonzero_above_threshold']>0 for r in rr for b in r['sensitivity_support']['blocks'] if b['parameter_layer']<b['state_layer'])})
        result={'classification':'STAGE A VALID — STRUCTURAL DIFFERENCE OBSERVED',
                'cases':60,'method_records':150,'timing_repeats':3,
                'maximum_exact_relative_error':max(g['relative_error'] for g in all_exact),
                'maximum_exact_absolute_error':max(g['maximum_absolute_error'] for g in all_exact),
                'single_layer_local_max_relative_error':max(g['relative_error'] for r in rows if r['method']=='G2' for g in r['groups']),
                'single_layer_local_max_absolute_error':max(g['maximum_absolute_error'] for r in rows if r['method']=='G2' for g in r['groups']),
                'nondegenerate_groups':sum(not g['numerically_degenerate'] for r in rows for g in r['groups']),
                'degenerate_groups':sum(g['numerically_degenerate'] for r in rows for g in r['groups']),
                'maximum_trajectory_error':max(r['trajectory_max_error'] for r in rows),
                'maximum_absolute_state':max(r['maximum_absolute_state'] for r in rows),
                'local_layer_results':layers,'resource_table':tables,'support_table':supports,
                'optional_controls':'SnAp-1, SnAp-2, UORO deferred; not executed',
                'gpu_cuda_used':False,'parameter_updates':0,'recommendation':'Owner review for Stage B; do not execute without new authorization'}
        assert any(g['relative_error_max']>1e-4 for g in layers if g['layer']<g['depth'])
        meter.finish()
        ledger=[json.loads(l) for l in (a.ROOT/'cpu_ledger.jsonl').read_text().splitlines()]
        result['resources']={'cpu_seconds':sum(r['cpu_seconds'] for r in ledger),
                             'job_wall_seconds':sum(r['wall_seconds'] for r in ledger),
                             'peak_rss_bytes':max(r['peak_rss_bytes'] for r in ledger),'ledger':ledger}
        (a.ROOT/'summary.json').write_text(json.dumps(result,indent=2))
        print(json.dumps(result,indent=2))
    finally: meter.finish()

if __name__=='__main__':main()
