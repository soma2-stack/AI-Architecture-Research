from spaceecs.collision import CollisionEvent
from spaceecs.ids import spawn_enemy, spawn_player
from spaceecs.model import World
from spaceecs.piercing import enable_piercing, resolve_piercing
from spaceecs.projectiles import spawn_projectile

def test_piercing_hits_at_most_three_distinct_live_targets():
    world = World()
    owner = spawn_player(world)
    targets = [spawn_enemy(world, i, 0, hp=5) for i in range(5)]
    shot = enable_piercing(spawn_projectile(world, owner.entity_id, 0, 0, 1, 0, damage=1))
    events = [CollisionEvent(shot.entity_id, item.entity_id, index / 10)
              for index, item in enumerate(targets)]
    events.insert(1, CollisionEvent(shot.entity_id, targets[0].entity_id, 0.15))
    resolve_piercing(world, shot.entity_id, events)
    assert [item.hp for item in targets] == [4, 4, 4, 5, 5]

def test_stale_and_duplicate_ids_do_not_use_hit_budget():
    from spaceecs.model import remove_entity
    world = World()
    owner = spawn_player(world)
    targets = [spawn_enemy(world, i, 0, hp=5) for i in range(4)]
    shot = enable_piercing(spawn_projectile(world, owner.entity_id, 0, 0, 1, 0))
    remove_entity(world, targets[0].entity_id)
    events = [CollisionEvent(shot.entity_id, targets[0].entity_id, 0.0)]
    events += [CollisionEvent(shot.entity_id, item.entity_id, i / 10)
               for i, item in enumerate(targets[1:], 1)]
    resolve_piercing(world, shot.entity_id, events)
    assert [item.hp for item in targets[1:]] == [4, 4, 4]

def test_resolve_event_skips_removed_target():
    from spaceecs.combat import resolve_events
    from spaceecs.model import remove_entity
    world = World()
    owner = spawn_player(world)
    target = spawn_enemy(world, 1, 0)
    shot = spawn_projectile(world, owner.entity_id, 0, 0, 1, 0)
    remove_entity(world, target.entity_id)
    assert resolve_events(world, [CollisionEvent(shot.entity_id, target.entity_id)]) == []
