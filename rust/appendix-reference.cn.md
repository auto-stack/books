# 附录

以下各节包含你在 Auto 学习旅程中可能觉得有用的参考材料，并在适用的地方提供了与 Rust 等价物的比较。

## 附录 A：关键字

以下列表包含 Auto 语言保留的关键字。因此，它们不能用作标识符。_标识符_是函数、变量、参数、类型字段、模块、包、常量、静态值、属性、类型或规范的名称。

### 当前使用的关键字

以下是 Auto 中当前使用的所有关键字列表，描述了它们的功能并注明了等效的 Rust 关键字。

| Auto 关键字 | Rust 等价物 | 描述 |
|------------|-----------|------|
| `actor` | _(无)_ | 定义一个 actor 类型 |
| `as` | `as` | 类型转换 |
| `break` | `break` | 立即退出循环 |
| `comptime` | _(无)_ | 标记函数在编译时执行 |
| `const` | `const` | 定义常量 |
| `continue` | `continue` | 继续下一次循环迭代 |
| `dyn` | `dyn` | 对规范对象的动态派发 |
| `else` | `else` | `if` 和 `if let` 控制流的回退分支 |
| `enum` | `enum` | 定义枚举 |
| `ext` | `impl` | 为类型附加方法 |
| `extern` | `extern` | 链接外部函数或变量 |
| `false` | `false` | 布尔假字面量 |
| `fn` | `fn` | 定义函数 |
| `for` | `for` | 遍历迭代器中的项 |
| `has` | _(无)_ | 通过组合委托行为 |
| `if` | `if` | 基于条件表达式的分支 |
| `in` | `in` | `for` 循环语法的一部分 |
| `is` | `match` | 将值与模式匹配；组合类型 |
| `let` | `let` | 绑定变量 |
| `loop` | `loop` | 无条件循环 |
| `mod` | `mod` | 定义模块 |
| `mut` | `mut` | _(Rust)_ 表示可变性 |
| `on` | _(无)_ | 处理 actor 消息；订阅蓝图 |
| `pub` | `pub` | 表示公共可见性 |
| `return` | `return` | 从函数返回 |
| `Self` | `Self` | 正在定义或实现的类型的别名 |
| `self` | `self` | 方法主体 |
| `spec` | `trait` | 定义规范（共享行为接口） |
| `static` | `static` | 全局变量 |
| `sys` | `unsafe` | 表示系统级（不安全）代码 |
| `tell` | _(无)_ | 向 actor 发送消息 |
| `true` | `true` | 布尔真字面量 |
| `type` | `struct` / `type` | 定义数据类型或类型别名 |
| `use` | `use` | 将符号引入作用域 |
| `var` | `let mut` | 声明可变变量 |
| `where` | `where` | 用规范约束限制类型 |
| `while` | `while` | 条件循环 |
| `yield` | _(无)_ | 在蓝图中将控制权交还运行时 |

### Auto 独有关键字

这些关键字存在于 Auto 中，但没有直接的 Rust 等价物：

| 关键字 | 描述 |
|-------|------|
| `actor` | 定义并发处理消息的 actor 类型 |
| `comptime` | 标记在编译时执行的函数 |
| `ext` | 为类型附加方法（替代 Rust 的 `impl`） |
| `has` | 将方法调用委托给包含的类型 |
| `is` | 模式匹配（替代 `match`）和类型组合 |
| `on` | Actor 中的消息处理器；蓝图订阅 |
| `spec` | 定义行为规范（替代 Rust 的 `trait`） |
| `sys` | 系统级代码（替代 Rust 的 `unsafe`） |
| `tell` | 向 actor 发送消息 |
| `var` | 可变变量声明的简写 |

### Rust 中有但 Auto 中没有的关键字

这些 Rust 关键字在 Auto 中不存在，因为 Auto 以不同方式处理它们的用例：

| Rust 关键字 | Auto 等价物 | 原因 |
|-----------|-----------|------|
| `async` | `~T` 返回类型 | 蓝图通过类型而非关键字指示 |
| `await` | `on` 块 | 订阅蓝图而非等待 |
| `crate` | _(包根)_ | Auto 使用基于包的模块解析 |
| `impl` | `ext` | 不同关键字，相同概念 |
| `match` | `is` | 不同关键字，相同模式语法 |
| `move` | _(隐式)_ | Auto 使用隐式移动语义 |
| `mut` | `var` | 可变绑定的简写 |
| `ref` | _(不需要)_ | AutoFree 处理引用语义 |
| `struct` | `type` | 统一的类型声明关键字 |
| `super` | _(父引用)_ | Auto 使用带父路径的 `use` |
| `trait` | `spec` | 为 Auto 语义重命名 |
| `union` | `union` | 仅在联合体声明中是关键字 |

### 为未来使用保留的关键字

以下关键字目前没有任何功能，但被 Auto 保留以备将来可能使用：

- `abstract`
- `become`
- `do`
- `final`
- `macro`
- `override`
- `priv`
- `try`
- `typeof`
- `virtual`

## 附录 B：运算符和符号

### 运算符

表 B-1 包含 Auto 中的运算符，并与 Rust 进行比较。大多数运算符在两种语言中是相同的。

| 运算符 | 示例 | 描述 | Auto 与 Rust 差异 |
|-------|------|------|------------------|
| `!` | `!expr` | 逻辑取反 | 相同 |
| `!=` | `expr != expr` | 不等于 | 相同 |
| `%` | `expr % expr` | 取余 | 相同 |
| `%=` | `var %= expr` | 取余赋值 | 相同 |
| `&` | `&expr` | 借用/引用 | 相同 |
| `&` | `expr & expr` | 按位与 | 相同 |
| `&&` | `expr && expr` | 逻辑与 | 相同 |
| `*` | `expr * expr` | 乘法 | 相同 |
| `*` | `*expr` | 解引用 | 相同 |
| `+` | `expr + expr` | 加法 | 相同 |
| `+=` | `var += expr` | 加法赋值 | 相同 |
| `-` | `-expr` | 取负 | 相同 |
| `-` | `expr - expr` | 减法 | 相同 |
| `-=` | `var -= expr` | 减法赋值 | 相同 |
| `->` | `fn() -> type` | 函数返回类型 | 相同语法，也用于 `is` 分支 |
| `.` | `expr.ident` | 字段访问 | 相同 |
| `..` | `..`, `expr..`, `..expr` | 范围 | 相同 |
| `..=` | `expr..=expr` | 包含范围 | 相同 |
| `..` | `Type(x, ..)` | 忽略剩余字段 | 相同概念，Auto 用 `()` 不用 `{}` |
| `/` | `expr / expr` | 除法 | 相同 |
| `/=` | `var /= expr` | 除法赋值 | 相同 |
| `:` | `ident: type` | 类型注解 | Auto 字段用空格：`name Type` |
| `==` | `expr == expr` | 等于 | 相同 |
| `=>` | `pat => expr` | 匹配分支 | 仅 Rust；Auto 用 `->` |
| `@` | `ident @ pat` | 模式绑定 | 相同 |
| `^` | `expr ^ expr` | 按位异或 | 相同 |
| `\|` | `pat \| pat` | 模式选择 | 相同 |
| `\|\|` | `expr \|\| expr` | 逻辑或 | 相同 |
| `?` | `expr?` | 错误传播 | Rust: `expr?` 后缀；Auto: `expr!` 后缀 |
| `~` | `~expr`, `~T` | 蓝图运算符 | 仅 Auto：创建/转换蓝图 |

### Auto 特有运算符

| 运算符 | 示例 | 描述 |
|-------|------|------|
| `~` | `~5`, `~T` | 蓝图创建/类型操作符 |
| `~race` | `~race(a, b)` | 第一个完成的蓝图获胜 |
| `~join` | `~join(a, b)` | 等待所有蓝图完成 |
| `~spawn` | `~spawn(() => {})` | 在后台运行蓝图 |
| `~yield` | `~yield` | 将控制权交还运行时 |
| `~sleep` | `~sleep(ms)` | 非阻塞睡眠 |
| `!` | `expr!` | 错误传播（后缀） |
| `?` | `?T` | 可选类型（类型前缀） |

### 关键语法差异：Auto vs Rust

| 特性 | Auto | Rust |
|------|------|------|
| 匹配分支 | `pat -> expr` | `pat => expr,` |
| 错误传播 | `expr!` | `expr?` |
| 可选类型 | `?T` | `Option<T>` |
| 错误类型 | `!T` | `Result<T, E>` |
| 蓝图类型 | `~T` | `impl Future<Output = T>` |
| 类型声明 | `type Name { }` | `struct Name { }` |
| 方法块 | `ext Name { }` | `impl Name { }` |
| 规范/Trait | `spec Name { }` | `trait Name { }` |
| 模式匹配 | `is` | `match` |
| 不安全 | `sys { }` | `unsafe { }` |
| 可变变量 | `var x = 5` | `let mut x = 5` |
| 字符串格式化 | `f"${x}"` | `format!("{}", x)` |
| 打印 | `print(x)` | `println!("{}", x)` |
| 断言相等 | `assert_eq(a, b)` | `assert_eq!(a, b)` |
| 派生 | `#derive[Debug]` | `#[derive(Debug)]` |
| 字段分隔符 | `name Type`（空格） | `name: Type`（冒号） |
| 枚举访问 | `Enum.Variant` | `Enum::Variant` |
| 模块路径 | `use.mod Name` | `use mod::Name;` |

### 非运算符符号

| 符号 | 解释 | Auto 与 Rust 差异 |
|-----|------|------------------|
| `"..."` | 字符串字面量 | 相同 |
| `'c'` | 字符字面量 | 相同 |
| `f"..."` | 格式化字符串 | Auto: `f"${expr}"`；Rust: `format!("{}", expr)` |
| `\|...\| expr` | 闭包 | 相同语法 |
| `_` | 忽略的模式绑定 | 相同 |
| `()` | 单元类型/空元组 | 相同 |
| `.` | 方法调用/字段访问 | 相同 |
| `#` | 属性前缀 | Auto: `#derive[...]`；Rust: `#[derive(...)]` |

## 附录 C：可派生规范

在书中多个地方，我们讨论了 `#derive[]` 属性，你可以将其应用于 `type` 或 `enum` 定义。`#derive[]` 属性生成代码，在你标注的类型上实现带有默认实现的规范。

这是 Auto 中 Rust `#[derive(...)]` 属性的等价物。

<Listing number="C-1" file-name="src/main.at" caption="在类型上使用 #derive[]">

```auto
#derive[Debug, Eq, Clone]
type Point {
    x int
    y int
}

fn main() {
    let p = Point(x: 1, y: 2)
    print(f"{p:?}")

    let q = p.clone()
    assert_eq(p, q)
}
```

```rust
#[derive(Debug, PartialEq, Clone)]
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let p = Point { x: 1, y: 2 };
    println!("{:?}", p);

    let q = p.clone();
    assert_eq!(p, q);
}
```

</Listing>

### `Debug` 用于程序员输出

`Debug` 规范启用调试格式化。在 Auto 中，在格式字符串中使用 `{:?}`：

```auto
print(f"{my_value:?}")
```

```rust
println!("{:?}", my_value);
```

`Debug` 是 `assert_eq` 所需的，它在断言失败时打印值。

### `Eq` 用于相等比较

`Eq` 规范（等同于 Rust 的 `PartialEq` + `Eq`）启用 `==` 和 `!=` 的相等比较：

```auto
#derive[Eq]
type Color {
    r int
    g int
    b int
}

fn main() {
    let c1 = Color(r: 255, g: 0, b: 0)
    let c2 = Color(r: 255, g: 0, b: 0)
    assert(c1 == c2)
}
```

```rust
#[derive(PartialEq, Eq)]
struct Color {
    r: i32,
    g: i32,
    b: i32,
}

fn main() {
    let c1 = Color { r: 255, g: 0, b: 0 };
    let c2 = Color { r: 255, g: 0, b: 0 };
    assert!(c1 == c2);
}
```

当在类型上派生时，两个实例仅在_所有_字段相等时才相等。当在枚举上派生时，每个变体等于自身，不等于其他变体。

### `Ord` 用于排序比较

`Ord` 规范启用比较运算符 `<`、`>`、`<=`、`>=`：

```auto
#derive[Ord]
enum Priority {
    Low
    Medium
    High
}
```

```rust
#[derive(PartialOrd, Ord)]
enum Priority {
    Low,
    Medium,
    High,
}
```

当在枚举上派生时，先声明的变体被认为小于后声明的变体。

### `Clone` 用于复制值

`Clone` 规范允许显式深拷贝一个值：

```auto
#derive[Clone]
type Config {
    name String
    value int
}

fn main() {
    let original = Config(name: "test", value: 42)
    let copy = original.clone()
}
```

```rust
#[derive(Clone)]
struct Config {
    name: String,
    value: i32,
}

fn main() {
    let original = Config { name: "test".to_string(), value: 42 };
    let copy = original.clone();
}
```

### `Hash` 用于映射到固定大小值

`Hash` 规范允许将类型用作 `HashMap` 或 `HashSet` 中的键：

```auto
#derive[Hash, Eq]
type UserId {
    id int
}

fn main() {
    let mut scores = HashMap<UserId, int>()
    scores.insert(UserId(id: 1), 100)
}
```

```rust
use std::collections::HashMap;

#[derive(Hash, PartialEq, Eq)]
struct UserId {
    id: i32,
}

fn main() {
    let mut scores = HashMap::new();
    scores.insert(UserId { id: 1 }, 100);
}
```

### `Default` 用于默认值

`Default` 规范为类型提供默认值：

```auto
#derive[Default]
type Config {
    host String    // 默认为 ""
    port int       // 默认为 0
    debug bool     // 默认为 false
}

fn main() {
    let config = Config.default()
    // 覆盖特定字段
    let config = Config(host: "localhost", ..Config.default())
}
```

```rust
#[derive(Default)]
struct Config {
    host: String,
    port: i32,
    debug: bool,
}

fn main() {
    let config = Config::default();
    // Override specific fields
    let config = Config { host: "localhost".to_string(), ..Config::default() };
}
```

### 可派生规范速查表

| Auto 规范 | Rust 等价物 | 启用功能 |
|----------|-----------|---------|
| `Debug` | `Debug` | `{:?}` 格式化 |
| `Eq` | `PartialEq` + `Eq` | `==`、`!=` 运算符 |
| `Ord` | `PartialOrd` + `Ord` | `<`、`>`、`<=`、`>=` 运算符 |
| `Clone` | `Clone` | `.clone()` 方法 |
| `Copy` | `Copy` | 赋值时隐式复制 |
| `Hash` | `Hash` | 用作 `HashMap`/`HashSet` 键 |
| `Default` | `Default` | `.default()` 方法 |

Auto 使用 `Eq` 作为单一规范，而 Rust 分为 `PartialEq` + `Eq`。同样，Auto 的 `Ord` 覆盖了 Rust 的 `PartialOrd` + `Ord`。这种简化是可行的，因为 Auto 不需要以相同方式处理 `NaN` 边缘情况——浮点类型在语言中有特殊的内置处理。

### 派生语法比较

| 特性 | Auto | Rust |
|------|------|------|
| 属性 | `#derive[Debug, Eq]` | `#[derive(Debug, PartialEq, Eq)]` |
| 多个 | `[]` 中逗号分隔 | `()` 中逗号分隔 |
| 自定义派生 | `#apply[comptime_fn]` | 独立的过程宏 crate |

## 附录 D：Auto vs Rust — 完整映射

本节提供了书中涵盖的 Auto 和 Rust 概念之间的综合映射。

### 类型系统

| 概念 | Auto | Rust |
|------|------|------|
| 定义类型 | `type Name { field Type }` | `struct Name { field: Type }` |
| 定义枚举 | `enum Name { Variant }` | `enum Name { Variant }` |
| 方法 | `ext Name { fn method() {} }` | `impl Name { fn method(&self) {} }` |
| 接口 | `spec Name { fn method() }` | `trait Name { fn method(&self); }` |
| 实现规范 | `spec Name for Type { }` | `impl Name for Type { }` |
| 泛型 | `fn name<T>(x T)` | `fn name<T>(x: T)` |
| 规范约束 | `fn name<T Spec>(x T)` | `fn name<T: Trait>(x: T)` |
| 可选 | `?T` | `Option<T>` |
| 结果 | `!T` | `Result<T, E>` |
| 蓝图 | `~T` | `impl Future<Output = T>` |
| Never 类型 | `!` | `!` |
| 类型别名 | `type Alias = Type` | `type Alias = Type;` |

### 控制流

| 概念 | Auto | Rust |
|------|------|------|
| 模式匹配 | `is` | `match` |
| 匹配分支 | `pat -> expr` | `pat => expr,` |
| 条件解构 | `if let` | `if let` |
| 错误传播 | `expr!` | `expr?` |
| 恐慌 | `panic("msg")` | `panic!("msg")` |

### 并发

| 概念 | Auto | Rust |
|------|------|------|
| 并发单元 | Actor | 线程 |
| 定义 | `actor Name { }` | `thread::spawn(\|\| { })` |
| 发送消息 | `actor.tell(Msg)` | `tx.send(msg)` |
| 接收 | `on Msg(data) { }` | `rx.recv()` |
| 异步类型 | `~T` | `impl Future<Output = T>` |
| 等待 | `on bp as v { }` | `bp.await` |
| 竞争 | `~race(a, b)` | `tokio::select!` |
| 连接 | `~join(a, b)` | `tokio::join!(a, b)` |

### 面向对象

| 概念 | Auto | Rust |
|------|------|------|
| 组合 | `is Type` | 手动嵌入 |
| 委托 | `has Type` | 手动委托 |
| 动态派发 | `dyn Spec` | `dyn Trait` |

### 元编程

| 概念 | Auto | Rust |
|------|------|------|
| 派生 | `#derive[Spec]` | `#[derive(Trait)]` |
| 编译期 | `comptime fn` | 过程宏 |
| 条件编译 | `#if[debug]` | `#[cfg(debug)]` |
| 不安全 | `sys { }` | `unsafe { }` |

## 附录 E：Auto 包工具

### `automan` vs `cargo`

| 命令 | Auto（`automan`） | Rust（`cargo`） |
|------|-----------------|----------------|
| 新建项目 | `automan new name` | `cargo new name` |
| 构建 | `automan build` | `cargo build` |
| 运行 | `automan run` | `cargo run` |
| 测试 | `automan test` | `cargo test` |
| 检查 | `automan check` | `cargo check` |
| 添加依赖 | `automan add pkg` | 添加到 `Cargo.toml` |
| 发布构建 | `automan build --release` | `cargo build --release` |
| 包文件 | `auto.toml` | `Cargo.toml` |
| 源码目录 | `src/` | `src/` |
| 入口点 | `src/main.at` | `src/main.rs` |

Auto 转译为 C，因此 `automan build` 最终通过系统的 C 编译器生成原生二进制文件。这意味着 Auto 程序可以直接调用 C 库，无需额外的 FFI 绑定。
