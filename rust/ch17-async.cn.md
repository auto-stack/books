# 使用 `~T` 进行异步编程

我们让计算机执行的许多操作可能需要一段时间才能完成。如果在等待这些长时间运行的过程完成时，我们还能做其他事情就好了。现代计算机提供了两种同时处理多个操作的技术：并行和并发。然而，我们的程序逻辑通常以线性方式编写。我们希望能够指定程序应该执行的操作以及函数可以暂停的节点，让程序的其他部分在此期间运行，而无需事先准确指定每段代码应该运行的顺序和方式。_异步编程_是一种抽象，它让我们通过潜在的暂停点和最终结果来表达代码，并为我们处理协调的细节。

Rust 的异步编程方法围绕 `Future` trait、`async` 和 `await` 关键字以及 `tokio` 等外部运行时 crate 构建。Auto 采用了不同的方法：使用 `~T` 类型操作符和 `on` 块的_蓝图_（blueprint）。_蓝图_是对尚未发生的计算的描述——它"蓝图化"了一个在未来某个时刻产生的 `T` 类型的值。蓝图是惰性的：在有人用 `on` 块订阅它们之前，它们什么也不做。

这个模型自然地映射到现实世界的异步问题：

- **网络请求** — 等待数据而不阻塞
- **定时器和延迟** — 暂停执行而不消耗线程
- **用户界面事件** — 响应点击、按键和其他输入
- **文件 I/O** — 读写文件而不使程序停滞

本章将涵盖以下主题：

- Auto 的 `~T` 蓝图与 Rust 的 `Future` trait 有何不同
- 如何使用 `on` 块创建和消费蓝图
- 并发模式：竞赛、连接和消息传递
- 让出控制和构建自定义异步抽象
- 蓝图与第 16 章中 Auto 的 Actor 模型如何关联

## 从 Future 到蓝图

### Rust 的方法：Future 和 async/await

在 Rust 中，异步编程围绕 `Future` trait 展开。`Future` 表示一个现在可能还没准备好但将来会变为就绪的值。你在块和函数上应用 `async` 关键字来指定它们可以被中断和恢复。在 async 块或函数内，你使用 `await` 关键字等待 future 完成。每个 `await` 点都是代码可能暂停并让其他工作继续进行的潜在位置。

Future 在 Rust 中是_惰性的_：在你 `.await` 它们之前，它们什么也不做。这类似于迭代器在你调用 `.next()` 之前什么也不做。

Rust 还需要一个_异步运行时_——一个管理异步代码执行的独立 crate。标准库提供了构建块但不提供运行时本身。流行的运行时包括 `tokio` 和 `async-std`。

### Auto 的方法：使用 `~T` 的蓝图

Auto 使用不同的抽象：_蓝图_。蓝图写作 `~T`，意思是"一个最终会产生 `T` 类型值的蓝图"。与 Rust 的 future 不同，蓝图被设计为直接与语言的事件系统和 Actor 模型集成。

关键概念有：

1. **`~T`** — 蓝图类型，表示一个延迟的计算
2. **`on` 块** — 订阅蓝图并处理其结果
3. **`yield`** — 显式将控制权交还运行时
4. **`~join`** — 等待多个蓝图完成
5. **`~race`** — 等待多个蓝图中第一个完成

### 蓝图 vs Future

| 概念 | Rust | Auto |
|------|------|------|
| 延迟类型 | `Future<Output = T>` | `~T` |
| 定义异步工作 | `async fn` / `async {}` | `~T` 表达式 |
| 等待结果 | `.await` | `on` 块 |
| 惰性求值 | Future 默认是惰性的 | 蓝图默认是惰性的 |
| 运行时 | 外部 crate（`tokio` 等） | 内置运行时 |
| 取消 | Drop future | 取消蓝图 |
| 组合器 | `.map()`、`.then()` 等 | `~join`、`~race`、`on` |
| 生成任务 | `tokio::spawn()` | 将蓝图传递给 Actor |

Auto 的内置运行时意味着你不需要选择和配置外部异步运行时。运行时与第 16 章的 Actor 系统集成，使 actor 和异步操作的无缝结合成为可能。

## 创建蓝图

### 基本蓝图创建

在 Auto 中，你通过在类型上使用 `~` 操作符来创建蓝图。最常见的方式是使用蓝图表达式：

<Listing number="17-1" file-name="src/main.at" caption="一个立即解决的简单蓝图">

```auto
fn main() {
    let value = ~5
    on value as v {
        print(f"Got: ${v}")  // Got: 5
    }
}
```

```rust
async fn main() {
    let value = async { 5 };
    let v = value.await;
    println!("Got: {v}");
}
```

</Listing>

表达式 `~5` 创建一个蓝图，当被订阅时会产生值 `5`。`on value as v` 块订阅蓝图并在值可用时将结果绑定到 `v`。

### 蓝图函数

你可以定义返回蓝图的函数。这些函数描述了蓝图被订阅时将发生的工作：

<Listing number="17-2" file-name="src/main.at" caption="返回蓝图的函数">

```auto
fn fetch_data(url String) ~String {
    ~net.get(url).body()
}

fn main() {
    let data = fetch_data("https://example.com")
    on data as result {
        print(f"Got ${result.len()} bytes")
    }
}
```

```rust
async fn fetch_data(url: &str) -> String {
    let response = reqwest::get(url).await.unwrap();
    response.text().await.unwrap()
}

fn main() {
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        let data = fetch_data("https://example.com").await;
        println!("Got {} bytes", data.len());
    });
}
```

</Listing>

函数 `fetch_data` 返回 `~String`——一个最终会产生 `String` 的蓝图。在函数内部，`~` 将网络操作包装在蓝图中。`main` 中的 `on` 块订阅蓝图并处理结果。

与 Rust 的主要区别：

- **函数上没有 `async` 关键字** — 返回类型 `~String` 足以表明这是一个异步函数
- **没有 `.await` 关键字** — 取而代之的是 `on` 块订阅蓝图
- **无需运行时设置** — Auto 的运行时是内置的

### 包含多个步骤的蓝图表达式

蓝图可以包含多个步骤，用 `~` 链接在一起：

<Listing number="17-3" file-name="src/main.at" caption="链式蓝图操作">

```auto
fn page_title(url String) ~?String {
    let response = ~net.get(url)
    let text = ~response.body()
    let parsed = Html.parse(text)
    parsed.select_first("title").map(|t| t.inner_text())
}

fn main() {
    let title = page_title("https://example.com")
    on title as result {
        match result {
            Some(t) -> print(f"Title: ${t}"),
            None -> print("No title found"),
        }
    }
}
```

```rust
async fn page_title(url: &str) -> Option<String> {
    let response_text = reqwest::get(url).await.unwrap().text().await.unwrap();
    Html::parse(&response_text)
        .select_first("title")
        .map(|title| title.inner_html())
}

fn main() {
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        match page_title("https://example.com").await {
            Some(t) => println!("Title: {t}"),
            None => println!("No title found"),
        }
    });
}
```

</Listing>

函数体中的每个 `~` 标记一个蓝图可能暂停并将控制权交给运行时的点。这些是_让步点_——类似于 Rust 的 `.await` 点。运行时可以在每个让步点切换到其他工作，从而实现并发。

### `on` 块的工作方式

`on` 块是 Auto 订阅蓝图并处理其结果的机制。它有几种形式：

```auto
// 基本：处理结果
on blueprint as value {
    // 使用 value
}

// 带错误处理
on blueprint as value catch err {
    // 处理错误
}

// 同时处理多个蓝图
on (a, b) as (x, y) {
    // 使用 x 和 y
}
```

与 Rust 的 `.await`（一个返回值的表达式）不同，`on` 块是在块内处理结果的语句。这种设计使错误处理和多蓝图协调更加自然。

## 使用蓝图实现并发

### 竞赛蓝图

一种常见的模式是启动多个操作并取最先完成的那个。Auto 提供了 `~race`：

<Listing number="17-4" file-name="src/main.at" caption="竞赛两个蓝图">

```auto
fn main() {
    let title1 = page_title("https://www.rust-lang.org")
    let title2 = page_title("https://www.autolang.org")

    let first = ~race(title1, title2)

    on first as result {
        print(f"First result: ${result}")
    }
}
```

```rust
fn main() {
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        let title1 = page_title("https://www.rust-lang.org");
        let title2 = page_title("https://www.autolang.org");

        let (url, maybe_title) =
            match tokio::select!(r = title1 => ("rust-lang", r),
                                 r = title2 => ("autolang", r)) {
                (url, title) => (url, title),
            };

        println!("First result from {url}: {:?}", maybe_title);
    });
}
```

</Listing>

`~race` 返回一个蓝图，它会在任一输入蓝图完成时以该结果解决。另一个蓝图会自动取消。这类似于 Rust 的 `tokio::select!` 宏，但表达为常规函数。

### 连接蓝图

当你需要等待_所有_蓝图完成时，使用 `~join`：

<Listing number="17-5" file-name="src/main.at" caption="连接多个蓝图">

```auto
fn main() {
    let user = ~fetch_user(1)
    let posts = ~fetch_posts(1)

    on ~join(user, posts) as (u, p) {
        print(f"User: ${u.name}, Posts: ${p.len()}")
    }
}
```

```rust
#[tokio::main]
async fn main() {
    let user = fetch_user(1);
    let posts = fetch_posts(1);
    let (u, p) = tokio::join!(user, posts);
    println!("User: {}, Posts: {}", u.name, p.len());
}
```

</Listing>

`~join` 等待所有蓝图完成，并将它们的结果作为元组返回。这等同于 Rust 的 `tokio::join!` 宏。

### 生成后台工作

对于即发即忘的异步操作，你可以生成一个蓝图在后台运行：

<Listing number="17-6" file-name="src/main.at" caption="生成后台蓝图">

```auto
fn main() {
    let task = ~spawn(() => {
        for i in 1..10 {
            print(f"hi number ${i} from spawned task!")
            ~sleep(500)
        }
    })

    for i in 1..5 {
        print(f"hi number ${i} from main!")
        ~sleep(500)
    }

    on task as _ {
        print("Spawned task completed")
    }
}
```

```rust
use std::time::Duration;

#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        for i in 1..10 {
            println!("hi number {i} from spawned task!");
            tokio::time::sleep(Duration::from_millis(500)).await;
        }
    });

    for i in 1..5 {
        println!("hi number {i} from main!");
        tokio::time::sleep(Duration::from_millis(500)).await;
    }

    handle.await.unwrap();
    println!("Spawned task completed");
}
```

</Listing>

`~spawn` 函数在后台启动一个蓝图运行，类似于 `tokio::spawn`。主工作立即继续。`on task as _` 块等待生成的任务完成。

## 蓝图之间的消息传递

蓝图可以通过通道进行通信，类似于我们在第 16 章中看到的 Actor 模型。Auto 提供了与蓝图自然集成的异步通道：

<Listing number="17-7" file-name="src/main.at" caption="蓝图之间的消息传递">

```auto
fn main() {
    let (tx, rx) = ~channel()

    let sender = ~spawn(() => {
        let messages = ["hello", "from", "blueprint", "world"]
        for msg in messages {
            tx.send(msg)
            ~sleep(500)
        }
    })

    let receiver = ~spawn(() => {
        on rx.recv() as msg {
            print(f"Received: ${msg}")
        }
    })

    on ~join(sender, receiver) as _ {
        print("Done")
    }
}
```

```rust
use std::time::Duration;
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel(32);

    let sender = tokio::spawn(async move {
        let messages = vec!["hello", "from", "async", "world"];
        for msg in messages {
            tx.send(msg).await.unwrap();
            tokio::time::sleep(Duration::from_millis(500)).await;
        }
    });

    let receiver = tokio::spawn(async move {
        while let Some(msg) = rx.recv().await {
            println!("Received: {msg}");
        }
    });

    tokio::join!(sender, receiver);
    println!("Done");
}
```

</Listing>

`~channel` 函数创建一个异步通道。发送是非阻塞的。`rx.recv()` 调用产生一个蓝图，当消息到达时解决。

与 Rust 的主要区别：

- **send 不需要 `.await`** — 发送是同步且即时的
- **`on rx.recv()`** — 订阅接收蓝图以等待消息
- **无需 `move` 闭包** — Auto 的隐式 move 自动处理所有权

### 多个发送者

与 Rust 的通道一样，Auto 的异步通道支持多个发送者：

<Listing number="17-8" file-name="src/main.at" caption="一个通道上的多个发送者">

```auto
fn main() {
    let (tx, rx) = ~channel()

    let tx1 = tx.clone()
    let sender1 = ~spawn(() => {
        let messages = ["hello", "from", "task", "one"]
        for msg in messages {
            tx1.send(msg)
            ~sleep(500)
        }
    })

    let sender2 = ~spawn(() => {
        let messages = ["more", "messages", "for", "you"]
        for msg in messages {
            tx.send(msg)
            ~sleep(1500)
        }
    })

    let receiver = ~spawn(() => {
        on rx.recv() as msg {
            print(f"Received: ${msg}")
        }
    })

    on ~join(sender1, sender2, receiver) as _ {}
}
```

```rust
use std::time::Duration;
use tokio::sync::mpsc;

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel(32);

    let tx1 = tx.clone();
    let sender1 = tokio::spawn(async move {
        let messages = vec!["hello", "from", "task", "one"];
        for msg in messages {
            tx1.send(msg).await.unwrap();
            tokio::time::sleep(Duration::from_millis(500)).await;
        }
    });

    let sender2 = tokio::spawn(async move {
        let messages = vec!["more", "messages", "for", "you"];
        for msg in messages {
            tx.send(msg).await.unwrap();
            tokio::time::sleep(Duration::from_millis(1500)).await;
        }
    });

    let receiver = tokio::spawn(async move {
        while let Some(msg) = rx.recv().await {
            println!("Received: {msg}");
        }
    });

    tokio::join!(sender1, sender2, receiver);
}
```

</Listing>

## 让出控制

### 协作式多任务

Auto 的异步模型使用_协作式多任务_。蓝图运行直到遇到让步点（一个 `~` 操作），然后将控制权交还运行时。在让步点之间，代码同步运行。这意味着没有让步点的长时间计算会_饿死_其他蓝图。

<Listing number="17-9" file-name="src/main.at" caption="慢速计算饿死其他蓝图">

```auto
fn slow(name String, ms int) {
    // 模拟阻塞操作
    thread.sleep(Duration.from_millis(ms))
    print(f"'${name}' ran for ${ms}ms")
}

fn main() {
    let a = () => {
        print("'a' started")
        slow("a", 30)
        slow("a", 10)
        slow("a", 20)
        ~sleep(50)
        print("'a' finished")
    }

    let b = () => {
        print("'b' started")
        slow("b", 75)
        slow("b", 10)
        slow("b", 15)
        slow("b", 350)
        ~sleep(50)
        print("'b' finished")
    }

    on ~race(~spawn(a), ~spawn(b)) as _ {}
}
```

```rust
use std::thread;
use std::time::Duration;

fn slow(name: &str, ms: u64) {
    thread::sleep(Duration::from_millis(ms));
    println!("'{name}' ran for {ms}ms");
}

#[tokio::main]
async fn main() {
    let a = async {
        println!("'a' started");
        slow("a", 30);
        slow("a", 10);
        slow("a", 20);
        tokio::time::sleep(Duration::from_millis(50)).await;
        println!("'a' finished");
    };

    let b = async {
        println!("'b' started");
        slow("b", 75);
        slow("b", 10);
        slow("b", 15);
        slow("b", 350);
        tokio::time::sleep(Duration::from_millis(50)).await;
        println!("'b' finished");
    };

    tokio::select! {
        _ = a => {},
        _ = b => {},
    }
}
```

</Listing>

在 `slow` 调用之间没有让步点，一个蓝图会在另一个获得机会之前运行完所有慢速操作。末尾的 `~sleep(50)` 是唯一的让步点。

### 使用 `~yield` 协作

要解决这个问题，在长时间运行的操作之间添加显式让步点：

<Listing number="17-10" file-name="src/main.at" caption="使用 `~yield` 与其他蓝图协作">

```auto
fn main() {
    let a = () => {
        print("'a' started")
        slow("a", 30)
        ~yield
        slow("a", 10)
        ~yield
        slow("a", 20)
        ~yield
        print("'a' finished")
    }

    let b = () => {
        print("'b' started")
        slow("b", 75)
        ~yield
        slow("b", 10)
        ~yield
        slow("b", 15)
        ~yield
        slow("b", 350)
        ~yield
        print("'b' finished")
    }

    on ~race(~spawn(a), ~spawn(b)) as _ {}
}
```

```rust
#[tokio::main]
async fn main() {
    let a = async {
        println!("'a' started");
        slow("a", 30);
        tokio::task::yield_now().await;
        slow("a", 10);
        tokio::task::yield_now().await;
        slow("a", 20);
        tokio::task::yield_now().await;
        println!("'a' finished");
    };

    let b = async {
        println!("'b' started");
        slow("b", 75);
        tokio::task::yield_now().await;
        slow("b", 10);
        tokio::task::yield_now().await;
        slow("b", 15);
        tokio::task::yield_now().await;
        slow("b", 350);
        tokio::task::yield_now().await;
        println!("'b' finished");
    };

    tokio::select! {
        _ = a => {},
        _ = b => {},
    }
}
```

</Listing>

`~yield` 表达式创建一个立即将控制权交还运行时的蓝图，允许其他蓝图取得进展。这等同于 Rust 的 `tokio::task::yield_now().await`。现在慢速操作会在两个蓝图之间交错执行。

在需要与运行时中的其他蓝图共享计算量的繁重工作时使用 `~yield`。不要过度使用——让步有少量开销，有些操作最好不打断地运行。

## 构建自定义异步抽象

蓝图可以自然地组合。你可以从更简单的蓝图构建更高级的抽象。让我们构建一个 `timeout` 函数：

<Listing number="17-11" file-name="src/main.at" caption="从蓝图构建超时功能">

```auto
fn timeout<T>(blueprint ~T, max_time Duration) ~!T {
    ~match ~race(blueprint, ~sleep(max_time)) {
        Success(value) -> Ok(value)
        TimedOut -> Err(max_time)
    }
}

fn main() {
    let slow = ~() => {
        ~sleep(5000)
        "Finally finished"
    }

    let result = timeout(slow, Duration.from_secs(2))

    on result as outcome {
        match outcome {
            Ok(message) -> print(f"Succeeded with '${message}'"),
            Err(duration) -> print(f"Failed after ${duration.as_secs()} seconds"),
        }
    }
}
```

```rust
use std::time::Duration;
use tokio::select;

async fn timeout<T>(future: impl std::future::Future<Output = T>,
                    max_time: Duration) -> Result<T, Duration> {
    select! {
        output = future => Ok(output),
        _ = tokio::time::sleep(max_time) => Err(max_time),
    }
}

#[tokio::main]
async fn main() {
    let slow = async {
        tokio::time::sleep(Duration::from_secs(5)).await;
        "Finally finished"
    };

    match timeout(slow, Duration::from_secs(2)).await {
        Ok(message) => println!("Succeeded with '{message}'"),
        Err(duration) => {
            println!("Failed after {} seconds", duration.as_secs())
        }
    }
}
```

</Listing>

`timeout` 函数将用户的蓝图与睡眠计时器进行竞赛。如果蓝图先完成，它返回 `Ok` 和结果。如果计时器先触发，它返回 `Err` 和经过的时长。这与 Rust 的 `tokio::select!` 是相同的模式，但表达为常规函数。

因为蓝图可以与其他蓝图组合，你可以从小的构建块构建强大的工具——进而将这些工具与网络调用、重试等操作结合使用。

## 蓝图与 Actor

Auto 的蓝图与第 16 章的 Actor 模型集成。Actor 可以发送和接收蓝图，蓝图也可以与 Actor 交互：

<Listing number="17-12" file-name="src/main.at" caption="将蓝图与 Actor 结合">

```auto
actor Fetcher {
    on Fetch(url String) ~String {
        let response = ~net.get(url)
        ~response.body()
    }
}

fn main() {
    let fetcher = Fetcher.init()

    let result = fetcher.ask(Fetch("https://example.com"))

    on result as body {
        print(f"Got ${body.len()} bytes")
    }
}
```

```rust
use std::sync::{Arc, Mutex};

struct Fetcher;

impl Fetcher {
    async fn fetch(&self, url: &str) -> String {
        let response = reqwest::get(url).await.unwrap();
        response.text().await.unwrap()
    }
}

#[tokio::main]
async fn main() {
    let fetcher = Fetcher;
    let body = fetcher.fetch("https://example.com").await;
    println!("Got {} bytes", body.len());
}
```

</Listing>

当 Actor 的 `on` 处理器返回蓝图类型（`~String`）时，`ask` 操作返回一个蓝图，它在 Actor 完成处理消息时解决。这意味着你可以使用 `on` 等待结果而不阻塞。

### 何时使用蓝图 vs Actor

| 场景 | 使用蓝图 | 使用 Actor |
|------|---------|-----------|
| 单个异步操作 | 是 | 否 |
| 流式数据 | 是（使用 `~stream`） | 否 |
| 有状态的服务 | 否 | 是 |
| 基于消息的工作流 | 两者皆可 | 首选 |
| CPU 密集型并行 | 有限 | 有限（使用线程） |
| 网络 I/O | 是 | 可以 |
| 共享可变状态 | 否 | 是（封装的） |

在实践中，大多数 Auto 程序结合使用两者：Actor 用于长期存活的有状态服务，蓝图用于单个异步操作。

## 蓝图速查表

| 功能 | Auto（`~T`） | Rust（`Future`） |
|------|-------------|-----------------|
| 延迟类型 | `~T` | `impl Future<Output = T>` |
| 定义异步函数 | `fn name() ~T { }` | `async fn name() -> T { }` |
| 等待结果 | `on bp as v { }` | `let v = bp.await;` |
| 竞赛 | `~race(a, b)` | `tokio::select!` |
| 等待全部 | `~join(a, b)` | `tokio::join!(a, b)` |
| 生成后台任务 | `~spawn(() => { })` | `tokio::spawn(async { })` |
| 让出控制 | `~yield` | `yield_now().await` |
| 睡眠 | `~sleep(ms)` | `tokio::time::sleep(d).await` |
| 通道 | `~channel()` | `tokio::sync::mpsc::channel()` |
| 错误类型 | `!T`（在蓝图中） | `Result<T, E>` |
| 运行时 | 内置 | 外部 crate |
| 可组合性 | 蓝图可组合 | Future 可组合 |

## 总结

Auto 的 `~T` 蓝图系统提供了一种与 Rust 基于 `Future` 的模型不同的异步编程方法：

1. **`~T` 蓝图** — 产生 `T` 类型值的延迟计算
2. **`on` 块** — 订阅蓝图并处理结果，替代 `.await`
3. **`~race` 和 `~join`** — 并发组合多个蓝图
4. **`~yield`** — 显式与运行时协作
5. **`~spawn`** — 在后台运行蓝图
6. **`~channel`** — 蓝图之间的异步消息传递
7. **内置运行时** — 无需外部运行时 crate
8. **Actor 集成** — 蓝图和 Actor 无缝协作

蓝图用 Rust `Future` trait 的细粒度控制换取了更精简、集成的体验。内置运行时消除了选择和配置外部异步基础设施的需要，`on` 块语法使错误处理和多蓝图协调变得自然。

在下一章，我们将探讨 Auto 中的面向对象模式，以及 `is`/`has`/`spec` 系统与 Rust 的 trait 对象的比较。
