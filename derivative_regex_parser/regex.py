from pyformlang.finite_automaton import Symbol
from pyformlang.regular_expression import Regex as pfl_Regex
from pyformlang.regular_expression.regex_objects import Empty, Epsilon, Operator, Concatenation, KleeneStar, Union

class Regex(pfl_Regex):
    def _nullable(self):
        if str(self.head) == str(Empty()):
            return False
        if str(self.head) == str(Epsilon()):
            return True 
        
        if str(self.head) == str(Concatenation()):
            r1 = Regex(str(self.sons[0]))
            r2 = Regex(str(self.sons[1]))
            return r1._nullable() and r2._nullable()

        if str(self.head) == str(KleeneStar()):
            return True

        if str(self.head) == str(Union()):
            return Regex(str(self.sons[0]))._nullable() or Regex(str(self.sons[1]))._nullable()

        return False

    def _dSymbol(self, c):
        if str(self.head) == str(Empty()):
            return self
        if str(self.head) == str(Epsilon()):
            return Regex(str(Empty()))
        
        if str(self.head) == str(Concatenation()):
                r1 = Regex(str(self.sons[0]))
                r2 = Regex(str(self.sons[1]))
                if r1._nullable():
                    return r1._dSymbol(c).concatenate(r2).union(r2._dSymbol(c))
                else:
                    return r1._dSymbol(c).concatenate(r2)

        if str(self.head) == str(KleeneStar()):
            return Regex(str(self.sons[0]))._dSymbol(c).concatenate(self)

        if str(self.head) == str(Union()):
            return Regex(str(self.sons[0]))._dSymbol(c).union(Regex(str(self.sons[1]))._dSymbol(c))

        if self.head._value == c:
            return Regex(Epsilon()._value)
        else:
            return Regex(str(Empty()))
        assert False

    def d_accepts(self, word):
        if len(word) > 0:
            regex = Regex(str(self._dSymbol(word[0])))
            for c in word[1:]:
                regex = Regex(str(regex._dSymbol(c)))
            return regex._nullable()
        else:
            return self._nullable()
