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
        self.val = StrVal(val[1:-1]) #remove quotes from string
    
    def eval_node(self, env):
        return self.val
    
    def __str__(self):
        return f'"{self.val}"'

# evaluates to number
class ExprNum(Expr):
    """Number expression"""
    def __init__(self, val: int):
        self.val = NumVal(val)

    def __int__(self):
        return self.val

    def eval_node(self, env):
        return self.val

    # The following are operation overloaders for dealing with adding ExprNums
    def __add__(self, other):
        #TODO remove
        raise Exception('THIS SHOULD BE HAPPENING: ExprNum __add__()')
        # in case other is an int, just add the int so we don't try to access .val
        v = other if type(other) is int else other.val

        return ExprNum(v + self.val)

    __radd__ = __add__

    def __sub__(self, other):
        #TODO remove
        raise Exception('THIS SHOULD BE HAPPENING: ExprNum __sub__()')
        v = other if type(other) is int else other.val

        return ExprNum(self.val - v)
    
    def __rsub__(self, other):
        #TODO remove
        raise Exception('THIS SHOULD BE HAPPENING: ExprNum __rsum__()')
        v = other if type(other) is int else other.val

        return ExprNum(v - self.val)


    def __mul__(self, other):
        #TODO remove
        raise Exception('THIS SHOULD BE HAPPENING: ExprNum __mul__()')

        # in case other is an int, just mult the int so we don't try to access
        # to acess the int's 'val' attribute, which doesn't exist
        v = other if type(other) is int else other.val

        return ExprNum(v * self.val)

    __rmul__ = __mul__

    def __str__(self):
        return str(self.val)

    ##TODO REMOVE ALL BELOW
    # The following are overloaded comparison operators for dealing with ExprNums
    def __gt__(self, other):
        #TODO remove
        raise Exception('THIS SHOULD BE HAPPENING: ExprNum comparison operator')
        return self.val > other.val

    def __ge__(self, other):
        #TODO remove
        raise Exception('THIS SHOULD BE HAPPENING: ExprNum comparison operator')
        return self.val >= other.val

    def __lt__(self, other):
        #TODO remove
        raise Exception('THIS SHOULD BE HAPPENING: ExprNum comparison operator')
        return self.val < other.val
    
    def __le__(self, other):
        #TODO remove
        raise Exception('THIS SHOULD BE HAPPENING: ExprNum comparison operator')
        if isinstance(other, Expr):
            return self.val <= other.val

        return self.val <= other

    def __eq__(self, other):
        #TODO remove
        raise Exception('THIS SHOULD BE HAPPENING: ExprNum comparison operator')
        if isinstance(other, Expr):
            return self.val == other.val

        return self.val == other

    def __ne__(self, other):
        #TODO remove
        raise Exception('THIS SHOULD BE HAPPENING: ExprNum comparison operator')
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

        return v

        """TODO remove
        # depending on the stype that the value is, return a different expression type
        if type(v) is str:
            return ExprStr(v)
        elif type(v) is int:
            return ExprNum(v)
        elif type(v) is list:
            return ListExpr(v)
        elif isinstance(v, ExprSym):
            return self.eval_node(env)
        elif isinstance(v, Expr):
            return v
        """
        
        raise Exception("Symbol was wasn't a valid type")

############################################################
# Functions
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

    # list of list operators
    _list_op = ['head', 'tail', 'append', 'splice']

    def __init__(self, op, vals: list):
        self.op = op
        self.vals = vals # Expression sequence


    def _arithmatic_eval(self, env):
        """Evaluates an arithmatic operator"""
        total = NumVal(0)
        if self.op == '+':
            for v in self.vals:
                total += v.eval_node(env)

        elif self.op == '-':
            total = self.vals[0].eval_node(env)
            for v in self.vals[1:]:
                total -= v.eval_node(env)

        elif self.op == '*':
            total = NumVal(1)
            for v in self.vals:
                total *= v.eval_node(env)

        elif self.op == '/':
            total = self.vals[0].eval_node(env)
            for v in self.vals[1:]:
                total = total // v.eval_node(env)

        return total#ExprNum(total)

    def _comparison_eval(self, env):
        # evaluates a comparison operator

        # check to make sure there are only two values
        if len(self.vals) != 2:
            raise IncorrectNumOfArgs(f'Operation "{self.op}" takes 2 arguments')

        val0 = self.vals[0]
        val1 = self.vals[1]
        if self.op == '>':
            return NumVal(1 if val0.eval_node(env) > val1.eval_node(env) else 0)
        elif self.op == '<':
            return NumVal(1 if val0.eval_node(env) < val1.eval_node(env) else 0)
        elif self.op == '<=':
            return NumVal(1 if val0.eval_node(env) <= val1.eval_node(env) else 0)
        elif self.op == '>=':
            return NumVal(1 if val0.eval_node(env) >= val1.eval_node(env) else 0)
        elif self.op == '==':
            return NumVal(1 if val0.eval_node(env) == val1.eval_node(env) else 0)
        elif self.op == '!=':
            return NumVal(1 if val0.eval_node(env) != val1.eval_node(env) else 0)

    def _list_eval(self, env):
        """TODO UNCOMMENT AFTER VALS IMPLEMENTED
        if self.op == 'head':
            if len(self.vals) == 0:
                raise IncorrectNumOfArgs("head takes a list as it's argument")

            print(f'DEBUG: self.vals={self.vals}')
            print(f'DEBUG: self.vals[0]={self.vals[0]}')
            return ListExpr(self.vals[0].vals)
            
        elif self.op == 'tail':
            pass
        elif self.op == 'append':
            pass
        elif self.op == 'splice':
            pass #TODO
        """

    def eval_node(self, env):
        # check if the given op was an arithmatic operator or a comparison operator
        if self.op in self._arithmatic_op:
            return self._arithmatic_eval(env)

        elif self.op in self._comparison_op:
            return self._comparison_eval(env)

        elif self.op in self._list_op:
            return self._list_eval(env)

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
        if self.cond.eval_node(env) != NumVal(0):
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

class ListExpr(Expr):
    """List expression"""

    def __init__(self, exprseq):
        self.raw_vals = exprseq

        # if the ListExpr is being made by ExprSym, we give it raw data only, so
        # we can take it for what it is, else, we don't have real values yet.
        # exprseq will always have expressions if it comes from parsing
        #self.vals = []

    def eval_node(self, env):
        val_list = []

        # get the raw value of each expression
        for e in self.raw_vals:
            v = e
            while isinstance(v, Expr):
                v = v.eval_node(env)

            val_list.append(v)

        #self.vals = val_list
        #print(self.vals)
        return ListVal(val_list)

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


"""
Value replacement classes:

---------------------ExprStr
----------------------ExprNum
-----------------------ExprSym
FuncDef - eval_node() should create a func val
FuncCall - eval_node() should retrieve FuncVal from evnironment
----------------------PrimOp -
PrintExpr - handle printing of values (__str__ in values?)
Environment - holds symbol:Val pairs
"""
class Val():
    """Value object base class"""

    def __init__(self, val):
        raise NotImplementedError('Cannot call constructor for Val base class')
        
class NumVal(Val):
    """Value wrapper for integers"""

    def __init__(self, val: int):
        if type(val) is not int:
            raise ValNotIntendedType(f'Given value is not a NumVal')

        self.val = val

    def __add__(self, other):
        return NumVal(self.val + other.val)
    
    def __sub__(self, other):
        return NumVal(self.val - other.val)
    
    def __mul__(self, other):
        return NumVal(self.val * other.val)
    
    def __floordiv__(self, other):
        return NumVal(self.val // other.val)
    
    def __truediv__(self, other):
        return NumVal(self.val // other.val)

    def __gt__(self, other):
        return self.val > other.val

    def __lt__(self, other):
        return self.val < other.val

    def __le__(self, other):
        return self.val <= other.val

    def __ge__(self, other):
        return self.val >= other.val
    
    def __eq__(self, other):
        return self.val == other.val
    
    def __ne__(self, other):
        return self.val != other.val

    def __str__(self):
        return str(self.val)

class StrVal(Val):
    """Value wrapper for strings"""

    def __init__(self, val):
        if type(val) is not str:
            raise ValNotIntendedType(f'Given value is not a StrVal')

        self.val = val
    
    def __str__(self):
        return self.val

class ListVal(Val):
    """Value wrapper for lists"""
    def __init__(self, val):
        if type(val) is not list:
            raise ValNotIntendedType(f'Given value is not a ListVal')

        self.val = val

    def head(self):
        return self.val[0]

    def tail(self):
        return self.val[1:]
        
    def __str__(self):
        s = "("
        for v in self.val:
            s += str(v) + ' '
        
        return str(s[:-1] + ')')

class NilVal(Val):
    """Nil value representation"""
    def __init__(self):
        pass
