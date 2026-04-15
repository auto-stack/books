# Variables and Statements

In the previous chapter, we used operators to write expressions that perform arithmetic computations.

In this chapter, you'll learn about variables and statements, the `use` statement (Auto's equivalent of `import`), and the `print` function. We'll also introduce more of the vocabulary we use to talk about programs, including "argument" and "module".

## Variables

A **variable** is a name that refers to a value. To create a variable, we write an **assignment statement** using the `let` keyword:

```auto
let n = 17
```

An assignment statement has three parts: the `let` keyword, the name of the variable, and an expression whose value is assigned. In this example, the expression is an integer.

In the following example, the expression is a floating-point number:

```auto
let pi = 3.141592653589793
```

And in this example, the expression is a string:

```auto
let message = "And now for something completely different"
```

When you run an assignment statement, there is no output. Auto creates the variable and gives it a value, but the assignment statement itself has no visible effect. However, after creating a variable, you can use it in expressions and function calls:

```auto
let n = 17
print(n + 25)       // prints 42
print(2 * pi)       // prints 6.283185307179586
```

In Auto, variables are declared with `let`. If you need a variable whose value can change later, you can use `let mut` (short for "mutable"):

```auto
let mut x = 5
x = 10              // reassignment is allowed because of mut
```

Without `mut`, reassignment is not allowed, which helps prevent accidental changes to values that should stay constant.

> **Note for Python Programmers:**
>
> Python does not have the `let` or `mut` keywords -- you simply write `n = 17`. In Auto, `let` is required for all variable declarations. The `a2p` transpiler strips `let` and `let mut` when generating Python code, since all Python variables are mutable by default.

<Listing number="2-1" file-name="variables.auto" caption="Variable assignment and reassignment">

```auto
fn main() {
    // Creating variables with let
    let n = 17
    let pi = 3.141592653589793
    let message = "And now for something completely different"

    // Using variables in expressions
    print(n + 25)
    print(2 * pi)

    // Using variables in function calls
    print(round(pi))
    print(len(message))

    // Mutable variable with let mut
    let mut x = 5
    print(x)
    x = 10
    print(x)
}
```

```python
def main():
    # Creating variables
    n = 17
    pi = 3.141592653589793
    message = "And now for something completely different"

    # Using variables in expressions
    print(n + 25)
    print(2 * pi)

    # Using variables in function calls
    print(round(pi))
    print(len(message))

    # Mutable variable
    x = 5
    print(x)
    x = 10
    print(x)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

First, we declare three variables using `let`: `n` (an integer), `pi` (a float), and `message` (a string). We then use these variables in arithmetic expressions (`n + 25`, `2 * pi`) and function calls (`round(pi)`, `len(message)`). The results demonstrate that once a variable is created, it can be used anywhere its value is needed.

Next, we use `let mut` to declare `x` as a mutable variable. We print its initial value (`5`), then reassign it to `10` and print again. Without `mut`, the reassignment `x = 10` would not be allowed. In the Python translation, all variables are mutable by default, so the `let mut` distinction disappears.

## State Diagrams

A common way to represent variables on paper is to write the variable name with an arrow pointing to its value. For example, after the following assignments:

```auto
let message = "And now for something completely different"
let n = 17
let pi = 3.141592653589793
```

A state diagram would look like this:

```
message --> "And now for something completely different"
n        --> 17
pi       --> 3.141592653589793
```

This kind of figure is called a **state diagram** because it shows what state each of the variables is in (think of it as the variable's state of mind). We'll use state diagrams throughout the book to represent a model of how variables and their values are stored.

## Variable Names

Variable names can be as long as you like. They can contain both letters and numbers, but they can't begin with a number. It is legal to use uppercase letters, but it is conventional to use only lowercase for variable names.

The only punctuation that can appear in a variable name is the underscore character, `_`. It is often used in names with multiple words, such as `your_name` or `airspeed_of_unladen_swallow`.

If you give a variable an illegal name, you get a syntax error. The name `million!` is illegal because it contains punctuation:

```auto
// ERROR: unexpected '!' in variable name
let million! = 1000000
```

`76trombones` is illegal because it starts with a number:

```auto
// ERROR: variable names cannot start with a digit
let 76trombones = "big parade"
```

`class` is also illegal, but it might not be obvious why:

```auto
// ERROR: expected identifier, found keyword
let class = "Self-Defence Against Fresh Fruit"
```

It turns out that `class` is a **keyword**, which is a special word used to specify the structure of a program. Keywords can't be used as variable names.

Here is a complete list of Auto's keywords:

```
fn        let       mut       if        else
for       in        return    true      false
use       as        type      struct    impl
break     continue  while     match     with
```

You don't have to memorize this list. In most development environments, keywords are displayed in a different color; if you try to use one as a variable name, you'll know.

> **Note for Python Programmers:**
>
> Auto has fewer keywords than Python. Many Python keywords like `def`, `class`, `import`, `try`, `except`, `yield`, etc. are handled differently in Auto. For example, Auto uses `fn` instead of `def`, `use` instead of `import`, and `type` instead of `class` for defining custom types.

<Listing number="2-3" file-name="keywords.auto" caption="Keywords and illegal variable names">

```auto
fn main() {
    // Legal variable names
    let my_name = "Alice"
    let _private = 42
    let item_count = 100
    let speed2 = 60

    print(my_name)
    print(_private)
    print(item_count)
    print(speed2)

    // These would cause syntax errors:
    // let 76trombones = "big parade"   // starts with a number
    // let million! = 1000000           // contains punctuation
    // let fn = "keyword"               // fn is a keyword
}
```

```python
def main():
    # Legal variable names
    my_name = "Alice"
    _private = 42
    item_count = 100
    speed2 = 60

    print(my_name)
    print(_private)
    print(item_count)
    print(speed2)

    # These would cause syntax errors:
    # 76trombones = "big parade"   # starts with a number
    # million! = 1000000           # contains punctuation
    # fn = "keyword"               # fn is a keyword (in Auto)


if __name__ == "__main__":
    main()
```

</Listing>

## The use Statement

In order to use some features, you have to **import** them. In Auto, this is done with the `use` keyword. For example, the following statement imports the `math` module:

```auto
use math
```

A **module** is a collection of variables and functions. The `math` module provides a variable called `pi` that contains the value of the mathematical constant pi. We can display its value like this:

```auto
use math
print(math.pi)
```

To use a variable in a module, you have to use the **dot operator** (`.`) between the name of the module and the name of the variable.

The `math` module also contains functions. For example, `sqrt` computes square roots, and `pow` raises one number to the power of a second number:

```auto
use math
print(math.sqrt(25))    // prints 5.0
print(math.pow(5, 2))   // prints 25.0
```

> **Note for Python Programmers:**
>
> Auto uses `use math` instead of Python's `import math`. The `a2p` transpiler converts `use` to `import` automatically. The dot operator works the same way in both languages.

<Listing number="2-2" file-name="use_print.auto" caption="Using modules and the print function">

```auto
use math

fn main() {
    // Using module variables
    print("The value of pi is approximately")
    print(math.pi)

    // Using module functions
    print(math.sqrt(25))
    print(math.pow(5, 2))

    // print can display any number of values
    print("Any", "number", "of", "arguments")

    // print separates values with a space
    print("The value of pi is approximately", math.pi)
}
```

```python
import math


def main():
    # Using module variables
    print("The value of pi is approximately")
    print(math.pi)

    # Using module functions
    print(math.sqrt(25))
    print(math.pow(5, 2))

    # print can display any number of values
    print("Any", "number", "of", "arguments")

    # print separates values with a space
    print("The value of pi is approximately", math.pi)


if __name__ == "__main__":
    main()
```

</Listing>

## Expressions and Statements

So far, we've seen a few kinds of expressions. An expression can be a single value, like an integer, floating-point number, or string. It can also be a collection of values and operators. And it can include variable names and function calls. Here's an expression that includes several of these elements:

```auto
use math
19 + n + round(math.pi) * 2
```

We have also seen a few kinds of statements. A **statement** is a unit of code that has an effect, but no value. For example, an assignment statement creates a variable and gives it a value, but the statement itself has no value:

```auto
let n = 17
```

Similarly, a `use` statement has an effect -- it imports a module so we can use the variables and functions it contains -- but it has no visible effect:

```auto
use math
```

Computing the value of an expression is called **evaluation**. Running a statement is called **execution**.

## The print Function

When you evaluate an expression in an interactive environment, the result is displayed. But if you evaluate more than one expression, only the value of the last one is displayed.

To display more than one value, you can use the `print` function:

```auto
print(n + 2)
print(n + 3)
```

It also works with floating-point numbers and strings:

```auto
print("The value of pi is approximately")
print(math.pi)
```

You can also pass a sequence of expressions separated by commas:

```auto
print("The value of pi is approximately", math.pi)
```

Notice that `print` puts a space between the values.

## Arguments

When you call a function, the expressions in parentheses are called **arguments**.

Some of the functions we've seen so far take only one argument, like `int`:

```auto
int("101")       // converts string to integer: 101
```

Some take two, like `math.pow`:

```auto
math.pow(5, 2)   // raises 5 to the power of 2: 25.0
```

Some can take additional arguments that are optional. For example, `int` can take a second argument that specifies the base of the number:

```auto
int("101", 2)    // interprets "101" as base 2: 5
```

`round` also takes an optional second argument, which is the number of decimal places to round off to:

```auto
round(math.pi, 3)    // rounds pi to 3 decimal places: 3.142
```

Some functions can take any number of arguments, like `print`:

```auto
print("Any", "number", "of", "arguments")
```

If you call a function and provide too many arguments, that's a `TypeError`. If you provide too few arguments, that's also a `TypeError`. And if you provide an argument with a type the function can't handle, that's a `TypeError`, too. This kind of checking can be annoying when you are getting started, but it helps you detect and correct errors.

## Comments

As programs get bigger and more complicated, they get more difficult to read. Formal languages are dense, and it is often difficult to look at a piece of code and figure out what it is doing and why.

For this reason, it is a good idea to add notes to your programs to explain in natural language what the program is doing. These notes are called **comments**.

In Auto, comments start with the `//` symbol:

```auto
// number of seconds in 42:42
let seconds = 42 * 60 + 42
```

In this case, the comment appears on a line by itself. You can also put comments at the end of a line:

```auto
let miles = 10 / 1.61     // 10 kilometers in miles
```

Everything from `//` to the end of the line is ignored -- it has no effect on the execution of the program.

Comments are most useful when they document non-obvious features of the code. It is reasonable to assume that the reader can figure out *what* the code does; it is more useful to explain *why*.

This comment is redundant with the code and useless:

```auto
let v = 8     // assign 8 to v
```

This comment contains useful information that is not in the code:

```auto
let v = 8     // velocity in miles per hour
```

Good variable names can reduce the need for comments, but long names can make complex expressions hard to read, so there is a tradeoff.

> **Note for Python Programmers:**
>
> Auto uses `//` for comments, while Python uses `#`. The `a2p` transpiler converts `//` to `#` automatically.

## Debugging

Three kinds of errors can occur in a program: syntax errors, runtime errors, and semantic errors. It is useful to distinguish between them in order to track them down more quickly.

* **Syntax error**: "Syntax" refers to the structure of a program and the rules about that structure. If there is a syntax error anywhere in your program, the compiler does not run the program. It displays an error message immediately.

* **Runtime error**: If there are no syntax errors, the program can start running. But if something goes wrong while it is running, the program displays an error message and stops. This type of error is also called an **exception** because it indicates that something exceptional has happened.

* **Semantic error**: The third type of error is "semantic", which means related to meaning. If there is a semantic error in your program, it runs without generating error messages, but it does not do what you intended. Identifying semantic errors can be tricky because it requires you to work backward by looking at the output of the program and trying to figure out what it is doing.

As we've seen, an illegal variable name is a syntax error. If you use an operator with a type it doesn't support, that's a runtime error. And if you write an expression that produces the wrong result due to incorrect logic (like forgetting the order of operations), that's a semantic error.

## Glossary

**variable:**
A name that refers to a value.

**assignment statement:**
A statement that assigns a value to a variable using `let`.

**state diagram:**
A graphical representation of a set of variables and the values they refer to.

**keyword:**
A special word used to specify the structure of a program. Keywords cannot be used as variable names.

**use statement:**
A statement that reads a module file so we can use the variables and functions it contains. Equivalent to Python's `import`.

**module:**
A file that contains Auto code, including function definitions and sometimes other statements.

**dot operator:**
The operator, `.`, used to access a function or variable in another module by specifying the module name followed by a dot and the function or variable name.

**evaluate:**
Perform the operations in an expression in order to compute a value.

**statement:**
A unit of code that has an effect but no value.

**execute:**
Run a statement and do what it says.

**argument:**
A value provided to a function when the function is called.

**comment:**
Text included in a program that provides information about the program but has no effect on its execution.

**runtime error:**
An error that causes a program to display an error message and exit.

**exception:**
An error that is detected while the program is running.

**semantic error:**
An error that causes a program to do the wrong thing, but not to display an error message.

## Exercises

### Exercise

Whenever you learn a new feature, you should make errors on purpose to see what goes wrong.

- We've seen that `let n = 17` is legal. What about `17 = n`?
- What about `let x = 1` followed by `let x = 2`?
- What happens if you spell the name of a module wrong and try `use maath`?

### Exercise

Practice using Auto as a calculator:

**Part 1.** The volume of a sphere with radius $r$ is $\frac{4}{3} \pi r^3$. What is the volume of a sphere with radius 5? Start with a variable named `radius` and then assign the result to a variable named `volume`. Display the result. Add comments to indicate that `radius` is in centimeters and `volume` in cubic centimeters.

**Part 2.** A rule of trigonometry says that for any value of $x$, $(\cos x)^2 + (\sin x)^2 = 1$. Let's see if it's true for a specific value of $x$ like 42. Create a variable named `x` with this value. Then use `math.cos` and `math.sin` to compute the sine and cosine, and the sum of their squares. The result should be close to 1.

**Part 3.** In addition to `pi`, the other variable defined in the `math` module is `e`, which represents the base of the natural logarithm. Compute $e^2$ three ways: using `math.e` and the exponentiation operator (`**`), using `math.pow`, and using `math.exp`.
