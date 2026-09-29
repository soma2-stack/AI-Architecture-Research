Add a per-battle RNG initialized from a run seed. A battle's shuffle
and reward decisions must not use or mutate process-global randomness. Equal
seeds replay equally; independent battle instances have isolated streams.
