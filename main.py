from ctl.utils.evaluator import Evaluator

from ctl.utils.parser import GraphParser
from ctl.utils.parser import CTLParser

from traceback import print_exc
from os import path

import sys

def main():

    if not(len(sys.argv) == 2):
        sys.exit("Wrong arguments!\n$ python3 main.py <input.txt>")

    # If argc == 3, than a txt file name should have been provided as argv[2]
    filename = sys.argv[1]

    if not (path.exists(filename)):
        sys.exit("{0} not exists".format(filename))

    graphParser = GraphParser(filename)
    graph = graphParser.parse()
    print(graph)
    ctlParser = CTLParser(filename)
    expressions = ctlParser.parse()

    evaluator = Evaluator(expressions[0], graph)

    tree = evaluator.evaluate()

    print("")
    print("")
    print("-------------- Tree ------------")
    tree.dfs()

    print("-------------- Graph ------------")
    for key in sorted(graph.nodes):
        print(graph.nodes[key])

if __name__ == '__main__':
    main()