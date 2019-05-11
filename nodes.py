# nodes.py
#
# TODO: make all objects for non-terminals
from typing import List


class ASTNode():
    def eval_node(self):
        pass



class Expr(ASTNode):
    val = None

    def eval_node(self):
        pass
    

class ExprSeq(ASTNode):
    exprs = None

    def __init__(self, exprs: list):
        self.exprs = exprs

# evaluates to integer
class ExprNum(Expr):

    def __init__(self, val):
        self.val = val

    def eval_node(self):
        return self.val

# evaluates to ExprNum
class PrimOp(Expr):

    def __init__(self, op, vals: list):
        self.op = op
        self.vals = vals

    def eval_node(self):
        total = 0
        if self.op == '+':
            for v in self.vals:
                total += v.eval_node()

        elif self.op == '-':
            total = self.vals[0].eval_node()
            for v in self.vals[1:]:
                total -= v.eval_node()

        elif self.op == '*':
            total = 1
            for v in self.vals:
                total *= v.eval_node()

        elif self.op == '/':
            total = self.vals[0].eval_node()
            for v in self.vals[1:]:
                total /= v.eval_node()

        return ExprNum(total)

p = PrimOp('+', [ExprNum(100), ExprNum(20), ExprNum(30)])

print(p.eval_node().val)