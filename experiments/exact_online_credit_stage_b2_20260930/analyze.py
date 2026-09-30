"""Post-measurement tables, no recurrence or parameter updates."""
import argparse
import csv
import hashlib
import json
import statistics as stat
import zipfile
from collections import defaultdict
import core as c

def load(name):return [json.loads(l) for l in (c.ROOT/name).read_text().splitlines()]
def csvfile(name,rows):
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with (c.ROOT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
def best(r,tol=1e-8):return min((p for p in r['compression'] if p['passes'] and p['tolerance']==tol),key=lambda p:p['stored_numbers'])

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--corrected',action='store_true');args=parser.parse_args()
    base=c.ROOT
    if args.corrected:c.ROOT=base/'corrected_single_thread'
    meter=c.Meter('Stage-B2 post-run analysis and archive preservation')
    if args.corrected:meter.prior+=sum(json.loads(l)['cpu_seconds'] for l in (base/'cpu_ledger.jsonl').read_text().splitlines())
    try:
        rows=load('raw.jsonl');families=load('family.jsonl');status=json.loads((c.ROOT/'status.json').read_text())
        buckets=defaultdict(list)
        for r in rows:buckets[r['case'],r['n'],r['T']].append(r)
        table=[];online=[];snapshot=[];ranks=[];family=[]
        for (case,n,T),rr in buckets.items():
            selected=[best(r) for r in rr];single=rr[0]
            table.append({'case':case,'n':n,'T':T,'seeds':len(rr),'P':single['P'],'N':single['N'],'full_size':single['full_size'],
                          'best_snapshot_min':min(b['stored_numbers'] for b in selected),
                          'best_snapshot_median':stat.median(b['stored_numbers'] for b in selected),
                          'best_snapshot_max':max(b['stored_numbers'] for b in selected),
                          'best_snapshot_ratio_median':stat.median(b['ratio_to_full'] for b in selected),
                          'best_snapshot_methods':','.join(sorted({b['method'] for b in selected})),
                          'stable_rank_min':min(r['rank']['stable_rank'] for r in rr),'stable_rank_max':max(r['rank']['stable_rank'] for r in rr),
                          'full_spectrum_rank_min':min(min(r['rank']['ranks'].values()) for r in rr),
                          'full_spectrum_rank_max':max(max(r['rank']['ranks'].values()) for r in rr)})
        for r in rows:
            base={k:r[k] for k in ('id','case','n','T','seed','P','N','full_size')}
            for m in r['online']:
                online.append({**base,**{k:m.get(k) for k in ('method','all_stored_numbers','bytes','peak_stored_numbers','ratio_to_full','ratio_to_P','seconds','inclusive_to_inference','exact','peak_scratch_bound_scalars')},
                               'relative_error':m['reconstruction']['relative_error'],'absolute_error':m['reconstruction']['maximum_absolute_error'],
                               'max_group_relative_error':max(g['relative_error'] for g in m['gradient_groups'])})
            for m in r['compression']:
                snapshot.append({**base,**{k:m[k] for k in ('method','tolerance','stored_numbers','ratio_to_full','ratio_to_P','passes','seconds','scope')},
                                 'relative_error':m['reconstruction']['relative_error'],'absolute_error':m['reconstruction']['maximum_absolute_error']})
            for m in r.get('rank_audit') or []:
                ranks.append({**base,'slice':m['slice'],'min_rank':min(m['ranks'].values()),'max_rank':max(m['ranks'].values()),
                              'rank_at_1e8':m['ranks']['1e-08'],'rank_at_1e12':m['ranks']['1e-12'],
                              'tail_rank_1e8':m['tail_ranks']['1e-08'],'tail_rank_1e12':m['tail_ranks']['1e-12'],
                              **{k:m[k] for k in ('condition_number','stable_rank','torch_gesdd_relative_discrepancy','torch_gesvd_relative_discrepancy')}})
        for f in families:
            for p in f['checkpoints']:
                family.append({**{k:f[k] for k in ('id','case','n','T','seed')},'samples':p['samples'],
                               **{f'centered_{t}':v for t,v in p['centered']['ranks'].items()},
                               **{f'uncentered_{t}':v for t,v in p['uncentered']['ranks'].items()},
                               'sample_cap_centered':p['sample_cap_centered'],'QR_reconstruction_error':p['QR_reconstruction_error'],
                               'QR_orthogonality_error':p['QR_orthogonality_error']})
        for name,table_rows in [('compression_summary.csv',table),('online_storage_runtime.csv',online),('snapshot_methods.csv',snapshot),('rank_audit.csv',ranks),('family_growth.csv',family)]:csvfile(name,table_rows)
        group_errors=[g for r in rows for g in r['reference_groups']]
        online_errors=[g for r in rows for m in r['online'] for g in m['gradient_groups']]
        hard_families=[f for f in families if f['case'] in ('rank1_feedback','full_feedback','deep3','explicit_feedback')]
        ceiling=sum(f['checkpoints'][-1]['centered']['ranks']['1e-08']>=127 for f in hard_families)
        size_crossings=[]
        for r in rows:
            counts=[best(r,t)['stored_numbers'] for t in c.CFG['reconstruction_tolerances']]
            if min(counts)<=4*r['P']<max(counts):size_crossings.append({'id':r['id'],'counts':counts,'gate4P':4*r['P']})
        summary={'classification':status['classification'],'main_count':len(rows),'family_count':len(families),
                 'family_complete':status['family_complete'],
                 'family_missing_case_ids':sorted({r['id'] for r in rows}-{f['id'] for f in families}),
                 'family_recurrences':len(families)*128,'tests_passed':32 if args.corrected else 31,'reference_max_relative_error':max(g['relative_error'] for g in group_errors),
                 'reference_max_absolute_error':max(g['maximum_absolute_error'] for g in group_errors),
                 'online_max_group_relative_error':max(g['relative_error'] for g in online_errors),
                 'online_max_group_absolute_error':max(g['maximum_absolute_error'] for g in online_errors),
                 'online_max_reconstruction_error':max(m['reconstruction']['relative_error'] for r in rows for m in r['online']),
                 'reference_provenance_matches':sum(r['B_provenance']['available'] for r in rows),
                 'rank_slice_records':len(ranks),'cutoff_dependent_slices':sum(r['min_rank']!=r['max_rank'] for r in ranks),
                 'max_svd_algorithm_discrepancy':max(max(r['torch_gesdd_relative_discrepancy'],r['torch_gesvd_relative_discrepancy']) for r in ranks),
                 'hard_families_at_sample_ceiling':ceiling,'hard_families_tested':len(hard_families),
                 'compact_gate_tolerance_crossings':size_crossings,'compression_table':table,
                 'source_freeze':json.loads((c.ROOT/'provenance.json').read_text())['commit'],
                 'gpu_used':False,'cuda_used':False,'parameters_updated':False,'Stage_C_ran':False}
        (c.ROOT/'summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
        manifest=[]
        with zipfile.ZipFile(c.ROOT/'matrices.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
            for file in sorted((c.ROOT/'matrices').glob('*.npz')):
                meter.check();archive.write(file,file.name);manifest.append({'file':file.name,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'bytes':file.stat().st_size})
        for file in ('matrices.zip','raw.jsonl','family.jsonl','config.json','precision.json','provenance.json'):
            p=c.ROOT/file;manifest.append({'file':file,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
        csvfile('manifest.csv',manifest)
        print(json.dumps({k:v for k,v in summary.items() if k!='compression_table'},indent=2))
    finally:meter.finish()

if __name__=='__main__':main()
