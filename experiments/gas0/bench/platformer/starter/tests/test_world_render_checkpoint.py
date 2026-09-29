import pytest
from platformer.camera import Camera,centered_view,clamp_camera
from platformer.checkpoint import (Checkpoint,CheckpointManager,activate_if_reached,capture,
                                   checkpoint_payload,checkpoint_reached,respawn,respawn_active)
from platformer.collision import carry_body,landing,platform_delta,resolve_landing,separate_x
from platformer.geometry import Rect
from platformer.level import parse_level
from platformer.model import Body,Platform,Player,Vec2,Waypoint
from platformer.render import marker_counts,player_line,render_hud,render_level,world_snapshot
from platformer.world import (World,award_goal,carry_on_platform,first_waypoint,goal_reached,
                              platform_by_id,remove_platform,restart_at_checkpoint,route_complete,
                              route_distance,tick,tick_many,world_bounds)

def make_world():
    p=Player("p",Vec2(1,0),Vec2(0,0),1,1,False)
    platform=Platform("floor",(0,2,5,3))
    return World(p,[platform],route=[Waypoint(2,1)])

def test_landing_sets_ground_state_and_zeroes_vertical_speed():
    p=Player("p",Vec2(1,1.2),Vec2(0,2),1,1,False)
    platform=Platform("floor",(0,2,5,3))
    assert resolve_landing(p,platform,1.8)
    assert p.on_ground and p.velocity.y==0 and p.position.y==1

def test_landing_requires_downward_crossing():
    p=Player("p",Vec2(1,1),Vec2(0,-1),1,1,False)
    assert not landing(p,Platform("f",(0,2,5,3)),1)

def test_horizontal_separation_stops_velocity():
    p=Player("p",Vec2(0.2,0),Vec2(2,0),1,1,False)
    assert separate_x(p,Platform("wall",(1,0,2,4)))
    assert p.velocity.x==0 and p.position.x==0

def test_platform_carry_applies_single_delta():
    body=Body("b",Vec2(3,1),Vec2(0,0))
    assert carry_body(body,Vec2(1,0),Vec2(1,0))==Vec2(0,0)
    assert body.position==Vec2(3,1)

def test_platform_delta_is_current_minus_previous():
    assert platform_delta(Vec2(1,2),Vec2(1,2))==Vec2(0,0)

def test_world_tick_and_coin_removal():
    world=make_world(); world.coins={"c"}
    result=tick(world,0.01)
    assert result["tick"]==1 and world.tick_count==1
    assert world.player.score==0
    from platformer.world import remove_coin
    assert remove_coin(world,"c") and not remove_coin(world,"c") and world.player.score==1

def test_world_platforms_are_sorted_by_id():
    world=World(Player("p",Vec2(),Vec2()),[Platform("z",(2,2,3,3)),Platform("a",(0,0,1,1))])
    assert [p.platform_id for p in world.platforms]==["a","z"]

def test_checkpoint_capture_and_respawn():
    p=Player("p",Vec2(4,5),Vec2(3,2),1,1,False,2,7)
    point=capture(p,"cp1"); p.position=Vec2(0,0); p.score=0
    assert respawn(p,point)==Vec2(4,5)
    assert p.velocity==Vec2() and p.score==7 and p.lives==2

def test_checkpoint_overlap_and_payload():
    p=Player("p",Vec2(1,1),Vec2(),1,1)
    cp=Checkpoint("cp",Vec2(1,1),4)
    assert checkpoint_reached(p,Rect(0,0,2,2))
    assert checkpoint_payload(cp)=={"id":"cp","position":[1,1],"score":4}

def test_camera_follow_and_visibility():
    camera=Camera(4,3); assert camera.follow(Vec2(8,7),10,9)==Vec2(6,5.5)
    assert camera.visible(Vec2(7,7)) and not camera.visible(Vec2(1,1))

def test_camera_clamps_small_world_and_view():
    camera=Camera(10,10); camera.position=Vec2(8,8)
    assert clamp_camera(camera,4,4)==Vec2(0,0)
    assert centered_view(Vec2(2,2),4,4)==Vec2(0,0)

def test_text_renderer_overlays_player_without_mutating_level():
    level=parse_level("S.G")
    before=level.text(); p=Player("p",Vec2(1,0),Vec2())
    assert render_level(level,p)=="S@G" and level.text()==before

def test_hud_and_level_marker_counts_are_deterministic():
    level=parse_level("S.PG")
    p=Player("p",Vec2(0,0),Vec2())
    assert marker_counts(level)["P"]==1
    assert "T4" in render_hud(p,4) and player_line(p).startswith("p ")

def test_first_waypoint_selects_route_order():
    assert first_waypoint([Waypoint(2,3),Waypoint(4,5)])==Waypoint(2,3)

def test_checkpoint_manager_unlocks_activates_and_round_trips():
    manager=CheckpointManager(); first=Checkpoint("a",Vec2(1,2),3); manager.unlock(first)
    manager.unlock(Checkpoint("b",Vec2(4,5),6)); manager.activate("b")
    restored=CheckpointManager.from_payload(manager.payload())
    assert restored.ids()==("a","b") and restored.active().checkpoint_id=="b"

def test_checkpoint_manager_rejects_unknown_activation():
    with pytest.raises(KeyError): CheckpointManager().activate("missing")

def test_checkpoint_activation_requires_overlap():
    manager=CheckpointManager(); cp=Checkpoint("a",Vec2(1,1))
    player=Player("p",Vec2(10,10),Vec2())
    assert not activate_if_reached(manager,player,cp,Rect(0,0,2,2))
    assert activate_if_reached(manager,Player("q",Vec2(1,1),Vec2()),cp,Rect(0,0,2,2))

def test_respawn_active_handles_missing_checkpoint():
    assert not respawn_active(Player("p",Vec2(),Vec2()),CheckpointManager())

def test_world_platform_and_goal_queries():
    world=make_world(); assert platform_by_id(world,"floor") is world.platforms[0]
    assert remove_platform(world,"floor") and not remove_platform(world,"floor")
    assert world_bounds(world)==(0.0,0.0,0.0,0.0)

def test_goal_overlap_and_idempotent_award():
    world=make_world(); goal=Rect(1,0,2,1)
    assert goal_reached(world,goal)
    assert award_goal(world,"exit",100) and not award_goal(world,"exit",100)
    assert world.player.score==100

def test_tick_many_and_route_helpers():
    world=make_world(); assert len(tick_many(world,3,0.01))==3
    assert route_distance([Waypoint(0,0),Waypoint(2,0),Waypoint(2,3)])==5
    assert route_complete([Waypoint(0,0)],1)

def test_restart_resets_tick_and_restores_checkpoint_state():
    world=make_world(); world.tick_count=10; cp=Checkpoint("a",Vec2(2,2),7)
    result=restart_at_checkpoint(world,cp)
    assert result["tick"]==0 and world.player.position==Vec2(2,2)
