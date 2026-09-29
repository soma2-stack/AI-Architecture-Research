from spaceecs.collision import CollisionEvent
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.piercing import enable_piercing, resolve_piercing
from spaceecs.projectiles import spawn_projectile

def test_deferred_piercing_limit_is_enforced():
    world = World()
    owner = spawn_player(world)
    targets = [spawn_enemy(world, i, 0, hp=5) for i in range(5)]
    shot = enable_piercing(spawn_projectile(world, owner.entity_id, 0, 0, 1, 0))
    events = [CollisionEvent(shot.entity_id, e.entity_id, i) for i, e in enumerate(targets)]
    resolve_piercing(world, shot.entity_id, events)
    assert [e.hp for e in targets] == [4, 4, 4, 5, 5]
