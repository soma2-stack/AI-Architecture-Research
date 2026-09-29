Route each randomized wave attribute through a seed-owned RNG attached
to its Game. Equal seeds replay identically; distinct Game instances must not
share state. Do not import or call module-global random outside td/rng.py.
