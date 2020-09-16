from . import utils
from .graph import Graph


def algo(graph, regexp):
    intersection_bool_ms = graph.intersect(regexp)
    intersection_squashed = utils.squash_bool_ms(intersection_bool_ms)
    res = utils.transitive_closure(intersection_squashed)
    start_states, final_states = graph.intersect_starts_and_finals(regexp)
    size = regexp.size

    reachable = []
    for i, j, val in res:
        i_outer, i_inner = utils.num_to_coord(i, size)
        j_outer, j_inner = utils.num_to_coord(j, size)
        if i in start_states and j in final_states:
            reachable.append((i_outer, j_outer))

    edges, inter_size = utils.bool_ms_to_edges(intersection_bool_ms)
    intersection = Graph(
        edges,
        inter_size,
        start_states=start_states,
        final_states=final_states,
    )
    return intersection, reachable
