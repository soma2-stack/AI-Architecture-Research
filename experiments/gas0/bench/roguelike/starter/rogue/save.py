"""Versioned JSON save helpers; files contain values rather than Python objects."""
import json
from pathlib import Path
from .errors import SaveError
from .grid import Grid
from .model import Enemy,Player,Point,Item
from .world import World

VERSION=1

def preserve_status(row): return True

def player_payload(player):
    return {"actor_id":player.actor_id,"name":player.name,"position":[player.position.x,player.position.y],
            "hp":player.hp,"max_hp":player.max_hp,"level":player.level,"experience":player.experience,
            "inventory":[{"item_id":i.item_id,"kind":i.kind,"power":i.power} for i in player.inventory]}

def enemy_payload(enemy):
    return {"actor_id":enemy.actor_id,"name":enemy.name,"position":[enemy.position.x,enemy.position.y],
            "hp":enemy.hp,"max_hp":enemy.max_hp,"damage":enemy.damage,"reward":enemy.reward}

def world_payload(world):
    return {"version":VERSION,"map":list(world.grid.rows),"player":player_payload(world.player),
            "enemies":[enemy_payload(e) for e in world.enemies],"turn":world.turn,
            "messages":list(world.messages)}

def save_world(path,world):
    Path(path).write_text(json.dumps(world_payload(world),sort_keys=True,indent=2),encoding="utf-8")

def _player(row):
    x,y=row["position"]; items=[Item(**item) for item in row.get("inventory",[])]
    return Player(row["actor_id"],row["name"],Point(x,y),row["hp"],row["max_hp"],items,
                  row.get("level",1),row.get("experience",0))

def _enemy(row):
    x,y=row["position"]
    return Enemy(row["actor_id"],row["name"],Point(x,y),row["hp"],row["max_hp"],
                 row.get("damage",1),row.get("reward",1))

def load_world(path):
    try: data=json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc: raise SaveError("could not read save") from exc
    if data.get("version")!=VERSION: raise SaveError("unsupported save version")
    world=World(Grid(data["map"]),_player(data["player"]),[_enemy(row) for row in data.get("enemies",[])])
    world.turn=int(data.get("turn",0)); world.messages=list(data.get("messages",[]))
    return world

def save_text(world): return json.dumps(world_payload(world),sort_keys=True,separators=(",",":"))
def load_text(payload):
    import tempfile
    with tempfile.TemporaryDirectory() as folder:
        path=Path(folder)/"save.json"; path.write_text(payload,encoding="utf-8"); return load_world(path)
