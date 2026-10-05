import json, sys
for f in sys.argv[1:]:
    print('==', f)
    for line in open(f):
        line = line.strip()
        if not line: continue
        r = json.loads(line); m = r['meta']
        print(m.get('kind', 'c1'), m.get('n'), 'T', m['T'], 'maxin %.3f' % m['max_abs_input'], 'hT %.1e' % m['endpoint_max_abs_h'],
              'vbox', ['%.3f' % v for v in m.get('future_input_range_for_box', [])], 'sec %.0f' % m['seconds'])
        for e in r['encoders']:
            print('   m=%2d %s %-6s uni=%.2e worst=%.2e ledger=%.2e nu_med=%.2e z/target=%.1e count=%d' % (
                e['m'], 'H' if e['hybrid'] else 'P', e['policy'], e['uniform_query_error'], e['worst_box_query_error'] or -1,
                e['ledger_bound'] or -1, e['nu_median'] or -1, e['z_T'] / e['ledger_target_z'], e['count']))
