# 包、模块与代码组织

随着你编写的程序越来越大，代码组织将变得越来越重要。通过将相关功能分组并将不同功能的代码分离，你可以更清楚地知道在哪里找到实现特定功能的代码，以及在哪里修改功能的行为方式。

到目前为止，我们编写的程序都是在一个文件的一个模块中。随着项目的增长，你应该通过将代码拆分为多个模块和多个文件来组织代码。一个包可以包含多个二进制可执行文件和可选的一个库。随着包的增长，你可以将部分代码提取为单独的包，作为外部依赖。本章将介绍所有这些技术。

我们还将讨论封装实现细节，这让你能在更高的层次上复用代码：一旦你实现了一个操作，其他代码就可以通过公共接口调用你的代码，而不需要了解实现的工作原理。

Auto 的模块系统（有时统称为 _模块系统_）包括：

* **包（Packages）**：`automan` 的功能，让你构建、测试和共享模块
* **模块（Modules）**：产生库或可执行文件的代码树
* **导入（Imports）**：`use` 关键字让你控制路径的组织和作用域
* **扩展（Extensions）**：`ext` 关键字让你跨模块边界添加方法

在本章中，我们将介绍这些功能在 Auto 中的工作方式，以及它们与 Rust 模块系统的比较。

## 包和模块

模块系统中首先介绍的是包和模块。

_模块_ 是 Auto 编译器一次处理的最小代码量。模块可以有两种形式：二进制模块（带有 `main` 函数）或库模块（没有 `main`，用于共享）。

_包_ 是一个或多个模块的集合，提供一组功能。包包含一个 _auto.toml_ 文件，描述如何构建这些模块。

Auto 和 Rust 包系统的关键区别：

| 概念 | Auto | Rust |
|------|------|------|
| 包管理器 | `automan` | `cargo` |
| 配置文件 | `auto.toml` | `Cargo.toml` |
| 锁文件 | `auto.lock` | `Cargo.lock` |
| 编译器 | `autoc` | `rustc` |
| 包注册中心 | (待定) | crates.io |
| 代码单元名称 | `modules` | `crates` |

### 使用 `automan` 创建包

要创建一个新的 Auto 包，使用 `automan` 命令：

```console
$ automan new my-project
     Created binary (application) `my-project` package
$ ls my-project
auto.toml
src
$ ls my-project/src
main.at
```

这将创建一个具有以下结构的包：

```text
my-project
├── auto.toml
└── src
    └── main.at
```

Auto 的包结构遵循与 Rust 类似的约定，但使用 `.at` 文件扩展名而非 `.rs`。

### Auto 的代码组织层级

Auto 在三个层级组织代码：

1. **模块（mod）**：一个文件或文件夹，类似于 Rust 模块。每个文件是一个模块。每个文件夹也是一个模块，有一个以文件夹命名的入口文件。
2. **库（lib）**：多个模块组织成一个库，实现一套完整的功能。
3. **包（pac）**：一个或多个库组织成一个代码包，用于依赖管理。

## 使用类型和扩展组织代码

在 Auto 中，组织相关功能的主要方式是通过类型和扩展。虽然 Auto 的完整模块系统（原生 `mod`、`pub` 和 `use`）仍在开发中，但 `type` 和 `ext` 关键字提供了一种强大的方式来分组相关代码。

### 分组相关函数

你可以使用类型将相关函数分组在一起，类似于模块分组相关项的方式：

<Listing number="7-3" file-name="main.auto" caption="使用类型和 `ext` 组织相关函数">

```auto
type Config {
    verbose bool
    level int
}

ext Config {
    fn new(verbose bool, level int) Config {
        Config(verbose, level)
    }

    fn describe() String {
        if .verbose {
            f"Config(level=${.level})"
        } else {
            "Config"
        }
    }
}

fn main() {
    let config = Config.new(true, 3)
    print(config.describe())
}
```

```rust
struct Config {
    verbose: bool,
    level: i32,
}

impl Config {
    fn new(verbose: bool, level: i32) -> Config {
        Config { verbose, level }
    }

    fn describe(&self) -> String {
        if self.verbose {
            format!("Config(level={})", self.level)
        } else {
            String::from("Config")
        }
    }
}

fn main() {
    let config = Config::new(true, 3);
    println!("{}", config.describe());
}
```

</Listing>

这种方法提供了与模块相同的许多好处：

- **分组**：相关函数分组在类型名称下
- **命名空间**：函数通过类型名访问（`Config.new()`）
- **封装**：类型的字段和方法明确关联

### 构建复杂组织

对于更复杂的组织，你可以链式调用方法来创建流畅的 API：

<Listing number="7-4" file-name="main.auto" caption="使用构建器模式组织数学操作">

```auto
type Math {
    value int
}

ext Math {
    fn new(value int) Math {
        Math(value)
    }

    fn add(other int) Math {
        Math(.value + other)
    }

    fn double() Math {
        .add(.value)
    }

    fn result() int {
        .value
    }
}

fn main() {
    let m = Math.new(5)
    let doubled = m.double()
    print(f"Result: ${doubled.result()}")
}
```

```rust
struct Math {
    value: i32,
}

impl Math {
    fn new(value: i32) -> Math {
        Math { value }
    }

    fn add(&self, other: i32) -> Math {
        Math { value: self.value + other }
    }

    fn double(&self) -> Math {
        self.add(self.value)
    }

    fn result(&self) -> i32 {
        self.value
    }
}

fn main() {
    let m = Math::new(5);
    let doubled = m.double();
    println!("Result: {}", doubled.result());
}
```

</Listing>

## 使用外部 Rust 包

Auto 可以通过 `use.rust` 指令利用 Rust 广泛的生态系统。这允许你从 Rust 标准库和外部包导入类型和函数：

<Listing number="7-1" file-name="main.auto" caption="使用 `use.rust` 从 Rust 标准库导入">

```auto
use.rust std::collections::HashMap

fn main() {
    var scores = HashMap.new()
    scores.insert("Blue", 10)
    scores.insert("Red", 50)
    print(f"Scores: ${scores}")
}
```

```rust
use std::collections::HashMap;

fn main() {
    let mut scores = HashMap::new();
    scores.insert("Blue", 10);
    scores.insert("Red", 50);
    println!("Scores: {:?}", scores);
}
```

</Listing>

`use.rust` 指令在转译过程中将导入语句直接传递给 Rust 编译器。这使得 Auto 在原生模块系统开发期间就能访问 Rust 的完整标准库和包生态系统。

### 多个导入

你可以使用多个 `use.rust` 语句导入不同的类型：

<Listing number="7-2" file-name="main.auto" caption="多个 `use.rust` 导入">

```auto
use.rust std::collections::HashMap

fn main() {
    var map = HashMap.new()
    map.insert("key", "value")
    print(f"Map: ${map}")
}
```

```rust
use std::collections::HashMap;

fn main() {
    let mut map = HashMap::new();
    map.insert("key", "value");
    println!("Map: {:?}", map);
}
```

</Listing>

<Listing number="7-5" file-name="main.auto" caption="导入文件系统函数">

```auto
use.rust std::fs::read_to_string

fn main() {
    print("File reading example")
}
```

```rust
use std::fs::read_to_string;

fn main() {
    println!("File reading example");
}
```

</Listing>

## Auto 的模块愿景

Auto 的模块系统设计遵循以下目标：

- **简化的导入**：一旦模块系统完全实现，原生 Auto 导入将使用不带 `.rust` 后缀的 `use`
- **跨平台组织**：`ext` 关键字允许平台特定的实现跨模块边界填充方法
- **可见性默认值**：Auto 计划使用 `#[pub]` 注解来控制可见性，类似于 Rust 的 `pub` 关键字

计划的模块结构遵循以下模式：

```text
my-package/
├── auto.toml
└── src/
    ├── main.at          # 二进制入口点
    ├── lib.at           # 库入口点（可选）
    ├── config.at        # Config 模块
    └── utils/           # Utils 模块（目录）
        ├── utils.at     # 模块入口文件
        └── http.at      # 子模块
```

每个文件是一个模块。每个文件夹也是一个模块，有一个以文件夹命名的入口文件。这反映了 Rust 的模块约定，但使用 `.at` 文件扩展名。

## 总结

Auto 的代码组织系统提供了与 Rust 相同的目标，但在实现上有一些差异：

| 概念 | Auto | Rust |
|------|------|------|
| 包管理器 | `automan` | `cargo` |
| 配置文件 | `auto.toml` | `Cargo.toml` |
| 代码单元 | `module` | `crate` |
| 定义类型 | `type Name { }` | `struct Name { }` |
| 扩展类型 | `ext Name { }` | `impl Name { }` |
| 导入 (Rust) | `use.rust path::item` | `use path::item;` |
| 可见性 | `#[pub]`（计划中） | `pub` |
| 文件扩展名 | `.at` | `.rs` |

虽然 Auto 的原生模块系统仍在开发中，但 `type`、`ext` 和 `use.rust` 的组合提供了有效的代码组织方式。`type` 关键字分组相关数据，`ext` 跨文件边界添加方法，而 `use.rust` 提供对 Rust 生态系统的访问。

在下一章中，我们将了解标准库中的一些集合数据结构，你可以在整洁组织的代码中使用它们。
