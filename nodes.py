"""Abstract Syntax Tree Nodes

All the nodes used to construct an abstract syntax tree
"""

from vals import *
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

    def __str__(self):
        return str(self.val)

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
        self.val = FuncVal(params, expr)
    
    def eval_node(self, env):
        # Add the symbol that is the function name to the current environment,
        # and the make its associated value this object
        env.add_symbol(self.symbol, self.val)
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
    _list_op = ['head', 'tail', 'append', 'splice', 'length', 'nth']

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
        if self.op == 'head':
            if len(self.vals) != 1:
                raise IncorrectNumOfArgs("head takes a list as it's argument")

            new_val = self.vals[0].eval_node(env)
            if not new_val.islist():
                raise ValNotIntendedType("head takes a list as it's argument")

            return new_val.head()
            
        elif self.op == 'tail':
            if len(self.vals) != 1:
                raise IncorrectNumOfArgs("tail takes a list as it's argument")
            
            new_val = self.vals[0].eval_node(env)

            if not new_val.islist():
                raise ValNotIntendedType("head takes a list as it's argument")
                
            return new_val.tail()            

        elif self.op == 'append':
            if len(self.vals) != 2:
                raise IncorrectNumOfArgs("append takes a list and a value as it's arguments")

            new_vals = [v.eval_node(env) for v in self.vals]

            if not new_vals[0].islist():
                raise ValNotIntendedType("append takes a list and a value as it's arguments")
            
            return new_vals[0].append(new_vals[1])

        elif self.op == 'splice':
            if len(self.vals) != 3:
                #TODO fix these error messages
                raise IncorrectNumOfArgs("""splice takes a list, a start index,\
                    and an end index for it's arguments""")

            new_vals = [v.eval_node(env) for v in self.vals]
            
            if not (new_vals[0].islist() and new_vals[1].isnum() and new_vals[2].isnum()):
                raise ValNotIntendedType("""splice takes a list, a start index,\
                    and an end index for it's arguments""")
            
            return new_vals[0].splice(new_vals[1], new_vals[2])
        elif self.op == 'length':
            if len(self.vals) != 1:
                raise IncorrectNumOfArgs("length takes a list as it's argument")
            
            new_val = self.vals[0].eval_node(env)

            if not new_val.islist():
                raise ValNotIntendedType("length takes a list as it's argument")

            return new_val.length()
        elif self.op == 'nth':
            if len(self.vals) != 2:
                raise IncorrectNumOfArgs("nth takes a list and an index as it's argument")

            new_vals = [v.eval_node(env) for v in self.vals]

            if not (new_vals[0].islist() or new_vals[1].isnum()):
                raise ValNotIntendedType("nth takes a list and an index as it's argument")
            
            return new_vals[0].nth(new_vals[1])


    def eval_node(self, env):
        # check if the given op was an arithmatic operator or a comparison operator
        if self.op in self._arithmatic_op:
            return self._arithmatic_eval(env)

        elif self.op in self._comparison_op:
            return self._comparison_eval(env)

        elif self.op in self._list_op:
            return self._list_eval(env)

class Assignment(Expr):
    """Assignment expression
    
    Upon evaluation, the given symbol is added to the given environment with
    it's value being the result of the given expression.
    """

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
    """If expression
    
    Given three expressions, a condition, and two actions. The condition is
    evaluated to a boolean expression. If the expression is true, we use the
    first action, otherwise, we use the second action.
    """

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
    """Print expression
    
    Evaluates the given expression, prints the result, and then returns it.
    """
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

