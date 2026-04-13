# 最终项目：使用 Actor 构建Web 服务器

这是一段漫长的旅程，但我们已经到达了书的末尾。在本章中，我们将一起构建一个项目，以演示最后几章中涵盖的一些概念，同时回顾早期的一些经验。

对于我们的最终项目，我们将制作一个显示"Hello!"的 Web 服务器。

以下是我们构建 Web 服务器的计划：

1. 了解一些关于 TCP 和 HTTP 的知识。
2. 在套接字上监听 TCP 连接。
3. 解析少量 HTTP 请求。
4. 创建正确的 HTTP 响应。
5. 使用 Auto 的 Actor 模型提高服务器的吞吐量。

在开始之前，我们应该提到两个细节。首先，我们将使用的方法不是用 Auto 构建 Web 服务器的最佳方式。社区成员可能会发布提供更完整 Web 服务器实现的生产就绪包。然而，我们在本章的意图是帮助你学习，而不是走捷径。

其次，我们将使用 Auto 第 16 章中的 Actor 模型，而不是像 Rust 中那样使用线程和线程池。Actor 为并发请求处理提供了自然的模型：每个连接由自己的 actor 处理，监听器 actor 分发传入的连接。

## 构建单线程 Web 服务器

### 监听 TCP 连接

我们的 Web 服务器需要监听 TCP 连接。让我们创建一个新项目：

```bash
$ automan new hello
     Created binary (application) `hello` project
$ cd hello
```

<Listing number="21-1" file-name="src/main.at" caption="监听传入的流并打印消息">

```auto
use.net TcpListener

fn main() {
    let listener = TcpListener.bind("127.0.0.1:7878")!

    for stream in listener.incoming() {
        let stream = stream!
        print("Connection established!")
    }
}
```

```rust
use std::net::TcpListener;

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        println!("Connection established!");
    }
}
```

</Listing>

使用 `TcpListener`，我们可以在地址 `127.0.0.1:7878` 上监听 TCP 连接。在地址中，冒号之前的部分是代表你计算机的 IP 地址，`7878` 是端口。

`bind` 函数返回 `!TcpListener`——Auto 的错误传播类型，等同于 `Result<TcpListener, Error>`。我们使用 `!` 来解包它，出错时会 panic（类似于 Rust 中的 `.unwrap()`）。

`incoming` 方法返回一个迭代器，为我们提供一系列流。单个_流_代表客户端和服务器之间的开放连接。

### 读取请求

让我们实现从浏览器读取请求的功能：

<Listing number="21-2" file-name="src/main.at" caption="从 TcpStream 读取数据并打印">

```auto
use.net {TcpListener, TcpStream}
use.io {BufReader, BufRead}

fn main() {
    let listener = TcpListener.bind("127.0.0.1:7878")!

    for stream in listener.incoming() {
        let stream = stream!
        handle_connection(stream)
    }
}

fn handle_connection(stream TcpStream) {
    let buf_reader = BufReader.new(&stream)
    let http_request = buf_reader
        .lines()
        .map(|result| result!)
        .take_while(|line| !line.is_empty())
        .collect(List<String>)

    print(f"Request: {http_request}")
}
```

```rust
use std::{
    io::{BufReader, BufRead, Write},
    net::{TcpListener, TcpStream},
};

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        handle_connection(stream);
    }
}

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    println!("Request: {http_request:#?}");
}
```

</Listing>

我们使用 `BufReader` 从 TCP 流读取数据，并将 HTTP 请求行收集到 `List<String>` 中。浏览器通过发送两个连续换行符来表示 HTTP 请求的结束，所以我们取行直到遇到空行。

### 写入响应

HTTP 响应具有特定的格式：

```
HTTP-Version Status-Code Reason-Phrase CRLF
headers CRLF
message-body
```

让我们发送一个响应：

<Listing number="21-3" file-name="src/main.at" caption="写入一个简单的成功 HTTP 响应">

```auto
use.net {TcpListener, TcpStream}
use.io {BufReader, BufRead, Write}

fn main() {
    let listener = TcpListener.bind("127.0.0.1:7878")!

    for stream in listener.incoming() {
        let stream = stream!
        handle_connection(stream)
    }
}

fn handle_connection(mut stream TcpStream) {
    let buf_reader = BufReader.new(&stream)
    let http_request = buf_reader
        .lines()
        .map(|result| result!)
        .take_while(|line| !line.is_empty())
        .collect(List<String>)

    let response = "HTTP/1.1 200 OK\r\n\r\n"
    stream.write_all(response.as_bytes())!
}
```

```rust
use std::{
    io::{BufReader, BufRead, Write},
    net::{TcpListener, TcpStream},
};

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        handle_connection(stream);
    }
}

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let http_request: Vec<_> = buf_reader
        .lines()
        .map(|result| result.unwrap())
        .take_while(|line| !line.is_empty())
        .collect();

    let response = "HTTP/1.1 200 OK\r\n\r\n";
    stream.write_all(response.as_bytes()).unwrap();
}
```

</Listing>

### 返回真正的 HTML

让我们返回实际的 HTML 内容。创建一个 `hello.html` 文件：

<Listing number="21-4" file-name="hello.html" caption="要返回的示例 HTML 文件">

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Hello!</title>
  </head>
  <body>
    <h1>Hello!</h1>
    <p>Hi from Auto</p>
  </body>
</html>
```

</Listing>

现在修改 `handle_connection` 以返回 HTML 文件：

<Listing number="21-5" file-name="src/main.at" caption="将 hello.html 的内容作为响应体发送">

```auto
fn handle_connection(mut stream TcpStream) {
    let buf_reader = BufReader.new(&stream)
    let request_line = buf_reader.lines().next()!!

    let (status_line, filename) = if request_line == "GET / HTTP/1.1" {
        ("HTTP/1.1 200 OK", "hello.html")
    } else {
        ("HTTP/1.1 404 NOT FOUND", "404.html")
    }

    let contents = fs.read_to_string(filename)!
    let length = contents.len()

    let response = f"{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}"
    stream.write_all(response.as_bytes())!
}
```

```rust
fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let request_line = buf_reader.lines().next().unwrap().unwrap();

    let (status_line, filename) = if request_line == "GET / HTTP/1.1" {
        ("HTTP/1.1 200 OK", "hello.html")
    } else {
        ("HTTP/1.1 404 NOT FOUND", "404.html")
    };

    let contents = fs::read_to_string(filename).unwrap();
    let length = contents.len();

    let response =
        format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");
    stream.write_all(response.as_bytes()).unwrap();
}
```

</Listing>

我们检查请求行，对 `/` 的请求提供 `hello.html`，其他任何请求返回 `404.html`。你还需要创建一个 `404.html` 文件：

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Hello!</title>
  </head>
  <body>
    <h1>Oops!</h1>
    <p>Sorry, I don't know what you're asking for.</p>
  </body>
</html>
```

太棒了！我们现在有一个简单的 Web 服务器，对一种请求返回内容页面，对所有其他请求返回 404 响应。

目前，我们的服务器在单线程中运行，意味着它一次只能处理一个请求。让我们使用 Auto 的 Actor 模型来解决这个问题。

## 从单线程到基于 Actor 的服务器

### 单线程的问题

目前，服务器按顺序处理每个请求，意味着在第一个连接处理完成之前不会处理第二个连接。如果服务器接收到越来越多的请求，这种串行执行会越来越不理想。

### 模拟慢速请求

让我们添加一个 `/sleep` 端点来看看问题：

<Listing number="21-6" file-name="src/main.at" caption="使用 /sleep 模拟慢速请求">

```auto
fn handle_connection(mut stream TcpStream) {
    let buf_reader = BufReader.new(&stream)
    let request_line = buf_reader.lines().next()!!

    let (status_line, filename) = if request_line == "GET / HTTP/1.1" {
        ("HTTP/1.1 200 OK", "hello.html")
    } else if request_line == "GET /sleep HTTP/1.1" {
        thread.sleep(Duration.from_secs(5))
        ("HTTP/1.1 200 OK", "hello.html")
    } else {
        ("HTTP/1.1 404 NOT FOUND", "404.html")
    }

    let contents = fs.read_to_string(filename)!
    let length = contents.len()

    let response = f"{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}"
    stream.write_all(response.as_bytes())!
}
```

```rust
fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let request_line = buf_reader.lines().next().unwrap().unwrap();

    let (status_line, filename) = match &request_line[..] {
        "GET / HTTP/1.1" => ("HTTP/1.1 200 OK", "hello.html"),
        "GET /sleep HTTP/1.1" => {
            thread::sleep(Duration::from_secs(5));
            ("HTTP/1.1 200 OK", "hello.html")
        }
        _ => ("HTTP/1.1 404 NOT FOUND", "404.html"),
    };

    let contents = fs::read_to_string(filename).unwrap();
    let length = contents.len();

    let response =
        format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");
    stream.write_all(response.as_bytes()).unwrap();
}
```

</Listing>

如果你在一个浏览器标签页中打开 `/sleep`，在另一个中打开 `/`，第二个请求将不得不等待五秒睡眠结束。这是因为我们的服务器顺序处理连接。

### 使用 Actor 实现并发

在 Rust 中，解决方案是线程池。在 Auto 中，我们使用 Actor 模型（第 16 章）。我们将创建一个 `Worker` actor 来并发处理连接：

<Listing number="21-7" file-name="src/main.at" caption="用于处理连接的 Worker actor">

```auto
use.net {TcpListener, TcpStream}
use.io {BufReader, BufRead, Write}

actor Worker {
    on Handle(stream TcpStream) {
        handle_connection(stream)
    }
}

actor Server {
    on Start() {
        let listener = TcpListener.bind("127.0.0.1:7878")!

        for stream in listener.incoming() {
            let stream = stream!
            let worker = Worker.init()
            worker.tell(Handle(stream))
        }
    }
}

fn main() {
    let server = Server.init()
    server.tell(Start())
}
```

```rust
use std::{
    fs,
    io::{BufReader, BufRead, Write},
    net::{TcpListener, TcpStream},
    sync::{Arc, Mutex, mpsc},
    thread,
};

// 在 Rust 中，你需要一个带有 worker 的 ThreadPool 结构体、
// 用于任务分发的通道，以及 Arc<Mutex<...>>
// 参见 Rust Book 的完整实现。

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    let pool = ThreadPool::new(4);

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        pool.execute(|| {
            handle_connection(stream);
        });
    }
}
```

</Listing>

每个传入的连接都会创建一个新的 `Worker` actor。`Worker` actor 接收一个带有 TCP 流的 `Handle` 消息，并独立处理连接。由于 actor 并发运行，多个请求可以并行处理而不会互相阻塞。

这比 Rust 的线程池方法简单得多。在 Rust 中，你需要：

- 一个带有 `Worker` 线程向量的 `ThreadPool` 结构体
- 用于向 worker 发送任务的通道（`mpsc`）
- `Arc<Mutex<...>>` 用于共享对接收器的访问
- 手动 `Drop` 实现用于优雅关闭

在 Auto 中，actor 自动处理所有这些：

| 关注点 | Rust（线程池） | Auto（Actor） |
|--------|---------------|---------------|
| 并发执行 | `thread::spawn` | Actor `init()` |
| 任务分发 | `mpsc` 通道 | `tell()` 消息 |
| 共享状态 | `Arc<Mutex<T>>` | Actor 内部状态 |
| 优雅关闭 | 手动 `Drop` 实现 | Actor 生命周期 |
| 样板代码 | ~80 行 | ~15 行 |

### Worker 池 Actor

为了更好的资源管理，我们可以创建一个池 actor 来管理固定数量的 worker actor：

<Listing number="21-8" file-name="src/main.at" caption="管理多个 worker 的 worker 池 actor">

```auto
actor WorkerPool {
    workers List<Worker>

    on Init(size int) {
        var workers = List<Worker>()
        for i in 0..size {
            workers.push(Worker.init())
        }
        .workers = workers
    }

    on Handle(stream TcpStream) {
        // 选择下一个可用的 worker（轮询）
        let worker = .workers.pop()
        worker.tell(Handle(stream))
        .workers.unshift(worker)
    }
}

actor Server {
    on Start() {
        let listener = TcpListener.bind("127.0.0.1:7878")!
        let pool = WorkerPool.init()
        pool.tell(Init(4))

        for stream in listener.incoming() {
            let stream = stream!
            pool.tell(Handle(stream))
        }
    }
}

fn main() {
    let server = Server.init()
    server.tell(Start())
}
```

```rust
use std::{
    sync::{Arc, Mutex, mpsc},
    thread,
};

pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: Option<mpsc::Sender<Job>>,
}

type Job = Box<dyn FnOnce() + Send + 'static>;

impl ThreadPool {
    pub fn new(size: usize) -> ThreadPool {
        assert!(size > 0);

        let (sender, receiver) = mpsc::channel();
        let receiver = Arc::new(Mutex::new(receiver));

        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id, Arc::clone(&receiver)));
        }

        ThreadPool { workers, sender: Some(sender) }
    }

    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);
        self.sender.as_ref().unwrap().send(job).unwrap();
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        drop(self.sender.take());

        for worker in self.workers.drain(..) {
            println!("Shutting down worker {}", worker.id);
            worker.thread.join().unwrap();
        }
    }
}

struct Worker {
    id: usize,
    thread: Option<thread::JoinHandle<()>>,
}

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Worker {
        let thread = thread::spawn(move || {
            loop {
                let message = receiver.lock().unwrap().recv();

                match message {
                    Ok(job) => {
                        println!("Worker {id} got a job; executing.");
                        job();
                    }
                    Err(_) => {
                        println!("Worker {id} disconnected; shutting down.");
                        break;
                    }
                }
            }
        });

        Worker { id, thread: Some(thread) }
    }
}
```

</Listing>

`WorkerPool` actor 维护一个 worker actor 列表，使用轮询调度在它们之间分发连接。每个 worker 独立处理其连接。如果某个 worker 正忙，池会将连接分配给下一个可用的 worker。

### 优雅关闭

Auto 中的 actor 自然支持优雅关闭。当服务器 actor 停止时，所有子 worker 都会收到通知，可以完成处理当前的连接：

<Listing number="21-9" file-name="src/main.at" caption="使用 actor 实现优雅关闭">

```auto
actor Worker {
    running bool

    on Init() {
        .running = true
    }

    on Handle(stream TcpStream) {
        if .running {
            handle_connection(stream)
        }
    }

    on Stop() {
        .running = false
        print("Worker shutting down")
    }
}

actor Server {
    pool WorkerPool

    on Start() {
        let listener = TcpListener.bind("127.0.0.1:7878")!
        .pool = WorkerPool.init()
        .pool.tell(Init(4))

        // 有限时间内接受连接（演示用途）
        var count = 0
        for stream in listener.incoming() {
            let stream = stream!
            .pool.tell(Handle(stream))
            count += 1
            if count >= 2 {
                break
            }
        }

        // 优雅关闭
        .pool.tell(Stop())
        print("Server shutting down")
    }
}

fn main() {
    let server = Server.init()
    server.tell(Start())
}
```

```rust
use hello::ThreadPool;
use std::{
    fs,
    io::{BufReader, BufRead, Write},
    net::{TcpListener, TcpStream},
    thread,
    time::Duration,
};

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    let pool = ThreadPool::new(4);

    for stream in listener.incoming().take(2) {
        let stream = stream.unwrap();

        pool.execute(|| {
            handle_connection(stream);
        });
    }

    println!("Shutting down.");
}
```

</Listing>

## 完整服务器代码

以下是完整的服务器实现：

<Listing number="21-10" file-name="src/main.at" caption="使用 Actor 模型的完整 Web 服务器">

```auto
use.net {TcpListener, TcpStream}
use.io {BufReader, BufRead, Write}
use.fs
use.thread
use.time Duration

// -- 连接处理器 --

fn handle_connection(stream TcpStream) {
    let buf_reader = BufReader.new(&stream)
    let request_line = buf_reader.lines().next()!!

    let (status_line, filename) = if request_line == "GET / HTTP/1.1" {
        ("HTTP/1.1 200 OK", "hello.html")
    } else if request_line == "GET /sleep HTTP/1.1" {
        thread.sleep(Duration.from_secs(5))
        ("HTTP/1.1 200 OK", "hello.html")
    } else {
        ("HTTP/1.1 404 NOT FOUND", "404.html")
    }

    let contents = fs.read_to_string(filename)!
    let length = contents.len()

    let response = f"{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}"
    stream.write_all(response.as_bytes())!
}

// -- Worker Actor --

actor Worker {
    on Handle(stream TcpStream) {
        handle_connection(stream)
    }
}

// -- Worker 池 Actor --

actor WorkerPool {
    workers List<Worker>

    on Init(size int) {
        var workers = List<Worker>()
        for i in 0..size {
            workers.push(Worker.init())
        }
        .workers = workers
    }

    on Handle(stream TcpStream) {
        let worker = .workers.pop()
        worker.tell(Handle(stream))
        .workers.unshift(worker)
    }

    on Stop() {
        print("Pool shutting down")
    }
}

// -- 服务器 Actor --

actor Server {
    on Start() {
        let listener = TcpListener.bind("127.0.0.1:7878")!
        let pool = WorkerPool.init()
        pool.tell(Init(4))

        for stream in listener.incoming() {
            let stream = stream!
            pool.tell(Handle(stream))
        }
    }
}

// -- 入口点 --

fn main() {
    let server = Server.init()
    server.tell(Start())
}
```

```rust
use hello::ThreadPool;
use std::{
    fs,
    io::{BufReader, BufRead, Write},
    net::{TcpListener, TcpStream},
    thread,
    time::Duration,
};

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    let pool = ThreadPool::new(4);

    for stream in listener.incoming() {
        let stream = stream.unwrap();

        pool.execute(|| {
            handle_connection(stream);
        });
    }

    println!("Shutting down.");
}

fn handle_connection(mut stream: TcpStream) {
    let buf_reader = BufReader::new(&stream);
    let request_line = buf_reader.lines().next().unwrap().unwrap();

    let (status_line, filename) = match &request_line[..] {
        "GET / HTTP/1.1" => ("HTTP/1.1 200 OK", "hello.html"),
        "GET /sleep HTTP/1.1" => {
            thread::sleep(Duration::from_secs(5));
            ("HTTP/1.1 200 OK", "hello.html")
        }
        _ => ("HTTP/1.1 404 NOT FOUND", "404.html"),
    };

    let contents = fs::read_to_string(filename).unwrap();
    let length = contents.len();

    let response =
        format!("{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}");
    stream.write_all(response.as_bytes()).unwrap();
}
```

</Listing>

## Auto vs Rust：Web 服务器比较

| 方面 | Rust（线程池） | Auto（Actor 模型） |
|------|---------------|---------------------|
| 并发单元 | 操作系统线程 | Actor |
| 任务分发 | `mpsc` 通道 + `Arc<Mutex>` | `tell()` 消息 |
| 共享状态 | `Arc<Mutex<T>>` | Actor 内部状态 |
| Worker 创建 | `thread::spawn` | `Worker.init()` |
| 优雅关闭 | 手动 `Drop` + `Option::take` | Actor `Stop` 消息 |
| 池代码量 | ~80 行 | ~25 行 |
| 容易出错的地方 | `Arc<Mutex<Receiver>>` | 极少 |
| 内存安全 | 借用检查器 | AutoFree + 消息隔离 |

Auto 的 Actor 模型消除了 Rust 线程池所需的复杂 `Arc<Mutex<...>>` 模式。每个 actor 拥有自己的状态，通信通过消息进行，从设计上使数据竞争变得不可能。

## 增强建议

如果你想继续增强这个项目，以下是一些建议：

- 为 `Worker` actor 添加每个请求的日志
- 使用 `~T` 蓝图（第 17 章）进行异步请求处理
- 使用 `Router` actor 添加请求路由
- 实现 actor 消息拦截器形式的中间件
- 为 `handle_connection` 函数添加测试
- 为消息类型使用 `#derive[Debug]`

## 总结

做得好！你已经读完了整本书！在这个最终项目中，我们构建了一个 Web 服务器，使用了许多 Auto 特性：

1. **基本 I/O** — 从 TCP 流读取、写入响应和读取文件
2. **使用 `is` 进行模式匹配** — 匹配 HTTP 请求行
3. **使用 `!T` 进行错误处理** — 使用 `!` 进行可能失败的操作
4. **Actor 模型** — 使用 actor 进行并发请求处理，而不是线程池
5. **消息传递** — 使用 `tell()` 在 actor 之间分发工作
6. **类型系统** — 定义消息类型和 actor 状态

关键要点是，Auto 的 Actor 模型为并发服务器实现提供了比线程池更简单、更安全的替代方案。Rust 需要 `Arc<Mutex<>>`、通道和手动 `Drop` 实现，而 Auto 使用带消息传递的 actor——一种从构造上消除数据竞争同时保持代码简洁易读的模型。

感谢你加入我们的 Auto 之旅。你现在准备好实现自己的 Auto 项目并帮助他人的项目了。继续构建吧！
