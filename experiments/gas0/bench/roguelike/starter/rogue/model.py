"""Typed world values. Coordinates are integer grid locations."""
from __future__ import annotations
from dataclasses import dataclass, field
from .errors import InvalidAction

@dataclass(frozen=True,order=True)
class Point:
    x:int
    y:int
    def moved(self,dx,dy): return Point(self.x+int(dx),self.y+int(dy))
    def manhattan(self,other): return abs(self.x-other.x)+abs(self.y-other.y)

@dataclass
class Actor:
    actor_id:str
    name:str
    position:Point
    hp:int
    max_hp:int
    def __post_init__(self):
        if not self.actor_id or not self.name: raise ValueError("actor id and name required")
        if self.max_hp<=0 or not 0<=self.hp<=self.max_hp: raise ValueError("invalid health")
    @property
    def alive(self): return self.hp>0
    def heal(self,amount):
        if amount<0: raise ValueError("healing cannot be negative")
        before=self.hp; self.hp=min(self.max_hp,self.hp+int(amount)); return self.hp-before
    def take_damage(self,amount):
        if amount<0: raise ValueError("damage cannot be negative")
        before=self.hp; self.hp=max(0,self.hp-int(amount)); return before-self.hp

@dataclass
class Player(Actor):
    inventory:list["Item"]=field(default_factory=list)
    level:int=1
    experience:int=0
    def add_experience(self,amount):
        if amount<0: raise ValueError("experience cannot be negative")
        self.experience+=int(amount)
        while self.experience>=self.level*10:
            self.experience-=self.level*10; self.level+=1; self.max_hp+=2; self.hp=min(self.max_hp,self.hp+2)
        return self.level
    def place(self,position): self.position=position
    def require_alive(self):
        if not self.alive: raise InvalidAction("dead player cannot act")

@dataclass
class Enemy(Actor):
    damage:int=1
    reward:int=1
    def __post_init__(self):
        super().__post_init__()
        if self.damage<0 or self.reward<0: raise ValueError("invalid enemy stats")

@dataclass(frozen=True)
class Item:
    item_id:str
    kind:str
    power:int=0
    def __post_init__(self):
        if not self.item_id or self.kind not in {"potion","key","weapon"}: raise ValueError("invalid item")
        if self.power<0: raise ValueError("item power cannot be negative")

def actor_at(actors,position): return next((a for a in actors if a.position==position and a.alive),None)
def living(actors): return [actor for actor in actors if actor.alive]
def stable_actor_ids(actors): return tuple(sorted(actor.actor_id for actor in actors))
