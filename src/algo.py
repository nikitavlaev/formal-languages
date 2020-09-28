from src import utils
from src.graph import Graph


def algo(graph, regexp, closure_algo=1):
    print("Intersecting graphs...")
    intersection_bool_ms = graph.intersect(regexp)
    print("Squashing...")
    intersection_squashed = utils.squash_bool_ms(intersection_bool_ms)
    print("Calculating closure...")
    res = utils.transitive_closure(intersection_squashed, closure_algo)
    print("Starts and finals...")
    start_states, final_states = graph.intersect_starts_and_finals(regexp)
    size = regexp.size

    reachable = []
    
    print("Calculating reachables...")
    for i, j, val in res:
        i_outer, i_inner = utils.num_to_coord(i, size)
        j_outer, j_inner = utils.num_to_coord(j, size)
        if i in start_states and j in final_states:
            reachable.append((i_outer, j_outer))

    print("Creating intersection")
    edges, inter_size = utils.bool_ms_to_edges(intersection_bool_ms)
    intersection = Graph(
        edges,
        inter_size,
        start_states=start_states,
        final_states=final_states,
    )
    return intersection, reachable
