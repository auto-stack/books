# Chapter 8: C Library Functions

> Level 1 — Acquaintance
>
> The standard library: what C provides out of the box and how Auto wraps it.

No C program works in isolation. The C standard library provides essential functions
for I/O, string manipulation, mathematics, memory management, and system interaction.
Auto wraps most of these in safer, more ergonomic interfaces while preserving the
underlying C implementation.

---

## 8.1 General Properties

The C standard library is organized into **headers**, each declaring a set of related
functions, types, and macros:

| Header       | Purpose                          | Key functions                 |
|--------------|----------------------------------|-------------------------------|
| `<stdio.h>`  | Input/output                     | `printf`, `scanf`, `fopen`    |
| `<stdlib.h>` | General utilities                | `malloc`, `free`, `exit`, `abs` |
| `<string.h>` | String handling                  | `strlen`, `strcmp`, `strcpy`  |
| `<math.h>`   | Mathematics                      | `sqrt`, `sin`, `pow`, `ceil`  |
| `<time.h>`   | Date and time                    | `time`, `clock`, `strftime`   |
| `<ctype.h>`  | Character classification         | `isdigit`, `toupper`          |
| `<assert.h>` | Diagnostics                      | `assert`                      |
| `<errno.h>`  | Error indicators                 | `errno`, `strerror`           |
| `<stddef.h>` | Common definitions               | `size_t`, `NULL`, `offsetof`  |

To use a library function, you `#include` its header:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
```

Auto implicitly includes the transpiled equivalents. You do not write `#include`
directly — the a2c transpiler adds the necessary headers based on which functions
your code uses.

**Error handling with `errno`:** Many C library functions report errors by setting
the global variable `errno` and returning a sentinel value (often `NULL` or `-1`).

```c
// C: checking errno
errno = 0;
double result = sqrt(-1.0);
if (errno != 0) {
    fprintf(stderr, "Error: %s\n", strerror(errno));
}
```

Auto wraps these patterns into return types that force error checking (such as
optional types `?T` or result types `Result<T, E>`), eliminating the risk of
forgetting to check `errno`.

> **Takeaway:** In C, always check return values and `errno` for library calls. In
> Auto, the type system forces you to handle errors.

---

## 8.2 Integer Arithmetic

The `<stdlib.h>` header provides integer arithmetic utilities:

```c
// C
int absolute = abs(-42);          // 42
div_t result = div(17, 5);        // result.quot = 3, result.rem = 2
```

Auto provides these through built-in operators and library functions:

```auto
let quotient int = 17 / 5        // 3
let remainder int = 17 % 5       // 2
let absolute int = abs(-42)      // 42
```

<Listing path="listings/ch08/listing-08-01" title="Integer arithmetic with stdlib" />

> **Takeaway:** C's `div` function returns a `struct` containing both quotient and
> remainder in a single operation. Auto's separate `/` and `%` operators are clearer
> for most use cases.

---

## 8.3 Numerics

The `<math.h>` header provides floating-point mathematics:

| Function   | Purpose            | Example                  |
|------------|--------------------|--------------------------|
| `sqrt(x)`  | Square root        | `sqrt(25.0) = 5.0`      |
| `pow(x,y)` | x to power y       | `pow(2,10) = 1024.0`    |
| `ceil(x)`  | Round up           | `ceil(3.2) = 4.0`       |
| `floor(x)` | Round down         | `floor(3.8) = 3.0`      |
| `fabs(x)`  | Absolute value     | `fabs(-3.14) = 3.14`    |
| `fmod(x,y)`| Float remainder    | `fmod(7.5, 2.0) = 1.5`  |
| `sin(x)`   | Sine (radians)     | `sin(3.14159) ≈ 0.0`    |
| `cos(x)`   | Cosine (radians)   | `cos(0.0) = 1.0`        |
| `log(x)`   | Natural logarithm  | `log(2.71828) ≈ 1.0`    |

Auto provides the same functions. Since Auto unifies `float` and `double` into
`float`, the compiler selects the appropriate C function (`sqrtf` vs `sqrt`)
based on precision needs.

---

## 8.4 I/O

**Formatted output** with `printf` is C's primary output mechanism:

```c
// C
printf("Hello, %s! You are %d years old.\n", name, age);
printf("PI = %.2f\n", 3.14159);           // PI = 3.14
printf("Hex: 0x%X\n", 255);               // Hex: 0xFF
```

Auto's `print` handles formatting automatically:

```auto
print("Hello,", name, "! You are", age, "years old.")
print("PI =", 3.14159)
```

**Format specifiers** in C (for reference):

| Specifier | Type           | Example output          |
|-----------|----------------|------------------------|
| `%d`      | `int`          | `42`                   |
| `%u`      | `unsigned int` | `42`                   |
| `%f`      | `double`       | `3.140000`             |
| `%.2f`    | `double`       | `3.14`                 |
| `%s`      | `char*`        | `hello`                |
| `%c`      | `char`         | `A`                    |
| `%x`      | `int` (hex)    | `2a`                   |
| `%p`      | pointer        | `0x7ffd1234`           |
| `%zu`     | `size_t`       | `42`                   |
| `%%`      | literal `%`    | `%`                    |

**File I/O** in C uses `FILE*` handles:

```c
// C
FILE *f = fopen("data.txt", "r");
if (!f) { perror("fopen"); return 1; }
char line[256];
while (fgets(line, sizeof(line), f)) {
    printf("%s", line);
}
fclose(f);
```

Auto provides higher-level file operations:

```auto
let content str = read_file("data.txt")
print(content)
write_file("output.txt", "Hello, file!")
```

<Listing path="listings/ch08/listing-08-02" title="Formatted I/O" />

> **Takeaway:** C's `printf` format strings are powerful but error-prone — a wrong
> specifier causes undefined behavior. Auto's `print` infers types at compile time.

---

## 8.5 String Processing

C strings are null-terminated `char` arrays. The `<string.h>` header provides:

| Function       | Purpose                    | Auto equivalent        |
|----------------|----------------------------|------------------------|
| `strlen(s)`    | String length              | `len(s)`               |
| `strcmp(a,b)`  | Compare (returns -1/0/1)   | `a == b` (bool)        |
| `strcpy(d,s)`  | Copy string                | `let d = s`            |
| `strcat(d,s)`  | Concatenate                | `a + b`                |
| `strchr(s,c)`  | Find character             | `s.find(c)`            |
| `strstr(s,sub)`| Find substring             | `s.contains(sub)`      |

The key difference is safety. C's string functions require manual buffer management:

```c
// C: dangerous if dest is too small
char dest[10];
strcpy(dest, "Hello, World!");   // BUFFER OVERFLOW!
```

Auto strings are dynamically sized and bounds-checked:

```auto
let greeting str = "Hello, World!"   // safe, auto-sized
```

<Listing path="listings/ch08/listing-08-03" title="String processing" />

> **Takeaway:** C string handling is the source of countless security vulnerabilities
> (buffer overflows, off-by-one errors). Auto's `str` type eliminates these by
> managing memory and bounds automatically.

---

## 8.6 Time

The `<time.h>` header provides time-related functions:

```c
// C: current time as timestamp
time_t now = time(NULL);
printf("Timestamp: %ld\n", (long)now);

// C: formatted time
char buf[64];
strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", localtime(&now));
printf("Date/time: %s\n", buf);
```

Auto provides simpler wrappers:

```auto
let now int = time()
let formatted str = strftime("%Y-%m-%d %H:%M:%S")
print("Current time:", formatted)
```

---

## 8.7 Runtime Environment

C provides functions to interact with the runtime environment:

```c
// C: environment variables
char *home = getenv("HOME");
printf("HOME = %s\n", home);

// C: execute system command
int ret = system("ls -la");
```

Auto equivalents:

```auto
let home str = env("HOME")
print("HOME =", home)

// System command
let ret int = system("ls -la")
```

---

## 8.8 Program Termination

C offers several ways to terminate a program:

| Function   | Header       | Behavior                           |
|------------|-------------|-------------------------------------|
| `exit(n)`  | `<stdlib.h>` | Clean shutdown, flush buffers       |
| `abort()`  | `<stdlib.h>` | Abnormal termination, no cleanup    |
| `_Exit(n)` | `<stdlib.h>` | Immediate termination, no cleanup   |
| `assert(e)`| `<assert.h>` | Abort if `e` is false (debug only)  |

```c
// C
if (ptr == NULL) {
    fprintf(stderr, "Fatal: out of memory\n");
    exit(EXIT_FAILURE);     // EXIT_FAILURE = 1
}
exit(EXIT_SUCCESS);         // EXIT_SUCCESS = 0
```

Auto provides the same functions with clearer naming:

```auto
if ptr == nil {
    print("Fatal: out of memory")
    exit(1)
}
exit(0)
```

The `assert` macro in C is disabled in release builds (`NDEBUG`). Auto's assertion
mechanism is always active unless explicitly compiled in release mode.

> **Takeaway:** Prefer `exit` over `abort` for normal error conditions — `exit`
> runs cleanup handlers and flushes I/O buffers. Use `abort` only for truly
> unrecoverable errors.

---

## Quick Reference

| Category       | C function                  | Auto equivalent             |
|----------------|-----------------------------|------------------------------|
| Print          | `printf(fmt, ...)`         | `print(...)`                |
| Scan           | `scanf(fmt, ...)`          | `read_line()`               |
| File open      | `fopen(path, mode)`        | `read_file(path)`           |
| File write     | `fprintf(f, fmt, ...)`     | `write_file(path, data)`    |
| String length  | `strlen(s)`                | `len(s)`                    |
| String compare | `strcmp(a, b)`             | `a == b`                    |
| String concat  | `strcat(d, s)`             | `a + b`                     |
| Absolute value | `abs(n)`, `fabs(x)`        | `abs(n)`                    |
| Square root    | `sqrt(x)`                  | `sqrt(x)`                   |
| Power          | `pow(x, y)`                | `pow(x, y)`                 |
| Exit           | `exit(n)`                  | `exit(n)`                   |
| Assert         | `assert(expr)`             | `assert(expr)`              |
| Environment    | `getenv(name)`             | `env(name)`                 |
| System call    | `system(cmd)`              | `system(cmd)`               |
| Current time   | `time(NULL)`               | `time()`                    |
| Error number   | `errno`                    | Error types (Result/Option) |

---

*This completes Level 1 — Acquaintance. You now understand the fundamentals of C
and how Auto maps to them. The next levels will build on this foundation.*
