# 入门

本章让你开始运行程序。我们从 *Modern C* 的第一个程序开始，适配到 Auto，然后逐步讲解如何在两种语言中编译和执行。

## 1.1 命令式编程

C 是一门命令式语言。你编写一系列语句，计算机按顺序执行：赋值、计算、输出、重复。没有魔法——程序严格按你说的做，一步一步来。

Auto 也是命令式的。相同的顺序模型同样适用。区别在于表面语法：Auto 去除了 C 要求的样板代码，同时保留了执行模型。

### 第一个程序

看看 *Modern C* 的第一个程序。它创建一个包含五个浮点数的数组，遍历它们，打印每个值及其平方：

<Listing name="第一个程序" file="listings/ch01/listing-01-01">

这个程序的 C 版本如下：

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    double A[5] = {9.0, 2.9, 0.0, 0.00007, 3e+25};
    for (size_t i = 0; i < 5; ++i) {
        double val = A[i];
        double sq = val * val;
        printf("element %zu is %g, square is %g\n", i, val, sq);
    }
    return EXIT_SUCCESS;
}
```

运行这个程序，你会看到：

```
element 0 is 9, square is 81
element 1 is 2.9, square is 8.41
element 2 is 0, square is 0
element 3 is 7e-05, square is 4.9e-09
element 4 is 3e+25, square is 9e+50
```

### 对比两个版本

让我们逐行比较关键差异：

**数组声明。** C 使用 `double A[5] = {...}`。Auto 使用 `let A [5]float = [5]float{...}`。类型放在名称之后，`float` 映射到 C 的 `double` 以保证浮点精度。

**For 循环。** C 要求 `for (size_t i = 0; i < 5; ++i)`，需要显式的初始化、条件和递增。Auto 使用 `for i in 0..5`——基于范围的形式，等价但更简洁。

**打印。** C 使用带格式说明符（`%zu`、`%g`）的 `printf`。Auto 使用 `print(...)`，自动处理格式化。a2c 转译器生成正确的 `printf` 调用和相应的格式说明符。

**返回。** C 要求在 `main` 末尾写 `return EXIT_SUCCESS;`（或 `return 0;`）。Auto 的 `fn main()` 不需要显式返回——a2c 自动插入 `return 0;`。

### "命令式"到底是什么意思

"命令式"这个词来自拉丁语 *imperare*，意为"命令"。在命令式程序中，你发出命令：

- **赋值**一个值给变量。
- **计算**一个表达式并存储结果。
- **调用**一个函数执行操作。
- **重复**一段代码直到满足条件。

C 和 Auto 都遵循这个模型。函数体中的语句从上到下依次执行。控制流构造（`if`、`for`、`while`）修改这个顺序，但基本模型是顺序执行。

### 本示例中的现代 C 关键概念

这第一个程序已经展示了几个现代 C 原则：

1. **带显式大小的数组。** `[5]float` 在类型中明确指定大小。现代 C 风格更偏好这种方式而非隐式大小数组，因为它能防止缓冲区溢出。

2. **浮点精度。** Auto 的 `float` 类型映射到 C 的 `double`，不是 `float`。这是有意为之：单精度 `float` 很少是数值计算的正确默认选择。现代 C 提出了相同的建议。

3. **结构化输出。** `print` 语句接受多个参数并自动格式化。C 的 `printf` 要求你手动匹配格式说明符和参数类型。Auto 消除了这个容易出错的步骤。

4. **无全局状态。** 所有内容都是 `main` 的局部变量。这在两种语言中都是好实践：尽量减少全局变量。

> **C 深潜：** 现代 C 建议用 `size_t` 作为索引数组的循环计数器，因为 `size_t` 保证能容纳任何有效的数组索引。`size_t` 类型在 `<stddef.h>`（以及其他几个头文件）中定义为无符号整数类型。a2c 转译器为简化起见在基于范围的循环中使用 `int`，但直接写 C 时这个原则值得记住。使用有符号类型如 `int` 作为数组索引，在与 `size_t` 值（如 `sizeof` 的结果）比较时可能产生警告。

> **要点：** 命令式编程是有序的语句序列。Auto 和 C 共享这个模型——区别在于语法，而非语义。

## 1.2 编译和运行

要运行上面的程序，你需要编译它。C 和 Auto 的工作流有所不同。

### C 工作流

在 C 中，你编写 `.c` 文件并调用编译器：

```bash
# 使用 gcc
gcc -o listing-01-01 listing-01-01.c
./listing-01-01

# 使用 clang
clang -o listing-01-01 listing-01-01.c
./listing-01-01
```

Modern C 建议编译时启用警告并使用最新标准：

```bash
gcc -std=c17 -Wall -Wextra -o listing-01-01 listing-01-01.c
```

`-std=c17` 标志选择 C17 标准。`-Wall -Wextra` 标志启用大多数有用的警告。在现代 C 实践中，带警告编译不是可选的——它能捕获真正的 bug。

### Auto 工作流

在 Auto 中，你使用 a2c 转译器然后构建：

```bash
auto a2c      # 将所有 .at 文件转译为 .c
auto b        # 构建：编译生成的 C 代码
```

两步过程分离了关注点：a2c 处理 Auto 到 C 的翻译，C 编译器处理优化和代码生成。你永远不会失去对中间 C 代码的可见性。

<Listing name="编译和运行" file="listings/ch01/listing-01-02">

上面的 Listing 是一个更简单的程序。让我们追踪发生的过程：

1. `auto a2c` 读取 `main.at` 并生成 `main.c`。
2. `auto b` 对 `main.c` 调用 C 编译器并生成可执行文件。
3. 你运行可执行文件，看到输出：

```
Modern C meets Auto!
The answer is 42
```

### a2c 生成了什么

转译器生成干净、可读的 C 代码。对于 `listing-01-02`，输出如下：

```c
// Auto → C transpiled by a2c
#include <stdio.h>

int main(void) {
    printf("%s\n", "Modern C meets Auto!");
    int answer = 42;
    printf("%s %d\n", "The answer is", answer);
    return 0;
}
```

注意这些细节：

- `// Auto → C transpiled by a2c` 头部标识该文件是生成的。
- `#include <stdio.h>` 因为程序使用了 `print` 而自动添加。
- `print("text")` 变成 `printf("%s\n", "text")`——换行符已包含。
- `print("label", x)` 变成 `printf("%s %d\n", "label", x)`——格式说明符根据参数类型推断。
- `int main(void)` 和 `return 0;` 从 `fn main()` 生成。

### 实践中的完整管线

完整的开发周期如下：

```bash
# 1. 编写你的 Auto 程序
$ cat main.at
fn main() {
    print("Modern C meets Auto!")
    let answer int = 42
    print("The answer is", answer)
}

# 2. 转译为 C
$ auto a2c

# 3. 检查生成的 C（可选但推荐）
$ cat main.c
// Auto → C transpiled by a2c
...

# 4. 构建并运行
$ auto b
$ ./listing-01-02
Modern C meets Auto!
The answer is 42
```

> **C 深潜：** C 的 `printf` 函数是可变参数的——它在格式字符串之后接受任意数量的参数。格式字符串必须与参数类型匹配：`%d` 对应 `int`，`%f` 对应 `double`，`%s` 对应 `char*`，`%zu` 对应 `size_t`。不匹配会导致未定义行为。Auto 的 `print` 通过自动生成正确的格式字符串消除了这类 bug。

> **要点：** a2c 转译器在 Auto 的简洁语法和 C 的显式控制之间架起桥梁。每个 Auto 构造映射到特定的 C 模式。

### 错误消息和调试

当出错时，错误可能来自两个地方：

1. **a2c 错误** -- Auto 代码中的语法错误。这些错误会报告文件和行号，就像编译器一样。
2. **C 编译器错误** -- 生成的 C 中的错误。如果 a2c 工作正常，这种情况很少见，但在边界情况下可能发生。

当遇到 C 编译器错误时，查看生成的 `.c` 文件。错误消息中的行号指的是 C 文件，不是 Auto 文件。与你的 Auto 源码交叉引用以找到对应行。

常见的调试工作流：

```bash
# 如果 auto a2c 成功但 auto b 失败：
$ auto a2c
$ cat main.c           # 检查生成的 C 代码
$ gcc -c main.c        # 尝试手动编译以获得更好的错误消息
```

## 快速参考

| 概念 | C | Auto |
|---|---|---|
| 主函数 | `int main(void) { ... return 0; }` | `fn main() { }` |
| 包含头文件 | `#include <stdio.h>` | （自动） |
| 变量 | `double x = 1.5;` | `let x float = 1.5` |
| 数组 | `double A[5] = {1,2,3,4,5};` | `let A [5]float = [5]float{1,2,3,4,5}` |
| For 循环 | `for (int i = 0; i < n; i++)` | `for i in 0..n` |
| 打印 | `printf("x = %d\n", x);` | `print("x =", x)` |
| 编译 | `gcc -o prog prog.c` | `auto a2c && auto b` |
| 成功退出 | `return EXIT_SUCCESS;` | （隐式） |
| 警告 | `-Wall -Wextra` | （内置在 `auto b` 中） |
