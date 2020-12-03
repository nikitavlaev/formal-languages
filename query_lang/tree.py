from argparse import ArgumentParser
from antlr4.tree.Trees import Trees
from query_lang.parsing import ANTLRGrammar

class TreeTraverser():
    def __init__(self, parser):
        self.parser = parser
        self.cnt = 0
        self.stack = [0]
        self.edges = []
        self.nodes = []

    def traverse(self, tree):
        parent_label = Trees.getNodeText(tree, self.parser.ruleNames)
        self.nodes.append((self.stack[-1], parent_label))
        for child in Trees.getChildren(tree):
            self.cnt += 1
            self.edges.append((self.stack[-1], self.cnt))
            self.stack.append(self.cnt)
            self.traverse(child)
            self.stack.pop()

def print_tree():
    parser = ArgumentParser(
        description="""Generate DOT file with parse tree of given script"""
    )
    parser.add_argument(
        'script',
        help='Path to script written in DB language'
    )
    parser.add_argument(
        'dot_file',
        help='Path to save generated DOT file'
    )

    args = parser.parse_args()
    ANTLRGrammar(args.script).generate_dot_tree(args.dot_file)


if __name__ == "__main__":
    print_tree()