# Appendix A: Keyword Reference

This appendix lists every keyword, operator, and built-in construct in the Auto language, organized by category. Each entry includes a one-line description, the chapter where it was first introduced, and a minimal usage example.

---

## 1. Declarations

| Keyword | Description | Chapter | Example |
|---------|-------------|---------|---------|
| `fn` | Define a function or method | Ch. 3 | `fn add(a int, b int) int { a + b }` |
| `let` | Declare an immutable binding | Ch. 2 | `let x = 10` |
| `var` | Declare a mutable binding | Ch. 2 | `var count = 0` |
| `const` | Declare a compile-time constant | Ch. 2 | `const MAX_SIZE = 1024` |
| `type` | Define a custom data type (struct) | Ch. 6 | `type Point { x f64, y f64 }` |
| `enum` | Define a tagged union or C-style enum | Ch. 7 | `enum Color { RED = 1, GREEN = 2 }` |
| `task` | Define an actor task | Ch. 15 | `task Counter { var count int = 0 }` |
| `mod` | Declare a module | Ch. 10 | `mod network { ... }` |
| `use` | Import a module or package | Ch. 10 | `use io` |
| `use.rust` | Import a Rust stdlib type | Ch. 10 | `use.rust std::collections::HashMap` |
| `import` | Import a specific item from a module | Ch. 10 | `import fmt::println` |
| `pub` | Mark an item as publicly visible | Ch. 10 | `pub fn greet() { ... }` |
| `static` | Mark a method as a static (type-level) method | Ch. 6 | `static fn new() Counter { ... }` |

---

## 2. Control Flow

| Keyword | Description | Chapter | Example |
|---------|-------------|---------|---------|
| `if` | Conditional branch | Ch. 3 | `if x > 0 { print("positive") }` |
| `else` | Alternate branch for `if` | Ch. 3 | `if ok { ... } else { ... }` |
| `is` | Pattern matching (replaces `match`) | Ch. 7 | `is x { 0 => print("zero"), else => ... }` |
| `else` (in `is`) | Catch-all arm in pattern matching | Ch. 7 | `is val { _ => ... }` |
| `for` | Iteration loop or conditional loop (replaces `while`) | Ch. 3 | `for i < 10 { i = i + 1 }` |
| `for ... in` | Iterate over a collection or range | Ch. 3 | `for item in list { print(item) }` |
| `for ... in ..` | Range iteration | Ch. 3 | `for i in 0..10 { print(i) }` |
| `loop` | Infinite loop | Ch. 3 | `loop { ... }` |
| `break` | Exit a loop early | Ch. 3 | `if done { break }` |
| `continue` | Skip to the next loop iteration | Ch. 3 | `if skip { continue }` |
| `return` | Return a value from a function | Ch. 3 | `return x + 1` |
| `yield` | Produce a value from an iterator or generator | Ch. 19 | `yield item` |

---

## 3. Object-Oriented Programming

| Keyword | Description | Chapter | Example |
|---------|-------------|---------|---------|
| `is` (in type) | Single inheritance | Ch. 8 | `type Hawk is Bird { speed f64 }` |
| `has` | Composition with auto-delegation | Ch. 8 | `type Car has Engine { brand str }` |
| `spec` | Define a behavioral contract (trait) | Ch. 8 | `spec Drawable { fn draw() }` |
| `as` | Implement a spec for a type | Ch. 8 | `ext Circle as Drawable { ... }` |
| `ext` | Define methods on a type (post-hoc extension) | Ch. 6 | `ext Point { fn distance() f64 { ... } }` |
| `mut fn` | Declare a method that mutates the receiver | Ch. 8 | `mut fn increment() void { .count = .count + 1 }` |
| `super` | Access the parent type's fields or methods | Ch. 8 | `super.fly()` |

---

## 4. Error Handling

| Keyword | Description | Chapter | Example |
|---------|-------------|---------|---------|
| `?T` | Optional (nullable) type | Ch. 9 | `fn find(id int) ?User { ... }` |
| `!T` | Error-propagating result type | Ch. 9 | `fn read(path str) !str { ... }` |
| `?` (operator) | Propagate an error or unwrap a value | Ch. 9 | `let data = fs.read("f.txt")?` |
| `!` (on fn) | Mark a function as error-propagating | Ch. 9 | `fn main() ! { ... }` |
| `try` | Begin a try block for exception-style error handling | Ch. 9 | `try { risky_operation() }` |
| `catch` | Catch an error from a `try` block | Ch. 9 | `catch e { print(e) }` |
| `throw` | Raise an error explicitly | Ch. 9 | `throw "something went wrong"` |
| `Some` | Construct an optional value with data | Ch. 9 | `Some(42)` |
| `None` | Represent a missing optional value | Ch. 9 | `None` |
| `Ok` | Construct a successful result | Ch. 9 | `Ok(value)` |
| `Err` | Construct an error result | Ch. 9 | `Err("not found")` |

---

## 5. Concurrency

| Keyword | Description | Chapter | Example |
|---------|-------------|---------|---------|
| `spawn` | Launch a new actor task | Ch. 15 | `let handle = spawn Counter()` |
| `send` | Send a message to an actor | Ch. 15 | `handle.send(Increment)` |
| `receive` | Receive a message in an actor | Ch. 15 | `let msg = receive` |
| `on` | Pattern-match on incoming messages (actor mailbox) | Ch. 7, 15 | `on Increment => .count = .count + 1` |
| `select` | Wait on multiple async operations | Ch. 16 | `select { msg => ..., timeout => ... }` |
| `task` | Define an actor blueprint | Ch. 15 | `task PingPong { ... }` |
| `~T` | Blueprint type (deferred / future) | Ch. 16 | `fn fetch(url str) ~str { ... }` |
| `.await` | Wait for an async blueprint to resolve | Ch. 16 | `let data = fetch(url).await` |

---

## 6. Memory & Ownership

| Keyword | Description | Chapter | Example |
|---------|-------------|---------|---------|
| `view T` | Borrow a value as read-only | Ch. 11 | `fn print_name(v view User) { ... }` |
| `mut T` | Borrow a value as mutable | Ch. 11 | `fn reset(m mut Counter) { m.count = 0 }` |
| `*T` | Raw pointer type (unsafe, `sys` required) | Ch. 11 | `let ptr *int = sys addr_of(x)` |
| `move` | Explicitly transfer ownership | Ch. 12 | `consume(move data)` |
| `clone` | Create a deep copy of a value | Ch. 12 | `let copy = data.clone()` |
| `free` | Manually deallocate a value | Ch. 12 | `free(buf)` |
| `sys` | Enter an unsafe context (low-level access) | Ch. 11 | `sys { let p = *addr }` |

---

## 7. Generics

| Keyword | Description | Chapter | Example |
|---------|-------------|---------|---------|
| `<T>` | Generic type parameter | Ch. 13 | `fn identity(x T) T { x }` |
| `<T, U>` | Multiple generic parameters | Ch. 13 | `type Pair<T, U> { first T, second U }` |
| `where` | Constraint clause for generic bounds | Ch. 13 | `fn compare<T>(a T, b T) int where T: Ord { ... }` |
| `impl` | Satisfy a spec bound in a where clause | Ch. 13 | `where T: impl Drawable` |
| `List<T>` | Generic dynamic array | Ch. 4, 13 | `let list List<int> = List.new()` |
| `Map<K, V>` | Generic hash map | Ch. 4, 13 | `let m Map<str, int> = {}` |
| `Result<T, E>` | Generic result type | Ch. 9, 13 | `fn divide(a int, b int) Result<int, str> { ... }` |

---

## 8. Attributes & Metaprogramming

| Attribute | Description | Chapter | Example |
|-----------|-------------|---------|---------|
| `#[test]` | Mark a function as a test | Ch. 18 | `#[test] fn test_add() { ... }` |
| `#[comptime]` | Evaluate a function or block at compile time | Ch. 20 | `#[comptime] fn name() str { "hello" }` |
| `#[cfg(...)]` | Conditional compilation based on target or feature | Ch. 20 | `#[cfg(target_os = "linux")] fn linux_only() { ... }` |
| `#[macro]` | Define a comptime macro | Ch. 20 | `#[macro] fn assert_eq(a, b) { ... }` |
| `#[inline]` | Hint the compiler to inline a function | Ch. 20 | `#[inline] fn small_fn() int { 42 }` |
| `#[derive(...)]` | Auto-generate common trait implementations | Ch. 20 | `#[derive(Debug, Clone)] type Point { x f64, y f64 }` |

---

## 9. Literals & Built-in Types

| Keyword / Literal | Description | Chapter | Example |
|--------------------|-------------|---------|---------|
| `true` | Boolean true | Ch. 2 | `let active = true` |
| `false` | Boolean false | Ch. 2 | `let done = false` |
| `nil` | Null / absent value | Ch. 9 | `let x ?int = nil` |
| `str` | String type | Ch. 2 | `let name str = "Auto"` |
| `int` | Default integer type (32-bit) | Ch. 2 | `let x int = 42` |
| `f64` | 64-bit floating-point type | Ch. 2 | `let pi f64 = 3.14` |
| `bool` | Boolean type | Ch. 2 | `let flag bool = true` |
| `char` | Unicode character type | Ch. 7 | `let c char = 'A'` |
| `void` | Unit type (no meaningful value) | Ch. 3 | `fn greet() void { print("hi") }` |
| `List<T>` | Dynamic array type | Ch. 4 | `var items = List.new()` |
| `Map<K, V>` | Hash map type | Ch. 4 | `var m Map<str, int> = {}` |
| `Set<T>` | Hash set type | Ch. 4 | `var s Set<int> = Set.new()` |

---

## 10. Other

| Keyword | Description | Chapter | Example |
|---------|-------------|---------|---------|
| `self` | Access the current instance (via `.` prefix, not a parameter) | Ch. 6 | `.name` (equivalent to `self.name` in other languages) |
| `super` | Reference the parent type in inheritance | Ch. 8 | `super.fly()` |
| `print` | Print a value to stdout | Ch. 1 | `print("Hello, Auto!")` |
| `automan` | Auto's package manager and build tool | Ch. 1 | `$ automan new my_project` |
| `.` (field access) | Access a field or call a method on a value | Ch. 6 | `point.x` / `list.len()` |
| `..` (range) | Create a half-open range | Ch. 3 | `for i in 0..10 { ... }` |
| `$var` | String interpolation (variable) | Ch. 2 | `print("Hello, $name")` |
| `${expr}` | String interpolation (expression) | Ch. 2 | `print("result: ${a + b}")` |
| `_` | Wildcard pattern (ignore a value) | Ch. 7 | `is x { _ => print("anything") }` |

---

## Quick Cross-Reference: Keyword to Chapter

| Chapter | Title | Key Keywords Introduced |
|---------|-------|------------------------|
| 1 | Getting Started | `fn`, `print`, `automan` |
| 2 | Variables & Operators | `let`, `var`, `const`, `true`, `false`, `str`, `int`, `f64`, `bool`, `$var` |
| 3 | Functions & Control Flow | `if`, `else`, `for`, `loop`, `break`, `continue`, `return`, `void`, `..` |
| 4 | Collections & Nodes | `List<T>`, `Map<K, V>`, `Set<T>` |
| 6 | Types & `let` | `type`, `ext`, `static`, `self` (implicit), tuples |
| 7 | Enums & Pattern Matching | `enum`, `is`, `on`, `char`, `_` |
| 8 | OOP Reshaped | `is` (inheritance), `has`, `spec`, `as`, `mut fn`, `super` |
| 9 | Error Handling | `?T`, `!T`, `?`, `try`, `catch`, `throw`, `Some`, `None`, `Ok`, `Err` |
| 10 | Packages & Modules | `mod`, `use`, `use.rust`, `import`, `pub` |
| 11 | References & Pointers | `view`, `mut`, `*T`, `sys`, lifetimes |
| 12 | Memory & Ownership | `move`, `clone`, `free`, ownership rules |
| 13 | Generics | `<T>`, `where`, `impl` (bounds), generic types |
| 15 | Actor Concurrency | `spawn`, `send`, `receive`, `on`, `task`, `select` |
| 16 | Async with `~T` | `~T`, `.await`, async functions |
| 17 | Smart Casts & Flow Typing | `if x is T`, union types, flow-sensitive narrowing |
| 18 | Testing | `#[test]`, `assert_eq`, `assert` |
| 19 | Closures & Iterators | `yield`, closures, `.iter()`, `.map()`, `.filter()`, `.fold()` |
| 20 | Comptime & Metaprogramming | `#[comptime]`, `#[cfg(...)]`, `#[macro]`, `#[inline]`, `#[derive(...)]` |
