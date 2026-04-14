# 基础

对于大多数编程语言来说，代码必须经过*编译*或*解释*才能运行。在 Auto 这样的静态类型语言中，编译器会在代码执行之前检查类型错误。Auto 的 `a2ts` 转译器更进一步：它生成的 TypeScript 输出还可以被 `tsc` 检查，为你提供双层类型安全保障。

本章介绍 Auto 中与 TypeScript 基础知识直接对应的核心特性。如果你之前写过 TypeScript，其中大部分概念会觉得很熟悉——Auto 只是用更简洁的语法来表达它们。

## 静态类型检查

Auto 是一种静态类型语言。这意味着编译器在编译期就知道每个变量和表达式的类型，并且会拒绝混合不兼容类型的代码。例如，在需要 `str` 的地方传入 `int` 会导致编译错误，这与 TypeScript 中的行为完全一致。

区别在于 Auto 在使用 `a2ts` 转译时就会检查这些错误，而生成的 TypeScript 代码保留了类型信息，因此 `tsc` 可以捕获 Auto 编译器遗漏的任何问题。这种双重检查策略意味着你可以从 `a2ts` 获得快速、清晰的错误信息，同时以 TypeScript 编译器作为安全网。

## 非异常故障

类型错误并不是 Auto 在编译期捕获的唯一错误类型。属性名拼写错误、函数参数数量不匹配、忘记处理 `null` 值——这些都在代码运行之前就被捕获了。在 JavaScript 中，这些错误只会在运行时暴露——通常以令人困惑的 `undefined is not a function` 错误出现。Auto 消除了 TypeScript 开发者每天都会遇到的一整类 bug。

## 类型驱动的工具支持

由于 Auto 具有静态类型系统，编辑器可以在你输入时提供实时反馈：自动补全建议、内联错误诊断以及自动重构支持。这与今天使用 TypeScript 获得的工具体验完全一致，并且通过 Auto 语言服务器开箱即用。

## Hello, World

每本编程书都以 "Hello, World" 开头。以下是 Auto 中的写法以及 `a2ts` 生成的 TypeScript 代码：

<Listing number="01-01" file="main">

```auto
fn main() {
    print("Hello, world!")
}
```

```typescript
/**
 * AutoLang TypeScript Runtime
 */
const print = console.log.bind(console);

function range(start: number, end: number, eq: boolean = false): number[] {
    const res: number[] = [];
    if (eq) {
        for (let i = start; i <= end; i++) res.push(i);
    } else {
        for (let i = start; i < end; i++) res.push(i);
    }
    return res;
}


function main(): void {
    console.log("Hello, world!");
}

main();
```

</Listing>

有几个地方需要注意。Auto 使用 `fn` 声明函数，使用 `print()` 代替 `console.log()`。没有分号。`a2ts` 转译器会生成标准的 `function`，带有 `void` 返回类型，将 `print` 替换为 `console.log`，并在文件末尾添加 `main()` 调用，使程序真正可以运行。

## 显式类型标注

Auto 允许你在函数签名中直接标注参数和返回类型，使用空格分隔的语法，而不是 TypeScript 的冒号分隔标注：

<Listing number="01-02" file="main">

```auto
fn greet(person str, date Date) {
    print(f"Hello ${person}, today is ${date.toDateString()}!")
}
```

```typescript
/**
 * AutoLang TypeScript Runtime
 */
const print = console.log.bind(console);

function range(start: number, end: number, eq: boolean = false): number[] {
    const res: number[] = [];
    if (eq) {
        for (let i = start; i <= end; i++) res.push(i);
    } else {
        for (let i = start; i < end; i++) res.push(i);
    }
    return res;
}

function greet(person: string, date: Date): void {
    console.log(`Hello ${person}, today is ${date.toDateString()}!`);
}
```

</Listing>

在 Auto 中，每个参数的类型列在名称之后，用空格分隔：`person str` 表示"一个名为 `person`、类型为 `str` 的参数"。`a2ts` 转译器会将其转换为 TypeScript 的 `person: string` 语法。返回类型使用相同的空格分隔约定——如果我们想返回 `str`，会写成 `fn greet() str { ... }`。

Auto 中的字符串插值使用 `f"..."` 配合 `${expr}` 占位符，直接映射到 TypeScript 的模板字面量语法。

## 类型推断

你并不总是需要手写类型标注。Auto 可以从初始值推断变量的类型，就像 TypeScript 一样：

<Listing number="01-03" file="main">

```auto
fn main() {
    let msg = "hello there!"
    print(msg)
}
```

```typescript
/**
 * AutoLang TypeScript Runtime
 */
const print = console.log.bind(console);

function range(start: number, end: number, eq: boolean = false): number[] {
    const res: number[] = [];
    if (eq) {
        for (let i = start; i <= end; i++) res.push(i);
    } else {
        for (let i = start; i < end; i++) res.push(i);
    }
    return res;
}

function main(): void {
    const msg = "hello there!";
    console.log(msg);
}

main();
```

</Listing>

变量 `msg` 用字符串字面量初始化，所以 Auto 将其类型推断为 `str`。`a2ts` 转译器生成 `const`，因为 Auto 的 `let` 默认是不可变的。如果你需要可变变量，在 Auto 中使用 `var`，它会转译为 TypeScript 的 `let`。

## 类型擦除

Auto 的类型仅在编译期存在。当 `a2ts` 将代码转译为 TypeScript 时，类型标注会保留在 TypeScript 输出中供 `tsc` 检查，但它们在运行时没有任何效果。这与 TypeScript 使用的模型相同：类型在 TypeScript 编译为 JavaScript 时被擦除。在 Auto 的情况下，类型在 `a2ts` 到 TypeScript 的转译阶段就被擦除了——但生成的 TypeScript 保留了它们，用于下游的 `tsc` 检查。

## 严格模式

Auto 默认就是严格的。没有 `strict` 标志可以切换——从你开始写代码的那一刻起，你就获得了完整的类型检查。这意味着 `noImplicitAny` 和 `strictNullChecks` 始终启用。在 TypeScript 中，这些是通过 `tsconfig.json` 启用的可选编译器选项。Auto 将它们内置到语言中，因为经验表明严格模式能捕获最常见和最具破坏性的 bug。

如果你来自一个没有使用严格模式的 TypeScript 项目，一开始可能会看到更多的编译错误。这是有意为之的——Auto 宁愿在编译期暴露 bug，也不愿让它溜到运行时。

## 速查表

下表总结了本章涵盖的 Auto 和 TypeScript 之间的核心语法差异：

| 概念 | Auto | TypeScript |
|------|------|-----------|
| 不可变变量 | `let x = 5` | `const x = 5` |
| 可变变量 | `var x = 5` | `let x = 5` |
| 类型标注 | `x int` | `x: number` |
| 函数 | `fn add(a int, b int) int` | `function add(a: number, b: number): number` |
| 打印输出 | `print("msg")` | `console.log("msg")` |
| 字符串插值 | `f"text ${x}"` | `` `text ${x}` `` |
