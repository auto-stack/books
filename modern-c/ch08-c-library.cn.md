# 第八章：C 库函数

> 级别 1 — 入门
>
> 标准库：C 开箱提供了什么，以及 Auto 如何封装它。

没有 C 程序是孤立运行的。C 标准库提供了 I/O、字符串操作、数学、内存管理和系统交互的基本函数。Auto 将大多数函数封装在更安全、更易用的接口中，同时保留了底层的 C 实现。

---

## 8.1 一般属性

C 标准库按**头文件**组织，每个头文件声明一组相关的函数、类型和宏：

| 头文件        | 用途                          | 主要函数                      |
|--------------|-------------------------------|-------------------------------|
| `<stdio.h>`  | 输入/输出                     | `printf`, `scanf`, `fopen`    |
| `<stdlib.h>` | 通用工具                      | `malloc`, `free`, `exit`, `abs` |
| `<string.h>` | 字符串处理                    | `strlen`, `strcmp`, `strcpy`  |
| `<math.h>`   | 数学运算                      | `sqrt`, `sin`, `pow`, `ceil`  |
| `<time.h>`   | 日期和时间                    | `time`, `clock`, `strftime`   |
| `<ctype.h>`  | 字符分类                      | `isdigit`, `toupper`          |
| `<assert.h>` | 诊断                          | `assert`                      |
| `<errno.h>`  | 错误指示器                    | `errno`, `strerror`           |
| `<stddef.h>` | 通用定义                      | `size_t`, `NULL`, `offsetof`  |

要使用库函数，需要 `#include` 其头文件：

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
```

Auto 隐式包含转译后的等价内容。你不需要直接写 `#include`——a2c 转译器根据代码使用的函数添加必要的头文件。

**用 `errno` 处理错误：** 许多 C 库函数通过设置全局变量 `errno` 并返回哨兵值（通常是 `NULL` 或 `-1`）来报告错误。

```c
// C：检查 errno
errno = 0;
double result = sqrt(-1.0);
if (errno != 0) {
    fprintf(stderr, "Error: %s\n", strerror(errno));
}
```

Auto 将这些模式封装到强制错误检查的返回类型中（如可选类型 `?T` 或结果类型 `Result<T, E>`），消除了忘记检查 `errno` 的风险。

> **要点：** 在 C 中，始终检查库调用的返回值和 `errno`。在 Auto 中，类型系统强制你处理错误。

---

## 8.2 整数算术

`<stdlib.h>` 头文件提供整数算术工具：

```c
// C
int absolute = abs(-42);          // 42
div_t result = div(17, 5);        // result.quot = 3, result.rem = 2
```

Auto 通过内置运算符和库函数提供这些功能：

```auto
let quotient int = 17 / 5        // 3
let remainder int = 17 % 5       // 2
let absolute int = abs(-42)      // 42
```

<Listing path="listings/ch08/listing-08-01" title="用 stdlib 进行整数算术" />

> **要点：** C 的 `div` 函数在单次操作中返回包含商和余数的 `struct`。Auto 的独立 `/` 和 `%` 运算符对大多数用例更清晰。

---

## 8.3 数值运算

`<math.h>` 头文件提供浮点数学运算：

| 函数       | 用途              | 示例                     |
|-----------|------------------|--------------------------|
| `sqrt(x)` | 平方根            | `sqrt(25.0) = 5.0`      |
| `pow(x,y)`| x 的 y 次方       | `pow(2,10) = 1024.0`    |
| `ceil(x)` | 向上取整          | `ceil(3.2) = 4.0`       |
| `floor(x)`| 向下取整          | `floor(3.8) = 3.0`      |
| `fabs(x)` | 绝对值            | `fabs(-3.14) = 3.14`    |
| `fmod(x,y)`| 浮点取余         | `fmod(7.5, 2.0) = 1.5`  |
| `sin(x)`  | 正弦（弧度）      | `sin(3.14159) ≈ 0.0`    |
| `cos(x)`  | 余弦（弧度）      | `cos(0.0) = 1.0`        |
| `log(x)`  | 自然对数          | `log(2.71828) ≈ 1.0`    |

Auto 提供相同的函数。由于 Auto 将 `float` 和 `double` 统一为 `float`，编译器根据精度需求选择合适的 C 函数（`sqrtf` vs `sqrt`）。

---

## 8.4 I/O

**格式化输出**使用 `printf` 是 C 的主要输出机制：

```c
// C
printf("Hello, %s! You are %d years old.\n", name, age);
printf("PI = %.2f\n", 3.14159);           // PI = 3.14
printf("Hex: 0x%X\n", 255);               // Hex: 0xFF
```

Auto 的 `print` 自动处理格式：

```auto
print("Hello,", name, "! You are", age, "years old.")
print("PI =", 3.14159)
```

**C 中的格式说明符**（供参考）：

| 说明符 | 类型           | 示例输出                |
|-------|----------------|------------------------|
| `%d`  | `int`          | `42`                   |
| `%u`  | `unsigned int` | `42`                   |
| `%f`  | `double`       | `3.140000`             |
| `%.2f`| `double`       | `3.14`                 |
| `%s`  | `char*`        | `hello`                |
| `%c`  | `char`         | `A`                    |
| `%x`  | `int`（十六进制）| `2a`                 |
| `%p`  | 指针           | `0x7ffd1234`           |
| `%zu` | `size_t`       | `42`                   |
| `%%`  | 字面量 `%`     | `%`                    |

**文件 I/O** 在 C 中使用 `FILE*` 句柄：

```c
// C
FILE *f = fopen("data.txt", "r");
if (!f) { perror("fopen"); return 1; }
char line[256];
while (fgets(line, sizeof(line), f)) {
    printf("%s", line);
}
fclose(f);
```

Auto 提供更高级的文件操作：

```auto
let content str = read_file("data.txt")
print(content)
write_file("output.txt", "Hello, file!")
```

<Listing path="listings/ch08/listing-08-02" title="格式化 I/O" />

> **要点：** C 的 `printf` 格式字符串强大但容易出错——错误的说明符会导致未定义行为。Auto 的 `print` 在编译时推断类型。

---

## 8.5 字符串处理

C 字符串是以 null 结尾的 `char` 数组。`<string.h>` 头文件提供：

| 函数           | 用途                      | Auto 等价              |
|---------------|---------------------------|------------------------|
| `strlen(s)`   | 字符串长度                 | `len(s)`               |
| `strcmp(a,b)` | 比较（返回 -1/0/1）       | `a == b`（布尔值）     |
| `strcpy(d,s)` | 复制字符串                 | `let d = s`            |
| `strcat(d,s)` | 拼接                       | `a + b`                |
| `strchr(s,c)` | 查找字符                   | `s.find(c)`            |
| `strstr(s,sub)`| 查找子串                  | `s.contains(sub)`      |

关键区别在于安全性。C 的字符串函数需要手动缓冲区管理：

```c
// C：如果 dest 太小则很危险
char dest[10];
strcpy(dest, "Hello, World!");   // 缓冲区溢出！
```

Auto 字符串是动态大小且有边界检查的：

```auto
let greeting str = "Hello, World!"   // 安全，自动调整大小
```

<Listing path="listings/ch08/listing-08-03" title="字符串处理" />

> **要点：** C 字符串处理是无数安全漏洞的根源（缓冲区溢出、差一错误）。Auto 的 `str` 类型通过自动管理内存和边界消除了这些问题。

---

## 8.6 时间

`<time.h>` 头文件提供时间相关函数：

```c
// C：当前时间作为时间戳
time_t now = time(NULL);
printf("Timestamp: %ld\n", (long)now);

// C：格式化时间
char buf[64];
strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", localtime(&now));
printf("Date/time: %s\n", buf);
```

Auto 提供更简单的封装：

```auto
let now int = time()
let formatted str = strftime("%Y-%m-%d %H:%M:%S")
print("Current time:", formatted)
```

---

## 8.7 运行时环境

C 提供与运行时环境交互的函数：

```c
// C：环境变量
char *home = getenv("HOME");
printf("HOME = %s\n", home);

// C：执行系统命令
int ret = system("ls -la");
```

Auto 等价物：

```auto
let home str = env("HOME")
print("HOME =", home)

// 系统命令
let ret int = system("ls -la")
```

---

## 8.8 程序终止

C 提供多种终止程序的方式：

| 函数       | 头文件       | 行为                              |
|-----------|-------------|-----------------------------------|
| `exit(n)` | `<stdlib.h>` | 清洁关闭，刷新缓冲区              |
| `abort()` | `<stdlib.h>` | 异常终止，不清理                   |
| `_Exit(n)`| `<stdlib.h>` | 立即终止，不清理                   |
| `assert(e)`| `<assert.h>` | 如果 `e` 为假则中止（仅调试）     |

```c
// C
if (ptr == NULL) {
    fprintf(stderr, "Fatal: out of memory\n");
    exit(EXIT_FAILURE);     // EXIT_FAILURE = 1
}
exit(EXIT_SUCCESS);         // EXIT_SUCCESS = 0
```

Auto 提供相同函数但命名更清晰：

```auto
if ptr == nil {
    print("Fatal: out of memory")
    exit(1)
}
exit(0)
```

C 中的 `assert` 宏在发布构建中禁用（`NDEBUG`）。Auto 的断言机制始终激活，除非显式以发布模式编译。

> **要点：** 正常错误条件优先使用 `exit` 而不是 `abort`——`exit` 运行清理处理程序并刷新 I/O 缓冲区。`abort` 仅用于真正不可恢复的错误。

---

## 快速参考

| 类别         | C 函数                      | Auto 等价                   |
|-------------|-----------------------------|------------------------------|
| 打印         | `printf(fmt, ...)`         | `print(...)`                |
| 扫描         | `scanf(fmt, ...)`          | `read_line()`               |
| 文件打开     | `fopen(path, mode)`        | `read_file(path)`           |
| 文件写入     | `fprintf(f, fmt, ...)`     | `write_file(path, data)`    |
| 字符串长度   | `strlen(s)`                | `len(s)`                    |
| 字符串比较   | `strcmp(a, b)`             | `a == b`                    |
| 字符串拼接   | `strcat(d, s)`             | `a + b`                     |
| 绝对值       | `abs(n)`, `fabs(x)`        | `abs(n)`                    |
| 平方根       | `sqrt(x)`                  | `sqrt(x)`                   |
| 幂运算       | `pow(x, y)`                | `pow(x, y)`                 |
| 退出         | `exit(n)`                  | `exit(n)`                   |
| 断言         | `assert(expr)`             | `assert(expr)`              |
| 环境变量     | `getenv(name)`             | `env(name)`                 |
| 系统调用     | `system(cmd)`              | `system(cmd)`               |
| 当前时间     | `time(NULL)`               | `time()`                    |
| 错误号       | `errno`                    | 错误类型（Result/Option）   |

---

*这完成了级别 1 — 入门。你现在了解了 C 的基础知识以及 Auto 如何映射到它们。后续级别将在此基础之上构建。*
