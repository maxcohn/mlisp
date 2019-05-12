# repl.py

# read evaluate print loop
import lisp
import nodes

if __name__ == "__main__":
    print('Lisp!')

    lexer = lisp.LispLexer()
    parser = lisp.LispParser()

    # create for initial environment
    init_env = nodes.Environment(None)

    while True:
        i = input('> ')

        ast = parser.parse(lexer.tokenize(i))
        print(ast.eval_node(init_env))
        #print(f'Symbol table: {init_env.print_table()}')
        #init_env.print_table()
        print(f'{init_env.symbol_table}')