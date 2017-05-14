class Tree(object):
    """docstring for Tree"""
    def __init__(self):
        print("")
        

class TreeNode():
    """docstring for Tree"""
    def __init__(self, expression, label, left = None, right = None):
        """
            TreeNode constructor

            expresion should determine which kind of evaluation I need to perform
            in a State Machine

            label is the name that will be assigned to nodes which the evaluated expression is True

            left and right should be another TreeNode
        """
        self.expression = expression
        self.label = label
        self.left = left
        self.right = right
        self.arg = arg
        