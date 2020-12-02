from pathlib import Path
import os

from pyformlang.cfg import Variable

from context_free_algos.cfg import custom_CFG
from query_lang.run_script import run_script


class TestCYK:
    GRAMMAR_PATH = "query_lang/grammar.txt"


    def test_all(self):
        with open(self.GRAMMAR_PATH, 'r') as f:
            gram = custom_CFG.read_cfg(
                f.read(),
                start_symbol=Variable("SCRIPT"),
                contains_regexes=True,
                track_variables=True,
            )
        gram = gram.to_normal_form()

        script = """
            connect "ABC"
        """
        assert(run_script(script, gram=gram))

        script = """
            select count edges from "g" intersect grammar
        """
        assert(run_script(script, gram=gram))

        script = """
            select count edges from setStartAndFinal {3, 2, 6} 1:6 "g"
        """
        assert(run_script(script, gram=gram))

        script = """
            select count edges from [term(a)?.term(b)*.(term(c)|term(d))+]
        """
        assert(run_script(script, gram=gram))

        script = """
            select count edges from "g" intersect [term(a).term(b)*.(term(c)|term(d))+]
        """
        assert(run_script(script, gram=gram))

        script = """
            select count edges from setStartAndFinal _ _ "g"
        """
        assert(run_script(script, gram=gram))

        script = """
            select count edges from setStartAndFinal _ _ ("g" intersect grammar)
        """
        assert(run_script(script, gram=gram))

        script = """
            select filter (v, e, u) -> (e hasLbl abc) : edges from "g"
        """
        assert(run_script(script, gram=gram))

        script = """
            select filter (v, e, u) -> (e hasLbl abc & isStart v | !(isFinal u)) : edges from "g"
        """
        assert(run_script(script, gram=gram))

        script = """
            select count edges from "g1" intersect ("g2" intersect "g3")
        """
        assert(run_script(script, gram=gram))

        script = """
            s : nonterm(S).term(a).nonterm(S).term(b)
            s : term(eps)
        """
        assert(run_script(script, gram=gram))

        script = """
            select edges from [term(a)?.term(b)*.(term(c)|term(d))+]
        """
        assert(run_script(script, gram=gram))
