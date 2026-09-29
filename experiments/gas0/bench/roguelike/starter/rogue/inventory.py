"""Inventory operations preserve order and reject duplicate item identities."""
from .errors import InvalidAction
from .model import Item,Player

class Inventory:
    def __init__(self,items=None): self.items=list(items or [])
    def __len__(self): return len(self.items)
    def __iter__(self): return iter(self.items)
    def add(self,item:Item):
        if any(old.item_id==item.item_id for old in self.items): raise ValueError("duplicate item id")
        self.items.append(item); return item
    def find(self,item_id): return next((item for item in self.items if item.item_id==item_id),None)
    def remove(self,item_id):
        item=self.find(item_id)
        if item is None: raise KeyError(item_id)
        self.items.remove(item); return item
    def count_kind(self,kind): return sum(item.kind==kind for item in self.items)
    def item_ids(self): return tuple(item.item_id for item in self.items)

def use_potion(player:Player,item_id):
    item=next((row for row in player.inventory if row.item_id==item_id),None)
    if item is None: raise KeyError(item_id)
    if item.kind!="potion": raise InvalidAction("item is not a potion")
    restored=player.heal(item.power); player.inventory.remove(item)
    return restored

def has_key(player,key_id=None):
    return any(item.kind=="key" and (key_id is None or item.item_id==key_id) for item in player.inventory)

def inventory_weight(items): return sum(1+item.power//5 for item in items)
