# Auto Book from TypeScript Handbook — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a TypeScript-focused Auto book at `d:/autostack/book/typescript/`, parallel to the existing Rust book, based on the TypeScript Handbook v2.

**Architecture:** Side-by-side Auto/TypeScript code examples. Auto code transpiles to TypeScript via a2ts. TS-only features (Conditional Types, Mapped Types, Template Literal Types) shown as inline TS blocks with callout notes.

**Tech Stack:** Auto language, a2ts transpiler, TypeScript, mdBook format

---

## Context

The Rust book (`d:/autostack/book/rust/`) has 21 chapters with bilingual (EN+CN) output. Now we need a parallel book targeting TypeScript/JavaScript developers, using the official TypeScript Handbook v2 as source material. The a2ts transpiler is mature (29 test cases, full feature parity with a2r for core constructs).

## Design Decisions

1. **Chapter numbering: Restart from 01** — standalone book, different audience
2. **Output directory: `d:/autostack/book/typescript/`**
3. **Sync script: New `scripts/sync_ts_listings.py`** — adapted from `sync_listings.py` with 4-5 line changes (book dir, `.expected.ts`, ` ```typescript ` code blocks)
4. **TS-only features: Inline ` ```typescript ` blocks** (no listings) with callout: `> **TypeScript-only**: This feature has no Auto equivalent.`

## Directory Structure

```
d:/autostack/book/typescript/
  SUMMARY.md
  ch00-introduction.md / .cn.md
  ch01-basics.md / .cn.md
  ch02-everyday-types.md / .cn.md
  ch03-narrowing.md / .cn.md
  ch04-functions.md / .cn.md
  ch05-object-types.md / .cn.md
  ch06-creating-types.md / .cn.md
  ch07-type-operators.md / .cn.md
  ch08-classes.md / .cn.md
  ch09-modules.md / .cn.md
  ch10-errors.md / .cn.md
  listings/
    ch01/ ... ch10/
      listing-XX-YY/
        main.at
        main.expected.ts
        pac.at
```

## Auto ↔ TypeScript Mapping Reference

Source: `d:/autostack/auto-lang/crates/auto-lang/src/trans/ts_types.rs`, `ts_stmt.rs`, `ts_expr.rs`

| Auto | TypeScript | Notes |
|------|-----------|-------|
| `let x = 5` | `const x = 5` | immutable |
| `var x = 5` | `let x = 5` | mutable |
| `int`, `float`, `byte` | `number` | all numeric → number |
| `bool` | `boolean` | |
| `str`, `String` | `string` | |
| `[]T` | `T[]` | arrays |
| `Map<K, V>` | `Record<K, V>` | |
| `?T` (Option) | `T \| null` | nullable |
| `!T` (Result) | `T \| Error` | error union |
| `type Name { fields }` | `class Name { fields; constructor(...) }` | |
| `spec Name { methods }` | `interface Name { methods }` | |
| `type Child as Spec { }` | `class Child implements Spec { }` | |
| `type Child extends Parent { }` | `class Child extends Parent { }` | |
| `enum Name { A B C }` | `const enum Name { A, B, C }` | scalar |
| `enum Name { A int, B str }` | discriminated union + factory | homogeneous |
| `fn name(params) ret { }` | `function name(params): ret { }` | |
| `(a int, b int) => expr` | `(a: number, b: number) => expr` | closures |
| `is x { A => ... }` | `switch (x) { case A: ... }` | pattern matching |
| `for x in arr { }` | `for (const x of arr) { }` | for-each |
| `for x in 0..10 { }` | `for (let x = 0; x < 10; x++) { }` | range |
| `for cond { }` | `while (cond) { }` | while |
| `print("msg")` | `console.log("msg")` | via runtime prelude |
| `f"text ${x}"` | `` `text ${x}` `` | template literals |
| `Name(args)` | `new Name(args)` | constructor call |
| `self.field` | `this.field` | |

## Twoslash Stripping Rules

The TS Handbook uses `ts twoslash` annotations. Strip all:
- `// @errors: ...` — expected error codes
- `// ^?` — hover type inspection
- `// ---cut---` — code folding
- `// @noErrors`, `// @noUnusedLocals`, etc. — compiler config
- `// @showEmit`, `// @target: ...` — emit control
- YAML frontmatter blocks at file tops

## Chapter Plan (11 chapters)

### ch00 — Introduction

**Source:** `The Handbook.md` (59 lines)
**Listings:** None (pure prose)

Adapt the handbook intro. Target JS/TS developers. Explain Auto's value prop: less syntax, same type safety, transpiles to TypeScript via a2ts.

---

### ch01 — Basics

**Source:** `Basics.md` (440 lines)
**Listings:**

| # | .at concept | Auto | TS concept |
|---|-------------|------|-----------|
| 01-01 | Hello world | `fn main() { print("Hello, world!") }` | console.log |
| 01-02 | Explicit types | `fn greet(person str, date Date) { ... }` | Parameter type annotations |
| 01-03 | Type inference | `let msg = "hello"` | Inferred types |

**TS-only (inline):** `tsc` compiler, `tsconfig.json`, `strict` flag, `noImplicitAny`, `strictNullChecks`, downleveling

---

### ch02 — Everyday Types

**Source:** `Everyday Types.md` (737 lines)
**Listings:**

| # | .at concept | Auto | TS concept |
|---|-------------|------|-----------|
| 02-01 | Primitives | `str`/`int`/`bool` | string/number/boolean |
| 02-02 | Arrays | `[]int`, `[]str` | T[] |
| 02-03 | Object types | `type User { name str, age int }` | class/interface |
| 02-04 | Functions | `fn add(a int, b int) int` | Function annotations |
| 02-05 | Optional params | `fn greet(name str, title? str)` | Optional parameters |
| 02-06 | Nullable | `let name ?str = None` | null \| undefined |

**TS-only:** `any`, tuple types `[number, string]`, literal types, `readonly` arrays

---

### ch03 — Narrowing

**Source:** `Narrowing.md` (773 lines)
**Listings:**

| # | .at concept | Auto | TS concept |
|---|-------------|------|-----------|
| 03-01 | Pattern matching | `x is Some(v) => ... None => ...` | typeof narrowing |
| 03-02 | Truthiness | `if value { ... }` | Truthiness narrowing |
| 03-03 | Type narrowing | `value is int => ... str => ...` | Union narrowing |

**TS-only:** `typeof` guard, `instanceof`, `in` operator, assignment narrowing, type predicates (`x is number`)
**Note:** This is the hardest chapter. TS narrowing is tied to union types. Auto uses `is` pattern matching instead. Reframe as "Type Guards and Pattern Matching."

---

### ch04 — More on Functions

**Source:** `More on Functions.md` (889 lines)
**Listings:**

| # | .at concept | Auto | TS concept |
|---|-------------|------|-----------|
| 04-01 | Closures | `(a int, b int) => a + b` | Arrow functions |
| 04-02 | Generic fn | `fn identity<T>(arg T) T { arg }` | Generic functions |
| 04-03 | Generic constraints | `fn longest<T>(a T, b T) T` where T has `.len()` | Constraints |
| 04-04 | Function types | `fn apply(fn (int) => int, x int) int` | Function type params |
| 04-05 | Optional params | `fn greet(name str, age? int)` | Optional params |
| 04-06 | Rest params | `fn sum(nums ...int) int` | Rest parameters |

**TS-only:** Call signatures, construct signatures, overloads, `this` parameter typing, assertion functions

---

### ch05 — Object Types

**Source:** `Object Types.md` (1111 lines)
**Listings:**

| # | .at concept | Auto | TS concept |
|---|-------------|------|-----------|
| 05-01 | Interface | `spec Greetable { fn greet() str }` | interface |
| 05-02 | Implements | `type User as Greetable { ... }` | implements |
| 05-03 | Inheritance | `type Dog extends Animal { breed str }` | extends |
| 05-04 | Generic types | `type Box<T> { value T }` | Generic classes |
| 05-05 | Optional fields | `type Config { host str, port? int }` | Optional properties |
| 05-06 | Index access | `type Dict { fn get(key str) ?str }` | Index signatures |

**TS-only:** `interface` vs `type` distinction, intersection types (`&`), union of objects, `readonly` modifier, excess property checking

---

### ch06 — Creating Types from Types

**Source:** `Type Manipulation/_Creating Types from Types.md` + `Generics.md`
**Listings:**

| # | .at concept | Auto | TS concept |
|---|-------------|------|-----------|
| 06-01 | Generic fn | `fn identity<T>(arg T) T { arg }` | Generics basics |
| 06-02 | Generic type | `type Box<T> { value T }` | Generic types |
| 06-03 | Generic class method | `ext Box<T> { fn get() T { self.value } }` | Generic methods |
| 06-04 | Multiple type params | `type Pair<T, U> { first T, second U }` | Multiple generics |

**TS-only:** `ReturnType<T>`, `Parameters<T>`, built-in utility types

---

### ch07 — Type Operators

**Source:** `Keyof Type Operator.md`, `Typeof Type Operator.md`, `Indexed Access Types.md`
**Listings:**

| # | .at concept | Auto | TS concept |
|---|-------------|------|-----------|
| 07-01 | Object access | `person.name` | Property access |
| 07-02 | Type-safe lookup | `fn get_field(obj, key str)` | Dynamic access pattern |

**TS-only (most of chapter):** `keyof`, `typeof` type operator, Indexed Access Types `Type["property"]` — these are pure type-level features with no Auto equivalent

---

### ch08 — Classes

**Source:** `Classes.md` (1470 lines)
**Listings:**

| # | .at concept | Auto | TS concept |
|---|-------------|------|-----------|
| 08-01 | Class basics | `type Point { x float, y float }` | Fields |
| 08-02 | Methods | `ext Point { fn distance(self) float { ... } }` | Instance methods |
| 08-03 | Inheritance | `type Dog extends Animal { ... }` | extends |
| 08-04 | Implements | `type Dog as Runnable { ... }` | implements |
| 08-05 | Constructor | `type User { name str, fn init(name str) { self.name = name } }` | constructor |
| 08-06 | Static members | `fn User.create() User { ... }` | static |

**TS-only:** Accessors (get/set), abstract classes, private/protected/public modifiers, class method parameter bivariance, constructor signatures in type positions

---

### ch09 — Modules

**Source:** `Modules.md` (407 lines) + `Type Declarations.md` (100 lines)
**Listings:**

| # | .at concept | Auto | TS concept |
|---|-------------|------|-----------|
| 09-01 | Exports | `fn add(a int, b int) int { a + b }` in separate file | Named exports |
| 09-02 | Imports | `use utils` / `use utils::add` | ES module imports |

**TS-only (most of chapter):** CommonJS vs ESM, `.d.ts` files, `@types` packages, `tsconfig.json` module options, type-only imports, ambient modules

---

### ch10 — Understanding Errors

**Source:** `Understanding Errors.md` (71 lines)
**Listings:** None (pure prose)

Explain TS error terminology ("assignable to", "not assignable"), error elaborations. Adapt for Auto compiler errors.

---

## Implementation Phases

### Phase 1: Infrastructure + ch00-ch02

**Step 1.1:** Create `d:/autostack/book/typescript/` directory structure
**Step 1.2:** Create `SUMMARY.md`, `ch00-introduction.md` + `.cn.md`
**Step 1.3:** Create `scripts/sync_ts_listings.py` (copy from sync_listings.py, change book dir + .expected.ts + ```typescript)
**Step 1.4:** Create ch01 listings (01-01 through 01-03) + `ch01-basics.md` + `.cn.md`
**Step 1.5:** Create ch02 listings (02-01 through 02-06) + `ch02-everyday-types.md` + `.cn.md`
**Step 1.6:** Run `sync_ts_listings.py --dry-run`, verify, commit

### Phase 2: ch03-ch05

**Step 2.1:** Create ch03 listings + `ch03-narrowing.md` + `.cn.md`
**Step 2.2:** Create ch04 listings + `ch04-functions.md` + `.cn.md`
**Step 2.3:** Create ch05 listings + `ch05-object-types.md` + `.cn.md`
**Step 2.4:** Sync + commit

### Phase 3: ch06-ch08

**Step 3.1:** Create ch06 listings + `ch06-creating-types.md` + `.cn.md`
**Step 3.2:** Create ch07 listings + `ch07-type-operators.md` + `.cn.md`
**Step 3.3:** Create ch08 listings + `ch08-classes.md` + `.cn.md`
**Step 3.4:** Sync + commit

### Phase 4: ch09-ch10

**Step 4.1:** Create ch09 listings + `ch09-modules.md` + `.cn.md`
**Step 4.2:** Create `ch10-errors.md` + `.cn.md` (no listings)
**Step 4.3:** Final sync + commit

---

## Risk Areas

1. **Narrowing (ch03):** TS narrowing is tied to union types; Auto uses `is` pattern matching. Needs reframing, not translation.
2. **Object Types (ch05):** `interface` vs `type` distinction differs from Auto's `spec` vs `type`.
3. **Type-level programming (ch06-07):** Conditional Types, Mapped Types, Template Literal Types have zero Auto equivalent — TS-only inline blocks only.
4. **Classes (ch08):** 1470 lines of source, Auto lacks accessors/abstract/private — significant trimming needed.
5. **a2ts gaps:** `readonly`, abstract classes, overloads may not be fully supported. Verify against 23 existing test cases before creating listings.

## Verification

1. `cd d:/autostack/auto-lang && cargo test -p auto-lang --lib a2ts` — all 22 a2ts tests pass
2. `python scripts/sync_ts_listings.py --dry-run` — listings in sync
3. Manual review of each chapter for Auto syntax correctness (Gotcha Checklist)
4. All inline TS blocks stripped of twoslash annotations

## Critical Reference Files

| File | Purpose |
|------|---------|
| `d:/autostack/auto-lang/crates/auto-lang/src/trans/ts_types.rs` | Authoritative Auto→TS type mapping |
| `d:/autostack/auto-lang/crates/auto-lang/src/trans/ts_stmt.rs` | Statement transpilation (type/spec/enum/fn) |
| `d:/autostack/auto-lang/crates/auto-lang/src/trans/ts_expr.rs` | Expression transpilation (closures/print/f-strings) |
| `d:/autostack/auto-lang/crates/auto-lang/test/a2ts/` | 23 test directories (.at + .expected.ts) |
| `d:/autostack/book/scripts/sync_listings.py` | Template for sync_ts_listings.py |
| `d:/autostack/book/rust/ch05-structs.md` | Reference for Listing tag format |
| `D:/github/.../handbook-v2/*.md` | Source material (18 files) |
