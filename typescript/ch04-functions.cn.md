# 更多关于函数

Auto 中的函数使用 `fn` 关键字，类型注解用空格分隔。本章介绍闭包、
泛型、可选参数以及其他与函数相关的特性。

## 闭包（箭头函数）

Auto 支持使用箭头语法 `(params) => expression` 定义闭包。闭包可以
捕获周围作用域中的变量，并赋值给变量或作为参数传递。

<Listing number="04-01" file="listings/ch04/listing-04-01/main.at" caption="闭包">

```auto
fn main() {
    let add = (a int, b int) => a + b
    let double = (n int) => n * 2

    print(add(3, 4))
    print(double(5))
}
```

```typescript
function main(): void {
    const add: (number, number) => any = (a: number, b: number) => a + b;
    const double: (number) => number = (n: number) => n * 2;
    

    console.log(add(3, 4));
    console.log(double(5));
}

main();
```

</Listing>

带类型注解的闭包直接转译为带相同类型的 TypeScript 箭头函数。参数类型
在输出中保留。

## 泛型函数

泛型允许你编写适用于任何类型的函数。Auto 使用与 TypeScript 相同的
`<T>` 语法：

<Listing number="04-02" file="listings/ch04/listing-04-02/main.at" caption="泛型函数">

```auto
fn identity<T>(arg T) T {
    arg
}

fn main() {
    let a = identity(5)
    let b = identity("hello")
    print(a)
    print(b)
}
```

```typescript
function identity(arg: T): T {
    arg;
}

function main(): void {
    const a = identity(5);
    const b = identity("hello");
    console.log(a);
    console.log(b);
}

main();
```

</Listing>

类型参数 `<T>` 会直接传递到 TypeScript 输出中。TypeScript 从参数推断
具体类型——调用时无需显式指定类型参数。

## 泛型与数组

泛型与数组类型配合使用特别方便。你可以编写接受任意元素类型数组的函数：

<Listing number="04-03" file="listings/ch04/listing-04-03/main.at" caption="带数组的泛型函数">

```auto
fn first<T>(arr []T) T {
    arr[0]
}

fn main() {
    let nums = [1, 2, 3]
    let n = first(nums)
    print(n)
}
```

```typescript
function first(arr: T[]): T {
    arr[0];
}

function main(): void {
    const nums: number[] = [1, 2, 3];
    const n = first(nums);
    console.log(n);
}

main();
```

</Listing>

注意 Auto 中的 `[]T` 在 TypeScript 中变为 `T[]`——括号位置是相反的。

## 可选参数

可选参数在参数名前使用 `?` 前缀。可选参数在调用时可以省略，在函数体
内其类型变为 `T | null`。

<Listing number="04-05" file="listings/ch04/listing-04-05/main.at" caption="可选参数">

```auto
fn greet(name int, greeting? int) {
    if greeting {
        print(greeting, name)
    } else {
        print(name)
    }
}

fn main() {
    greet(42)
    greet(42, 1)
}
```

```typescript
function greet(name: number, greeting: number | null): void {
    if (greeting) {
        console.log(greeting, name);
    } else {
        console.log(name);
    }
}

function main(): void {
    greet(42);
    greet(42, 1);
}

main();
```

</Listing>

Auto 中的可选参数直接转译为 TypeScript 的可选参数（`param?: T`）。
使用 `if` 检查来确定参数是否被提供。

## 特殊返回类型

TypeScript 有几种与函数相关的特殊类型：

| TypeScript | Auto | 描述 |
|-----------|------|------|
| `void` | （隐式） | 函数无返回值 |
| `unknown` | — | 比 `any` 更安全的替代 |
| `never` | — | 函数永不返回 |
| `Function` | — | 无类型函数（避免使用） |

Auto 没有将 `unknown`、`never` 或 `Function` 作为显式类型。不返回值的
函数在 TypeScript 输出中隐式具有 `void` 返回类型。

## TypeScript 独有功能

### 函数重载

```typescript
// 仅限 TypeScript
function makeDate(timestamp: number): Date;
function makeDate(m: number, d: number, y: number): Date;
function makeDate(mOrTimestamp: number, d?: number, y?: number): Date {
    // 实现
}
```

Auto 不支持函数重载。请改用带联合参数类型的单一函数或基于枚举的分发。

### 剩余参数

```typescript
// 仅限 TypeScript
function sum(...nums: number[]): number {
    return nums.reduce((a, b) => a + b, 0);
}
```

### `this` 参数

```typescript
// 仅限 TypeScript
db.filterUsers(function (this: User) {
    console.log(this.name);
});
```

Auto 使用 `self` 而不是 `this`，并且不支持显式的 `this` 参数声明。

## 快速参考

| TypeScript | Auto | 描述 |
|-----------|------|------|
| `(a: number) => number` | `(a int) => int` | 箭头函数 |
| `function f<T>(x: T): T` | `fn f<T>(x T) T` | 泛型函数 |
| `function f(x?: number)` | `fn f(x? int)` | 可选参数 |
| `function f(...args: number[])` | — | 剩余参数 |
| `f<number>(x)` | `f(x)` | 类型参数推断 |
