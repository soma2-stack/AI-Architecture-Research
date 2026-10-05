import json, reduced
res = []
for n in range(2000, 4001):
    r = reduced.solve(n)
    res.append((n, r['min'], r['argmin']))
json.dump(res, open('scan_2000_4000.json', 'w'))
mins = [m for _, m, _ in res]
# crossings
def first_persistent(th):
    for i in range(len(res)):
        if all(m > th for m in mins[i:]):
            return res[i][0]
def last_below(th):
    idx = [res[i][0] for i in range(len(res)) if mins[i] <= th]
    return max(idx) if idx else None
for th in (0.0, 0.02):
    print('threshold', th, 'last n with min<=th:', last_below(th), 'first n from which min>th persistently:', first_persistent(th))
nonmono = sum(1 for i in range(1, len(mins)) if mins[i] < mins[i-1])
print('non-monotone steps:', nonmono, 'argmins:', set(a for _,_,a in res))
for n, m, a in res:
    if n in (2000, 2100, 2200, 2300, 2400, 2500, 3000, 3500, 4000):
        print(n, m, a)
