# from src.db_languageListener import db_languageListener
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from query_lang.antlr_grammar.antlr_grammarLexer import antlr_grammarLexer
from query_lang.antlr_grammar.antlr_grammarParser import antlr_grammarParser
from query_lang.tree import TreeTraverser


class ANTLRGrammar:

    @staticmethod
    def __parse(path):
        stream = FileStream(path)
        lexer = antlr_grammarLexer(stream)
        token_stream = CommonTokenStream(lexer)
        parser = antlr_grammarParser(token_stream)
        parser.addErrorListener(AlarmingErrorListener())
        try:
            return parser.script()
        except Exception:
            return False

    @staticmethod
    def check(path):
        return ANTLRGrammar.__parse(path) is not None

    @staticmethod
    def generate_dot_tree(path):
        tree = ANTLRGrammar.__parse(path)
        traverser = TreeTraverser(antlr_grammarParser)
        traverser.traverse(tree)

        with open(path, 'w+') as dot_tree:
            dot_tree.write('digraph script {\n')
            for (index, label) in traverser.nodes:
                raw_label = '\\' + label if label == '\"' else label
                dot_tree.write(f'\t{index} [label="{raw_label}"];\n')
            dot_tree.write('\n')
            for (node_from, node_to) in traverser.edges:
                dot_tree.write(f'\t{node_from} -> {node_to};\n')
            dot_tree.write('}')


class AlarmingErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise Exception

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        raise Exception

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        raise Exception

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        raise Exception
