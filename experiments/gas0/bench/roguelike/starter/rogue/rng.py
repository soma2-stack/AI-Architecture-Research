"""Small seeded random source used by deterministic map and loot helpers."""
import random

class SeededRNG:
    def __init__(self,seed): self.seed=int(seed); self._random=random.Random(self.seed)
    def randint(self,low,high): return self._random.randint(int(low),int(high))
    def choice(self,values):
        if not values: raise ValueError("cannot choose from empty sequence")
        return self._random.choice(tuple(values))
    def shuffle(self,values):
        result=list(values); self._random.shuffle(result); return result
    def state(self): return self._random.getstate()
    def restore(self,state): self._random.setstate(state)

def loot_roll(rng,chance=0.25): return rng.randint(0,9999)<int(float(chance)*10000)
def choose_spawn(rng,points): return rng.choice(points)
def deterministic_order(rng,values): return tuple(rng.shuffle(values))
def clamped_chance(value): return max(0.0,min(1.0,float(value)))
