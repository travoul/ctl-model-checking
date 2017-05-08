import traceback
from GraphNode import GraphNode
from Graph import Graph

class Parser():
	"""docstring for Parser"""
	def __init__(self, fileName):
		self.fileName = fileName

	def parse(self):

		try:
			with open(self.fileName, 'r') as inputData:

				lines = inputData.readlines()
				numberOfStates = int(lines[0])

				nodes = {}
				for i in range(1, numberOfStates + 1):
					node = self.createGraphNode(lines[i])
					nodes[node.name] = node

				return Graph(nodes)
		except Exception as e:
			traceback.print_exc(e)
		

	def createGraphNode(self, data):

		data = data.split()

		name = data[0]

		numberOfProperties = int(data[1])
		properties = data[2:2 + numberOfProperties]

		numberOfNextStates = int(data[numberOfProperties + 2])
		nextStates = data[numberOfProperties + 3:]

		return GraphNode(name, properties, nextStates)
