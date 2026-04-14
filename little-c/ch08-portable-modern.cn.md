# 第8章：可移植与现代 C

> 第 81--90 节
> C 代码必须能到处运行。Auto 让可移植成为默认选项，而非例外。

C 最大的优势在于可移植性。同一份 C 代码可以在 Linux、macOS、Windows 和嵌入式系统上
编译运行。但真正的可移植性需要理解平台差异——字节序、字长、线程 API 和编译器扩展。

Auto 默认生成可移植的 C 代码。a2c 转译器处理平台相关的细节，让你专注于程序逻辑。
本章介绍 C 的可移植性全景以及 Auto 如何简化它。

---

## 81. C 标准时间线

C 语言经历了多次标准演进，每次都增加新特性并保持向后兼容：

**C89/C90** —— 基础。ANSI 于 1989 年标准化 C，ISO 于 1990 年采纳。这是每个编译器
都支持的"经典"C。函数必须先声明后使用，变量必须在代码块顶部声明，`//` 注释不是标准。

**C99** —— 现代化的 C。增加了 `//` 注释、混合声明与代码、`<stdint.h>` 固定宽度整数、
变长数组和指派初始化器。

**C11** —— 并发更新。增加了 `_Static_assert`、`_Generic`、`<threads.h>`、原子操作
和对齐说明符。Auto 正是以 C11 为目标。

**C17/C23** —— 改进和新特性。C23 增加了 `typeof`、`constexpr`、`auto` 类型推断和
改进的属性语法。

Auto 生成 C11 兼容的代码，在保证广泛编译器支持的同时包含 `_Static_assert` 和
`<stdatomic.h>` 等现代特性。

<Listing id="listing-08-01" title="C 标准时间线" path="listings/ch08/listing-08-01" />

---

## 82. 可移植性与字节序

字节序决定了多字节值在内存中的存储方式：

- **小端序（Little-endian）**：最低有效字节在前（x86、ARM）
- **大端序（Big-endian）**：最高有效字节在前（某些网络协议、旧架构）

```c
/* 在 C 中检测字节序 */
uint32_t val = 1;
if (*(uint8_t *)&val == 1) {
    /* 小端序 */
} else {
    /* 大端序 */
}
```

网络协议使用大端序（网络字节序）。C 提供了 `htonl()`、`ntohl()`、`htons()` 和
`ntohs()` 用于转换。

Auto 透明地处理字节序。当你读写二进制数据时，Auto 生成正确的字节序转换代码。
你编写平台无关的代码；a2c 添加平台相关的处理。

---

## 83. 内联汇编

内联汇编允许你在 C 代码中嵌入特定 CPU 指令：

```c
/* GCC 内联汇编（x86-64） */
static inline uint64_t rdtsc(void) {
    uint32_t lo, hi;
    __asm__ __volatile__ ("rdtsc" : "=a" (lo), "=d" (hi));
    return ((uint64_t)hi << 32) | lo;
}
```

内联汇编的特点：
- **不可移植**：每种 CPU 架构有不同的指令和语法
- **编译器相关**：GCC、MSVC 和 Clang 有不同的内联汇编语法
- **危险**：错误的约束可能破坏寄存器或内存

Auto 不支持内联汇编。如果需要，可以编写 C 文件并通过 FFI 调用。这样将汇编隔离，
其余代码保持可移植。

---

## 84. 交叉编译

交叉编译是指在不同于目标平台的系统上进行编译：

```bash
# 在 x86 机器上为 ARM 编译
$ arm-linux-gnueabihf-gcc -o program program.c

# 在 Linux 上为 Windows 编译
$ x86_64-w64-mingw32-gcc -o program.exe program.c
```

交叉编译需要：
- 目标平台的工具链（编译器、链接器、头文件、库）
- 正确的 sysroot 和库路径
- 代码中的平台特定 `#ifdef` 保护

Auto 通过 a2c 简化交叉编译：

```bash
# Auto 交叉编译（概念性）
$ auto build --target arm-linux
$ auto build --target windows
```

a2c 生成适合目标的 C 代码并调用正确的交叉编译器。你只需指定目标，Auto 处理其余。

---

## 85. 使用 pthreads 进行线程编程

POSIX 线程（pthreads）是类 Unix 系统上的标准 C 线程 API：

```c
#include <pthread.h>

void *worker(void *arg) {
    int id = *(int *)arg;
    printf("Worker %d running\n", id);
    return NULL;
}

int main(void) {
    pthread_t t1, t2;
    int id1 = 1, id2 = 2;
    pthread_create(&t1, NULL, worker, &id1);
    pthread_create(&t2, NULL, worker, &id2);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    return 0;
}
```

Pthreads 很冗长：你需要手动管理线程创建、汇合、互斥锁和条件变量。Windows 有自己
的线程 API（`CreateThread`），使可移植的线程编程更加困难。

Auto 使用基于任务的并发模型代替原始线程：

```auto
task worker(id int) {
    print("Worker", id, "running")
}
```

任务是通过邮箱（mailbox）通信的轻量级工作单元。运行时自动将任务映射到操作系统线程。
不需要互斥锁、条件变量或平台特定的线程 API。

<Listing id="listing-08-02" title="使用 pthreads 进行线程编程" path="listings/ch08/listing-08-02" />

---

## 86. 原子操作

当多个线程访问共享数据时，你需要原子操作来防止数据竞争：

```c
#include <stdatomic.h>

atomic_int counter = ATOMIC_VAR_INIT(0);

/* 线程安全的递增 */
atomic_fetch_add(&counter, 1);

/* 线程安全的比较并交换 */
int expected = 5;
atomic_compare_exchange_strong(&counter, &expected, 10);
```

C11 的 `<stdatomic.h>` 提供了原子类型和操作。常见模式：
- **原子递增**：`atomic_fetch_add` 用于计数器
- **比较并交换**：`atomic_compare_exchange_strong` 用于无锁算法
- **原子加载/存储**：`atomic_load`、`atomic_store` 用于标志位

Auto 的任务模型从设计上避免了共享可变状态。任务通过消息传递（邮箱）通信，
而非共享内存。当你确实需要共享状态时，Auto 提供了安全的抽象。

---

## 87. FFI：从 Auto 调用 C

Auto 的优势之一是无缝的 C 互操作。你可以通过外部函数接口（FFI）调用任何 C 函数：

```auto
// 声明一个外部 C 函数
sys extern fn abs(n int) int

fn main() {
    let x int = -42
    let y int = abs(x)
    print("abs(-42) =", y)
}
```

`sys extern` 声明告诉 a2c 此函数存在于 C 的标准库中。转译器生成直接的 C 函数调用，
没有包装开销。

FFI 规则：
- C 类型直接映射：`int` 到 `int`，`float` 到 `float`，`str` 到 `char*`
- C 结构体可以用 `sys extern type` 声明
- C 枚举映射到 Auto 枚举
- 指针参数使用 Auto 的引用语法

这意味着每个 C 库都可以自动供 Auto 程序使用。

<Listing id="listing-08-03" title="FFI：从 Auto 调用 C" path="listings/ch08/listing-08-03" />

---

## 88. 更安全的替代方案

C 默认是不安全的。但许多不安全的模式有更安全的替代方案：

| 不安全的 C 模式          | 更安全的替代方案               | Auto 对应                |
|--------------------------|--------------------------------|--------------------------|
| `char*` 字符串           | `strncpy`、`snprintf`         | `str` 类型，边界安全      |
| `malloc`/`free`          | 竞技场分配器、内存池           | Auto 内存管理             |
| 原始指针运算              | 带边界的数组索引               | 边界检查的数组            |
| `strcpy`                 | 带大小限制的 `strncpy`         | 安全字符串操作            |
| `sprintf`                | `snprintf`                     | 类型安全的 `print`        |
| `gets`                   | `fgets`                        | 安全输入函数              |
| 未检查的数组访问          | 手动长度追踪                   | 带长度追踪的切片          |

Auto 默认使用安全选项。你必须使用 `unsafe` 块显式选择不安全操作，类似于 Rust 的方法。

```auto
unsafe {
    // 原始指针操作放在这里
    // 此块可审计且隔离
}
```

---

## 89. 现代风格

现代 C（C11+）支持比 C89 更清晰的代码风格。Auto 在此基础上建立了自己的约定：

**到处使用 `const`**（C）/ Auto 变量默认不可变：

```c
/* C */
const char *const msg = "hello";  /* 不可变指针，不可变数据 */
```

```auto
// Auto：let 不可变，var 可变
let msg str = "hello"
```

**命名初始化器**提高清晰度：

```c
struct Point p = {.x = 1, .y = 2};  /* C99 指派初始化器 */
```

```auto
let p Point = Point(1, 2)  /* Auto：清晰简洁 */
```

**`_Static_assert` 用于编译时检查**（C11）：

```c
_Static_assert(sizeof(int) == 4, "int must be 4 bytes");
```

Auto 的类型系统在编译时捕获大多数问题，无需显式断言。

<Listing id="listing-08-04" title="现代风格" path="listings/ch08/listing-08-04" />

---

## 90. 练习：可移植的多线程程序

本练习结合可移植性和并发概念。程序检测字节序并展示 Auto 如何处理平台差异。

在 C 中，你需要：
- 针对不同平台的 `#ifdef` 保护
- 手动字节序转换
- pthreads 或平台特定的线程 API
- Windows 与 Unix 的条件编译

在 Auto 中，这些由工具链处理。

<Listing id="listing-08-05" title="可移植的多线程练习" path="listings/ch08/listing-08-05" />

**练习题：**

1. 修改 listing-08-05 以检测系统的字长（32 位 vs 64 位）。
2. 添加一个函数，将 32 位整数在大端序和小端序之间转换。用 `is_little_endian()`
   的结果进行测试。
3. 研究：`#pragma pack` 的作用是什么？什么时候需要使用它？

---

## 速查表

| 节号  | 主题          | C 工具/方法             | Auto 方法              |
|-------|---------------|------------------------|------------------------|
| 81    | C 标准        | C89 到 C23             | 通过 a2c 以 C11 为目标  |
| 82    | 字节序        | 手动检测/转换           | 工具链处理              |
| 83    | 内联汇编      | `__asm__` 块           | 不支持；使用 FFI        |
| 84    | 交叉编译      | 交叉工具链             | `auto build --target`  |
| 85    | 线程编程      | pthreads               | 任务/邮箱并发           |
| 86    | 原子操作      | `<stdatomic.h>`        | 消息传递模型            |
| 87    | FFI           | 不适用                 | `sys extern` 声明       |
| 88    | 安全性        | 手动使用更安全的 API    | 默认安全                |
| 89    | 现代风格      | C11 特性               | Auto 约定               |
| 90    | 练习          | 平台保护 + pthreads    | 可移植的 Auto 代码      |
