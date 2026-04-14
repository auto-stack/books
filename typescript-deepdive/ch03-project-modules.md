# Project & Modules

This chapter covers how TypeScript and Auto organize code into projects and
modules — the fundamental building blocks of large-scale programs.

## Compilation Context

In TypeScript, a **compilation context** is defined by `tsconfig.json`. It
tells the compiler which files to include, what compiler options to use, and
where to find type declarations:

```json
{
  "compilerOptions": {
    "target": "es2020",
    "module": "esnext",
    "strict": true
  },
  "include": ["src/**/*"]
}
```

In Auto, the compilation context is defined by `pac.at`:

```auto
// pac.at
name: "my-app"
version: "0.1.0"
lang: "ts"

app("my-app") {}
```

Auto is more opinionated — there is no equivalent of `compilerOptions`
because Auto bakes in sensible defaults (strict types, block scoping,
immutability-by-default).

## File Discovery: Explicit vs Glob

TypeScript uses glob patterns in `tsconfig.json` to discover files:

```json
{
  "include": ["src/**/*"],
  "exclude": ["src/**/*.spec.ts"]
}
```

Auto takes the opposite approach — **every module must be explicitly declared**
with `mod`. There is no glob-based auto-inclusion, which eliminates entire
categories of configuration bugs (accidentally including test files,
build artifacts, etc.):

```auto
// main.at — the entry point
mod utils
mod models

fn main() {
    // modules are available because they were declared above
}
```

## Modules: File Scope

In TypeScript, files share a **global namespace** by default. A file only
becomes a module when it contains an `import` or `export`:

```typescript
// TypeScript: global.ts — shared global namespace
var globalVar = 42;

// TypeScript: module.ts — file module (has import)
import { something } from "./other";
export var local = 123;
```

Auto is **file-module-only** by design. Every `.at` file is a module with
its own scope. Names must be explicitly imported with `use`:

```auto
// Auto: utils.at
fn add(a int, b int) int {
    a + b
}
```

```auto
// Auto: main.at
mod utils

fn main() {
    let result = utils.add(1, 2)
    print(result)
}
```

## Imports and Exports

TypeScript uses `import`/`export`:

```typescript
// TypeScript
// math.ts
export function add(a: number, b: number): number {
    return a + b;
}

// main.ts
import { add } from "./math";
add(1, 2);
```

Auto uses `use` for importing and Auto's module system for organizing:

```auto
// Auto
use utils::add

fn main() {
    let result = add(1, 2)
}
```

## Declaration Spaces

TypeScript has two declaration spaces: **type** (for annotations) and
**variable** (for runtime values). An `interface` exists only in the type
space; a `class` straddles both:

```typescript
// TypeScript
interface Foo {}        // type space only
var x = Foo;            // ERROR — not in variable space

class Bar {}           // both spaces
var y: Bar;             // OK — type space
var z = Bar;            // OK — variable space
```

Auto unifies these — `spec`, `type`, `enum`, `fn`, `let`, `var` declarations
are all available in their module scope. Types are usable as annotations
and values are usable at runtime without distinction.

## Namespaces

TypeScript supports `namespace` blocks for logical grouping:

```typescript
// TypeScript
namespace Utility {
    export function log(msg: string) { console.log(msg); }
    namespace Inner {
        export function helper() { }
    }
}
```

Auto does not have inline namespace blocks. Organization is achieved
through the `mod` system — each module lives in its own file, and
hierarchical naming (`mod utils::http`) provides namespace-like grouping:

```auto
// Auto — organized via mod hierarchy
mod utils
mod utils::http
mod utils::json
```

## Quick Reference

| TypeScript | Auto | Notes |
|-----------|------|-------|
| `tsconfig.json` | `pac.at` | Auto is more opinionated |
| `"include": ["src/**/*"]` | `mod utils` | Auto requires explicit declarations |
| `export` | Public by default | Auto exports all top-level declarations |
| `import { x } from "./y"` | `use y::x` | Different syntax, same concept |
| `namespace X { }` | Not needed | `mod` hierarchy provides organization |
| Global namespace mode | Not available | Auto is file-module-only |
