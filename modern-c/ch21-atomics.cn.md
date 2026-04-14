# 第二十一章：原子操作与内存一致性

> 级别 3 -- 经验
>
> 使用原子操作和内存排序进行无锁编程——C 并发的最深层次，编译器和 CPU 都是你要对抗的对手。

原子操作是所有高级并发原语的基础。互斥量使用原子操作。条件变量使用原子操作。即使是多线程程序中最简单的"这个标志是否设置？"检查也需要原子操作才能保证正确性。本章涵盖了本书中技术要求最高的内容。

---

## 21.1 先行发生关系

当两个线程访问相同的内存时，这些访问"发生"的顺序并不总是清楚的。编译器可能重排指令。CPU 可能重排内存操作。缓存层次结构可能延迟可见性。

**先行发生**（happened-before）关系定义了一个操作是否保证对另一个操作可见：

```c
// C 深入：先行发生
// 线程 1：              线程 2：
// x = 1;                if (flag == 1)
// flag = 1;                 assert(x == 1);  // 可能失败
```

没有适当的同步，线程 2 可能看到 `flag == 1` 但 `x == 0`。编译器或 CPU 可能重排存储，或者缓存可能在线程 2 读取 `flag` 时尚未传播对 `x` 的写入。

> **C 深入：** 先行发生关系由 C 标准定义（以及之前的 Java 内存模型）。它是一种偏序关系：并非所有操作都彼此有序。只有通过同步（互斥量加锁/解锁、具有适当内存排序的原子操作）连接的操作才能建立先行发生关系。

关键洞察：**程序顺序不是内存顺序**。你编写的代码不是 CPU 执行的顺序，也不是其他线程观察效果的顺序。

**Auto 的方法。** Auto 的 Actor 模型完全避免了这个问题。每个 Actor 拥有自己的数据。消息按顺序传递。没有共享可变状态意味着没有内存排序问题。

---

## 21.2 提供同步的 C 库调用

C11 通过 `<stdatomic.h>` 提供原子操作：

```c
// C 深入：原子操作
#include <stdatomic.h>
#include <stdio.h>
#include <threads.h>

static _Atomic int counter = 0;

int worker(void *arg) {
    for (int i = 0; i < 100000; i++) {
        atomic_fetch_add(&counter, 1);
    }
    return 0;
}

int main(void) {
    thrd_t t1, t2;
    thrd_create(&t1, worker, NULL);
    thrd_create(&t2, worker, NULL);
    thrd_join(t1, NULL);
    thrd_join(t2, NULL);

    printf("Counter: %d\n", atomic_load(&counter));  // 200000
    return 0;
}
```

`_Atomic` 类型限定符使对该对象的操作成为原子的。`atomic_fetch_add` 函数原子性地递增计数器。不需要互斥量。

> **C 深入：** 原子操作使用 CPU 级别原语实现：
> - x86：`LOCK` 前缀指令（例如 `LOCK XADD`）
> - ARM：`LDXR`/`STXR` 独占加载/存储对
> - 某些架构使用全局比较并交换循环
>
> `_Atomic` 类型可能具有与非原子对应物不同的大小或对齐方式。`_Atomic(int)` 在主流平台上总是无锁的，但 `_Atomic(struct large)` 可能使用内部锁。

常见原子操作：

| 操作                | 函数                          | 描述                        |
|--------------------|-------------------------------|-----------------------------|
| 加载               | `atomic_load(&x)`             | 原子读取                    |
| 存储               | `atomic_store(&x, val)`       | 原子写入                    |
| 获取并加           | `atomic_fetch_add(&x, 1)`     | 加并返回旧值                |
| 获取并减           | `atomic_fetch_sub(&x, 1)`     | 减并返回旧值                |
| 比较并交换         | `atomic_compare_exchange_strong` | CAS 操作                  |
| 交换               | `atomic_exchange(&x, val)`    | 原子交换                    |
| 标志测试并设置     | `atomic_flag_test_and_set`    | 简单自旋锁原语              |

<Listing path="listings/ch21/listing-21-01" title="原子操作" />

**Auto 的方法。** Auto 不直接暴露原子操作。高级并发抽象（Actor、消息传递）是预期的接口。对于系统编程，原子操作可能通过 `sys` 模块暴露。

---

## 21.3 顺序一致性

默认的内存排序是**顺序一致性**（`memory_order_seq_cst`）：

```c
// C 深入：顺序一致性
#include <stdatomic.h>
#include <stdio.h>

static _Atomic int x = 0;
static _Atomic int y = 0;
static _Atomic int r1 = 0;
static _Atomic int r2 = 0;

// 线程 1：                    线程 2：
// atomic_store(&x, 1);        atomic_store(&y, 1);
// r1 = atomic_load(&y);       r2 = atomic_load(&x);

// 使用 seq_cst：r1==0 和 r2==0 同时成立是不可能的
// 所有线程对所有原子操作的单个总顺序达成一致
```

顺序一致性是最强的内存模型。所有线程对所有原子操作的单个总排序达成一致。它最容易推理但实现最昂贵。

> **C 深入：** 在 x86 上，顺序一致性相对便宜，因为 x86 有强内存模型（Total Store Order）。带 `seq_cst` 的 `atomic_store` 编译为 `MOV` + `MFENCE` 或 `LOCK XCHG`。在 ARM 上，`seq_cst` 需要 `DMB`（数据内存屏障）指令，这更昂贵。`seq_cst` 和 `relaxed` 之间的性能差异在 ARM 上可能达到 2-10 倍。

**Auto 的方法。** Auto Actor 通过消息通信。消息传递默认是顺序一致的。Actor 运行时在内部处理内存屏障。程序员永远不需要考虑内存排序。

---

## 21.4 其他一致性模型

C 提供了四种更弱的内存排序用于性能敏感的代码：

### 宽松（`memory_order_relaxed`）

没有排序保证。只保证原子性：

```c
// C 深入：宽松排序
#include <stdatomic.h>

static _Atomic int counter = 0;

// 多个线程：
atomic_fetch_add_explicit(&counter, 1, memory_order_relaxed);
// 每次递增是原子的，但与其他操作的排序不保证
```

当你只需要原子性而不需要排序时使用宽松（例如统计计数器，其中确切顺序无关紧要）。

### 获取（`memory_order_acquire`）

当前线程中不能有任何读或写被重排到此加载之前：

```c
// C 深入：获取排序
// 生产者：
// atomic_store_explicit(&flag, 1, memory_order_release);
//
// 消费者：
// if (atomic_load_explicit(&flag, memory_order_acquire)) {
//     // release 之前的所有写入在此处可见
//     assert(data == 42);  // 保证
// }
```

### 释放（`memory_order_acq_rel`）

不能有任何读或写被重排到此存储之后。与获取配对建立同步：

```c
// C 深入：release/acquire 模式
#include <stdatomic.h>
#include <stdio.h>

static int data = 0;
static _Atomic int ready = 0;

// 线程 1（生产者）：
void produce(void) {
    data = 42;    // 普通写入
    atomic_store_explicit(&ready, 1, memory_order_release);
}

// 线程 2（消费者）：
void consume(void) {
    while (atomic_load_explicit(&ready, memory_order_acquire) == 0) {}
    printf("data = %d\n", data);  // 保证看到 42
}
```

> **C 深入：** release/acquire 模式是最常见的非默认排序。它建立先行发生关系：release 存储之前的所有写入在 acquire 加载之后可见。这是无锁数据结构的基础。`memory_order_acq_rel` 将两者组合用于读-修改-写操作（如比较并交换）。

### 内存排序总结

| 排序                | 保证                                    | 使用场景                  |
|--------------------|-----------------------------------------|---------------------------|
| `seq_cst`          | 单个总顺序                              | 默认，最安全              |
| `acq_rel`          | 读-修改-写上的获取+释放                 | 比较并交换循环            |
| `acquire`          | 加载前不能重排                          | 读取同步数据              |
| `release`          | 存储后不能重排                          | 发布同步数据              |
| `relaxed`          | 仅原子性                                | 简单计数器                |

> **C 深入：** 使用 `seq_cst` 以外的内存排序是专家专属领域。不正确使用 `relaxed` 可能导致只在特定硬件（ARM、POWER）和特定编译器优化级别下才会出现的微妙错误。Linux 内核为了性能广泛使用 `relaxed`，但开发者是世界上内存模型方面最顶尖的专家。对于应用代码，除非性能分析证明是瓶颈，否则始终使用 `seq_cst`。

**Auto 的方法。** Auto 在其并发模型之后隐藏了内存排序：

```auto
// Auto：内存排序由运行时处理
// Actor 通过消息通信
// 消息传递提供 acquire/release 语义
// 不需要显式的 memory_order_* 类型

fn main() {
    // 顺序执行 -- 没有内存排序问题
    let x int = 0
    for i in 0..100 {
        x = x + 1
    }
    print("Sequential count:", x)
    print("Auto：Actor 提供安全的并发，无需原子操作")
}
```

> **C 深入：** 理解原子操作和内存排序对 C 系统程序员至关重要。即使 Auto 隐藏了这些细节，实现 Auto 运行时的底层 C 代码广泛使用了它们。`atomic_*` 函数和 `memory_order_*` 枚举是每个无锁算法、每个互斥量实现和每个并发数据结构的构建块。

---

## 快速参考

| 概念                  | C 机制                              | Auto 机制                  |
|----------------------|-------------------------------------|----------------------------|
| 原子操作             | `_Atomic`、`atomic_fetch_add`       | 不直接暴露                  |
| 顺序一致性           | `memory_order_seq_cst`              | 消息传递的默认行为          |
| 获取/释放            | `memory_order_acquire/release`      | 由运行时处理                |
| 宽松排序             | `memory_order_relaxed`              | 不适用                      |
| 比较并交换           | `atomic_compare_exchange_strong`    | 不直接暴露                  |
| 无锁原语             | `atomic_flag`                       | 不适用                      |

---

*原子操作是并发编程的基石。C 给你完全的控制权——和完全的责任。Auto 的 Actor 模型用安全性换取了这种控制权：你永远不需要考虑内存排序，因为运行时会为你处理。对于需要原始原子操作的罕见情况，`sys` 模块将提供逃逸通道。*
