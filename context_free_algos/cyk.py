from context_free_algos.cfg import custom_CFG


def CYK(gram, w):
    n = len(w)
    if n == 0:
        return gram.is_eps_reachable

    r = len(gram.variables)
    var_nums = {}
    for i, var in enumerate(gram.variables):
        var_nums[var] = i

    P = [[[False for i in range(r)] for j in range(n)] for k in range(n + 1)]

    for prod in gram.productions:
        for s in range(n):
            if len(prod.body) == 1 and prod.body[0].value == w[s]:
                v = var_nums[prod.head]
                P[1][s][v] = True

    for l in range(2, n + 1):
        for s in range(n - l + 1):
            for p in range(1, l):
                for prod in gram.productions:
                    if len(prod.body) > 1:
                        a = var_nums[prod.head]
                        b = var_nums[prod.body[0]]
                        c = var_nums[prod.body[1]]
                        if P[p][s][b] and P[l - p][s + p][c]:
                            P[l][s][a] = True

    return P[n][0][var_nums[gram.start_symbol]]


def run_cyk_from_file(gram_file_name, w_file_name):
    gram = custom_CFG.read_cfg(open(gram_file_name, 'r').read())
    gram = gram.to_normal_form()

    res = []
    with open(w_file_name, 'r') as w_f:
        for w in w_f.readlines():
            res.append(CYK(gram, w.strip()))
    return res
