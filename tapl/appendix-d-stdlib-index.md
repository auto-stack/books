# Appendix D: Standard Library Index

This appendix provides an alphabetically-organized reference of all standard
library functions and types demonstrated in this book. For detailed examples and
cross-language comparisons, see [Chapter 21 (Standard Library Tour)](ch21-stdlib.md).

## std::core

Core types and macros available in every Auto program without an explicit `use`.

| Name | Signature | Kind | Description | Ch. |
|------|-----------|------|-------------|-----|
| `Bool` | -- | type | Boolean type with values `true` and `false` | 2 |
| `Float` | -- | type | 64-bit floating-point number type | 2 |
| `format!` | `format!(template, args...) String` | macro | Interpolate values into a string template | 2, 21 |
| `Int` | -- | type | 64-bit signed integer type | 2 |
| `panic!` | `panic!(msg)` | macro | Halt the program with an error message | 9 |
| `print` | `print(value)` | fn | Write a value to stdout without a trailing newline | 4, 21 |
| `println` | `println(value)` | fn | Write a value to stdout with a trailing newline | 1, 2, 21 |
| `String` | -- | type | Heap-allocated UTF-8 text string | 2 |

## std::string

Methods on the `String` type for text processing. See [Listing 21-1](ch21-stdlib.md)
for a full example.

| Name | Signature | Kind | Description | Ch. |
|------|-----------|------|-------------|-----|
| `contains` | `s.contains(needle) bool` | method | Return `true` if `needle` is a substring of `s` | 21 |
| `ends_with` | `s.ends_with(suffix) bool` | method | Return `true` if `s` ends with `suffix` | 21 |
| `join` | `list.join(sep) String` | method | Concatenate list elements separated by `sep` | 21 |
| `len` | `s.len() int` | method | Return the byte length of `s` | 4, 18 |
| `replace` | `s.replace(old, new) String` | method | Return a copy of `s` with all occurrences of `old` replaced by `new` | 21 |
| `split` | `s.split(delimiter) List<String>` | method | Split `s` into a list of substrings | 4, 21 |
| `starts_with` | `s.starts_with(prefix) bool` | method | Return `true` if `s` starts with `prefix` | 21 |
| `to_lower` | `s.to_lower() String` | method | Return a lowercase copy of `s` | 21 |
| `to_upper` | `s.to_upper() String` | method | Return an uppercase copy of `s` | 21 |
| `trim` | `s.trim() String` | method | Remove leading and trailing whitespace | 21 |

## std::math

Mathematical functions and constants. See [Listing 21-2](ch21-stdlib.md).

| Name | Signature | Kind | Description | Ch. |
|------|-----------|------|-------------|-----|
| `abs` | `abs(x) T` | fn | Return the absolute value of `x` | 21 |
| `ceil` | `ceil(x) Float` | fn | Round `x` up to the nearest integer | 21 |
| `clamp` | `clamp(value, lo, hi) T` | fn | Constrain `value` to the range `[lo, hi]` | 21 |
| `floor` | `floor(x) Float` | fn | Round `x` down to the nearest integer | 21 |
| `max` | `max(a, b) T` | fn | Return the larger of `a` and `b` | 21 |
| `min` | `min(a, b) T` | fn | Return the smaller of `a` and `b` | 21 |
| `pow` | `pow(base, exp) Float` | fn | Raise `base` to the power of `exp` | 21 |
| `round` | `round(x) Float` | fn | Round `x` to the nearest integer | 21 |
| `sqrt` | `sqrt(x) Float` | fn | Return the square root of `x` | 21 |

## std::collections

Operations on `List<T>`, `Map<K,V>`, and `Set<T>`. Iterator methods (`.map()`,
`.filter()`, `.fold()`) are covered in [Chapter 19](ch19-closures.md); the
functions below are the additional collection helpers. See [Listing 21-4](ch21-stdlib.md).

| Name | Signature | Kind | Description | Ch. |
|------|-----------|------|-------------|-----|
| `chunk` | `list.chunk(size) List<List<T>>` | method | Split `list` into sub-lists of at most `size` elements | 21 |
| `contains` | `list.contains(value) bool` | method | Return `true` if `value` is in `list` | 4 |
| `filter` | `list.filter(pred) List<T>` | method | Keep only elements satisfying `pred` | 19 |
| `flatten` | `list.flatten() List<T>` | method | Flatten a list of lists into a single list | 21 |
| `fold` | `list.fold(init, fn) T` | method | Reduce the list to a single value with an accumulator | 19 |
| `is_empty` | `list.is_empty() bool` | method | Return `true` if the collection has no elements | 4 |
| `len` | `list.len() int` | method | Return the number of elements | 4 |
| `map` | `list.map(fn) List<U>` | method | Transform each element by applying `fn` | 19 |
| `push` | `list.push(value)` | method | Append `value` to the end of `list` | 4 |
| `reverse` | `list.reverse() List<T>` | method | Return a new list with elements in reverse order | 21 |
| `sort` | `list.sort() List<T>` | method | Return a new sorted copy of `list` (ascending by default) | 4, 21 |
| `unique` | `list.unique() List<T>` | method | Remove duplicates while preserving insertion order | 21 |
| `zip` | `list.zip(other) List<(T, U)>` | method | Combine two lists into a list of pairs | 21 |

## std::fs

File I/O, path manipulation, and directory operations. These functions use the
`!T` result type for error handling. See [Listing 21-3](ch21-stdlib.md).

| Name | Signature | Kind | Description | Ch. |
|------|-----------|------|-------------|-----|
| `copy` | `copy(src, dst)` | fn | Copy a file from `src` to `dst` | 21 |
| `exists` | `exists(path) bool` | fn | Return `true` if the file or directory at `path` exists | 14, 21 |
| `list_dir` | `list_dir(path) List<String>` | fn | List entries in the directory at `path` | 21 |
| `mkdir` | `mkdir(path)` | fn | Create a directory (and parents if needed) | 21 |
| `path_join` | `path_join(parts...) String` | fn | Join path segments with the platform separator | 14, 21 |
| `read_file` | `read_file(path) !String` | fn | Read the entire contents of a file as a string | 14, 21 |
| `remove` | `remove(path)` | fn | Delete a file or empty directory | 21 |
| `write_file` | `write_file(path, content)` | fn | Write `content` to a file, creating or overwriting it | 21 |

## std::json

JSON serialization and deserialization. Works with any type that implements
the `Serialize` and `Deserialize` specs. See [Listing 21-6](ch21-stdlib.md).

| Name | Signature | Kind | Description | Ch. |
|------|-----------|------|-------------|-----|
| `from_json!` | `from_json!(str, T) !T` | macro | Deserialize a JSON string into a value of type `T` | 21 |
| `to_json` | `to_json(value) String` | fn | Serialize a value to a compact JSON string | 21 |
| `to_json_pretty` | `to_json_pretty(value) String` | fn | Serialize a value to an indented JSON string | 21 |

## std::time

Types and functions for working with dates, times, and durations. See
[Listing 21-5](ch21-stdlib.md).

| Name | Signature | Kind | Description | Ch. |
|------|-----------|------|-------------|-----|
| `Duration` | -- | type | A span of time (e.g., 2 hours, 30 minutes) | 21 |
| `Duration.hours` | `Duration.hours(n) Duration` | fn | Create a duration of `n` hours | 21 |
| `Duration.minutes` | `Duration.minutes(n) Duration` | fn | Create a duration of `n` minutes | 21 |
| `Duration.seconds` | `Duration.seconds(n) Duration` | fn | Create a duration of `n` seconds | 21 |
| `Time` | -- | type | A point in time (instant) | 21 |
| `Time.now` | `Time.now() Time` | fn | Return the current time as a `Time` value | 21 |
| `Time.parse` | `Time.parse(str, fmt) !Time` | fn | Parse a time string using the given format specifier | 21 |
| `format` | `time.format(fmt) String` | method | Format a `Time` value as a string using `strftime` specifiers | 21 |
| `total_minutes` | `dur.total_minutes() int` | method | Convert a duration to its total value in minutes | 21 |
| `total_seconds` | `dur.total_seconds() int` | method | Convert a duration to its total value in seconds | 21 |

## std::thread

Concurrency primitives for spawning threads and controlling execution. See
[Chapter 15](ch15-actors.md) and [Chapter 16](ch16-async.md).

| Name | Signature | Kind | Description | Ch. |
|------|-----------|------|-------------|-----|
| `join` | `handle.join()` | method | Wait for a spawned thread to complete | 15 |
| `sleep` | `sleep(duration)` | fn | Block the current thread for the given duration | 15 |
| `spawn` | `spawn fn` | keyword | Start executing a function as a new actor/thread | 15 |
| `yield` | `yield` | keyword | Return control to the runtime scheduler | 15 |

## std::testing

Assertions and test infrastructure. See [Chapter 18](ch18-testing.md).

| Name | Signature | Kind | Description | Ch. |
|------|-----------|------|-------------|-----|
| `#\[test\]` | `#[test]` | attribute | Mark a function as a test to be run by `automan test` | 18 |
| `assert` | `assert(cond)` | fn | Panic if `cond` is `false` | 18 |
| `assert_eq` | `assert_eq(a, b)` | fn | Panic if `a` does not equal `b`; prints both values on failure | 18 |
| `assert_ne` | `assert_ne(a, b)` | fn | Panic if `a` equals `b`; prints both values on failure | 18 |
| `test_main` | `test_main()` | fn | Run all functions annotated with `#[test]` | 18 |
