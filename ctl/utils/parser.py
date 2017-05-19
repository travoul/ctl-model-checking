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
        return Translator(expression).translatedExpression


class Translator():
    """
        Translate CTL
    """
    def __init__(self, expression):
        self.translatedExpression = self.convertCTL(expression)

    def simpleImplication(self, expression):

        for i in range(len(expression)):
            if expression[i:i+2] == list('->'):
                del expression[i+1]
                expression[i] = '|'
                expression.insert(i, ')')
                expression.insert(1, '!')
                expression.insert(1, '(')
                break

        return expression

    def doubleImplication(self, expression):

        for i in range(len(expression)):
            if expression[i:i+3] == list('<->'):
                lElements = expression[1:i]
                rElements = expression[i+3:-1]
                expression = (['('] + self.simpleImplication(['('] + lElements + ['-', '>'] + rElements + [')']) + 
                              ['&'] + self.simpleImplication(['('] + rElements + ['-', '>'] + lElements + [')']) + [')'])
                break

        return expression

    def convertAX(self, expression):

        for i in range(len(expression)):
            if expression[i:i+2] == list('AX'):
                expression = self.convertGeneral(expression, list('EX'), i)
                break

        return expression

    def convertEF(self, expression):

        for i in range(len(expression)):
            if expression[i:i+2] == ['E', 'F']:
                expression[i:i+2] = ['E', 'U']
                expression.insert(i+3, ',')
                expression.insert(i+3, ')')
                expression.insert(i+3, 'true')
                expression.insert(i+3, '(')

                break

        return expression

    def convertAG(self, expression):

        changes = False

        for i in range(len(expression)):
            if expression[i:i+2] == list('AG'):
                expression = self.convertGeneral(expression, list('EF'), i)
                break

        return self.convertEF(expression)

    def convertEG(self, expression):

        for i in range(len(expression)):
            if expression[i:i+2] == list('EG'):
                expression = self.convertGeneral(expression, list('AF'), i)
                break

        return expression

    def convertGeneral (self, expression, term, i):

        expression[i:i+2] = term
        #changing interior
        expression.insert(i+3, '!')
        expression.insert(i+3, '(')
        expression.insert(len(expression)-1, ')')
        #changing exterior
        expression.insert(0, '!')
        expression.insert(0, '(')
        expression.insert(len(expression)-1, ')')

        return expression

    def convertAU(self, expression):

        changes = False

        begin = 0
        middle = 0
        end = len(expression) - 2

        lElements = []
        rElements = []

        for i in range(len(expression)):
            if expression[i:i+2] == list('AU'):
                begin = i+3
                changes = True
            if expression[i] == ',':
                middle = i
                break

        if (changes == True):
            lElements = expression[begin:middle]
            rElements = expression[middle+1:end]

            blockEG = ['(', '!', '(', 'E', 'G', '(', '(', '!'] + rElements + [')', ')', ')', ')']
            blockEG = self.convertEG(blockEG)

            blockEU = ( ['E', 'U', '(', '(', '!'] + rElements 
                    + [')', ',', '(', '(', '!' ] + lElements 
                    + [')', '&', '(', '!'] + rElements 
                    + [')', ')'] )

            return ['('] + blockEG + ['&', '(', '!', '('] + blockEU + [')', ')', ')', ')']

        else:
            return expression

    def callAll(self, expression):

        expression = self.doubleImplication(expression)
        expression = self.simpleImplication(expression)
        expression = self.convertAX(expression)
        expression = self.convertEF(expression)
        expression = self.convertAG(expression)
        expression = self.convertEG(expression)
        expression = self.convertAU(expression)

        return expression

    def convertCTL(self, expression):

        expression.replace(" ", "")
        expression = list(expression)

        openP = []
        i=0

        #Runs the entire expression, looking for each pair of ()
        while (i < len(expression)):

            #There is a sub expression to look. Save where it begins
            if expression[i] == '(':
                openP.append(i)
            
            #A sub expression has ended. Analyze it!
            if expression[i] == ')':
                
                oldSize = len(expression)
                
                left = openP[len(openP)-1]
                right = i+1
                
                del openP[len(openP)-1]
                
                expression = expression[:left] + self.callAll(expression[left:right])  + expression[right:]
                
                newSize = len(expression)    
                
                i += newSize - oldSize

            i += 1

        return ''.join(expression)
            
            
