Make equal-tick collision event ordering independent of component
table insertion order. Sort by projectile ID and then target entity ID. Decide
that a future piercing projectile may affect multiple targets; defer piercing
until Stage 7.
