from pyformlang.finite_automaton import \
    DeterministicFiniteAutomaton, \
    NondeterministicFiniteAutomaton
from utils import graph_utils as utils
from cached_property import cached_property


class SimpleGraph():
    fa = None

    def __init__(
        self,
        size,
        edges=None,
        bool_ms=None,
        start_states=None,
        final_states=None,
    ):
        self.size = size
        self._bool_ms = bool_ms
        self._edges = edges
        self.start_states = start_states
        self.final_states = final_states
        assert bool_ms or edges

    @cached_property
    def bool_ms(self):
        return self._bool_ms or utils.edges_to_bool_ms(self.edges, self.size)

    @cached_property
    def edges(self):
        return self._edges or utils.bool_ms_to_edges(self.bool_ms)

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

    def intersect_bool_ms(self, other):
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

    def intersection(self, other, closure_algo=1):
        print("Intersecting graphs...")
        intersection_bool_ms = self.intersect_bool_ms(other)
        size = list(intersection_bool_ms.values())[0].nrows
        print("Starts and finals...")
        start_states, final_states = self.intersect_starts_and_finals(other)
        return SimpleGraph(
            size,
            bool_ms=intersection_bool_ms,
            start_states=start_states,
            final_states=final_states,
        )
