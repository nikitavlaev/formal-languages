from itertools import starmap


def read_edges(edges_file_name):
    with open(edges_file_name, 'r') as g_f:
        edges_map = map(lambda line: line.split(), g_f.readlines())
        edges = list(starmap(lambda vs, l, ve: (int(vs), l, int(ve)), edges_map))
    return edges
