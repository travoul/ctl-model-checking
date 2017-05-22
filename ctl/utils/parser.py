from ctl.models.graph import GraphNode
from ctl.models.graph import Graph
from ctl.models.tree import TreeNode
from ctl.models.tree import Tree

from traceback import print_exc

class GraphParser():
    """
        This class opens and reads the input file. It then creates
        the graph representing the state machine described in the file.
    """
    def __init__(self, filename):
        self.filename = filename
        self.label = 0

    def parse(self):
        """
            Open the input file and create each nod of the graph,
            representing a different state. It also create the
            necessary edges and label each state according to its name
            ans properties.
        """
        try:
            with open(self.filename, 'r') as inputData:     #open file

                lines = inputData.readlines()               #read all lines
                numberOfStates = int(lines[0])              #get number of states

                #Checking for empty state machine
                if (numberOfStates <= 0):
                    return None

                #Nodes of the graph are stored as a dictionary, with key as
                #it own name.
                nodes = {}

                #Read each of the lines and crete a node representing it.
                for i in range(1, numberOfStates + 1):
                    node = self.createGraphNode(lines[i])
                    
                    #Checking for invalid states
                    for nextState in node.nextStates:
                        if (int(nextState) > numberOfStates) or (int(nextState) < 1):
                            print('Error at line ' + str(i) + ' "' + lines[i][:-1] + '"')
                            return None
                    
                    nodes[node.name] = node

                #Returns the constructed graph
                return Graph(nodes)

        #If there was an error with the input file
        except Exception as e:
            print_exc(e)

    def createGraphNode(self, data):
        """
            This function is used to create a node of the graph
            representing the state machine in the input file.
        """

        #Data has all the line information. Creates a list from it (separates by space)
        data = data.split()

        #The name of the state is the first element of the line
        name = data[0]

        #Number of properties this state has
        numberOfProperties = int(data[1])

        #Each property of the state is read
        properties = data[2:2 + numberOfProperties]

        #NUmber of next states from that node
        numberOfNextStates = int(data[numberOfProperties + 2])

        #Stores each of these next states
        nextStates = data[numberOfProperties + 3:]

        #Returns the node constructed
        return GraphNode(name, properties, nextStates)

class CTLParser():
    """
        This class opens and reads the input file for parsing
        the CTL expression.
    """
    def __init__(self, filename):
        self.filename = filename
        self.expressions = []

    def parse(self):
        """
            This function open the input file and parse only the CTL
            expression. It then return a list of all expressions on the file.
        """
        try:
            with open(self.filename, 'r') as inputData:

                lines = inputData.readlines()
                numberOfStates = int(lines[0])

                #Creates a list of all expressions (tuple)
                #The class Expression is used for translating the CTL expressions
                self.expressions = tuple([ Expression(expression.strip().replace(" ", "")) for expression in lines[numberOfStates + 1:] ])
                return self.expressions
        
        #If there was a problem when oppening the file
        except Exception as e:
            print_exc(e)


class Expression():
    """
        This class is responsible for translating the CTL expression,
        together with the Translator class.
    """
    def __init__(self, original):
        self.original = original
        self.translated = self.translate(original)

    def __str__(self):
        """
            Used for printing only
        """
        return "E({0})\tTE({1})".format(self.original, self.translated)

    def translate(self, expression):
        """
            This function returns the translated expression. It
            uses the functions define in the Translator class.
        """
        return Translator(expression).translatedExpression


class Translator():
    """
        This class represents the Translator of the CTL expression. When an expression
        is readed by the parser, it is sent to this class. The expression is translated
        in the defined operators: EF, EU, AF, ! (not), & (and) and | (or).
    """
    def __init__(self, expression):
        self.translatedExpression = self.convertCTL(expression)


    def simpleImplication(self, expression):
        """
            Translates a simple implication operator (->).
            Ex: (a)->(b) will be returned as !(a)|(b).
        """
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
        """
            Translates a double implication operator (<->).
            Ex: (a)<->(b) will be returned as ((a)->(b))^((b)->(a))
        """
        for i in range(len(expression)):
            if expression[i:i+3] == list('<->'):
                lElements = expression[1:i]
                rElements = expression[i+3:-1]
                expression = (['('] + self.simpleImplication(['('] + lElements + ['-', '>'] + rElements + [')']) + 
                              ['&'] + self.simpleImplication(['('] + rElements + ['-', '>'] + lElements + [')']) + [')'])
                break

        return expression

    def convertAX(self, expression):
        """
            Translates the AX operator. Note that the general conversion function
            'convertGeneral()' is used, since the same logic can be applied to
            other operators.
            Ex: AX((a)) will be returned as !EX(!(a))
        """
        for i in range(len(expression)):
            if expression[i:i+2] == list('AX'):
                expression = self.convertGeneral(expression, list('EX'), i)
                break

        return expression

    def convertEF(self, expression):
        """
            Translates the EF operator. This operator has a specific rule, and the
            'convertGeneral()' function will not be used.
            Ex: EF((a)) will be returned as EU((true), (a)).
        """
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
        """
            Translates the AG operator. Note that the general conversion function
            'convertGeneral()' is used, since the same logic can be applied to
            other operators.
            Ex: AG((a)) will be returned as !EF(!(a))
        """
        for i in range(len(expression)):
            if expression[i:i+2] == list('AG'):
                expression = self.convertGeneral(expression, list('EF'), i)
                break

        return self.convertEF(expression)

    def convertEG(self, expression):
        """
            Translates the EG operator. Note that the general conversion function
            'convertGeneral()' is used, since the same logic can be applied to
            other operators.
            Ex: EG((a)) will be returned as !AF(!(a))
        """
        for i in range(len(expression)):
            if expression[i:i+2] == list('EG'):
                expression = self.convertGeneral(expression, list('AF'), i)
                break

        return expression

    def convertGeneral (self, expression, term, i):
        """
            Some operators such as EG, AG and AX should be translated, and the
            logic applied in this process is similar to all these three operator.
            So a general function was created to be used by all these operations.
            It receives the expression (expression), the term which will be used
            as a substitute (term) and the index of where the substitution should
            occur (i).
        """

        expression[i:i+2] = term                    #Substitution for the new term
        
        #changing interior parentheses
        expression.insert(i+3, '!')     
        expression.insert(i+3, '(')
        expression.insert(len(expression)-1, ')')
        
        #changing exterior parentheses
        expression.insert(0, '!')
        expression.insert(0, '(')
        expression.insert(len(expression)-1, ')')

        return expression

    def convertAU(self, expression):
        """
            Translates the AU operator. This operator has a specific rule, and the
            'convertGeneral()' function will not be used.
            Ex: AU((a),(b)) will be returned as AF(b)^EU((!b),((!b)^(!a)))
        """

        changes = False     #If any changes were made in the expression,
                            #this variable is set as True.

        begin = 0                   #Indicates the begging of the AU expression
        middle = 0                  #Indicates the position of the comma
        end = len(expression) - 2   #Indicates the ende of the AU expression

        lElements = []      #Left elements (AU((lElements),(rElements)))
        rElements = []      #Right elements

        #Searchs for the AU operator
        for i in range(len(expression)):
            if expression[i:i+2] == list('AU'):
                begin = i+3         
                changes = True      #Changes are going to be done!

        #Used for parentheses counting. This is important to know
        #where when the expression ends.
        pCount = 0

        #Since the expression has the AU operator, it should be translated
        if changes == True:
            for i in range(begin, len(expression)):
                
                if expression[i] == '(':
                    pCount += 1
                elif expression[i] == ')':
                    pCount -= 1
                
                #When pCount == 0, we know we readed the first expression
                #(lElements) from the AU operator, so the next term is a comma.
                if pCount == 0:
                    middle = i + 1
                    break

            #Separates the left and right elements of the AU operator.
            #The format is AU((lElements),(rElements)).
            lElements = expression[begin:middle]   
            rElements = expression[middle+1:end]

            #Creates the EG element.
            blockEG = ['(', '!', '(', 'E', 'G', '(', '(', '!'] + rElements + [')', ')', ')', ')']
            blockEG = self.convertEG(blockEG)   #Converts the EG element.

            #Creates the EU element.
            blockEU = ( ['E', 'U', '(', '(', '!'] + rElements 
                    + [')', ',', '(', '(', '!' ] + lElements 
                    + [')', '&', '(', '!'] + rElements 
                    + [')', ')'] )

            #Return the translated expression.
            return ['('] + blockEG + ['&', '(', '!', '('] + blockEU + [')', ')', ')', ')']

        else:
            #No conversion were perfomed. Returning the initial expression.
            return expression

    def callAll(self, expression):
        """
            This function receives an expression and check what
            operators are present. If an operator is found, he is
            converted.
        """
        expression = self.doubleImplication(expression)
        expression = self.simpleImplication(expression)
        expression = self.convertAX(expression)
        expression = self.convertEF(expression)
        expression = self.convertAG(expression)
        expression = self.convertEG(expression)
        expression = self.convertAU(expression)

        #Return the converted expression.
        return expression

    def convertCTL(self, expression):
        """
            The initial function which translates the expression.
            It receives the expression as a parameter and separate each
            of the sub-expressions by parantheses. These are then sent
            for conversion. For example, the expression (AX((a)->(b)))
            will first convert the expressions (a), then (b), then
            ((a)->(b)) and finally AX((a)->(b)).
        """

        #If there were any spaces
        expression.replace(" ", "")

        #Convert the expression to a list
        expression = list(expression)

        #This list stores the positions of the parantheses.
        openP = []
        i=0

        #Runs the entire expression, looking for each pair of ()
        while (i < len(expression)):

            #There is a sub expression to look. Save where it begins
            if expression[i] == '(':
                openP.append(i)
            
            #A sub expression has ended. Analyze it!
            if expression[i] == ')':
                
                #the old size of the expression (before conversion)
                oldSize = len(expression)
                
                #Position of the left parenthesis
                left = openP[len(openP)-1]

                #Position of the right paranthesis
                right = i+1
                
                #Deletes this lat parenthesis
                del openP[len(openP)-1]
                
                #Translate only the sub expression, and concatenates it with the old parts
                expression = expression[:left] + self.callAll(expression[left:right])  + expression[right:]
                
                #The new expression may differ in size
                newSize = len(expression)    
                
                # i must now point to the end of the translated expression
                i += newSize - oldSize

            i += 1

        #Returns the translated expression as a string.
        return ''.join(expression)
            
            
