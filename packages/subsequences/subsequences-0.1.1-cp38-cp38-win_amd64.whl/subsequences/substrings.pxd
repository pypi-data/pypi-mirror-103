import cython

ctypedef fused anyarray:
    short[:]
    int[:]
    long[:]
    object[:]
    object


cpdef bint is_substring(anyarray subseq, anyarray seq)
