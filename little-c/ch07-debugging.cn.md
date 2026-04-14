# 第 7 章：调试、测试、性能分析

> 第 71--80 节
> C 的调试工具强大但依赖手动操作。Auto 旨在在错误发生之前就阻止它们。

调试是 C 和 Auto 差异最显著的地方。C 程序可能有只在特定条件下才出现的
微妙内存错误。gdb 和 valgrind 等工具之所以存在，正是因为 C 缺乏安全
保证使得它们成为必需品。

Auto 在语言层面阻止了许多这类错误。当错误确实发生时，Auto 的测试框架
和断言能帮助尽早发现。本章涵盖你应该了解的 C 工具以及 Auto 的内置替代
方案。

---

## 71. 使用 GDB 调试

GDB（GNU 调试器）是标准的 C 调试器。它可以让你：

- 设置断点在某一行暂停执行
- 逐行单步执行代码
- 检查变量和内存
- 查看调用栈

```bash
$ gcc -g program.c -o program    # -g 添加调试符号
$ gdb ./program
(gdb) break main
(gdb) run
(gdb) next
(gdb) print x
(gdb) backtrace
```

GDB 功能强大但学习曲线陡峭。大多数开发者通过 VS Code 的调试适配器
或 TUI 界面来使用它。

Auto 目前还没有专用调试器，但由于 Auto 转译为 C，你可以在生成的
C 代码上使用 GDB。映射关系很直接，因为 Auto 构造直接对应 C 等价物。

---

## 72. Valgrind 内存检查

Valgrind 检测编译器和运行时检查遗漏的内存错误：

```bash
$ valgrind --leak-check=full ./program
==1234== Invalid read of size 4
==1234==    at 0x400544: main (program.c:12)
==1234==  Address 0x5205054 is 0 bytes after a block of size 4 alloc'd
```

Valgrind 能捕获：
- 释放后使用
- 缓冲区溢出（读和写）
- 内存泄漏
- 未初始化内存读取

运行 Valgrind 很慢 —— 程序会慢 10-50 倍。它通常在 CI 流水线中或
追踪特定错误时使用。

Auto 在大多数情况下使 Valgrind 变得不必要，因为语言在编译时阻止了
这些错误。边界检查、所有权追踪和可选类型消除了 Valgrind 检测的整类
内存错误。

---

## 73. 断言

断言是验证条件为真的运行时检查。如果失败，程序会中止并显示消息。

**C 断言：**

```c
#include <assert.h>
assert(x > 0);                    /* 简单断言 */
assert(ptr != NULL && "ptr must not be null");  /* 带消息 */
```

**Auto 断言：**

```auto
assert(x > 0, "x 必须为正数")
assert(ptr != nil, "ptr 不能为 null")
```

Auto 的 `assert` 按惯例包含消息参数，比 C 的默认断言输出更具信息量。
转译器将其映射为带有字符串化条件的 C `assert()`。

<Listing id="listing-07-01" title="调试策略" path="listings/ch07/listing-07-01" />
<Listing id="listing-07-02" title="断言" path="listings/ch07/listing-07-02" />

---

## 74. 单元测试

C 没有内置测试框架。项目通常使用第三方库如 Check、Unity，或编写
最小测试工具：

```c
void test_add(void) {
    assert(add(2, 3) == 5);
    assert(add(-1, 1) == 0);
}
int main(void) {
    test_add();
    printf("All tests passed!\n");
}
```

Auto 内置测试功能，通过 `auto t` 命令运行：

```auto
test "add two numbers" {
    assert add(2, 3) == 5
}

test "subtract numbers" {
    assert subtract(5, 3) == 2
}
```

用 `auto t` 运行测试。无需安装框架，无需样板代码，无需宏。

<Listing id="listing-07-03" title="Auto 中的单元测试" path="listings/ch07/listing-07-03" />

---

## 75. 日志系统

日志比 `printf` 调试更有用，因为它可以：
- 按严重级别过滤
- 定向到文件而非控制台
- 保留在生产代码中（不像调试打印）

C 中的简单日志器：

```c
typedef enum { LOG_DEBUG, LOG_INFO, LOG_WARN, LOG_ERROR } LogLevel;

void log_msg(LogLevel level, const char *msg) {
    const char *names[] = {"DEBUG", "INFO", "WARN", "ERROR"};
    fprintf(stderr, "[%s] %s\n", names[level], msg);
}
```

Auto 用类型安全的枚举和字符串处理使这更简洁：

```auto
type Level enum { Debug, Info, Warn, Error }

fn log_msg(level Level, msg str) {
    print("[" + str(level) + "] " + msg)
}
```

---

## 76. 性能分析

性能分析告诉你程序在哪里花费时间。标准 C 工具是 gprof：

```bash
$ gcc -pg program.c -o program    # -pg 添加性能分析插桩
$ ./program                       # 运行程序
$ gprof program gmon.out > report.txt
```

gprof 显示：
- 每个函数花费的时间
- 调用次数
- 调用图（谁调用了谁）

现代替代方案包括 Linux 上的 `perf` 和 macOS 上的 Instruments。它们使用
硬件性能计数器，无需重新编译即可分析。

Auto 可能通过其工具链支持性能分析。由于 Auto 转译为 C，现有的 C
分析工具可在生成的代码上使用。

---

## 77. 未定义行为 —— 以及 Auto 如何阻止它们

C 大约有 200 个未定义行为（UB）。以下是最危险的：

**缓冲区溢出：**

```c
int arr[3];
arr[5] = 42;    /* UB！写入超出数组边界 */
```
Auto：数组有边界检查。越界访问是编译错误或运行时 panic。

**释放后使用：**

```c
free(ptr);
*ptr = 42;      /* UB！访问已释放的内存 */
```
Auto：AutoFree 所有权系统确保指针在所有者释放后永远不会被使用。

**空指针解引用：**

```c
int *p = NULL;
*p = 42;        /* UB！解引用 NULL */
```
Auto：`?T` 可选类型强制你在访问值之前检查 `nil`。

**整数溢出：**

```c
int x = INT_MAX;
x++;            /* UB！有符号溢出 */
```
Auto：默认使用检查算术。溢出产生运行时错误而非静默回绕。

<Listing id="listing-07-04" title="未定义行为 —— Auto 阻止" path="listings/ch07/listing-07-04" />

---

## 78. 崩溃分析

当 C 程序崩溃时，操作系统可能生成**核心转储** —— 崩溃时进程内存的快照。

```bash
$ ulimit -c unlimited          # 启用核心转储
$ ./program                    # 程序崩溃
Segmentation fault (core dumped)
$ gdb ./program core
(gdb) backtrace                # 显示崩溃位置
(gdb) frame 0                  # 跳转到崩溃帧
(gdb) print *ptr               # 检查错误指针
```

读取回溯是崩溃分析的第一步：
1. 从顶部帧开始 —— 那是崩溃发生的地方
2. 查找空指针、无效内存或除以零
3. 沿调用栈向下追溯，理解是如何到达那里的

转译为 C 的 Auto 程序可以用同样的方式调试，但大多数需要这种分析的
崩溃已被 Auto 的安全保证所阻止。

---

## 79. 代码审查清单

无论你写 C 还是 Auto，这些检查都适用：

**正确性：**
- [ ] 每个函数是否处理了所有输入情况？
- [ ] 返回值是否检查了错误？
- [ ] 边界情况是否测试了（空输入、最大值、null/nil）？

**内存安全（C 特有）：**
- [ ] 每个 `malloc` 是否都有对应的 `free`？
- [ ] 指针在解引用前是否检查了 NULL？
- [ ] 数组索引是否在边界内？
- [ ] 是否存在释放后使用或双重释放？

**Auto 特有：**
- [ ] `!T` 错误返回类型是否已处理？
- [ ] `?T` 可选类型在使用前是否已解包？
- [ ] 是否使用断言检查不变量？

**风格：**
- [ ] 名称是否具有描述性且一致？
- [ ] 代码是否不依赖注释就能阅读？
- [ ] 注释是否解释了"为什么"而非"什么"？

---

## 80. 练习：修复 Bug

本练习包含有意的 bug。找到它们，理解为什么是 bug，然后修复它们。

<Listing id="listing-07-05" title="修复 Bug 练习" path="listings/ch07/listing-07-05" />

**Bug 提示：**
1. `sum_to(10)` 应该返回 55。它返回了吗？检查循环范围。
2. `is_positive(0)` —— 零是正数吗？函数应该返回什么？
3. `fib(-1)` —— 函数是否正确处理了负数输入？

这些正是断言和测试能捕获的 bug 类型。在运行之前添加 `assert` 调用来
验证每个函数的行为。

---

## 快速参考

| 节号 | 主题               | C 工具/方法        | Auto 方案              |
|------|--------------------|--------------------|------------------------|
| 71   | 调试器             | GDB                | 转译 C + GDB           |
| 72   | 内存检查           | Valgrind           | 不需要（安全语言）     |
| 73   | 断言               | `assert.h`         | 内置 `assert`          |
| 74   | 单元测试           | Check、Unity 等    | `auto t` 内置          |
| 75   | 日志               | 手动实现           | 类型安全日志器         |
| 76   | 性能分析           | gprof、perf        | 兼容 C 工具链          |
| 77   | 未定义行为         | ~200 个 UB         | 语言层面阻止           |
| 78   | 崩溃分析           | 核心转储、GDB      | 大多数崩溃已被阻止     |
| 79   | 代码审查           | 手动清单           | 相同 + Auto 特有项目   |
| 80   | 修复 Bug           | GDB + Valgrind     | `assert` + `auto t`    |
