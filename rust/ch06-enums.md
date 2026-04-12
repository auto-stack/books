# Enums and Pattern Matching

In this chapter, we'll look at _enumerations_, also referred to as _enums_.
Enums allow you to define a type by enumerating its possible variants. First
we'll define and use an enum to show how an enum can encode meaning along with
data. Next, we'll explore a particularly useful enum, called `Option`, which
expresses that a value can be either something or nothing. Then, we'll look at
how pattern matching with the `is` keyword makes it easy to run different code
for different values of an enum. Finally, we'll cover how Auto's `??` operator
provides a concise way to handle optional values.

## Defining an Enum

Where structs give you a way of grouping together related fields and data, like
a `Rectangle` with its `width` and `height`, enums give you a way of saying a
value is one of a possible set of values. For example, we may want to say that
`Rectangle` is one of a set of possible shapes that also includes `Circle` and
`Triangle`. To do this, Auto allows us to encode these possibilities as an enum.

Let's look at a situation we might want to express in code and see why enums
are useful and more appropriate than structs in this case. Say we need to work
with directions. We can _enumerate_ all possible variants, which is where
enumeration gets its name.

<Listing number="6-1" file-name="main.auto" caption="Defining a `Direction` enum">

```auto
enum Direction {
    North
    South
    East
    West
}

fn main() {
    let heading = Direction.North
    print(f"Heading: ${heading}")
}
```

```rust
enum Direction {
    North,
    South,
    East,
    West,
}

fn main() {
    let heading = Direction::North;
    println!("Heading: {}", heading);
}
```

</Listing>

`Direction` is now a custom data type that we can use elsewhere in our code. Note
the key differences from Rust:

| Feature | Auto | Rust |
|---------|------|------|
| Access variant | `Direction.North` | `Direction::North` |
| Display output | `${dir}` (auto Display) | Requires `#[derive(Display)]` |

Auto uses dot notation (`.`) to access enum variants, while Rust uses the double
colon (`::`). Auto also automatically generates a `Display` implementation for
enums, allowing you to use them directly in string interpolation.

### Enum Values

We can create instances of each variant and pass them to functions:

<Listing number="6-2" file-name="main.auto" caption="Passing enum values to functions">

```auto
enum Direction {
    North
    South
    East
    West
}

fn print_direction(dir Direction) {
    print(f"Direction: ${dir}")
}

fn main() {
    let heading = Direction.North
    print_direction(heading)
}
```

```rust
enum Direction {
    North,
    South,
    East,
    West,
}

fn print_direction(dir: Direction) {
    println!("Direction: {}", dir);
}

fn main() {
    let heading = Direction::North;
    print_direction(heading);
}
```

</Listing>

### Enums with Data

One advantage of enums over structs is that each variant can hold different
types and amounts of data. Rather than an enum inside a struct, we can put data
directly into each enum variant:

<Listing number="6-3" file-name="main.auto" caption="An `IpAddr` enum whose variants store `String` values">

```auto
enum IpAddr {
    V4 String
    V6 String
}

fn main() {
    let home = IpAddr.V4("127.0.0.1")
    let loopback = IpAddr.V6("::1")
    print("IP addresses created")
}
```

```rust
enum IpAddr {
    V4(String),
    V6(String),
}

fn main() {
    let home = IpAddr::V4(String::from("127.0.0.1"));
    let loopback = IpAddr::V6(String::from("::1"));
    println!("IP addresses created");
}
```

</Listing>

Each variant can have different types and amounts of associated data. Here's an
example with a mix of empty variants and variants with data:

<Listing number="6-4" file-name="main.auto" caption="A `Message` enum with different data in variants">

```auto
enum Message {
    Quit
    Write String
}

fn main() {
    let msg = Message.Write("hello")
    print("Message created")
}
```

```rust
enum Message {
    Quit,
    Write(String),
}

fn main() {
    let msg = Message::Write(String::from("hello"));
    println!("Message created");
}
```

</Listing>

Key differences:

| Feature | Auto | Rust |
|---------|------|------|
| Empty variant | `Quit` (no parentheses) | `Quit` |
| Data variant | `Write String` | `Write(String)` |
| Construct with data | `Message.Write("hello")` | `Message::Write(String::from("hello"))` |

### Methods on Enums

Just like with structs, we can use the `ext` keyword to define methods on enums:

<Listing number="6-10" file-name="main.auto" caption="Defining methods on an enum with `ext`">

```auto
enum Message {
    Quit
    Write String
}

ext Message {
    fn call() {
        print("Message called")
    }
}

fn main() {
    let msg = Message.Write("hello")
    msg.call()
}
```

```rust
enum Message {
    Quit,
    Write(String),
}

impl Message {
    fn call(&self) {
        println!("Message called");
    }
}

fn main() {
    let msg = Message::Write(String::from("hello"));
    msg.call();
}
```

</Listing>

The `ext` keyword works the same way for enums as it does for structs — it adds
methods (generating Rust `impl` blocks) with implicit `self` and `.field` shorthand.

### The `Option` Enum

Auto's `Option` type is expressed using the `?T` syntax, which represents a value
that could be something or nothing. This is Auto's equivalent of Rust's
`Option<T>`:

```auto
// ?T is syntactic sugar for May<T> (Auto's Option type)
// It can be Some(value) or None
```

```rust
// Option<T> can be Some(value) or None
```

The `?T` syntax eliminates the null reference problem that Tony Hoare famously
called his "billion-dollar mistake." Instead of null, Auto makes you explicitly
handle the case where a value might be absent.

<Listing number="6-7" file-name="main.auto" caption="Using `?T` as a return type with `Some` and `None`">

```auto
fn maybe_value(x int) ?int {
    if x > 0 {
        return Some(x)
    }
    return None
}

fn main() {
    let result1 = maybe_value(10)
    let result2 = maybe_value(-5)
    print("Done")
}
```

```rust
fn maybe_value(x: i32) -> Option<i32> {
    if x > 0 {
        return Some(x);
    }
    return None;
}

fn main() {
    let result1 = maybe_value(10);
    let result2 = maybe_value(-5);
    println!("Done");
}
```

</Listing>

Key differences for Option:

| Feature | Auto | Rust |
|---------|------|------|
| Option type | `?T` | `Option<T>` |
| Has value | `Some(value)` | `Some(value)` |
| No value | `None` | `None` |
| Function return | `fn foo() ?int` | `fn foo() -> Option<i32>` |

Because `?T` and `T` are different types, the compiler won't let you use an
optional value as if it were definitely present. You must explicitly handle the
`None` case.

## Pattern Matching with `is`

Auto uses the `is` keyword for pattern matching, which is equivalent to Rust's
`match` expression. The `is` expression compares a value against a series of
patterns and executes code based on which pattern matches.

### Basic Pattern Matching

<Listing number="6-5" file-name="main.auto" caption="Pattern matching on an enum with `is`">

```auto
enum Coin {
    Penny int
    Nickel int
    Dime int
    Quarter int
}

fn value_in_cents(coin Coin) int {
    is coin {
        Coin.Penny(v) => v
        Coin.Nickel(v) => v
        Coin.Dime(v) => v
        Coin.Quarter(v) => v
    }
}

fn main() {
    let c = Coin.Penny(1)
    print(f"Value: ${value_in_cents(c)}")
}
```

```rust
enum Coin {
    Penny(i32),
    Nickel(i32),
    Dime(i32),
    Quarter(i32),
}

fn value_in_cents(coin: Coin) -> i32 {
    match coin {
        Coin::Penny(v) => v,
        Coin::Nickel(v) => v,
        Coin::Dime(v) => v,
        Coin::Quarter(v) => v,
    }
}

fn main() {
    let c = Coin::Penny(1);
    println!("Value: {}", value_in_cents(c));
}
```

</Listing>

Key differences:

| Feature | Auto | Rust |
|---------|------|------|
| Match keyword | `is value { }` | `match value { }` |
| Wildcard arm | `else =>` | `_ =>` |
| Arm separator | newline (no commas) | commas between arms |
| Pattern syntax | `Variant.Name(binding)` | `Variant::Name(binding)` |

### Patterns That Bind to Values

One of the most powerful features of `is` is that patterns can bind to the
values inside enum variants:

<Listing number="6-6" file-name="main.auto" caption="Destructuring enum variants with `is`">

```auto
enum Atom {
    Int int
    Char char
    Float float
}

fn main() {
    let atom = Atom.Int(11)

    is atom {
        Atom.Int(i) => print(f"Got Int: ${i}")
        Atom.Char(c) => print(f"Got Char: ${c}")
        Atom.Float(f) => print(f"Got Float: ${f}")
    }
}
```

```rust
enum Atom {
    Int(i32),
    Char(char),
    Float(f64),
}

fn main() {
    let atom = Atom::Int(11);

    match atom {
        Atom::Int(i) => println!("Got Int: {}", i),
        Atom::Char(c) => println!("Got Char: {}", c),
        Atom::Float(f) => println!("Got Float: {}", f),
    }
}
```

</Listing>

When `atom` is `Atom.Int(11)`, the pattern `Atom.Int(i)` matches and `i` binds
to the value `11`. The bound variable can then be used in the arm's code.

### Matching `Option` with `is`

We can use `is` to handle `?T` (Option) values, just as we would with any other
enum:

<Listing number="6-8" file-name="main.auto" caption="Using `is` to match on `?int` (Option) values">

```auto
fn plus_one(x ?int) ?int {
    is x {
        None => None
        Some(i) => Some(i + 1)
    }
}

fn main() {
    let five = Some(5)
    let six = plus_one(five)
    let none = plus_one(None)
    print("Done")
}
```

```rust
fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        None => None,
        Some(i) => Some(i + 1),
    }
}

fn main() {
    let five = Some(5);
    let six = plus_one(five);
    let none = plus_one(None);
    println!("Done");
}
```

</Listing>

### Matches Are Exhaustive

Just like Rust's `match`, Auto's `is` is exhaustive — the compiler will ensure
that you handle every possible case. If you forget a case, you'll get a
compile-time error.

### Catch-All with `else`

The `else` arm is the catch-all pattern, equivalent to Rust's `_`:

<Listing number="6-9" file-name="main.auto" caption="Catch-all pattern with `else`">

```auto
fn dice_roll(value int) {
    is value {
        3 => print("Lucky number 3!")
        7 => print("Got a 7!")
        else => print(f"Rolled: ${value}")
    }
}

fn main() {
    dice_roll(3)
    dice_roll(7)
    dice_roll(5)
}
```

```rust
fn dice_roll(value: i32) {
    match value {
        3 => println!("Lucky number 3!"),
        7 => println!("Got a 7!"),
        _ => println!("Rolled: {}", value),
    }
}

fn main() {
    dice_roll(3);
    dice_roll(7);
    dice_roll(5);
}
```

</Listing>

The `else` arm matches any value not specifically listed in other arms. Note
that `else` must come last, since arms are evaluated in order.

## Concise Optional Handling with `??`

The `??` (null coalescing) operator provides a concise way to unwrap an optional
value with a default:

<Listing number="6-11" file-name="main.auto" caption="The `??` null coalescing operator">

```auto
fn main() {
    let x = 10
    let y = x ?? 0
    print(f"y = ${y}")
}
```

```rust
fn main() {
    let x = Some(10);
    let y = x.unwrap_or(0);
    println!("y = {}", y);
}
```

</Listing>

The `??` operator is Auto's equivalent of Rust's `.unwrap_or()` method. If the
left side has a value, it returns that value; otherwise, it returns the right
side as a default.

This is useful when you want to provide a fallback value without the verbosity
of a full `is` match:

```auto
// Verbose: full is match
let result = is optional_value {
    Some(v) => v
    None => default_value
}

// Concise: ?? operator
let result = optional_value ?? default_value
```

## Summary

Auto's enums and pattern matching provide the same power as Rust's, with a more
streamlined syntax:

| Concept | Auto | Rust |
|---------|------|------|
| Define enum | `enum Name { ... }` | `enum Name { ... }` |
| Access variant | `Name.Variant` | `Name::Variant` |
| Data variant | `Variant Type` | `Variant(Type)` |
| Pattern match | `is value { }` | `match value { }` |
| Wildcard arm | `else =>` | `_ =>` |
| Option type | `?T` | `Option<T>` |
| Some value | `Some(value)` | `Some(value)` |
| No value | `None` | `None` |
| Null coalesce | `x ?? default` | `x.unwrap_or(default)` |
| Enum methods | `ext Name { }` | `impl Name { }` |

Enums are a powerful tool in your Auto toolbox. Combined with structs from
Chapter 5, you can create custom types that express the concepts in your
program's domain. The `is` pattern matching and `??` operator make working with
enums and optional values both safe and concise.

Let's move on to Chapter 7 and look at how Auto organizes code with packages and
modules.
