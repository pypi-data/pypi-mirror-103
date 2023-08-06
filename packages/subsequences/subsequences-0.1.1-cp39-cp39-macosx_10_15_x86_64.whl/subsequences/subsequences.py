import cython  # type: ignore


@cython.infer_types(True)
@cython.boundscheck(False)  # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def is_subsequence(subseq, seq):
    """Check if `subseq` is a subsequence of `seq`."""
    n = len(seq)
    m = len(subseq)

    if m > n:
        return False

    i = 0  # index of seq
    j = 0  # index of subseq

    while i < n and j < m:
        if seq[i] == subseq[j]:
            j += 1
        i += 1

    return j == m
