# 第十六章：性能

> 级别 3 — 经验
>
> 内联函数、restrict 限定符和性能测量——榨取 C 的每一个周期，以及 Auto 如何为你处理优化。

性能很重要。不是每个程序都需要，也不是每时每刻都需要，但当它重要时，C 程序员需要理解如何编写快速代码以及如何证明代码是快的。C 通过 `inline` 和 `restrict` 等关键字、编译器属性和精确测量为你提供对性能的细粒度控制。Auto 采取不同的方法：编译器处理大多数优化，你专注于编写清晰的代码。

---

## 16.1 内联函数

C 的 `inline` 关键字向编译器建议将函数体直接替换到调用点，避免函数调用的开销：

```c
// C 深入：内联函数
static inline int square(int n) {
    return n * n;
}

static inline int max(int a, int b) {
    return (a > b) ? a : b;
}
```

C 中 `inline` 的规则微妙且经常被误解：

- `inline` 本身**不**保证内联——它只是一个提示。
- 在头文件中定义的 `inline` 函数需要在一个翻译单元中有对应的外部定义，否则程序具有未定义行为（C99/C11）。
- `static inline` 是实际的解决方案：每个翻译单元都有自己的副本，链接器不会看到重复符号。
- 编译器可以完全忽略 `inline`。现代编译器经常内联没有标记 `inline` 的函数，而拒绝内联标记了的函数。

> **C 深入：** C 中 `inline` 与链接之间的交互是语言中最令人困惑的方面之一。C99 引入了具有外部链接语义的 `inline`，与 C++ 不同。在实践中，大多数 C 程序员在头文件中使用 `static inline`，避免这种复杂性。C23 通过使 `inline` 行为更像 C++ 来简化了这一点。

**Auto 的方法。** Auto 没有 `inline` 关键字。编译器根据启发式算法自动决定内联：

- 小函数总是被内联。
- 在热循环中调用的函数是内联候选。
- 程序员可以标注性能关键的函数，但编译器做最终决定。

```auto
// Auto：不需要 inline 关键字
fn square(n int) int {
    n * n
}

fn max(a int, b int) int {
    if a > b { a } else { b }
}

fn main() {
    print("square(7) =", square(7))
    print("max(3, 7) =", max(3, 7))
}
```

<Listing path="listings/ch16/listing-16-01" title="内联函数" />

---

## 16.2 restrict 限定符

`restrict` 限定符告诉编译器指针是访问其所指向对象的唯一方式。这使得原本不可能的优化成为可能：

```c
// C 深入：restrict 限定符
void vector_add(double *restrict result,
                const double *restrict a,
                const double *restrict b,
                int n) {
    for (int i = 0; i < n; i++) {
        result[i] = a[i] + b[i];
    }
}
```

没有 `restrict`，编译器必须假设 `result`、`a` 和 `b` 可能重叠。有了 `restrict`，它知道它们不会重叠，所以可以：

- 向量化循环（使用 SIMD 指令）。
- 重排加载和存储。
- 将值在寄存器中保留更长时间。

`restrict` 用错就是未定义行为：

```c
// C 深入：restrict 违规
int arr[10] = {0};
void add(int *restrict a, int *restrict b) {
    *a += *b;
}
add(arr + 0, arr + 0);  // UB：a 和 b 别名同一数组
```

> **C 深入：** C 中的 `restrict` 语义是根据指针与其底层对象之间的"基于"关系定义的。C 标准中的正式定义出了名地难以理解。在实践中，`restrict` 意味着"我保证这些指针不会别名"。如果你违反了这个承诺，任何事情都可能发生。

**Auto 的方法。** Auto 不暴露 `restrict`。编译器自动执行别名分析。当编译器能证明两个引用不会别名时，它应用与 `restrict` 相同的优化。当它无法证明时，它生成安全的代码。

> **C 深入：** 许多 C 标准库函数使用 `restrict`：`memcpy`、`strcpy`、`printf` 和大多数字符串函数。`memcpy` 上的 `restrict` 限定符是它区别于 `memmove` 的地方——`memcpy` 要求不重叠的区域，`memmove` 处理重叠。搞错这一点是微妙缺陷的经典来源。

---

## 16.3 非顺序和可复现属性

C23 引入了两个新的函数属性用于优化提示：

**`[[unsequenced]]`**：函数的结果仅依赖于其参数且无副作用。编译器可以缓存结果或重排调用。

```c
// C 深入：[[unsequenced]] 属性
[[unsequenced]] double square(double x) {
    return x * x;
}
// 编译器可以在编译时计算 square(5)
// 并为相同参数的重复调用重用结果
```

**`[[reproducible]]`**：函数对相同参数总是返回相同结果，但可能有副作用（如日志记录）。

```c
// C 深入：[[reproducible]] 属性
[[reproducible]] int lookup(const int *table, int index) {
    return table[index];  // 相同 table，相同 index -> 相同结果
}
```

| 属性                  | 纯净？ | 副作用？ | 可缓存？ |
|----------------------|--------|---------|---------|
| `[[unsequenced]]`    | 是     | 无      | 是      |
| `[[reproducible]]`   | 是     | 可能有  | 有限    |

这些属性是程序员对编译器的承诺。违反它们是未定义行为。

> **C 深入：** 这些属性是 C 对 GCC `__attribute__((const))` 和 `__attribute__((pure))` 的回应。它们服务于类似目的：告诉编译器函数可以安全优化。C23 版本具有更清晰的语义并且是标准化的。

**Auto 的方法。** Auto 的编译器自动执行纯净性分析。不访问全局状态且无副作用的函数被视为纯函数。程序员不需要用属性标注函数。

---

## 16.4 测量与检查

优化之前，你必须测量。C 提供 `<time.h>` 中的 `clock()` 进行基本计时：

```c
// C 深入：性能测量
#include <time.h>
#include <stdio.h>

int fibonacci(int n) {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main(void) {
    clock_t start = clock();
    int result = fibonacci(35);
    clock_t end = clock();

    double elapsed = (double)(end - start) / CLOCKS_PER_SEC;
    printf("fib(35) = %d\n", result);
    printf("Time: %.3f seconds\n", elapsed);
    return 0;
}
```

`clock()` 的问题：

- 测量 CPU 时间，不是挂钟时间。
- 精度是实现定义的——对于微基准测试可能太粗。
- 不区分用户时间和系统时间。
- `CLOCKS_PER_SEC` 在不同平台上不同。

对于严肃的性能分析，C 程序员使用外部工具：

| 工具           | 用途                           |
|---------------|-------------------------------|
| `perf`        | Linux 性能计数器               |
| `gprof`       | 调用图分析                     |
| `Valgrind`    | 内存和缓存分析                  |
| `Instruments` | macOS 性能分析                 |
| `VTune`       | Intel 硬件性能分析              |

> **C 深入：** 优化的黄金法则：测量，不要猜测。程序员在预测时间花在哪里方面 notoriously 能力很差。性能分析一致表明，80% 的执行时间花在 20% 的代码中。先分析，后优化，再测量。

<Listing path="listings/ch16/listing-16-02" title="性能测量" />

**Auto 的方法。** Auto 提供内置基准测试工具。`auto bench` 命令无需手动 `clock()` 调用即可测量执行时间：

```auto
// Auto：内置基准测试
fn fibonacci(n int) int {
    if n <= 1 { return n }
    fibonacci(n - 1) + fibonacci(n - 2)
}

fn main() {
    let n int = 35
    print("Computing fib(" + str(n) + ")...")
    let result int = fibonacci(n)
    print("Result:", result)
    print("Use 'auto bench' for precise timing")
}
```

Auto 的工具将性能分析集成到开发工作流中。你不需要修改代码来测量它。

---

## 快速参考

| 概念                  | C 机制                       | Auto 机制                  |
|----------------------|------------------------------|----------------------------|
| 函数内联             | `inline` 关键字              | 自动                       |
| 头文件放置           | 头文件中的 `static inline`   | 不需要                     |
| 指针别名             | `restrict` 限定符            | 自动别名分析               |
| 纯函数               | `[[unsequenced]]` 属性       | 自动纯净性分析             |
| 可复现函数           | `[[reproducible]]` 属性      | 自动分析                   |
| 计时                 | `clock()`、外部分析工具      | `auto bench` 命令          |
| 优化提示             | 手动标注                     | 编译器驱动                 |

---

*性能是 C 存在的原因。但手动优化提示是现代编译器可以承担的负担。Auto 将这个负担从程序员身上卸下，通过智能编译提供可比的性能。*
