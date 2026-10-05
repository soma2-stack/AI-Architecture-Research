# Internal audit repairs

Historical accepted sources were not edited. These repairs concern only
new, uncommitted derivations and administration in this folder.

1. The first mathematical check run passed every mathematical assertion,
   then crashed in Windows RAM reporting. See INITIAL_CHECK_FAILURE.txt.
   The missing ctypes HANDLE declaration was added; no inequality changed.

2. The first resume insertion asserted before writing because the notebook
   uses LF around its heading and CRLF elsewhere. Its pre-addition SHA still
   matched the provenance receipt. The insertion now detects the exact
   local heading newline and preserves all original bytes.

3. The new auxiliary legal-spike formula originally omitted a 1/sqrt(k)
   factor on gamma_U. The separate direct Householder check failed at n=200:
   direct .6540188927521463 versus formula .5878821507884462.
   The wrong formula was a*g*(sqrt(k)-gamma_U)/sqrt(n).
   Re-derivation gives (U e_(d-1))_(d-1)=1-gamma_U/k, hence the correct
   a*g*(sqrt(k)-gamma_U/sqrt(k))/sqrt(n). The limit g/sqrt(2) and failure of
   uniform 1/sqrt(n) row leverage are unchanged. This lemma is an upper-side
   obstruction only; no main lower construction, amplitude, margin constant,
   query, test tolerance, or original accepted theorem was changed.
   PROOF.md, REPORT.md and audit.py were corrected before final commit.
