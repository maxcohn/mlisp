"""Exceptions

All the exceptions used for specific cases for the interpreter.
"""

class SymbolNotFound(Exception):
    """Raised when symbol cannot be found in table"""
    pass

class IncorrectNumOfArgs(Exception):
    """Raised when a function call has given the wrong number of arguments"""
    pass
