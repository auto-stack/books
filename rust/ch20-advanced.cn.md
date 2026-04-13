# 高级特性

到目前为止，你已经学习了 Auto 编程语言中最常用的部分。在第 21 章做最后一个项目之前，我们将看看语言的几个方面，这些你可能偶尔会遇到，但可能不会每天都使用。你可以将本章作为参考，以便在遇到任何未知内容时查阅。这里介绍的特性在非常特定的情况下很有用。虽然你可能不经常用到它们，但我们想确保你掌握 Auto 提供的所有特性。

在本章中，我们将涵盖：

- **`sys` 块**：Auto 中等同于 Rust unsafe 的机制，用于当你需要绕过语言的安全保证时
- **高级类型**：类型别名、never 类型和动态大小类型
- **编译期元编程**：Auto 使用 `#[]` 进行编译期代码生成，替代 Rust 的宏系统

## `sys` 块

我们目前讨论过的所有代码都通过 AutoFree 在编译时强制执行 Auto 的内存安全保证。然而，Auto 内部隐藏着第二种语言，它不强制执行这些内存安全保证：它被称为_系统模式_（sys mode），工作方式类似普通 Auto，但赋予你额外的能力。它使用 `sys` 关键字而不是 Rust 的 `unsafe`。

系统模式的存在是因为静态分析本质上是保守的。当编译器试图确定代码是否遵守保证时，拒绝一些有效的程序比接受一些无效的程序更好。在这些情况下，你可以使用 `sys` 代码告诉编译器，"相信我，我知道我在做什么。"

Auto 拥有系统模式的另一个原因是底层计算机硬件本质上是不安全的。如果 Auto 不允许你进行不安全操作，你就无法完成某些任务。Auto 需要允许你进行底层系统编程，例如直接与操作系统交互甚至编写你自己的操作系统。

### 系统超能力

要切换到系统模式，使用 `sys` 关键字，然后启动一个包含系统级代码的新块。你可以在系统模式下执行以下在安全 Auto 中不能做的操作，我们称之为_系统超能力_：

1. 解引用原始指针（`*T`）
2. 调用 `sys` 函数或方法
3. 访问或修改可变静态变量
4. 实现 `sys` 规范
5. 访问联合体的字段
6. 通过 FFI 调用 C 函数

重要的是要理解，`sys` 并不会关闭 AutoFree 或禁用 Auto 的任何其他安全检查。`sys` 关键字只让你访问那些编译器不检查内存安全的特性。

此外，`sys` 并不意味着块内的代码一定是危险的。其意图是作为程序员，你要确保 `sys` 块内的代码以有效的方式访问内存。

为了尽可能隔离系统代码，最好将此类代码封装在安全的抽象中并提供安全的 API。

### 解引用原始指针

系统模式有两种类似于引用的原始指针类型：`*T`（不可变原始指针）和 `*mut T`（可变原始指针）。它们对应于 Rust 的 `*const T` 和 `*mut T`。

<Listing number="20-1" file-name="src/main.at" caption="创建和解引用原始指针">

```auto
fn main() {
    var num = 5

    let r1 = &raw num        // *int（不可变原始指针）
    let r2 = &raw mut num    // *mut int（可变原始指针）

    sys {
        print(f"r1 is: {*r1}")
        print(f"r2 is: {*r2}")
    }
}
```

```rust
fn main() {
    let mut num = 5;

    let r1 = &raw const num;
    let r2 = &raw mut num;

    unsafe {
        println!("r1 is: {}", *r1);
        println!("r2 is: {}", *r2);
    }
}
```

</Listing>

请注意，我们可以在安全代码中创建原始指针；只是不能在 `sys` 块之外解引用原始指针。创建指针没有什么危害；只有当我们尝试访问它指向的值时，才可能遇到无效值。

与常规引用不同，原始指针：

- 允许忽略借用规则，可以同时拥有同一位置的不可变和可变指针
- 不保证指向有效内存
- 允许为 null
- 不实现任何自动清理

### 调用系统函数

你可以在 `sys` 块中执行的第二种操作是调用系统函数。系统函数在定义的其余部分之前有一个额外的 `sys`：

<Listing number="20-2" file-name="src/main.at" caption="调用系统函数">

```auto
sys fn dangerous() {}

fn main() {
    sys {
        dangerous()
    }
}
```

```rust
unsafe fn dangerous() {}

fn main() {
    unsafe {
        dangerous();
    }
}
```

</Listing>

我们必须在 `sys` 块内调用 `dangerous` 函数。如果我们尝试在没有 `sys` 块的情况下调用它，我们会得到一个错误。

#### 在系统代码上创建安全抽象

仅仅因为函数包含系统代码并不意味着我们需要将整个函数标记为 `sys`。实际上，将系统代码包装在安全函数中是一种常见的抽象。例如，让我们实现 `split_at_mut`：

<Listing number="20-3" file-name="src/main.at" caption="内部使用 sys 的安全抽象">

```auto
fn split_at_mut(values &mut [int], mid int) (&mut [int], &mut [int]) {
    let len = values.len()
    assert(mid <= len)

    let ptr = values.as_mut_ptr()

    sys {
        (
            slice.from_raw_parts_mut(ptr, mid),
            slice.from_raw_parts_mut(ptr.add(mid), len - mid),
        )
    }
}

fn main() {
    var v = [1, 2, 3, 4, 5, 6]
    let (a, b) = split_at_mut(&mut v, 3)
    assert_eq(a, &mut [1, 2, 3])
    assert_eq(b, &mut [4, 5, 6])
}
```

```rust
use std::slice;

fn split_at_mut(values: &mut [i32], mid: usize) -> (&mut [i32], &mut [i32]) {
    let len = values.len();
    let ptr = values.as_mut_ptr();

    assert!(mid <= len);

    unsafe {
        (
            slice::from_raw_parts_mut(ptr, mid),
            slice::from_raw_parts_mut(ptr.add(mid), len - mid),
        )
    }
}

fn main() {
    let mut vector = vec![1, 2, 3, 4, 5, 6];
    let (left, right) = split_at_mut(&mut vector, 3);
    assert_eq!(left, &mut [1, 2, 3]);
    assert_eq!(right, &mut [4, 5, 6]);
}
```

</Listing>

请注意，我们不需要将 `split_at_mut` 标记为 `sys`，我们可以从安全的 Auto 中调用此函数。我们创建了一个安全抽象，其实现以安全的方式使用了 `sys` 代码。

### 外部函数接口（FFI）

有时你的 Auto 代码可能需要与用另一种语言编写的代码交互。由于 Auto 转译为 C，它具有天然的 FFI 支持：

<Listing number="20-4" file-name="src/main.at" caption="声明和调用 extern C 函数">

```auto
sys extern "C" {
    fn abs(input int) int
}

fn main() {
    sys {
        print(f"Absolute value of -3 according to C: {abs(-3)}")
    }
}
```

```rust
unsafe extern "C" {
    fn abs(input: i32) -> i32;
}

fn main() {
    unsafe {
        println!("Absolute value of -3 according to C: {}", abs(-3));
    }
}
```

</Listing>

在 `sys extern "C"` 块内，我们列出来自 C 的外部函数的名称和签名。`"C"` 部分定义了外部函数使用的应用程序二进制接口（ABI）。

由于 Auto 转译为 C，与 C 库的 FFI 非常直接。调用 C 函数不需要额外的桥接代码或包装器生成。

### 访问或修改可变静态变量

Auto 中的全局变量被称为_静态_变量。访问和修改可变静态变量需要 `sys`：

<Listing number="20-5" file-name="src/main.at" caption="读取或写入可变静态变量">

```auto
static mut COUNTER int = 0

/// SAFETY: 在多个线程同时调用此函数是未定义行为。
sys fn add_to_count(inc int) {
    sys {
        COUNTER += inc
    }
}

fn main() {
    sys {
        add_to_count(3)
        print(f"COUNTER: {COUNTER}")
    }
}
```

```rust
static mut COUNTER: u32 = 0;

/// SAFETY: Calling this from more than a single thread at a time is
/// undefined behavior.
unsafe fn add_to_count(inc: u32) {
    unsafe {
        COUNTER += inc;
    }
}

fn main() {
    unsafe {
        add_to_count(3);
        println!("COUNTER: {}", *(&raw const COUNTER));
    }
}
```

</Listing>

对于全局可访问的可变数据，很难确保没有数据竞争，这就是为什么 Auto 认为可变静态变量需要 `sys`。在可能的情况下，最好使用我们在第 16 章（Actor）中讨论的并发技术，这样编译器可以检查数据访问是否安全完成。

### 实现系统规范

我们可以使用 `sys` 来实现系统规范。当一个规范的方法中至少有一个具有编译器无法验证的不变量时，该规范就是系统级的：

<Listing number="20-6" file-name="src/main.at" caption="定义和实现系统规范">

```auto
sys spec Foo {
    // 方法放在这里
}

sys spec Foo for int {
    // 方法实现放在这里
}

fn main() {}
```

```rust
unsafe trait Foo {
    // methods go here
}

unsafe impl Foo for i32 {
    // method implementations go here
}

fn main() {}
```

</Listing>

通过使用 `sys spec ... for Type`，我们承诺将遵守编译器无法验证的不变量。

### `sys` vs `unsafe` 速查表

| 特性 | Auto（`sys`） | Rust（`unsafe`） |
|------|-------------|-----------------|
| 关键字 | `sys` | `unsafe` |
| 原始指针类型 | `*T`、`*mut T` | `*const T`、`*mut T` |
| 系统/不安全函数 | `sys fn` | `unsafe fn` |
| 系统/不安全 trait | `sys spec` | `unsafe trait` |
| FFI 块 | `sys extern "C"` | `unsafe extern "C"` |
| 静态变量 | `static mut` 在 `sys` 中 | `static mut` 在 `unsafe` 中 |
| 安全抽象 | 鼓励使用 | 鼓励使用 |
| 转译为 | C 代码 | 原生代码 |

## 高级类型

### 类型别名

Auto 提供声明_类型别名_的能力，为现有类型提供另一个名称，就像 Rust 一样。例如，我们可以为 `int` 创建别名 `Kilometers`：

<Listing number="20-7" file-name="src/main.at" caption="创建类型别名">

```auto
type Kilometers = int

fn main() {
    let x int = 5
    let y Kilometers = 5

    print(f"x + y = {x + y}")
}
```

```rust
type Kilometers = i32;

fn main() {
    let x: i32 = 5;
    let y: Kilometers = 5;

    println!("x + y = {}", x + y);
}
```

</Listing>

别名 `Kilometers` 是 `int` 的同义词；与新类型模式不同，`Kilometers` 不是一个独立的新类型。类型为 `Kilometers` 的值将被视为与类型为 `int` 的值相同。

类型别名的主要用例是减少重复。例如，像 `Box<dyn Fn() + Send>` 这样冗长的类型可以被别名化：

```auto
type Thunk = Box<dyn Fn() + Send>

fn takes_long_type(f Thunk) {
    // ...
}

fn returns_long_type() Thunk {
    // ...
}
```

### Never 类型

Auto 有一个特殊类型命名为 `!`，被称为 _never 类型_，因为当一个函数永远不会返回时，它作为返回类型的占位符。这与 Rust 的 never 类型概念相同：

```auto
fn bar() ! {
    panic("something went wrong")
}
```

```rust
fn bar() -> ! {
    panic!("something went wrong");
}
```

请注意，Auto 使用 `!` 既作为 `!T` 中的错误类型（等同于 `Result<T, E>`），也作为 never 类型。编译器根据上下文区分它们：`!T` 是一个错误传播结果类型，而独立使用的 `!` 作为返回类型意味着函数永远不会返回。

never 类型在与 `panic()`、`return`、`break` 和 `continue` 一起使用时很有用——所有这些都产生类型为 `!` 的值，可以强制转换为任何其他类型。

### 动态大小类型

Auto 有_动态大小类型_（DST），类似于 Rust。最常见的 DST 是 `str`（不是 `String`）。我们不能直接创建类型为 `str` 的变量，因为编译器不知道要分配多少空间。相反，我们总是在指针后面使用 DST：`&str`、`Box<str>` 等。

规范对象（`dyn Spec`）也是 DST，这就是为什么它们必须放在像 `Box<dyn Draw>` 或 `&dyn Draw` 这样的指针后面。

## 编译期元编程

Rust 使用宏（`macro_rules!` 和过程宏）进行元编程——编写生成代码的代码。Auto 用_编译期_（comptime）替代了整个系统：在编译时运行的代码。这受到了 Zig 的 comptime 的启发，比 Rust 的宏系统更强大且更容易理解。

### 为什么用编译期而不是宏？

Rust 中的宏有几个缺点：

- `macro_rules!` 使用与普通 Rust 代码不同的复杂模式匹配语法
- 过程宏需要独立的 crate 和像 `syn`、`quote` 这样的依赖
- 宏错误通常很难阅读
- 宏不容易内省类型

Auto 的编译期系统解决了这些问题：

- 编译期代码使用常规 Auto 语法——没有特殊的宏语言
- 不需要独立的 crate
- 错误信息清晰，因为它们来自正常的 Auto 代码
- 编译期有完整的类型内省能力

### `#[]` 属性系统

Auto 使用 `#[]` 属性进行编译期代码生成。它们的作用与 Rust 的 `#[derive]`、`#[proc_macro]` 和其他属性相同：

<Listing number="20-8" file-name="src/main.at" caption="使用内置的 derive 属性">

```auto
#derive[Debug, Eq]
type Point {
    x int
    y int
}

fn main() {
    let p = Point(x: 1, y: 2)
    print(f"{p:?}")  // 使用 Debug 实现
}
```

```rust
#[derive(Debug, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 1, y: 2 };
    println!("{:?}", p);
}
```

</Listing>

`#derive[...]` 属性自动为你的类型生成规范实现。这等同于 Rust 的 `#[derive(...)]`。

### 编写自定义编译期函数

Auto 允许你编写编译期函数——在编译时执行并生成代码的常规 Auto 函数。这同时替代了声明式宏和过程宏：

<Listing number="20-9" file-name="src/main.at" caption="生成代码的编译期函数">

```auto
comptime fn generate_hello(type_name String) String {
    f"""
ext {type_name} {{
    fn hello() {{
        print("Hello from {type_name}!")
    }}
}}
"""
}

// 应用编译期函数来生成代码
#apply[generate_hello]
type Greeter {}

fn main() {
    Greeter.hello()  // 由编译期生成
}
```

```rust
use proc_macro::TokenStream;
use quote::quote;

#[proc_macro_derive(Hello)]
pub fn hello_derive(input: TokenStream) -> TokenStream {
    let ast = syn::parse(input).unwrap();
    let name = &ast.ident;
    let generated = quote! {
        impl Hello for #name {
            fn hello() {
                println!("Hello from {}!", stringify!(#name));
            }
        }
    };
    generated.into()
}

// In another crate:
// #[derive(Hello)]
// struct Greeter;
```

</Listing>

在 Rust 中，过程宏需要独立的 crate、`syn` 和 `quote` crate，以及复杂的 token 操作。在 Auto 中，编译期函数只是用 `comptime` 标记的常规函数，它返回代码字符串或直接操作 AST。

### 编译期 vs Rust 宏

<Listing number="20-10" file-name="src/main.at" caption="编译期列表创建 vs vec! 宏">

```auto
// Auto 不需要 vec! 宏——列表字面量直接工作
fn main() {
    let v = [1, 2, 3]  // List<int>
    print(f"{v}")
}
```

```rust
fn main() {
    let v = vec![1, 2, 3];  // 使用 vec! 宏
    println!("{:?}", v);
}
```

</Listing>

许多在 Rust 中需要宏的模式在 Auto 中不需要编译期：

| Rust 模式 | 需要宏吗？ | Auto 等价物 |
|-----------|----------|------------|
| 向量字面量 | 是（`vec![]`） | 否（`[1, 2, 3]`） |
| 格式化打印 | 是（`println!`） | 否（`print(f"{}")`） |
| 派生 trait | 是（`#[derive]`） | 是（`#derive[]`） |
| 自定义代码生成 | 是（过程宏） | 是（编译期） |
| 条件编译 | 是（`cfg!`） | 是（`#if[]`） |

### 属性式编译期

Auto 支持在编译时转换代码的自定义属性：

<Listing number="20-11" file-name="src/main.at" caption="自定义属性式编译期">

```auto
// 为路由处理器定义自定义属性
#attr[route]
comptime fn route_handler(attr String, item String) String {
    // 从 attr 解析路由，将函数包装
    // 为路由注册代码
    f"""
// Register route: {attr}
{item}
routes.register("{attr}", handler)
"""
}

// 使用属性
#route[GET, "/"]
fn index() {
    "Hello, World!"
}
```

```rust
use proc_macro::TokenStream;

#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
    // Parse attr and item, generate routing code
    // Requires syn and quote crates
    item
}
```

</Listing>

### 条件编译

Auto 使用 `#if[]` 提供编译期条件编译：

<Listing number="20-12" file-name="src/main.at" caption="条件编译">

```auto
#if[debug]
fn log(msg String) {
    print(f"[DEBUG] {msg}")
}

#if[release]
fn log(msg String) {
    // 发布版本中不做任何事
}

fn main() {
    log("Starting application")
}
```

```rust
#[cfg(debug_assertions)]
fn log(msg: &str) {
    println!("[DEBUG] {msg}");
}

#[cfg(not(debug_assertions))]
fn log(msg: &str) {
    // No-op in release builds
}

fn main() {
    log("Starting application");
}
```

</Listing>

### 内联编译期表达式

Auto 允许内联编译期表达式——在编译时运行并产生值的代码：

<Listing number="20-13" file-name="src/main.at" caption="内联编译期表达式">

```auto
fn main() {
    // 在编译期计算常量
    const MAX_SIZE = comptime {
        let base = 1024
        let scale = 4
        base * scale
    }

    // 在编译期生成类型信息
    comptime {
        for field in config.fields {
            print(f"Field: {field.name}")
        }
    }

    print(f"Max size: {MAX_SIZE}")
}
```

```rust
const MAX_SIZE: usize = 1024 * 4;

fn main() {
    println!("Max size: {MAX_SIZE}");
}
```

</Listing>

### 编译期 vs Rust 宏速查表

| 特性 | Rust | Auto |
|------|------|------|
| 声明式宏 | `macro_rules!` | 不需要（使用编译期） |
| 过程宏 | 独立 crate + `syn`/`quote` | `comptime fn` |
| 派生宏 | `#[derive(Trait)]` | `#derive[Trait]` |
| 属性宏 | `#[proc_macro_attribute]` | `#attr[...]` + `comptime fn` |
| 函数式宏 | `#[proc_macro]` | `comptime fn` |
| 条件编译 | `#[cfg(...)]` | `#if[...]` |
| 类型内省 | 不可用 | 完整的编译期反射 |
| 需要独立 crate | 是（过程宏） | 否 |
| 语法 | 特殊宏语法 | 常规 Auto 语法 |

## `sys` 和编译期使用指南

### 何时使用 `sys`

在以下情况使用 `sys` 块：

- 通过 FFI 与 C 库交互
- 实现底层数据结构（如 `List<T>` 的内部实现）
- 进行指针算术
- 直接访问硬件

始终将 `sys` 代码包装在安全抽象中。保持 `sys` 块尽可能小。使用 `/// SAFETY:` 注释记录安全不变量。

### 何时使用编译期

在以下情况使用编译期：

- 生成重复代码（如规范实现）
- 在 Auto 内实现领域特定语言
- 执行编译期验证
- 减少样板代码

在可能的情况下，优先使用常规函数和泛型而不是编译期。编译期增加了复杂性；仅在替代方案更差时使用。

## 总结

本章涵盖了 Auto 的高级特性：

1. **`sys` 块** — Auto 中等同于 `unsafe` 的机制，用于在必要时绕过安全保证。使用 `sys` 关键字替代 `unsafe`，使用 `*T`/`*mut T` 替代 `*const T`/`*mut T`，使用 `sys spec` 替代 `unsafe trait`。

2. **高级类型** — 类型别名用于减少重复，never 类型 `!` 用于不返回的函数，动态大小类型必须放在指针后面使用。

3. **编译期元编程** — Auto 替代 Rust 宏系统的机制。使用 `#[]` 属性和 `comptime fn` 替代 `macro_rules!` 和过程宏。不需要独立的 crate，全部使用熟悉的函数语法。

与 Rust 的关键区别在于，Auto 用统一的编译期系统替代了复杂的宏生态系统。Rust 有三种宏，每种都有自己的语法和 crate 要求，而 Auto 有一个单一的 `comptime` 机制，使用熟悉的函数语法。而 Rust 使用 `unsafe`，Auto 使用 `sys`——一个更简单的关键字，表达退出安全保证的相同概念。

在下一章，我们将把整本书讨论的所有内容付诸实践，构建一个最终项目：一个使用 Auto Actor 模型的 Web 服务器。
