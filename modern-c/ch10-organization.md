# Chapter 10: Organization and Documentation

> Level 2 — Cognition
>
> Structuring programs across files: interfaces, implementations, and documentation.

A program that fits in one file is a script. A program that spans dozens of
files is a system. This chapter covers how C organizes code into interface and
implementation, and how Auto's module system provides a cleaner alternative.

---

## 10.1 Interface Documentation

In C, the **interface** is declared in a **header file** (`.h`) and the
**implementation** lives in a **source file** (`.c`). The header is a contract:

```c
// geometry.h — interface
#ifndef GEOMETRY_H
#define GEOMETRY_H

typedef struct {
    float width;
    float height;
} Rectangle;

float Rectangle_area(Rectangle r);
float Rectangle_perimeter(Rectangle r);

#endif
```

```c
// geometry.c — implementation
#include "geometry.h"

float Rectangle_area(Rectangle r) {
    return r.width * r.height;
}

float Rectangle_perimeter(Rectangle r) {
    return 2.0f * (r.width + r.height);
}
```

Other files that need `Rectangle` include the header:

```c
// main.c
#include "geometry.h"
#include <stdio.h>

int main(void) {
    Rectangle r = {4.0f, 6.0f};
    printf("Area: %f\n", Rectangle_area(r));
    return 0;
}
```

**Documentation comments.** C uses `/** ... */` for documentation. Many
projects adopt conventions similar to Doxygen:

```c
/**
 * @brief Calculate the area of a rectangle.
 * @param r The rectangle
 * @return The area as a float
 */
float Rectangle_area(Rectangle r);
```

**Auto's approach.** Auto replaces header files with its `mod` and `use`
system. Types and their associated functions form a natural interface:

```auto
// geometry.at — both interface and implementation
type Rectangle {
    width float
    height float
}

fn Rectangle.new(w float, h float) Rectangle {
    Rectangle(w, h)
}

fn Rectangle.area(r Rectangle) float {
    r.width * r.height
}

fn Rectangle.perimeter(r Rectangle) float {
    2.0 * (r.width + r.height)
}
```

Another file uses the module with `use`:

```auto
// main.at
use geometry

fn main() {
    let r Rectangle = Rectangle.new(4.0, 6.0)
    print("Area:", r.area(r))
}
```

<Listing path="listings/ch10/listing-10-01" title="Interface documentation" />

The a2c transpiler generates the `.h` file automatically from the Auto source.
You never write header guards, forward declarations, or `#include` directives
by hand.

> **Takeaway:** In C, the header file is the interface. Keep it minimal --
> declare types and function signatures, but not implementation details.
> Auto makes this separation automatic.

---

## 10.2 Implementation

Separating interface from implementation serves several purposes:

1. **Compilation speed.** Changing an implementation file does not force
   recompilation of files that only include the header.
2. **Encapsulation.** Consumers of the interface see only what the header
   exposes. Internal details remain hidden.
3. **Parallel development.** Teams can agree on a header and then implement
   independently.

**Multi-file projects in C** require a build system. A simple `Makefile`:

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -std=c17

myapp: main.o geometry.o
	$(CC) $(CFLAGS) -o $@ $^

main.o: main.c geometry.h
	$(CC) $(CFLAGS) -c main.c

geometry.o: geometry.c geometry.h
	$(CC) $(CFLAGS) -c geometry.c

clean:
	rm -f *.o myapp
```

**Multi-file projects in Auto** use `pac.at` for package configuration:

```
name: "geometry-app"
version: "0.1.0"
lang: "c"

app("geometry-app") {}
```

The `auto build` command reads `pac.at`, resolves dependencies between `.at`
files, and invokes a2c followed by the C compiler. No manual Makefile needed.

**Documentation as discipline.** Every public function should have a comment
that answers three questions:

- **What** does this function do?
- **What** are its parameters?
- **What** does it return?

In C:

```c
/**
 * Sort an array of integers in ascending order.
 * @param arr  The array to sort
 * @param n    Number of elements in arr
 * @return     0 on success, -1 on error
 */
int sort_ints(int* arr, size_t n);
```

In Auto, function names and type signatures carry more information, reducing
the need for verbose documentation:

```auto
// The name and types are self-documenting
fn sort_ascending(arr []int) []int {
    // implementation
}
```

> **Takeaway:** Documentation is part of the interface. Write it for every
> public function. In Auto, strong typing and descriptive names reduce but do
> not eliminate the need for comments.

---

## Quick Reference

| Concept          | C mechanism            | Auto mechanism            |
|------------------|------------------------|---------------------------|
| Interface        | `.h` header file       | `mod` (module)            |
| Implementation   | `.c` source file       | `.at` source file         |
| Import           | `#include "file.h"`    | `use module_name`         |
| Header guard     | `#ifndef` / `#define`  | Automatic                 |
| Forward declare  | `struct Foo;`          | Automatic                 |
| Build config     | `Makefile`, `CMake`    | `pac.at`                  |
| Build command    | `make`                 | `auto build`              |
| Doc comments     | `/** @brief ... */`    | `//` and self-documenting |

---

*With code organized and documented, the next chapter dives into the most
powerful -- and dangerous -- feature of C: pointers.*
