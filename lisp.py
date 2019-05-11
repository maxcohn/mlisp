from sly import Lexer, Parser

# Current goals:
# Primative operations: +, -, *, /
# Evaluation of syntax tree (maybe save things as objects)

source = '(+ 10 (- 20 30))'

def print_ast_help(ast: tuple, indent: int):
    for v in ast:
        #print(type(v))
        if type(v) is tuple or type(v) is list:
            print_ast_help(v, indent + 1)
        else:
            print(f'{"--" * indent} {v}')

def print_ast(ast: tuple):
    print_ast_help(ast, 0)


class LispLexer(Lexer):
    tokens = {LPAREN, RPAREN, NUMBER, SYMBOL, DEFUN, PLUS,
        MINUS, MULT, DIV
    }

    ignore = ' \t'
    ignore_comment = r';.*'
    
    # Tokens
    NUMBER = r'\-?\d+'
    SYMBOL = r'[a-zA-Z_]\w*'
    LPAREN = r'\('
    RPAREN = r'\)'
    PLUS = r'\+'
    MINUS = r'\-'
    MULT = r'\*'
    DIV = r'/'

    SYMBOL['defun'] = DEFUN
    
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    def error(self, t):
        print(f'Illegal character {t.value[0]}')
        self.index += 1
   
lexer = LispLexer()
for t in lexer.tokenize(source):
    print(f'{t.type}, {t.value}')

class LispParser(Parser):
    tokens = LispLexer.tokens

    
    @_('expr')
    def program(self, p):
        return ('program', p.expr)

    @_('exprseq expr')
    def exprseq(self, p):
        return p.exprseq + [p.expr]
    
    @_('expr')
    def exprseq(self, p):
        return [p.expr]

    @_('NUMBER')
    def expr(self, p):
        return ('expr', p.NUMBER)
    
    @_('LPAREN op exprseq RPAREN')
    def expr(self, p):
        return ('expr', p.op, p.exprseq)

    """ @_('SYMBOL')
    def expr(self, p):
        return ('expr', p.SYMBOL) """

    @_('PLUS', 'MINUS', 'MULT', 'DIV')
    def op(self, p):
        return ('operator', p[0])


lexer = LispLexer()    
parser = LispParser()

ast = parser.parse(lexer.tokenize(source))
print( ast )
print_ast(ast)

class ASTNode():
    pass

class Operator(ASTNode):

    def __init__(self, op, vals):
        self.op = op
        self.vals = vals

    def eval_node(self):
        total = 0
        if self.op == '+':
            for v in self.vals:
                total += v

        elif self.op == '-':
            total = self.vals[0]
            for v in self.vals[1:]:
                total -= v

        elif self.op == '*':
            total = 1
            for v in self.vals:
                total *= v

        elif self.op == '/':
            total = self.vals[0]
            for v in self.vals[1:]:
                total /= v

        return total

o = Operator('/', [100, 5, 4])
print(o.eval_node())