from rogue.effects import StatusBook
from rogue.grid import Grid
from rogue.model import Item,Player,Point
from rogue.rng import SeededRNG,world_loot_roll
from rogue.save import save_world,load_world
from rogue.world import World

def test_world_state_round_trip_keeps_status_inventory_and_rng(tmp_path):
    world=World(Grid(["..." ]),Player("p","Hero",Point(0,0),5,10,[Item("c","charm")]),rng=SeededRNG(3))
    world.statuses.apply_poison("p",2,1); world_loot_roll(world)
    path=tmp_path/"save.json"; save_world(path,world); loaded=load_world(path)
    assert loaded.statuses.get("p").remaining==2 and loaded.player.inventory[0].kind=="charm"
    assert world_loot_roll(world)==world_loot_roll(loaded)
