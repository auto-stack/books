# Chapter 16: Performance

> Level 3 — Experience
>
> Inline functions, restrict qualifiers, and measurement -- squeezing every
> cycle out of C, and how Auto handles optimization for you.

Performance matters. Not for every program, and not at every moment, but when
it matters, C programmers need to understand how to write fast code and how to
prove that their code is fast. C gives you fine-grained control over
performance through keywords like `inline` and `restrict`, through compiler
attributes, and through careful measurement. Auto takes a different approach:
the compiler handles most optimizations, and you focus on writing clear code.

---

## 16.1 Inline Functions

The C `inline` keyword suggests to the compiler that a function's body should
be substituted directly at the call site, avoiding the overhead of a function
call:

```c
// C Deep Dive: inline functions
static inline int square(int n) {
    return n * n;
}

static inline int max(int a, int b) {
    return (a > b) ? a : b;
}
```

The rules for `inline` in C are subtle and frequently misunderstood:

- `inline` alone does **not** guarantee inlining -- it is a hint.
- An `inline` function defined in a header needs a corresponding external
  definition in exactly one translation unit, or the program has undefined
  behavior (C99/C11).
- `static inline` is the practical solution: each TU gets its own copy, and
  the linker sees no duplicate symbols.
- Compilers are free to ignore `inline` entirely. Modern compilers often
  inline functions that are not marked `inline` and refuse to inline functions
  that are.

> **C Deep Dive:** The interaction between `inline` and linkage in C is one of
> the most confusing aspects of the language. C99 introduced `inline` with
> external linkage semantics that differ from C++. In practice, most C
> programmers use `static inline` in headers and avoid the complexity. C23
> simplifies this by making `inline` behave more like C++.

**Auto's approach.** Auto does not have an `inline` keyword. The compiler
decides inlining automatically based on heuristics:

- Small functions are always inlined.
- Functions called in hot loops are candidates for inlining.
- The programmer can annotate performance-critical functions, but the compiler
  makes the final decision.

```auto
// Auto: no inline keyword needed
fn square(n int) int {
    n * n
}

fn max(a int, b int) int {
    if a > b { a } else { b }
}

fn main() {
    print("square(7) =", square(7))
    print("max(3, 7) =", max(3, 7))
}
```

<Listing path="listings/ch16/listing-16-01" title="Inline functions" />

---

## 16.2 restrict Qualifiers

The `restrict` qualifier tells the compiler that a pointer is the only way to
access the object it points to. This enables optimizations that would
otherwise be impossible:

```c
// C Deep Dive: restrict qualifier
void vector_add(double *restrict result,
                const double *restrict a,
                const double *restrict b,
                int n) {
    for (int i = 0; i < n; i++) {
        result[i] = a[i] + b[i];
    }
}
```

Without `restrict`, the compiler must assume that `result`, `a`, and `b` might
overlap. With `restrict`, it knows they do not, so it can:

- Vectorize the loop (use SIMD instructions).
- Reorder loads and stores.
- Keep values in registers longer.

Getting `restrict` wrong is undefined behavior:

```c
// C Deep Dive: restrict violation
int arr[10] = {0};
void add(int *restrict a, int *restrict b) {
    *a += *b;
}
add(arr + 0, arr + 0);  // UB: a and b alias the same array
```

> **C Deep Dive:** The `restrict` semantics in C are defined in terms of
> "based on" relationships between pointers and their underlying objects.
> The formal definition in the C standard is notoriously difficult to
> understand. In practice, `restrict` means "I promise these pointers don't
> alias." If you break that promise, anything can happen.

**Auto's approach.** Auto does not expose `restrict`. The compiler performs
alias analysis automatically. When the compiler can prove that two references
do not alias, it applies the same optimizations as `restrict`. When it cannot
prove it, it generates safe code.

> **C Deep Dive:** Many C standard library functions use `restrict`:
> `memcpy`, `strcpy`, `printf`, and most string functions. The `restrict`
> qualifier on `memcpy` is what distinguishes it from `memmove` -- `memcpy`
> requires non-overlapping regions, `memmove` handles overlap. Getting this
> wrong is a classic source of subtle bugs.

---

## 16.3 Unsequenced and Reproducible Attributes

C23 introduces two new function attributes for optimization hints:

**`[[unsequenced]]`**: The function's result depends only on its arguments and
has no side effects. The compiler may cache results or reorder calls.

```c
// C Deep Dive: [[unsequenced]] attribute
[[unsequenced]] double square(double x) {
    return x * x;
}
// Compiler can compute square(5) at compile time
// and reuse the result for repeated calls with same argument
```

**`[[reproducible]]`**: The function always returns the same result for the
same arguments, but may have side effects (like logging).

```c
// C Deep Dive: [[reproducible]] attribute
[[reproducible]] int lookup(const int *table, int index) {
    return table[index];  // same table, same index -> same result
}
```

| Attribute           | Pure?  | Side effects? | Cacheable? |
|---------------------|--------|---------------|------------|
| `[[unsequenced]]`   | Yes    | No            | Yes        |
| `[[reproducible]]`  | Yes    | May have      | Limited    |

These attributes are promises from the programmer to the compiler. Violating
them is undefined behavior.

> **C Deep Dive:** These attributes are C's answer to GCC's `__attribute__((const))`
> and `__attribute__((pure))`. They serve similar purposes: telling the
> compiler that a function is safe to optimize. The C23 versions have clearer
> semantics and are standardized.

**Auto's approach.** Auto's compiler performs purity analysis automatically.
Functions that do not access global state and have no side effects are treated
as pure. The programmer does not need to annotate functions with attributes.

---

## 16.4 Measurement and Inspection

Before optimizing, you must measure. C provides `clock()` from `<time.h>` for
basic timing:

```c
// C Deep Dive: performance measurement
#include <time.h>
#include <stdio.h>

int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main(void) {
    clock_t start = clock();
    int result = fibonacci(35);
    clock_t end = clock();

    double elapsed = (double)(end - start) / CLOCKS_PER_SEC;
    printf("fib(35) = %d\n", result);
    printf("Time: %.3f seconds\n", elapsed);
    return 0;
}
```

Problems with `clock()`:

- Measures CPU time, not wall clock time.
- Resolution is implementation-defined -- may be too coarse for microbenchmarks.
- Does not separate user time from system time.
- `CLOCKS_PER_SEC` varies across platforms.

For serious profiling, C programmers use external tools:

| Tool          | Purpose                          |
|---------------|----------------------------------|
| `perf`        | Linux performance counters       |
| `gprof`       | Call graph profiling             |
| `Valgrind`    | Memory and cache analysis        |
| `Instruments` | macOS profiling                  |
| `VTune`       | Intel hardware profiling         |

> **C Deep Dive:** The golden rule of optimization: measure, don't guess.
> Programmers are notoriously bad at predicting where time is spent.
> Profiling consistently shows that 80% of execution time is in 20% of the
> code. Profile first, optimize second, measure again third.

<Listing path="listings/ch16/listing-16-02" title="Performance measurement" />

**Auto's approach.** Auto provides built-in benchmarking tools. The `auto bench`
command measures execution time without manual `clock()` calls:

```auto
// Auto: built-in benchmarking
fn fibonacci(n int) int {
    if n <= 1 { return n }
    fibonacci(n - 1) + fibonacci(n - 2)
}

fn main() {
    let n int = 35
    print("Computing fib(" + str(n) + ")...")
    let result int = fibonacci(n)
    print("Result:", result)
    print("Use 'auto bench' for precise timing")
}
```

Auto's tooling integrates profiling into the development workflow. You do not
need to modify your code to measure it.

---

## Quick Reference

| Concept                | C mechanism                  | Auto mechanism             |
|------------------------|------------------------------|----------------------------|
| Function inlining      | `inline` keyword             | Automatic                  |
| Header placement       | `static inline` in headers   | Not needed                 |
| Pointer aliasing       | `restrict` qualifier         | Automatic alias analysis   |
| Pure functions         | `[[unsequenced]]` attribute  | Automatic purity analysis  |
| Reproducible functions | `[[reproducible]]` attribute | Automatic analysis         |
| Timing                 | `clock()`, external profilers| `auto bench` command       |
| Optimization hints     | Manual annotations           | Compiler-driven            |

---

*Performance is the reason C exists. But manual optimization hints are a
burden that modern compilers can shoulder automatically. Auto takes that burden
off the programmer while delivering comparable performance through intelligent
compilation.*
