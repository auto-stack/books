# Getting Started

This chapter adapts "The Little Book of C" for Auto programmers targeting C.
You will learn what C is, why Auto targets it, and how to set up your
development environment for the a2c transpiler pipeline.

## 1. What C Is

C is a general-purpose programming language created in 1972 by Dennis Ritchie
at Bell Labs. It remains one of the most widely used languages in the world.
Operating systems, embedded systems, databases, and language runtimes are all
written in C.

### Why Auto Targets C

Auto's `a2c` transpiler converts Auto source code into C. This gives Auto
programs access to every platform that has a C compiler — which is effectively
every platform. The a2c pipeline:

1. Parse Auto source into an AST.
2. Lower the AST to C, mapping Auto constructs to their C equivalents.
3. Emit `.c` files that compile with any standard C compiler (GCC, Clang, MSVC).

You write clean, high-level Auto. The transpiler produces portable C.

## 2. Installing the Toolchain

To develop Auto programs that compile to C, install two things:

1. **A C compiler** — GCC, Clang, or MSVC.
2. **Auto + a2c** — the Auto toolchain including the a2c transpiler.

### Installing a C Compiler

On Linux, install GCC via your distribution's package manager:

```console
$ sudo apt install build-essential    # Debian/Ubuntu
$ sudo dnf install gcc                # Fedora
```

On macOS, install Xcode's command-line tools:

```console
$ xcode-select --install
```

On Windows, install Visual Studio or the Build Tools, which include MSVC.

### Installing Auto

Download and install Auto from the official site. Verify the installation:

```console
$ auto --version
auto x.y.z (yyyy-mm-dd)
```

## 3. First Program

Every journey begins with Hello World.

<Listing name="hello-world" file="listings/ch00/listing-00-01">

```auto
fn main() {
    print("Hello, world!")
}
```

</Listing>

The a2c transpiler produces this C output:

```c
// Auto → C transpiled by a2c
#include <stdio.h>

int main(void) {
    printf("%s\n", "Hello, world!");
    return 0;
}
```

Key mappings to notice:

- `fn main()` becomes `int main(void)`.
- `print("text")` becomes `printf("%s\n", "text");`.
- An implicit `return 0;` is added at the end of `main`.

## 4. Anatomy of an Auto Program

Compare the Auto and C versions side by side:

```auto
fn main() {
    let name str = "C Learner"
    let age int = 25
    print("Hello,", name)
    print("Age:", age)
}
```

```c
#include <stdio.h>

int main(void) {
    char* name = "C Learner";
    int age = 25;
    printf("%s %s\n", "Hello,", name);
    printf("%s %d\n", "Age:", age);
    return 0;
}
```

<Listing name="first-program" file="listings/ch00/listing-00-02">

```auto
fn main() {
    let name str = "C Learner"
    let age int = 25
    print("Hello,", name)
    print("Age:", age)
}
```

</Listing>

Auto eliminates boilerplate: no `#include`, no semicolons, no explicit
`return 0;`, no format specifiers in `print`.

## 5. Headers and the Preprocessor

In C, you use `#include` to pull in header files and `#define` for macros.
The C preprocessor runs before the compiler and performs text substitution.

Auto does not have a preprocessor. Instead, Auto uses a module system:

- `mod` declares a module.
- `use` imports symbols from another module.
- The a2c transpiler automatically adds the correct `#include` directives.

For example, using `print` in Auto automatically includes `<stdio.h>` in the
generated C.

> **C Only**: C's preprocessor supports conditional compilation (`#ifdef`),
> token pasting (`##`), and variadic macros. Auto has no equivalent — these
> are low-level mechanisms you should rarely need.

## 6. Compiling and Linking

In traditional C development, you run the preprocessor, compiler, assembler,
and linker separately or through a Makefile. With Auto, the workflow is simpler:

```console
$ auto a2c main.at        # Transpile Auto → C
$ auto b                   # Build: transpile + compile + link
```

The `auto a2c` command produces `.c` files. The `auto b` command runs the
full pipeline: transpile, compile with the system C compiler, and link into
an executable.

## 7. Errors and Warnings

Auto provides two layers of error reporting:

1. **Auto compiler errors** — caught before transpilation. These include
   type errors, undefined variables, and syntax issues. Auto's error messages
   point to the exact location in your `.at` source.

2. **C compiler errors** — caught after transpilation, in the generated `.c`
   files. These are rare for well-formed Auto programs, but can occur with
   platform-specific issues.

When you see a C compiler error, the a2c transpiler annotates the generated
C with `// line X: main.at` comments so you can trace it back to your Auto
source.

## 8. The `auto` Command Line

The `auto` CLI provides several commands:

| Command | Purpose |
|---------|---------|
| `auto a2c file.at` | Transpile Auto to C |
| `auto b` | Build project (transpile + compile + link) |
| `auto r` | Build and run |
| `auto t` | Run tests |
| `auto new name` | Create a new project |
| `auto fmt` | Format source files |
| `auto check` | Type-check without generating code |

## 9. Project Structure

A typical Auto project that targets C looks like this:

```
my-project/
├── pac.at           # Package config
├── src/
│   └── main.at      # Entry point
└── out/
    └── main.c       # Generated by a2c
```

The `pac.at` file declares the project name, version, and target language:

```
name: "my-project"
version: "0.1.0"
lang: "c"

app("my-project") {}
```

<Listing name="project-with-pac" file="listings/ch00/listing-00-03">

```auto
fn greet(name str) {
    print("Hello,", name)
}

fn main() {
    greet("C Learner")
    greet("Auto Developer")
}
```

</Listing>

Running `auto b` reads `pac.at`, transpiles all `.at` files to `.c`, compiles
them with the system C compiler, and produces the final executable.

## Quick Reference

| Concept | Auto | C |
|---------|------|---|
| Entry point | `fn main()` | `int main(void)` |
| Print | `print("text")` | `printf("%s\n", "text")` |
| Include | automatic | `#include <stdio.h>` |
| Immutable variable | `let x int = 5` | `const int x = 5;` |
| Mutable variable | `var x int = 5` | `int x = 5;` |
| Build command | `auto b` | `gcc -o out main.c` |
| Package config | `pac.at` | `Makefile` / `CMakeLists.txt` |
| Modules | `mod` / `use` | `#include` |
