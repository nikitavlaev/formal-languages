import pygraphblas as pgb
from itertools import starmap


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


def edges_to_bool_ms(edges, size):
    label_edges = {}
    for vs, label, ve in edges:
        if label in label_edges.keys():
            label_edges[label]['starts'].append(vs)
            label_edges[label]['ends'].append(ve)
        else:
            label_edges[label] = {}
            label_edges[label]['starts'] = [vs]
            label_edges[label]['ends'] = [ve]
    bool_ms = {}
    for label, edge in label_edges.items():
        bool_ms[label] = pgb.Matrix.from_lists(
            edge['starts'],
            edge['ends'],
            [1 for i in range(len(edge['starts']))],
            nrows=size,
            ncols=size,
        )
    return bool_ms


def bool_ms_to_edges(bool_ms):
    edges = []
    for label, m in bool_ms.items():
        for i, j, _ in m:
            edges.append((i, label, j))
    return edges, list(bool_ms.values())[0].nrows


def squash_bool_ms(bool_ms):
    bool_ms = list(bool_ms.values())
    res = bool_ms[0]
    for other in bool_ms[1:]:
        res = res + other
    return res


def read_edges(edges_file_name):
    with open(edges_file_name, 'r') as g_f:
        edges_map = map(lambda line: line.split(), g_f.readlines())
        edges = list(starmap(lambda vs, l, ve: (int(vs), l, int(ve)), edges_map))
    return edges
