# 模块

Auto 有自己基于 `mod` 和 `use` 关键字的模块系统，与 TypeScript 的 ES
Module 系统截然不同。本章涵盖两种方式。

## Auto 模块

Auto 使用 `mod` 声明组织代码，使用 `use` 导入符号：

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

`mod math` 声明告诉转译器查找名为 `math` 的模块（可以是文件 `math.at`
或目录 `math/mod.at`）。该模块导出的所有符号都可以通过 `math.` 命名空间
访问。

### 模块文件结构

Auto 模块遵循基于文件的约定：

- `math.at` — 单文件模块
- `math/mod.at` — 目录模块，包含子模块如 `math/ops.at`

### 重导出

模块可以重导出符号：

```auto
// math/mod.at
mod ops
pub use ops.add
pub use ops.subtract
```

`pub use` 指令使 `add` 和 `subtract` 对 `math` 模块的使用者可用，而不会
暴露内部的 `ops` 子模块。

## TypeScript：ES 模块语法

TypeScript 使用 ES 模块语法进行导入和导出：

### 命名导出

```typescript
// utils.ts
export function add(a: number, b: number): number {
    return a + b;
}

export const PI = 3.14159;
```

### 命名导入

```typescript
// main.ts
import { add, PI } from "./utils";

console.log(add(1, 2));
console.log(PI);
```

### 命名空间导入

```typescript
import * as utils from "./utils";

console.log(utils.add(1, 2));
console.log(utils.PI);
```

### 默认导出

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

每个文件最多只能有一个默认导出。通常优先使用命名导出，以保持一致性和
重构安全性。

## TypeScript：`import type`

当你只需要类型（不需要值）时，使用 `import type` 明确意图，并确保导入在
编译时被擦除：

```typescript
// 仅限 TypeScript
import type { User, Config } from "./types";

function greet(user: User): void {
    console.log(`Hello, ${user.name}`);
}
```

你也可以混合类型导入和值导入：

```typescript
// 仅限 TypeScript
import { processData, type Result } from "./processor";
```

这将 `processData` 作为运行时值导入，将 `Result` 作为仅类型导入。

## TypeScript：CommonJS vs ESM

TypeScript 可以同时输出 CommonJS 和 ES 模块格式：

### CommonJS（Node.js 默认）

```typescript
// CommonJS 输出
const utils = require("./utils");
console.log(utils.add(1, 2));
```

### ES 模块

```typescript
// ESM 输出
import { add } from "./utils.js";
console.log(add(1, 2));
```

输出格式由 `tsconfig.json` 控制：

```json
{
    "compilerOptions": {
        "module": "NodeNext",
        "moduleResolution": "NodeNext"
    }
}
```

面向 Node.js 的现代 TypeScript 项目应该使用 `"NodeNext"` 作为 `module` 和
`moduleResolution` 的值。浏览器项目应使用 `"ESNext"`。

## TypeScript：`.d.ts` 文件

声明文件（`.d.ts`）描述 JavaScript 代码的类型，不包含任何运行时逻辑：

```typescript
// types.d.ts
declare module "external-lib" {
    export function parse(input: string): object;
    export function stringify(data: object): string;
}
```

声明文件会被 TypeScript 编译器自动拾取。你也可以使用三斜线指令引用它们：

```typescript
/// <reference path="./types.d.ts" />
```

### `declare global`

使用 `declare global` 在模块内扩展全局类型：

```typescript
// 仅限 TypeScript
declare global {
    interface Array<T> {
        myCustomMethod(): T;
    }
}
```

## TypeScript：`tsconfig.json` 模块选项

`tsconfig.json` 中与模块相关的主要选项：

| Option | 描述 |
|--------|------|
| `"module": "ESNext"` | 输出 ES 模块 |
| `"module": "NodeNext"` | 使用 Node.js 模块解析（推荐） |
| `"moduleResolution": "NodeNext"` | 匹配 Node.js 解析算法 |
| `"moduleResolution": "Bundler"` | 使用打包器感知的解析 |
| `"isolatedModules": true` | 确保每个文件可以独立转译 |
| `"esModuleInterop": true` | 允许从 CommonJS 模块默认导入 |
| `"verbatimModuleSyntax": true` | 强制仅类型导入使用显式 `type` |
| `"paths": { "@/*": ["src/*"] }` | 导入路径别名 |

现代项目的 `tsconfig.json` 示例：

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

## 快速参考

| TypeScript | Auto | 描述 |
|-----------|------|------|
| `import { x } from "./mod"` | `mod modname` | 导入模块 |
| `import * as x from "./mod"` | `mod modname` | 命名空间导入 |
| `export function f() { }` | (所有 `pub` 符号) | 导出 |
| `export default X` | -- | 默认导出（仅限 TypeScript） |
| `import type { T }` | -- | 仅类型导入（仅限 TypeScript） |
| `require("./mod")` | -- | CommonJS 导入（仅限 TypeScript） |
| `.d.ts` 文件 | -- | 类型声明（仅限 TypeScript） |
| `tsconfig.json` | -- | 编译器配置（仅限 TypeScript） |
| `pub use x` | `pub use x` | 重导出 |
