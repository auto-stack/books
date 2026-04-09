# Common Programming Concepts

This chapter covers concepts that appear in almost every programming language
and how they work in Auto. Many programming languages have much in common at
their core. None of the concepts presented in this chapter are unique to Auto,
but we'll discuss them in the context of Auto and explain the conventions
around using them.

Specifically, you'll learn about variables, basic types, functions, comments,
and control flow. These foundations will be in every Auto program, and learning
them early will give you a strong core to start from.

> #### Keywords
>
> The Auto language has a set of _keywords_ that are reserved for use by the
> language only, much as in other languages. Keep in mind that you cannot use
> these words as names of variables or functions. Most of the keywords have
> special meanings, and you'll be using them to do various tasks in your Auto
> programs. You can find the list of the keywords in Appendix A.

## Variables and Mutability

As mentioned in the "Storing Values with Variables" section of Chapter 2, by
default, variables are immutable. This is one of many nudges Auto gives you to
write your code in a way that takes advantage of the safety and easy concurrency
that Auto offers. However, you still have the option to make your variables
mutable. Let's explore how and why Auto encourages you to favor immutability
and why sometimes you might want to opt out.

When a variable is immutable, once a value is bound to a name, you can't change
that value. To illustrate, create a new project called _variables_:

```console
$ automan new variables
$ cd variables
```

Then, in your new _variables_ directory, open _src/main.auto_ and replace its
code with the following, which won't compile just yet:

<span class="filename">Filename: src/main.auto</span>

```auto,ignore,does_not_compile
fn main() ! {
    let x = 5
    println("The value of x is: " + x.to_string())
    x = 6
    println("The value of x is: " + x.to_string())
}
```

```rust,ignore,does_not_compile
fn main() {
    let x = 5;
    println!("The value of x is: {x}");
    x = 6;
    println!("The value of x is: {x}");
}
```

Save and run the program using `automan run`. You should receive an error
message:

```text
error: cannot assign twice to immutable variable `x`
```

This example shows how the compiler helps you find errors in your programs.
Compiler errors can be frustrating, but they only mean your program isn't safely
doing what you want it to do yet; they do _not_ mean that you're not a good
programmer!

You received the error message `cannot assign twice to immutable variable x`
because you tried to assign a second value to the immutable `x` variable.

It's important that we get compile-time errors when we attempt to change a
value that's designated as immutable, because this very situation can lead to
bugs. If one part of our code operates on the assumption that a value will
never change and another part of our code changes that value, it's possible
that the first part of the code won't do what it was designed to do. The Auto
compiler guarantees that when you state that a value won't change, it really
won't change, so you don't have to keep track of it yourself.

But mutability can be very useful and can make code more convenient to write.
In Auto, you make a variable mutable by using `var` instead of `let`. Using
`var` also conveys intent to future readers of the code by indicating that
other parts of the code will be changing this variable's value.

For example, let's change _src/main.auto_ to the following:

<span class="filename">Filename: src/main.auto</span>

```auto
fn main() ! {
    var x = 5
    println("The value of x is: " + x.to_string())
    x = 6
    println("The value of x is: " + x.to_string())
}
```

```rust
fn main() {
    let mut x = 5;
    println!("The value of x is: {x}");
    x = 6;
    println!("The value of x is: {x}");
}
```

When we run the program now, we get this:

```console
$ automan run
   Compiling variables v0.1.0
    Finished dev [unoptimized + debuginfo] target(s) in 0.30s
     Running `target/debug/variables`
The value of x is: 5
The value of x is: 6
```

We're allowed to change the value bound to `x` from `5` to `6` when `var` is
used. Ultimately, deciding whether to use mutability or not is up to you and
depends on what you think is clearest in that particular situation.

### Declaring Constants

Like immutable variables, _constants_ are values that are bound to a name and
are not allowed to change, but there are a few differences between constants
and variables.

First, you aren't allowed to use `var` with constants. Constants aren't just
immutable by default—they're always immutable. You declare constants using the
`const` keyword instead of the `let` keyword, and the type of the value _must_
be annotated.

Constants can be declared in any scope, including the global scope, which makes
them useful for values that many parts of code need to know about.

The last difference is that constants may be set only to a constant expression,
not the result of a value that could only be computed at runtime.

Here's an example of a constant declaration:

```auto
const THREE_HOURS_IN_SECONDS: int = 60 * 60 * 3
```

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

The constant's name is `THREE_HOURS_IN_SECONDS`, and its value is set to the
result of multiplying 60 (seconds in a minute) by 60 (minutes in an hour) by 3
(hours). Auto's naming convention for constants is to use all uppercase with
underscores between words.

### Shadowing

As you saw in the guessing game tutorial in Chapter 2, you can declare a new
variable with the same name as a previous variable. We say that the first
variable is _shadowed_ by the second. In effect, the second variable
overshadows the first, taking any uses of the variable name to itself until
either it itself is shadowed or the scope ends.

In Auto, we can shadow a variable by using the same variable's name and
repeating the `let` keyword:

<span class="filename">Filename: src/main.auto</span>

```auto
fn main() ! {
    let x = 5
    let x = x + 1
    {
        let x = x * 2
        println("The value of x in the inner scope is: " + x.to_string())
    }
    println("The value of x is: " + x.to_string())
}
```

```rust
fn main() {
    let x = 5;
    let x = x + 1;
    {
        let x = x * 2;
        println!("The value of x in the inner scope is: {x}");
    }
    println!("The value of x is: {x}");
}
```

This program first binds `x` to a value of `5`. Then, it creates a new variable
`x` by repeating `let x =`, taking the original value and adding `1` so the
value of `x` is `6`. Then, within an inner scope, the third `let` shadows `x`
and multiplies the previous value by `2` to give `x` a value of `12`. When that
scope is over, the inner shadowing ends and `x` returns to being `6`.

Shadowing is different from using `var` because we'll get a compile-time error
if we accidentally try to reassign to a `let` variable without using the `let`
keyword. By using `let`, we can perform a few transformations on a value but
have the variable be immutable after those transformations have completed.

The other difference between `var` and shadowing is that because we're
effectively creating a new variable when we use the `let` keyword again, we can
change the type of the value but reuse the same name:

```auto
let spaces = "   "
let spaces = spaces.length()
```

```rust
let spaces = "   ";
let spaces = spaces.len();
```

The first `spaces` variable is a string type, and the second `spaces` variable
is a number type. Shadowing spares us from having to come up with different
names like `spaces_str` and `spaces_num`.

## Data Types

Every value in Auto is of a certain _data type_, which tells Auto what kind of
data is being specified so that it knows how to work with that data. We'll look
at two data type subsets: scalar and compound.

Keep in mind that Auto is a _statically typed_ language, which means that it
must know the types of all variables at compile time. The compiler can usually
infer what type we want to use based on the value and how we use it. In cases
when many types are possible, we must add a type annotation:

```auto
let guess: int = "42".to_int().expect("Not a number!")
```

```rust
let guess: u32 = "42".parse().expect("Not a number!");
```

### Scalar Types

A _scalar_ type represents a single value. Auto has four primary scalar types:
integers, floating-point numbers, Booleans, and characters.

#### Integer Types

An _integer_ is a number without a fractional component. Table 3-1 shows the
built-in integer types in Auto.

<span class="caption">Table 3-1: Integer Types in Auto</span>

| Length  | Signed  | Unsigned |
| ------- | ------- | -------- |
| 8-bit   | `i8`    | `u8`     |
| 16-bit  | `i16`   | `u16`    |
| 32-bit  | `i32`   | `u32`    |
| 64-bit  | `i64`   | `u64`    |
| 128-bit | `i128`  | `u128`   |
| Architecture-dependent | `isize` | `usize`  |

_Signed_ and _unsigned_ refer to whether it's possible for the number to be
negative. Signed numbers are stored using two's complement representation.

You can write integer literals in any of the forms shown in Table 3-2.

<span class="caption">Table 3-2: Integer Literals in Auto</span>

| Number literals  | Example       |
| ---------------- | ------------- |
| Decimal          | `98_222`      |
| Hex              | `0xff`        |
| Octal            | `0o77`        |
| Binary           | `0b1111_0000` |
| Byte (`u8` only) | `b'A'`        |

Number literals can use `_` as a visual separator to make the number easier to
read, such as `1_000`. The default integer type is `i32`.

> ##### Integer Overflow
>
> If you try to change a variable to a value outside the range of its type,
> _integer overflow_ will occur. In debug mode, Auto will panic at runtime.
> In release mode, Auto performs two's complement wrapping. To explicitly
> handle overflow, Auto provides methods like `wrapping_add`, `checked_add`,
> and `saturating_add`.

#### Floating-Point Types

Auto has two primitive types for _floating-point numbers_: `f32` and `f64`,
which are 32 bits and 64 bits in size, respectively. The default type is `f64`
because on modern CPUs, it's roughly the same speed as `f32` but is capable of
more precision.

<span class="filename">Filename: src/main.auto</span>

```auto
fn main() ! {
    let x = 2.0      // f64
    let y: f32 = 3.0 // f32
}
```

```rust
fn main() {
    let x = 2.0; // f64
    let y: f32 = 3.0; // f32
}
```

Floating-point numbers are represented according to the IEEE-754 standard.

#### Numeric Operations

Auto supports the basic mathematical operations for all number types: addition,
subtraction, multiplication, division, and remainder. Integer division truncates
toward zero.

<span class="filename">Filename: src/main.auto</span>

```auto
fn main() ! {
    // addition
    let sum = 5 + 10
    // subtraction
    let difference = 95.5 - 4.3
    // multiplication
    let product = 4 * 30
    // division
    let quotient = 56.7 / 32.2
    // remainder
    let remainder = 43 % 5
}
```

```rust
fn main() {
    // addition
    let sum = 5 + 10;
    // subtraction
    let difference = 95.5 - 4.3;
    // multiplication
    let product = 4 * 30;
    // division
    let quotient = 56.7 / 32.2;
    // remainder
    let remainder = 43 % 5;
}
```

#### The Boolean Type

A Boolean type in Auto has two possible values: `true` and `false`. Booleans
are one byte in size. The Boolean type is specified using `bool`.

```auto
fn main() ! {
    let t = true
    let f: bool = false
}
```

```rust
fn main() {
    let t = true;
    let f: bool = false;
}
```

#### The Character Type

Auto's `char` type is the language's most primitive alphabetic type:

```auto
fn main() ! {
    let c = 'z'
    let z: char = 'Z'
    let heart_eyed_cat = '😻'
}
```

```rust
fn main() {
    let c = 'z';
    let z: char = 'Z';
    let heart_eyed_cat = '😻';
}
```

Note that `char` literals use single quotes, as opposed to string literals,
which use double quotes. Auto's `char` type is 4 bytes in size and represents a
Unicode scalar value.

### Compound Types

_Compound types_ can group multiple values into one type. Auto has two primitive
compound types: tuples and arrays.

#### The Tuple Type

A _tuple_ is a general way of grouping together a number of values with a
variety of types into one compound type. Tuples have a fixed length: Once
declared, they cannot grow or shrink in size.

<span class="filename">Filename: src/main.auto</span>

```auto
fn main() ! {
    let tup: (int, f64, bool) = (500, 6.4, true)
    let (x, y, z) = tup
    println("The value of y is: " + y.to_string())
}
```

```rust
fn main() {
    let tup: (i32, f64, bool) = (500, 6.4, true);
    let (x, y, z) = tup;
    println!("The value of y is: {y}");
}
```

We can also access a tuple element directly by using a period (`.`) followed by
the index:

```auto
let five_hundred = tup.0
let six_point_four = tup.1
```

```rust
let five_hundred = tup.0;
let six_point_four = tup.1;
```

The tuple without any values is called _unit_, written `()`. Expressions
implicitly return the unit value if they don't return any other value.

#### The Array Type

Another way to have a collection of multiple values is with an _array_. Unlike
a tuple, every element of an array must have the same type. Arrays in Auto have
a fixed length.

```auto
let a = [1, 2, 3, 4, 5]
```

```rust
let a = [1, 2, 3, 4, 5];
```

Arrays are useful when you want your data allocated on the stack rather than the
heap, or when you want to ensure that you always have a fixed number of
elements.

You write an array's type using square brackets with the type of each element,
a semicolon, and then the number of elements:

```auto
let a: [int; 5] = [1, 2, 3, 4, 5]
```

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

You can also initialize an array to contain the same value for each element:

```auto
let a = [3; 5]  // same as [3, 3, 3, 3, 3]
```

```rust
let a = [3; 5]; // same as [3, 3, 3, 3, 3]
```

#### Array Element Access

You can access elements of an array using indexing:

```auto
let a = [1, 2, 3, 4, 5]
let first = a[0]
let second = a[1]
```

```rust
let a = [1, 2, 3, 4, 5];
let first = a[0];
let second = a[1];
```

#### Invalid Array Element Access

If you try to access an element past the end of the array, Auto will panic at
runtime:

```console
thread 'main' panicked at src/main.auto:19:19:
index out of bounds: the len is 5 but the index is 10
```

This is an example of Auto's memory safety principles in action. Auto protects
you against invalid memory access by immediately exiting instead of allowing
the access and continuing.

## Functions

Functions are prevalent in Auto code. You've already seen one of the most
important functions in the language: the `main` function, which is the entry
point of many programs. You've also seen the `fn` keyword, which allows you to
declare new functions.

Auto code uses _snake case_ as the conventional style for function and variable
names, in which all letters are lowercase and underscores separate words.

<span class="filename">Filename: src/main.auto</span>

```auto
fn main() ! {
    println("Hello, world!")
    another_function()
}

fn another_function() {
    println("Another function.")
}
```

```rust
fn main() {
    println!("Hello, world!");
    another_function();
}

fn another_function() {
    println!("Another function.");
}
```

Note that we defined `another_function` _after_ the `main` function in the
source code; we could have defined it before as well. Auto doesn't care where
you define your functions, only that they're defined somewhere in a scope that
can be seen by the caller.

### Parameters

We can define functions to have _parameters_, which are special variables that
are part of a function's signature:

```auto
fn main() ! {
    another_function(5)
}

fn another_function(x: int) {
    println("The value of x is: " + x.to_string())
}
```

```rust
fn main() {
    another_function(5);
}

fn another_function(x: i32) {
    println!("The value of x is: {x}");
}
```

In function signatures, you _must_ declare the type of each parameter. This is
a deliberate decision in Auto's design: requiring type annotations in function
definitions means the compiler almost never needs you to use them elsewhere in
the code to figure out what type you mean.

When defining multiple parameters, separate the parameter declarations with
commas:

```auto
fn print_labeled_measurement(value: int, unit_label: char) {
    println("The value is: " + value.to_string() + unit_label)
}
```

```rust
fn print_labeled_measurement(value: i32, unit_label: char) {
    println!("The value is: {value}{unit_label}");
}
```

### Statements and Expressions

Function bodies are made up of a series of statements optionally ending in an
expression. Because Auto is an expression-based language, this is an important
distinction to understand.

- _Statements_ are instructions that perform some action and do not return a
  value.
- _Expressions_ evaluate to a resultant value.

Creating a variable and assigning a value to it with `let` is a statement.
Function definitions are also statements. Statements do not return values.
Therefore, you can't assign a `let` statement to another variable.

Expressions evaluate to a value and make up most of the rest of the code that
you'll write in Auto. A new scope block created with curly brackets is an
expression, for example:

```auto
fn main() ! {
    let y = {
        let x = 3
        x + 1
    }
    println("The value of y is: " + y.to_string())
}
```

```rust
fn main() {
    let y = {
        let x = 3;
        x + 1
    };
    println!("The value of y is: {y}");
}
```

The block evaluates to `4`. That value gets bound to `y` as part of the `let`
statement. Note the `x + 1` line without a semicolon at the end—expressions do
not include ending semicolons. If you add a semicolon to the end of an
expression, you turn it into a statement, and it will then not return a value.

Note that in Auto, semicolons are optional in most places. The compiler uses
line breaks and context to determine where statements end. However, within a
block expression that returns a value, you should not add a semicolon after the
final expression.

### Functions with Return Values

Functions can return values to the code that calls them. We don't name return
values, but we must declare their type after an arrow (`->`). In Auto, the
return value of the function is synonymous with the value of the final
expression in the block of the body of a function. You can return early from a
function by using the `return` keyword, but most functions return the last
expression implicitly.

<span class="filename">Filename: src/main.auto</span>

```auto
fn five() -> int {
    5
}

fn main() ! {
    let x = five()
    println("The value of x is: " + x.to_string())
}
```

```rust
fn five() -> i32 {
    5
}

fn main() {
    let x = five();
    println!("The value of x is: {x}");
}
```

There are no function calls, macros, or even `let` statements in the `five`
function—just the number `5` by itself. That's a perfectly valid function in
Auto. The `5` is the function's return value because it's the final expression.

Let's look at another example:

```auto
fn plus_one(x: int) -> int {
    x + 1
}
```

```rust
fn plus_one(x: i32) -> i32 {
    x + 1
}
```

## Comments

All programmers strive to make their code easy to understand, but sometimes
extra explanation is warranted. In these cases, programmers leave _comments_ in
their source code that the compiler will ignore but that people reading the
source code may find useful.

Here's a simple comment:

```auto
// hello, world
```

In Auto, comments start with two slashes, and the comment continues until the
end of the line. For comments that extend beyond a single line, you'll need to
include `//` on each line:

```auto
// So we're doing something complicated here, long enough that we need
// multiple lines of comments to do it! Whew!
```

Comments can also be placed at the end of lines containing code:

```auto
let x = 5 // this is also a comment
```

Auto also has documentation comments, which we'll discuss in Chapter 14.

## Control Flow

The ability to run some code depending on whether a condition is `true` and the
ability to run some code repeatedly while a condition is `true` are basic
building blocks in most programming languages. The most common constructs that
let you control the flow of execution of Auto code are `if` expressions and
loops.

### `if` Expressions

An `if` expression allows you to branch your code depending on conditions:

<span class="filename">Filename: src/main.auto</span>

```auto
fn main() ! {
    let number = 3
    if number < 5 {
        println("condition was true")
    } else {
        println("condition was false")
    }
}
```

```rust
fn main() {
    let number = 3;
    if number < 5 {
        println!("condition was true");
    } else {
        println!("condition was false");
    }
}
```

All `if` expressions start with the keyword `if`, followed by a condition. The
condition _must_ be a `bool`. Auto will not automatically try to convert
non-Boolean types to a Boolean.

#### Handling Multiple Conditions with `else if`

You can use multiple conditions by combining `if` and `else` in an `else if`
expression:

```auto
let number = 6

if number % 4 == 0 {
    println("number is divisible by 4")
} else if number % 3 == 0 {
    println("number is divisible by 3")
} else if number % 2 == 0 {
    println("number is divisible by 2")
} else {
    println("number is not divisible by 4, 3, or 2")
}
```

```rust
let number = 6;

if number % 4 == 0 {
    println!("number is divisible by 4");
} else if number % 3 == 0 {
    println!("number is divisible by 3");
} else if number % 2 == 0 {
    println!("number is divisible by 2");
} else {
    println!("number is not divisible by 4, 3, or 2");
}
```

Using too many `else if` expressions can clutter your code. Chapter 6 describes
Auto's `is` keyword for pattern matching, which is a more powerful branching
construct for these cases.

#### Using `if` in a `let` Statement

Because `if` is an expression, we can use it on the right side of a `let`
statement:

```auto
let condition = true
let number = if condition { 5 } else { 6 }
```

```rust
let condition = true;
let number = if condition { 5 } else { 6 };
```

The values that have the potential to be results from each arm of the `if` must
be the same type.

### Repetition with Loops

It's often useful to execute a block of code more than once. Auto provides
several _loops_: `loop`, `while`, and `for`.

#### Repeating Code with `loop`

The `loop` keyword tells Auto to execute a block of code over and over again
either forever or until you explicitly tell it to stop:

```auto
fn main() ! {
    loop {
        println("again!")
    }
}
```

```rust
fn main() {
    loop {
        println!("again!");
    }
}
```

You can place the `break` keyword within the loop to tell the program when to
stop executing. We also used `continue` in the guessing game, which tells the
program to skip over any remaining code in this iteration and go to the next.

#### Returning Values from Loops

You can add the value you want returned after the `break` expression:

```auto
fn main() ! {
    var counter = 0
    let result = loop {
        counter += 1
        if counter == 10 {
            break counter * 2
        }
    }
    println("The result is " + result.to_string())
}
```

```rust
fn main() {
    let mut counter = 0;
    let result = loop {
        counter += 1;
        if counter == 10 {
            break counter * 2;
        }
    };
    println!("The result is {result}");
}
```

#### Loop Labels

If you have loops within loops, `break` and `continue` apply to the innermost
loop. You can optionally specify a _loop label_ to disambiguate:

```auto
'counting_up: loop {
    println("count = " + count.to_string())
    var remaining = 10
    loop {
        println("remaining = " + remaining.to_string())
        if remaining == 9 {
            break
        }
        if count == 2 {
            break 'counting_up
        }
        remaining -= 1
    }
    count += 1
}
```

#### Conditional Loops with `while`

A program will often need to evaluate a condition within a loop. The `while`
loop is a built-in construct for this:

```auto
let mut number = 3
while number != 0 {
    println(number.to_string() + "!")
    number -= 1
}
println("LIFTOFF!!!")
```

```rust
let mut number = 3;
while number != 0 {
    println!("{number}!");
    number -= 1;
}
println!("LIFTOFF!!!");
```

#### Looping Through a Collection with `for`

You can use a `for` loop to iterate over the elements of a collection:

```auto
let a = [10, 20, 30, 40, 50]
for element in a {
    println("the value is: " + element.to_string())
}
```

```rust
let a = [10, 20, 30, 40, 50];
for element in a {
    println!("the value is: {element}");
}
```

The safety and conciseness of `for` loops make them the most commonly used loop
construct in Auto. Even when you want to run code a certain number of times,
most Auto developers would use a `for` loop with a range:

```auto
for number in (1..4).rev() {
    println(number.to_string() + "!")
}
println("LIFTOFF!!!")
```

```rust
for number in (1..4).rev() {
    println!("{number}!");
}
println!("LIFTOFF!!!");
```

## Summary

You made it! This was a sizable chapter: You learned about variables, scalar
and compound data types, functions, comments, `if` expressions, and loops! To
practice with the concepts discussed in this chapter, try building programs to
do the following:

- Convert temperatures between Fahrenheit and Celsius.
- Generate the *n*th Fibonacci number.
- Print the lyrics to "The Twelve Days of Christmas," taking advantage of the
  repetition in the song.

When you're ready to move on, we'll talk about a concept in Auto that
_doesn't_ commonly exist in other programming languages: its memory model.
