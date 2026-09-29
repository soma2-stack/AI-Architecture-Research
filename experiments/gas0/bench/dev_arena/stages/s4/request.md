A path request whose start and destination are the same
returns an empty route, so the caller treats an actor already at its destination
as unreachable. Diagnose and fix this edge case without changing wall traversal
or ordinary route selection.
