# Chapter 9: Style

> Level 2 — Cognition
>
> Writing code that humans can read: formatting, naming, and internationalization.

Code is read far more often than it is written. Style is not cosmetic -- it is
engineering discipline that reduces bugs, accelerates review, and makes
maintenance possible. This chapter covers the conventions that C programmers
have developed over five decades and how Auto encodes many of them into the
language itself.

---

## 9.1 Formatting

Consistent formatting is the single easiest improvement you can make to a
codebase. The C community has converged on several widely accepted rules:

**Indentation.** Use either 4 spaces or tabs consistently throughout a project.
Never mix them. Most modern C projects prefer 4-space indentation.

```c
// Good: consistent 4-space indent
if (x > 0) {
    for (int i = 0; i < x; i++) {
        printf("%d\n", i);
    }
}

// Bad: mixed indentation
if (x > 0) {
	for (int i = 0; i < x; i++) {
        printf("%d\n", i);
	}
}
```

**Line length.** Keep lines under 80 characters. Long lines indicate overly
complex expressions that should be broken up.

```c
// Good: broken across lines
int result = compute_something(
    input_data,
    buffer_size,
    &output_count
);

// Bad: excessively long line
int result = compute_something(input_data, buffer_size, &output_count);
```

**Brace style.** The two dominant styles in C are K&R (opening brace on the
same line) and Allman (opening brace on its own line). Pick one and be
consistent.

```c
// K&R style (most common in C)
if (condition) {
    do_something();
}

// Allman style
if (condition)
{
    do_something();
}
```

Auto uses K&R style by default and enforces it with `auto fmt`:

```auto
// Auto enforces consistent formatting
fn calculate_area(width float, height float) float {
    width * height
}
```

Running `auto fmt` on a project reformats every file to a single canonical
style, eliminating formatting debates entirely.

> **Takeaway:** Consistency matters more than any particular style choice.
> If your project has a convention, follow it. If not, adopt `auto fmt`.

---

## 9.2 Naming

Names are the primary documentation of intent. Well-chosen names make code
self-explanatory; poorly chosen names create confusion.

**C naming conventions:**

| Entity          | Convention          | Example                    |
|-----------------|---------------------|----------------------------|
| Variables       | `snake_case`        | `buffer_size`, `row_count` |
| Functions       | `snake_case`        | `compute_area`, `parse_int`|
| Type names      | `PascalCase`        | `TreeNode`, `FileHandle`   |
| Macros/Constants| `UPPER_SNAKE_CASE`  | `MAX_SIZE`, `PI`           |
| Struct members  | `snake_case`        | `first_name`, `age`        |

**Descriptive names.** A name should convey what something is or does:

```c
// Good: descriptive names
int student_count = 0;
float average_grade = 0.0f;
const char* output_filename = "result.txt";

// Bad: cryptic abbreviations
int sc = 0;
float ag = 0.0f;
const char* ofn = "result.txt";
```

**Auto naming conventions.** Auto uses `snake_case` for functions and variables,
`PascalCase` for types, and associates functions with types using dot notation:

```auto
type Rectangle {
    width float
    height float
}

fn Rectangle.area(r Rectangle) float {
    r.width * r.height
}

fn main() {
    let rect Rectangle = Rectangle(5.0, 3.0)
    print("Area:", rect.area(rect))
}
```

The key advantage of Auto's naming system is that associated functions
(`Rectangle.area`) are discoverable -- the type name acts as a namespace.
In C, you must rely on naming conventions (`rectangle_area`) to achieve
the same clarity.

<Listing path="listings/ch09/listing-09-01" title="Clean code style" />

> **Takeaway:** Write names that a newcomer could understand without context.
> Avoid single-letter names except for loop counters (`i`, `j`, `k`).

---

## 9.3 Internationalization

Modern software must handle text in every language. C has historically been
poor at this, but C23 and Auto both provide better support.

**Character sets.** C's `char` is at least 8 bits and traditionally holds
ASCII. C23 mandates that the execution character set include the basic
character set and allows extended characters through encoding:

```c
// C: source charset must support at least ASCII
// Extended characters depend on locale
printf("Hello\n");      // ASCII only
printf("Bonjour\n");    // ASCII compatible
```

**UTF-8.** The dominant encoding for international text is UTF-8, which
represents every Unicode code point as a sequence of 1-4 bytes. C23 introduces
`char8_t` and `u8string` literals:

```c
// C23
const char8_t* greeting = u8"Hello, world!";
```

Auto has built-in UTF-8 support. The `str` type is always UTF-8 encoded:

```auto
let greeting str = "Hello, world!"
let chinese str = "你好世界"
let emoji str = "Hello 🌍"
print(greeting)
print(chinese)
print(emoji)
```

**Source code encoding.** Auto source files are UTF-8 by default. Identifiers
may use ASCII characters. String literals may contain any valid UTF-8:

```auto
// Valid Auto: UTF-8 string literals
let message str = "中文 — Chinese"
let greeting str = "こんにちは — Japanese"
print(message)
print(greeting)
```

> **Takeaway:** Always use UTF-8 for text. C's historical encoding problems
> (Shift-JIS, Latin-1, etc.) are solved by universal UTF-8 adoption. Auto
> makes this the default.

---

## Quick Reference

| Aspect          | C convention                | Auto convention              |
|-----------------|----------------------------|------------------------------|
| Indentation     | 4 spaces or tabs           | 4 spaces (enforced by `fmt`) |
| Line length     | 80 characters              | 80 characters (enforced)     |
| Brace style     | K&R or Allman              | K&R (enforced)               |
| Variable names  | `snake_case`               | `snake_case`                 |
| Function names  | `snake_case`               | `snake_case` / `Type.method` |
| Type names      | `PascalCase`               | `PascalCase`                 |
| Constants       | `UPPER_SNAKE_CASE`         | `UPPER_SNAKE_CASE`           |
| String encoding | Platform-dependent         | UTF-8 always                 |
| Formatting tool | `clang-format`, `indent`   | `auto fmt`                   |

---

*With style conventions established, the next chapter covers how to organize
code across files and document interfaces.*
