# Control Flow

In the programs we have seen till now, there has always been a series of statements faithfully executed in exact top-down order. What if you wanted to change the flow of how it works? For example, you want the program to take some decisions and do different things depending on different situations, such as printing "Good Morning" or "Good Evening" depending on the time of the day?

As you might have guessed, this is achieved using control flow statements. There are three control flow statements in Auto -- `if`, `for` (which serves as both a `for` loop and a `while` loop), and the associated `break` and `continue` statements.

## The `if` Statement

The `if` statement is used to check a condition: *if* the condition is true, we run a block of statements (called the _if-block_), *else* we process another block of statements (called the _else-block_). The *else* clause is optional. You can chain multiple conditions using `else if`.

Let's see a simple example:

<Listing number="6-1" file-name="if.auto" caption="Using the if statement">

```auto
fn main() {
    let number = 23

    if number < 0 {
        print("Negative")
    } else if number == 0 {
        print("Zero")
    } else {
        print("Positive")
    }
}
```

```python
def main():
    number = 23

    if number < 0:
        print("Negative")
    elif number == 0:
        print("Zero")
    else:
        print("Positive")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

In this program, we declare a variable `number` and assign it the value `23`. Then we check whether the number is negative, zero, or positive using an `if` / `else if` / `else` chain.

In Auto, the `if` statement does not use parentheses around the condition -- you simply write `if condition { ... }`. The curly braces `{}` define the block of code that runs when the condition is true. Compare this with Python, which uses a colon `:` after the condition and indentation for the block.

Notice that Auto's `else if` becomes Python's `elif` when transpiled by `a2p`. This is because Python uses the keyword `elif` (short for "else if"), while Auto spells it out in full.

> **Note for Python Programmers:**
>
> In Python, conditions end with a colon (`:`) and blocks are defined by indentation. In Auto, conditions do not use a colon -- blocks are defined by curly braces `{}`. The `a2p` transpiler handles this conversion automatically.
>
> Also note that Auto uses `else if` (two words), while Python uses `elif` (one word).

A minimal valid `if` statement in Auto looks like this:

```auto
if true {
    print("Yes, it is true")
}
```

You can have another `if` statement inside the block of an `if` statement and so on -- this is called a nested `if` statement. Remember that the `else if` and `else` parts are optional.

## The `while` Loop (Using `for`)

Auto does not have a `while` keyword. Instead, the `for` keyword doubles as a while loop when given a boolean condition instead of a range. The `a2p` transpiler detects this pattern and outputs Python's `while` statement.

This design keeps the language simple -- one keyword, `for`, handles both iteration and conditional looping.

<Listing number="6-2" file-name="while.auto" caption="Using the while loop pattern in Auto">

```auto
fn main() {
    let mut running = true
    let mut count = 0

    for running {
        print(count)
        count += 1
        if count >= 5 {
            running = false
        }
    }
}
```

```python
def main():
    running = True
    count = 0

    while running:
        print(count)
        count += 1
        if count >= 5:
            running = False


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

In this program, we declare two mutable variables using `let mut`: `running` (a boolean flag) and `count` (a counter). The `mut` keyword tells Auto that these variables will be reassigned later.

We then write `for running { ... }`. Since `running` is a boolean expression (not a range like `0..10`), the `a2p` transpiler recognizes this as a while loop and transpiles it to Python's `while running:`.

Inside the loop body, we print the current value of `count`, increment it by 1, and check whether it has reached 5. If so, we set `running` to `false`, which causes the loop to stop on the next condition check.

The output is:

```
0
1
2
3
4
```

> **Note for Python Programmers:**
>
> Auto has no `while` keyword. When you write `for condition { ... }` where `condition` is a boolean expression (not a range), `a2p` transpiles it to Python's `while condition:`. This is Auto's design philosophy -- one `for` keyword serves both purposes.
>
> Note that Auto uses `let mut` to declare mutable variables. In Python, all variables are mutable by default, so `a2p` simply removes the `let mut` prefix in the output.

## The `for` Loop

The `for` loop with a range is used to iterate over a sequence of numbers. The syntax is `for variable in start..end { ... }`, which generates numbers from `start` up to (but not including) `end`.

<Listing number="6-3" file-name="for_range.auto" caption="Using the for loop with a range">

```auto
fn main() {
    for i in 0..5 {
        print(i)
    }
}
```

```python
def main():
    for i in range(0, 5):
        print(i)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

We write `for i in 0..5 { ... }` which iterates `i` over the values `0`, `1`, `2`, `3`, `4`. Notice that `5` is **not** included -- the range `0..5` goes up to but does not include the upper bound, just like Python's `range(0, 5)`.

When transpiled by `a2p`, the Auto range `0..5` becomes Python's `range(0, 5)`. Both produce the same sequence of numbers: `[0, 1, 2, 3, 4]`.

The output is:

```
0
1
2
3
4
```

> **Note for Python Programmers:**
>
> Auto's `0..5` is exactly equivalent to Python's `range(0, 5)`. The `..` operator creates a half-open range (exclusive upper bound). When you need a step other than 1, you can use `for i in 0..10 { if i % 2 == 0 { ... } }` to iterate with a condition, or `a2p` will handle more complex range expressions in future versions.

## The `break` Statement

The `break` statement is used to *break* out of a loop statement -- that is, stop the execution of a looping statement, even if the loop condition has not become `false` or the sequence of items has not been completely iterated over.

<Listing number="6-4" file-name="break_stmt.auto" caption="Using the break statement">

```auto
fn main() {
    for i in 0..10 {
        if i == 5 {
            break
        }
        print(i)
    }
}
```

```python
def main():
    for i in range(0, 10):
        if i == 5:
            break
        print(i)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

In this program, we iterate `i` from `0` to `9`. However, inside the loop body we check if `i` equals `5`. When it does, we execute `break`, which immediately exits the loop -- no more iterations are performed and the program continues after the loop.

So even though the range goes up to `10`, the loop only prints values `0` through `4`, then stops.

The output is:

```
0
1
2
3
4
```

> **Note:** The `break` statement works in both kinds of `for` loops in Auto -- range loops (`for i in 0..10`) and conditional loops (`for condition`).

## The `continue` Statement

The `continue` statement is used to tell Auto to skip the rest of the statements in the current loop block and to *continue* to the next iteration of the loop.

<Listing number="6-5" file-name="continue_stmt.auto" caption="Using the continue statement">

```auto
fn main() {
    for i in 0..10 {
        if i % 2 == 0 {
            continue
        }
        print(i)
    }
}
```

```python
def main():
    for i in range(0, 10):
        if i % 2 == 0:
            continue
        print(i)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

In this program, we iterate `i` from `0` to `9`. For each value, we check if it is even (`i % 2 == 0`). If it is even, the `continue` statement skips the rest of the loop body (the `print(i)` call) and moves on to the next iteration. If it is odd, the `print(i)` executes normally.

This effectively prints only the odd numbers from 0 to 9.

The output is:

```
1
3
5
7
9
```

> **Note:** The `continue` statement works in both kinds of `for` loops in Auto -- range loops and conditional loops.

## Summary

We have seen how to use the control flow statements in Auto:

- **`if` / `else if` / `else`** -- make decisions based on conditions. Auto uses `else if` which `a2p` transpiles to Python's `elif`.
- **`for condition { ... }`** -- Auto's while loop pattern. When the `for` keyword is followed by a boolean expression (not a range), `a2p` transpiles it to Python's `while`.
- **`for i in start..end { ... }`** -- iterate over a range of numbers. The range `0..5` is equivalent to Python's `range(0, 5)`.
- **`break`** -- exit a loop immediately, regardless of the loop condition.
- **`continue`** -- skip the rest of the current iteration and move to the next one.

Remember that Auto uses curly braces `{}` to define blocks, while Python uses indentation. The `a2p` transpiler handles this conversion automatically, so you can write clean, brace-delimited Auto code and get properly indented Python output.

Next, we will see how to create and use functions.
