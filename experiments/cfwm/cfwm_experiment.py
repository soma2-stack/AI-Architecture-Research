"""
H.2 — Commutation-Factored World Model: learned move pruning.

World: k labelled tokens on a line of L cells. Actions: move token i by -1/+1; blocked
(no-op) if out of bounds or target cell occupied. Two moves commute at s unless the
tokens interact (blocking), so independence is STATE-DEPENDENT.

Planner: iterative-deepening DFS (no closed list — the memory-limited setting where
move pruning matters). Pruning rule for consecutive actions (a, b) taken from state s:
    prune if b < a (canonical order) and I(a, b | s) says "a,b commute at s".
With the true relation this is safe: the lexicographically smallest optimal plan is
never pruned (swapping a commuting, out-of-order pair would give a smaller plan).

Question: can I(a,b|s) be LEARNED from raw interaction (execute both orders from the
same state, compare outcomes — no domain description), how many samples are needed,
and what do learned-predicate errors cost (lost / longer plans) vs. the search savings?
"""
import numpy as np, itertools, json, sys, time, torch
torch.set_num_threads(4)


class LineWorld:
    def __init__(self, L, k):
        self.L, self.k = L, k
        self.actions = [(i, d) for i in range(k) for d in (-1, 1)]
        self.A = len(self.actions)

    def step(self, s, a):
        i, d = self.actions[a]
        p = s[i] + d
        if p < 0 or p >= self.L or p in s:
            return s
        s2 = list(s); s2[i] = p
        return tuple(s2)

    def commute(self, s, a, b):
        return self.step(self.step(s, a), b) == self.step(self.step(s, b), a)

    def random_state(self, rng):
        return tuple(rng.choice(self.L, self.k, replace=False).tolist())

    def encode(self, s, a, b):
        # raw encoding: one-hot position of each token + one-hot of both actions (no hand-made relational features)
        v = np.zeros(self.k * self.L + 2 * self.A, dtype=np.float32)
        for i, p in enumerate(s):
            v[i * self.L + p] = 1
        v[self.k * self.L + a] = 1
        v[self.k * self.L + self.A + b] = 1
        return v


def train_predicate(world, n, seed, epochs=60):
    rng = np.random.default_rng(seed)
    X, Y = [], []
    for _ in range(n):
        s = world.random_state(rng)
        a, b = rng.choice(world.A, 2, replace=False)
        X.append(world.encode(s, a, b)); Y.append(float(world.commute(s, a, b)))
    X = torch.tensor(np.array(X)); Y = torch.tensor(np.array(Y))
    torch.manual_seed(seed)
    net = torch.nn.Sequential(torch.nn.Linear(X.shape[1], 128), torch.nn.ReLU(),
                              torch.nn.Linear(128, 128), torch.nn.ReLU(), torch.nn.Linear(128, 1))
    opt = torch.optim.Adam(net.parameters(), lr=2e-3, weight_decay=1e-5)
    bs = min(256, n)
    for ep in range(epochs):
        perm = torch.randperm(n)
        for i in range(0, n, bs):
            idx = perm[i:i + bs]
            loss = torch.nn.functional.binary_cross_entropy_with_logits(net(X[idx]).squeeze(1), Y[idx])
            opt.zero_grad(); loss.backward(); opt.step()
    return net


class Planner:
    def __init__(self, world, mode, net=None, thr=0.99):
        self.w, self.mode, self.net, self.thr = world, mode, net, thr
        self.cache = {}

    def commutes(self, s, a, b):
        if self.mode == "oracle":
            return self.w.commute(s, a, b)
        return self.table[(s, a, b)]

    def precompute(self):
        """batched inference of the learned predicate over every (state, a, b) — speed-up only"""
        keys, X = [], []
        for s in itertools.permutations(range(self.w.L), self.w.k):
            for a in range(self.w.A):
                for b in range(self.w.A):
                    if a != b:
                        keys.append((s, a, b)); X.append(self.w.encode(s, a, b))
        with torch.no_grad():
            P = torch.sigmoid(self.net(torch.tensor(np.array(X)))).squeeze(1).numpy()
        self.table = {k: bool(p > self.thr) for k, p in zip(keys, P)}
        return self

    def iddfs(self, start, goal, max_depth):
        self.nodes = 0
        for depth in range(max_depth + 1):
            path = self._dfs(start, goal, depth, None, None)
            if path is not None:
                return path
        return None

    def _dfs(self, s, goal, depth, prev_a, prev_s):
        self.nodes += 1
        if s == goal:
            return []
        if depth == 0:
            return None
        for b in range(self.w.A):
            s2 = self.w.step(s, b)
            if s2 == s:
                continue                       # skip no-ops (blocked moves)
            if self.mode != "none" and prev_a is not None and b < prev_a and self.commutes(prev_s, prev_a, b):
                continue                       # canonical-order move pruning
            r = self._dfs(s2, goal, depth - 1, b, s)
            if r is not None:
                return [b] + r
        return None


def bfs_dist(world, start, goal):
    from collections import deque
    q, seen = deque([(start, 0)]), {start}
    while q:
        s, d = q.popleft()
        if s == goal:
            return d
        for a in range(world.A):
            s2 = world.step(s, a)
            if s2 not in seen:
                seen.add(s2); q.append((s2, d + 1))
    return None


def evaluate(world, tasks, planner, max_depth):
    nodes, lost, longer = [], 0, 0
    t0 = time.time()
    for (st, gl, opt) in tasks:
        p = planner.iddfs(st, gl, max_depth)
        nodes.append(planner.nodes)
        if p is None:
            lost += 1
        elif len(p) > opt:
            longer += 1
    return dict(mean_nodes=float(np.mean(nodes)), median_nodes=float(np.median(nodes)), lost=lost,
                longer=longer, n=len(tasks), secs=time.time() - t0)


def make_tasks(world, n, lo, hi, seed):
    rng = np.random.default_rng(seed)
    tasks = []
    while len(tasks) < n:
        s, g = world.random_state(rng), world.random_state(rng)
        d = bfs_dist(world, s, g)
        if d is not None and lo <= d <= hi:
            tasks.append((s, g, d))
    return tasks


def predicate_accuracy(world, net, thr, n, seed):
    rng = np.random.default_rng(seed)
    fp = fn = pos = neg = 0
    for _ in range(n):
        s = world.random_state(rng); a, b = rng.choice(world.A, 2, replace=False)
        truth = world.commute(s, a, b)
        with torch.no_grad():
            pred = torch.sigmoid(net(torch.tensor(world.encode(s, a, b))[None])).item() > thr
        pos += truth; neg += (not truth)
        fp += (pred and not truth); fn += ((not pred) and truth)
    return dict(false_commute_rate=fp / max(neg, 1), missed_commute_rate=fn / max(pos, 1), frac_commute=pos / n)


if __name__ == "__main__":
    L, k = int(sys.argv[1]), int(sys.argv[2])
    lo, hi, ntask = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    world = LineWorld(L, k)
    tasks = make_tasks(world, ntask, lo, hi, 7)
    out = {"L": L, "k": k, "plan_len": [lo, hi]}
    out["none"] = evaluate(world, tasks, Planner(world, "none"), hi)
    out["oracle"] = evaluate(world, tasks, Planner(world, "oracle"), hi)
    print(json.dumps(out), flush=True)
    for n in [100, 300, 1000, 3000, 10000, 30000]:
        net = train_predicate(world, n, seed=n)
        for thr in [0.5, 0.9, 0.99]:
            acc = predicate_accuracy(world, net, thr, 3000, 99)
            ev = evaluate(world, tasks, Planner(world, "learned", net, thr).precompute(), hi)
            r = dict(n_train=n, thr=thr, **acc, **ev)
            out.setdefault("learned", []).append(r)
            print(json.dumps(r), flush=True)
    json.dump(out, open(f"cfwm_L{L}_k{k}.json", "w"), indent=1)
