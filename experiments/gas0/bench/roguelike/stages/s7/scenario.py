from rogue.grid import Grid
from rogue.model import Player,Point
from rogue.world import World
world=World(Grid(["..." ]),Player("p","Hero",Point(0,0),1,1),[])
assert world.last_enemy_name() is None
