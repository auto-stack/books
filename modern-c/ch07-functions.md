# Chapter 7: Functions

> Level 1 — Acquaintance
>
> Encapsulating logic into reusable, composable units.

Functions are the primary mechanism for organizing code. A function takes inputs
(parameters), performs computation, and produces an output (return value). C and Auto
share the same fundamental model but differ in syntax, type expression, and safety
guarantees.

---

## 7.1 Simple Functions

A C function has a return type, a name, a parameter list, and a body:

```c
// C
int max(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
```

An Auto function uses the `fn` keyword with type annotations following parameter names:

```auto
// Auto
fn max(a int, b int) int {
    if a > b { a } else { b }
}
```

Key differences:

| Feature              | C                            | Auto                          |
|----------------------|------------------------------|-------------------------------|
| Keyword              | None (return type first)     | `fn`                          |
| Return type          | Before function name         | After parameter list          |
| Parameter syntax     | `int a, int b`               | `a int, b int`               |
| Return statement     | `return expr;`               | Last expression or `return`   |
| Empty parameters     | `void`                       | Empty `()`                    |
| Missing return       | Undefined behavior           | Compile error                 |

**Implicit return:** In Auto, the last expression in a block is its value. There is
no need for an explicit `return` keyword when the function body is a single expression
or when the last expression is the intended return value:

```auto
fn square(x int) int {
    x * x             // implicit return
}

fn clamp(val int, lo int, hi int) int {
    max(lo, min(val, hi))    // implicit return
}
```

**Forward declarations:** In C, functions must be declared before use. This often
requires forward declarations (prototypes) at the top of a file:

```c
int min(int a, int b);     // forward declaration
int max(int a, int b) { ... }
int clamp(int v, int lo, int hi) { return max(lo, min(v, hi)); }
int min(int a, int b) { return a < b ? a : b; }
```

Auto does not require forward declarations. The compiler resolves function references
in a single pass, so you can call a function before it is defined:

```auto
fn clamp(val int, lo int, hi int) int {
    max(lo, min(val, hi))
}

fn max(a int, b int) int {
    if a > b { a } else { b }
}

fn min(a int, b int) int {
    if a < b { a } else { b }
}
```

<Listing path="listings/ch07/listing-07-01" title="Simple functions" />

> **Takeaway:** Auto's implicit return and lack of forward declarations reduce
> boilerplate. Focus on the logic, not the ceremony.

---

## 7.2 main Is Special

Every C program starts executing at the `main` function. The C standard defines two
valid signatures:

```c
// Form 1: no arguments
int main(void) {
    // ...
    return 0;
}

// Form 2: command-line arguments
int main(int argc, char *argv[]) {
    for (int i = 0; i < argc; i++) {
        printf("argv[%d] = %s\n", i, argv[i]);
    }
    return 0;
}
```

Auto simplifies `main`:

```auto
// Auto: no arguments
fn main() {
    // ...
}

// Auto: with command-line arguments
fn main(args [str]) {
    for i in 0..len(args) {
        print("arg[", i, "] =", args[i])
    }
}
```

The transpiler maps `fn main()` to `int main(void)` and `fn main(args [str])` to
`int main(int argc, char *argv[])`.

Differences:

| Feature           | C                           | Auto                        |
|-------------------|-----------------------------|------------------------------|
| Return type       | `int` (required)            | Omitted (transpiler adds)   |
| Return value      | `return 0;` for success     | Omitted (implicit success)  |
| Argument count    | `argc`                      | `len(args)`                 |
| Argument array    | `char *argv[]`              | `[str]`                     |
| Exit codes        | `return n;` or `exit(n)`    | `return n` or `exit(n)`     |

> **Takeaway:** In C, `main` returns `int`. Forgetting the return is technically
> undefined behavior in older C standards (C89), though C99 and later allow omitting
> it. Auto handles this automatically.

---

## 7.3 Recursion

A function is **recursive** if it calls itself. Recursion is the same concept in both
languages — the differences are purely syntactic.

**Factorial** — the classic recursive example:

```c
// C
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

```auto
// Auto
fn factorial(n int) int {
    if n <= 1 {
        1
    } else {
        n * factorial(n - 1)
    }
}
```

**Fibonacci** — demonstrates multiple recursive calls:

```c
// C
int fibonacci(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

```auto
// Auto
fn fibonacci(n int) int {
    if n <= 0 { return 0 }
    if n == 1 { return 1 }
    fibonacci(n - 1) + fibonacci(n - 2)
}
```

Note that Auto uses `return` as an early exit inside `if` blocks. The last expression
in a non-`if` branch is an implicit return.

<Listing path="listings/ch07/listing-07-02" title="Recursion: factorial and fibonacci" />

### How Recursion Works

Each recursive call creates a new **stack frame** containing:
- The function's parameters
- Local variables
- The return address

For `factorial(5)`, the call stack grows like this:

```
factorial(5)
  → 5 * factorial(4)
    → 4 * factorial(3)
      → 3 * factorial(2)
        → 2 * factorial(1)
          → 1   (base case)
```

Then the results unwind: `1 → 2 → 6 → 24 → 120`.

**Stack overflow:** If recursion goes too deep (e.g., `factorial(1000000)`), the
stack runs out of space. C and Auto both face this limitation. For deep recursion,
use an iterative approach or tail-call optimization (where supported).

> **Takeaway:** Recursion is elegant but watch out for stack depth. For production
> code, prefer iterative solutions for algorithms that may recurse deeply.

---

## Quick Reference

| Concept            | C syntax                     | Auto syntax                  |
|--------------------|------------------------------|------------------------------|
| Function declare   | `int f(int a) { ... }`      | `fn f(a int) int { ... }`   |
| Void return        | `void f(void) { ... }`      | `fn f() { ... }`            |
| Return value       | `return expr;`              | Last expr or `return expr`   |
| Forward declare    | `int f(int a);`             | Not needed                   |
| main (simple)      | `int main(void)`            | `fn main()`                  |
| main (args)        | `int main(int argc, char *argv[])` | `fn main(args [str])` |
| Recursion          | Same as regular function     | Same as regular function     |
| Early return       | `return;` / `return val;`   | `return` / `return val`      |

---

*Next: [Chapter 8 — C Library Functions](ch08-c-library.md)*
