# Modern C → Auto Book Design

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a complete Auto language adaptation of "Modern C" (Jens Gustedt, 438 pages, 21 chapters across 4 levels), placed at `modern-c/`.

**Architecture:** Follow the same format as the existing books (`rust/`, `typescript/`, `typescript-deepdive/`, `little-c/`): each chapter maps to a chapter file with EN `.md` + CN `.cn.md` pair, listings in chapter subdirectories with `main.at` + `main.expected.c` + `pac.at` (with `lang: "c"`). The book is organized into 4 levels (Encounter, Acquaintance, Cognition, Experience) covering 21 chapters.

**Tech Stack:** Auto language, a2c transpiler (`auto a2c`), `auto trans c` command

---

## Positioning

- **Handbook** (`typescript/`): Quick-start reference for TypeScript developers
- **DeepDive** (`typescript-deepdive/`): In-depth type system exploration
- **Rust Book** (`rust/`): Systems programming with Rust target
- **Little C** (`little-c/`): Gentle introduction to C for Auto programmers
- **Modern C** (`modern-c/`): Deep, rigorous C programming — abstract state machine, memory model, type-generic programming, threads, atomics

## Original Book Structure (4 levels, 21 chapters)

| Ch | Level | Title | Sections | Strategy |
|----|-------|-------|----------|----------|
| 00 | — | Introduction | — | Book overview, Modern C philosophy, how to read |
| 01 | 0 Encounter | Getting Started | 1.1-1.2 | First program, compiling → Auto equivalents |
| 02 | 0 Encounter | Program Structure | 2.1-2.4 | Grammar, declarations, definitions, statements |
| 03 | 1 Acquaintance | Control Flow | 3.1-3.3 | Conditionals, iterations, switch → `if`/`for`/`is` |
| 04 | 1 Acquaintance | Expressions | 4.1-4.6 | Operators, arithmetic, boolean → Auto equivalents |
| 05 | 1 Acquaintance | Basic Values & Data | 5.1-5.7 | Types, abstract state machine, constants → Auto types |
| 06 | 1 Acquaintance | Derived Data Types | 6.1-6.4 | Arrays, pointers, structs, typedef → Auto `type`/`enum` |
| 07 | 1 Acquaintance | Functions | 7.1-7.3 | Functions, main, recursion → Auto `fn` |
| 08 | 1 Acquaintance | C Library Functions | 8.1-8.8 | stdlib, numerics, I/O, strings, time → Auto stdlib |
| 09 | 2 Cognition | Style | 9.1-9.3 | Formatting, naming, i18n → Auto conventions |
| 10 | 2 Cognition | Organization & Documentation | 10.1-10.2 | Interface docs, implementation → Auto mod/use |
| 11 | 2 Cognition | Pointers | 11.1-11.4 | Pointer ops, structs, arrays, function pointers → Auto refs |
| 12 | 2 Cognition | The C Memory Model | 12.1-12.7 | Memory model, unions, alignment → Auto's safe model |
| 13 | 2 Cognition | Storage | 13.1-13.5 | malloc/free, lifetime, initialization → AutoFree |
| 14 | 2 Cognition | Processing & I/O | 14.1-14.6 | Text, formatted input, UTF-8, binary → Auto I/O |
| 15 | 2 Cognition | Program Failure | 15.1-15.6 | Errors, UB, failure handling → Auto `!T` error type |
| 16 | 3 Experience | Performance | 16.1-16.4 | Inline, restrict, attributes, measurement → Auto perf |
| 17 | 3 Experience | Function-like Macros | 17.1-17.5 | Macros, argument checking, varargs → Auto comptime |
| 18 | 3 Experience | Type-generic Programming | 18.1-18.4 | Generic selection, type inference → Auto generics |
| 19 | 3 Experience | Variations in Control Flow | 19.1-19.6 | setjmp/longjmp, signals → Auto error handling |
| 20 | 3 Experience | Threads | 20.1-20.7 | pthreads, mutexes, condition variables → Auto actors |
| 21 | 3 Experience | Atomics & Memory Consistency | 21.1-21.4 | Happened-before, consistency models → Auto concurrency |

## Auto-to-C Transpilation Rules (from a2c test cases)

| Auto | C |
|------|---|
| `fn main() { }` | `int main(void) { return 0; }` |
| `fn add(a int, b int) int { a + b }` | `int add(int a, int b) { return a + b; }` |
| `print("text")` | `printf("%s\n", "text");` |
| `print("val:", x)` | `printf("%s %d\n", "val:", x);` |
| `let x int = 5` | `int x = 5;` |
| `var x = 5` | `int x = 5;` (type inferred) |
| `type Point { x int, y int }` | `struct Point { int x; int y; };` |
| `Point(1, 2)` | `{.x = 1, .y = 2}` (designated init) |
| `enum Color { RED, GREEN, BLUE }` | `enum Color { COLOR_RED, COLOR_GREEN, COLOR_BLUE };` |
| `Color.BLUE` | `COLOR_BLUE` |
| `enum Atom { Int int, Float float }` | `struct Atom { tag; union { int Int; float Float; } as; };` |
| `Atom.Int(11)` | `{.tag = ATOM_INT, .as.Int = 11}` |
| `.field` (in methods) | `self->field` |
| `p.modulus()` | `Point_Modulus(&p)` |
| `is x { 0 => ... else => ... }` | `switch (x) { case 0: ... default: ... }` |
| `spec Flyer { fn fly() }` | vtable struct with function pointers |
| `type Pigeon as Flyer { }` | vtable instance + method functions |
| `has core WarpDrive for Engine` | forwarding function `Starship_start → WarpDrive_start` |
| `for i in 0..10 { }` | `for (int i = 0; i < 10; i++) { }` |

## Key Differences from Little C Book

1. **Deeper technical content**: Modern C covers the abstract state machine, effective types, alignment, and the full C memory model in rigorous detail
2. **Advanced C features**: Type-generic programming (`_Generic`), `restrict`, `inline`, `_Atomic`, `_Static_assert`
3. **Concurrency**: Full chapters on threads (mutexes, condition variables) and atomic operations
4. **C-only heavy**: Chapters 12, 16-19, 20-21 are deeply C-specific. Present as "C Deep Dive" with Auto's alternatives where applicable
5. **More listings**: ~46 listings in the original, we'll create ~50 listings

## Code Example Strategy

1. **C concepts that map to Auto**: Show C code from original book → Auto equivalent → a2c output
2. **Auto handles it differently**: Show C approach → Auto's safer/cleaner equivalent
3. **C-only deep dive**: "C Deep Dive" callout with brief explanation (e.g., `_Generic`, `setjmp`, `_Atomic`)

## File Structure

```
modern-c/
├── ch00-introduction.md / .cn.md
├── ch01-getting-started.md / .cn.md
├── ch02-program-structure.md / .cn.md
├── ch03-control-flow.md / .cn.md
├── ch04-expressions.md / .cn.md
├── ch05-basic-values.md / .cn.md
├── ch06-derived-types.md / .cn.md
├── ch07-functions.md / .cn.md
├── ch08-c-library.md / .cn.md
├── ch09-style.md / .cn.md
├── ch10-organization.md / .cn.md
├── ch11-pointers.md / .cn.md
├── ch12-memory-model.md / .cn.md
├── ch13-storage.md / .cn.md
├── ch14-io-processing.md / .cn.md
├── ch15-program-failure.md / .cn.md
├── ch16-performance.md / .cn.md
├── ch17-macros.md / .cn.md
├── ch18-type-generic.md / .cn.md
├── ch19-control-flow-variations.md / .cn.md
├── ch20-threads.md / .cn.md
├── ch21-atomics.md / .cn.md
├── listings/
│   ├── ch01/
│   │   └── listing-01-01/
│   │       ├── main.at
│   │       ├── main.expected.c
│   │       └── pac.at
│   ├── ch02/
│   │   └── ...
│   └── ...
└── stdlib/
    └── runtime.c
```

## Listings Plan (key sections with code)

| Listing | Ch | Topic |
|---------|-----|-------|
| ch01/ | | |
| listing-01-01 | 1 | First program with designated initializers |
| listing-01-02 | 1 | Compiling and running |
| ch02/ | | |
| listing-02-01 | 2 | Declarations and definitions |
| listing-02-02 | 2 | Statements and control |
| ch03/ | | |
| listing-03-01 | 3 | Conditional execution (if/else) |
| listing-03-02 | 3 | Iterations (for/while) |
| listing-03-03 | 3 | Multiple selection (switch → is) |
| ch04/ | | |
| listing-04-01 | 4 | Arithmetic operators |
| listing-04-02 | 4 | Boolean context and ternary |
| ch05/ | | |
| listing-05-01 | 5 | Basic types and the abstract state machine |
| listing-05-02 | 5 | Specifying values and conversions |
| listing-05-03 | 5 | Named constants and enumerations |
| ch06/ | | |
| listing-06-01 | 6 | Arrays and array operations |
| listing-06-02 | 6 | Pointers as opaque types |
| listing-06-03 | 6 | Structures and type aliases |
| ch07/ | | |
| listing-07-01 | 7 | Simple functions |
| listing-07-02 | 7 | Recursion |
| ch08/ | | |
| listing-08-01 | 8 | Integer arithmetic (stdlib) |
| listing-08-02 | 8 | Formatted I/O |
| listing-08-03 | 8 | String processing |
| ch09/ | | |
| listing-09-01 | 9 | Clean code style |
| ch10/ | | |
| listing-10-01 | 10 | Interface documentation pattern |
| ch11/ | | |
| listing-11-01 | 11 | Pointer operations |
| listing-11-02 | 11 | Pointers and structures |
| listing-11-03 | 11 | Function pointers |
| ch12/ | | |
| listing-12-01 | 12 | Memory model and unions |
| listing-12-02 | 12 | Effective types and alignment |
| ch13/ | | |
| listing-13-01 | 13 | malloc and storage duration |
| listing-13-02 | 13 | Initialization patterns |
| ch14/ | | |
| listing-14-01 | 14 | Text processing |
| listing-14-02 | 14 | Formatted input |
| ch15/ | | |
| listing-15-01 | 15 | Error handling patterns |
| listing-15-02 | 15 | Error checking and cleanup |
| ch16/ | | |
| listing-16-01 | 16 | Inline functions |
| listing-16-02 | 16 | Performance measurement |
| ch17/ | | |
| listing-17-01 | 17 | Function-like macros → Auto comptime |
| ch18/ | | |
| listing-18-01 | 18 | Type-generic programming → Auto generics |
| listing-18-02 | 18 | Type inference |
| ch19/ | | |
| listing-19-01 | 19 | setjmp/longjmp → Auto error handling |
| ch20/ | | |
| listing-20-01 | 20 | Thread basics |
| listing-20-02 | 20 | Mutexes and critical sections |
| ch21/ | | |
| listing-21-01 | 21 | Atomic operations |

## Execution Order

### Batch 1: Setup + ch00-ch03 (intro + Encounter + start Acquaintance)
- Create directory structure, stdlib/runtime.c
- Write ch00 (Introduction) + ch01 (Getting Started) + ch02 (Program Structure) + ch03 (Control Flow)
- Create listings for ch01-ch03
- Verify listings with `auto a2c`

### Batch 2: ch04-ch08 (Acquaintance — expressions, values, types, functions, library)
- Write ch04 (Expressions) + ch05 (Basic Values) + ch06 (Derived Types)
- Write ch07 (Functions) + ch08 (C Library)
- Create listings
- Verify listings compile

### Batch 3: ch09-ch12 (Cognition — style, org, pointers, memory model)
- Write ch09 (Style) + ch10 (Organization) + ch11 (Pointers)
- Write ch12 (Memory Model)
- Create listings — heaviest C-specific content
- Verify listings compile

### Batch 4: ch13-ch15 (Cognition — storage, I/O, failure)
- Write ch13 (Storage) + ch14 (I/O Processing)
- Write ch15 (Program Failure)
- Create listings

### Batch 5: ch16-ch18 (Experience — performance, macros, type-generic)
- Write ch16 (Performance) + ch17 (Function-like Macros)
- Write ch18 (Type-generic Programming)
- Create listings

### Batch 6: ch19-ch21 (Experience — control flow, threads, atomics)
- Write ch19 (Control Flow Variations) + ch20 (Threads)
- Write ch21 (Atomics & Memory Consistency)
- Create listings

### Final: Sync, update README, commit
- Update README.md / README.cn.md
- Final review pass

## Verification

After each batch:
- All listings transpile: `auto a2c <listing-dir>/main.at`
- Compare output with `main.expected.c`
- Manual review for Auto syntax correctness

## Reference: Content Source

The original book "Modern C" by Jens Gustedt is a 438-page PDF located at `D:\books\C\ModernC.pdf`. Key content to extract during implementation:

- **Level 0 (Encounter, ch1-2)**: Basic imperative programming, program structure
- **Level 1 (Acquaintance, ch3-8)**: Control flow, expressions, types, functions, library
- **Level 2 (Cognition, ch9-15)**: Style, pointers, memory model, storage, I/O, failure
- **Level 3 (Experience, ch16-21)**: Performance, macros, generics, threads, atomics
