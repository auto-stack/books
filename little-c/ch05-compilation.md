# Compilation and Build Process

This chapter covers how Auto code becomes an executable. You will learn the
compilation pipeline, how Auto replaces the C preprocessor, and how `pac.at`
and `auto b` replace Makefiles for multi-file projects.

## 51. Compilation Pipeline

C compilation has four stages:

1. **Preprocessing** — expand `#include`, `#define`, `#ifdef`
2. **Compilation** — convert C source to assembly
3. **Assembly** — convert assembly to object code (`.o` files)
4. **Linking** — combine object files and libraries into an executable

Auto adds a transpilation step before this pipeline:

```
auto.at → [a2c transpiler] → auto.c → [cc compiler] → auto.o → [linker] → auto
```

The `a2c` transpiler converts Auto source to C source. Then a standard C
compiler (gcc, clang, or msvc) takes over.

<Listing name="compilation-pipeline" file="listings/ch05/listing-05-01">

```auto
fn square(n int) int {
    n * n
}

fn main() {
    let result int = square(7)
    print("7 squared =", result)
}
```

</Listing>

Running `auto b` on this file invokes a2c, then cc, then the linker. The
result is a native executable with no runtime dependency on Auto.

## 52. Preprocessor and Macros

C uses the preprocessor for constants and macro functions:

```c
#define PI 3.14159
#define MAX(a, b) ((a) > (b) ? (a) : (b))
```

Macros are text substitution — no type checking, no scoping, and subtle bugs
with multi-evaluation. Auto eliminates the preprocessor entirely:

<Listing name="preprocessor" file="listings/ch05/listing-05-02">

```auto
fn main() {
    // C uses #define PI 3.14159
    // Auto uses let (immutable binding)
    let pi float = 3.14159
    let radius float = 5.0
    let area float = pi * radius * radius
    print("Area:", area)

    // C uses #define MAX(a,b) ((a)>(b)?(a):(b))
    // Auto uses a regular function
    let larger int = max(10, 20)
    print("Max:", larger)
}

fn max(a int, b int) int {
    if a > b { a } else { b }
}
```

</Listing>

Auto's `let` creates immutable bindings (like `const` in C). The `max` function
is type-safe and evaluated once. The compiler may inline it for performance,
giving you macro speed without macro dangers.

## 53. Conditional Compilation

C uses `#ifdef` for platform-specific code:

```c
#ifdef _WIN32
    #include <windows.h>
#else
    #include <unistd.h>
#endif
```

Auto does not have conditional compilation. Instead, use different source files
for different platforms and select the right file at build time through `pac.at`
configuration. This keeps each file complete and readable.

For build-time configuration, Auto supports `comptime` blocks that evaluate
constants during transpilation, but this is an advanced topic beyond this
chapter's scope.

## 54. Inline Functions

C's `inline` keyword suggests the compiler should copy the function body into the
call site:

```c
static inline int square(int x) { return x * x; }
```

Auto does not have an `inline` keyword. The a2c transpiler and the C compiler
collaborate on inlining decisions. Small functions like `max` are automatically
candidates for inlining. You can hint priority with annotations in `pac.at`:

```
optimize: "speed"   // prefer faster code, more inlining
optimize: "size"    // prefer smaller code, less inlining
```

## 55. Makefiles and pac.at

C projects use Makefiles to define build rules:

```makefile
CC = gcc
CFLAGS = -Wall -O2

main: main.o utils.o
	$(CC) $(CFLAGS) -o main main.o utils.o

main.o: main.c
	$(CC) $(CFLAGS) -c main.c
```

Auto replaces Makefiles with `pac.at` — a declarative project file. You declare
what to build, not how to build it:

<Listing name="makefile" file="listings/ch05/listing-05-03">

```auto
fn greet(name str) {
    print("Hello,", name)
}

fn farewell(name str) {
    print("Goodbye,", name)
}

fn main() {
    greet("World")
    farewell("World")
}
```

</Listing>

The `pac.at` file lists the app and its dependencies. Running `auto b` reads
`pac.at`, transpiles all `.at` files to `.c`, compiles them, and links the
result. No rules to write, no timestamps to track.

## 56. Multi-File Projects

C splits code across `.c` and `.h` files. Header files declare types and
functions; source files define them. You must keep headers and sources in sync.

Auto uses `mod` and `use` to organize code without headers:

<Listing name="multi-file" file="listings/ch05/listing-05-04">

```auto
// math_utils.at
// mod math_utils

fn add(a int, b int) int {
    a + b
}

fn multiply(a int, b int) int {
    a * b
}

// main.at
// use math_utils

fn main() {
    let sum int = add(3, 4)
    let product int = multiply(3, 4)
    print("Sum:", sum)
    print("Product:", product)
}
```

</Listing>

The `mod math_utils` declaration creates a module. The `use math_utils`
declaration imports it. The a2c transpiler generates the corresponding `.h` and
`.c` files automatically, keeping declarations and definitions always in sync.

## 57. Static and Shared Libraries

C builds libraries as archives (`.a` static) or shared objects (`.so` / `.dll`):

```bash
ar rcs libmath.a math.o       # static library
gcc -shared -o libmath.so math.o  # shared library
```

Auto's `auto b` command handles library creation through `pac.at` configuration:

```
lib("math_utils") {
    src: ["math_utils.at"]
    type: "static"    # or "shared"
}
```

When you declare a library in `pac.at`, `auto b` transpiles the Auto sources,
compiles them, and archives them. Other modules link against the library by
listing it as a dependency. You never run `ar` or `ld` manually.

## 58. Compiler Flags

C projects pass flags to the compiler:

```bash
gcc -Wall -Wextra -O2 -std=c11 -o program main.c
```

Auto sets sensible defaults in `pac.at`:

| Flag | Purpose | Auto Default |
|------|---------|-------------|
| `-Wall -Wextra` | Enable warnings | Yes |
| `-O2` | Optimization level | Yes |
| `-std=c11` | C standard | C11 |
| `-g` | Debug symbols | Debug builds |
| `-DNDEBUG` | Disable asserts | Release builds |

Override defaults in `pac.at`:

```
app("myapp") {
    cflags: ["-O3", "-march=native"]
}
```

## 59. Object Files

Each `.c` file compiles to an object file (`.o` on Linux/macOS, `.obj` on
Windows). Object files contain machine code with unresolved symbols. The linker
resolves symbols by combining object files.

When `auto b` runs on a multi-file project:

```
math_utils.at → math_utils.c → math_utils.o ─┐
                                               ├→ linker → myapp
main.at       → main.c       → main.o       ─┘
```

Each Auto source file produces exactly one `.c` file, which produces one `.o`
file. The linker combines them into the final executable. Understanding this
flow helps debug linking errors like "undefined reference to `foo`" — it means
the linker cannot find the object file that defines `foo`.

## 60. Practice: Build a Multi-File Project

Build a small project with a counter module and a main program. This exercise
covers module creation, the build process, and linking.

<Listing name="libraries" file="listings/ch05/listing-05-05">

```auto
type Counter {
    count int
}

fn Counter.new() Counter {
    Counter(0)
}

fn Counter.increment(c Counter) {
    c.count = c.count + 1
}

fn Counter.value(c Counter) int {
    c.count
}

fn main() {
    var c Counter = Counter.new()
    c.increment(c)
    c.increment(c)
    c.increment(c)
    print("Count:", c.value(c))
}
```

</Listing>

Try this: split the `Counter` type into its own file `counter.at` with
`mod counter`, create a `pac.at` that lists both files, and run `auto b` to
build the project. Verify that a2c generates `counter.h`, `counter.c`,
`main.c`, and links them correctly.

## Quick Reference

| Concept | Auto | C |
|---------|------|---|
| Transpile | `a2c main.at` | N/A |
| Build | `auto b` | `make` |
| Project file | `pac.at` | `Makefile` |
| Constant | `let pi float = 3.14` | `#define PI 3.14` |
| Macro function | `fn max(a, b) int` | `#define MAX(a,b) ...` |
| Conditional | separate source files | `#ifdef` |
| Module declare | `mod math_utils` | `math_utils.h` + `math_utils.c` |
| Module import | `use math_utils` | `#include "math_utils.h"` |
| Static library | `lib("name") { type: "static" }` | `ar rcs libname.a` |
| Shared library | `lib("name") { type: "shared" }` | `gcc -shared` |
| Compiler flags | `pac.at` cflags field | `CFLAGS` in Makefile |
| Optimization | `optimize: "speed"` | `-O2` / `-O3` |
