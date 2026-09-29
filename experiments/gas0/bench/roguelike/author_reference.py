"""Build the text roguelike's staged reference and private tests."""
from __future__ import annotations
import difflib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent; STARTER=ROOT/"starter"; STAGES=ROOT/"stages"; REFERENCE=ROOT/"reference"
def snapshot(): return {p.relative_to(STARTER).as_posix():p.read_text(encoding="utf-8") for p in STARTER.rglob("*.py") if "__pycache__" not in p.parts}
def diff(a,b):
    out=[]
    for name in sorted(set(a)|set(b)):
        x=a.get(name,"").splitlines(keepends=True); y=b.get(name,"").splitlines(keepends=True)
        if x!=y: out.extend(difflib.unified_diff(x,y,fromfile=f"a/{name}" if name in a else "/dev/null",tofile=f"b/{name}" if name in b else "/dev/null"))
    return "".join(out)
def put(n,folder,name,body):
    p=STAGES/f"s{n}"/folder/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(body.strip()+"\n",encoding="utf-8")
def rep(state,name,old,new):
    if state[name].count(old)!=1: raise AssertionError((name,old,state[name].count(old)))
    state[name]=state[name].replace(old,new)
def patch(n,a,b): (REFERENCE/f"s{n}.patch").write_bytes(diff(a,b).encode("utf-8"))

def main():
    for d in (STAGES,REFERENCE):
        if d.exists(): shutil.rmtree(d)
    REFERENCE.mkdir(parents=True); state=snapshot(); files=state.copy(); (REFERENCE/"s1.patch").write_bytes(b"")
    put(1,"","request.md","""Do not edit. Inspect the game and return JSON with exactly q1 through q8: q1 the player record; q2 the map class; q3 the movement function; q4 combat attack function; q5 potion use entry point; q6 save schema version; q7 deterministic RNG class; q8 text renderer. Use exact identifiers and values.""")

    # Stage 2: tonic improves maximum health and current health by two.
    model="rogue/model.py"; inventory="rogue/inventory.py"
    rep(state,model,'{"potion","key","weapon"}','{"potion","key","weapon","tonic"}')
    state[inventory]+='''\n\ndef use_tonic(player,item_id):\n    item=next((row for row in player.inventory if row.item_id==item_id),None)\n    if item is None: raise KeyError(item_id)\n    if item.kind!="tonic": raise InvalidAction("item is not a tonic")\n    player.max_hp+=2\n    player.hp=min(player.max_hp,player.hp+2)\n    player.inventory.remove(item)\n    return player.max_hp,player.hp\n'''
    put(2,"","request.md","""Add a tonic consumable. Designer decision D2.1: using one permanently raises maximum health by 2 and restores up to 2 current health; it is consumed once. Keep ordinary potion behavior unchanged.""")
    put(2,"visible","test_stage2.py","""from rogue.inventory import use_tonic
from rogue.model import Item,Player,Point

def test_tonic_raises_cap_and_heals_two():
    player=Player("p","Hero",Point(0,0),5,10,[Item("t","tonic")])
    assert use_tonic(player,"t")== (12,7)
    assert player.inventory==[]
""")
    put(2,"hidden","test_stage2.py","""from rogue.inventory import use_tonic
from rogue.model import Item,Player,Point

def test_tonic_at_full_health_keeps_new_capacity_available():
    player=Player("p","Hero",Point(0,0),10,10,[Item("t","tonic")])
    use_tonic(player,"t")
    assert player.max_hp==12 and player.hp==12

def test_tonic_consumption_cannot_be_repeated():
    import pytest
    player=Player("p","Hero",Point(0,0),5,10,[Item("t","tonic")])
    use_tonic(player,"t")
    with pytest.raises(KeyError): use_tonic(player,"t")
""")
    put(2,"hidden","test_stage2_legacy.py","""from rogue.combat import attack
from rogue.model import Enemy,Player,Point

def test_flat_attack_has_no_damage_type_field_yet():
    p=Player("p","Hero",Point(0,0),5,5); e=Enemy("e","Rat",Point(1,0),3,3)
    assert not hasattr(attack(p,e,1),"damage_type")
""")
    put(2,"","supersedes.json","[]"); patch(2,files,state); files=state.copy()

    # Stage 3: status ledger and nonlethal poison; defer a cleansing charm.
    state["rogue/effects.py"]='''"""Compact turn-based status effect ledger."""
from dataclasses import dataclass
from .combat import poison_tick_amount

@dataclass
class Poison:
    remaining:int
    damage:int
    def __post_init__(self):
        if self.remaining<0 or self.damage<0: raise ValueError("invalid poison")

class StatusBook:
    def __init__(self): self.effects={}
    def apply_poison(self,actor_id,turns,damage):
        self.effects[actor_id]=Poison(int(turns),int(damage)); return self.effects[actor_id]
    def get(self,actor_id): return self.effects.get(actor_id)
    def remove(self,actor_id): return self.effects.pop(actor_id,None)
    def payload(self):
        return {key:{"remaining":value.remaining,"damage":value.damage} for key,value in sorted(self.effects.items())}
    @classmethod
    def from_payload(cls,data):
        book=cls(); book.effects={key:Poison(**row) for key,row in data.items()}; return book

def tick_poison(actor,book):
    effect=book.get(actor.actor_id)
    if effect is None or effect.remaining==0 or not actor.alive: return 0
    amount=poison_tick_amount(effect.damage)
    applied=min(amount,max(0,actor.hp-1))
    actor.take_damage(applied); effect.remaining-=1
    if effect.remaining==0: book.remove(actor.actor_id)
    return applied

def status_names(book,actor_id): return ("poison",) if book.get(actor_id) else ()
'''
    world="rogue/world.py"
    rep(state,world,'from .model import Enemy,Player,Point,actor_at\n',
        'from .model import Enemy,Player,Point,actor_at\nfrom .effects import StatusBook\n')
    rep(state,world,'    messages:list[str]=field(default_factory=list)\n',
        '    messages:list[str]=field(default_factory=list)\n    statuses:StatusBook=field(default_factory=StatusBook)\n')
    put(3,"","request.md","""Add persistent poison status effects that tick once at the end of each turn. Designer decision D3.1: poison cannot reduce a living actor below 1 HP. Defer a cleansing-charm interaction until Stage 7; do not implement it yet.""")
    put(3,"visible","test_stage3.py","""from rogue.effects import StatusBook,tick_poison
from rogue.model import Player,Point

def test_poison_ticks_and_expires():
    player=Player("p","Hero",Point(0,0),8,10); book=StatusBook()
    book.apply_poison("p",2,2)
    assert tick_poison(player,book)>0
    assert tick_poison(player,book)>0 and book.get("p") is None
""")
    put(3,"hidden","test_stage3.py","""from rogue.effects import StatusBook,tick_poison
from rogue.model import Player,Point

def test_poison_is_nonlethal_even_when_damage_exceeds_health():
    player=Player("p","Hero",Point(0,0),2,10); book=StatusBook(); book.apply_poison("p",1,50)
    tick_poison(player,book)
    assert player.hp==1 and player.alive

def test_status_book_round_trip_preserves_duration():
    book=StatusBook(); book.apply_poison("p",3,2)
    restored=StatusBook.from_payload(book.payload())
    assert restored.get("p").remaining==3 and restored.get("p").damage==2

def test_poison_for_another_actor_does_not_tick_player():
    player=Player("p","Hero",Point(0,0),8,10); book=StatusBook(); book.apply_poison("e",2,2)
    assert tick_poison(player,book)==0 and player.hp==8
""")
    put(3,"hidden","test_cleanse_deferred.py","""def test_cleansing_charm_is_deferred():
    import rogue.effects as effects
    assert not hasattr(effects,"use_cleansing_charm")
""")
    put(3,"","supersedes.json","[]"); patch(3,files,state); files=state.copy()

    # Stage 4 injects a bounded-damage regression into a starter helper so every
    # validation replay mode can apply the bug patch before Stage 3 reference code.
    combat="rogue/combat.py"
    old='    return max(0,int(damage))'
    injected='    value=max(0,int(damage))\n    return value*2 if value>3 else value'
    before=state.copy(); rep(state,combat,old,injected); bugged=state.copy()
    (STAGES/"s4").mkdir(parents=True,exist_ok=True)
    (STAGES/"s4"/"bug.patch").write_bytes(diff(before,bugged).encode("utf-8"))
    put(4,"","request.md","""After the latest status change, poison is removing health faster than its configured tick amount. Find and fix the double-application regression; preserve duration and the nonlethal rule.""")
    put(4,"visible","test_stage4.py","""from rogue.effects import StatusBook,tick_poison
from rogue.model import Player,Point

def test_poison_applies_configured_damage_once():
    player=Player("p","Hero",Point(0,0),8,10); book=StatusBook(); book.apply_poison("p",1,4)
    assert tick_poison(player,book)==4 and player.hp==4
""")
    put(4,"hidden","test_stage4.py","""from rogue.effects import StatusBook,tick_poison
from rogue.model import Player,Point

def test_repeated_poison_ticks_do_not_double_damage():
    player=Player("p","Hero",Point(0,0),10,10); book=StatusBook(); book.apply_poison("p",2,4)
    assert tick_poison(player,book)==4 and tick_poison(player,book)==4
    assert player.hp==2
""")
    put(4,"","supersedes.json","[]")
    fixed=state.copy(); rep(fixed,combat,injected,old); patch(4,state,fixed); state=fixed; files=state.copy()

    # Stage 5 typed damage packets and resistances.
    state["rogue/damage.py"]='''"""Typed damage packets with explicit, bounded mitigation."""
from dataclasses import dataclass
from enum import Enum
from .model import Actor

class DamageType(str,Enum):
    PHYSICAL="physical"; FIRE="fire"; POISON="poison"

@dataclass(frozen=True)
class DamagePacket:
    amount:int
    kind:DamageType
    source_id:str
    def __post_init__(self):
        if self.amount<0: raise ValueError("damage cannot be negative")

@dataclass(frozen=True)
class ResistanceProfile:
    physical:int=0
    fire:int=0
    poison:int=0
    def against(self,kind): return max(0,int(getattr(self,DamageType(kind).value)))

@dataclass(frozen=True)
class DamageOutcome:
    kind:DamageType
    attempted:int
    resisted:int
    applied:int
    defeated:bool

def resolve_damage(target:Actor,packet:DamagePacket,resistance=ResistanceProfile()):
    blocked=min(packet.amount,resistance.against(packet.kind))
    applied=target.take_damage(packet.amount-blocked)
    return DamageOutcome(packet.kind,packet.amount,blocked,applied,not target.alive)

def weakness_bonus(packet,weakness):
    return DamagePacket(packet.amount+1,packet.kind,packet.source_id) if DamageType(packet.kind)==DamageType(weakness) else packet
'''
    combat_source=state[combat]
    rep(state,combat,'from .errors import InvalidAction\n','from .errors import InvalidAction\nfrom .damage import DamagePacket,DamageType,ResistanceProfile,resolve_damage\n')
    rep(state,combat,'    defeated:bool\n','    defeated:bool\n    damage_type:str="physical"\n')
    rep(state,combat,'def attack(source:Actor,target:Actor,power=1):\n',
        'def attack(source:Actor,target:Actor,power=1,kind=DamageType.PHYSICAL,resistance=ResistanceProfile()):\n')
    rep(state,combat,'    amount=max(0,int(power)); applied=target.take_damage(amount)\n'
        '    return CombatResult(source.actor_id,target.actor_id,amount,applied,not target.alive)\n',
        '    packet=DamagePacket(max(0,int(power)),DamageType(kind),source.actor_id)\n'
        '    outcome=resolve_damage(target,packet,resistance)\n'
        '    return CombatResult(source.actor_id,target.actor_id,outcome.attempted,outcome.applied,outcome.defeated,outcome.kind.value)\n')
    put(5,"","request.md","""Replace flat attack damage with typed physical, fire, and poison damage packets. Apply a matching resistance before health loss, preserve nonnegative damage and defeat reporting, and keep the existing default attack physical.""")
    put(5,"visible","test_stage5.py","""from rogue.combat import attack
from rogue.damage import DamageType,ResistanceProfile
from rogue.model import Enemy,Player,Point

def test_default_attack_is_typed_physical():
    p=Player("p","Hero",Point(0,0),5,5); e=Enemy("e","Rat",Point(1,0),5,5)
    result=attack(p,e,2)
    assert result.damage_type=="physical" and e.hp==3

def test_matching_resistance_reduces_only_that_damage_type():
    p=Player("p","Hero",Point(0,0),5,5); e=Enemy("e","Rat",Point(1,0),5,5)
    result=attack(p,e,4,DamageType.FIRE,ResistanceProfile(fire=3))
    assert result.applied==1 and result.damage_type=="fire"
""")
    put(5,"hidden","test_stage5.py","""from rogue.damage import DamagePacket,DamageType,ResistanceProfile,resolve_damage,weakness_bonus
from rogue.model import Enemy,Point

def test_resistance_cannot_absorb_more_than_attempted_damage():
    enemy=Enemy("e","Rat",Point(0,0),5,5)
    outcome=resolve_damage(enemy,DamagePacket(2,DamageType.FIRE,"p"),ResistanceProfile(fire=10))
    assert outcome.resisted==2 and outcome.applied==0 and enemy.hp==5

def test_weakness_bonus_is_typed_and_immutable():
    packet=DamagePacket(2,DamageType.FIRE,"p")
    assert weakness_bonus(packet,DamageType.FIRE).amount==3
    assert weakness_bonus(packet,DamageType.POISON) is packet and packet.amount==2
""")
    put(5,"","supersedes.json",json.dumps(["tests/hidden_2/test_stage2_legacy.py"]))
    patch(5,files,state); files=state.copy()

    # Stage 6 world-owned RNG and static rule.
    world="rogue/world.py"
    rep(state,world,'from .effects import StatusBook\n','from .effects import StatusBook\nfrom .rng import SeededRNG,loot_roll\n')
    rep(state,world,'    statuses:StatusBook=field(default_factory=StatusBook)\n',
        '    statuses:StatusBook=field(default_factory=StatusBook)\n'
        '    rng:SeededRNG=field(default_factory=lambda:SeededRNG(0))\n'
        '    random_draws:int=0\n')
    state["rogue/rng.py"]+='''\n\ndef world_loot_roll(world,chance=0.25):\n    """Consume exactly one draw from this world's retained random stream."""\n    world.random_draws+=1\n    return loot_roll(world.rng,chance)\n\ndef roll_enemy_drop(world,enemy_id,chance=0.25):\n    return {"enemy_id":enemy_id,"dropped":world_loot_roll(world,chance),"draw":world.random_draws}\n'''
    put(6,"","request.md","""Persistent global constraint G6.1: every stochastic gameplay choice must draw from the World-owned seeded stream; no module-global random state. Add a deterministic world loot event that consumes one draw and retains its draw count. Preserve reproducibility across identical seeds.""")
    put(6,"","static_checks.py","""import ast
from pathlib import Path

def test_random_draws_are_owned_by_seeded_rng():
    root=Path(__file__).resolve().parents[1]/"rogue"
    for path in root.glob("*.py"):
        tree=ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute):
                if isinstance(node.func.value,ast.Name) and node.func.value.id=="random":
                    assert path.name=="rng.py" and node.func.attr=="Random",path.name
""")
    put(6,"visible","test_stage6.py","""from rogue.rng import world_loot_roll
from rogue.save import load_world,save_world
from rogue.grid import Grid
from rogue.model import Player,Point
from rogue.world import World
from rogue.rng import SeededRNG

def test_world_seed_repeats_loot_stream():
    a=World(Grid(["..." ]),Player("p","P",Point(0,0),1,1),rng=SeededRNG(9))
    b=World(Grid(["..." ]),Player("p","P",Point(0,0),1,1),rng=SeededRNG(9))
    assert [world_loot_roll(a) for _ in range(5)]==[world_loot_roll(b) for _ in range(5)]
    assert a.random_draws==5
""")
    put(6,"hidden","test_stage6.py","""from rogue.rng import SeededRNG,world_loot_roll
from rogue.grid import Grid
from rogue.model import Player,Point
from rogue.world import World

def test_each_world_event_consumes_one_private_draw():
    world=World(Grid(["..." ]),Player("p","P",Point(0,0),1,1),rng=SeededRNG(4))
    before=world.random_draws
    world_loot_roll(world,1.0)
    assert world.random_draws==before+1

def test_world_streams_are_isolated():
    a=World(Grid(["..." ]),Player("a","A",Point(0,0),1,1),rng=SeededRNG(7))
    b=World(Grid(["..." ]),Player("b","B",Point(0,0),1,1),rng=SeededRNG(7))
    world_loot_roll(a); assert a.random_draws==1 and b.random_draws==0
""")
    put(6,"","supersedes.json","[]"); patch(6,files,state); files=state.copy()

    # Stage 7 fixes empty-enemy summary crash and implements deferred charm.
    old='    def last_enemy_name(self): return self.visible_enemies()[-1].name\n'
    new='    def last_enemy_name(self):\n        enemies=self.visible_enemies()\n        return enemies[-1].name if enemies else None\n'
    rep(state,world,old,new)
    state["rogue/effects.py"]+='''\n\ndef use_cleansing_charm(player,book,item_id):\n    item=next((row for row in player.inventory if row.item_id==item_id),None)\n    if item is None: raise KeyError(item_id)\n    if item.kind!="charm": raise ValueError("item is not a cleansing charm")\n    book.remove(player.actor_id); player.heal(1); player.inventory.remove(item)\n    return player.hp\n'''
    rep(state,model,'{"potion","key","weapon","tonic"}','{"potion","key","weapon","tonic","charm"}')
    put(7,"","scenario.py","""from rogue.grid import Grid
from rogue.model import Player,Point
from rogue.world import World
world=World(Grid(["..." ]),Player("p","Hero",Point(0,0),1,1),[])
assert world.last_enemy_name() is None
""")
    put(7,"","request.md","""The empty-room victory report crashes after the last enemy is removed. Diagnose and fix the runtime failure. Also implement the cleansing-charm interaction deferred in Stage 3: it removes poison from the player, heals 1 HP, and consumes the charm.""")
    put(7,"visible","test_stage7.py","""from rogue.effects import StatusBook,use_cleansing_charm
from rogue.model import Item,Player,Point

def test_cleansing_charm_removes_poison_heals_and_consumes():
    player=Player("p","Hero",Point(0,0),5,10,[Item("c","charm")]); book=StatusBook()
    book.apply_poison("p",3,2)
    assert use_cleansing_charm(player,book,"c")==6
    assert book.get("p") is None and player.inventory==[]
""")
    put(7,"hidden","test_stage7.py","""from rogue.effects import StatusBook,use_cleansing_charm
from rogue.model import Item,Player,Point
from rogue.world import World
from rogue.grid import Grid

def test_empty_world_summary_is_safe_after_final_defeat():
    world=World(Grid(["..." ]),Player("p","Hero",Point(0,0),1,1),[])
    assert world.last_enemy_name() is None

def test_charm_preserves_unrelated_statuses_and_cannot_be_reused():
    player=Player("p","Hero",Point(0,0),1,10,[Item("c","charm")]); book=StatusBook()
    book.apply_poison("other",2,1); book.apply_poison("p",1,1)
    use_cleansing_charm(player,book,"c")
    assert book.get("other").remaining==2 and book.get("p") is None
""")
    put(7,"hidden","test_cleanse_deferred_stage7.py","""from rogue.effects import StatusBook,use_cleansing_charm
from rogue.model import Item,Player,Point

def test_deferred_cleansing_charm_removes_poison_and_consumes_item():
    player=Player("p","Hero",Point(0,0),4,10,[Item("c","charm")]); book=StatusBook()
    book.apply_poison("p",2,2); use_cleansing_charm(player,book,"c")
    assert book.get("p") is None and player.hp==5 and player.inventory==[]
""")
    put(7,"","supersedes.json",json.dumps(["tests/hidden_3/test_cleanse_deferred.py"]))
    patch(7,files,state); files=state.copy()

    # Stage 8 persists typed state, effects and the world-owned random stream.
    save="rogue/save.py"
    rep(state,save,'"messages":list(world.messages)}','"messages":list(world.messages),\n            "statuses":world.statuses.payload(),"random_draws":world.random_draws,\n            "rng_state":world.rng.state()}')
    rep(state,save,'    world.turn=int(data.get("turn",0)); world.messages=list(data.get("messages",[]))\n',
        '    world.turn=int(data.get("turn",0)); world.messages=list(data.get("messages",[]))\n'
        '    from .effects import StatusBook\n'
        '    from .rng import SeededRNG\n'
        '    world.statuses=StatusBook.from_payload(data.get("statuses",{}))\n'
        '    world.random_draws=int(data.get("random_draws",0))\n'
        '    world.rng=SeededRNG(0)\n'
        '    if data.get("rng_state") is not None: world.rng.restore(data["rng_state"])\n')
    # JSON array state becomes tuple before random.Random.setstate.
    rng="rogue/rng.py"
    rep(state,rng,'    def restore(self,state): self._random.setstate(state)\n',
        '    def restore(self,state):\n'
        '        version,values,gauss=state\n'
        '        self._random.setstate((version,tuple(values),gauss))\n')
    put(8,"","request.md","""Integrate typed damage, status effects, inventory, turn state, and the world's RNG stream with versioned save/load. A save/load round trip must preserve poison duration, tonic/charm inventory, damage-related actor state, RNG continuation, and deterministic next loot result.""")
    put(8,"visible","test_stage8.py","""from rogue.effects import StatusBook
from rogue.grid import Grid
from rogue.model import Item,Player,Point
from rogue.rng import SeededRNG,world_loot_roll
from rogue.save import save_world,load_world
from rogue.world import World

def test_world_state_round_trip_keeps_status_inventory_and_rng(tmp_path):
    world=World(Grid(["..." ]),Player("p","Hero",Point(0,0),5,10,[Item("c","charm")]),rng=SeededRNG(3))
    world.statuses.apply_poison("p",2,1); world_loot_roll(world)
    path=tmp_path/"save.json"; save_world(path,world); loaded=load_world(path)
    assert loaded.statuses.get("p").remaining==2 and loaded.player.inventory[0].kind=="charm"
    assert world_loot_roll(world)==world_loot_roll(loaded)
""")
    put(8,"hidden","test_stage8.py","""from rogue.combat import attack
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
""")
    put(8,"","supersedes.json","[]"); patch(8,files,state)

    manifest={"project":"roguelike","kind":"evaluation","stages":8,
      "orientation_answers":{"q1":"rogue.model.Player","q2":"rogue.grid.Grid","q3":"rogue.world.move_player","q4":"rogue.combat.attack","q5":"rogue.inventory.use_potion","q6":1,"q7":"rogue.rng.SeededRNG","q8":"rogue.display.render_grid"},
      "probes":[
       {"introduced":1,"retired":2,"tests":[f"Q{i}" for i in range(1,9)],"text_only":False,"requirement":"R1.1"},
       {"introduced":2,"retired":None,"tests":["tests/hidden_2/test_stage2.py::test_tonic_at_full_health_keeps_new_capacity_available","tests/hidden_2/test_stage2.py::test_tonic_consumption_cannot_be_repeated"],"text_only":False,"requirement":"R2.1"},
       {"introduced":2,"retired":5,"tests":["tests/hidden_2/test_stage2_legacy.py::test_flat_attack_has_no_damage_type_field_yet"],"text_only":True,"requirement":"R2.2"},
       {"introduced":3,"retired":None,"tests":["tests/hidden_3/test_stage3.py::test_poison_is_nonlethal_even_when_damage_exceeds_health","tests/hidden_3/test_stage3.py::test_status_book_round_trip_preserves_duration","tests/hidden_3/test_stage3.py::test_poison_for_another_actor_does_not_tick_player"],"text_only":False,"requirement":"R3.1"},
       {"introduced":3,"retired":7,"tests":["tests/hidden_3/test_cleanse_deferred.py::test_cleansing_charm_is_deferred"],"text_only":True,"requirement":"R3.2"},
       {"introduced":4,"retired":None,"tests":["tests/hidden_4/test_stage4.py::test_repeated_poison_ticks_do_not_double_damage"],"text_only":False,"requirement":"R4.1"},
       {"introduced":5,"retired":None,"tests":["tests/hidden_5/test_stage5.py::test_resistance_cannot_absorb_more_than_attempted_damage","tests/hidden_5/test_stage5.py::test_weakness_bonus_is_typed_and_immutable"],"text_only":False,"requirement":"R5.1"},
       {"introduced":6,"retired":None,"tests":["tests/hidden_6/test_stage6.py::test_each_world_event_consumes_one_private_draw","tests/hidden_6/test_stage6.py::test_world_streams_are_isolated"],"text_only":False,"requirement":"G6.1"},
       {"introduced":7,"retired":None,"tests":["tests/hidden_7/test_stage7.py::test_empty_world_summary_is_safe_after_final_defeat","tests/hidden_7/test_stage7.py::test_charm_preserves_unrelated_statuses_and_cannot_be_reused","tests/hidden_7/test_cleanse_deferred_stage7.py::test_deferred_cleansing_charm_removes_poison_and_consumes_item"],"text_only":False,"requirement":"R3.2"},
       {"introduced":8,"retired":None,"tests":["tests/hidden_8/test_stage8.py::test_cumulative_system_round_trip_preserves_deterministic_next_drop"],"text_only":False,"requirement":"R8.1"}]}
    (ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__": main()
