# Chapter 6: System Programming

> Sections 61--70
> System programming is where C shines -- and where Auto chooses a different path.

C was born to write operating systems. Its standard library sits directly on top of
kernel system calls, and every C programmer eventually learns about file descriptors,
processes, signals, and memory mapping. Auto takes a higher-level approach: it wraps
the dangerous primitives in safe APIs and does not expose raw syscalls.

This chapter is heavy on C-only concepts. We present them as essential knowledge for
understanding how programs interact with the operating system, then show Auto's
simplified alternatives where they exist.

---

## 61. System Calls vs Standard Library

Every operating system provides a set of **system calls** -- functions that request
services from the kernel. In C, you can call them directly:

```c
/* Raw syscall */
ssize_t n = read(fd, buffer, sizeof(buffer));

/* Stdlib wrapper (buffers data, more portable) */
size_t n = fread(buffer, 1, sizeof(buffer), file);
```

The standard library wraps raw syscalls with buffering, error handling, and
portability. `fread()` calls `read()` internally but adds a user-space buffer.

Auto goes further: functions like `print()`, `read_file()`, and `write_file()`
hide all the syscall details entirely. You never deal with file descriptors or
buffer management.

<Listing id="listing-06-01" title="System calls vs stdlib" path="listings/ch06/listing-06-01" />

**Key insight**: In C, understanding syscalls is essential. In Auto, the language
handles them for you. But knowing what happens under the hood makes you a better
programmer in either language.

---

## 62. Process Creation (fork/exec)

On POSIX systems, new processes are created with `fork()`:

```c
pid_t pid = fork();
if (pid == 0) {
    /* Child process */
    execvp("ls", argv);
} else {
    /* Parent process */
    waitpid(pid, NULL, 0);
}
```

`fork()` creates an exact copy of the current process. `exec()` replaces that copy
with a new program. This two-step pattern is fundamental to how shells, servers,
and daemons work.

Auto does **not** expose `fork()` or `exec()` directly. Instead, it may provide a
task-based concurrency model that is safer and more portable.

<Listing id="listing-06-02" title="Process creation (fork/exec)" path="listings/ch06/listing-06-02" />

---

## 63. File Descriptors

A **file descriptor** is a small integer the kernel uses to track open files,
sockets, and pipes. In C:

```c
int fd = open("data.txt", O_RDONLY);
read(fd, buffer, 1024);
close(fd);
```

Every process starts with three standard descriptors:

| FD | Name    | Purpose    |
|----|---------|------------|
| 0  | stdin   | Standard input  |
| 1  | stdout  | Standard output |
| 2  | stderr  | Standard error  |

Auto provides `read_file()` and `write_file()` so you never touch file descriptors
directly. The transpiler generates the correct `open`/`read`/`close` sequence.

<Listing id="listing-06-03" title="File descriptors" path="listings/ch06/listing-06-03" />

---

## 64. Pipes and Redirection

Pipes connect processes. A pipe has two ends: you write to one and read from the other.

```c
int pipefd[2];
pipe(pipefd);
/* pipefd[0] = read end, pipefd[1] = write end */
write(pipefd[1], "hello", 5);
read(pipefd[0], buf, 5);
```

The `dup2()` function redirects file descriptors -- this is how shells implement
`|`, `>`, and `<`. When you type `ls | grep foo`, the shell creates a pipe, forks
two processes, and connects stdout of `ls` to stdin of `grep`.

Auto uses message passing between tasks instead of raw pipes.

<Listing id="listing-06-04" title="Pipes and redirection" path="listings/ch06/listing-06-04" />

---

## 65. Signals

Signals are asynchronous notifications sent to a process. Common signals:

| Signal   | Default Action | Typical Use          |
|----------|---------------|----------------------|
| SIGINT   | Terminate     | Ctrl+C interrupt     |
| SIGTERM  | Terminate     | Graceful shutdown    |
| SIGSEGV  | Crash         | Memory violation     |
| SIGKILL  | Terminate     | Cannot be caught     |

In C, you install a handler with `signal()` or `sigaction()`:

```c
void on_sigint(int sig) {
    printf("Caught SIGINT!\n");
}
signal(SIGINT, on_sigint);
```

Signal handling is tricky: handlers run in restricted contexts where most library
functions are unsafe to call. Auto does not expose raw signal handling.

<Listing id="listing-06-05" title="Signals and handlers" path="listings/ch06/listing-06-05" />

---

## 66. Memory Mapping (mmap)

`mmap()` maps a file or anonymous memory region into the process address space:

```c
void *ptr = mmap(NULL, size, PROT_READ | PROT_WRITE,
                 MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
/* Use ptr like a regular pointer */
munmap(ptr, size);
```

`mmap` is used for:
- File I/O (memory-mapped files are faster than read/write)
- Shared memory between processes
- Allocating large aligned buffers

This is advanced C territory. Auto may eventually provide safe memory-mapped
collections, but for now it is purely a C concept worth knowing about.

---

## 67. Time and Clock APIs

C provides several time functions:

```c
time_t now = time(NULL);          /* Wall clock seconds */
clock_t ticks = clock();          /* CPU time used */
struct timespec ts;
clock_gettime(CLOCK_MONOTONIC, &ts);  /* High resolution */
```

Each measures something different -- wall time vs CPU time vs monotonic time.
Choosing the wrong one leads to subtle bugs, especially with time zone changes
or system clock adjustments.

Auto may provide wrappers like `time.now()` that return a clean `Time` type
instead of raw integers or structs.

---

## 68. Environment Variables

Environment variables are key-value strings passed from parent to child process:

```c
const char *home = getenv("HOME");
setenv("MY_VAR", "42", 1);   /* 1 = overwrite */
```

They are commonly used for configuration, paths, and feature flags. In Auto,
these may be exposed through a typed API:

```auto
let home str = env("HOME")
```

This is one area where the C API is already simple, and Auto's improvement is
mainly about type safety and missing-key handling.

---

## 69. Error Handling and Return Codes

C uses a combination of return values and the global `errno` variable:

```c
int fd = open("missing.txt", O_RDONLY);
if (fd == -1) {
    perror("open failed");   /* prints: open failed: No such file or directory */
    /* errno contains the specific error code */
}
```

The `errno` pattern is error-prone: any library call can overwrite it, and
forgetting to check return codes is one of the most common C bugs.

Auto uses a `!T` error type instead:

```auto
let content !str = read_file("missing.txt")
// Must handle the error case explicitly
```

This forces you to handle errors and eliminates the entire class of "forgot to
check the return code" bugs.

---

## 70. Practice: Mini Shell

A shell is the classic system programming exercise. In C, it requires:

1. Reading a command line
2. Parsing arguments
3. Forking a child process
4. Executing the command in the child
5. Waiting for the child to finish

This exercise combines file descriptors, fork/exec, and pipes -- nearly every
concept from this chapter.

<Listing id="listing-06-06" title="Mini shell practice" path="listings/ch06/listing-06-06" />

**Challenge**: Implement a shell that supports:
- Running a command with arguments
- Piping output between two commands (`ls | wc`)
- Redirecting output to a file (`ls > out.txt`)

This requires deep C knowledge. In Auto, you would use a higher-level process API
instead.

---

## Quick Reference

| Section | C Concept          | Auto Equivalent          | Difficulty |
|---------|--------------------|--------------------------|------------|
| 61      | Syscalls vs stdlib | `print()`, `read_file()` | Beginner   |
| 62      | fork/exec          | Task-based concurrency   | Advanced   |
| 63      | File descriptors   | `read_file()`, `write_file()` | Intermediate |
| 64      | Pipes, dup2        | Message passing          | Advanced   |
| 65      | signal/sigaction   | Not exposed              | Advanced   |
| 66      | mmap               | Not exposed              | Expert     |
| 67      | time/clock         | `time.now()` (planned)   | Intermediate |
| 68      | getenv/setenv      | `env()` (planned)        | Beginner   |
| 69      | errno, return codes| `!T` error type          | Intermediate |
| 70      | Mini shell         | Higher-level process API | Advanced   |
