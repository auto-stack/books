# Chapter 13: Storage

> Level 2 — Cognition
>
> malloc, storage duration, initialization -- how C manages object lifetimes
> and how Auto makes it automatic.

Memory management is where C programs most often go wrong. Memory leaks,
use-after-free, double-free, and dangling pointers account for a large fraction
of C's security vulnerabilities. This chapter examines C's storage mechanisms
and shows how Auto eliminates entire categories of memory errors.

---

## 13.1 malloc and Friends

C provides four functions for dynamic memory allocation:

```c
// C Deep Dive: dynamic allocation
void *malloc(size_t size);        // allocate size bytes (uninitialized)
void *calloc(size_t n, size_t s); // allocate n*s bytes (zero-initialized)
void *realloc(void *p, size_t s); // resize allocation (may move)
void free(void *p);               // deallocate
```

Typical usage in C:

```c
// C Deep Dive: malloc lifecycle
int *arr = malloc(10 * sizeof(int));  // allocate
if (!arr) { /* handle error */ }       // check NULL
for (int i = 0; i < 10; i++) {
    arr[i] = i * i;                    // use
}
// ... later ...
free(arr);                             // deallocate
arr = NULL;                            // avoid dangling pointer
```

The problems are legion:

- **Forgetting to free**: memory leaks that grow over time.
- **Using after free**: undefined behavior, often exploitable.
- **Double free**: corrupts the heap allocator's internal state.
- **Not checking NULL**: dereferencing a failed allocation crashes.
- **Wrong size**: `malloc(sizeof(int*))` when you meant `malloc(sizeof(int))`.

**Auto's replacement: automatic storage.** Auto manages object lifetimes
automatically. There is no `malloc`, `free`, `realloc`, or `calloc` in Auto:

```auto
// Auto: no malloc/free, automatic lifetime management
var arr [10]int
for i in 0..10 {
    arr[i] = i * i
}
print("First:", arr[0])
// no free needed -- storage reclaimed automatically
```

When Auto needs dynamically-sized collections, the standard library provides
growable containers with automatic cleanup:

```auto
// Auto: growable buffer
type Buffer {
    data [256]int
    size int
}

fn Buffer.new() Buffer {
    Buffer([256]int{}, 0)
}

fn Buffer.push(b Buffer, val int) {
    if b.size < 256 {
        b.data[b.size] = val
        b.size = b.size + 1
    }
}
```

<Listing path="listings/ch13/listing-13-01" title="malloc and storage duration" />

> **C Deep Dive:** `malloc` returns `void*`, which C implicitly converts to any
> pointer type. This means `int *p = malloc(...)` works without a cast in C
> but not C++. Many programmers add the cast `(int*)malloc(...)`, which is
> worse -- it suppresses the warning if you forget to include `<stdlib.h>`.

---

## 13.2 Storage Duration

Every C object has one of three **storage durations**:

| Duration     | Lifetime                           | Example                |
|-------------|-------------------------------------|------------------------|
| Static       | Entire program execution           | Global, `static` local |
| Automatic    | Enclosing block execution          | Local variables        |
| Allocated    | From `malloc` to `free`            | Heap objects           |

```c
// C Deep Dive: storage durations
int global = 42;              // static: lives forever

void example(void) {
    static int count = 0;     // static: lives forever, init once
    int local = 10;           // automatic: lives until block ends
    int *heap = malloc(sizeof(int)); // allocated: lives until free()
    *heap = 20;
    free(heap);
}
```

The most dangerous aspect of C's storage model is returning pointers to
automatic variables:

```c
// C Deep Dive: classic bug -- dangling pointer
int* make_value(void) {
    int x = 42;
    return &x;    // WARNING: address of local variable returned!
}
// *make_value() is undefined behavior
```

**Auto's approach: value semantics.** Auto uses value semantics by default.
Functions return values, not pointers. The caller receives its own copy:

```auto
// Auto: safe value returns
fn make_value() int {
    let x int = 42
    x    // return by value -- always safe
}

fn main() {
    let v int = make_value()
    print("Got:", v)    // 42, no dangling pointer possible
}
```

> **C Deep Dive:** C99 added variable-length arrays (VLAs) to avoid `malloc`
> for locally-sized arrays. But VLAs have problems: unbounded stack allocation
> can overflow the stack silently, and they were made optional in C11. Auto
> provides fixed-size arrays and growable containers instead.

---

## 13.3 Using Objects Before Definition

In C, a variable must be declared before it is used. This sounds simple, but
the interaction with `goto`, forward references, and mutually referential
structures creates complexity:

```c
// C Deep Dive: forward declarations
struct Node;                        // forward declaration
struct Node {
    int value;
    struct Node *next;             // pointer to forward-declared type
};

// Forward function declarations
static int helper(int x);          // declaration
int compute(int x) {
    return helper(x * 2);          // use before definition
}
static int helper(int x) {         // definition
    return x + 1;
}
```

For functions, C allows using a function before its definition only if a
forward declaration (prototype) is provided. Without it, C historically
assumed the function returns `int` -- a source of subtle bugs.

**Auto's approach: declaration order independence.** Auto resolves function
and type references across the entire compilation unit. Forward declarations
are unnecessary:

```auto
// Auto: order-independent definitions
fn compute(x int) int {
    helper(x * 2)     // use before definition -- OK
}

fn helper(x int) int {
    x + 1
}

fn main() {
    print("Result:", compute(5))
}
```

> **C Deep Dive:** The C standard says that jumping past a variable
> declaration with a VLA or a variably-modified type is undefined behavior.
> Auto avoids VLAs entirely and has no `goto`, eliminating this class of
> problems.

---

## 13.4 Initialization

C provides several ways to initialize objects, and choosing the wrong one
has consequences:

```c
// C Deep Dive: initialization forms
int a;                          // uninitialized: contains garbage
int b = 0;                      // copy initialization
int c = {42};                   // brace initialization
int arr[3] = {1, 2, 3};        // array initialization
int zeros[5] = {0};             // all elements zeroed

struct Point { int x; int y; };
struct Point p1 = {1, 2};            // positional
struct Point p2 = {.y = 2, .x = 1};  // designated (C99)
struct Point p3 = (struct Point){3, 4}; // compound literal
```

Uninitialized local variables are one of C's most common bug sources:

```c
// C Deep Dive: uninitialized variable
int x;              // garbage value
printf("%d\n", x);  // undefined behavior: indeterminate value
```

**Auto's approach: mandatory initialization.** Auto requires that every
variable be initialized at declaration. Default values are provided by
constructor functions:

```auto
// Auto: all variables initialized
type Config {
    name str
    value int
    active bool
}

fn Config.default() Config {
    Config("unnamed", 0, false)
}

fn Config.with_name(name str) Config {
    Config(name, 0, true)
}

fn main() {
    let default_cfg Config = Config.default()
    let named_cfg Config = Config.with_name("production")
    print("Default:", default_cfg.name, default_cfg.active)
    print("Named:", named_cfg.name, named_cfg.active)
}
```

<Listing path="listings/ch13/listing-13-02" title="Initialization patterns" />

> **C Deep Dive:** Designated initializers (`{.x = 1, .y = 2}`) are one of
> C99's best features. They make structure initialization self-documenting
> and order-independent. Auto uses constructor functions for the same purpose,
> providing named initialization with type safety.

---

## 13.5 Machine Model

At the lowest level, C's machine model treats memory as a flat array of bytes.
Each byte has an address, and every object occupies a contiguous range of
addresses:

```c
// C Deep Dive: memory as byte array
int value = 0x41424344;
unsigned char *bytes = (unsigned char *)&value;
for (size_t i = 0; i < sizeof(value); i++) {
    printf("byte[%zu] = 0x%02x\n", i, bytes[i]);
}
// Little-endian output:
// byte[0] = 0x44  ('D')
// byte[1] = 0x43  ('C')
// byte[2] = 0x42  ('B')
// byte[3] = 0x41  ('A')
```

The machine model has important implications:

- **Endianness**: the byte order of multi-byte values differs by platform.
- **Padding**: structures may contain unnamed padding bytes between members.
- **Trap representations**: some bit patterns may cause hardware faults.
- **Signedness**: negative integers use two's complement (mandatory in C23).

**Auto's approach: abstracted machine model.** Auto programmers do not need
to think about endianness, padding, or trap representations. The a2c
transpiler handles these details when generating C code:

```auto
// Auto: no concern for byte-level representation
let value int = 0x41424344
print("Value:", value)
// a2c generates correct code for the target platform
```

> **C Deep Dive:** Before C23, signed integer representation was implementation-
> defined. C could theoretically use sign-magnitude or one's complement. In
> practice, every implementation used two's complement. C23 finally made it
> mandatory, removing a source of portability concern that never mattered in
> reality.

---

## Quick Reference

| Concept              | C mechanism                | Auto mechanism            |
|----------------------|----------------------------|---------------------------|
| Dynamic allocation   | `malloc`, `calloc`         | Automatic, containers     |
| Deallocation         | `free`                     | Automatic cleanup         |
| Resize allocation    | `realloc`                  | Growable containers       |
| Storage duration     | Static / automatic / alloc | Automatic                 |
| Forward declaration  | Prototypes                 | Not needed                |
| Initialization       | Multiple forms             | Constructors, mandatory   |
| Designated init      | `{.field = val}`           | Constructor arguments     |
| Uninitialized vars   | Allowed (dangerous)        | Forbidden                 |
| Machine model        | Byte array, endianness     | Abstracted                |

---

*Storage and initialization are the foundation of reliable programs. Auto
eliminates the entire class of memory management bugs by removing manual
allocation and requiring initialization. The next chapter covers I/O and
text processing.*
