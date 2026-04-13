# Actor Concurrency

Handling concurrent programming safely and efficiently is one of Auto's major
goals. _Concurrent programming_, in which different parts of a program execute
independently, and _parallel programming_, in which different parts of a
program execute at the same time, are becoming increasingly important as more
computers take advantage of their multiple processors.

Rust's approach to concurrency is built around threads, channels, and shared
state with `Mutex<T>` and `Arc<T>`. Auto takes a different approach: the
_Actor model_. In the actor model, concurrency is expressed through independent
_units of computation_ called _actors_ that communicate exclusively by sending
messages to each other. No actor can directly access another actor's state.

This model eliminates entire classes of concurrency bugs:

- **No data races** — actors don't share memory
- **No deadlocks** — there are no locks to deadlock on
- **No stale references** — communication is via message passing, not shared
  pointers

Auto's ownership system still plays a crucial role: it ensures that messages
sent between actors transfer ownership cleanly, preventing the sender from
accidentally using data that has been sent to another actor.

> **Note:** The Actor model is Auto's primary concurrency abstraction. For
> compatibility with Rust libraries, Auto also supports thread-based concurrency
> through `use.rust`. This chapter focuses on the Actor model, which is the
> idiomatic Auto approach.

Here are the topics we'll cover in this chapter:

- How the Actor model differs from thread-based concurrency
- How to create actors and send messages between them
- Message-passing patterns: request/response, fan-out, and pipelines
- Shared-state patterns when interop with Rust threads is needed
- Concurrency specs: `Send` and marker specs

## From Threads to Actors

In Rust, concurrency is based on _threads_ — OS-level units of execution that
share memory. Threads communicate through _channels_ (message passing) or
_shared state_ protected by mutexes.

### The Problem with Shared Memory

Thread-based concurrency with shared memory is powerful but error-prone:

- **Race conditions**: threads accessing data in an inconsistent order
- **Deadlocks**: two threads waiting for each other, preventing both from
  continuing
- **Subtle bugs** that only happen in certain situations and are hard to
  reproduce

Rust's ownership system helps prevent many of these issues at compile time, but
the mental model is still complex. You must reason about locks, lifetimes, and
thread boundaries simultaneously.

### The Actor Model

The Actor model, first described by Carl Hewitt in 1973, takes a different
approach. An _actor_ is the fundamental unit of computation with these
properties:

1. Each actor has its own private state — no other actor can access it
2. Actors communicate exclusively by sending asynchronous messages
3. When an actor receives a message, it can:
   - Send messages to other actors
   - Create new actors
   - Change its own state for the next message

This model maps naturally to many real-world concurrency problems and avoids
the pitfalls of shared-memory concurrency.

### Actor Model vs Thread Model

| Concept | Rust (Threads) | Auto (Actors) |
|---------|---------------|----------------|
| Unit of concurrency | Thread | Actor |
| Communication | Channels or shared state | Message passing |
| State sharing | Mutex + Arc | No sharing |
| Data races | Prevented by ownership | Impossible by design |
| Deadlocks | Possible | Impossible (no locks) |
| Error handling | Result types | Message-level errors |

## Creating Actors

In Auto, an actor is defined using the `actor` keyword. An actor encapsulates
its own state and defines which messages it can receive.

### Defining an Actor

<Listing number="16-1" file-name="src/main.at" caption="A simple counter actor">

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
// Rust equivalent using threads and channels
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

The `Counter` actor maintains a private `count` field. The `on Increment` block
handles incoming `Increment` messages. The `on GetCount -> int` block handles
`GetCount` messages and returns the current count.

Key differences from Rust's approach:

- **No `Arc<Mutex<T>>`** — the actor owns its state privately
- **No `move` closures** — the actor model handles ownership transfer
  automatically
- **No `.lock().unwrap()`** — no locks needed, messages are processed one at a
  time

### Actor Lifecycle

Each actor goes through these phases:

1. **Creation** — `Counter.init()` creates a new actor instance
2. **Running** — the actor processes messages from its mailbox
3. **Shutdown** — when all references are dropped, the actor stops

### Sending Messages

There are two ways to send messages to an actor:

- **`send`** — fire-and-forget (asynchronous, no response expected)
- **`ask`** — request-response (waits for a return value)

```auto
counter.send(Increment)         // fire and forget
let n = counter.ask(GetCount)   // waits for response
```

## Message Passing Patterns

### Basic Message Passing

Let's create a more complete example: a logger actor that receives messages and
prints them.

<Listing number="16-2" file-name="src/main.at" caption="A logger actor that prints messages">

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

In Rust, you'd need to create a channel, define an enum for messages, spawn a
thread, and manually match on incoming messages. Auto's actor model packages
this into a more concise, purpose-built abstraction.

### Fan-Out: Multiple Actors, One Message

A common pattern is broadcasting a message to multiple actors:

<Listing number="16-3" file-name="src/main.at" caption="Fan-out: sending messages to multiple workers">

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

    // Send work to each worker
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

### Pipeline: Actors in Sequence

Messages can flow through a pipeline of actors, each performing a
transformation:

<Listing number="16-4" file-name="src/main.at" caption="A pipeline of actors processing data">

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

## State Management in Actors

Each actor maintains its own private state. When processing a message, the actor
can modify its state, and those changes persist for the next message.

### Accumulator Pattern

<Listing number="16-5" file-name="src/main.at" caption="An actor that accumulates values">

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

The Auto version is significantly simpler: no `Arc`, no `Mutex`, no thread
management. The actor processes one message at a time, so there's no possibility
of data races on `total`.

### Actor with Complex State

<Listing number="16-6" file-name="src/main.at" caption="A key-value store actor">

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

## Interop with Rust Threads

When you need to use Rust's thread-based concurrency (for example, to call a
Rust library that uses threads), Auto provides access through `use.rust`:

<Listing number="16-7" file-name="src/main.at" caption="Using Rust threads for interop">

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

### When to Use Actors vs Threads

| Scenario | Use Actors | Use Threads |
|----------|-----------|-------------|
| Independent services | Yes | No |
| Shared mutable state | Avoid with actors | Mutex + Arc |
| CPU-bound parallelism | Limited | Yes |
| Rust library interop | No | Yes |
| Message-based workflows | Yes | Possible but verbose |
| Simple background task | Yes | Either |

## The `Send` Spec

Like Rust, Auto uses the `Send` spec to indicate that a type can be safely
transferred between actors (or threads). The ownership system ensures that
values transferred via messages move cleanly from one actor to another.

Most Auto types automatically implement `Send`. The main exception is types that
contain non-thread-safe Rust references accessed via `use.rust`.

### Ownership Transfer in Messages

When you send a message containing a value, ownership of that value transfers to
the receiving actor:

```auto
let data = List.of(1, 2, 3)
worker.send(Process(data))
// data is no longer valid here — ownership was transferred
```

This prevents the sender from accidentally modifying data that the receiver is
now using. The ownership system catches this at compile time.

### Cloning Before Sending

If you need to keep a copy, clone the data before sending:

```auto
let data = List.of(1, 2, 3)
worker.send(Process(data.clone()))
// data is still valid here — we sent a clone
print(data)  // works fine
```

## Concurrency Quick Reference

| Feature | Auto (Actors) | Rust (Threads) |
|---------|---------------|----------------|
| Define unit | `actor Name { }` | `thread::spawn(\|\| { })` |
| Send message | `actor.send(Msg)` | `tx.send(val)` |
| Request/response | `actor.ask(Msg)` | `rx.recv()` + `tx.send()` |
| Shared state | Not shared — actor owns it | `Arc<Mutex<T>>` |
| Prevent data races | By design (no sharing) | Ownership + type system |
| Prevent deadlocks | By design (no locks) | Careful lock ordering |
| Create new unit | `Name.init()` | `thread::spawn()` |
| Marker spec | `Send` | `Send` + `Sync` |

## Summary

Auto's actor model provides a fundamentally different approach to concurrency
from Rust's thread-based model:

1. **Actors** — independent units of computation with private state
2. **Message passing** — the only way actors communicate; no shared memory
3. **`send` and `ask`** — fire-and-forget and request-response patterns
4. **Ownership transfer** — messages transfer ownership, preventing data races
5. **No locks** — actors process one message at a time, eliminating deadlocks
6. **Rust interop** — thread-based concurrency available via `use.rust`

The actor model trades the flexibility of shared memory for the safety and
simplicity of isolated state. For most concurrent applications, this trade-off
results in code that is easier to write, easier to understand, and free of
entire categories of concurrency bugs.

In the next chapter, we'll explore Auto's async programming model with `~T`
blueprints and how it relates to Rust's `async`/`await`.
