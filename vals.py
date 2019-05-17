
from exceptions import *

class Val():
    """Value object base class"""

    def __init__(self, val):
        raise NotImplementedError('Cannot call constructor for Val base class')
    
    def islist(self):
        return isinstance(self, ListVal)

    def isnum(self):
        return isinstance(self, NumVal)

    def isstr(self):
        return isinstance(self, StrVal)
    
    def isfunc(self):
        return isinstance(self, FuncVal)
        
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
    
    def __int__(self):
        return self.val

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
        return ListVal(self.val[1:])

    def append(self, new_val: Val):
        new_list = [ v for v in self.val ]
        new_list.append(new_val)
        return ListVal(new_list)

    def splice(self, start: NumVal, end: NumVal):
        return ListVal(self.val[int(start):int(end)])
    
    def length(self):
        return NumVal(len(self.val))
        
    def __str__(self):
        if len(self.val) == 0:
            return '()'
        
        s = "("
        for v in self.val:
            s += str(v) + ' '
        
        return str(s[:-1] + ')')

class FuncVal(Val):

    def __init__(self, params, expr):
        self.params = params
        self.expr = expr

class NilVal(Val):
    """Nil value representation"""
    def __init__(self):
        pass
