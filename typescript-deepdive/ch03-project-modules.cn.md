# 项目与模块

本章涵盖 TypeScript 和 Auto 如何将代码组织为项目和模块——大型程序的
基础构建块。

## 编译上下文

在 TypeScript 中，**编译上下文**由 `tsconfig.json` 定义。它告诉编译器
包含哪些文件、使用什么编译器选项、在哪里找类型声明：

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

在 Auto 中，编译上下文由 `pac.at` 定义：

```auto
// pac.at
name: "my-app"
version: "0.1.0"
lang: "ts"

app("my-app") {}
```

Auto 更加固执己见——没有 `compilerOptions` 的等价物，因为 Auto 内置了
合理的默认值（严格类型、块作用域、默认不可变）。

## 文件发现：显式 vs Glob

TypeScript 在 `tsconfig.json` 中使用 glob 模式发现文件：

```json
{
  "include": ["src/**/*"],
  "exclude": ["src/**/*.spec.ts"]
}
```

Auto 采取相反的方式——**每个模块必须用 `mod` 显式声明**。没有基于
glob 的自动包含，这消除了整类配置错误（意外包含测试文件、构建
产物等）：

```auto
// main.at — 入口文件
mod utils
mod models

fn main() {
    // 模块因为上面声明了所以可用
}
```

## 模块：文件作用域

在 TypeScript 中，文件默认共享**全局命名空间**。只有当文件包含
`import` 或 `export` 时才成为模块：

```typescript
// TypeScript: global.ts — 共享全局命名空间
var globalVar = 42;

// TypeScript: module.ts — 文件模块（有 import）
import { something } from "./other";
export var local = 123;
```

Auto **设计上就是纯文件模块**。每个 `.at` 文件都是有自己作用域的模块。
名称必须用 `use` 显式导入：

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

## 导入和导出

TypeScript 使用 `import`/`export`：

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

Auto 使用 `use` 导入，通过模块系统组织：

```auto
// Auto
use utils::add

fn main() {
    let result = add(1, 2)
}
```

## 声明空间

TypeScript 有两个声明空间：**类型**（用于注解）和**变量**（用于运行时值）。
`interface` 仅存在于类型空间；`class` 跨越两者：

```typescript
// TypeScript
interface Foo {}        // 仅类型空间
var x = Foo;            // 错误 — 不在变量空间

class Bar {}           // 两个空间
var y: Bar;             // OK — 类型空间
var z = Bar;            // OK — 变量空间
```

Auto 统一了这些——`spec`、`type`、`enum`、`fn`、`let`、`var` 声明都在
其模块作用域中可用。类型可用作注解，值可用作运行时，无需区分。

## 命名空间

TypeScript 支持 `namespace` 块进行逻辑分组：

```typescript
// TypeScript
namespace Utility {
    export function log(msg: string) { console.log(msg); }
    namespace Inner {
        export function helper() { }
    }
}
```

Auto 没有内联的命名空间块。组织通过 `mod` 系统实现——每个模块
在自己的文件中，层级命名（`mod utils::http`）提供类似命名空间的分组：

```auto
// Auto — 通过 mod 层级组织
mod utils
mod utils::http
mod utils::json
```

## 快速参考

| TypeScript | Auto | 说明 |
|-----------|------|------|
| `tsconfig.json` | `pac.at` | Auto 更固执己见 |
| `"include": ["src/**/*"]` | `mod utils` | Auto 要求显式声明 |
| `export` | 默认公开 | Auto 导出所有顶层声明 |
| `import { x } from "./y"` | `use y::x` | 不同语法，相同概念 |
| `namespace X { }` | 不需要 | `mod` 层级提供组织 |
| 全局命名空间模式 | 不可用 | Auto 是纯文件模块 |
