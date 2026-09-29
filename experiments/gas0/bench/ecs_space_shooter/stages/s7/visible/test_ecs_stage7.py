from spaceecs.collision import CollisionEvent
from spaceecs.combat import resolve_events
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World, remove_entity
from spaceecs.projectiles import spawn_projectile

def test_stale_collision_target_is_ignored():
    world = World()
    owner = spawn_player(world)
    target = spawn_enemy(world, 1, 0)
    shot = spawn_projectile(world, owner.entity_id, 0, 0, 1, 0)
    remove_entity(world, target.entity_id)
    assert resolve_events(world, [CollisionEvent(shot.entity_id, target.entity_id)]) == []
