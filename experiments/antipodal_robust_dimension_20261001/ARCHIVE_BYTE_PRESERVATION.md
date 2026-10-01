# Raw-byte archive preservation

The first archive commit, 357765a, used Git's existing automatic text newline
normalization. The working evidence and its hashes were unchanged, but text
blobs could differ from the raw bytes referenced by the original manifests.

This follow-up explicitly disables newline conversion for this archive and the
new third-order experiment, and re-stages the current original bytes. It also
stores raw copies of externally referenced frozen dependencies. No original
file, result, failed run or historical manifest is rewritten. The new
BYTE_EXACT_ARCHIVE.json records this complete preservation snapshot; the first
EVIDENCE_ARCHIVE.json remains as its historical predecessor.

The dependency copy map allows raw-byte verification even if a future checkout
normalizes an external source file. The original source-relative hashes remain
unchanged in FROZEN.json. No earlier execution time or preregistration is claimed.
