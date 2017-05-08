class Graph(object):
	"""docstring for Graph"""
	def __init__(self):
		self.nodes = {}
		self.hasProperty = False

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



