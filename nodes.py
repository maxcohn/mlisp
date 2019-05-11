# nodes.py
#
# TODO: make all objects for non-terminals
# TODO: NEED defun, setq, if, strings, print

from typing import List


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

    def eval_node(self):
        return self.val

    def __add__(self, other):
        return ExprNum(other + self.val)

    def __str__(self):
        return str(self.val)

# evaluates to ExprNum
class PrimOp(Expr):

    def __init__(self, op, vals: list):
        self.op = op
        self.vals = vals

    def eval_node(self):
        total = ExprNum(0)
        if self.op == '+':
            for v in self.vals:
                total += v.eval_node()

        elif self.op == '-':
            total = self.vals[0].eval_node()
            for v in self.vals[1:]:
                total -= v.eval_node()

        elif self.op == '*':
            total = Expr(1)
            for v in self.vals:
                total *= v.eval_node()

        elif self.op == '/':
            total = self.vals[0].eval_node()
            for v in self.vals[1:]:
                total /= v.eval_node()

        return ExprNum(total)

p = Program(PrimOp('+', [ExprNum(10), ExprNum(20), ExprNum(40)]))

print(p.eval_node())