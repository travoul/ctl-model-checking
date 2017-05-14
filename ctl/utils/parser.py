from ctl.models.graph import GraphNode
from ctl.models.graph import Graph
from ctl.models.tree import Tree

from traceback import print_exc

class Parser():
    """docstring for Parser"""
    def __init__(self, filename):
        self.filename = filename

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
                    "expression" : ctlExpression
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
