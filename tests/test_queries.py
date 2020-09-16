from src import algo
from src.graph import Graph
from src.regexp import Regexp
from pathlib import Path
from pyformlang.finite_automaton import \
    NondeterministicFiniteAutomaton, \
    Symbol, \
    State


class TestQueries:
    tests_folder = "test_data"

    symb_a = Symbol("a")
    symb_b = Symbol("b")
    symb_c = Symbol("c")
    symb_d = Symbol("d")

    def run_test(
        self,
        num,
        ndfa=None,
        starts_spec=False,
        ends_spec=False,
        ans_spec=False,
    ):
        current_test_path = Path(
            Path(__file__).parent,
            self.tests_folder,
            f'test{num}',
        )

        starts = None
        ends = None
        if starts_spec:
            starts_file = Path(current_test_path, f'starts{num}.txt')
            starts = list(map(int, open(starts_file).readline().split()))
        if ends_spec:
            ends_file = Path(current_test_path, f'ends{num}.txt')
            ends = list(map(int, open(ends_file).readline().split()))

        graph = Graph.from_txt(
            Path(current_test_path, f'graph{num}.txt'),
            starts,
            ends,
        )
        regexp = Regexp.from_txt(
            Path(current_test_path, f'regexp{num}.txt'),
        )
        intersection, reachable = algo.algo(graph, regexp)

        if ans_spec:
            with open(Path(current_test_path, f'ans{num}.txt'), 'r') as f_ans:
                for line in f_ans.readlines():
                    vs, ve = map(int, line.split())
                    assert (vs, ve) in reachable

        if ndfa is not None:
            print(intersection.fa.to_dict(), intersection.fa.start_states)
            print(ndfa.to_dict(), ndfa.start_states)
            assert intersection.fa.is_equivalent_to(ndfa)

    def test_1(self):
        ndfa = NondeterministicFiniteAutomaton()

        state0 = State(0)
        state1 = State(1)

        ndfa.add_start_state(state0)
        ndfa.add_start_state(state1)
        ndfa.add_final_state(state1)
        ndfa.add_final_state(state0)

        ndfa.add_transition(state0, self.symb_a, state1)

        self.run_test(1, ndfa=ndfa, ans_spec=True)

    def test_2(self):
        ndfa = NondeterministicFiniteAutomaton()

        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)

        ndfa.add_start_state(state0)

        ndfa.add_final_state(state2)
        ndfa.add_final_state(state3)

        ndfa.add_transition(state0, self.symb_a, state1)
        ndfa.add_transition(state1, self.symb_b, state2)
        ndfa.add_transition(state1, self.symb_c, state3)

        self.run_test(2, ndfa=ndfa, starts_spec=True, ans_spec=True)

    def test_3(self):
        ndfa = NondeterministicFiniteAutomaton()

        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)

        ndfa.add_start_state(state0)

        ndfa.add_final_state(state2)
        ndfa.add_final_state(state3)

        ndfa.add_transition(state0, self.symb_b, state1)
        ndfa.add_transition(state1, self.symb_a, state2)
        ndfa.add_transition(state2, self.symb_a, state3)

        self.run_test(
            3,
            ndfa=ndfa,
            starts_spec=True,
            ends_spec=True,
            ans_spec=True,
        )
