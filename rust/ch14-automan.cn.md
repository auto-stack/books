# 深入了解 automan

到目前为止，我们只使用了 `automan` 的最基本功能来构建、运行和测试代码，但它的能力远不止于此。本章将讨论一些更高级的功能，展示如何做到以下几点：

- 通过发布配置文件（release profiles）自定义构建
- 在包注册中心发布库
- 用工作空间（workspaces）组织大型项目
- 从包注册中心安装二进制文件
- 使用自定义命令扩展 `automan`

`automan` 与 Rust 的构建系统 Cargo 共享许多概念。如果你以前用过 Cargo，这里很多内容会很熟悉，不过 Auto 的工具链仍在不断发展中。

## 使用发布配置文件自定义构建

在 Auto 中，_发布配置文件_是预定义的可自定义配置，允许程序员更精细地控制代码编译的各种选项。每个配置文件独立配置，互不影响。

`automan` 有两个主要配置文件：运行 `automan build` 时使用的 `dev` 配置文件，以及运行 `automan build --release` 时使用的 `release` 配置文件。`dev` 配置文件为开发提供了合理的默认值，`release` 配置文件则为发布构建提供了优化的默认值。

这些配置文件名称可能在你构建输出的信息中见过：

```console
$ automan build
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
$ automan build --release
    Finished `release` profile [optimized] target(s) in 0.32s
```

`dev` 和 `release` 就是编译器使用的不同配置文件。

`automan` 为每个配置文件设置了默认值，当你在项目的 _auto.toml_ 文件中没有显式添加 `[profile.*]` 部分时，这些默认值就会生效。通过为需要自定义的配置文件添加 `[profile.*]` 部分，你可以覆盖默认设置的任何子集。例如，以下是 `dev` 和 `release` 配置文件中 `opt-level` 设置的默认值：

文件名：auto.toml

```toml
[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
```

`opt-level` 设置控制编译器对代码应用的优化级别，范围为 0 到 3。应用更多优化会延长编译时间，所以如果你在开发阶段频繁编译代码，你会希望更少的优化以加快编译速度，即使生成的代码运行得更慢。因此 `dev` 的默认 `opt-level` 是 `0`。当你准备发布代码时，多花些时间编译是值得的。你只需在发布模式下编译一次，但会多次运行编译后的程序，所以发布模式用更长的编译时间换取更快的运行速度。这就是 `release` 配置文件的默认 `opt-level` 为 `3` 的原因。

你可以通过在 _auto.toml_ 中添加不同的值来覆盖默认设置。例如，如果我们想在开发配置文件中使用优化级别 1，可以在项目的 _auto.toml_ 文件中添加这两行：

文件名：auto.toml

```toml
[profile.dev]
opt-level = 1
```

这段代码覆盖了默认设置 `0`。现在当我们运行 `automan build` 时，`automan` 会使用 `dev` 配置文件的默认值加上我们对 `opt-level` 的自定义。因为我们把 `opt-level` 设为 `1`，`automan` 会应用比默认更多的优化，但不如发布构建那么多。

这与 Cargo 的发布配置文件工作方式相同。有关每个配置文件的完整配置选项和默认值列表，请参阅 `automan` 的文档。

## 将包发布到注册中心

我们已经从注册中心使用过包作为项目的依赖，但你也可以通过发布自己的包来与他人分享代码。包注册中心分发你包的源代码，因此它主要托管开源代码。

> **注意：** Auto 的包注册中心仍在开发中。本节描述了注册中心可用后发布将如何工作。在此期间，你可以通过 Auto-to-Rust 转译工作流将 Auto 包作为 Rust crate 发布，或者直接托管 Git 仓库来分享 Auto 包。

Auto 和 `automan` 提供了一些功能，使你发布的包更容易被他人找到和使用。接下来我们将讨论其中一些功能，然后解释如何发布包。

### 编写有用的文档注释

准确地记录你的包将帮助其他用户了解如何以及何时使用它们，因此投入时间编写文档是值得的。在第 3 章，我们讨论了如何使用两个斜杠 `//` 来注释 Auto 代码。Auto 还有一种特殊的注释用于文档，即_文档注释_，它可以生成 HTML 文档。这些 HTML 文档显示公共 API 项的文档注释内容，面向的是想了解如何_使用_你的包而非如何_实现_它的程序员。

文档注释使用三个斜杠 `///` 而不是两个，并支持 Markdown 格式。将文档注释放在被文档说明的项之前。代码清单 14-1 展示了一个名为 `my_package` 的包中 `add_one` 函数的文档注释。

<Listing number="14-1" file-name="src/lib.at" caption="函数的文档注释">

```auto
/// 给传入的数字加一。
///
/// # Examples
///
/// ```
/// let arg = 5
/// let answer = my_package::add_one(arg)
///
/// assert_eq(6, answer)
/// ```
pub fn add_one(x int) int {
    x + 1
}
```

```rust
/// Adds one to the number given.
///
/// # Examples
///
/// ```
/// let arg = 5;
/// let answer = my_crate::add_one(arg);
///
/// assert_eq!(6, answer);
/// ```
pub fn add_one(x: i32) -> i32 {
    x + 1
}
```

</Listing>

这里我们给出了 `add_one` 函数的功能描述，用 `Examples` 标题开始了一个小节，然后提供了演示如何使用 `add_one` 函数的代码。我们可以通过运行 `automan doc` 从这个文档注释生成 HTML 文档。此命令使用 `autodoc` 工具（等价于 Rust 的 `rustdoc`）并将生成的 HTML 文档放在 _target/doc_ 目录中。

为方便起见，运行 `automan doc --open` 会构建当前包文档的 HTML（以及所有包依赖的文档）并在浏览器中打开结果。

#### 常用的小节

我们在代码清单 14-1 中使用了 `# Examples` Markdown 标题创建了一个名为 "Examples" 的 HTML 小节。以下是包作者在文档中常用的其他小节：

- **Panics**：被文档说明的函数可能发生 panic 的场景。不希望程序 panic 的调用者应确保不在这些情况下调用该函数。
- **Errors**：如果函数返回 `!T`（Auto 的错误类型），描述可能发生的错误类型以及导致这些错误返回的条件，可以帮助调用者编写代码以不同方式处理不同类型的错误。
- **Safety**：如果函数使用了 `sys` 关键字（我们在第 20 章讨论 `sys`），应该有一个小节解释为什么该函数是不安全的，并说明该函数期望调用者遵守的不变量。

大多数文档注释不需要所有这些小节，但这是一个很好的清单，可以提醒你用户可能感兴趣了解的代码方面。

#### 文档注释作为测试

在文档注释中添加示例代码可以帮助演示如何使用你的库，还有一个额外的好处：运行 `automan test` 会将文档中的代码示例作为测试运行！没有什么比带示例的文档更好了。但也没有什么比因代码在文档编写后发生了变化而无法工作的示例更糟糕了。如果我们用代码清单 14-1 中 `add_one` 函数的文档运行 `automan test`，我们会在测试结果中看到这样的输出：

```text
   Doc-tests my_package

running 1 test
test src/lib.at - add_one (line 5) ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 filtered out
```

现在，如果我们修改了函数或示例，使得示例中的 `assert_eq` 发生 panic，再次运行 `automan test`，我们会看到文档测试捕获了示例和代码不同步的问题！

#### 包含项的注释

`//!` 风格的文档注释为_包含_这些注释的项添加文档，而不是为注释_之后_的项添加文档。我们通常在包根文件（约定为 _src/lib.at_）或模块内部使用这种文档注释，来记录整个包或模块。

例如，要为包含 `add_one` 函数的 `my_package` 包添加描述其用途的文档，我们在 _src/lib.at_ 文件开头添加以 `//!` 开头的文档注释，如代码清单 14-2 所示。

<Listing number="14-2" file-name="src/lib.at" caption="整个 `my_package` 包的文档">

```auto
//! # My Package
//!
//! `my_package` 是一个工具集合，使执行某些计算更加方便。

/// 给传入的数字加一。
// --snip--
///
/// # Examples
///
/// ```
/// let arg = 5
/// let answer = my_package::add_one(arg)
///
/// assert_eq(6, answer)
/// ```
pub fn add_one(x int) int {
    x + 1
}
```

```rust
//! # My Crate
//!
//! `my_crate` is a collection of utilities to make performing certain
//! calculations more convenient.

/// Adds one to the number given.
// --snip--
///
/// # Examples
///
/// ```
/// let arg = 5;
/// let answer = my_crate::add_one(arg);
///
/// assert_eq!(6, answer);
/// ```
pub fn add_one(x: i32) -> i32 {
    x + 1
}
```

</Listing>

注意以 `//!` 开头的最后一行之后没有任何代码。因为我们用 `//!` 而不是 `///` 开始注释，我们是在为包含此注释的项添加文档，而不是为此注释之后的项。在这种情况下，这个项就是 _src/lib.at_ 文件，即包根。这些注释描述了整个包。

当我们运行 `automan doc --open` 时，这些注释会显示在 `my_package` 文档首页的公共项列表上方。

包含项的文档注释对于描述包和模块特别有用。使用它们来解释容器的整体用途，帮助用户理解包的组织方式。

### 导出便捷的公共 API

公共 API 的结构是发布包时需要重点考虑的问题。使用你的包的人对你代码结构的熟悉程度远不如你，如果你的包有很深的模块层次，他们可能很难找到想要使用的部分。

在第 7 章，我们介绍了如何用类型和扩展来组织代码，以及如何使用 `use` 关键字将项引入作用域。然而，你在开发包时有意义的结构可能对你的用户来说并不方便。你可能想用包含多层的层次结构来组织类型，但那样想使用你在层次深处定义的类型的用户可能会很难发现它的存在。他们也可能因为必须输入 `use my_package::some_module::another_module::UsefulType` 而不是 `use my_package::UsefulType` 而感到烦恼。

好消息是，如果结构对其他人使用来说不方便，你不必重新安排内部组织：你可以使用 `pub use` 重新导出项，创建一个与私有结构不同的公共结构。_重新导出_将一个位置的公共项在另一个位置也设为公共，就像它是在另一个位置定义的一样。

例如，假设我们创建了一个名为 `art` 的库来建模艺术概念。这个库中有两个模块：一个 `kinds` 模块包含两个枚举 `PrimaryColor` 和 `SecondaryColor`，一个 `utils` 模块包含一个名为 `mix` 的函数，如代码清单 14-3 所示。

<Listing number="14-3" file-name="src/lib.at" caption="一个将项组织到 `kinds` 和 `utils` 模块中的 `art` 库">

```auto
//! # Art
//!
//! 一个用于建模艺术概念的库。

pub mod kinds {
    /// RYB 色彩模型中的原色。
    pub enum PrimaryColor {
        Red
        Yellow
        Blue
    }

    /// RYB 色彩模型中的间色。
    pub enum SecondaryColor {
        Orange
        Green
        Purple
    }
}

pub mod utils {
    use kinds::*;

    /// 将两种原色等量混合，创建一种间色。
    pub fn mix(c1 PrimaryColor, c2 PrimaryColor) SecondaryColor {
        // --snip--
        // TODO: 实现
    }
}
```

```rust
//! # Art
//!
//! A library for modeling artistic concepts.

pub mod kinds {
    /// The primary colors according to the RYB color model.
    pub enum PrimaryColor {
        Red,
        Yellow,
        Blue,
    }

    /// The secondary colors according to the RYB color model.
    pub enum SecondaryColor {
        Orange,
        Green,
        Purple,
    }
}

pub mod utils {
    use crate::kinds::*;

    /// Combines two primary colors in equal amounts to create
    /// a secondary color.
    pub fn mix(c1: PrimaryColor, c2: PrimaryColor) -> SecondaryColor {
        // --snip--
        unimplemented!();
    }
}
```

</Listing>

注意 `PrimaryColor` 和 `SecondaryColor` 类型以及 `mix` 函数没有列在生成文档的首页上。我们需要点击 `kinds` 和 `utils` 才能看到它们。

依赖此库的另一个包需要 `use` 语句将 `art` 中的项引入作用域，指定当前定义的模块结构。代码清单 14-4 展示了一个使用 `art` 包中 `PrimaryColor` 和 `mix` 项的示例。

<Listing number="14-4" file-name="src/main.at" caption="使用 `art` 包内部结构导出项的包">

```auto
use art::kinds::PrimaryColor
use art::utils::mix

fn main() {
    let red = PrimaryColor.Red
    let yellow = PrimaryColor.Yellow
    mix(red, yellow)
}
```

```rust
use art::kinds::PrimaryColor;
use art::utils::mix;

fn main() {
    let red = PrimaryColor::Red;
    let yellow = PrimaryColor::Yellow;
    mix(red, yellow);
}
```

</Listing>

代码清单 14-4 的作者必须弄清楚 `PrimaryColor` 在 `kinds` 模块中，`mix` 在 `utils` 模块中。`art` 包的模块结构对开发它的开发者来说比使用它的人更有意义。内部结构对试图理解如何_使用_ `art` 包的人来说没有提供有用的信息，反而会造成困惑，因为使用者必须弄清楚去哪里找，并且必须在 `use` 语句中指定模块名。

要消除公共 API 中的内部组织，我们可以修改代码清单 14-3 中的 `art` 包代码，添加 `pub use` 语句在顶层重新导出项，如代码清单 14-5 所示。

<Listing number="14-5" file-name="src/lib.at" caption="添加 `pub use` 语句重新导出项">

```auto
//! # Art
//!
//! 一个用于建模艺术概念的库。

pub use self::kinds::PrimaryColor
pub use self::kinds::SecondaryColor
pub use self::utils::mix

pub mod kinds {
    // --snip--
    /// RYB 色彩模型中的原色。
    pub enum PrimaryColor {
        Red
        Yellow
        Blue
    }

    /// RYB 色彩模型中的间色。
    pub enum SecondaryColor {
        Orange
        Green
        Purple
    }
}

pub mod utils {
    // --snip--
    use kinds::*;

    /// 将两种原色等量混合，创建一种间色。
    pub fn mix(c1 PrimaryColor, c2 PrimaryColor) SecondaryColor {
        SecondaryColor.Orange
    }
}
```

```rust
//! # Art
//!
//! A library for modeling artistic concepts.

pub use self::kinds::PrimaryColor;
pub use self::kinds::SecondaryColor;
pub use self::utils::mix;

pub mod kinds {
    // --snip--
    /// The primary colors according to the RYB color model.
    pub enum PrimaryColor {
        Red,
        Yellow,
        Blue,
    }

    /// The secondary colors according to the RYB color model.
    pub enum SecondaryColor {
        Orange,
        Green,
        Purple,
    }
}

pub mod utils {
    // --snip--
    use crate::kinds::*;

    /// Combines two primary colors in equal amounts to create
    /// a secondary color.
    pub fn mix(c1: PrimaryColor, c2: PrimaryColor) -> SecondaryColor {
        SecondaryColor::Orange
    }
}
```

</Listing>

`automan doc` 为此包生成的 API 文档现在会在首页列出并链接重新导出的项，使 `PrimaryColor` 和 `SecondaryColor` 类型以及 `mix` 函数更容易找到。

`art` 包的用户仍然可以像代码清单 14-4 那样查看和使用内部结构，或者像代码清单 14-6 那样使用更便捷的结构。

<Listing number="14-6" file-name="src/main.at" caption="使用 `art` 包重新导出项的程序">

```auto
use art::PrimaryColor
use art::mix

fn main() {
    // --snip--
    let red = PrimaryColor.Red
    let yellow = PrimaryColor.Yellow
    mix(red, yellow)
}
```

```rust
use art::PrimaryColor;
use art::mix;

fn main() {
    // --snip--
    let red = PrimaryColor::Red;
    let yellow = PrimaryColor::Yellow;
    mix(red, yellow);
}
```

</Listing>

当有很多嵌套模块时，使用 `pub use` 在顶层重新导出类型可以极大改善使用包的人的体验。`pub use` 的另一个常见用途是在当前包中重新导出依赖项的定义，使该包的定义成为你包公共 API 的一部分。

创建有用的公共 API 结构更像是一门艺术而非科学，你可以不断迭代找到最适合用户的 API。选择 `pub use` 让你灵活地安排包的内部结构，并将内部结构与呈现给用户的内容解耦。

### 设置账户

> **注意：** Auto 的包注册中心仍在开发中。账户设置过程将与其他语言注册中心（如 Rust 的 crates.io）类似。以下描述了预期的工作流程。

在发布任何包之前，你需要在 Auto 包注册中心创建账户并获取 API 令牌。然后运行 `automan login` 命令，在提示时粘贴你的 API 密钥：

```console
$ automan login
abcdefghijklmnopqrstuvwxyz012345
```

此命令会告知 `automan` 你的 API 令牌，并将其存储在本地的 _~/.automan/credentials.toml_ 中。注意此令牌是密钥：不要与任何人分享。如果因任何原因分享了，你应该立即撤销并生成新令牌。

### 为新包添加元数据

在发布之前，你需要在包的 _auto.toml_ 文件的 `[package]` 部分添加一些元数据。你的包需要一个唯一的名称。注册中心上的包名按先到先得的原则分配。在尝试发布之前，搜索你想使用的名称。如果该名称已被使用，你需要找另一个名称并编辑 _auto.toml_ 中的 `name` 字段：

文件名：auto.toml

```toml
[package]
name = "guessing_game"
```

当你运行 `automan publish` 时，如果缺少必需的元数据，你会收到警告和错误信息：

```text
warning: manifest has no description, license, documentation, homepage or repository.
error: failed to publish to registry
missing or empty metadata fields: description, license.
```

在 _auto.toml_ 中添加描述和许可证。对于 `license` 字段，使用 SPDX 许可证标识符。例如，指定 MIT 许可证：

文件名：auto.toml

```toml
[package]
name = "guessing_game"
license = "MIT"
```

你也可以指定多个许可证，用 `OR` 分隔：

```toml
[package]
name = "guessing_game"
version = "0.1.0"
description = "一个有趣的游戏，你猜测计算机选择了什么数字。"
license = "MIT OR Apache-2.0"
```

有了唯一的名称、版本号、描述和许可证，准备发布的 _auto.toml_ 文件可能如下：

文件名：auto.toml

```toml
[package]
name = "guessing_game"
version = "0.1.0"
description = "一个有趣的游戏，你猜测计算机选择了什么数字。"
license = "MIT OR Apache-2.0"

[dependencies]
```

### 发布到注册中心

现在你已经创建了账户、保存了 API 令牌、选择了包名并指定了必需的元数据，可以发布了！发布包会将特定版本上传到注册中心供他人使用。

请注意，发布是_永久性的_。版本永远无法被覆盖，代码也无法删除（除非在特定情况下）。包注册中心的一个主要目标是作为代码的永久归档，使所有依赖注册中心中包的项目构建能持续正常工作。允许删除版本将使这一目标无法实现。不过，你可以发布的包版本数量没有限制。

运行 `automan publish` 命令来发布你的包：

```console
$ automan publish
   Packaging guessing_game v0.1.0
    Packaged 6 files, 1.2KiB
   Verifying guessing_game v0.1.0
   Compiling guessing_game v0.1.0
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.19s
   Uploading guessing_game v0.1.0
    Published guessing_game v0.1.0
```

恭喜！你现在已经与 Auto 社区分享了你的代码，任何人都可以轻松地将你的包添加为他们项目的依赖。

### 发布现有包的新版本

当你对包做了修改并准备好发布新版本时，修改 _auto.toml_ 中指定的 `version` 值并重新发布。使用语义化版本规则，根据你所做更改的类型来决定合适的下一个版本号，然后运行 `automan publish` 上传新版本。

### 从注册中心废弃版本

虽然你不能删除包的先前版本，但可以阻止未来的项目将它们添加为新依赖。当某个包版本因某种原因有问题时，这很有用。在这种情况下，`automan` 支持"撤回"（yank）包版本。

_撤回_（Yanking）一个版本会阻止新项目依赖该版本，同时允许所有已依赖它的现有项目继续使用。本质上，撤回意味着所有有 _auto.lock_ 文件的项目不会中断，而任何未来生成的 _auto.lock_ 文件也不会使用被撤回的版本。

要撤回某个包的版本，运行 `automan yank` 并指定要撤回的版本：

```console
$ automan yank --vers 1.0.1
    Yanking guessing_game@1.0.1
```

在命令中添加 `--undo`，你也可以撤销撤回，允许项目再次依赖该版本：

```console
$ automan yank --vers 1.0.1 --undo
    Unyanking guessing_game@1.0.1
```

撤回_不会_删除任何代码。它不能删除意外上传的密钥。如果发生这种情况，你必须立即重置这些密钥。

## automan 工作空间

在第 12 章，我们构建了一个包含二进制和库的包。随着项目发展，你可能发现库部分不断变大，想要进一步将包拆分为多个库包。`automan` 提供了一个叫做_工作空间_的功能，可以帮助管理同步开发的多个相关包。

### 创建工作空间

_工作空间_是一组共享同一个 _auto.lock_ 和输出目录的包。让我们用工作空间来创建一个项目——我们使用简单的代码，以便专注于工作空间的结构。创建工作空间有多种方式，我们只展示一种常见方式。我们将创建一个包含一个二进制和两个库的工作空间。二进制将提供主要功能，并依赖这两个库。一个库提供 `add_one` 函数，另一个提供 `add_two` 函数。

首先，创建工作空间的新目录：

```console
$ mkdir add
$ cd add
```

接下来，在 _add_ 目录中创建配置整个工作空间的 _auto.toml_ 文件。此文件不会有 `[package]` 部分。相反，它以 `[workspace]` 部分开始：

文件名：auto.toml

```toml
[workspace]
members = []
```

接下来，在 _add_ 目录中运行 `automan new` 创建 `adder` 二进制包：

```console
$ automan new adder
     Created binary (application) `adder` package
```

在工作空间内运行 `automan new` 也会自动将新创建的包添加到 `[workspace]` 定义中的 `members` 键里：

```toml
[workspace]
members = ["adder"]
```

此时，我们可以通过运行 `automan build` 来构建工作空间。你的 _add_ 目录中的文件应该如下：

```text
├── auto.lock
├── auto.toml
├── adder
│   ├── auto.toml
│   └── src
│       └── main.at
└── target
```

工作空间在顶层有一个 _target_ 目录用于放置编译产物；`adder` 包没有自己的 _target_ 目录。即使我们从 _adder_ 目录内运行 `automan build`，编译产物仍然会放在 _add/target_ 而不是 _add/adder/target_。`automan` 这样组织工作空间的 _target_ 目录是因为工作空间中的包是要互相依赖的。如果每个包都有自己的 _target_ 目录，每个包就得重新编译工作空间中的所有其他包，将产物放在自己的 _target_ 目录中。通过共享一个 _target_ 目录，各包可以避免不必要的重复编译。

### 在工作空间中创建第二个包

接下来，让我们在工作空间中创建另一个成员包，命名为 `add_one`。生成一个新的库包：

```console
$ automan new add_one --lib
     Created library `add_one` package
```

顶层 _auto.toml_ 现在会在 `members` 列表中包含 `add_one`：

文件名：auto.toml

```toml
[workspace]
members = ["adder", "add_one"]
```

你的 _add_ 目录现在应该包含这些目录和文件：

```text
├── auto.lock
├── auto.toml
├── add_one
│   ├── auto.toml
│   └── src
│       └── lib.at
├── adder
│   ├── auto.toml
│   └── src
│       └── main.at
└── target
```

在 _add_one/src/lib.at_ 文件中，让我们添加一个 `add_one` 函数：

<Listing number="14-7" file-name="add_one/src/lib.at" caption="库包中的 `add_one` 函数">

```auto
pub fn add_one(x int) int {
    x + 1
}
```

```rust
pub fn add_one(x: i32) -> i32 {
    x + 1
}
```

</Listing>

现在我们可以让包含二进制的 `adder` 包依赖包含库的 `add_one` 包。首先，需要在 _adder/auto.toml_ 中添加对 `add_one` 的路径依赖：

文件名：adder/auto.toml

```toml
[dependencies]
add_one = { path = "../add_one" }
```

`automan` 不会假设工作空间中的包会互相依赖，所以我们需要明确声明依赖关系。

接下来，让我们在 `adder` 包中使用 `add_one` 函数。打开 _adder/src/main.at_，修改 `main` 函数来调用 `add_one`，如代码清单 14-8 所示。

<Listing number="14-8" file-name="adder/src/main.at" caption="从 `adder` 包使用 `add_one` 库包">

```auto
fn main() {
    let num = 10
    print(f"Hello, world! ${num} plus one is ${add_one::add_one(num)}!")
}
```

```rust
fn main() {
    let num = 10;
    println!("Hello, world! {} plus one is {}!", num, add_one::add_one(num));
}
```

</Listing>

让我们在顶层 _add_ 目录运行 `automan build` 来构建工作空间：

```console
$ automan build
   Compiling add_one v0.1.0
   Compiling adder v0.1.0
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.22s
```

要从 _add_ 目录运行二进制包，使用 `-p` 参数指定要运行的工作空间中的包名：

```console
$ automan run -p adder
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running target/debug/adder
Hello, world! 10 plus one is 11!
```

### 依赖外部包

注意工作空间只在顶层有一个 _auto.lock_ 文件，而不是每个包目录中都有一个。这确保了所有包使用相同版本的依赖。如果我们向 _adder/auto.toml_ 和 _add_one/auto.toml_ 添加相同的外部包，`automan` 会将两者解析为一个版本并记录在唯一的 _auto.lock_ 中。让工作空间中的所有包使用相同的依赖意味着这些包始终互相兼容。

让我们向 _add_one/auto.toml_ 添加外部依赖：

文件名：add_one/auto.toml

```toml
[dependencies]
rand = "0.8.5"
```

在 _add_ 目录运行 `automan build` 构建整个工作空间会引入并编译 `rand` 依赖。

顶层 _auto.lock_ 现在包含了 `add_one` 对 `rand` 依赖的信息。然而，即使 `rand` 在工作空间某处被使用，除非我们也把 `rand` 添加到其他包的 _auto.toml_ 文件中，否则不能在其他包中使用它。这确保了每个包明确声明自己的依赖。

### 在工作空间中添加测试

让我们再添加一个改进，在 `add_one` 包中为 `add_one::add_one` 函数添加测试：

<Listing number="14-9" file-name="add_one/src/lib.at" caption="在 `add_one` 库包中添加测试">

```auto
pub fn add_one(x int) int {
    x + 1
}

#[test]
fn it_works() {
    assert_eq(3, add_one(2))
}
```

```rust
pub fn add_one(x: i32) -> i32 {
    x + 1
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(3, add_one(2));
    }
}
```

</Listing>

现在在顶层 _add_ 目录运行 `automan test`。在这样结构的工作空间中运行 `automan test` 会运行工作空间中所有包的测试：

```console
$ automan test
   Compiling add_one v0.1.0
   Compiling adder v0.1.0
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.20s
     Running unittests src/lib.at (add_one)

running 1 test
test it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 filtered out
```

我们也可以在顶层目录使用 `-p` 标志运行工作空间中特定包的测试：

```console
$ automan test -p add_one
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running unittests src/lib.at (add_one)

running 1 test
test it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 filtered out
```

如果你将工作空间中的包发布到注册中心，工作空间中的每个包都需要单独发布。与 `automan test` 类似，我们可以使用 `-p` 标志指定要发布的包名来发布特定包。

随着项目增长，考虑使用工作空间：它使你能用更小、更容易理解的组件来工作，而不是一大团代码。此外，如果工作空间中的包经常同时修改，将它们放在工作空间中可以更容易地协调各包之间的变更。

## 使用 `automan install` 安装二进制文件

`automan install` 命令允许你在本地安装和使用二进制包。这不是为了替代系统包管理器；它是为 Auto 开发者提供的一种便捷方式，用来安装他人在包注册中心上分享的工具。注意，你只能安装有二进制目标的包——即有 _src/main.at_ 文件或另一个指定为二进制的文件的包，而非库目标（库目标本身不能运行，但适合包含在其他程序中）。

所有通过 `automan install` 安装的二进制文件都存储在安装根目录的 _bin_ 文件夹中。如果你没有自定义配置，此目录将是 _$HOME/.automan/bin_。确保此目录在你的 `$PATH` 中，以便能运行通过 `automan install` 安装的程序。

例如，要安装注册中心上发布的工具：

```console
$ automan install some-tool
   Installing some-tool v1.2.3
    Finished `release` profile [optimized + debuginfo] target(s) in 6.73s
  Installing ~/.automan/bin/some-tool
   Installed package `some-tool v1.2.3`
```

只要安装目录在你的 `$PATH` 中，你就可以直接从命令行运行已安装的工具。

## 使用自定义命令扩展 automan

`automan` 的设计允许你通过新的子命令来扩展它，而无需修改 `automan` 本身。如果你的 `$PATH` 中有一个名为 `automan-something` 的二进制文件，你可以通过运行 `automan something` 来像 `automan` 子命令一样运行它。当你运行 `automan --list` 时，这类自定义命令也会被列出。能够使用 `automan install` 安装扩展，然后像内置的 `automan` 工具一样运行它们，这是 `automan` 设计中极其方便的一个特性！

## automan 与 Cargo 对比速查表

| 功能 | Auto（`automan`） | Rust（`cargo`） |
|------|-------------------|----------------|
| 构建 | `automan build` | `cargo build` |
| 运行 | `automan run` | `cargo run` |
| 测试 | `automan test` | `cargo test` |
| 文档 | `automan doc` | `cargo doc` |
| 发布 | `automan publish` | `cargo publish` |
| 安装 | `automan install` | `cargo install` |
| 新项目 | `automan new name` | `cargo new name` |
| 配置文件 | `auto.toml` | `Cargo.toml` |
| 锁文件 | `auto.lock` | `Cargo.lock` |
| 源文件扩展名 | `.at` | `.rs` |
| 注册中心 | （待定） | crates.io |

## 总结

使用 `automan` 和包注册中心分享代码是使 Auto 生态系统在许多不同任务中有用的一部分。Auto 的标准库小而稳定，但包很容易分享、使用和改进，且时间线与语言本身不同。不要害羞，分享对你有用的代码——它可能对其他人也有用！

本章涵盖了：

1. **发布配置文件** —— 自定义 `dev` 和 `release` 的构建优化
2. **文档注释** —— `///` 和 `//!` 用于生成文档和运行文档测试
3. **`pub use` 重新导出** —— 使公共 API 对用户更便捷
4. **发布包** —— 账户设置、元数据、版本管理和撤回
5. **工作空间** —— 管理共享依赖的多个相关包
6. **安装二进制文件** —— `automan install` 用于本地工具安装
7. **自定义命令** —— 用 `automan-*` 二进制文件扩展 `automan`

在下一章，我们将探讨 Auto 中的引用和指针，以及它们与 Rust 智能指针类型的关系。
