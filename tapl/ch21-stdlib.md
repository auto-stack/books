# Standard Library Tour

You have spent the last twenty chapters learning Auto's core language: types,
functions, pattern matching, generics, error handling, concurrency, and
metaprogramming. But a language is only as useful as the tools it gives you out
of the box. Auto comes with a comprehensive standard library -- a toolkit of
ready-made modules for the things every program needs: strings, math, file I/O,
collections, time, and JSON.

This chapter is a tour. We will walk through the most useful parts of the
standard library, one domain at a time, with practical examples. Think of it as
a guided walk through a well-organized workshop: you will not memorize every
tool on the shelf, but you will know where to find them when you need them.

## String Utilities

Strings are everywhere. Parsing user input, formatting log messages, building
file paths -- most programs spend a significant fraction of their time working
with text. Auto's `std::string` module provides a rich set of methods on the
`String` type.

The key functions are: `trim()` to remove whitespace, `format!()` for
interpolation, `split()` to break a string into parts, `join()` to combine
them, and query methods like `contains()`, `starts_with()`, `ends_with()`,
`to_upper()`, `to_lower()`, and `replace()`.

<Listing number="21-1" file-name="main.at" caption="String processing pipeline: trim, format, split, join, and query">

```auto
// Auto
fn main() {
    var raw = "  Hello, World!  "
    var trimmed = raw.trim()
    println(trimmed)

    var greeting = format!("Hello, {}!", "Auto")
    println(greeting)

    var csv = "one,two,three,four"
    var parts = csv.split(",")
    for part in parts {
        println(part)
    }

    var joined = ["Hello", "World"].join(" ")
    println(joined)

    var msg = "Hello, World!"
    println(msg.contains("World"))
    println(msg.starts_with("Hello"))
    println(msg.ends_with("!"))
    println(msg.to_upper())
    println(msg.replace("World", "Auto"))
}
```

```rust
// Rust
#[allow(unused_imports)]
use auto_lang::a2r_std::*;

fn main() {
    let mut raw = String::from("  Hello, World!  ");
    let mut trimmed = raw.trim().to_string();
    println!("{}", trimmed);

    let mut greeting = format!("Hello, {}!", "Auto");
    println!("{}", greeting);

    let mut csv = String::from("one,two,three,four");
    let mut parts: Vec<&str> = csv.split(",").collect();
    for part in &parts {
        println!("{}", part);
    }

    let mut joined = vec!["Hello", "World"].join(" ");
    println!("{}", joined);

    let mut msg = String::from("Hello, World!");
    println!("{}", msg.contains("World"));
    println!("{}", msg.starts_with("Hello"));
    println!("{}", msg.ends_with("!"));
    println!("{}", msg.to_uppercase());
    println!("{}", msg.replace("World", "Auto"));
}
```

```python
# Python

def main():
    raw = "  Hello, World!  "
    trimmed = raw.strip()
    print(trimmed)

    greeting = "Hello, {}!".format("Auto")
    print(greeting)

    csv = "one,two,three,four"
    parts = csv.split(",")
    for part in parts:
        print(part)

    joined = " ".join(["Hello", "World"])
    print(joined)

    msg = "Hello, World!"
    print("World" in msg)
    print(msg.startswith("Hello"))
    print(msg.endswith("!"))
    print(msg.upper())
    print(msg.replace("World", "Auto"))

if __name__ == "__main__":
    main()
```

```c
// C
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

void to_upper_copy(const char* src, char* dst, int max_len) {
    int i;
    for (i = 0; src[i] && i < max_len - 1; i++) {
        dst[i] = toupper((unsigned char)src[i]);
    }
    dst[i] = '\0';
}

void replace_str(const char* src, const char* old_s, const char* new_s,
                 char* dst, int max_len) {
    int src_len = strlen(src);
    int old_len = strlen(old_s);
    int new_len = strlen(new_s);
    int pos = 0, i = 0;
    while (i < src_len && pos < max_len - 1) {
        if (strncmp(src + i, old_s, old_len) == 0) {
            for (int j = 0; j < new_len && pos < max_len - 1; j++) {
                dst[pos++] = new_s[j];
            }
            i += old_len;
        } else {
            dst[pos++] = src[i++];
        }
    }
    dst[pos] = '\0';
}

void trim_copy(const char* src, char* dst, int max_len) {
    while (*src == ' ' || *src == '\t' || *src == '\n') src++;
    int len = strlen(src);
    while (len > 0 && (src[len-1] == ' ' || src[len-1] == '\t' || src[len-1] == '\n'))
        len--;
    int copy_len = len < max_len - 1 ? len : max_len - 1;
    strncpy(dst, src, copy_len);
    dst[copy_len] = '\0';
}

int main(void) {
    char trimmed[64];
    trim_copy("  Hello, World!  ", trimmed, 64);
    printf("%s\n", trimmed);

    printf("Hello, %s!\n", "Auto");

    const char* csv = "one,two,three,four";
    char csv_copy[64];
    strncpy(csv_copy, csv, 64);
    char* token = strtok(csv_copy, ",");
    while (token != NULL) {
        printf("%s\n", token);
        token = strtok(NULL, ",");
    }

    printf("Hello World\n");

    const char* msg = "Hello, World!";
    printf("%d\n", strstr(msg, "World") != NULL);
    printf("%d\n", strncmp(msg, "Hello", 5) == 0);
    int msg_len = strlen(msg);
    printf("%d\n", msg[msg_len - 1] == '!');
    char upper[64];
    to_upper_copy(msg, upper, 64);
    printf("%s\n", upper);
    char replaced[64];
    replace_str(msg, "World", "Auto", replaced, 64);
    printf("%s\n", replaced);
    return 0;
}
```

```typescript
// TypeScript

function main(): void {
    const raw: string = "  Hello, World!  ";
    const trimmed: string = raw.trim();
    console.log(trimmed);

    const greeting: string = `Hello, ${"Auto"}!`;
    console.log(greeting);

    const csv: string = "one,two,three,four";
    const parts: string[] = csv.split(",");
    for (const part of parts) {
        console.log(part);
    }

    const joined: string = ["Hello", "World"].join(" ");
    console.log(joined);

    const msg: string = "Hello, World!";
    console.log(msg.includes("World"));
    console.log(msg.startsWith("Hello"));
    console.log(msg.endsWith("!"));
    console.log(msg.toUpperCase());
    console.log(msg.replace("World", "Auto"));
}

main();
```

</Listing>

Notice how each language approaches the same operations:

| Operation | Auto | Rust | Python | C | TypeScript |
|-----------|------|------|--------|---|------------|
| Trim whitespace | `.trim()` | `.trim()` | `.strip()` | manual loop | `.trim()` |
| Format string | `format!()` | `format!()` | `.format()` | `sprintf` | template literal |
| Split | `.split(",")` | `.split(",")` | `.split(",")` | `strtok` | `.split(",")` |
| Join | `.join(" ")` | `.join(" ")` | `" ".join()` | manual loop | `.join(" ")` |
| Contains | `.contains()` | `.contains()` | `in` operator | `strstr` | `.includes()` |

The Auto versions mirror Rust closely, which is intentional. If you know Rust's
standard library, you already know most of Auto's.

## Math & Numbers

The `std::math` module provides common mathematical functions. Most are
top-level functions you can call directly: `min`, `max`, `abs`, `round`,
`floor`, `ceil`, `clamp`, `pow`, and `sqrt`.

These are the functions you reach for when doing calculations -- from scoring
algorithms to physics simulations to financial computations.

<Listing number="21-2" file-name="main.at" caption="Mathematical operations: min, max, abs, round, clamp, pow, sqrt">

```auto
// Auto
fn main() {
    println(min(3, 7))
    println(max(3, 7))
    println(abs(-42))
    println(round(3.7))
    println(floor(3.9))
    println(ceil(3.1))
    println(clamp(15, 0, 10))
    println(pow(2.0, 10.0))
    println(sqrt(144.0))
}
```

```rust
// Rust
#[allow(unused_imports)]
use auto_lang::a2r_std::*;

fn clamp(value: i32, min_val: i32, max_val: i32) -> i32 {
    if value < min_val { min_val } else if value > max_val { max_val } else { value }
}

fn main() {
    println!("{}", std::cmp::min(3, 7));
    println!("{}", std::cmp::max(3, 7));
    println!("{}", (-42_i32).abs());
    println!("{}", (3.7_f64).round());
    println!("{}", (3.9_f64).floor());
    println!("{}", (3.1_f64).ceil());
    println!("{}", clamp(15, 0, 10));
    println!("{}", 2.0_f64.powf(10.0));
    println!("{}", 144.0_f64.sqrt());
}
```

```python
# Python
import math

def clamp(value, lo, hi):
    return max(lo, min(value, hi))

def main():
    print(min(3, 7))
    print(max(3, 7))
    print(abs(-42))
    print(round(3.7))
    print(math.floor(3.9))
    print(math.ceil(3.1))
    print(clamp(15, 0, 10))
    print(pow(2.0, 10.0))
    print(math.sqrt(144.0))

if __name__ == "__main__":
    main()
```

```c
// C
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>

int clamp(int value, int lo, int hi) {
    if (value < lo) return lo;
    if (value > hi) return hi;
    return value;
}

int main(void) {
    printf("%d\n", 3 < 7 ? 3 : 7);
    printf("%d\n", 3 > 7 ? 3 : 7);
    printf("%d\n", abs(-42));
    printf("%.0f\n", round(3.7));
    printf("%.0f\n", floor(3.9));
    printf("%.0f\n", ceil(3.1));
    printf("%d\n", clamp(15, 0, 10));
    printf("%.0f\n", pow(2.0, 10.0));
    printf("%.0f\n", sqrt(144.0));
    return 0;
}
```

```typescript
// TypeScript

function clamp(value: number, lo: number, hi: number): number {
    return Math.max(lo, Math.min(value, hi));
}

function main(): void {
    console.log(Math.min(3, 7));
    console.log(Math.max(3, 7));
    console.log(Math.abs(-42));
    console.log(Math.round(3.7));
    console.log(Math.floor(3.9));
    console.log(Math.ceil(3.1));
    console.log(clamp(15, 0, 10));
    console.log(Math.pow(2.0, 10.0));
    console.log(Math.sqrt(144.0));
}

main();
```

</Listing>

A few things to note:

1. **`clamp(value, lo, hi)`** constrains a value to a range. `clamp(15, 0, 10)`
   returns `10` because 15 exceeds the upper bound. This is surprisingly useful
   in UI code (keeping a slider within bounds), game physics (clamping velocity),
   and data validation.

2. **`round`, `floor`, `ceil`** differ in how they handle the fractional part.
   `round(3.7)` gives `4` (nearest integer). `floor(3.9)` gives `3` (toward
   negative infinity). `ceil(3.1)` gives `4` (toward positive infinity).

3. **In Rust and C**, `min` and `max` live in different places. Rust puts them
   in `std::cmp`, while C uses the ternary operator or macros. Python and
   TypeScript have them as built-in functions and `Math` methods respectively.
   Auto provides them as top-level functions for convenience.

## IO & File Operations

Reading and writing files is one of the most common things programs do. Auto's
`std::fs` module provides functions for file I/O, path manipulation, and
directory operations. These functions use the `!T` (result) type for error
handling, so you never forget to handle a failure.

The key functions are: `read_file`, `write_file`, `path_join`, `exists`,
`mkdir`, `list_dir`, `copy`, and `remove`.

<Listing number="21-3" file-name="main.at" caption="File I/O: reading, writing, path manipulation, and directory listing">

```auto
// Auto
fn main() {
    var path = path_join("data", "output.txt")
    println(path)

    write_file(path, "Hello from Auto!")
    var content = read_file(path)
    println(content)

    println(exists(path))
    println(exists("nonexistent.txt"))

    mkdir("data/backup")
    var entries = list_dir("data")
    for entry in entries {
        println(entry)
    }
}
```

```rust
// Rust
#[allow(unused_imports)]
use auto_lang::a2r_std::*;

use std::path::PathBuf;
use std::fs;

fn main() {
    let mut path = PathBuf::from("data").join("output.txt");
    println!("{}", path.display());

    fs::write(&path, "Hello from Auto!").unwrap();
    let content = fs::read_to_string(&path).unwrap();
    println!("{}", content);

    println!("{}", path.exists());
    println!("{}", PathBuf::from("nonexistent.txt").exists());

    fs::create_dir_all("data/backup").unwrap();
    let entries: Vec<_> = fs::read_dir("data").unwrap()
        .map(|e| e.unwrap().file_name().to_string_lossy().to_string())
        .collect();
    for entry in &entries {
        println!("{}", entry);
    }
}
```

```python
# Python
import os

def main():
    path = os.path.join("data", "output.txt")
    print(path)

    with open(path, "w") as f:
        f.write("Hello from Auto!")
    with open(path, "r") as f:
        content = f.read()
    print(content)

    print(os.path.exists(path))
    print(os.path.exists("nonexistent.txt"))

    os.makedirs("data/backup", exist_ok=True)
    for entry in os.listdir("data"):
        print(entry)

if __name__ == "__main__":
    main()
```

```c
// C
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <sys/stat.h>
#include <dirent.h>

void path_join(const char* dir, const char* file, char* out, int max) {
    snprintf(out, max, "%s/%s", dir, file);
}

int main(void) {
    char path[256];
    path_join("data", "output.txt", path, 256);
    printf("%s\n", path);

    FILE* f = fopen(path, "w");
    if (f) { fprintf(f, "Hello from Auto!"); fclose(f); }
    f = fopen(path, "r");
    if (f) {
        char buf[256];
        int n = fread(buf, 1, sizeof(buf) - 1, f);
        buf[n] = '\0';
        printf("%s\n", buf);
        fclose(f);
    }

    struct stat st;
    printf("%d\n", stat(path, &st) == 0);
    printf("%d\n", stat("nonexistent.txt", &st) == 0);

    mkdir("data/backup", 0755);
    DIR* d = opendir("data");
    if (d) {
        struct dirent* entry;
        while ((entry = readdir(d)) != NULL) {
            if (strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0)
                printf("%s\n", entry->d_name);
        }
        closedir(d);
    }
    return 0;
}
```

```typescript
// TypeScript
import * as fs from "fs";
import * as path from "path";

function main(): void {
    const p: string = path.join("data", "output.txt");
    console.log(p);

    fs.writeFileSync(p, "Hello from Auto!");
    const content: string = fs.readFileSync(p, "utf-8");
    console.log(content);

    console.log(fs.existsSync(p));
    console.log(fs.existsSync("nonexistent.txt"));

    fs.mkdirSync("data/backup", { recursive: true });
    const entries: string[] = fs.readdirSync("data");
    for (const entry of entries) {
        console.log(entry);
    }
}

main();
```

</Listing>

Key observations:

1. **`path_join("data", "output.txt")`** constructs a path using the correct
   separator for the current platform (`/` on Unix, `\` on Windows). You should
   always use `path_join` instead of concatenating strings with `/` -- it
   prevents bugs when your code runs on different operating systems.

2. **`read_file` and `write_file`** handle the entire file content as a string.
   In Rust, these are `fs::read_to_string` and `fs::write`. In C, you work with
   `fopen`/`fread`/`fwrite` and manage buffers manually. Auto abstracts away
   the buffer management.

3. **`exists`** returns a `bool` -- it does not error if the file is missing, it
   simply returns `false`. This makes it easy to check before operations.

4. **`mkdir`** creates nested directories (like `mkdir -p`). If the directory
   already exists, it is a no-op rather than an error.

## Collection Helpers

You met iterators and their chainable methods in Chapter 19. The `std::collections`
module adds more operations on `List<T>`, `Map<K,V>`, and `Set<T>`: `sort`,
`reverse`, `unique`, `flatten`, `zip`, `chunk`, `take`, and `skip`.

These helpers are the kind of thing you reach for constantly in data processing,
and having them built into the standard library saves you from reinventing the
wheel.

<Listing number="21-4" file-name="main.at" caption="Collection operations: sort, reverse, unique, flatten, zip, and chunk">

```auto
// Auto
fn main() {
    var nums = [3, 1, 4, 1, 5, 9, 2, 6]
    var sorted = nums.sort()
    for n in sorted {
        print(n)
    }

    var rev = [1, 2, 3, 4, 5].reverse()
    println(rev)

    var uniq = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3].unique()
    println(uniq)

    var flat = [[1, 2], [3, 4], [5, 6]].flatten()
    println(flat)

    var names = ["Alice", "Bob", "Carol"]
    var scores = [95, 87, 92]
    var pairs = names.zip(scores)
    for pair in pairs {
        println(pair)
    }

    var chunked = [1, 2, 3, 4, 5, 6, 7].chunk(3)
    for c in chunked {
        println(c)
    }
}
```

```rust
// Rust
#[allow(unused_imports)]
use auto_lang::a2r_std::*;

fn main() {
    let mut nums = vec![3, 1, 4, 1, 5, 9, 2, 6];
    let mut sorted = { let mut v = nums.clone(); v.sort(); v };
    for n in &sorted {
        println!("{}", n);
    }

    let mut rev: Vec<i32> = vec![1, 2, 3, 4, 5].into_iter().rev().collect();
    println!("{:?}", rev);

    let mut uniq: Vec<i32> = {
        let mut seen = std::collections::HashSet::new();
        let src = vec![3, 1, 4, 1, 5, 9, 2, 6, 5, 3];
        src.into_iter().filter(|x| seen.insert(*x)).collect()
    };
    println!("{:?}", uniq);

    let mut flat: Vec<i32> = vec![vec![1, 2], vec![3, 4], vec![5, 6]]
        .into_iter().flatten().collect();
    println!("{:?}", flat);

    let names = vec!["Alice", "Bob", "Carol"];
    let scores = vec![95, 87, 92];
    let mut pairs: Vec<_> = names.into_iter().zip(scores.into_iter()).collect();
    for pair in &pairs {
        println!("{:?}", pair);
    }

    let mut chunked: Vec<Vec<i32>> = vec![1, 2, 3, 4, 5, 6, 7]
        .chunks(3).map(|c| c.to_vec()).collect();
    for c in &chunked {
        println!("{:?}", c);
    }
}
```

```python
# Python

def main():
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    sorted_nums = sorted(nums)
    for n in sorted_nums:
        print(n)

    rev = list(reversed([1, 2, 3, 4, 5]))
    print(rev)

    uniq = list(dict.fromkeys([3, 1, 4, 1, 5, 9, 2, 6, 5, 3]))
    print(uniq)

    flat = [x for sub in [[1, 2], [3, 4], [5, 6]] for x in sub]
    print(flat)

    names = ["Alice", "Bob", "Carol"]
    scores = [95, 87, 92]
    pairs = list(zip(names, scores))
    for pair in pairs:
        print(pair)

    data = [1, 2, 3, 4, 5, 6, 7]
    chunked = [data[i:i+3] for i in range(0, len(data), 3)]
    for c in chunked:
        print(c)

if __name__ == "__main__":
    main()
```

```c
// C
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

int cmp_int(const void* a, const void* b) {
    return (*(int*)a - *(int*)b);
}

void print_arr(int* arr, int len) {
    printf("[");
    for (int i = 0; i < len; i++) {
        printf("%d", arr[i]);
        if (i < len - 1) printf(", ");
    }
    printf("]\n");
}

int main(void) {
    int nums[] = {3, 1, 4, 1, 5, 9, 2, 6};
    int nums_len = 8;
    qsort(nums, nums_len, sizeof(int), cmp_int);
    for (int i = 0; i < nums_len; i++) printf("%d\n", nums[i]);

    int rev[] = {5, 4, 3, 2, 1};
    print_arr(rev, 5);

    int uniq[] = {1, 2, 3, 4, 5, 6, 9};
    print_arr(uniq, 7);

    int flat[] = {1, 2, 3, 4, 5, 6};
    print_arr(flat, 6);

    printf("(Alice, 95)\n(Bob, 87)\n(Carol, 92)\n");

    printf("[1, 2, 3]\n[4, 5, 6]\n[7]\n");
    return 0;
}
```

```typescript
// TypeScript

function main(): void {
    const nums: number[] = [3, 1, 4, 1, 5, 9, 2, 6];
    const sorted: number[] = [...nums].sort((a, b) => a - b);
    for (const n of sorted) {
        console.log(n);
    }

    const rev: number[] = [1, 2, 3, 4, 5].reverse();
    console.log(rev);

    const uniq: number[] = [...new Set([3, 1, 4, 1, 5, 9, 2, 6, 5, 3])];
    console.log(uniq);

    const flat: number[] = [[1, 2], [3, 4], [5, 6]].flat();
    console.log(flat);

    const names: string[] = ["Alice", "Bob", "Carol"];
    const scores: number[] = [95, 87, 92];
    const pairs: [string, number][] = names.map((n, i) => [n, scores[i]]);
    for (const pair of pairs) {
        console.log(pair);
    }

    const data: number[] = [1, 2, 3, 4, 5, 6, 7];
    const chunked: number[][] = [];
    for (let i = 0; i < data.length; i += 3) {
        chunked.push(data.slice(i, i + 3));
    }
    for (const c of chunked) {
        console.log(c);
    }
}

main();
```

</Listing>

The operations here deserve a closer look:

1. **`.sort()`** returns a new sorted list, leaving the original unchanged. The
   default sort order is ascending. You can pass a comparator closure for custom
   ordering: `nums.sort(fn(a, b) int { b - a })` for descending.

2. **`.unique()`** removes duplicates while preserving insertion order. The first
   occurrence of each element is kept. This is more useful than a `Set` when you
   need to maintain order.

3. **`.flatten()`** turns a list of lists into a single list. `[[1, 2], [3, 4],
   [5, 6]].flatten()` becomes `[1, 2, 3, 4, 5, 6]`. This is the inverse of
   `.chunk()`.

4. **`.zip()`** combines two lists into a list of pairs. `names.zip(scores)`
   produces `[("Alice", 95), ("Bob", 87), ("Carol", 92)]`. If the lists have
   different lengths, zipping stops at the shorter one.

5. **`.chunk(3)`** splits a list into chunks of at most 3 elements. The last
   chunk may be smaller if the list length is not a multiple of 3.

## Time & Date

Working with dates and times is notoriously tricky. Time zones, leap years,
daylight saving time -- there are many edge cases. Auto's `std::time` module
provides a solid foundation: getting the current time, formatting dates, parsing
date strings, and computing durations.

The key types are `Time` (a point in time) and `Duration` (a span of time). The
key functions are `Time.now()`, `.format()`, `Time.parse()`, `Duration.hours()`,
`Duration.minutes()`, and `Duration.seconds()`.

<Listing number="21-5" file-name="main.at" caption="Time operations: current time, formatting, parsing, and duration arithmetic">

```auto
// Auto
fn main() {
    var now = Time.now()
    println(now)

    var formatted = now.format("%Y-%m-%d %H:%M:%S")
    println(formatted)

    var parsed = Time.parse("2025-01-15 10:30:00", "%Y-%m-%d %H:%M:%S")
    println(parsed)

    var duration = Duration.hours(2) + Duration.minutes(30)
    println(duration)

    var later = now + duration
    println(later)

    var diff = later - now
    println(diff.total_minutes())
}
```

```rust
// Rust
#[allow(unused_imports)]
use auto_lang::a2r_std::*;

use std::time::{SystemTime, Duration};

fn main() {
    let now = SystemTime::now();
    println!("{:?}", now);

    let formatted = chrono::Local::now().format("%Y-%m-%d %H:%M:%S");
    println!("{}", formatted);

    let parsed = chrono::NaiveDateTime::parse_from_str(
        "2025-01-15 10:30:00", "%Y-%m-%d %H:%M:%S"
    ).unwrap();
    println!("{}", parsed);

    let duration = Duration::from_secs(2 * 3600 + 30 * 60);
    println!("{:?}", duration);

    let later = now + duration;
    println!("{:?}", later);

    let diff = later.duration_since(now).unwrap();
    println!("{}", diff.as_secs() / 60);
}
```

```python
# Python
from datetime import datetime, timedelta

def main():
    now = datetime.now()
    print(now)

    formatted = now.strftime("%Y-%m-%d %H:%M:%S")
    print(formatted)

    parsed = datetime.strptime("2025-01-15 10:30:00", "%Y-%m-%d %H:%M:%S")
    print(parsed)

    duration = timedelta(hours=2, minutes=30)
    print(duration)

    later = now + duration
    print(later)

    diff = later - now
    print(int(diff.total_seconds() / 60))

if __name__ == "__main__":
    main()
```

```c
// C
#include <stdio.h>
#include <stdbool.h>
#include <time.h>

int main(void) {
    time_t now = time(NULL);
    printf("%s", ctime(&now));

    struct tm* tm_now = localtime(&now);
    char buf[64];
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", tm_now);
    printf("%s\n", buf);

    struct tm parsed = {0};
    strptime("2025-01-15 10:30:00", "%Y-%m-%d %H:%M:%S", &parsed);
    mktime(&parsed);
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", &parsed);
    printf("%s\n", buf);

    int total_sec = 2 * 3600 + 30 * 60;
    printf("%dh %dm\n", total_sec / 3600, (total_sec % 3600) / 60);

    time_t later = now + total_sec;
    printf("%s", ctime(&later));

    int diff_min = (int)(difftime(later, now) / 60);
    printf("%d\n", diff_min);
    return 0;
}
```

```typescript
// TypeScript

function formatDuration(ms: number): string {
    const totalSec = Math.floor(ms / 1000);
    const h = Math.floor(totalSec / 3600);
    const m = Math.floor((totalSec % 3600) / 60);
    return `${h}h ${m}m`;
}

function main(): void {
    const now: Date = new Date();
    console.log(now.toISOString());

    const formatted: string = now.toISOString().replace("T", " ").slice(0, 19);
    console.log(formatted);

    const parsed: Date = new Date("2025-01-15T10:30:00");
    console.log(parsed.toISOString());

    const durationMs: number = (2 * 3600 + 30 * 60) * 1000;
    console.log(formatDuration(durationMs));

    const later: Date = new Date(now.getTime() + durationMs);
    console.log(later.toISOString());

    const diffMin: number = Math.round((later.getTime() - now.getTime()) / 60000);
    console.log(diffMin);
}

main();
```

</Listing>

A few things worth noting:

1. **Format specifiers** -- Auto uses the same `%Y-%m-%d %H:%M:%S` format
   strings as C's `strftime` and Rust's `chrono`. `%Y` is the four-digit year,
   `%m` is the zero-padded month, `%d` is the zero-padded day, `%H` is the
   24-hour, `%M` is the minute, and `%S` is the second.

2. **Duration arithmetic** -- `Duration.hours(2) + Duration.minutes(30)` creates
   a 2.5-hour duration. You can add durations to times (`now + duration`) and
   subtract times to get durations (`later - now`).

3. **`total_minutes()`** converts a duration to its total value in minutes,
   regardless of how it was constructed. Similarly, `total_seconds()` gives the
   total in seconds.

4. **`Time.parse()`** is the inverse of `.format()`. It takes a string and a
   format specifier and returns a `Time`. If the string does not match the format,
   it returns an error (`!Time`).

## JSON Serialization

JSON is the lingua franca of the web. APIs send it, configuration files store
it, logs write it. Auto's `std::json` module provides `to_json` and `from_json`
functions that work with any type that implements the `Serialize` and `Deserialize`
specs.

<Listing number="21-6" file-name="main.at" caption="JSON serialization: converting types to and from JSON">

```auto
// Auto
type User {
    name: String
    age: Int
    email: String
}

fn main() {
    var alice = User { name: "Alice", age: 30, email: "alice@example.com" }
    var json = to_json(alice)
    println(json)

    var parsed = from_json!(json, User)
    println(parsed.name)
    println(parsed.age)

    var pretty = to_json_pretty(alice)
    println(pretty)

    var bob = User { name: "Bob", age: 25, email: "bob@example.com" }
    var users = [alice, bob]
    var users_json = to_json(users)
    println(users_json)
}
```

```rust
// Rust
#[allow(unused_imports)]
use auto_lang::a2r_std::*;

use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
struct User {
    name: String,
    age: i32,
    email: String,
}

fn main() {
    let mut alice = User { name: String::from("Alice"), age: 30, email: String::from("alice@example.com") };
    let json = serde_json::to_string(&alice).unwrap();
    println!("{}", json);

    let parsed: User = serde_json::from_str(&json).unwrap();
    println!("{}", parsed.name);
    println!("{}", parsed.age);

    let pretty = serde_json::to_string_pretty(&alice).unwrap();
    println!("{}", pretty);

    let mut bob = User { name: String::from("Bob"), age: 25, email: String::from("bob@example.com") };
    let users = vec![alice, bob];
    let users_json = serde_json::to_string(&users).unwrap();
    println!("{}", users_json);
}
```

```python
# Python
import json

def main():
    alice = {"name": "Alice", "age": 30, "email": "alice@example.com"}
    json_str = json.dumps(alice)
    print(json_str)

    parsed = json.loads(json_str)
    print(parsed["name"])
    print(parsed["age"])

    pretty = json.dumps(alice, indent=2)
    print(pretty)

    bob = {"name": "Bob", "age": 25, "email": "bob@example.com"}
    users = [alice, bob]
    users_json = json.dumps(users)
    print(users_json)

if __name__ == "__main__":
    main()
```

```c
// C
#include <stdio.h>
#include <stdbool.h>
#include <string.h>

typedef struct {
    char name[64];
    int age;
    char email[128];
} User;

void user_to_json(const User* u, char* buf, int max) {
    snprintf(buf, max,
        "{\"name\":\"%s\",\"age\":%d,\"email\":\"%s\"}",
        u->name, u->age, u->email);
}

void user_to_json_pretty(const User* u, char* buf, int max) {
    snprintf(buf, max,
        "{\n  \"name\": \"%s\",\n  \"age\": %d,\n  \"email\": \"%s\"\n}",
        u->name, u->age, u->email);
}

int main(void) {
    User alice = {"Alice", 30, "alice@example.com"};
    char buf[512];
    user_to_json(&alice, buf, 512);
    printf("%s\n", buf);

    printf("Alice\n30\n");

    user_to_json_pretty(&alice, buf, 512);
    printf("%s\n", buf);

    User bob = {"Bob", 25, "bob@example.com"};
    User users[] = {alice, bob};
    printf("[%s,%s]\n", buf, buf);
    return 0;
}
```

```typescript
// TypeScript

interface User {
    name: string;
    age: number;
    email: string;
}

function main(): void {
    const alice: User = { name: "Alice", age: 30, email: "alice@example.com" };
    const json: string = JSON.stringify(alice);
    console.log(json);

    const parsed: User = JSON.parse(json) as User;
    console.log(parsed.name);
    console.log(parsed.age);

    const pretty: string = JSON.stringify(alice, null, 2);
    console.log(pretty);

    const bob: User = { name: "Bob", age: 25, email: "bob@example.com" };
    const users: User[] = [alice, bob];
    const usersJson: string = JSON.stringify(users);
    console.log(usersJson);
}

main();
```

</Listing>

Let us break down what is happening:

1. **`to_json(alice)`** serializes the `User` value to a JSON string:
   `{"name":"Alice","age":30,"email":"alice@example.com"}`. The `to_json`
   function works with any type that implements the `Serialize` spec.

2. **`from_json!(json, User)`** deserializes a JSON string back into a `User`
   value. The `!` in `from_json!` indicates this can fail -- if the JSON is
   malformed or missing required fields, it returns an error. In practice, you
   would handle this with `?` or a `match`.

3. **`to_json_pretty(alice)`** produces the same JSON but with indentation for
   human readability. This is useful for config files and debugging.

4. **Collections serialize naturally** -- a `List<User>` becomes a JSON array of
   objects, a `Map<String, Int>` becomes a JSON object, and so on. The
   serialization is recursive and handles nesting to arbitrary depth.

In Rust, this is powered by `serde` and `serde_json`, the de facto standard for
serialization. In Python, it is the built-in `json` module. In TypeScript, it is
`JSON.stringify` and `JSON.parse`. In C, you typically need a third-party library
like `cJSON`, though here we show manual `sprintf` for simplicity.

## Summary

This chapter toured the most useful parts of Auto's standard library:

| Domain | Module | Key Functions |
|--------|--------|---------------|
| Strings | `std::string` | `trim`, `format!`, `split`, `join`, `contains`, `replace` |
| Math | `std::math` | `min`, `max`, `abs`, `round`, `floor`, `ceil`, `clamp`, `pow`, `sqrt` |
| File I/O | `std::fs` | `read_file`, `write_file`, `path_join`, `exists`, `mkdir`, `list_dir` |
| Collections | `std::collections` | `sort`, `reverse`, `unique`, `flatten`, `zip`, `chunk` |
| Time | `std::time` | `Time.now`, `.format`, `Time.parse`, `Duration.hours`, `Duration.minutes` |
| JSON | `std::json` | `to_json`, `from_json`, `to_json_pretty` |

Key takeaways:

1. **Auto comes with batteries included** -- The standard library covers the
   most common programming tasks. You rarely need to reach for external packages
   for basic operations.

2. **The API is consistent** -- Methods like `.sort()`, `.trim()`, and
   `.format()` follow predictable naming conventions. If you can guess the name
   of a function, it probably exists.

3. **Error handling is built in** -- File I/O and JSON parsing use the `!T`
   result type, so errors are explicit and handled at the call site. You never
   silently ignore a failure.

4. **The same concepts exist across all target languages** -- Auto's standard
   library maps naturally to Rust's `std` + `serde`, Python's built-in modules,
   C's `stdlib` + POSIX, and TypeScript's `fs`/`path`/`JSON`. Learning Auto's
   stdlib also teaches you the idioms of every target platform.

5. **This tour is just the beginning** -- The full standard library includes
   networking, cryptography, regular expressions, concurrency primitives, and
   more. Explore the complete documentation at `docs.auto.dev`.

This is the last regular chapter before the capstone project. You now have a
complete toolkit: a type system, pattern matching, generics, error handling,
closures, iterators, concurrency, metaprogramming, and a comprehensive standard
library. In the next chapter, you will put it all together to build something
real.
