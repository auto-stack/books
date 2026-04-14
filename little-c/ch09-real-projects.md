# Chapter 9: Building Real Projects

> Sections 91--100
> Everything you have learned comes together. Build libraries, tools, servers, and parsers.

Previous chapters covered C's building blocks and Auto's safer alternatives. Now it is
time to build real software. This chapter walks through complete projects -- from small
libraries to CLI tools, HTTP servers, and text parsers.

Each section presents both the C approach (what you would write manually) and the Auto
approach (what you write instead). By the end, you will have the patterns to build your
own projects.

---

## 91. Designing Small Libraries

A good library has a clear API, minimal dependencies, and composable building blocks.

**C library pattern:**
- Header file (`.h`) declares the public API
- Implementation file (`.c`) contains the logic
- Prefix all names to avoid collisions (e.g., `vec2_add`, `vec2_length`)

```c
/* vec2.h */
typedef struct { float x; float y; } Vec2;
Vec2 vec2_new(float x, float y);
Vec2 vec2_add(Vec2 a, Vec2 b);
float vec2_length(Vec2 v);
```

**Auto library pattern:**
- Types group related data
- Methods on types provide the API
- `mod` and `use` organize modules

```auto
type Vec2 { x float, y float }
fn Vec2.new(x float, y float) Vec2 { ... }
fn Vec2.add(a Vec2, b Vec2) Vec2 { ... }
fn Vec2.length(v Vec2) float { ... }
```

Auto's method syntax keeps APIs clean. The type name acts as a namespace, replacing
C's manual prefixing convention.

<Listing id="listing-09-01" title="Designing a small library" path="listings/ch09/listing-09-01" />

---

## 92. Building a CLI Tool

Command-line tools parse arguments and execute commands. In C, you use `argc`/`argv`
or a library like `getopt`:

```c
int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <command>\n", argv[0]);
        return 1;
    }
    if (strcmp(argv[1], "add") == 0) {
        printf("Adding task...\n");
    } else if (strcmp(argv[1], "list") == 0) {
        printf("Listing tasks...\n");
    }
}
```

Auto provides a cleaner interface:

```auto
fn main(args [str]) {
    is args[1] {
        "add"  => print("Adding task...")
        "list" => print("Listing tasks...")
        else   => print("Unknown command")
    }
}
```

The `main(args [str])` signature tells Auto you want command-line arguments as an
array of strings. The `is` expression replaces the verbose `if`/`else if` chain.

<Listing id="listing-09-02" title="Building a CLI tool" path="listings/ch09/listing-09-02" />

---

## 93. Tiny HTTP Server

Building an HTTP server in C requires socket programming:

```c
#include <sys/socket.h>
int server = socket(AF_INET, SOCK_STREAM, 0);
bind(server, (struct sockaddr *)&addr, sizeof(addr));
listen(server, 10);
int client = accept(server, NULL, NULL);
char buf[4096];
read(client, buf, sizeof(buf));
write(client, "HTTP/1.1 200 OK\r\n\r\nHello!", 26);
```

This is low-level: you manage sockets, parse HTTP requests manually, and handle
errors at every step. Production servers add epoll/kqueue for async I/O.

Auto provides higher-level abstractions for request handling:

```auto
type Request { method str, path str }
type Response { status int, body str }

fn handle_request(req Request) Response {
    is req.path {
        "/"     => Response(200, "Welcome!")
        "/about" => Response(200, "About page")
        else    => Response(404, "Not found")
    }
}
```

The routing logic is declarative. You define request types and response types, then
pattern-match on the path. Auto handles the socket plumbing.

<Listing id="listing-09-03" title="Tiny HTTP server" path="listings/ch09/listing-09-03" />

---

## 94. Key-Value Store

A key-value store combines data structures with file I/O:

**C implementation:**
- Hash table for in-memory lookups
- `fopen`/`fwrite` for persistence
- Manual memory management for keys and values

```c
typedef struct { char key[64]; char value[256]; } Entry;
Entry store[1024];
int count = 0;

const char *get(const char *key) {
    for (int i = 0; i < count; i++)
        if (strcmp(store[i].key, key) == 0)
            return store[i].value;
    return NULL;
}
```

**Auto implementation:**
- Maps provide built-in key-value storage
- File I/O handled by the standard library
- No manual memory management

```auto
let store Map(str, str) = Map.new()
store.set("name", "Alice")
let name str = store.get("name")
```

The key-value store pattern appears everywhere: configuration, caching, databases.
Understanding the C implementation helps you appreciate what Auto automates.

---

## 95. Custom Allocator

Memory allocation in C uses `malloc` and `free` by default. For performance-critical
code, you can write custom allocators:

**Arena allocator:** Allocate a large block, hand out pieces, free everything at once.

```c
typedef struct {
    char *buf;
    size_t offset;
    size_t capacity;
} Arena;

void *arena_alloc(Arena *a, size_t size) {
    if (a->offset + size > a->capacity) return NULL;
    void *ptr = a->buf + a->offset;
    a->offset += size;
    return ptr;
}

void arena_free(Arena *a) {
    free(a->buf);
    a->offset = 0;
}
```

**Pool allocator:** Fixed-size blocks for same-sized objects. Faster than `malloc`
for repeated allocations of the same type.

Custom allocators are a C-only advanced topic. Auto's memory management system uses
arena-based allocation internally, so you get the performance benefits without writing
the allocator yourself.

---

## 96. Text Parser

Parsing is fundamental: configuration files, programming languages, data formats.
A simple tokenizer splits input into meaningful pieces.

**C tokenizer:**
```c
while (*input) {
    while (isspace(*input)) input++;
    if (!*input) break;
    char *start = input;
    while (*input && !isspace(*input)) input++;
    printf("Token: %.*s\n", (int)(input - start), start);
}
```

**Auto tokenizer:**
```auto
fn tokenize(input str) {
    let tokens int = 0
    for i in 0..len(input) {
        if input[i] == " " { tokens = tokens + 1 }
    }
    print("Found", tokens + 1, "tokens")
}
```

Auto's string handling makes parsers cleaner. No pointer arithmetic, no manual
null-termination, no buffer overflow risks.

<Listing id="listing-09-04" title="Text parser" path="listings/ch09/listing-09-04" />

---

## 97. Tiny Interpreter

An expression evaluator is a mini-interpreter. It parses arithmetic expressions and
computes the result:

```c
/* C expression evaluator (simplified) */
int eval(const char *expr) {
    int a, b;
    char op;
    sscanf(expr, "%d %c %d", &a, &op, &b);
    switch (op) {
        case '+': return a + b;
        case '-': return a - b;
        case '*': return a * b;
        case '/': return b != 0 ? a / b : 0;
    }
    return 0;
}
```

A real interpreter has more components:
1. **Lexer**: Converts text into tokens
2. **Parser**: Builds an abstract syntax tree (AST)
3. **Evaluator**: Walks the AST and computes results

Auto's `type` and `is` expressions make ASTs natural:

```auto
type Expr {
    Num  { value int }
    Add  { left Expr, right Expr }
    Mul  { left Expr, right Expr }
}

fn eval(e Expr) int {
    is e {
        Num  => e.value
        Add  => eval(e.left) + eval(e.right)
        Mul  => eval(e.left) * eval(e.right)
    }
}
```

---

## 98. Interfacing with SQLite

SQLite is the most deployed database in the world. Using it from C:

```c
#include <sqlite3.h>
sqlite3 *db;
sqlite3_open("test.db", &db);
sqlite3_exec(db, "CREATE TABLE users (name TEXT)", NULL, NULL, NULL);
sqlite3_exec(db, "INSERT INTO users VALUES ('Alice')", NULL, NULL, NULL);
sqlite3_close(db);
```

From Auto, use FFI:

```auto
sys extern fn sqlite3_open(path str, db *sqlite3) int
sys extern fn sqlite3_exec(db *sqlite3, sql str, ...) int
sys extern fn sqlite3_close(db *sqlite3) int
```

The FFI pattern is the same as calling any C library:
1. Declare the C functions with `sys extern`
2. Call them from Auto code
3. a2c generates the correct C function calls

Every C library becomes an Auto library through FFI.

---

## 99. Packaging and Documentation

A complete Auto project has this structure:

```
my-project/
    pac.at          # Project manifest
    src/
        main.at     # Entry point
        lib.at      # Library module
    tests/
        main.at     # Tests
    docs/           # Documentation
```

**pac.at** declares the project:

```auto
name: "my-project"
version: "1.0.0"
lang: "c"

app("my-project") {}
```

**Documentation** in Auto uses doc comments:

```auto
// Adds two vectors and returns the result.
// Both vectors must have the same dimension.
fn Vec2.add(a Vec2, b Vec2) Vec2 {
    Vec2(a.x + b.x, a.y + b.y)
}
```

Build and run:
```bash
$ auto build       # Compile the project
$ auto run         # Run the compiled binary
$ auto t           # Run tests
$ auto doc         # Generate documentation
```

---

## 100. Practice: Build Your Own Project

This is your capstone exercise. Use everything you have learned to build a project
from scratch.

<Listing id="listing-09-05" title="Build your own project" path="listings/ch09/listing-09-05" />

**Project ideas:**

1. **Calculator**: Parse and evaluate arithmetic expressions (combine sections 96-97)
2. **File converter**: Read CSV, output JSON (combine sections 94, 96)
3. **Mini database**: Key-value store with file persistence (sections 93-94)
4. **Static site generator**: Read markdown files, output HTML
5. **Task manager**: CLI tool with add/list/complete commands (section 92)

**Steps for any project:**

1. Define your types first (data model)
2. Write the core logic as functions on those types
3. Add a CLI or API interface
4. Write tests for each function
5. Package it with `pac.at`

Choose one idea, implement it, and iterate. The template in listing-09-05 is your
starting point. Replace the placeholder types with your own, add functions, and build
something useful.

---

## Quick Reference

| Section | Topic               | C Tool/Approach        | Auto Approach             |
|---------|---------------------|------------------------|---------------------------|
| 91      | Small libraries     | .h/.h prefix pattern   | Types + methods + mod/use |
| 92      | CLI tool            | argc/argv, getopt      | `main(args [str])`, `is`  |
| 93      | HTTP server         | Socket programming     | Request/Response types    |
| 94      | Key-value store     | Hash table + file I/O  | Built-in Map type         |
| 95      | Custom allocator    | Arena/pool allocators  | Handled by runtime        |
| 96      | Text parser         | Pointer-based tokenizer| String-based tokenization |
| 97      | Tiny interpreter    | AST with tagged unions | Type + is pattern matching|
| 98      | SQLite FFI          | sqlite3.h C API        | `sys extern` FFI calls    |
| 99      | Packaging           | Makefiles, CMake       | pac.at + `auto` commands  |
| 100     | Build your project  | Manual setup           | Template + auto toolchain |
