# Chapter 11: Pointers

> Level 2 — Cognition
>
> The most powerful and dangerous feature of C, and how Auto eliminates the danger.

Pointers are C's defining feature. They give direct access to memory, enable
efficient data structures, and underlie every non-trivial C program. They are
also the source of most C bugs: null dereferences, dangling pointers, buffer
overflows, and use-after-free errors.

Auto eliminates raw pointers from user code while preserving the expressive
power they provide. This chapter is a deep dive into C pointers so you
understand what Auto handles for you.

---

## 11.1 Pointer Operations

A **pointer** is a variable that stores the address of another variable. C
provides two fundamental pointer operators:

- `&` (address-of): obtains the memory address of a variable
- `*` (dereference): accesses the value at a memory address

```c
// C Deep Dive: basic pointer operations
int x = 42;
int *ptr = &x;       // ptr holds the address of x
printf("Address: %p\n", (void*)ptr);
printf("Value: %d\n", *ptr);    // dereference: prints 42

*ptr = 99;            // modify x through the pointer
printf("x is now: %d\n", x);    // prints 99
```

**Pointer arithmetic.** Pointers to array elements support arithmetic:

```c
// C Deep Dive: pointer arithmetic
int arr[5] = {10, 20, 30, 40, 50};
int *p = arr;         // p points to arr[0]

p += 3;               // p now points to arr[3]
printf("%d\n", *p);   // prints 40

int diff = p - arr;   // pointer subtraction: 3
```

The compiler multiplies the offset by `sizeof(int)`, so `p += 3` actually
adds `3 * sizeof(int)` bytes to the address. This is why pointer arithmetic
requires a typed pointer -- the type determines the element size.

**Auto's replacement.** Auto has no pointer type. Array indexing replaces
pointer arithmetic:

```auto
let arr [5]int = [5]int{10, 20, 30, 40, 50}
print("arr[3]:", arr[3])   // direct indexing, no pointers
```

<Listing path="listings/ch11/listing-11-01" title="Pointer operations" />

> **C Deep Dive:** In C, `arr[i]` is defined as `*(arr + i)`. The subscript
> operator is syntactic sugar for pointer arithmetic. Understanding this
> equivalence is essential for reading C code.

---

## 11.2 Pointers and Structures

Pointers to structures are ubiquitous in C. They enable efficient pass-by-
reference and linked data structures:

```c
// C Deep Dive: pointer to struct
typedef struct {
    float x;
    float y;
} Point;

Point p = {3.0f, 4.0f};
Point *ptr = &p;

// Access members through pointer
printf("x = %f\n", ptr->x);    // -> operator
printf("y = %f\n", ptr->y);

// Equivalent: (*ptr).x
printf("x = %f\n", (*ptr).x);
```

The `->` operator is syntactic sugar for dereferencing a struct pointer and
accessing a member: `ptr->member` is equivalent to `(*ptr).member`.

**Linked structures.** Pointers enable self-referential types:

```c
// C Deep Dive: linked list node
typedef struct Node {
    int data;
    struct Node *next;    // pointer to same type
} Node;

Node c = {30, NULL};
Node b = {20, &c};
Node a = {10, &b};

// Traverse: a -> b -> c
Node *current = &a;
while (current != NULL) {
    printf("%d ", current->data);
    current = current->next;
}
// Output: 10 20 30
```

**Auto's replacement.** Auto passes structures by value and uses associated
functions. Linked data structures use `enum` with variants:

```auto
type Point {
    x float
    y float
}

fn Point.distance_from_origin(p Point) float {
    (p.x * p.x + p.y * p.y) ** 0.5
}
```

<Listing path="listings/ch11/listing-11-02" title="Pointers and structures" />

> **C Deep Dive:** The `->` operator exists because `.` binds tighter than `*`.
> Writing `*ptr.x` would parse as `*(ptr.x)`, which is wrong. The `->` operator
> avoids this pitfall.

---

## 11.3 Pointers and Arrays

In C, arrays and pointers are deeply connected. When an array name is used in
an expression (except as `sizeof` operand), it **decays** to a pointer to its
first element:

```c
// C Deep Dive: array-to-pointer decay
int arr[5] = {10, 20, 30, 40, 50};
int *p = arr;        // arr decays to &arr[0]

// These are equivalent:
arr[2] == *(arr + 2);
*(p + 2) == p[2];     // pointers support [] too
```

This decay has important implications:

1. Arrays cannot be assigned (`arr2 = arr1` is illegal).
2. Arrays passed to functions become pointers -- `sizeof` gives pointer size,
   not array size.
3. Pointer arithmetic scales by element size automatically.

```c
// C Deep Dive: array parameter decay
void print_sum(int *arr, size_t n) {
    // sizeof(arr) == sizeof(int*) here, NOT array size!
    int sum = 0;
    for (size_t i = 0; i < n; i++) {
        sum += arr[i];
    }
    printf("Sum: %d\n", sum);
}
```

**Auto's replacement.** Auto arrays are proper types that carry their length:

```auto
let arr [5]int = [5]int{10, 20, 30, 40, 50}
let length int = len(arr)   // 5 — no decay, no information loss
print("Third element:", arr[2])
```

> **C Deep Dive:** The relationship between arrays and pointers is the most
> confusing aspect of C for newcomers. An array is not a pointer -- it merely
> converts to one in most contexts. `sizeof(arr)` gives the full array size,
> but only in the scope where `arr` is declared as an array.

---

## 11.4 Function Pointers

C allows pointers to functions, enabling callbacks and runtime polymorphism:

```c
// C Deep Dive: function pointer
int ascending(int a, int b) { return a - b; }
int descending(int a, int b) { return b - a; }

// Function pointer type
typedef int (*Comparator)(int, int);

void sort(int *arr, size_t n, Comparator cmp) {
    // sort using the provided comparator
    for (size_t i = 0; i < n - 1; i++) {
        for (size_t j = 0; j < n - i - 1; j++) {
            if (cmp(arr[j], arr[j+1]) > 0) {
                int tmp = arr[j];
                arr[j] = arr[j+1];
                arr[j+1] = tmp;
            }
        }
    }
}

int main(void) {
    int data[] = {5, 2, 8, 1, 9};
    sort(data, 5, ascending);    // sort ascending
    sort(data, 5, descending);   // sort descending
}
```

Function pointer syntax is notoriously opaque:

```c
// C Deep Dive: reading function pointer declarations
int (*cmp)(int, int);              // pointer to function(int,int)->int
void (*signal(int, void(*)(int)))(int);  // truly incomprehensible
```

**Auto's replacement: `spec`.** Auto provides `spec` as a safe, readable
replacement for function pointers and virtual dispatch:

```auto
spec Comparator {
    fn compare(a int, b int) int
}

type Ascending {}

fn Ascending.compare(a int, b int) int {
    if a < b { -1 } else if a > b { 1 } else { 0 }
}

type Descending {}

fn Descending.compare(a int, b int) int {
    if a > b { -1 } else if a < b { 1 } else { 0 }
}
```

Any type that implements `Comparator` can be used wherever a `Comparator` is
expected. The a2c transpiler generates vtables (function pointer tables) under
the hood.

<Listing path="listings/ch11/listing-11-03" title="Function pointers and spec" />

> **C Deep Dive:** Function pointers are C's only mechanism for runtime
> polymorphism. They are used in the standard library (`qsort`, `signal`),
> GUI frameworks (callbacks), and plugin architectures. Auto's `spec`
> provides the same capability with compile-time type safety.

---

## Quick Reference

| Concept                | C mechanism            | Auto mechanism            |
|------------------------|------------------------|---------------------------|
| Address of variable    | `&x`                   | Not exposed               |
| Dereference            | `*ptr`                 | Not exposed               |
| Pointer arithmetic     | `ptr + n`, `ptr++`     | Array indexing `arr[i]`   |
| Struct pointer access  | `ptr->member`          | Direct `p.member`         |
| Array decay            | Automatic              | Does not occur            |
| Null pointer           | `NULL`                 | `nil` (in specific types) |
| Function pointer       | `int (*f)(int, int)`   | `spec` with implementations |
| Linked structures      | `struct Node *next`    | `enum` variants           |
| Callbacks              | Function pointers      | `spec` implementations   |

---

*Pointers connect directly to how C models memory. The next chapter covers
the C memory model in full depth -- objects, representation, unions,
alignment, and the strict aliasing rule.*
