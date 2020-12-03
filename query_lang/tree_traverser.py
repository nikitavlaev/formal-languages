from antlr4.tree.Trees import Trees

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