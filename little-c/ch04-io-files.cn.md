# 输入、输出与文件

本章介绍 Auto 如何处理输入、输出和文件操作，以及它们如何映射到 C 的 `stdio.h`
函数。你将学习标准流、文件 I/O、二进制数据、命令行参数和错误处理。

## 41. 标准 I/O

C 使用 `printf` 和 `scanf` 进行格式化 I/O。格式说明符如 `%d`、`%f` 和 `%s`
告诉编译器如何解释每个参数：

```c
printf("Name: %s, Age: %d\n", "Alice", 30);
scanf("%d", &x);
```

Auto 的 `print` 直接映射到 `printf`。转译器根据每个参数的类型自动推断正确的
格式说明符——无需手写 `%d` 或 `%s`。

<Listing name="standard-io" file="listings/ch04/listing-04-01">

```auto
fn main() {
    let name str = "Alice"
    let age int = 30
    let height float = 1.68

    print("Name:", name)
    print("Age:", age)
    print("Height:", height)
    print("Formatted:", name, "is", age, "years old")
}
```

</Listing>

转译器将 `print("Name:", name)` 转换为 `printf("%s %s\n", "Name:", name)`。
多个参数在输出中用空格分隔。对于读取输入，Auto 提供了 `read_line()` 函数，
映射到 `stdin` 上的 `fgets`。

## 42. 文件操作

C 的文件 I/O 围绕 `FILE*` 指针和 `fopen`/`fclose` 对展开：

```c
FILE *f = fopen("data.txt", "w");
fprintf(f, "Hello\n");
fclose(f);
```

Auto 用 `write_file` 和 `read_file` 函数简化了这一过程，在一个调用中处理
打开、写入、读取和关闭：

<Listing name="file-operations" file="listings/ch04/listing-04-02">

```auto
fn main() {
    // Auto file I/O is simplified compared to C
    // C: FILE *f = fopen("data.txt", "w"); fprintf(f, "..."); fclose(f);
    // Auto: write_file("data.txt", "Hello from Auto\n")

    let content str = "Hello from Auto\nLine 2\nLine 3\n"
    write_file("output.txt", content)
    print("Written to output.txt")

    let data str = read_file("output.txt")
    print("Read back:", data)
}
```

</Listing>

在底层，`write_file` 调用 `fopen`、`fputs` 和 `fclose`。`read_file` 函数将
整个文件读入一个堆分配的字符串。对于流式处理大文件，可使用 `read_lines`
逐行读取。

## 43. 二进制文件读写

C 使用 `fwrite` 和 `fread` 进行二进制 I/O：

```c
fwrite(&record, sizeof(struct Record), 1, file);
fread(&record, sizeof(struct Record), 1, file);
```

Auto 自动处理结构体的二进制序列化。转译器生成正确的 `sizeof` 和
`fwrite`/`fread` 调用。

<Listing name="binary-files" file="listings/ch04/listing-04-03">

```auto
type Record {
    id int
    value float
}

fn main() {
    let r Record = Record(1, 3.14)
    print("Record id:", r.id)
    print("Record value:", r.value)

    // C binary I/O:
    // fwrite(&r, sizeof(struct Record), 1, f);
    // fread(&r, sizeof(struct Record), 1, f);
    // Auto handles serialization automatically
}
```

</Listing>

二进制 I/O 适用于解析文本太慢的性能关键代码。注意，二进制文件在不同字节序的
架构之间不可移植。

## 44. 标准流

C 在 `<stdio.h>` 中定义了三个标准流：

- `stdin` —— 标准输入（默认为键盘）
- `stdout` —— 标准输出（默认为终端）
- `stderr` —— 标准错误（默认为终端）

Auto 将 `print` 映射到 `stdout`，提供 `eprint` 用于 `stderr`：

```auto
print("normal output")      // → fprintf(stdout, "%s\n", "normal output")
eprint("error: bad input")  // → fprintf(stderr, "%s\n", "error: bad input")
```

分离 stdout 和 stderr 允许你将正常输出重定向到文件，同时错误仍显示在终端：

```bash
./program > results.txt   # stdout 到文件，stderr 留在屏幕
```

## 45. 缓冲 I/O

C 通过缓冲提高 I/O 性能。`fgets` 从文件读取一行，`fputs` 将字符串写入文件：

```c
char line[256];
fgets(line, sizeof(line), file);
fputs(line, file);
```

Auto 的逐行函数映射到这些缓冲操作。标准库内部处理缓冲区大小。对于大多数程序，
默认缓冲区大小（通常为 8KB）提供良好的性能。

编写性能敏感代码时，注意 `fflush`。C 缓冲输出并按块写入。调用
`fflush(stdout)` 强制立即输出。Auto 在程序正常退出时自动调用 `fflush`。

## 46. 错误检查

C 使用 `errno` 和 `perror` 处理 I/O 错误：

```c
FILE *f = fopen("missing.txt", "r");
if (f == NULL) {
    perror("fopen failed");
    // errno contains the error code
}
```

Auto 包装 I/O 函数以检查错误。失败的操作返回可选类型（文件读取返回 `?str`），
迫使你显式处理错误情况：

```auto
let data ?str = read_file("missing.txt")
if data == nil {
    eprint("Failed to read file")
}
```

`?str` 类型在 C 中映射为 `char*`，其中 `NULL` 表示操作失败。这比 C 的方式
更安全，因为类型系统强制你进行检查。

## 47. 命令行参数

C 通过 `argc` 和 `argv` 接收命令行参数：

```c
int main(int argc, char *argv[]) {
    if (argc < 2) { /* no arguments */ }
    printf("Arg: %s\n", argv[1]);
}
```

Auto 使用类型化数组参数 `args [str]`：

<Listing name="cli-args" file="listings/ch04/listing-04-04">

```auto
fn main(args [str]) {
    if len(args) < 2 {
        print("Usage: program <name>")
        return
    }
    let name str = args[1]
    print("Hello,", name)
    print("Argument count:", len(args))
}
```

</Listing>

转译器将 `args [str]` 转换为 `int argc, char *argv[]`。`len` 函数映射为
`argc`，`args[i]` 映射为 `argv[i]`。注意 `argv[0]` 是程序名，因此用户
参数从 `argv[1]` 开始。

## 48. 读取配置文件

常见模式是从配置文件读取键值对。在 C 中，你需要使用 `fopen`、`fgets`、
`strtok` 和 `strcmp`。Auto 用高级函数简化了这一过程。

模式是：打开文件，逐行读取，按 `=` 分割，去除空白，存入数据结构。Auto 的
字符串方法使这个过程变得直接：

```auto
// Simplified config reading pattern
let content str = read_file("config.txt")
let lines [str] = split(content, "\n")
for line in lines {
    let parts [str] = split(line, "=")
    // store key-value pair
}
```

这映射为 C 代码，使用 `fgets` 循环、`strtok` 分割和字符串比较进行键匹配。

## 49. 序列化结构体

将结构体写入文本文件需要将每个字段转换为字符串。在 C 中，你用 `fprintf`
格式化每个字段：

```c
fprintf(f, "%d,%s,%f\n", rec.id, rec.name, rec.score);
```

Auto 的 `print` 自动处理格式化。对于文件序列化，你可以将 `print` 与文件
写入结合：

```auto
type Student {
    id int
    name str
    score float
}

fn Student.serialize(s Student) str {
    str(s.id) + "," + s.name + "," + str(s.score)
}
```

`str()` 函数将整数和浮点数转换为字符串表示，在 C 中映射为 `sprintf`。

## 50. 练习：日志读写器

构建一个日志系统，创建结构化日志条目，写入文件，然后读回。

<Listing name="log-reader" file="listings/ch04/listing-04-05">

```auto
type LogEntry {
    level str
    message str
}

fn LogEntry.new(level str, message str) LogEntry {
    LogEntry(level, message)
}

fn main() {
    let e1 LogEntry = LogEntry.new("INFO", "Server started")
    let e2 LogEntry = LogEntry.new("WARN", "Low memory")
    let e3 LogEntry = LogEntry.new("ERROR", "Disk full")

    print("[" + e1.level + "] " + e1.message)
    print("[" + e2.level + "] " + e3.message)
    print("[" + e3.level + "] " + e3.message)
}
```

</Listing>

这个练习结合了结构体定义、构造函数、字符串拼接和格式化输出。扩展它：将条目
写入文件，然后用解析函数读回。

## 快速参考

| 概念 | Auto | C |
|------|------|---|
| 打印 | `print("val:", x)` | `printf("%s %d\n", "val:", x)` |
| 错误输出 | `eprint("err")` | `fprintf(stderr, "%s\n", "err")` |
| 写文件 | `write_file("f.txt", data)` | `fopen` + `fputs` + `fclose` |
| 读文件 | `read_file("f.txt")` | `fopen` + `fgets` 循环 + `fclose` |
| 二进制写 | `write_binary(&r)` | `fwrite(&r, sizeof(r), 1, f)` |
| 二进制读 | `read_binary(&r)` | `fread(&r, sizeof(r), 1, f)` |
| 命令行参数 | `fn main(args [str])` | `int main(int argc, char *argv[])` |
| 参数数量 | `len(args)` | `argc` |
| 参数访问 | `args[1]` | `argv[1]` |
| 错误检查 | `?str` 返回 | `NULL` 检查 + `errno` |
| 字符串转换 | `str(x)` | `sprintf(buf, "%d", x)` |
| 字符串分割 | `split(s, ",")` | `strtok(s, ",")` |
