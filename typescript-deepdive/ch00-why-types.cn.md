# 为什么需要类型

本书深入探讨 TypeScript 的类型系统，以及这些概念如何映射到 Auto
编程语言。在进入语法细节之前，先建立*为什么类型很重要*的认知。

## 类型的价值

类型服务于两个根本目的：

1. **在编译期而非运行期捕获错误。** 编译器发现 bug 的代价远低于
   用户在生产环境中遇到 bug 的代价。

2. **作为活文档。** 函数签名是一份契约——签名描述函数*做什么*，
   函数体是它确实这样做的*证明*。

大型工程组织（Google、Microsoft、Meta）都独立得出了相同的结论：
有类型的代码库更容易维护、重构和扩展。

## Auto 的方式：默认有类型

与 TypeScript 中类型是*可选的*（合法的 JavaScript 就是合法的 TypeScript）
不同，Auto 将类型作为语言的一等公民。每个变量、函数参数和返回值
都有类型——要么是显式注解的，要么是编译器推导的。

```auto
// 显式类型注解
let name str = "Auto"

// 从上下文推导类型
let count = 42          // 推导为 int
let items = [1, 2, 3]   // 推导为 List<int>
```

```typescript
// 显式类型注解
let name: string = "Auto";

// 从上下文推导类型
let count = 42;          // 推导为 number
let items = [1, 2, 3];   // 推导为 number[]
```

Auto 使用**空格分隔**的类型注解（没有冒号），保持语法简洁无歧义：

```auto
fn greet(name str) {
    print("Hello, " + name)
}
```

```typescript
function greet(name: string): void {
    console.log("Hello, " + name);
}
```

## 结构化类型

Auto 和 TypeScript 都使用**结构化类型**——一个值的类型由其*形状*
决定，而非其*名称*。如果两个类型具有相同的结构，它们就是兼容的，
即使它们是分别定义的。

```auto
type Point2D {
    x int
    y int
}

type Point3D {
    x int
    y int
    z int
}

fn printX(p Point2D) {
    print(p.x)
}

fn main() {
    let p2 = Point2D(1, 2)
    let p3 = Point3D(1, 2, 3)
    printX(p2)   // 精确匹配
    printX(p3)   // 多余字段也可以 — 结构化类型
}
```

```typescript
interface Point2D { x: number; y: number; }
interface Point3D { x: number; y: number; z: number; }

function printX(p: Point2D): void {
    console.log(p.x);
}

const p2: Point2D = { x: 1, y: 2 };
const p3: Point3D = { x: 1, y: 2, z: 3 };
printX(p2);  // 精确匹配
printX(p3);  // 多余字段也可以 — 结构化类型
```

这与名义类型语言（如 Java 或 Rust 的 struct）不同——在那些语言中，
你必须显式声明继承或 trait 实现。

## 默认不可变

Auto 遵循**不可变是安全默认值**的哲学：

```auto
let x = 5        // 不可变 — 不能重新赋值
var y = 5        // 可变 — 可以用 `=` 重新赋值
```

```typescript
const x = 5;     // 不可变 — 不能重新赋值
let y = 5;       // 可变 — 可以用 = 重新赋值
```

这比 TypeScript 的 `let`（可变）更严格，但能在编译期捕获整类 bug。

## Auto 转译为 TypeScript

Auto 不是解释执行的——它提前编译为 TypeScript（或 Rust），然后在任何
JavaScript 引擎（或原生环境）上运行。这意味着：

- Auto 从自己的类型系统获得**编译期类型检查**
- 生成的 TypeScript 代码在**现有 JavaScript 运行时**上运行
- 你可以与任何 TypeScript/JavaScript 库互操作

## 本书涵盖内容

本书比快速入门指南更深入。我们覆盖：

- **类型系统基础**——注解、推导、兼容性
- **高级模式**——泛型、判别联合、混入
- **类型理论**——协变、逆变、结构化 vs 名义类型
- **设计模式**——单例、柯里化、事件发射器
- **错误处理**——哲学与实践模式
- **编译器架构**——Auto 的编译器管线如何工作

## 快速参考

| 概念 | TypeScript | Auto |
|------|-----------|------|
| 不可变变量 | `const x = 5` | `let x = 5` |
| 可变变量 | `let x = 5` | `var x = 5` |
| 类型注解 | `x: number` | `x int` |
| 函数 | `function` / `=>` | `fn` / `=>` |
| 接口 | `interface` | `spec` |
| 类 | `class` | `type` |
| 继承 | `extends` | `is` |
| 组合 | — | `has` |
| 模式匹配 | `switch` / `typeof` | `is` |
| 打印 | `console.log()` | `print()` |
