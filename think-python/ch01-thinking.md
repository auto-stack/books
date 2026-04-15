# Programming as a Way of Thinking

The first goal of this book is to teach you how to program in Auto.
But learning to program means learning a new way of thinking, so the second goal is to help you think like a computer scientist.
This way of thinking combines some of the best features of mathematics, engineering, and natural science.
Like mathematicians, computer scientists use formal languages to denote ideas -- specifically, computations.
Like engineers, they design things, assembling components into systems and evaluating trade-offs among alternatives.
Like scientists, they observe the behavior of complex systems, form hypotheses, and test predictions.

We will start with the most basic elements of programming and work our way up.
In this chapter, we'll see how Auto represents numbers, letters, and words.
And you'll learn to perform arithmetic operations.

You will also start to learn the vocabulary of programming, including terms like **operator**, **expression**, **value**, and **type**.
This vocabulary is important -- you will need it to understand the rest of the book, to communicate with other programmers, and to use tools effectively.

## Arithmetic Operators

An **arithmetic operator** is a symbol that represents an arithmetic computation.
For example, the plus sign, `+`, performs addition.

```auto
30 + 12
```

The minus sign, `-`, is the operator that performs subtraction.

```auto
43 - 1
```

The asterisk, `*`, performs multiplication.

```auto
6 * 7
```

And the forward slash, `/`, performs division.

```auto
84 / 2
```

Notice that the result of the division is `42.0` rather than `42`.
That's because there are two types of numbers in Auto:

- **integers**, which represent numbers with no fractional or decimal part, and

- **floating-point numbers**, which represent integers and numbers with a decimal point.

If you add, subtract, or multiply two integers, the result is an integer.
But if you divide two integers, the result is a floating-point number.

Auto provides another operator, `//`, that performs **integer division** (also called "floor division").
The result of integer division is always an integer -- it always rounds down (toward the "floor").

```auto
84 // 2    // result is 42
85 // 2    // result is 42 (rounds down, not 42.5)
```

The modulus operator, `%`, computes the remainder of integer division.

```auto
85 % 2     // result is 1
```

Finally, the operator `**` performs **exponentiation**; that is, it raises a number to a power.

```auto
7 ** 2     // result is 49
2 ** 10    // result is 1024
```

> **Note for Python Programmers:**
>
> Auto shares the same arithmetic operators as Python: `+`, `-`, `*`, `/`, `//`, `%`, and `**`. These are transpiled directly by `a2p` with no changes.

## Expressions

A collection of operators and numbers is called an **expression**.
An expression can contain any number of operators and numbers.
For example, here's an expression that contains two operators.

```auto
6 + 6 ** 2
```

Notice that exponentiation happens before addition.
Auto follows the standard order of operations: exponentiation happens before multiplication and division, which happen before addition and subtraction.

In the following example, multiplication happens before addition.

```auto
12 + 5 * 6
```

If you want the addition to happen first, you can use parentheses.

```auto
(12 + 5) * 6
```

Every expression has a **value**.
For example, the expression `6 * 7` has the value `42`.

<Listing number="1-1" file-name="arithmetic.auto" caption="Arithmetic operations in Auto">

```auto
fn main() {
    // Basic arithmetic
    print(30 + 12)
    print(43 - 1)
    print(6 * 7)
    print(84 / 2)

    // Integer division (floor division)
    print(84 // 2)
    print(85 // 2)

    // Modulus (remainder)
    print(85 % 2)

    // Exponentiation
    print(7 ** 2)
    print(2 ** 10)

    // Order of operations
    print(6 + 6 ** 2)
    print(12 + 5 * 6)
    print((12 + 5) * 6)
}
```

```python
def main():
    # Basic arithmetic
    print(30 + 12)
    print(43 - 1)
    print(6 * 7)
    print(84 / 2)

    # Integer division (floor division)
    print(84 // 2)
    print(85 // 2)

    # Modulus (remainder)
    print(85 % 2)

    # Exponentiation
    print(7 ** 2)
    print(2 ** 10)

    # Order of operations
    print(6 + 6 ** 2)
    print(12 + 5 * 6)
    print((12 + 5) * 6)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

This program demonstrates all seven arithmetic operators in Auto. The first four lines show the four basic operations: addition (`+`), subtraction (`-`), multiplication (`*`), and division (`/`). Notice that `84 / 2` produces `42.0` (a float), not `42` (an integer) -- this is because regular division always returns a float.

The integer division operator `//` always rounds down. So `85 // 2` is `42`, not `42.5`. The modulus operator `%` returns the remainder, so `85 % 2` is `1`. Exponentiation uses `**`: `7 ** 2` is `49`, and `2 ** 10` is `1024`.

The last three lines show the order of operations. In `6 + 6 ** 2`, exponentiation happens first, so this is `6 + 36 = 42`. In `12 + 5 * 6`, multiplication happens first, so this is `12 + 30 = 42`. With parentheses, `(12 + 5) * 6`, the addition happens first: `17 * 6 = 102`.

## Arithmetic Functions

In addition to the arithmetic operators, Auto provides built-in functions that work with numbers.

The `round` function takes a floating-point number and rounds it off to the nearest integer.

```auto
42.4.round()    // result is 42
42.6.round()    // result is 43
```

The `abs` function computes the absolute value of a number.

```auto
42.abs()        // result is 42
(-42).abs()     // result is 42
```

> **Note for Python Programmers:**
>
> In Python, you call these as `round(42.4)` and `abs(-42)`. In Auto, methods are called on values directly: `42.4.round()` and `(-42).abs()`. The `a2p` transpiler converts these to the equivalent Python function calls.

When we use a function like this, we say we're **calling** the function.
An expression that calls a function is a **function call**.

## Strings

In addition to numbers, Auto can also represent sequences of letters, which are called **strings** because the letters are strung together like beads on a necklace.
To write a string, we put a sequence of characters inside quotation marks.

```auto
"Hello"
'world'
```

Both single and double quotes work. Double quotes make it easy to include an apostrophe.

```auto
"it's a small world."
```

Strings can also contain spaces, punctuation, and digits.

```auto
"Well, "
```

The `+` operator works with strings; it joins two strings into a single string, which is called **concatenation**.

```auto
"Well, " + "it's a small " + "world."
```

The `*` operator also works with strings; it makes multiple copies of a string and concatenates them.

```auto
"Spam, " * 4
```

Auto provides a `len` function that computes the length of a string.

```auto
"Spam".len()    // result is 4
```

Notice that `len` counts the characters between the quotes, but not the quotes themselves.

Auto supports **f-strings** for string formatting. The syntax uses a `$` prefix before variable names inside the string.

```auto
let name = "Alice"
let age = 30
print(f"My name is $name and I am $age years old.")
```

> **Note for Python Programmers:**
>
> In Python, f-strings use `{name}` syntax. In Auto, the same feature uses `$name` syntax. The `a2p` transpiler converts `f"$name"` to `f"{name}"` automatically.

<Listing number="1-2" file-name="strings.auto" caption="String operations in Auto">

```auto
fn main() {
    // Strings with single and double quotes
    print("Hello")
    print('world')

    // String with apostrophe using double quotes
    print("it's a small world.")

    // String concatenation with +
    print("Well, " + "it's a small " + "world.")

    // String repetition with *
    print("Spam, " * 4)

    // String length
    print("Spam".len())

    // f-string with $ interpolation
    let name = "Alice"
    let age = 30
    print(f"My name is $name and I am $age years old.")
}
```

```python
def main():
    # Strings with single and double quotes
    print("Hello")
    print("world")

    # String with apostrophe using double quotes
    print("it's a small world.")

    # String concatenation with +
    print("Well, " + "it's a small " + "world.")

    # String repetition with *
    print("Spam, " * 4)

    # String length
    print(len("Spam"))

    # f-string with {var} interpolation
    name = "Alice"
    age = 30
    print(f"My name is {name} and I am {age} years old.")


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

We start by printing strings with both single and double quotes. Double quotes are especially useful when the string contains an apostrophe (`"it's a small world."`).

String concatenation uses the `+` operator to join three strings end-to-end. The `*` operator repeats a string: `"Spam, " * 4` produces `"Spam, Spam, Spam, Spam, "`. The `.len()` method returns the number of characters in a string -- `"Spam"` has 4 characters.

The f-string `f"My name is $name and I am $age years old."` uses `$name` and `$age` to interpolate variables. In the Python output, these become `{name}` and `{age}`.

## Values and Types

So far we've seen three kinds of values:

- `2` is an integer,

- `42.0` is a floating-point number, and

- `"Hello"` is a string.

A kind of value is called a **type**.
Every value has a type -- or we sometimes say it "belongs to" a type.

The types we have seen so far are:

- `int` for integers (whole numbers like `42`, `-7`, `1_000_000`)

- `float` for floating-point numbers (numbers with a decimal point like `3.14`, `0.5`)

- `str` for strings (sequences of characters like `"Hello, World!"`)

- `bool` for boolean values (`true` or `false`)

The type names `int`, `float`, and `str` can also be used to **convert** values from one type to another.
For example, `int` can take a floating-point number and convert it to an integer (always rounding down).

```auto
42.9.int()      // result is 42
```

And `float` can convert an integer to a floating-point value.

```auto
42.float()      // result is 42.0
```

Now, here's something that can be confusing.
What do you get if you put a sequence of digits in quotes?

```auto
"126"
```

It looks like a number, but it is actually a string.
If you try to use it like a number, you might get an error.
If you have a string that contains digits, you can use `int` to convert it to an integer.

```auto
int("126") / 3     // result is 42.0
```

If you have a string that contains digits and a decimal point, you can use `float` to convert it.

```auto
float("12.6")      // result is 12.6
```

When you write a large integer, you can use underscores to make it easier to read.

```auto
1_000_000          // one million
```

> **Note for Python Programmers:**
>
> In Python, type conversions are function calls: `int(42.9)`, `float(42)`, `int("126")`. In Auto, these are method calls on values: `42.9.int()`, `42.float()`, `int("126")`. The `a2p` transpiler converts all of these to the standard Python function-call form.
>
> Auto uses lowercase `true` and `false` for booleans, which `a2p` converts to Python's `True` and `False`.

<Listing number="1-3" file-name="type-conversion.auto" caption="Type conversion in Auto">

```auto
fn main() {
    // Built-in arithmetic functions
    print(42.4.round())
    print(42.6.round())

    // Absolute value
    print(42.abs())
    print((-42).abs())

    // Values and types
    // type(2)        -> int
    // type(42.0)     -> float
    // type("Hello")  -> str

    // Type conversion
    print(42.9.int())      // float to int (rounds down)
    print(42.float())      // int to float

    // String that looks like a number
    print(int("126"))      // string to int
    print(float("12.6"))   // string to float

    // Using converted values in arithmetic
    print(int("126") / 3)

    // Large numbers with underscores
    print(1_000_000)
}
```

```python
def main():
    # Built-in arithmetic functions
    print(round(42.4))
    print(round(42.6))

    # Absolute value
    print(abs(42))
    print(abs(-42))

    # Values and types
    # type(2)        -> int
    # type(42.0)     -> float
    # type("Hello")  -> str

    # Type conversion
    print(int(42.9))      # float to int (rounds down)
    print(float(42))      # int to float

    # String that looks like a number
    print(int("126"))     # string to int
    print(float("12.6"))  # string to float

    # Using converted values in arithmetic
    print(int("126") / 3)

    # Large numbers with underscores
    print(1_000_000)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

The first group of calls shows built-in functions: `42.4.round()` returns `42` and `42.6.round()` returns `43`. The `abs` function returns the absolute value -- `(-42).abs()` returns `42`.

The type conversion section shows how to convert between types. `42.9.int()` converts a float to an integer by rounding down (truncating), giving `42`. `42.float()` converts an integer to a float, giving `42.0`.

Converting strings to numbers is essential when you receive numeric input as text. `int("126")` turns the string `"126"` into the integer `126`. Once converted, you can use it in arithmetic: `int("126") / 3` produces `42.0`.

Finally, `1_000_000` shows how underscores can be used in numeric literals for readability. Auto (and Python) ignore the underscores when evaluating the number.

## Formal and Natural Languages

**Natural languages** are the languages people speak, like English, Spanish, and French.
They were not designed by people; they evolved naturally.

**Formal languages** are languages that are designed by people for specific applications.
For example, the notation that mathematicians use is a formal language that is particularly good at denoting relationships among numbers and symbols.
Similarly, programming languages are formal languages that have been designed to express computations.

Although formal and natural languages have some features in common, there are important differences:

- **Ambiguity**: Natural languages are full of ambiguity, which people deal with by using contextual clues and other information.
  Formal languages are designed to be nearly or completely unambiguous, which means that any program has exactly one meaning, regardless of context.

- **Redundancy**: In order to make up for ambiguity and reduce misunderstandings, natural languages use redundancy.
  As a result, they are often verbose.
  Formal languages are less redundant and more concise.

- **Literalness**: Natural languages are full of idiom and metaphor.
  Formal languages mean exactly what they say.

Because we all grow up speaking natural languages, it is sometimes hard to adjust to formal languages.
Formal languages are more dense than natural languages, so it takes longer to read them.
Also, the structure is important, so it is not always best to read from top to bottom, left to right.
Finally, the details matter.
Small errors in spelling and punctuation, which you can get away with in natural languages, can make a big difference in a formal language.

## Debugging

Programmers make mistakes.
For whimsical reasons, programming errors are called **bugs** and the process of tracking them down is called **debugging**.

There are three main kinds of errors you will encounter:

1. **Syntax errors**: Something is wrong with the structure of the program.
   For example, leaving out parentheses in a function call, or using a backtick instead of a quotation mark for a string.
   The compiler detects syntax errors before it runs the program.

2. **Runtime errors**: The program has correct syntax, but something goes wrong while it is running.
   For example, trying to divide a string by a number produces a runtime error.

3. **Logic errors (also called semantic errors)**: The program runs without producing an error message, but it does not do what you intended.

Programming, and especially debugging, sometimes brings out strong emotions.
If you are struggling with a difficult bug, you might feel angry, sad, or embarrassed.
Preparing for these reactions might help you deal with them.
One approach is to think of the computer as an employee with certain strengths, like speed and precision, and particular weaknesses, like lack of empathy and inability to grasp the big picture.

Your job is to be a good manager: find ways to take advantage of the strengths and mitigate the weaknesses.
And find ways to use your emotions to engage with the problem, without letting your reactions interfere with your ability to work effectively.

Learning to debug can be frustrating, but it is a valuable skill that is useful for many activities beyond programming.

## Glossary

**arithmetic operator:**
A symbol, like `+` and `*`, that denotes an arithmetic operation like addition or multiplication.

**integer:**
A type that represents numbers with no fractional or decimal part. In Auto, the type is `int`.

**floating-point:**
A type that represents integers and numbers with decimal parts. In Auto, the type is `float`.

**integer division:**
An operator, `//`, that divides two numbers and rounds down to an integer.

**modulus:**
An operator, `%`, that computes the remainder of integer division.

**exponentiation:**
An operator, `**`, that raises a number to a power.

**expression:**
A combination of variables, values, and operators.

**value:**
An integer, floating-point number, string, or boolean -- or one of other kinds of values we will see later.

**function:**
A named sequence of statements that performs some useful operation.

**function call:**
An expression that runs a function. In Auto, it consists of the function name followed by arguments in parentheses.

**syntax error:**
An error in a program that makes it impossible to parse -- and therefore impossible to run.

**runtime error:**
An error that does not occur until the program has started running.

**string:**
A type that represents sequences of characters. In Auto, the type is `str`.

**concatenation:**
Joining two strings end-to-end using the `+` operator.

**type:**
A category of values. The types we have seen so far are `int`, `float`, `str`, and `bool`.

**operand:**
One of the values on which an operator operates.

**natural language:**
Any of the languages that people speak that evolved naturally.

**formal language:**
Any of the languages that people have designed for specific purposes, such as representing mathematical ideas or computer programs.

**bug:**
An error in a program.

**debugging:**
The process of finding and correcting errors.

## Exercises

### Exercise 1

When you learn about a new feature, you should try it out and make mistakes on purpose.
That way, you learn the error messages, and when you see them again, you will know what they mean.

1. You can use a minus sign to make a negative number like `-2`. What happens if you put a plus sign before a number? What about `2++2`?

2. What happens if you have two values with no operator between them, like `4 2`?

3. If you call a function like `42.4.round()`, what happens if you leave out the parentheses?

### Exercise 2

The following questions give you a chance to practice writing arithmetic expressions.

1. How many seconds are there in 42 minutes 42 seconds?

2. How many miles are there in 10 kilometers? Hint: there are 1.61 kilometers in a mile.

3. If you run a 10 kilometer race in 42 minutes 42 seconds, what is your average pace in seconds per mile?

4. What is your average pace in minutes and seconds per mile?

5. What is your average speed in miles per hour?

Write an Auto program that computes and prints the answers.

### Exercise 3

Think about the following questions and try to answer them before you run any code:

1. What is the type of `765`?

2. What is the type of `2.718`?

3. What is the type of `"2 pi"`?

4. What is the result of `"126" + "3"`? Why is it not `"129"`?

5. What is the result of `int("126") + int("3")`?

Now write an Auto program to check your answers.
