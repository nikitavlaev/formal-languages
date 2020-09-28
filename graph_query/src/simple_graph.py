import pygraphblas as pgb
from pyformlang.finite_automaton import \
    DeterministicFiniteAutomaton, \
    NondeterministicFiniteAutomaton


class SimpleGraph():

    def __init__(self, edges, size):
        self.edges = edges
        self.size = size
        self.bool_ms = self.edges_to_bool_ms()

    def get_fa(self, start_states, final_states):
        fa = NondeterministicFiniteAutomaton()

        fa.add_transitions(self.edges)
        if start_states is None:
            start_states = list(range(self.size))
        for ss in start_states:
            fa.add_start_state(ss)
        if final_states is None:
            final_states = list(range(self.size))
        for fs in final_states:
            fa.add_final_state(fs)
        return fa

    def edges_to_bool_ms(self):
        label_edges = {}
        for vs, label, ve in self.edges:
            if label in label_edges.keys():
                label_edges[label]['starts'].append(vs)
                label_edges[label]['ends'].append(ve)
            else:
                label_edges[label] = {}
                label_edges[label]['starts'] = [vs]
                label_edges[label]['ends'] = [ve]
        bool_ms = {}
        for label, edge in label_edges.items():
            bool_ms[label] = pgb.Matrix.from_lists(
                edge['starts'],
                edge['ends'],
                [1 for i in range(len(edge['starts']))],
                nrows=self.size,
                ncols=self.size,
            )
        return bool_ms

    @staticmethod
    def dfa_normalize_states(dfa):
        res = DeterministicFiniteAutomaton()
        old_states = dfa._states
        states_map = {}
        for i, state in enumerate(old_states):
            states_map[state] = i

        old_transitions = dfa.to_dict()
        for vs, trs in old_transitions.items():
            for label, ve in trs.items():
                res.add_transition(
                    states_map[vs],
                    label,
                    states_map[ve],
                )
        start_states = map(
            lambda state: states_map[state],
            dfa.start_states,
            )
        final_states = map(
            lambda state: states_map[state],
            dfa.final_states,
            )
        for state in start_states:
            res.add_start_state(state)
        for state in final_states:
            res.add_final_state(state)
        return res, states_map

    def intersect(self, other):
        intersection_bool_ms = {}
        for label in self.bool_ms:
            if label in other.bool_ms:
                intersection_bool_ms[label] = self.bool_ms[label].kronecker(
                    other.bool_ms[label],
                )

        return intersection_bool_ms

    def intersect_starts_and_finals(self, other):
        start_states = []

        for state1 in self.fa.start_states:
            for state2 in other.fa.start_states:
                start_states.append(
                    int(str(state1)) * other.size + int(str(state2)),
                )

        final_states = []

        for state1 in self.fa.final_states:
            for state2 in other.fa.final_states:
                final_states.append(
                    int(str(state1)) * other.size + int(str(state2)),
                )

        return start_states, final_states
