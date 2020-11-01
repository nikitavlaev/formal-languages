
import pygraphblas as pgb
from context_free_algos.cfg import custom_CFG
from utils import graph_utils as utils
from graph.graph import Graph


def cfpq(edges, gram):
    n = 0
    for edge in edges:
        n = max(n, edge[0], edge[2])

    i = 0
    gram_edges = set()
    starts = []
    ends = []
    eps_nterms = set()
    heads = {}
    for prod in gram.productions:
        if len(prod.body) > 0:
            starts.append(i)
            for var in prod.body:
                gram_edges.add((i, var.value, i + 1))
                i += 1
            ends.append(i)
            i += 1
            heads[(starts[-1], ends[-1])] = prod.head
        else:
            eps_nterms.add(prod.head)

    gram_graph = Graph(
        i+1,
        edges=gram_edges,
        start_states=starts,
        final_states=ends,
    )

    for nterm in eps_nterms:
        for i in range(n + 1):
            edges.append((i, nterm.value, i))

    graph = Graph(
        n+1,
        edges=edges,
    )

    changed = True
    while changed:
        changed = False
        intersection = gram_graph.intersection(graph)
        squashed_bool_ms = utils.squash_bool_ms(intersection.bool_ms)
        closure = utils.transitive_closure(squashed_bool_ms, 1)
        for i, j, _ in closure:
            i_outer, i_inner = utils.num_to_coord(i, graph.size)
            j_outer, j_inner = utils.num_to_coord(j, graph.size)
            if i_outer in starts and j_outer in ends:
                nterm = heads[(i_outer, j_outer)]
                if nterm not in graph.bool_ms:
                    graph.bool_ms[nterm] = pgb.Matrix.sparse(pgb.BOOL, n + 1, n + 1)
                old_nvals = graph.bool_ms[nterm].nvals
                graph.bool_ms[nterm][(i_inner, j_inner)] = 1
                changed = changed or graph.bool_ms[nterm].nvals > old_nvals
    return graph.bool_ms[gram.start_symbol.value]


def run_cfpq_from_file(edges_file_name, gram_file_name):
    gram = custom_CFG.read_cfg(open(gram_file_name, 'r').read())
    print(gram.to_text())
    edges = utils.read_edges(edges_file_name)

    raw_res = cfpq(edges, gram)

    print(raw_res.to_string())

    res = set()
    for (vs, ve, _) in zip(*raw_res.to_lists()):
        res.add((vs, ve))
    print(res)
    return res


# if __name__ == "__main__":
#     print(run_cfpq_from_file(
#         "context_free_algos/tests/test_data/test4/test_g.txt",
#         "context_free_algos/tests/test_data/test4/test_gram.txt",
#         ))
