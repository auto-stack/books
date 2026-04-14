# 函数

函数是任何程序的基本构建块。TypeScript 和 Auto 都提供一等函数、闭包和高阶函数支持，但语法和一些关键语义有所不同。

## 函数声明

*函数声明*定义一个带有类型参数和返回类型的命名函数。两者的语法类似，但 Auto 更简洁。

```typescript
function add(a: number, b: number): number {
    return a + b;
}
```

```auto
fn add(a int, b int) int {
    a + b
}
```

Auto 使用 `fn` 关键字代替 `function`。两个关键区别：**Auto 不需要 `return`**——函数体中最后一个表达式会被隐式返回。`return` 关键字仍然可用，用于从函数中*提前退出*。

两种语言的返回类型注解都出现在参数列表之后：TypeScript 中为 `): number`，Auto 中为 `) int`。

## 闭包（箭头函数）

*闭包*（箭头函数）为匿名函数提供了轻量级语法。它们对于回调、高阶函数和函数式编程模式至关重要。

```typescript
const add = (a: number, b: number): number => a + b;
const greet = (name: string): void => {
    console.log("Hello, " + name);
};
```

```auto
let add = (a int, b int) => a + b
let greet = (name str) => print("Hello, " + name)
```

箭头语法在两种语言中几乎完全相同。Auto 使用空格分隔的类型注解（`a int`），而 TypeScript 使用冒号分隔的注解（`a: number`）。

一个重要的区别：TypeScript 的闭包常被用来解决 `this` 绑定问题。**Auto 没有这个问题**——它对方法使用显式的 `self` 参数，因此闭包纯粹用于其表达力。

## 函数类型

两种语言都将函数视为*一等值*——你可以将它们存储在变量中、作为参数传递、从其他函数中返回。

```typescript
let transform: (x: number) => number = (x) => x * 2;
let predicate: (x: number) => boolean = (x) => x > 0;
```

```auto
let transform fn(int) int = (x int) => x * 2
let predicate fn(int) bool = (x int) => x > 0
```

TypeScript 使用 `(x: number) => number` 表示可调用类型注解。Auto 使用更紧凑的 `fn(int) int` 语法。多参数函数类型遵循相同的模式：

```typescript
let combine: (a: number, b: string) => boolean;
```

```auto
let combine fn(int, str) bool
```

高阶函数——接受或返回其他函数的函数——与这些类型自然配合：

```auto
fn apply(f fn(int) int, x int) int {
    f(x)
}
```

```typescript
function apply(f: (x: number) => number, x: number): number {
    return f(x);
}
```

## 可选参数和默认参数

函数可以接受调用者可以省略的参数。TypeScript 使用 `?` 后缀表示可选参数；Auto 在类型前使用 `?` 前缀。

```typescript
function greet(name: string, greeting?: string): void {
    if (greeting !== undefined) {
        console.log(greeting + ", " + name + "!");
    } else {
        console.log("Hello, " + name + "!");
    }
}
```

```auto
fn greet(name str, greeting ?str) {
    if greeting != nil {
        print("{greeting}, {name}!")
    } else {
        print("Hello, {name}!")
    }
}
```

可选参数在两种语言中都**必须放在**所有必需参数之后。在 TypeScript 中，可选参数的类型为 `T | undefined`。在 Auto 中，类型为 `?T`，默认值为 `nil`。

你也可以提供*默认值*：

```typescript
function greet(name: string, greeting: string = "Hello"): void {
    console.log(greeting + ", " + name + "!");
}
```

```auto
fn greet(name str, greeting str = "Hello") {
    print("{greeting}, {name}!")
}
```

默认参数消除了手动检查 `undefined` / `nil` 的需要——编译器会自动插入这些检查。

## 函数重载

TypeScript 支持**函数重载**，允许为同一个函数名定义多个签名：

```typescript
function parse(value: string): number;
function parse(value: number): string;
function parse(value: string | number): string | number {
    if (typeof value === "string") {
        return parseInt(value, 10);
    }
    return value.toString();
}
```

> **仅限 TypeScript。** Auto *不支持*函数重载。取而代之的是，使用**联合类型**或**枚举**在单个函数体中处理不同的输入形式：

```auto
fn parse(value int | str) int | str {
    value is
        int => value
        str => int.from_str(value)
}
```

这种方法更简单，避免了编写多个签名后跟单个实现的样板代码。

## 方法和 `self`

在 TypeScript 中，方法使用 `this` 引用当前对象。`this` 的值取决于函数的*调用方式*，这是一个常见的 bug 来源：

```typescript
class Counter {
    count = 0;
    increment() {
        this.count++;
    }
}
const c = new Counter();
c.increment();       // this === c  — 正确
const fn = c.increment;
fn();                // this === undefined  — 严格模式下出错
```

Auto 使用**显式的 `self` 参数**代替隐式的 `this`。不存在动态绑定——无论方法如何被引用，`self` 始终指向当前实例：

```auto
type Counter {
    count int
    fn inc() {
        self.count = self.count + 1
    }
}
```

方法调用在两种语言中使用相同的 `obj.method()` 语法。但在 Auto 中，将方法提取到变量中会保留其接收者——不会有意外的绑定问题。

## 闭包和捕获变量

TypeScript 和 Auto 都支持*闭包*：从封闭作用域中捕获变量的函数。捕获的变量通过引用共享，这意味着修改在多次调用之间是可见的。

```auto
fn make_counter() fn() int {
    var count int = 0
    fn() int {
        count = count + 1
        count
    }
}
```

```typescript
function makeCounter(): () => number {
    let count = 0;
    return function (): number {
        count = count + 1;
        return count;
    };
}
```

每次调用 `make_counter()`（或 `makeCounter()`）都会创建一个**新的词法作用域**，包含自己的 `count` 变量。返回的闭包在多次调用之间保留对该变量的访问——这就是*闭包计数器*或*工厂*模式。

这种模式在两种语言中被广泛用于封装、迭代器和有状态的回调。

## 快速参考

| 概念 | TypeScript | Auto |
|---|---|---|
| 函数声明 | `function add(a: number, b: number): number` | `fn add(a int, b int) int` |
| 隐式返回 | 不支持 | 最后一个表达式隐式返回 |
| 箭头函数 | `const f = (x: number) => x * 2` | `let f = (x int) => x * 2` |
| 函数类型 | `(x: number) => number` | `fn(int) int` |
| 可选参数 | `function f(x?: string)` | `fn f(x ?str)` |
| 默认参数 | `function f(x: string = "hi")` | `fn f(x str = "hi")` |
| 函数重载 | 支持多个签名 | 不支持；使用联合类型 |
| 方法接收者 | `this`（动态绑定） | `self`（显式参数） |
| 闭包捕获 | 按引用捕获 | 按引用捕获 |
