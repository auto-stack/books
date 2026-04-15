# Return Values

In previous chapters, we've used built-in functions -- like `abs` and `round` -- and functions in the math module -- like `sqrt` and `pow`. When you call one of these functions, it returns a value you can assign to a variable or use as part of an expression.

The functions we have written so far are different. Some use the `print` function to display values, and some use turtle functions to draw figures. But they don't return values we assign to variables or use in expressions.

In this chapter, we'll see how to write functions that return values.

## Some functions have return values

When you call a function like `math.sqrt`, the result is called a **return value**. If you assign the return value to a variable, you can use it later or as part of an expression.

Here's an example of a function that returns a value:

```auto
fn circle_area(radius: f64) -> f64 {
    let area = 3.14159 * radius * radius
    return area
}
```

`circle_area` takes `radius` as a parameter and computes the area of a circle with that radius. The last line is a `return` statement that returns the value of `area`.

We can assign the return value to a variable:

```auto
let a = circle_area(3.66)
```

Or use it as part of an expression:

```auto
circle_area(radius) + 2.0 * circle_area(radius / 2.0)
```

`area` is a local variable in the function, so we can't access it from outside the function.

> **Note for Python Programmers:**
>
> Auto uses `-> f64` to declare the return type of a function. The `a2p` transpiler strips the return type annotation. In Auto, `return` works the same as in Python -- it ends the function and sends a value back to the caller.

<Listing number="6-1" file-name="return_values.auto" caption="Return values and pure functions">

```auto
fn circle_area(radius: f64) -> f64 {
    let area = 3.14159 * radius * radius
    return area
}

fn repeat_string(word: str, n: int) -> str {
    return word * n
}

fn main() {
    // Return value from circle_area
    let radius = 3.66
    let a = circle_area(radius)
    print("Area of circle with radius $radius:", a)

    // Using return value in an expression
    let total = circle_area(radius) + 2.0 * circle_area(radius / 2.0)
    print("Combined area:", total)

    // Pure function: repeat_string returns a value
    let line = repeat_string("Spam, ", 4)
    print(line)

    // Function without return statement returns nothing
    print(repeat_string("Finland, ", 3))
}
```

```python
import math

def circle_area(radius):
    area = math.pi * radius ** 2
    return area


def repeat_string(word, n):
    return word * n


def main():
    # Return value from circle_area
    radius = 3.66
    a = circle_area(radius)
    print(f"Area of circle with radius {radius}: {a}")

    # Using return value in an expression
    total = circle_area(radius) + 2.0 * circle_area(radius / 2.0)
    print(f"Combined area: {total}")

    # Pure function: repeat_string returns a value
    line = repeat_string("Spam, ", 4)
    print(line)

    # Function without return statement returns nothing
    print(repeat_string("Finland, ", 3))


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`circle_area` computes the area of a circle using the formula pi * r^2 and returns the result with `return area`. `repeat_string` takes a word and a count, then returns the word repeated `n` times using the `*` operator on strings. Both are **pure functions** -- they return a value without printing anything or having other side effects.

Inside `main()`, we call these functions and use their return values in expressions and assignments. Notice that the `return` keyword in Auto is the same as in Python.

## And some have None

If a function doesn't have a `return` statement, it returns `None`, which is a special value like `True` and `False`. For example, the `repeat` function from Chapter 3 uses `print` to display a string but does not use `return` to return a value.

In contrast, `repeat_string` uses `return word * n` to return the result. With this version, we can assign the result to a variable and use it later.

A function like this is called a **pure function** because it doesn't display anything or have any other effect -- other than returning a value.

## Return values and conditionals

If we did not have `abs`, we could write it like this:

```auto
fn absolute_value(x: f64) -> f64 {
    if x < 0.0 {
        return -x
    } else {
        return x
    }
}
```

If `x` is negative, the first `return` statement returns `-x` and the function ends immediately. Otherwise, the second `return` statement returns `x` and the function ends.

However, if you put `return` statements in a conditional, you have to make sure that every possible path through the program hits a `return` statement. Consider this incorrect version:

```auto
fn absolute_value_wrong(x: f64) -> f64 {
    if x < 0.0 {
        return -x
    }
    if x > 0.0 {
        return x
    }
    // BUG: what about x == 0? This function has no return for that case!
}
```

When `x` is `0`, neither condition is true, and the function ends without hitting a `return` statement, which means the return value is `None`.

Code that can never run is called **dead code**. For example, a `return` statement placed after another `return` that always executes can never be reached.

## Incremental development

As you write larger functions, you might find yourself spending more time debugging. To deal with increasingly complex programs, you might want to try **incremental development**, which is a way of adding and testing only a small amount of code at a time.

As an example, suppose you want to find the distance between two points represented by the coordinates (x1, y1) and (x2, y2). By the Pythagorean theorem, the distance is:

**distance = sqrt((x2 - x1)^2 + (y2 - y1)^2)**

The first step is to consider what a `distance` function should look like -- that is, what are the inputs (parameters) and what is the output (return value)?

For this function, the inputs are the coordinates of the points. The return value is the distance. Immediately you can write an outline of the function:

```auto
fn distance(x1: f64, y1: f64, x2: f64, y2: f64) -> f64 {
    return 0.0
}
```

This version doesn't compute distances yet -- it always returns zero. But it is a complete function with a return value, which means that you can test it before you make it more complicated.

The key aspects of incremental development are:

1. Start with a working program, make small changes, and test after every change.
2. Use variables to hold intermediate values so you can display and check them.
3. Once the program is working, remove the scaffolding.

Code used during development but not part of the final version is called **scaffolding**.

## Boolean functions

Functions can return the boolean values `true` and `false`, which is often convenient for encapsulating a complex test in a function. For example, `is_divisible` checks whether `x` is divisible by `y` with no remainder:

```auto
fn is_divisible(x: int, y: int) -> bool {
    return x % y == 0
}
```

The result of the `==` operator is a boolean, so we can return it directly without an `if` statement. Boolean functions are often used in conditional statements:

```auto
if is_divisible(6, 2) {
    print("divisible")
}
```

It is not necessary (and not idiomatic) to compare the result to `true`:

```auto
// Don't do this:
if is_divisible(6, 2) == true { ... }

// Just do this:
if is_divisible(6, 2) { ... }
```

<Listing number="6-2" file-name="incremental_dev.auto" caption="Incremental development and boolean functions">

```auto
fn is_divisible(x: int, y: int) -> bool {
    return x % y == 0
}

fn distance(x1: f64, y1: f64, x2: f64, y2: f64) -> f64 {
    let dx = x2 - x1
    let dy = y2 - y1
    let dsquared = dx * dx + dy * dy
    let result = dsquared.sqrt()
    return result
}

fn main() {
    // Step 1: Start with a stub that always returns 0
    // Step 2: Add dx, dy computation
    // Step 3: Add dsquared computation
    // Step 4: Use sqrt and return result

    let d = distance(1.0, 2.0, 4.0, 6.0)
    print("distance(1, 2, 4, 6) =", d)

    // Boolean function in a conditional
    if is_divisible(6, 2) {
        print("6 is divisible by 2")
    }

    if is_divisible(6, 4) {
        print("6 is divisible by 4")
    } else {
        print("6 is NOT divisible by 4")
    }
}
```

```python
import math

def is_divisible(x, y):
    return x % y == 0


def distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    dsquared = dx ** 2 + dy ** 2
    result = math.sqrt(dsquared)
    return result


def main():
    # Step 1: Start with a stub that always returns 0
    # Step 2: Add dx, dy computation
    # Step 3: Add dsquared computation
    # Step 4: Use sqrt and return result

    d = distance(1, 2, 4, 6)
    print(f"distance(1, 2, 4, 6) = {d}")

    # Boolean function in a conditional
    if is_divisible(6, 2):
        print("6 is divisible by 2")

    if is_divisible(6, 4):
        print("6 is divisible by 4")
    else:
        print("6 is NOT divisible by 4")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The `distance` function demonstrates the final result of incremental development. It computes `dx` and `dy` (the differences in x and y coordinates), then `dsquared` (sum of squares), and finally uses `sqrt` to get the distance. At each step during development, you would test the function to make sure the intermediate values are correct before adding more code.

The `is_divisible` function shows a concise boolean function -- it returns the result of `x % y == 0` directly. In the `main()` function, we use `is_divisible` as a condition in `if` statements, without comparing it to `true`.

> **Note for Python Programmers:**
>
> Auto uses `&&` instead of Python's `and`, and `||` instead of Python's `or`. Auto uses `true`/`false` instead of Python's `True`/`False`. The `a2p` transpiler converts these automatically.

## Recursion with return values

Now that we can write functions with return values, we can write recursive functions with return values. With that capability, we have passed an important threshold -- the subset of Auto we have is now **Turing complete**, which means that we can perform any computation that can be described by an algorithm.

To demonstrate recursion with return values, we'll evaluate a recursively defined mathematical function. The factorial function, denoted with the symbol `!`, is defined as:

- 0! = 1
- n! = n * (n-1)!

This definition says that the factorial of 0 is 1, and the factorial of any other value, n, is n multiplied by the factorial of n-1.

Following an incremental development process, here's the final function:

```auto
fn factorial(n: int) -> int {
    if n == 0 {
        return 1
    } else {
        let recurse = factorial(n - 1)
        return n * recurse
    }
}
```

The flow of execution for this program is similar to the flow of `countdown` in Chapter 5. If we call `factorial` with the value `3`:

Since 3 is not 0, we take the second branch and calculate the factorial of n-1...

> Since 2 is not 0, we take the second branch and calculate the factorial of n-1...
>
> > Since 1 is not 0, we take the second branch and calculate the factorial of n-1...
> >
> > > Since 0 equals 0, we take the first branch and return 1 without making any more recursive calls.
> >
> > The return value, 1, is multiplied by n, which is 1, and the result is returned.
>
> The return value, 1, is multiplied by n, which is 2, and the result is returned.

The return value 2 is multiplied by n, which is 3, and the result, 6, becomes the return value of the function call that started the whole process.

## Leap of faith

Following the flow of execution is one way to read programs, but it can quickly become overwhelming. An alternative is what I call the "leap of faith". When you come to a function call, instead of following the flow of execution, you *assume* that the function works correctly and returns the right result.

In fact, you are already practicing this leap of faith when you use built-in functions. When you call `abs` or `math.sqrt`, you don't examine the bodies of those functions -- you just assume that they work.

The same is true of recursive programs. When you get to the recursive call, instead of following the flow of execution, you should assume that the recursive call works and then ask yourself, "Assuming that I can compute the factorial of n-1, can I compute the factorial of n?" The recursive definition of factorial implies that you can, by multiplying by n.

## Fibonacci

After `factorial`, the most common example of a recursive function is `fibonacci`, which has the following definition:

- fibonacci(0) = 0
- fibonacci(1) = 1
- fibonacci(n) = fibonacci(n-1) + fibonacci(n-2)

Translated into Auto, it looks like this:

```auto
fn fibonacci(n: int) -> int {
    if n == 0 {
        return 0
    } else if n == 1 {
        return 1
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2)
    }
}
```

If you try to follow the flow of execution here, even for small values of n, your head explodes. But according to the leap of faith, if you assume that the two recursive calls work correctly, you can be confident that the last `return` statement is correct.

As an aside, this way of computing Fibonacci numbers is very inefficient. We'll explore why and suggest improvements in a later chapter.

<Listing number="6-4" file-name="recursion.auto" caption="Recursive factorial and Fibonacci">

```auto
fn factorial(n: int) -> int {
    if n == 0 {
        return 1
    } else {
        let recurse = factorial(n - 1)
        return n * recurse
    }
}

fn fibonacci(n: int) -> int {
    if n == 0 {
        return 0
    } else if n == 1 {
        return 1
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2)
    }
}

fn main() {
    // Factorial
    print("factorial(0):", factorial(0))
    print("factorial(1):", factorial(1))
    print("factorial(3):", factorial(3))
    print("factorial(5):", factorial(5))

    // Fibonacci
    print("fibonacci(0):", fibonacci(0))
    print("fibonacci(1):", fibonacci(1))
    print("fibonacci(5):", fibonacci(5))
    print("fibonacci(10):", fibonacci(10))
}
```

```python
def factorial(n):
    if n == 0:
        return 1
    else:
        recurse = factorial(n - 1)
        return n * recurse


def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def main():
    # Factorial
    print(f"factorial(0): {factorial(0)}")
    print(f"factorial(1): {factorial(1)}")
    print(f"factorial(3): {factorial(3)}")
    print(f"factorial(5): {factorial(5)}")

    # Fibonacci
    print(f"fibonacci(0): {fibonacci(0)}")
    print(f"fibonacci(1): {fibonacci(1)}")
    print(f"fibonacci(5): {fibonacci(5)}")
    print(f"fibonacci(10): {fibonacci(10)}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`factorial` uses the recursive definition: the base case is `n == 0` (returns 1), and the recursive case multiplies `n` by `factorial(n-1)`. The local variable `recurse` stores the result of the recursive call before multiplying by `n`.

`fibonacci` has two base cases (`n == 0` returns 0, `n == 1` returns 1) and makes two recursive calls in the else branch. This "tree recursion" structure means the function calls itself twice for each non-base case, which grows exponentially.

## Checking types

What happens if we call `factorial` with `1.5` as an argument? It looks like an infinite recursion. How can that be? The function has base cases when `n == 1` or `n == 0`. But if `n` is not an integer, we can *miss* the base case and recurse forever.

To avoid infinite recursion we can check the type of the argument. In Auto, the type system helps catch many of these errors at compile time. When you declare `fn factorial(n: int)`, passing a floating-point number would be a type error.

For additional safety, we can add **input validation** -- checking the parameters of a function to make sure they have the correct types and values.

## Debugging

Breaking a large program into smaller functions creates natural checkpoints for debugging. If a function is not working, there are three possibilities to consider:

- There is something wrong with the arguments the function is getting -- that is, a precondition is violated.
- There is something wrong with the function -- that is, a postcondition is violated.
- The caller is doing something wrong with the return value.

To rule out the first possibility, you can add a `print` statement at the beginning of the function that displays the values of the parameters. If the parameters look good, you can add a `print` statement before each `return` statement and display the return value. If the function seems to be working, look at the function call to make sure the return value is being used correctly -- or used at all!

Adding `print` statements at the beginning and end of a function can help make the flow of execution more visible.

## Glossary

**return value:**
The result of a function. If a function call is used as an expression, the return value is the value of the expression.

**pure function:**
A function that does not display anything or have any other effect, other than returning a return value.

**dead code:**
Part of a program that can never run, often because it appears after a `return` statement.

**incremental development:**
A program development plan intended to avoid debugging by adding and testing only a small amount of code at a time.

**scaffolding:**
Code that is used during program development but is not part of the final version.

**Turing complete:**
A language, or subset of a language, is Turing complete if it can perform any computation that can be described by an algorithm.

**input validation:**
Checking the parameters of a function to make sure they have the correct types and values.

## Exercises

### Exercise

Use incremental development to write a function called `hypot` that returns the length of the hypotenuse of a right triangle given the lengths of the other two legs as arguments.

Note: There's a function in the math module called `hypot` that does the same thing, but you should not use it for this exercise!

Even if you can write the function correctly on the first try, start with a function that always returns `0` and practice making small changes, testing as you go. When you are done, the function should only return a value -- it should not display anything.

### Exercise

Write a boolean function, `is_between(x, y, z)`, that returns `true` if x < y < z or if z < y < x, and `false` otherwise.

You can use these examples to test your function:

```
is_between(1, 2, 3)  // should be true
is_between(3, 2, 1)  // should be true
is_between(1, 3, 2)  // should be false
is_between(2, 3, 1)  // should be false
```

<Listing number="6-3" file-name="boolean_funcs.auto" caption="Boolean functions: is_between and is_power">

```auto
fn is_between(x: f64, y: f64, z: f64) -> bool {
    return (x < y && y < z) || (z < y && y < x)
}

fn is_power(a: int, b: int) -> bool {
    if a == 1 {
        return true
    }
    if a % b == 0 {
        return is_power(a / b, b)
    }
    return false
}

fn main() {
    // Testing is_between
    print("is_between(1, 2, 3):", is_between(1.0, 2.0, 3.0))
    print("is_between(3, 2, 1):", is_between(3.0, 2.0, 1.0))
    print("is_between(1, 3, 2):", is_between(1.0, 3.0, 2.0))
    print("is_between(2, 3, 1):", is_between(2.0, 3.0, 1.0))

    // Testing is_power
    print("is_power(65536, 2):", is_power(65536, 2))
    print("is_power(27, 3):", is_power(27, 3))
    print("is_power(24, 2):", is_power(24, 2))
    print("is_power(1, 17):", is_power(1, 17))
}
```

```python
def is_between(x, y, z):
    return (x < y and y < z) or (z < y and y < x)


def is_power(a, b):
    if a == 1:
        return True
    if a % b == 0:
        return is_power(a // b, b)
    return False


def main():
    # Testing is_between
    print(f"is_between(1, 2, 3): {is_between(1, 2, 3)}")
    print(f"is_between(3, 2, 1): {is_between(3, 2, 1)}")
    print(f"is_between(1, 3, 2): {is_between(1, 3, 2)}")
    print(f"is_between(2, 3, 1): {is_between(2, 3, 1)}")

    # Testing is_power
    print(f"is_power(65536, 2): {is_power(65536, 2)}")
    print(f"is_power(27, 3): {is_power(27, 3)}")
    print(f"is_power(24, 2): {is_power(24, 2)}")
    print(f"is_power(1, 17): {is_power(1, 17)}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`is_between` returns `true` if `y` is between `x` and `z` (either in ascending or descending order). It uses `&&` (and) and `||` (or) to combine the two possible orderings.

`is_power` checks if `a` is a power of `b` using recursion. The base case is `a == 1` (since b^0 = 1 for any b). If `a` is divisible by `b`, it recursively checks whether `a / b` is a power of `b`. Otherwise, `a` is not a power of `b`.

### Exercise

The Ackermann function, A(m, n), is defined:

- A(m, n) = n+1, if m = 0
- A(m, n) = A(m-1, 1), if m > 0 and n = 0
- A(m, n) = A(m-1, A(m, n-1)), if m > 0 and n > 0

Write a function named `ackermann` that evaluates the Ackermann function. What happens if you call `ackermann(5, 5)`?

You can use these examples to test your function:

```
ackermann(3, 2)  // should be 29
ackermann(3, 3)  // should be 61
ackermann(3, 4)  // should be 125
```

### Exercise

A number, a, is a power of b if it is divisible by b and a/b is a power of b. Write a function called `is_power` that takes parameters `a` and `b` and returns `true` if `a` is a power of `b`.

You can use these examples to test your function:

```
is_power(65536, 2)   // should be true
is_power(27, 3)      // should be true
is_power(24, 2)      // should be false
is_power(1, 17)      // should be true
```

### Exercise

The greatest common divisor (GCD) of a and b is the largest number that divides both of them with no remainder. One way to find the GCD of two numbers is based on the observation that if r is the remainder when a is divided by b, then gcd(a, b) = gcd(b, r). As a base case, we can use gcd(a, 0) = a.

Write a function called `gcd` that takes parameters `a` and `b` and returns their greatest common divisor.

You can use these examples to test your function:

```
gcd(12, 8)    // should be 4
gcd(13, 17)   // should be 1
```
