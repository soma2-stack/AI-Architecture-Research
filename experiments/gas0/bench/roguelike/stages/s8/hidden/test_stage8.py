from rogue.combat import attack
from rogue.damage import DamageType,ResistanceProfile
from rogue.grid import Grid
from rogue.model import Enemy,Item,Player,Point
from rogue.rng import SeededRNG,world_loot_roll
from rogue.save import save_world,load_world
from rogue.world import World

def test_cumulative_system_round_trip_preserves_deterministic_next_drop(tmp_path):
    world=World(Grid(["..." ]),Player("p","Hero",Point(0,0),6,12,[Item("t","tonic")]),
                [Enemy("e","Rat",Point(1,0),4,4)],rng=SeededRNG(31))
    world.statuses.apply_poison("p",3,1)
    attack(world.player,world.enemies[0],2,DamageType.FIRE,ResistanceProfile(fire=1))
    world_loot_roll(world)
    path=tmp_path/"state.json"; save_world(path,world); restored=load_world(path)
    assert restored.enemies[0].hp==world.enemies[0].hp
    assert restored.statuses.get("p").remaining==3
    assert world_loot_roll(world)==world_loot_roll(restored)
