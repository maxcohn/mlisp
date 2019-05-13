"""Lexer and Parser

This file contains the lexer and parser for the interpreter
"""

from sly import Lexer, Parser
from nodes import *
from exceptions import *

# Current goals: IF statements, print

class LispLexer(Lexer):
    """Lexer for this Lisp interpreter (using SLY)"""

    tokens = {LPAREN, RPAREN, NUMBER, SYMBOL, DEFUN, PLUS,
        MINUS, MULT, DIV, SETQ, STRING, IF, GT, LT, GTEQ,
        LTEQ, EQ, NEQ, PRINT
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
    GTEQ = r'>='
    LTEQ = r'<='
    GT = r'>'
    LT = r'<'
    EQ = r'=='
    NEQ = r'!='

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
   
class LispParser(Parser):
    """Parser for the lisp interpreter (using SLY)
    
    This class holds all our grammar rules, which in turn call functions to
    build an abstract syntax tree
    """

    tokens = LispLexer.tokens
 
    @_('expr')
    def program(self, p):
        return Program(p.expr)

    ############################################################
    # Expressions
    ############################################################
    @_('NUMBER')
    def expr(self, p):
        return ExprNum(p.NUMBER)

    @_('STRING')
    def expr(self, p):
        return ExprStr(p[0])

    @_('SYMBOL')
    def expr(self, p):
        # lookup symbol and return if exists, otherwise, raise exception
        return ExprSym(p.SYMBOL)
        
    # same idea here with renaming?
    @_('LPAREN funcdef RPAREN')
    def expr(self, p):
        return p.funcdef

    @_('LPAREN funccall RPAREN')
    def expr(self, p):
        return p.funccall

    @_('LPAREN assignment RPAREN')
    def expr(self, p):
        return p.assignment

    @_('LPAREN ifexpr RPAREN')
    def expr(self, p):
        return p.ifexpr
    
    @_('LPAREN printexpr RPAREN')
    def expr(self, p):
        return p.printexpr

    @_('exprseq expr')
    def exprseq(self, p):
        return p.exprseq + [p.expr]
    
    @_('expr')
    def exprseq(self, p):
        return [p.expr]

    ############################################################
    # Functions
    ############################################################

    @_('SETQ SYMBOL expr')
    def assignment(self, p):
        return Assignment(p.SYMBOL, p.expr)

    @_('PLUS', 'MINUS', 'MULT', 'DIV', 'GT', 'LT',
        'LTEQ', 'GTEQ', 'EQ', 'NEQ'
    )
    def op(self, p):
        return p[0]
    
    #TODO change to return an object instead of a string??
    @_('SYMBOL')
    def param(self, p):
        return p.SYMBOL

    @_('paramseq param')
    def paramseq(self, p):
        return p.paramseq + [p.param]

    @_('param')
    def paramseq(self, p):
        return [p.param]

    @_('LPAREN paramseq RPAREN')
    def paramlist(self, p):
        return p.paramseq
        

    @_('DEFUN SYMBOL paramlist expr')
    def funcdef(self, p):
        return FuncDef(p.SYMBOL, p.paramlist, p.expr)

    @_('SYMBOL exprseq')
    def funccall(self, p):
        return FuncCall(p.SYMBOL, p.exprseq)

    @_('op exprseq')
    def funccall(self, p):
        return PrimOp(p.op, p.exprseq)

    @_('IF expr expr expr')
    def ifexpr(self, p):
        return IfExpr(p.expr0, p.expr1, p.expr2)

    @_('PRINT expr')
    def printexpr(self, p):
        return PrintExpr(p.expr)
