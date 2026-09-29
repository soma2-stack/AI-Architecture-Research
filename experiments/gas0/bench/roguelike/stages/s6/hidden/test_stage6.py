from rogue.rng import SeededRNG,world_loot_roll
from rogue.grid import Grid
from rogue.model import Player,Point
from rogue.world import World

def test_each_world_event_consumes_one_private_draw():
    world=World(Grid(["..." ]),Player("p","P",Point(0,0),1,1),rng=SeededRNG(4))
    before=world.random_draws
    world_loot_roll(world,1.0)
    assert world.random_draws==before+1

def test_world_streams_are_isolated():
    a=World(Grid(["..." ]),Player("a","A",Point(0,0),1,1),rng=SeededRNG(7))
    b=World(Grid(["..." ]),Player("b","B",Point(0,0),1,1),rng=SeededRNG(7))
    world_loot_roll(a); assert a.random_draws==1 and b.random_draws==0
