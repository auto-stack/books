# Basics

Just printing `hello world` is not enough, is it? You want to do more than that -- you want to take some input, manipulate it and get something out of it. We can achieve this in Auto using constants and variables, and we'll learn some other concepts as well in this chapter.

## Comments

_Comments_ are any text to the right of the `//` symbol and are mainly useful as notes for the reader of the program.

For example:

```auto
print("Hello, World!") // This is an inline comment
```

or:

```auto
// This is a comment before the code
print("Hello, World!")
```

Use as many useful comments as you can in your program to:

- explain assumptions
- explain important decisions
- explain important details
- explain problems you're trying to solve
- explain problems you're trying to overcome in your program, etc.

[*Code tells you how, comments should tell you why*](http://www.codinghorror.com/blog/2006/12/code-tells-you-how-comments-tell-you-why.html).

This is useful for readers of your program so that they can easily understand what the program is doing. Remember, that person can be yourself after six months!

> **Note for Python Programmers:**
>
> Auto uses `//` for comments, while Python uses `#`. When transpiled by `a2p`, `//` comments are automatically converted to `#` comments in the output Python code.

Let's put comments into practice with a small program:

<Listing number="4-1" file-name="comments.auto" caption="Using comments in Auto">

```auto
// This is a comment
// and so is this

fn main() {
    print("Hello, World!") // This is also a comment
}
```

```python
# This is a comment
# and so is this


def main():
    print("Hello, World!")  # This is also a comment


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The first two lines are full-line comments -- they each start with `//` and the entire line is ignored by the compiler. Inside `main()`, the `// This is also a comment` part is an inline comment. The compiler ignores everything from `//` to the end of the line, so `print("Hello, World!")` runs normally while the comment is just there for human readers.

## Literal Constants

An example of a literal constant is a number like `5`, `1.23`, or a string like `"This is a string"` or `"It's a string!"`.

It is called a literal because it is _literal_ -- you use its value literally. The number `2` always represents itself and nothing else -- it is a _constant_ because its value cannot be changed. Hence, all these are referred to as literal constants.

## Numbers

Numbers are mainly of two types -- integers and floats.

An example of an integer is `2` which is just a whole number.

Examples of floating point numbers (or _floats_ for short) are `3.23` and `52.3E-4`. The `E` notation indicates powers of 10. In this case, `52.3E-4` means `52.3 * 10^-4`.

> **Note for Experienced Programmers**
>
> There is no separate `long` type. The `int` type can be an integer of any size. For readability, you can use underscores in numeric literals like `2_000_000`.

<Listing number="4-2" file-name="numbers.auto" caption="Working with numbers in Auto">

```auto
fn main() {
    // Integers
    let a = 5
    let b = -3
    let c = 2_000_000  // underscores for readability

    // Floats
    let pi = 3.14159
    let small = 1.5e-4

    // Arithmetic operations
    print(a + b)
    print(a * b)
    print(a / b)
    print(pi * c)
}
```

```python
def main():
    # Integers
    a = 5
    b = -3
    c = 2_000_000  # underscores for readability

    # Floats
    pi = 3.14159
    small = 1.5e-4

    # Arithmetic operations
    print(a + b)
    print(a * b)
    print(a / b)
    print(pi * c)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

We declare integer variables `a`, `b`, and `c` using `let`. Notice that `c` uses underscores to separate groups of digits -- this is a readability feature borrowed from Python and makes large numbers much easier to read at a glance. We also declare float variables `pi` and `small`. The `1.5e-4` is scientific notation meaning `1.5 * 10^-4`, which equals `0.00015`. Then we perform basic arithmetic: addition (`+`), multiplication (`*`), and division (`/`). Note that dividing two integers in Auto (when transpiled to Python) produces a float, just like in Python 3.

## Strings

A string is a _sequence_ of _characters_. Strings are basically just a bunch of words.

You will be using strings in almost every Auto program that you write, so pay attention to the following part.

### Double Quotes

You can specify strings using double quotes such as `"Hello, World!"`. Double quotes are the preferred style in Auto.

All white space i.e. spaces and tabs, within the quotes, are preserved as-is.

### Single Quote

Strings in single quotes work exactly the same way as strings in double quotes. An example is `'What\'s your name?'`.

### Multiline Strings

You can specify multi-line strings using triple double quotes -- `"""`. You can use single quotes and double quotes freely within the triple quotes. An example is:

```auto
"""This is a multi-line string. This is the first line.
This is the second line.
"What's your name?," I asked.
He said "Bond, James Bond."
"""
```

### Strings Are Immutable

This means that once you have created a string, you cannot change it. Although this might seem like a bad thing, it really isn't. We will see why this is not a limitation in the various programs that we see later on.

> **Note for C/C++ Programmers**
>
> There is no separate `char` data type in Auto. There is no real need for it and I am sure you won't miss it.

### String Formatting

Sometimes we may want to construct strings from other information. Auto supports _f-strings_ for this purpose. The syntax uses a `$` prefix before the variable name inside the string:

```auto
let name = "Swaroop"
let age = 20
print(f"$name was $age years old when he wrote this book")
```

> **Note for Python Programmers:**
>
> In Python, f-strings use `{name}` syntax. In Auto, the same feature uses `$name` syntax. The `a2p` transpiler converts `f"$name"` to `f"{name}"` automatically.

<Listing number="4-3" file-name="strings.auto" caption="Working with strings in Auto">

```auto
fn main() {
    // Single and double quotes
    let name = "Swaroop"
    let greeting = 'Hello'

    // Multiline string
    let story = """This is a multi-line string.
This is the second line.
"What's your name?" I asked.
He said "Bond, James Bond."
"""

    // f-string with $ interpolation
    let age = 20
    print(f"$name was $age years old when he wrote this book")
    print(f"Why is $name playing with that python?")

    // String concatenation
    print(name + " is " + "awesome")

    print(story)
}
```

```python
def main():
    # Single and double quotes
    name = "Swaroop"
    greeting = "Hello"

    # Multiline string
    story = """This is a multi-line string.
This is the second line.
"What's your name?" I asked.
He said "Bond, James Bond."
"""

    # f-string with {var} interpolation
    age = 20
    print(f"{name} was {age} years old when he wrote this book")
    print(f"Why is {name} playing with that python?")

    # String concatenation
    print(name + " is " + "awesome")

    print(story)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

We declare string variables using both double quotes (`"Swaroop"`) and single quotes (`'Hello'`). The multiline string uses triple double quotes (`"""`) and preserves all the formatting including newlines and embedded quotes. The f-strings use `$name` and `$age` to interpolate variables directly into the string -- when transpiled to Python, these become `{name}` and `{age}`. Finally, we demonstrate string concatenation using the `+` operator to join strings together.

### Escape Sequences

Suppose you want to have a string which contains a double quote (`"`), how will you specify this string? For example, the string is `"He said, "Hi.""`. You cannot specify `"He said, "Hi.""` because Auto will be confused as to where the string starts and ends. So, you will have to specify that this double quote does not indicate the end of the string. This can be done with the help of what is called an _escape sequence_. You specify the double quote as `\"` -- notice the backslash.

Similarly, you have to indicate the backslash itself using the escape sequence `\\`.

What if you wanted to specify a two-line string? One way is to use a triple-quoted string as shown previously, or you can use the escape sequence `\n` to indicate the start of a new line. Another useful escape sequence is the tab: `\t`.

## Variables

Using just literal constants can soon become boring -- we need some way of storing any information and manipulate them as well. This is where _variables_ come into the picture. Variables are exactly what the name implies -- their value can vary, i.e., you can store anything using a variable. Variables are just parts of your computer's memory where you store some information. Unlike literal constants, you need some method of accessing these variables and hence you give them names.

In Auto, you declare a variable using the `let` keyword:

```auto
let i = 5
```

This creates a variable called `i` and assigns it the value `5`.

> **Note for Python Programmers:**
>
> Python does not require the `let` keyword -- you simply write `i = 5`. In Auto, `let` is required for variable declarations. The `a2p` transpiler strips the `let` keyword when generating Python code.

### Identifier Naming

Variables are examples of identifiers. _Identifiers_ are names given to identify _something_. There are some rules you have to follow for naming identifiers:

- The first character of the identifier must be a letter of the alphabet (uppercase ASCII or lowercase ASCII or Unicode character) or an underscore (`_`).
- The rest of the identifier name can consist of letters (uppercase ASCII or lowercase ASCII or Unicode character), underscores (`_`) or digits (0-9).
- Identifier names are case-sensitive. For example, `myname` and `myName` are _not_ the same. Note the lowercase `n` in the former and the uppercase `N` in the latter.
- Examples of _valid_ identifier names are `i`, `name_2_3`. Examples of _invalid_ identifier names are `2things`, `this is spaced out`, `my-name` and `>a1b2_c3`.

<Listing number="4-4" file-name="variables.auto" caption="Using variables in Auto">

```auto
fn main() {
    // Variable declarations with let
    let i = 5
    print(i)

    i = i + 1
    print(i)

    // Variables can hold different types
    let name = "Alice"
    let score = 98.5
    let is_passing = true

    // Multi-line string in a variable
    let s = """This is a multi-line string.
This is the second line."""

    print(name)
    print(score)
    print(is_passing)
    print(s)
}
```

```python
def main():
    # Variable declarations
    i = 5
    print(i)

    i = i + 1
    print(i)

    # Variables can hold different types
    name = "Alice"
    score = 98.5
    is_passing = True

    # Multi-line string in a variable
    s = """This is a multi-line string.
This is the second line."""

    print(name)
    print(score)
    print(is_passing)
    print(s)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

First, we create a variable `i` using `let` and assign it the value `5`. We print it, then add `1` to it and print again -- we get `6` as expected. Note that when we reassign `i`, we do _not_ use `let` again -- `let` is only for the first declaration.

Then we declare variables holding different types of data: a string (`"Alice"`), a float (`98.5`), and a boolean (`true`). Notice that Auto uses lowercase `true` and `false` for booleans, which the `a2p` transpiler converts to Python's `True` and `False`.

Finally, we assign a multi-line string to the variable `s` and print it.

## Data Types

Variables can hold values of different types called _data types_. The basic types are numbers and strings, which we have already discussed. Auto is statically typed with type inference -- the compiler can usually figure out the type from the value you assign. You can also specify the type explicitly:

```auto
let age: int = 20
let pi: float = 3.14
let name: str = "Alice"
let is_active: bool = true
```

In later chapters, we will see how to create our own types using the `type` keyword.

> **Note for Python Programmers:**
>
> Auto is statically typed, unlike Python which is dynamically typed. When transpiled to Python by `a2p`, type annotations are preserved as Python type hints (e.g., `age: int = 20`). This means the generated Python code benefits from type checking tools like `mypy`.

## Objects

Remember, Auto refers to anything used in a program as an _object_. This is meant in the generic sense. Instead of saying "the _something_", we say "the _object_".

> **Note for Object Oriented Programming users:**
>
> Auto is strongly object-oriented in the sense that everything is an object including numbers, strings and functions.

## Indentation

Auto uses curly braces `{}` to define blocks of code, not indentation. This is a significant difference from Python, which uses indentation to define blocks.

For example, in Auto:

```auto
fn main() {
    let x = 5
    if x > 3 {
        print("x is greater than 3")
    }
}
```

The `{` and `}` clearly mark where each block begins and ends, regardless of how the code is indented. That said, you should still indent your code consistently for readability -- it is just not required by the language.

> **Note for Python Programmers:**
>
> Python uses indentation to define blocks and has no braces. Auto uses `{}` for blocks, similar to languages like JavaScript, Rust, and C. The `a2p` transpiler converts Auto's brace-delimited blocks into Python's indentation-based blocks automatically.
>
> **Note:** Even though Auto does not require indentation for correctness, always indent your code properly. Consistent indentation (4 spaces per level is the convention) makes your code readable and maintainable.

## Summary

We have covered quite a few topics in this chapter:

- **Comments** use `//` and are ignored by the compiler
- **Literal constants** are values like `5`, `3.14`, and `"hello"`
- **Numbers** include integers and floats
- **Strings** can use single or double quotes, multiline strings use `"""`, and f-strings with `$var` provide convenient formatting
- **Variables** are declared with `let` and follow standard naming rules
- **Data types** include `int`, `float`, `str`, `bool`, and more
- **Everything** in Auto is an object
- **Blocks** are defined with `{}` (not indentation like Python)

Now that we have gone through many nitty-gritty details, we can move on to more interesting stuff such as operators and expressions. Be sure to become comfortable with what you have read in this chapter.
