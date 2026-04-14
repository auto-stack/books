# Chapter 5: Basic Values & Data

> Level 1 — Acquaintance
>
> The foundation of all computation: types, values, and how C and Auto represent data.

This is the most important chapter in Level 1. Everything you build in C or Auto
rests on understanding how the language represents values in memory. We cover the
abstract machine model, basic types, conversions, initializers, named constants,
and binary representations.

---

## 5.1 The Abstract State Machine

> **C Deep Dive:** The C standard does not describe a physical computer. Instead it
> defines an **abstract state machine** that specifies what a conforming program must
> do. A real compiler's job is to produce code that behaves *as if* the abstract
> machine executed the program.

The abstract machine has:

- **Objects** — regions of storage that hold values (variables, allocated memory).
- **Values** — the bit patterns stored in objects, interpreted according to their type.
- **Side effects** — changes to the state of the machine (writing to a variable,
  calling an I/O function).
- **Sequence points** — moments when all preceding side effects are guaranteed complete.

When you write `int x = 42;`, the abstract machine:

1. Allocates storage for an object named `x`.
2. Determines that its type is `int`.
3. Stores the value `42` in that object.

Auto simplifies this model by removing undefined behavior. If an Auto program
compiles, it has well-defined semantics. The trade-off is that Auto hides certain
machine-level details that C exposes (such as raw pointer arithmetic and exact
object layout).

> **Takeaway:** C's abstract machine is a *contract* between you and the compiler.
> Stay within the contract and your code is portable and predictable. Violate it
> (e.g., via undefined behavior) and the compiler is free to do anything.

---

## 5.2 Basic Types

C has a small but nuanced set of fundamental types. Auto maps them to a cleaner
subset:

| C type         | Auto type   | Size (typical) | Notes                         |
|----------------|-------------|----------------|-------------------------------|
| `char`         | `char`      | 1 byte         | Character or small integer    |
| `signed char`  | `i8`        | 1 byte         | Explicitly signed 8-bit       |
| `unsigned char`| `u8`        | 1 byte         | Unsigned 8-bit                |
| `short`        | `i16`       | 2 bytes        | Short integer                 |
| `int`          | `int`       | 4 bytes        | Default integer               |
| `long`         | `i64`       | 4 or 8 bytes   | Platform-dependent            |
| `long long`    | `i64`       | 8 bytes        | At least 64-bit               |
| `float`        | `float`     | 4 bytes        | Single-precision IEEE 754     |
| `double`       | `float`     | 8 bytes        | Double-precision; Auto uses `float` for both |
| `_Bool`        | `bool`      | 1 byte         | C99 boolean; Auto has `bool`  |
| `size_t`       | `usize`     | 4 or 8 bytes   | Unsigned, sizeof result       |

Key differences:

- **C's `double` is distinct from `float`**. Auto unifies them as `float` and lets
  the compiler choose the precision.
- **C has signed/unsigned variants for every integer type.** Auto defaults to signed
  and provides explicit `u8`, `u16`, `u32`, `u64` for unsigned needs.
- **C's `char` may be signed or unsigned** depending on the platform. Auto treats
  `char` as a distinct type for character data only.

<Listing path="listings/ch05/listing-05-01" title="Basic types and the abstract state machine" />

---

## 5.3 Specifying Values

**Literals** are values written directly in the source code:

```c
// C integer literals
42          // decimal int
052         // octal int (42 decimal)
0x2A        // hexadecimal int (42 decimal)
42U         // unsigned int
42LL        // long long

// C floating-point literals
3.14        // double
3.14f       // float
1.0e-3      // double in scientific notation

// C character and string literals
'A'         // char (single quotes)
"hello"     // char[] / char* (double quotes)
```

Auto's literal syntax is similar but without type suffixes:

```auto
let n int = 42          // integer literal
let f float = 3.14      // floating-point literal
let c char = 'A'        // character literal
let s str = "hello"     // string literal
```

**Enumerations** create named integer constants:

```c
// C
enum color { RED, GREEN, BLUE };    // 0, 1, 2
enum color fav = GREEN;
```

```auto
// Auto
enum Color {
    Red
    Green
    Blue
}
let fav Color = Color.Green
```

> **Takeaway:** C's enumerations are plain integers — you can assign any `int` to an
> `enum` variable. Auto's enums are proper types with compile-time checking.

---

## 5.4 Implicit Conversions

C performs many conversions automatically. This is convenient but dangerous:

- **Integer promotion:** `char` and `short` are promoted to `int` in expressions.
- **Arithmetic conversion:** When mixing types, the narrower type is converted to
  the wider one. `int + float` promotes the `int` to `float` first.
- **Assignment conversion:** Assigning a wider type to a narrower type silently
  truncates. `double` to `int` drops the fractional part.

```c
int i = 3.14;     // i becomes 3 — silent truncation
double d = 42;    // d becomes 42.0 — safe promotion
```

Auto is stricter. Narrowing conversions require an explicit cast:

```auto
let i int = int(3.14)       // explicit — you acknowledge the truncation
let f float = float(42)     // widening — could be implicit, explicit is clearer
```

<Listing path="listings/ch05/listing-05-02" title="Type conversions and initializers" />

> **Takeaway:** In C, implicit conversions can silently lose data. Auto makes
> narrowing conversions explicit so you think about them.

---

## 5.5 Initializers

C's initializer syntax has evolved significantly. Modern C (C99 and later) supports
**designated initializers** that name the fields being set:

```c
// C array initializer
int primes[] = { 2, 3, 5, 7, 11 };

// C struct initializer (designated)
struct Point { int x; int y; };
struct Point p = { .x = 1, .y = 2 };
```

Auto uses a **constructor call** syntax that mirrors function calls:

```auto
// Auto array initializer
let primes [5]int = [5]int{2, 3, 5, 7, 11}

// Auto struct initializer (constructor syntax)
let p Point = Point(1, 2)
```

Uninitialized local variables in C have **indeterminate values** — reading them is
undefined behavior. Auto requires explicit initialization for `let` bindings; `var`
declarations may start uninitialized but the compiler warns about use before
assignment.

---

## 5.6 Named Constants

C has three mechanisms for named constants, each with different properties:

| Mechanism     | Example              | Type-safe | Scoped | Compile-time |
|---------------|----------------------|-----------|--------|--------------|
| `#define`     | `#define PI 3.14`    | No        | No     | Yes          |
| `const`       | `const double PI = 3.14;` | Partial | Yes   | Varies       |
| `enum`        | `enum { MAX = 1024 };` | Yes (int only) | Yes | Yes     |

Auto unifies these with `let`:

```auto
let pi float = 3.14159       // immutable constant
let max_size int = 1024      // immutable constant
```

Auto's `let` is always immutable and always scoped. The compiler can inline these
values at compile time when beneficial.

<Listing path="listings/ch05/listing-05-03" title="Named constants and enumerations" />

> **Takeaway:** In C, prefer `enum` for integer constants and `const` for other types.
> Avoid `#define` for constants — the preprocessor is a blunt tool. In Auto, `let`
> handles all cases uniformly.

---

## 5.7 Binary Representations

> **C Deep Dive:** Understanding how values are stored as bits is essential for
> systems programming. C gives you direct access to the bit level; Auto provides
> library functions for the same operations.

**Two's complement** is the standard representation for signed integers (mandated
by C23, universal in practice since C99). The most significant bit acts as a sign
bit: `0` for positive, `1` for negative. To negate a value, invert all bits and
add 1.

```
Value    8-bit two's complement
  0      00000000
  1      00000001
  42     00101010
 127     01111111
 -1      11111111
 -42     11010110
-128     10000000
```

**Bitwise operators** manipulate individual bits:

| Operator | C / Auto | Meaning                | Example (8-bit)          |
|----------|----------|------------------------|--------------------------|
| AND      | `a & b`  | Both bits 1 → 1        | `0x0F & 0x55 = 0x05`   |
| OR       | `a \| b` | Either bit 1 → 1       | `0x0F \| 0x55 = 0x5F`  |
| XOR      | `a ^ b`  | Bits differ → 1        | `0x0F ^ 0x55 = 0x5A`   |
| NOT      | `~a`     | Flip all bits           | `~0x0F = 0xF0`         |
| Left shift  | `a << n` | Shift bits left     | `1 << 3 = 8`           |
| Right shift | `a >> n` | Shift bits right    | `8 >> 3 = 1`           |

Common bit tricks:

```c
// Set bit n:       flags |= (1 << n);
// Clear bit n:     flags &= ~(1 << n);
// Toggle bit n:    flags ^= (1 << n);
// Test bit n:      (flags >> n) & 1
```

> **Takeaway:** Bitwise operations are the same in both languages. Auto provides
> these for low-level work, but most programs should use higher-level abstractions.

---

## Quick Reference

| Concept           | C                         | Auto                         |
|-------------------|---------------------------|------------------------------|
| Integer type      | `int`, `long`, `short`    | `int`, `i8`–`i64`           |
| Float type        | `float`, `double`         | `float`                      |
| Boolean type      | `_Bool` / `bool` (C23)    | `bool`                       |
| String type       | `char*` / `char[]`        | `str`                        |
| Integer literal   | `42`, `0x2A`, `052`       | `42`                         |
| Float literal     | `3.14`, `3.14f`           | `3.14`                       |
| Char literal      | `'A'`                     | `'A'`                        |
| String literal    | `"hello"`                 | `"hello"`                    |
| Enum              | `enum color { R, G, B };` | `enum Color { Red Green Blue }` |
| Cast              | `(int)x`                  | `int(x)`                     |
| Const variable    | `const int N = 10;`       | `let N int = 10`            |
| Preprocessor def  | `#define N 10`            | `let N int = 10`            |
| Array init        | `{ 1, 2, 3 }`             | `[3]int{1, 2, 3}`           |
| Struct init       | `{ .x = 1, .y = 2 }`      | `Point(1, 2)`               |

---

*Next: [Chapter 6 — Derived Data Types](ch06-derived-types.md)*
