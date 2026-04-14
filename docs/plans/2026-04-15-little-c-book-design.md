# The Little Book of C → Auto Book Design

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a complete Auto language adaptation of "The Little Book of C" (100 sections, 10 chapters), placed at `little-c/`.

**Architecture:** Follow the same format as the existing Rust book (`rust/`): each section maps to a chapter file with EN `.md` + CN `.cn.md` pair, listings in chapter subdirectories with `main.at` + `main.expected.c` + `pac.at` (with `lang: "c"`). The a2c transpiler already exists with 162 test cases and full CLI support (`auto a2c`).

**Tech Stack:** Auto language, a2c transpiler (`auto a2c`), `auto trans c` command

---

## Positioning

- **Handbook** (`typescript/`): Quick-start reference for TypeScript developers
- **DeepDive** (`typescript-deepdive/`): In-depth type system exploration
- **Rust Book** (`rust/`): Systems programming with Rust target
- **Little C** (`little-c/`): Low-level systems programming with C target — memory, pointers, structs, OS interfaces

## Original Book Structure (10 chapters, 100 sections)

| Ch | Title | Sections | Strategy |
|----|-------|----------|----------|
| 00 | Getting Started | 1-9 | Setup, first program, project structure → Auto equivalents |
| 01 | Language Basics | 11-20 | Data types, operators, control flow, functions → Auto primitives |
| 02 | Working with Memory | 21-30 | Pointers, arrays, strings, malloc/free → Auto's memory model |
| 03 | Structuring Data | 31-40 | Structs, unions, typedef, linked lists → Auto `type`/`enum`/`spec` |
| 04 | Input, Output and Files | 41-50 | printf/scanf, file I/O, errno → Auto print/files/error handling |
| 05 | Compilation & Build Process | 51-60 | Preprocessor, macros, Makefiles → Auto's `pac.at`/`auto b` |
| 06 | Working Close to the System | 61-70 | Syscalls, fork/exec, pipes, signals → Auto system-level features |
| 07 | Debugging, Testing, Profiling | 71-80 | gdb, valgrind, assertions, unit tests → Auto debugging tools |
| 08 | Portable and Modern C | 81-90 | C standards, portability, pthreads, FFI → Auto cross-platform |
| 09 | Building Real Projects | 91-100 | Libraries, CLI tools, HTTP server, parser → Auto project building |

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
| `s[1..3]` | `for (int i = 1; i < 3; i++) { printf("%c", s[i]); }` |

## Code Example Strategy

1. **C concepts that map to Auto**: Show C code from original book → Auto equivalent → a2c output
2. **Auto handles it differently**: Show C approach → Auto's safer/cleaner equivalent (e.g., no manual malloc/free)
3. **C-only low-level**: "C Only" callout with brief explanation (e.g., inline assembly, volatile)

## File Structure

```
little-c/
├── ch00-getting-started.md / .cn.md
├── ch01-language-basics.md / .cn.md
├── ch02-memory.md / .cn.md
├── ch03-structuring-data.md / .cn.md
├── ch04-io-files.md / .cn.md
├── ch05-compilation.md / .cn.md
├── ch06-system-programming.md / .cn.md
├── ch07-debugging.md / .cn.md
├── ch08-portable-modern.md / .cn.md
├── ch09-real-projects.md / .cn.md
├── listings/
│   ├── ch00/
│   │   └── listing-00-01/
│   │       ├── main.at
│   │       ├── main.expected.c
│   │       ├── main.expected.h
│   │       └── pac.at
│   ├── ch01/
│   │   └── ...
│   └── ...
└── stdlib/
    └── runtime.c
```

## Section-to-Chapter Mapping

Each original section (1-100) maps to content within the corresponding chapter file. Not every section gets its own listing — only sections with substantial code examples.

### Listings Plan (key sections with code)

| Listing | Section | Topic |
|---------|---------|-------|
| ch00/ | | |
| listing-00-01 | 1 | Hello World (Auto → C) |
| listing-00-02 | 3 | Writing and running first program |
| listing-00-03 | 9 | Minimal project with pac.at |
| ch01/ | | |
| listing-01-01 | 11 | Data types and variables |
| listing-01-02 | 13 | Operators and expressions |
| listing-01-03 | 14 | Control flow (if/else/switch → is) |
| listing-01-04 | 15 | Loops (for/while → for in) |
| listing-01-05 | 16 | Functions and parameters |
| listing-01-06 | 20 | Practice: calculator |
| ch02/ | | |
| listing-02-01 | 21 | Memory layout (stack vs heap) |
| listing-02-02 | 22 | Pointers and addresses |
| listing-02-03 | 23 | Arrays and pointer arithmetic |
| listing-02-04 | 24 | Strings as character arrays |
| listing-02-05 | 25 | Dynamic memory (malloc/free → Auto approach) |
| listing-02-06 | 28 | Function pointers and callbacks |
| listing-02-07 | 30 | Practice: memory management |
| ch03/ | | |
| listing-03-01 | 31 | Structures and nested structures |
| listing-03-02 | 32 | Unions and type reuse |
| listing-03-03 | 33 | Typedef → Auto type aliases |
| listing-03-04 | 36 | Linked lists |
| listing-03-05 | 37 | Stacks and queues |
| listing-03-06 | 39 | Minimal OOP in C → Auto spec/type |
| listing-03-07 | 40 | Practice: tiny library system |
| ch04/ | | |
| listing-04-01 | 41 | Standard I/O: printf/scanf → print |
| listing-04-02 | 42 | File operations: fopen/fclose |
| listing-04-03 | 43 | Binary file reading/writing |
| listing-04-04 | 47 | Command-line arguments |
| listing-04-05 | 50 | Practice: log reader/writer |
| ch05/ | | |
| listing-05-01 | 51 | Compilation pipeline |
| listing-05-02 | 52 | Preprocessor and macros → Auto approach |
| listing-05-03 | 55 | Makefiles → auto b / pac.at |
| listing-05-04 | 56 | Multi-file projects → mod/use |
| listing-05-05 | 57 | Static and shared libraries |
| ch06/ | | |
| listing-06-01 | 61 | System calls vs stdlib |
| listing-06-02 | 62 | Process creation (fork/exec) |
| listing-06-03 | 63 | File descriptors |
| listing-06-04 | 64 | Pipes and redirection |
| listing-06-05 | 65 | Signals and handlers |
| listing-06-06 | 70 | Practice: mini shell |
| ch07/ | | |
| listing-07-01 | 71 | Debugging strategies |
| listing-07-02 | 73 | Assertions and defensive programming |
| listing-07-03 | 74 | Unit testing in Auto |
| listing-07-04 | 77 | Common undefined behaviors → Auto prevents these |
| listing-07-05 | 80 | Practice: fix bugs |
| ch08/ | | |
| listing-08-01 | 81 | C standard timeline → Auto versioning |
| listing-08-02 | 85 | Threading with pthreads |
| listing-08-03 | 87 | FFI: calling C from Auto |
| listing-08-04 | 89 | Modern style: clean and readable |
| listing-08-05 | 90 | Practice: portable multithreaded program |
| ch09/ | | |
| listing-09-01 | 91 | Designing small libraries |
| listing-09-02 | 92 | Building a CLI tool |
| listing-09-03 | 93 | Tiny HTTP server |
| listing-09-04 | 96 | Writing a text parser |
| listing-09-05 | 100 | Practice: build your own project |

## Execution Order

### Batch 1: Setup + ch00-ch01 (2 chapters)
- Create directory structure, stdlib/runtime.c
- Write ch00 (Getting Started) + ch01 (Language Basics)
- Create listings for ch00 + ch01
- Verify listings with `auto a2c`

### Batch 2: ch02-ch03 (2 chapters — Memory & Data)
- Write ch02 (Working with Memory) + ch03 (Structuring Data)
- Create listings — heaviest C-specific content
- Verify listings compile

### Batch 3: ch04-ch05 (2 chapters — I/O & Build)
- Write ch04 (Input, Output and Files) + ch05 (Compilation & Build)
- Create listings
- Verify listings compile

### Batch 4: ch06-ch07 (2 chapters — System & Debug)
- Write ch06 (System Programming) + ch07 (Debugging, Testing)
- Create listings
- Some content is C-only (gdb, valgrind) — present as context

### Batch 5: ch08-ch09 (2 chapters — Modern C & Projects)
- Write ch08 (Portable and Modern C) + ch09 (Building Real Projects)
- Create listings
- Verify listings compile

### Final: Sync, update README, commit
- Update README.md / README.cn.md
- Final review pass

## Verification

After each batch:
- All listings transpile: `auto a2c <listing-dir>/main.at`
- Compare output with `main.expected.c`
- Manual review for Auto syntax correctness
