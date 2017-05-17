from ctl.models.graph import GraphNode
from ctl.models.graph import Graph
from ctl.models.tree import TreeNode
from ctl.models.tree import Tree

from traceback import print_exc

class GraphParser():
    """

    """
    def __init__(self, filename):
        self.filename = filename
        self.label = 0

    def parse(self):
        """

        """
        try:
            with open(self.filename, 'r') as inputData:

                lines = inputData.readlines()
                numberOfStates = int(lines[0])

                nodes = {}
                for i in range(1, numberOfStates + 1):
                    node = self.createGraphNode(lines[i])
                    nodes[node.name] = node

                return Graph(nodes)
        except Exception as e:
            print_exc(e)

    def createGraphNode(self, data):
        """

        """
        data = data.split()

        name = data[0]

        numberOfProperties = int(data[1])
        properties = data[2:2 + numberOfProperties]

        numberOfNextStates = int(data[numberOfProperties + 2])
        nextStates = data[numberOfProperties + 3:]

        return GraphNode(name, properties, nextStates)

class CTLParser():
    """

    """
    def __init__(self, filename):
        self.filename = filename
        self.expressions = []

    def parse(self):
        """

        """
        try:
            with open(self.filename, 'r') as inputData:

                lines = inputData.readlines()
                numberOfStates = int(lines[0])

                self.expressions = tuple([ Expression(expression.strip().replace(" ", "")) for expression in lines[numberOfStates + 1:] ])
                return self.expressions
        except Exception as e:
            print_exc(e)


class Expression():
    """
        docstring for Expression
    """
    def __init__(self, original):
        self.original = original
        self.translated = self.translate(original)

    def __str__(self):
        return "E({0})\tTE({1})".format(self.original, self.translated)

    def translate(self, expression):
        """
        
        """
        #
        #
        #   IGS, INSIRA SEU CODIGO AQUI!
        #   E SUBSTITUA O RETORNO DE expression PARA A TRADUCAO
        #
        return expression
        
        
