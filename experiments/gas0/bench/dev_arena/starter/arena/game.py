"""Headless arena orchestration and turn resolution."""
from __future__ import annotations

from . import ai
from .combat import strike, tick_status
from .inventory import Bag, pickup, use
from .mapgen import generate
from .model import Actor, Event, Item, Point, World
from .rng import Dice


class Arena:
    def __init__(self, seed: int, world: World | None = None):
        self.seed = seed
        self.dice = Dice(seed)
        self.world = world or generate(seed)
        self.bags: dict[str, Bag] = {}

    def add_player(self, actor_id="hero", pos=Point(1, 1)):
        actor = Actor(actor_id, pos, 10, 10, 2, "player", "@")
        self.world.add_actor(actor)
        self.bags[actor_id] = Bag()
        return actor

    def add_enemy(self, actor_id: str, pos: Point, hp=4, attack=1):
        actor = Actor(actor_id, pos, hp, hp, attack, "enemy", "e")
        self.world.add_actor(actor)
        return actor

    def player_move(self, actor_id: str, dx: int, dy: int):
        if abs(dx) + abs(dy) != 1:
            raise ValueError("one cardinal step required")
        actor = self.world.actors[actor_id]
        destination = actor.pos.shift(dx, dy)
        if not self.world.walkable(destination):
            self.world.events.append(Event("bump_wall", actor_id))
            return False
        target = self.world.actor_at(destination)
        if target:
            if target.faction != actor.faction:
                strike(self.world, actor, target, self.dice)
                return True
            self.world.events.append(Event("bump_actor", actor_id, target.actor_id))
            return False
        actor.move_to(destination)
        self.world.events.append(Event("move", actor_id))
        return True

    def player_pickup(self, actor_id: str):
        return pickup(self.world, self.world.actors[actor_id], self.bags[actor_id])

    def player_use(self, actor_id: str, item_id: str):
        return use(self.world, self.world.actors[actor_id], self.bags[actor_id], item_id)

    def enemy_turn(self):
        for actor in sorted(self.world.actors.values(), key=lambda a: a.actor_id):
            if actor.faction != "enemy" or not actor.alive:
                continue
            action, target = ai.choose_action(self.world, actor)
            if action == "attack":
                strike(self.world, actor, self.world.actors[target], self.dice)
            elif action == "move":
                actor.move_to(target)
                self.world.events.append(Event("move", actor.actor_id))

    def tick(self):
        for actor in self.world.actors.values():
            tick_status(self.world, actor)
        self.enemy_turn()
        self.world.turn += 1

    def place_potion(self, item_id: str, pos: Point, power=3):
        self.world.add_item(pos, Item(item_id, "potion", power))

    def events_since(self, index: int):
        return list(self.world.events[index:])
