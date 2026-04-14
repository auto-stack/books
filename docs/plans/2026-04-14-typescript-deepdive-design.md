# TypeScript DeepDive → Auto Book Design

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Create a complete Auto language adaptation of the "TypeScript DeepDive" book, placed at `typescript-deepdive/`.

**Architecture:** Follow the same format as the existing Handbook (`typescript/`) and Rust book (`rust/`): each chapter is a `.md` (EN) + `.cn.md` (CN) pair with side-by-side Auto/TypeScript code blocks and verifiable listings.

**Tech Stack:** Auto language, a2ts transpiler, `auto b` build system, Python sync script

---

## Positioning

- **Handbook** (`typescript/`): Quick-start reference — syntax, basic concepts, cheat-sheet style
- **DeepDive** (`typescript-deepdive/`): In-depth understanding — type system theory, design patterns, best practices, compiler architecture
- Both are **complete, standalone books** — DeepDive covers fundamentals too, but with deeper treatment

## Chapter Plan (16 chapters)

| Ch | Title | Source | Strategy |
|----|-------|--------|----------|
| 00 | Why Types | why-typescript | Auto perspective on type system value |
| 01 | Language Basics | javascript/recap + future-js | Map JS quirks to Auto design choices |
| 02 | Modern Language Features | classes, arrow, destructuring, spread, iterators | Auto equivalents: `type`/`ext`/closures/`for in` |
| 03 | Project & Modules | project/ | Auto `pac.at`/`use`/`mod` vs TS tsconfig/modules |
| 04 | Type System Basics | type-system | Primitives, arrays, interfaces, aliases |
| 05 | Interfaces & Enums | interfaces, enums | Auto `spec`/`enum` vs TS |
| 06 | Functions | functions, callable | Auto `fn`/closures/function types |
| 07 | Generics & Inference | generics, type-inference | Auto `<T>` constraints, inference rules |
| 08 | Type Compatibility | type-compatibility | Structural typing, covariance/contravariance |
| 09 | Type Guards & Exhaustiveness | typeGuard, literal-types, never | Auto `is` pattern matching vs TS guards |
| 10 | Discriminated Unions & Immutability | discriminated-unions, readonly | Auto enum + `is` vs TS discriminated unions |
| 11 | Index Signatures & Type Operators | index-signatures, moving-types | `has` composition, keyof/typeof as TS-only |
| 12 | Mixins & Error Handling | mixins, exceptions | Auto `has`/`ext` vs TS mixin patterns |
| 13 | Errors & Diagnostics | errors/ | Auto compiler errors vs TS error messages |
| 14 | Design Patterns | tips/ | Singleton, currying, event emitter in Auto |
| 15 | Compiler Architecture | compiler/ | Auto's lexer→parser→binder→checker→emitter |

## Skipped Chapters (pure JS/TS toolchain)

- QuickStarts (Node/Browser/Library)
- JSX/React
- NPM
- Testing (Jest/Cypress)
- Tools (Prettier/Husky/ESLint/Changelog)
- Options (noImplicitAny/strictNullChecks)
- @types / Ambient Declarations / lib.d.ts / Freshness
- jQuery tips, barrel files, export default

## Code Example Strategy

1. **Auto has equivalent**: Side-by-side Auto + TS code blocks
2. **Auto planned but not yet**: TS code + note about Auto's planned approach
3. **TS-only concept**: "TypeScript Only" code block with brief explanation

## File Structure

```
typescript-deepdive/
├── ch00-why-types.md / .cn.md
├── ch01-basics.md / .cn.md
├── ...
├── ch15-compiler.md / .cn.md
├── listings/
│   ├── ch00/
│   │   └── listing-00-01/
│   │       ├── main.at
│   │       ├── pac.at
│   │       └── main.expected.ts
│   ├── ch01/
│   │   └── ...
│   └── ...
└── stdlib/
    └── runtime.ts (shared with typescript/)
```

## Execution Order

### Batch 1: Setup + ch00-ch03 (4 chapters)
- Create directory structure, copy runtime.ts symlink
- Write ch00-ch03 (introductory chapters, lighter on listings)

### Batch 2: ch04-ch07 (4 chapters)
- Core type system chapters, heaviest listings
- Verify all listings compile with `auto b`

### Batch 3: ch08-ch11 (4 chapters)
- Advanced type system chapters
- Some content may be TS-only (covariance, index signatures)

### Batch 4: ch12-ch15 (4 chapters)
- Patterns, errors, compiler architecture
- Lighter on listings, heavier on prose

### Final: Sync, update README, commit

## Verification

After each batch:
- All listings compile: `auto b -d <listing-dir>`
- `python scripts/sync_deepdive_listings.py --dry-run`
- Manual review for Auto syntax correctness
