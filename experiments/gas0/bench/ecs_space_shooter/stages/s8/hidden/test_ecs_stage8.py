from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.piercing import enable_piercing
from spaceecs.projectiles import spawn_projectile
from spaceecs.save import load_world, save_world

def test_round_trip_preserves_shield_and_piercing():
    world = World(tick_count=4)
    owner = spawn_player(world)
    enemy = spawn_enemy(world, 2, 0)
    enemy.shield = 4
    shot = enable_piercing(spawn_projectile(world, owner.entity_id, 1, 0, 2, 0))
    restored = load_world(save_world(world))
    assert restored.entities[enemy.entity_id].shield == 4
    assert restored.projectiles[shot.entity_id].piercing

def test_next_identifier_survives_round_trip():
    world = World()
    spawn_enemy(world, 0, 0)
    restored = load_world(save_world(world))
    next_entity = spawn_enemy(restored, 1, 0)
    assert next_entity.entity_id == world.next_entity_id
