from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import Symbol


class TestAutomata:
    symb_a = Symbol("a")
    symb_b = Symbol("b")
    symb_c = Symbol("c")
    symb_d = Symbol("d")

    def init_dfas(self):
        # DFA that accepts "ab" and "ac"
        self.dfa1 = DeterministicFiniteAutomaton()
        # DFA that accepts "ac" and "ad"
        self.dfa2 = DeterministicFiniteAutomaton()

        state0 = State(0)
        state1 = State(1)
        state2 = State(2)
        state3 = State(3)
        
        # Add a start state
        self.dfa1.add_start_state(state0)
        self.dfa2.add_start_state(state0)

        # Add two final states
        self.dfa1.add_final_state(state2)
        self.dfa1.add_final_state(state3)

        self.dfa2.add_final_state(state2)
        self.dfa2.add_final_state(state3)

        # Create transitions
        self.dfa1.add_transition(state0, self.symb_a, state1)
        self.dfa1.add_transition(state1, self.symb_b, state2)
        self.dfa1.add_transition(state1, self.symb_c, state3)

        self.dfa2.add_transition(state0, self.symb_a, state1)
        self.dfa2.add_transition(state1, self.symb_c, state2)
        self.dfa2.add_transition(state1, self.symb_d, state3)

    def test_dfa1(self):
        self.init_dfas()
        assert(self.dfa1.accepts([self.symb_a, self.symb_b]))
        assert(self.dfa1.accepts([self.symb_a, self.symb_c]))
        assert(not self.dfa1.accepts([self.symb_a, self.symb_d]))

    def test_dfa2(self):
        self.init_dfas()
        assert(not self.dfa2.accepts([self.symb_a, self.symb_b]))
        assert(self.dfa2.accepts([self.symb_a, self.symb_c]))
        assert(self.dfa2.accepts([self.symb_a, self.symb_d]))

    def test_dfa_inter(self):
        self.init_dfas()
        dfa_inter = self.dfa1 & self.dfa2 

        # Intersection result should accept only "ac", but not "ab" or "ad"
        assert(not dfa_inter.accepts([self.symb_a, self.symb_b]))
        assert(dfa_inter.accepts([self.symb_a, self.symb_c]))
        assert(not dfa_inter.accepts([self.symb_a, self.symb_d]))
