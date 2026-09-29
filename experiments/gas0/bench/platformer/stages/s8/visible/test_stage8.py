from platformer.checkpoint import Checkpoint,CheckpointManager
from platformer.model import Player,Platform,Vec2
from platformer.save import load,save
from platformer.world import World

def test_save_round_trip_player_and_checkpoint(tmp_path):
    p=Player("p",Vec2(2,3),Vec2(1,-2),lives=2,score=8)
    manager=CheckpointManager(); manager.unlock(Checkpoint("cp",Vec2(4,5),8))
    world=World(p,[Platform("floor",(0,5,8,6),True)],tick_count=9,coins={"c"},fixed_updates=9)
    path=tmp_path/"save.json"; save(path,world,manager); restored,checks,one_way=load(path)
    assert restored.player.position==Vec2(2,3) and checks.active().checkpoint_id=="cp"
