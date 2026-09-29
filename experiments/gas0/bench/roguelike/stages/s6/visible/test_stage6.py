from rogue.rng import world_loot_roll
from rogue.save import load_world,save_world
from rogue.grid import Grid
from rogue.model import Player,Point
from rogue.world import World
from rogue.rng import SeededRNG

def test_world_seed_repeats_loot_stream():
    a=World(Grid(["..." ]),Player("p","P",Point(0,0),1,1),rng=SeededRNG(9))
    b=World(Grid(["..." ]),Player("p","P",Point(0,0),1,1),rng=SeededRNG(9))
    assert [world_loot_roll(a) for _ in range(5)]==[world_loot_roll(b) for _ in range(5)]
    assert a.random_draws==5
