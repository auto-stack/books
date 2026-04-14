# 第十九章：控制流变体

> 级别 3 -- 经验
>
> 非局部跳转、信号和结构化错误处理——理解 C 的控制流逃逸机制以及 Auto 如何用更安全的模式替代它们。

程序并不总是遵循直线路径。函数提前返回、循环跳出、错误通过调用栈传播。C 提供了几种非标准控制流机制：`goto`、`setjmp`/`longjmp` 和信号处理器。这些功能强大但危险。Auto 用结构化的替代方案取代了其中的大部分。

---

## 19.1 详细示例

考虑一个必须在多个层面处理错误的解析器：

```c
// C 深入：使用 goto 进行错误处理
#include <stdio.h>
#include <stdlib.h>

int parse_input(const char *input) {
    if (!input) goto error_null;
    if (*input == '\0') goto error_empty;

    int value = atoi(input);
    if (value <= 0) goto error_negative;

    printf("Parsed: %d\n", value);
    return value;

error_null:
    fprintf(stderr, "Error: null input\n");
    return -1;
error_empty:
    fprintf(stderr, "Error: empty input\n");
    return -2;
error_negative:
    fprintf(stderr, "Error: non-positive value\n");
    return -3;
}
```

C 程序员使用 `goto` 进行集中式错误清理。这是 C 中少数被接受的 `goto` 用法之一。模式是：跳转到一个释放资源并报告错误的标签。

**Auto 的方法。** Auto 使用 Result 类型进行错误传播：

```auto
// Auto：使用 Result 类型进行结构化错误处理
type ParseResult {
    value int
    ok bool
    error str
}

fn ParseResult.ok(val int) ParseResult {
    ParseResult(val, true, "")
}

fn ParseResult.err(msg str) ParseResult {
    ParseResult(0, false, msg)
}

fn parse_input(input str) ParseResult {
    if input == "" {
        return ParseResult.err("empty input")
    }
    let value int = int(input)
    if value <= 0 {
        return ParseResult.err("non-positive value")
    }
    ParseResult.ok(value)
}
```

<Listing path="listings/ch19/listing-19-01" title="setjmp/longjmp 到错误处理" />

---

## 19.2 顺序求值

C 中的逗号运算符从左到右求值操作数，并产生最后一个值：

```c
// C 深入：逗号运算符
int x = (1, 2, 3);     // x == 3
int y = (printf("a"), printf("b"), 42);  // 打印 "ab"，y == 42

// 常见用法：带多个递增的 for 循环
for (int i = 0, j = 10; i < j; i++, j--) {
    printf("i=%d j=%d\n", i, j);
}
```

逗号运算符是一个顺序点。左操作数在右操作数开始之前被完全求值。然而，分隔函数参数的逗号**不是**逗号运算符——它是标点符号。

> **C 深入：** C 中函数参数的求值顺序是未指定的。`f(a(), b())` 可能先调用 `a()` 也可能先调用 `b()`。这与逗号运算符不同，后者保证从左到右求值。混淆这两个概念是常见的错误来源。

**Auto 的方法。** Auto 没有逗号运算符。`for` 循环使用范围语法，函数参数以确定的顺序求值：

```auto
// Auto：不需要逗号运算符
fn main() {
    for i in 0..10 {
        print(i)
    }
}
```

这是一个 **C 独有**的特性。Auto 的设计消除了这种歧义。

---

## 19.3 短跳转

C 提供了几种短距离控制流转移机制：

```c
// C 深入：短跳转
for (int i = 0; i < 100; i++) {
    if (i == 5) continue;    // 跳到下一次迭代
    if (i == 10) break;      // 退出循环
    printf("%d ", i);
}
// 输出：0 1 2 3 4 6 7 8 9
```

`goto` 语句将控制转移到同一函数内的标签语句：

```c
// C 深入：使用 goto 进行清理
#include <stdio.h>
#include <stdlib.h>

int process(void) {
    FILE *f = fopen("data.txt", "r");
    if (!f) goto cleanup_none;

    char *buf = malloc(1024);
    if (!buf) goto cleanup_file;

    // ... 使用 f 和 buf 工作 ...

    free(buf);
    fclose(f);
    return 0;

cleanup_file:
    fclose(f);
cleanup_none:
    return -1;
}
```

> **C 深入：** `goto` 不能跨越函数边界跳转。不能跳过变长数组声明。不能从外部跳入选择或迭代语句的循环体。尽管有这些限制，`goto` 在 C 中被广泛用于错误处理和资源清理。

**Auto 的方法。** Auto 有 `break` 和 `continue` 但没有 `goto`。资源清理使用 defer（计划中）或 Result 类型：

```auto
// Auto：结构化控制流
fn process() int {
    for i in 0..100 {
        if i == 5 {
            continue
        }
        if i == 10 {
            break
        }
        print(i)
    }
    0
}
```

> **C 深入：** Auto 中没有 `goto` 是有意的。C 中 `goto` 的每种用法都可以用结构化构造替代：`break`、`continue`、提前返回或 Result 类型。这使得控制流显式且更容易推理。

---

## 19.4 函数

正常的函数调用和返回是最常见的控制流机制：

```c
// C 深入：函数返回
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// 尾调用优化（取决于编译器）
int sum_to(int n, int acc) {
    if (n == 0) return acc;
    return sum_to(n - 1, acc + n);  // 可能被优化为尾调用
}
```

函数返回到其调用者。调用栈记录返回地址和局部变量。深度递归可能导致栈溢出。

**Auto 的方法。** Auto 函数工作方式相同：

```auto
// Auto：函数和返回
fn factorial(n int) int {
    if n <= 1 {
        return 1
    }
    n * factorial(n - 1)
}

fn main() {
    print("5! =", factorial(5))
}
```

不需要特殊处理——这是标准控制流。

---

## 19.5 长跳转

`setjmp` 和 `longjmp` 提供跨越函数边界的非局部跳转：

```c
// C 深入：setjmp/longjmp
#include <stdio.h>
#include <setjmp.h>

jmp_buf error_handler;

void inner_function(int value) {
    if (value < 0) {
        longjmp(error_handler, 1);  // 跳回 setjmp
    }
    printf("Value: %d\n", value);
}

int main(void) {
    int status = setjmp(error_handler);
    if (status == 0) {
        inner_function(42);    // 正常路径
        inner_function(-1);    // 触发 longjmp
        inner_function(99);    // 永远不会到达
    } else {
        printf("Caught error: %d\n", status);
    }
    return 0;
}
```

`setjmp` 保存执行上下文。`longjmp` 恢复它，使 `setjmp` 以非零值再次返回。这是 C 最接近异常处理的等价物。

> **C 深入：** `longjmp` 不调用析构函数或清理函数。在 `setjmp` 和 `longjmp` 之间被修改的任何变量，除非是 `volatile` 的，否则具有不确定的值。这使得 `longjmp` 在复杂代码中极其危险。它完全绕过了正常的函数调用/返回机制。

**Auto 的方法。** Auto 使用 Result 类型（类似 Rust 的 `Result<T, E>`）进行错误传播，而不是非局部跳转：

```auto
// Auto：Result 类型替代 setjmp/longjmp
type Result {
    value int
    ok bool
    error str
}

fn Result.ok(val int) Result {
    Result(val, true, "")
}

fn inner_function(value int) Result {
    if value < 0 {
        return Result.err("negative value")
    }
    print("Value:", value)
    Result.ok(value)
}
```

错误通过调用栈显式返回。没有隐藏的控制流。不需要 `volatile`。每个函数签名都声明它是否可能失败。

> **C 深入：** C 的 `setjmp`/`longjmp` 是非局部错误传播的唯一标准机制。POSIX 有 `sigsetjmp`/`siglongjmp`，它还保存和恢复信号掩码。一些 C 编译器（GNU、Clang）支持 `__attribute__((cleanup))` 用于自动资源清理，但这是非标准的。

---

## 19.6 信号处理器

信号是发送给进程的异步通知：

```c
// C 深入：信号处理器
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>

void handle_sigint(int sig) {
    printf("Caught SIGINT (Ctrl+C)\n");
    exit(0);
}

void handle_sigsegv(int sig) {
    printf("Segmentation fault!\n");
    _exit(1);  // 使用 _exit，不是 exit -- 调用大多数函数是不安全的
}

int main(void) {
    signal(SIGINT, handle_sigint);
    signal(SIGSEGV, handle_sigsegv);

    while (1) {}  // 永远运行，直到 Ctrl+C
    return 0;
}
```

> **C 深入：** 信号处理器受到严重限制。你只能安全地调用异步信号安全函数（在 POSIX 中列出）。`printf`、`malloc` 和大多数标准库函数**不是**异步信号安全的。写入 `volatile sig_atomic_t` 变量是在信号处理器和主程序之间通信的唯一可移植方式。`sigaction()` 函数（POSIX）比 `signal()` 提供更多控制。

这是 **C 独有**领域。Auto 不直接暴露信号处理器。使用信号的系统编程应该在 C 中完成，并通过 Auto 的 `sys` 模块暴露。

```auto
// Auto：通过 sys 模块处理信号（概念性）
// fn main() {
//     sys.on_interrupt(fn() {
//         print("Interrupted")
//         sys.exit(0)
//     })
// }
```

---

## 快速参考

| 概念              | C 机制                     | Auto 机制                    |
|------------------|----------------------------|------------------------------|
| 错误清理         | `goto` 标签                | Result 类型、提前返回        |
| 顺序求值         | 逗号运算符                 | 不需要                       |
| 循环控制         | `break`、`continue`        | `break`、`continue`         |
| 短跳转           | `goto`                     | 不支持                       |
| 错误传播         | `setjmp`/`longjmp`         | Result 类型                  |
| 异步信号         | `signal()`、`sigaction()`  | `sys` 模块（计划中）         |

---

*C 的控制流逃逸机制之所以存在，是因为 C 缺乏结构化错误处理。Auto 用 Result 类型和显式错误传播取代了 `goto`、`setjmp`/`longjmp` 和临时错误代码——使控制流可见且安全。*
