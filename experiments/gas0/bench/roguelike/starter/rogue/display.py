"""Plain-text rendering for tests and terminal sessions."""
from .model import Point

def render_grid(grid,player=None,enemies=()):
    rows=[list(row) for row in grid.rows]
    for enemy in sorted(enemies,key=lambda item:item.actor_id):
        if enemy.alive: rows[enemy.position.y][enemy.position.x]="g"
    if player is not None and player.alive: rows[player.position.y][player.position.x]="@"
    return "\n".join("".join(row) for row in rows)

def health_bar(actor,width=10):
    width=max(1,int(width)); filled=round(width*actor.hp/actor.max_hp)
    return "["+"#"*filled+"-"*(width-filled)+"]"

def status_line(player,turn):
    return f"{player.name} HP {player.hp}/{player.max_hp} L{player.level} T{turn}"

def inventory_lines(items): return tuple(f"{item.item_id}: {item.kind} {item.power}" for item in items)
def event_log(messages,limit=5): return tuple(messages[-max(0,int(limit)):])

def point_text(point:Point): return f"{point.x},{point.y}"
def world_status(world):
    state="lost" if world.lost else "won" if world.won else "active"
    return {"state":state,"turn":world.turn,"enemies":len(world.visible_enemies())}
