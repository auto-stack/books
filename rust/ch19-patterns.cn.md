# 模式与匹配

模式是 Auto 中用于匹配类型结构（包括复杂和简单类型）的特殊语法。将模式与 `is` 表达式和其他构造结合使用，可以让你更好地控制程序的流程。模式由以下元素的某种组合构成：

- 字面量
- 解构的数组、枚举、类型或元组
- 变量
- 通配符
- 占位符

一些模式示例包括 `x`、`(a, 3)` 和 `Some(Color.Red)`。在模式有效的上下文中，这些组成部分描述了数据的形状。然后我们的程序将值与模式进行匹配，以确定它是否具有正确的数据形状来继续运行特定的代码。

要使用模式，我们将其与某个值进行比较。如果模式匹配该值，我们就在代码中使用该值的部分。回顾第 6 章中使用模式的 `is` 表达式，比如硬币分拣机的例子。如果值符合模式的形状，我们可以使用命名的部分。如果不符合，与该模式关联的代码就不会运行。

本章是关于模式的所有内容的参考。我们将介绍可以使用模式的有效位置、可反驳模式和不可反驳模式之间的区别，以及你可能见过的各种模式语法。到本章结束时，你将知道如何使用模式以清晰的方式表达许多概念。

> **注意：** Auto 使用 `is` 关键字替代 Rust 的 `match`。模式语法几乎完全相同，但关键字不同：`value is { ... }` 而不是 `match value { ... }`。

## 所有可以使用模式的位置

模式在 Auto 中的许多地方都会出现，而且你在不知不觉中已经大量使用了它们！本节讨论所有模式有效的位置。

### `is` 分支

正如第 6 章所讨论的，我们在 `is` 表达式的分支中使用模式。正式地说，`is` 表达式由 `is` 关键字、要匹配的值以及一个或多个由模式和表达式组成的分支定义，如果值匹配该分支的模式，则运行表达式：

```auto
value is {
    PATTERN -> EXPRESSION
    PATTERN -> EXPRESSION
    PATTERN -> EXPRESSION
}
```

例如，以下是第 6 章中匹配 `?int` 值的 `is` 表达式：

<Listing number="19-1" file-name="src/main.at" caption="使用 `is` 匹配可选值">

```auto
x is {
    None -> None
    Some(i) -> Some(i + 1)
}
```

```rust
match x {
    None => None,
    Some(i) => Some(i + 1),
}
```

</Listing>

`is` 表达式的一个要求是它们必须是_穷尽的_——所有可能的情况都必须被考虑到。确保覆盖每种可能性的一种方法是在最后一个分支使用捕获全部的模式。

特殊的 `_` 模式可以匹配任何值，但永远不会绑定到变量，因此通常用于最后一个分支。

### `let` 语句

每次使用 `let` 语句时，你都在使用模式。更正式地说，`let` 语句看起来像这样：

```auto
let PATTERN = EXPRESSION
```

<Listing number="19-2" file-name="src/main.at" caption="使用模式解构元组">

```auto
fn main() {
    let (x, y, z) = (1, 2, 3)
}
```

```rust
fn main() {
    let (x, y, z) = (1, 2, 3);
}
```

</Listing>

这里我们将一个元组与模式进行匹配。Auto 将值 `(1, 2, 3)` 与模式 `(x, y, z)` 比较，发现值匹配模式——即两者元素数量相同——所以 Auto 将 `1` 绑定到 `x`，`2` 绑定到 `y`，`3` 绑定到 `z`。

如果模式中的元素数量与元组中的元素数量不匹配，整体类型就不匹配，我们会得到编译错误。

### 条件 `if let` 表达式

在第 6 章中，我们讨论了如何使用 `if let` 表达式作为只匹配一种情况的 `is` 表达式的简写。

<Listing number="19-3" file-name="src/main.at" caption="混合使用 `if let`、`else if` 和 `else if let`">

```auto
fn main() {
    let favorite_color ?String = None
    let is_tuesday = false
    let age = "34".parse()

    if let Some(color) = favorite_color {
        print(f"Using your favorite color, ${color}, as the background")
    } else if is_tuesday {
        print("Tuesday is green day!")
    } else if let Ok(age) = age {
        if age > 30 {
            print("Using purple as the background color")
        } else {
            print("Using orange as the background color")
        }
    } else {
        print("Using blue as the background color")
    }
}
```

```rust
fn main() {
    let favorite_color: Option<&str> = None;
    let is_tuesday = false;
    let age: Result<u8, _> = "34".parse();

    if let Some(color) = favorite_color {
        println!("Using your favorite color, {color}, as the background");
    } else if is_tuesday {
        println!("Tuesday is green day!");
    } else if let Ok(age) = age {
        if age > 30 {
            println!("Using purple as the background color");
        } else {
            println!("Using orange as the background color");
        }
    } else {
        println!("Using blue as the background color");
    }
}
```

</Listing>

Auto 使用与 Rust 相同的 `if let` 语法。`if let` 也可以引入新变量来遮蔽现有变量，就像 Rust 一样。

### `while let` 条件循环

与 `if let` 类似，`while let` 条件循环允许 `while` 循环在模式继续匹配时持续运行：

<Listing number="19-4" file-name="src/main.at" caption="使用 `while let` 处理消息">

```auto
fn main() {
    let (tx, rx) = channel()
    spawn(() => {
        for val in [1, 2, 3] {
            tx.send(val)
        }
    })

    while let Ok(value) = rx.recv() {
        print(value)
    }
}
```

```rust
fn main() {
    let (tx, rx) = std::sync::mpsc::channel();
    std::thread::spawn(move || {
        for val in [1, 2, 3] {
            tx.send(val).unwrap();
        }
    });

    while let Ok(value) = rx.recv() {
        println!("{value}");
    }
}
```

</Listing>

此示例打印 `1`、`2`，然后打印 `3`。

### `for` 循环

在 `for` 循环中，紧跟在关键字 `for` 后面的值是一个模式。代码清单 19-5 演示了如何在 `for` 循环中使用模式来解构元组。

<Listing number="19-5" file-name="src/main.at" caption="在 `for` 循环中使用模式解构元组">

```auto
fn main() {
    let v = ['a', 'b', 'c']

    for (index, value) in v.enumerate() {
        print(f"${value} is at index ${index}")
    }
}
```

```rust
fn main() {
    let v = vec!['a', 'b', 'c'];

    for (index, value) in v.iter().enumerate() {
        println!("{value} is at index {index}");
    }
}
```

</Listing>

### 函数参数

函数参数也是模式。我们可以在函数参数中解构元组：

<Listing number="19-6" file-name="src/main.at" caption="函数参数解构元组">

```auto
fn print_coordinates(&(x, y) &(int, int)) {
    print(f"Current location: (${x}, ${y})")
}

fn main() {
    let point = (3, 5)
    print_coordinates(&point)
}
```

```rust
fn print_coordinates(&(x, y): &(i32, i32)) {
    println!("Current location: ({x}, {y})");
}

fn main() {
    let point = (3, 5);
    print_coordinates(&point);
}
```

</Listing>

此代码打印 `Current location: (3, 5)`。值 `&(3, 5)` 匹配模式 `&(x, y)`，所以 `x` 是 `3`，`y` 是 `5`。

## 可反驳性：模式是否可能匹配失败

模式有两种形式：_不可反驳的_和_可反驳的_。对于任何传入值都会匹配的模式是_不可反驳的_。例如 `let x = 5` 中的 `x`，因为 `x` 匹配任何值，所以不可能匹配失败。对于某些可能值会匹配失败的模式是_可反驳的_。例如 `if let Some(x) = a_value` 中的 `Some(x)`，因为如果值是 `None`，`Some(x)` 模式就不会匹配。

函数参数、`let` 语句和 `for` 循环只能接受不可反驳的模式，因为当值不匹配时程序无法做有意义的事情。`if let` 和 `while let` 表达式接受可反驳和不可反驳的模式。

如果我们尝试在需要不可反驳模式的地方使用可反驳模式，编译器会产生错误：

<Listing number="19-7" file-name="src/main.at" caption="使用 `let else` 处理可反驳模式">

```auto
fn main() {
    let some_option_value ?int = None
    let Some(x) = some_option_value else {
        return
    }
}
```

```rust
fn main() {
    let some_option_value: Option<i32> = None;
    let Some(x) = some_option_value else {
        return;
    };
}
```

</Listing>

`let ... else` 形式处理模式不匹配的情况。

## 模式语法

### 匹配字面量

<Listing number="19-8" file-name="src/main.at" caption="匹配字面量值">

```auto
fn main() {
    let x = 1

    x is {
        1 -> print("one")
        2 -> print("two")
        3 -> print("three")
        _ -> print("anything")
    }
}
```

```rust
fn main() {
    let x = 1;

    match x {
        1 => println!("one"),
        2 => println!("two"),
        3 => println!("three"),
        _ => println!("anything"),
    }
}
```

</Listing>

此代码打印 `one`，因为 `x` 中的值是 `1`。

### 匹配命名变量

命名变量是匹配任何值的不可反驳模式。但是，在 `is` 表达式中使用命名变量时有一个复杂之处。因为 `is` 开启新的作用域，在表达式中作为模式一部分声明的变量会遮蔽外部同名的变量：

<Listing number="19-9" file-name="src/main.at" caption="`is` 分支中的变量遮蔽">

```auto
fn main() {
    let x = Some(5)
    let y = 10

    x is {
        Some(50) -> print("Got 50")
        Some(y) -> print(f"Matched, y = ${y}")
        _ -> print(f"Default case, x = ${x}")
    }

    print(f"at the end: x = ${x}, y = ${y}")
}
```

```rust
fn main() {
    let x = Some(5);
    let y = 10;

    match x {
        Some(50) => println!("Got 50"),
        Some(y) => println!("Matched, y = {y}"),
        _ => println!("Default case, x = {x:?}"),
    }

    println!("at the end: x = {x:?}, y = {y}");
}
```

</Listing>

这打印 `Matched, y = 5`，因为 `Some(y)` 模式引入了一个新的 `y`，遮蔽了外部的 `y = 10`。最后打印 `at the end: x = Some(5), y = 10`，因为内部 `y` 的作用域已经结束。

### 使用 `|` 匹配多个模式

<Listing number="19-10" file-name="src/main.at" caption="使用 `|` 匹配多个模式">

```auto
fn main() {
    let x = 1

    x is {
        1 | 2 -> print("one or two")
        3 -> print("three")
        _ -> print("anything")
    }
}
```

```rust
fn main() {
    let x = 1;

    match x {
        1 | 2 => println!("one or two"),
        3 => println!("three"),
        _ => println!("anything"),
    }
}
```

</Listing>

### 使用 `..=` 匹配范围

<Listing number="19-11" file-name="src/main.at" caption="匹配值范围">

```auto
fn main() {
    let x = 5

    x is {
        1..=5 -> print("one through five")
        _ -> print("something else")
    }
}
```

```rust
fn main() {
    let x = 5;

    match x {
        1..=5 => println!("one through five"),
        _ => println!("something else"),
    }
}
```

</Listing>

如果 `x` 是 `1`、`2`、`3`、`4` 或 `5`，第一个分支将匹配。范围只允许用于数字或 `char` 值。

### 解构以拆分值

#### 类型（结构体）

<Listing number="19-12" file-name="src/main.at" caption="解构类型的字段">

```auto
type Point {
    x int
    y int
}

fn main() {
    let p = Point(x: 0, y: 7)

    let Point(x, y) = p
    assert_eq(0, x)
    assert_eq(7, y)
}
```

```rust
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 0, y: 7 };
    let Point { x, y } = p;
    assert_eq!(0, x);
    assert_eq!(7, y);
}
```

</Listing>

我们还可以在模式中使用字面值进行解构：

<Listing number="19-13" file-name="src/main.at" caption="解构并匹配字面值">

```auto
type Point {
    x int
    y int
}

fn main() {
    let p = Point(x: 0, y: 7)

    p is {
        Point(x, y: 0) -> print(f"On the x axis at ${x}")
        Point(x: 0, y) -> print(f"On the y axis at ${y}")
        Point(x, y) -> print(f"On neither axis: (${x}, ${y})")
    }
}
```

```rust
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 0, y: 7 };

    match p {
        Point { x, y: 0 } => println!("On the x axis at {x}"),
        Point { x: 0, y } => println!("On the y axis at {y}"),
        Point { x, y } => {
            println!("On neither axis: ({x}, {y})");
        }
    }
}
```

</Listing>

这打印 `On the y axis at 7`，因为 `x` 是 `0`。

#### 枚举

<Listing number="19-14" file-name="src/main.at" caption="解构枚举变体">

```auto
enum Message {
    Quit
    Move(x int, y int)
    Write(text String)
    ChangeColor(r int, g int, b int)
}

fn main() {
    let msg = Message.ChangeColor(0, 160, 255)

    msg is {
        Message.Quit -> {
            print("The Quit variant has no data to destructure.")
        }
        Message.Move(x, y) -> {
            print(f"Move in the x direction ${x} and in the y direction ${y}")
        }
        Message.Write(text) -> {
            print(f"Text message: ${text}")
        }
        Message.ChangeColor(r, g, b) -> {
            print(f"Change color to red ${r}, green ${g}, and blue ${b}")
        }
    }
}
```

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(i32, i32, i32),
}

fn main() {
    let msg = Message::ChangeColor(0, 160, 255);

    match msg {
        Message::Quit => {
            println!("The Quit variant has no data to destructure.");
        }
        Message::Move { x, y } => {
            println!("Move in the x direction {x} and in the y direction {y}");
        }
        Message::Write(text) => {
            println!("Text message: {text}");
        }
        Message::ChangeColor(r, g, b) => {
            println!("Change color to red {r}, green {g}, and blue {b}");
        }
    }
}
```

</Listing>

这打印 `Change color to red 0, green 160, and blue 255`。

#### 嵌套解构

<Listing number="19-15" file-name="src/main.at" caption="匹配嵌套枚举">

```auto
enum Color {
    Rgb(int, int, int)
    Hsv(int, int, int)
}

enum Message {
    Quit
    Move(x int, y int)
    Write(text String)
    ChangeColor(Color)
}

fn main() {
    let msg = Message.ChangeColor(Color.Hsv(0, 160, 255))

    msg is {
        Message.ChangeColor(Color.Rgb(r, g, b)) -> {
            print(f"Change color to red ${r}, green ${g}, and blue ${b}")
        }
        Message.ChangeColor(Color.Hsv(h, s, v)) -> {
            print(f"Change color to hue ${h}, saturation ${s}, value ${v}")
        }
        _ -> {}
    }
}
```

```rust
enum Color {
    Rgb(i32, i32, i32),
    Hsv(i32, i32, i32),
}

enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
    ChangeColor(Color),
}

fn main() {
    let msg = Message::ChangeColor(Color::Hsv(0, 160, 255));

    match msg {
        Message::ChangeColor(Color::Rgb(r, g, b)) => {
            println!("Change color to red {r}, green {g}, and blue {b}");
        }
        Message::ChangeColor(Color::Hsv(h, s, v)) => {
            println!("Change color to hue {h}, saturation {s}, value {v}");
        }
        _ => (),
    }
}
```

</Listing>

### 在模式中忽略值

#### 使用 `_` 忽略整个值

<Listing number="19-16" file-name="src/main.at" caption="使用 `_` 忽略值">

```auto
fn foo(_ int, y int) {
    print(f"This code only uses the y parameter: ${y}")
}

fn main() {
    foo(3, 4)
}
```

```rust
fn foo(_: i32, y: i32) {
    println!("This code only uses the y parameter: {y}");
}

fn main() {
    foo(3, 4);
}
```

</Listing>

#### 使用嵌套的 `_` 忽略部分值

<Listing number="19-17" file-name="src/main.at" caption="忽略元组中的部分值">

```auto
fn main() {
    let numbers = (2, 4, 8, 16, 32)

    numbers is {
        (first, _, third, _, fifth) -> {
            print(f"Some numbers: ${first}, ${third}, ${fifth}")
        }
    }
}
```

```rust
fn main() {
    let numbers = (2, 4, 8, 16, 32);

    match numbers {
        (first, _, third, _, fifth) => {
            println!("Some numbers: {first}, {third}, {fifth}");
        }
    }
}
```

</Listing>

这打印 `Some numbers: 2, 8, 32`。

#### 使用 `_` 前缀标记未使用变量

如果你创建了一个变量但没有使用它，Auto 会发出警告。你可以通过以下划线开头的名称来抑制警告：`_x` 仍然会绑定值，但 `_` 完全不会绑定。这种区别对所有权很重要：`_` 不会移动值，但 `_x` 会。

#### 使用 `..` 忽略剩余部分

<Listing number="19-18" file-name="src/main.at" caption="使用 `..` 忽略剩余字段">

```auto
type Point {
    x int
    y int
    z int
}

fn main() {
    let origin = Point(x: 0, y: 0, z: 0)

    origin is {
        Point(x, ..) -> print(f"x is ${x}")
    }
}
```

```rust
struct Point {
    x: i32,
    y: i32,
    z: i32,
}

fn main() {
    let origin = Point { x: 0, y: 0, z: 0 };

    match origin {
        Point { x, .. } => println!("x is {x}"),
    }
}
```

</Listing>

`..` 模式忽略我们没有显式匹配的值的所有部分。它必须是无歧义的——每个模式中只能使用一次 `..`。

### 匹配守卫

_匹配守卫_是在 `is` 分支的模式之后指定的额外 `if` 条件，该条件也必须匹配才能选择该分支：

<Listing number="19-19" file-name="src/main.at" caption="为模式添加匹配守卫">

```auto
fn main() {
    let num = Some(4)

    num is {
        Some(x) if x % 2 == 0 -> print(f"The number ${x} is even")
        Some(x) -> print(f"The number ${x} is odd")
        None -> {}
    }
}
```

```rust
fn main() {
    let num = Some(4);

    match num {
        Some(x) if x % 2 == 0 => println!("The number {x} is even"),
        Some(x) => println!("The number {x} is odd"),
        None => (),
    }
}
```

</Listing>

这打印 `The number 4 is even`。

匹配守卫用于表达模式本身无法表达的更复杂想法。你还可以使用守卫与外部变量进行比较：

<Listing number="19-20" file-name="src/main.at" caption="使用匹配守卫与外部变量比较">

```auto
fn main() {
    let x = Some(5)
    let y = 10

    x is {
        Some(50) -> print("Got 50")
        Some(n) if n == y -> print(f"Matched, n = ${n}")
        _ -> print(f"Default case, x = ${x}")
    }

    print(f"at the end: x = ${x}, y = ${y}")
}
```

```rust
fn main() {
    let x = Some(5);
    let y = 10;

    match x {
        Some(50) => println!("Got 50"),
        Some(n) if n == y => println!("Matched, n = {n}"),
        _ => println!("Default case, x = {x:?}"),
    }

    println!("at the end: x = {x:?}, y = {y}");
}
```

</Listing>

### `@` 绑定

`@` 操作符允许我们在测试值是否匹配模式的同时创建一个保存该值的变量：

<Listing number="19-21" file-name="src/main.at" caption="使用 `@` 在测试时绑定">

```auto
enum Message {
    Hello(id int)
}

fn main() {
    let msg = Message.Hello(id: 5)

    msg is {
        Message.Hello(id @ 3..=7) -> {
            print(f"Found an id in range: ${id}")
        }
        Message.Hello(id @ 10..=12) -> {
            print("Found an id in another range")
        }
        Message.Hello(id) -> print(f"Found some other id: ${id}")
    }
}
```

```rust
enum Message {
    Hello { id: i32 },
}

fn main() {
    let msg = Message::Hello { id: 5 };

    match msg {
        Message::Hello { id: id @ 3..=7 } => {
            println!("Found an id in range: {id}")
        }
        Message::Hello { id: 10..=12 } => {
            println!("Found an id in another range");
        }
        Message::Hello { id } => println!("Found some other id: {id}"),
    }
}
```

</Listing>

这打印 `Found an id in range: 5`。通过在范围 `3..=7` 之前指定 `id @`，我们捕获了匹配范围的值，同时也测试了它。

## `is` vs `match` 速查表

| 功能 | Auto（`is`） | Rust（`match`） |
|------|-------------|----------------|
| 关键字 | `is` | `match` |
| 分支语法 | `PATTERN -> EXPR` | `PATTERN => EXPR,` |
| 穷尽性 | 必须 | 必须 |
| 通配符 | `_` | `_` |
| 多个模式 | `1 \| 2` | `1 \| 2` |
| 范围 | `1..=5` | `1..=5` |
| 匹配守卫 | `if condition` | `if condition` |
| 绑定 | `x @ 1..=5` | `x @ 1..=5` |
| 忽略剩余 | `..` | `..` |
| 解构类型 | `Type(x, y)` | `Type { x, y }` |
| 解构枚举 | `Enum.Variant(x)` | `Enum::Variant(x)` |

## 总结

Auto 的模式在区分不同类型的数据方面非常有用。当在 `is` 表达式中使用时，Auto 确保你的模式覆盖了所有可能的值，否则程序不会编译。`let` 语句和函数参数中的模式使这些构造更加有用，能够将值解构为更小的部分并将这些部分赋给变量。我们可以创建简单或复杂的模式来满足我们的需求。

与 Rust 的主要语法差异是使用 `is` 而不是 `match`，以及 `->` 而不是 `=>`。模式语法本身——字面量、变量、通配符、范围、守卫和 `@` 绑定——几乎完全相同。

在下一章中，我们将探讨 Auto 的一些高级特性，包括 `sys`（Auto 的 `unsafe` 等价物）和编译期元编程。
