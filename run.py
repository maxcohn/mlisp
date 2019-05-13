"""Runs a lisp program

Accepts a lisp program via the first argument and runs it
"""


import sys

if __name__ == "__main__":
    source = None

    with open(sys.argv[1]) as f:
        source = f.read()

    print(source)