# Language Basics

This chapter covers the fundamental building blocks of Auto and how they map to
C. You will learn about data types, variables, operators, control flow, loops,
functions, and scope.

## 11. Data Types

Auto provides five basic types that map directly to C types:

| Auto Type | C Type | Description |
|-----------|--------|-------------|
| `int` | `int` | Integer (typically 32-bit) |
| `float` | `float` | Floating-point number |
| `bool` | `int` | Boolean (0 or 1) |
| `char` | `char` | Single character |
| `str` | `char*` | String (null-terminated) |

Auto's `bool` maps to C's `int` because C did not have a native `_Bool` until
C99, and many C codebases still use `int` for boolean values.

<Listing name="data-types" file="listings/ch01/listing-01-01">

```auto
fn main() {
    let age int = 25
    let height float = 1.75
    let initial char = 'A'
    let name str = "Auto"
    let active bool = true

    print("Age:", age)
    print("Height:", height)
    print("Initial:", initial)
    print("Name:", name)
    print("Active:", active)
}
```

</Listing>

The a2c transpiler adds the correct format specifier for each type: `%d` for
`int`, `%f` for `float`, `%c` for `char`, `%s` for `str`.

## 12. Constants and Scope

Auto uses `let` for immutable bindings and `var` for mutable variables:

```auto
let pi float = 3.14      // immutable
var count int = 0        // mutable
count = count + 1        // okay
```

In C, this maps to `const float pi = 3.14f;` and `int count = 0;`. Block scope
works the same way in both languages — variables declared inside `{ }` are
local to that block.

## 13. Operators

Auto's operators are nearly identical to C's.

<Listing name="operators" file="listings/ch01/listing-01-02">

```auto
fn main() {
    let a int = 10
    let b int = 3

    print("a + b =", a + b)
    print("a - b =", a - b)
    print("a * b =", a * b)
    print("a / b =", a / b)
    print("a % b =", a % b)

    print("a == b:", a == b)
    print("a > b:", a > b)
    print("a && b:", a > 0 && b > 0)
}
```

</Listing>

Arithmetic operators (`+`, `-`, `*`, `/`, `%`), comparison operators (`==`,
`!=`, `>`, `<`, `>=`, `<=`), and logical operators (`&&`, `||`) all map
directly to their C equivalents.

> **C Only**: C has bitwise assignment operators (`&=`, `|=`, `^=`, `<<=`,
> `>>=`) and the comma operator. Auto does not provide these directly.

## 14. Control Flow

Auto offers `if`/`else` for conditional logic and `is` for pattern matching
(which maps to C's `switch`).

<Listing name="control-flow" file="listings/ch01/listing-01-03">

```auto
fn classify(n int) str {
    if n > 0 {
        "positive"
    } else if n < 0 {
        "negative"
    } else {
        "zero"
    }
}

fn describe(x int) str {
    is x {
        0 => "nothing"
        1 => "one"
        2 => "two"
        else => "many"
    }
}
```

</Listing>

The `is` expression transpiles to a C `switch` statement. Unlike C's `switch`,
Auto's `is` does not require `break` statements — each arm implicitly returns
and there is no fall-through.

## 15. Loops

Auto provides `for` for counted iteration and `while` for conditional looping.

<Listing name="loops" file="listings/ch01/listing-01-04">

```auto
fn main() {
    for i in 0..5 {
        print("i =", i)
    }

    var sum int = 0
    var n int = 1
    while n <= 10 {
        sum = sum + n
        n = n + 1
    }
    print("Sum 1..10 =", sum)
}
```

</Listing>

The range loop `for i in 0..5` maps to `for (int i = 0; i < 5; i++)`. The
`while` loop maps directly to C's `while` with identical semantics.

> **C Only**: C has `do...while` and `goto`. Auto does not provide `goto`. A
> `do...while` equivalent can be written with `while true` and `break`.

## 16. Functions

Auto functions declare parameters with types and optional return types. If no
return type is specified, the function returns `void` in C.

<Listing name="functions" file="listings/ch01/listing-01-05">

```auto
fn add(a int, b int) int {
    a + b
}

fn factorial(n int) int {
    if n <= 1 {
        1
    } else {
        n * factorial(n - 1)
    }
}
```

</Listing>

The last expression in a function body is the return value. The a2c transpiler
inserts explicit `return` statements in the generated C. No forward
declarations are needed — Auto handles ordering.

## 17. Scope and Shadowing

Both Auto and C use block scope. Auto also supports shadowing — re-declaring a
variable with the same name in an inner scope:

```auto
let x int = 10
if true {
    let x int = 20
    print(x)    // 20
}
print(x)        // 10
```

In C, shadowing works the same way with nested `{ }` blocks.

## 18. Type Casting

Auto provides explicit type casts between compatible types. `let y float =
float(x)` maps to C's `(float)x`. Auto does not allow unsafe casts (e.g.,
casting `str` to `int`); the transpiler rejects invalid conversions.

## 19. Recursion

Recursion works identically in Auto and C. The `factorial` function in Listing
01-05 is a classic example. Auto supports direct and mutual recursion; the a2c
transpiler handles forward declarations automatically.

## 20. Practice: Calculator

Put everything together with a simple calculator.

<Listing name="calculator" file="listings/ch01/listing-01-06">

```auto
fn calculate(a int, op str, b int) int {
    if op == "+" {
        a + b
    } else if op == "-" {
        a - b
    } else if op == "*" {
        a * b
    } else if op == "/" {
        if b == 0 {
            print("Error: division by zero")
            0
        } else {
            a / b
        }
    } else {
        print("Unknown operator:", op)
        0
    }
}

fn main() {
    print("10 + 3 =", calculate(10, "+", 3))
    print("10 - 3 =", calculate(10, "-", 3))
    print("10 * 3 =", calculate(10, "*", 3))
    print("10 / 3 =", calculate(10, "/", 3))
    print("10 / 0 =", calculate(10, "/", 0))
}
```

</Listing>

Notice that `op == "+"` in Auto becomes `strcmp(op, "+") == 0` in the generated
C. String comparison in C requires `strcmp`; Auto's `==` operator handles this
automatically.

## Quick Reference

| Concept | Auto | C |
|---------|------|---|
| Integer | `int` | `int` |
| Float | `float` | `float` |
| Boolean | `bool` | `int` (0/1) |
| String | `str` | `char*` |
| Character | `char` | `char` |
| Immutable | `let x int = 5` | `const int x = 5;` |
| Mutable | `var x int = 5` | `int x = 5;` |
| If/else | `if { } else { }` | `if () { } else { }` |
| Switch | `is x { ... }` | `switch (x) { ... }` |
| For loop | `for i in 0..n` | `for (int i=0; i<n; i++)` |
| While loop | `while cond { }` | `while (cond) { }` |
| Function | `fn name(params) type { }` | `type name(params) { }` |
| Implicit return | last expression | explicit `return` |
| String compare | `a == b` | `strcmp(a, b) == 0` |
