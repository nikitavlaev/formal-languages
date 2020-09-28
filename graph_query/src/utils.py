def transitive_closure(m, algo_num):
    res = m.dup()
    changed = True
    while changed:
        changed = False
        old_not_nulls = res.nvals
        if algo_num == 1:
            res += res @ res
        else:
            res += res @ m
        new_not_nulls = res.nvals
        if new_not_nulls != old_not_nulls:
            changed = True

    return res


def num_to_coord(num, row_size):
    return num // row_size, num % row_size


def bool_ms_to_edges(bool_ms):
    edges = []
    for label, m in bool_ms.items():
        for i, j, value in m:
            edges.append((i, label, j))
    return edges, list(bool_ms.values())[0].nrows


def squash_bool_ms(bool_ms):
    bool_ms = list(bool_ms.values())
    res = bool_ms[0]
    for other in bool_ms[1:]:
        res = res + other
    return res
