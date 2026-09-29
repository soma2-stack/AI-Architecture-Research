"""Combat and status rules. The death event is emitted exactly once."""
from __future__ import annotations

from .model import Actor, Event, World
from .rng import Dice


def strike(world: World, attacker: Actor, defender: Actor, dice: Dice) -> int:
    if not attacker.alive or not defender.alive:
        return 0
    if attacker.pos.manhattan(defender.pos) != 1:
        raise ValueError("target not adjacent")
    amount = attacker.attack + dice.randint(0, 1)
    dealt = defender.receive(amount)
    world.events.append(Event("hit", attacker.actor_id, defender.actor_id, dealt))
    if not defender.alive:
        world.events.append(Event("death", defender.actor_id, attacker.actor_id))
    return dealt


def apply_status(world: World, actor: Actor, name: str, duration: int):
    if name not in {"poison", "slow"}:
        raise ValueError("unsupported status")
    if duration < 1:
        raise ValueError("status duration must be positive")
    actor.statuses[name] = max(actor.statuses.get(name, 0), duration)
    world.events.append(Event("status", actor.actor_id, detail=name))


def tick_status(world: World, actor: Actor):
    if not actor.alive:
        return
    for name in list(actor.statuses):
        if name == "poison":
            damage = actor.receive(1)
            world.events.append(Event("poison_tick", actor.actor_id, amount=damage))
            if not actor.alive:
                world.events.append(Event("death", actor.actor_id))
        actor.statuses[name] -= 1
        if actor.statuses[name] <= 0:
            del actor.statuses[name]


def can_act(actor: Actor) -> bool:
    return actor.alive and actor.statuses.get("slow", 0) == 0
