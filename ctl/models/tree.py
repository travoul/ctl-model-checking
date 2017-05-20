from tabulate import tabulate
from graphviz import Digraph

class Tree(object):
    """
        Tree is a Binary Tree used to store CTL Expressions.
    """
    def __init__(self, root):
        """
            root: the root of the tree
            nodes: a empty list that can be used later as auxiliary to printing data
        """
        self.root = root
        self.nodes = []

    def inOrder(self, root):
        """
            DFS inOrder traversal of the Tree.

            Tree.inOrder sets up a list containing information about every
            TreeNode that composes the Tree. This information is later used
            by Tree.toString
        """
        if root == None:
            return
        left = self.inOrder(root.left)
        self.nodes.append(root.toList())
        right = self.inOrder(root.right)

    def render(self):
        """
            Tree.render creates a view for the tree in graphviz's
            dot notation. Each node will be rendered with two lines
            of data. The 1st being the identifier (TreeNode.label)
            and se 2nd being the expression of a TreeNode
        """
        dot = Digraph(format='png')
        self.toGraphviz(self.root, dot)
        dot.render('Tree', view=True)

    def toString(self):
        """
            Tree.toString returns a table containing information that describes each
            TreeNode that composes the Tree as a string
        """
        self.inOrder(self.root)
        return tabulate(sorted(self.nodes, key=lambda entry : entry[1]), self.root.getHeaders())

    def toGraphviz(self, node, dot):
        """
            In graphviz's dot notation, a node is represented with a id, which
            in our case is going to be the TreeNode.expression

            TreeNode.toGraphviz traverses the Tree and sets up all the nodes
            with information in graphviz's dot notation. Each node contains the 
            label of a TreeNode and the expression related to that label.
        """
        if node == None:
            return

        dot.node(node.expression, "{0}\n{1}".format(node.label, node.expression))

        if node.left is not None:
            dot.edge(node.expression, node.left.expression)

        if node.right is not None:
            dot.edge(node.expression, node.right.expression)

        self.toGraphviz(node.left, dot)
        self.toGraphviz(node.right, dot)

class TreeNode():
    """
        TreeNode is a node that compoese a Tree
    """

    def __init__(self, expression, label, operator, prop):
        """
            expresion: CTL Expression
            label: a identifier that uniquely identifies a expression. The label is going to be used
            by the labeling algorithm
            operator: should be None if the TreeNode is not a leaf
            prop: should be None is TreeNode is a leaf
        """
        # Required
        self.expression = expression
        self.label = label

        # Optional 
        self.operator = operator
        self.prop = prop

        # Default
        self.right = None
        self.left = None
        
    def __str__(self):
        return "Expression {0}\tLabel {1}\tOperator {2}\Property: {3}".format(
            self.expression,
            self.label,
            self.operator,
            self.prop)

    def toList(self):
        """
            Returns a list containing important information that describes a TreeNode
        """
        return [self.expression, self.label, self.operator, self.prop]

    def getHeaders(self):
        """
            Returns the headers that should be used at Tree to print a table containing
            each node's data.
        """
        return ["Expression", "Label", "Operator", "Property"]