# 类型系统基础

本章涵盖 TypeScript 和 Auto 类型系统的基础构建块——原始类型、数组、
类型注解、联合类型，以及两种语言在类型安全方面的关键差异。

## `any` 逃生舱

TypeScript 提供了 `any` 类型，可以**完全禁用**某个值的类型检查。它是为
渐进式采用而设计的逃生舱，但也是语言中**最危险**的特性：

```typescript
// TypeScript — any 逃生舱
let data: any = "hello";
data = 42;                // 没有错误
data.toUpperCase();       // 编译时不报错，运行时崩溃
data.someRandomMethod();  // 也没有错误——静默损坏
```

一旦 `any` 进入你的代码库，它就会**传播**。任何从 `any` 表达式派生的
值也会变成 `any`，迅速侵蚀整个模块的类型安全。

TypeScript 还提供了 `unknown`，它是 `any` 的*类型安全*版本。你不能在
不缩小类型的情况下使用 `unknown` 值：

```typescript
let input: unknown = "hello";
input.toUpperCase();  // 错误 — Object is of type 'unknown'
if (typeof input === "string") {
    input.toUpperCase();  // OK — 已缩小为 string
}
```

Auto **没有 `any` 类型**——也没有 `unknown`。每个值都有具体的、经过检查的
类型。这不是限制，而是设计选择——从源头消除整类运行时错误。

## 原始类型

TypeScript 的原始类型直接继承自 JavaScript：

```typescript
// TypeScript — 所有数字都是 float64
let count: number = 42;
let pi: number = 3.14159;
let name: string = "hello";
let flag: boolean = true;
let nothing: null = null;
let undef: undefined = undefined;
let sym: symbol = Symbol("id");
let big: bigint = 9007199254740991n;
```

JavaScript 的 `number` 类型**始终是 float64**——即使对于整数也是如此。
这导致了众所周知的精度问题：

```typescript
// TypeScript
0.1 + 0.2;  // 0.30000000000000004 — 不是 0.3！
```

Auto 提供了更简洁、更明确的原始类型：

<Listing name="primitives" file="listings/ch04-primitives">

```auto
// Auto — primitive types and annotations
fn main() {
    // Explicit type annotations
    let count int = 42
    let pi f64 = 3.14159
    let name str = "Auto"
    let is_ready bool = true

    // Type inference
    let sum = count + 8       // inferred as int
    let items = [1, 2, 3]     // inferred as []int

    // Nullable types
    let middle_name ?str = nil

    // Arrays
    let numbers = [10, 20, 30]
    let doubled = numbers.map((n int) => n * 2)

    print("Name: {name}")
    print("Sum: {sum}")
    print("Doubled: {doubled}")

    // Union types
    let id: int | str = 42
    id = "user-001"

    // Tuple-like types
    let pair = (1, "hello")
    print("First: {pair.0}, Second: {pair.1}")
}
```

</Listing>

Auto 原始类型的关键差异：

1. **`int` 和 `f64` 是独立类型。** 整数运算是精确的——对整数不会有
   浮点数的意外结果。
2. **`nil` 统一了 `null` 和 `undefined`。** JavaScript 的两个"空"值被
   合并为一个，简化了空值处理。
3. **没有内置的 `symbol` 或 `bigint`。** Auto 在需要时通过标准库
   覆盖这些用例。

## 数组

数组是单一元素类型的有序、可索引集合。

```typescript
// TypeScript — 数组语法
let numbers: number[] = [1, 2, 3];
let names: string[] = ["Alice", "Bob"];
let matrix: boolean[][] = [[true, false], [false, true]];

numbers.push(4);
const last = numbers.pop();
const len = numbers.length;
const doubled = numbers.map(n => n * 2);
const evens = numbers.filter(n => n % 2 === 0);
```

```auto
// Auto — 数组语法
let numbers []int = [1, 2, 3]
let names []str = ["Alice", "Bob"]
let matrix [][]bool = [[true, false], [false, true]]

numbers.push(4)
let last = numbers.pop()
let len = numbers.len()
let doubled = numbers.map((n int) => n * 2)
let evens = numbers.filter((n int) => n % 2 == 0)
```

Auto 将方括号放在类型**前面**（`[]int`），遵循 Go 和 Pascal 的惯例。
TypeScript 将其放在**后面**（`number[]`）。两者的含义完全相同：同构值
的列表。

## 变量类型注解

TypeScript 使用**冒号**来注解变量类型：

```typescript
// TypeScript — 显式注解
let age: number = 30;
let name: string = "Alice";
let active: boolean = true;

// TypeScript — 类型推断
let score = 100;        // 推断为 number
let greeting = "hi";    // 推断为 string
```

Auto 使用**空格分隔**的注解——没有冒号：

```auto
// Auto — 显式注解
let age int = 30
let name str = "Alice"
let active bool = true

// Auto — 类型推断
let score = 100        // 推断为 int
let greeting = "hi"    // 推断为 str
```

在两种语言中，当编译器可以从初始化表达式推断类型时，注解是*可选的*。
当意图比简洁更重要时，使用显式注解——函数参数和公共 API 是很好的
候选场景。

## Interface 作为类型

TypeScript 使用 `interface` 定义对象形状：

```typescript
// TypeScript
interface Point {
    x: number;
    y: number;
}

let p: Point = { x: 1, y: 2 };
```

Auto 将 `type` 和 `interface` 统一为单一的 `type` 声明。这消除了 TypeScript
中关于何时使用哪个的常见困惑：

```auto
// Auto
type Point {
    x f64
    y f64
}

let p Point = { x: 1, y: 2 }
```

我们将在 [ch05](ch05-interfaces.md) 中深入探讨 `type` 声明。

## 联合类型与交叉类型

**联合类型**允许值是多种类型之一。TypeScript 和 Auto 都使用 `|` 运算符：

```typescript
// TypeScript
let id: string | number = 42;
id = "user-001";  // OK — 两种类型都允许
```

```auto
// Auto
let id: int | str = 42
id = "user-001"   // OK
```

**交叉类型**将多个类型合并为一个。TypeScript 使用 `&`：

```typescript
// TypeScript
interface HasId { id: number; }
interface HasName { name: string; }
type User = HasId & HasName;
```

Auto **没有**交叉类型。取而代之，它使用 `has` 组合将特性混入类型——
这个模式将在 [ch05](ch05-interfaces.md) 和 [ch12](ch12-composition.md) 中
介绍。

**可空类型**是联合类型的特例。在 TypeScript 中写 `string | null`。Auto
提供了语法糖：

```auto
// Auto — 可空语法糖
let name ?str = nil       // 等同于 str | nil
```

`?` 前缀简洁明了，让可空类型在代码中一目了然。

## 元组类型

元组是固定长度、按位置排列的数组，每个位置有自己的类型。

```typescript
// TypeScript — 元组
let pair: [string, number] = ["hello", 42];
let first: string = pair[0];
let second: number = pair[1];
```

```auto
// Auto — 元组
let pair = ("hello", 42)
let first str = pair.0
let second int = pair.1
```

元组对于从函数返回多个值很有用，但应谨慎使用——命名的 `type` 几乎
总是更清晰。

## 快速参考

| 概念 | TypeScript | Auto |
|------|-----------|------|
| 逃生舱 | `any`、`unknown` | 无——所有类型均被检查 |
| 整数 | `number`（float64） | `int` |
| 浮点数 | `number`（float64） | `f64` |
| 字符串 | `string` | `str` |
| 布尔值 | `boolean` | `bool` |
| 空值 | `null`、`undefined` | `nil` |
| 可空类型 | `T \| null` | `?T` |
| 数组 | `number[]` | `[]int` |
| 类型注解 | `let x: number` | `let x int` |
| 对象形状 | `interface` / `type` | `type` |
| 联合类型 | `string \| number` | `str \| int` |
| 交叉类型 | `A & B` | 使用 `has` 组合 |
| 元组 | `[string, number]` | `(str, int)` |
