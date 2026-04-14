# 入门指南

本章将《C 语言小书》适配为面向 C 目标的 Auto 程序员版本。你将了解 C 是什么、为什么
Auto 以 C 为目标，以及如何搭建 a2c 转译器的开发环境。

## 1. 什么是 C

C 是由贝尔实验室的 Dennis Ritchie 于 1972 年创建的通用编程语言。它至今仍是全球使用
最广泛的编程语言之一。操作系统、嵌入式系统、数据库和语言运行时都是用 C 编写的。

### 为什么 Auto 以 C 为目标

Auto 的 `a2c` 转译器将 Auto 源代码转换为 C。这使得 Auto 程序可以在任何拥有 C 编译器
的平台上运行——实际上就是所有平台。a2c 流程如下：

1. 将 Auto 源代码解析为 AST。
2. 将 AST 降低为 C，将 Auto 构造映射到对应的 C 等价物。
3. 生成 `.c` 文件，可使用任何标准 C 编译器（GCC、Clang、MSVC）编译。

你只需编写简洁、高层的 Auto 代码，转译器会生成可移植的 C 代码。

## 2. 安装工具链

要开发编译到 C 的 Auto 程序，需要安装两样东西：

1. **C 编译器** — GCC、Clang 或 MSVC。
2. **Auto + a2c** — 包含 a2c 转译器的 Auto 工具链。

### 安装 C 编译器

在 Linux 上，通过发行版的包管理器安装 GCC：

```console
$ sudo apt install build-essential    # Debian/Ubuntu
$ sudo dnf install gcc                # Fedora
```

在 macOS 上，安装 Xcode 命令行工具：

```console
$ xcode-select --install
```

在 Windows 上，安装 Visual Studio 或 Build Tools，其中包含 MSVC。

### 安装 Auto

从官方网站下载并安装 Auto。验证安装：

```console
$ auto --version
auto x.y.z (yyyy-mm-dd)
```

## 3. 第一个程序

每段旅程都从 Hello World 开始。

<Listing name="hello-world" file="listings/ch00/listing-00-01">

```auto
fn main() {
    print("Hello, world!")
}
```

</Listing>

a2c 转译器生成的 C 输出如下：

```c
// Auto → C transpiled by a2c
#include <stdio.h>

int main(void) {
    printf("%s\n", "Hello, world!");
    return 0;
}
```

注意以下关键映射：

- `fn main()` 变为 `int main(void)`。
- `print("text")` 变为 `printf("%s\n", "text");`。
- 在 `main` 末尾自动添加隐式的 `return 0;`。

## 4. 程序结构剖析

对比 Auto 和 C 版本：

```auto
fn main() {
    let name str = "C Learner"
    let age int = 25
    print("Hello,", name)
    print("Age:", age)
}
```

```c
#include <stdio.h>

int main(void) {
    char* name = "C Learner";
    int age = 25;
    printf("%s %s\n", "Hello,", name);
    printf("%s %d\n", "Age:", age);
    return 0;
}
```

<Listing name="first-program" file="listings/ch00/listing-00-02">

```auto
fn main() {
    let name str = "C Learner"
    let age int = 25
    print("Hello,", name)
    print("Age:", age)
}
```

</Listing>

Auto 消除了样板代码：不需要 `#include`、不需要分号、不需要显式的 `return 0;`、
不需要 `print` 中的格式说明符。

## 5. 头文件与预处理器

在 C 中，你使用 `#include` 引入头文件，使用 `#define` 定义宏。C 预处理器在编译之前
运行，执行文本替换。

Auto 没有预处理器。Auto 使用模块系统：

- `mod` 声明模块。
- `use` 从另一个模块导入符号。
- a2c 转译器会自动添加正确的 `#include` 指令。

例如，在 Auto 中使用 `print` 会自动在生成的 C 中包含 `<stdio.h>`。

> **仅 C**：C 的预处理器支持条件编译（`#ifdef`）、token 粘合（`##`）和可变参数宏。
> Auto 没有对应功能——这些是低层机制，很少需要使用。

## 6. 编译与链接

在传统 C 开发中，你需要分别运行预处理器、编译器、汇编器和链接器，或通过 Makefile
完成。使用 Auto，工作流更简单：

```console
$ auto a2c main.at        # 将 Auto 转译为 C
$ auto b                   # 构建：转译 + 编译 + 链接
```

`auto a2c` 命令生成 `.c` 文件。`auto b` 命令运行完整流程：转译、使用系统 C 编译器
编译，并链接为可执行文件。

## 7. 错误与警告

Auto 提供两层错误报告：

1. **Auto 编译器错误** — 在转译之前捕获。包括类型错误、未定义变量和语法问题。
   Auto 的错误消息会精确指向 `.at` 源文件中的位置。

2. **C 编译器错误** — 在转译之后、生成的 `.c` 文件中捕获。对于格式正确的 Auto
   程序来说很罕见，但可能在平台特定问题上出现。

当你看到 C 编译器错误时，a2c 转译器会在生成的 C 中添加 `// line X: main.at` 注释，
以便追溯到你 Auto 源代码。

## 8. `auto` 命令行

`auto` CLI 提供多个命令：

| 命令 | 用途 |
|------|------|
| `auto a2c file.at` | 将 Auto 转译为 C |
| `auto b` | 构建项目（转译 + 编译 + 链接）|
| `auto r` | 构建并运行 |
| `auto t` | 运行测试 |
| `auto new name` | 创建新项目 |
| `auto fmt` | 格式化源文件 |
| `auto check` | 类型检查（不生成代码）|

## 9. 项目结构

一个典型的以 C 为目标的 Auto 项目结构如下：

```
my-project/
├── pac.at           # 包配置
├── src/
│   └── main.at      # 入口点
└── out/
    └── main.c       # 由 a2c 生成
```

`pac.at` 文件声明项目名称、版本和目标语言：

```
name: "my-project"
version: "0.1.0"
lang: "c"

app("my-project") {}
```

<Listing name="project-with-pac" file="listings/ch00/listing-00-03">

```auto
fn greet(name str) {
    print("Hello,", name)
}

fn main() {
    greet("C Learner")
    greet("Auto Developer")
}
```

</Listing>

运行 `auto b` 会读取 `pac.at`，将所有 `.at` 文件转译为 `.c`，使用系统 C 编译器
编译，并生成最终的可执行文件。

## 快速参考

| 概念 | Auto | C |
|------|------|---|
| 入口点 | `fn main()` | `int main(void)` |
| 打印 | `print("text")` | `printf("%s\n", "text")` |
| 包含 | 自动 | `#include <stdio.h>` |
| 不可变变量 | `let x int = 5` | `const int x = 5;` |
| 可变变量 | `var x int = 5` | `int x = 5;` |
| 构建命令 | `auto b` | `gcc -o out main.c` |
| 包配置 | `pac.at` | `Makefile` / `CMakeLists.txt` |
| 模块 | `mod` / `use` | `#include` |
