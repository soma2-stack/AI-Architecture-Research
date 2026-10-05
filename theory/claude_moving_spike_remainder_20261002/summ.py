import json,sys
for f in sys.argv[1:]:
    print('==',f)
    for l in open(f):
        try: r=json.loads(l)
        except: continue
        print(r['start'][:24].ljust(24), 'UB/2e %.3f'%r['UB_2eps'], 'LB/2e %.3f'%r['LB_2eps'], 'spikeLB %.5f L%d'%(r['LB_spike'],r['LB_spike_L']), '1step %.5f'%r['LB_one_step'], 'rms1 %.5f'%r.get('LB_rms1',0), r['verdict'], 'L*',r['L_star'], '%.0fs'%r['sec'])
