# 接口与枚举

本章涵盖 TypeScript 和 Auto 如何建模类型之间的契约，以及如何表示一组
固定的可选值。这两个特性是编写安全、表达力强的代码的基础——但 Auto
对枚举采用了根本不同的方法。

## 接口到 Spec

在 TypeScript 中，`interface` 定义了一个**结构化契约**——其他类型必须
遵循的形状。接口在运行时没有影响；它们仅作为编译时检查存在：

```typescript
// TypeScript
interface Greetable {
    name: string;
    greet(): void;
}

class User implements Greetable {
    constructor(public name: string) {}
    greet() {
        console.log("Hello, " + this.name);
    }
}
```

Auto 使用 `spec` 达到同样的目的——纯结构化契约，无运行时开销：

```auto
// Auto
spec Greetable {
    fn greet()
}

type User as Greetable {
    name str
    fn greet() { print("Hello, " + self.name) }
}
```

一个关键区别：TypeScript 接口是*开放的*，支持**声明合并**——你可以在
其他位置通过重新声明来扩展接口。Auto spec 是*封闭的*——一旦定义，其形状
就固定了。这消除了通过合并声明意外引入属性导致的一整类 bug。

## 实现接口

TypeScript 在类上使用 `implements` 关键字：

```typescript
// TypeScript
class User implements Greetable, Serializable {
    // ...
}
```

Auto 在类型上使用 `as` 关键字：

<Listing name="spec-implementation" file="listings/ch05-spec-implementation">

```auto
// Auto
type User as Greetable {
    name str
    fn greet() { print("Hello, " + self.name) }
}
```

</Listing>

Auto 的结构化类型意味着 `as` 关键字在技术上是可选的——如果类型的形状
匹配 spec，它就自动满足该 spec。然而，显式的 `as` 声明被推荐用于
**文档和意图表达**：它们告诉读者一致性是刻意设计的，而非偶然。

多个 spec 实现使用逗号分隔的列表：

```auto
// Auto — 多个 spec
type User as Greetable, Serializable {
    name str
    fn greet() { ... }
    fn serialize() str { ... }
}
```

## TypeScript 枚举 vs Auto 枚举

这是本章中**最重要的概念差异**。尽管共享"enum"这个名称，TypeScript
和 Auto 的含义根本不同。

TypeScript 枚举是*命名常量*。它们在运行时生成真正的 JavaScript 对象：

```typescript
// TypeScript — 数字枚举（双向映射）
enum Direction {
    Up,      // 0
    Down,    // 1
    Left,    // 2
    Right    // 3
}

// TypeScript — 字符串枚举
enum Status {
    Active = "ACTIVE",
    Inactive = "INACTIVE"
}
```

TypeScript 还有 `const enum`（编译时内联）和*异构*枚举（混合数字和字符串）。
所有这些都只是有组织的常量集合。

**Auto 枚举是代数数据类型**——可以携带数据载荷的标签联合：

```auto
// Auto — 带数据载荷的枚举
enum Shape {
    Circle(f64),
    Rect(f64, f64),
    Triangle(f64, f64, f64)
}
```

每个变体不是裸常量——它包装真实数据。`Circle` *包含*半径，`Rect` *包含*
宽度和高度。这使得 Auto 枚举比 TypeScript 枚举更具表达力。

## 用 `is` 进行模式匹配

TypeScript 使用 `switch` 配合 `typeof`、`in` 或属性检查来进行类型收窄。
这很冗长且容易出错——编译器无法验证所有情况都已处理：

```typescript
// TypeScript — 可辨识联合 + switch
type Shape =
    | { kind: "circle"; radius: number }
    | { kind: "rect"; width: number; height: number };

function area(s: Shape): number {
    switch (s.kind) {
        case "circle":
            return Math.PI * s.radius * s.radius;
        case "rect":
            return s.width * s.height;
        // 忘了 "triangle"？编译器不会警告你。
    }
}
```

Auto 提供 `is` 关键字进行**穷举模式匹配**。编译器验证每个变体都被处理：

```auto
// Auto — 穷举模式匹配
fn area(s Shape) f64 {
    s is
        Circle(r) => 3.14159 * r * r
        Rect(w, h) => w * h
        Triangle(a, b, c) => {
            let s = (a + b + c) / 2
            sqrt(s * (s - a) * (s - b) * (s - c))
        }
}
```

如果你给 `Shape` 添加了新变体却忘记在 `area` 中处理，编译器会产生错误。
这就是**穷举检查**——Auto 提供的最强安全保证之一。

## 枚举作为数据载体

Auto 枚举替代了 TypeScript 的*可辨识联合*模式。考虑一个表示成功或失败的
`Result` 类型：

```typescript
// TypeScript — 可辨识联合（冗长）
type Result<T> =
    | { tag: "Ok"; value: T }
    | { tag: "Err"; error: string };

function processResult(r: Result<number>): void {
    switch (r.tag) {
        case "Ok":
            console.log("Success: " + r.value);
            break;
        case "Err":
            console.log("Error: " + r.error);
            break;
    }
}
```

同样的概念在 Auto 中要简洁得多：

```auto
// Auto — 枚举作为数据载体
enum Result<T> {
    Ok(T),
    Err(str)
}

fn process_result(r Result<int>) {
    r is
        Ok(value) => print("Success: {value}")
        Err(msg) => print("Error: {msg}")
}
```

Auto 还提供 `?T` 作为可空值的语法糖——等价于 `enum Option<T> { Some(T), None }`。
这消除了对 TypeScript 中常见的 `T | null | undefined` 模式的需求。

## 用 `has` 组合

TypeScript 使用**混入（mixin）**在类层次之间复用代码——通常通过在运行时
合并原型的函数工厂实现。这很复杂且依赖运行时行为。

Auto 提供 `has` 关键字进行简洁的编译时组合：

```auto
// Auto — 用 has 组合
type Wing {
    span f64
    fn flap() { print("Flapping!") }
}

type Duck has Wing {
    name str
}

fn main() {
    let d = Duck(name: "Donald", span: 1.2)
    d.flap()  // Duck 继承了 Wing 的方法
}
```

`type Duck has Wing` 让 `Duck` 获得 `Wing` 的所有字段和方法——没有运行时
魔法，没有原型操作。组合完全在编译时解决。完整的 mixin 模式在第 12 章中
介绍。

## 快速参考

| 概念 | TypeScript | Auto |
|------|-----------|------|
| 接口定义 | `interface Foo { }` | `spec Foo { }` |
| 实现接口 | `class X implements Foo` | `type X as Foo { }` |
| 多接口实现 | `class X implements A, B` | `type X as A, B { }` |
| 命名常量 | `enum Dir { Up, Down }` | `const { Up = 0; Down = 1 }` |
| 标签联合 | `{ tag: "Ok"; value: T } \| { ... }` | `enum Result<T> { Ok(T), Err(str) }` |
| 模式匹配 | `switch` + 类型守卫 | `is` 关键字 |
| 穷举检查 | 手动 / never 类型 | 编译器强制 |
| 可空类型 | `T \| null` | `?T` |
| 混入 / 组合 | 类混入（运行时） | `has` 关键字（编译时） |
