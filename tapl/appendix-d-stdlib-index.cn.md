# 附录 D：标准库索引

本附录按字母顺序列出本书中演示的所有标准库函数和类型。详细的代码示例和跨语言
对比请参阅[第 21 章（标准库导览）](ch21-stdlib.md)。

## std::core

每个 Auto 程序中无需显式 `use` 即可使用的核心类型和宏。

| 名称 | 签名 | 类别 | 说明 | 章节 |
|------|------|------|------|------|
| `Bool` | -- | 类型 | 布尔类型，值为 `true` 或 `false` | 2 |
| `Float` | -- | 类型 | 64 位浮点数类型 | 2 |
| `format!` | `format!(模板, 参数...) String` | 宏 | 将值插入字符串模板进行格式化 | 2, 21 |
| `Int` | -- | 类型 | 64 位有符号整数类型 | 2 |
| `panic!` | `panic!(消息)` | 宏 | 输出错误信息并中止程序 | 9 |
| `print` | `print(值)` | 函数 | 将值写入标准输出，不追加换行符 | 4, 21 |
| `println` | `println(值)` | 函数 | 将值写入标准输出并追加换行符 | 1, 2, 21 |
| `String` | -- | 类型 | 堆分配的 UTF-8 文本字符串 | 2 |

## std::string

`String` 类型上的文本处理方法。完整示例见[清单 21-1](ch21-stdlib.md)。

| 名称 | 签名 | 类别 | 说明 | 章节 |
|------|------|------|------|------|
| `contains` | `s.contains(needle) bool` | 方法 | 若 `needle` 是 `s` 的子串则返回 `true` | 21 |
| `ends_with` | `s.ends_with(suffix) bool` | 方法 | 若 `s` 以 `suffix` 结尾则返回 `true` | 21 |
| `join` | `list.join(sep) String` | 方法 | 用 `sep` 连接列表中的元素 | 21 |
| `len` | `s.len() int` | 方法 | 返回 `s` 的字节长度 | 4, 18 |
| `replace` | `s.replace(old, new) String` | 方法 | 返回 `s` 的副本，将所有 `old` 替换为 `new` | 21 |
| `split` | `s.split(delimiter) List<String>` | 方法 | 将 `s` 按分隔符拆分为子串列表 | 4, 21 |
| `starts_with` | `s.starts_with(prefix) bool` | 方法 | 若 `s` 以 `prefix` 开头则返回 `true` | 21 |
| `to_lower` | `s.to_lower() String` | 方法 | 返回 `s` 的小写副本 | 21 |
| `to_upper` | `s.to_upper() String` | 方法 | 返回 `s` 的大写副本 | 21 |
| `trim` | `s.trim() String` | 方法 | 去除首尾空白字符 | 21 |

## std::math

数学函数和常量。见[清单 21-2](ch21-stdlib.md)。

| 名称 | 签名 | 类别 | 说明 | 章节 |
|------|------|------|------|------|
| `abs` | `abs(x) T` | 函数 | 返回 `x` 的绝对值 | 21 |
| `ceil` | `ceil(x) Float` | 函数 | 向上取整 | 21 |
| `clamp` | `clamp(value, lo, hi) T` | 函数 | 将 `value` 约束在 `[lo, hi]` 范围内 | 21 |
| `floor` | `floor(x) Float` | 函数 | 向下取整 | 21 |
| `max` | `max(a, b) T` | 函数 | 返回 `a` 和 `b` 中的较大值 | 21 |
| `min` | `min(a, b) T` | 函数 | 返回 `a` 和 `b` 中的较小值 | 21 |
| `pow` | `pow(base, exp) Float` | 函数 | 计算 `base` 的 `exp` 次幂 | 21 |
| `round` | `round(x) Float` | 函数 | 四舍五入到最近的整数 | 21 |
| `sqrt` | `sqrt(x) Float` | 函数 | 返回 `x` 的平方根 | 21 |

## std::collections

`List<T>`、`Map<K,V>` 和 `Set<T>` 上的操作。迭代器方法（`.map()`、`.filter()`、
`.fold()`）在[第 19 章](ch19-closures.md)中介绍；以下为额外的集合辅助方法。
见[清单 21-4](ch21-stdlib.md)。

| 名称 | 签名 | 类别 | 说明 | 章节 |
|------|------|------|------|------|
| `chunk` | `list.chunk(size) List<List<T>>` | 方法 | 将列表分割为最多 `size` 个元素的子列表 | 21 |
| `contains` | `list.contains(value) bool` | 方法 | 若 `value` 在列表中则返回 `true` | 4 |
| `filter` | `list.filter(pred) List<T>` | 方法 | 仅保留满足谓词 `pred` 的元素 | 19 |
| `flatten` | `list.flatten() List<T>` | 方法 | 将列表的列表展平为单层列表 | 21 |
| `fold` | `list.fold(init, fn) T` | 方法 | 用累加器将列表归约为单个值 | 19 |
| `is_empty` | `list.is_empty() bool` | 方法 | 若集合为空则返回 `true` | 4 |
| `len` | `list.len() int` | 方法 | 返回元素个数 | 4 |
| `map` | `list.map(fn) List<U>` | 方法 | 对每个元素应用 `fn` 进行变换 | 19 |
| `push` | `list.push(value)` | 方法 | 在列表末尾追加 `value` | 4 |
| `reverse` | `list.reverse() List<T>` | 方法 | 返回元素顺序反转的新列表 | 21 |
| `sort` | `list.sort() List<T>` | 方法 | 返回排序后的新列表（默认升序） | 4, 21 |
| `unique` | `list.unique() List<T>` | 方法 | 去重并保留插入顺序 | 21 |
| `zip` | `list.zip(other) List<(T, U)>` | 方法 | 将两个列表合并为元组列表 | 21 |

## std::fs

文件 I/O、路径操作和目录操作。这些函数使用 `!T` 结果类型进行错误处理。
见[清单 21-3](ch21-stdlib.md)。

| 名称 | 签名 | 类别 | 说明 | 章节 |
|------|------|------|------|------|
| `copy` | `copy(src, dst)` | 函数 | 将文件从 `src` 复制到 `dst` | 21 |
| `exists` | `exists(path) bool` | 函数 | 若 `path` 处的文件或目录存在则返回 `true` | 14, 21 |
| `list_dir` | `list_dir(path) List<String>` | 函数 | 列出 `path` 目录下的条目 | 21 |
| `mkdir` | `mkdir(path)` | 函数 | 创建目录（必要时同时创建父目录） | 21 |
| `path_join` | `path_join(段...) String` | 函数 | 使用平台分隔符拼接路径 | 14, 21 |
| `read_file` | `read_file(path) !String` | 函数 | 读取文件全部内容为字符串 | 14, 21 |
| `remove` | `remove(path)` | 函数 | 删除文件或空目录 | 21 |
| `write_file` | `write_file(path, content)` | 函数 | 将 `content` 写入文件，创建或覆盖 | 21 |

## std::json

JSON 序列化与反序列化。适用于任何实现了 `Serialize` 和 `Deserialize` 规范
的类型。见[清单 21-6](ch21-stdlib.md)。

| 名称 | 签名 | 类别 | 说明 | 章节 |
|------|------|------|------|------|
| `from_json!` | `from_json!(str, T) !T` | 宏 | 将 JSON 字符串反序列化为 `T` 类型的值 | 21 |
| `to_json` | `to_json(value) String` | 函数 | 将值序列化为紧凑的 JSON 字符串 | 21 |
| `to_json_pretty` | `to_json_pretty(value) String` | 函数 | 将值序列化为带缩进的 JSON 字符串 | 21 |

## std::time

用于处理日期、时间和时间段的类型与函数。见[清单 21-5](ch21-stdlib.md)。

| 名称 | 签名 | 类别 | 说明 | 章节 |
|------|------|------|------|------|
| `Duration` | -- | 类型 | 一段时间跨度（如 2 小时 30 分钟） | 21 |
| `Duration.hours` | `Duration.hours(n) Duration` | 函数 | 创建 `n` 小时的时长 | 21 |
| `Duration.minutes` | `Duration.minutes(n) Duration` | 函数 | 创建 `n` 分钟的时长 | 21 |
| `Duration.seconds` | `Duration.seconds(n) Duration` | 函数 | 创建 `n` 秒的时长 | 21 |
| `Time` | -- | 类型 | 时间点（时刻） | 21 |
| `Time.now` | `Time.now() Time` | 函数 | 返回当前时间 | 21 |
| `Time.parse` | `Time.parse(str, fmt) !Time` | 函数 | 按格式说明符解析时间字符串 | 21 |
| `format` | `time.format(fmt) String` | 方法 | 按 `strftime` 格式说明符将时间格式化为字符串 | 21 |
| `total_minutes` | `dur.total_minutes() int` | 方法 | 将时长转换为总分钟数 | 21 |
| `total_seconds` | `dur.total_seconds() int` | 方法 | 将时长转换为总秒数 | 21 |

## std::thread

用于生成线程和控制执行的并发原语。见[第 15 章](ch15-actors.md)和
[第 16 章](ch16-async.md)。

| 名称 | 签名 | 类别 | 说明 | 章节 |
|------|------|------|------|------|
| `join` | `handle.join()` | 方法 | 等待生成的线程完成 | 15 |
| `sleep` | `sleep(duration)` | 函数 | 阻塞当前线程指定时长 | 15 |
| `spawn` | `spawn 函数` | 关键字 | 将函数作为新的 actor/线程启动执行 | 15 |
| `yield` | `yield` | 关键字 | 将控制权交还给运行时调度器 | 15 |

## std::testing

断言和测试基础设施。见[第 18 章](ch18-testing.md)。

| 名称 | 签名 | 类别 | 说明 | 章节 |
|------|------|------|------|------|
| `#\[test\]` | `#[test]` | 属性 | 将函数标记为测试，由 `automan test` 运行 | 18 |
| `assert` | `assert(cond)` | 函数 | 若 `cond` 为 `false` 则 panic | 18 |
| `assert_eq` | `assert_eq(a, b)` | 函数 | 若 `a` 不等于 `b` 则 panic；失败时打印两个值 | 18 |
| `assert_ne` | `assert_ne(a, b)` | 函数 | 若 `a` 等于 `b` 则 panic；失败时打印两个值 | 18 |
| `test_main` | `test_main()` | 函数 | 运行所有标记了 `#[test]` 的函数 | 18 |
