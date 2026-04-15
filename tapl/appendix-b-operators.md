# Appendix B: Operator Table

This appendix provides a comprehensive reference for every operator in Auto, organized by precedence from highest to lowest. When multiple operators appear in the same expression, Auto evaluates them according to this ordering.

## Precedence Summary

Operators with higher precedence bind more tightly. Within the same group, most operators are left-associative unless noted otherwise.

| Precedence | Category | Operators |
|---|---|---|
| 1 (highest) | Unary prefix | `-` `!` `*` `view` `mut` `~` |
| 2 | Multiplicative | `*` `/` `%` |
| 3 | Additive | `+` `-` |
| 4 | Comparison | `<` `>` `<=` `>=` |
| 5 | Equality | `==` `!=` `is` |
| 6 | Logical AND | `&&` (alias: `and`) |
| 7 | Logical OR | `\|\|` (alias: `or`) |
| 8 | Null coalescing | `??` |
| 9 | Range | `..` `..=` |
| 10 | Assignment | `=` `+=` `-=` `*=` `/=` `%=` |
| 11 | Pipe | `\|>` |
| 12 (lowest) | Error propagation | postfix `!` postfix `?` |

## Detailed Tables

### 1. Unary Prefix Operators

These operators appear before their operand. They have the highest precedence.

| Operator | Description | Example | Rust | Python | C | TypeScript | Chapter |
|---|---|---|---|---|---|---|---|
| `-` | Numeric negation | `-x` | `-x` | `-x` | `-x` | `-x` | [2](ch02-variables-operators.md) |
| `!` | Boolean NOT | `!flag` | `!flag` | `not flag` | `!flag` | `!flag` | [2](ch02-variables-operators.md) |
| `*` | Dereference (raw pointer) | `*ptr` | `*ptr` | N/A | `*ptr` | N/A | [11](ch11-references.md) |
| `view` | Borrow as read-only reference | `view s` | `&s` | N/A | `const T*` | `readonly` | [11](ch11-references.md) |
| `mut` | Borrow as mutable reference | `mut s` | `&mut s` | N/A | `T*` | N/A | [11](ch11-references.md) |
| `~` | Async blueprint (type modifier) | `~String` | `impl Future` | `Awaitable` | N/A | `Promise` | [16](ch16-async.md) |

### 2. Multiplicative Operators

Standard arithmetic for multiplication, division, and remainder. Left-associative.

| Operator | Description | Example | Result | Rust | Python | C | TypeScript | Chapter |
|---|---|---|---|---|---|---|---|---|
| `*` | Multiplication | `6 * 7` | `42` | `6 * 7` | `6 * 7` | `6 * 7` | `6 * 7` | [2](ch02-variables-operators.md) |
| `/` | Integer division | `15 / 4` | `3` | `15 / 4` | `15 // 4` | `15 / 4` | `Math.trunc(15/4)` | [2](ch02-variables-operators.md) |
| `%` | Remainder (modulo) | `17 % 5` | `2` | `17 % 5` | `17 % 5` | `17 % 5` | `17 % 5` | [2](ch02-variables-operators.md) |

Division of two `int` values truncates toward zero. If either operand is `float`, the result is `float`.

### 3. Additive Operators

Addition and subtraction. Left-associative. The `+` operator also concatenates strings.

| Operator | Description | Example | Result | Rust | Python | C | TypeScript | Chapter |
|---|---|---|---|---|---|---|---|---|
| `+` | Addition / concatenation | `5 + 3` | `8` | `5 + 3` | `5 + 3` | `5 + 3` | `5 + 3` | [2](ch02-variables-operators.md) |
| `-` | Subtraction | `10 - 4` | `6` | `10 - 4` | `10 - 4` | `10 - 4` | `10 - 4` | [2](ch02-variables-operators.md) |

### 4. Comparison Operators

These operators compare two values and return a `bool`. They work on numbers, strings (lexicographic), and booleans.

| Operator | Description | Example | Result | Rust | Python | C | TypeScript | Chapter |
|---|---|---|---|---|---|---|---|---|
| `<` | Less than | `10 < 20` | `true` | `10 < 20` | `10 < 20` | `10 < 20` | `10 < 20` | [2](ch02-variables-operators.md) |
| `>` | Greater than | `10 > 20` | `false` | `10 > 20` | `10 > 20` | `10 > 20` | `10 > 20` | [2](ch02-variables-operators.md) |
| `<=` | Less than or equal | `10 <= 10` | `true` | `10 <= 10` | `10 <= 10` | `10 <= 10` | `10 <= 10` | [2](ch02-variables-operators.md) |
| `>=` | Greater than or equal | `10 >= 20` | `false` | `10 >= 20` | `10 >= 20` | `10 >= 20` | `10 >= 20` | [2](ch02-variables-operators.md) |

### 5. Equality Operators

Equality checks and type tests.

| Operator | Description | Example | Result | Rust | Python | C | TypeScript | Chapter |
|---|---|---|---|---|---|---|---|---|
| `==` | Equal to | `10 == 20` | `false` | `10 == 20` | `10 == 20` | `10 == 20` | `10 === 20` | [2](ch02-variables-operators.md) |
| `!=` | Not equal to | `10 != 20` | `true` | `10 != 20` | `10 != 20` | `10 != 20` | `10 !== 20` | [2](ch02-variables-operators.md) |
| `is` | Type check / pattern match | `x is int` | `bool` | `matches!` | `isinstance()` | N/A | `typeof` / `instanceof` | [7](ch07-enums.md), [17](ch17-smart-casts.md) |

The `is` operator checks whether a value matches a type or pattern. In control flow, it triggers smart casts that narrow the type within the branch (see [Chapter 17][ch17]).

### 6. Logical AND

Short-circuit evaluation: if the left side is `false`, the right side is not evaluated.

| Operator | Description | Example | Result | Rust | Python | C | TypeScript | Chapter |
|---|---|---|---|---|---|---|---|---|
| `&&` | Logical AND (symbolic) | `true && false` | `false` | `true && false` | N/A | `a && b` | `a && b` | [2](ch02-variables-operators.md) |
| `and` | Logical AND (keyword) | `true and false` | `false` | N/A | `a and b` | N/A | N/A | [2](ch02-variables-operators.md) |

Both forms are interchangeable. The `a2p` transpiler converts `&&` to `and` for Python.

### 7. Logical OR

Short-circuit evaluation: if the left side is `true`, the right side is not evaluated.

| Operator | Description | Example | Result | Rust | Python | C | TypeScript | Chapter |
|---|---|---|---|---|---|---|---|---|
| `\|\|` | Logical OR (symbolic) | `true \|\| false` | `true` | `true \|\| false` | N/A | `a \|\| b` | `a \|\| b` | [2](ch02-variables-operators.md) |
| `or` | Logical OR (keyword) | `true or false` | `true` | N/A | `a or b` | N/A | N/A | [2](ch02-variables-operators.md) |

Both forms are interchangeable. The `a2p` transpiler converts `||` to `or` for Python.

### 8. Null Coalescing

| Operator | Description | Example | Rust | Python | C | TypeScript | Chapter |
|---|---|---|---|---|---|---|---|
| `??` | Default value for `?T` | `name ?? "unknown"` | `.unwrap_or("unknown")` | `name or "unknown"` | N/A | `name ?? "unknown"` | [9](ch09-error-handling.md) |

The `??` operator returns the left side if it is `Some(value)`, otherwise it returns the right side as the default. It only applies to `?T` (optional) values.

### 9. Range Operators

Used in `for` loops and to create range expressions.

| Operator | Description | Example | Values | Rust | Python | C | TypeScript | Chapter |
|---|---|---|---|---|---|---|---|---|
| `..` | Exclusive end range | `0..5` | 0, 1, 2, 3, 4 | `0..5` | `range(0, 5)` | `for (i=0;i<5;i++)` | N/A | [3](ch03-functions.md) |
| `..=` | Inclusive end range | `1..=5` | 1, 2, 3, 4, 5 | `1..=5` | `range(1, 6)` | `for (i=1;i<=5;i++)` | N/A | [3](ch03-functions.md) |

The `..` range is exclusive on the right (does not include the upper bound). The `..=` range is inclusive on the right (includes the upper bound).

### 10. Assignment Operators

Assignment is a statement in Auto, not an expression. It does not return a value.

| Operator | Description | Example | Equivalent | Rust | Python | C | TypeScript | Chapter |
|---|---|---|---|---|---|---|---|---|
| `=` | Assign | `x = 5` | -- | `x = 5` | `x = 5` | `x = 5` | `x = 5` | [2](ch02-variables-operators.md) |
| `+=` | Add and assign | `x += 3` | `x = x + 3` | `x += 3` | `x += 3` | `x += 3` | `x += 3` | [2](ch02-variables-operators.md) |
| `-=` | Subtract and assign | `x -= 2` | `x = x - 2` | `x -= 2` | `x -= 2` | `x -= 2` | `x -= 2` | [2](ch02-variables-operators.md) |
| `*=` | Multiply and assign | `x *= 4` | `x = x * 4` | `x *= 4` | `x *= 4` | `x *= 4` | `x *= 4` | [2](ch02-variables-operators.md) |
| `/=` | Divide and assign | `x /= 2` | `x = x / 2` | `x /= 2` | `x //= 2` | `x /= 2` | `x /= 2` | [2](ch02-variables-operators.md) |
| `%=` | Remainder and assign | `x %= 3` | `x = x % 3` | `x %= 3` | `x %= 3` | `x %= 3` | `x %= 3` | [2](ch02-variables-operators.md) |

### 11. Pipe Operator

| Operator | Description | Example | Rust | Python | C | TypeScript | Chapter |
|---|---|---|---|---|---|---|---|
| `\|>` | Forward pipe | `data \|> transform \|> save` | Method chaining | Method chaining | N/A | Method chaining | [19](ch19-closures.md) |

The pipe operator feeds the left side as the first argument to the function on the right. It enables a data-flow style where transformations are read left to right. This is equivalent to method chaining (`data.transform().save()`), but works with standalone functions.

### 12. Error Propagation Operators

These postfix operators handle `?T` (optional) and `!T` (result) types. They have the lowest precedence because they apply to the entire preceding expression.

| Operator | Description | Example | Rust | Python | C | TypeScript | Chapter |
|---|---|---|---|---|---|---|---|
| postfix `!` | Unwrap `!T`; panic on `Err` | `parse(s)!` | `.unwrap()` | N/A | N/A | `!` (non-null assert) | [9](ch09-error-handling.md) |
| postfix `?` | Propagate error / unwrap `!T` | `read_file(path)?` | `?` (same) | N/A | N/A | N/A | [9](ch09-error-handling.md) |

The postfix `!` unwraps a `!T` value, returning the `Ok` payload or panicking with the `Err` message. It is similar to Rust's `.unwrap()`.

The postfix `?` propagates errors up the call stack. Inside a function marked with `!` in its return type, `expr?` unwraps the result on success or returns the error to the caller. It is equivalent to Rust's `?` operator.

## Type Modifier Operators

These operators appear in type positions rather than expression positions. They modify the meaning of a type annotation.

| Modifier | Description | Example | Rust Equivalent | Chapter |
|---|---|---|---|---|
| `?T` | Optional (nullable) value | `fn find(id int) ?User` | `Option<T>` | [9](ch09-error-handling.md) |
| `!T` | Result (fallible) value | `fn read(path str) !str` | `Result<T, String>` | [9](ch09-error-handling.md) |
| `~T` | Async blueprint (future) | `fn fetch(url str) ~str` | `impl Future<Output=T>` | [16](ch16-async.md) |

These can be composed: `~?String` is a future optional string, and `~!int` is a future fallible integer.

## Access Operators

These operators are used for member access and optional chaining. They are not listed in the precedence table because they are postfix accessors with inherent precedence (left to right, tightly binding).

| Operator | Description | Example | Rust | Python | C | TypeScript | Chapter |
|---|---|---|---|---|---|---|---|
| `.` | Field / method access | `user.name` | `user.name` | `user.name` | `user.name` | `user.name` | [8](ch08-oop.md) |
| `?.` | Optional chaining | `addr?.city` | `.as_ref()?.city` | N/A | N/A | `addr?.city` | [9](ch09-error-handling.md) |
| `.await` | Await async blueprint | `fetch().await` | `.await` | `await` | N/A | `await` | [16](ch16-async.md) |

## Notes

- **Short-circuit evaluation**: `&&` and `||` evaluate the right side only if necessary. If the left side of `&&` is `false`, the right side is skipped. If the left side of `||` is `true`, the right side is skipped.
- **No operator overloading**: Auto does not support user-defined operator overloading. All operators have fixed semantics defined by the language.
- **Integer division**: Dividing two `int` values with `/` truncates toward zero. Use at least one `float` operand for decimal division.
- **Assignment is not an expression**: Unlike C, assignment in Auto does not return a value. You cannot write `x = y = 5` or use assignment inside an `if` condition.
- **Keyword aliases**: `and` and `or` are aliases for `&&` and `||`. They exist primarily for readability and for the Python transpiler, which maps them directly.
