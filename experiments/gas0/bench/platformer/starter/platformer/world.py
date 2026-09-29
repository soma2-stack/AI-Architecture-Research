"""Headless level state and frame update orchestration."""
from dataclasses import dataclass,field
from .model import Player,Waypoint,Vec2
from .physics import step_body
from .collision import resolve_landing,carry_body

@dataclass
class World:
    player:Player
    platforms:list
    tick_count:int=0
    coins:set=field(default_factory=set)
    route:list[Waypoint]=field(default_factory=list)
    def __post_init__(self): self.platforms=sorted(self.platforms,key=lambda p:p.platform_id)
    def score(self,amount): return self.player.award(amount)
    def state(self):
        return {"tick":self.tick_count,"x":self.player.position.x,"y":self.player.position.y,
                "vx":self.player.velocity.x,"vy":self.player.velocity.y,"grounded":self.player.on_ground,
                "score":self.player.score,"lives":self.player.lives}

def first_waypoint(route): return route[0]

def tick(world,dt=1/60):
    world.tick_count+=1; previous_bottom=world.player.position.y+world.player.height
    step_body(world.player,dt)
    for platform in world.platforms:
        if resolve_landing(world.player,platform,previous_bottom): break
    return world.state()

def carry_on_platform(player,previous,current):
    if player.on_ground: return carry_body(player,previous,current)
    return Vec2(0,0)

def remove_coin(world,coin_id):
    if coin_id not in world.coins: return False
    world.coins.remove(coin_id); world.player.award(1); return True

def tick_many(world,count,dt=1/60):
    if count<0: raise ValueError("count cannot be negative")
    return [tick(world,dt) for _ in range(int(count))]

def goal_reached(world,goal_rect):
    from .geometry import Rect,overlap,from_body
    return overlap(from_body(world.player),goal_rect)

def platform_by_id(world,platform_id):
    return next((item for item in world.platforms if item.platform_id==platform_id),None)

def remove_platform(world,platform_id):
    platform=platform_by_id(world,platform_id)
    if platform is None: return False
    world.platforms.remove(platform); return True

def restart_at_checkpoint(world,checkpoint):
    from .checkpoint import respawn
    respawn(world.player,checkpoint); world.tick_count=0
    return world.state()

def award_goal(world,goal_id,points):
    if goal_id in world.coins: return False
    world.coins.add(goal_id); world.player.award(points); return True

def world_bounds(world):
    if not world.platforms: return (0.0,0.0,0.0,0.0)
    left=min(p.rect[0] for p in world.platforms); top=min(p.rect[1] for p in world.platforms)
    right=max(p.rect[2] for p in world.platforms); bottom=max(p.rect[3] for p in world.platforms)
    return (left,top,right,bottom)

def route_distance(route):
    return sum(abs(a.x-b.x)+abs(a.y-b.y) for a,b in zip(route,route[1:]))

def route_complete(route,index): return index>=len(route)
