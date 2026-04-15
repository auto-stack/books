# TAPL — The Auto Programming Language: Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create "The Auto Programming Language" — the definitive guide to Auto, with 23 chapters + 4 appendices, all 5-language listings, bilingual EN/CN.

**Architecture:** Progressive Depth structure in 3 phases (Script → System → AIOS). Each chapter is one task: create listings first (`.at` + 4 `.expected.*` files), then write EN chapter, then CN chapter, then commit. A new sync script handles the 5-language listing format.

**Tech Stack:** Auto language, transpilers (a2r→Rust, a2p→Python, a2c→C, a2ts→TypeScript), AutoVM

---

## Task 1: Scaffold — Directory Structure & SUMMARY.md

**Files:**
- Create: `tapl/SUMMARY.md`
- Create: `tapl/listings/` (empty directory tree for ch01–ch22)
- Create: `scripts/sync_tapl_listings.py`

**Step 1: Create directory structure**

```bash
mkdir -p tapl/listings/{ch01,ch02,ch03,ch04,ch05,ch06,ch07,ch08,ch09,ch10,ch11,ch12,ch13,ch14,ch15,ch16,ch17,ch18,ch19,ch20,ch21,ch22}
```

**Step 2: Write SUMMARY.md**

Create `tapl/SUMMARY.md` with the full 3-phase table of contents:

```markdown
# The Auto Programming Language

[Introduction](ch00-introduction.md)

## Phase 1 — Auto as Script

- [Getting Started](ch01-getting-started.md)
- [Variables & Operators](ch02-variables-operators.md)
- [Functions & Control Flow](ch03-functions.md)
- [Collections & Nodes](ch04-collections.md)
- [Project: Guessing Game](ch05-guessing-game.md)

## Phase 2 — Auto as System

- [Types & `let`](ch06-types.md)
- [Enums & Pattern Matching](ch07-enums.md)
- [OOP Reshaped](ch08-oop.md)
- [Error Handling](ch09-error-handling.md)
- [Packages & Modules](ch10-modules.md)
- [References & Pointers](ch11-references.md)
- [Memory & Ownership](ch12-memory.md)
- [Generics](ch13-generics.md)
- [Project: File Processor](ch14-file-processor.md)

## Phase 3 — Auto as AIOS

- [Actor Concurrency](ch15-actors.md)
- [Async with `~T`](ch16-async.md)
- [Smart Casts & Flow Typing](ch17-smart-casts.md)
- [Testing](ch18-testing.md)
- [Closures & Iterators](ch19-closures.md)
- [Comptime & Metaprogramming](ch20-comptime.md)
- [Standard Library Tour](ch21-stdlib.md)
- [Project: Multi-user Chat Server](ch22-chat-server.md)

## Appendices

- [Appendix A: Keyword Reference](appendix-a-keywords.md)
- [Appendix B: Operator Table](appendix-b-operators.md)
- [Appendix C: Transpiler Quick-Ref](appendix-c-transpiler-quick-ref.md)
- [Appendix D: Standard Library Index](appendix-d-stdlib-index.md)
```

**Step 3: Write the 5-language sync script**

Create `scripts/sync_tapl_listings.py` — adapted from `scripts/sync_listings.py` but handling 5 code blocks (auto, rust, python, c, typescript). Key differences from the Rust-only sync script:
- `BOOK_DIR` points to `tapl/`
- `read_listing_code()` reads 5 files: `main.at`, `main.expected.rs`, `main.expected.py`, `main.expected.c`, `main.expected.ts`
- `replace_listing_block()` replaces all 5 code blocks
- Each listing directory contains: `main.at`, `main.expected.rs`, `main.expected.py`, `main.expected.c`, `main.expected.ts`, `pac.at`

**Step 4: Commit**

```bash
git add tapl/SUMMARY.md tapl/listings/ scripts/sync_tapl_listings.py
git commit -m "feat(tapl): scaffold directory structure, SUMMARY.md, and sync script"
```

---

## Task 2: ch00 — Introduction

**Files:**
- Create: `tapl/ch00-introduction.md`
- Create: `tapl/ch00-introduction.cn.md`

**No listings** — this chapter is pure prose.

**EN chapter sections:**
1. What is Auto?
2. Language as AIOS — the philosophy
3. Dual Mode: VM and AOT
4. AI-Native Design
5. How This Book Works — the 5-language format explained
6. Who This Book Is For
7. Conventions Used in This Book

**CN chapter:** Full Chinese translation of the EN version.

**Step 1: Write `tapl/ch00-introduction.md`**

Write the English introduction. Key content:
- Auto is a modern programming language designed for the AI era
- AIOS philosophy: Task, Mailbox, and AutoVM as core metaphors
- Dual mode: AutoVM for development (fast iteration), AOT for production (zero-cost)
- AI-native: designed for AI-generated code with high signal-to-noise ratio
- How to read the 5-language listings: Auto is always first, followed by Rust, Python, C, and TypeScript
- No code examples in this chapter

**Step 2: Write `tapl/ch00-introduction.cn.md`**

Full Chinese translation with matching section structure.

**Step 3: Commit**

```bash
git add tapl/ch00-introduction.md tapl/ch00-introduction.cn.md
git commit -m "feat(tapl): add ch00 introduction (EN + CN)"
```

---

## Task 3: ch01 — Getting Started

**Files:**
- Create: `tapl/ch01-getting-started.md`
- Create: `tapl/ch01-getting-started.cn.md`
- Create: `tapl/listings/ch01/listing-01-01/` (Hello World)
- Create: `tapl/listings/ch01/listing-01-02/` (automan project)

**Phase 1 rules:** `var` only, no `let`, no explicit type annotations on variables, function params typed, returns inferred.

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 01-01 | Hello, World! | `fn main()`, `print()` |
| 01-02 | auto.toml generated by automan | Package manifest |

**Step 1: Create listing-01-01**

`listings/ch01/listing-01-01/main.at`:
```auto
fn main() {
    print("Hello, world!")
}
```

`listings/ch01/listing-01-01/main.expected.rs`:
```rust
// Auto-generated by a2r transpiler

#[allow(unused_imports)]
use auto_lang::a2r_std::*;

fn main() {
    println!("Hello, world!");
}
```

`listings/ch01/listing-01-01/main.expected.py`:
```python
# Auto-generated by a2p transpiler

def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
```

`listings/ch01/listing-01-01/main.expected.c`:
```c
// Auto-generated by a2c transpiler

#include <stdio.h>

int main(void) {
    printf("Hello, world!\n");
    return 0;
}
```

`listings/ch01/listing-01-01/main.expected.ts`:
```typescript
// Auto-generated by a2ts transpiler

function main(): void {
    console.log("Hello, world!");
}

main();
```

`listings/ch01/listing-01-01/pac.at`:
```auto
name: "listing-01-01"
version: "0.1.0"

app("listing-01-01") {}
```

**Step 2: Create listing-01-02** (auto.toml — toml only, no .expected.* needed)

`listings/ch01/listing-01-02/auto.toml`:
```toml
[package]
name = "hello_auto"
version = "0.1.0"

[dependencies]
```

**Step 3: Write EN chapter `tapl/ch01-getting-started.md`**

Sections:
1. Installation (autoc + autovm on Linux/macOS/Windows)
2. Hello, World! (Listing 1-1, run with `autovm main.auto`)
3. The Anatomy of an Auto Program
4. Compilation and Execution (`autoc` vs `autovm`)
5. Hello, automan! (Listing 1-2, `automan new`, `automan run`)
6. Summary

**Step 4: Write CN chapter `tapl/ch01-getting-started.cn.md`**

**Step 5: Commit**

```bash
git add tapl/ch01-getting-started.md tapl/ch01-getting-started.cn.md tapl/listings/ch01/
git commit -m "feat(tapl): add ch01 getting started (EN + CN)"
```

---

## Task 4: ch02 — Variables & Operators

**Files:**
- Create: `tapl/ch02-variables-operators.md`
- Create: `tapl/ch02-variables-operators.cn.md`
- Create: `tapl/listings/ch02/listing-02-01/` through `listing-02-06/`

**Phase 1 rules:** Only `var`, all type-inferred, no type annotations on variables.

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 02-01 | Variable declarations | `var x = 5`, type inference |
| 02-02 | Number operations | `int`, `float`, arithmetic |
| 02-03 | String basics | String literals, concatenation, f-strings |
| 02-04 | Boolean logic | `true`, `false`, `&&`, `\|\|`, `!` |
| 02-05 | Comparison operators | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| 02-06 | Shadowing | Re-declaring `var` with same name |

**Step 1: Create all listing files** (6 listings × 6 files each = 36 files)

For each listing, create: `main.at`, `main.expected.rs`, `main.expected.py`, `main.expected.c`, `main.expected.ts`, `pac.at`.

**Step 2: Write EN chapter**

Sections:
1. `var` — Mutable Variables
2. Numbers — Integers and Floats (Listing 2-01, 2-02)
3. Strings — Literals and F-strings (Listing 2-03)
4. Booleans (Listing 2-04)
5. Comparison and Logical Operators (Listing 2-05)
6. Shadowing (Listing 2-06)
7. Exercises

**Step 3: Write CN chapter**

**Step 4: Commit**

```bash
git add tapl/ch02-variables-operators.md tapl/ch02-variables-operators.cn.md tapl/listings/ch02/
git commit -m "feat(tapl): add ch02 variables & operators (EN + CN)"
```

---

## Task 5: ch03 — Functions & Control Flow

**Files:**
- Create: `tapl/ch03-functions.md`
- Create: `tapl/ch03-functions.cn.md`
- Create: `tapl/listings/ch03/listing-03-01/` through `listing-03-08/`

**Phase 1 rules:** Function params typed (`fn greet(name String)`), return types inferred, no `let`.

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 03-01 | Basic function | `fn`, parameters, return |
| 03-02 | Expression bodies | Implicit return from last expression |
| 03-03 | if / else if / else | Conditional branching |
| 03-04 | while loop | `for cond { ... }` (Auto's while) |
| 03-05 | for loop | `for i in 0..10 { ... }` |
| 03-06 | Iterating collections | `for item in list { ... }` |
| 03-07 | break and continue | Loop control |
| 03-08 | Early return | `return` in functions |

**Step 1–4:** Same pattern as Task 4.

```bash
git add tapl/ch03-functions.md tapl/ch03-functions.cn.md tapl/listings/ch03/
git commit -m "feat(tapl): add ch03 functions & control flow (EN + CN)"
```

---

## Task 6: ch04 — Collections & Nodes

**Files:**
- Create: `tapl/ch04-collections.md`
- Create: `tapl/ch04-collections.cn.md`
- Create: `tapl/listings/ch04/listing-04-01/` through `listing-04-08/`

**Phase 1 rules:** JSON-like arrays/objects, no generic syntax, hashmaps/sets via inference, `node` introduced.

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 04-01 | Array literal | `[1, 2, 3]`, indexing, length |
| 04-02 | Object literal | `{ name: "Alice", age: 30 }`, field access |
| 04-03 | HashMap by inference | `var scores = { "Alice": 90, "Bob": 85 }` |
| 04-04 | Set by inference | `var unique = { 1, 2, 3 }` (or set literal) |
| 04-05 | List operations | `.push()`, `.pop()`, `.contains()` |
| 04-06 | String as collection | Iteration, slicing, methods |
| 04-07 | Node basics | `node` for linked structures |
| 04-08 | Node traversal | Walking a linked list / tree |

**Step 1–4:** Same pattern.

```bash
git add tapl/ch04-collections.md tapl/ch04-collections.cn.md tapl/listings/ch04/
git commit -m "feat(tapl): add ch04 collections & nodes (EN + CN)"
```

---

## Task 7: ch05 — Project: Guessing Game

**Files:**
- Create: `tapl/ch05-guessing-game.md`
- Create: `tapl/ch05-guessing-game.cn.md`
- Create: `tapl/listings/ch05/listing-05-01/` through `listing-05-04/`

**Phase 1 capstone.** Combines everything from Ch 1–4.

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 05-01 | Guessing game v1 | Basic input, random, comparison |
| 05-02 | Adding loops | `for` loop to allow multiple guesses |
| 05-03 | Handling different outcomes | `if`/`else` for too high / too low / correct |
| 05-04 | Complete game | Final version with all features |

**Step 1–4:** Same pattern. This is a tutorial chapter — walk the reader through building the game step by step, explaining each addition.

```bash
git add tapl/ch05-guessing-game.md tapl/ch05-guessing-game.cn.md tapl/listings/ch05/
git commit -m "feat(tapl): add ch05 guessing game project (EN + CN)"
```

---

## Task 8: ch06 — Types & `let`

**Files:**
- Create: `tapl/ch06-types.md`
- Create: `tapl/ch06-types.cn.md`
- Create: `tapl/listings/ch06/listing-06-01/` through `listing-06-07/`

**Phase 2 begins.** This is the "growing up" chapter. `let` introduced, explicit type annotations, `type` keyword.

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 06-01 | `let` vs `var` | Immutable vs mutable binding |
| 06-02 | Explicit type annotations | `var x int = 5`, `let name String = "Alice"` |
| 06-03 | Defining a type | `type User { name String, age int }` |
| 06-04 | Default constructor | `User { name: "Alice", age: 30 }` |
| 06-05 | Adding methods with `ext` | `ext User { fn greet() { ... } }` |
| 06-06 | Tuple types | `(int, String)` |
| 06-07 | Type aliases | `type Point = (int, int)` |

**Step 1–4:** Same pattern.

```bash
git add tapl/ch06-types.md tapl/ch06-types.cn.md tapl/listings/ch06/
git commit -m "feat(tapl): add ch06 types & let (EN + CN)"
```

---

## Task 9: ch07 — Enums & Pattern Matching

**Files:**
- Create: `tapl/ch07-enums.md`
- Create: `tapl/ch07-enums.cn.md`
- Create: `tapl/listings/ch07/listing-07-01/` through `listing-07-07/`

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 07-01 | Basic enum | `enum Direction { North, South, East, West }` |
| 07-02 | Enum with data | `enum Shape { Circle(float), Rect(float, float) }` |
| 07-03 | Pattern matching with `is` | `is shape { Circle(r) => ... }` |
| 07-04 | `on` blocks | Message handler style matching |
| 07-05 | Destructuring | Nested pattern matching |
| 07-06 | Exhaustive matching | Compiler-enforced completeness |
| 07-07 | Matching with guards | `is x { n if n > 0 => ... }` |

**Step 1–4:** Same pattern.

```bash
git add tapl/ch07-enums.md tapl/ch07-enums.cn.md tapl/listings/ch07/
git commit -m "feat(tapl): add ch07 enums & pattern matching (EN + CN)"
```

---

## Task 10: ch08 — OOP Reshaped

**Files:**
- Create: `tapl/ch08-oop.md`
- Create: `tapl/ch08-oop.cn.md`
- Create: `tapl/listings/ch08/listing-08-01/` through `listing-08-08/`

**The centerpiece chapter.** Auto's unique OOP model: `is`, `has`, `spec`, `as`, `ext`.

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 08-01 | `type` as data container | `type Point { x int, y int }` |
| 08-02 | `is` — inheritance | `type Hawk is Bird { ... }` |
| 08-03 | `has` — composition + delegation | `type Person has Hand { ... }` (auto-delegation) |
| 08-04 | `spec` — behavioral contract | `spec Drawable { fn draw() }` |
| 08-05 | `as` — implementing a spec | `type Circle as Drawable { fn draw() { ... } }` |
| 08-06 | `ext` — post-hoc extension | `ext String { fn shout() { ... } }` |
| 08-07 | Orphan rule override | `ext File as Reader { ... }` |
| 08-08 | Putting it all together | Combined example using all 5 keywords |

**Step 1–4:** Same pattern.

```bash
git add tapl/ch08-oop.md tapl/ch08-oop.cn.md tapl/listings/ch08/
git commit -m "feat(tapl): add ch08 OOP reshaped (EN + CN)"
```

---

## Task 11: ch09 — Error Handling

**Files:**
- Create: `tapl/ch09-error-handling.md`
- Create: `tapl/ch09-error-handling.cn.md`
- Create: `tapl/listings/ch09/listing-09-01/` through `listing-09-07/`

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 09-01 | `?T` — optional values | `var name ?String = none` |
| 09-02 | Optional chaining | `user?.address?.street` |
| 09-03 | `!T` — error type | `fn parse(s String) !int` |
| 09-04 | The `!` operator | Propagating errors with trailing `!` |
| 09-05 | Custom error types | `type ParseError { message String }` |
| 09-06 | try / catch patterns | Handling errors explicitly |
| 09-07 | Error handling best practices | When to use `?T` vs `!T` |

**Step 1–4:** Same pattern.

```bash
git add tapl/ch09-error-handling.md tapl/ch09-error-handling.cn.md tapl/listings/ch09/
git commit -m "feat(tapl): add ch09 error handling (EN + CN)"
```

---

## Task 12: ch10 — Packages & Modules

**Files:**
- Create: `tapl/ch10-modules.md`
- Create: `tapl/ch10-modules.cn.md`
- Create: `tapl/listings/ch10/listing-10-01/` through `listing-10-05/`

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 10-01 | automan new project | `automan new my_project` |
| 10-02 | auto.toml with dependencies | `[dependencies]` section |
| 10-03 | `mod` and `use` | Defining and importing modules |
| 10-04 | Module visibility | Public vs private |
| 10-05 | Splitting into files | Multi-file project structure |

**Step 1–4:** Same pattern.

```bash
git add tapl/ch10-modules.md tapl/ch10-modules.cn.md tapl/listings/ch10/
git commit -m "feat(tapl): add ch10 packages & modules (EN + CN)"
```

---

## Task 13: ch11 — References & Pointers

**Files:**
- Create: `tapl/ch11-references.md`
- Create: `tapl/ch11-references.cn.md`
- Create: `tapl/listings/ch11/listing-11-01/` through `listing-11-06/`

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 11-01 | `view T` — read-only reference | Immutable borrowing |
| 11-02 | `mut T` — mutable reference | Mutable borrowing |
| 11-03 | Reference rules | Only one mutable OR many immutable |
| 11-04 | `*T` — raw pointer | System-level pointer access |
| 11-05 | `&self` in methods | Self-reference in `ext` blocks |
| 11-06 | Reference lifetime basics | Scopes and validity |

**Step 1–4:** Same pattern.

```bash
git add tapl/ch11-references.md tapl/ch11-references.cn.md tapl/listings/ch11/
git commit -m "feat(tapl): add ch11 references & pointers (EN + CN)"
```

---

## Task 14: ch12 — Memory & Ownership

**Files:**
- Create: `tapl/ch12-memory.md`
- Create: `tapl/ch12-memory.cn.md`
- Create: `tapl/listings/ch12/listing-12-01/` through `listing-12-06/`

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 12-01 | Stack vs heap | Where values live |
| 12-02 | Implicit move | Transfer of ownership across scopes |
| 12-03 | Clone for copy | `.clone()` when you need a duplicate |
| 12-04 | Escape analysis | Compiler decides stack or heap |
| 12-05 | AutoFree | Automatic cleanup without GC |
| 12-06 | Zero-GC in practice | Performance implications |

**Step 1–4:** Same pattern.

```bash
git add tapl/ch12-memory.md tapl/ch12-memory.cn.md tapl/listings/ch12/
git commit -m "feat(tapl): add ch12 memory & ownership (EN + CN)"
```

---

## Task 15: ch13 — Generics

**Files:**
- Create: `tapl/ch13-generics.md`
- Create: `tapl/ch13-generics.cn.md`
- Create: `tapl/listings/ch13/listing-13-01/` through `listing-13-07/`

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 13-01 | Generic function | `fn largest<T>(list []T) T` |
| 13-02 | Generic type | `type Box<T> { value T }` |
| 13-03 | `spec` bounds | `fn foo<T>(x T) where T: Comparable` |
| 13-04 | Multiple bounds | Combining specs |
| 13-05 | Generic methods | `ext Box<T> { fn unwrap() T }` |
| 13-06 | Monomorphization | Zero-cost generics |
| 13-07 | Generic enums | `enum Result<T, E> { Ok(T), Err(E) }` |

**Step 1–4:** Same pattern.

```bash
git add tapl/ch13-generics.md tapl/ch13-generics.cn.md tapl/listings/ch13/
git commit -m "feat(tapl): add ch13 generics (EN + CN)"
```

---

## Task 16: ch14 — Project: File Processor

**Files:**
- Create: `tapl/ch14-file-processor.md`
- Create: `tapl/ch14-file-processor.cn.md`
- Create: `tapl/listings/ch14/listing-14-01/` through `listing-14-05/`

**Phase 2 capstone.** CLI tool using types, enums, error handling, file I/O, generics.

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 14-01 | Argument parsing | Reading CLI args |
| 14-02 | File reading with error handling | `!T` for file operations |
| 14-03 | Config type | `type Config` with fields |
| 14-04 | Search function with generics | Generic search logic |
| 14-05 | Complete file processor | Full CLI application |

**Step 1–4:** Same pattern. Tutorial-style walkthrough.

```bash
git add tapl/ch14-file-processor.md tapl/ch14-file-processor.cn.md tapl/listings/ch14/
git commit -m "feat(tapl): add ch14 file processor project (EN + CN)"
```

---

## Task 17: ch15 — Actor Concurrency

**Files:**
- Create: `tapl/ch15-actors.md`
- Create: `tapl/ch15-actors.cn.md`
- Create: `tapl/listings/ch15/listing-15-01/` through `listing-15-07/`

**Phase 3 begins.**

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 15-01 | Spawning a task | `task`, `spawn` |
| 15-02 | Sending messages | `send`, message types |
| 15-03 | Receiving with `on` | `on Message { ... }` handler |
| 15-04 | Actor with state | `task.ram`, state isolation |
| 15-05 | `main` as primary actor | The top-level actor |
| 15-06 | Multiple actors | Fan-out / fan-in patterns |
| 15-07 | Actor error handling | Error propagation across actors |

**Step 1–4:** Same pattern.

```bash
git add tapl/ch15-actors.md tapl/ch15-actors.cn.md tapl/listings/ch15/
git commit -m "feat(tapl): add ch15 actor concurrency (EN + CN)"
```

---

## Task 18: ch16 — Async with `~T`

**Files:**
- Create: `tapl/ch16-async.md`
- Create: `tapl/ch16-async.cn.md`
- Create: `tapl/listings/ch16/listing-16-01/` through `listing-16-06/`

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 16-01 | `~T` blueprint | Defining async return type |
| 16-02 | Async function | `fn fetch(url String) ~String` |
| 16-03 | `on` for async handlers | Completing async operations |
| 16-04 | Composing async | Chaining multiple `~T` operations |
| 16-05 | Async + actors | Combining actors with async |
| 16-06 | Timeout and cancellation | Managing async lifecycle |

**Step 1–4:** Same pattern.

```bash
git add tapl/ch16-async.md tapl/ch16-async.cn.md tapl/listings/ch16/
git commit -m "feat(tapl): add ch16 async with ~T (EN + CN)"
```

---

## Task 19: ch17 — Smart Casts & Flow Typing

**Files:**
- Create: `tapl/ch17-smart-casts.md`
- Create: `tapl/ch17-smart-casts.cn.md`
- Create: `tapl/listings/ch17/listing-17-01/` through `listing-17-05/`

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 17-01 | `if x is T` narrowing | Flow-sensitive type narrowing |
| 17-02 | Union types | `String \| int`, working with mixed types |
| 17-03 | Exhaustive narrowing | Compiler-enforced handling |
| 17-04 | Smart cast in when blocks | Pattern + type narrowing combined |
| 17-05 | Type-safe dispatch | No casting needed |

**Step 1–4:** Same pattern.

```bash
git add tapl/ch17-smart-casts.md tapl/ch17-smart-casts.cn.md tapl/listings/ch17/
git commit -m "feat(tapl): add ch17 smart casts & flow typing (EN + CN)"
```

---

## Task 20: ch18 — Testing

**Files:**
- Create: `tapl/ch18-testing.md`
- Create: `tapl/ch18-testing.cn.md`
- Create: `tapl/listings/ch18/listing-18-01/` through `listing-18-05/`

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 18-01 | First test | `#[test] fn test_addition()` |
| 18-02 | Assert macros | `assert!`, `assert_eq!`, `assert_ne!` |
| 18-03 | Testing error cases | Testing `!T` functions |
| 18-04 | Integration tests | Multi-module testing |
| 18-05 | Test organization | `automan test`, test directory structure |

**Step 1–4:** Same pattern.

```bash
git add tapl/ch18-testing.md tapl/ch18-testing.cn.md tapl/listings/ch18/
git commit -m "feat(tapl): add ch18 testing (EN + CN)"
```

---

## Task 21: ch19 — Closures & Iterators

**Files:**
- Create: `tapl/ch19-closures.md`
- Create: `tapl/ch19-closures.cn.md`
- Create: `tapl/listings/ch19/listing-19-01/` through `listing-19-07/`

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 19-01 | Closure syntax | `\|x\| x + 1` |
| 19-02 | Capturing variables | Closure environment |
| 19-03 | Iterator basics | `.iter()`, `.next()` |
| 19-04 | `.map()` | Transforming elements |
| 19-05 | `.filter()` | Selecting elements |
| 19-06 | `.fold()` | Reducing to a single value |
| 19-07 | Chaining iterators | `.filter().map().collect()` |

**Step 1–4:** Same pattern.

```bash
git add tapl/ch19-closures.md tapl/ch19-closures.cn.md tapl/listings/ch19/
git commit -m "feat(tapl): add ch19 closures & iterators (EN + CN)"
```

---

## Task 22: ch20 — Comptime & Metaprogramming

**Files:**
- Create: `tapl/ch20-comptime.md`
- Create: `tapl/ch20-comptime.cn.md`
- Create: `tapl/listings/ch20/listing-20-01/` through `listing-20-05/`

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 20-01 | `#[]` attribute basics | Compile-time annotations |
| 20-02 | Simple macro | Code generation at compile time |
| 20-03 | Conditional compilation | `#[cfg(target = "linux")]` |
| 20-04 | Platform detection | `#[cfg(target_os)]` |
| 20-05 | Compile-time evaluation | Running code during compilation |

**Step 1–4:** Same pattern.

```bash
git add tapl/ch20-comptime.md tapl/ch20-comptime.cn.md tapl/listings/ch20/
git commit -m "feat(tapl): add ch20 comptime & metaprogramming (EN + CN)"
```

---

## Task 23: ch21 — Standard Library Tour

**Files:**
- Create: `tapl/ch21-stdlib.md`
- Create: `tapl/ch21-stdlib.cn.md`
- Create: `tapl/listings/ch21/listing-21-01/` through `listing-21-06/`

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 21-01 | File I/O | `read_file()`, `write_file()` |
| 21-02 | Networking basics | TCP connections |
| 21-03 | JSON serialization | `to_json()`, `from_json()` |
| 21-04 | Collections deep dive | Advanced HashMap, HashSet operations |
| 21-05 | String processing | Regex, splitting, searching |
| 21-06 | Time and date | Timestamps, formatting, parsing |

**Step 1–4:** Same pattern.

```bash
git add tapl/ch21-stdlib.md tapl/ch21-stdlib.cn.md tapl/listings/ch21/
git commit -m "feat(tapl): add ch21 standard library tour (EN + CN)"
```

---

## Task 24: ch22 — Project: Multi-user Chat Server

**Files:**
- Create: `tapl/ch22-chat-server.md`
- Create: `tapl/ch22-chat-server.cn.md`
- Create: `tapl/listings/ch22/listing-22-01/` through `listing-22-06/`

**Phase 3 capstone.** Real distributed system: actors for user sessions, async message routing, networking.

**Listings:**

| # | Caption | Auto Concept |
|---|---------|-------------|
| 22-01 | Message types | `enum ChatMsg { Join, Leave, Say }` |
| 22-02 | User actor | Actor per connected user |
| 22-03 | Room actor | Central chat room with state |
| 22-04 | Async connection handling | `~T` for network I/O |
| 22-05 | Message broadcasting | Fan-out pattern |
| 22-06 | Complete chat server | Full integration |

**Step 1–4:** Same pattern. Tutorial-style walkthrough.

```bash
git add tapl/ch22-chat-server.md tapl/ch22-chat-server.cn.md tapl/listings/ch22/
git commit -m "feat(tapl): add ch22 chat server project (EN + CN)"
```

---

## Task 25: Appendix A — Keyword Reference

**Files:**
- Create: `tapl/appendix-a-keywords.md`
- Create: `tapl/appendix-a-keywords.cn.md`

**No listings.** Reference table of every Auto keyword:

| Keyword | Syntax | Description |
|---------|--------|-------------|
| `fn` | `fn name(params) { body }` | Function definition |
| `var` | `var x = expr` | Mutable variable |
| `let` | `let x = expr` | Immutable binding |
| `type` | `type Name { fields }` | Data container |
| `enum` | `enum Name { variants }` | Sum type |
| `is` | `is expr { patterns }` | Pattern matching |
| `on` | `on Msg { body }` | Message handler |
| `spec` | `spec Name { methods }` | Behavioral contract |
| `as` | `type X as Spec { }` | Spec implementation |
| `ext` | `ext Type { methods }` | Extension |
| `has` | `type X has Y { }` | Composition |
| `if` / `else` | `if cond { } else { }` | Conditional |
| `for` / `in` | `for x in range { }` | Loop |
| `return` | `return expr` | Early return |
| `true` / `false` | | Boolean literals |
| `spawn` | `spawn task_name` | Create actor |
| `send` | `send target msg` | Send message |
| `use` | `use module` | Import |
| `mod` | `mod name { }` | Module definition |
| `sys` | `sys { unsafe_code }` | System-level block |

(Plus all other keywords)

```bash
git add tapl/appendix-a-keywords.md tapl/appendix-a-keywords.cn.md
git commit -m "feat(tapl): add appendix A keyword reference (EN + CN)"
```

---

## Task 26: Appendix B — Operator Table

**Files:**
- Create: `tapl/appendix-b-operators.md`
- Create: `tapl/appendix-b-operators.cn.md`

**No listings.** Complete operator reference with precedence and associativity.

```bash
git add tapl/appendix-b-operators.md tapl/appendix-b-operators.cn.md
git commit -m "feat(tapl): add appendix B operator table (EN + CN)"
```

---

## Task 27: Appendix C — Transpiler Quick-Ref

**Files:**
- Create: `tapl/appendix-c-transpiler-quick-ref.md`
- Create: `tapl/appendix-c-transpiler-quick-ref.cn.md`

**No listings.** Mapping tables: Auto ↔ Rust ↔ Python ↔ C ↔ TypeScript for every major concept. This is the Rosetta Stone appendix.

```bash
git add tapl/appendix-c-transpiler-quick-ref.md tapl/appendix-c-transpiler-quick-ref.cn.md
git commit -m "feat(tapl): add appendix C transpiler quick-ref (EN + CN)"
```

---

## Task 28: Appendix D — Standard Library Index

**Files:**
- Create: `tapl/appendix-d-stdlib-index.md`
- Create: `tapl/appendix-d-stdlib-index.cn.md`

**No listings.** Function/type listing organized by module (io, net, collections, string, time, etc.).

```bash
git add tapl/appendix-d-stdlib-index.md tapl/appendix-d-stdlib-index.cn.md
git commit -m "feat(tapl): add appendix D stdlib index (EN + CN)"
```

---

## Task 29: Update README

**Files:**
- Modify: `README.md` — Add TAPL as the 8th book in the collection table

Add a new row to the Book Collection table and add a full section describing TAPL with chapter listing table (same format as the other 7 books).

```bash
git add README.md
git commit -m "docs: add TAPL to README book collection"
```

---

## Execution Strategy

### Per-chapter workflow

Each chapter task (Tasks 2–24) follows this workflow:

1. **Create listing directories** — `mkdir -p tapl/listings/chNN/listing-NN-MM/`
2. **Write listing files** — For each listing, create all 6 files:
   - `main.at` (Auto source)
   - `main.expected.rs` (Rust transpiler output)
   - `main.expected.py` (Python transpiler output)
   - `main.expected.c` (C transpiler output)
   - `main.expected.ts` (TypeScript transpiler output)
   - `pac.at` (package manifest)
3. **Write EN chapter** — `tapl/chNN-topic.md` with `<Listing>` tags and prose
4. **Write CN chapter** — `tapl/chNN-topic.cn.md` (full Chinese translation)
5. **Commit** — One commit per chapter

### Parallelization

Chapters within the same phase can be generated in parallel (independent content). Natural batches:
- **Batch A:** ch01–ch04 (Phase 1 chapters before project)
- **Batch B:** ch06–ch13 (Phase 2 chapters before project)
- **Batch C:** ch15–ch21 (Phase 3 chapters before project)
- Projects (ch05, ch14, ch22) should come after their phase chapters
- Appendices can all be done in parallel

### Estimated scope

- **27 content tasks** (23 chapters + 4 appendices)
- **2 infrastructure tasks** (scaffold + README update)
- **~150 listings** across all chapters
- **~900 listing files** (150 listings × 6 files each)
- **58 markdown files** (27 content tasks × 2 languages + SUMMARY.md + sync script updates)

### Reference materials

When writing each chapter, consult these companion books for Auto language patterns:
- `rust/` — for systems-level Auto code and a2r transpiler output format
- `typescript/` and `typescript-deepdive/` — for type system and a2ts output format
- `little-c/` and `modern-c/` — for low-level concepts and a2c output format
- `byte-of-python/` and `think-python/` — for beginner-friendly tone and a2p output format
