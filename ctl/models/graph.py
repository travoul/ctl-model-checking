class Graph():
    """
        docstring for Graph
    """
    def __init__(self, nodes):
        self.nodes = nodes
        self.hasProperty = False

    def __str__(self):
        return "Number of Nodes: {0}\nNodes: {1}\n".format(len(self.nodes), self.nodes.keys())

    def addNode (self, node):
        nodes[node.name] = node

    def clearNodesLabels(self):
        for node in nodes:
            nodes[node].clearLabels()

    def setNodesNotVisited(self):
        for node in nodes:
            nodes[node].visited = False

    def reset(self):
        self.clearNodesLabels()
        self.setNodesNotVisited()
        self.hasProperty = False

class GraphNode():
    """
        docstring for Node
    """

    def __init__(self, name, properties, nextStates):
        self.properties = properties
        self.nextStates = nextStates
        self.labels = []
        self.name = name
        self.visited = False

    def __str__(self):
        return "Node {0}\nProperties {1}\nNext States: {2}\n----------".format(self.name, self.properties, self.nextStates)

    def addLabel (self, label):
        self.labels.append(label)

    def clearLabels (self):
        self.labels = []

    def isLabeledWith (self, label):
        return label in self.labels