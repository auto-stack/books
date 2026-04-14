# Modules

Auto has its own module system based on `mod` and `use` keywords, which is
quite different from TypeScript's ES Module system. This chapter covers both
approaches.

## Auto Modules

Auto organizes code into modules using `mod` declarations and imports symbols
with `use`:

```auto
mod math

fn main() {
    print(math.add(1, 2))
    print(math.PI)
}
```

```typescript
import { add, PI } from "./math";

function main(): void {
    console.log(add(1, 2));
    console.log(PI);
}

main();
```

The `mod math` declaration tells the transpiler to look for a module named
`math` (either a file `math.at` or a directory `math/mod.at`). All exported
symbols from that module become available under the `math.` namespace.

### Module File Structure

Auto modules follow a file-based convention:

- `math.at` — a single-file module
- `math/mod.at` — a directory module with sub-modules like `math/ops.at`

### Re-exporting

Modules can re-export symbols:

```auto
// math/mod.at
mod ops
pub use ops.add
pub use ops.subtract
```

The `pub use` directive makes `add` and `subtract` available to consumers of
the `math` module without exposing the internal `ops` sub-module.

## TypeScript: ES Module Syntax

TypeScript uses ES Module syntax for importing and exporting:

### Named Exports

```typescript
// utils.ts
export function add(a: number, b: number): number {
    return a + b;
}

export const PI = 3.14159;
```

### Named Imports

```typescript
// main.ts
import { add, PI } from "./utils";

console.log(add(1, 2));
console.log(PI);
```

### Namespace Imports

```typescript
import * as utils from "./utils";

console.log(utils.add(1, 2));
console.log(utils.PI);
```

### Default Exports

```typescript
// logger.ts
export default class Logger {
    log(msg: string): void {
        console.log(msg);
    }
}
```

```typescript
import Logger from "./logger";

const logger = new Logger();
logger.log("hello");
```

Each file can have at most one default export. Named exports are generally
preferred for consistency and refactoring safety.

## TypeScript: `import type`

When you only need types (not values), use `import type` to make the intent
clear and to ensure the import is erased at compile time:

```typescript
// TypeScript only
import type { User, Config } from "./types";

function greet(user: User): void {
    console.log(`Hello, ${user.name}`);
}
```

You can also mix type-only and value imports:

```typescript
// TypeScript only
import { processData, type Result } from "./processor";
```

This imports `processData` as a runtime value and `Result` as a type-only
import.

## TypeScript: CommonJS vs ESM

TypeScript can target both CommonJS and ES Module output formats:

### CommonJS (Node.js default)

```typescript
// CommonJS output
const utils = require("./utils");
console.log(utils.add(1, 2));
```

### ES Modules

```typescript
// ESM output
import { add } from "./utils.js";
console.log(add(1, 2));
```

The output format is controlled by `tsconfig.json`:

```json
{
    "compilerOptions": {
        "module": "NodeNext",
        "moduleResolution": "NodeNext"
    }
}
```

Modern TypeScript projects targeting Node.js should use `"NodeNext"` for
both `module` and `moduleResolution`. Browser projects should use `"ESNext"`.

## TypeScript: `.d.ts` Files

Declaration files (`.d.ts`) describe the types of JavaScript code without
containing any runtime logic:

```typescript
// types.d.ts
declare module "external-lib" {
    export function parse(input: string): object;
    export function stringify(data: object): string;
}
```

Declaration files are automatically picked up by the TypeScript compiler.
You can also use triple-slash directives to reference them:

```typescript
/// <reference path="./types.d.ts" />
```

### `declare global`

Use `declare global` to augment global types from within a module:

```typescript
// TypeScript only
declare global {
    interface Array<T> {
        myCustomMethod(): T;
    }
}
```

## TypeScript: `tsconfig.json` Module Options

Key module-related options in `tsconfig.json`:

| Option | Description |
|--------|-------------|
| `"module": "ESNext"` | Output ES modules |
| `"module": "NodeNext"` | Use Node.js module resolution (recommended) |
| `"moduleResolution": "NodeNext"` | Match Node.js resolution algorithm |
| `"moduleResolution": "Bundler"` | Use bundler-aware resolution |
| `"isolatedModules": true` | Ensure each file can be transpiled independently |
| `"esModuleInterop": true` | Allow default imports from CommonJS modules |
| `"verbatimModuleSyntax": true` | Enforce explicit `type` on type-only imports |
| `"paths": { "@/*": ["src/*"] }` | Path aliases for imports |

Example `tsconfig.json` for a modern project:

```json
{
    "compilerOptions": {
        "target": "ES2022",
        "module": "NodeNext",
        "moduleResolution": "NodeNext",
        "strict": true,
        "isolatedModules": true,
        "verbatimModuleSyntax": true
    }
}
```

## Quick Reference

| TypeScript | Auto | Description |
|-----------|------|-------------|
| `import { x } from "./mod"` | `mod modname` | Import module |
| `import * as x from "./mod"` | `mod modname` | Namespace import |
| `export function f() { }` | (all `pub` symbols) | Export |
| `export default X` | -- | Default export (TS-only) |
| `import type { T }` | -- | Type-only import (TS-only) |
| `require("./mod")` | -- | CommonJS import (TS-only) |
| `.d.ts` files | -- | Type declarations (TS-only) |
| `tsconfig.json` | -- | Compiler config (TS-only) |
| `pub use x` | `pub use x` | Re-export |
