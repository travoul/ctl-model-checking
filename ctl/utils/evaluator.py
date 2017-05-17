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
        self.helper = EvaluatorHelper(stateMachine)
        self.label = 0

    def evaluate(self):
        tree = Tree(self.build(self.expression.translated))

        self.analyze(tree.root)

        return tree

    def analyze(self, node):
        """

        """
        # Caso o operator tenha somente um no a esquerda como EX e AF,
        # eh preciso verificar se o node passado nao eh nulo
        if node == None:
            return None
        print("analyze", node)
        if node.prop != None:
            # deveria aplica o label a todos os nós com essa propriedade
            # no folha
            self.helper.applyLabel(node, None, None)
            print("-----------------------------------")
            return node.label
        else:
            # eu sei que node.prop eh None, entao node.operator nao deve ser None
            # Ou seja, preciso do resultado dos meus filhinhos
            left = self.analyze(node.left)
            right = self.analyze(node.right)
            print("Left {0}    Right: {1}".format(left, right))
            self.helper.applyLabel(node, left, right)
            print("-----------------------------------")

            return node.label

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
        root = TreeNode(expression, self.label, operator, prop)
        self.label = self.label + 1
        root.left = self.build(leftExpression)
        root.right = self.build(rightExpression)

        return root

class EvaluatorHelper():
    """
        docstring for EvaluatorHelper
    """
    def __init__(self, graph):
        self.graph = graph
        self.operators = {
            "&": self.andOperator,
            "|": self.orOperator,
            "eu": self.eu,
            "ex": self.ex,
            "af": self.af,
            "!": self.neg
        }

    def applyLabel(self, node, leftLabel, rightLabel):
        if leftLabel == None and rightLabel == None:
            self.prop(node.label, node.prop)
        else:
            self.operators[node.operator](node.label, leftLabel, rightLabel)

    def neg(self, label, left, dummy):
        nodes = self.graph.nodes
        for key in nodes:
            if left not in nodes[key].labels:
                nodes[key].labels.append(label)

    def andOperator(self, label, left, right):
        nodes = self.graph.nodes
        for key in nodes:
            if left in nodes[key].labels and right in nodes[key].labels:
                nodes[key].labels.append(label)

    def orOperator(self, label, left, right):
        nodes = self.graph.nodes
        for key in nodes:
            if left in nodes[key].labels or right in nodes[key].labels:
                nodes[key].labels.append(label)

    def eu(self, label, left, until):
        print("eu")

    def ex(self, label, left, dummy):
        print("ex")

    def af(self, label, left, dummy):
        print("af")

    def prop(self, label, prop):
        nodes = self.graph.nodes
        for key in nodes:
            if prop in nodes[key].properties:
                nodes[key].labels.append(label)