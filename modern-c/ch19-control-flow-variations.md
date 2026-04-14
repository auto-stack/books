# Chapter 19: Variations in Control Flow

> Level 3 -- Experience
>
> Non-local jumps, signals, and structured error handling -- understanding C's
> control flow escape hatches and how Auto replaces them with safer patterns.

Programs don't always follow a straight-line path. Functions return early, loops
break out, errors propagate through call stacks. C provides several mechanisms
for non-standard control flow: `goto`, `setjmp`/`longjmp`, and signal handlers.
These are powerful but dangerous. Auto replaces most of them with structured
alternatives.

---

## 19.1 A Detailed Example

Consider a parser that must handle errors at multiple levels:

```c
// C Deep Dive: error handling with goto
#include <stdio.h>
#include <stdlib.h>

int parse_input(const char *input) {
    if (!input) goto error_null;
    if (*input == '\0') goto error_empty;

    int value = atoi(input);
    if (value <= 0) goto error_negative;

    printf("Parsed: %d\n", value);
    return value;

error_null:
    fprintf(stderr, "Error: null input\n");
    return -1;
error_empty:
    fprintf(stderr, "Error: empty input\n");
    return -2;
error_negative:
    fprintf(stderr, "Error: non-positive value\n");
    return -3;
}
```

C programmers use `goto` for centralized error cleanup. It is one of the few
accepted uses of `goto` in C. The pattern is: jump to a label that releases
resources and reports the error.

**Auto's approach.** Auto uses Result types for error propagation:

```auto
// Auto: Result type for structured error handling
type ParseResult {
    value int
    ok bool
    error str
}

fn ParseResult.ok(val int) ParseResult {
    ParseResult(val, true, "")
}

fn ParseResult.err(msg str) ParseResult {
    ParseResult(0, false, msg)
}

fn parse_input(input str) ParseResult {
    if input == "" {
        return ParseResult.err("empty input")
    }
    let value int = int(input)
    if value <= 0 {
        return ParseResult.err("non-positive value")
    }
    ParseResult.ok(value)
}
```

<Listing path="listings/ch19/listing-19-01" title="setjmp/longjmp to error handling" />

---

## 19.2 Sequencing

The comma operator in C evaluates operands left-to-right and yields the last
value:

```c
// C Deep Dive: comma operator
int x = (1, 2, 3);     // x == 3
int y = (printf("a"), printf("b"), 42);  // prints "ab", y == 42

// Common use: for-loop with multiple increments
for (int i = 0, j = 10; i < j; i++, j--) {
    printf("i=%d j=%d\n", i, j);
}
```

The comma operator is a sequencing point. The left operand is fully evaluated
before the right operand begins. However, the comma that separates function
arguments is **not** the comma operator -- it is punctuation.

> **C Deep Dive:** Evaluation order of function arguments is unspecified in C.
> `f(a(), b())` may call `a()` or `b()` first. This is different from the comma
> operator, which guarantees left-to-right evaluation. Mixing these two concepts
> is a common source of bugs.

**Auto's approach.** Auto does not have a comma operator. The `for` loop uses
range syntax, and function arguments are evaluated in a defined order:

```auto
// Auto: no comma operator needed
fn main() {
    for i in 0..10 {
        print(i)
    }
}
```

This is a **C-only** feature. Auto's design eliminates the ambiguity.

---

## 19.3 Short Jumps

C provides several mechanisms for short-range control flow transfer:

```c
// C Deep Dive: short jumps
for (int i = 0; i < 100; i++) {
    if (i == 5) continue;    // skip to next iteration
    if (i == 10) break;      // exit loop
    printf("%d ", i);
}
// Output: 0 1 2 3 4 6 7 8 9
```

The `goto` statement transfers control to a labeled statement within the same
function:

```c
// C Deep Dive: goto for cleanup
#include <stdio.h>
#include <stdlib.h>

int process(void) {
    FILE *f = fopen("data.txt", "r");
    if (!f) goto cleanup_none;

    char *buf = malloc(1024);
    if (!buf) goto cleanup_file;

    // ... work with f and buf ...

    free(buf);
    fclose(f);
    return 0;

cleanup_file:
    fclose(f);
cleanup_none:
    return -1;
}
```

> **C Deep Dive:** `goto` cannot jump across function boundaries. It cannot jump
> past variable-length array declarations. It cannot jump into the body of a
> selection or iteration statement from outside. Despite these restrictions,
> `goto` is widely used in C for error handling and resource cleanup.

**Auto's approach.** Auto has `break` and `continue` but no `goto`. Resource
cleanup uses defer (planned) or Result types:

```auto
// Auto: structured control flow
fn process() int {
    for i in 0..100 {
        if i == 5 {
            continue
        }
        if i == 10 {
            break
        }
        print(i)
    }
    0
}
```

> **C Deep Dive:** The absence of `goto` in Auto is deliberate. Every use of
> `goto` in C can be replaced with structured constructs: `break`, `continue`,
> early returns, or Result types. This makes control flow explicit and easier
> to reason about.

---

## 19.4 Functions

Normal function calls and returns are the most common control flow mechanism:

```c
// C Deep Dive: function returns
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// Tail call optimization (compiler-dependent)
int sum_to(int n, int acc) {
    if (n == 0) return acc;
    return sum_to(n - 1, acc + n);  // may be optimized as tail call
}
```

Functions return to their caller. The call stack records return addresses and
local variables. Deep recursion can overflow the stack.

**Auto's approach.** Auto functions work identically:

```auto
// Auto: functions and returns
fn factorial(n int) int {
    if n <= 1 {
        return 1
    }
    n * factorial(n - 1)
}

fn main() {
    print("5! =", factorial(5))
}
```

No special handling needed -- this is standard control flow.

---

## 19.5 Long Jumps

`setjmp` and `longjmp` provide non-local jumps across function boundaries:

```c
// C Deep Dive: setjmp/longjmp
#include <stdio.h>
#include <setjmp.h>

jmp_buf error_handler;

void inner_function(int value) {
    if (value < 0) {
        longjmp(error_handler, 1);  // jump back to setjmp
    }
    printf("Value: %d\n", value);
}

int main(void) {
    int status = setjmp(error_handler);
    if (status == 0) {
        inner_function(42);    // normal path
        inner_function(-1);    // triggers longjmp
        inner_function(99);    // never reached
    } else {
        printf("Caught error: %d\n", status);
    }
    return 0;
}
```

`setjmp` saves the execution context. `longjmp` restores it, causing `setjmp`
to return again with a non-zero value. This is C's closest equivalent to
exception handling.

> **C Deep Dive:** `longjmp` does not call destructors or cleanup functions. Any
> variables that were modified between `setjmp` and `longjmp` have indeterminate
> values unless they are `volatile`. This makes `longjmp` extremely dangerous
> in complex code. It bypasses the normal function call/return mechanism entirely.

**Auto's approach.** Auto uses Result types (like Rust's `Result<T, E>`) for
error propagation instead of non-local jumps:

```auto
// Auto: Result types replace setjmp/longjmp
type Result {
    value int
    ok bool
    error str
}

fn Result.ok(val int) Result {
    ParseResult(val, true, "")
}

fn inner_function(value int) Result {
    if value < 0 {
        return Result.err("negative value")
    }
    print("Value:", value)
    Result.ok(value)
}
```

The error is returned through the call stack explicitly. No hidden control flow.
No `volatile` needed. Every function signature declares whether it can fail.

> **C Deep Dive:** C's `setjmp`/`longjmp` is the only standard mechanism for
> non-local error propagation. POSIX has `sigsetjmp`/`siglongjmp` which also
> saves and restores the signal mask. Some C compilers (GNU, Clang) support
> `__attribute__((cleanup))` for automatic resource cleanup, but this is
> non-standard.

---

## 19.6 Signal Handlers

Signals are asynchronous notifications sent to a process:

```c
// C Deep Dive: signal handlers
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>

void handle_sigint(int sig) {
    printf("Caught SIGINT (Ctrl+C)\n");
    exit(0);
}

void handle_sigsegv(int sig) {
    printf("Segmentation fault!\n");
    _exit(1);  // _exit, not exit -- unsafe to call most functions
}

int main(void) {
    signal(SIGINT, handle_sigint);
    signal(SIGSEGV, handle_sigsegv);

    while (1) {}  // run forever until Ctrl+C
    return 0;
}
```

> **C Deep Dive:** Signal handlers are severely restricted. You can only safely
> call async-signal-safe functions (listed in POSIX). `printf`, `malloc`, and
> most standard library functions are **not** async-signal-safe. Writing to a
> `volatile sig_atomic_t` variable is the only portable way to communicate
> between a signal handler and the main program. The `sigaction()` function
> (POSIX) provides more control than `signal()`.

This is **C-only** territory. Auto does not expose signal handlers directly.
Systems programming with signals should be done in C and exposed through an
Auto `sys` module.

```auto
// Auto: signal handling via sys module (conceptual)
// fn main() {
//     sys.on_interrupt(fn() {
//         print("Interrupted")
//         sys.exit(0)
//     })
// }
```

---

## Quick Reference

| Concept           | C mechanism                | Auto mechanism              |
|-------------------|----------------------------|-----------------------------|
| Error cleanup     | `goto` labels              | Result types, early return  |
| Sequencing        | Comma operator             | Not needed                  |
| Loop control      | `break`, `continue`        | `break`, `continue`         |
| Short jumps       | `goto`                     | Not supported               |
| Error propagation | `setjmp`/`longjmp`         | Result types                |
| Async signals     | `signal()`, `sigaction()`  | `sys` module (planned)      |

---

*C's control flow escape hatches exist because C lacks structured error handling.
Auto replaces `goto`, `setjmp`/`longjmp`, and ad-hoc error codes with Result
types and explicit error propagation -- making control flow visible and safe.*
