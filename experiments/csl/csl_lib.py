"""
csl_lib — Certified Structural Learning as a reusable component (reference implementation, NumPy only).

Use it inside ANY model that grows/prunes parts (rules, experts, adapters, laws, memory slots):

    cert = Certifier(alpha_per_window=0.1, window=10_000, proposals_per_window=200)
    cid  = cert.propose(key, budget_share=1.0)          # budget fixed at proposal time (predictable)
    ...
    for each new example:
        # For every PENDING claim, give a statistic Z in [-1, 1] computed only from the model state
        # BEFORE seeing the label and from the label itself, with E[Z | past] <= 0 if the claim is useless.
        # Score-test recipe ("certify the need"):  Z = s * residual * phi(x) / R,
        #   residual = y - p (classification) or clip(y - yhat, -R, R) (regression), |phi| <= 1,
        #   s = direction proposed from PAST data, R = an input-INDEPENDENT bound.
        cert.observe_pending(cid, Z)
        # For every ADMITTED claim, give Z' in [-1, 1] with E[Z' | past] <= 0 while it keeps helping by
        # >= delta (e.g., Z' = (loss_with - loss_without + delta) / bound for its frozen certified statement).
        cert.observe_admitted(cid, Z_prime)
        for cid in cert.newly_admitted(): ...add the part to the model...
        for cid in cert.newly_retired():  ...remove the part...

Guarantees (see Claude_Research.md, Part L):
  * E[# never-useful claims admitted among those proposed in any window] <= alpha_per_window
    (union bound; holds under drift, adaptive proposals, arbitrary dependence, continuous monitoring);
  * average run length to a false retirement >= arl (Shiryaev-Roberts e-detector).
Lessons built in: mixture of bets; SR (not start-at-admission) retirement; stopping/restarting tests is always valid.
"""
import math
import numpy as np

LAMS = np.array([0.025, 0.05, 0.1, 0.2, 0.4, 0.8])


def _mix_log(lw):
    m = lw.max()
    return m + math.log(np.exp(lw - m).mean())


class Certifier:
    def __init__(self, alpha_per_window=0.1, window=10_000, proposals_per_window=200, arl=1e5):
        self.alpha_slot = alpha_per_window / proposals_per_window
        self.window, self.max_props, self.arl = window, proposals_per_window, arl
        self.claims = {}            # key -> dict(state, alpha, lw, lwr, t_prop, t_adm)
        self.t = 0
        self._recent = []           # proposal times inside the current window (budget accounting)
        self._new_adm, self._new_ret = [], []

    # ----------------------------------------------------------------- proposals
    def propose(self, key, budget_share=1.0):
        """Register a candidate. budget_share in (0, 1] (e.g., a proposer's confidence or 2**-codelength).
        Returns False if the per-window proposal budget is exhausted (then the claim is NOT tested)."""
        self._recent = [s for s in self._recent if s > self.t - self.window]
        if len(self._recent) >= self.max_props or key in self.claims:
            return False
        self._recent.append(self.t)
        self.claims[key] = dict(state="pending", alpha=self.alpha_slot * min(max(budget_share, 1e-12), 1.0),
                                lw=np.zeros(len(LAMS)), lwr=np.zeros(len(LAMS)), t_prop=self.t, t_adm=None)
        return True

    def drop(self, key):
        """Stop testing a pending claim (always valid: stopping never creates an admission)."""
        if key in self.claims and self.claims[key]["state"] == "pending":
            del self.claims[key]

    def restart(self, key):
        """Down-scale a pending claim's wealth to <= 1 (always valid), e.g. after an overlapping admission."""
        c = self.claims.get(key)
        if c and c["state"] == "pending":
            c["lw"] = np.minimum(c["lw"], 0.0)

    # ----------------------------------------------------------------- evidence
    def observe_pending(self, key, z):
        c = self.claims[key]
        assert c["state"] == "pending" and -1.0 <= z <= 1.0
        c["lw"] += np.log1p(LAMS * z)
        if _mix_log(c["lw"]) >= math.log(1.0 / c["alpha"]):
            c["state"], c["t_adm"] = "admitted", self.t
            c["lwr"][:] = 0.0
            self._new_adm.append(key)

    def observe_admitted(self, key, z):
        c = self.claims[key]
        assert c["state"] == "admitted" and -1.0 <= z <= 1.0
        c["lwr"] = np.logaddexp(0.0, c["lwr"]) + np.log1p(LAMS * z)     # Shiryaev-Roberts, per bet size
        if _mix_log(c["lwr"]) >= math.log(self.arl):
            c["state"] = "retired"
            self._new_ret.append(key)

    def tick(self):
        """Call once per example after all observe_* calls."""
        self.t += 1

    # ----------------------------------------------------------------- queries
    def newly_admitted(self):
        out, self._new_adm = self._new_adm, []
        return out

    def newly_retired(self):
        out, self._new_ret = self._new_ret, []
        for k in out:
            del self.claims[k]
        return out

    def state(self, key):
        return self.claims[key]["state"] if key in self.claims else None

    def evidence(self, key):
        """log-wealth of a pending claim (admission) or log SR statistic of an admitted claim (retirement)"""
        c = self.claims[key]
        return _mix_log(c["lw"]) if c["state"] == "pending" else _mix_log(c["lwr"])


if __name__ == "__main__":
    # tiny self-test: one real effect, 50 null candidates; count false admissions
    rng = np.random.default_rng(0)
    cert = Certifier(proposals_per_window=51)
    keys = list(range(51))
    for k in keys:
        cert.propose(k)
    admitted = set()
    for t in range(5000):
        x = rng.random(51) < 0.5
        y = float(rng.random() < (0.75 if x[0] else 0.25))      # only feature 0 matters
        p = 0.5                                                  # current model: constant
        for k in keys:
            if cert.state(k) == "pending":
                cert.observe_pending(k, (y - p) * (1.0 if x[k] else -1.0))   # s=+1, phi = +-1, R = 1
        admitted.update(cert.newly_admitted())
        cert.tick()
    print("admitted:", sorted(admitted), "(expected: [0]; false admissions have prob <= 0.1)")
