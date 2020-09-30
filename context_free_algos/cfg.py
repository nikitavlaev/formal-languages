import pyformlang.cfg as cfg
from cached_property import cached_property
import string


class custom_CFG(cfg.CFG):

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
    def read_cfg(cls, text, start_symbol=cfg.Variable("S")):
        variables = set()
        productions = set()
        terminals = set()

        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            cls._read_line(line, productions, terminals, variables)
        return cls(variables=variables, terminals=terminals,
                   productions=productions, start_symbol=start_symbol)
