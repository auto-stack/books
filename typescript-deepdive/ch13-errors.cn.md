# 错误与诊断

类型系统的实用性取决于它产生的错误信息。TypeScript 在**清晰、可操作的诊断消息**方面投入了大量精力，不仅告诉你*哪里*出了问题，还告诉你*为什么*。理解如何阅读这些消息，以及 Auto 的设计如何从根源上消除整类错误，是你每天都在使用的实用技能。

## 阅读错误消息

TypeScript 错误消息有两种形式。**简洁形式**是你在终端 `tsc` 输出中看到的：

```
error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
```

**详细形式**是 IDE 悬停提示中显示的。它将简洁消息展开为完整的链：

```
Argument of type 'string' is not assignable to parameter of type 'number'.
  The call would succeed against 'number', but fails for 'string'.
```

链中的每一行都回答一个连续的**"为什么？"**问题。第一行陈述问题，第二行解释底层的类型关系。更长的链可能显示泛型实例化步骤或属性级别的不匹配。

关键洞察：**从上到下阅读错误链**。顶行命名错误；后续每一行提供一层额外的上下文。当链引用泛型类型或联合成员时，最后一行通常是最具操作性的——它准确告诉你哪些类型不兼容。

Auto 的错误消息遵循相同的理念。当类型不匹配发生时，编译器会解释期望类型、实际类型以及检测到不匹配的上下文。目标始终是让你尽快找到修复方案。

## TypeScript 错误代码

每个 TypeScript 错误都有一个数字代码。以下是你最常遇到的：

| 代码 | 含义 |
|------|------|
| `TS2304` | 找不到名称 |
| `TS2307` | 找不到模块 |
| `TS2322` | 类型不可赋值 |
| `TS2339` | 属性不存在于类型上 |
| `TS2345` | 参数类型不匹配 |
| `TS2532` | 对象可能为 `undefined` |

错误代码让错误变得**可搜索**。当你看到 `TS2532` 时，可以直接搜索它，而不需要用自然语言描述问题。这对不太常见的代码尤其有价值。

要抑制特定错误，TypeScript 提供了两个注释指令：

```typescript
// @ts-expect-error — 文档化下一行预期会产生错误
// @ts-ignore       — 静默抑制下一行的错误
```

优先使用 `@ts-expect-error` 而非 `@ts-ignore`。如果错误消失了（因为你修复了它），`@ts-expect-error` 本身会产生警告，提示你清理这个不再需要的指令。`@ts-ignore` 则会静默隐藏，可能掩盖真正的 bug。

Auto 使用错误代码也是出于同样的原因——它们使编译器错误可搜索且跨版本保持一致。

## 常见 TypeScript 错误

**TS2304 — 找不到名称。** 你忘记导入类型或变量，或者声明文件缺失。

```typescript
// Error: Cannot find name 'User'.
const user: User = { name: "Alice" };
```

修复：添加 `import { User } from "./models";`

**TS2307 — 找不到模块。** 模块路径错误，或者 `@types` 包未安装。

```typescript
// Error: Cannot find module 'lodash'.
import _ from "lodash";
```

修复：运行 `npm install @types/lodash` 或修正路径。

**TS2322 — 类型不匹配。** 最常见的 TypeScript 错误。你在期望某种类型的地方赋了另一种类型的值。

```typescript
let age: number = "twenty";  // TS2322: Type 'string' is not assignable to 'number'
```

修复：确保值与声明的类型匹配，或拓宽类型注解。

**TS2532 — 对象可能为 undefined。** `strictNullChecks` 标志会捕获潜在的 null 或 undefined 访问。

```typescript
function getLength(s: string | undefined): number {
    return s.length;  // TS2532: Object is possibly 'undefined'
}
```

修复：在访问属性之前添加 null 检查。

**TS2345 — 参数类型不匹配。** 函数参数与参数类型不匹配。

```typescript
function greet(name: string): void { console.log("Hello, " + name); }
greet(42);  // TS2345: Argument of type 'number' is not assignable to 'string'
```

修复：将参数转换为期望的类型。

## Auto 的诊断理念

Auto **通过设计**消除了整类错误：

- **没有 `any`** — 不存在"隐式 any"错误，因为类型始终是已知的或显式声明的。
- **没有 `null`/`undefined` 二元性** — 不存在"可能为 undefined"的错误。可选值使用 `?T`（`Option<T>`），强制显式处理。
- **显式 `self`** — 不存在"this 可能为 undefined"或"this 上下文丢失"的错误。方法显式声明 `self`，编译器确保它始终可用。
- **没有分号** — 不存在"缺少分号"或"多余分号"的解析错误。
- **`let` 默认不可变** — 重新赋值需要 `var`，这意味着意外的变异会在编译时被捕获。

当 Auto 确实报告错误时，它们遵循与 TypeScript 相同的链模式：错误代码、问题描述，以及解释类型为何不兼容的上下文。区别在于 TypeScript 开发者每天遇到的许多错误在 Auto 中**根本不可能发生**。

## 实践中的类型错误

以下是常见错误场景以及 Auto 如何预防它们。

**缺少返回值。** 在 TypeScript 中，声明了返回类型的函数如果忘记写 `return` 语句，可能会静默返回 `undefined`。Auto 使用**隐式返回**——函数体中最后一个表达式就是返回值。不存在"忘记"返回的可能。

**未使用的变量。** TypeScript 和 Auto 都会警告未使用的变量。在 TypeScript 中，这由 `noUnusedLocals` 编译器选项控制。Auto 始终发出警告，因为未使用的变量几乎总是一个错误。

**泛型中的类型不匹配。** 两种语言都会报告泛型实例化中的类型不匹配。区别在于 Auto 的逃生通道更少——没有 `any` 转型，也没有类型断言操作符可以绕过类型系统。如果类型不匹配，你必须修复类型，而不是抑制错误。

**模式匹配中缺少枚举情况。** 在 TypeScript 中，`switch` 语句默认不强制穷尽性检查。你需要 `never` 类型技巧或 lint 规则。Auto 的 `is` 模式匹配**始终检查穷尽性**。如果你向枚举添加新变体，每个匹配它的 `is` 表达式都会产生编译错误，直到所有情况都被处理。

## 调试类型错误

当你遇到类型错误时，请遵循以下策略：

1. **从上到下阅读错误链。** 第一行命名错误；后续行解释原因。
2. **在 IDE 中悬停查看类型。** 将光标放在变量上查看其推断类型。通常推断类型比你预期的更宽泛。
3. **用注解引导推断。** 在 TypeScript 中，使用 `as Type` 或显式注解。在 Auto 中，添加显式类型注解以帮助编译器消除歧义。
4. **隔离错误。** 将有问题的表达式提取到一个小的、自包含的示例中。这会消除噪音，使类型关系变得清晰。
5. **文档化有意的类型不匹配。** 在 TypeScript 中，使用 `// @ts-expect-error` 并加上注释解释为什么不匹配是预期的。在 Auto 中，如果类型不匹配是有意的，请重新考虑设计——类型系统在告诉你一些重要的信息。

最有效的策略是**在寻找修复方案之前完整阅读错误消息**。大多数 TypeScript 错误链包含完整的诊断信息。一旦你理解了链在告诉你什么，修复方案通常是显而易见的。

<Listing name="common-errors" file="listings/ch13-common-errors">

```auto
// Auto — common error scenarios

// Error: type mismatch
fn add(a int, b int) int { a + b }
// let result = add("hello", "world")  // Error: expected int, got str

// Error: missing enum case
enum Color { Red, Green, Blue }

fn describe(c Color) str {
    c is
        Red => "red"
        Green => "green"
        // Missing Blue — compiler error: non-exhaustive pattern match
}

// Error: nil safety
fn process(name ?str) {
    // print(name.len())  // Error: name is ?str, must check for nil first
    name is
        Some(n) => print("Length: {n.len()}")
        None => print("No name")
}

// Error: immutability
fn main() {
    let x = 5
    // x = 10  // Error: cannot reassign immutable variable

    var y = 5
    y = 10  // OK — var is mutable
    print("y = {y}")
}
```

```typescript
// TypeScript — common error scenarios

// Error: type mismatch
function add(a: number, b: number): number { return a + b; }
// let result = add("hello", "world");  // TS2345: Argument of type 'string'

// Error: missing case in switch
type Color = "Red" | "Green" | "Blue";
function describe(c: Color): string {
    switch (c) {
        case "Red": return "red";
        case "Green": return "green";
        // Missing "Blue" — no compiler error without exhaustive check
    }
}

// Error: possibly undefined (strictNullChecks)
function process(name: string | null): void {
    // console.log(name.length);  // TS2532: Object is possibly 'null'
    if (name !== null) {
        console.log("Length: " + name.length);
    }
}

// Error: const assignment
function main(): void {
    const x = 5;
    // x = 10;  // TS2588: Cannot assign to 'x' because it is a constant

    let y = 5;
    y = 10;  // OK
    console.log("y = " + y);
}
```

</Listing>

## 快速参考

| 概念 | TypeScript | Auto |
|---|---|---|
| 错误代码格式 | `TS2345` | 数字代码（相同约定） |
| 错误抑制 | `// @ts-expect-error` | *(不可用 — 修复错误)* |
| 可能为 undefined | `TS2532`（strictNullChecks） | *(不可能发生 — 使用 `?T`)* |
| 隐式 any | `TS7006` | *(不可能发生 — 没有 `any`)* |
| 缺少返回值 | `TS7030` | *(不可能发生 — 隐式返回)* |
| 非穷尽 switch | *(默认无错误)* | 编译错误（内置于 `is`） |
| 不可变性违规 | `TS2588`（const） | 编译错误（`let` 不可变） |
| 类型断言逃生 | `x as Type` | *(不可用 — 没有逃生通道)* |
