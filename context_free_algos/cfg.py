from cached_property import cached_property
import string

import pyformlang.cfg as cfg
from pyformlang.regular_expression import Regex

class custom_CFG(cfg.CFG):
    __var_state_counter = 0

    def __init__(self, variables, terminals, start_symbol, productions):
        super().__init__(variables, terminals, start_symbol, productions)

    @classmethod
    def from_CFG(cls, cfg):
        return cls(
            cfg.variables,
            cfg.terminals,
            cfg.start_symbol,
            cfg.productions,
            )

    def to_normal_form(self):
        new = super().to_normal_form()
        if self.is_eps_reachable:
            new.productions.add(
                cfg.Production(self.start_symbol, [])
            )
        return custom_CFG.from_CFG(new)

    @cached_property
    def is_eps_reachable(self):
        reachable = set()
        for prod in self.productions:
            if len(prod.body) == 0:
                reachable.add(prod.head)

        changed = True
        while changed:
            changed = False
            for prod in self.productions:
                if prod.head not in reachable:
                    if prod.body[0] in reachable:
                        if len(prod.body) == 1 or prod.body[1] in reachable:
                            reachable.add(prod.head)
                            changed = True

        return self.start_symbol in reachable

    @classmethod
    def _read_line(cls, line, productions, terminals, variables):
        prod_s = line.split(' ', 1)
        head_s = prod_s[0]
        if len(prod_s) > 1:
            body_s = prod_s[1]
        else:
            body_s = ''
        head = cfg.Variable(head_s.strip())
        variables.add(head)
        body = []
        for body_component in body_s.split():
            if body_component[0] in string.ascii_uppercase:
                body_var = cfg.Variable(body_component)
                variables.add(body_var)
                body.append(body_var)
            else:
                body_ter = cfg.Terminal(body_component)
                terminals.add(body_ter)
                body.append(body_ter)
        productions.add(cfg.Production(head, body))

    @classmethod
    def read_cfg(cls, text, start_symbol=cfg.Variable("S"), contains_regexes=False, track_variables=False):
        variables = set()
        productions = set()
        terminals = set()

        if track_variables:
            for line in text.splitlines():
                head = line.strip().split(' ', 1)[0]
                variables.add(cfg.Variable(head))
        
        for line in text.splitlines():
            if contains_regexes and \
               len(line.split()) > 1 and \
               len(line.strip().split(' ', 1)[1]) > 1 and \
               any(symb in line for symb in ['*', '|', '+', '?', ]):
                raw_head, *raw_body = line.strip().split(' ', 1)
                regex = Regex.from_python_regex(' '.join(raw_body))
                head = cfg.Variable(raw_head)
                cur_cfg = cls._create_cfg_from_regex(head, regex, track_variables)
                terminals.update(cur_cfg.terminals)
                productions.update(cur_cfg.productions)
                variables.update(cur_cfg.variables)
            else:
                line = line.strip()
                if not line:
                    continue
                if track_variables:
                    tmp_vars = set()
                    cls._read_line(line, productions, terminals, tmp_vars)
                else:
                    cls._read_line(line, productions, terminals, variables)
        return cls(variables=variables, terminals=terminals,
                   productions=productions, start_symbol=start_symbol)

    @classmethod
    def _create_cfg_from_regex(cls, head, regex, track_variables):
        dfa = regex.to_epsilon_nfa().to_deterministic().minimize()
        transitions = dfa._transition_function._transitions
        state_to_var = {}
        productions, terminals, variables = set(), set(), set()
        for state in dfa.states:
            state_to_var[state] = cfg.Variable(f'{state}:{cls.__var_state_counter}')
            cls.__var_state_counter += 1
        variables.update(state_to_var.values())
        for start_state in dfa.start_states:
            productions.add(cfg.Production(head, [state_to_var[start_state]]))
        for state_from in transitions:
            for edge_symb in transitions[state_from]:
                state_to = transitions[state_from][edge_symb]
                current_prod_head = state_to_var[state_from]
                current_prod_body = []
                if any(letter.isupper() for letter in edge_symb.value) and not track_variables:
                    var = cfg.Variable(edge_symb.value)
                    variables.add(var)
                    current_prod_body.append(var)
                elif edge_symb.value != 'eps':
                    term = cfg.Terminal(edge_symb.value)
                    terminals.add(term)
                    current_prod_body.append(term)
                current_prod_body.append(state_to_var[state_to])
                productions.add(cfg.Production(current_prod_head, current_prod_body))
                if state_to in dfa.final_states:
                    productions.add(cfg.Production(state_to_var[state_to], []))
        if not productions:
            return cfg.CFG(variables, terminals, head, {cfg.Production(head, [])})
        return cfg.CFG(variables, terminals, head, productions)

    @cached_property
    def split_productions(self):
        term_productions = []
        eps_productions = []
        norm_productions = []
        for prod in self.productions:
            if len(prod.body) == 0:
                eps_productions.append(prod)
            elif len(prod.body) == 1:
                term_productions.append(prod)
            else:
                norm_productions.append(prod)
        return eps_productions, term_productions, norm_productions
