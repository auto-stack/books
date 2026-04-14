# Chapter 18: Type-generic Programming

> Level 3 -- Experience
>
> _Generic, type inference, and anonymous functions -- writing code that works
> across types in C, and how Auto's generics system makes it natural.

C was designed as a typed language: every object has a type, and operations
are defined for specific types. But real programs need to operate on data
regardless of its exact type. C has evolved mechanisms for type-generic
programming -- `_Generic`, `auto`, `typeof` -- and Auto takes these ideas
further with a full generics system.

---

## 18.1 Inherent Type-generic Features

C has always had implicit type-generic features through conversions and
promotions:

```c
// C Deep Dive: implicit conversions
short s = 42;
int i = s;          // short promotes to int (integer promotion)
long l = i;         // int converts to long (usual conversion)
double d = l;       // long converts to double (usual conversion)

int a = 3;
double b = 4.2;
double c = a + b;   // a is converted to double before addition
```

The usual arithmetic conversion rules determine the common type for binary
operations:

1. Integer promotions are performed on both operands.
2. If the types differ, the "narrower" type is converted to the "wider" type.
3. If both are integer types, the signedness is resolved according to complex
   rules in the standard.

> **C Deep Dive:** The integer promotion rules in C are a frequent source of
> surprises. On most platforms, `short` values are promoted to `int` before
> any arithmetic operation. This means `short a, b; auto c = a + b;` produces
> an `int`, not a `short`. The rules also interact with signedness in
> non-obvious ways: `unsigned int` vs `long` depends on platform sizes.

These conversions are automatic but not always safe:

```c
// C Deep Dive: conversion pitfalls
int big = 2147483647;    // INT_MAX on 32-bit int
float f = big;            // may lose precision (float has 23-bit mantissa)
int back = f;             // implementation-defined if f > INT_MAX

unsigned int u = -1;     // well-defined: UINT_MAX via modular conversion
int signed_val = u;       // implementation-defined if u > INT_MAX
```

**Auto's approach.** Auto requires explicit conversions between types. No
implicit narrowing conversions:

```auto
// Auto: explicit conversions
fn main() {
    let i int = 42
    let d float = float(i)     // explicit conversion
    let s int = int(d)         // explicit conversion
    print("i:", i)
    print("d:", d)
    print("s:", s)
}
```

---

## 18.2 Generic Selection

C11 introduced `_Generic` for compile-time type dispatch:

```c
// C Deep Dive: _Generic
#include <stdio.h>

#define print_val(x) _Generic((x), \
    int: print_int,                \
    double: print_double,          \
    char*: print_string            \
)(x)

void print_int(int x) { printf("%d\n", x); }
void print_double(double x) { printf("%f\n", x); }
void print_string(char *x) { printf("%s\n", x); }

int main(void) {
    print_val(42);            // calls print_int
    print_val(3.14);          // calls print_double
    print_val("hello");       // calls print_string
    return 0;
}
```

`_Generic` is a compile-time construct. The compiler selects the matching
association based on the type of the controlling expression. It does not
evaluate the expression at runtime.

> **C Deep Dive:** `_Generic` is powerful but verbose. Each type needs its own
> function, and the mapping must be maintained manually. It also has
> surprising behavior with qualified types: `const int` and `int` are
> different types for `_Generic`, so you may need entries for both.

The `<tgmath.h>` header uses `_Generic` to provide type-generic math
functions:

```c
// C Deep Dive: tgmath.h
#include <tgmath.h>

double d = sqrt(2.0);       // calls sqrt(double)
float f = sqrtf(2.0f);      // calls sqrtf(float) -- but with tgmath:
float g = sqrt(2.0f);       // also calls sqrtf! type-generic dispatch
```

**Auto's approach.** Auto plans to provide generics through `spec` constraints:

```auto
// Auto: generics with spec constraints (planned)
// fn add<T>(a T, b T) T where T: Numeric {
//     a + b
// }

// For now, use separate functions or comptime dispatch
fn generic_add(a int, b int) int {
    a + b
}

fn generic_add_f(a float, b float) float {
    a + b
}
```

<Listing path="listings/ch18/listing-18-01" title="Type-generic programming" />

---

## 18.3 Type Inference

C23 introduces type inference with the `auto` keyword and `typeof`:

```c
// C Deep Dive: C23 type inference
auto x = 42;               // int
auto pi = 3.14;             // double (C defaults to double)
auto name = "hello";        // char* (pointer, not array)

typeof(x) y = x;            // y has the same type as x: int
typeof(3.14) z = 2.72;     // z is double
```

The `auto` keyword in C23 is different from `auto` in older C, where it meant
"automatic storage duration" (a stack variable). In C23, `auto` means
"deduce the type from the initializer."

`typeof` (and `typeof_unqual`) gives you the type of an expression:

```c
// C Deep Dive: typeof uses
int arr[10];
typeof(arr) other;          // int[10]
typeof(arr[0]) val;         // int
typeof(&arr) ptr;           // int(*)[10]

// Useful in macros
#define SWAP(a, b) do { \
    typeof(a) _tmp = a; \
    a = b; \
    b = _tmp; \
} while (0)
```

> **C Deep Dive:** C23's `auto` does not change the type system -- it merely
> deduces the type at compile time. The resulting type is exactly the same as
> if you had written it explicitly. This is different from C++'s `auto`,
> which can deduce different types (e.g., dropping references). C's `auto`
> always deduces the unqualified type of the initializer expression.

**Auto's approach.** Auto has type inference through `var`:

```auto
// Auto: type inference
fn main() {
    var x = 42           // inferred as int
    var pi = 3.14        // inferred as float
    var name = "Auto"    // inferred as str
    var flag = true      // inferred as bool

    print("x:", x)
    print("pi:", pi)
    print("name:", name)
    print("flag:", flag)
}
```

<Listing path="listings/ch18/listing-18-02" title="Type inference" />

Key differences between C23 `auto` and Auto `var`:

| Feature            | C23 `auto`              | Auto `var`               |
|--------------------|-------------------------|--------------------------|
| Declaration        | `auto x = 42;`          | `var x = 42`             |
| Type deduction     | From initializer        | From initializer         |
| Must initialize    | Yes                     | Yes                      |
| Cannot be `NULL`   | No (can be pointer)     | No null pointers         |
| String type        | `char*`                 | `str` (owned string)     |

---

## 18.4 Anonymous Functions

C does not have anonymous functions (lambdas) in the standard language. The
closest equivalent is function pointers:

```c
// C Deep Dive: function pointers
int add(int a, int b) { return a + b; }
int mul(int a, int b) { return a * b; }

int apply(int (*op)(int, int), int a, int b) {
    return op(a, b);
}

int main(void) {
    printf("%d\n", apply(add, 3, 7));  // 10
    printf("%d\n", apply(mul, 3, 7));  // 21
    return 0;
}
```

Apple's Blocks extension adds anonymous functions to C:

```c
// C Deep Dive: Apple Blocks (extension)
#include <Block.h>

int main(void) {
    int (^add)(int, int) = ^(int a, int b) {
        return a + b;
    };
    printf("%d\n", add(3, 7));  // 10
    return 0;
}
```

> **C Deep Dive:** The Blocks extension is not part of standard C. It is
> supported by Clang and Apple's toolchain. GNU C has nested functions as an
> extension, but they are not re-entrant and cannot be returned from functions.
> Neither extension is portable.

**Auto's approach.** Auto plans to support closures as first-class values:

```auto
// Auto: closures (planned)
fn apply(f fn(int, int) int, a int, b int) int {
    f(a, b)
}

fn main() {
    let add = fn(a int, b int) int { a + b }
    let mul = fn(a int, b int) int { a * b }

    print("add:", apply(add, 3, 7))    // 10
    print("mul:", apply(mul, 3, 7))    // 21
}
```

Until closures are implemented, function pointers work the same way as in C:

```auto
// Auto: function values (current)
fn add(a int, b int) int { a + b }

fn apply(f fn(int, int) int, a int, b int) int {
    f(a, b)
}

fn main() {
    print("result:", apply(add, 3, 7))
}
```

> **C Deep Dive:** The lack of standard closures in C is a significant
> limitation. C++ has lambdas (since C++11), Rust has closures, Go has
> anonymous functions, and even Java has lambdas. C's insistence on
> compile-time function definitions makes higher-order programming awkward.
> Auto's closure design draws from these languages to provide a natural
> closure syntax.

---

## Quick Reference

| Concept              | C mechanism                  | Auto mechanism             |
|----------------------|------------------------------|----------------------------|
| Type conversions     | Implicit (with rules)        | Explicit                   |
| Type dispatch        | `_Generic` (C11)             | Generics with `spec`       |
| Type-generic math    | `<tgmath.h>`                | Planned generics           |
| Type inference       | `auto` (C23)                 | `var`                      |
| Type-of expression   | `typeof` (C23)               | Inferred from context      |
| Anonymous functions  | Blocks (extension)           | Closures (planned)         |
| Function pointers    | `int (*)(int, int)`          | `fn(int, int) int`         |

---

*Type-generic programming in C requires layers of macros, `_Generic`, and
compiler extensions. Auto makes it natural: write the algorithm once, and the
type system ensures it works correctly for every type.*
