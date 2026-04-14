# Chapter 7: Debugging, Testing, Profiling

> Sections 71--80
> C's debugging tools are powerful but manual. Auto aims to prevent bugs before they happen.

Debugging is where C and Auto diverge most dramatically. C programs can have subtle
memory bugs that only appear under specific conditions. Tools like gdb and valgrind
exist because C's lack of safety guarantees makes them necessary.

Auto prevents many of these bugs at the language level. When bugs do occur, Auto's
testing framework and assertions help catch them early. This chapter covers both the
C tools you should know about and Auto's built-in alternatives.

---

## 71. Debugging with GDB

GDB (GNU Debugger) is the standard C debugger. It lets you:

- Set breakpoints to pause execution at a line
- Step through code line by line
- Inspect variables and memory
- Examine the call stack

```bash
$ gcc -g program.c -o program    # -g adds debug symbols
$ gdb ./program
(gdb) break main
(gdb) run
(gdb) next
(gdb) print x
(gdb) backtrace
```

GDB is powerful but has a steep learning curve. Most developers use it through a
frontend like VS Code's debug adapter or a TUI interface.

Auto does not yet have a dedicated debugger, but since Auto transpiles to C, you
can use GDB on the generated C code. The mapping is straightforward because Auto
constructs translate directly to C equivalents.

---

## 72. Valgrind Memory Checking

Valgrind detects memory errors that compilers and runtime checks miss:

```bash
$ valgrind --leak-check=full ./program
==1234== Invalid read of size 4
==1234==    at 0x400544: main (program.c:12)
==1234==  Address 0x5205054 is 0 bytes after a block of size 4 alloc'd
```

Valgrind catches:
- Use after free
- Buffer overflows (read and write)
- Memory leaks
- Uninitialized memory reads

Running Valgrind is slow -- your program runs 10-50x slower. It is typically used
in CI pipelines or when tracking down a specific bug.

Auto makes Valgrind unnecessary for most cases because the language prevents
these errors at compile time. Bounds checking, ownership tracking, and optional
types eliminate the entire class of memory bugs that Valgrind detects.

---

## 73. Assertions

Assertions are runtime checks that verify a condition is true. If it fails, the
program aborts with a message.

**C assertions:**

```c
#include <assert.h>
assert(x > 0);                    /* Simple assertion */
assert(ptr != NULL && "ptr must not be null");  /* With message */
```

**Auto assertions:**

```auto
assert(x > 0, "x must be positive")
assert(ptr != nil, "ptr must not be null")
```

Auto's `assert` includes a message parameter by convention, making it more
informative than C's default assertion output. The transpiler maps this to
C's `assert()` with the stringified condition.

<Listing id="listing-07-01" title="Debugging strategies" path="listings/ch07/listing-07-01" />
<Listing id="listing-07-02" title="Assertions" path="listings/ch07/listing-07-02" />

---

## 74. Unit Testing

C has no built-in testing framework. Projects typically use third-party libraries
like Check, Unity, or write minimal test harnesses:

```c
void test_add(void) {
    assert(add(2, 3) == 5);
    assert(add(-1, 1) == 0);
}
int main(void) {
    test_add();
    printf("All tests passed!\n");
}
```

Auto has built-in testing with the `auto t` command:

```auto
test "add two numbers" {
    assert add(2, 3) == 5
}

test "subtract numbers" {
    assert subtract(5, 3) == 2
}
```

Run tests with `auto t`. No framework to install, no boilerplate, no macros.

<Listing id="listing-07-03" title="Unit testing in Auto" path="listings/ch07/listing-07-03" />

---

## 75. Logging Systems

Logging is more useful than `printf` debugging because it can be:
- Filtered by severity level
- Directed to files instead of console
- Left in production code (unlike debug prints)

A simple logger in C:

```c
typedef enum { LOG_DEBUG, LOG_INFO, LOG_WARN, LOG_ERROR } LogLevel;

void log_msg(LogLevel level, const char *msg) {
    const char *names[] = {"DEBUG", "INFO", "WARN", "ERROR"};
    fprintf(stderr, "[%s] %s\n", names[level], msg);
}
```

Auto makes this cleaner with type-safe enums and string handling:

```auto
type Level enum { Debug, Info, Warn, Error }

fn log_msg(level Level, msg str) {
    print("[" + str(level) + "] " + msg)
}
```

---

## 76. Profiling

Profiling tells you where your program spends its time. The standard C tool is gprof:

```bash
$ gcc -pg program.c -o program    # -pg adds profiling instrumentation
$ ./program                       # Run the program
$ gprof program gmon.out > report.txt
```

gprof shows:
- Time spent in each function
- Number of calls
- Call graph (who called whom)

Modern alternatives include `perf` on Linux and Instruments on macOS. These use
hardware performance counters and can profile without recompilation.

Auto may support profiling through its toolchain. Since Auto transpiles to C,
existing C profiling tools work on the generated code.

---

## 77. Undefined Behaviors -- and How Auto Prevents Them

C has roughly 200 undefined behaviors (UBs). These are the most dangerous:

**Buffer overflow:**

```c
int arr[3];
arr[5] = 42;    /* UB! Writes past the array */
```
Auto: Arrays have bounds checking. Out-of-bounds access is a compile error
or a runtime panic.

**Use after free:**

```c
free(ptr);
*ptr = 42;      /* UB! Accessing freed memory */
```
Auto: AutoFree ownership system ensures pointers are never used after their
owner releases them.

**Null pointer dereference:**

```c
int *p = NULL;
*p = 42;        /* UB! Dereferencing NULL */
```
Auto: `?T` optional type forces you to check for `nil` before accessing the value.

**Integer overflow:**

```c
int x = INT_MAX;
x++;            /* UB! Signed overflow */
```
Auto: Checked arithmetic by default. Overflow produces a runtime error instead
of wrapping silently.

<Listing id="listing-07-04" title="Undefined behaviors -- Auto prevents" path="listings/ch07/listing-07-04" />

---

## 78. Crash Analysis

When a C program crashes, the operating system may produce a **core dump** -- a
snapshot of the process memory at the time of the crash.

```bash
$ ulimit -c unlimited          # Enable core dumps
$ ./program                    # Program crashes
Segmentation fault (core dumped)
$ gdb ./program core
(gdb) backtrace                # Show where it crashed
(gdb) frame 0                  # Jump to the crashing frame
(gdb) print *ptr               # Inspect the bad pointer
```

Reading a backtrace is the first step in crash analysis:
1. Start from the top frame -- that is where the crash occurred
2. Look for null pointers, invalid memory, or divide-by-zero
3. Walk down the call stack to understand how you got there

Auto programs that transpile to C can be debugged the same way, but most crashes
that require this analysis are prevented by Auto's safety guarantees.

---

## 79. Code Review Checklist

Whether you write C or Auto, these checks apply:

**Correctness:**
- [ ] Does every function handle all input cases?
- [ ] Are return values checked for errors?
- [ ] Are edge cases tested (empty input, max values, null/nil)?

**Memory safety (C-specific):**
- [ ] Is every `malloc` matched with `free`?
- [ ] Are pointers checked for NULL before dereference?
- [ ] Are array indices within bounds?
- [ ] Is there any use-after-free or double-free?

**Auto-specific:**
- [ ] Are `!T` error return types handled?
- [ ] Are `?T` optionals unwrapped before use?
- [ ] Are assertions used for invariants?

**Style:**
- [ ] Are names descriptive and consistent?
- [ ] Is the code readable without comments?
- [ ] Are comments explaining *why*, not *what*?

---

## 80. Practice: Fix the Bugs

This exercise contains intentional bugs. Find them, understand why they are bugs,
and fix them.

<Listing id="listing-07-05" title="Fix bugs practice" path="listings/ch07/listing-07-05" />

**Bug hints:**
1. `sum_to(10)` should return 55. Does it? Check the loop range.
2. `is_positive(0)` -- is zero positive? What should the function return?
3. `fib(-1)` -- does the function handle negative inputs correctly?

These are the kinds of bugs that assertions and tests catch. Add `assert` calls
to verify each function's behavior before running it.

---

## Quick Reference

| Section | Topic              | C Tool/Approach    | Auto Approach          |
|---------|--------------------|--------------------|------------------------|
| 71      | Debugger           | GDB                | Transpiled C + GDB     |
| 72      | Memory checker     | Valgrind           | Not needed (safe lang) |
| 73      | Assertions         | `assert.h`         | Built-in `assert`      |
| 74      | Unit testing       | Check, Unity, etc. | `auto t` built-in      |
| 75      | Logging            | Manual implementation | Type-safe logger    |
| 76      | Profiling          | gprof, perf        | C toolchain compatible |
| 77      | Undefined behaviors| ~200 UBs           | Prevented at language level |
| 78      | Crash analysis     | Core dumps, GDB    | Most crashes prevented |
| 79      | Code review        | Manual checklist   | Same + Auto-specific items |
| 80      | Fix bugs           | GDB + Valgrind     | `assert` + `auto t`    |
