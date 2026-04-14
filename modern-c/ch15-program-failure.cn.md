# 第十五章：程序失败

> 级别 2 — 认知
>
> 未定义行为、错误码、信号——C 中如何出错以及 Auto 如何防止它们。

程序会失败。问题不在于失败是否会发生，而在于语言如何帮助你预防、检测和恢复。C 的失败处理方法是最小化的：语言假设程序员总是正确的，并且很少提供安全网。Auto 采取相反的方法——语言通过编译时检查和运行时安全帮助程序员避免失败。

---

## 15.1 不当行为

C 将程序错误行为分为几个类别。最危险的是**未定义行为**（UB）：

> 未定义行为：标准不对其施加任何要求的行为。

UB 意味着编译器被允许做任何事情。常见示例：

```c
// C 深入：未定义行为
int arr[5];
arr[10] = 42;           // UB：越界访问

int *p = NULL;
*p = 42;                // UB：空指针解引用

int x;
printf("%d\n", x);      // UB：读取未初始化变量

int a = INT_MAX;
int b = a + 1;          // UB：有符号整数溢出

free(p);
*p = 42;                // UB：释放后使用
```

UB 在实践中实际发生的情况：

| 场景              | 可能的后果                      |
|-------------------|---------------------------------|
| 缓冲区溢出       | 静默数据损坏                    |
| 空指针解引用     | 段错误（崩溃）                  |
| 释放后使用       | 任意代码执行                    |
| 整数溢出         | 不正确的结果                    |
| 类型混淆         | 数据损坏，安全漏洞              |

编译器利用 UB 进行优化。如果标准说行为未定义，编译器可以假设它永远不会发生：

```c
// C 深入：编译器利用 UB
int *check(int *p) {
    int x = *p;        // 解引用 p
    if (p == NULL) {   // 编译器移除此检查：如果 p 是 NULL，
        return NULL;   // 上面的解引用就是 UB，
    }                   // 而 UB "不会发生"
    return p;
}
```

**Auto 如何防止 UB。** Auto 通过以下方式消除整类 UB：

- **边界检查**：数组访问在可能时在编译时验证，在必要时在运行时验证。
- **空值安全**：Auto 中没有空指针。可选值使用显式 `Option` 类型。
- **初始化强制**：每个变量必须初始化。
- **无指针算术**：数组索引替代所有指针算术。
- **溢出检测**：整数溢出在运行时被捕获。

```auto
// Auto：UB 预防
fn safe_divide(a int, b int) int {
    if b == 0 {
        print("Error: division by zero")
        return 0
    }
    a / b
}

fn safe_access(arr [5]int, index int) int {
    if index < 0 || index >= 5 {
        print("Error: index out of bounds")
        return 0
    }
    arr[index]
}
```

<Listing path="listings/ch15/listing-15-01" title="错误处理" />

> **C 深入：** C/C++ 代码中大约 60% 的 CVE（常见漏洞和暴露）是由作为未定义行为的内存安全违规引起的。这是 Rust、Swift 和 Auto 等语言的主要动机。

---

## 15.2 程序状态退化

C 区分几个级别的不确定行为：

**实现定义行为**：编译器必须文档化其行为。

```c
// C 深入：实现定义行为
int x = -1;
int y = x >> 1;   // 算术右移还是逻辑右移？
// 实现定义：可能是 -1（算术）或 INT_MAX（逻辑）
```

**未指定行为**：标准允许多种有效结果。

```c
// C 深入：未指定行为
int f(void) { printf("f\n"); return 1; }
int g(void) { printf("g\n"); return 2; }
int result = f() + g();   // 可能输出 "f g" 或 "g f"
// 操作数的求值顺序是未指定的
```

**区域设置相关行为**：取决于运行时区域设置。

```c
// C 深入：区域设置相关行为
printf("%d\n", isalpha(0xE9));  // 取决于区域设置：带锐音符的 e？
```

这些不如 UB 危险，但它们使程序在不同编译器、平台和配置上的行为不同——可移植性的噩梦。

**Auto 的方法。** Auto 指定求值顺序（从左到右），提供平台无关的整数语义，并普遍使用 UTF-8。程序在每个平台上的行为相同：

```auto
// Auto：确定性行为
fn f() int { print("f"); 1 }
fn g() int { print("g"); 2 }
fn main() {
    let result int = f() + g()   // 始终先输出 "f" 再输出 "g"
    print("Result:", result)
}
```

> **C 深入：** C 中未指定的求值顺序是微妙缺陷的常见来源。像 `a[i] = i++` 这样的代码是 UB（在没有序列点的情况下修改和读取 `i`）。甚至 `printf("%d %d", i++, i)` 也是 UB。Auto 通过具有清晰的求值顺序完全消除了序列点的顾虑。

---

## 15.3 不幸事件

运行时错误发生在程序遇到意外条件时：

```c
// C 深入：运行时错误
int *p = malloc(1000000000000);  // 可能返回 NULL
int x = 1 / 0;                   // 浮点异常（信号）
int arr[3]; arr[10];             // 可能崩溃也可能不崩溃（UB）

// 栈溢出
void recurse(void) { recurse(); }  // 无限递归 -> 崩溃
```

C 通过**信号**处理这些情况——来自操作系统的异步通知：

```c
// C 深入：信号
#include <signal.h>

void handler(int sig) {
    if (sig == SIGSEGV) {
        fprintf(stderr, "Segmentation fault\n");
        _exit(1);
    }
}

int main(void) {
    signal(SIGSEGV, handler);
    // ...
}
```

标准信号：

| 信号       | 原因                        | 默认动作       |
|-----------|------------------------------|---------------|
| `SIGABRT` | 调用了 `abort()`            | 终止          |
| `SIGFPE`  | 算术错误                     | 终止          |
| `SIGILL`  | 非法指令                     | 终止          |
| `SIGINT`  | 终端 Ctrl+C                  | 终止          |
| `SIGSEGV` | 无效内存访问                  | 终止          |
| `SIGTERM` | 终止请求                     | 终止          |

C 中的信号处理极其有限。只能从信号处理程序中调用异步信号安全函数。`printf`、`malloc` 和大多数库函数都不是异步信号安全的。

**Auto 的方法。** Auto 通过防止信号的触发来避免信号：

- 没有空指针意味着不会从空指针解引用产生 `SIGSEGV`。
- 边界检查意味着不会从缓冲区溢出产生 `SIGSEGV`。
- 运行时检查在硬件异常之前捕获除零。

> **C 深入：** 编写正确的信号处理程序是 C 编程中最难的任务之一。信号可能在任何时候到达，甚至在指令执行中间。生产代码中的大多数"信号处理程序"在技术上都是未定义行为。最安全的方法是设置一个 `volatile sig_atomic_t` 标志并在主循环中检查它。

---

## 15.4 连环不幸事件

C 中的失败倾向于级联。一个小错误在程序中传播，导致越来越严重的症状：

```c
// C 深入：级联失败
char* read_file(const char *path) {
    FILE *f = fopen(path, "r");    // 可能返回 NULL
    // 忘记检查！
    char *buf = malloc(1024);      // 可能返回 NULL
    // 忘记检查！
    fgets(buf, 1024, f);           // 如果 f 是 NULL，UB
    return buf;                    // 调用者必须 free——他们会吗？
}

void process(void) {
    char *data = read_file("input.txt");  // 可能是 NULL
    int len = strlen(data);               // 如果 data 是 NULL，UB
    printf("Length: %d\n", len);
    // 忘记 free(data)！内存泄漏
}
```

每个缺失的错误检查都在累积。在实际代码中，这导致：

1. 一个 NULL 指针静默地通过多个函数传播。
2. 最终它被解引用，导致远离根因的崩溃。
3. 崩溃报告显示的是症状，不是原因。
4. 调试需要沿调用链回溯。

**Auto 的方法：快速失败，清晰失败。** Auto 的哲学是尽早检测错误并使其不可能被忽略：

```auto
// Auto：显式错误处理
type Result {
    value int
    ok bool
}

fn Result.ok(val int) Result {
    Result(val, true)
}

fn Result.err() Result {
    Result(0, false)
}

fn process(data int) Result {
    if data < 0 {
        print("Invalid input:", data)
        return Result.err()
    }
    Result.ok(data * 2)
}
```

<Listing path="listings/ch15/listing-15-02" title="错误检查与清理" />

> **C 深入：** 对生产 C 代码的研究表明，错误处理代码通常比正常路径包含更多缺陷。原因很简单：错误路径很少被测试，并且手动的 `if (error) goto cleanup` 模式既繁琐又容易出错。Auto 的 `Result` 类型强制程序员在每个调用点处理错误。

---

## 15.5 处理失败

C 的主要错误报告机制是**错误码**：

```c
// C 深入：错误码
#include <errno.h>

errno = 0;
FILE *f = fopen("missing.txt", "r");
if (f == NULL) {
    // errno 由 fopen 设置
    fprintf(stderr, "Error %d: %s\n", errno, strerror(errno));
}
```

`errno` 的问题：

- **成功调用不会将其清零**：必须在调用函数之前清除 `errno` 才能可靠地检测错误。
- **全局状态**：在旧 C 标准中不是线程安全的。C11 添加了线程本地存储，`errno` 现在通常是线程本地的。
- **单一值**：一次只有一个错误；嵌套调用会覆盖它。
- **无类型安全**：任何 `int` 值都是有效的 errno。

`perror` 函数提供方便的错误消息：

```c
// C 深入：perror
FILE *f = fopen("config.txt", "r");
if (!f) {
    perror("fopen");    // 输出 "fopen: No such file or directory"
    return 1;
}
```

**Auto 的方法：`Result` 类型。** Auto 使用 `Result` 类型（类似于 Rust 的 `Result` 和 Zig 的错误联合）处理可失败的操作：

```auto
// Auto：用于错误处理的 Result 类型
type Result {
    value int
    ok bool
}

fn Result.ok(val int) Result {
    Result(val, true)
}

fn Result.err() Result {
    Result(0, false)
}
```

调用者必须在使用 `value` 之前检查 `ok` 字段。忽略可失败函数的结果是编译时警告。

> **C 深入：** Go 使用多返回值 `(value, error)` 进行错误处理。Rust 使用 `Result<T, E>` 和 `?` 运算符。Zig 使用带 `try` 的错误联合。C 使用 `errno` 和返回码。每种方法都有权衡。Auto 的 `Result` 类型汲取了这些设计的精华。

---

## 15.6 错误检查与清理

C 的资源清理是手动且容易出错的。标准模式使用 `goto` 进行集中清理：

```c
// C 深入：使用 goto 清理
int process_file(const char *path) {
    FILE *f = NULL;
    char *buf = NULL;
    int result = -1;

    f = fopen(path, "r");
    if (!f) goto cleanup;

    buf = malloc(4096);
    if (!buf) goto cleanup;

    if (!fgets(buf, 4096, f)) goto cleanup;

    // 处理 buf...
    result = 0;

cleanup:
    if (buf) free(buf);
    if (f) fclose(f);
    return result;
}
```

这个模式如此常见，以至于出现在 Linux 内核、PostgreSQL 和大多数大型 C 代码库中。它能工作，但很脆弱：

- 在清理块中忘记释放资源会泄漏它。
- 添加新资源需要更新所有清理代码。
- `goto` 必须只向前跳转；向后跳转会创建循环。
- 资源必须按获取的相反顺序释放。

一些 C 编译器支持清理属性：

```c
// C 深入：自动清理（GCC/Clang 扩展）
void cleanup_file(FILE **f) { if (*f) fclose(*f); }

int read_data(void) {
    FILE *f __attribute__((cleanup(cleanup_file))) = fopen("data.txt", "r");
    if (!f) return -1;
    // f 在作用域结束时自动关闭
    return 0;
}
```

**Auto 的方法：自动清理。** Auto 通过其存储模型自动管理资源清理。资源在超出作用域时被释放。程序员永远不需要编写清理代码：

```auto
// Auto：自动清理，不需要 goto
fn process(data int) Result {
    if data < 0 {
        print("Invalid input:", data)
        return Result.err()
    }
    Result.ok(data * 2)
}

fn main() {
    let r1 Result = process(21)
    if r1.ok {
        print("Success:", r1.value)
    }

    let r2 Result = process(-5)
    if !r2.ok {
        print("Processing failed")
    }
}
```

> **C 深入：** `defer` 语句由 Go 推广并被 Zig 采用，是清理问题的现代解决方案。它安排一个清理动作在函数返回时运行。C2x 考虑但未添加 `defer`。Auto 的自动存储管理无需显式 `defer` 语句即可达到相同效果。

---

## 快速参考

| 概念                | C 机制                      | Auto 机制                  |
|--------------------|-----------------------------|----------------------------|
| 未定义行为         | "程序员总是正确的"           | 设计预防                   |
| 缓冲区溢出         | UB，常被利用                 | 边界检查                   |
| 空指针解引用       | UB，崩溃或被利用             | 没有空指针                 |
| 未初始化读取       | UB，垃圾值                   | 强制初始化                 |
| 整数溢出           | UB（有符号）                 | 运行时检测                 |
| 错误报告           | `errno`、返回码              | `Result` 类型              |
| 错误检查           | 手动 `if` 检查              | `Result.ok` 字段           |
| 资源清理           | `goto cleanup` 或 RAII      | 自动                       |
| 信号处理           | `signal()`，有限             | 从源头预防                 |
| 级联失败           | 常见                         | 类型系统控制               |

---

*这完成了级别 2 — 认知。你现在理解了 C 程序如何失败以及 Auto 的设计如何防止最常见的失败模式。从级别 2 到级别 3 的过渡标志着从理解 C 内部机制到使用 Auto 抽象构建真实程序的转变。*
