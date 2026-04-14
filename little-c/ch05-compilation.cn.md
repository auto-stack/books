# 编译与构建过程

本章介绍 Auto 代码如何变为可执行文件。你将学习编译流水线、Auto 如何替代 C 预处理器，
以及 `pac.at` 和 `auto b` 如何替代 Makefile 管理多文件项目。

## 51. 编译流水线

C 编译有四个阶段：

1. **预处理** —— 展开 `#include`、`#define`、`#ifdef`
2. **编译** —— 将 C 源码转换为汇编
3. **汇编** —— 将汇编转换为目标代码（`.o` 文件）
4. **链接** —— 将目标文件和库组合为可执行文件

Auto 在此流水线之前增加了一个转译步骤：

```
auto.at → [a2c 转译器] → auto.c → [cc 编译器] → auto.o → [链接器] → auto
```

`a2c` 转译器将 Auto 源码转换为 C 源码。然后标准的 C 编译器（gcc、clang 或 msvc）
接管后续流程。

<Listing name="compilation-pipeline" file="listings/ch05/listing-05-01">

```auto
fn square(n int) int {
    n * n
}

fn main() {
    let result int = square(7)
    print("7 squared =", result)
}
```

</Listing>

对此文件运行 `auto b` 会依次调用 a2c、cc 和链接器。结果是一个不依赖 Auto 运行时的
原生可执行文件。

## 52. 预处理器与宏

C 使用预处理器定义常量和宏函数：

```c
#define PI 3.14159
#define MAX(a, b) ((a) > (b) ? (a) : (b))
```

宏是文本替换——没有类型检查、没有作用域，还存在多重求值的微妙 bug。Auto 完全
消除了预处理器：

<Listing name="preprocessor" file="listings/ch05/listing-05-02">

```auto
fn main() {
    // C uses #define PI 3.14159
    // Auto uses let (immutable binding)
    let pi float = 3.14159
    let radius float = 5.0
    let area float = pi * radius * radius
    print("Area:", area)

    // C uses #define MAX(a,b) ((a)>(b)?(a):(b))
    // Auto uses a regular function
    let larger int = max(10, 20)
    print("Max:", larger)
}

fn max(a int, b int) int {
    if a > b { a } else { b }
}
```

</Listing>

Auto 的 `let` 创建不可变绑定（类似 C 的 `const`）。`max` 函数是类型安全的，
且只求值一次。编译器可能会内联它以获得与宏相当的性能，但没有宏的危险。

## 53. 条件编译

C 使用 `#ifdef` 处理平台特定代码：

```c
#ifdef _WIN32
    #include <windows.h>
#else
    #include <unistd.h>
#endif
```

Auto 没有条件编译。相反，为不同平台使用不同的源文件，通过 `pac.at` 配置在
构建时选择正确的文件。这使得每个文件都完整且可读。

对于构建时配置，Auto 支持 `comptime` 块在转译期间求值常量，但这是高级话题，
超出了本章范围。

## 54. 内联函数

C 的 `inline` 关键字建议编译器将函数体复制到调用点：

```c
static inline int square(int x) { return x * x; }
```

Auto 没有 `inline` 关键字。a2c 转译器和 C 编译器协同决定内联。像 `max` 这样
的小函数自动成为内联候选。你可以在 `pac.at` 中通过注解提示优先级：

```
optimize: "speed"   // 偏好更快代码，更多内联
optimize: "size"    // 偏好更小代码，更少内联
```

## 55. Makefile 与 pac.at

C 项目使用 Makefile 定义构建规则：

```makefile
CC = gcc
CFLAGS = -Wall -O2

main: main.o utils.o
	$(CC) $(CFLAGS) -o main main.o utils.o

main.o: main.c
	$(CC) $(CFLAGS) -c main.c
```

Auto 用 `pac.at`——一个声明式项目文件——替代 Makefile。你声明构建什么，而不是
如何构建：

<Listing name="makefile" file="listings/ch05/listing-05-03">

```auto
fn greet(name str) {
    print("Hello,", name)
}

fn farewell(name str) {
    print("Goodbye,", name)
}

fn main() {
    greet("World")
    farewell("World")
}
```

</Listing>

`pac.at` 文件列出应用及其依赖。运行 `auto b` 读取 `pac.at`，将所有 `.at` 文件
转译为 `.c`，编译它们，并链接结果。无需编写规则，无需跟踪时间戳。

## 56. 多文件项目

C 将代码分散在 `.c` 和 `.h` 文件中。头文件声明类型和函数；源文件定义它们。
你必须保持头文件和源文件同步。

Auto 使用 `mod` 和 `use` 组织代码，无需头文件：

<Listing name="multi-file" file="listings/ch05/listing-05-04">

```auto
// math_utils.at
// mod math_utils

fn add(a int, b int) int {
    a + b
}

fn multiply(a int, b int) int {
    a * b
}

// main.at
// use math_utils

fn main() {
    let sum int = add(3, 4)
    let product int = multiply(3, 4)
    print("Sum:", sum)
    print("Product:", product)
}
```

</Listing>

`mod math_utils` 声明创建一个模块。`use math_utils` 声明导入它。a2c 转译器
自动生成对应的 `.h` 和 `.c` 文件，保持声明和定义始终同步。

## 57. 静态库与共享库

C 将库构建为归档文件（`.a` 静态）或共享对象（`.so` / `.dll`）：

```bash
ar rcs libmath.a math.o       # 静态库
gcc -shared -o libmath.so math.o  # 共享库
```

Auto 的 `auto b` 命令通过 `pac.at` 配置处理库创建：

```
lib("math_utils") {
    src: ["math_utils.at"]
    type: "static"    # 或 "shared"
}
```

当你在 `pac.at` 中声明一个库时，`auto b` 转译 Auto 源文件，编译它们，并归档。
其他模块通过将库列为依赖来链接。你永远不需要手动运行 `ar` 或 `ld`。

## 58. 编译器标志

C 项目向编译器传递标志：

```bash
gcc -Wall -Wextra -O2 -std=c11 -o program main.c
```

Auto 在 `pac.at` 中设置合理的默认值：

| 标志 | 用途 | Auto 默认值 |
|------|------|------------|
| `-Wall -Wextra` | 启用警告 | 是 |
| `-O2` | 优化级别 | 是 |
| `-std=c11` | C 标准 | C11 |
| `-g` | 调试符号 | Debug 构建 |
| `-DNDEBUG` | 禁用断言 | Release 构建 |

在 `pac.at` 中覆盖默认值：

```
app("myapp") {
    cflags: ["-O3", "-march=native"]
}
```

## 59. 目标文件

每个 `.c` 文件编译为一个目标文件（Linux/macOS 上为 `.o`，Windows 上为 `.obj`）。
目标文件包含带有未解析符号的机器代码。链接器通过组合目标文件来解析符号。

当 `auto b` 在多文件项目上运行时：

```
math_utils.at → math_utils.c → math_utils.o ─┐
                                               ├→ 链接器 → myapp
main.at       → main.c       → main.o       ─┘
```

每个 Auto 源文件生成恰好一个 `.c` 文件，后者生成一个 `.o` 文件。链接器将它们
组合为最终的可执行文件。理解这个流程有助于调试"undefined reference to `foo`"
之类的链接错误——这意味着链接器找不到定义 `foo` 的目标文件。

## 60. 练习：构建多文件项目

构建一个小型项目，包含一个计数器模块和主程序。本练习涵盖模块创建、构建过程
和链接。

<Listing name="libraries" file="listings/ch05/listing-05-05">

```auto
type Counter {
    count int
}

fn Counter.new() Counter {
    Counter(0)
}

fn Counter.increment(c Counter) {
    c.count = c.count + 1
}

fn Counter.value(c Counter) int {
    c.count
}

fn main() {
    var c Counter = Counter.new()
    c.increment(c)
    c.increment(c)
    c.increment(c)
    print("Count:", c.value(c))
}
```

</Listing>

尝试以下操作：将 `Counter` 类型拆分到自己的文件 `counter.at` 中，使用
`mod counter`，创建一个列出两个文件的 `pac.at`，然后运行 `auto b` 构建项目。
验证 a2c 生成了 `counter.h`、`counter.c`、`main.c` 并正确链接了它们。

## 快速参考

| 概念 | Auto | C |
|------|------|---|
| 转译 | `a2c main.at` | N/A |
| 构建 | `auto b` | `make` |
| 项目文件 | `pac.at` | `Makefile` |
| 常量 | `let pi float = 3.14` | `#define PI 3.14` |
| 宏函数 | `fn max(a, b) int` | `#define MAX(a,b) ...` |
| 条件编译 | 独立源文件 | `#ifdef` |
| 模块声明 | `mod math_utils` | `math_utils.h` + `math_utils.c` |
| 模块导入 | `use math_utils` | `#include "math_utils.h"` |
| 静态库 | `lib("name") { type: "static" }` | `ar rcs libname.a` |
| 共享库 | `lib("name") { type: "shared" }` | `gcc -shared` |
| 编译器标志 | `pac.at` cflags 字段 | Makefile 中的 `CFLAGS` |
| 优化 | `optimize: "speed"` | `-O2` / `-O3` |
