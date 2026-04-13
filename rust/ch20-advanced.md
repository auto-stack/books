# Advanced Features

By now, you've learned the most commonly used parts of the Auto programming
language. Before we do one more project in Chapter 21, we'll look at a few
aspects of the language you might run into every once in a while but may not
use every day. You can use this chapter as a reference for when you encounter
any unknowns. The features covered here are useful in very specific situations.
Although you might not reach for them often, we want to make sure you have a
grasp of all the features Auto has to offer.

In this chapter, we'll cover:

- **`sys` blocks**: Auto's equivalent of unsafe Rust, for when you need to step
  outside the language's safety guarantees
- **Advanced types**: Type aliases, the never type, and dynamically sized types
- **Comptime metaprogramming**: Auto's compile-time code generation with `#[]`,
  replacing Rust's macro system

## `sys` Blocks

All the code we've discussed so far has had Auto's memory safety guarantees
enforced at compile time through AutoFree. However, Auto has a second language
hidden inside it that doesn't enforce these memory safety guarantees: it's
called _sys mode_ and works just like regular Auto but gives you extra
capabilities. It uses the `sys` keyword instead of Rust's `unsafe`.

Sys mode exists because, by nature, static analysis is conservative. When the
compiler tries to determine whether or not code upholds the guarantees, it's
better for it to reject some valid programs than to accept some invalid
programs. In these cases, you can use `sys` code to tell the compiler, "Trust
me, I know what I'm doing."

Another reason Auto has a sys mode is that the underlying computer hardware is
inherently unsafe. If Auto didn't let you do unsafe operations, you couldn't do
certain tasks. Auto needs to allow you to do low-level systems programming, such
as directly interacting with the operating system or even writing your own
operating system.

### Sys Superpowers

To switch to sys mode, use the `sys` keyword and then start a new block that
holds the system-level code. You can take several actions in sys mode that you
can't in safe Auto, which we call _sys superpowers_. Those superpowers include
the ability to:

1. Dereference a raw pointer (`*T`)
2. Call a `sys` function or method
3. Access or modify a mutable static variable
4. Implement a `sys` spec
5. Access fields of unions
6. Call C functions through FFI

It's important to understand that `sys` doesn't turn off AutoFree or disable
any of Auto's other safety checks. The `sys` keyword only gives you access to
these features that are then not checked by the compiler for memory safety.

In addition, `sys` does not mean the code inside the block is necessarily
dangerous. The intent is that as the programmer, you'll ensure that the code
inside a `sys` block will access memory in a valid way.

To isolate sys code as much as possible, it's best to enclose such code within
a safe abstraction and provide a safe API.

### Dereferencing Raw Pointers

Sys mode has two raw pointer types similar to references: `*T` (immutable raw
pointer) and `*mut T` (mutable raw pointer). These correspond to Rust's
`*const T` and `*mut T`.

<Listing number="20-1" file-name="src/main.at" caption="Creating and dereferencing raw pointers">

```auto
fn main() {
    var num = 5

    let r1 = &raw num        // *int (immutable raw pointer)
    let r2 = &raw mut num    // *mut int (mutable raw pointer)

    sys {
        print(f"r1 is: {*r1}")
        print(f"r2 is: {*r2}")
    }
}
```

```rust
fn main() {
    let mut num = 5;

    let r1 = &raw const num;
    let r2 = &raw mut num;

    unsafe {
        println!("r1 is: {}", *r1);
        println!("r2 is: {}", *r2);
    }
}
```

</Listing>

Notice that we can create raw pointers in safe code; we just can't dereference
raw pointers outside a `sys` block. Creating a pointer does no harm; it's only
when we try to access the value that it points at that we might end up dealing
with an invalid value.

Unlike regular references, raw pointers:

- Are allowed to ignore borrowing rules by having both immutable and mutable
  pointers to the same location
- Aren't guaranteed to point to valid memory
- Are allowed to be null
- Don't implement any automatic cleanup

### Calling Sys Functions

The second type of operation you can perform in a `sys` block is calling sys
functions. Sys functions have an extra `sys` before the rest of the definition:

<Listing number="20-2" file-name="src/main.at" caption="Calling a sys function">

```auto
sys fn dangerous() {}

fn main() {
    sys {
        dangerous()
    }
}
```

```rust
unsafe fn dangerous() {}

fn main() {
    unsafe {
        dangerous();
    }
}
```

</Listing>

We must call the `dangerous` function within a `sys` block. If we try to call
it without the `sys` block, we'll get an error.

#### Creating a Safe Abstraction over Sys Code

Just because a function contains sys code doesn't mean we need to mark the
entire function as `sys`. In fact, wrapping sys code in a safe function is a
common abstraction. As an example, let's implement `split_at_mut`:

<Listing number="20-3" file-name="src/main.at" caption="A safe abstraction using sys internally">

```auto
fn split_at_mut(values &mut [int], mid int) (&mut [int], &mut [int]) {
    let len = values.len()
    assert(mid <= len)

    let ptr = values.as_mut_ptr()

    sys {
        (
            slice.from_raw_parts_mut(ptr, mid),
            slice.from_raw_parts_mut(ptr.add(mid), len - mid),
        )
    }
}

fn main() {
    var v = [1, 2, 3, 4, 5, 6]
    let (a, b) = split_at_mut(&mut v, 3)
    assert_eq(a, &mut [1, 2, 3])
    assert_eq(b, &mut [4, 5, 6])
}
```

```rust
use std::slice;

fn split_at_mut(values: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    let len = values.len();
    let ptr = values.as_mut_ptr();

    assert!(mid <= len);

    unsafe {
        (
            slice::from_raw_parts_mut(ptr, mid),
            slice::from_raw_parts_mut(ptr.add(mid), len - mid),
        )
    }
}

fn main() {
    let mut vector = vec![1, 2, 3, 4, 5, 6];
    let (left, right) = split_at_mut(&mut vector, 3);
    assert_eq!(left, &mut [1, 2, 3]);
    assert_eq!(right, &mut [4, 5, 6]);
}
```

</Listing>

Note that we don't need to mark `split_at_mut` as `sys`, and we can call this
function from safe Auto. We've created a safe abstraction to the sys code with
an implementation that uses `sys` code in a safe way.

### Foreign Function Interface (FFI)

Sometimes your Auto code might need to interact with code written in another
language. Since Auto transpiles to C, it has natural FFI support:

<Listing number="20-4" file-name="src/main.at" caption="Declaring and calling an extern C function">

```auto
sys extern "C" {
    fn abs(input int) int
}

fn main() {
    sys {
        print(f"Absolute value of -3 according to C: {abs(-3)}")
    }
}
```

```rust
unsafe extern "C" {
    fn abs(input: i32) -> i32;
}

fn main() {
    unsafe {
        println!("Absolute value of -3 according to C: {}", abs(-3));
    }
}
```

</Listing>

Within the `sys extern "C"` block, we list the names and signatures of external
functions from C. The `"C"` part defines the application binary interface (ABI)
the external function uses.

Because Auto transpiles to C, FFI with C libraries is straightforward. No
additional bridge code or wrapper generation is needed for calling C functions.

### Accessing or Modifying Mutable Static Variables

Global variables in Auto are called _static_ variables. Accessing and modifying
mutable static variables requires `sys`:

<Listing number="20-5" file-name="src/main.at" caption="Reading from or writing to a mutable static variable">

```auto
static mut COUNTER int = 0

/// SAFETY: Calling this from more than a single thread at a time is
/// undefined behavior.
sys fn add_to_count(inc int) {
    sys {
        COUNTER += inc
    }
}

fn main() {
    sys {
        add_to_count(3)
        print(f"COUNTER: {COUNTER}")
    }
}
```

```rust
static mut COUNTER: u32 = 0;

/// SAFETY: Calling this from more than a single thread at a time is
/// undefined behavior.
unsafe fn add_to_count(inc: u32) {
    unsafe {
        COUNTER += inc;
    }
}

fn main() {
    unsafe {
        add_to_count(3);
        println!("COUNTER: {}", *(&raw const COUNTER));
    }
}
```

</Listing>

With mutable data that is globally accessible, it's difficult to ensure that
there are no data races, which is why Auto considers mutable static variables
to require `sys`. Where possible, it's preferable to use the concurrency
techniques we discussed in Chapter 16 (Actors) so that the compiler checks that
data access is done safely.

### Implementing a Sys Spec

We can use `sys` to implement a sys spec. A spec is sys when at least one of
its methods has some invariant that the compiler can't verify:

<Listing number="20-6" file-name="src/main.at" caption="Defining and implementing a sys spec">

```auto
sys spec Foo {
    // methods go here
}

sys spec Foo for int {
    // method implementations go here
}

fn main() {}
```

```rust
unsafe trait Foo {
    // methods go here
}

unsafe impl Foo for i32 {
    // method implementations go here
}

fn main() {}
```

</Listing>

By using `sys spec ... for Type`, we're promising that we'll uphold the
invariants that the compiler can't verify.

### `sys` vs `unsafe` Quick Reference

| Feature | Auto (`sys`) | Rust (`unsafe`) |
|---------|-------------|-----------------|
| Keyword | `sys` | `unsafe` |
| Raw pointer types | `*T`, `*mut T` | `*const T`, `*mut T` |
| Sys/unsafe function | `sys fn` | `unsafe fn` |
| Sys/unsafe trait | `sys spec` | `unsafe trait` |
| FFI block | `sys extern "C"` | `unsafe extern "C"` |
| Static variables | `static mut` in `sys` | `static mut` in `unsafe` |
| Safe abstraction | Encouraged | Encouraged |
| Transpiles to | C code | Native code |

## Advanced Types

### Type Aliases

Auto provides the ability to declare a _type alias_ to give an existing type
another name, just like Rust. For example, we can create the alias `Kilometers`
to `int`:

<Listing number="20-7" file-name="src/main.at" caption="Creating a type alias">

```auto
type Kilometers = int

fn main() {
    let x int = 5
    let y Kilometers = 5

    print(f"x + y = {x + y}")
}
```

```rust
type Kilometers = i32;

fn main() {
    let x: i32 = 5;
    let y: Kilometers = 5;

    println!("x + y = {}", x + y);
}
```

</Listing>

The alias `Kilometers` is a synonym for `int`; unlike a newtype pattern,
`Kilometers` is not a separate, new type. Values of type `Kilometers` will be
treated the same as values of type `int`.

The main use case for type aliases is reducing repetition. For example, a
lengthy type like `Box<dyn Fn() + Send>` can be aliased:

```auto
type Thunk = Box<dyn Fn() + Send>

fn takes_long_type(f Thunk) {
    // ...
}

fn returns_long_type() Thunk {
    // ...
}
```

### The Never Type

Auto has a special type named `!` that's known as the _never type_ because it
stands in the place of the return type when a function will never return. This
is the same concept as Rust's never type:

```auto
fn bar() ! {
    panic("something went wrong")
}
```

```rust
fn bar() -> ! {
    panic!("something went wrong");
}
```

Note that Auto uses `!` both as the error type in `!T` (the equivalent of
`Result<T, E>`) and as the never type. The compiler distinguishes between them
based on context: `!T` is an error-propagating result type, while standalone `!`
as a return type means the function never returns.

The never type is useful with `panic()`, `return`, `break`, and `continue` —
all of these produce values of type `!` that can be coerced into any other type.

### Dynamically Sized Types

Auto has _dynamically sized types_ (DSTs), similar to Rust. The most common DST
is `str` (not `String`). We can't create a variable of type `str` directly
because the compiler doesn't know how much space to allocate. Instead, we
always use DSTs behind a pointer: `&str`, `Box<str>`, etc.

Spec objects (`dyn Spec`) are also DSTs, which is why they must be behind a
pointer like `Box<dyn Draw>` or `&dyn Draw`.

## Comptime Metaprogramming

Rust uses macros (`macro_rules!` and procedural macros) for metaprogramming —
writing code that writes code. Auto replaces this entire system with
_comptime_: code that runs at compile time. This is inspired by Zig's comptime
and is more powerful and easier to understand than Rust's macro system.

### Why Comptime Instead of Macros?

Macros in Rust have several downsides:

- `macro_rules!` uses a complex pattern-matching syntax that's different from
  normal Rust code
- Procedural macros require separate crates and dependencies like `syn` and
  `quote`
- Macro errors are often hard to read
- Macros can't easily introspect types

Auto's comptime system solves these problems:

- Comptime code uses regular Auto syntax — no special macro language
- No separate crates needed
- Error messages are clear because they come from normal Auto code
- Full type introspection at compile time

### The `#[]` Attribute System

Auto uses `#[]` attributes for compile-time code generation. These serve the
same role as Rust's `#[derive]`, `#[proc_macro]`, and other attributes:

<Listing number="20-8" file-name="src/main.at" caption="Using built-in derive attributes">

```auto
#derive[Debug, Eq]
type Point {
    x int
    y int
}

fn main() {
    let p = Point(x: 1, y: 2)
    print(f"{p:?}")  // Uses Debug impl
}
```

```rust
#[derive(Debug, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 1, y: 2 };
    println!("{:?}", p);
}
```

</Listing>

The `#derive[...]` attribute automatically generates spec implementations for
your types. This is the equivalent of Rust's `#[derive(...)]`.

### Writing Custom Comptime Functions

Auto lets you write comptime functions — regular Auto functions that execute
at compile time and generate code. This replaces both declarative and
procedural macros:

<Listing number="20-9" file-name="src/main.at" caption="A comptime function generating code">

```auto
comptime fn generate_hello(type_name String) String {
    f"""
ext {type_name} {{
    fn hello() {{
        print("Hello from {type_name}!")
    }}
}}
"""
}

// Apply the comptime function to generate code
#apply[generate_hello]
type Greeter {}

fn main() {
    Greeter.hello()  // Generated by comptime
}
```

```rust
use proc_macro::TokenStream;
use quote::quote;

#[proc_macro_derive(Hello)]
pub fn hello_derive(input: TokenStream) -> TokenStream {
    let ast = syn::parse(input).unwrap();
    let name = &ast.ident;
    let generated = quote! {
        impl Hello for #name {
            fn hello() {
                println!("Hello from {}!", stringify!(#name));
            }
        }
    };
    generated.into()
}

// In another crate:
// #[derive(Hello)]
// struct Greeter;
```

</Listing>

In Rust, procedural macros require a separate crate, the `syn` and `quote`
crates, and complex token manipulation. In Auto, a comptime function is just a
regular function marked with `comptime` that returns a string of code or
directly manipulates the AST.

### Comptime vs Rust Macros

<Listing number="20-10" file-name="src/main.at" caption="Comptime list creation vs vec! macro">

```auto
// Auto doesn't need a vec! macro — List literals work directly
fn main() {
    let v = [1, 2, 3]  // List<int>
    print(f"{v}")
}
```

```rust
fn main() {
    let v = vec![1, 2, 3];  // Uses the vec! macro
    println!("{:?}", v);
}
```

</Listing>

Many patterns that require macros in Rust don't need comptime in Auto:

| Rust Pattern | Requires Macro? | Auto Equivalent |
|-------------|----------------|-----------------|
| Vector literals | Yes (`vec![]`) | No (`[1, 2, 3]`) |
| Print with formatting | Yes (`println!`) | No (`print(f"{}")`) |
| Derive traits | Yes (`#[derive]`) | Yes (`#derive[]`) |
| Custom code generation | Yes (proc macro) | Yes (comptime) |
| Conditional compilation | Yes (`cfg!`) | Yes (`#if[]`) |

### Attribute-Like Comptime

Auto supports custom attributes that transform code at compile time:

<Listing number="20-11" file-name="src/main.at" caption="Custom attribute-like comptime">

```auto
// Define a custom attribute for route handlers
#attr[route]
comptime fn route_handler(attr String, item String) String {
    // Parse the route from attr, wrap the function
    // with routing registration code
    f"""
// Register route: {attr}
{item}
routes.register("{attr}", handler)
"""
}

// Use the attribute
#route[GET, "/"]
fn index() {
    "Hello, World!"
}
```

```rust
use proc_macro::TokenStream;

#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
    // Parse attr and item, generate routing code
    // Requires syn and quote crates
    item
}
```

</Listing>

### Conditional Compilation

Auto provides compile-time conditional compilation using `#if[]`:

<Listing number="20-12" file-name="src/main.at" caption="Conditional compilation">

```auto
#if[debug]
fn log(msg String) {
    print(f"[DEBUG] {msg}")
}

#if[release]
fn log(msg String) {
    // No-op in release builds
}

fn main() {
    log("Starting application")
}
```

```rust
#[cfg(debug_assertions)]
fn log(msg: &str) {
    println!("[DEBUG] {msg}");
}

#[cfg(not(debug_assertions))]
fn log(msg: &str) {
    // No-op in release builds
}

fn main() {
    log("Starting application");
}
```

</Listing>

### Inline Comptime Expressions

Auto allows inline comptime expressions — code that runs at compile time and
produces a value:

<Listing number="20-13" file-name="src/main.at" caption="Inline comptime expressions">

```auto
fn main() {
    // Compute a constant at compile time
    const MAX_SIZE = comptime {
        let base = 1024
        let scale = 4
        base * scale
    }

    // Generate a type at compile time
    comptime {
        for field in config.fields {
            print(f"Field: {field.name}")
        }
    }

    print(f"Max size: {MAX_SIZE}")
}
```

```rust
const MAX_SIZE: usize = 1024 * 4;

fn main() {
    println!("Max size: {MAX_SIZE}");
}
```

</Listing>

### Comptime vs Rust Macros Quick Reference

| Feature | Rust | Auto |
|---------|------|------|
| Declarative macros | `macro_rules!` | Not needed (use comptime) |
| Procedural macros | Separate crate + `syn`/`quote` | `comptime fn` |
| Derive macros | `#[derive(Trait)]` | `#derive[Trait]` |
| Attribute macros | `#[proc_macro_attribute]` | `#attr[...]` + `comptime fn` |
| Function-like macros | `#[proc_macro]` | `comptime fn` |
| Conditional compilation | `#[cfg(...)]` | `#if[...]` |
| Type introspection | Not available | Full comptime reflection |
| Separate crate required | Yes (proc macros) | No |
| Syntax | Special macro syntax | Regular Auto syntax |

## `sys` and Comptime Guidelines

### When to Use `sys`

Use `sys` blocks when you need to:

- Interface with C libraries through FFI
- Implement low-level data structures (like `List<T>` internals)
- Do pointer arithmetic
- Access hardware directly

Always wrap `sys` code in safe abstractions. Keep `sys` blocks as small as
possible. Document safety invariants with `/// SAFETY:` comments.

### When to Use Comptime

Use comptime when you need to:

- Generate repetitive code (like spec implementations)
- Implement domain-specific languages within Auto
- Perform compile-time validation
- Reduce boilerplate

Prefer regular functions and generics over comptime when possible. Comptime
adds complexity; use it only when the alternatives are worse.

## Summary

This chapter covered Auto's advanced features:

1. **`sys` blocks** — Auto's equivalent of `unsafe`, for stepping outside
   safety guarantees when necessary. Uses `sys` keyword instead of `unsafe`,
   `*T`/`*mut T` instead of `*const T`/`*mut T`, and `sys spec` instead of
   `unsafe trait`.

2. **Advanced types** — Type aliases for reducing repetition, the never type
   `!` for functions that don't return, and dynamically sized types that must
   be used behind pointers.

3. **Comptime metaprogramming** — Auto's replacement for Rust's macro system.
   Uses `#[]` attributes and `comptime fn` instead of `macro_rules!` and
   procedural macros. No separate crates needed, regular Auto syntax throughout.

The key difference from Rust is that Auto replaces the complex macro ecosystem
with a unified comptime system. Where Rust has three kinds of macros each with
their own syntax and crate requirements, Auto has a single `comptime` mechanism
that uses familiar function syntax. And where Rust uses `unsafe`, Auto uses
`sys` — a simpler keyword for the same concept of opting out of safety
guarantees.

In the next chapter, we'll put everything we've discussed throughout the book
into practice and build a final project: a web server using Auto's Actor model.
