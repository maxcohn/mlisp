# repl.py

# read evaluate print loop
import lisp


if __name__ == "__main__":
    print('Lisp!')

    lexer = lisp.LispLexer()
    parser = lisp.LispParser()

    while True:
        i = input('> ')

        ast = parser.parse(lexer.tokenize(i))
        print(ast.eval_node())