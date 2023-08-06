import cython

ctypedef fused anyarray:
    short[:]
    int[:]
    long[:]
    object[:]
    object


cpdef bint is_subsequence(anyarray subseq, anyarray seq)
