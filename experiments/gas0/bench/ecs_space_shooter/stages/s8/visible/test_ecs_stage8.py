from spaceecs.ids import spawn_enemy
from spaceecs.model import World
from spaceecs.save import load_world, save_world

def test_world_round_trip_preserves_core_state():
    world = World(tick_count=7)
    enemy = spawn_enemy(world, 2, 3, hp=6)
    restored = load_world(save_world(world))
    assert restored.tick_count == 7
    assert restored.entities[enemy.entity_id].hp == 6
