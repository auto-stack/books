# Chapter 15: Program Failure

> Level 2 — Cognition
>
> Undefined behavior, error codes, signals -- how things go wrong in C
> and how Auto prevents them.

Programs fail. The question is not whether failure will occur, but how the
language helps you prevent, detect, and recover from it. C's approach to
failure is minimal: the language assumes the programmer is always right and
provides few safety nets. Auto takes the opposite approach -- the language
helps the programmer avoid failure through compile-time checks and runtime
safety.

---

## 15.1 Wrongdoings

C classifies program misbehavior into several categories. The most dangerous
is **undefined behavior** (UB):

> Undefined behavior: behavior for which the standard imposes no requirements.

UB means the compiler is allowed to do literally anything. Common examples:

```c
// C Deep Dive: undefined behavior
int arr[5];
arr[10] = 42;           // UB: out-of-bounds access

int *p = NULL;
*p = 42;                // UB: null pointer dereference

int x;
printf("%d\n", x);      // UB: reading uninitialized variable

int a = INT_MAX;
int b = a + 1;          // UB: signed integer overflow

free(p);
*p = 42;                // UB: use after free
```

What actually happens with UB in practice:

| Scenario            | Possible consequence             |
|---------------------|-----------------------------------|
| Buffer overflow     | Silent data corruption            |
| Null dereference    | Segmentation fault (crash)        |
| Use after free      | Arbitrary code execution          |
| Integer overflow    | Incorrect results                 |
| Type confusion      | Data corruption, security hole    |

Compilers exploit UB for optimization. If the standard says the behavior is
undefined, the compiler may assume it never happens:

```c
// C Deep Dive: compiler exploits UB
int *check(int *p) {
    int x = *p;        // dereference p
    if (p == NULL) {   // compiler removes this: if p were NULL,
        return NULL;   // the dereference above would be UB,
    }                   // and UB "doesn't happen"
    return p;
}
```

**How Auto prevents UB.** Auto eliminates entire categories of UB through:

- **Bounds checking**: array accesses are validated at compile time where
  possible, runtime where necessary.
- **Null safety**: there are no null pointers in Auto. Optional values use
  explicit `Option` types.
- **Initialization enforcement**: every variable must be initialized.
- **No pointer arithmetic**: array indexing replaces all pointer arithmetic.
- **Overflow detection**: integer overflow is caught at runtime.

```auto
// Auto: UB prevention
fn safe_divide(a int, b int) int {
    if b == 0 {
        print("Error: division by zero")
        return 0
    }
    a / b
}

fn safe_access(arr [5]int, index int) int {
    if index < 0 || index >= 5 {
        print("Error: index out of bounds")
        return 0
    }
    arr[index]
}
```

<Listing path="listings/ch15/listing-15-01" title="Error handling" />

> **C Deep Dive:** Approximately 60% of CVEs (Common Vulnerabilities and
> Exposures) in C/C++ code are caused by memory safety violations that are
> undefined behavior. This is the primary motivation for languages like Rust,
> Swift, and Auto.

---

## 15.2 Program State Degradation

C distinguishes between several levels of unspecified behavior:

**Implementation-defined behavior**: the compiler must document what it does.

```c
// C Deep Dive: implementation-defined
int x = -1;
int y = x >> 1;   // arithmetic or logical shift?
// Implementation-defined: may be -1 (arithmetic) or INT_MAX (logical)
```

**Unspecified behavior**: the standard allows multiple valid outcomes.

```c
// C Deep Dive: unspecified behavior
int f(void) { printf("f\n"); return 1; }
int g(void) { printf("g\n"); return 2; }
int result = f() + g();   // may print "f g" or "g f"
// Evaluation order of operands is unspecified
```

**Locale-specific behavior**: depends on the runtime locale.

```c
// C Deep Dive: locale-specific
printf("%d\n", isalpha(0xE9));  // depends on locale: e with acute?
```

These are not as dangerous as UB, but they make programs behave differently
across compilers, platforms, and configurations -- a portability nightmare.

**Auto's approach.** Auto specifies evaluation order (left to right),
provides platform-independent integer semantics, and uses UTF-8 universally.
Programs behave the same way on every platform:

```auto
// Auto: deterministic behavior
fn f() int { print("f"); 1 }
fn g() int { print("g"); 2 }
fn main() {
    let result int = f() + g()   // always prints "f" then "g"
    print("Result:", result)
}
```

> **C Deep Dive:** The unspecified evaluation order in C is a frequent source
> of subtle bugs. Code like `a[i] = i++` is UB (modifying and reading `i`
> without a sequence point). Even `printf("%d %d", i++, i)` is UB. Auto
> eliminates sequence-point concerns entirely by having clear evaluation order.

---

## 15.3 Unfortunate Incidents

Runtime errors occur when the program encounters an unexpected condition:

```c
// C Deep Dive: runtime errors
int *p = malloc(1000000000000);  // may return NULL
int x = 1 / 0;                   // floating-point exception (signal)
int arr[3]; arr[10];             // may or may not crash (UB)

// Stack overflow
void recurse(void) { recurse(); }  // infinite recursion -> crash
```

C handles these through **signals** -- asynchronous notifications from the
operating system:

```c
// C Deep Dive: signals
#include <signal.h>

void handler(int sig) {
    if (sig == SIGSEGV) {
        fprintf(stderr, "Segmentation fault\n");
        _exit(1);
    }
}

int main(void) {
    signal(SIGSEGV, handler);
    // ...
}
```

Standard signals:

| Signal     | Cause                        | Default action |
|-----------|------------------------------|----------------|
| `SIGABRT` | `abort()` called             | Terminate      |
| `SIGFPE`  | Arithmetic error             | Terminate      |
| `SIGILL`  | Illegal instruction          | Terminate      |
| `SIGINT`  | Ctrl+C from terminal         | Terminate      |
| `SIGSEGV` | Invalid memory access        | Terminate      |
| `SIGTERM` | Termination request          | Terminate      |

Signal handling in C is extremely limited. Only async-signal-safe functions
may be called from signal handlers. `printf`, `malloc`, and most library
functions are not async-signal-safe.

**Auto's approach.** Auto avoids signals by preventing their triggers:

- No null pointers means no `SIGSEGV` from null dereference.
- Bounds checking means no `SIGSEGV` from buffer overflow.
- Runtime checks catch division by zero before the hardware exception.

> **C Deep Dive:** Writing a correct signal handler is one of the hardest
> tasks in C programming. The signal may arrive at any point, even mid-
> instruction. Most "signal handlers" in production code are technically
> undefined behavior. The safest approach is to set a `volatile sig_atomic_t`
> flag and check it in the main loop.

---

## 15.4 Series of Unfortunate Events

Failures in C tend to cascade. A small error propagates through the program,
causing increasingly severe symptoms:

```c
// C Deep Dive: cascading failure
char* read_file(const char *path) {
    FILE *f = fopen(path, "r");    // may return NULL
    // forgot to check!
    char *buf = malloc(1024);      // may return NULL
    // forgot to check!
    fgets(buf, 1024, f);           // UB if f is NULL
    return buf;                    // caller must free -- will they?
}

void process(void) {
    char *data = read_file("input.txt");  // may be NULL
    int len = strlen(data);               // UB if data is NULL
    printf("Length: %d\n", len);
    // forgot to free(data)! memory leak
}
```

Each missing error check compounds. In real code, this leads to:

1. A NULL pointer propagates silently through several functions.
2. Eventually it is dereferenced, causing a crash far from the root cause.
3. The crash report shows the symptom, not the cause.
4. Debugging requires tracing back through the call chain.

**Auto's approach: fail fast, fail clearly.** Auto's philosophy is to detect
errors as early as possible and make them impossible to ignore:

```auto
// Auto: explicit error handling
type Result {
    value int
    ok bool
}

fn Result.ok(val int) Result {
    Result(val, true)
}

fn Result.err() Result {
    Result(0, false)
}

fn process(data int) Result {
    if data < 0 {
        print("Invalid input:", data)
        return Result.err()
    }
    Result.ok(data * 2)
}
```

<Listing path="listings/ch15/listing-15-02" title="Error checking and cleanup" />

> **C Deep Dive:** Studies of production C code show that error handling code
> often contains more bugs than the happy path. The reason is simple: error
> paths are rarely tested, and the manual `if (error) goto cleanup` pattern
> is tedious and error-prone. Auto's `Result` type forces the programmer to
> handle errors at every call site.

---

## 15.5 Dealing with Failures

C's primary error reporting mechanism is **error codes**:

```c
// C Deep Dive: error codes
#include <errno.h>

errno = 0;
FILE *f = fopen("missing.txt", "r");
if (f == NULL) {
    // errno is set by fopen
    fprintf(stderr, "Error %d: %s\n", errno, strerror(errno));
}
```

Problems with `errno`:

- **Not set to zero by successful calls**: must clear `errno` before calling
  a function to detect errors reliably.
- **Global state**: not thread-safe in older C standards. C11 added
  thread-local storage, and `errno` is now typically thread-local.
- **Single value**: only one error at a time; nested calls overwrite it.
- **No type safety**: any `int` value is a valid errno.

The `perror` function provides a convenient error message:

```c
// C Deep Dive: perror
FILE *f = fopen("config.txt", "r");
if (!f) {
    perror("fopen");    // prints "fopen: No such file or directory"
    return 1;
}
```

**Auto's approach: `Result` type.** Auto uses a `Result` type (similar to
Rust's `Result` and Zig's error unions) for fallible operations:

```auto
// Auto: Result type for error handling
type Result {
    value int
    ok bool
}

fn Result.ok(val int) Result {
    Result(val, true)
}

fn Result.err() Result {
    Result(0, false)
}
```

The caller must check the `ok` field before using the `value`. Ignoring the
result of a fallible function is a compile-time warning.

> **C Deep Dive:** Go uses multiple return values `(value, error)` for error
> handling. Rust uses `Result<T, E>` with the `?` operator. Zig uses error
> unions with `try`. C uses `errno` and return codes. Each approach has
> tradeoffs. Auto's `Result` type draws from the best of these designs.

---

## 15.6 Error Checking and Cleanup

C's resource cleanup is manual and error-prone. The standard pattern uses
`goto` for centralized cleanup:

```c
// C Deep Dive: cleanup with goto
int process_file(const char *path) {
    FILE *f = NULL;
    char *buf = NULL;
    int result = -1;

    f = fopen(path, "r");
    if (!f) goto cleanup;

    buf = malloc(4096);
    if (!buf) goto cleanup;

    if (!fgets(buf, 4096, f)) goto cleanup;

    // process buf...
    result = 0;

cleanup:
    if (buf) free(buf);
    if (f) fclose(f);
    return result;
}
```

This pattern is so common that it appears in the Linux kernel, PostgreSQL,
and most large C codebases. It works, but it is fragile:

- Forgetting to free a resource in the cleanup block leaks it.
- Adding a new resource requires updating all cleanup code.
- The `goto` must jump forward only; backward jumps create loops.
- Resources must be freed in reverse order of acquisition.

Some C compilers support cleanup attributes:

```c
// C Deep Dive: automatic cleanup (GCC/Clang extension)
void cleanup_file(FILE **f) { if (*f) fclose(*f); }

int read_data(void) {
    FILE *f __attribute__((cleanup(cleanup_file))) = fopen("data.txt", "r");
    if (!f) return -1;
    // f is automatically closed when scope ends
    return 0;
}
```

**Auto's approach: automatic cleanup.** Auto manages resource cleanup
automatically through its storage model. Resources are released when they go
out of scope. The programmer never writes cleanup code:

```auto
// Auto: automatic cleanup, no goto needed
fn process(data int) Result {
    if data < 0 {
        print("Invalid input:", data)
        return Result.err()
    }
    Result.ok(data * 2)
}

fn main() {
    let r1 Result = process(21)
    if r1.ok {
        print("Success:", r1.value)
    }

    let r2 Result = process(-5)
    if !r2.ok {
        print("Processing failed")
    }
}
```

> **C Deep Dive:** The `defer` statement, popularized by Go and adopted by
> Zig, is a modern solution to the cleanup problem. It schedules a cleanup
> action to run when the function returns. C2x considered but did not add
> `defer`. Auto's automatic storage management achieves the same result
> without requiring explicit `defer` statements.

---

## Quick Reference

| Concept              | C mechanism                | Auto mechanism            |
|----------------------|----------------------------|---------------------------|
| Undefined behavior   | "Programmer is always right" | Prevented by design     |
| Buffer overflow      | UB, often exploited        | Bounds checking           |
| Null dereference     | UB, crash or exploit       | No null pointers          |
| Uninitialized read   | UB, garbage value          | Mandatory initialization  |
| Integer overflow     | UB (signed)                | Runtime detection         |
| Error reporting      | `errno`, return codes      | `Result` type             |
| Error checking       | Manual `if` checks         | `Result.ok` field         |
| Resource cleanup     | `goto cleanup` or RAII     | Automatic                 |
| Signal handling      | `signal()`, limited        | Prevented at source       |
| Cascading failure    | Common                     | Contained by type system  |

---

*This completes Level 2 -- Cognition. You now understand how C programs fail
and how Auto's design prevents the most common failure modes. The transition
from Level 2 to Level 3 marks the shift from understanding C's internals to
building real programs with Auto's abstractions.*
