# Input, Output and Files

This chapter covers how Auto handles input, output, and file operations, and how
these map to C's `stdio.h` functions. You will learn about standard streams,
file I/O, binary data, command-line arguments, and error handling.

## 41. Standard I/O

C uses `printf` and `scanf` for formatted I/O. Format specifiers like `%d`,
`%f`, and `%s` tell the compiler how to interpret each argument:

```c
printf("Name: %s, Age: %d\n", "Alice", 30);
scanf("%d", &x);
```

Auto's `print` maps directly to `printf`. The transpiler infers the correct
format specifier from each argument's type — no `%d` or `%s` needed.

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

The transpiler converts `print("Name:", name)` to `printf("%s %s\n", "Name:", name)`.
Multiple arguments are separated by spaces in the output. For reading input, Auto
provides `read_line()` which maps to `fgets` on `stdin`.

## 42. File Operations

C file I/O revolves around `FILE*` pointers and the `fopen`/`fclose` pair:

```c
FILE *f = fopen("data.txt", "w");
fprintf(f, "Hello\n");
fclose(f);
```

Auto simplifies this with `write_file` and `read_file` functions that handle
opening, writing, reading, and closing in one call:

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

Under the hood, `write_file` calls `fopen`, `fputs`, and `fclose`. The
`read_file` function reads the entire file into a heap-allocated string. For
streaming large files, use line-by-line reading with `read_lines`.

## 43. Binary File Reading and Writing

C uses `fwrite` and `fread` for binary I/O:

```c
fwrite(&record, sizeof(struct Record), 1, file);
fread(&record, sizeof(struct Record), 1, file);
```

Auto handles binary serialization of structs automatically. The transpiler
generates the correct `sizeof` and `fwrite`/`fread` calls.

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

Binary I/O is useful for performance-critical code where parsing text is too
slow. Be aware that binary files are not portable across architectures with
different byte orders.

## 44. Standard Streams

C defines three standard streams in `<stdio.h>`:

- `stdin` — standard input (keyboard by default)
- `stdout` — standard output (terminal by default)
- `stderr` — standard error (terminal by default)

Auto maps `print` to `stdout` and provides `eprint` for `stderr`:

```auto
print("normal output")      // → fprintf(stdout, "%s\n", "normal output")
eprint("error: bad input")  // → fprintf(stderr, "%s\n", "error: bad input")
```

Separating stdout and stderr lets you redirect normal output to a file while
errors still appear on the terminal:

```bash
./program > results.txt   # stdout goes to file, stderr stays on screen
```

## 45. Buffered I/O

C buffers I/O for performance. `fgets` reads a line from a file, and `fputs`
writes a string to a file:

```c
char line[256];
fgets(line, sizeof(line), file);
fputs(line, file);
```

Auto's line-by-line functions map to these buffered operations. The standard
library handles buffer sizes internally. For most programs, the default buffer
size (typically 8KB) provides good performance.

When writing performance-sensitive code, be aware of `fflush`. C buffers output
and writes it in chunks. Call `fflush(stdout)` to force immediate output. Auto
calls `fflush` automatically when the program exits normally.

## 46. Error Checking

C uses `errno` and `perror` for I/O errors:

```c
FILE *f = fopen("missing.txt", "r");
if (f == NULL) {
    perror("fopen failed");
    // errno contains the error code
}
```

Auto wraps I/O functions to check for errors. Failed operations return an
optional (`?str` for file reads) so you handle the error case explicitly:

```auto
let data ?str = read_file("missing.txt")
if data == nil {
    eprint("Failed to read file")
}
```

The `?str` type maps to `char*` in C, where `NULL` means the operation failed.
This is safer than C's approach because the type system forces you to check.

## 47. Command-Line Arguments

C receives command-line arguments through `argc` and `argv`:

```c
int main(int argc, char *argv[]) {
    if (argc < 2) { /* no arguments */ }
    printf("Arg: %s\n", argv[1]);
}
```

Auto uses a typed array parameter `args [str]`:

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

The transpiler converts `args [str]` to `int argc, char *argv[]`. The `len`
function maps to `argc`, and `args[i]` maps to `argv[i]`. Note that `argv[0]`
is the program name, so user arguments start at `argv[1]`.

## 48. Reading Config Files

A common pattern is reading key-value pairs from a config file. In C you would
use `fopen`, `fgets`, `strtok`, and `strcmp`. Auto simplifies this with
higher-level functions.

The pattern is: open the file, read each line, split on `=`, trim whitespace,
and store in a data structure. Auto's string methods make this straightforward:

```auto
// Simplified config reading pattern
let content str = read_file("config.txt")
let lines [str] = split(content, "\n")
for line in lines {
    let parts [str] = split(line, "=")
    // store key-value pair
}
```

This maps to C code that uses `fgets` in a loop, `strtok` for splitting, and
string comparison for key matching.

## 49. Serializing Structs

Writing a struct to a text file requires converting each field to a string.
In C, you format each field with `fprintf`:

```c
fprintf(f, "%d,%s,%f\n", rec.id, rec.name, rec.score);
```

Auto's `print` handles formatting automatically. For serialization to files,
you can combine `print` with file writing:

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

The `str()` function converts integers and floats to their string
representations, mapping to `sprintf` in C.

## 50. Practice: Log Reader/Writer

Build a log system that creates structured log entries, writes them to a file,
and reads them back.

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

This exercise combines struct definitions, constructors, string concatenation,
and formatted output. Extend it by writing entries to a file and reading them
back with a parsing function.

## Quick Reference

| Concept | Auto | C |
|---------|------|---|
| Print | `print("val:", x)` | `printf("%s %d\n", "val:", x)` |
| Error output | `eprint("err")` | `fprintf(stderr, "%s\n", "err")` |
| Write file | `write_file("f.txt", data)` | `fopen` + `fputs` + `fclose` |
| Read file | `read_file("f.txt")` | `fopen` + `fgets` loop + `fclose` |
| Binary write | `write_binary(&r)` | `fwrite(&r, sizeof(r), 1, f)` |
| Binary read | `read_binary(&r)` | `fread(&r, sizeof(r), 1, f)` |
| CLI args | `fn main(args [str])` | `int main(int argc, char *argv[])` |
| Arg count | `len(args)` | `argc` |
| Arg access | `args[1]` | `argv[1]` |
| Error check | `?str` return | `NULL` check + `errno` |
| String convert | `str(x)` | `sprintf(buf, "%d", x)` |
| Split string | `split(s, ",")` | `strtok(s, ",")` |
