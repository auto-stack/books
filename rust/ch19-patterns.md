# Patterns and Matching

Patterns are a special syntax in Auto for matching against the structure of
types, both complex and simple. Using patterns in conjunction with `is`
expressions and other constructs gives you more control over a program's
control flow. A pattern consists of some combination of the following:

- Literals
- Destructured arrays, enums, types, or tuples
- Variables
- Wildcards
- Placeholders

Some example patterns include `x`, `(a, 3)`, and `Some(Color.Red)`. In the
contexts in which patterns are valid, these components describe the shape of
data. Our program then matches values against the patterns to determine whether
it has the correct shape of data to continue running a particular piece of
code.

To use a pattern, we compare it to some value. If the pattern matches the
value, we use the value parts in our code. Recall the `is` expressions in
Chapter 6 that used patterns, such as the coin-sorting machine example. If the
value fits the shape of the pattern, we can use the named pieces. If it
doesn't, the code associated with the pattern won't run.

This chapter is a reference on all things related to patterns. We'll cover the
valid places to use patterns, the difference between refutable and irrefutable
patterns, and the different kinds of pattern syntax that you might see. By the
end of the chapter, you'll know how to use patterns to express many concepts in
a clear way.

> **Note:** Auto uses the `is` keyword where Rust uses `match`. The pattern
> syntax is nearly identical, but the keyword is different: `value is { ... }`
> instead of `match value { ... }`.

## All the Places Patterns Can Be Used

Patterns pop up in a number of places in Auto, and you've been using them a lot
without realizing it! This section discusses all the places where patterns are
valid.

### `is` Arms

As discussed in Chapter 6, we use patterns in the arms of `is` expressions.
Formally, `is` expressions are defined as the keyword `is`, a value to match
on, and one or more arms that consist of a pattern and an expression to run if
the value matches that arm's pattern, like this:

```auto
value is {
    PATTERN -> EXPRESSION
    PATTERN -> EXPRESSION
    PATTERN -> EXPRESSION
}
```

For example, here's the `is` expression from Chapter 6 that matches on a
`?int` value in the variable `x`:

<Listing number="19-1" file-name="src/main.at" caption="Matching on an optional value with `is`">

```auto
x is {
    None -> None
    Some(i) -> Some(i + 1)
}
```

```rust
match x {
    None => None,
    Some(i) => Some(i + 1),
}
```

</Listing>

One requirement for `is` expressions is that they need to be _exhaustive_ — all
possibilities for the value must be accounted for. One way to ensure that you've
covered every possibility is to have a catch-all pattern for the last arm: a
variable name matching any value can never fail and thus covers every remaining
case.

The particular pattern `_` will match anything, but it never binds to a
variable, so it's often used in the last arm.

### `let` Statements

Every time you use a `let` statement, you've been using patterns. More
formally, a `let` statement looks like this:

```auto
let PATTERN = EXPRESSION
```

<Listing number="19-2" file-name="src/main.at" caption="Using a pattern to destructure a tuple">

```auto
fn main() {
    let (x, y, z) = (1, 2, 3)
}
```

```rust
fn main() {
    let (x, y, z) = (1, 2, 3);
}
```

</Listing>

Here, we match a tuple against a pattern. Auto compares the value `(1, 2, 3)`
to the pattern `(x, y, z)` and sees that the value matches the pattern — that
is, it sees that the number of elements is the same in both — so Auto binds
`1` to `x`, `2` to `y`, and `3` to `z`.

If the number of elements in the pattern doesn't match the number of elements
in the tuple, the overall type won't match and we'll get a compiler error.

### Conditional `if let` Expressions

In Chapter 6, we discussed how to use `if let` expressions mainly as a shorter
way to write the equivalent of an `is` that only matches one case.

<Listing number="19-3" file-name="src/main.at" caption="Mixing `if let`, `else if`, and `else if let`">

```auto
fn main() {
    let favorite_color ?String = None
    let is_tuesday = false
    let age = "34".parse()

    if let Some(color) = favorite_color {
        print(f"Using your favorite color, ${color}, as the background")
    } else if is_tuesday {
        print("Tuesday is green day!")
    } else if let Ok(age) = age {
        if age > 30 {
            print("Using purple as the background color")
        } else {
            print("Using orange as the background color")
        }
    } else {
        print("Using blue as the background color")
    }
}
```

```rust
fn main() {
    let favorite_color: Option<&str> = None;
    let is_tuesday = false;
    let age: Result<u8, _> = "34".parse();

    if let Some(color) = favorite_color {
        println!("Using your favorite color, {color}, as the background");
    } else if is_tuesday {
        println!("Tuesday is green day!");
    } else if let Ok(age) = age {
        if age > 30 {
            println!("Using purple as the background color");
        } else {
            println!("Using orange as the background color");
        }
    } else {
        println!("Using blue as the background color");
    }
}
```

</Listing>

Auto uses the same `if let` syntax as Rust. The `if let` can also introduce
new variables that shadow existing variables, just like Rust.

### `while let` Conditional Loops

Similar to `if let`, the `while let` conditional loop allows a `while` loop to
run for as long as a pattern continues to match:

<Listing number="19-4" file-name="src/main.at" caption="Using `while let` to process messages">

```auto
fn main() {
    let (tx, rx) = channel()
    spawn(() => {
        for val in [1, 2, 3] {
            tx.send(val)
        }
    })

    while let Ok(value) = rx.recv() {
        print(value)
    }
}
```

```rust
fn main() {
    let (tx, rx) = std::sync::mpsc::channel();
    std::thread::spawn(move || {
        for val in [1, 2, 3] {
            tx.send(val).unwrap();
        }
    });

    while let Ok(value) = rx.recv() {
        println!("{value}");
    }
}
```

</Listing>

This example prints `1`, `2`, and then `3`.

### `for` Loops

In a `for` loop, the value that directly follows the keyword `for` is a
pattern. Listing 19-5 demonstrates how to use a pattern in a `for` loop to
destructure a tuple.

<Listing number="19-5" file-name="src/main.at" caption="Using a pattern in a `for` loop to destructure a tuple">

```auto
fn main() {
    let v = ['a', 'b', 'c']

    for (index, value) in v.enumerate() {
        print(f"${value} is at index ${index}")
    }
}
```

```rust
fn main() {
    let v = vec!['a', 'b', 'c'];

    for (index, value) in v.iter().enumerate() {
        println!("{value} is at index {index}");
    }
}
```

</Listing>

### Function Parameters

Function parameters are also patterns. We can destructure tuples in function
parameters:

<Listing number="19-6" file-name="src/main.at" caption="A function with parameters that destructure a tuple">

```auto
fn print_coordinates(&(x, y) &(int, int)) {
    print(f"Current location: (${x}, ${y})")
}

fn main() {
    let point = (3, 5)
    print_coordinates(&point)
}
```

```rust
fn print_coordinates(&(x, y): &(i32, i32)) {
    println!("Current location: ({x}, {y})");
}

fn main() {
    let point = (3, 5);
    print_coordinates(&point);
}
```

</Listing>

This code prints `Current location: (3, 5)`. The values `&(3, 5)` match the
pattern `&(x, y)`, so `x` is `3` and `y` is `5`.

## Refutability: Whether a Pattern Might Fail to Match

Patterns come in two forms: _refutable_ and _irrefutable_. Patterns that will
match for any possible value passed are _irrefutable_. An example would be `x`
in the statement `let x = 5` because `x` matches anything and therefore cannot
fail to match. Patterns that can fail to match for some possible value are
_refutable_. An example would be `Some(x)` in the expression `if let Some(x) =
a_value` because if the value is `None`, the `Some(x)` pattern will not match.

Function parameters, `let` statements, and `for` loops can only accept
irrefutable patterns because the program cannot do anything meaningful when
values don't match. The `if let` and `while let` expressions accept refutable
and irrefutable patterns.

If we try to use a refutable pattern where an irrefutable pattern is required,
the compiler will produce an error:

<Listing number="19-7" file-name="src/main.at" caption="Using `let else` with a refutable pattern">

```auto
fn main() {
    let some_option_value ?int = None
    let Some(x) = some_option_value else {
        return
    }
}
```

```rust
fn main() {
    let some_option_value: Option<i32> = None;
    let Some(x) = some_option_value else {
        return;
    };
}
```

</Listing>

The `let ... else` form handles the case where the pattern doesn't match.

## Pattern Syntax

### Matching Literals

<Listing number="19-8" file-name="src/main.at" caption="Matching literal values">

```auto
fn main() {
    let x = 1

    x is {
        1 -> print("one")
        2 -> print("two")
        3 -> print("three")
        _ -> print("anything")
    }
}
```

```rust
fn main() {
    let x = 1;

    match x {
        1 => println!("one"),
        2 => println!("two"),
        3 => println!("three"),
        _ => println!("anything"),
    }
}
```

</Listing>

This code prints `one` because the value in `x` is `1`.

### Matching Named Variables

Named variables are irrefutable patterns that match any value. However, there
is a complication when you use named variables in `is` expressions. Because
`is` starts a new scope, variables declared as part of a pattern inside these
expressions will shadow those with the same name outside:

<Listing number="19-9" file-name="src/main.at" caption="Variable shadowing in `is` arms">

```auto
fn main() {
    let x = Some(5)
    let y = 10

    x is {
        Some(50) -> print("Got 50")
        Some(y) -> print(f"Matched, y = ${y}")
        _ -> print(f"Default case, x = ${x}")
    }

    print(f"at the end: x = ${x}, y = ${y}")
}
```

```rust
fn main() {
    let x = Some(5);
    let y = 10;

    match x {
        Some(50) => println!("Got 50"),
        Some(y) => println!("Matched, y = {y}"),
        _ => println!("Default case, x = {x:?}"),
    }

    println!("at the end: x = {x:?}, y = {y}");
}
```

</Listing>

This prints `Matched, y = 5` because the `Some(y)` pattern introduces a new
`y` that shadows the outer `y = 10`. At the end, it prints `at the end: x =
Some(5), y = 10` because the inner `y`'s scope has ended.

### Matching Multiple Patterns with `|`

<Listing number="19-10" file-name="src/main.at" caption="Matching multiple patterns with `|`">

```auto
fn main() {
    let x = 1

    x is {
        1 | 2 -> print("one or two")
        3 -> print("three")
        _ -> print("anything")
    }
}
```

```rust
fn main() {
    let x = 1;

    match x {
        1 | 2 => println!("one or two"),
        3 => println!("three"),
        _ => println!("anything"),
    }
}
```

</Listing>

### Matching Ranges with `..=`

<Listing number="19-11" file-name="src/main.at" caption="Matching a range of values">

```auto
fn main() {
    let x = 5

    x is {
        1..=5 -> print("one through five")
        _ -> print("something else")
    }
}
```

```rust
fn main() {
    let x = 5;

    match x {
        1..=5 => println!("one through five"),
        _ => println!("something else"),
    }
}
```

</Listing>

If `x` is `1`, `2`, `3`, `4`, or `5`, the first arm will match. Ranges are
only allowed with numeric or `char` values.

### Destructuring to Break Apart Values

#### Types (Structs)

<Listing number="19-12" file-name="src/main.at" caption="Destructuring a type's fields">

```auto
type Point {
    x int
    y int
}

fn main() {
    let p = Point(x: 0, y: 7)

    let Point(x, y) = p
    assert_eq(0, x)
    assert_eq(7, y)
}
```

```rust
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 0, y: 7 };
    let Point { x, y } = p;
    assert_eq!(0, x);
    assert_eq!(7, y);
}
```

</Listing>

We can also destructure with literal values as part of the pattern:

<Listing number="19-13" file-name="src/main.at" caption="Destructuring and matching literal values">

```auto
type Point {
    x int
    y int
}

fn main() {
    let p = Point(x: 0, y: 7)

    p is {
        Point(x, y: 0) -> print(f"On the x axis at ${x}")
        Point(x: 0, y) -> print(f"On the y axis at ${y}")
        Point(x, y) -> print(f"On neither axis: (${x}, ${y})")
    }
}
```

```rust
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 0, y: 7 };

    match p {
        Point { x, y: 0 } => println!("On the x axis at {x}"),
        Point { x: 0, y } => println!("On the y axis at {y}"),
        Point { x, y } => {
            println!("On neither axis: ({x}, {y})");
        }
    }
}
```

</Listing>

This prints `On the y axis at 7` because `x` is `0`.

#### Enums

<Listing number="19-14" file-name="src/main.at" caption="Destructuring enum variants">

```auto
enum Message {
    Quit
    Move(x int, y int)
    Write(text String)
    ChangeColor(r int, g int, b int)
}

fn main() {
    let msg = Message.ChangeColor(0, 160, 255)

    msg is {
        Message.Quit -> {
            print("The Quit variant has no data to destructure.")
        }
        Message.Move(x, y) -> {
            print(f"Move in the x direction ${x} and in the y direction ${y}")
        }
        Message.Write(text) -> {
            print(f"Text message: ${text}")
        }
        Message.ChangeColor(r, g, b) -> {
            print(f"Change color to red ${r}, green ${g}, and blue ${b}")
        }
    }
}
```

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

fn main() {
    let msg = Message::ChangeColor(0, 160, 255);

    match msg {
        Message::Quit => {
            println!("The Quit variant has no data to destructure.");
        }
        Message::Move { x, y } => {
            println!("Move in the x direction {x} and in the y direction {y}");
        }
        Message::Write(text) => {
            println!("Text message: {text}");
        }
        Message::ChangeColor(r, g, b) => {
            println!("Change color to red {r}, green {g}, and blue {b}");
        }
    }
}
```

</Listing>

This prints `Change color to red 0, green 160, and blue 255`.

#### Nested Destructuring

<Listing number="19-15" file-name="src/main.at" caption="Matching on nested enums">

```auto
enum Color {
    Rgb(int, int, int)
    Hsv(int, int, int)
}

enum Message {
    Quit
    Move(x int, y int)
    Write(text String)
    ChangeColor(Color)
}

fn main() {
    let msg = Message.ChangeColor(Color.Hsv(0, 160, 255))

    msg is {
        Message.ChangeColor(Color.Rgb(r, g, b)) -> {
            print(f"Change color to red ${r}, green ${g}, and blue ${b}")
        }
        Message.ChangeColor(Color.Hsv(h, s, v)) -> {
            print(f"Change color to hue ${h}, saturation ${s}, value ${v}")
        }
        _ -> {}
    }
}
```

```rust
enum Color {
    Rgb(i32, i32, i32),
    Hsv(i32, i32, i32),
}

enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(Color),
}

fn main() {
    let msg = Message::ChangeColor(Color::Hsv(0, 160, 255));

    match msg {
        Message::ChangeColor(Color::Rgb(r, g, b)) => {
            println!("Change color to red {r}, green {g}, and blue {b}");
        }
        Message::ChangeColor(Color::Hsv(h, s, v)) => {
            println!("Change color to hue {h}, saturation {s}, value {v}");
        }
        _ => (),
    }
}
```

</Listing>

### Ignoring Values in a Pattern

#### An Entire Value with `_`

<Listing number="19-16" file-name="src/main.at" caption="Using `_` to ignore a value">

```auto
fn foo(_ int, y int) {
    print(f"This code only uses the y parameter: ${y}")
}

fn main() {
    foo(3, 4)
}
```

```rust
fn foo(_: i32, y: i32) {
    println!("This code only uses the y parameter: {y}");
}

fn main() {
    foo(3, 4);
}
```

</Listing>

#### Parts of a Value with a Nested `_`

<Listing number="19-17" file-name="src/main.at" caption="Ignoring parts of a tuple">

```auto
fn main() {
    let numbers = (2, 4, 8, 16, 32)

    numbers is {
        (first, _, third, _, fifth) -> {
            print(f"Some numbers: ${first}, ${third}, ${fifth}")
        }
    }
}
```

```rust
fn main() {
    let numbers = (2, 4, 8, 16, 32);

    match numbers {
        (first, _, third, _, fifth) => {
            println!("Some numbers: {first}, {third}, {fifth}");
        }
    }
}
```

</Listing>

This prints `Some numbers: 2, 8, 32`.

#### An Unused Variable Starting with `_`

If you create a variable but don't use it, Auto will issue a warning. You can
suppress the warning by starting the name with an underscore: `_x` still binds
the value, but `_` does not bind at all. This distinction matters for ownership:
`_` won't move the value, but `_x` will.

#### Remaining Parts with `..`

<Listing number="19-18" file-name="src/main.at" caption="Ignoring remaining fields with `..`">

```auto
type Point {
    x int
    y int
    z int
}

fn main() {
    let origin = Point(x: 0, y: 0, z: 0)

    origin is {
        Point(x, ..) -> print(f"x is ${x}")
    }
}
```

```rust
struct Point {
    x: i32,
    y: i32,
    z: i32,
}

fn main() {
    let origin = Point { x: 0, y: 0, z: 0 };

    match origin {
        Point { x, .. } => println!("x is {x}"),
    }
}
```

</Listing>

The `..` pattern ignores any parts of a value that we haven't explicitly
matched. It must be unambiguous — you can only use `..` once per pattern.

### Match Guards

A _match guard_ is an additional `if` condition, specified after the pattern in
an `is` arm, that must also match for that arm to be chosen:

<Listing number="19-19" file-name="src/main.at" caption="Adding a match guard to a pattern">

```auto
fn main() {
    let num = Some(4)

    num is {
        Some(x) if x % 2 == 0 -> print(f"The number ${x} is even")
        Some(x) -> print(f"The number ${x} is odd")
        None -> {}
    }
}
```

```rust
fn main() {
    let num = Some(4);

    match num {
        Some(x) if x % 2 == 0 => println!("The number {x} is even"),
        Some(x) => println!("The number {x} is odd"),
        None => (),
    }
}
```

</Listing>

This prints `The number 4 is even`.

Match guards are useful for expressing more complex ideas than a pattern alone
allows. You can also use the guard to compare against outer variables:

<Listing number="19-20" file-name="src/main.at" caption="Using a match guard to compare with an outer variable">

```auto
fn main() {
    let x = Some(5)
    let y = 10

    x is {
        Some(50) -> print("Got 50")
        Some(n) if n == y -> print(f"Matched, n = ${n}")
        _ -> print(f"Default case, x = ${x}")
    }

    print(f"at the end: x = ${x}, y = ${y}")
}
```

```rust
fn main() {
    let x = Some(5);
    let y = 10;

    match x {
        Some(50) => println!("Got 50"),
        Some(n) if n == y => println!("Matched, n = {n}"),
        _ => println!("Default case, x = {x:?}"),
    }

    println!("at the end: x = {x:?}, y = {y}");
}
```

</Listing>

### `@` Bindings

The `@` operator lets us create a variable that holds a value at the same time
we're testing that value for a pattern match:

<Listing number="19-21" file-name="src/main.at" caption="Using `@` to bind while testing">

```auto
enum Message {
    Hello(id int)
}

fn main() {
    let msg = Message.Hello(id: 5)

    msg is {
        Message.Hello(id @ 3..=7) -> {
            print(f"Found an id in range: ${id}")
        }
        Message.Hello(id @ 10..=12) -> {
            print("Found an id in another range")
        }
        Message.Hello(id) -> print(f"Found some other id: ${id}")
    }
}
```

```rust
enum Message {
    Hello { id: i32 },
}

fn main() {
    let msg = Message::Hello { id: 5 };

    match msg {
        Message::Hello { id: id @ 3..=7 } => {
            println!("Found an id in range: {id}")
        }
        Message::Hello { id: 10..=12 } => {
            println!("Found an id in another range");
        }
        Message::Hello { id } => println!("Found some other id: {id}"),
    }
}
```

</Listing>

This prints `Found an id in range: 5`. By specifying `id @` before the range
`3..=7`, we capture whatever value matched the range while also testing it.

## `is` vs `match` Quick Reference

| Feature | Auto (`is`) | Rust (`match`) |
|---------|-------------|----------------|
| Keyword | `is` | `match` |
| Arm syntax | `PATTERN -> EXPR` | `PATTERN => EXPR,` |
| Exhaustiveness | Required | Required |
| Wildcard | `_` | `_` |
| Multiple patterns | `1 \| 2` | `1 \| 2` |
| Range | `1..=5` | `1..=5` |
| Match guard | `if condition` | `if condition` |
| Binding | `x @ 1..=5` | `x @ 1..=5` |
| Ignore rest | `..` | `..` |
| Destructure type | `Type(x, y)` | `Type { x, y }` |
| Destructure enum | `Enum.Variant(x)` | `Enum::Variant(x)` |

## Summary

Auto's patterns are very useful in distinguishing between different kinds of
data. When used in `is` expressions, Auto ensures that your patterns cover
every possible value, or your program won't compile. Patterns in `let`
statements and function parameters make those constructs more useful, enabling
the destructuring of values into smaller parts and assigning those parts to
variables. We can create simple or complex patterns to suit our needs.

The key syntactic difference from Rust is the use of `is` instead of `match`,
and `->` instead of `=>`. The pattern syntax itself — literals, variables,
wildcards, ranges, guards, and `@` bindings — is nearly identical.

In the next chapter, we'll look at some advanced aspects of Auto's features,
including `sys` (Auto's equivalent of `unsafe`) and comptime metaprogramming.
