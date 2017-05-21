from ctl.models.tree import TreeNode
from ctl.models.tree import Tree

class Evaluator():
    """
        Evaluator
    """
    def __init__(self, expression, stateMachine):
        """
            expression: Expression type as implemented in ctl.utils.parser.Expression
            stateMachine: Graph type as implemented in ctl.models.graph.Graph
        """
        self.expression = expression
        self.stateMachine = stateMachine
        self.helper = EvaluatorHelper(stateMachine)
        self.label = 0
        self.labels = {}

    def evaluate(self):
        """
            Evaluator.evaluate is the interface which is used to evaluate CTL Expression
            in self.stateMachine. It is a wrapper that first builds a syntactic tree by
            invoking Evaluator.build and later analyze the generated tree by applying
            labels according to a label algorithm as implemented in EvaluatorHelper
        """
        tree = Tree(self.build(self.expression.translated))
        self.analyze(tree.root)
        return tree

    def analyze(self, node):
        """
            Given a syntactic tree that starts at node, uses self.helper
            to label the graph according to the current node and its children
        """
        if node == None:
            return None

        if node.prop != None:
            # Leaf nodes
            self.helper.applyLabel(node, None, None)
            return node.label
        else:
            # If a node is not a leaf, then it is required the result of
            # its children nodes
            left = self.analyze(node.left)
            right = self.analyze(node.right)
            self.helper.applyLabel(node, left, right)

            return node.label

    def getLabel(self, expression):
        """
            Evaluator.getLabel populates self.labels with new
            labels and returns labels for expressions that have
            already been assigned a label
        """
        try:
            self.labels[expression]
        except KeyError:
            self.labels[expression] = self.label
            self.label = self.label + 1

        return self.labels[expression]

    def build(self, expression):
        """
            Given a CTL Expression, Evaluator.build recursively builds a
            synthatic tree that will be later evaluated
        """
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
            elif expression[1:4].upper() in ["AF(","EX("]:
                operator = expression[1:3]
                it = 1
                leftExpression = expression[4:-2]
                
            elif expression[1:4].upper() in ["EU("]:
                operator = expression[1:3]
                it = 1
                newExpression = expression[4:-2]

                pCount = 0
                comma = 0

                for i in range(len(newExpression)):
                    if newExpression[i] == '(':
                        pCount += 1
                    if newExpression[i] == ')':
                        pCount -= 1
                    if pCount == 0:
                        comma = i + 1
                        break

                leftExpression = newExpression[:comma]
                rightExpression = newExpression[comma+1:]
                
            else:
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

        root = TreeNode(expression, self.getLabel(expression), operator, prop)
        root.left = self.build(leftExpression)
        root.right = self.build(rightExpression)

        return root

class EvaluatorHelper():
    """
        EvaluatorHelper contains methods that implements algorithms used to
        evaluate a CTL Expression.
    """
    def __init__(self, graph):
        """

        """
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
        """
            Interface that should be invoked when using EvaluatorHelper.

            EvaluatorHelper.applyLabel uses self.operators dictionary
            to redirect the call to a proper operator handler.
        """
        if leftLabel == None and rightLabel == None:
            self.prop(node.label, node.prop)
        else:
            self.operators[node.operator.lower()](node.label, leftLabel, rightLabel)

    def neg(self, label, left, dummy):
        """
            Evaluator.neg labels a node if the node does not have
            'left' in its labels set
        """
        nodes = self.graph.nodes
        for key in nodes:
            if left not in nodes[key].labels:
                nodes[key].labels.update([label])

    def andOperator(self, label, left, right):
        """
            Evaluator.andOperator labels a node if the node does
            have both 'left' and 'right' in its labels set
        """
        nodes = self.graph.nodes
        for key in nodes:
            if left in nodes[key].labels and right in nodes[key].labels:
                nodes[key].labels.update([label])

    def orOperator(self, label, left, right):
        """
            Evaluator.orOperator labels a node if it have 'left'
            or 'right' in its labels set
        """
        nodes = self.graph.nodes
        for key in nodes:
            if left in nodes[key].labels or right in nodes[key].labels:
                nodes[key].labels.update([label])

    def eu(self, label, left, until):
        """
            Evaluator.eu algorithm is segmented into two steps.
            
            1st step: for all nodes, label each node that have
            'until' in its labels set.

            2nd step: Label all nodes that contains 'left' in
            its labels set and if a next state have 'until' in
            its labels set. Rerun 2nd step while updates occur.
        """
        nodes = self.graph.nodes

        for key in nodes:
            if until in nodes[key].labels:
                nodes[key].labels.update([label])

        shouldUpdate = True
        while shouldUpdate:
            shouldUpdate = False
            for key in nodes:
                if label in nodes[key].labels:
                    continue

                # If I ever get here, it means i wasn't labeled as 'label' yet
                for nextState in nodes[key].nextStates:
                    if left in nodes[key].labels and label in nodes[nextState].labels:
                        nodes[key].labels.update([label])
                        shouldUpdate = True
                        break

    def ex(self, label, left, dummy):
        """
            Evaluator.ex checks if a next state of a node have 'left'
            in its labels set. If it does have, the Evaluator.ex algorithm
            is completed and the node is labeled with 'label'
        """
        nodes = self.graph.nodes
        for key in nodes:
            for nextState in nodes[key].nextStates:
                if left in nodes[nextState].labels:
                    nodes[key].labels.update([label])
                    break

    def af(self, label, left, dummy):
        """
            Evaluator.af algorithm is segmented into two steps.
            
            1st step: for all nodes, label each node that have
            'left' in its labels set.

            2nd step: Label all nodes that all its next states
            contains 'left' in its labels set. Rerun 2nd step
            while updates occur.
        """
        nodes = self.graph.nodes
        for key in nodes:
            if left in nodes[key].labels:
                nodes[key].labels.update([label])

        shouldUpdate = True
        while shouldUpdate:

            shouldUpdate = False
            for key in nodes:

                # In case there is a self loop just leave it as it is
                if key in nodes[key].nextStates or label in nodes[key].labels:
                    continue

                countStates = len(nodes[key].nextStates)
                count = 0

                for nextState in nodes[key].nextStates:
                    if label in nodes[nextState].labels:
                        count = count + 1
                    else: break

                if count == countStates:
                    nodes[key].labels.update([label])
                    shouldUpdate = True

    def prop(self, label, prop):
        """
            EvaluatorHelper.prop labels a graph based on a leaf node of the
            CTL Expression's synthatic tree. All leaf nodes are base cases
            of a single property and a Node will be labeled with label if
            and only if prop is contained in Node's properties.
        """
        nodes = self.graph.nodes
        for key in nodes:
            if prop in nodes[key].properties or prop == 'true':
                nodes[key].labels.update([label])