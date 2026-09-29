"""Value objects for axis-aligned, deterministic platform motion."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Vec2:
    x:float=0.0
    y:float=0.0
    def __add__(self,other): return Vec2(self.x+other.x,self.y+other.y)
    def __sub__(self,other): return Vec2(self.x-other.x,self.y-other.y)
    def scaled(self,factor): return Vec2(self.x*factor,self.y*factor)
    def length_squared(self): return self.x*self.x+self.y*self.y

@dataclass
class Body:
    body_id:str
    position:Vec2
    velocity:Vec2
    width:float=1.0
    height:float=1.0
    on_ground:bool=False
    def __post_init__(self):
        if not self.body_id or self.width<=0 or self.height<=0: raise ValueError("invalid body")
    def translate(self,delta): self.position=self.position+delta
    def bounds(self): return (self.position.x,self.position.y,self.position.x+self.width,self.position.y+self.height)

@dataclass
class Player(Body):
    lives:int=3
    score:int=0
    dash_ticks:int=0
    def award(self,points):
        if points<0: raise ValueError("points cannot be negative")
        self.score+=int(points); return self.score
    def lose_life(self): self.lives=max(0,self.lives-1); return self.lives

@dataclass(frozen=True)
class Platform:
    platform_id:str
    rect:tuple[float,float,float,float]
    moving:bool=False
    def __post_init__(self):
        if not self.platform_id: raise ValueError("platform id required")
        x1,y1,x2,y2=self.rect
        if x2<=x1 or y2<=y1: raise ValueError("platform bounds must have positive area")

@dataclass
class Waypoint:
    x:float
    y:float
    dwell:int=0
    def __post_init__(self):
        if self.dwell<0: raise ValueError("dwell cannot be negative")

def clamp(value,low,high): return max(low,min(high,value))
def direction(value): return 1 if value>0 else -1 if value<0 else 0
def quantize(value,step=0.01): return round(round(value/step)*step,8)
def body_center(body): return Vec2(body.position.x+body.width/2,body.position.y+body.height/2)
