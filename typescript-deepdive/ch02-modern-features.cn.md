# 现代语言特性

本章涵盖 TypeScript 从 ES6+ 采用的现代编程语言特性，以及 Auto 对
这些概念各自的处理方式。

## 类 → 带方法的类型

TypeScript 使用 ES6 类，包含 `constructor`、`extends` 和访问修饰符：

```typescript
// TypeScript
class Point {
    constructor(public x: number, public y: number) {}
    add(other: Point): Point {
        return new Point(this.x + other.x, this.y + other.y);
    }
}

class Point3D extends Point {
    constructor(x: number, y: number, public z: number) {
        super(x, y);
    }
}
```

Auto 使用 `type` 声明配合内联方法。继承使用 `is` 关键字：

```auto
type Point {
    x int
    y int

    fn add(other Point) Point {
        Point(self.x + other.x, self.y + other.y)
    }
}

type Point3D is Point {
    z int

    fn add(other Point3D) Point3D {
        Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
    }
}
```

Auto 没有 `public`/`private`/`protected` 访问修饰符。所有字段默认可访问
（Auto 倾向于简洁而非通过关键字实现封装）。

## 箭头函数 → 闭包

TypeScript 箭头函数有两个用途：简洁语法和词法 `this` 捕获：

```typescript
// TypeScript
const inc = (x: number): number => x + 1;
const nums = [1, 2, 3].map(n => n * 2);
```

Auto 闭包不需要解决 `this` 问题（Auto 使用显式 `self`）。简洁语法
直接对应：

```auto
// Auto
let inc = (x int) => x + 1
let doubled = items.map((n int) => n * 2)
```

函数类型使用 `fn` 关键字进行注解：

```auto
// Auto
let transform: fn(int) int = (x int) => x + 1
```

```typescript
// TypeScript
let transform: (x: number) => number = (x) => x + 1;
```

## `let` / `const` → `let` / `var`

TypeScript 有 `let`（可变，块作用域）和 `const`（不可变）：

```typescript
// TypeScript
let x = 5;       // 可变
const y = 10;    // 不可变
```

Auto 翻转了默认值——`let` 不可变，`var` 可变：

```auto
// Auto
let x = 5        // 不可变 — 不能重新赋值
var y = 10       // 可变 — 可以重新赋值
```

这遵循 Rust 的哲学：不可变是安全的默认值。

## 解构

TypeScript 支持对象和数组的解构：

```typescript
// TypeScript
const { x, y } = point;
const [first, ...rest] = items;
```

Auto 通过 `is` 模式匹配支持解构：

```auto
// Auto
let Point { x, y } = point
```

## 展开 / 剩余参数

TypeScript 使用 `...` 进行展开和收集剩余参数：

```typescript
// TypeScript
const combined = [...list1, ...list2];
const sum = (a: number, b: number, ...rest: number[]) => rest.reduce((x, y) => x + y, 0);
```

Auto 目前没有展开/剩余语法。对于数组，使用 `+` 拼接或方法调用。
可变参数使用尾部 `...`：

```auto
// Auto
let combined = list1 + list2

fn sum(a int, b int, ...) {
    // ... 收集剩余参数
}
```

## 模板字符串 → f-字符串

TypeScript 使用反引号模板字面量和 `${}`：

```typescript
// TypeScript
const greeting = `Hello, ${name}! You are ${age} years old.`;
```

Auto 在 `print()` 中使用 `{}` 进行字符串插值：

```auto
// Auto
print("Hello, {name}! You are {age} years old.")
```

## 迭代器与 `for...of`

TypeScript 使用 `for...of` 迭代：

```typescript
// TypeScript
for (const item of items) {
    console.log(item);
}
```

Auto 使用 `for item in collection`：

```auto
// Auto
for item in items {
    print(item)
}

// 带索引
for i, item in items {
    print("{i}: {item}")
}
```

范围使用 `range()`：

```auto
// Auto
for i in range(1, 10) {
    print(i)
}
```

## Async/Await → `~T` / `on`

TypeScript 使用 `async`/`await`：

```typescript
// TypeScript
async function fetchData(): Promise<string> {
    const response = await fetch(url);
    return response.text();
}
```

Auto 使用 `~T` 表示异步类型，`?` 用于等待：

```auto
// Auto
fn fetch_data() !str {
    let response = http_get(url)?
    response.text()?
}
```

`!` 返回类型表示函数传播错误（等价于返回 `Promise` 或 `Result`）。
`?` 操作符解包值或在出错时提前返回。

## 快速参考

| TypeScript (ES6+) | Auto | 说明 |
|-------------------|------|------|
| `class` / `extends` | `type` / `is` | Auto 使用结构化类型 |
| `(x) => x + 1` | `(x int) => x + 1` | 相同的闭包语法 |
| `fn(x: number): number` | `fn(int) int` | 函数类型注解 |
| `let x = 5` | `let x = 5`（不可变） | Auto 默认不可变 |
| `const x = 5` | `let x = 5` | 相同语义 |
| `var x = 5`（TS — 可变） | `var x = 5`（Auto — 可变） | 相同关键字，不同默认值 |
| `...spread` | 暂不支持 | 使用拼接 |
| `` `${expr}` `` | `print()` 中的 `{expr}` | 字符串插值 |
| `for...of` | `for item in collection` | Auto 使用 `in` 关键字 |
| `async/await` | `!` / `?` | 错误传播模型 |
