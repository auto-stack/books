# TAPL — The Auto Programming Language (Design Document)

**Date:** 2026-04-15
**Project:** The Auto Programming Language — the definitive guide to Auto
**Output directory:** `tapl/`

---

## 1. Project Overview

TAPL is the 8th book in the Auto book collection and the first **original** book — not an adaptation of an existing work. It is the definitive guide to the Auto programming language.

The book follows a **Progressive Depth** structure with three explicit phases, mirroring Auto's dual nature: it starts as a friendly scripting language running on AutoVM, then "grows" into a full systems programming language.

**Core design principles:**

- Every code listing shows **all 5 languages**: Auto + Rust + Python + C + TypeScript
- Light, incremental tone — simple to hard, with many examples
- Bilingual: English (`.md`) + Chinese (`.cn.md`) for every chapter
- Three phases with capstone projects at the end of each

---

## 2. Listing Format

All listings use the established `<Listing>` XML tag format with **5 code blocks**:

````markdown
<Listing number="01-01" file="main" caption="Hello, World!">

```auto
fn main() {
    print("Hello, world!")
}
```

```rust
fn main() {
    println!("Hello, world!");
}
```

```python
def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
```

```c
#include <stdio.h>

int main(void) {
    printf("Hello, world!\n");
    return 0;
}
```

```typescript
function main(): void {
    console.log("Hello, world!");
}

main();
```

</Listing>
````

**Rule:** Every listing shows all 5 languages, always. No exceptions.

---

## 3. File Organization

```
tapl/
├── SUMMARY.md                              # Table of contents
├── ch00-introduction.md                     # English chapters
├── ch00-introduction.cn.md                  # Chinese chapters
├── ch01-getting-started.md
├── ch01-getting-started.cn.md
├── ...                                      # ch02-ch22 + appendix
├── appendix-a-keywords.md
├── appendix-a-keywords.cn.md
├── appendix-b-operators.md
├── appendix-b-operators.cn.md
├── appendix-c-transpiler-quick-ref.md
├── appendix-c-transpiler-quick-ref.cn.md
├── appendix-d-stdlib-index.md
├── appendix-d-stdlib-index.cn.md
└── listings/                                # Code examples
    ├── ch01/
    │   └── listing-01-01/
    │       ├── main.at              # Auto source
    │       ├── main.expected.rs     # Rust transpiler output
    │       ├── main.expected.py     # Python transpiler output
    │       ├── main.expected.c      # C transpiler output
    │       ├── main.expected.ts     # TypeScript transpiler output
    │       └── pac.at              # Package config
    ├── ch02/
    └── ...
```

**Rules:**

- Each chapter: one `.md` (English) + one `.cn.md` (Chinese)
- Sections within chapters use `##` headings
- Listings organized by chapter in `listings/` directory
- Every listing has 5 source files: `.at` + `.expected.rs` + `.expected.py` + `.expected.c` + `.expected.ts`

---

## 4. Chapter Structure

### Phase 1 — Auto as Script (Ch 0–5)

Auto as a friendly scripting language. All examples run on AutoVM. The tone is light and inviting — like Python or JavaScript tutorials. No type annotations on variables, no generic syntax, no `let`.

**Phase 1 rules:**

- Only `var` for variables (no `let` — immutability introduced in Phase 2)
- Function parameters have type hints; return types are inferred
- No generic syntax visible anywhere
- Collections use JSON-like arrays `[1, 2, 3]` and objects `{ name: "Alice" }`
- HashMaps and Sets work via full type inference — no `<K,V>` annotations
- AutoVM is the runtime

| Ch | English Title | Key Topics |
|----|--------------|------------|
| 0  | Introduction | What is Auto, AIOS philosophy, dual mode (VM/AOT), AI-native design, how this book works, the 5-language format |
| 1  | Getting Started | Installation (`autoc` + `autovm`), Hello World, REPL playground, basic expressions |
| 2  | Variables & Operators | `var x = 5` (no `let`), numbers, strings, booleans, operators — all type-inferred, zero explicit type annotations |
| 3  | Functions & Control Flow | `fn greet(name String) { ... }` (typed params, inferred returns), `if`/`else`, `while`, `for`/`in`, early returns, expression bodies |
| 4  | Collections & Nodes | JSON-like arrays, objects, hashmaps, sets via inference, `node` for linked/tree structures — no generics |
| 5  | Project: Guessing Game | Capstone — input handling, random numbers, loops, string conversion, combining Ch 1–4 |

### Phase 2 — Auto as System (Ch 6–14)

Auto "grows up." Explicit types, `let` for immutability, data containers, the full OOP system, references, memory, and generics. Rust and C become the primary comparison languages.

**Phase 2 rules:**

- `let` introduced as the immutable companion to `var`
- Full type annotations available everywhere
- Generic syntax `List<T>` introduced in Ch 13
- `type` keyword replaces anonymous objects
- References and memory model explored in depth

| Ch  | English Title | Key Topics |
|-----|--------------|------------|
| 6   | Types & `let` | Explicit type annotations, `let` (immutable) vs `var` (mutable), `type` for data containers, typed fields, default constructor |
| 7   | Enums & Pattern Matching | `enum`, sum types, `is` for matching, `on` blocks, destructuring, exhaustive matching |
| 8   | OOP Reshaped | The golden triangle: `is` (inheritance), `has` (composition + delegation), `spec` (contracts), `as` (implementation), `ext` (extension) |
| 9   | Error Handling | `?T` (optional), `!T` (error propagation), try/catch patterns, custom error types, the `!` operator |
| 10  | Packages & Modules | `automan`, `auto.toml`, `mod`/`use`, project structure, publishing packages |
| 11  | References & Pointers | `view T` (read-only), `mut T` (mutable ref), `*T` (raw pointer), borrowing rules, `&self` in methods |
| 12  | Memory & Ownership | Implicit move semantics, escape analysis, AutoFree, stack vs heap, lifetimes, zero-GC |
| 13  | Generics | Generic functions `fn foo<T>(x T)`, generic types `List<T>`, `spec` bounds, monomorphization, zero-cost abstraction |
| 14  | Project: File Processor | Capstone — CLI tool using types, enums, error handling, file I/O, generics for reusable components |

### Phase 3 — Auto as AIOS (Ch 15–22)

Full systems programming. Actor concurrency, async, comptime, and the capstone project. This is where Auto reveals its full power as an AI Operating System.

| Ch  | English Title | Key Topics |
|-----|--------------|------------|
| 15  | Actor Concurrency | `task`, `spawn`, mailboxes, `send`, state isolation (`task.ram`), message passing, `main` as primary actor |
| 16  | Async with `~T` | `~T` blueprints, `on` blocks for async handlers, futures, composing async operations |
| 17  | Smart Casts & Flow Typing | `if x is T` narrowing, union types `T | U`, flow-sensitive typing, type-safe dispatch |
| 18  | Testing | Unit tests, integration tests, `#[test]` attribute, test-driven development in Auto |
| 19  | Closures & Iterators | Closures, iterator chains (`.map()`, `.filter()`, `.fold()`), lazy evaluation, functional patterns |
| 20  | Comptime & Metaprogramming | `#[]` compile-time directives, macros, AOT-stage logic, conditional compilation, platform detection |
| 21  | Standard Library Tour | I/O, networking, serialization, collections deep dive, string processing, time/date |
| 22  | Project: Multi-user Chat Server | Capstone — actors for user sessions, async message routing, networking, combining everything |

### Appendices

| App | Title | Content |
|-----|-------|---------|
| A   | Keyword Reference | Every Auto keyword with syntax and one-line description |
| B   | Operator Table | All operators, precedence, associativity |
| C   | Transpiler Quick-Ref | Auto ↔ Rust ↔ Python ↔ C ↔ TypeScript mapping tables |
| D   | Standard Library Index | Function/type listing by module |

---

## 5. Narrative Arc

The book follows a deliberate "growing up" narrative:

1. **Phase 1 (Script):** "You already know how to program — here's Auto as a friendly scripting language." Python and TypeScript listings feel natural. C and Rust listings show the contrast — "see how simple Auto is?"

2. **Phase 2 (System):** "Now let's understand what Auto really is." The language gains explicit types, ownership, memory management. Rust and C listings become more relevant. Python/TypeScript listings sometimes show limitations ("this pattern doesn't translate directly").

3. **Phase 3 (AIOS):** "Now let's see what Auto can do that others can't." Actors, comptime, and the full AIOS vision. This is Auto's unique territory — the other languages are shown for comparison but Auto clearly shines.

---

## 6. Reference Books

Modeled on the structure and tone of:

- *The Rust Programming Language* (Klabnik & Nichols) — chapter pacing, project integration
- *The C Programming Language* (Kernighan & Ritchie) — concise, example-driven exposition
- *A Byte of Python* (Swaroop C H) — beginner-friendly scripting tone (Phase 1)
- *Modern C* (Jens Gustedt) — rigorous systems coverage (Phase 2–3)

---

## 7. Total Scope

- **23 chapters** (ch00–ch22) + **4 appendices**
- **3 capstone projects** (Guessing Game, File Processor, Chat Server)
- **Estimated ~200+ code listings**, each in 5 languages
- **~1000+ code files** in `listings/` directory
- Full bilingual coverage (EN + CN)
