from graphviz import Digraph

class Graph():
    """
        Graph is a collection of GraphNodes
    """
    def __init__(self, nodes = {}):
        """
            nodes: a dictionary containing all the nodes that composes the Graph.
            the key is a GraphNode's name and the value is the GraphNode itself
        """
        self.nodes = nodes

    def __str__(self):
        return "{0} Nodes\n{1}\n".format(len(self.nodes), " ".join(self.nodes.keys()))

    def addNode (self, node):
        """
            Inserts a node into Graph.nodes dictionary
        """
        nodes[node.name] = node

    def reset(self):
        """
            Graph.reset clears all nodes' labels
        """
        for node in nodes:
            nodes[node].clearLabels()

    def render(self):
        """
            Graph.render creates a view for the graph in graphviz's
            dot notation. Each node will be rendered with two lines
            of data. The 1st being the identifier (GraphNode.name)
            and se 2nd being the properties of a GraphNode
        """
        dot = Digraph(comment="State Machine", format='png')
        
        for node in self.nodes:
            strings = self.nodes[node].toGraphviz()
            dot.node(strings["id"], strings["text"])
            dot.edges(self.nodes[node].edgesToGraphviz())

        dot.render('Graph', view=True)

class GraphNode():
    """
        GraphNode is the Node that composes a Graph
    """

    def __init__(self, name, properties, nextStates):
        """
            name: identifier that should uniquely identify a GraphNode
            properties: a list of properties that describes characteristics
            of a GraphNode
            nextStates: list os states that can be reached through GraphNode

            labels: attribute that will store all the labels that the labeling
            algorithm judges that a GraphNode should have
        """
        self.properties = properties
        self.nextStates = nextStates
        self.labels = set()
        self.name = name

    def __str__(self):
        return "Node {0}\nProperties {1}\nNext States {2}\nLabels {3}\n-------------------------------"\
            .format(self.name, sorted(self.properties), sorted(self.nextStates), sorted(self.labels))

    def toGraphviz(self):
        """
            In graphviz's dot notation, a node is represented with a id, which
            in our case is going to be the GraphNode.name

            GraphNode.toGraphviz returns a dictionary containing the id that
            will represent GraphNode in graphviz's dot notation and the text
            that will be shown when the graph gets rendered.
        """
        prop = ""

        for p in self.properties:
            prop = "{0} {1}".format(prop, p)

        return {
            "id": self.name,
            "text": "{0}\n{1}".format(self.name, prop.strip())
        }

    def edgesToGraphviz(self):
        """
            In graphviz's dot notation, edges are represented as follows:

            Suppose the graph itself contains two nodes 'A' and 'B' that are
            connected to each other, the link between there nodes is represented
            as 'AB'.

            GraphNode.edgesToGraphviz returns a list of the connections between
            self and its next states that are formatted as described above
        """
        return [ "{0}{1}".format(self.name,state) for state in self.nextStates ]

    def clearLabels (self):
        """
            Labels are a crucial part of the labeling algorithm used to evaluate
            CTL expressions in a graph. If there are more than one expression to
            be evaluated, than it is required to reset the labels of a GraphNode

            GraphNode.clearLabels restarts the labels of a GraphNode
        """
        self.labels = set()
