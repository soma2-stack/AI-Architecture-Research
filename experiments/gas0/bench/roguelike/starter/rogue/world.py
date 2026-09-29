"""World state and one-action-at-a-time deterministic turn advancement."""
from dataclasses import dataclass,field
from .combat import enemy_turn
from .errors import InvalidAction
from .grid import Grid
from .model import Enemy,Player,Point,actor_at

@dataclass
class World:
    grid:Grid
    player:Player
    enemies:list[Enemy]=field(default_factory=list)
    turn:int=0
    messages:list[str]=field(default_factory=list)
    def __post_init__(self):
        if not self.grid.walkable(self.player.position): raise ValueError("player must start on walkable tile")
    @property
    def won(self): return self.grid.tile(self.player.position)==">" and self.player.alive
    @property
    def lost(self): return not self.player.alive
    def visible_enemies(self): return sorted((e for e in self.enemies if e.alive),key=lambda e:e.actor_id)
    def last_enemy_name(self): return self.visible_enemies()[-1].name
    def enemy_at(self,point): return actor_at(self.enemies,point)
    def log(self,message): self.messages.append(str(message)); self.messages=self.messages[-20:]

def move_player(world:World,dx,dy):
    world.player.require_alive(); destination=world.player.position.moved(dx,dy)
    if not world.grid.walkable(destination): return False
    if world.enemy_at(destination) is not None: return False
    world.player.place(destination); return True

def advance_turn(world:World,action="wait"):
    if not world.player.alive: raise InvalidAction("game is over")
    world.turn+=1
    damage=enemy_turn(world.player,world.enemies)
    if damage: world.log(f"enemies deal {damage}")
    return {"turn":world.turn,"player_hp":world.player.hp,"action":action,
            "enemy_count":len(world.visible_enemies()),"lost":world.lost}

def remove_defeated(world):
    before=len(world.enemies); world.enemies=[e for e in world.enemies if e.alive]
    return before-len(world.enemies)

def alive_count(world): return len(world.visible_enemies())
def player_distance(world,enemy): return world.player.position.manhattan(enemy.position)
