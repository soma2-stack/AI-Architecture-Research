"""Plain level view for tests; no renderer or window dependency."""
from .model import Vec2

def render_level(level,player=None):
    rows=[list(row) for row in level.rows]
    if player is not None:
        x=int(player.position.x); y=int(player.position.y)
        if 0<=y<len(rows) and 0<=x<len(rows[y]): rows[y][x]="@"
    return "\n".join("".join(row) for row in rows)

def player_line(player): return f"{player.body_id} {player.position.x:.2f},{player.position.y:.2f} {player.lives}L {player.score}P"
def render_hud(player,tick): return f"T{tick} {player_line(player)}"
def marker_counts(level): return {glyph:len(level.find(glyph)) for glyph in ("S","G","P","M")}
def world_snapshot(world): return {"state":world.state(),"coins":sorted(world.coins),"platforms":[p.platform_id for p in world.platforms]}
