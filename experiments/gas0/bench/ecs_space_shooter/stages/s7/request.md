A projectile may retain collision events for an entity that was
removed earlier in the same update. Make event resolution tolerate stale
references. Implement the deferred piercing behavior for piercing projectiles;
unrelated entities and repeated contacts must not be damaged twice.
