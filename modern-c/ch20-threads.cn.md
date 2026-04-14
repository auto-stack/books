# 第二十章：线程

> 级别 3 -- 经验
>
> 使用 C 线程、互斥量和条件变量进行共享内存并发——以及为什么 Auto 的 Actor 模型使大部分这些变得不必要。

并发是 C 程序最容易出错的地方。数据竞争、死锁和微妙的内存排序错误以难以复现和修复而闻名。C11 引入了基于 POSIX 线程的标准线程 API。Auto 采取了根本不同的方法：具有隔离状态的 Actor 通过消息传递进行通信。

---

## 20.1 简单的线程间控制

C11 提供了 `thrd_create` 和 `thrd_join` 用于线程管理：

```c
// C 深入：线程创建
#include <threads.h>
#include <stdio.h>

int worker(void *arg) {
    int id = *(int *)arg;
    printf("Worker %d started\n", id);
    int sum = 0;
    for (int i = 0; i < 100; i++) {
        sum += i;
    }
    printf("Worker %d finished, sum = %d\n", id, sum);
    return 0;
}

int main(void) {
    thrd_t t1, t2;
    int id1 = 1, id2 = 2;

    thrd_create(&t1, worker, &id1);
    thrd_create(&t2, worker, &id2);

    thrd_join(t1, NULL);
    thrd_join(t2, NULL);
    return 0;
}
```

> **C 深入：** C 线程共享整个地址空间。每个线程都可以读写每个全局变量。这使得数据竞争极其容易创建。线程函数必须返回 `int`（不是 POSIX 的 `void*`）。`thrd_create` 的参数以 `void*` 传递——这是类型错误的常见来源。

**Auto 的方法。** Auto 使用 Actor 模型代替原始线程：

```auto
// Auto：顺序执行（Actor 模型计划中）
fn worker(id int) {
    print("Worker", id, "started")
    var sum int = 0
    for i in 0..100 {
        sum = sum + i
    }
    print("Worker", id, "finished, sum =", sum)
}

fn main() {
    worker(1)
    worker(2)
}
```

<Listing path="listings/ch20/listing-20-01" title="线程基础" />

---

## 20.2 无竞争初始化

C 提供 `call_once` 用于一次性初始化：

```c
// C 深入：call_once
#include <threads.h>
#include <stdio.h>

static once_flag init_flag = ONCE_FLAG_INIT;
static int shared_config;

void init_config(void) {
    printf("Initializing config...\n");
    shared_config = 42;
}

int worker(void *arg) {
    call_once(&init_flag, init_config);
    printf("Config: %d\n", shared_config);
    return 0;
}
```

`call_once` 保证 `init_config` 只被调用一次，即使多个线程同时调用 `call_once`。这取代了双重检查锁定模式。

> **C 深入：** 在 `call_once` 之前，程序员使用"双重检查锁定"，这以难以正确实现而闻名。该模式需要原子操作和内存屏障。`call_once` 封装了所有复杂性。POSIX 有 `pthread_once` 实现相同目的。

**Auto 的方法。** Auto 自然地处理初始化。每个 Actor 在启动时初始化自己的状态。没有共享状态意味着没有初始化竞争。

---

## 20.3 线程局部数据

C11 引入了 `thread_local` 存储用于每线程数据：

```c
// C 深入：thread_local
#include <threads.h>
#include <stdio.h>

thread_local int counter = 0;

int worker(void *arg) {
    for (int i = 0; i < 1000; i++) {
        counter++;    // 每个线程有自己的计数器
    }
    printf("Thread counter: %d\n", counter);
    return 0;
}

int main(void) {
    thrd_t t1, t2;
    thrd_create(&t1, worker, NULL);
    thrd_create(&t2, worker, NULL);
    thrd_join(t1, NULL);
    thrd_join(t2, NULL);
    // 两个都打印 1000 -- 没有共享，没有竞争
    return 0;
}
```

`thread_local` 变量每个线程有一个实例。它们通过给每个线程自己的副本来避免数据竞争。

> **C 深入：** `thread_local` 是一个存储类说明符，类似于 `static` 或 `extern`。它可以与 `static` 组合用于内部链接。`thread_local` 变量的地址在每个线程中不同。获取其地址并传递给另一个线程会创建数据竞争。

**Auto 的方法。** Auto 的 Actor 模型自然地隔离状态。每个 Actor 有自己的私有数据——等价于默认情况下所有东西都是 `thread_local` 的。不需要关键字。

---

## 20.4 关键数据和关键区段

互斥量保护共享数据免受并发访问：

```c
// C 深入：互斥量
#include <threads.h>
#include <stdio.h>

static mtx_t mutex;
static int counter = 0;

int worker(void *arg) {
    for (int i = 0; i < 100000; i++) {
        mtx_lock(&mutex);
        counter++;
        mtx_unlock(&mutex);
    }
    return 0;
}

int main(void) {
    mtx_init(&mutex, mtx_plain);

    thrd_t t1, t2;
    thrd_create(&t1, worker, NULL);
    thrd_create(&t2, worker, NULL);
    thrd_join(t1, NULL);
    thrd_join(t2, NULL);

    printf("Counter: %d\n", counter);  // 200000
    mtx_destroy(&mutex);
    return 0;
}
```

> **C 深入：** 忘记解锁互斥量（例如由于提前返回或类似异常的错误）会造成死锁。C 没有 RAII 来自动释放互斥量。POSIX 有 `pthread_mutexattr_settype` 与 `PTHREAD_MUTEX_ERRORCHECK` 来检测双重锁定。`mtx_timed` 类型允许定时锁定尝试。C 标准不提供读写锁。

**Auto 的方法。** 没有共享可变状态意味着没有互斥量：

```auto
// Auto：没有共享状态，没有互斥量
type Counter {
    value int
}

fn Counter.new() Counter {
    Counter(0)
}

fn Counter.increment(c Counter) {
    c.value = c.value + 1
}

fn main() {
    var counter Counter = Counter.new()
    for i in 0..1000 {
        counter.increment(counter)
    }
    print("Counter:", counter.value)
}
```

<Listing path="listings/ch20/listing-20-02" title="互斥量和关键区段" />

---

## 20.5 条件变量

条件变量允许线程等待某个条件：

```c
// C 深入：条件变量
#include <threads.h>
#include <stdio.h>

static mtx_t mutex;
static cnd_t cond;
static int ready = 0;

int producer(void *arg) {
    mtx_lock(&mutex);
    ready = 1;
    printf("Produced data\n");
    cnd_signal(&cond);
    mtx_unlock(&mutex);
    return 0;
}

int consumer(void *arg) {
    mtx_lock(&mutex);
    while (!ready) {
        cnd_wait(&cond, &mutex);  // 释放互斥量，等待，重新获取
    }
    printf("Consumed data\n");
    mtx_unlock(&mutex);
    return 0;
}
```

`cnd_wait` 调用原子性地释放互斥量并阻塞线程。当 `cnd_signal` 唤醒它时，`cnd_wait` 在返回前重新获取互斥量。

> **C 深入：** 条件变量必须始终与互斥量和谓词循环一起使用（`while (!ready)`，不是 `if (!ready)`）。标准允许虚假唤醒——线程可能在未调用 `cnd_signal` 的情况下从 `cnd_wait` 中唤醒。谓词循环处理这种情况。`cnd_broadcast` 唤醒所有等待的线程。

**Auto 的方法。** Auto 计划中的 Actor 邮箱取代条件变量：

```auto
// Auto：消息传递取代条件变量（概念性）
// actor Consumer {
//     fn on_message(msg Message) {
//         // 当消息到达时被调用——不需要显式等待
//         print("Received:", msg.data)
//     }
// }
print("Auto actors 通过邮箱接收消息")
print("不需要显式的条件变量")
```

---

## 20.6 高级线程管理

真实的 C 程序使用线程池、future 和工作队列：

```c
// C 深入：线程池概念
#include <threads.h>
#include <stdio.h>
#include <stdlib.h>

#define POOL_SIZE 4
#define TASK_COUNT 16

typedef struct {
    thrd_t threads[POOL_SIZE];
    int task_queue[TASK_COUNT];
    int queue_size;
    mtx_t queue_mutex;
    cnd_t queue_cond;
    int shutdown;
} ThreadPool;

void pool_submit(ThreadPool *pool, int task) {
    mtx_lock(&pool->queue_mutex);
    pool->task_queue[pool->queue_size++] = task;
    cnd_signal(&pool->queue_cond);
    mtx_unlock(&pool->queue_mutex);
}
```

> **C 深入：** 在 C 中构建正确的线程池需要互斥量、条件变量和关闭标志的仔细协调。常见陷阱包括：丢失唤醒（在等待前发信号）、任务饥饿（不公平调度）和关闭竞争（等待后检查标志）。生产质量的线程池有数百行代码。

**Auto 的方法。** Actor 模型自动提供这些抽象：

- 每个 Actor 是一个并发单元（类似轻量级线程）
- 消息在 Actor 的邮箱中排队（类似任务队列）
- 运行时高效调度 Actor（类似线程池）

不需要手动线程管理。

---

## 20.7 确保活性

并发错误不仅限于数据竞争：

**死锁**发生在线程互相等待时：

```c
// C 深入：死锁场景
// 线程 1：mtx_lock(&A); mtx_lock(&B);  // 持有 A，等待 B
// 线程 2：mtx_lock(&B); mtx_lock(&A);  // 持有 B，等待 A
// 结果：两个线程永远等待
```

> **C 深入：** 死锁预防策略包括：锁定排序（始终以相同顺序获取锁）、trylock 配合退避（非阻塞尝试）和锁层次结构（给锁分配数字级别）。这些都不是由编译器强制执行的——纯粹是纪律性编程。

**饥饿**发生在线程永远无法访问资源时。活锁发生在线程不断对彼此做出反应而没有进展时。

**Auto 的方法。** Actor 模型在设计上防止死锁：

- Actor 不共享锁（没有锁排序问题）
- 消息传递是异步的（没有阻塞等待）
- 运行时公平调度 Actor（没有饥饿）

```auto
// Auto：设计上无死锁
print("Actor 模型防止死锁")
print("没有共享锁，没有循环等待")
print("运行时确保公平调度")
```

---

## 快速参考

| 概念                | C 机制                         | Auto 机制                     |
|--------------------|--------------------------------|-------------------------------|
| 线程创建           | `thrd_create`、`thrd_join`     | Actor 生成                    |
| 一次性初始化       | `call_once`                    | Actor 初始化                  |
| 线程局部数据       | `thread_local`                 | Actor 状态（默认）            |
| 互斥               | `mtx_lock` / `mtx_unlock`      | 不需要（消息传递）            |
| 等待               | `cnd_wait` / `cnd_signal`      | 邮箱接收                      |
| 线程池             | 手动实现                        | 运行时调度器                  |
| 死锁预防           | 锁排序、纪律                    | 设计上消除                    |

---

*C 线程是手动的、容易出错的，需要深厚的专业知识才能正确使用。Auto 的 Actor 模型在设计上消除了数据竞争、死锁和饥饿——用原始性能换取正确性，这几乎总是正确的权衡。*
