# Chapter 17: Function-like Macros

> Level 3 -- Experience
>
> Text substitution, preprocessor tricks, and why Auto replaces macros with
> compile-time metaprogramming.

Function-like macros are one of C's most powerful and most dangerous features.
They enable metaprogramming through text substitution before the compiler sees
the code. Auto takes a fundamentally different approach: it provides
compile-time code generation through the `#[]` comptime system, which is
type-safe and predictable.

---

## 17.1 How Macros Work

Macros are processed by the C preprocessor before compilation. The preprocessor
performs text substitution:

```c
// C Deep Dive: macro basics
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define SQUARE(x)  ((x) * (x))
#define PI 3.14159265

int result = MAX(3, 7);        // expands to: ((3) > (7) ? (3) : (7))
int area = SQUARE(5);          // expands to: ((5) * (5))
double circ = 2 * PI * r;     // expands to: 2 * 3.14159265 * r
```

The preprocessor is a separate phase of translation. It knows nothing about
C types, scoping rules, or syntax. It performs literal text replacement.

Macro expansion happens in several steps:

1. Scan the token sequence for macro invocations.
2. Substitute arguments (with `#` and `##` processing).
3. Rescan the result for further macros.
4. Repeat until no more substitutions are possible.

> **C Deep Dive:** The rescanning step can cause infinite recursion. The C
> standard prevents this by not re-expanding a macro during its own expansion.
> But mutual recursion between macros is allowed and is sometimes used
> intentionally in advanced macro programming.

**Auto's approach.** Auto has no preprocessor and no macros. Every operation
that would use a macro in C uses a regular function or comptime metaprogramming:

```auto
// Auto: regular functions replace macros
fn safe_max(a int, b int) int {
    if a > b { a } else { b }
}

fn safe_square(n int) int {
    n * n
}
```

---

## 17.2 Argument Checking

Macros do not check argument types. The substitution is purely textual, which
leads to subtle bugs:

```c
// C Deep Dive: macro pitfalls
#define SQUARE(x) ((x) * (x))

int a = SQUARE(2 + 3);
// Expands to: ((2 + 3) * (2 + 3)) = 25 (correct with parentheses)

// But what about this?
#define BAD_SQUARE(x) x * x
int b = BAD_SQUARE(2 + 3);
// Expands to: 2 + 3 * 2 + 3 = 2 + 6 + 3 = 11 (wrong!)
```

The most dangerous pitfall is double evaluation:

```c
// C Deep Dive: double evaluation
#define MAX(a, b) ((a) > (b) ? (a) : (b))

int x = 5;
int y = MAX(x++, 3);
// Expands to: ((x++) > (3) ? (x++) : (3))
// x is incremented TWICE if x > 3! x becomes 7, not 6.
```

Common macro problems:

| Problem              | Example                     | Consequence              |
|----------------------|-----------------------------|--------------------------|
| Missing parentheses  | `x * x` with `2 + 3`       | Wrong precedence         |
| Double evaluation    | `MAX(x++, y)`               | Side effect runs twice   |
| No type checking     | `MAX("hello", 3)`          | Compiles, crashes        |
| No debugging         | Step into macro             | Not visible in debugger  |
| Scope issues         | Macro uses local variable   | Name collisions          |

> **C Deep Dive:** The rule for safe macros: always parenthesize every parameter
> and the entire expression. `#define SQUARE(x) ((x) * (x))`. Even then,
> double evaluation is impossible to prevent. The only truly safe macro is
> one whose arguments are simple identifiers or constants.

**Auto's approach.** Auto functions have none of these problems:

```auto
// Auto: no macro pitfalls
fn safe_max(a int, b int) int {
    if a > b { a } else { b }
}

fn main() {
    // Arguments evaluated exactly once
    var x int = 5
    let y int = safe_max(x, 3)   // x evaluated once
    print("x:", x)               // x is still 5
    print("y:", y)               // y is 5
}
```

<Listing path="listings/ch17/listing-17-01" title="Macros to Auto functions" />

---

## 17.3 Context of Invocation

Macros can access context information through predefined identifiers:

```c
// C Deep Dive: predefined macros
#define LOG(msg) printf("%s:%d: %s\n", __FILE__, __LINE__, msg)

void process(void) {
    LOG("starting process");    // prints "main.c:5: starting process"
    LOG("done");                // prints "main.c:6: done"
}
```

Standard predefined macros:

| Macro         | Value                           |
|---------------|---------------------------------|
| `__FILE__`    | Source file name (string literal)|
| `__LINE__`    | Current line number (integer)   |
| `__DATE__`    | Compilation date (string)       |
| `__TIME__`    | Compilation time (string)       |
| `__func__`    | Current function name (C99)     |
| `__STDC__`    | 1 if compiler conforms to C     |

These are useful for debugging, logging, and assertions:

```c
// C Deep Dive: assert using context
#define ASSERT(expr) do { \
    if (!(expr)) { \
        fprintf(stderr, "%s:%d: assertion failed: %s\n", \
                __FILE__, __LINE__, #expr); \
        abort(); \
    } \
} while (0)
```

> **C Deep Dive:** The `do { ... } while (0)` idiom wraps the macro body so
> it behaves like a single statement. Without it, `if (cond) ASSERT(x); else ...`
> would break because the `else` would attach to the `if` inside the macro.

**Auto's approach.** Auto's comptime `#[]` system provides similar capabilities:

```auto
// Auto: comptime context
fn process() {
    // comptime #[] provides compile-time information
    // #[file] -> current file name
    // #[line] -> current line number
    // #[fn]   -> current function name
    print("Processing...")    // Auto's print includes source info in debug
}
```

---

## 17.4 Variable-length Argument Lists

Macros support variadic arguments through `__VA_ARGS__`:

```c
// C Deep Dive: variadic macros
#define LOG(fmt, ...) printf("[LOG] " fmt "\n", __VA_ARGS__)

LOG("value: %d", 42);         // [LOG] value: 42
LOG("x=%d y=%d", x, y);      // [LOG] x=3 y=7
```

C23 adds `__VA_OPT__` to handle the comma when `__VA_ARGS__` is empty:

```c
// C Deep Dive: __VA_OPT__
#define LOG(fmt, ...) printf(fmt __VA_OPT__(,) __VA_ARGS__)
LOG("hello");                 // printf("hello") -- no trailing comma
LOG("x=%d", 42);             // printf("x=%d", 42)
```

> **C Deep Dive:** Before `__VA_OPT__`, the empty-argument problem was a
> significant pain point. GCC introduced `##__VA_ARGS__` as an extension to
> eat the preceding comma. C23 standardized the solution with `__VA_OPT__`,
> but many codebases still use the GCC extension.

**Auto's approach.** Auto has variadic functions built into the language:

```auto
// Auto: variadic functions
fn print_all(items ...str) {
    for item in items {
        print(item)
    }
}

fn main() {
    print_all("hello", "world")
    print_all("one", "two", "three")
}
```

Auto's variadic functions are type-safe. Each argument must match the declared
parameter type (or be convertible to it).

---

## 17.5 Default Arguments

C macros can simulate default arguments through clever tricks:

```c
// C Deep Dive: simulated default arguments
#define GREET_IMPL(name, greeting) printf("%s, %s!\n", greeting, name)
#define GET_GREET(a, b, FUNC, ...) FUNC
#define GREET(...) GET_GREET(__VA_ARGS__, GREET_IMPL,)(\
    __VA_ARGS__)
```

This is unreadable, fragile, and relies on preprocessor quirks. Yet it appears
in production code because C has no native default arguments.

> **C Deep Dive:** The simulated default argument trick works by exploiting
> the fact that `__VA_ARGS__` maps to the Nth argument. When fewer arguments
> are provided, the default function name appears in the correct position.
> This technique is used by major libraries including the Linux kernel's
> `dev_dbg` macro family.

**Auto's approach.** Auto may support default parameters in the future:

```auto
// Auto: default parameters (planned)
fn greet(name str, greeting str = "Hello") {
    print(greeting + ", " + name + "!")
}

fn main() {
    greet("World")             // Hello, World!
    greet("World", "Hi")      // Hi, World!
}
```

Until default parameters are implemented, the idiomatic approach is to define
wrapper functions:

```auto
// Auto: wrapper function for defaults
fn greet(name str) {
    greet_with(name, "Hello")
}

fn greet_with(name str, greeting str) {
    print(greeting + ", " + name + "!")
}

fn main() {
    greet("World")             // Hello, World!
    greet_with("World", "Hi")  // Hi, World!
}
```

> **Key message:** Auto's comptime `#[]` replaces the entire C preprocessor
> with a type-safe, predictable compile-time metaprogramming system. No text
> substitution, no double evaluation, no parentheses games.

---

## Quick Reference

| Concept              | C mechanism                  | Auto mechanism             |
|----------------------|------------------------------|----------------------------|
| Text substitution    | `#define` preprocessor       | Regular functions          |
| Type safety          | None (textual)               | Full type checking         |
| Double evaluation    | Common pitfall               | Impossible                 |
| Debugging            | Not visible in debugger      | Normal function debugging  |
| Context info         | `__FILE__`, `__LINE__`       | Comptime `#[]` system      |
| Variadic arguments   | `__VA_ARGS__`                | Variadic functions         |
| Default arguments    | Macro tricks                 | Default parameters (planned)|
| Stringification      | `#` operator                 | Comptime operations        |
| Token pasting        | `##` operator                | Comptime code generation   |

---

*Macros are C's original metaprogramming system. They work at the text level,
before the compiler sees the code. Auto moves metaprogramming into the
language itself, where it can be type-checked, debugged, and understood.*
