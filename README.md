
# mlisp - Lisp Interpreter

## What is this?

I've grown to have a big appreciation for languages, language design, and
language implementation. At some point in the near future, I plan on building
a compiler (probably C), but before that, I figured that an interpreter would
be a good way to get familiar with the first half of the compilation process
(lexical analysis and syntactic analysis)

Lisp in an interesting family of languages, in that they aren't very similar to
most of the big languages used in production when in comes to syntax. They do
however act as a great tool for teaching the fundamentals of functional
programming.

I chose to write a Lisp style language because they have a simple syntax, so
it would be a great starting place for someone like me trying to get involved
in language development.

## Ok, but what does this Lisp have?

I've implemented the following:
* Assignment `(setq v 10)`
* Function definition `(defun add10 (x) (+ 10 x))`
* Function calling `(func param1 param2)`
* Types:
    * Integers: `10`, `-5`
    * Strings: `"hello world"`
* If expressions

There are examples in the `tests` directory of this repository

## Quirks

No language is without it's quirks

* There are no booleans, instead we use the classic non-zero = true and zero
= false

## Possible fixes

* Add values to store underlying data type instead of raw python data
* Probably will need to add more comparison operator overloading for all expression types
* type checking for ops and user defined functions
* better errors

Values

Val - Parent class

ValNum - Integer
ValStr - String
ValList - List of Vals
ValFunc - Replace function definition

TODO

lambdaexpr - evaluates to FuncVAl
FuncVal implementation
Document new code
possibly divide into new files??
add better checking of args to PrimOps

add list functions
    last
    init
    reverse
    nth

new prim ops:
    max, min = works on lists and multiple nums
    logical and/or/xor/not