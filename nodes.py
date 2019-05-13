"""Abstract Syntax Tree Nodes

All the nodes used to construct an abstract syntax tree
"""

# nodes.py
#
# TODO: NEED print, empty param list (new grammar rule)

from exceptions import *

class ASTNode():
    """Base class for all abstract syntax tree nodes"""

    def eval_node(self, env):
        """Evaluation function that all ASTNodes must implement"""
        raise NotImplementedError("This node doesn't implement eval_node()")
        

class Program(ASTNode):
    """Starting node for all abstract syntax trees"""
    def __init__(self, exprs):
        self.exprs = exprs

    def eval_node(self, env):
        v = None
        for e in self.exprs:
            v = e.eval_node(env)
        return v

############################################################
# Expressions
############################################################
class Expr(ASTNode):
    """Base class for all expression nodes"""

    def eval_node(self, env):
        raise NotImplementedError("This node doesn't implement eval_node()")


class ExprSeq(ASTNode):
    """Sequence of expressions (multiple expressions stored as a list"""
    def __init__(self, exprs: list):
        self.exprs = exprs

class ExprStr(Expr):
    """String expression"""
    def __init__(self, val: str):
        self.val = val#[1:-1] # remove quotes from string
    
    def eval_node(self, env):
        return self.val[1:-1]
    
    def __str__(self):
        return self.val

# evaluates to number
class ExprNum(Expr):
    """Number expression"""
    def __init__(self, val: int):
        self.val = val

    def __int__(self):
        return self.val

    def eval_node(self, env):
        return self.val

    # The following are operation overloaders for dealing with adding ExprNums
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

    # The following are overloaded comparison operators for dealing with ExprNums
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
        if isinstance(other, Expr):
            return self.val == other.val

        return self.val == other

    def __ne__(self, other):
        if isinstance(other, Expr):
            return self.val != other.val

        return self.val != other

class ExprSym(Expr):
    """Expression for storing a symbol"""
    def __init__(self, val):
        self.val = val
    
    def eval_node(self, env):
        # A symbol is essentially a variable, so to retrieve it's value,
        # we have to check in the environment
        v = env.lookup(self.val)


        # depending on the stype that the value is, return a different expression type
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
    """The definition of a user defined function"""

    def __init__(self, symbol, params, expr):
        self.symbol = symbol
        self.params = params
        self.expr = expr
    
    def eval_node(self, env):
        # Add the symbol that is the function name to the current environment,
        # and the make its associated value this object
        env.add_symbol(self.symbol, self)
        return self.symbol

class FuncCall(Expr):
    """Call to a user defined funtion"""

    def __init__(self, symbol, args):
        self.symbol = symbol
        self.args = args
    
    def eval_node(self, env):
        # look up FuncDef object associated with the function name
        func = env.lookup(self.symbol)

        # check to make sure the correct number of arguments were given to the function
        if len(self.args) != len(func.params):
            raise IncorrectNumOfArgs(f'''Function: "{func.symbol}" was given \
                {len(self.args)} arguments, when it takes {len(func.params)}''')
        
        # create a new enviornment and populate it with the given arguments
        new_env = Environment(env)
        for i in range(len(self.args)):
            new_env.add_symbol(func.params[i], self.args[i].eval_node(env))
        
        # run the FuncDef's expression with the new environment
        return func.expr.eval_node(new_env)

# evaluates to ExprNum
class PrimOp(Expr):
    """Primative operation node
    
    A primative operation include the basic arithmatic operations and arithmatic
    operations. All PrimOps evaluate to ExprNum.
    """

    # list of comparison operators
    _comparison_op = ['>', '<', '<=', '>=', '==', '!=']

    # list of arithmatic operators
    _arithmatic_op = ['+', '/', '-', '*']

    def __init__(self, op, vals: list):
        self.op = op
        self.vals = vals


    def _arithmatic_eval(self, env):
        """Evaluates an arithmatic operator"""
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
        # evaluates a comparison operator

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
        # check if the given op was an arithmatic operator or a comparison operator
        if self.op in self._arithmatic_op:
            return self._arithmatic_eval(env)

        elif self.op in self._comparison_op:
            return self._comparison_eval(env)

class Assignment(Expr):
    """Assignment expression"""

    def __init__(self, symbol, expr: Expr):
        self.symbol = symbol
        self.expr = expr

    def eval_node(self, env):
        # get the value of the given expression 
        expr_val = self.expr.eval_node(env)

        while isinstance(expr_val, Expr):    
            expr_val = expr_val.eval_node(env)

        # add new symbol to the environment with it's new value
        env.add_symbol(self.symbol, expr_val)

        return expr_val

class IfExpr(Expr):
    """If expression"""

    def __init__(self, cond, act1, act2):
        # condition, followed by 'then' and 'else'
        self.cond = cond
        self.act1 = act1
        self.act2 = act2

    def eval_node(self, env):

        # if the condition evaluates to true (non-zero)
        if self.cond.eval_node(env) != (0):
            return self.act1.eval_node(env)
        
        # else
        return self.act2.eval_node(env)
        
class PrintExpr(Expr):
    """Print expression"""
    def __init__(self, expr: Expr):
        self.expr = expr
    
    def eval_node(self, env):
        # calculate valye of node, print, and then return
        v = self.expr.eval_node(env)
        print(v)
        return v



class Environment():
    """Evnironment of symbols

    Contains bindings for symbols and their values for each environment.
    Environments are chained together so that we can emulate scope without
    overwriting symbol values.
    """
    
    # I'm leaving this line here as a permanent reminder as to how this creates
    # a static variable. I've been tainted by my beloved C# and Java and though
    # that this created an instance variable.
    #symbol_table = { }

    def __init__(self, prev):
        self.prev_env = prev
        self.symbol_table = {}

    def lookup(self, symbol: str):
        """Check if the given symbol is in the environment chain
        
        Parameters
        ----------
        symbol : str
            Symbol being looks for in the environment chain
        """

        # if the symbol isn't in the current table
        if symbol not in self.symbol_table:
            # check the next environment
            if self.prev_env is not None:
                return self.prev_env.lookup(symbol)
            # if it wasn't in any, raise an exception
            raise SymbolNotFound(f'Symbol: "{symbol}" not found')

        return self.symbol_table[symbol]

    def add_symbol(self, symbol: str, val):
        """Add a new symbol to the current environment
        
        Parameters
        ----------
        symbol : str
            Symbol being bound to val
        val
            Value being found to symbol
        """
        self.symbol_table[symbol] = val

    