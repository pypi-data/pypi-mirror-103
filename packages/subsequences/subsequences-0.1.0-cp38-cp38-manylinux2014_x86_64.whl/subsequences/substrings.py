import cython  # type: ignore


@cython.infer_types(True)
@cython.boundscheck(False)  # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def is_substring(subseq, seq):
    """Check if `subseq` is a substring of `seq`."""
    n = len(seq)
    m = len(subseq)

    if m > n:
        return False
    j = 0
    for i in range(n):
        if seq[i] == subseq[j]:
            j += 1
            if j == m:
                return True
        else:
            j = 0
            if n - i <= m:
                return False
    return False
