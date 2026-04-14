# 第十四章：处理与 I/O

> 级别 2 — 认知
>
> 文本处理、格式化 I/O、字符编码——C 如何处理数据的流入和流出，以及 Auto 如何简化它。

输入和输出是程序与外界交互的地方。C 的 I/O 库以 `stdio.h` 为核心，提供了一组灵活但容易出错的工具。本章涵盖文本处理、格式化输入、字符编码和二进制流——以及 Auto 如何提供更安全的替代方案。

---

## 14.1 文本处理

C 在 `<ctype.h>` 中提供字符分类函数：

```c
// C 深入：字符分类
#include <ctype.h>
int ch = 'A';
isalpha(ch);    // 真：字母
isdigit(ch);    // 假：不是数字
isupper(ch);    // 真：大写
islower(ch);    // 假：不是小写
isspace(ch);    // 假：不是空白
toupper(ch);    // 'A' -> 'A'
tolower(ch);    // 'A' -> 'a'
```

这些函数有一个关键警告：传递不能表示为 `unsigned char` 或 `EOF` 的值是未定义行为。实际上，这意味着在 `char` 为有符号的平台上传递值超过 127 的 `char` 可能导致 UB。

`<string.h>` 中的字符串操作：

```c
// C 深入：字符串操作
strlen("hello");           // 5
strcpy(dst, src);          // 复制——dst 必须足够大！
strcat(dst, src);          // 连接——dst 必须足够大！
strcmp("abc", "def");      // 负数：abc < def
strncmp("abc", "abd", 2);  // 0：前 2 个字符相等
strchr("hello", 'l');      // 指向第一个 'l' 的指针
strstr("hello", "ell");    // 指向 "ell" 的指针
```

`strcpy` 和 `strcat` 函数是许多缓冲区溢出漏洞的根源。C11 添加了 `strncpy_s` 和 `strcat_s` 作为更安全的替代方案，但它们仍然使用不足。

**Auto 的方法：安全的字符串操作。** Auto 字符串具有长度跟踪且不可变。可能溢出的操作根本不会出现：

```auto
// Auto：安全的文本处理
fn count_words(text str) int {
    var count int = 0
    var in_word bool = false
    for i in 0..len(text) {
        let ch str = str(text[i])
        if ch == " " {
            in_word = false
        } else {
            if !in_word {
                count = count + 1
            }
            in_word = true
        }
    }
    count
}
```

<Listing path="listings/ch14/listing-14-01" title="文本处理" />

> **C 深入：** `strlen` 的运行时间为 O(n)，因为它必须扫描空终止符。Auto 的 `len` 运行时间为 O(1)，因为字符串长度与数据一起存储。这个差异在热循环中很重要。

---

## 14.2 格式化输入

C 的 `scanf` 系列读取格式化输入：

```c
// C 深入：scanf
int age;
char name[64];
printf("Enter name and age: ");
scanf("%63s", name);     // 读取字符串（有界）
scanf("%d", &age);       // 读取整数

// 常见陷阱：
// scanf("%s", name);    // 无界：缓冲区溢出！
// scanf("%d", &age);    // 如果输入是 "abc"？未定义状态
```

`scanf` 以难以正确使用而闻名：

- **缓冲区溢出**：没有宽度说明符的 `%s` 读取无限输入。
- **错误恢复**：不匹配时，`scanf` 将无效输入留在流中。
- **返回值**：必须检查以了解转换了多少项。
- **空白处理**：`%s` 跳过前导空白；`%c` 不跳过。

C 中更安全的模式是用 `fgets` 读取完整行，然后解析：

```c
// C 深入：更安全的输入解析
char line[256];
if (fgets(line, sizeof(line), stdin)) {
    int value;
    if (sscanf(line, "%d", &value) == 1) {
        printf("Got: %d\n", value);
    } else {
        fprintf(stderr, "Not a number\n");
    }
}
```

**Auto 的方法：类型化输入函数。** Auto 提供直接转换函数，返回可选值，消除了对格式字符串的需求：

```auto
// Auto：安全的输入解析
fn parse_int(s str) int {
    let result int = int(s)
    result
}

fn main() {
    let input str = "42"
    let value int = parse_int(input)
    print("Parsed:", value)
    print("Double:", value * 2)
}
```

<Listing path="listings/ch14/listing-14-02" title="格式化输入" />

> **C 深入：** `printf`/`scanf` 格式字符串系统是嵌入在字符串字面量中的领域特定语言。编译器无法完全验证格式字符串与参数列表的匹配（尽管 GCC 和 Clang 提供 `-Wformat` 警告）。不匹配会导致未定义行为。Auto 完全消除了格式字符串。

---

## 14.3 扩展字符集

C 最初假设 ASCII。支持国际化文本需要宽字符和多字节编码：

```c
// C 深入：宽字符
#include <wchar.h>
#include <locale.h>

setlocale(LC_ALL, "");           // 使用系统区域设置

wchar_t wc = L'A';               // 宽字符
wchar_t ws[] = L"Hello";         // 宽字符串
wprintf(L"Wide: %ls\n", ws);     // 宽字符输出
```

`wchar_t` 的大小因平台而异：Windows 上为 2 字节（UTF-16），Linux 上为 4 字节（UTF-32）。这使得宽字符代码不可移植。

关键宽字符函数：

| 窄字符函数      | 宽字符等价     | 用途           |
|----------------|---------------|----------------|
| `strlen`       | `wcslen`      | 字符串长度     |
| `strcpy`       | `wcscpy`      | 复制字符串     |
| `strcmp`       | `wcscmp`      | 比较字符串     |
| `strchr`       | `wcschr`      | 查找字符       |
| `printf`       | `wprintf`     | 格式化输出     |

**Auto 的方法：到处都是 UTF-8。** Auto 使用 UTF-8 作为其原生字符串编码，与 ASCII 兼容且被普遍支持：

```auto
// Auto：原生 UTF-8 字符串
let greeting str = "Hello, world!"
let chinese str = "你好，世界"
print(greeting)
print(chinese)
print("Length:", len(greeting))
```

> **C 深入：** `wchar_t` 在平台间的不一致性是可移植性缺陷的主要来源。在 Linux 上能工作的代码可能在 Windows 上失败，因为那里的 `wchar_t` 是 2 字节。UTF-8 通过基于字节和平台无关避免了这个问题。整个世界正在趋同于 UTF-8。

---

## 14.4 UTF-8 编码

UTF-8 用 1 到 4 字节编码 Unicode 码点：

```c
// C 深入：UTF-8 编码
// 码点           字节数     二进制模式
// U+0000-007F   1 字节     0xxxxxxx
// U+0080-07FF   2 字节     110xxxxx 10xxxxxx
// U+0800-FFFF   3 字节     1110xxxx 10xxxxxx 10xxxxxx
// U+10000-10FFFF 4 字节    11110xxx 10xxxxxx 10xxxxxx 10xxxxxx

// 示例：'€'（U+20AC）编码为 0xE2 0x82 0xAC（3 字节）
const char *euro = "\xE2\x82\xAC";
printf("Euro sign: %s\n", euro);
printf("Byte length: %zu\n", strlen(euro));  // 3，不是 1
```

UTF-8 的关键特性：

- **ASCII 兼容**：有效的 ASCII 即是有效的 UTF-8。
- **自同步**：任何以 `0` 或 `11` 开头的字节都是前导字节。
- **无空字节**：C 字符串函数可用于 UTF-8 字符串。
- **前缀属性**：没有有效编码是另一个编码的前缀。

C23 在 `<uchar.h>` 中引入了 `char8_t` 用于显式 UTF-8 字符类型：

```c
// C 深入：C23 char8_t
char8_t uc = u8'A';              // UTF-8 字符
const char8_t *us = u8"Hello";   // UTF-8 字符串字面量
```

**Auto 的方法：默认 UTF-8。** 每个 Auto 字符串都是 UTF-8 字符串。`len` 函数返回字节长度。字符级操作由标准库提供：

```auto
// Auto：原生 UTF-8
let text str = "cafe\u0301"    // cafe 带组合重音
print("Text:", text)
print("Bytes:", len(text))
```

> **C 深入：** C 中一个常见的 UTF-8 错误是使用 `strlen` 来计算"字符"——它计算的是字节数。可见字符数（字素簇）可能小于字节数。Auto 的标准库同时提供字节计数和字素簇计数功能。

---

## 14.5 可重启文本转换

C 提供可重启转换函数用于在编码之间切换：

```c
// C 深入：可重启转换
#include <wchar.h>
#include <locale.h>

// 将多字节转换为宽字符
mbstate_t state = {0};
const char *mbstr = "Hello";
wchar_t wc;
size_t n = mbrtowc(&wc, mbstr, MB_CUR_MAX, &state);
// n：消耗的字节数，或错误时为 (size_t)-1
```

这些函数存在是因为编码转换可能被中断（例如，在缓冲区边界），需要从中断处恢复。`mbstate_t` 对象携带中间状态。

相关函数：

- `mbrtowc`：多字节到宽字符（可重启）
- `wcrtomb`：宽字符到多字节（可重启）
- `mbsrtowcs`：多字节字符串到宽字符串（可重启）
- `wcsrtombs`：宽字符串到多字节字符串（可重启）

不可重启的版本（`mbtowc`、`wctomb`、`mbstowcs`、`wcstombs`）使用隐藏的内部状态，不是线程安全的。

**Auto 的方法：不暴露。** Auto 内部处理所有编码转换。程序员使用 UTF-8 字符串，永远不需要考虑 `mbstate_t` 或转换状态：

```auto
// Auto：编码在内部处理
let text str = "Hello"
print(text)
// 没有 mbstate_t，没有 mbrtowc——它就是能工作
```

> **C 深入：** 可重启转换函数是 C 标准库中最不被理解的部分之一。它们在应用代码中很少直接使用。大多数程序使用 ICU 或 libiconv 等更高级的库。Auto 完全封装了这种复杂性。

---

## 14.6 二进制流

C 区分文本流和二进制流：

```c
// C 深入：二进制 I/O
FILE *fp = fopen("data.bin", "rb");   // 二进制模式
if (!fp) { perror("fopen"); return 1; }

int values[100];
size_t n = fread(values, sizeof(int), 100, fp);
printf("Read %zu integers\n", n);
fclose(fp);
```

在文本流上，C 可能转换某些字符：

- **行结束符**：`\n` 在 Windows 上可能变为 `\r\n`。
- **Ctrl+Z**：在 Windows 上可能被视为文件结束。
- **空字节**：在文本模式下可能不被保留。

二进制模式（`"rb"`、`"wb"`）禁用这些转换：

```c
// C 深入：写入二进制数据
FILE *out = fopen("output.bin", "wb");
int data[] = {1, 2, 3, 4, 5};
fwrite(data, sizeof(int), 5, out);
fclose(out);

// 读回
FILE *in = fopen("output.bin", "rb");
int readback[5];
fread(readback, sizeof(int), 5, in);
fclose(in);
```

**Auto 的方法。** Auto 通过其标准库提供文件 I/O，具有清晰的类型安全 API。二进制和文本模式通过使用的函数区分，而不是模式字符串：

```auto
// Auto：文件 I/O（标准库）
// let data = File.read_bytes("data.bin")
// let text = File.read_text("data.txt")
print("Auto provides type-safe file I/O")
```

> **C 深入：** 文本/二进制的区别是 C 中最烦人的可移植性问题之一。在 Linux 上能工作的代码（文本和二进制模式相同）可能在 Windows 上崩溃（它们不同）。始终对二进制数据使用二进制模式，对人类可读文本使用文本模式。

---

## 快速参考

| 概念                | C 机制                      | Auto 机制                  |
|--------------------|-----------------------------|----------------------------|
| 字符分类           | `<ctype.h>` 函数            | 字符串方法                 |
| 字符串操作         | `<string.h>` 函数           | 内置运算符                 |
| 格式化输出         | `printf`                   | `print`                   |
| 格式化输入         | `scanf`                    | 类型转换函数               |
| 宽字符            | `wchar_t`、`<wchar.h>`    | 不暴露                     |
| UTF-8 编码         | 手动或 `<uchar.h>`         | 原生支持                   |
| 编码转换           | `mbrtowc`、`wcrtomb`      | 内部                       |
| 二进制 I/O         | `fread`、`fwrite`、`"rb"`  | 标准库                     |
| 文本 I/O           | `fgets`、`fputs`、`"r"`   | 标准库                     |
| 行结束符           | 平台相关                    | 规范化                     |

---

*文本处理和 I/O 是实际程序的基础。Auto 的原生 UTF-8 支持和类型安全的 I/O 消除了困扰 C 程序的编码混乱和缓冲区溢出风险。下一章将面对最严酷的现实：程序失败。*
