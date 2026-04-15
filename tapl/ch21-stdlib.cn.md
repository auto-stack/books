# 标准库导览

在前二十章中，你学习了 Auto 的核心语言：类型、函数、模式匹配、泛型、错误处理、
并发和元编程。但一门语言的价值取决于它开箱即用提供了多少工具。Auto 附带了一个
全面的标准库——一个包含各种现成模块的工具箱，涵盖每个程序都需要的功能：字符串、
数学、文件 I/O、集合、时间和 JSON。

本章是一次导览。我们将按领域逐一介绍标准库中最实用的部分，并配有实际的代码示例。
把它想象成一次井然有序的车间参观：你不需要记住架子上每一个工具的位置，但你会
知道需要时去哪里找。

## 字符串工具

字符串无处不在。解析用户输入、格式化日志消息、构建文件路径——大多数程序都有
相当一部分时间在处理文本。Auto 的 `std::string` 模块为 `String` 类型提供了丰富
的方法集。

核心函数包括：`trim()` 用于去除空白，`format!()` 用于插值格式化，`split()`
用于拆分字符串，`join()` 用于合并，以及查询方法如 `contains()`、`starts_with()`
、`ends_with()`、`to_upper()`、`to_lower()` 和 `replace()`。

<Listing number="21-1" file-name="main.at" caption="字符串处理流水线：trim、format、split、join 和查询">

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

注意每种语言如何实现相同的操作：

| 操作 | Auto | Rust | Python | C | TypeScript |
|------|------|------|--------|---|------------|
| 去除空白 | `.trim()` | `.trim()` | `.strip()` | 手动循环 | `.trim()` |
| 格式化字符串 | `format!()` | `format!()` | `.format()` | `sprintf` | 模板字面量 |
| 拆分 | `.split(",")` | `.split(",")` | `.split(",")` | `strtok` | `.split(",")` |
| 合并 | `.join(" ")` | `.join(" ")` | `" ".join()` | 手动循环 | `.join(" ")` |
| 包含 | `.contains()` | `.contains()` | `in` 运算符 | `strstr` | `.includes()` |

Auto 的版本与 Rust 高度相似，这是有意为之的。如果你熟悉 Rust 的标准库，那么你
已经掌握了 Auto 的大部分 API。

## 数学与数值

`std::math` 模块提供了常用的数学函数。大多数是顶层函数，可以直接调用：`min`、
`max`、`abs`、`round`、`floor`、`ceil`、`clamp`、`pow` 和 `sqrt`。

这些是进行计算时常用的函数——从评分算法到物理模拟再到金融计算。

<Listing number="21-2" file-name="main.at" caption="数学运算：min、max、abs、round、clamp、pow、sqrt">

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

几点说明：

1. **`clamp(value, lo, hi)`** 将值约束在一个范围内。`clamp(15, 0, 10)` 返回 `10`
   ，因为 15 超过了上限。这个函数出人意料地有用——UI 代码中保持滑块在边界内、
   游戏物理中限制速度、数据验证中等场景都会用到。

2. **`round`、`floor`、`ceil`** 处理小数部分的方式不同。`round(3.7)` 得到 `4`
   （四舍五入到最近的整数）。`floor(3.9)` 得到 `3`（向负无穷方向取整）。
   `ceil(3.1)` 得到 `4`（向正无穷方向取整）。

3. **在 Rust 和 C 中**，`min` 和 `max` 位于不同的地方。Rust 把它们放在 `std::cmp`
   中，C 则使用三元运算符或宏。Python 和 TypeScript 分别以内置函数和 `Math`
   方法提供。Auto 为了方便，将它们作为顶层函数提供。

## IO 与文件操作

读写文件是程序最常做的事情之一。Auto 的 `std::fs` 模块提供了文件 I/O、路径
操作和目录操作相关的函数。这些函数使用 `!T`（结果类型）进行错误处理，所以你
永远不会忘记处理失败情况。

核心函数包括：`read_file`、`write_file`、`path_join`、`exists`、`mkdir`、
`list_dir`、`copy` 和 `remove`。

<Listing number="21-3" file-name="main.at" caption="文件 I/O：读取、写入、路径操作和目录列表">

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

关键观察：

1. **`path_join("data", "output.txt")`** 使用当前平台的正确分隔符（Unix 上是 `/`
   ，Windows 上是 `\`）构建路径。你应该始终使用 `path_join` 而不是用 `/` 拼接
   字符串——这样可以防止在不同操作系统上运行时出现 bug。

2. **`read_file` 和 `write_file`** 将整个文件内容作为字符串处理。在 Rust 中，
   它们是 `fs::read_to_string` 和 `fs::write`。在 C 中，你需要手动使用 `fopen`
   /`fread`/`fwrite` 并管理缓冲区。Auto 抽象了缓冲区管理的细节。

3. **`exists`** 返回 `bool`——如果文件不存在不会报错，只是返回 `false`。这让
   检查操作变得很简单。

4. **`mkdir`** 创建嵌套目录（类似 `mkdir -p`）。如果目录已经存在，它不会报错，
   而是静默跳过。

## 集合工具

你在第 19 章学习了迭代器及其可链式调用的方法。`std::collections` 模块为
`List<T>`、`Map<K,V>` 和 `Set<T>` 添加了更多操作：`sort`、`reverse`、
`unique`、`flatten`、`zip`、`chunk`、`take` 和 `skip`。

这些辅助函数在数据处理中非常常用，将它们内置在标准库中可以省去你重复造轮子
的麻烦。

<Listing number="21-4" file-name="main.at" caption="集合操作：sort、reverse、unique、flatten、zip 和 chunk">

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

这些操作值得仔细分析：

1. **`.sort()`** 返回一个新的已排序列表，原始列表不变。默认排序顺序是升序。你
   可以传入比较器闭包来自定义排序：`nums.sort(fn(a, b) int { b - a })` 实现
   降序排列。

2. **`.unique()`** 去除重复元素，同时保持插入顺序。每个元素的第一次出现被保留。
   当你需要保持顺序时，这比 `Set` 更有用。

3. **`.flatten()`** 将列表的列表变成单个列表。`[[1, 2], [3, 4], [5, 6]].flatten()`
   变成 `[1, 2, 3, 4, 5, 6]`。这是 `.chunk()` 的逆操作。

4. **`.zip()`** 将两个列表组合成对列表。`names.zip(scores)` 生成
   `[("Alice", 95), ("Bob", 87), ("Carol", 92)]`。如果两个列表长度不同，
   zip 会在较短的列表处停止。

5. **`.chunk(3)`** 将列表分成最多 3 个元素一块。如果列表长度不是 3 的倍数，
   最后一块可能更小。

## 时间与日期

处理日期和时间是出了名的棘手。时区、闰年、夏令时——到处都是边界情况。Auto 的
`std::time` 模块提供了坚实的基础：获取当前时间、格式化日期、解析日期字符串和
计算时间间隔。

核心类型是 `Time`（时间点）和 `Duration`（时间段）。核心函数包括 `Time.now()`
、`.format()`、`Time.parse()`、`Duration.hours()`、`Duration.minutes()` 和
`Duration.seconds()`。

<Listing number="21-5" file-name="main.at" caption="时间操作：当前时间、格式化、解析和时间间隔运算">

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

几点说明：

1. **格式说明符** -- Auto 使用与 C 的 `strftime` 和 Rust 的 `chrono` 相同的
   `%Y-%m-%d %H:%M:%S` 格式字符串。`%Y` 是四位年份，`%m` 是零填充的月份，
   `%d` 是零填充的日期，`%H` 是 24 小时制的小时，`%M` 是分钟，`%S` 是秒。

2. **时间间隔运算** -- `Duration.hours(2) + Duration.minutes(30)` 创建一个 2.5
   小时的时间间隔。你可以将时间间隔加到时间上（`now + duration`），也可以
   用时间相减得到时间间隔（`later - now`）。

3. **`total_minutes()`** 将时间间隔转换为其总分钟数，不管它是如何构造的。类似地，
   `total_seconds()` 返回总秒数。

4. **`Time.parse()`** 是 `.format()` 的逆操作。它接受一个字符串和一个格式说明符，
   返回一个 `Time`。如果字符串与格式不匹配，则返回错误（`!Time`）。

## JSON 序列化

JSON 是 Web 的通用语言。API 发送它，配置文件存储它，日志写入它。Auto 的
`std::json` 模块提供了 `to_json` 和 `from_json` 函数，可与任何实现了 `Serialize`
和 `Deserialize` spec 的类型一起使用。

<Listing number="21-6" file-name="main.at" caption="JSON 序列化：在类型与 JSON 之间转换">

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

让我们分析一下发生了什么：

1. **`to_json(alice)`** 将 `User` 值序列化为 JSON 字符串：
   `{"name":"Alice","age":30,"email":"alice@example.com"}`。`to_json` 函数
   可与任何实现了 `Serialize` spec 的类型一起使用。

2. **`from_json!(json, User)`** 将 JSON 字符串反序列化回 `User` 值。`from_json!`
   中的 `!` 表示这可能失败——如果 JSON 格式错误或缺少必需字段，它返回错误。
   在实践中，你应该用 `?` 或 `match` 来处理。

3. **`to_json_pretty(alice)`** 产生相同的 JSON，但带有缩进以便人类阅读。这在
   配置文件和调试中很有用。

4. **集合自然地序列化** -- `List<User>` 变成 JSON 对象数组，`Map<String, Int>`
   变成 JSON 对象，以此类推。序列化是递归的，可以处理任意深度的嵌套。

在 Rust 中，这由 `serde` 和 `serde_json` 驱动，它们是序列化事实上的标准。在
Python 中，这是内置的 `json` 模块。在 TypeScript 中，是 `JSON.stringify` 和
`JSON.parse`。在 C 中，通常需要第三方库如 `cJSON`，不过这里我们展示了简单的
`sprintf` 实现。

## 总结

本章导览了 Auto 标准库中最实用的部分：

| 领域 | 模块 | 核心函数 |
|------|------|----------|
| 字符串 | `std::string` | `trim`、`format!`、`split`、`join`、`contains`、`replace` |
| 数学 | `std::math` | `min`、`max`、`abs`、`round`、`floor`、`ceil`、`clamp`、`pow`、`sqrt` |
| 文件 I/O | `std::fs` | `read_file`、`write_file`、`path_join`、`exists`、`mkdir`、`list_dir` |
| 集合 | `std::collections` | `sort`、`reverse`、`unique`、`flatten`、`zip`、`chunk` |
| 时间 | `std::time` | `Time.now`、`.format`、`Time.parse`、`Duration.hours`、`Duration.minutes` |
| JSON | `std::json` | `to_json`、`from_json`、`to_json_pretty` |

核心要点：

1. **Auto 开箱即用** -- 标准库涵盖了最常见的编程任务。你很少需要为基本操作
   引入外部包。

2. **API 一致性好** -- `.sort()`、`.trim()`、`.format()` 等方法遵循可预测的
   命名约定。如果你能猜到函数名，它很可能就存在。

3. **错误处理内置** -- 文件 I/O 和 JSON 解析使用 `!T` 结果类型，所以错误在
   调用处是显式的，并被妥善处理。你永远不会静默地忽略一个失败。

4. **相同的概念适用于所有目标语言** -- Auto 的标准库自然映射到 Rust 的 `std`
   + `serde`、Python 的内置模块、C 的 `stdlib` + POSIX，以及 TypeScript 的
   `fs`/`path`/`JSON`。学习 Auto 的标准库同时也教会你每个目标平台的惯用方式。

5. **这趟导览只是开始** -- 完整的标准库还包括网络、加密、正则表达式、并发
   原语等更多内容。请访问 `docs.auto.dev` 查看完整文档。

这是毕业设计之前的最后一个常规章节。你现在拥有完整的工具箱：类型系统、模式匹配、
泛型、错误处理、闭包、迭代器、并发、元编程，以及一个全面的标准库。在下一章中，
你将把所有这些整合起来，构建一个真实的项目。
