# 判别联合与不可变性

判别联合（discriminated unions）是建模多种不同形态数据的最强大模式之一。结合不可变性，它们赋予你安全、可预测且编译器可穷尽验证的代码。TypeScript 通过手动构造的对象联合来支持这一模式，而 Auto 通过 `enum` 将其作为一等语言特性提供。

## 什么是判别联合？

**判别联合**使用一个共享属性——称为**判别符（discriminant）**——来告诉编译器你正在处理联合类型中的哪个变体。一旦编译器知道了判别符，它就会自动收窄类型，让你只能访问属于该变体的字段。

在 TypeScript 中，你通过给每个对象变体添加一个共同属性来手动构建判别联合：

```typescript
type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "rect"; width: number; height: number };
```

`kind` 属性就是判别符。每个变体都携带它，其字面量值唯一标识了形状。

在 Auto 中，判别联合是内置在语言中的。带数据载荷的 `enum` 关键字**就是**判别联合——变体名本身就是判别符：

```auto
enum Shape {
    Circle(f64)
    Rect(f64, f64)
}
```

无需手动 `kind` 字段，无需对象样板代码。编译器知道每个变体并强制穷尽处理。

## TypeScript 的手动方式

以下是 TypeScript 中的完整模式：

```typescript
type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "rect"; width: number; height: number };

function area(shape: Shape): number {
    switch (shape.kind) {
        case "circle":
            return Math.PI * shape.radius ** 2;
        case "rect":
            return shape.width * shape.height;
    }
}
```

冗长就是代价。每个变体都需要 `{ kind: "..."; ... }` 包装器。穷尽性检查依赖于赋值给 `never`：

```typescript
function area(shape: Shape): number {
    switch (shape.kind) {
        case "circle":
            return Math.PI * shape.radius ** 2;
        case "rect":
            return shape.width * shape.height;
        default:
            const _exhaustive: never = shape;
            return _exhaustive;
    }
}
```

如果你添加了新变体但忘记处理，TypeScript 会标记 `never` 赋值。它有效，但这是一种约定而非语言保证。

## Auto 的原生 Enum 方式

Auto 消除了样板代码。带载荷的枚举本质就是判别联合：

```auto
enum Shape {
    Circle(f64)
    Rect(f64, f64)
}

fn area(s Shape) f64 {
    s is
        Circle(r) => 3.14159 * r * r
        Rect(w, h) => w * h
}
```

编译器**知道**每个变体。如果你添加了新的变体，`is` 表达式会产生编译时错误，除非你处理了它。不需要 `never` 技巧——穷尽性由语言保证。

这是 Auto 中最自然的数据建模模式。使用枚举来表示任何可以是几种不同情况之一的事物：形状、结果、消息、状态、AST 节点。

## Result 模式

判别联合最实用的用途之一是**显式错误处理**。在 TypeScript 中，你手动构建：

```typescript
type Result<T> =
    | { ok: true; value: T }
    | { ok: false; error: string };
```

在 Auto 中，只需一行：

```auto
enum Result<T> {
    Ok(T)
    Err(str)
}
```

Auto 的 `Result` 用你传递的值替代了 `try`/`catch`。错误不是异常——它们是数据。编译器强制你在每个调用点都确认 `Ok` 和 `Err`。

<Listing name="result-type" file="listings/ch10-result-type">

该 listing 展示了一个完整的示例：解析整数、安全除法以及对 `Result` 的模式匹配。它还演示了 `let` 和 `var` 的不可变性。

</Listing>

## 用 `let` 实现不可变性

TypeScript 和 Auto 在变量可变性方面采取了相反的默认立场：

| 概念 | TypeScript | Auto |
|------|-----------|------|
| 不可变绑定 | `const` | `let` |
| 可变绑定 | `let` | `var` |

这是一个常见的混淆点。TypeScript 的 `let` 允许重新赋值；Auto 的 `let` **不允许**。在 Auto 中，你必须用 `var` 主动选择可变性。

```typescript
// TypeScript
const name = "production";   // 不能重新赋值
let attempts = 0;            // 可以重新赋值
attempts = attempts + 1;     // 没问题
```

```auto
// Auto
let name = "production"      // 不能重新赋值
var attempts int = 0          // 可以重新赋值
attempts = attempts + 1       // 没问题
```

Auto 的选择使 `let` 成为安全的默认值。你可以一目了然地看到哪些变量可能会改变——它们是用 `var` 声明的。

## Readonly 深度解析

TypeScript 提供三个级别的 `readonly` 保护：

```typescript
// 1. readonly 属性修饰符
interface Config {
    readonly name: string;
    readonly port: number;
}

// 2. Readonly 工具类型（浅层）
type FrozenConfig = Readonly<Config>;

// 3. readonly 数组
const items: ReadonlyArray<string> = ["a", "b"];
```

`readonly` 修饰符防止对单个属性的重新赋值。`Readonly<T>` 将其应用于类型中的每个属性。两者都是**浅层的**——嵌套对象仍然是可变的，除非你递归地应用 `Readonly`。

Auto 采取了更简单的方式。`let` 给你不可变绑定。对于深层不可变性，使用不可变数据结构。没有 `readonly` 关键字，因为不可变性是默认的：

```auto
let config = {name: "production", port: 8080}
// config.name = "staging"  // 编译错误 — config 是 let
```

当你需要修改时，用 `var` 包装，编译器会精确追踪作用域。

## 快速参考

| 概念 | TypeScript | Auto |
|------|-----------|------|
| 定义判别联合 | `type T = { kind: "a"; ... } \| { kind: "b"; ... }` | `enum T { A(...), B(...) }` |
| 匹配变体 | `switch (x.kind)` | `x is A(v) => ...` |
| 穷尽性检查 | `const _: never = x` | 编译时自动检查 |
| Result 类型 | `type Result<T> = { ok: true; value: T } \| { ok: false; error: string }` | `enum Result<T> { Ok(T), Err(str) }` |
| 不可变变量 | `const x = 5` | `let x = 5` |
| 可变变量 | `let x = 5` | `var x = 5` |
| 只读属性 | `readonly name: string` | `let` 绑定（默认） |
| 所有属性只读 | `Readonly<T>` | `let` 默认 |
| 只读数组 | `ReadonlyArray<T>` | 默认不可变 |
