"""Runs a lisp program

Accepts a lisp program via the first argument and runs it
"""


import sys
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

    ast = parser.parse(lexer.tokenize(source))

    ast.eval_node(init_env)
    #print(ast.eval_node(init_env))