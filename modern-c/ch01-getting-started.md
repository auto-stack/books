# Getting Started

This chapter gets you running. We start with the first program from *Modern C*, adapted to Auto, and then walk through how to compile and execute it in both languages.

## 1.1 Imperative Programming

C is an imperative language. You write sequences of statements that the computer executes in order: assign a value, compute a result, print output, repeat. There is no magic -- the program does exactly what you tell it, step by step.

Auto is imperative too. The same sequential model applies. The difference is surface syntax: Auto removes the boilerplate that C requires while preserving the execution model.

### The First Program

Consider the first program from *Modern C*. It creates an array of five floating-point numbers, iterates over them, and prints each value alongside its square:

<Listing name="First Program" file="listings/ch01/listing-01-01">

The C version of this program would look like this:

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    double A[5] = {9.0, 2.9, 0.0, 0.00007, 3e+25};
    for (size_t i = 0; i < 5; ++i) {
        double val = A[i];
        double sq = val * val;
        printf("element %zu is %g, square is %g\n", i, val, sq);
    }
    return EXIT_SUCCESS;
}
```

When you run this program, you see:

```
element 0 is 9, square is 81
element 1 is 2.9, square is 8.41
element 2 is 0, square is 0
element 3 is 7e-05, square is 4.9e-09
element 4 is 3e+25, square is 9e+50
```

### Comparing the Two Versions

Let us compare the key differences line by line:

**Array declaration.** C uses `double A[5] = {...}`. Auto uses `let A [5]float = [5]float{...}`. The type comes after the name in Auto, and `float` maps to C's `double` for floating-point precision.

**For loop.** C requires `for (size_t i = 0; i < 5; ++i)` with explicit initialization, condition, and increment. Auto uses `for i in 0..5` -- a range-based form that is equivalent but far more concise.

**Print.** C uses `printf` with format specifiers (`%zu`, `%g`). Auto uses `print(...)` which handles formatting automatically. The a2c transpiler generates the correct `printf` call with appropriate format specifiers.

**Return.** C requires `return EXIT_SUCCESS;` (or `return 0;`) at the end of `main`. Auto's `fn main()` does not require an explicit return -- a2c inserts `return 0;` automatically.

### What "Imperative" Really Means

The word "imperative" comes from the Latin *imperare*, "to command." In an imperative program, you issue commands:

- **Assign** a value to a variable.
- **Compute** an expression and store the result.
- **Call** a function to perform an action.
- **Repeat** a block of code until a condition is met.

Both C and Auto follow this model. The statements in a function body execute from top to bottom, one after another. Control flow constructs (`if`, `for`, `while`) modify this order, but the fundamental model is sequential execution.

### Key Modern C Concepts in This Example

This first program already demonstrates several Modern C principles:

1. **Arrays with explicit sizes.** `[5]float` makes the size explicit in the type. Modern C style prefers this over implicit-size arrays because it prevents buffer overflows.

2. **Floating-point precision.** Auto's `float` type maps to C's `double`, not `float`. This is a deliberate choice: single-precision `float` is rarely the right default for numerical work. Modern C makes the same recommendation.

3. **Structured output.** The `print` statement takes multiple arguments and formats them automatically. C's `printf` requires you to manually match format specifiers to argument types. Auto removes this error-prone step.

4. **No global state.** Everything is local to `main`. This is good practice in both languages: minimize global variables.

> **C Deep Dive:** Modern C recommends `size_t` for loop counters that index arrays, because `size_t` is guaranteed to hold any valid array index. The `size_t` type is defined in `<stddef.h>` (and several other headers) as an unsigned integer type. The a2c transpiler uses `int` for simplicity in range-based loops, but the principle is worth remembering when writing C directly. Using a signed type like `int` for array indices can cause warnings when compared with `size_t` values such as the result of `sizeof`.

> **Takeaway:** Imperative programming is about ordered sequences of statements. Auto and C share this model -- the difference is syntax, not semantics.

## 1.2 Compiling and Running

To run the program above, you need to compile it. The workflow differs between C and Auto.

### The C Workflow

In C, you write a `.c` file and invoke the compiler:

```bash
# With gcc
gcc -o listing-01-01 listing-01-01.c
./listing-01-01

# With clang
clang -o listing-01-01 listing-01-01.c
./listing-01-01
```

Modern C recommends compiling with warnings enabled and a recent standard:

```bash
gcc -std=c17 -Wall -Wextra -o listing-01-01 listing-01-01.c
```

The `-std=c17` flag selects the C17 standard. The `-Wall -Wextra` flags enable most useful warnings. Compiling with warnings is not optional in modern C practice -- it catches real bugs.

### The Auto Workflow

In Auto, you use the a2c transpiler and then build:

```bash
auto a2c      # Transpile all .at files to .c
auto b        # Build: compile the generated C
```

The two-step process separates concerns: a2c handles the Auto-to-C translation, and the C compiler handles optimization and code generation. You never lose visibility into the intermediate C code.

<Listing name="Compiling and Running" file="listings/ch01/listing-01-02">

The listing above is a simpler program. Let us trace through what happens:

1. `auto a2c` reads `main.at` and produces `main.c`.
2. `auto b` invokes the C compiler on `main.c` and produces an executable.
3. You run the executable and see the output:

```
Modern C meets Auto!
The answer is 42
```

### What a2c Produces

The transpiler generates clean, readable C. For `listing-01-02`, the output is:

```c
// Auto → C transpiled by a2c
#include <stdio.h>

int main(void) {
    printf("%s\n", "Modern C meets Auto!");
    int answer = 42;
    printf("%s %d\n", "The answer is", answer);
    return 0;
}
```

Notice the details:

- The `// Auto → C transpiled by a2c` header identifies the file as generated.
- `#include <stdio.h>` is added automatically because the program uses `print`.
- `print("text")` becomes `printf("%s\n", "text")` -- the newline is included.
- `print("label", x)` becomes `printf("%s %d\n", "label", x)` -- format specifiers are inferred from the argument types.
- `int main(void)` with `return 0;` is generated from `fn main()`.

### The Full Pipeline in Practice

Here is what the complete development cycle looks like:

```bash
# 1. Write your Auto program
$ cat main.at
fn main() {
    print("Modern C meets Auto!")
    let answer int = 42
    print("The answer is", answer)
}

# 2. Transpile to C
$ auto a2c

# 3. Inspect the generated C (optional but recommended)
$ cat main.c
// Auto → C transpiled by a2c
...

# 4. Build and run
$ auto b
$ ./listing-01-02
Modern C meets Auto!
The answer is 42
```

> **C Deep Dive:** C's `printf` function is variadic -- it accepts any number of arguments after the format string. The format string must match the types of the arguments: `%d` for `int`, `%f` for `double`, `%s` for `char*`, `%zu` for `size_t`. Mismatches cause undefined behavior. Auto's `print` eliminates this class of bugs by generating the correct format string automatically.

> **Takeaway:** The a2c transpiler bridges Auto's simple syntax and C's explicit control. Every Auto construct maps to a specific C pattern.

### Error Messages and Debugging

When something goes wrong, the error can come from two places:

1. **a2c errors** -- syntax errors in your Auto code. These are reported with file and line numbers, just like a compiler.
2. **C compiler errors** -- errors in the generated C. These are rare if a2c is working correctly, but can happen with edge cases.

When you get a C compiler error, look at the generated `.c` file. The line numbers in the error message refer to the C file, not the Auto file. Cross-reference with your Auto source to find the corresponding line.

A common workflow for debugging:

```bash
# If auto a2c succeeds but auto b fails:
$ auto a2c
$ cat main.c           # Check the generated C
$ gcc -c main.c        # Try compiling manually for better error messages
```

## Quick Reference

| Concept | C | Auto |
|---|---|---|
| Main function | `int main(void) { ... return 0; }` | `fn main() { }` |
| Include headers | `#include <stdio.h>` | (automatic) |
| Variable | `double x = 1.5;` | `let x float = 1.5` |
| Array | `double A[5] = {1,2,3,4,5};` | `let A [5]float = [5]float{1,2,3,4,5}` |
| For loop | `for (int i = 0; i < n; i++)` | `for i in 0..n` |
| Print | `printf("x = %d\n", x);` | `print("x =", x)` |
| Compile | `gcc -o prog prog.c` | `auto a2c && auto b` |
| Exit success | `return EXIT_SUCCESS;` | (implicit) |
| Warnings | `-Wall -Wextra` | (built into `auto b`) |
