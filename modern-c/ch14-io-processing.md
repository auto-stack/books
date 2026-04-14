# Chapter 14: Processing and I/O

> Level 2 — Cognition
>
> Text processing, formatted I/O, character encodings -- how C handles data
> flowing in and out, and how Auto simplifies it.

Input and output are where programs meet the outside world. C's I/O library,
centered on `stdio.h`, provides a flexible but error-prone set of tools. This
chapter covers text processing, formatted input, character encodings, and
binary streams -- and how Auto provides safer alternatives.

---

## 14.1 Text Processing

C provides character classification functions in `<ctype.h>`:

```c
// C Deep Dive: character classification
#include <ctype.h>
int ch = 'A';
isalpha(ch);    // true: alphabetic
isdigit(ch);    // false: not a digit
isupper(ch);    // true: uppercase
islower(ch);    // false: not lowercase
isspace(ch);    // false: not whitespace
toupper(ch);    // 'A' -> 'A'
tolower(ch);    // 'A' -> 'a'
```

These functions have a critical caveat: passing a value not representable as
`unsigned char` or `EOF` is undefined behavior. In practice, this means
passing a `char` from a platform where `char` is signed can cause UB for
characters with values above 127.

String operations in `<string.h>`:

```c
// C Deep Dive: string operations
strlen("hello");           // 5
strcpy(dst, src);          // copy -- dst must be large enough!
strcat(dst, src);          // concatenate -- dst must be large enough!
strcmp("abc", "def");      // negative: abc < def
strncmp("abc", "abd", 2);  // 0: first 2 chars equal
strchr("hello", 'l');      // pointer to first 'l'
strstr("hello", "ell");    // pointer to "ell"
```

The `strcpy` and `strcat` functions are responsible for many buffer overflow
vulnerabilities. C11 added `strncpy_s` and `strcat_s` as safer alternatives,
but they remain underused.

**Auto's approach: safe string operations.** Auto strings are length-tracked
and immutable. Operations that could overflow simply do not arise:

```auto
// Auto: safe text processing
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

<Listing path="listings/ch14/listing-14-01" title="Text processing" />

> **C Deep Dive:** `strlen` runs in O(n) time because it must scan for the
> null terminator. Auto's `len` runs in O(1) because string length is stored
> alongside the data. This difference matters in hot loops.

---

## 14.2 Formatted Input

C's `scanf` family reads formatted input:

```c
// C Deep Dive: scanf
int age;
char name[64];
printf("Enter name and age: ");
scanf("%63s", name);     // read string (bounded)
scanf("%d", &age);       // read integer

// Common pitfalls:
// scanf("%s", name);    // UNBOUNDED: buffer overflow!
// scanf("%d", &age);    // what if input is "abc"? undefined state
```

`scanf` is notoriously difficult to use correctly:

- **Buffer overflows**: `%s` without a width specifier reads unlimited input.
- **Error recovery**: on mismatch, `scanf` leaves invalid input in the stream.
- **Return value**: must be checked to know how many items were converted.
- **Whitespace handling**: `%s` skips leading whitespace; `%c` does not.

The safer pattern in C is to read a full line with `fgets`, then parse:

```c
// C Deep Dive: safer input parsing
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

**Auto's approach: typed input functions.** Auto provides direct conversion
functions that return optional values, eliminating the need for format strings:

```auto
// Auto: safe input parsing
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

<Listing path="listings/ch14/listing-14-02" title="Formatted input" />

> **C Deep Dive:** The `printf`/`scanf` format string system is a domain-
> specific language embedded in string literals. The compiler cannot fully
> validate format strings against the argument list (though GCC and Clang
> provide `-Wformat` warnings). Mismatches cause undefined behavior. Auto
> eliminates format strings entirely.

---

## 14.3 Extended Character Sets

C originally assumed ASCII. Supporting international text requires wide
characters and multibyte encodings:

```c
// C Deep Dive: wide characters
#include <wchar.h>
#include <locale.h>

setlocale(LC_ALL, "");           // use system locale

wchar_t wc = L'A';               // wide character
wchar_t ws[] = L"Hello";         // wide string
wprintf(L"Wide: %ls\n", ws);     // wide output
```

`wchar_t` has platform-dependent size: 2 bytes on Windows (UTF-16), 4 bytes
on Linux (UTF-32). This makes wide-character code non-portable.

Key wide-character functions:

| Narrow function | Wide equivalent | Purpose              |
|-----------------|-----------------|----------------------|
| `strlen`        | `wcslen`        | String length        |
| `strcpy`        | `wcscpy`        | Copy string          |
| `strcmp`        | `wcscmp`        | Compare strings      |
| `strchr`        | `wcschr`        | Find character       |
| `printf`        | `wprintf`       | Formatted output     |

**Auto's approach: UTF-8 everywhere.** Auto uses UTF-8 as its native string
encoding, which is ASCII-compatible and universally supported:

```auto
// Auto: native UTF-8 strings
let greeting str = "Hello, world!"
let chinese str = "你好，世界"
print(greeting)
print(chinese)
print("Length:", len(greeting))
```

> **C Deep Dive:** The `wchar_t` inconsistency between platforms is a major
> source of portability bugs. Code that works on Linux may fail on Windows
> because `wchar_t` is 2 bytes there. UTF-8 avoids this problem by being
> byte-based and platform-independent. The entire world is converging on
> UTF-8.

---

## 14.4 UTF-8 Encodings

UTF-8 encodes Unicode code points in 1 to 4 bytes:

```c
// C Deep Dive: UTF-8 encoding
// Code point    Bytes       Binary pattern
// U+0000-007F   1 byte      0xxxxxxx
// U+0080-07FF   2 bytes     110xxxxx 10xxxxxx
// U+0800-FFFF   3 bytes     1110xxxx 10xxxxxx 10xxxxxx
// U+10000-10FFFF 4 bytes    11110xxx 10xxxxxx 10xxxxxx 10xxxxxx

// Example: '€' (U+20AC) encodes as 0xE2 0x82 0xAC (3 bytes)
const char *euro = "\xE2\x82\xAC";
printf("Euro sign: %s\n", euro);
printf("Byte length: %zu\n", strlen(euro));  // 3, not 1
```

Key UTF-8 properties:

- **ASCII compatible**: valid ASCII is valid UTF-8.
- **Self-synchronizing**: any byte starting with `0` or `11` is a lead byte.
- **No null bytes**: C string functions work on UTF-8 strings.
- **Prefix property**: no valid encoding is a prefix of another.

C23 introduces `<uchar.h>` with `char8_t` for explicit UTF-8 character type:

```c
// C Deep Dive: C23 char8_t
char8_t uc = u8'A';              // UTF-8 character
const char8_t *us = u8"Hello";   // UTF-8 string literal
```

**Auto's approach: UTF-8 by default.** Every Auto string is a UTF-8 string.
The `len` function returns the byte length. Character-level operations are
provided by the standard library:

```auto
// Auto: UTF-8 native
let text str = "cafe\u0301"    // cafe with combining accent
print("Text:", text)
print("Bytes:", len(text))
```

> **C Deep Dive:** A common UTF-8 mistake in C is using `strlen` to count
> "characters" -- it counts bytes. The number of visible characters (grapheme
> clusters) may be less than the byte count. Auto's standard library provides
> functions for both byte count and grapheme cluster count.

---

## 14.5 Restartable Text Conversion

C provides restartable conversion functions for switching between encodings:

```c
// C Deep Dive: restartable conversion
#include <wchar.h>
#include <locale.h>

// Convert multibyte to wide character
mbstate_t state = {0};
const char *mbstr = "Hello";
wchar_t wc;
size_t n = mbrtowc(&wc, mbstr, MB_CUR_MAX, &state);
// n: number of bytes consumed, or (size_t)-1 on error
```

These functions exist because encoding conversion may be interrupted (e.g.,
at buffer boundaries) and needs to resume where it left off. The `mbstate_t`
object carries the intermediate state.

Related functions:

- `mbrtowc`: multibyte to wide character (restartable)
- `wcrtomb`: wide character to multibyte (restartable)
- `mbsrtowcs`: multibyte string to wide string (restartable)
- `wcsrtombs`: wide string to multibyte string (restartable)

The non-restartable versions (`mbtowc`, `wctomb`, `mbstowcs`, `wcstombs`)
use hidden internal state and are not thread-safe.

**Auto's approach: not exposed.** Auto handles all encoding conversions
internally. The programmer works with UTF-8 strings and never needs to think
about `mbstate_t` or conversion state:

```auto
// Auto: encoding handled internally
let text str = "Hello"
print(text)
// No mbstate_t, no mbrtowc -- it just works
```

> **C Deep Dive:** The restartable conversion functions are among the least
> understood parts of the C standard library. They are rarely used directly
> in application code. Most programs use higher-level libraries like ICU or
> libiconv instead. Auto encapsulates this complexity entirely.

---

## 14.6 Binary Streams

C distinguishes between text streams and binary streams:

```c
// C Deep Dive: binary I/O
FILE *fp = fopen("data.bin", "rb");   // binary mode
if (!fp) { perror("fopen"); return 1; }

int values[100];
size_t n = fread(values, sizeof(int), 100, fp);
printf("Read %zu integers\n", n);
fclose(fp);
```

On text streams, C may transform certain characters:

- **Line endings**: `\n` may become `\r\n` on Windows.
- **Ctrl+Z**: may be treated as end-of-file on Windows.
- **Null bytes**: may not be preserved in text mode.

Binary mode (`"rb"`, `"wb"`) disables these transformations:

```c
// C Deep Dive: write binary data
FILE *out = fopen("output.bin", "wb");
int data[] = {1, 2, 3, 4, 5};
fwrite(data, sizeof(int), 5, out);
fclose(out);

// Read it back
FILE *in = fopen("output.bin", "rb");
int readback[5];
fread(readback, sizeof(int), 5, in);
fclose(in);
```

**Auto's approach.** Auto provides file I/O through its standard library
with clear type-safe APIs. Binary and text modes are distinguished by the
function used, not by mode strings:

```auto
// Auto: file I/O (standard library)
// let data = File.read_bytes("data.bin")
// let text = File.read_text("data.txt")
print("Auto provides type-safe file I/O")
```

> **C Deep Dive:** The text/binary distinction is one of the most annoying
> portability issues in C. Code that works on Linux (where text and binary
> modes are identical) may break on Windows (where they differ). Always use
> binary mode for binary data, and text mode for human-readable text.

---

## Quick Reference

| Concept              | C mechanism                | Auto mechanism            |
|----------------------|----------------------------|---------------------------|
| Character classify   | `<ctype.h>` functions      | String methods            |
| String operations    | `<string.h>` functions     | Built-in operators        |
| Formatted output     | `printf`                   | `print`                   |
| Formatted input      | `scanf`                    | Type conversion functions |
| Wide characters      | `wchar_t`, `<wchar.h>`    | Not exposed               |
| UTF-8 encoding       | Manual or `<uchar.h>`      | Native support            |
| Encoding conversion  | `mbrtowc`, `wcrtomb`      | Internal                  |
| Binary I/O           | `fread`, `fwrite`, `"rb"`  | Standard library          |
| Text I/O             | `fgets`, `fputs`, `"r"`   | Standard library          |
| Line ending          | Platform-dependent         | Normalized                |

---

*Text processing and I/O are fundamental to real-world programs. Auto's
native UTF-8 support and type-safe I/O eliminate the encoding confusion and
buffer overflow risks that plague C programs. The next chapter confronts the
hardest reality: program failure.*
