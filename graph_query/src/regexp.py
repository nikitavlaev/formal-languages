from src.simple_graph import SimpleGraph
from pyformlang.regular_expression import Regex


class Regexp(SimpleGraph):
    def __init__(self, size, edges, fa, states_map=None):
        super(Regexp, self).__init__(
            size,
            edges=edges,
            start_states=set([fa.start_state]),
            final_states=fa._final_states,
        )
        self.fa = fa
        self.states_map = states_map

    @staticmethod
    def from_str(st, py=True):
        if py:
            e_dfa = Regex.from_python_regex(st).to_epsilon_nfa()
        else:
            e_dfa = Regex(st).to_epsilon_nfa()
        dfa = e_dfa.to_deterministic().minimize()

        dfa, states_map = SimpleGraph.dfa_normalize_states(dfa)
        edges = []
        size = 0
        for vs, labels in dfa.to_dict().items():
            for label, ve in labels.items():
                vs, ve = int(str(vs)), int(str(ve))
                label = str(label)
                size = max(size, vs, ve)
                edges.append((vs, label, ve))
        return Regexp(size + 1, edges, dfa, states_map)

    @staticmethod
    def from_txt(filename, py=True):
        with open(filename, 'r') as f:
            return Regexp.from_str(f.readline(), py)
