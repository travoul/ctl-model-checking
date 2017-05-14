from ctl.utils.parser import Parser

from traceback import print_exc
from os import getcwd
from os import path

import sys

def main():

    if not(len(sys.argv) == 2):
        sys.exit("")

    # If argc == 3, than a txt file name should have been provided as argv[2]
    filename = sys.argv[1]

    if not (path.exists(filename)):
        sys.exit("{0} not exists".format(filename))

    parser = Parser(filename)
    parsedInput = parser.parse()

    graph = parsedInput["graph"]
    ctlExpression = parsedInput["expression"]

    print(graph)
    print(ctlExpression)

    for node in graph.nodes:
        print(graph.nodes[node])

    print("ctl-model-checking says goodbye!")

if __name__ == '__main__':
    main()