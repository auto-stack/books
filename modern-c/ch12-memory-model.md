# Chapter 12: The C Memory Model

> Level 2 — Cognition
>
> Objects, bytes, unions, effective types, alignment -- the deepest C internals.

This is the most technically dense chapter in the book. The C memory model
defines how data is stored, accessed, and interpreted at the byte level.
Understanding it is essential for writing correct low-level C and for
appreciating what Auto abstracts away.

---

## 12.1 Uniform Memory Model

In C, all data -- integers, floats, structs, arrays -- is stored as a
contiguous sequence of **bytes**. Each byte has a unique address, and every
object in memory can be inspected as raw bytes.

```c
// C Deep Dive: object representation
int x = 42;
unsigned char *bytes = (unsigned char*)&x;
printf("Byte 0: 0x%02x\n", bytes[0]);
printf("Byte 1: 0x%02x\n", bytes[1]);
// On little-endian: 0x2a, 0x00 (for int32)
```

Key concepts:

- **Object**: a region of storage that holds a value of a specific type.
- **Representation**: the sequence of bytes that encodes the value.
- **`sizeof`**: the number of bytes an object occupies.

```c
// C Deep Dive: sizes of common types
printf("sizeof(char):   %zu\n", sizeof(char));   // always 1
printf("sizeof(int):    %zu\n", sizeof(int));    // usually 4
printf("sizeof(float):  %zu\n", sizeof(float));  // usually 4
printf("sizeof(double): %zu\n", sizeof(double)); // usually 8
printf("sizeof(int*):   %zu\n", sizeof(int*));   // 4 or 8
```

The size of a type determines how many bytes pointer arithmetic advances.
`sizeof(char)` is always 1 by definition -- it is the fundamental unit of
storage in C.

> **C Deep Dive:** C guarantees that any object can be copied byte-by-byte
> using `memcpy`. This is the basis for serialization and deserialization.
> Auto provides the same guarantee for its value types.

---

## 12.2 Unions

A **union** is a type where all members share the same memory location. The
size of a union equals the size of its largest member:

```c
// C Deep Dive: union
union Value {
    int i;
    float f;
    char s[16];
};

union Value v;
v.i = 42;                // store as int
printf("%d\n", v.i);     // read as int: 42
v.f = 3.14f;             // overwrite with float
printf("%f\n", v.f);     // read as float: 3.14
// printf("%d\n", v.i);  // UNDEFINED BEHAVIOR: wrong type!
```

Reading from a member that was not the last one written is undefined behavior
in standard C (with exceptions for signedness variants). This makes bare
unions dangerous.

**Tagged unions** solve this by pairing a discriminant (tag) with the union:

```c
// C Deep Dive: tagged union
enum ValueType { VAL_INT, VAL_FLOAT, VAL_STRING };

struct TaggedValue {
    enum ValueType tag;
    union {
        int i;
        float f;
        char s[16];
    } data;
};

void describe(struct TaggedValue v) {
    switch (v.tag) {
        case VAL_INT:    printf("integer: %d\n", v.data.i); break;
        case VAL_FLOAT:  printf("float: %f\n", v.data.f); break;
        case VAL_STRING: printf("string: %s\n", v.data.s); break;
    }
}
```

**Auto's replacement: `enum` with data.** Auto provides tagged unions as a
first-class feature, eliminating the manual bookkeeping:

```auto
enum Value {
    IntVal int
    FloatVal float
    StrVal str
}

fn describe(v Value) str {
    is v {
        IntVal(n) => "integer: " + str(n)
        FloatVal(f) => "float: " + str(f)
        StrVal(s) => "string: " + s
    }
}
```

<Listing path="listings/ch12/listing-12-01" title="Memory model and unions" />

> **C Deep Dive:** Tagged unions are one of the most common patterns in C.
> They are so fundamental that Rust has `enum`, Swift has `enum with associated
> values`, and Auto has `enum` -- all providing the same capability with
> language support instead of manual discipline.

---

## 12.3 Memory and State

Every object in C has an **effective type** that determines how it may be
accessed. The C standard imposes the **strict aliasing rule**: an object
shall have its stored value accessed only through an lvalue expression that
has one of the following types:

- A type compatible with the effective type of the object
- A qualified version of a type compatible with the effective type
- A type that is the signed or unsigned type corresponding to the effective
  type
- A type that is a character type (`char`, `unsigned char`, `signed char`)

```c
// C Deep Dive: strict aliasing violation
int x = 42;
float *fp = (float*)&x;   // VIOLATION: float* cannot alias int
*fp = 3.14f;               // UNDEFINED BEHAVIOR

// Correct: use memcpy for type punning
float f;
memcpy(&f, &x, sizeof(f)); // well-defined byte-level copy
```

The strict aliasing rule exists because compilers assume pointers of different
types do not alias the same memory, enabling optimizations. Violating it
causes silent miscompilation -- the worst kind of bug.

> **C Deep Dive:** `char*` is the universal escape hatch. You can always
> access any object's bytes through a `char*` or `unsigned char*`. This is
> how `memcpy` and `printf` work internally.

---

## 12.4 Pointers to Unspecific Objects: `void*`

C's `void*` is a generic pointer that can point to any object type but cannot
be dereferenced directly:

```c
// C Deep Dive: void*
void *generic = &x;           // any pointer converts to void*
int *specific = generic;      // void* converts back implicitly

// Cannot dereference void*:
// *generic;                   // ERROR: incomplete type

// Must cast first:
printf("%d\n", *(int*)generic);
```

`void*` is used extensively in C for generic interfaces:

```c
void qsort(void *base, size_t nmemb, size_t size,
           int (*compar)(const void*, const void*));
```

Auto avoids `void*` entirely. Generic functions in Auto use type parameters
or `spec` constraints:

```auto
// Auto: no void*, generics are type-safe
fn max(a int, b int) int {
    if a > b { a } else { b }
}
```

> **C Deep Dive:** `void*` is the root cause of many C bugs. It bypasses the
> type system, so passing the wrong type to `qsort`'s comparator causes
> undefined behavior with no compiler warning. Auto's type system prevents
> this class of errors entirely.

---

## 12.5 Explicit Conversions

C allows explicit type conversions (casts) between any pointer types:

```c
// C Deep Dive: explicit conversion
int x = 0x41424344;
char *bytes = (char*)&x;        // int* to char*
printf("%c\n", bytes[0]);       // 'D' on little-endian

// Dangerous: unrelated types
float f = 1.0f;
int *ip = (int*)&f;             // float* to int*
printf("%d\n", *ip);            // implementation-defined
```

Cast categories:

| Cast                    | Safety           | Example                   |
|-------------------------|------------------|---------------------------|
| Integer to integer      | May lose value   | `(int)3.14`               |
| Pointer to integer      | Implementation   | `(uintptr_t)ptr`          |
| Integer to pointer      | Implementation   | `(int*)0x1234`            |
| Pointer to pointer      | Often UB         | `(float*)&int_var`        |
| Pointer to `void*`      | Always safe      | `(void*)ptr`              |
| `void*` to pointer      | Safe if correct  | `(int*)void_ptr`          |

**Auto's approach.** Auto provides explicit, safe conversion functions:

```auto
let x int = 42
let f float = float(x)   // safe, well-defined conversion
print("int to float:", f)
```

Conversions between incompatible types are caught at compile time. There is
no way to reinterpret bytes as a different type without going through a
byte-level interface.

> **C Deep Dive:** The C cast operator `(Type)value` is one of the most
> dangerous features in the language. It tells the compiler "trust me, I
> know what I'm doing" -- and often, the programmer is wrong. C++ introduced
> `static_cast`, `reinterpret_cast`, and `dynamic_cast` to distinguish
> these cases. Auto eliminates the need for most casts entirely.

---

## 12.6 Effective Types

When memory is dynamically allocated, it initially has no effective type. The
type is established when a value is stored through a typed lvalue:

```c
// C Deep Dive: effective types for allocated memory
void *raw = malloc(sizeof(int));
int *ip = (int*)raw;
*ip = 42;                  // effective type of *raw is now int
printf("%d\n", *ip);       // OK: access matches effective type

float *fp = (float*)raw;
*fp = 3.14f;               // effective type is now float
printf("%f\n", *fp);       // OK
// printf("%d\n", *ip);    // UB: effective type changed to float
```

This matters because the compiler is free to assume that an `int*` and a
`float*` never point to the same memory (strict aliasing). Changing the
effective type and then accessing through the old type is undefined behavior.

Auto's type system prevents this entirely. Memory is always accessed through
its declared type. There is no way to change the effective type of a variable.

> **C Deep Dive:** Effective types and strict aliasing together form the most
> subtle area of C semantics. Compiler optimizations (especially auto-
> vectorization) rely on strict aliasing. The `-fstrict-aliasing` flag in
> GCC and Clang enables these optimizations. Use `-Wstrict-aliasing` to get
> warnings about potential violations.

---

## 12.7 Alignment

Every C type has an **alignment requirement** -- the number of bytes between
successive addresses at which objects of that type can be allocated:

```c
// C Deep Dive: alignment
printf("alignof(char):   %zu\n", alignof(char));   // 1
printf("alignof(int):    %zu\n", alignof(int));    // usually 4
printf("alignof(double): %zu\n", alignof(double)); // usually 8

// Explicit alignment
alignas(16) int aligned_x = 42;  // 16-byte aligned
```

Misaligned access can cause:

- **Performance degradation** on x86 (hardware handles it slowly)
- **Bus errors** on ARM and other architectures (program crashes)
- **SIMD failures** (vector operations require 16/32/64-byte alignment)

C23 provides `alignas` and `alignof` (or `_Alignas` and `_Alignof`):

```c
// C Deep Dive: alignment in structures
struct aligned_data {
    alignas(16) float vec[4];  // SIMD-friendly alignment
    int count;
};
```

The compiler may insert **padding bytes** between structure members to satisfy
alignment:

```c
struct Example {
    char  a;    // 1 byte + 3 padding
    int   b;    // 4 bytes
    char  c;    // 1 byte + 3 padding
};
// sizeof(struct Example) == 12 (not 6)
```

<Listing path="listings/ch12/listing-12-02" title="Effective types and alignment" />

**Auto's approach.** Auto handles alignment automatically. The a2c transpiler
adds appropriate `alignas` specifiers and reorders structure members for
optimal packing. Programmers never need to think about alignment.

> **C Deep Dive:** `malloc` always returns memory aligned to `max_align_t`,
> the maximum fundamental alignment. For extended alignments (e.g., 64-byte
> for AVX-512), use `aligned_alloc` or `posix_memalign`. Auto wraps these
> automatically.

---

## Quick Reference

| Concept              | C mechanism                | Auto mechanism            |
|----------------------|----------------------------|---------------------------|
| Object representation| Bytes via `unsigned char*` | Abstracted                |
| Tagged union         | `struct { enum + union }`  | `enum` with data variants |
| Effective type       | Runtime property           | Always declared type      |
| Strict aliasing      | Compiler assumption        | Enforced by type system   |
| Generic pointer      | `void*`                   | Not exposed               |
| Type punning         | Pointer cast or `memcpy`   | Explicit conversions only |
| Alignment            | `alignas`, `alignof`       | Automatic                 |
| Structure padding    | Compiler-inserted          | Automatic                 |
| Size query           | `sizeof`                  | `sizeof`                  |
| Byte copy            | `memcpy`                  | `copy`                    |

---

*This completes Level 2 -- Cognition. You now understand the C memory model
at the byte level and how Auto abstracts its dangers. The next level enters
the experience phase, where we put this knowledge to work.*
