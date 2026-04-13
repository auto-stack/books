# Actor 并发

安全高效地处理并发编程是 Auto 的主要目标之一。_并发编程_是指程序的不同部分独立执行，_并行编程_是指程序的不同部分同时执行。随着越来越多的计算机利用多核处理器，这两者变得越来越重要。

Rust 的并发方法围绕线程、通道和共享状态（`Mutex<T>` 和 `Arc<T>`）构建。Auto 采用了不同的方法：_Actor 模型_。在 Actor 模型中，并发通过独立的_计算单元_（称为_actor_）来表达，它们只通过发送消息来通信。任何 actor 都不能直接访问另一个 actor 的状态。

这个模型消除了整类并发 bug：

- **无数据竞争** — actor 不共享内存
- **无死锁** — 没有可以死锁的锁
- **无过期引用** — 通信通过消息传递，而非共享指针

Auto 的所有权系统仍然扮演着关键角色：它确保 actor 之间发送的消息干净地转移所有权，防止发送者意外使用已发送给另一个 actor 的数据。

> **注意：** Actor 模型是 Auto 的主要并发抽象。为了与 Rust 库兼容，Auto 也通过 `use.rust` 支持基于线程的并发。本章重点介绍 Actor 模型，这是 Auto 惯用的方法。

本章将涵盖以下主题：

- Actor 模型与基于线程的并发有何不同
- 如何创建 actor 并在它们之间发送消息
- 消息传递模式：请求/响应、扇出和管道
- 需要与 Rust 线程互操作时的共享状态模式
- 并发规范：`Send` 和标记规范

## 从线程到 Actor

在 Rust 中，并发基于_线程_——共享内存的操作系统级执行单元。线程通过_通道_（消息传递）或受互斥锁保护的_共享状态_进行通信。

### 共享内存的问题

基于线程的共享内存并发虽然强大，但容易出错：

- **竞争条件**：线程以不一致的顺序访问数据
- **死锁**：两个线程互相等待，导致都无法继续
- **微妙的 bug**：只在特定情况下出现，难以复现

Rust 的所有权系统有助于在编译时防止许多这些问题，但心智模型仍然复杂。你必须同时考虑锁、生命周期和线程边界。

### Actor 模型

Actor 模型最早由 Carl Hewitt 于 1973 年提出，采用了不同的方法。_Actor_ 是计算的基本单元，具有以下属性：

1. 每个 actor 有自己的私有状态——其他 actor 无法访问
2. Actor 只通过发送异步消息进行通信
3. 当 actor 收到消息时，它可以：
   - 向其他 actor 发送消息
   - 创建新的 actor
   - 为下一条消息改变自己的状态

这个模型自然地映射到许多现实世界的并发问题，并避免了共享内存并发的陷阱。

### Actor 模型 vs 线程模型

| 概念 | Rust（线程） | Auto（Actor） |
|------|-------------|---------------|
| 并发单元 | 线程 | Actor |
| 通信方式 | 通道或共享状态 | 消息传递 |
| 状态共享 | Mutex + Arc | 不共享 |
| 数据竞争 | 由所有权防止 | 设计上不可能 |
| 死锁 | 可能 | 不可能（无锁） |
| 错误处理 | Result 类型 | 消息级错误 |

## 创建 Actor

在 Auto 中，使用 `actor` 关键字定义 actor。一个 actor 封装自己的状态，并定义它可以接收哪些消息。

### 定义 Actor

<Listing number="16-1" file-name="src/main.at" caption="一个简单的计数器 actor">

```auto
actor Counter {
    var count int

    fn init() Counter {
        Counter(count: 0)
    }

    on Increment {
        .count += 1
    }

    on GetCount -> int {
        .count
    }
}

fn main() {
    let counter = Counter.init()
    counter.send(Increment)
    counter.send(Increment)
    let result = counter.ask(GetCount)
    print(f"Count is ${result}")  // Count is 2
}
```

```rust
// Rust 等价实现，使用线程和通道
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let counter_clone = Arc::clone(&counter);

    let handle = thread::spawn(move || {
        let mut num = counter_clone.lock().unwrap();
        *num += 1;
        *num += 1;
    });

    handle.join().unwrap();
    println!("Count is {}", *counter.lock().unwrap());
}
```

</Listing>

`Counter` actor 维护一个私有的 `count` 字段。`on Increment` 块处理传入的 `Increment` 消息。`on GetCount -> int` 块处理 `GetCount` 消息并返回当前计数。

与 Rust 方法的主要区别：

- **无需 `Arc<Mutex<T>>`** — actor 私有拥有其状态
- **无需 `move` 闭包** — actor 模型自动处理所有权转移
- **无需 `.lock().unwrap()`** — 不需要锁，消息逐一处理

### Actor 生命周期

每个 actor 经历以下阶段：

1. **创建** — `Counter.init()` 创建新的 actor 实例
2. **运行** — actor 处理邮箱中的消息
3. **关闭** — 当所有引用被 drop 时，actor 停止

### 发送消息

有两种向 actor 发送消息的方式：

- **`send`** — 即发即忘（异步，不期望响应）
- **`ask`** — 请求-响应（等待返回值）

```auto
counter.send(Increment)         // 即发即忘
let n = counter.ask(GetCount)   // 等待响应
```

## 消息传递模式

### 基本消息传递

让我们创建一个更完整的示例：一个接收消息并打印的日志 actor。

<Listing number="16-2" file-name="src/main.at" caption="打印消息的日志 actor">

```auto
actor Logger {
    var prefix String

    fn init(prefix String) Logger {
        Logger(prefix)
    }

    on Log(msg String) {
        print(f"[${.prefix}] ${msg}")
    }
}

fn main() {
    let logger = Logger.init("app")
    logger.send(Log("Server started"))
    logger.send(Log("Processing request"))
    logger.send(Log("Server stopped"))
}
```

```rust
use std::sync::mpsc;
use std::thread;

enum LoggerMsg {
    Log(String),
}

fn main() {
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        let prefix = "app";
        for msg in rx {
            match msg {
                LoggerMsg::Log(text) => {
                    println!("[{}] {}", prefix, text);
                }
            }
        }
    });

    tx.send(LoggerMsg::Log("Server started".to_string())).unwrap();
    tx.send(LoggerMsg::Log("Processing request".to_string())).unwrap();
    tx.send(LoggerMsg::Log("Server stopped".to_string())).unwrap();
}
```

</Listing>

在 Rust 中，你需要创建通道、定义消息枚举、生成线程并手动匹配传入消息。Auto 的 actor 模型将这一切打包成更简洁、专用的抽象。

### 扇出：多个 Actor，一条消息

一种常见的模式是将消息广播到多个 actor：

<Listing number="16-3" file-name="src/main.at" caption="扇出：向多个工作 actor 发送消息">

```auto
actor Worker {
    let id int

    fn init(id int) Worker {
        Worker(id)
    }

    on Process(data String) {
        print(f"Worker ${.id} processing: ${data}")
    }
}

fn main() {
    let workers = [
        Worker.init(1),
        Worker.init(2),
        Worker.init(3),
    ]

    // 向每个工作 actor 发送工作
    let data = ["task-a", "task-b", "task-c"]
    for i in 0..3 {
        workers[i].send(Process(data[i]))
    }
}
```

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let data = ["task-a", "task-b", "task-c"];

    let handles: Vec<_> = (0..3)
        .map(|i| {
            let data = data[i].to_string();
            thread::spawn(move || {
                println!("Worker {} processing: {}", i + 1, data);
            })
        })
        .collect();

    for handle in handles {
        handle.join().unwrap();
    }
}
```

</Listing>

### 管道：顺序处理

消息可以流经一系列 actor，每个 actor 执行一次转换：

<Listing number="16-4" file-name="src/main.at" caption="actor 管道处理数据">

```auto
actor Validator {
    on Validate(input String) ?String {
        if input.len() > 0 {
            Some(input)
        } else {
            None
        }
    }
}

actor Uppercaser {
    on Uppercase(input String) String {
        input.to_uppercase()
    }
}

fn main() {
    let validator = Validator.init()
    let uppercaser = Uppercaser.init()

    let input = "hello"
    let validated = validator.ask(Validate(input))
    if let Some(data) = validated {
        let result = uppercaser.ask(Uppercase(data))
        print(f"Result: ${result}")  // Result: HELLO
    }
}
```

```rust
fn validate(input: &str) -> Option<&str> {
    if !input.is_empty() {
        Some(input)
    } else {
        None
    }
}

fn uppercase(input: &str) -> String {
    input.to_uppercase()
}

fn main() {
    let input = "hello";
    if let Some(data) = validate(input) {
        let result = uppercase(data);
        println!("Result: {}", result);
    }
}
```

</Listing>

## Actor 中的状态管理

每个 actor 维护自己的私有状态。处理消息时，actor 可以修改其状态，这些更改会保留到下一条消息。

### 累加器模式

<Listing number="16-5" file-name="src/main.at" caption="累加值的 actor">

```auto
actor Accumulator {
    var total int

    fn init() Accumulator {
        Accumulator(total: 0)
    }

    on Add(value int) {
        .total += value
    }

    on GetTotal -> int {
        .total
    }

    on Reset {
        .total = 0
    }
}

fn main() {
    let acc = Accumulator.init()
    acc.send(Add(10))
    acc.send(Add(20))
    acc.send(Add(5))
    print(f"Total: ${acc.ask(GetTotal)}")  // Total: 35
    acc.send(Reset)
    print(f"After reset: ${acc.ask(GetTotal)}")  // After reset: 0
}
```

```rust
use std::sync::{Arc, Mutex};
use std::thread;

struct Accumulator {
    total: i32,
}

fn main() {
    let acc = Arc::new(Mutex::new(Accumulator { total: 0 }));
    let acc1 = Arc::clone(&acc);
    let acc2 = Arc::clone(&acc);
    let acc3 = Arc::clone(&acc);

    let h1 = thread::spawn(move || {
        let mut a = acc1.lock().unwrap();
        a.total += 10;
    });
    let h2 = thread::spawn(move || {
        let mut a = acc2.lock().unwrap();
        a.total += 20;
    });
    let h3 = thread::spawn(move || {
        let mut a = acc3.lock().unwrap();
        a.total += 5;
    });

    h1.join().unwrap();
    h2.join().unwrap();
    h3.join().unwrap();

    println!("Total: {}", acc.lock().unwrap().total);
}
```

</Listing>

Auto 版本明显更简单：没有 `Arc`、没有 `Mutex`、没有线程管理。Actor 一次处理一条消息，因此 `total` 上不可能有数据竞争。

### 具有复杂状态的 Actor

<Listing number="16-6" file-name="src/main.at" caption="键值存储 actor">

```auto
actor KVStore {
    var data Map<String, String>

    fn init() KVStore {
        KVStore(data: Map.new())
    }

    on Set(key String, value String) {
        .data.insert(key, value)
    }

    on Get(key String) ?String {
        .data.get(key)
    }

    on Delete(key String) {
        .data.remove(key)
    }

    on Count -> int {
        .data.len()
    }
}

fn main() {
    let store = KVStore.init()
    store.send(Set("name", "Auto"))
    store.send(Set("version", "0.1"))
    print(f"name = ${store.ask(Get("name"))}")   // name = Some("Auto")
    print(f"count = ${store.ask(Count)}")          // count = 2
    store.send(Delete("version"))
    print(f"count = ${store.ask(Count)}")          // count = 1
}
```

```rust
use std::collections::HashMap;
use std::sync::{Arc, Mutex};

struct KVStore {
    data: HashMap<String, String>,
}

fn main() {
    let store = Arc::new(Mutex::new(KVStore {
        data: HashMap::new(),
    }));

    {
        let mut s = store.lock().unwrap();
        s.data.insert("name".to_string(), "Auto".to_string());
        s.data.insert("version".to_string(), "0.1".to_string());
    }

    {
        let s = store.lock().unwrap();
        println!("name = {:?}", s.data.get("name"));
        println!("count = {}", s.data.len());
    }

    {
        let mut s = store.lock().unwrap();
        s.data.remove("version");
    }

    println!("count = {}", store.lock().unwrap().data.len());
}
```

</Listing>

## 与 Rust 线程互操作

当你需要使用 Rust 的基于线程的并发时（例如，调用使用线程的 Rust 库），Auto 通过 `use.rust` 提供访问：

<Listing number="16-7" file-name="src/main.at" caption="使用 Rust 线程进行互操作">

```auto
use.rust std::thread
use.rust std::sync::{Arc, Mutex}

fn main() {
    let counter = Arc.new(Mutex.new(0))
    var handles = List.new()

    for _ in 0..10 {
        let counter_clone = Arc.clone(&counter)
        let handle = thread.spawn(() => {
            var num = counter_clone.lock().unwrap()
            *num += 1
        })
        handles.push(handle)
    }

    for handle in handles {
        handle.join().unwrap()
    }

    print(f"Result: ${*counter.lock().unwrap()}")  // Result: 10
}
```

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut num = counter.lock().unwrap();
            *num += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Result: {}", *counter.lock().unwrap());
}
```

</Listing>

### 何时使用 Actor vs 线程

| 场景 | 使用 Actor | 使用线程 |
|------|-----------|---------|
| 独立服务 | 是 | 否 |
| 共享可变状态 | 用 actor 避免 | Mutex + Arc |
| CPU 密集型并行 | 有限 | 是 |
| Rust 库互操作 | 否 | 是 |
| 基于消息的工作流 | 是 | 可以但冗长 |
| 简单后台任务 | 是 | 两者皆可 |

## `Send` 规范

与 Rust 类似，Auto 使用 `Send` 规范来表示类型可以在 actor（或线程）之间安全转移。所有权系统确保通过消息传递的值从一个 actor 干净地转移到另一个 actor。

大多数 Auto 类型自动实现 `Send`。主要例外是包含通过 `use.rust` 访问的非线程安全 Rust 引用的类型。

### 消息中的所有权转移

当发送包含值的消息时，该值的所有权转移到接收 actor：

```auto
let data = List.of(1, 2, 3)
worker.send(Process(data))
// data 在此处不再有效 — 所有权已转移
```

这防止发送者意外修改接收者正在使用的数据。所有权系统在编译时捕获此问题。

### 发送前克隆

如果需要保留副本，在发送前克隆数据：

```auto
let data = List.of(1, 2, 3)
worker.send(Process(data.clone()))
// data 在此处仍然有效 — 我们发送了克隆
print(data)  // 正常工作
```

## 并发速查表

| 功能 | Auto（Actor） | Rust（线程） |
|------|---------------|-------------|
| 定义单元 | `actor Name { }` | `thread::spawn(\|\| { })` |
| 发送消息 | `actor.send(Msg)` | `tx.send(val)` |
| 请求/响应 | `actor.ask(Msg)` | `rx.recv()` + `tx.send()` |
| 共享状态 | 不共享 — actor 拥有 | `Arc<Mutex<T>>` |
| 防止数据竞争 | 设计保证（不共享） | 所有权 + 类型系统 |
| 防止死锁 | 设计保证（无锁） | 小心的锁排序 |
| 创建新单元 | `Name.init()` | `thread::spawn()` |
| 标记规范 | `Send` | `Send` + `Sync` |

## 总结

Auto 的 actor 模型提供了一种与 Rust 基于线程的模型根本不同的并发方法：

1. **Actor** — 具有私有状态的独立计算单元
2. **消息传递** — actor 通信的唯一方式；不共享内存
3. **`send` 和 `ask`** — 即发即忘和请求-响应模式
4. **所有权转移** — 消息转移所有权，防止数据竞争
5. **无锁** — actor 一次处理一条消息，消除死锁
6. **Rust 互操作** — 通过 `use.rust` 可用基于线程的并发

Actor 模型用共享内存的灵活性换取了隔离状态的安全性和简单性。对于大多数并发应用，这种权衡产生的代码更容易编写、更容易理解，并且没有整类并发 bug。

在下一章，我们将探讨 Auto 使用 `~T` 蓝图的异步编程模型，以及它与 Rust 的 `async`/`await` 的关系。
