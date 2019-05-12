# nodes.py
#
# TODO: make all objects for non-terminals
# TODO: NEED defun, setq, if, print

from exceptions import *

#############################333
# Temporary symbol table
###################################
symbol_table = { }

class ASTNode():
    def eval_node(self):
        pass

class Program(ASTNode):

    def __init__(self, expr):
        self.expr = expr

    def eval_node(self):
        return self.expr.eval_node()

class Expr(ASTNode):

    def eval_node(self):
        raise Exception("uh oh")
    
class Assignment(Expr):

    def __init__(self, symbol, expr: Expr):
        self.symbol = symbol
        self.expr = expr

    def eval_node(self):
        expr_val = self.expr.eval_node()
        symbol_table[self.symbol] = expr_val
        return expr_val

class ExprSeq(ASTNode):
    exprs = None

    def __init__(self, exprs: list):
        self.exprs = exprs

class ExprStr(Expr):

    def __init__(self, val: str):
        self.val = val
    
    def eval_node(self):
        return self.val
    
    def __str__(self):
        return self.val

# evaluates to number
class ExprNum(Expr):

    def __init__(self, val: int):
        self.val = val

    def __int__(self):
        return self.val

    def eval_node(self):
        return self.val

    def __add__(self, other):
        # in case other is an int, just add the int so we don't try to access .val
        v = other if type(other) is int else other.val
        #print(f'other ({type(other)}), self ({type(self.val)})')
        return ExprNum(v + self.val)

    __radd__ = __add__

    def __mul__(self, other):
        # in case other is an int, just mult the int so we don't try to access
        # to acess the int's 'val' attribute, which doesn't exist
        v = other if type(other) is int else other.val

        return ExprNum(v * self.val)

    __rmul__ = __mul__

    def __str__(self):
        return str(self.val)

# evaluates to ExprNum
class PrimOp(Expr):

    def __init__(self, op, vals: list):
        self.op = op
        self.vals = vals

    def eval_node(self):
        total = 0
        if self.op == '+':
            for v in self.vals:
                #print(type(v), sys.stderr)
                total += v.eval_node()

        elif self.op == '-':
            total = self.vals[0].eval_node()
            for v in self.vals[1:]:
                total -= v.eval_node()

        elif self.op == '*':
            total = 1
            for v in self.vals:
                #print(f'v: {type(v)}, v.eval_node(): {type(v.eval_node())}, total: {type(total)}')

                total *= v.eval_node()

        elif self.op == '/':
            total = self.vals[0].eval_node()
            for v in self.vals[1:]:
                total = int(total / v.eval_node())

        return ExprNum(total)

#p = Program(PrimOp('+', [ExprNum(10), ExprNum(20), ExprNum(40)]))

#print(p.eval_node())