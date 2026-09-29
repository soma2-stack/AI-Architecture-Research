from platformer.checkpoint import Checkpoint,CheckpointManager
from platformer.model import Player,Platform,Vec2,Waypoint
from platformer.save import load,save
from platformer.world import World

def test_full_round_trip_preserves_fixed_counter_route_checkpoint_and_one_way(tmp_path):
    player=Player("p",Vec2(2.5,3),Vec2(1,-2),1,1,False,2,9,3)
    world=World(player,[Platform("floor",(0,5,8,6),True)],tick_count=12,coins={"coin"},
                route=[Waypoint(3,4,1)],fixed_updates=12)
    manager=CheckpointManager(); manager.unlock(Checkpoint("cp",Vec2(7,8),9))
    row={"id":"one","rect":[1,2,4,3]}
    path=tmp_path/"save.json"; save(path,world,manager,[type("OneWay",(),{"platform_id":"one","rect":(1,2,4,3)})()])
    restored,checks,one_way=load(path)
    assert restored.player.velocity==Vec2(1,-2) and restored.fixed_updates==12
    assert restored.route==[Waypoint(3,4,1)] and restored.coins=={"coin"}
    assert checks.active().position==Vec2(7,8) and one_way==[row]
