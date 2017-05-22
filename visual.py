from ctl.utils.evaluator import Evaluator

from ctl.utils.parser import GraphParser
from ctl.utils.parser import CTLParser

from traceback import print_exc
from os import path

import sys

def main():
    # Checking input arguments
    if not(len(sys.argv) == 2):
        sys.exit("# ERROR: Invalid number of arguments!\n The arguments must follow the rule:\n   $ python3 main.py <input_state_machine.txt>\n If you want to get Graphviz visualization, you must follow the rule:\n   $ python3 main.py <input_state_machine.txt> true")

    # If argc == 2, than a txt file name should have been provided as argv[2]
    filename = sys.argv[1]

    # Checking if the file exists
    if not (path.exists(filename)):
        sys.exit(" # Error: {0} not exists".format(filename))

    # Parsing input file, which contains the State Machine and the CTL expression that is going to be evaluated
    graphParser = GraphParser(filename)
    graph = graphParser.parse()
    
    # Parsing CTL expression that was found in the file
    ctlParser = CTLParser(filename)
    expressions = ctlParser.parse()

    # Printing Tree and State Machine using Graphviz
    graph.render()
    tree.render()

if __name__ == '__main__':
main()