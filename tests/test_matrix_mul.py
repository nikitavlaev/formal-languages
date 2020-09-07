import pygraphblas as pgb 


def test_matrix_mul():
    A = pgb.Matrix.from_lists(
        [0, 0, 1, 3, 3, 4, 1, 5],
        [1, 3, 2, 4, 5, 2, 5, 4],
        [9, 3, 8, 6, 1, 4, 7, 2],
        )

    B = pgb.Matrix.from_lists(
        [0, 0, 1, 3, 3, 4, 1, 5],
        [2, 3, 3, 2, 5, 4, 5, 4],
        [9, 3, 8, 6, 2, 4, 5, 2],
        )

    C = pgb.Matrix.from_lists(
        [0, 0, 0, 1, 1, 1, 3, 3, 3, 4, 4, 5], 
        [1, 2, 3, 2, 3, 5, 2, 4, 5, 2, 4, 4], 
        [9, 9, 9, 8, 8, 35, 6, 6, 2, 4, 4, 4],
        )

    assert(C.iseq(A * B))
