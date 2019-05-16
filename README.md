
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
    * Functions
    * Lists: `(list 1 2 3 4 5)`
* If expressions: `(if cond then else)`

There are examples in the `examples` directory of this repository

## Quirks

No language is without it's quirks

* There are no booleans, instead we use numbers to represent (similar to C)

## Primitive operations

`+`, `-`, `/`, `*` - Arithmetic operators (2+ numbers)

`>`, `<`, `<=`, `>=`, `==`, `!=` - Comparison operators (2 numbers)

`print` - Prints given value (1 value)

`list` - Creates a list (1+ values)

`head` - Returns first element of list (1 list)

`tail` - Returns list of all elements but first (1 list)

`length` - Returns length of list (1 list)

`append` - Appends given value to list (1 list, value)

`splice` - Returns list spliced by parameters (list, start, end)

## Possible fixes

* Probably will need to add more comparison operator overloading for all expression types
* type checking for ops and user defined functions
* better errors


### TODO
lambdaexpr - evaluates to FuncVAl

Document new code

possibly divide into new files??

add better checking of args to PrimOps

add list functions
    last
    init
    reverse
    nth
