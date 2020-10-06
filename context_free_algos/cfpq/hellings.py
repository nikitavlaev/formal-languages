from context_free_algos.cfg import custom_CFG
from context_free_algos.graph_utils import read_edges


def hellings(edges, gram):
    r = set()
    n = 0
    for edge in edges:
        n = max(n, edge[0], edge[2])

    if gram.is_eps_reachable:
        for v in range(n):
            r.add((gram.start_symbol, v, v))

    final_nterms = {}
    for prod in gram.productions:
        if len(prod.body) == 1:
            if prod.body[0].value in final_nterms:
                final_nterms[prod.body[0].value].append(prod.head)
            else:
                final_nterms[prod.body[0].value] = [prod.head]

    for edge in edges:
        if edge[1] in final_nterms:
            for nterm in final_nterms[edge[1]]:
                r.add((nterm, edge[0], edge[2]))

    m = r.copy()

    while len(m) > 0:
        nterm, vs, ve = m.pop()

        for elem in r.copy():
            if elem[2] == vs:
                for prod in gram.productions:
                    new_elem = (prod.head, elem[1], ve)
                    if new_elem not in r and prod.body.__eq__([elem[0], nterm]):
                        m.add(new_elem)
                        r.add(new_elem)

        for elem in r.copy():
            if elem[1] == ve:
                for prod in gram.productions:
                    new_elem = (prod.head, vs, elem[2])
                    if new_elem not in r and prod.body.__eq__([nterm, elem[0]]):
                        m.add(new_elem)
                        r.add(new_elem)
    return r


def run_hellings_from_file(edges_file_name, gram_file_name):
    gram = custom_CFG.read_cfg(open(gram_file_name, 'r').read())

    gram = gram.to_normal_form()
    edges = read_edges(edges_file_name)

    raw_res = hellings(edges, gram)

    res = set()
    for (nterm, vs, ve) in raw_res:
        if nterm == gram.start_symbol:
            res.add((vs, ve))
    return res
