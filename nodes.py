"""Abstract Syntax Tree Nodes

All the nodes used to construct an abstract syntax tree
"""

# nodes.py
#
# TODO: NEED  if, print, empty param list (new grammar rule)
#TODO: comparisons: <,>,<=,>=,==, !=

from exceptions import *

class ASTNode():
    def eval_node(self, env):
        pass

class Program(ASTNode):

    def __init__(self, expr):
        self.expr = expr

    def eval_node(self, env):
        return self.expr.eval_node(env)

############################################################
# Expressions
############################################################
class Expr(ASTNode):

    def eval_node(self, env):
        raise Exception("uh oh")


class ExprSeq(ASTNode):
    exprs = None

    def __init__(self, exprs: list):
        self.exprs = exprs

class ExprStr(Expr):

    def __init__(self, val: str):
        self.val = val
    
    def eval_node(self, env):
        return self.val
    
    def __str__(self):
        return self.val

# evaluates to number
class ExprNum(Expr):

    def __init__(self, val: int):
        self.val = val

    def __int__(self):
        return self.val

    def eval_node(self, env):
        return self.val

    def __add__(self, other):
        # in case other is an int, just add the int so we don't try to access .val
        v = other if type(other) is int else other.val

        return ExprNum(v + self.val)

    __radd__ = __add__

    def __sub__(self, other):
        v = other if type(other) is int else other.val

        return ExprNum(self.val - v)
    
    def __rsub__(self, other):
        v = other if type(other) is int else other.val

        return ExprNum(v - self.val)


    def __mul__(self, other):
        # in case other is an int, just mult the int so we don't try to access
        # to acess the int's 'val' attribute, which doesn't exist
        v = other if type(other) is int else other.val

        return ExprNum(v * self.val)

    __rmul__ = __mul__

    def __str__(self):
        return str(self.val)

    def __gt__(self, other):
        return self.val > other.val

    def __ge__(self, other):
        return self.val >= other.val

    def __lt__(self, other):
        return self.val < other.val
    
    def __le__(self, other):
        if isinstance(other, Expr):
            return self.val <= other.val

        return self.val <= other

    def __eq__(self, other):
        return self.val == other.val

    def __ne__(self, other):
        if isinstance(other, Expr):
            return self.val != other.val

        return self.val != other



class ExprSym(Expr):

    def __init__(self, val):
        self.val = val
    
    def eval_node(self, env):
        v = env.lookup(self.val)

        if type(v) is str:
            return ExprStr(v)
        elif type(v) is int:
            return ExprNum(v)
        elif isinstance(v, ExprSym):
            return self.eval_node(env)
        elif isinstance(v, Expr):
            return v

############################################################
# Expressions
############################################################
class FuncDef(ASTNode):
    
    def __init__(self, symbol, params, expr):
        self.symbol = symbol
        self.params = params
        self.expr = expr
    
    def eval_node(self, env):
        env.add_symbol(self.symbol, self)

        return self.symbol

class FuncCall(Expr):

    def __init__(self, symbol, args):
        self.symbol = symbol
        self.args = args
    
    def eval_node(self, env):
        func = env.lookup(self.symbol)

        if len(self.args) != len(func.params):
            raise IncorrectNumOfArgs(f'''Function: "{func.symbol}" was given \
                {len(self.args)} arguments, when it takes {len(func.params)}''')
        
        new_env = Environment(env)
        for i in range(len(self.args)):
            new_env.add_symbol(func.params[i], self.args[i].eval_node(env))
        
        return func.expr.eval_node(new_env)

# evaluates to ExprNum
class PrimOp(Expr):

    _comparison_op = ['>', '<', '<=', '>=', '==', '!=']

    _arithmatic_op = ['+', '/', '-', '*']

    def __init__(self, op, vals: list):
        self.op = op
        self.vals = vals

    def _arithmatic_eval(self, env):
        total = 0
        if self.op == '+':
            for v in self.vals:
                total += v.eval_node(env)

        elif self.op == '-':
            total = self.vals[0].eval_node(env)
            for v in self.vals[1:]:
                total -= v.eval_node(env)

        elif self.op == '*':
            total = 1
            for v in self.vals:
                total *= v.eval_node(env)

        elif self.op == '/':
            total = self.vals[0].eval_node(env)
            for v in self.vals[1:]:
                total = int(total / v.eval_node(env))

        return ExprNum(total)

    def _comparison_eval(self, env):
        # check to make sure there are only two values
        if len(self.vals) != 2:
            raise IncorrectNumOfArgs(f'Operation "{self.op}" takes 2 arguments')

        if self.op == '>':
            return ExprNum(1 if self.vals[0].eval_node(env) > self.vals[1].eval_node(env) else 0)
        elif self.op == '<':
            return ExprNum(1 if self.vals[0].eval_node(env) < self.vals[1].eval_node(env) else 0)
        elif self.op == '<=':
            return ExprNum(1 if self.vals[0].eval_node(env) <= self.vals[1].eval_node(env) else 0)
        elif self.op == '>=':
            return ExprNum(1 if self.vals[0].eval_node(env) >= self.vals[1].eval_node(env) else 0)
        elif self.op == '==':
            return ExprNum(1 if self.vals[0].eval_node(env) == self.vals[1].eval_node(env) else 0)
        elif self.op == '!=':
            return ExprNum(1 if self.vals[0].eval_node(env) != self.vals[1].eval_node(env) else 0)


    def eval_node(self, env):
        
        if self.op in self._arithmatic_op:
            return self._arithmatic_eval(env)

        elif self.op in self._comparison_op:
            return self._comparison_eval(env)

class Assignment(Expr):

    def __init__(self, symbol, expr: Expr):
        self.symbol = symbol
        self.expr = expr

    def eval_node(self, env):
        expr_val = self.expr.eval_node(env)

        while isinstance(expr_val, Expr):    
            expr_val = expr_val.eval_node(env)

        # if expr_val is a string, remove the quotes
        if type(expr_val) is str:
            expr_val = expr_val[1:-1]

        env.add_symbol(self.symbol, expr_val)

        return expr_val

class IfExpr(Expr):

    def __init__(self, cond, act1, act2):
        self.cond = cond
        self.act1 = act1
        self.act2 = act2

    def eval_node(self, env):
        if self.cond.eval_node(env) != (0):
            return self.act1.eval_node(env)
        
        return self.act2.eval_node(env)
        




class Environment():
    
    symbol_table = { }

    def __init__(self, prev):
        self.prev_env = prev

    def lookup(self, symbol: str):
        if symbol not in self.symbol_table:
            if self.prev_env is not None:
                return self.prev_env.lookup(symbol)

            raise SymbolNotFound(f'Symbol: "{symbol}" not found')

        return self.symbol_table[symbol]

    def add_symbol(self, symbol: str, val):
        self.symbol_table[symbol] = val

        
