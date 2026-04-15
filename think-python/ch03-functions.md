# Functions

In the previous chapter we used several functions provided by the standard library, like `int` and `float`, and a few provided by the `math` module, like `sqrt` and `pow`. In this chapter, you will learn how to create your own functions and run them. We'll see how one function can call another. And we'll introduce the `for` loop, which is used to repeat a computation.

## Defining New Functions

A **function definition** specifies the name of a new function and the sequence of statements that run when the function is called. Here's an example:

```auto
fn print_lyrics() {
    print("I'm a lumberjack, and I'm okay.")
    print("I sleep all night and I work all day.")
}
```

`fn` is a keyword that indicates this is a function definition. The name of the function is `print_lyrics`. Anything that's a legal variable name is also a legal function name.

The empty parentheses after the name indicate that this function doesn't take any arguments.

The first line of the function definition is called the **header** -- the rest is called the **body**. The header ends with a colon and the body is enclosed in curly braces `{}`. The body of this function contains two print statements; in general, the body of a function can contain any number of statements of any kind.

Defining a function creates a **function object**. Now that we've defined a function, we can call it the same way we call built-in functions:

```auto
print_lyrics()
```

When the function runs, it executes the statements in the body, which display the first two lines of "The Lumberjack Song".

> **Note for Python Programmers:**
>
> Auto uses `fn` instead of Python's `def`, and the function body is enclosed in `{}` instead of using indentation. The `a2p` transpiler converts `fn` to `def` and generates properly indented Python code.

<Listing number="3-1" file-name="define_call.auto" caption="Define and call a function">

```auto
fn print_lyrics() {
    print("I'm a lumberjack, and I'm okay.")
    print("I sleep all night and I work all day.")
}

fn main() {
    // Calling the function
    print_lyrics()
    print()
    print_lyrics()
}
```

```python
def print_lyrics():
    print("I'm a lumberjack, and I'm okay.")
    print("I sleep all night and I work all day.")


def main():
    # Calling the function
    print_lyrics()
    print()
    print_lyrics()


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

We define `print_lyrics` using the `fn` keyword followed by the function name and parentheses. The body, enclosed in `{}`, contains two `print` statements. Inside `main()`, we call `print_lyrics()` twice, with a blank line in between. Each call executes the body of the function from top to bottom.

## Parameters

Some of the functions we have seen require arguments; for example, when you call `abs` you pass a number. Some functions take more than one argument; for example, `math.pow` takes two, the base and the exponent.

Here is a definition for a function that takes an argument:

```auto
fn print_twice(string: str) {
    print(string)
    print(string)
}
```

The variable name in parentheses is a **parameter**. When the function is called, the value of the argument is assigned to the parameter. For example, we can call `print_twice` like this:

```auto
print_twice("Dennis Moore, ")
```

You can also use a variable as an argument:

```auto
let line = "Dennis Moore, "
print_twice(line)
```

In this example, the value of `line` gets assigned to the parameter `string`.

> **Note for Python Programmers:**
>
> Auto uses `string: str` to declare a parameter with its type. The `a2p` transpiler strips the type annotation, producing `string` in the Python output. You can also omit the type annotation in Auto if you prefer.

<Listing number="3-2" file-name="parameters.auto" caption="Function with parameters">

```auto
fn print_twice(string: str) {
    print(string)
    print(string)
}

fn repeat(word: str, n: int) {
    let result = word * n
    print(result)
}

fn main() {
    // Call with a literal argument
    print_twice("Dennis Moore, ")

    // Call with a variable argument
    let line = "Dennis Moore, "
    print_twice(line)

    // Call a function with two parameters
    let spam = "Spam, "
    repeat(spam, 4)
}
```

```python
def print_twice(string):
    print(string)
    print(string)


def repeat(word, n):
    result = word * n
    print(result)


def main():
    # Call with a literal argument
    print_twice("Dennis Moore, ")

    # Call with a variable argument
    line = "Dennis Moore, "
    print_twice(line)

    # Call a function with two parameters
    spam = "Spam, "
    repeat(spam, 4)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`print_twice` takes one parameter, `string`, and prints it twice. `repeat` takes two parameters, `word` and `n`, and prints the word repeated `n` times using the `*` operator on strings.

Inside `main()`, we call `print_twice` with both a literal string and a variable. We also call `repeat` with a string variable and an integer. Notice that the parameter names inside the function (`string`, `word`, `n`) are separate from the variable names in the caller (`line`, `spam`).

## Calling Functions

Once you have defined a function, you can use it inside another function. To demonstrate, we'll write functions that print the lyrics of "The Spam Song":

> Spam, Spam, Spam, Spam,
> Spam, Spam, Spam, Spam,
> Spam, Spam,
> (Lovely Spam, Wonderful Spam!)
> Spam, Spam,

We'll start with the `repeat` function from the previous section. Then we can define higher-level functions that build on it:

```auto
fn first_two_lines() {
    repeat("Spam, ", 4)
    repeat("Spam, ", 4)
}

fn last_three_lines() {
    repeat("Spam, ", 2)
    print("(Lovely Spam, Wonderful Spam!)")
    repeat("Spam, ", 2)
}

fn print_verse() {
    first_two_lines()
    last_three_lines()
}
```

When we run `print_verse`, it calls `first_two_lines`, which calls `repeat`, which calls `print`. That's a lot of functions. Of course, we could have done the same thing with fewer functions, but the point of this example is to show how functions can work together.

## Repetition

If we want to display more than one verse, we can use a `for` statement. Here's a simple example:

```auto
for i in 0..2 {
    print(i)
}
```

The header starts with the keyword `for`, a new variable named `i`, the keyword `in`, and a **range expression** `0..2` which produces the values `0` and `1`. In Auto, as in many programming languages, counting starts from `0`.

When the `for` statement runs, it assigns the first value from the range to `i` and then runs the body, which displays `0`. When it gets to the end of the body, it loops back to the header -- which is why this statement is called a **loop**. The second time through the loop, it assigns the next value to `i`, and displays it. Then, because that's the last value from the range, the loop ends.

Here's how we can use a `for` loop to print two verses of the song:

```auto
for i in 0..2 {
    print("Verse", i)
    print_verse()
    print()
}
```

You can put a `for` loop inside a function. For example, `print_n_verses` takes a parameter named `n` and displays the given number of verses:

```auto
fn print_n_verses(n: int) {
    for i in 0..n {
        print_verse()
        print()
    }
}
```

In this example, we don't use `i` in the body of the loop, but there has to be a variable name in the header anyway.

> **Note for Python Programmers:**
>
> Auto uses `0..n` for ranges instead of Python's `range(n)`. The `a2p` transpiler converts `0..n` to `range(n)` automatically. Auto does not have a `while` statement; use `for` with a range or conditional breaks instead.

<Listing number="3-3" file-name="repetition.auto" caption="Repetition with for loops">

```auto
fn repeat(word: str, n: int) {
    print(word * n)
}

fn first_two_lines() {
    repeat("Spam, ", 4)
    repeat("Spam, ", 4)
}

fn last_three_lines() {
    repeat("Spam, ", 2)
    print("(Lovely Spam, Wonderful Spam!)")
    repeat("Spam, ", 2)
}

fn print_verse() {
    first_two_lines()
    last_three_lines()
}

fn main() {
    // Simple for loop
    print("Counting:")
    for i in 0..3 {
        print(i)
    }

    // Using a for loop to repeat verses
    print("Two verses:")
    for i in 0..2 {
        print("Verse", i)
        print_verse()
    }
}
```

```python
def repeat(word, n):
    print(word * n)


def first_two_lines():
    repeat("Spam, ", 4)
    repeat("Spam, ", 4)


def last_three_lines():
    repeat("Spam, ", 2)
    print("(Lovely Spam, Wonderful Spam!)")
    repeat("Spam, ", 2)


def print_verse():
    first_two_lines()
    last_three_lines()


def main():
    # Simple for loop
    print("Counting:")
    for i in range(3):
        print(i)

    # Using a for loop to repeat verses
    print("Two verses:")
    for i in range(2):
        print("Verse", i)
        print_verse()


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

First, a simple `for` loop counts from `0` to `2` using `0..3`. The range expression `0..3` produces the values `0`, `1`, and `2` -- the upper bound is exclusive, just like Python's `range(3)`.

Then, a second `for` loop uses `0..2` to print two verses of the Spam Song. Each iteration calls `print_verse()`, which in turn calls `first_two_lines()` and `last_three_lines()`, demonstrating how functions can be composed to build more complex behavior from simpler pieces.

## Variables and Parameters Are Local

When you create a variable inside a function, it is **local**, which means that it only exists inside the function. For example, the following function takes two arguments, concatenates them, and prints the result twice:

```auto
fn cat_twice(part1: str, part2: str) {
    let cat = part1 + part2
    print_twice(cat)
}
```

Here's an example that uses it:

```auto
let line1 = "Always look on the "
let line2 = "bright side of life."
cat_twice(line1, line2)
```

When `cat_twice` runs, it creates a local variable named `cat`, which is destroyed when the function ends. If we try to display it outside the function, we get an error -- `cat` is not defined there.

Parameters are also local. For example, outside `cat_twice`, there is no such thing as `part1` or `part2`.

<Listing number="3-4" file-name="local_scope.auto" caption="Local variables and scope">

```auto
fn print_twice(string: str) {
    print(string)
    print(string)
}

fn cat_twice(part1: str, part2: str) {
    // cat is a local variable
    let cat = part1 + part2
    print_twice(cat)
    // cat is destroyed when this function ends
}

fn main() {
    let line1 = "Always look on the "
    let line2 = "bright side of life."
    cat_twice(line1, line2)

    // This would be an error -- cat is local to cat_twice:
    // print(cat)

    // These would also be errors -- parameters are local:
    // print(part1)
    // print(part2)
}
```

```python
def print_twice(string):
    print(string)
    print(string)


def cat_twice(part1, part2):
    # cat is a local variable
    cat = part1 + part2
    print_twice(cat)
    # cat is destroyed when this function ends


def main():
    line1 = "Always look on the "
    line2 = "bright side of life."
    cat_twice(line1, line2)

    # This would be an error -- cat is local to cat_twice:
    # print(cat)

    # These would also be errors -- parameters are local:
    # print(part1)
    # print(part2)


if __name__ == "__main__":
    main()
```

</Listing>

**How It Works**

`cat_twice` receives two parameters, `part1` and `part2`, which are local to that function. It creates another local variable, `cat`, by concatenating the two parameters. When `cat_twice` finishes executing, all of its local variables (`cat`, `part1`, `part2`) are destroyed.

Inside `main()`, we call `cat_twice` with `line1` and `line2`. After the call returns, we cannot access `cat`, `part1`, or `part2` from `main()` -- they only exist inside `cat_twice`. The commented-out lines show what would happen if we tried: we'd get a `NameError` in Python.

## Stack Diagrams

To keep track of which variables can be used where, it is sometimes useful to draw a **stack diagram**. Like state diagrams, stack diagrams show the value of each variable, but they also show the function each variable belongs to.

Each function is represented by a **frame**. A frame is a box with the name of a function on the outside and the parameters and local variables of the function on the inside.

Here's a text representation of the stack diagram for the `cat_twice` example when it is running and has called `print_twice`:

```
+------------------+
| __main__         |
| line1  -> "..."  |
| line2  -> "..."  |
+------------------+
| cat_twice        |
| part1  -> "..."  |
| part2  -> "..."  |
| cat    -> "..."  |
+------------------+
| print_twice      |
| string -> "..."  |
+------------------+
```

The frames are arranged in a stack that indicates which function called which. Reading from the bottom, `print_twice` was called by `cat_twice`, which was called by `__main__` -- which is a special name for the topmost frame. When you create a variable outside of any function, it belongs to `__main__`.

## Tracebacks

When a runtime error occurs in a function, the program displays the name of the function that was running, the name of the function that called it, and so on, up the stack. This list of functions is called a **traceback**.

For example, if `print_twice` tries to access a variable that is local to another function, you get an error. The traceback shows that `cat_twice` called `print_twice`, and the error occurred in `print_twice`.

The order of the functions in the traceback is the same as the order of the frames in the stack diagram. The function that was running when the error occurred is at the bottom.

## Why Functions?

It may not be clear yet why it is worth the trouble to divide a program into functions. There are several reasons:

- **Readability**: Creating a new function gives you an opportunity to name a group of statements, which makes your program easier to read and debug.

- **Eliminating repetition**: Functions can make a program smaller by eliminating repetitive code. Later, if you make a change, you only have to make it in one place.

- **Debugging**: Dividing a long program into functions allows you to debug the parts one at a time and then assemble them into a working whole.

- **Reusability**: Well-designed functions are often useful for many programs. Once you write and debug one, you can reuse it.

## Debugging

Debugging can be frustrating, but it is also challenging, interesting, and sometimes even fun. And it is one of the most important skills you can learn.

In some ways debugging is like detective work. You are given clues and you have to infer the events that led to the results you see.

Debugging is also like experimental science. Once you have an idea about what is going wrong, you modify your program and try again. If your hypothesis was correct, you can predict the result of the modification, and you take a step closer to a working program. If your hypothesis was wrong, you have to come up with a new one.

For some people, programming and debugging are the same thing; that is, programming is the process of gradually debugging a program until it does what you want. The idea is that you should start with a working program and make small modifications, debugging them as you go.

If you find yourself spending a lot of time debugging, that is often a sign that you are writing too much code before you start testing. If you take smaller steps, you might find that you can move faster.

## Glossary

**function definition:**
A statement that creates a function using the `fn` keyword.

**header:**
The first line of a function definition, from `fn` to the opening `{`.

**body:**
The sequence of statements inside a function definition, enclosed in `{}`.

**function object:**
A value created by a function definition. The name of the function is a variable that refers to a function object.

**parameter:**
A name used inside a function to refer to the value passed as an argument.

**loop:**
A statement that runs one or more statements repeatedly.

**local variable:**
A variable defined inside a function, which can only be accessed inside the function.

**stack diagram:**
A graphical representation of a stack of functions, their variables, and the values they refer to.

**frame:**
A box in a stack diagram that represents a function call. It contains the local variables and parameters of the function.

**traceback:**
A list of the functions that are executing, printed when an exception occurs.

## Exercises

### Exercise

Write a function named `print_right` that takes a string named `text` as a parameter and prints the string with enough leading spaces that the last letter of the string is in the 40th column of the display.

Hint: Use the `len` function, the string concatenation operator (`+`) and the string repetition operator (`*`).

### Exercise

Write a function called `triangle` that takes a string and an integer and draws a pyramid with the given height, made up using copies of the string. Here's an example of a pyramid with `5` levels, using the string `'L'`:

```
    L
   LLL
  LLLLL
 LLLLLLL
LLLLLLLLL
```

### Exercise

Write a function called `rectangle` that takes a string and two integers and draws a rectangle with the given width and height, made up using copies of the string. For example, `rectangle("H", 5, 4)` should produce:

```
HHHHH
HHHHH
HHHHH
HHHHH
```

### Exercise

The song "99 Bottles of Beer" starts with this verse:

> 99 bottles of beer on the wall
> 99 bottles of beer
> Take one down, pass it around
> 98 bottles of beer on the wall

Then the second verse is the same, except that it starts with 98 bottles and ends with 97. The song continues until there are 0 bottles of beer.

Write a function called `bottle_verse` that takes a number as a parameter and displays the verse that starts with the given number of bottles.

Hint: Consider starting with a function that can print the first, second, or last line of the verse, and then use it to write `bottle_verse`.
