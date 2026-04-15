# Functions

Functions are reusable pieces of programs. They allow you to give a name to a block of statements, allowing you to run that block using the specified name anywhere in your program and any number of times. This is known as *calling* the function. We have already used many built-in functions such as `print` and `range`.

The function concept is probably *the* most important building block of any non-trivial software (in any programming language), so we will explore various aspects of functions in this chapter.

Functions are defined using the `fn` keyword. After this keyword comes an *identifier* name for the function, followed by a pair of parentheses which may enclose some parameter names with their types, and finally the return type. The function body is enclosed in curly braces `{}`. An example will show that this is actually very simple:

## Defining a Function

Here is a minimal function definition in Auto:

```auto
fn greet() {
    print("Hello, World!")
}
```

Compare this with the Python equivalent:

```python
def greet():
    print("Hello, World!")
```

In Auto, you use `fn` instead of Python's `def`, and the function body is enclosed in curly braces `{}` instead of using indentation. Functions with a return type use the `->` syntax:

```auto
fn add(a: int, b: int) -> int {
    return a + b
}
```

This becomes the following in Python:

```python
def add(a, b):
    return a + b
```

Notice that the `a2p` transpiler removes the type annotations -- Auto's type hints (`int`) are used for readability and are not carried into the Python output.

## Function Parameters

A function can take parameters, which are values you supply to the function so that the function can *do* something utilising those values. These parameters are just like variables except that the values of these variables are defined when we call the function and are already assigned values when the function runs.

Parameters are specified within the pair of parentheses in the function definition, separated by commas. When we call the function, we supply the values in the same way. Note the terminology used -- the names given in the function definition are called *parameters* whereas the values you supply in the function call are called *arguments*.

<Listing number="7-1" file-name="param.auto" caption="Function parameters">

```auto
fn print_max(a: int, b: int) {
    if a > b {
        print(f"$a is maximum")
    } else if a < b {
        print(f"$b is maximum")
    } else {
        print("Both are equal")
    }
}

fn main() {
    // directly pass literal values
    print_max(3, 4)

    let x = 5
    let y = 7

    // pass variables as arguments
    print_max(x, y)
}
```

```python
def print_max(a, b):
    if a > b:
        print(f"{a} is maximum")
    elif a < b:
        print(f"{b} is maximum")
    else:
        print("Both are equal")


def main():
    # directly pass literal values
    print_max(3, 4)

    x = 5
    y = 7

    # pass variables as arguments
    print_max(x, y)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

Here, we define a function called `print_max` that uses two parameters called `a` and `b`. We find out the greater number using a simple `if..else if..else` statement and then print the bigger number.

The first time we call the function `print_max`, we directly supply the numbers as arguments. In the second case, we call the function with variables as arguments. `print_max(x, y)` causes the value of argument `x` to be assigned to parameter `a` and the value of argument `y` to be assigned to parameter `b`. The `print_max` function works the same way in both cases.

The output is:

```
4 is maximum
7 is maximum
```

> **Note for Python Programmers:**
>
> In Auto, function parameters require type annotations (e.g., `a: int`). The `a2p` transpiler strips these type annotations when generating Python code. Auto uses `//` for comments, which becomes `#` in Python.

## Local Variables

When you declare variables inside a function definition, they are not related in any way to other variables with the same names used outside the function -- i.e. variable names are *local* to the function. This is called the *scope* of the variable. All variables have the scope of the block they are declared in starting from the point of definition of the name.

<Listing number="7-2" file-name="local.auto" caption="Using local variables">

```auto
fn func(x: int) {
    print(f"x is $x")
    let x = 2
    print(f"Changed local x to $x")
}

fn main() {
    let x = 50
    func(x)
    print(f"x is still $x")
}
```

```python
def func(x):
    print(f"x is {x}")
    x = 2
    print(f"Changed local x to {x}")


def main():
    x = 50
    func(x)
    print(f"x is still {x}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The first time that we print the *value* of the name *x* with the first line in the function's body, Auto uses the value of the parameter declared in the main block, above the function definition.

Next, we assign the value `2` to `x`. The name `x` is local to our function. So, when we change the value of `x` in the function, the `x` defined in the main block remains unaffected.

With the last `print` statement, we display the value of `x` as defined in the main block, thereby confirming that it is actually unaffected by the local assignment within the previously called function.

The output is:

```
x is 50
Changed local x to 2
x is still 50
```

> **Note for Python Programmers:**
>
> In Auto, you must declare local variables with `let` (or `let mut` for mutable ones). In the function above, `let x = 2` creates a new local variable `x` that shadows the parameter `x`. In Python, you simply assign `x = 2` without any declaration keyword. The `a2p` transpiler removes the `let` keyword when generating Python code.

## The `global` Statement

If you want to assign a value to a name defined at the top level of the program (i.e. not inside any kind of scope such as functions or classes), then you have to tell Auto that the name is not local, but it is *global*. We do this using the `global` statement. It is impossible to assign a value to a variable defined outside a function without the `global` statement.

You can use the values of such variables defined outside the function (assuming there is no variable with the same name within the function). However, this is not encouraged and should be avoided since it becomes unclear to the reader of the program as to where that variable's definition is. Using the `global` statement makes it amply clear that the variable is defined in an outermost block.

<Listing number="7-3" file-name="global.auto" caption="Using the global statement">

```auto
let mut x = 50

fn func() {
    global x
    print(f"x is $x")
    x = 2
    print(f"Changed global x to $x")
}

fn main() {
    func()
    print(f"Value of x is $x")
}
```

```python
x = 50


def func():
    global x
    print(f"x is {x}")
    x = 2
    print(f"Changed global x to {x}")


def main():
    func()
    print(f"Value of x is {x}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The `global` statement is used to declare that `x` is a global variable -- hence, when we assign a value to `x` inside the function, that change is reflected when we use the value of `x` in the main block.

You can specify more than one global variable using the same `global` statement e.g. `global x, y, z`.

The output is:

```
x is 50
Changed global x to 2
Value of x is 2
```

> **Note for Python Programmers:**
>
> The `global` statement works the same way in Auto as in Python. Note however that in Auto, the top-level variable must be declared with `let mut` (not just `let`) if you intend to modify it from within a function. The `a2p` transpiler removes the `let mut` declaration and places the bare `x = 50` assignment at the module level in the Python output.

## Default Argument Values

For some functions, you may want to make some parameters *optional* and use default values in case the user does not want to provide values for them. This is done with the help of default argument values. You can specify default argument values for parameters by appending to the parameter name in the function definition the assignment operator (`=`) followed by the default value.

Note that the default argument value should be a constant. More precisely, the default argument value should be immutable -- this is explained in detail in later chapters. For now, just remember this.

<Listing number="7-4" file-name="default.auto" caption="Default argument values">

```auto
fn say(message: str, times: int = 1) {
    for i in 0..times {
        print(message)
    }
}

fn main() {
    say("Hello")
    say("World", 5)
}
```

```python
def say(message, times=1):
    for i in range(0, times):
        print(message)


def main():
    say("Hello")
    say("World", 5)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The function named `say` is used to print a string as many times as specified. If we don't supply a value, then by default, the string is printed just once. We achieve this by specifying a default argument value of `1` to the parameter `times`.

In the first usage of `say`, we supply only the string and it prints the string once. In the second usage of `say`, we supply both the string and an argument `5` stating that we want to *say* the string message 5 times.

The output is:

```
Hello
World
World
World
World
World
```

> **Note for Python Programmers:**
>
> Default argument values work the same way in Auto as in Python: `fn say(message: str, times: int = 1)`. The `a2p` transpiler converts this to `def say(message, times=1):`, stripping the type annotations while preserving the default value.

> **CAUTION**
>
> Only those parameters which are at the end of the parameter list can be given default argument values i.e. you cannot have a parameter with a default argument value preceding a parameter without a default argument value in the function's parameter list.
>
> This is because the values are assigned to the parameters by position. For example, `fn func(a: int, b: int = 5)` is valid, but `fn func(a: int = 5, b: int)` is *not valid*.

## Keyword Arguments

If you have some functions with many parameters and you want to specify only some of them, then you can give values for such parameters by naming them -- this is called *keyword arguments* -- we use the name (keyword) instead of the position (which we have been using all along) to specify the arguments to the function.

There are two advantages -- one, using the function is easier since we do not need to worry about the order of the arguments. Two, we can give values to only those parameters to which we want to, provided that the other parameters have default argument values.

<Listing number="7-5" file-name="keyword.auto" caption="Keyword arguments">

```auto
fn func(a: int, b: int = 5, c: int = 10) {
    print(f"a is $a and b is $b and c is $c")
}

fn main() {
    func(3, 7)
    func(25, c = 24)
    func(c = 50, a = 100)
}
```

```python
def func(a, b=5, c=10):
    print(f"a is {a} and b is {b} and c is {c}")


def main():
    func(3, 7)
    func(25, c=24)
    func(c=50, a=100)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The function named `func` has one parameter without a default argument value, followed by two parameters with default argument values.

In the first usage, `func(3, 7)`, the parameter `a` gets the value `3`, the parameter `b` gets the value `7` and `c` gets the default value of `10`.

In the second usage `func(25, c=24)`, the variable `a` gets the value of 25 due to the position of the argument. Then, the parameter `c` gets the value of `24` due to naming i.e. keyword arguments. The variable `b` gets the default value of `5`.

In the third usage `func(c=50, a=100)`, we use keyword arguments for all specified values. Notice that we are specifying the value for parameter `c` before that for `a` even though `a` is defined before `c` in the function definition.

The output is:

```
a is 3 and b is 7 and c is 10
a is 25 and b is 5 and c is 24
a is 100 and b is 5 and c is 50
```

> **Note for Python Programmers:**
>
> Keyword arguments work the same way in Auto as in Python. When calling `func(c=50, a=100)`, Auto uses the `=` operator for keyword assignment (not `:`), matching Python's syntax. The `a2p` transpiler passes keyword arguments through unchanged.

## VarArgs Parameters

Sometimes you might want to define a function that can take _any_ number of parameters, i.e. **var**iable number of **arg**uments. In Python, this is achieved using the star (`*`) and double-star (`**`) operators.

Auto does not currently support `*args` or `**kwargs` syntax. This is a Python-specific feature. In Auto, you can achieve similar results by using an array or a dictionary type.

Here is how you would write this in Auto using an array parameter as a workaround:

<Listing number="7-6" file-name="varargs.auto" caption="Variable arguments (Auto vs Python)">

```auto
fn total(numbers: [int]) {
    let mut sum = 0
    for n in numbers {
        sum += n
    }
    print(f"The sum is $sum")
}

fn main() {
    total([1, 2])
    total([1, 2, 3, 4])
}
```

```python
def total(*numbers):
    print("a", numbers[0] if numbers else 5)

    # iterate through all the items in tuple
    for single_item in numbers[1:]:
        print("single_item", single_item)

    print("The sum is", sum(numbers))


def main():
    total(10, 1, 2, 3)
    print("---")
    total()
```

</Listing>

**How It Works**

In the Auto version, we pass a list `[1, 2]` as a single parameter of type `[int]` (an array of integers). The function iterates over the array and computes the sum. This achieves the same goal as Python's `*args` without needing special syntax.

In the Python equivalent, we show the original Python `*args` pattern for reference. The starred parameter `*numbers` collects all positional arguments into a tuple. We also see that Python supports an optional `**kwargs` (double-starred) parameter to collect keyword arguments into a dictionary -- this has no direct Auto equivalent.

The output of the Auto version is:

```
The sum is 3
The sum is 10
```

> **Note for Python Programmers:**
>
> Auto does not support `*args` or `**kwargs`. Instead, pass arrays and dictionaries explicitly. For example, instead of `def func(*args)`, use `fn func(args: [int])` in Auto and pass `func([1, 2, 3])`. The `a2p` transpiler converts the Auto array type `[int]` to a Python list, which works similarly for iteration purposes.
>
> The Python equivalent shown above demonstrates the original `*args`/`**kwargs` pattern from "A Byte of Python" for reference, but the Auto version uses explicit array parameters instead.

## The `return` Statement

The `return` statement is used to *return* from a function i.e. break out of the function. We can optionally *return a value* from the function as well.

<Listing number="7-7" file-name="return.auto" caption="Using the return statement">

```auto
fn maximum(x: int, y: int) -> str {
    if x > y {
        return f"$x"
    } else if x == y {
        return "The numbers are equal"
    } else {
        return f"$y"
    }
}

fn main() {
    print(maximum(2, 3))
}
```

```python
def maximum(x, y):
    if x > y:
        return f"{x}"
    elif x == y:
        return "The numbers are equal"
    else:
        return f"{y}"


def main():
    print(maximum(2, 3))


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The `maximum` function returns the maximum of the parameters, in this case the numbers supplied to the function. It uses a simple `if..else if..else` statement to find the greater value and then *returns* that value.

Note that a `return` statement without a value is equivalent to `return None`. `None` is a special type in Python that represents nothingness. For example, it is used to indicate that a variable has no value if it has a value of `None`.

Every function implicitly contains a `return None` statement at the end unless you have written your own `return` statement. You can see this by running `print(some_function())` where the function `some_function` does not use the `return` statement.

The output is:

```
3
```

> **Note for Python Programmers:**
>
> In Auto, functions that return a value must declare the return type using `-> type`. The `a2p` transpiler strips the return type annotation from the Python output. Note that Auto uses explicit `return` statements (required due to a known transpiler behavior where trailing expressions in `if` blocks can be lost).
>
> **Tip:** There is a built-in function called `max` that already implements the 'find maximum' functionality, so use this built-in function whenever possible.

## DocStrings

Python has a nifty feature called *documentation strings*, usually referred to by its shorter name *docstrings*. DocStrings are an important tool that you should make use of since it helps to document the program better and makes it easier to understand. Amazingly, we can even get the docstring back from, say a function, when the program is actually running!

Auto does not have a built-in docstring mechanism like Python's triple-quoted strings. Instead, Auto uses `//` comments placed at the top of a function body to document it. This is a simpler approach that keeps the language lightweight.

<Listing number="7-8" file-name="docstring.auto" caption="Documenting functions with comments">

```auto
fn print_max(x: int, y: int) {
    // Prints the maximum of two numbers.
    // The two values must be integers.
    let a = x
    let b = y
    if a > b {
        print(f"$a is maximum")
    } else {
        print(f"$b is maximum")
    }
}

fn main() {
    print_max(3, 5)
    // In Python, you can access docstrings via print_max.__doc__
    // Auto does not support runtime docstring access.
    print("Documentation: Use // comments at the top of a function body.")
}
```

```python
def print_max(x, y):
    """Prints the maximum of two numbers.

    The two values must be integers."""
    # convert to integers, if possible
    x = int(x)
    y = int(y)

    if x > y:
        print(x, "is maximum")
    else:
        print(y, "is maximum")


def main():
    print_max(3, 5)
    print(print_max.__doc__)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

In the Auto version, we place `//` comment lines at the top of the function body to serve as documentation. These comments describe what the function does and any important notes about its parameters or behavior. While these comments are not accessible at runtime like Python docstrings, they serve the same purpose of documenting the code for other developers.

In the Python equivalent, we use the traditional Python docstring -- a triple-quoted string on the first logical line of the function. Python treats this string as the `__doc__` attribute of the function, making it accessible at runtime via `print_max.__doc__` or through the `help()` built-in function.

The output is:

```
5 is maximum
Documentation: Use // comments at the top of a function body.
```

> **Note for Python Programmers:**
>
> Auto uses `//` comments for documentation instead of Python's docstrings. There is no runtime equivalent to `__doc__` or `help()` in Auto. The `a2p` transpiler converts `//` comments to `#` comments in the Python output. If you need runtime-accessible documentation in Python, you can add it manually to the transpiled code.
>
> The convention in Auto is to place documentation comments on the lines immediately following the function's opening brace. Start with a capital letter and end with a period, just like Python docstring conventions.

## Summary

We have seen so many aspects of functions but note that we still haven't covered all aspects of them. However, we have already covered most of what you'll use regarding Auto functions on an everyday basis.

- **`fn` keyword** -- defines a function. Auto uses `fn` instead of Python's `def`.
- **Parameters** -- values passed into a function. Auto requires type annotations (e.g., `a: int`), which `a2p` strips in the Python output.
- **Local variables** -- variables declared inside a function with `let` are scoped to that function.
- **`global` statement** -- allows a function to modify a variable defined at the top level. The top-level variable must be declared with `let mut`.
- **Default argument values** -- make parameters optional (e.g., `times: int = 1`). Only trailing parameters can have defaults.
- **Keyword arguments** -- pass arguments by name rather than position (e.g., `func(c=50, a=100)`).
- **VarArgs** -- Auto does not support `*args`/`**kwargs`. Use explicit array or dictionary parameters instead.
- **`return` statement** -- returns a value from a function. Functions with return types use `-> type` in the signature.
- **DocStrings** -- Auto uses `//` comments for documentation. There is no runtime `__doc__` attribute equivalent.

Next, we will see how to use as well as create modules.
