"""Finite rectangular map operations with deterministic neighbor order."""
from collections import deque
from .errors import InvalidMap
from .model import Point

WALL="#"; FLOOR="."; DOOR="+"; EXIT=">"
DIRECTIONS=((0,-1),(-1,0),(1,0),(0,1))

class Grid:
    def __init__(self,rows):
        self.rows=tuple(str(row) for row in rows)
        if not self.rows or not self.rows[0]: raise InvalidMap("map is empty")
        width=len(self.rows[0])
        if any(len(row)!=width for row in self.rows): raise InvalidMap("map rows must have equal width")
        if any(ch not in {WALL,FLOOR,DOOR,EXIT,"@","g"} for row in self.rows for ch in row):
            raise InvalidMap("map contains unknown tile")
        self.width=width; self.height=len(self.rows)
    def contains(self,point): return 0<=point.x<self.width and 0<=point.y<self.height
    def tile(self,point):
        if not self.contains(point): raise IndexError(point)
        return self.rows[point.y][point.x]
    def walkable(self,point): return self.contains(point) and self.tile(point)!=WALL
    def neighbors(self,point):
        return tuple(point.moved(dx,dy) for dx,dy in DIRECTIONS if self.walkable(point.moved(dx,dy)))
    def points(self):
        for y in range(self.height):
            for x in range(self.width): yield Point(x,y)
    def markers(self,marker): return tuple(p for p in self.points() if self.tile(p)==marker)
    def distance_map(self,start):
        distances={start:0}; queue=deque([start])
        while queue:
            current=queue.popleft()
            for nxt in self.neighbors(current):
                if nxt not in distances: distances[nxt]=distances[current]+1; queue.append(nxt)
        return distances
    def reachable(self,start,target): return target in self.distance_map(start)
    def nearest_reachable(self,start,targets):
        distances=self.distance_map(start)
        options=[(distances[p],p.y,p.x,p) for p in targets if p in distances]
        return min(options)[-1] if options else None
    def to_text(self): return "\n".join(self.rows)

def parse_map(text): return Grid(text.splitlines())
def orthogonal_distance(a,b): return a.manhattan(b)
def within_bounds(point,width,height): return 0<=point.x<width and 0<=point.y<height
