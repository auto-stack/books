# Async Programming with `~T`

Many operations we ask a computer to do could take a while to finish. In Auto,
as in most languages, these kinds of operations are called _asynchronous_ or
_async_. The `~T` type modifier is Auto's way of expressing a value that
represents a computation which will complete at some point in the future — a
_time blueprint_.

In this chapter, we'll cover:

- What `~T` means and how it relates to Rust's `Future` trait
- How to create and compose async operations
- Concurrency patterns with async tasks
- Streams: async iterators over time
- How `~T` interacts with Auto's actor model
- When to use actors vs async vs threads

## What Is a Time Blueprint?

Consider two different operations:

1. **Rendering a video** — this is _CPU-bound_. Every frame must be computed,
   and more CPU power directly means faster rendering. This is _parallelism_:
   doing multiple things at the same time.

2. **Downloading a video** — this is _I/O-bound_. The network determines the
   speed, not your CPU. While waiting for data, your CPU sits idle. This is
   where _concurrency_ shines: you can start a download, switch to other work
   while waiting, and come back when data arrives.

> **Parallelism vs Concurrency**: Parallelism is about doing multiple things
> simultaneously. Concurrency is about managing multiple tasks by switching
> between them. You can have concurrency on a single CPU core. Parallelism
> requires multiple cores.

Rust's `Future` trait represents a value that may not be ready yet. Auto's `~T`
takes this concept further: `~T` is a _time blueprint_ — a description of a
value that will materialize in the future. The `~` symbol represents the
temporal dimension: the value exists, just not yet.

- `int` — a value you have right now
- `~int` — a blueprint for an `int` that will arrive later
- `~String` — a blueprint for a `String` that will arrive later

> **Note**: In Rust, async functions return `impl Future<Output = T>`. In Auto,
> async functions return `~T`. The blueprint metaphor is intentional: `~T`
> describes _how_ to produce the value, not the value itself. Like an
> architectural blueprint, it must be "built" (awaited) to produce the result.

## Creating Async Functions

In Auto, an async function is one that returns a `~T` type. You use the `async`
keyword to mark a function as asynchronous, and `.await` to wait for a
blueprint's result.

### Your First Async Function

<Listing number="17-1" file-name="src/main.at" caption="An async function that fetches a page title">

```auto
use net.http

async fn page_title(url String) ~?String {
    let response = http.get(url).await
    let text = response.text().await
    Html.parse(text).select_first("title")
        .map((title) => title.inner_html())
}

fn main() {
    async.block(async {
        let url = "https://example.com"
        let title = page_title(url).await
        match title {
            Some(t) => print(t),
            None => print("No title found"),
        }
    })
}
```

```rust
use trpl::{block_on, get, Html};

async fn page_title(url: &str) -> Option<String> {
    let response_text = trpl::get(url).await.text().await;
    Html::parse(&response_text)
        .select_first("title")
        .map(|title| title.inner_html())
}

fn main() {
    block_on(async {
        let url = "https://example.com";
        let title = page_title(url).await;
        match title {
            Some(t) => println!("{t}"),
            None => println!("No title found"),
        }
    })
}
```

</Listing>

There are several important things to notice here:

1. `page_title` returns `~?String` — a blueprint for an optional string
2. The `.await` keyword suspends execution until the blueprint resolves
3. `async.block` sets up the async runtime and waits for the result
4. The `main` function itself is not async — it enters the async world via
   `async.block`

### The `async.block` Entry Point

Unlike Rust, where you need an external runtime like `tokio`, Auto has a
built-in async runtime. `async.block` is the bridge from synchronous to
asynchronous code:

```auto
fn main() {
    async.block(async {
        // You can use .await here
    })
}
```

```rust
fn main() {
    trpl::block_on(async {
        // You can use .await here
    })
}
```

`async.block` takes a blueprint and _materializes_ it — it runs the async
runtime, executes the blueprint, and returns the final value. This is the
entry point for all async code in an Auto program.

### What Happens at `.await`

When you call `.await`, the following happens:

1. If the value is ready, return it immediately
2. If not, _suspend_ the current computation and yield control to the runtime
3. The runtime can switch to other pending blueprints
4. When the value becomes available, _resume_ the computation

This is _cooperative multitasking_: blueprints yield control at await points,
and the runtime schedules them fairly. Unlike OS threads, which are
_preemptively_ scheduled, async tasks choose when to yield.

> **Key Insight**: In Rust, this suspension and resumption is implemented via a
> state machine that the compiler generates for each `async` block. Auto uses
> the same technique internally, but exposes it through the cleaner `~T` type
> notation.

## Concurrency with Async

The real power of async becomes apparent when you have multiple operations that
can proceed concurrently.

### Racing Two Operations

<Listing number="17-2" file-name="src/main.at" caption="Racing two page title fetches">

```auto
use net.http

async fn page_title(url String) ~?String {
    let response = http.get(url).await
    let text = response.text().await
    Html.parse(text).select_first("title")
        .map((title) => title.inner_html())
}

fn main() {
    async.block(async {
        let title_fut_1 = page_title("https://example.com")
        let title_fut_2 = page_title("https://example.org")

        let (url, maybe_title) = async.race(title_fut_1, title_fut_2).await
        match maybe_title {
            Some(title) => print(f"${url}: ${title}"),
            None => print(f"${url}: no title found"),
        }
    })
}
```

```rust
use trpl::{block_on, get, Html, Either};

async fn page_title(url: &str) -> Option<String> {
    let response_text = trpl::get(url).await.text().await;
    Html::parse(&response_text)
        .select_first("title")
        .map(|title| title.inner_html())
}

fn main() {
    block_on(async {
        let title_fut_1 = page_title("https://example.com");
        let title_fut_2 = page_title("https://example.org");

        let (url, maybe_title) = match trpl::select(title_fut_1, title_fut_2).await {
            Either::Left((url, title)) => (url, title),
            Either::Right((url, title)) => (url, title),
        };
        match maybe_title {
            Some(title) => println!("{url}: {title}"),
            None => println!("{url}: no title found"),
        }
    })
}
```

</Listing>

`async.race` starts both blueprints and returns as soon as either one
completes. The other blueprint is cancelled. This is useful when you want the
fastest response and don't need both results.

### Spawning Async Tasks

Sometimes you want to run a blueprint in the background without waiting for it
immediately. Auto provides `async.spawn` for this:

<Listing number="17-3" file-name="src/main.at" caption="Spawning async tasks">

```auto
fn main() {
    async.block(async {
        let handle = async.spawn(async {
            for i in 1..10 {
                print(f"hi number ${i} from the spawned task!")
                async.sleep(500).await  // 500ms
            }
        })

        for i in 1..5 {
            print(f"hi number ${i} from the main task!")
            async.sleep(750).await  // 750ms
        }

        handle.await  // wait for spawned task to finish
    })
}
```

```rust
fn main() {
    trpl::block_on(async {
        let handle = trpl::spawn_task(async {
            for i in 1..10 {
                println!("hi number {i} from the spawned task!");
                trpl::sleep(Duration::from_millis(500)).await;
            }
        });

        for i in 1..5 {
            println!("hi number {i} from the main task!");
            trpl::sleep(Duration::from_millis(750)).await;
        }

        handle.await.unwrap();
    })
}
```

</Listing>

`async.spawn` starts a blueprint as a separate task and returns a _handle_.
The handle is itself a `~T` — a blueprint for the task's result. You can
continue doing other work and `.await` the handle when you need the result.

### Joining Multiple Blueprints

While `race` returns the first result, `join` waits for _all_ blueprints:

<Listing number="17-4" file-name="src/main.at" caption="Joining two async tasks">

```auto
fn main() {
    async.block(async {
        let fut1 = async {
            print("Task 1 starting...")
            async.sleep(1000).await
            print("Task 1 done!")
            42
        }

        let fut2 = async {
            print("Task 2 starting...")
            async.sleep(500).await
            print("Task 2 done!")
            "hello"
        }

        let (result1, result2) = async.join(fut1, fut2).await
        print(f"Results: ${result1}, ${result2}")
    })
}
```

```rust
fn main() {
    trpl::block_on(async {
        let fut1 = async {
            println!("Task 1 starting...");
            trpl::sleep(Duration::from_millis(1000)).await;
            println!("Task 1 done!");
            42
        };

        let fut2 = async {
            println!("Task 2 starting...");
            trpl::sleep(Duration::from_millis(500)).await;
            println!("Task 2 done!");
            "hello"
        };

        let (result1, result2) = trpl::join(fut1, fut2).await;
        println!("Results: {}, {}", result1, result2);
    })
}
```

</Listing>

`async.join` runs both blueprints concurrently and returns both results as a
tuple. If either blueprint panics, the other is cancelled.

## Async Channels

Just as actors communicate via message passing, async tasks can communicate
through _async channels_. An async channel is like a pipe: one end sends
values, the other end receives them asynchronously.

<Listing number="17-5" file-name="src/main.at" caption="Async channel message passing">

```auto
fn main() {
    async.block(async {
        let (tx, rx) = async.channel(int)

        let tx_task = async {
            let vals = [
                "hello",
                "from",
                "the",
                "async",
                "channel",
            ]
            for val in vals {
                tx.send(val).await
            }
            // tx is dropped here, closing the channel
        }

        let rx_task = async {
            while let Some(received) = rx.recv().await {
                print(f"Got: ${received}")
            }
        }

        async.join(tx_task, rx_task).await
    })
}
```

```rust
fn main() {
    trpl::block_on(async {
        let (tx, mut rx) = trpl::channel();

        let tx_fut = async {
            let vals = vec![
                String::from("hello"),
                String::from("from"),
                String::from("the"),
                String::from("async"),
                String::from("channel"),
            ];
            for val in vals {
                tx.send(val).unwrap();
            }
        };

        let rx_fut = async {
            while let Some(received) = rx.recv().await {
                println!("Got: {}", received);
            }
        };

        trpl::join(tx_fut, rx_fut).await;
    })
}
```

</Listing>

The channel has two ends:

- **`tx`** (transmitter): sends values with `tx.send(value).await`
- **`rx`** (receiver): receives values with `rx.recv().await`

The `rx.recv()` returns `~?T` — a blueprint for an optional value. It returns
`Some(value)` when a message arrives, and `None` when the channel is closed
(i.e., all transmitters have been dropped).

### Multiple Producers

You can have multiple tasks sending to the same channel by cloning the
transmitter:

<Listing number="17-6" file-name="src/main.at" caption="Multiple producers on one channel">

```auto
fn main() {
    async.block(async {
        let (tx, rx) = async.channel(String)

        let tx1 = async {
            tx.send("from task 1").await
        }

        let tx2 = async {
            tx.send("from task 2").await
        }

        let rx_task = async {
            while let Some(msg) = rx.recv().await {
                print(f"Received: ${msg}")
            }
        }

        async.join_all([tx1, tx2, rx_task]).await
    })
}
```

```rust
fn main() {
    trpl::block_on(async {
        let (tx, mut rx) = trpl::channel();

        let tx1 = tx.clone();
        let tx_fut1 = async move {
            tx1.send("from task 1".to_string()).unwrap();
        };

        let tx_fut2 = async move {
            tx.send("from task 2".to_string()).unwrap();
        };

        let rx_fut = async {
            while let Some(msg) = rx.recv().await {
                println!("Received: {}", msg);
            }
        };

        trpl::join!(tx_fut1, tx_fut2, rx_fut);
    })
}
```

</Listing>

`async.join_all` takes a list of blueprints and waits for all of them to
complete. This is the multi-blueprint counterpart to `async.join`.

## Yielding Control

Async tasks cooperate by yielding control at `.await` points. But what if a
task does heavy computation without any await points? It would monopolize the
runtime, starving other tasks.

### The Problem: Blocking Without Awaiting

<Listing number="17-7" file-name="src/main.at" caption="A slow computation blocking the runtime">

```auto
fn slow(name String) {
    // Simulates heavy CPU work — NO await points!
    var count = 0
    for i in 0..1000000 {
        count += i
    }
    print(f"${name}: count = ${count}")
}

fn main() {
    async.block(async {
        let a = async { slow("A") }
        let b = async { slow("B") }
        async.join(a, b).await
    })
}
```

```rust
fn slow(name: &str) {
    // Simulates heavy CPU work — NO await points!
    let mut count = 0;
    for i in 0..1_000_000 {
        count += i;
    }
    println!("{name}: count = {count}");
}

fn main() {
    trpl::block_on(async {
        let a = async { slow("A") };
        let b = async { slow("B") };
        trpl::join(a, b).await;
    })
}
```

</Listing>

Because `slow` has no `.await` points, task A runs to completion before task B
even starts. There is no interleaving — no concurrency.

### The Solution: `async.yield_now`

<Listing number="17-8" file-name="src/main.at" caption="Yielding control with `async.yield_now`">

```auto
fn slow(name String) {
    var count = 0
    for i in 0..1000000 {
        count += i
        if i % 100000 == 0 {
            async.yield_now()  // let other tasks run
        }
    }
    print(f"${name}: count = ${count}")
}

fn main() {
    async.block(async {
        let a = async { slow("A") }
        let b = async { slow("B") }
        async.join(a, b).await
    })
}
```

```rust
fn slow(name: &str) {
    let mut count = 0;
    for i in 0..1_000_000 {
        count += i;
        if i % 100_000 == 0 {
            trpl::yield_now().await;
        }
    }
    println!("{name}: count = {count}");
}

fn main() {
    trpl::block_on(async {
        let a = async { slow("A") };
        let b = async { slow("B") };
        trpl::join(a, b).await;
    })
}
```

</Listing>

`async.yield_now()` explicitly yields control back to the runtime, allowing
other tasks to make progress. Use it in CPU-heavy loops that don't have natural
await points.

> **Rule of Thumb**: If you have a long-running computation inside an async
> context, periodically call `async.yield_now()` to be a good citizen of the
> cooperative runtime.

## Composing Blueprints: Timeout

One of the most powerful patterns in async programming is composing
blueprints to build higher-level abstractions. Let's build a `timeout`
function that wraps any blueprint with a time limit.

<Listing number="17-9" file-name="src/main.at" caption="Building a timeout from `race` and `sleep`">

```auto
async fn timeout(blueprint ~T, max_ms int) ~!T {
    match async.race(blueprint, async.sleep(max_ms)).await {
        Result.Ok(value) => value,
        Result.Err(ms) => !throw(f"Timed out after ${ms}ms"),
    }
}

fn main() {
    async.block(async {
        let slow_task = async {
            async.sleep(5000).await  // takes 5 seconds
            "finally done"
        }

        match timeout(slow_task, 1000).await {  // 1 second limit
            Ok(value) => print(f"Got: ${value}"),
            Err(msg) => print(f"Failed: ${msg}"),  // This prints
        }
    })
}
```

```rust
async fn timeout<F: Future>(future_to_try: F, max_time: Duration)
    -> Result<F::Output, Duration>
where
    F: Future,
{
    match trpl::select(future_to_try, trpl::sleep(max_time)).await {
        Either::Left(output) => Ok(output),
        Either::Right(_) => Err(max_time),
    }
}

fn main() {
    trpl::block_on(async {
        let slow_task = async {
            trpl::sleep(Duration::from_secs(5)).await;
            "finally done"
        };

        match timeout(slow_task, Duration::from_secs(1)).await {
            Ok(value) => println!("Got: {}", value),
            Err(_duration) => println!("Failed: timed out"),  // This prints
        }
    })
}
```

</Listing>

The `timeout` function races the given blueprint against `async.sleep`. If the
blueprint finishes first, we return its value. If the sleep finishes first, we
return an error. This is a clean example of blueprint composition: complex
behavior built from simple primitives.

## Streams: Async Iterators

A `~T` blueprint produces a single value. But many real-world data sources
produce _multiple_ values over time: WebSocket messages, file lines, sensor
readings, UI events. For these, Auto provides _streams_.

A stream is to `~T` what an iterator is to a regular value: it produces a
sequence of values asynchronously.

### Creating and Consuming Streams

<Listing number="17-10" file-name="src/main.at" caption="Creating a stream from an iterator">

```auto
fn main() {
    async.block(async {
        let vals = [1, 2, 3, 4, 5]
        let mut stream = async.stream_from(vals)

        while let Some(value) = stream.next().await {
            print(f"The value was: ${value}")
        }
    })
}
```

```rust
fn main() {
    trpl::block_on(async {
        let vals = vec![1, 2, 3, 4, 5];
        let mut stream = trpl::stream_from_iter(vals);

        while let Some(value) = stream.next().await {
            println!("The value was: {value}");
        }
    })
}
```

</Listing>

The `while let Some(value) = stream.next().await` pattern is the async
equivalent of `for value in iterator`. Each call to `stream.next().await`
produces the next value, suspending if none is available yet.

### Stream from a Channel

Channels are naturally stream-like — values arrive over time:

<Listing number="17-11" file-name="src/main.at" caption="Using a channel receiver as a stream">

```auto
fn main() {
    async.block(async {
        let (tx, rx) = async.channel(int)

        // Spawn a task that produces values
        async.spawn(async {
            for i in 1..6 {
                tx.send(i).await
                async.sleep(1000).await  // one per second
            }
        })

        // Consume as a stream
        let mut stream = rx.stream()
        while let Some(value) = stream.next().await {
            print(f"Received: ${value}")
        }
    })
}
```

```rust
fn main() {
    trpl::block_on(async {
        let (tx, mut rx) = trpl::channel();

        trpl::spawn_task(async move {
            for i in 1..6 {
                tx.send(i).unwrap();
                trpl::sleep(Duration::from_secs(1)).await;
            }
        });

        while let Some(value) = rx.recv().await {
            println!("Received: {value}");
        }
    })
}
```

</Listing>

### Composing Streams

Like iterators, streams support combinators for transforming and filtering:

<Listing number="17-12" file-name="src/main.at" caption="Stream combinators">

```auto
fn main() {
    async.block(async {
        let vals = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        let results = async.stream_from(vals)
            .filter((x) => x % 2 == 0)       // keep even numbers
            .map((x) => x * 3)               // triple them
            .take(3)                           // first 3 results

        while let Some(value) = results.next().await {
            print(value)  // 6, 12, 18
        }
    })
}
```

```rust
fn main() {
    trpl::block_on(async {
        let vals = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
        let mut results = trpl::stream_from_iter(vals)
            .filter(|x| x % 2 == 0)
            .map(|x| x * 3)
            .take(3);

        while let Some(value) = results.next().await {
            println!("{value}");  // 6, 12, 18
        }
    })
}
```

</Listing>

## Actors and Async: When to Use Which

Auto provides two primary concurrency models: _actors_ (Chapter 16) and _async_
(this chapter). Both are built into the language and runtime. Here's how to
decide which to use:

| Scenario | Use Actors | Use Async (`~T`) |
|----------|-----------|-------------------|
| Independent services with state | Yes | No |
| Request/response workflows | Either | Yes |
| Streaming data | No | Yes |
| State machines | Yes | Either |
| CPU-bound parallelism | Limited | Use threads |
| Many I/O-bound operations | Either | Yes |
| Message-based communication | Yes | Channels |

### Combining Actors and Async

Actors and async can be combined. An actor can `.await` blueprints inside its
message handlers:

<Listing number="17-13" file-name="src/main.at" caption="An actor that uses async operations">

```auto
use net.http

actor PageFetcher {
    on FetchTitle(url String) ~?String {
        let response = http.get(url).await
        let text = response.text().await
        Html.parse(text).select_first("title")
            .map((t) => t.inner_html())
    }
}

fn main() {
    let fetcher = PageFetcher.init()

    async.block(async {
        let title = fetcher.ask(FetchTitle("https://example.com")).await
        match title {
            Some(t) => print(f"Title: ${t}"),
            None => print("No title found"),
        }
    })
}
```

```rust
use trpl::{block_on, get, Html};

async fn page_title(url: &str) -> Option<String> {
    let response_text = trpl::get(url).await.text().await;
    Html::parse(&response_text)
        .select_first("title")
        .map(|title| title.inner_html())
}

fn main() {
    block_on(async {
        let title = page_title("https://example.com").await;
        match title {
            Some(t) => println!("Title: {t}"),
            None => println!("No title found"),
        }
    })
}
```

</Listing>

In this pattern, the actor's `on` handler is itself async — it returns `~T`.
The `ask` call returns a blueprint that resolves when the actor finishes
processing the message.

### Threads, Actors, and Async

Auto supports three levels of concurrency, each suited to different problems:

1. **OS Threads** — for CPU-bound parallelism (via `use.rust`)
2. **Actors** — for stateful, message-passing concurrent services
3. **Async Tasks** — for I/O-bound operations and streaming data

The async runtime multiplexes many lightweight tasks onto a pool of OS threads,
using _work stealing_ to balance load. This means you can have thousands of
concurrent async tasks without thousands of OS threads.

## Under the Hood: How `~T` Works

Understanding what happens inside `~T` helps you write better async code.

### Blueprints as State Machines

When the Auto compiler encounters an async function, it transforms it into a
state machine. Each `.await` point is a state transition:

```auto
async fn page_title(url String) ~?String {
    // State 1: Initial
    let response = http.get(url).await        // -> State 2
    // State 2: Got response
    let text = response.text().await           // -> State 3
    // State 3: Got text
    Html.parse(text).select_first("title")
        .map((t) => t.inner_html())
}
```

Conceptually, the compiler creates something like:

```auto
enum PageTitleBlueprint {
    State1 { url String },
    State2 { response HttpResponse },
    State3 { text String },
    Done,
}
```

Each time `poll` is called on the blueprint, it advances to the next state or
returns `Pending` if it needs to wait.

### Pinning

One subtlety of async state machines is that they can be _self-referential_:
one state might hold a reference to data from a previous state. If the
blueprint were moved in memory, those references would become invalid.

Auto handles this automatically: blueprints are _pinned_ in memory once they
begin executing. You don't need to think about pinning in normal code, but it's
worth knowing it exists under the hood.

In Rust, this is expressed with the `Pin<P>` type and the `Unpin` marker trait.
Auto's runtime manages pinning implicitly, so you never need to annotate
lifetimes or use `Pin<Box<...>>`.

### The `~T` Type Hierarchy

| Type | Meaning | Example |
|------|---------|---------|
| `T` | A value available now | `42`, `"hello"` |
| `~T` | A blueprint for a future `T` | `http.get(url)` |
| `~?T` | A blueprint for a future optional `T` | `page_title(url)` |
| `~!T` | A blueprint for a future result `T` | `timeout(task, 1000)` |
| `Stream<T>` | A sequence of `~?T` values over time | `rx.stream()` |

The modifiers compose naturally: `~?T` is a blueprint for an optional value,
`~!T` is a blueprint that may fail.

## Async Quick Reference

| Feature | Auto (`~T`) | Rust (`Future`) |
|---------|-------------|-----------------|
| Return type | `~T` | `impl Future<Output = T>` |
| Wait for result | `.await` | `.await` |
| Enter async world | `async.block` | `block_on` / `#[tokio::main]` |
| Spawn task | `async.spawn` | `tokio::spawn` / `trpl::spawn_task` |
| Race first result | `async.race(a, b)` | `tokio::select!` / `trpl::select` |
| Wait for all | `async.join(a, b)` | `tokio::join!` / `trpl::join` |
| Wait for many | `async.join_all(list)` | `tokio::join_all` / `futures::join_all` |
| Sleep | `async.sleep(ms)` | `tokio::time::sleep` / `trpl::sleep` |
| Yield control | `async.yield_now()` | `tokio::task::yield_now()` |
| Channel | `async.channel(T)` | `tokio::sync::mpsc` / `trpl::channel` |
| Timeout | `async.race` + sleep | `tokio::time::timeout` |
| Async sequence | `Stream<T>` | `impl Stream<Item = T>` |
| Runtime | Built-in | External (tokio, async-std) |

## Summary

Auto's `~T` async model provides a clean, composable way to handle
asynchronous operations:

1. **`~T`** — a time blueprint representing a future value
2. **`.await`** — materialize a blueprint, suspending until it resolves
3. **`async.block`** — enter the async world from synchronous code
4. **`async.spawn`** — run a blueprint as a separate task
5. **`async.race`** — compete blueprints, first wins
6. **`async.join`** — run blueprints concurrently, wait for all
7. **`async.channel`** — communicate between async tasks
8. **`async.yield_now`** — cooperatively yield control
9. **Streams** — async iterators for sequences of values over time
10. **Composition** — build complex behavior from simple blueprints

The `~T` system integrates naturally with Auto's actor model: actors can await
blueprints, and async tasks can send messages to actors. Together, they provide
a complete concurrency story that covers CPU-bound work (threads), stateful
services (actors), and I/O-bound operations (async).

In the next chapter, we'll explore Auto's approach to object-oriented
programming with the `is`, `has`, and `spec` keywords.
