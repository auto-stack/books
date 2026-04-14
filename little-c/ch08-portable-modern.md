# Chapter 8: Portable and Modern C

> Sections 81--90
> C code must run everywhere. Auto makes portability the default, not the exception.

C's greatest strength is its portability. The same C code can compile on Linux, macOS,
Windows, and embedded systems. But achieving true portability requires understanding
platform differences -- endianness, word size, threading APIs, and compiler extensions.

Auto generates portable C code by default. The a2c transpiler handles platform-specific
concerns so you can focus on your program's logic. This chapter covers the C portability
landscape and how Auto simplifies it.

---

## 81. C Standards Timeline

C has evolved through several standards, each adding features while maintaining
backwards compatibility:

**C89/C90** -- The foundation. ANSI standardized C in 1989, ISO in 1990. This is
the "classic" C that every compiler supports. Functions must be declared before use,
variables must be declared at the top of a block, and `//` comments are not standard.

**C99** -- Modernized C. Added `//` comments, mixed declarations and code, `<stdint.h>`
for fixed-width integers, variable-length arrays, and designated initializers.

**C11** -- The concurrency update. Added `_Static_assert`, `_Generic`, `<threads.h>`,
atomic operations, and alignment specifiers. This is what Auto targets.

**C17/C23** -- Refinements and new features. C23 adds `typeof`, `constexpr`, `auto`
type inference, and improved attribute syntax.

Auto generates C11-compatible code, which gives broad compiler support while including
modern features like `_Static_assert` and `<stdatomic.h>`.

<Listing id="listing-08-01" title="C standards timeline" path="listings/ch08/listing-08-01" />

---

## 82. Portability and Endianness

Endianness determines how multi-byte values are stored in memory:

- **Little-endian**: Least significant byte first (x86, ARM)
- **Big-endian**: Most significant byte first (some network protocols, older architectures)

```c
/* Detecting endianness in C */
uint32_t val = 1;
if (*(uint8_t *)&val == 1) {
    /* Little-endian */
} else {
    /* Big-endian */
}
```

Network protocols use big-endian (network byte order). C provides `htonl()`, `ntohl()`,
`htons()`, and `ntohs()` for conversion.

Auto handles endianness transparently. When you read or write binary data, Auto
generates the correct byte-order conversions. You write platform-independent code;
a2c adds the platform-specific handling.

---

## 83. Inline Assembly

Inline assembly lets you embed CPU-specific instructions in C code:

```c
/* GCC inline assembly for x86-64 */
static inline uint64_t rdtsc(void) {
    uint32_t lo, hi;
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t)hi << 32) | lo;
}
```

Inline assembly is:
- **Non-portable**: Each CPU architecture has different instructions and syntax
- **Compiler-specific**: GCC, MSVC, and Clang have different inline assembly syntaxes
- **Dangerous**: Wrong constraints can corrupt registers or memory

Auto does not support inline assembly. If you need it, write a C file and call it
via FFI. This keeps the assembly isolated and the rest of your code portable.

---

## 84. Cross-Compilation

Cross-compilation means building for a platform different from the one you are
compiling on:

```bash
# Build for ARM on an x86 machine
$ arm-linux-gnueabihf-gcc -o program program.c

# Build for Windows on Linux
$ x86_64-w64-mingw32-gcc -o program.exe program.c
```

Cross-compilation requires:
- A toolchain for the target platform (compiler, linker, headers, libraries)
- Correct sysroot and library paths
- Platform-specific `#ifdef` guards in your code

Auto simplifies cross-compilation through a2c:

```bash
# Auto cross-compilation (conceptual)
$ auto build --target arm-linux
$ auto build --target windows
```

a2c generates target-appropriate C code and invokes the correct cross-compiler.
You specify the target; Auto handles the rest.

---

## 85. Threading with Pthreads

POSIX Threads (pthreads) is the standard C threading API on Unix-like systems:

```c
#include <pthread.h>

void *worker(void *arg) {
    int id = *(int *)arg;
    printf("Worker %d running\n", id);
    return NULL;
}

int main(void) {
    pthread_t t1, t2;
    int id1 = 1, id2 = 2;
    pthread_create(&t1, NULL, worker, &id1);
    pthread_create(&t2, NULL, worker, &id2);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    return 0;
}
```

Pthreads are verbose: you manage thread creation, joining, mutexes, and condition
variables manually. Windows has its own threading API (`CreateThread`), making
portable threading even harder.

Auto uses a task-based concurrency model instead of raw threads:

```auto
task worker(id int) {
    print("Worker", id, "running")
}
```

Tasks are lightweight units of work that communicate through mailboxes. The runtime
maps tasks to OS threads automatically. No mutexes, no condition variables, no
platform-specific thread APIs.

<Listing id="listing-08-02" title="Threading with pthreads" path="listings/ch08/listing-08-02" />

---

## 86. Atomic Operations

When multiple threads access shared data, you need atomic operations to prevent
data races:

```c
#include <stdatomic.h>

atomic_int counter = ATOMIC_VAR_INIT(0);

/* Thread-safe increment */
atomic_fetch_add(&counter, 1);

/* Thread-safe compare-and-swap */
int expected = 5;
atomic_compare_exchange_strong(&counter, &expected, 10);
```

C11's `<stdatomic.h>` provides atomic types and operations. Common patterns:
- **Atomic increment**: `atomic_fetch_add` for counters
- **Compare-and-swap**: `atomic_compare_exchange_strong` for lock-free algorithms
- **Atomic load/store**: `atomic_load`, `atomic_store` for flags

Auto's task-based model avoids shared mutable state by design. Tasks communicate
through message passing (mailboxes), not shared memory. When you do need shared
state, Auto provides safe abstractions.

---

## 87. FFI: Calling C from Auto

One of Auto's strengths is seamless C interop. You can call any C function
through the Foreign Function Interface (FFI):

```auto
// Declare an external C function
sys extern fn abs(n int) int

fn main() {
    let x int = -42
    let y int = abs(x)
    print("abs(-42) =", y)
}
```

The `sys extern` declaration tells a2c that this function exists in C's standard
library. The transpiler generates a direct C function call -- no wrapper overhead.

FFI rules:
- C types map directly: `int` to `int`, `float` to `float`, `str` to `char*`
- C structs can be declared with `sys extern type`
- C enums map to Auto enums
- Pointer parameters use Auto's reference syntax

This means every C library is automatically available to Auto programs.

<Listing id="listing-08-03" title="FFI: calling C from Auto" path="listings/ch08/listing-08-03" />

---

## 88. Safer Alternatives

C is unsafe by default. But many unsafe patterns have safer alternatives:

| Unsafe C Pattern         | Safer Alternative              | Auto Equivalent          |
|--------------------------|--------------------------------|--------------------------|
| `char*` strings          | `strncpy`, `snprintf`         | `str` type, bounds-safe  |
| `malloc`/`free`          | Arena allocators, pools        | Auto memory management   |
| Raw pointer arithmetic   | Array indexing with bounds     | Bounds-checked arrays    |
| `strcpy`                 | `strncpy` with size limit      | Safe string operations   |
| `sprintf`                | `snprintf`                     | Type-safe `print`        |
| `gets`                   | `fgets`                        | Safe input functions     |
| Unchecked array access   | Manual length tracking         | Length-tracked slices    |

Auto makes the safe option the default. You have to explicitly opt into unsafe
operations using `unsafe` blocks, similar to Rust's approach.

```auto
unsafe {
    // Raw pointer operations go here
    // This block is auditable and isolated
}
```

---

## 89. Modern Style

Modern C (C11+) supports cleaner code style than C89. Auto builds on this with
its own conventions:

**Use `const` everywhere** (C) / Auto variables are immutable by default:

```c
/* C */
const char *const msg = "hello";  /* immutable pointer, immutable data */
```

```auto
// Auto: let is immutable, var is mutable
let msg str = "hello"
```

**Named initializers** for clarity:

```c
struct Point p = {.x = 1, .y = 2};  /* C99 designated initializer */
```

```auto
let p Point = Point(1, 2)  /* Auto: clear and concise */
```

**`_Static_assert` for compile-time checks** (C11):

```c
_Static_assert(sizeof(int) == 4, "int must be 4 bytes");
```

Auto's type system catches most issues at compile time without explicit assertions.

<Listing id="listing-08-04" title="Modern style" path="listings/ch08/listing-08-04" />

---

## 90. Practice: Portable Multithreaded Program

This exercise combines portability and concurrency concepts. The program detects
endianness and demonstrates how Auto handles platform differences.

In C, you would need:
- `#ifdef` guards for different platforms
- Manual byte-order conversion
- pthreads or platform-specific threading APIs
- Conditional compilation for Windows vs Unix

In Auto, these concerns are handled by the toolchain.

<Listing id="listing-08-05" title="Portable multithreaded practice" path="listings/ch08/listing-08-05" />

**Exercises:**

1. Modify listing-08-05 to detect the system's word size (32-bit vs 64-bit).
2. Add a function that converts a 32-bit integer between big-endian and
   little-endian. Test it on the result of `is_little_endian()`.
3. Research: What does `#pragma pack` do? When would you need it?

---

## Quick Reference

| Section | Topic               | C Tool/Approach         | Auto Approach              |
|---------|---------------------|-------------------------|----------------------------|
| 81      | C standards         | C89 through C23         | Targets C11 via a2c        |
| 82      | Endianness          | Manual detection/conversion | Handled by toolchain    |
| 83      | Inline assembly     | `__asm__` blocks        | Not supported; use FFI     |
| 84      | Cross-compilation   | Cross-toolchains        | `auto build --target`      |
| 85      | Threading           | pthreads                | Task/mailbox concurrency   |
| 86      | Atomics             | `<stdatomic.h>`         | Message passing model      |
| 87      | FFI                 | N/A                     | `sys extern` declarations  |
| 88      | Safety              | Manual safer APIs       | Safe by default            |
| 89      | Modern style        | C11 features            | Auto conventions           |
| 90      | Practice            | Platform guards + pthreads | Portable Auto code      |
