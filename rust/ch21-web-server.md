# Final Project: Building a Web Server with Actors

It's been a long journey, but we've reached the end of the book. In this
chapter, we'll build one more project together to demonstrate some of the
concepts we covered in the final chapters, as well as recap some earlier
lessons.

For our final project, we'll make a web server that says "Hello!" and looks like
Figure 21-1 in a web browser.

Here is our plan for building the web server:

1. Learn a bit about TCP and HTTP.
2. Listen for TCP connections on a socket.
3. Parse a small number of HTTP requests.
4. Create a proper HTTP response.
5. Improve the throughput of our server with Auto's Actor model.

Before we get started, we should mention two details. First, the method we'll
use won't be the best way to build a web server with Auto. Community members
may publish production-ready packages that provide more complete web server
implementations. However, our intention in this chapter is to help you learn,
not to take the easy route.

Second, instead of using threads and a thread pool as you would in Rust, we'll
use Auto's Actor model from Chapter 16. Actors provide a natural model for
concurrent request handling: each connection is handled by its own actor, and
a listener actor distributes incoming connections.

## Building a Single-Threaded Web Server

### Listening to the TCP Connection

Our web server needs to listen to a TCP connection. Let's make a new project:

```bash
$ automan new hello
     Created binary (application) `hello` project
$ cd hello
```

<Listing number="21-1" file-name="src/main.at" caption="Listening for incoming streams and printing a message">

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

Using `TcpListener`, we can listen for TCP connections at the address
`127.0.0.1:7878`. In the address, the section before the colon is an IP address
representing your computer, and `7878` is the port.

The `bind` function returns a `!TcpListener` — Auto's error-propagating type
equivalent to `Result<TcpListener, Error>`. We use `!` to unwrap it, which
would panic on error (similar to `.unwrap()` in Rust).

The `incoming` method returns an iterator that gives us a sequence of streams.
A single _stream_ represents an open connection between the client and the
server.

### Reading the Request

Let's implement the functionality to read the request from the browser:

<Listing number="21-2" file-name="src/main.at" caption="Reading from the TcpStream and printing the data">

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

We read from the TCP stream using a `BufReader` and collect the HTTP request
lines into a `List<String>`. The browser signals the end of an HTTP request by
sending two newline characters in a row, so we take lines until we get an empty
line.

### Writing a Response

HTTP responses have a specific format:

```
HTTP-Version Status-Code Reason-Phrase CRLF
headers CRLF
message-body
```

Let's send a response:

<Listing number="21-3" file-name="src/main.at" caption="Writing a tiny successful HTTP response">

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

### Returning Real HTML

Let's return actual HTML content. Create a `hello.html` file:

<Listing number="21-4" file-name="hello.html" caption="A sample HTML file to return">

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

Now modify `handle_connection` to return the HTML file:

<Listing number="21-5" file-name="src/main.at" caption="Sending the contents of hello.html as the response body">

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

We check the request line and serve either `hello.html` for requests to `/` or
`404.html` for anything else. You'll need to create a `404.html` file as well:

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

Awesome! We now have a simple web server that responds to one request with a
page of content and responds to all other requests with a 404 response.

Currently, our server runs in a single thread, meaning it can only serve one
request at a time. Let's fix that using Auto's Actor model.

## From Single-Threaded to Actor-Based Server

### The Problem with Single Threading

Right now, the server will process each request in turn, meaning it won't
process a second connection until the first connection is finished processing.
If the server received more and more requests, this serial execution would be
less and less optimal.

### Simulating a Slow Request

Let's add a `/sleep` endpoint to see the problem:

<Listing number="21-6" file-name="src/main.at" caption="Simulating a slow request with /sleep">

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

If you open `/sleep` in one browser tab and `/` in another, the second request
will have to wait until the five-second sleep finishes. This is because our
server handles connections sequentially.

### Using Actors for Concurrency

In Rust, the solution would be a thread pool. In Auto, we use the Actor model
(Chapter 16). We'll create a `Worker` actor that handles connections
concurrently:

<Listing number="21-7" file-name="src/main.at" caption="A Worker actor for handling connections">

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

// In Rust, you'd need a ThreadPool struct with workers,
// channels for job distribution, and Arc<Mutex<...>>
// See the Rust Book's full implementation.

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

Each incoming connection creates a new `Worker` actor. The `Worker` actor
receives a `Handle` message with the TCP stream and processes the connection
independently. Because actors run concurrently, multiple requests are handled
in parallel without blocking each other.

This is much simpler than Rust's thread pool approach. In Rust, you need:

- A `ThreadPool` struct with a vector of `Worker` threads
- A channel (`mpsc`) for sending jobs to workers
- `Arc<Mutex<...>>` for shared access to the receiver
- Manual `Drop` implementation for graceful shutdown

In Auto, actors handle all of this automatically:

| Concern | Rust (Thread Pool) | Auto (Actor) |
|---------|-------------------|--------------|
| Concurrent execution | `thread::spawn` | Actor `init()` |
| Job distribution | `mpsc` channel | `tell()` messages |
| Shared state | `Arc<Mutex<T>>` | Actor's internal state |
| Graceful shutdown | Manual `Drop` impl | Actor lifecycle |
| Boilerplate | ~80 lines | ~15 lines |

### A Worker Pool Actor

For better resource management, we can create a pool actor that manages a fixed
number of worker actors:

<Listing number="21-8" file-name="src/main.at" caption="A worker pool actor managing multiple workers">

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
        // Pick the next available worker (round-robin)
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

The `WorkerPool` actor maintains a list of worker actors and distributes
connections among them using round-robin scheduling. Each worker processes its
connections independently. If a worker is busy, the pool assigns the connection
to the next available worker.

### Graceful Shutdown

Actors in Auto support graceful shutdown naturally. When the server actor stops,
all child workers are notified and can finish processing their current
connections:

<Listing number="21-9" file-name="src/main.at" caption="Graceful shutdown with actors">

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

        // Accept connections for a limited time (demo purposes)
        var count = 0
        for stream in listener.incoming() {
            let stream = stream!
            .pool.tell(Handle(stream))
            count += 1
            if count >= 2 {
                break
            }
        }

        // Graceful shutdown
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

## Full Server Code

Here's the complete server implementation:

<Listing number="21-10" file-name="src/main.at" caption="Complete web server with Actor model">

```auto
use.net {TcpListener, TcpStream}
use.io {BufReader, BufRead, Write}
use.fs
use.thread
use.time Duration

// -- Connection Handler --

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

// -- Worker Pool Actor --

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

// -- Server Actor --

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

// -- Entry Point --

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

## Auto vs Rust: Web Server Comparison

| Aspect | Rust (Thread Pool) | Auto (Actor Model) |
|--------|-------------------|---------------------|
| Concurrency unit | OS threads | Actors |
| Job distribution | `mpsc` channel + `Arc<Mutex>` | `tell()` messages |
| Shared state | `Arc<Mutex<T>>` | Actor internal state |
| Worker creation | `thread::spawn` | `Worker.init()` |
| Graceful shutdown | Manual `Drop` + `Option::take` | Actor `Stop` message |
| Code for pool | ~80 lines | ~25 lines |
| Error-prone areas | `Arc<Mutex<Receiver>>` | Minimal |
| Memory safety | Borrow checker | AutoFree + message isolation |

Auto's Actor model eliminates the need for the complex `Arc<Mutex<...>>`
patterns that Rust's thread pool requires. Each actor owns its state, and
communication happens through messages, making data races impossible by design.

## Ideas for Enhancement

If you want to continue enhancing this project, here are some ideas:

- Add logging to the `Worker` actor for each request
- Use `~T` blueprints (Chapter 17) for async request handling
- Add request routing with a `Router` actor
- Implement middleware as actor message interceptors
- Add tests for the `handle_connection` function
- Use `#derive[Debug]` for message types

## Summary

Well done! You've made it to the end of the book! In this final project, we
built a web server using many of Auto's features:

1. **Basic I/O** — Reading from TCP streams, writing responses, and reading
   files
2. **Pattern matching with `is`** — Matching HTTP request lines
3. **Error handling with `!T`** — Using `!` for fallible operations
4. **Actor model** — Using actors for concurrent request handling instead of
   thread pools
5. **Message passing** — Using `tell()` to distribute work among actors
6. **Type system** — Defining message types and actor state

The key takeaway is that Auto's Actor model provides a simpler, safer
alternative to thread pools for concurrent server implementations. Where Rust
requires `Arc<Mutex<>>`, channels, and manual `Drop` implementations, Auto uses
actors with message passing — a model that eliminates data races by construction
while keeping the code concise and readable.

Thank you for joining us on this tour of Auto. You're now ready to implement
your own Auto projects and help with other people's projects. Keep building!
