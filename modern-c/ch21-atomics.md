# Chapter 21: Atomics & Memory Consistency

> Level 3 -- Experience
>
> Lock-free programming with atomic operations and memory ordering -- the deepest
> level of C concurrency, where even the compiler and CPU are your adversaries.

Atomics are the foundation upon which all higher-level concurrency primitives
are built. Mutexes use atomics. Condition variables use atomics. Even the
simplest "is this flag set?" check in a multithreaded program requires atomic
operations for correctness. This chapter covers the most technically demanding
material in the entire book.

---

## 21.1 The Happened-before Relation

When two threads access the same memory, the order in which those accesses
"happen" is not always clear. The compiler may reorder instructions. The CPU
may reorder memory operations. Cache hierarchies may delay visibility.

The **happened-before** relation defines whether one operation is guaranteed to
be visible to another:

```c
// C Deep Dive: happens-before
// Thread 1:           Thread 2:
// x = 1;              if (flag == 1)
// flag = 1;               assert(x == 1);  // MAY FAIL
```

Without proper synchronization, Thread 2 may see `flag == 1` but `x == 0`.
The compiler or CPU may reorder the stores, or the cache may not have
propagated the write to `x` by the time Thread 2 reads `flag`.

> **C Deep Dive:** The happened-before relation is defined by the C standard
> (and by the Java Memory Model before it). It is a partial ordering: not all
> operations are ordered relative to each other. Only operations connected by
> synchronization (mutex lock/unlock, atomic operations with appropriate memory
> ordering) establish happened-before relationships.

The key insight: **program order is not memory order**. The code you write is
not the order in which the CPU executes or the order in which other threads
observe the effects.

**Auto's approach.** Auto's actor model avoids this entirely. Each actor owns
its data. Messages are delivered in order. No shared mutable state means no
memory ordering concerns.

---

## 21.2 C Library Calls That Provide Synchronization

C11 provides atomic operations through `<stdatomic.h>`:

```c
// C Deep Dive: atomic operations
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

The `_Atomic` type qualifier makes operations on that object atomic. The
`atomic_fetch_add` function atomically increments the counter. No mutex needed.

> **C Deep Dive:** Atomic operations are implemented using CPU-level primitives:
> - x86: `LOCK` prefix instructions (e.g., `LOCK XADD`)
> - ARM: `LDXR`/`STXR` exclusive load/store pairs
> - Some architectures use a global compare-and-swap loop
>
> `_Atomic` types may have different sizes or alignments than their non-atomic
> counterparts. `_Atomic(int)` is always lock-free on mainstream platforms, but
> `_Atomic(struct large)` may use internal locks.

Common atomic operations:

| Operation            | Function                      | Description                  |
|----------------------|-------------------------------|------------------------------|
| Load                 | `atomic_load(&x)`             | Read atomically              |
| Store                | `atomic_store(&x, val)`       | Write atomically             |
| Fetch-add            | `atomic_fetch_add(&x, 1)`     | Add and return old value     |
| Fetch-sub            | `atomic_fetch_sub(&x, 1)`     | Subtract and return old      |
| Compare-exchange     | `atomic_compare_exchange_strong` | CAS operation             |
| Exchange             | `atomic_exchange(&x, val)`    | Swap atomically              |
| Flag test-and-set    | `atomic_flag_test_and_set`    | Simple spinlock primitive    |

<Listing path="listings/ch21/listing-21-01" title="Atomic operations" />

**Auto's approach.** Auto does not expose atomics directly. Higher-level
concurrency abstractions (actors, message passing) are the intended interface.
For systems programming, atomics may be exposed through a `sys` module.

---

## 21.3 Sequential Consistency

The default memory ordering is **sequential consistency** (`memory_order_seq_cst`):

```c
// C Deep Dive: sequential consistency
#include <stdatomic.h>
#include <stdio.h>

static _Atomic int x = 0;
static _Atomic int y = 0;
static _Atomic int r1 = 0;
static _Atomic int r2 = 0;

// Thread 1:             Thread 2:
// atomic_store(&x, 1);  atomic_store(&y, 1);
// r1 = atomic_load(&y); r2 = atomic_load(&x);

// With seq_cst: it is IMPOSSIBLE for both r1==0 and r2==0
// All threads agree on a single total order of operations
```

Sequential consistency is the strongest memory model. All threads agree on a
single total ordering of all atomic operations. It is the easiest to reason
about but the most expensive to implement.

> **C Deep Dive:** On x86, sequential consistency is relatively cheap because
> x86 has a strong memory model (Total Store Order). `atomic_store` with
> `seq_cst` compiles to `MOV` + `MFENCE` or `LOCK XCHG`. On ARM, `seq_cst`
> requires `DMB` (Data Memory Barrier) instructions, which are more expensive.
> The performance difference between `seq_cst` and `relaxed` can be 2-10x on
> ARM.

**Auto's approach.** Auto actors communicate through messages. Message delivery
is sequentially consistent by default. The actor runtime handles memory barriers
internally. Programmers never need to think about memory ordering.

---

## 21.4 Other Consistency Models

C provides four weaker memory orderings for performance-sensitive code:

### Relaxed (`memory_order_relaxed`)

No ordering guarantees. Only atomicity is guaranteed:

```c
// C Deep Dive: relaxed ordering
#include <stdatomic.h>

static _Atomic int counter = 0;

// Multiple threads:
atomic_fetch_add_explicit(&counter, 1, memory_order_relaxed);
// Each increment is atomic, but ordering with other operations is not guaranteed
```

Use relaxed when you only need atomicity, not ordering (e.g., a statistics
counter where the exact order doesn't matter).

### Acquire (`memory_order_acquire`)

No reads or writes in the current thread can be reordered before this load:

```c
// C Deep Dive: acquire ordering
// Producer:
// atomic_store_explicit(&flag, 1, memory_order_release);
//
// Consumer:
// if (atomic_load_explicit(&flag, memory_order_acquire)) {
//     // all writes before the release are visible here
//     assert(data == 42);  // guaranteed
// }
```

### Release (`memory_order_acq_rel`)

No reads or writes can be reordered after this store. Paired with acquire to
establish synchronization:

```c
// C Deep Dive: release/acquire pattern
#include <stdatomic.h>
#include <stdio.h>

static int data = 0;
static _Atomic int ready = 0;

// Thread 1 (producer):
void produce(void) {
    data = 42;    // ordinary write
    atomic_store_explicit(&ready, 1, memory_order_release);
}

// Thread 2 (consumer):
void consume(void) {
    while (atomic_load_explicit(&ready, memory_order_acquire) == 0) {}
    printf("data = %d\n", data);  // guaranteed to see 42
}
```

> **C Deep Dive:** The release/acquire pattern is the most common non-default
> ordering. It establishes a happened-before relationship: all writes before the
> release store are visible after the acquire load. This is the foundation of
> lock-free data structures. `memory_order_acq_rel` combines both for
> read-modify-write operations (like compare-exchange).

### Memory Ordering Summary

| Ordering              | Guarantee                                | Use case                  |
|-----------------------|------------------------------------------|---------------------------|
| `seq_cst`             | Single total order                       | Default, safest           |
| `acq_rel`             | Acquire + release on RMW ops             | Compare-and-swap loops    |
| `acquire`             | No reordering before load                | Reading synchronized data |
| `release`             | No reordering after store                | Publishing synchronized data |
| `relaxed`             | Only atomicity                           | Simple counters           |

> **C Deep Dive:** Using memory orderings other than `seq_cst` is expert-only
> territory. Incorrect use of `relaxed` can cause subtle bugs that only manifest
> under specific hardware (ARM, POWER) and specific compiler optimization
> levels. The Linux kernel uses `relaxed` extensively for performance, but the
> developers are among the world's foremost experts on memory models. For
> application code, always use `seq_cst` unless profiling proves it is a
> bottleneck.

**Auto's approach.** Auto hides memory ordering behind its concurrency model:

```auto
// Auto: memory ordering handled by the runtime
// Actors communicate via messages
// Message delivery provides acquire/release semantics
// No explicit memory_order_* types needed

fn main() {
    // Sequential execution -- no memory ordering concerns
    let x int = 0
    for i in 0..100 {
        x = x + 1
    }
    print("Sequential count:", x)
    print("Auto: actors provide safe concurrency without atomics")
}
```

> **C Deep Dive:** Understanding atomics and memory ordering is essential for C
> systems programmers. Even if Auto hides these details, the underlying C code
> that implements Auto's runtime uses them extensively. The `atomic_*` functions
> and `memory_order_*` enumerations are the building blocks of every lock-free
> algorithm, every mutex implementation, and every concurrent data structure.

---

## Quick Reference

| Concept                 | C mechanism                         | Auto mechanism            |
|-------------------------|-------------------------------------|---------------------------|
| Atomic operations       | `_Atomic`, `atomic_fetch_add`       | Not exposed directly      |
| Sequential consistency  | `memory_order_seq_cst`              | Default for message passing |
| Acquire/release         | `memory_order_acquire/release`      | Handled by runtime        |
| Relaxed ordering        | `memory_order_relaxed`              | Not applicable            |
| Compare-and-swap        | `atomic_compare_exchange_strong`    | Not exposed directly      |
| Lock-free primitives    | `atomic_flag`                       | Not applicable            |

---

*Atomic operations are the bedrock of concurrent programming. C gives you full
control -- and full responsibility. Auto's actor model trades that control for
safety: you never need to think about memory ordering, because the runtime
handles it for you. For the rare cases where you need raw atomics, the `sys`
module will provide escape hatches.*
