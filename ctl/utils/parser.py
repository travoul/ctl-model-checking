from ctl.models.graph import GraphNode
from ctl.models.graph import Graph
from ctl.models.tree import TreeNode
from ctl.models.tree import Tree

from ctl.utils import CTLUtils

from traceback import print_exc

class Parser():
    """docstring for Parser"""
    def __init__(self, filename):
        self.filename = filename
        self.helper = CTLUtils()
        self.label = 0

    def parse(self):
        try:
            with open(self.filename, 'r') as inputData:

                lines = inputData.readlines()
                numberOfStates = int(lines[0])

                nodes = {}
                for i in range(1, numberOfStates + 1):
                    node = self.createGraphNode(lines[i])
                    nodes[node.name] = node

                ctlExpression = lines[len(lines) - 1]


                return {
                    "graph" : Graph(nodes),
                    "expression" : self.parseCTL(ctlExpression)
                }

        except Exception as e:
            print_exc(e)

    def createGraphNode(self, data):

        data = data.split()

        name = data[0]

        numberOfProperties = int(data[1])
        properties = data[2:2 + numberOfProperties]

        numberOfNextStates = int(data[numberOfProperties + 2])
        nextStates = data[numberOfProperties + 3:]

        return GraphNode(name, properties, nextStates)

    def parseCTL(self, expression):
        """
        """

        # Base case where the expression has been parsed to its smallest
        # granularity (there is no operands)
        if (helper.isProperty(expression))
            return createTreeNode(expression, 0)

        splitedExpression = helper.splitExpression(expression)

        operator = splitedExpression["operator"]
        leftExpression = splitedExpression["left"]
        rightExpression = None

        if (helper.shouldHaveRightExpression()):
            rightExpression = splitedExpression["right"]

        root = createTreeNode(expression, 0)
        
        return Tree(root)

