import argparse

from graph.graph import Graph
from graph.regexp import Regexp
from graph_query.algo import algo


def main():
    parser = argparse.ArgumentParser(
        description=('Script to execute simple query on graph using '
                     'tensor product automata intersection'),
    )
    parser.add_argument(
        "-g", "--graph-file",
        help=('File with graph as edge list. '
              'Format: (vertice, label, vertice)'),
        required=True,
    )
    parser.add_argument(
        "-r", "--regexp-file",
        help=('File with regexp as a query. '
              'e.g. (0 2 (13? 6)*)+  (15 | 14)*)'),
        required=True,
    )
    parser.add_argument(
        "--start-vertices-file",
        help=('File with starting vertices set. '
              'e.g. 0 4 5 8'),
        required=False,
    )
    parser.add_argument(
        "--end-vertices-file",
        help=('File with  vertices set. '
              'e.g. 0 4 5 8'),
        required=False,
    )

    args = parser.parse_args()

    starts = None
    starts_file = args.start_vertices_file
    if starts_file is not None:
        starts = list(map(int, open(starts_file).readline().split()))

    ends = None
    ends_file = args.end_vertices_file
    if ends_file is not None:
        ends = list(map(int, open(ends_file).readline().split()))

    graph = Graph.from_txt(args.graph_file, starts, ends)
    regexp = Regexp.from_txt(args.regexp_file)

    intersection, reachable = algo(graph, regexp)

    labeled_edges = {}
    for label, bool_m in intersection.bool_ms.items():
        labeled_edges[label] = bool_m.nvals

    print("Num of labeled edges:")
    print(labeled_edges)
    print("Pairs of reachable vertices")
    print(reachable)


if __name__ == '__main__':
    main()
