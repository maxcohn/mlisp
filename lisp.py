from sly import Lexer, Parser
from nodes import *
from exceptions import *

# Current goals:
# Primative operations: +, -, *, /
# Evaluation of syntax tree (maybe save things as objects)


source = '"hello world"'#'(+ 10 (- 50 30))'
#source = '(+ 10 20 40)'
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
        MINUS, MULT, DIV, SETQ, IF, STRING, PRINT
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
    STRING = '"[^"]*"'

    SYMBOL['defun'] = DEFUN
    SYMBOL['setq'] = SETQ
    SYMBOL['if'] = IF
    SYMBOL['print'] = PRINT
    
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    def error(self, t):
        print(f'Illegal character {t.value[0]}')
        self.index += 1
   
#lexer = LispLexer()
#for t in lexer.tokenize(source):
#    print(f'{t.type}, {t.value}')

class LispParser(Parser):
    tokens = LispLexer.tokens

    
    @_('expr')
    def program(self, p):
        return Program(p.expr)

    @_('exprseq expr')
    def exprseq(self, p):
        return p.exprseq + [p.expr]
    
    @_('expr')
    def exprseq(self, p):
        return [p.expr]

    @_('NUMBER')
    def expr(self, p):
        return ExprNum(p.NUMBER)
    
    @_('LPAREN op exprseq RPAREN')
    def expr(self, p):
        return PrimOp(p.op, p.exprseq)

    @_('STRING')
    def expr(self, p):
        return ExprStr(p[0])

    @_('SYMBOL')
    def expr(self, p):
        # lookup symbol and return if exists, otherwise, raise exception
        if p.SYMBOL not in symbol_table:
            raise SymbolNotFoundException(f'Symbol "{p.SYMBOL}" was not found')
        
        val = symbol_table[p.SYMBOL]
        if type(val) is str:
            return ExprStr(val)
        elif type(val) is int:
            return ExprNum(val)
        
        raise Exception('uh oh, thats not a valid symbol')
        

    @_('PLUS', 'MINUS', 'MULT', 'DIV')
    def op(self, p):
        return p[0]
    
    @_('LPAREN SETQ SYMBOL expr RPAREN')
    def expr(self, p):
        symbol_table[p.SYMBOL] = p.expr
        return Assignment(p.SYMBOL, p.expr)
    


lexer = LispLexer()    
parser = LispParser()



source = '(* (+ 10 (+ 100 20) (/ 10 5)) 50)'

ast = parser.parse(lexer.tokenize(source))
#print( ast )
#print_ast(ast)


#o = Operator('/', [100, 5, 4])
#print(ast.eval_node())

