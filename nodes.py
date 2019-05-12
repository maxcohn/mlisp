# nodes.py
#
# TODO: make all objects for non-terminals
# TODO: NEED defun, if, print

from exceptions import *

#############################333
# Temporary symbol table
###################################
symbol_table = { }

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

class ExprSym(Expr):

    def __init__(self, val):
        self.val = val
    
    def eval_node(self, env):
        v = env.lookup(self.val)

        print(f'symbol: {type(v)}')

        if type(v) is str:
            return ExprStr(v)
        elif type(v) is int:
            return ExprNum(v)
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

        return self.symbol # does this print the name?

class FuncCall(Expr):

    def __init__(self, symbol, args):
        self.symbol = symbol
        self.args = args
    
    def eval_node(self, env):
        func = env.lookup(self.symbol)

        if len(self.args) != len(func.params):
            raise IncorrectNumOfArgs(f'''Function: "{func.symbol}" was given \
                {len(self.args)} arguments, when it takes {len(func.params)}''')
        
        # map param symbols with their given args
        mapping = [ (func.params[i], self.args[i]) for i in range(len(self.args)) ]
        
        new_env = Environment(env)
        for i in range(len(self.args)):
            print(f'adding new symbol: ({func.params[i]},{self.args[i]})')
            new_env.add_symbol(func.params[i], self.args[i])
        
        print(f'new_env: {new_env.symbol_table}')
        return func.expr.eval_node(new_env)

# evaluates to ExprNum
class PrimOp(Expr):

    def __init__(self, op, vals: list):
        self.op = op
        self.vals = vals

    def eval_node(self, env):
        total = 0
        if self.op == '+':
            for v in self.vals:
                #print(type(v), sys.stderr)
                print(f'v = {type(v.val)}')
                print(f'v.eval_node(env) = {v.eval_node(env)}')
                print(f'env = {env.symbol_table}')
                total += v.eval_node(env)

        elif self.op == '-':
            total = self.vals[0].eval_node(env)
            for v in self.vals[1:]:
                total -= v.eval_node(env)

        elif self.op == '*':
            total = 1
            for v in self.vals:
                #print(f'v: {type(v)}, v.eval_node(env): {type(v.eval_node(env))}, total: {type(total)}')

                total *= v.eval_node(env)

        elif self.op == '/':
            total = self.vals[0].eval_node(env)
            for v in self.vals[1:]:
                total = int(total / v.eval_node(env))

        return ExprNum(total)

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

        #print(f'symbol:{self.symbol}, val:{expr_val}')
        env.add_symbol(self.symbol, expr_val)

        return expr_val

#p = Program(PrimOp('+', [ExprNum(10), ExprNum(20), ExprNum(40)]))

#print(p.eval_node(env))



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
    
    def print_table(self):
        print(self.symbol_table)
        
