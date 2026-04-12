# 使用结构体组织相关数据

_结构体（struct）_ 是一种自定义数据类型，允许你将多个相关的值打包并命名，组成一个有意义的整体。在 Auto 中，结构体使用 `type` 关键字而非 Rust 的 `struct` 关键字来定义，但概念是相同的。如果你熟悉面向对象语言，结构体就像对象的数据属性。

在本章中，我们将比较元组与结构体的异同，演示如何定义和实例化结构体，并讨论如何使用 `type` 块内的内联定义和 `ext` 关键字来定义关联函数和方法。

## 定义和实例化结构体

结构体与元组类似，都可以持有多个相关值。和元组一样，结构体的各个部分可以是不同的类型。与元组不同的是，在结构体中你需要为每个数据片段命名，这样可以清楚地表达各个值的含义。

在 Auto 中定义结构体，我们使用 `type` 关键字并为类型命名。然后，在花括号内定义字段的名称和类型。注意，Auto 使用空格分隔的类型标注（`name Type`），而非 Rust 的冒号语法（`name: Type`）。

<Listing number="5-1" file-name="main.auto" caption="一个 `User` 类型定义">

```auto
type User {
    active bool
    username String
    email String
    sign_in_count int
}

fn main() {
    let user1 = User(true, "someusername123", "someone@example.com", 1)
    print(f"email: ${user1.email}")
}
```

```rust
struct User {
    active: bool,
    username: String,
    email: String,
    sign_in_count: u64,
}

fn main() {
    let user1 = User {
        active: true,
        username: String::from("someusername123"),
        email: String::from("someone@example.com"),
        sign_in_count: 1,
    };
    println!("email: {}", user1.email);
}
```

</Listing>

与 Rust 的关键区别：

| 特性 | Auto | Rust |
|------|------|------|
| 定义结构体 | `type Name { }` | `struct Name { }` |
| 字段类型语法 | `name Type` | `name: Type` |
| 创建实例 | `Name(val1, val2)` | `Name { field: val }` |
| 可变实例 | `var user = Name(...)` | `let mut user = Name { ... }` |

Auto 使用位置构造函数语法（`User(true, "name", ...)`）而非 Rust 的命名字段语法（`User { active: true, ... }`）。参数按照字段声明的顺序进行匹配。

### 可变实例

要修改字段，使用 `var` 创建可变实例：

<Listing number="5-2" file-name="main.auto" caption="修改可变 `User` 实例中 `email` 字段的值">

```auto
type User {
    active bool
    username String
    email String
    sign_in_count int
}

fn main() {
    var user1 = User(true, "someusername123", "someone@example.com", 1)
    user1.email = "another@example.com"
    print(f"email: ${user1.email}")
}
```

```rust
struct User {
    active: bool,
    username: String,
    email: String,
    sign_in_count: u64,
}

fn main() {
    let mut user1 = User {
        active: true,
        username: String::from("someusername123"),
        email: String::from("someone@example.com"),
        sign_in_count: 1,
    };
    user1.email = String::from("another@example.com");
    println!("email: {}", user1.email);
}
```

</Listing>

注意，整个实例必须是可变的；Auto 不允许只将某些字段标记为可变，这与 Rust 一致。

## 一个使用结构体的示例程序

让我们编写一个计算矩形面积的程序，从简单变量开始，逐步重构为使用结构体。

### 使用独立变量

<Listing number="5-3" file-name="main.auto" caption="使用独立的 width 和 height 变量计算矩形面积">

```auto
fn area(width int, height int) int {
    width * height
}

fn main() {
    let width1 = 30
    let height1 = 50
    print(f"The area of the rectangle is ${area(width1, height1)} square pixels.")
}
```

```rust
fn area(width: u32, height: u32) -> u32 {
    width * height
}

fn main() {
    let width1 = 30;
    let height1 = 50;
    println!(
        "The area of the rectangle is {} square pixels.",
        area(width1, height1)
    );
}
```

</Listing>

这段代码的问题在于 `width` 和 `height` 是相关的，但函数签名并没有传达这种关系。让我们用类型来重构。

### 使用类型重构

<Listing number="5-4" file-name="main.auto" caption="定义 `Rectangle` 类型并计算其面积">

```auto
type Rectangle {
    width int
    height int
}

fn area(rect Rectangle) int {
    rect.width * rect.height
}

fn main() {
    let rect1 = Rectangle(30, 50)
    print(f"The area of the rectangle is ${area(rect1)} square pixels.")
}
```

```rust
struct Rectangle {
    width: u32,
    height: u32,
}

fn area(rect: &Rectangle) -> u32 {
    rect.width * rect.height
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };
    println!(
        "The area of the rectangle is {} square pixels.",
        area(&rect1)
    );
}
```

</Listing>

现在函数签名清楚地表明它计算的是一个 `Rectangle` 的面积，且 `width` 和 `height` 字段有了名称并被关联起来。

### 使用 `.view` 借用

如第 4 章所述，我们可以使用 `.view` 来借用值而不获取所有权：

<Listing number="5-5" file-name="main.auto" caption="使用 `.view` 借用 Rectangle">

```auto
type Rectangle {
    width int
    height int
}

fn area(rect Rectangle) int {
    rect.width * rect.height
}

fn main() {
    let rect1 = Rectangle(30, 50)
    print(f"The area of the rectangle is ${area(rect1.view)} square pixels.")
}
```

```rust
struct Rectangle {
    width: u32,
    height: u32,
}

fn area(rect: &Rectangle) -> u32 {
    rect.width * rect.height
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };
    println!(
        "The area of the rectangle is {} square pixels.",
        area(&rect1)
    );
}
```

</Listing>

## 方法

方法是在类型的上下文中定义的函数。在 Auto 中，方法可以通过两种方式定义：

1. **内联方法** — 直接在 `type { }` 块内定义
2. **扩展方法** — 在类型定义外部的 `ext` 块中定义

两种方式都会生成 Rust 的 `impl` 块。

### 定义内联方法

在 Auto 中，你可以直接在 `type` 块内定义方法。`self` 参数是隐式的 — 在方法体内，使用 `.field` 来访问实例的字段：

<Listing number="5-6" file-name="main.auto" caption="在 `Rectangle` 类型上定义 `area` 方法">

```auto
type Rectangle {
    width int
    height int

    fn area() int {
        .width * .height
    }
}

fn main() {
    let rect1 = Rectangle(30, 50)
    print(f"The area of the rectangle is ${rect1.area()} square pixels.")
}
```

```rust
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

fn main() {
    let rect1 = Rectangle {
        width: 30,
        height: 50,
    };
    println!(
        "The area of the rectangle is {} square pixels.",
        rect1.area()
    );
}
```

</Listing>

关键区别：

| 特性 | Auto | Rust |
|------|------|------|
| 定义方法 | 在 `type { }` 块内 | 在单独的 `impl` 块中 |
| self 参数 | 隐式（不需要写） | 显式 `&self` |
| 访问自身字段 | `.field` | `self.field` |

`.field` 语法是 `self.field` 的简写。Auto 自动注入 `&self` 作为第一个参数，并在转译的 Rust 代码中将 `.field` 转换为 `self.field`。

### 带多个参数的方法

你可以在隐式的 `self` 之后为方法添加额外参数：

<Listing number="5-7" file-name="main.auto" caption="具有多个方法的 `Rectangle` 类型">

```auto
type Rectangle {
    width int
    height int

    fn area() int {
        .width * .height
    }

    fn is_square() bool {
        .width == .height
    }
}

fn main() {
    let rect1 = Rectangle(30, 50)
    let rect2 = Rectangle(40, 40)

    print(f"rect1 area: ${rect1.area()}")
    print(f"rect1 is square: ${rect1.is_square()}")
    print(f"rect2 is square: ${rect2.is_square()}")
}
```

```rust
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }

    fn is_square(&self) -> bool {
        self.width == self.height
    }
}

fn main() {
    let rect1 = Rectangle { width: 30, height: 50 };
    let rect2 = Rectangle { width: 40, height: 40 };

    println!("rect1 area: {}", rect1.area());
    println!("rect1 is square: {}", rect1.is_square());
    println!("rect2 is square: {}", rect2.is_square());
}
```

</Listing>

### 使用 `ext` 定义关联函数

在 Rust 中，关联函数（如 `String::from`）是在 `impl` 块中定义的不以 `self` 作为第一个参数的函数。在 Auto 中，你使用 `ext` 关键字在类型初始定义之后添加关联函数和方法：

<Listing number="5-8" file-name="main.auto" caption="使用 `ext` 添加关联函数">

```auto
type Rectangle {
    width int
    height int

    fn area() int {
        .width * .height
    }
}

ext Rectangle {
    fn square(size int) Rectangle {
        Rectangle(size, size)
    }
}

fn main() {
    let sq = Rectangle.square(3)
    print(f"Square area: ${sq.area()}")
}
```

```rust
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

impl Rectangle {
    fn square(size: u32) -> Rectangle {
        Rectangle { width: size, height: size }
    }
}

fn main() {
    let sq = Rectangle::square(3);
    println!("Square area: {}", sq.area());
}
```

</Listing>

关联函数的关键映射区别：

| 特性 | Auto | Rust |
|------|------|------|
| 定义扩展 | `ext TypeName { }` | `impl TypeName { }` |
| 调用关联函数 | `TypeName.method()` | `TypeName::method()` |
| 构造函数调用 | `TypeName(args)` | `TypeName { field: val }` |

`ext` 关键字是 Auto 中等价于 Rust `impl` 的机制，用于向类型添加方法和关联函数。与 `impl` 不同，`ext` 可以在代码库的任何位置使用，不仅限于类型定义之后。

### 多个 `ext` 块

每个类型可以有多个 `ext` 块。这对于按功能组织方法非常有用：

<Listing number="5-9" file-name="main.auto" caption="使用多个 `ext` 块">

```auto
type Rectangle {
    width int
    height int

    fn area() int {
        .width * .height
    }
}

ext Rectangle {
    fn double_width() int {
        .width * 2
    }
}

fn main() {
    let rect1 = Rectangle(30, 50)
    print(f"Area: ${rect1.area()}")
    print(f"Double width: ${rect1.double_width()}")
}
```

```rust
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

impl Rectangle {
    fn double_width(&self) -> u32 {
        self.width * 2
    }
}

fn main() {
    let rect1 = Rectangle { width: 30, height: 50 };
    println!("Area: {}", rect1.area());
    println!("Double width: {}", rect1.double_width());
}
```

</Listing>

## 类元组类型

Auto 没有 Rust 的"元组结构体"（即未命名字段的结构体）。取而代之，使用带有命名字段的常规类型，这样可以提供更好的可读性：

<Listing number="5-10" file-name="main.auto" caption="用命名类型替代元组结构体">

```auto
type Color {
    red int
    green int
    blue int
}

type Point {
    x int
    y int
    z int
}

fn main() {
    let black = Color(0, 0, 0)
    let origin = Point(0, 0, 0)
    print(f"black: ${black.red}, ${black.green}, ${black.blue}")
    print(f"origin: ${origin.x}, ${origin.y}, ${origin.z}")
}
```

```rust
struct Color {
    red: i32,
    green: i32,
    blue: i32,
}

struct Point {
    x: i32,
    y: i32,
    z: i32,
}

fn main() {
    let black = Color { red: 0, green: 0, blue: 0 };
    let origin = Point { x: 0, y: 0, z: 0 };
    println!("black: {}, {}, {}", black.red, black.green, black.blue);
    println!("origin: {}, {}, {}", origin.x, origin.y, origin.z);
}
```

</Listing>

> ### 类型数据的所有权
>
> 在 Auto 中，与 Rust 一样，类型可以拥有其数据（使用 `String`）或借用数据（使用 `.view`）。当类型拥有其数据时，只要整个类型实例有效，数据就是有效的。Auto 的编译器会自动处理生命周期检查，无需显式标注。

## 总结

Auto 的 `type` 关键字提供了与 Rust 的 `struct` 相同的功能，但语法更加简洁：

| 概念 | Auto | Rust |
|------|------|------|
| 定义类型 | `type Name { fields }` | `struct Name { fields }` |
| 字段语法 | `name Type` | `name: Type` |
| 创建实例 | `Name(val1, val2)` | `Name { field: val }` |
| 可变实例 | `var x = Name(...)` | `let mut x = Name { ... }` |
| 内联方法 | 在 `type { }` 块内 | 在 `impl` 块中 |
| 扩展方法 | `ext Name { }` | `impl Name { }` |
| 访问自身字段 | `.field` | `self.field` |
| 关联函数 | `ext Name { fn new() }` | `impl Name { fn new() }` |
| 调用关联函数 | `Name.fn()` | `Name::fn()` |

类型和枚举（将在第 6 章讨论）是构建程序领域中新类型的基石，让你能够充分利用 Auto 的编译时类型检查。

接下来让我们进入第 6 章，了解枚举和 `is` 关键字的模式匹配。
