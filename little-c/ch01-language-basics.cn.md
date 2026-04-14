# 语言基础

本章介绍 Auto 的基本构建块以及它们如何映射到 C。你将学习数据类型、变量、运算符、
控制流、循环、函数和作用域。

## 11. 数据类型

Auto 提供五种基本类型，直接映射到 C 类型：

| Auto 类型 | C 类型 | 说明 |
|-----------|--------|------|
| `int` | `int` | 整数（通常为 32 位）|
| `float` | `float` | 浮点数 |
| `bool` | `int` | 布尔值（0 或 1）|
| `char` | `char` | 单个字符 |
| `str` | `char*` | 字符串（以 null 结尾）|

Auto 的 `bool` 映射到 C 的 `int`，因为 C 直到 C99 才有原生的 `_Bool` 类型，
而许多 C 代码库仍然使用 `int` 作为布尔值。

<Listing name="data-types" file="listings/ch01/listing-01-01">

```auto
fn main() {
    let age int = 25
    let height float = 1.75
    let initial char = 'A'
    let name str = "Auto"
    let active bool = true

    print("Age:", age)
    print("Height:", height)
    print("Initial:", initial)
    print("Name:", name)
    print("Active:", active)
}
```

</Listing>

a2c 转译器为每种类型添加正确的格式说明符：`%d` 用于 `int`，`%f` 用于 `float`，
`%c` 用于 `char`，`%s` 用于 `str`。

## 12. 常量与作用域

Auto 使用 `let` 表示不可变绑定，使用 `var` 表示可变变量：

```auto
let pi float = 3.14      // 不可变
var count int = 0        // 可变
count = count + 1        // 正确
```

在 C 中映射为 `const float pi = 3.14f;` 和 `int count = 0;`。块作用域在两种
语言中工作方式相同——在 `{ }` 内声明的变量是该块的局部变量。

## 13. 运算符

Auto 的运算符与 C 几乎完全相同。

<Listing name="operators" file="listings/ch01/listing-01-02">

```auto
fn main() {
    let a int = 10
    let b int = 3

    print("a + b =", a + b)
    print("a - b =", a - b)
    print("a * b =", a * b)
    print("a / b =", a / b)
    print("a % b =", a % b)

    print("a == b:", a == b)
    print("a > b:", a > b)
    print("a && b:", a > 0 && b > 0)
}
```

</Listing>

算术运算符（`+`、`-`、`*`、`/`、`%`）、比较运算符（`==`、`!=`、`>`、`<`、
`>=`、`<=`）和逻辑运算符（`&&`、`||`）都直接映射到对应的 C 运算符。

> **仅 C**：C 有位赋值运算符（`&=`、`|=`、`^=`、`<<=`、`>>=`）和逗号运算符。
> Auto 不直接提供这些。

## 14. 控制流

Auto 提供 `if`/`else` 进行条件判断，提供 `is` 进行模式匹配（映射到 C 的 `switch`）。

<Listing name="control-flow" file="listings/ch01/listing-01-03">

```auto
fn classify(n int) str {
    if n > 0 {
        "positive"
    } else if n < 0 {
        "negative"
    } else {
        "zero"
    }
}

fn describe(x int) str {
    is x {
        0 => "nothing"
        1 => "one"
        2 => "two"
        else => "many"
    }
}
```

</Listing>

`is` 表达式转译为 C 的 `switch` 语句。与 C 的 `switch` 不同，Auto 的 `is` 不
需要 `break` 语句——每个分支隐式返回，不存在穿透问题。

## 15. 循环

Auto 提供 `for` 用于计数迭代，`while` 用于条件循环。

<Listing name="loops" file="listings/ch01/listing-01-04">

```auto
fn main() {
    for i in 0..5 {
        print("i =", i)
    }

    var sum int = 0
    var n int = 1
    while n <= 10 {
        sum = sum + n
        n = n + 1
    }
    print("Sum 1..10 =", sum)
}
```

</Listing>

范围循环 `for i in 0..5` 映射为 `for (int i = 0; i < 5; i++)`。`while` 循环
直接映射到 C 的 `while`，语义完全相同。

> **仅 C**：C 有 `do...while` 和 `goto`。Auto 不提供 `goto`。`do...while`
> 的等价写法可以用 `while true` 加 `break` 实现。

## 16. 函数

Auto 函数声明带有类型参数和可选的返回类型。如果未指定返回类型，函数在 C 中
返回 `void`。

<Listing name="functions" file="listings/ch01/listing-01-05">

```auto
fn add(a int, b int) int {
    a + b
}

fn factorial(n int) int {
    if n <= 1 {
        1
    } else {
        n * factorial(n - 1)
    }
}
```

</Listing>

函数体中的最后一个表达式是返回值。a2c 转译器在生成的 C 中插入显式的 `return`
语句。不需要前向声明——Auto 会自动处理顺序。

## 17. 作用域与变量遮蔽

Auto 和 C 都使用块作用域。Auto 还支持变量遮蔽——在内部作用域中重新声明同名变量：

```auto
let x int = 10
if true {
    let x int = 20
    print(x)    // 20
}
print(x)        // 10
```

在 C 中，遮蔽通过嵌套 `{ }` 块以相同方式工作。

## 18. 类型转换

Auto 提供兼容类型之间的显式类型转换。`let y float = float(x)` 映射到 C 的
`(float)x`。Auto 不允许不安全的转换（例如将 `str` 转换为 `int`），转译器会
拒绝无效转换。

## 19. 递归

递归在 Auto 和 C 中的工作方式完全相同。清单 01-05 中的 `factorial` 函数就是
经典示例。Auto 支持直接递归和相互递归，a2c 转译器会自动处理前向声明。

## 20. 练习：计算器

将所有内容整合到一个简单的计算器中。

<Listing name="calculator" file="listings/ch01/listing-01-06">

```auto
fn calculate(a int, op str, b int) int {
    if op == "+" {
        a + b
    } else if op == "-" {
        a - b
    } else if op == "*" {
        a * b
    } else if op == "/" {
        if b == 0 {
            print("Error: division by zero")
            0
        } else {
            a / b
        }
    } else {
        print("Unknown operator:", op)
        0
    }
}

fn main() {
    print("10 + 3 =", calculate(10, "+", 3))
    print("10 - 3 =", calculate(10, "-", 3))
    print("10 * 3 =", calculate(10, "*", 3))
    print("10 / 3 =", calculate(10, "/", 3))
    print("10 / 0 =", calculate(10, "/", 0))
}
```

</Listing>

注意 Auto 中的 `op == "+"` 在生成的 C 中变为 `strcmp(op, "+") == 0`。C 中的
字符串比较需要 `strcmp`；Auto 的 `==` 运算符会自动处理。

## 快速参考

| 概念 | Auto | C |
|------|------|---|
| 整数 | `int` | `int` |
| 浮点数 | `float` | `float` |
| 布尔值 | `bool` | `int` (0/1) |
| 字符串 | `str` | `char*` |
| 字符 | `char` | `char` |
| 不可变 | `let x int = 5` | `const int x = 5;` |
| 可变 | `var x int = 5` | `int x = 5;` |
| 条判断 | `if { } else { }` | `if () { } else { }` |
| 分支匹配 | `is x { ... }` | `switch (x) { ... }` |
| 计数循环 | `for i in 0..n` | `for (int i=0; i<n; i++)` |
| 条件循环 | `while cond { }` | `while (cond) { }` |
| 函数 | `fn name(params) type { }` | `type name(params) { }` |
| 隐式返回 | 最后一个表达式 | 显式 `return` |
| 字符串比较 | `a == b` | `strcmp(a, b) == 0` |
