class GraphNode(object):
    """docstring for Node"""

    def __init__(self, properties, nextStates, name):
        self.properties = properties
        self.nextStates = nextStates
        self.labels = []
        self.name = name
        self.visited = False
        
    def addLabel (self, label):
        self.labels.append(label)

    def clearLabels (self):
        self.labels = []

    def isLabeledWith (self, label):
        return label in self.labels