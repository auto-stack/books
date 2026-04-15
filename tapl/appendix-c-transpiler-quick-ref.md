# Appendix C: Transpiler Quick-Reference

This appendix is a cheat sheet for developers who already know Rust, Python, C, or
TypeScript. Each table shows a common Auto pattern in the left column and its
equivalent in the four target languages to the right. Use it to quickly map Auto
syntax onto a language you are familiar with -- or to understand what a transpiled
Auto program looks like in your language of choice.

> **Tip:** This appendix covers syntax mappings only. For the reasoning behind each
> design decision, see the chapter listed in the "See also" note for each section.

---

## C.1 Variables & Mutability

Auto distinguishes mutable bindings (`var`) from immutable ones (`let`). The type
is inferred from the initializer.

*See also: [Chapter 2 -- Variables & Operators][ch02], [Chapter 6 -- Types & `let`][ch06]*

| Auto | Rust | Python | C | TypeScript | Notes |
|------|------|--------|---|------------|-------|
| `var x = 5` | `let mut x: i64 = 5;` | `x = 5` | `int x = 5;` | `let x = 5;` | Auto `var` is always mutable; type inferred |
| `let x = 5` | `let x: i64 = 5;` | `x = 5` | `const int x = 5;` | `const x = 5;` | Auto `let` is immutable; reassignment is a compile error |
| `var x: Int = 5` | `let mut x: i64 = 5;` | `x: int = 5` | `int x = 5;` | `let x: number = 5;` | Explicit type annotation overrides inference |
| `var name = "Alice"` | `let mut name = String::from("Alice");` | `name = "Alice"` | `char name[] = "Alice";` | `let name = "Alice";` | Strings are first-class in Auto; no manual allocation |
| `var pi = 3.14` | `let mut pi: f64 = 3.14;` | `pi = 3.14` | `double pi = 3.14;` | `let pi = 3.14;` | Auto `Float` maps to 64-bit floating point |
| `let (a, b) = (1, 2)` | `let (a, b) = (1, 2);` | `a, b = 1, 2` | -- | `const [a, b] = [1, 2];` | Tuple destructuring; C has no built-in equivalent |

---

## C.2 Functions

Functions use `fn` in Auto. Parameter types are written after the parameter name
(without a colon). Return types are inferred unless explicitly annotated.

*See also: [Chapter 3 -- Functions & Control Flow][ch03], [Chapter 6 -- Types & `let`][ch06]*

| Auto | Rust | Python | C | TypeScript | Notes |
|------|------|--------|---|------------|-------|
| `fn add(a Int, b Int) Int { return a + b }` | `fn add(a: i64, b: i64) -> i64 { a + b }` | `def add(a: int, b: int) -> int: return a + b` | `int add(int a, int b) { return a + b; }` | `function add(a: number, b: number): number { return a + b; }` | Explicit return type annotation |
| `fn greet(name String) { print("Hi " + name) }` | `fn greet(name: String) { println!("Hi {}", name); }` | `def greet(name: str): print(f"Hi {name}")` | `void greet(const char* name) { printf("Hi %s", name); }` | `function greet(name: string): void { ... }` | Return type inferred as `Unit` |
| `fn abs(x Int) Int { if x < 0 { -x } else { x } }` | `fn abs(x: i64) -> i64 { if x < 0 { -x } else { x } }` | `def abs(x: int) -> int: return -x if x < 0 else x` | `int abs(int x) { return x < 0 ? -x : x; }` | `function abs(x: number): number { return x < 0 ? -x : x; }` | Implicit return (last expression) |
| `fn main() { ... }` | `fn main() { ... }` | `def main(): ...` | `int main(void) { ... }` | (no standard entry point) | Program entry point |
| `return expr` | `return expr;` / `expr` (tail) | `return expr` | `return expr;` | `return expr;` | Auto supports both explicit `return` and implicit tail expression |

---

## C.3 Control Flow

Auto uses `if/else if/else`, `for` (both conditional and range-based), and `on`
for pattern matching. There is no `switch` keyword.

*See also: [Chapter 3 -- Functions & Control Flow][ch03], [Chapter 7 -- Enums & Pattern Matching][ch07]*

| Auto | Rust | Python | C | TypeScript | Notes |
|------|------|--------|---|------------|-------|
| `if x > 0 { ... } else if x == 0 { ... } else { ... }` | `if x > 0 { ... } else if x == 0 { ... } else { ... }` | `if x > 0: ... elif x == 0: ... else: ...` | `if (x > 0) { ... } else if (x == 0) { ... } else { ... }` | `if (x > 0) { ... } else if (x === 0) { ... } else { ... }` | Auto `if` is an expression; can return a value |
| `var y = if x > 0 { x } else { -x }` | `let y = if x > 0 { x } else { -x };` | `y = x if x > 0 else -x` | `int y = x > 0 ? x : -x;` | `const y = x > 0 ? x : -x;` | Conditional as expression |
| `for true { ... }` | `loop { ... }` | `while True: ...` | `for (;;) { ... }` | `while (true) { ... }` | Infinite loop |
| `for i in 0..10 { ... }` | `for i in 0..10 { ... }` | `for i in range(10): ...` | `for (int i = 0; i < 10; i++) { ... }` | `for (let i = 0; i < 10; i++) { ... }` | Range loop; Auto uses `0..n` exclusive upper bound |
| `for item in list { ... }` | `for item in &list { ... }` | `for item in list: ...` | (requires iterator macro) | `for (const item of list) { ... }` | Iterator-based loop |
| `on Some(v) { print(v) } on None { print("none") }` | `match opt { Some(v) => ..., None => ... }` | `match opt: case Some(v): ... case None: ...` | (no direct equivalent) | (no direct equivalent) | `on` is Auto's pattern matching construct |

---

## C.4 Types & Structs

Custom data types use the `type` keyword in Auto. Methods are attached with `ext`.

*See also: [Chapter 6 -- Types & `let`][ch06], [Chapter 8 -- OOP Reshaped][ch08]*

| Auto | Rust | Python | C | TypeScript | Notes |
|------|------|--------|---|------------|-------|
| `type Point { x Float, y Float }` | `struct Point { x: f64, y: f64 }` | `@dataclass\nclass Point:\n  x: float\n  y: float` | `typedef struct { double x; double y; } Point;` | `interface Point { x: number; y: number; }` | Auto `type` is a product type (struct) |
| `Point { x: 1.0, y: 2.0 }` | `Point { x: 1.0, y: 2.0 }` | `Point(x=1.0, y=2.0)` | `(Point){ .x = 1.0, .y = 2.0 }` | `{ x: 1.0, y: 2.0 } as Point` | Constructor uses named fields |
| `p.x` | `p.x` | `p.x` | `p.x` | `p.x` | Field access is identical across languages |
| `ext fn area(self Point) Float { self.x * self.y }` | `impl Point { fn area(&self) -> f64 { self.x * self.y } }` | `def area(self) -> float: return self.x * self.y` | `double point_area(Point* p) { return p->x * p->y; }` | `function area(this: Point): number { ... }` | `ext` attaches methods to types |
| `type Pair<T> { first T, second T }` | `struct Pair<T> { first: T, second: T }` | `from typing import Generic, TypeVar` (class) | (no generics; use `void*` or macros) | `interface Pair<T> { first: T; second: T; }` | Generic types |

---

## C.5 Enums

Auto enums can carry data in each variant, like Rust's `enum`. Pattern matching
with `on` handles each variant.

*See also: [Chapter 7 -- Enums & Pattern Matching][ch07]*

| Auto | Rust | Python | C | TypeScript | Notes |
|------|------|--------|---|------------|-------|
| `enum Direction { North, South, East, West }` | `enum Direction { North, South, East, West }` | `class Direction(Enum): NORTH = 0; ...` | `enum { NORTH, SOUTH, EAST, WEST };` | `enum Direction { North, South, East, West }` | Simple C-like enum |
| `enum Option<T> { Some(T), None }` | `enum Option<T> { Some(T), None }` | `from typing import Optional` (built-in) | (no direct equivalent) | `type Option<T> = T \| null;` | Data-carrying enum (algebraic data type) |
| `enum Result<T> { Ok(T), Err(String) }` | `enum Result<T, E> { Ok(T), Err(E) }` | (use exceptions or custom union) | (no direct equivalent) | `type Result<T> = { ok: true, value: T } \| { ok: false, error: string };` | Error-carrying enum |
| `var d = Direction.North` | `let d = Direction::North;` | `d = Direction.NORTH` | `enum Direction d = NORTH;` | `const d = Direction.North;` | Variant access uses `.` in Auto, `::` in Rust |
| `on d { is North { ... } is South { ... } }` | `match d { Direction::North => { ... }, Direction::South => { ... } }` | `match d: case Direction.NORTH: ...` | `switch (d) { case NORTH: ... }` | `switch (d) { case Direction.North: ... }` | Pattern matching with `on` and `is` |

---

## C.6 Error Handling

Auto uses `?T` for optional values and `!T` for fallible operations, inspired by
Rust but with streamlined syntax.

*See also: [Chapter 9 -- Error Handling][ch09]*

| Auto | Rust | Python | C | TypeScript | Notes |
|------|------|--------|---|------------|-------|
| `?Int` (optional value) | `Option<i32>` | `Optional[int]` | (no equivalent; use sentinel) | `number \| null` | `?T` is syntactic sugar for `Some(T) \| None` |
| `!Int` (fallible result) | `Result<i32, String>` | (use exceptions) | `int` with error code return | `Result<number, string>` (custom) | `!T` is syntactic sugar for `Ok(T) \| Err(String)` |
| `!x` (unwrap) | `x.unwrap()` | `x` (raises if None) | (caller must check) | `x!` (non-null assertion) | Panics if `None`/`Err`; use in tests or when invariant is guaranteed |
| `var v = !result` | `let v = result.unwrap();` | `v = result` | `v = result; // hope for the best` | `const v = result!;` | Unwrap asserts success; crashes on failure |
| `fn read() !String { ... }` | `fn read() -> Result<String, io::Error> { ... }` | `def read() -> str: ...` (raises) | `int read(char* buf, int len);` (error code) | `function read(): Result<string, Error> { ... }` | `!T` in return position signals fallibility |
| `try { expr } catch e { ... }` | (no try/catch; use `match` on `Result`) | `try: ... except Exception as e: ...` | (no try/catch) | `try { ... } catch (e) { ... }` | Auto provides `try/catch` for interop with exception-based systems |

---

## C.7 Collections

Auto has built-in `List`, `Map`, and `Set` types with literal syntax.

*See also: [Chapter 4 -- Collections & Nodes][ch04], [Chapter 21 -- Standard Library Tour][ch21]*

| Auto | Rust | Python | C | TypeScript | Notes |
|------|------|--------|---|------------|-------|
| `[1, 2, 3]` | `vec![1, 2, 3]` | `[1, 2, 3]` | `int arr[] = {1, 2, 3};` | `[1, 2, 3]` | List literal |
| `var list: List<Int> = []` | `let list: Vec<i32> = vec![];` | `list: list[int] = []` | `int* list = malloc(0);` | `const list: number[] = [];` | Empty typed list |
| `list.push(4)` | `list.push(4);` | `list.append(4)` | (manual reallocation) | `list.push(4);` | Append to list |
| `list.len()` | `list.len()` | `len(list)` | (track size manually) | `list.length` | List length |
| `{"name": "Alice", "age": 30}` | `HashMap::from([("name", "Alice"), ("age", 30)])` | `{"name": "Alice", "age": 30}` | (no built-in map) | `const m = new Map([["name", "Alice"], ["age", 30]]);` | Map literal |
| `map["name"]` | `map.get("name")` | `map["name"]` | (no built-in map) | `m.get("name")` | Map access |
| `{"a", "b", "c"}` | `HashSet::from(["a", "b", "c"])` | `{"a", "b", "c"}` | (no built-in set) | `new Set(["a", "b", "c"])` | Set literal |

---

## C.8 String Operations

Auto strings support interpolation with `{}` inside string literals.

*See also: [Chapter 2 -- Variables & Operators][ch02], [Chapter 21 -- Standard Library Tour][ch21]*

| Auto | Rust | Python | C | TypeScript | Notes |
|------|------|--------|---|------------|-------|
| `format!("Hello, {name}!")` | `format!("Hello, {}!", name)` | `f"Hello, {name}!"` | `sprintf(buf, "Hello, %s!", name);` | `` `Hello, ${name}!` `` | String interpolation |
| `"Hello, " + name` | `format!("Hello, {}", name)` / `"Hello, ".to_string() + &name` | `"Hello, " + name` | `strcat(buf, name)` | `` `Hello, ${name}` `` | String concatenation |
| `name.len()` | `name.len()` | `len(name)` | `strlen(name)` | `name.length` | String length |
| `name.upper()` | `name.to_uppercase()` | `name.upper()` | (no built-in) | `name.toUpperCase()` | Uppercase conversion |
| `name.contains("li")` | `name.contains("li")` | `"li" in name` | `strstr(name, "li") != NULL` | `name.includes("li")` | Substring search |
| `name.split(",")` | `name.split(",")` | `name.split(",")` | `strtok(name, ",")` | `name.split(",")` | Split into list |

---

## C.9 Concurrency

Auto's concurrency model is built on actors and message passing, not shared-memory
threads. This is the AIOS layer.

*See also: [Chapter 15 -- Actor Concurrency][ch15], [Chapter 16 -- Async with `~T`][ch16]*

| Auto | Rust | Python | C | TypeScript | Notes |
|------|------|--------|---|------------|-------|
| `spawn greeter` | `std::thread::spawn(\|\| greeter())` | `threading.Thread(target=greeter).start()` | `pthread_create(&t, NULL, greeter, NULL);` | `new Worker(greeter);` | Spawn a concurrent task |
| `send greeter "Hello"` | `tx.send("Hello".to_string())` | `queue.put("Hello")` | `write(pipe_fd, "Hello", 5);` | `worker.postMessage("Hello");` | Send a message to a task |
| `on msg String { print(msg) }` | `for msg in rx { println!("{}", msg); }` | `msg = queue.get()` | `read(pipe_fd, buf, sizeof(buf));` | `self.onmessage = (e) => { ... }` | Receive and pattern-match messages |
| `~T` (async type) | `impl Future<Output = T>` | `Awaitable[T]` (via `asyncio`) | (no built-in async) | `Promise<T>` | Auto's async marker type |
| `await expr` | `expr.await` | `await expr` | (no built-in async) | `await expr` | Suspend until async result is ready |
| `var handle = spawn worker` | `let handle = JoinHandle::from(...)` | `t = Thread(target=worker)` | `pthread_t t;` | `const w = new Worker(worker);` | Capture a handle to a spawned task |

---

## C.10 Attributes & Metadata

Attributes modify how functions and types are compiled or processed. They use the
`#[...]` syntax, borrowed from Rust.

*See also: [Chapter 18 -- Testing][ch18], [Chapter 20 -- Comptime & Metaprogramming][ch20]*

| Auto | Rust | Python | C | TypeScript | Notes |
|------|------|--------|---|------------|-------|
| `#[test]` | `#[test]` | `@pytest` / `@unittest` | (no built-in; use framework macros) | `@test` (Jest) | Mark a function as a test |
| `#[comptime]` | `const fn` | (no equivalent) | (no equivalent) | (no equivalent) | Evaluate function at compile time |
| `#[inline]` | `#[inline]` | (no equivalent) | `inline` | (no equivalent) | Hint to inline the function |
| `#[deprecated]` | `#[deprecated]` | `@deprecated` | `__attribute__((deprecated))` | `@deprecated` (TSDoc) | Warn when the item is used |
| `#[derive(Debug)]` | `#[derive(Debug)]` | `@dataclass` with `__repr__` | (no equivalent) | (no equivalent) | Auto-generate common trait implementations |
| `#[target(os = "linux")]` | `#[cfg(target_os = "linux")]` | `sys.platform == "linux"` (runtime) | `#ifdef __linux__` | (no equivalent) | Conditional compilation |
