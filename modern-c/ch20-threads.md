# Chapter 20: Threads

> Level 3 -- Experience
>
> Shared-memory concurrency with C threads, mutexes, and condition variables --
> and why Auto's actor model makes most of this unnecessary.

Concurrency is where C programs most often go wrong. Data races, deadlocks, and
subtle memory ordering bugs are notoriously difficult to reproduce and fix. C11
introduced a standard threading API based on POSIX threads. Auto takes a
fundamentally different approach: actors with isolated state communicating
through message passing.

---

## 20.1 Simple Interthread Control

C11 provides `thrd_create` and `thrd_join` for thread management:

```c
// C Deep Dive: thread creation
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

> **C Deep Dive:** C threads share the entire address space. Every thread can
> read and write every global variable. This makes data races trivially easy to
> create. The thread function must return `int` (not `void*` like POSIX). The
> `thrd_create` argument is passed as `void*` -- common source of type errors.

**Auto's approach.** Auto uses the actor model instead of raw threads:

```auto
// Auto: sequential execution (actor model is planned)
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

<Listing path="listings/ch20/listing-20-01" title="Thread basics" />

---

## 20.2 Race-free Initialization

C provides `call_once` for one-time initialization:

```c
// C Deep Dive: call_once
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

`call_once` guarantees that `init_config` is called exactly once, even if
multiple threads call `call_once` simultaneously. This replaces the
double-checked locking pattern.

> **C Deep Dive:** Before `call_once`, programmers used "double-checked locking"
> which is notoriously difficult to get right. The pattern requires atomic
> operations and memory barriers. `call_once` encapsulates all the complexity.
> POSIX has `pthread_once` which serves the same purpose.

**Auto's approach.** Auto handles initialization naturally. Each actor
initializes its own state when it starts. No shared state means no
initialization races.

---

## 20.3 Thread-local Data

C11 introduced `thread_local` storage for per-thread data:

```c
// C Deep Dive: thread_local
#include <threads.h>
#include <stdio.h>

thread_local int counter = 0;

int worker(void *arg) {
    for (int i = 0; i < 1000; i++) {
        counter++;    // each thread has its own counter
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
    // Both print 1000 -- no sharing, no races
    return 0;
}
```

`thread_local` variables have one instance per thread. They avoid data races
by giving each thread its own copy.

> **C Deep Dive:** `thread_local` is a storage class specifier like `static` or
> `extern`. It can be combined with `static` for internal linkage. The address
> of a `thread_local` variable is different in each thread. Taking its address
> and passing it to another thread creates a data race.

**Auto's approach.** Auto's actor model naturally isolates state. Each actor
has its own private data -- equivalent to everything being `thread_local` by
default. No keyword needed.

---

## 20.4 Critical Data and Critical Sections

Mutexes protect shared data from concurrent access:

```c
// C Deep Dive: mutex
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

> **C Deep Dive:** Forgetting to unlock a mutex (e.g., due to an early return
> or exception-like error) creates a deadlock. C has no RAII to automatically
> release mutexes. POSIX has `pthread_mutexattr_settype` with `PTHREAD_MUTEX_ERRORCHECK`
> to detect double locks. The `mtx_timed` type allows timed lock attempts.
> C does not provide reader-writer locks in the standard.

**Auto's approach.** No shared mutable state means no mutexes:

```auto
// Auto: no shared state, no mutexes
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

<Listing path="listings/ch20/listing-20-02" title="Mutexes and critical sections" />

---

## 20.5 Condition Variables

Condition variables allow threads to wait for a condition:

```c
// C Deep Dive: condition variables
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
        cnd_wait(&cond, &mutex);  // releases mutex, waits, reacquires
    }
    printf("Consumed data\n");
    mtx_unlock(&mutex);
    return 0;
}
```

The `cnd_wait` call atomically releases the mutex and blocks the thread.
When `cnd_signal` wakes it, `cnd_wait` reacquires the mutex before returning.

> **C Deep Dive:** Condition variables must always be used with a mutex and a
> predicate loop (`while (!ready)`, not `if (!ready)`). Spurious wakeups are
> allowed by the standard -- a thread may wake from `cnd_wait` without
> `cnd_signal` being called. The predicate loop handles this. `cnd_broadcast`
> wakes all waiting threads.

**Auto's approach.** Auto's planned actor mailboxes replace condition variables:

```auto
// Auto: message passing replaces condition variables (conceptual)
// actor Consumer {
//     fn on_message(msg Message) {
//         // called when message arrives -- no explicit wait
//         print("Received:", msg.data)
//     }
// }
print("Auto actors receive messages via mailboxes")
print("No explicit condition variables needed")
```

---

## 20.6 Sophisticated Thread Management

Real C programs use thread pools, futures, and work queues:

```c
// C Deep Dive: thread pool concept
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

> **C Deep Dive:** Building a correct thread pool in C requires careful
> coordination of mutexes, condition variables, and shutdown flags. Common
> pitfalls include: lost wakeups (signal before wait), task starvation (unfair
> scheduling), and shutdown races (checking flag after wait). Production-quality
> thread pools are hundreds of lines of code.

**Auto's approach.** The actor model provides these abstractions automatically:

- Each actor is a unit of concurrency (like a lightweight thread)
- Messages are queued in the actor's mailbox (like a task queue)
- The runtime schedules actors efficiently (like a thread pool)

No manual thread management needed.

---

## 20.7 Ensure Liveness

Concurrency bugs go beyond data races:

**Deadlock** occurs when threads wait on each other:

```c
// C Deep Dive: deadlock scenario
// Thread 1: mtx_lock(&A); mtx_lock(&B);  // holds A, waits for B
// Thread 2: mtx_lock(&B); mtx_lock(&A);  // holds B, waits for A
// Result: both threads wait forever
```

> **C Deep Dive:** Deadlock prevention strategies include: lock ordering (always
> acquire locks in the same order), trylock with backoff (non-blocking attempt),
> and lock hierarchy (assign numerical levels to locks). None of these are
> enforced by the compiler -- they are purely disciplined programming.

**Starvation** occurs when a thread never gets access to a resource. Livelock
occurs when threads repeatedly react to each other without making progress.

**Auto's approach.** The actor model prevents deadlocks by design:

- Actors don't share locks (no lock ordering issues)
- Message passing is asynchronous (no blocking waits)
- The runtime schedules actors fairly (no starvation)

```auto
// Auto: deadlock-free by design
print("Actor model prevents deadlocks")
print("No shared locks, no circular waits")
print("Runtime ensures fair scheduling")
```

---

## Quick Reference

| Concept              | C mechanism                    | Auto mechanism                |
|----------------------|--------------------------------|-------------------------------|
| Thread creation      | `thrd_create`, `thrd_join`     | Actor spawning                |
| One-time init        | `call_once`                    | Actor initialization          |
| Thread-local data    | `thread_local`                 | Actor state (default)         |
| Mutual exclusion     | `mtx_lock` / `mtx_unlock`      | Not needed (message passing)  |
| Waiting              | `cnd_wait` / `cnd_signal`      | Mailbox receive               |
| Thread pools         | Manual implementation          | Runtime scheduler             |
| Deadlock prevention  | Lock ordering, discipline      | Eliminated by design          |

---

*C threading is manual, error-prone, and requires deep expertise to use correctly.
Auto's actor model eliminates data races, deadlocks, and starvation by design --
trading raw performance for correctness, which is almost always the right tradeoff.*
