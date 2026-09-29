"""Rectangle helpers; starter contact treats touching edges as collision."""
from dataclasses import dataclass
from .model import Vec2

@dataclass(frozen=True)
class Rect:
    left:float
    top:float
    right:float
    bottom:float
    def __post_init__(self):
        if self.right<self.left or self.bottom<self.top: raise ValueError("inverted rectangle")
    @property
    def width(self): return self.right-self.left
    @property
    def height(self): return self.bottom-self.top
    @property
    def area(self): return self.width*self.height
    def moved(self,delta:Vec2): return Rect(self.left+delta.x,self.top+delta.y,self.right+delta.x,self.bottom+delta.y)
    def contains(self,point): return self.left<=point.x<=self.right and self.top<=point.y<=self.bottom

def overlap(a:Rect,b:Rect):
    return a.left<=b.right and a.right>=b.left and a.top<=b.bottom and a.bottom>=b.top

def intersection(a:Rect,b:Rect):
    left=max(a.left,b.left); top=max(a.top,b.top); right=min(a.right,b.right); bottom=min(a.bottom,b.bottom)
    return Rect(left,top,right,bottom) if right>=left and bottom>=top else None

def union(a:Rect,b:Rect): return Rect(min(a.left,b.left),min(a.top,b.top),max(a.right,b.right),max(a.bottom,b.bottom))
def from_body(body): return Rect(*body.bounds())
def distance(a:Vec2,b:Vec2): return ((a.x-b.x)**2+(a.y-b.y)**2)**0.5
