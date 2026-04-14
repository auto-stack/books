# 语言基础

本章涵盖基础语言概念，对比 JavaScript 的设计选择与 Auto 如何处理
同样的问题。理解这些差异是编写地道 Auto 代码的关键。

## 相等性：无隐式转换

JavaScript 有两个相等运算符：`==`（带类型转换）和 `===`（严格）。
强制转换的 `==` 会产生令人意外的结果：

```typescript
// TypeScript / JavaScript
"" == "0";     // false
0 == "";       // true（！）
null == undefined; // true
```

Auto **没有隐式转换**。相等性总是比较相同类型的值：

```auto
// Auto
1 == 1         // true
1 == 2         // false
"a" == "a"     // true
// 类型之间没有隐式转换
```

## 引用与值

在 JavaScript 中，对象是引用类型——赋值对象不会复制它，通过一个变量
的修改在所有别名中可见：

```typescript
// TypeScript / JavaScript
const foo = { x: 1 };
const bar = foo;
foo.x = 2;
console.log(bar.x);  // 2 — 同一个引用
```

Auto 更明确地区分值和引用语义。基本类型（`int`、`float`、`str`、`bool`）
是值类型——赋值时复制。复杂类型（`type` 实例、列表）默认是引用语义，
但需要时可以显式复制。

## 空值

JavaScript 有两个"空"值：`undefined`（未初始化）和 `null`（有意为空）。
这造成了混淆：

```typescript
// TypeScript
let x;              // undefined
let y = null;        // null
typeof undefined;    // "undefined"
typeof null;         // "object"（！）
```

Auto 使用单一的 `nil` 值表示"无值"：

```auto
// Auto
var x int           // 默认值取决于类型
let y = nil         // 显式无值
```

对于可选值，Auto 使用 `?T` 可空类型（类似 Rust 的 `Option<T>`），通过
模式匹配来检查：

```auto
fn process(name ?str) {
    name is
        Some(n) => print("Got:", n)
        None => print("No name provided")
}
```

## `this` 绑定

在 JavaScript 中，`this` 由函数的*调用方式*决定，而非定义位置。
这是 JavaScript 最令人困惑的方面之一：

```typescript
// TypeScript / JavaScript
const obj = {
    name: "Alice",
    greet() { console.log(this.name); }
};
obj.greet();    // "Alice" — this = obj
const fn = obj.greet;
fn();           // undefined — this = global/undefined
```

Auto 使用**显式的 `self`**。没有动态的 `this` 绑定——`self` 始终
引用当前实例：

<Listing name="self-in-methods" file="listings/ch01-self-in-methods">

```auto
type User {
    name str
    fn greet() {
        print("Hello from " + self.name)
    }
}

fn main() {
    let user = User("Alice")
    user.greet()
}
```

</Listing>

## 闭包

闭包是从外层作用域捕获变量的函数。JavaScript 和 Auto 都支持闭包，
但 Auto 的类型系统提供更强的保证：

<Listing name="closure-counter" file="listings/ch01-closure-counter">

```auto
fn apply(f fn(int) int, x int) int {
    f(x)
}

fn double(x int) int {
    x * 2
}

fn main() {
    let result = apply(double, 5)
    print(result)
}
```

</Listing>

## 数字

JavaScript 只有一种数字类型（`number`），即 64 位浮点数。这会导致
IEEE 754 精度问题：

```typescript
// TypeScript / JavaScript
0.1 + 0.2;  // 0.30000000000000004
```

Auto 有**独立的整数和浮点类型**：

```auto
// Auto
let x int = 42          // 整数
let y f64 = 3.14        // 浮点数
let z = 0.1 + 0.2       // f64，同样有 IEEE 754 行为
```

## 真值性：显式条件

JavaScript 在条件中隐式将值转换为布尔值。假值包括 `false`、`0`、`NaN`、
`""`、`null`、`undefined`——其他都是真值：

```typescript
// TypeScript / JavaScript
if ("hello") { }   // truthy
if (0) { }         // falsy
if ({}) { }        // truthy（即使是空对象！）
```

Auto 要求**显式布尔条件**：

```auto
// Auto
let name = "Alice"
if name != nil {       // 显式 nil 检查
    print("Has name")
}

if count > 0 {          // 显式布尔表达式
    print("Positive")
}
```

## 快速参考

| JavaScript 怪癖 | Auto 的处理方式 |
|----------------|----------------|
| `==` 类型转换 | 无隐式转换 |
| 两个空值（`null`、`undefined`） | 单一 `nil` + `?T` 可空类型 |
| 动态 `this` 绑定 | 方法中使用显式 `self` |
| 单一 `number` 类型 | 独立的 `int`、`float`、`double` |
| 隐式真值性 | 显式布尔条件 |
| `var` 是函数作用域 | `let`（不可变）/ `var`（可变）块作用域 |
| 没有深层不可变性 | `let` 默认不可变 |
