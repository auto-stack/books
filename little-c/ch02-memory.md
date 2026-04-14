# Working with Memory

This chapter explores how memory works in C and how Auto abstracts the details.
You will learn about memory layout, pointers, arrays, strings, dynamic memory,
function pointers, and how Auto prevents common memory errors.

## 21. Memory Layout

Every C program divides memory into four segments:

```
+------------------+
| Code (text)      |  compiled instructions
+------------------+
| Data / BSS       |  global and static variables
+------------------+
| Heap             |  malloc/free region (grows up)
+------------------+
| Stack            |  local variables, call frames (grows down)
+------------------+
```

- **Code** holds the compiled machine instructions.
- **Data** holds initialized globals; BSS holds zero-initialized globals.
- **Heap** is for dynamically allocated memory (`malloc`/`free`).
- **Stack** is for local variables and function call frames.

Auto maps naturally onto this model. `let` and `var` declarations inside
functions go on the stack. Auto's AutoFree system manages heap allocations
automatically, so you never call `malloc` or `free` by hand.

<Listing name="memory-layout" file="listings/ch02/listing-02-01">

```auto
fn main() {
    let local int = 42
    print("Stack value:", local)

    // In C, global vars live in data segment
    // In Auto, all memory management is automatic
    print("Auto manages stack and heap automatically")
}
```

</Listing>

## 22. Pointers and Addresses

In C, every variable lives at a memory address. You get the address with `&`
and dereference with `*`:

```c
int x = 42;
int *p = &x;    // p holds the address of x
printf("%d\n", *p);  // prints 42
```

Auto does not expose raw pointers. Instead, it uses optional references (`?T`)
to represent a value that may or may not reference another value. The a2c
transpiler generates pointer code behind the scenes.

<Listing name="pointers" file="listings/ch02/listing-02-02">

```auto
fn main() {
    let x int = 42
    let ptr ?int = x  // Auto optional reference
    print("Value:", x)
    print("Has reference:", ptr != nil)
}
```

</Listing>

## 23. Arrays and Pointer Arithmetic

In C, arrays and pointers are closely related. `a[i]` is equivalent to
`*(a + i)`. Auto arrays map to C arrays with bounds-checked access where
possible.

<Listing name="arrays" file="listings/ch02/listing-02-03">

```auto
fn main() {
    let scores [5]int = [5]int{90, 85, 78, 92, 88}
    for i in 0..5 {
        print("Score", i, "=", scores[i])
    }
    print("First three printed via loop")
    for i in 0..3 {
        print(scores[i])
    }
}
```

</Listing>

Auto's `a[i]` maps directly to C's `a[i]`. Slicing (`a[1..3]`) is a
compile-time feature in Auto; the transpiler generates a loop or copy.

> **C Only**: C allows pointer arithmetic like `p + 1` to step through memory.
> Auto does not expose this. Use array indexing instead.

## 24. Strings as Character Arrays

C strings are arrays of `char` ending with a null terminator (`'\0'`). The
string `"Hello"` occupies 6 bytes: `H`, `e`, `l`, `l`, `o`, `\0`.

Auto's `str` type maps to `char*` in C. Auto handles null termination
automatically. String concatenation (`+`) in Auto generates the appropriate
`malloc`, `strcpy`, and `strcat` calls in C.

<Listing name="strings" file="listings/ch02/listing-02-04">

```auto
fn main() {
    let greeting str = "Hello"
    let name str = "World"
    let full str = greeting + " " + name
    print(full)
    print("Length:", len(full))
}
```

</Listing>

The `len()` built-in maps to `strlen()` in C. Auto guarantees strings are
always null-terminated.

## 25. Dynamic Memory

C uses `malloc` to allocate heap memory and `free` to release it:

```c
int *arr = malloc(10 * sizeof(int));
// ... use arr ...
free(arr);
```

Auto's AutoFree system tracks allocations and frees them automatically at the
end of their scope. You never write `malloc` or `free` in Auto code.

<Listing name="dynamic-memory" file="listings/ch02/listing-02-05">

```auto
fn main() {
    // Auto handles memory automatically via AutoFree
    // No manual malloc/free needed
    var total int = 0
    for i in 1..11 {
        total = total + i
    }
    print("Sum 1..10 =", total)

    // C equivalent would use malloc:
    // int *arr = malloc(10 * sizeof(int));
    // ... use arr ...
    // free(arr);
    // Auto does this automatically
}
```

</Listing>

## 26. Memory Leaks and Undefined Behavior

The most common C memory errors are:

- **Memory leaks**: forgetting to `free` allocated memory.
- **Use-after-free**: accessing memory after it has been freed.
- **Buffer overflow**: writing past the end of an array.
- **Dangling pointers**: using a pointer whose target has gone out of scope.

Auto prevents these by design:

- AutoFree ensures every allocation is freed when its scope ends.
- No raw pointers means no use-after-free or dangling pointer bugs.
- Array bounds are checked at compile time where possible.

## 27. const and volatile

C's `const` qualifier tells the compiler a value will not change:

```c
const int x = 42;
x = 10;  // compiler error
```

Auto's `let` is equivalent to `const` — once bound, the value cannot be
reassigned. Auto's `var` is like a plain C variable.

C's `volatile` qualifier tells the compiler not to optimize away reads/writes
(e.g., for hardware registers). Auto does not provide `volatile`; this is a
C-only feature for low-level systems programming.

## 28. Function Pointers and Callbacks

C uses function pointers for callbacks and strategy patterns:

```c
int (*op)(int, int);
op = &add;
result = op(3, 4);
```

Auto replaces function pointers with the `spec` system, which provides a
type-safe interface for polymorphic behavior.

<Listing name="function-pointers" file="listings/ch02/listing-02-06">

```auto
spec IntOp {
    fn apply(a int, b int) int
}

type Adder {}

fn Adder.apply(a int, b int) int {
    a + b
}

type Multiplier {}

fn Multiplier.apply(a int, b int) int {
    a * b
}

fn compute(op Adder, a int, b int) int {
    op.apply(a, b)
}

fn main() {
    let adder Adder = Adder()
    let mult Multiplier = Multiplier()
    print("3 + 4 =", compute(adder, 3, 4))
}
```

</Listing>

## 29. Deep vs Shallow Copies

In C, assigning a struct copies it by value (deep copy of fields). Assigning a
pointer only copies the address (shallow copy):

```c
struct Point a = {1, 2};
struct Point b = a;     // deep copy: b has its own x, y
struct Point *p = &a;   // shallow: p points to a
```

Auto uses value semantics by default. Assigning `let b Point = a` creates an
independent copy, just like C struct assignment. Auto's `?T` optional
references provide the equivalent of pointers when you need shared access.

## 30. Practice: Memory Management

Apply what you have learned about memory, recursion, and Auto's guarantees.

<Listing name="memory-practice" file="listings/ch02/listing-02-07">

```auto
fn fibonacci(n int) int {
    if n <= 1 {
        n
    } else {
        fibonacci(n - 1) + fibonacci(n - 2)
    }
}

fn main() {
    for i in 0..10 {
        print("fib(" + str(i) + ") =", fibonacci(i))
    }
}
```

</Listing>

The recursive `fibonacci` function uses the stack for each call frame. Auto
ensures no memory leaks even with deep recursion — stack frames are reclaimed
automatically when functions return.

## Quick Reference

| Concept | Auto | C |
|---------|------|---|
| Stack variable | `let x int = 5` | `int x = 5;` |
| Heap allocation | automatic (AutoFree) | `malloc(size)` |
| Heap free | automatic | `free(ptr)` |
| Pointer | not exposed | `int *p = &x` |
| Optional ref | `?T` | `T*` (nullable) |
| Array | `[N]T{...}` | `T arr[N] = {...}` |
| String | `str` | `char*` |
| String concat | `a + b` | `strcat`/`malloc` |
| String length | `len(s)` | `strlen(s)` |
| Immutable | `let x` | `const int x` |
| Mutable | `var x` | `int x` |
| Function pointer | `spec` + `type` | `int (*fn)(int, int)` |
| Value copy | default behavior | struct assignment |
| Null check | `x != nil` | `p != NULL` |
