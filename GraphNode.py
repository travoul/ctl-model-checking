class GraphNode():
    """docstring for Node"""

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