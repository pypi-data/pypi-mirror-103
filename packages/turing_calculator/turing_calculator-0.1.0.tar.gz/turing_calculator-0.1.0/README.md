# Simple Calculator

## What is this?

A pretty straight forward calculator for Python that can do the following:

* Stores current value of number until it is reset
* Addition / Subtraction
* Multiplication / Division
* Calculate nth root of a number

## Installation:

`pip install turing_calculator`

## Usage

`from turing_calculator import Calculator`
Initialise:
`calc = Calculator()`
Add 5 to current value:
`calc.add(5)`
Subtract 3:
`calc.subtract(3)`
Multiply by 25:
`calc.multiply(25)`
Divide by 2:
`calc.divide(2)`
Nth Root (In this case, square root):
`calc.root(2)`
Current Value:
`calc.val`
Reset to zero:
`calc.reset()`