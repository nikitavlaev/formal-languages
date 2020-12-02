from context_free_algos.cfg import custom_CFG
from utils.graph_utils import read_edges
import pygraphblas as pgb


def cfpq(edges, gram):
    n = 0
    for edge in edges:
        n = max(n, edge[0], edge[2])

    eps_productions, term_productions, norm_productions = gram.split_productions

    bool_ms = {}
    for nterm in gram.variables:
        bool_ms[nterm] = pgb.Matrix.sparse(pgb.BOOL, n + 1, n + 1)

    for (vs, l, ve) in edges:
        for prod in term_productions:
            if prod.body[0].value == l:
                bool_ms[prod.head][(vs, ve)] = 1

    for prod in eps_productions:
        for i in range(n + 1):
            bool_ms[prod.head][(i, i)] = 1

    changed = gram.variables
    while changed:
        old_changed = changed
        changed = set()
        for prod in norm_productions:
            if prod.body[0] in old_changed or prod.body[1] in old_changed:
                old_nval = bool_ms[prod.head].nvals
                bool_ms[prod.head] = bool_ms[prod.head] + (bool_ms[prod.body[0]] @ bool_ms[prod.body[1]])
                if (bool_ms[prod.head].nvals != old_nval):
                    changed.add(prod.head)

    return bool_ms[gram.start_symbol]


def run_cfpq_from_file(edges_file_name, gram_file_name):
    gram = custom_CFG.read_cfg(open(gram_file_name, 'r').read())

    gram = gram.to_normal_form()
    print(gram.to_text())
    edges = read_edges(edges_file_name)

    raw_res = cfpq(edges, gram)

    print(raw_res.to_string())

    res = set()
    for (vs, ve, _) in zip(*raw_res.to_lists()):
        res.add((vs, ve))
    print(res)
    return res
