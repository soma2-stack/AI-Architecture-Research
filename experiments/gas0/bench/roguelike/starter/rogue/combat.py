"""Turn-based combat primitives and damage accounting."""
from dataclasses import dataclass
from .model import Actor,Enemy,Player
from .errors import InvalidAction

@dataclass(frozen=True)
class CombatResult:
    source_id:str
    target_id:str
    attempted:int
    applied:int
    defeated:bool

def poison_tick_amount(damage):
    """Central tick calculation so effects and combat use one rule."""
    return max(0,int(damage))

def attack(source:Actor,target:Actor,power=1):
    if not source.alive: raise InvalidAction("dead actor cannot attack")
    if not target.alive: raise InvalidAction("target is already defeated")
    amount=max(0,int(power)); applied=target.take_damage(amount)
    return CombatResult(source.actor_id,target.actor_id,amount,applied,not target.alive)

def enemy_turn(player:Player,enemies):
    total=0
    for enemy in sorted(enemies,key=lambda item:item.actor_id):
        if enemy.alive and enemy.position.manhattan(player.position)<=1:
            total+=player.take_damage(enemy.damage)
    return total

def combat_log(result):
    outcome="defeated" if result.defeated else "hit"
    return f"{result.source_id} {outcome} {result.target_id} for {result.applied}"

def damage_total(results): return sum(result.applied for result in results)
