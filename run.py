"""Runs a lisp program

Accepts a lisp program via the first argument and runs it
"""


import sys
import time

import lisp
import nodes

if __name__ == "__main__":
    source = None

    # read in entire file
    with open(sys.argv[1]) as f:
        source = f.read()

    #print(source)

    # create lexer and parser
    lexer = lisp.LispLexer()
    parser = lisp.LispParser()

    # create for initial environment
    init_env = nodes.Environment(None)

    start_time = int(round(time.time() * 1000))

    ast = parser.parse(lexer.tokenize(source))

    ast.eval_node(init_env)

    end_time = int(round(time.time() * 1000))

    print(f'Total time for program execution (ms): {0.001 * (end_time - start_time)}')
    #print(ast.eval_node(init_env))