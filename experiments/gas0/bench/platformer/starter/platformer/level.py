"""Text-only level parsing and deterministic marker discovery."""
from .errors import LevelError
from .model import Vec2

WALL="#"; EMPTY="."; START="S"; GOAL="G"; PLATFORM="="

class Level:
    def __init__(self,rows):
        self.rows=tuple(str(row) for row in rows)
        if not self.rows or not self.rows[0]: raise LevelError("empty level")
        self.width=len(self.rows[0]); self.height=len(self.rows)
        if any(len(row)!=self.width for row in self.rows): raise LevelError("level must be rectangular")
        if any(ch not in {WALL,EMPTY,START,GOAL,PLATFORM,"M","P"} for row in self.rows for ch in row): raise LevelError("unknown level glyph")
        if len(self.find(START))!=1: raise LevelError("level needs one start")
    def find(self,glyph): return tuple(Vec2(x,y) for y,row in enumerate(self.rows) for x,ch in enumerate(row) if ch==glyph)
    def tile(self,x,y):
        if not 0<=x<self.width or not 0<=y<self.height: return WALL
        return self.rows[y][x]
    def text(self): return "\n".join(self.rows)

def parse_level(text): return Level(text.splitlines())
def is_solid(glyph): return glyph in {WALL,PLATFORM}
def goal_position(level):
    found=level.find(GOAL); return found[0] if found else None
def start_position(level): return level.find(START)[0]
def collectable_positions(level): return level.find("P")

def neighbors(level,point):
    x,y=int(point.x),int(point.y)
    options=(Vec2(x,y-1),Vec2(x-1,y),Vec2(x+1,y),Vec2(x,y+1))
    return tuple(p for p in options if level.tile(int(p.x),int(p.y))!=WALL)

def reachable(level,start,target):
    pending=[start]; seen={start}
    while pending:
        current=pending.pop(0)
        if current==target: return True
        for nxt in neighbors(level,current):
            if nxt not in seen: seen.add(nxt); pending.append(nxt)
    return False

def level_bounds(level): return (0,0,level.width,level.height)

def count_solid(level): return sum(is_solid(ch) for row in level.rows for ch in row)

def walkable(level,point): return level.tile(int(point.x),int(point.y)) not in {WALL}

def nearest_marker(level,point,glyph):
    matches=level.find(glyph)
    return min(matches,key=lambda p:(abs(p.x-point.x)+abs(p.y-point.y),p.y,p.x)) if matches else None

def collect_marker(level,point,glyph):
    x,y=int(point.x),int(point.y)
    if level.tile(x,y)!=glyph: return False
    rows=[list(row) for row in level.rows]; rows[y][x]=EMPTY
    level.rows=tuple("".join(row) for row in rows)
    return True

def platform_tiles(level):
    """Return one unit rectangle for every solid platform glyph."""
    from .model import Platform
    return tuple(Platform(f"tile:{x}:{y}",(x,y,x+1,y+1))
                 for y,row in enumerate(level.rows) for x,glyph in enumerate(row)
                 if glyph==PLATFORM)

def contains_hazard(level,point): return level.tile(int(point.x),int(point.y))=="M"

def starts_at(level,point): return point==start_position(level)

def level_size(level):
    """Return the stable rectangular extent and number of grid cells."""
    return {"width":level.width,"height":level.height,"cells":level.width*level.height}

def in_bounds(level,x,y):
    return 0<=int(x)<level.width and 0<=int(y)<level.height
