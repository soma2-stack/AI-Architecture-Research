"""Capacity-limited item bag and deterministic pickup/use actions."""
from __future__ import annotations

from dataclasses import dataclass, field

from .model import Actor, Event, Item, World


@dataclass
class Bag:
    capacity: int = 6
    items: list[Item] = field(default_factory=list)

    def __post_init__(self):
        if self.capacity < 1:
            raise ValueError("invalid capacity")

    def has_space(self) -> bool:
        return len(self.items) < self.capacity

    def add(self, item: Item):
        if not self.has_space():
            raise ValueError("bag full")
        self.items.append(item)

    def remove(self, item_id: str) -> Item:
        for index, item in enumerate(self.items):
            if item.item_id == item_id:
                return self.items.pop(index)
        raise KeyError(item_id)

    def kinds(self) -> list[str]:
        return [item.kind for item in self.items]

    def find(self, kind: str) -> Item | None:
        return next((item for item in self.items if item.kind == kind), None)


def pickup(world: World, actor: Actor, bag: Bag) -> Item | None:
    stack = world.items.get(actor.pos, [])
    if not stack or not bag.has_space():
        return None
    item = stack.pop(0)
    bag.add(item)
    if not stack:
        world.items.pop(actor.pos, None)
    world.events.append(Event("pickup", actor.actor_id, detail=item.item_id))
    return item


def use(world: World, actor: Actor, bag: Bag, item_id: str) -> int:
    item = bag.remove(item_id)
    if item.kind != "potion":
        bag.add(item)
        raise ValueError("item is not usable")
    healed = actor.heal(item.power)
    world.events.append(Event("heal", actor.actor_id, amount=healed))
    return healed
