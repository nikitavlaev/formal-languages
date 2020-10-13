from src.simple_graph import SimpleGraph


class Graph(SimpleGraph):

    def __init__(
        self,
        size,
        edges=[],
        bool_ms={},
        start_states=None,
        final_states=None,
    ):
        super(Graph, self).__init__(
            size,
            edges=edges,
            bool_ms=bool_ms,
            start_states=start_states,
            final_states=final_states,
        )

    @property
    def fa(self):
        return self.get_fa(self.start_states, self.final_states)

    @staticmethod
    def from_txt(filename, start_states=None, final_states=None):
        edges = []
        size = 0
        with open(filename, 'r') as f:
            for line in f.readlines():
                vs, label, ve = line.split()
                vs, ve = int(vs), int(ve)
                size = max(size, vs, ve)
                edges.append((vs, label, ve))
        return Graph(
            size + 1,
            edges=edges,
            start_states=start_states,
            final_states=final_states,
        )
