# 枚举与模式匹配

在本章中，我们将介绍 _枚举（enumerations）_，也称为 _enums_。枚举允许你通过列举其可能的变体来定义一个类型。首先，我们将定义和使用一个枚举，展示枚举如何将含义与数据一起编码。接下来，我们将探索一个特别有用的枚举 —— `Option`，它表示一个值可以是某个值，也可以什么都不是。然后，我们将了解如何使用 `is` 关键字进行模式匹配，从而轻松地为枚举的不同值运行不同的代码。最后，我们将介绍 Auto 的 `??` 运算符如何提供一种简洁的方式来处理可选值。

## 定义枚举

结构体提供了一种将相关字段和数据组织在一起的方式（比如带有 `width` 和 `height` 的 `Rectangle`），而枚举则提供了一种表示某个值是一组可能值之一的方式。例如，我们可能想说 `Rectangle` 是一组可能形状中的一种，这组形状还包括 `Circle` 和 `Triangle`。为此，Auto 允许我们将这些可能性编码为枚举。

让我们看一个需要在代码中表达的场景，看看为什么枚举比结构体更合适。假设我们需要处理方向。我们可以 _枚举_ 所有可能的变体 —— 这就是"枚举"名称的由来。

<Listing number="6-1" file-name="main.auto" caption="定义一个 `Direction` 枚举">

```auto
enum Direction {
    North
    South
    East
    West
}

fn main() {
    let heading = Direction.North
    print(f"Heading: ${heading}")
}
```

```rust
enum Direction {
    North,
    South,
    East,
    West,
}

fn main() {
    let heading = Direction::North;
    println!("Heading: {}", heading);
}
```

</Listing>

`Direction` 现在是一个自定义数据类型，可以在代码的其他地方使用。注意与 Rust 的关键区别：

| 特性 | Auto | Rust |
|------|------|------|
| 访问变体 | `Direction.North` | `Direction::North` |
| 显示输出 | `${dir}`（自动 Display） | 需要 `#[derive(Display)]` |

Auto 使用点号（`.`）访问枚举变体，而 Rust 使用双冒号（`::`）。Auto 还会自动为枚举生成 `Display` 实现，允许你直接在字符串插值中使用它们。

### 枚举值

我们可以创建每个变体的实例，并将它们传递给函数：

<Listing number="6-2" file-name="main.auto" caption="将枚举值传递给函数">

```auto
enum Direction {
    North
    South
    East
    West
}

fn print_direction(dir Direction) {
    print(f"Direction: ${dir}")
}

fn main() {
    let heading = Direction.North
    print_direction(heading)
}
```

```rust
enum Direction {
    North,
    South,
    East,
    West,
}

fn print_direction(dir: Direction) {
    println!("Direction: {}", dir);
}

fn main() {
    let heading = Direction::North;
    print_direction(heading);
}
```

</Listing>

### 带数据的枚举

枚举相对于结构体的一个优势是，每个变体可以持有不同类型和数量的数据。我们不需要在结构体内部嵌套枚举，而是可以直接将数据放入每个枚举变体中：

<Listing number="6-3" file-name="main.auto" caption="一个 `IpAddr` 枚举，其变体存储 `String` 值">

```auto
enum IpAddr {
    V4 String
    V6 String
}

fn main() {
    let home = IpAddr.V4("127.0.0.1")
    let loopback = IpAddr.V6("::1")
    print("IP addresses created")
}
```

```rust
enum IpAddr {
    V4(String),
    V6(String),
}

fn main() {
    let home = IpAddr::V4(String::from("127.0.0.1"));
    let loopback = IpAddr::V6(String::from("::1"));
    println!("IP addresses created");
}
```

</Listing>

每个变体可以有不同类型和数量的关联数据。以下是空变体和带数据变体混合的例子：

<Listing number="6-4" file-name="main.auto" caption="一个 `Message` 枚举，不同变体持有不同数据">

```auto
enum Message {
    Quit
    Write String
}

fn main() {
    let msg = Message.Write("hello")
    print("Message created")
}
```

```rust
enum Message {
    Quit,
    Write(String),
}

fn main() {
    let msg = Message::Write(String::from("hello"));
    println!("Message created");
}
```

</Listing>

关键区别：

| 特性 | Auto | Rust |
|------|------|------|
| 空变体 | `Quit`（无括号） | `Quit` |
| 带数据变体 | `Write String` | `Write(String)` |
| 构造带数据变体 | `Message.Write("hello")` | `Message::Write(String::from("hello"))` |

### 枚举方法

与结构体一样，我们可以使用 `ext` 关键字为枚举定义方法：

<Listing number="6-10" file-name="main.auto" caption="使用 `ext` 在枚举上定义方法">

```auto
enum Message {
    Quit
    Write String
}

ext Message {
    fn call() {
        print("Message called")
    }
}

fn main() {
    let msg = Message.Write("hello")
    msg.call()
}
```

```rust
enum Message {
    Quit,
    Write(String),
}

impl Message {
    fn call(&self) {
        println!("Message called");
    }
}

fn main() {
    let msg = Message::Write(String::from("hello"));
    msg.call();
}
```

</Listing>

`ext` 关键字对枚举的工作方式与结构体相同 —— 它添加方法（生成 Rust 的 `impl` 块），使用隐式 `self` 和 `.field` 简写。

### `Option` 枚举

Auto 的 `Option` 类型使用 `?T` 语法表示，代表一个值可能是某个值，也可能什么都不是。这是 Auto 中等价于 Rust `Option<T>` 的写法：

```auto
// ?T 是 May<T>（Auto 的 Option 类型）的语法糖
// 它可以是 Some(value) 或 None
```

```rust
// Option<T> 可以是 Some(value) 或 None
```

`?T` 语法消除了 Tony Hoare 著名的"十亿美元错误"——空引用问题。Auto 不使用 null，而是让你显式处理值可能缺失的情况。

<Listing number="6-7" file-name="main.auto" caption="使用 `?T` 作为返回类型，配合 `Some` 和 `None`">

```auto
fn maybe_value(x int) ?int {
    if x > 0 {
        return Some(x)
    }
    return None
}

fn main() {
    let result1 = maybe_value(10)
    let result2 = maybe_value(-5)
    print("Done")
}
```

```rust
fn maybe_value(x: i32) -> Option<i32> {
    if x > 0 {
        return Some(x);
    }
    return None;
}

fn main() {
    let result1 = maybe_value(10);
    let result2 = maybe_value(-5);
    println!("Done");
}
```

</Listing>

Option 的关键区别：

| 特性 | Auto | Rust |
|------|------|------|
| Option 类型 | `?T` | `Option<T>` |
| 有值 | `Some(value)` | `Some(value)` |
| 无值 | `None` | `None` |
| 函数返回 | `fn foo() ?int` | `fn foo() -> Option<i32>` |

因为 `?T` 和 `T` 是不同的类型，编译器不会让你把可选值当作确定存在的值来使用。你必须显式处理 `None` 的情况。

## 使用 `is` 进行模式匹配

Auto 使用 `is` 关键字进行模式匹配，等价于 Rust 的 `match` 表达式。`is` 表达式将一个值与一系列模式进行比较，并根据匹配到的模式执行相应的代码。

### 基本模式匹配

<Listing number="6-5" file-name="main.auto" caption="使用 `is` 对枚举进行模式匹配">

```auto
enum Coin {
    Penny int
    Nickel int
    Dime int
    Quarter int
}

fn value_in_cents(coin Coin) int {
    is coin {
        Coin.Penny(v) => v
        Coin.Nickel(v) => v
        Coin.Dime(v) => v
        Coin.Quarter(v) => v
    }
}

fn main() {
    let c = Coin.Penny(1)
    print(f"Value: ${value_in_cents(c)}")
}
```

```rust
enum Coin {
    Penny(i32),
    Nickel(i32),
    Dime(i32),
    Quarter(i32),
}

fn value_in_cents(coin: Coin) -> i32 {
    match coin {
        Coin::Penny(v) => v,
        Coin::Nickel(v) => v,
        Coin::Dime(v) => v,
        Coin::Quarter(v) => v,
    }
}

fn main() {
    let c = Coin::Penny(1);
    println!("Value: {}", value_in_cents(c));
}
```

</Listing>

关键区别：

| 特性 | Auto | Rust |
|------|------|------|
| 匹配关键字 | `is value { }` | `match value { }` |
| 通配符分支 | `else =>` | `_ =>` |
| 分支分隔符 | 换行（无逗号） | 分支之间用逗号 |
| 模式语法 | `Variant.Name(binding)` | `Variant::Name(binding)` |

### 绑定值的模式

`is` 最强大的特性之一是模式可以绑定到枚举变体内部的值：

<Listing number="6-6" file-name="main.auto" caption="使用 `is` 解构枚举变体">

```auto
enum Atom {
    Int int
    Char char
    Float float
}

fn main() {
    let atom = Atom.Int(11)

    is atom {
        Atom.Int(i) => print(f"Got Int: ${i}")
        Atom.Char(c) => print(f"Got Char: ${c}")
        Atom.Float(f) => print(f"Got Float: ${f}")
    }
}
```

```rust
enum Atom {
    Int(i32),
    Char(char),
    Float(f64),
}

fn main() {
    let atom = Atom::Int(11);

    match atom {
        Atom::Int(i) => println!("Got Int: {}", i),
        Atom::Char(c) => println!("Got Char: {}", c),
        Atom::Float(f) => println!("Got Float: {}", f),
    }
}
```

</Listing>

当 `atom` 是 `Atom.Int(11)` 时，模式 `Atom.Int(i)` 匹配，`i` 绑定到值 `11`。绑定的变量随后可以在分支代码中使用。

### 使用 `is` 匹配 Option

我们可以像处理其他枚举一样，使用 `is` 来处理 `?T`（Option）值：

<Listing number="6-8" file-name="main.auto" caption="使用 `is` 匹配 `?int`（Option）值">

```auto
fn plus_one(x ?int) ?int {
    is x {
        None => None
        Some(i) => Some(i + 1)
    }
}

fn main() {
    let five = Some(5)
    let six = plus_one(five)
    let none = plus_one(None)
    print("Done")
}
```

```rust
fn plus_one(x: Option<i32>) -> Option<i32> {
    match x {
        None => None,
        Some(i) => Some(i + 1),
    }
}

fn main() {
    let five = Some(5);
    let six = plus_one(five);
    let none = plus_one(None);
    println!("Done");
}
```

</Listing>

### 匹配是穷尽的

与 Rust 的 `match` 一样，Auto 的 `is` 是穷尽的 —— 编译器会确保你处理了每一种可能的情况。如果你遗漏了某个情况，你将得到编译时错误。

### 使用 `else` 作为通配符

`else` 分支是通配符模式，等价于 Rust 的 `_`：

<Listing number="6-9" file-name="main.auto" caption="使用 `else` 作为通配符模式">

```auto
fn dice_roll(value int) {
    is value {
        3 => print("Lucky number 3!")
        7 => print("Got a 7!")
        else => print(f"Rolled: ${value}")
    }
}

fn main() {
    dice_roll(3)
    dice_roll(7)
    dice_roll(5)
}
```

```rust
fn dice_roll(value: i32) {
    match value {
        3 => println!("Lucky number 3!"),
        7 => println!("Got a 7!"),
        _ => println!("Rolled: {}", value),
    }
}

fn main() {
    dice_roll(3);
    dice_roll(7);
    dice_roll(5);
}
```

</Listing>

`else` 分支匹配所有未在其他分支中列出的值。注意 `else` 必须放在最后，因为分支是按顺序求值的。

## 使用 `??` 简洁处理可选值

`??`（空值合并）运算符提供了一种简洁的方式来为可选值提供默认值：

<Listing number="6-11" file-name="main.auto" caption="`??` 空值合并运算符">

```auto
fn main() {
    let x = 10
    let y = x ?? 0
    print(f"y = ${y}")
}
```

```rust
fn main() {
    let x = Some(10);
    let y = x.unwrap_or(0);
    println!("y = {}", y);
}
```

</Listing>

`??` 运算符是 Auto 中等价于 Rust `.unwrap_or()` 方法的写法。如果左侧有值，就返回该值；否则返回右侧的默认值。

当你想提供一个回退值而不需要使用完整的 `is` 匹配时，这非常有用：

```auto
// 繁琐：完整的 is 匹配
let result = is optional_value {
    Some(v) => v
    None => default_value
}

// 简洁：?? 运算符
let result = optional_value ?? default_value
```

## 总结

Auto 的枚举和模式匹配提供了与 Rust 相同的强大功能，但语法更加简洁：

| 概念 | Auto | Rust |
|------|------|------|
| 定义枚举 | `enum Name { ... }` | `enum Name { ... }` |
| 访问变体 | `Name.Variant` | `Name::Variant` |
| 数据变体 | `Variant Type` | `Variant(Type)` |
| 模式匹配 | `is value { }` | `match value { }` |
| 通配符分支 | `else =>` | `_ =>` |
| Option 类型 | `?T` | `Option<T>` |
| 有值 | `Some(value)` | `Some(value)` |
| 无值 | `None` | `None` |
| 空值合并 | `x ?? default` | `x.unwrap_or(default)` |
| 枚举方法 | `ext Name { }` | `impl Name { }` |

枚举是 Auto 工具箱中一个强大的工具。结合第 5 章的结构体，你可以创建自定义类型来表达程序领域中的概念。`is` 模式匹配和 `??` 运算符使得处理枚举和可选值既安全又简洁。

接下来让我们进入第 7 章，了解 Auto 如何使用包和模块来组织代码。
