# Chapter 6: Derived Data Types

> Level 1 — Acquaintance
>
> Building complex data structures from basic types: arrays, pointers, structs, and type aliases.

C derives complex types from its basic building blocks. Arrays group elements of the
same type contiguously in memory. Pointers reference other objects indirectly. Structs
bundle heterogeneous fields into one unit. Type aliases give new names to existing
types. Auto provides all of these with a cleaner syntax.

---

## 6.1 Arrays

An **array** is a fixed-size sequence of elements of the same type, stored contiguously
in memory. The array size is part of its type and cannot change at runtime.

```c
// C
int primes[5] = { 2, 3, 5, 7, 11 };
printf("first = %d\n", primes[0]);    // first = 2
printf("count = %zu\n", sizeof(primes)/sizeof(primes[0]));  // count = 5
```

```auto
// Auto
let primes [5]int = [5]int{2, 3, 5, 7, 11}
print("first =", primes[0])
print("count =", len(primes))
```

Key differences:

| Feature             | C                          | Auto                        |
|---------------------|----------------------------|------------------------------|
| Declaration         | `int a[5];`               | `let a [5]int`              |
| Size in type        | Prefix: `int a[N]`        | Suffix: `[N]int`            |
| Array length        | `sizeof(a)/sizeof(a[0])`  | `len(a)`                    |
| Bounds checking     | None (undefined behavior) | Runtime check (default)     |
| Multidimensional    | `int m[3][4]`             | `[3][4]int`                 |

**Array-to-pointer decay:** In C, an array name in most contexts decays to a pointer
to its first element. This is the source of many subtle bugs. Auto does not have
this decay — arrays remain arrays.

```c
// C: decay in action
int a[5] = {1,2,3,4,5};
int *p = a;        // a decays to &a[0]
p[10] = 99;        // UNDEFINED BEHAVIOR: out of bounds
```

> **Takeaway:** C arrays have no bounds checking. Accessing `a[10]` on a 5-element
> array compiles without error but corrupts memory. Auto inserts runtime bounds
> checks by default.

<Listing path="listings/ch06/listing-06-01" title="Arrays and iteration" />

---

## 6.2 Pointers as Opaque Types

> **C Deep Dive:** A pointer is a variable that stores the address of another object.
> Pointers are C's most powerful and most dangerous feature. They enable dynamic data
> structures, efficient parameter passing, and hardware access — but also memory leaks,
> dangling references, and buffer overflows.

```c
// C: basic pointer usage
int x = 42;
int *ptr = &x;         // ptr holds the address of x
printf("*ptr = %d\n", *ptr);   // *ptr = 42 (dereference)
*ptr = 99;              // modifies x through ptr
```

Auto does not expose raw pointers. Instead it provides:

- **References** — safe, non-null handles managed by the compiler.
- **Optional types** (`?T`) — nullable references that must be checked before use.

```auto
// Auto: no raw pointers
let x int = 42
// Auto manages references; no address-of operator needed
print("Value:", x)

// Optional type for nullable references
let maybe ?int = x
if maybe != nil {
    print("Has value:", maybe)
}
```

The pointer concept map between C and Auto:

| C concept           | Auto equivalent         | Notes                              |
|---------------------|------------------------|-------------------------------------|
| `T *p`             | Reference / `&T`       | Non-null, compiler-managed         |
| `NULL`             | `nil`                  | Explicit null for optional types    |
| `T *p` (nullable)  | `?T`                   | Must check before use              |
| `*p` (dereference) | Direct access           | No dereference syntax needed       |
| `&x` (address-of)  | Automatic              | Compiler manages addresses         |
| `p->field`         | `p.field` or `p.method()` | Uniform access syntax           |

<Listing path="listings/ch06/listing-06-02" title="Pointers as opaque references" />

> **Takeaway:** If you are coming from C, think of Auto references as pointers that
> are never null and are automatically freed. Optional types replace nullable pointers
> with explicit null checks.

---

## 6.3 Structures

A **structure** groups named fields of possibly different types into a single unit:

```c
// C
struct Fraction {
    int num;
    int den;
};

struct Fraction half = { .num = 1, .den = 2 };
printf("1/2 = %f\n", (double)half.num / half.den);
```

```auto
// Auto
type Fraction {
    num int
    den int
}

let half Fraction = Fraction(1, 2)
print("1/2 =", half.to_float(half))
```

Key differences in struct handling:

| Feature            | C                              | Auto                          |
|--------------------|--------------------------------|-------------------------------|
| Declaration        | `struct Name { ... };`         | `type Name { ... }`           |
| Usage              | `struct Name var;`             | `let var Name`                |
| Field access       | `var.field` or `ptr->field`    | `var.field` (uniform)         |
| Initialization     | `{ .field = value }`           | `Name(value, ...)` or `.new()`|
| Methods            | None (separate functions)      | Associated functions          |
| Type alias needed  | Often `typedef struct Name Name;` | Automatic                 |

**Associated functions** in Auto let you attach behavior to a type:

```auto
type Fraction {
    num int
    den int
}

fn Fraction.new(n int, d int) Fraction {
    Fraction(n, d)
}

fn Fraction.to_float(f Fraction) float {
    float(f.num) / float(f.den)
}
```

This transpiles to C as:

```c
struct Fraction Fraction_new(int n, int d) { ... }
float Fraction_to_float(struct Fraction f) { ... }
```

<Listing path="listings/ch06/listing-06-03" title="Structures and type aliases" />

> **Takeaway:** Auto's `type` keyword replaces `struct`, `typedef`, and adds
> associated functions. The transpiler generates the C `struct` and companion
> functions automatically.

---

## 6.4 Type Aliases

C uses `typedef` to create alternative names for types:

```c
typedef unsigned int uint;
typedef struct Point Point;       // convenience alias
typedef int (*Comparator)(const void *, const void *);  // function pointer type
```

Auto uses the `type` keyword for all type definitions and aliases:

```auto
type uint = u32                    // alias for existing type
type Point {                       // new struct type
    x int
    y int
}
type Callback = fn(int, int) int   // function type alias
```

The C-to-Auto mapping for `typedef`:

| C typedef                    | Auto equivalent              |
|------------------------------|------------------------------|
| `typedef int Width;`         | `type Width = int`           |
| `typedef struct S S;`        | Not needed (`type S {}`)     |
| `typedef void (*Fn)(int);`   | `type Fn = fn(int)`          |
| `typedef int Arr[10];`       | `type Arr = [10]int`         |

> **Takeaway:** In C, `typedef` is optional but widely used for clarity. In Auto,
> `type` is the universal keyword for defining new types and aliases, eliminating
> the `struct` + `typedef` ceremony.

---

## Quick Reference

| Concept          | C syntax                        | Auto syntax                   |
|------------------|---------------------------------|-------------------------------|
| Array declare    | `int a[5];`                    | `let a [5]int`               |
| Array init       | `{ 1, 2, 3 }`                  | `[5]int{1, 2, 3}`            |
| Array element    | `a[i]`                         | `a[i]`                        |
| Array length     | `sizeof(a)/sizeof(a[0])`       | `len(a)`                      |
| Pointer declare  | `int *p;`                      | Not exposed                   |
| Null pointer     | `NULL`                         | `nil`                         |
| Optional ref     | `int *p` (nullable)            | `?int`                        |
| Struct declare   | `struct S { int x; };`         | `type S { x int }`            |
| Struct init      | `{ .x = 1 }`                   | `S(1)` or `S.new(1)`          |
| Field access     | `s.field` / `p->field`         | `s.field` (uniform)           |
| Type alias       | `typedef int Width;`           | `type Width = int`            |
| Associated fn    | Separate function              | `fn S.method(self) ...`       |

---

*Next: [Chapter 7 — Functions](ch07-functions.md)*
