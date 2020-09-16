from src.simple_graph import SimpleGraph


class Graph(SimpleGraph):

    def __init__(self, edges, size, start_states=None, final_states=None):
        super(Graph, self).__init__(edges, size)
        self.fa = self.get_fa(start_states, final_states)

    @staticmethod
    def from_txt(filename, start_states, final_states):
        edges = []
        size = 0
        with open(filename, 'r') as f:
            for line in f.readlines():
                vs, label, ve = line.split()
                vs, ve = int(vs), int(ve)
                size = max(size, vs, ve)
                edges.append((vs, label, ve))
        return Graph(edges, size + 1, start_states, final_states)
