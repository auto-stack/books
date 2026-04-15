# Conditionals and Recursion

The main topic of this chapter is the `if` statement, which executes different code depending on the state of the program. And with the `if` statement we'll be able to explore one of the most powerful ideas in computing, **recursion**.

But we'll start with three new features: the modulus operator, boolean expressions, and logical operators.

## Integer Division and Modulus

Recall that the integer division operator, `/`, divides two numbers and rounds down to an integer. For example, suppose the run time of a movie is 105 minutes. You might want to know how long that is in hours. Integer division returns the integer number of hours:

```auto
let minutes = 105
let hours = minutes / 60
print(hours)   // prints: 1
```

To get the remainder, you could subtract off one hour in minutes. Or you could use the **modulus operator**, `%`, which divides two numbers and returns the remainder:

```auto
let remainder = minutes % 60
print(remainder)   // prints: 45
```

<Listing number="5-1" file-name="modulus.auto" caption="Modulus operator: integer division and remainder">

```auto
fn main() {
    // Integer division and modulus
    let minutes = 105
    let hours = minutes / 60
    print("Minutes: $minutes")
    print("Hours: $hours")
    print()

    // Remainder via subtraction
    let remainder = minutes - hours * 60
    print("Remainder (subtraction): $remainder")

    // Remainder via modulus operator
    let remainder2 = minutes % 60
    print("Remainder (modulus): $remainder2")
    print()

    // Extract rightmost digits
    let x = 123
    print("x = $x")
    print("x % 10 = ${x % 10}")
    print("x % 100 = ${x % 100}")
    print()

    // Clock arithmetic
    let start = 11
    let duration = 3
    let end = (start + duration) % 12
    print("Start: ${start} AM")
    print("Duration: $duration hours")
    print("End: ${if end == 0 { 12 } else { end }} PM")

    // Divisibility check
    let y = 15
    print()
    print("Is $y divisible by 3? ${y % 3 == 0}")
    print("Is $y divisible by 4? ${y % 4 == 0}")
}
```

```python
def main():
    # Integer division and modulus
    minutes = 105
    hours = minutes // 60
    print(f"Minutes: {minutes}")
    print(f"Hours: {hours}")
    print()

    # Remainder via subtraction
    remainder = minutes - hours * 60
    print(f"Remainder (subtraction): {remainder}")

    # Remainder via modulus operator
    remainder2 = minutes % 60
    print(f"Remainder (modulus): {remainder2}")
    print()

    # Extract rightmost digits
    x = 123
    print(f"x = {x}")
    print(f"x % 10 = {x % 10}")
    print(f"x % 100 = {x % 100}")
    print()

    # Clock arithmetic
    start = 11
    duration = 3
    end = (start + duration) % 12
    print(f"Start: {start} AM")
    print(f"Duration: {duration} hours")
    print(f"End: {12 if end == 0 else end} PM")

    # Divisibility check
    y = 15
    print()
    print(f"Is {y} divisible by 3? {y % 3 == 0}")
    print(f"Is {y} divisible by 4? {y % 4 == 0}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

We divide `105` minutes by `60` using `/` (integer division in Auto), getting `1` hour. The modulus operator `%` gives the remainder, `45`. We also demonstrate extracting rightmost digits (`123 % 10` is `3`, `123 % 100` is `23`), clock arithmetic (11 AM + 3 hours wraps to 2 PM), and divisibility checking (15 is divisible by 3 but not by 4).

> **Note for Python Programmers:**
>
> Auto uses `/` for integer division (when both operands are integers). The `a2p` transpiler converts this to Python's `//` operator automatically. Auto's `%` operator works the same as Python's.

## Boolean Expressions

A **boolean expression** is an expression that is either true or false. For example, the following expressions use the equals operator, `==`, which compares two values and produces `true` if they are equal and `false` otherwise:

```auto
5 == 5    // true
5 == 7    // false
```

`true` and `false` are special values that belong to the type `bool`; they are not strings.

A common error is to use a single equal sign (`=`) instead of a double equal sign (`==`). Remember that `=` assigns a value to a variable and `==` compares two values.

The `==` operator is one of the **relational operators**; the others are:

| Operator | Meaning |
|----------|---------|
| `!=` | Not equal |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal to |
| `<=` | Less than or equal to |

> **Note for Python Programmers:**
>
> Auto uses `true` and `false` (lowercase). The `a2p` transpiler converts them to Python's `True` and `False` automatically.

## Logical Operators

To combine boolean values into expressions, we can use **logical operators**. In Auto, these are `&&` (and), `||` (or), and `!` (not).

<Listing number="5-2" file-name="boolean_logical.auto" caption="Boolean and logical operators">

```auto
fn main() {
    // Boolean expressions
    let x = 5
    let y = 7

    print("x = $x, y = $y")
    print("x == y: ${x == y}")
    print("x != y: ${x != y}")
    print("x > y: ${x > y}")
    print("x < y: ${x < y}")
    print("x >= y: ${x >= y}")
    print("x <= y: ${x <= y}")
    print()

    // Logical operators
    print("x > 0 && x < 10: ${x > 0 && x < 10}")
    print("x % 2 == 0 || x % 3 == 0: ${x % 2 == 0 || x % 3 == 0}")
    print("!(x > y): ${!(x > y)}")
    print()

    // Combining conditions
    let age = 25
    let has_ticket = true
    print("age = $age, has_ticket = $has_ticket")
    print("Can enter: ${age >= 18 && has_ticket}")

    // Negation
    let is_raining = false
    print("is_raining = $is_raining")
    print("Should go outside: ${!is_raining}")
}
```

```python
def main():
    # Boolean expressions
    x = 5
    y = 7

    print(f"x = {x}, y = {y}")
    print(f"x == y: {x == y}")
    print(f"x != y: {x != y}")
    print(f"x > y: {x > y}")
    print(f"x < y: {x < y}")
    print(f"x >= y: {x >= y}")
    print(f"x <= y: {x <= y}")
    print()

    # Logical operators
    print(f"x > 0 and x < 10: {x > 0 and x < 10}")
    print(f"x % 2 == 0 or x % 3 == 0: {x % 2 == 0 or x % 3 == 0}")
    print(f"not (x > y): {not (x > y)}")
    print()

    # Combining conditions
    age = 25
    has_ticket = True
    print(f"age = {age}, has_ticket = {has_ticket}")
    print(f"Can enter: {age >= 18 and has_ticket}")

    # Negation
    is_raining = False
    print(f"is_raining = {is_raining}")
    print(f"Should go outside: {not is_raining}")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

We test all six relational operators on `x` and `y`. Then we combine conditions with logical operators: `&&` requires both conditions to be true, `||` requires at least one, and `!` negates a boolean. The last examples show real-world use: checking entry eligibility (age >= 18 AND has a ticket) and checking whether to go outside (NOT raining).

> **Note for Python Programmers:**
>
> Auto uses `&&` instead of Python's `and`, `||` instead of `or`, and `!` instead of `not`. The `a2p` transpiler converts these automatically.

## if Statements

In order to write useful programs, we almost always need the ability to check conditions and change the behavior of the program accordingly. **Conditional statements** give us this ability. The simplest form is the `if` statement:

```auto
if x > 0 {
    print("x is positive")
}
```

The boolean expression after `if` is called the **condition**. If it is true, the statements in the block run. If not, they don't.

## Chained Conditionals

Sometimes there are more than two possibilities and we need more than two branches. One way to express a computation like that is a **chained conditional**, which uses `else if`:

```auto
if x < y {
    print("x is less than y")
} else if x > y {
    print("x is greater than y")
} else {
    print("x and y are equal")
}
```

There is no limit on the number of `else if` clauses. If there is an `else` clause, it has to be at the end, but there doesn't have to be one. Each condition is checked in order. If the first is false, the next is checked, and so on. If one of them is true, the corresponding branch runs and the `if` statement ends. Even if more than one condition is true, only the first true branch runs.

> **Note for Python Programmers:**
>
> Auto uses `else if` instead of Python's `elif`. The `a2p` transpiler converts `else if` to `elif` automatically.

## Nested Conditionals

One conditional can also be nested within another. We could have written the comparison example like this:

```auto
if x == y {
    print("x and y are equal")
} else {
    if x < y {
        print("x is less than y")
    } else {
        print("x is greater than y")
    }
}
```

The outer `if` statement contains two branches. The first branch contains a simple statement. The second branch contains another `if` statement. Although the indentation makes the structure apparent, **nested conditionals** can be difficult to read. In general, you should avoid them when you can.

Logical operators often provide a way to simplify nested conditional statements. For example, this nested conditional:

```auto
if 0 < x {
    if x < 10 {
        print("x is a positive single-digit number.")
    }
}
```

Can be simplified to:

```auto
if 0 < x && x < 10 {
    print("x is a positive single-digit number.")
}
```

## if / else if / else

<Listing number="5-3" file-name="conditionals.auto" caption="if / else if / else statements">

```auto
fn classify_number(x: int) {
    if x > 0 {
        print("$x is positive")
    } else if x < 0 {
        print("$x is negative")
    } else {
        print("$x is zero")
    }
}

fn classify_even_odd(x: int) {
    if x % 2 == 0 {
        print("$x is even")
    } else {
        print("$x is odd")
    }
}

fn classify_temperature(temp: int) {
    if temp >= 30 {
        print("$temp C is hot")
    } else if temp >= 20 {
        print("$temp C is warm")
    } else if temp >= 10 {
        print("$temp C is cool")
    } else {
        print("$temp C is cold")
    }
}

fn compare(x: int, y: int) {
    if x < y {
        print("$x is less than $y")
    } else if x > y {
        print("$x is greater than $y")
    } else {
        print("$x and $y are equal")
    }
}

fn main() {
    // if / else
    print("=== Positive / Negative / Zero ===")
    classify_number(5)
    classify_number(-3)
    classify_number(0)
    print()

    // if / else (even/odd)
    print("=== Even / Odd ===")
    classify_even_odd(4)
    classify_even_odd(7)
    print()

    // Chained conditionals (else if)
    print("=== Temperature ===")
    classify_temperature(35)
    classify_temperature(25)
    classify_temperature(15)
    classify_temperature(5)
    print()

    // Chained conditional (three-way comparison)
    print("=== Comparison ===")
    compare(3, 5)
    compare(7, 2)
    compare(4, 4)
}
```

```python
def classify_number(x):
    if x > 0:
        print(f"{x} is positive")
    elif x < 0:
        print(f"{x} is negative")
    else:
        print(f"{x} is zero")


def classify_even_odd(x):
    if x % 2 == 0:
        print(f"{x} is even")
    else:
        print(f"{x} is odd")


def classify_temperature(temp):
    if temp >= 30:
        print(f"{temp} C is hot")
    elif temp >= 20:
        print(f"{temp} C is warm")
    elif temp >= 10:
        print(f"{temp} C is cool")
    else:
        print(f"{temp} C is cold")


def compare(x, y):
    if x < y:
        print(f"{x} is less than {y}")
    elif x > y:
        print(f"{x} is greater than {y}")
    else:
        print(f"{x} and {y} are equal")


def main():
    # if / else
    print("=== Positive / Negative / Zero ===")
    classify_number(5)
    classify_number(-3)
    classify_number(0)
    print()

    # if / else (even/odd)
    print("=== Even / Odd ===")
    classify_even_odd(4)
    classify_even_odd(7)
    print()

    # Chained conditionals (elif)
    print("=== Temperature ===")
    classify_temperature(35)
    classify_temperature(25)
    classify_temperature(15)
    classify_temperature(5)
    print()

    # Chained conditional (three-way comparison)
    print("=== Comparison ===")
    compare(3, 5)
    compare(7, 2)
    compare(4, 4)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`classify_number` uses a three-way `if`/`else if`/`else` to categorize a number as positive, negative, or zero. `classify_even_odd` uses the modulus operator to check if a number is even or odd. `classify_temperature` demonstrates a longer `else if` chain with four branches, checking temperature ranges from hot to cold. `compare` uses a chained conditional to compare two numbers.

Note how `classify_temperature` works: conditions are checked in order, so `temp >= 30` is checked first. If `temp` is `25`, the first condition is false, so the next (`temp >= 20`) is checked and found to be true -- the remaining branches are skipped.

## Recursion

It is legal for a function to call itself. It may not be obvious why that is a good thing, but it turns out to be one of the most magical things a program can do. Here's an example:

<Listing number="5-4" file-name="recursion.auto" caption="Simple recursion: countdown">

```auto
fn countdown(n: int) {
    if n <= 0 {
        print("Blastoff!")
    } else {
        print(n)
        countdown(n - 1)
    }
}

fn print_n(string: str, n: int) {
    if n > 0 {
        print(string)
        print_n(string, n - 1)
    }
}

fn main() {
    // Countdown from 3
    print("Countdown from 3:")
    countdown(3)
    print()

    // Countdown from 1
    print("Countdown from 1:")
    countdown(1)
    print()

    // Print a string n times
    print("Print 'Spam' 4 times:")
    print_n("Spam", 4)
    print()

    // Print with n = 0 (base case, prints nothing)
    print("Print 'Hello' 0 times:")
    print_n("Hello", 0)
}
```

```python
def countdown(n):
    if n <= 0:
        print("Blastoff!")
    else:
        print(n)
        countdown(n - 1)


def print_n(string, n):
    if n > 0:
        print(string)
        print_n(string, n - 1)


def main():
    # Countdown from 3
    print("Countdown from 3:")
    countdown(3)
    print()

    # Countdown from 1
    print("Countdown from 1:")
    countdown(1)
    print()

    # Print a string n times
    print("Print 'Spam' 4 times:")
    print_n("Spam", 4)
    print()

    # Print with n = 0 (base case, prints nothing)
    print("Print 'Hello' 0 times:")
    print_n("Hello", 0)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`countdown` checks if `n` is less than or equal to `0`. If so, it prints "Blastoff!" -- this is called the **base case**. Otherwise, it prints `n` and then calls itself with `n - 1`.

When we call `countdown(3)`, the execution begins with `n=3`. Since `n > 0`, it displays `3` and calls `countdown(2)`:

> The execution of `countdown` begins with `n=2`. Since `n > 0`, it displays `2` and calls `countdown(1)`:
>
> > The execution of `countdown` begins with `n=1`. Since `n > 0`, it displays `1` and calls `countdown(0)`:
> >
> > > The execution of `countdown` begins with `n=0`. Since `n <= 0`, it displays "Blastoff!" and returns.
> >
> > The `countdown` that got `n=1` returns.
>
> The `countdown` that got `n=2` returns.

The `countdown` that got `n=3` returns.

`print_n` works similarly: if `n > 0`, it prints the string and calls itself with `n - 1`. If `n` is `0`, the condition is false and the function does nothing -- this is the base case.

A function that calls itself is **recursive**. For simple examples like these, it is probably easier to use a `for` loop. But we will see examples later that are hard to write with a `for` loop and easy to write with recursion, so it is good to start early.

## Infinite Recursion

If a recursion never reaches a base case, it goes on making recursive calls forever, and the program never terminates. This is known as **infinite recursion**, and it is generally not a good idea. Here's a minimal function with an infinite recursion:

```auto
fn recurse() {
    recurse()
}
```

Every time `recurse` is called, it calls itself, which creates another frame. There is a limit to the number of frames that can be on the stack at the same time. If a program exceeds the limit, it causes a runtime error.

If you encounter an infinite recursion by accident, review your function to confirm that there is a base case that does not make a recursive call. And if there is a base case, check whether you are guaranteed to reach it.

## Keyboard Input

The programs we have written so far accept no input from the user. They just do the same thing every time.

Auto provides a built-in function called `input` that stops the program and waits for the user to type something. When the user presses Return or Enter, the program resumes and `input` returns what the user typed as a string.

```auto
let text = input()
print("You typed: $text")
```

Before getting input from the user, you might want to display a prompt telling the user what to type. `input` can take a prompt as an argument:

```auto
let name = input("What is your name?\n")
print("Hello, $name!")
```

If you expect the user to type an integer, you can use the `int` function to convert the return value:

```auto
let speed = int(input("Enter speed: "))
print("Speed is $speed")
```

But if they type something that's not an integer, you'll get a runtime error. We will see how to handle this kind of error later.

## Stack Diagrams for Recursive Functions

Here's a stack diagram that shows the frames created when we called `countdown` with `n = 3`:

```
+------------------+
| countdown        |
| n -> 3           |
+------------------+
| countdown        |
| n -> 2           |
+------------------+
| countdown        |
| n -> 1           |
+------------------+
| countdown        |
| n -> 0           |
+------------------+
```

The four `countdown` frames have different values for the parameter `n`. The bottom of the stack, where `n=0`, is called the **base case**. It does not make a recursive call, so there are no more frames below it.

## Debugging

When a syntax or runtime error occurs, the error message contains a lot of information, but it can be overwhelming. The most useful parts are usually:

- What kind of error it was, and
- Where it occurred.

Syntax errors are usually easy to find, but there are a few gotchas. Errors related to spaces and tabs can be tricky because they are invisible and we are used to ignoring them.

Error messages indicate where the problem was discovered, but the actual error might be earlier in the code. The same is true of runtime errors.

In general, you should take the time to read error messages carefully, but don't assume that everything they say is correct.

## Glossary

**recursion:**
The process of calling the function that is currently executing.

**modulus operator:**
An operator, `%`, that works on integers and returns the remainder when one number is divided by another.

**boolean expression:**
An expression whose value is either `true` or `false`.

**relational operator:**
One of the operators that compares its operands: `==`, `!=`, `>`, `<`, `>=`, and `<=`.

**logical operator:**
One of the operators that combines boolean expressions, including `&&` (and), `||` (or), and `!` (not).

**conditional statement:**
A statement that controls the flow of execution depending on some condition.

**condition:**
The boolean expression in a conditional statement that determines which branch runs.

**block:**
One or more statements enclosed in `{}` to indicate they are part of another statement.

**branch:**
One of the alternative sequences of statements in a conditional statement.

**chained conditional:**
A conditional statement with a series of alternative branches using `else if`.

**nested conditional:**
A conditional statement that appears in one of the branches of another conditional statement.

**recursive:**
A function that calls itself is recursive.

**base case:**
A conditional branch in a recursive function that does not make a recursive call.

**infinite recursion:**
A recursion that doesn't have a base case, or never reaches it. Eventually, an infinite recursion causes a runtime error.

**newline:**
A character that creates a line break between two parts of a string.

## Exercises

### Exercise

Use integer division and the modulus operator to write a function that takes a number of seconds and prints the time in hours, minutes, and seconds. For example, `print_time(3661)` should display `1 hour, 1 minute, 1 second`.

### Exercise

If you are given three sticks, you may or may not be able to arrange them in a triangle. For any three lengths, there is a test to see if it is possible to form a triangle:

> If any of the three lengths is greater than the sum of the other two, then you cannot form a triangle. Otherwise, you can.

Write a function named `is_triangle` that takes three integers as arguments, and that prints either "Yes" or "No", depending on whether you can or cannot form a triangle from sticks with the given lengths. Hint: Use a chained conditional.

Test your function with the following cases:

```auto
is_triangle(4, 5, 6)    // should be Yes
is_triangle(1, 2, 3)    // should be Yes (degenerate)
is_triangle(6, 2, 3)    // should be No
is_triangle(1, 1, 12)   // should be No
```

### Exercise

What is the output of the following program? Draw a stack diagram that shows the state of the program when it prints the result.

```auto
fn recurse(n: int, s: int) {
    if n == 0 {
        print(s)
    } else {
        recurse(n - 1, n + s)
    }
}

fn main() {
    recurse(3, 0)
}
```

### Exercise

Write a recursive function called `fibonacci` that takes an integer `n` and returns the nth Fibonacci number. The Fibonacci sequence is defined as: `fib(0) = 0`, `fib(1) = 1`, and `fib(n) = fib(n-1) + fib(n-2)` for `n > 1`. Print the first 10 Fibonacci numbers.

Hint: You will need a function that returns a value, which we will cover in the next chapter. For now, you can use `print` to display each value.
