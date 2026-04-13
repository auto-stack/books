# Appendix

The following sections contain reference material you may find useful in your
Auto journey, with comparisons to Rust equivalents where applicable.

## Appendix A: Keywords

The following lists contain keywords that are reserved for use by the Auto
language. As such, they cannot be used as identifiers. _Identifiers_ are names
of functions, variables, parameters, type fields, modules, packages, constants,
static values, attributes, types, or specs.

### Keywords Currently in Use

The following is a list of all keywords currently in use in Auto, with their
functionality described and the equivalent Rust keyword noted.

| Auto Keyword | Rust Equivalent | Description |
|-------------|----------------|-------------|
| `actor` | _(none)_ | Define an actor type |
| `as` | `as` | Type casting |
| `break` | `break` | Exit a loop immediately |
| `comptime` | _(none)_ | Mark a function for compile-time execution |
| `const` | `const` | Define a constant |
| `continue` | `continue` | Continue to the next loop iteration |
| `dyn` | `dyn` | Dynamic dispatch to a spec object |
| `else` | `else` | Fallback for `if` and `if let` control flow |
| `enum` | `enum` | Define an enumeration |
| `ext` | `impl` | Attach methods to a type |
| `extern` | `extern` | Link an external function or variable |
| `false` | `false` | Boolean false literal |
| `fn` | `fn` | Define a function |
| `for` | `for` | Loop over items from an iterator |
| `has` | _(none)_ | Delegate behavior through composition |
| `if` | `if` | Branch based on a conditional expression |
| `in` | `in` | Part of `for` loop syntax |
| `is` | `match` | Match a value to patterns; compose types |
| `let` | `let` | Bind a variable |
| `loop` | `loop` | Loop unconditionally |
| `mod` | `mod` | Define a module |
| `mut` | `mut` | _(Rust)_ Denote mutability |
| `on` | _(none)_ | Handle actor messages; subscribe to blueprints |
| `pub` | `pub` | Denote public visibility |
| `return` | `return` | Return from function |
| `Self` | `Self` | Type alias for the type being defined |
| `self` | `self` | Method subject |
| `spec` | `trait` | Define a specification (shared behavior interface) |
| `static` | `static` | Global variable |
| `sys` | `unsafe` | Denote system-level (unsafe) code |
| `tell` | _(none)_ | Send a message to an actor |
| `true` | `true` | Boolean true literal |
| `type` | `struct` / `type` | Define a data type or type alias |
| `use` | `use` | Bring symbols into scope |
| `var` | `let mut` | Declare a mutable variable |
| `where` | `where` | Constrain a type with spec bounds |
| `while` | `while` | Loop conditionally |
| `yield` | _(none)_ | Return control to the runtime in a blueprint |

### Auto-Only Keywords

These keywords exist in Auto but have no direct Rust equivalent:

| Keyword | Description |
|---------|-------------|
| `actor` | Defines an actor type that processes messages concurrently |
| `comptime` | Marks a function to execute at compile time |
| `ext` | Attaches methods to a type (replaces Rust's `impl`) |
| `has` | Delegates method calls to a contained type |
| `is` | Pattern matching (replaces `match`) and type composition |
| `on` | Message handler in actors; blueprint subscription |
| `spec` | Defines a behavior specification (replaces Rust's `trait`) |
| `sys` | System-level code (replaces Rust's `unsafe`) |
| `tell` | Sends a message to an actor |
| `var` | Shorthand for mutable variable declaration |

### Rust Keywords Not in Auto

These Rust keywords don't exist in Auto because Auto handles their use cases
differently:

| Rust Keyword | Auto Equivalent | Reason |
|-------------|----------------|--------|
| `async` | `~T` return type | Blueprints are indicated by type, not keyword |
| `await` | `on` block | Subscribe to blueprints instead of awaiting |
| `crate` | _(package root)_ | Auto uses package-based module resolution |
| `impl` | `ext` | Different keyword, same concept |
| `match` | `is` | Different keyword, same pattern syntax |
| `move` | _(implicit)_ | Auto uses implicit move semantics |
| `mut` | `var` | Shorthand for mutable bindings |
| `ref` | _(not needed)_ | AutoFree handles reference semantics |
| `struct` | `type` | Unified type declaration keyword |
| `super` | _(parent reference)_ | Auto uses `use` with parent paths |
| `trait` | `spec` | Renamed for Auto's semantics |
| `union` | `union` | Only a keyword in union declarations |

### Keywords Reserved for Future Use

The following keywords do not yet have any functionality but are reserved by
Auto for potential future use:

- `abstract`
- `become`
- `do`
- `final`
- `macro`
- `override`
- `priv`
- `try`
- `typeof`
- `virtual`

## Appendix B: Operators and Symbols

### Operators

Table B-1 contains the operators in Auto, with comparisons to Rust. Most
operators are identical between the two languages.

| Operator | Example | Description | Auto vs Rust |
|----------|---------|-------------|-------------|
| `!` | `!expr` | Logical complement | Same |
| `!=` | `expr != expr` | Not equal | Same |
| `%` | `expr % expr` | Remainder | Same |
| `%=` | `var %= expr` | Remainder assignment | Same |
| `&` | `&expr` | Borrow / reference | Same |
| `&` | `expr & expr` | Bitwise AND | Same |
| `&&` | `expr && expr` | Logical AND | Same |
| `*` | `expr * expr` | Multiplication | Same |
| `*` | `*expr` | Dereference | Same |
| `+` | `expr + expr` | Addition | Same |
| `+=` | `var += expr` | Addition assignment | Same |
| `-` | `-expr` | Negation | Same |
| `-` | `expr - expr` | Subtraction | Same |
| `-=` | `var -= expr` | Subtraction assignment | Same |
| `->` | `fn() -> type` | Function return type | Same syntax, also used in `is` arms |
| `.` | `expr.ident` | Field access | Same |
| `..` | `..`, `expr..`, `..expr` | Range | Same |
| `..=` | `expr..=expr` | Inclusive range | Same |
| `..` | `Type(x, ..)` | Ignore remaining fields | Same concept, Auto uses `()` not `{}` |
| `/` | `expr / expr` | Division | Same |
| `/=` | `var /= expr` | Division assignment | Same |
| `:` | `ident: type` | Type annotation | Auto: `name Type` (space, not colon) for fields |
| `==` | `expr == expr` | Equality | Same |
| `=>` | `pat => expr` | Match arm | Rust only; Auto uses `->` |
| `@` | `ident @ pat` | Pattern binding | Same |
| `^` | `expr ^ expr` | Bitwise XOR | Same |
| `|` | `pat \| pat` | Pattern alternatives | Same |
| `\|\|` | `expr \|\| expr` | Logical OR | Same |
| `?` | `expr?` | Error propagation | Rust: `expr?` suffix; Auto: `expr!` suffix |
| `~` | `~expr`, `~T` | Blueprint operator | Auto only: creates/transforms blueprints |

### Auto-Specific Operators

| Operator | Example | Description |
|----------|---------|-------------|
| `~` | `~5`, `~T` | Blueprint creation / type operator |
| `~race` | `~race(a, b)` | First-completed blueprint wins |
| `~join` | `~join(a, b)` | Wait for all blueprints |
| `~spawn` | `~spawn(() => {})` | Run blueprint in background |
| `~yield` | `~yield` | Yield control to runtime |
| `~sleep` | `~sleep(ms)` | Non-blocking sleep |
| `!` | `expr!` | Error propagation (postfix) |
| `?` | `?T` | Optional type (prefix on type) |

### Key Syntax Differences: Auto vs Rust

| Feature | Auto | Rust |
|---------|------|------|
| Match arms | `pat -> expr` | `pat => expr,` |
| Error propagation | `expr!` | `expr?` |
| Optional type | `?T` | `Option<T>` |
| Error type | `!T` | `Result<T, E>` |
| Blueprint type | `~T` | `impl Future<Output = T>` |
| Type declaration | `type Name { }` | `struct Name { }` |
| Method block | `ext Name { }` | `impl Name { }` |
| Spec/Trait | `spec Name { }` | `trait Name { }` |
| Pattern match | `is` | `match` |
| Unsafe | `sys { }` | `unsafe { }` |
| Mutable var | `var x = 5` | `let mut x = 5` |
| String format | `f"${x}"` | `format!("{}", x)` |
| Print | `print(x)` | `println!("{}", x)` |
| Assert equal | `assert_eq(a, b)` | `assert_eq!(a, b)` |
| Derive | `#derive[Debug]` | `#[derive(Debug)]` |
| Field separator | `name Type` (space) | `name: Type` (colon) |
| Enum access | `Enum.Variant` | `Enum::Variant` |
| Module path | `use.mod Name` | `use mod::Name;` |

### Non-operator Symbols

| Symbol | Explanation | Auto vs Rust |
|--------|-------------|-------------|
| `"..."` | String literal | Same |
| `'c'` | Character literal | Same |
| `f"..."` | Format string | Auto: `f"${expr}"`; Rust: `format!("{}", expr)` |
| `\|...\| expr` | Closure | Same syntax |
| `_` | Ignored pattern binding | Same |
| `()` | Unit type / empty tuple | Same |
| `.` | Method call / field access | Same |
| `#` | Attribute prefix | Auto: `#derive[...]`; Rust: `#[derive(...)]` |

## Appendix C: Derivable Specs

In various places in the book, we've discussed the `#derive[]` attribute, which
you can apply to a `type` or `enum` definition. The `#derive[]` attribute
generates code that will implement a spec with its default implementation on the
type you've annotated.

This is the Auto equivalent of Rust's `#[derive(...)]` attribute.

<Listing number="C-1" file-name="src/main.at" caption="Using #derive[] on a type">

```auto
#derive[Debug, Eq, Clone]
type Point {
    x int
    y int
}

fn main() {
    let p = Point(x: 1, y: 2)
    print(f"{p:?}")

    let q = p.clone()
    assert_eq(p, q)
}
```

```rust
#[derive(Debug, PartialEq, Clone)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 1, y: 2 };
    println!("{:?}", p);

    let q = p.clone();
    assert_eq!(p, q);
}
```

</Listing>

### `Debug` for Programmer Output

The `Debug` spec enables debug formatting. In Auto, use `{:?}` in format
strings:

```auto
print(f"{my_value:?}")
```

```rust
println!("{:?}", my_value);
```

`Debug` is required for `assert_eq`, which prints values when an assertion
fails.

### `Eq` for Equality Comparisons

The `Eq` spec (equivalent to Rust's `PartialEq` + `Eq`) enables equality
comparison with `==` and `!=`:

```auto
#derive[Eq]
type Color {
    r int
    g int
    b int
}

fn main() {
    let c1 = Color(r: 255, g: 0, b: 0)
    let c2 = Color(r: 255, g: 0, b: 0)
    assert(c1 == c2)
}
```

```rust
#[derive(PartialEq, Eq)]
struct Color {
    r: i32,
    g: i32,
    b: i32,
}

fn main() {
    let c1 = Color { r: 255, g: 0, b: 0 };
    let c2 = Color { r: 255, g: 0, b: 0 };
    assert!(c1 == c2);
}
```

When derived on types, two instances are equal only if _all_ fields are equal.
When derived on enums, each variant equals itself and no others.

### `Ord` for Ordering Comparisons

The `Ord` spec enables comparison operators `<`, `>`, `<=`, `>=`:

```auto
#derive[Ord]
enum Priority {
    Low
    Medium
    High
}
```

```rust
#[derive(PartialOrd, Ord)]
enum Priority {
    Low,
    Medium,
    High,
}
```

When derived on enums, variants declared earlier are considered less than
variants declared later.

### `Clone` for Duplicating Values

The `Clone` spec allows explicit deep copy of a value:

```auto
#derive[Clone]
type Config {
    name String
    value int
}

fn main() {
    let original = Config(name: "test", value: 42)
    let copy = original.clone()
}
```

```rust
#[derive(Clone)]
struct Config {
    name: String,
    value: i32,
}

fn main() {
    let original = Config { name: "test".to_string(), value: 42 };
    let copy = original.clone();
}
```

### `Hash` for Mapping to Fixed-Size Values

The `Hash` spec enables using a type as a key in `HashMap` or `HashSet`:

```auto
#derive[Hash, Eq]
type UserId {
    id int
}

fn main() {
    let mut scores = HashMap<UserId, int>()
    scores.insert(UserId(id: 1), 100)
}
```

```rust
use std::collections::HashMap;

#[derive(Hash, PartialEq, Eq)]
struct UserId {
    id: i32,
}

fn main() {
    let mut scores = HashMap::new();
    scores.insert(UserId { id: 1 }, 100);
}
```

### `Default` for Default Values

The `Default` spec provides a default value for a type:

```auto
#derive[Default]
type Config {
    host String    // defaults to ""
    port int       // defaults to 0
    debug bool     // defaults to false
}

fn main() {
    let config = Config.default()
    // Override specific fields
    let config = Config(host: "localhost", ..Config.default())
}
```

```rust
#[derive(Default)]
struct Config {
    host: String,
    port: i32,
    debug: bool,
}

fn main() {
    let config = Config::default();
    // Override specific fields
    let config = Config { host: "localhost".to_string(), ..Config::default() };
}
```

### Derivable Specs Quick Reference

| Auto Spec | Rust Equivalent | Enables |
|-----------|----------------|---------|
| `Debug` | `Debug` | `{:?}` formatting |
| `Eq` | `PartialEq` + `Eq` | `==`, `!=` operators |
| `Ord` | `PartialOrd` + `Ord` | `<`, `>`, `<=`, `>=` operators |
| `Clone` | `Clone` | `.clone()` method |
| `Copy` | `Copy` | Implicit copy on assignment |
| `Hash` | `Hash` | Use as `HashMap`/`HashSet` key |
| `Default` | `Default` | `.default()` method |

Auto uses `Eq` as a single spec where Rust splits into `PartialEq` + `Eq`.
Similarly, Auto's `Ord` covers both `PartialOrd` + `Ord` from Rust. This
simplification works because Auto doesn't need to handle `NaN` edge cases in
the same way — floating-point types have special handling built into the
language.

### Derive Syntax Comparison

| Feature | Auto | Rust |
|---------|------|------|
| Attribute | `#derive[Debug, Eq]` | `#[derive(Debug, PartialEq, Eq)]` |
| Multiple | Comma-separated in `[]` | Comma-separated in `()` |
| Custom derive | `#apply[comptime_fn]` | Separate proc-macro crate |

## Appendix D: Auto vs Rust — Complete Mapping

This section provides a comprehensive mapping between Auto and Rust concepts
covered throughout the book.

### Type System

| Concept | Auto | Rust |
|---------|------|------|
| Define type | `type Name { field Type }` | `struct Name { field: Type }` |
| Define enum | `enum Name { Variant }` | `enum Name { Variant }` |
| Methods | `ext Name { fn method() {} }` | `impl Name { fn method(&self) {} }` |
| Interface | `spec Name { fn method() }` | `trait Name { fn method(&self); }` |
| Implement spec | `spec Name for Type { }` | `impl Name for Type { }` |
| Generic | `fn name<T>(x T)` | `fn name<T>(x: T)` |
| Spec bound | `fn name<T Spec>(x T)` | `fn name<T: Trait>(x: T)` |
| Optional | `?T` | `Option<T>` |
| Result | `!T` | `Result<T, E>` |
| Blueprint | `~T` | `impl Future<Output = T>` |
| Never type | `!` | `!` |
| Type alias | `type Alias = Type` | `type Alias = Type;` |

### Control Flow

| Concept | Auto | Rust |
|---------|------|------|
| Pattern match | `is` | `match` |
| Match arm | `pat -> expr` | `pat => expr,` |
| Conditional | `if let` | `if let` |
| Error propagate | `expr!` | `expr?` |
| Panic | `panic("msg")` | `panic!("msg")` |

### Concurrency

| Concept | Auto | Rust |
|---------|------|------|
| Unit | Actor | Thread |
| Define | `actor Name { }` | `thread::spawn(\|\| { })` |
| Send message | `actor.tell(Msg)` | `tx.send(msg)` |
| Receive | `on Msg(data) { }` | `rx.recv()` |
| Async type | `~T` | `impl Future<Output = T>` |
| Await | `on bp as v { }` | `bp.await` |
| Race | `~race(a, b)` | `tokio::select!` |
| Join | `~join(a, b)` | `tokio::join!(a, b)` |

### OOP

| Concept | Auto | Rust |
|---------|------|------|
| Composition | `is Type` | Manual embedding |
| Delegation | `has Type` | Manual delegation |
| Dynamic dispatch | `dyn Spec` | `dyn Trait` |

### Metaprogramming

| Concept | Auto | Rust |
|---------|------|------|
| Derive | `#derive[Spec]` | `#[derive(Trait)]` |
| Compile-time | `comptime fn` | Procedural macro |
| Conditional | `#if[debug]` | `#[cfg(debug)]` |
| Unsafe | `sys { }` | `unsafe { }` |

## Appendix E: Auto Package Tooling

### `automan` vs `cargo`

| Command | Auto (`automan`) | Rust (`cargo`) |
|---------|-----------------|----------------|
| New project | `automan new name` | `cargo new name` |
| Build | `automan build` | `cargo build` |
| Run | `automan run` | `cargo run` |
| Test | `automan test` | `cargo test` |
| Check | `automan check` | `cargo check` |
| Add dependency | `automan add pkg` | Add to `Cargo.toml` |
| Build release | `automan build --release` | `cargo build --release` |
| Package file | `auto.toml` | `Cargo.toml` |
| Source directory | `src/` | `src/` |
| Entry point | `src/main.at` | `src/main.rs` |

Auto transpiles to C, so `automan build` ultimately produces a native binary
through the system's C compiler. This means Auto programs can call C libraries
directly without additional FFI bindings.
