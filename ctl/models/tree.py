class Tree(object):
    """
        docstring for Tree
    """

    def __init__(self, root):
        """
        """
        self.root = root
        

class TreeNode():
    """
        docstring for Tree
    """

    def __init__(self, expression, label, operator = None, prop = None):
        """
            TreeNode constructor

            expresion should determine which kind of evaluation I need to perform
            in a State Machine

            label is the name that will be assigned to nodes which the evaluated expression is True

            left and right should be another TreeNode
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
        return "Expression: {0} \t Label: {1} \t Operator: {2} \t Property: {3}".format(
            self.expression,
            self.label,
            self.operator,
            self.prop)

    def toList(self):
        return [self.expression, self.label, self.operator, self.prop]

    @staticmethod
    def getHeaders():
        return ["expression", "label", "operator", "property"]