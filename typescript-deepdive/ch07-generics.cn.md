# 泛型与类型推断

泛型（generics）是类型系统中最强大的特性之一。它允许你编写**可复用、类型安全的抽象**，适用于多种类型而无需重复代码。结合*类型推断*（type inference），泛型同时提供了安全性和简洁性。

## 为什么需要泛型？

没有泛型时，你面临一个两难的选择：为每种类型复制函数，或者使用 `any` 并完全丧失类型安全。

```typescript
// TypeScript — 没有泛型
function identityNumber(arg: number): number { return arg; }
function identityString(arg: string): string { return arg; }
```

有了泛型，一个函数就能处理所有类型：

```typescript
// TypeScript — 使用泛型
function identity<T>(arg: T): T { return arg; }
```

```auto
// Auto — 使用泛型
fn identity<T>(value T) T {
    value
}
```

类型参数 `<T>` 充当*占位符*，代表调用者提供的任意类型。编译器保证输入和输出类型一致——没有 `any`，没有运行时意外。

## 泛型函数

**泛型函数**在函数名后用尖括号声明一个或多个类型参数。调用者通常不需要显式指定类型参数——编译器会从参数中推断出来。

```typescript
function identity<T>(arg: T): T {
    return arg;
}

const a = identity(42);        // T 推断为 number
const b = identity("hello");   // T 推断为 string
```

```auto
fn identity<T>(value T) T {
    value
}

let a = identity(42)       // T 推断为 int
let b = identity("hello")  // T 推断为 str
```

```typescript
// 显式类型参数（很少需要）
const c = identity<boolean>(true);
```

```auto
// 显式类型参数（很少需要）
let c = identity<bool>(true)
```

当推断存在歧义时（例如没有参数可供参考），你可以显式提供类型参数。否则，让编译器自动推断即可。

## 泛型类型

类型本身也可以参数化。**泛型类型**存储或操作未知类型 `T` 的值，该类型由用户在构造时指定。

```typescript
class Box<T> {
    constructor(public value: T) {}
}

const intBox = new Box<number>(42);
const strBox = new Box("hello");  // T 推断为 string
```

```auto
type Box<T> {
    value T
}

let intBox = Box<int>(42)
let strBox = Box("hello")  // T 推断为 str
```

你可以声明多个类型参数来构建更复杂的结构：

```typescript
interface Pair<T, U> {
    first: T;
    second: U;
}
```

```auto
type Pair<T, U> {
    first T
    second U
}
```

泛型类型还可以定义**泛型方法**，引入自己独立的类型参数：

```auto
type Box<T> {
    value T

    fn map<U>(f fn(T) U) Box<U> {
        Box(f(self.value))
    }
}
```

这里 `map` 引入了*第二个*类型参数 `U`，它独立于 `T`。返回类型是 `Box<U>`，而不是 `Box<T>`。

## 泛型规格（接口）

**泛型规格**（spec）定义了一个由类型参数化的契约。实现该规格的任何类型都必须满足给定类型参数的契约。

```typescript
interface Container<T> {
    get(): T;
    set(value: T): void;
}

class List<T> implements Container<T> {
    private items: T[] = [];
    get(): T | undefined { return this.items[0]; }
    set(value: T) { this.items.push(value); }
}
```

```auto
spec Container<T> {
    fn get() T
    fn set(value T)
}

type List<T> as Container<T> {
    items []T

    fn get() ?T {
        self.items[0]
    }

    fn set(value T) {
        self.items.push(value)
    }
}
```

规格是 Auto 中等价于 TypeScript 接口的概念。当类型声明 `as Container<T>` 时，编译器会验证所有必需的方法都存在且签名匹配。

## 类型推断

TypeScript 和 Auto 都会进行**类型推断**——编译器自动推导类型，这样你就不必在每个地方都手写类型注解。推断在以下几种上下文中生效。

*变量初始化*——类型从初始化表达式推断：

```typescript
const x = 42;          // number
const name = "Ada";    // string
const flags = [true, false];  // boolean[]
```

```auto
let x = 42          // int
let name = "Ada"    // str
let flags = [true, false]  // []bool
```

*函数返回类型*——当函数体明显时可以省略：

```auto
fn double(n int) int {
    n * 2
}
```

*泛型类型参数*——从调用处的实参推断：

```typescript
const result = identity("hello");  // T = string
```

```auto
let result = identity("hello")  // T = str
```

*数组字面量*——元素类型从内容推断：

```typescript
const nums = [1, 2, 3];     // number[]
const mixed = [1, "two"];   // (number | string)[]
```

```auto
let nums = [1, 2, 3]       // []int
let mixed = [1, "two"]     // [](int | str)
```

TypeScript 的 `noImplicitAny` 标志确保推断不会静默回退到 `any`。Auto 根本没有 `any` 类型——推断要么成功，要么编译器报错。

## 泛型约束

有时候泛型参数需要比"任意类型"更受限。**约束**（constraints）限制了哪些类型对类型参数是合法的。

```typescript
function getLength<T extends { length: number }>(arg: T): number {
    return arg.length;
}

getLength("hello");    // OK — string 有 .length
getLength([1, 2, 3]);  // OK — 数组有 .length
// getLength(42);      // 错误 — number 没有 .length
```

```auto
fn get_length<T>(arg T) int where T: HasLength {
    arg.length()
}
```

在 TypeScript 中，类型参数上的 `extends` 添加约束。在 Auto 中，`where` 子句起到同样的作用——编译器检查 `T` 是否满足 `HasLength`（一个具有 `length() int` 方法的规格）。

约束将在后续章节深入讲解。现在只需记住：*约束让泛型更有用，因为它允许你对类型参数调用方法。*

## TypeScript 独有的泛型特性

TypeScript 拥有丰富的**类型级编程**（type-level programming）系统，远超简单的参数化类型。这些特性在 Auto 中没有对应物：

- **条件类型**（conditional types）—— `T extends U ? X : Y`
- **映射类型**（mapped types）—— `{ [K in keyof T]: T[K] }`
- **模板字面量类型**（template literal types）—— `` `hello ${string}` ``
- **工具类型**（utility types）—— `Partial<T>`、`Required<T>`、`Pick<T, K>`、`Omit<T, K>`

```typescript
type Readonly<T> = { readonly [K in keyof T]: T[K] };
type NameOnly = Pick<{ name: string; age: number }, "name">;
//   ^ { name: string }
```

这些构造允许你在*类型层面变换类型*，从已有类型创建新类型。Auto 有意省略了这些——Auto 中的泛型保持简洁：参数化类型、参数化函数和规格约束。没有类型级计算，没有元编程。

这个设计选择使 Auto 的类型系统易于学习且编译速度快，而 TypeScript 的高级特性以额外的复杂度为代价，处理复杂的库类型。

## 快速参考

| 概念 | TypeScript | Auto |
|---|---|---|
| 泛型函数 | `function id<T>(x: T): T` | `fn id<T>(x T) T` |
| 泛型类/类型 | `class Box<T> { v: T }` | `type Box<T> { v T }` |
| 泛型接口 | `interface I<T> { get(): T }` | `spec I<T> { fn get() T }` |
| 多类型参数 | `<T, U>` | `<T, U>` |
| 类型推断 | `identity(42)` → `T = number` | `identity(42)` → `T = int` |
| 约束 | `<T extends Foo>` | `<T> where T: Foo` |
| 条件类型 | `T extends U ? X : Y` | *(不支持)* |
| 映射类型 | `{ [K in keyof T]: T[K] }` | *(不支持)* |
| 工具类型 | `Partial<T>`、`Pick<T, K>` | *(不支持)* |
