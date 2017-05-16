from ctl.models.tree import TreeNode
from ctl.models.tree import Tree

class Evaluator():
    """
        docstring for Evaluator
    """
    def __init__(self, expression, stateMachine):
        """
            expression is a of Expression type as implemented in ctl.utils.parser.Expression
            stateMachine is of Graph type as implemented in ctl.models.graph.Graph
        """
        self.expression = expression
        self.stateMachine = stateMachine

    def evaluate(self):
        return Tree(self.build(self.expression.translated))

    def build(self, expression):
        if expression == None:
            return None

        rightExpression = None
        leftExpression = None
        operator = None
        prop = None

        parenthesesCount = 1
        left = 2
        it = 2

        if expression[1] != '(':
            if (expression[1]) == '!':
                operator = '!'
                it = 1
                leftExpression = expression[2:-1]
            # Cuidao com o length!!!!!!
            elif expression[1:4].upper() in ["AF(","EX("]:
                operator = expression[1:3]
                it = 1
                leftExpression = expression[4:-2]
                
            elif expression[1:4].upper() in ["EU("]:
                operator = expression[1:3]
                it = 1
                newExpression = expression[4:-2]
                leftExpression, rightExpression = newExpression.split(',')
                # print(newExpression, leftExpression, rightExpression)
            else:
                # nao tem operator!
                prop = expression[1:len(expression) - 1]
        else:
            while parenthesesCount != 0:
                if expression[it] == '(':
                    parenthesesCount = parenthesesCount + 1
                elif expression[it] == ')':
                    parenthesesCount = parenthesesCount - 1
                it = it + 1

            rightExpression = expression[it + 1:-1]
            leftExpression = expression[1:it]
            operator = expression[it]

        # print(operator, leftExpression, rightExpression, prop)
        root = TreeNode(expression, 0, operator, prop)
        root.left = self.build(leftExpression)
        root.right = self.build(rightExpression)

        return root