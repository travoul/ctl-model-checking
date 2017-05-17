class Tree(object):
    """
        docstring for Tree
    """
    def __init__(self, root):
        """
        """
        self.root = root

    def dfs(self, order="in-order"):
        if order == "in-order":
            return self.inOrder(self.root)
        else:
            return self.inOrder(self.root)

    def inOrder(self, root):
        if root == None:
            return
        left = self.inOrder(root.left)
        print(root)
        right = self.inOrder(root.right)
        

class TreeNode():
    """
        docstring for Tree
    """

    def __init__(self, expression, label, operator, prop):
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