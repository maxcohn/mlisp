"""Read-Evaluate-Print-Loop

Running this file creates a lexer and parser and then begins a loop for user
entry. The prompt accepts Lisp code 1 line at a time, which all have access
to the global/initial environment.
"""

import lisp
import nodes

if __name__ == "__main__":
    print('Lisp!')

    # create lexer and parser
    lexer = lisp.LispLexer()
    parser = lisp.LispParser()

    # create for initial environment
    init_env = nodes.Environment(None)

    # begin REPL
    while True:
        i = input('> ')

        if i.strip() == '(quit)':
            break

        # create syntax tree and then evaluate/print
        ast = parser.parse(lexer.tokenize(i))
        
        #try:
        print(ast.eval_node(init_env))
        #except Exception as e:
        #    print(e)
        #    continue
        
        #print(f'table = {init_env.symbol_table}')
        #for i in init_env.symbol_table:
        #    print(f'{i} type={type(i)}, {type(init_env.symbol_table[i])}')

    print('See ya!')   