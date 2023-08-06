Algebra generator that can easily create algebra equations in the Ax + b = C format. It can also solve equations in Ax + b = C. Right now, only the operations, '-' and '+' are supported

# Getting Started
The following is an example of how to create a algebra math equation.
The `algebraMathGenerator.generateAlgebraEquation()` will return a class, so you can get the equation by adding a `.equation` after it.


```py
import algebraMathGenerator

equationClass = algebraMathGenerator.generateAlgebraEquation(operation = "+")
print(equationType.equation)

```

You can solve equations with `algebraMathGenerator.solveAlgebraEquation(equation : class)`. The equation variable should be a class returned from `algebraMathGenerator.generateAlgebraEquation()`

```py
import algebraMathGenerator

equationClass = algebraMathGenerator.generateAlgebraEquation(operation = "+")
answer = algebraMathGenerator.solveAlgebraEquation(equationType)
print(equationClass.equation) # returns an equation
print(answer) # returns the answer to the equation above

```

## Equation Class Properties
The `algebraMathGenerator.generateAlgebraEquation()` has many properties.

`algebraMathGenerator.generateAlgebraEquation()` properties:

> .equation
> .variable
> .operation
> .equalsTo
> .coeffecient
> .constant


You can even loop through the generate method to produce a bunch of equations and their answers!
