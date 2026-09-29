"""Author the eight-stage deterministic headless platformer benchmark."""
from __future__ import annotations
import difflib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent; STARTER=ROOT/"starter"; STAGES=ROOT/"stages"; REFERENCE=ROOT/"reference"
def snap(): return {p.relative_to(STARTER).as_posix():p.read_text(encoding="utf-8") for p in STARTER.rglob("*.py") if "__pycache__" not in p.parts}
def diff(a,b):
    out=[]
    for name in sorted(set(a)|set(b)):
        x=a.get(name,"").splitlines(keepends=True); y=b.get(name,"").splitlines(keepends=True)
        if x!=y: out.extend(difflib.unified_diff(x,y,fromfile=f"a/{name}" if name in a else "/dev/null",tofile=f"b/{name}" if name in b else "/dev/null"))
    return "".join(out)
def put(n,folder,name,body):
    p=STAGES/f"s{n}"/folder/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(body.strip()+"\n",encoding="utf-8")
def rep(s,name,a,b):
    if s[name].count(a)!=1: raise AssertionError((name,a,s[name].count(a)))
    s[name]=s[name].replace(a,b)
def patch(n,a,b): (REFERENCE/f"s{n}.patch").write_bytes(diff(a,b).encode("utf-8"))

def main():
    for d in (STAGES,REFERENCE):
        if d.exists(): shutil.rmtree(d)
    REFERENCE.mkdir(parents=True); s=snap(); before=s.copy(); (REFERENCE/"s1.patch").write_bytes(b"")
    put(1,"","request.md","""Do not edit. Inspect the platformer and return JSON with exactly q1 through q8: q1 the Player type; q2 the rectangle overlap function; q3 fixed-step body integrator; q4 solid landing resolver; q5 ASCII level parser; q6 checkpoint capture function; q7 World frame update; q8 text renderer. Use exact identifiers.""")

    # Stage 2: directional dash keeps vertical velocity unchanged.
    s["platformer/dash.py"]='''"""Short horizontal burst input for the headless player."""
from .model import Vec2,clamp

def dash(player,axis,speed=12,ticks=6):
    if ticks<=0: return False
    direction=1 if axis>0 else -1 if axis<0 else 0
    if direction==0: return False
    player.velocity=Vec2(direction*abs(float(speed)),player.velocity.y)
    player.dash_ticks=int(ticks)
    return True

def advance_dash(player):
    if player.dash_ticks<=0: return False
    player.dash_ticks-=1
    return player.dash_ticks>0

def cancel_dash(player): player.dash_ticks=0
def dash_ready(player): return player.dash_ticks==0
'''
    put(2,"","request.md","""Add a directional dash. It sets horizontal speed from the input direction and configured magnitude for a bounded number of ticks. Preserve the player's current vertical velocity exactly, including while airborne; zero direction does not start a dash.""")
    put(2,"visible","test_stage2.py","""from platformer.dash import dash
from platformer.model import Player,Vec2

def test_dash_preserves_airborne_vertical_velocity():
    player=Player("p",Vec2(0,0),Vec2(1,7),on_ground=False)
    assert dash(player,1,12,4)
    assert player.velocity==Vec2(12,7) and player.dash_ticks==4
""")
    put(2,"hidden","test_stage2.py","""from platformer.dash import advance_dash,dash,dash_ready
from platformer.model import Player,Vec2

def test_left_dash_preserves_negative_vertical_velocity():
    player=Player("p",Vec2(),Vec2(3,-5),on_ground=False)
    assert dash(player,-1,8,2) and player.velocity==Vec2(-8,-5)

def test_zero_direction_does_not_start_dash():
    player=Player("p",Vec2(),Vec2(2,4))
    assert not dash(player,0) and dash_ready(player)

def test_dash_duration_counts_down_without_changing_vertical_speed():
    player=Player("p",Vec2(),Vec2(0,9),on_ground=False); dash(player,1,3,2)
    assert advance_dash(player) and not advance_dash(player)
    assert player.velocity.y==9 and dash_ready(player)
""")
    put(2,"hidden","test_stage2_legacy.py","""from platformer.geometry import Rect,overlap

def test_closed_edge_contact_counts_as_collision_in_legacy_geometry():
    assert overlap(Rect(0,0,1,1),Rect(1,0,2,1))
""")
    put(2,"","supersedes.json","[]"); patch(2,before,s); before=s.copy()

    # Stage 3 pressure plate requires a grounded player; defer one-way platforms.
    s["platformer/pressure.py"]='''"""Weight-sensitive pressure switch evaluation."""
from .geometry import Rect,overlap,from_body

def pressed(player,plate):
    if not player.on_ground: return False
    feet=Rect(player.position.x,player.position.y+player.height-0.05,
              player.position.x+player.width,player.position.y+player.height+0.05)
    return overlap(feet,plate)

def update_plate(player,plate,previous=False):
    current=pressed(player,plate)
    return {"pressed":current,"activated":current and not previous,
            "released":previous and not current}

def plate_weight(player): return max(1,int(player.width*player.height))
'''
    put(3,"","request.md","""Add pressure plates and activation-edge reporting. Designer decision D3.1: only a grounded player's feet can press a plate; airborne overlap does not activate it. Defer one-way platform support until Stage 7.""")
    put(3,"visible","test_stage3.py","""from platformer.geometry import Rect
from platformer.model import Player,Vec2
from platformer.pressure import pressed,update_plate

def test_grounded_player_presses_plate():
    player=Player("p",Vec2(1,1),Vec2(),on_ground=True)
    assert pressed(player,Rect(0,1.9,3,2.2))

def test_airborne_overlap_does_not_press_plate():
    player=Player("p",Vec2(1,1),Vec2(),on_ground=False)
    assert not pressed(player,Rect(0,1.9,3,2.2))
""")
    put(3,"hidden","test_stage3.py","""from platformer.geometry import Rect
from platformer.model import Player,Vec2
from platformer.pressure import plate_weight,update_plate

def test_plate_reports_only_transition_edges():
    player=Player("p",Vec2(1,1),Vec2(),on_ground=True); plate=Rect(0,1.9,3,2.2)
    assert update_plate(player,plate,False)=={"pressed":True,"activated":True,"released":False}
    assert update_plate(player,plate,True)=={"pressed":True,"activated":False,"released":False}

def test_plate_weight_is_positive_for_small_players():
    player=Player("p",Vec2(),Vec2(),width=.5,height=.5)
    assert plate_weight(player)==1
""")
    put(3,"hidden","test_one_way_deferred.py","""def test_one_way_platform_support_is_deferred():
    import importlib.util
    assert importlib.util.find_spec("platformer.one_way") is None
""")
    put(3,"","supersedes.json","[]"); patch(3,before,s); before=s.copy()

    # Stage 4 injected double platform displacement; stable starter helper.
    collision="platformer/collision.py"; old='    return current-previous'; injected='    return (current-previous).scaled(2)'
    prior=s.copy(); rep(s,collision,old,injected); bugged=s.copy()
    (STAGES/"s4").mkdir(parents=True,exist_ok=True)
    (STAGES/"s4"/"bug.patch").write_bytes(diff(prior,bugged).encode("utf-8"))
    put(4,"","request.md","""Moving platforms carry a grounded player farther than the platform moves. Diagnose and fix the repeated displacement while keeping normal gravity and landing behavior intact.""")
    put(4,"visible","test_stage4.py","""from platformer.collision import carry_body
from platformer.model import Body,Vec2

def test_platform_carry_matches_one_frame_delta():
    body=Body("b",Vec2(3,1),Vec2())
    carry_body(body,Vec2(1,0),Vec2(2,0))
    assert body.position==Vec2(4,1)
""")
    put(4,"hidden","test_stage4.py","""from platformer.collision import carry_body
from platformer.model import Body,Vec2

def test_vertical_and_horizontal_carrier_motion_apply_once():
    body=Body("b",Vec2(5,5),Vec2())
    delta=carry_body(body,Vec2(1,2),Vec2(4,6))
    assert delta==Vec2(3,4) and body.position==Vec2(8,9)
""")
    put(4,"","supersedes.json","[]")
    fixed=s.copy(); rep(fixed,collision,injected,old); patch(4,s,fixed); s=fixed; before=s.copy()

    # Stage 5 adopts half-open collision intervals.
    geom="platformer/geometry.py"
    rep(s,geom,'return a.left<=b.right and a.right>=b.left and a.top<=b.bottom and a.bottom>=b.top',
        'return a.left<b.right and a.right>b.left and a.top<b.bottom and a.bottom>b.top')
    rep(s,geom,'return Rect(left,top,right,bottom) if right>=left and bottom>=top else None',
        'return Rect(left,top,right,bottom) if right>left and bottom>top else None')
    put(5,"","request.md","""Change collision rectangles to half-open intervals: touching edges are adjacent but have zero shared area and do not collide. Update overlap and intersection consistently; preserve positive-area collisions and platform landing semantics.""")
    put(5,"visible","test_stage5.py","""from platformer.geometry import Rect,intersection,overlap

def test_edge_contact_is_not_overlap():
    assert not overlap(Rect(0,0,1,1),Rect(1,0,2,1))
    assert intersection(Rect(0,0,1,1),Rect(1,0,2,1)) is None
""")
    put(5,"hidden","test_stage5.py","""from platformer.geometry import Rect,intersection,overlap

def test_positive_area_still_collides_but_corner_contact_does_not():
    assert overlap(Rect(0,0,2,2),Rect(1,1,3,3))
    assert not overlap(Rect(0,0,1,1),Rect(1,1,2,2))

def test_intersection_uses_half_open_area():
    assert intersection(Rect(0,0,2,2),Rect(1,1,3,3))==Rect(1,1,2,2)
""")
    put(5,"","supersedes.json",json.dumps(["tests/hidden_2/test_stage2_legacy.py"]))
    patch(5,before,s); before=s.copy()

    # Stage 6 integer fixed-point update path.
    s["platformer/fixed.py"]='''"""Signed fixed-point arithmetic for reproducible frame updates."""
from dataclasses import dataclass
SCALE=65536

@dataclass(frozen=True,order=True)
class Fixed:
    raw:int
    @classmethod
    def from_number(cls,value): return cls(round(float(value)*SCALE))
    def to_number(self): return self.raw/SCALE
    def __add__(self,other): return Fixed(self.raw+coerce(other).raw)
    def __sub__(self,other): return Fixed(self.raw-coerce(other).raw)
    def __mul__(self,other): return Fixed((self.raw*coerce(other).raw)//SCALE)
    def __truediv__(self,other):
        divisor=coerce(other).raw
        if divisor==0: raise ZeroDivisionError("fixed division by zero")
        return Fixed((self.raw*SCALE)//divisor)

def coerce(value): return value if isinstance(value,Fixed) else Fixed.from_number(value)
def fixed_sum(values): return Fixed(sum(coerce(v).raw for v in values))
def quantized_position(x,y): return (Fixed.from_number(x),Fixed.from_number(y))
'''
    s["platformer/fixed.py"]+='''\ndef step_fixed_body(body,dt,gravity=18):\n    fx,fy=quantized_position(body.position.x,body.position.y)\n    vx,vy=quantized_position(body.velocity.x,body.velocity.y)\n    step=coerce(dt); g=coerce(gravity)\n    if not body.on_ground: vy=vy+g*step\n    fx=fx+vx*step; fy=fy+vy*step\n    body.position=type(body.position)(fx.to_number(),fy.to_number())\n    body.velocity=type(body.velocity)(vx.to_number(),vy.to_number())\n    return body.position\n'''
    world="platformer/world.py"
    rep(s,world,'from .physics import step_body\n','from .physics import step_body\nfrom .fixed import step_fixed_body\n')
    rep(s,world,'    coins:set=field(default_factory=set)\n','    coins:set=field(default_factory=set)\n    fixed_updates:int=0\n')
    rep(s,world,'    step_body(world.player,dt)\n',
        '    step_fixed_body(world.player,dt)\n    world.fixed_updates+=1\n')
    put(6,"","request.md","""Persistent global constraint G6.1: authoritative World frame integration uses signed fixed-point integer state, not floating accumulation. Convert to display numbers only at API/render boundaries; keep repeated updates deterministic.""")
    put(6,"","static_checks.py","""import ast
from pathlib import Path

def test_world_frame_path_uses_fixed_point():
    root=Path(__file__).resolve().parents[1]/"platformer"
    tree=ast.parse((root/"world.py").read_text(encoding="utf-8"))
    calls={node.func.id for node in ast.walk(tree) if isinstance(node,ast.Call) and isinstance(node.func,ast.Name)}
    assert "step_fixed_body" in calls and "step_body" not in calls
""")
    put(6,"visible","test_stage6.py","""from platformer.fixed import Fixed

def test_fixed_operations_keep_integer_raw_state():
    a=Fixed.from_number(1.25); b=Fixed.from_number(0.5)
    result=a+b
    assert type(result.raw) is int and result.to_number()==1.75
""")
    put(6,"hidden","test_stage6.py","""from platformer.fixed import Fixed
from platformer.model import Player,Vec2
from platformer.world import World,tick_many

def test_world_updates_quantize_to_same_fixed_state_each_run():
    def simulate():
        world=World(Player("p",Vec2(),Vec2(1,0)),[])
        tick_many(world,60,1/60)
        return (world.player.position,world.player.velocity,world.fixed_updates)
    assert simulate()==simulate() and simulate()[2]==60

def test_fixed_division_by_zero_is_explicit():
    import pytest
    with pytest.raises(ZeroDivisionError): Fixed.from_number(1)/Fixed(0)
""")
    put(6,"","supersedes.json","[]"); patch(6,before,s); before=s.copy()

    # Stage 7 repairs empty route crash and implements deferred one-way platforms.
    rep(s,world,'def first_waypoint(route): return route[0]','def first_waypoint(route): return route[0] if route else None')
    s["platformer/one_way.py"]='''"""One-way platforms only catch downward crossings from above."""
from dataclasses import dataclass
from .geometry import Rect
from .model import Vec2

@dataclass(frozen=True)
class OneWayPlatform:
    platform_id:str
    rect:tuple[float,float,float,float]
    def __post_init__(self):
        if not self.platform_id or self.rect[2]<=self.rect[0] or self.rect[3]<=self.rect[1]:
            raise ValueError("invalid one-way platform")

def can_land(body,platform,previous_bottom):
    left,top,right,bottom=body.bounds(); pl,pt,pr,pb=platform.rect
    return (body.velocity.y>=0 and previous_bottom<=pt<=bottom and right>pl and left<pr)

def land(body,platform,previous_bottom):
    if not can_land(body,platform,previous_bottom): return False
    body.position=Vec2(body.position.x,platform.rect[1]-body.height)
    body.velocity=Vec2(body.velocity.x,0); body.on_ground=True
    return True

def blocks_from_below(body,platform): return False
'''
    put(7,"","scenario.py","""from platformer.world import first_waypoint
assert first_waypoint([]) is None
""")
    put(7,"","request.md","""The scripted route has no waypoint and crashes while selecting the next target. Fix the empty-route case. Also implement the one-way platforms deferred in Stage 3: catch downward crossings from above and allow upward passage from below.""")
    put(7,"visible","test_stage7.py","""from platformer.model import Body,Vec2
from platformer.one_way import OneWayPlatform,land
from platformer.world import first_waypoint

def test_empty_route_has_no_next_waypoint():
    assert first_waypoint([]) is None

def test_one_way_platform_catches_from_above():
    body=Body("b",Vec2(1,1.5),Vec2(0,2),1,1,False)
    assert land(body,OneWayPlatform("p",(0,2,4,3)),1.5)
    assert body.on_ground and body.velocity.y==0
""")
    put(7,"hidden","test_stage7.py","""from platformer.model import Body,Vec2
from platformer.one_way import OneWayPlatform,blocks_from_below,can_land,land
from platformer.world import first_waypoint

def test_waypoint_selector_is_safe_for_empty_and_nonempty_routes():
    assert first_waypoint([]) is None
    assert first_waypoint([Vec2(1,2)])==Vec2(1,2)

def test_one_way_platform_allows_ascending_body_to_pass_through():
    body=Body("b",Vec2(1,2.2),Vec2(0,-3),1,1,False)
    platform=OneWayPlatform("p",(0,2,4,3))
    assert not can_land(body,platform,3.2) and not blocks_from_below(body,platform)

def test_one_way_requires_horizontal_overlap_and_downward_motion():
    platform=OneWayPlatform("p",(0,2,4,3))
    body=Body("b",Vec2(5,1),Vec2(0,2),1,1,False)
    assert not land(body,platform,1.5)
""")
    put(7,"hidden","test_one_way_deferred_stage7.py","""from platformer.model import Body,Vec2
from platformer.one_way import OneWayPlatform,land

def test_deferred_one_way_platform_catches_from_above_but_not_below():
    p=OneWayPlatform("p",(0,2,4,3))
    above=Body("a",Vec2(1,1),Vec2(0,2),1,1,False)
    below=Body("b",Vec2(1,2.2),Vec2(0,-2),1,1,False)
    assert land(above,p,1.8)
    assert not land(below,p,3.2)
""")
    put(7,"","supersedes.json",json.dumps(["tests/hidden_3/test_one_way_deferred.py"]))
    patch(7,before,s); before=s.copy()

    # Stage 8 save integrates fixed world, checkpoint manager and one-way state.
    s["platformer/save.py"]='''"""Deterministic JSON checkpoint integration for the headless platformer."""
import json
from pathlib import Path
from .checkpoint import CheckpointManager
from .fixed import SCALE
from .model import Player,Vec2,Platform,Waypoint
from .world import World

VERSION=1
def payload(world,checkpoints=None,one_way=()):
    p=world.player
    return {"version":VERSION,"player":{"id":p.body_id,"position":[p.position.x,p.position.y],
        "velocity":[p.velocity.x,p.velocity.y],"width":p.width,"height":p.height,"on_ground":p.on_ground,
        "lives":p.lives,"score":p.score,"dash_ticks":p.dash_ticks},
        "platforms":[{"id":x.platform_id,"rect":list(x.rect),"moving":x.moving} for x in world.platforms],
        "tick":world.tick_count,"coins":sorted(world.coins),"fixed_updates":world.fixed_updates,
        "fixed_scale":SCALE,"route":[{"x":w.x,"y":w.y,"dwell":w.dwell} for w in world.route],
        "checkpoints":(checkpoints or CheckpointManager()).payload(),
        "one_way":[{"id":x.platform_id,"rect":list(x.rect)} for x in one_way]}

def save(path,world,checkpoints=None,one_way=()):
    Path(path).write_text(json.dumps(payload(world,checkpoints,one_way),sort_keys=True,indent=2),encoding="utf-8")

def load(path):
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("version")!=VERSION: raise ValueError("unsupported save version")
    row=data["player"]; p=Player(row["id"],Vec2(*row["position"]),Vec2(*row["velocity"]),
        row["width"],row["height"],row["on_ground"],row["lives"],row["score"],row.get("dash_ticks",0))
    platforms=[Platform(x["id"],tuple(x["rect"]),x.get("moving",False)) for x in data["platforms"]]
    world=World(p,platforms,tick_count=data["tick"],coins=set(data["coins"]),
                route=[Waypoint(**w) for w in data["route"]],
                fixed_updates=data.get("fixed_updates",0))
    return world,CheckpointManager.from_payload(data.get("checkpoints",{})),data.get("one_way",[])
'''
    put(8,"","request.md","""Integrate world, checkpoint manager, fixed-update counters, route state, and one-way platform definitions with deterministic save/load. Round-trip must preserve player motion, score/lives, activated checkpoint, collected coins, and one-way platform geometry.""")
    put(8,"visible","test_stage8.py","""from platformer.checkpoint import Checkpoint,CheckpointManager
from platformer.model import Player,Platform,Vec2
from platformer.save import load,save
from platformer.world import World

def test_save_round_trip_player_and_checkpoint(tmp_path):
    p=Player("p",Vec2(2,3),Vec2(1,-2),lives=2,score=8)
    manager=CheckpointManager(); manager.unlock(Checkpoint("cp",Vec2(4,5),8))
    world=World(p,[Platform("floor",(0,5,8,6),True)],tick_count=9,coins={"c"},fixed_updates=9)
    path=tmp_path/"save.json"; save(path,world,manager); restored,checks,one_way=load(path)
    assert restored.player.position==Vec2(2,3) and checks.active().checkpoint_id=="cp"
""")
    put(8,"hidden","test_stage8.py","""from platformer.checkpoint import Checkpoint,CheckpointManager
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
""")
    put(8,"","supersedes.json","[]"); patch(8,before,s)

    manifest={"project":"platformer","kind":"evaluation","stages":8,
      "orientation_answers":{"q1":"platformer.model.Player","q2":"platformer.geometry.overlap","q3":"platformer.physics.step_body","q4":"platformer.collision.resolve_landing","q5":"platformer.level.parse_level","q6":"platformer.checkpoint.capture","q7":"platformer.world.tick","q8":"platformer.render.render_level"},
      "probes":[
       {"introduced":1,"retired":2,"tests":[f"Q{i}" for i in range(1,9)],"text_only":False,"requirement":"R1.1"},
       {"introduced":2,"retired":None,"tests":["tests/hidden_2/test_stage2.py::test_left_dash_preserves_negative_vertical_velocity","tests/hidden_2/test_stage2.py::test_zero_direction_does_not_start_dash","tests/hidden_2/test_stage2.py::test_dash_duration_counts_down_without_changing_vertical_speed"],"text_only":False,"requirement":"R2.1"},
       {"introduced":2,"retired":5,"tests":["tests/hidden_2/test_stage2_legacy.py::test_closed_edge_contact_counts_as_collision_in_legacy_geometry"],"text_only":True,"requirement":"R2.2"},
       {"introduced":3,"retired":None,"tests":["tests/hidden_3/test_stage3.py::test_plate_reports_only_transition_edges","tests/hidden_3/test_stage3.py::test_plate_weight_is_positive_for_small_players"],"text_only":False,"requirement":"R3.1"},
       {"introduced":3,"retired":7,"tests":["tests/hidden_3/test_one_way_deferred.py::test_one_way_platform_support_is_deferred"],"text_only":True,"requirement":"R3.2"},
       {"introduced":4,"retired":None,"tests":["tests/hidden_4/test_stage4.py::test_vertical_and_horizontal_carrier_motion_apply_once"],"text_only":False,"requirement":"R4.1"},
       {"introduced":5,"retired":None,"tests":["tests/hidden_5/test_stage5.py::test_positive_area_still_collides_but_corner_contact_does_not"],"text_only":False,"requirement":"R5.1"},
       {"introduced":6,"retired":None,"tests":["tests/hidden_6/test_stage6.py::test_world_updates_quantize_to_same_fixed_state_each_run","tests/hidden_6/test_stage6.py::test_fixed_division_by_zero_is_explicit"],"text_only":False,"requirement":"G6.1"},
       {"introduced":7,"retired":None,"tests":["tests/hidden_7/test_stage7.py::test_waypoint_selector_is_safe_for_empty_and_nonempty_routes","tests/hidden_7/test_stage7.py::test_one_way_platform_allows_ascending_body_to_pass_through","tests/hidden_7/test_one_way_deferred_stage7.py::test_deferred_one_way_platform_catches_from_above_but_not_below"],"text_only":False,"requirement":"R3.2"},
       {"introduced":8,"retired":None,"tests":["tests/hidden_8/test_stage8.py::test_full_round_trip_preserves_fixed_counter_route_checkpoint_and_one_way"],"text_only":False,"requirement":"R8.1"}]}
    (ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__": main()
