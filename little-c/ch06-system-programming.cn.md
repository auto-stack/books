# 第 6 章：系统编程

> 第 61--70 节
> 系统编程是 C 语言的天下 —— 而 Auto 选择了一条不同的路。

C 语言诞生于编写操作系统的需求。它的标准库直接建立在内核系统调用之上，
每个 C 程序员最终都要学习文件描述符、进程、信号和内存映射。Auto 采取了
更高层次的方案：它将危险的原语封装在安全的 API 中，不暴露原始系统调用。

本章有大量 C 独有的概念。我们将它们作为理解程序如何与操作系统交互的
必备知识来讲解，并在有 Auto 简化替代方案的地方加以说明。

---

## 61. 系统调用与标准库

每个操作系统都提供一组**系统调用** —— 向内核请求服务的函数。在 C 中，
你可以直接调用它们：

```c
/* 原始系统调用 */
ssize_t n = read(fd, buffer, sizeof(buffer));

/* 标准库包装（带缓冲，可移植性更好） */
size_t n = fread(buffer, 1, sizeof(buffer), file);
```

标准库用缓冲、错误处理和可移植性包装了原始系统调用。`fread()` 内部
调用 `read()`，但添加了用户空间缓冲。

Auto 走得更远：`print()`、`read_file()`、`write_file()` 等函数
完全隐藏了系统调用的细节。你不需要处理文件描述符或缓冲管理。

<Listing id="listing-06-01" title="系统调用 vs 标准库" path="listings/ch06/listing-06-01" />

**要点**：在 C 中，理解系统调用是必不可少的。在 Auto 中，语言替你
处理了这些。但了解底层原理能让你在两种语言中都成为更优秀的程序员。

---

## 62. 进程创建（fork/exec）

在 POSIX 系统上，新进程通过 `fork()` 创建：

```c
pid_t pid = fork();
if (pid == 0) {
    /* 子进程 */
    execvp("ls", argv);
} else {
    /* 父进程 */
    waitpid(pid, NULL, 0);
}
```

`fork()` 创建当前进程的精确副本。`exec()` 用新程序替换该副本。
这个两步模式是 shell、服务器和守护进程工作方式的基础。

Auto **不**直接暴露 `fork()` 或 `exec()`。相反，它可能提供基于任务的
并发模型，更安全也更可移植。

<Listing id="listing-06-02" title="进程创建（fork/exec）" path="listings/ch06/listing-06-02" />

---

## 63. 文件描述符

**文件描述符**是内核用来追踪打开的文件、套接字和管道的小整数。在 C 中：

```c
int fd = open("data.txt", O_RDONLY);
read(fd, buffer, 1024);
close(fd);
```

每个进程启动时有三个标准描述符：

| FD | 名称    | 用途      |
|----|---------|----------|
| 0  | stdin   | 标准输入  |
| 1  | stdout  | 标准输出  |
| 2  | stderr  | 标准错误  |

Auto 提供 `read_file()` 和 `write_file()`，因此你永远不需要直接操作
文件描述符。转译器会生成正确的 `open`/`read`/`close` 序列。

<Listing id="listing-06-03" title="文件描述符" path="listings/ch06/listing-06-03" />

---

## 64. 管道与重定向

管道连接进程。管道有两端：一端写入，另一端读取。

```c
int pipefd[2];
pipe(pipefd);
/* pipefd[0] = 读端，pipefd[1] = 写端 */
write(pipefd[1], "hello", 5);
read(pipefd[0], buf, 5);
```

`dup2()` 函数重定向文件描述符 —— 这就是 shell 实现 `|`、`>` 和 `<`
的方式。当你输入 `ls | grep foo` 时，shell 创建管道、派生两个进程，
并将 `ls` 的 stdout 连接到 `grep` 的 stdin。

Auto 使用任务间的消息传递代替原始管道。

<Listing id="listing-06-04" title="管道与重定向" path="listings/ch06/listing-06-04" />

---

## 65. 信号

信号是发送给进程的异步通知。常见信号：

| 信号     | 默认动作 | 典型用途      |
|----------|---------|--------------|
| SIGINT   | 终止    | Ctrl+C 中断  |
| SIGTERM  | 终止    | 优雅关闭     |
| SIGSEGV  | 崩溃    | 内存违规     |
| SIGKILL  | 终止    | 无法被捕获   |

在 C 中，用 `signal()` 或 `sigaction()` 安装处理函数：

```c
void on_sigint(int sig) {
    printf("Caught SIGINT!\n");
}
signal(SIGINT, on_sigint);
```

信号处理很棘手：处理函数运行在受限上下文中，大多数库函数在其中调用
是不安全的。Auto 不暴露原始信号处理。

<Listing id="listing-06-05" title="信号与处理函数" path="listings/ch06/listing-06-05" />

---

## 66. 内存映射（mmap）

`mmap()` 将文件或匿名内存区域映射到进程地址空间：

```c
void *ptr = mmap(NULL, size, PROT_READ | PROT_WRITE,
                 MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
/* 像普通指针一样使用 ptr */
munmap(ptr, size);
```

`mmap` 的用途包括：
- 文件 I/O（内存映射文件比 read/write 更快）
- 进程间共享内存
- 分配大型对齐缓冲区

这是高级 C 领域。Auto 最终可能会提供安全的内存映射集合，但目前
这纯粹是一个值得了解的 C 概念。

---

## 67. 时间与时钟 API

C 提供多种时间函数：

```c
time_t now = time(NULL);          /* 挂钟时间（秒） */
clock_t ticks = clock();          /* 已用 CPU 时间 */
struct timespec ts;
clock_gettime(CLOCK_MONOTONIC, &ts);  /* 高分辨率 */
```

每种测量不同的东西 —— 挂钟时间 vs CPU 时间 vs 单调时间。选错会导致
微妙错误，尤其是在时区变化或系统时钟调整时。

Auto 可能提供 `time.now()` 等包装函数，返回干净的 `Time` 类型，
而不是原始整数或结构体。

---

## 68. 环境变量

环境变量是从父进程传递给子进程的键值字符串：

```c
const char *home = getenv("HOME");
setenv("MY_VAR", "42", 1);   /* 1 = 覆盖 */
```

它们通常用于配置、路径和特性标志。在 Auto 中，这些可能通过类型化
API 暴露：

```auto
let home str = env("HOME")
```

这是一个 C API 已经很简单的领域，Auto 的改进主要在于类型安全和
缺失键处理。

---

## 69. 错误处理与返回码

C 使用返回值和全局 `errno` 变量的组合：

```c
int fd = open("missing.txt", O_RDONLY);
if (fd == -1) {
    perror("open failed");
    /* errno 包含具体错误码 */
}
```

`errno` 模式容易出错：任何库调用都可能覆盖它，忘记检查返回码是最
常见的 C 错误之一。

Auto 使用 `!T` 错误类型替代：

```auto
let content !str = read_file("missing.txt")
// 必须显式处理错误情况
```

这强制你处理错误，消除了"忘记检查返回码"这一整类错误。

---

## 70. 练习：迷你 Shell

Shell 是经典的系统编程练习。在 C 中，它需要：

1. 读取命令行
2. 解析参数
3. 派生子进程
4. 在子进程中执行命令
5. 等待子进程完成

这个练习结合了文件描述符、fork/exec 和管道 —— 几乎本章的每个概念。

<Listing id="listing-06-06" title="迷你 Shell 练习" path="listings/ch06/listing-06-06" />

**挑战**：实现一个支持以下功能的 shell：
- 运行带参数的命令
- 在两个命令间管道输出（`ls | wc`）
- 将输出重定向到文件（`ls > out.txt`）

这需要深厚的 C 知识。在 Auto 中，你会使用更高层的进程 API。

---

## 快速参考

| 节号 | C 概念              | Auto 对应               | 难度     |
|------|--------------------|-------------------------|---------|
| 61   | 系统调用 vs 标准库  | `print()`、`read_file()` | 入门    |
| 62   | fork/exec          | 基于任务的并发           | 高级    |
| 63   | 文件描述符          | `read_file()`、`write_file()` | 中级 |
| 64   | 管道、dup2          | 消息传递                | 高级    |
| 65   | signal/sigaction   | 不暴露                  | 高级    |
| 66   | mmap               | 不暴露                  | 专家    |
| 67   | time/clock         | `time.now()`（计划中）  | 中级    |
| 68   | getenv/setenv      | `env()`（计划中）       | 入门    |
| 69   | errno、返回码       | `!T` 错误类型           | 中级    |
| 70   | 迷你 Shell         | 高层进程 API            | 高级    |
