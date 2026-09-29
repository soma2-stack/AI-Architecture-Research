"""In-memory checkpoint snapshot values; disk integration is added later."""
from dataclasses import dataclass
from .model import Vec2

@dataclass(frozen=True)
class Checkpoint:
    checkpoint_id:str
    position:Vec2
    score:int=0

def capture(player,checkpoint_id): return Checkpoint(checkpoint_id,player.position,player.score)
def respawn(player,checkpoint):
    player.position=checkpoint.position; player.velocity=Vec2(0,0); player.on_ground=False
    player.lives=max(1,player.lives); player.score=checkpoint.score
    return player.position

def checkpoint_reached(player,checkpoint_rect):
    from .geometry import Rect,overlap,from_body
    return overlap(from_body(player),checkpoint_rect)

def choose_checkpoint(checkpoints): return max(checkpoints,key=lambda c:c.checkpoint_id) if checkpoints else None
def checkpoint_payload(checkpoint): return {"id":checkpoint.checkpoint_id,"position":[checkpoint.position.x,checkpoint.position.y],"score":checkpoint.score}

class CheckpointManager:
    """Track unlocked checkpoints and choose the most recently activated one."""
    def __init__(self): self._by_id={}; self.active_id=None
    def unlock(self,checkpoint):
        self._by_id[checkpoint.checkpoint_id]=checkpoint
        if self.active_id is None: self.active_id=checkpoint.checkpoint_id
        return checkpoint
    def activate(self,checkpoint_id):
        if checkpoint_id not in self._by_id: raise KeyError(checkpoint_id)
        self.active_id=checkpoint_id; return self._by_id[checkpoint_id]
    def active(self): return self._by_id.get(self.active_id)
    def ids(self): return tuple(sorted(self._by_id))
    def payload(self):
        return {"active":self.active_id,"checkpoints":[checkpoint_payload(c) for c in
                sorted(self._by_id.values(),key=lambda item:item.checkpoint_id)]}
    @classmethod
    def from_payload(cls,data):
        manager=cls()
        for row in data.get("checkpoints",[]):
            manager.unlock(Checkpoint(row["id"],Vec2(*row["position"]),row.get("score",0)))
        if data.get("active") is not None: manager.activate(data["active"])
        return manager

def activate_if_reached(manager,player,checkpoint,rect):
    if not checkpoint_reached(player,rect): return False
    manager.unlock(checkpoint); manager.activate(checkpoint.checkpoint_id)
    return True

def respawn_active(player,manager):
    checkpoint=manager.active()
    if checkpoint is None: return False
    respawn(player,checkpoint); return True
