"""Campaign progression ledger with idempotent reward events.

An event ID prevents loading a checkpoint twice from double-awarding its
experience. The ledger stores immutable primitive records so it can be copied
or serialized without retaining references to mutable actors.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class RewardEvent:
    event_id:str
    actor_id:str
    amount:int
    source:str

    def __post_init__(self):
        if not self.event_id or not self.actor_id or not self.source:
            raise ValueError("reward event fields are required")
        if self.amount<0: raise ValueError("reward cannot be negative")

class ExperienceLedger:
    def __init__(self,events=None):
        self.events=[]; self._ids=set()
        for event in events or (): self.record(event)
    def record(self,event):
        if event.event_id in self._ids: return False
        self.events.append(event); self._ids.add(event.event_id); return True
    def total(self,actor_id):
        return sum(event.amount for event in self.events if event.actor_id==actor_id)
    def sources(self,actor_id):
        return tuple(event.source for event in self.events if event.actor_id==actor_id)
    def event_count(self,actor_id=None):
        return sum(actor_id is None or event.actor_id==actor_id for event in self.events)
    def payload(self):
        return [{"event_id":e.event_id,"actor_id":e.actor_id,"amount":e.amount,"source":e.source}
                for e in self.events]
    @classmethod
    def from_payload(cls,rows):
        return cls(RewardEvent(**row) for row in rows)
    def copy(self): return ExperienceLedger(self.events)

def level_for_experience(experience):
    amount=max(0,int(experience)); level=1; threshold=10
    while amount>=threshold:
        amount-=threshold; level+=1; threshold=level*10
    return level

def progress_to_next(experience):
    amount=max(0,int(experience)); level=1; threshold=10
    while amount>=threshold:
        amount-=threshold; level+=1; threshold=level*10
    return {"level":level,"into_level":amount,"needed":threshold-amount}

def award_defeat(ledger,enemy,player):
    event=RewardEvent(f"defeat:{enemy.actor_id}:{player.actor_id}",player.actor_id,
                      int(enemy.reward),"enemy_defeat")
    return ledger.record(event)

def campaign_score(turns,defeats,treasure):
    turns=max(0,int(turns)); defeats=max(0,int(defeats)); treasure=max(0,int(treasure))
    return defeats*100+treasure*10-max(0,turns-defeats)

def rank_score(score):
    value=int(score)
    if value>=1000: return "S"
    if value>=500: return "A"
    if value>=100: return "B"
    return "C"

def actor_totals(ledger):
    """Return a stable mapping of actors to accumulated reward."""
    actor_ids=sorted({event.actor_id for event in ledger.events})
    return {actor_id:ledger.total(actor_id) for actor_id in actor_ids}

def top_earners(ledger,limit=3):
    """Rank actors by total reward and break ties by persistent actor ID."""
    totals=actor_totals(ledger)
    ranked=sorted(totals.items(),key=lambda row:(-row[1],row[0]))
    return ranked[:max(0,int(limit))]

def event_ids(ledger):
    """Expose event identity without allowing callers to mutate the ledger."""
    return tuple(event.event_id for event in ledger.events)
