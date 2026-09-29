Entity identifiers must increase monotonically for the lifetime of
each World and must never be reused after removal. Keep identifier allocation
world-local. Add a static guard against reintroducing a free-list allocator.
