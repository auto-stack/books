# 类与方法

Auto 是一种**面向对象的语言** -- 也就是说，它提供了支持面向对象编程的特性，面向对象编程具有以下特征：

-   大部分计算以对象上的操作来表达。

-   对象通常表示现实世界中的事物，方法通常对应事物在现实世界中交互的方式。

-   程序包含类型和方法的定义。

例如，在上一章中我们定义了一个 `Time` 类型，对应人们记录时间的方式，我们还定义了对应人们对时间执行的操作的函数。但 `Time` 类型的定义和后续的函数定义之间没有明确的联系。

我们可以通过将函数重写为**方法**（method）来使这种联系变得明确，方法是在类型定义内部定义的。

## 定义方法

在上一章中，我们定义了一个名为 `Time` 的类型，并编写了一个名为 `print_time` 的函数来显示一天中的时间。

```auto
type Time {
    hour: int,
    minute: int,
    second: int,
}

fn print_time(time: Time) {
    let s = f"{time.hour:02d}:{time.minute:02d}:{time.second:02d}"
    print(s)
}
```

要将 `print_time` 变成方法，我们用 `&self` 作为第一个参数来定义它。`&self` 参数指代调用方法的对象 -- 它是**接收者**（receiver）。

```auto
type Time {
    hour: int,
    minute: int,
    second: int,

    fn print_time(&self) {
        let s = f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
        print(s)
    }
}
```

要调用这个方法，你使用点表示法在 `Time` 实例上调用它：

```auto
let start = make_time(9, 45, 0)
start.print_time()  // 09:45:00
```

在这个版本中，`start` 是方法被调用的对象，称为**接收者**。在方法内部，`self` 指向与 `start` 相同的对象。

## 另一个方法

下面是上一章的 `time_to_int` 函数，重写为方法：

```auto
fn time_to_int(&self) -> int {
    let minutes = self.hour * 60 + self.minute
    let seconds = minutes * 60 + self.second
    return seconds
}
```

与前面的示例一样，方法使用 `&self` 作为第一个参数，并通过 `self` 访问字段。除此之外，方法与函数完全相同。

```auto
let start = make_time(9, 45, 0)
let secs = start.time_to_int()
print("Seconds:", secs)  // 35100
```

通常我们说"调用"（call）函数，"调用"（invoke）方法，但它们的意思相同。

## 静态方法

作为另一个示例，让我们考虑 `int_to_time` 函数。这个函数接受 `seconds` 作为参数并返回一个新的 `Time` 对象。如果我们将它转换为方法，就必须在一个 `Time` 对象上调用它。但如果我们正试图创建一个新的 `Time` 对象，应该在什么上调用它呢？

我们可以使用**静态方法**（static method）来解决这个问题，静态方法没有 `&self` 参数，是在类型本身而不是实例上调用的。

```auto
fn int_to_time(seconds: int) -> Time {
    let (minute, second) = divmod(seconds, 60)
    let (hour, minute) = divmod(minute, 60)
    return make_time(hour, minute, second)
}
```

因为它是静态方法，所以没有 `&self` 参数。要调用它，我们使用 `Time`，即类型名称：

```auto
let start = Time.int_to_time(34800)
start.print_time()  // 09:40:00
```

结果是一个表示 9:40 的新对象。

<Listing number="15-1" file-name="defining_methods.auto" caption="定义具有实例方法和静态方法的类型">

```auto
type Time {
    hour: int,
    minute: int,
    second: int,
}

fn print_time(&self) {
    let s = f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
    print(s)
}

fn time_to_int(&self) -> int {
    let minutes = self.hour * 60 + self.minute
    let seconds = minutes * 60 + self.second
    return seconds
}

fn add_time(&self, hours: int, minutes: int, seconds: int) -> Time {
    let duration = make_time(hours, minutes, seconds)
    let total = Time.time_to_int(self) + Time.time_to_int(duration)
    return Time.int_to_time(total)
}

fn int_to_time(seconds: int) -> Time {
    let (minute, second) = divmod(seconds, 60)
    let (hour, minute) = divmod(minute, 60)
    return make_time(hour, minute, second)
}

fn make_time(hour: int, minute: int, second: int) -> Time {
    return Time{hour: hour, minute: minute, second: second}
}

fn main() {
    let start = make_time(9, 45, 0)

    // 在实例上调用方法
    start.print_time()  // 09:45:00

    // 另一个方法
    let secs = start.time_to_int()
    print("Seconds since midnight:", secs)  // 35100

    // 调用返回新对象的方法
    let end = start.add_time(1, 32, 0)
    end.print_time()  // 11:17:00

    // 通过类型调用静态方法
    let t = Time.int_to_time(3661)
    t.print_time()  // 01:01:01
}
```

```python
class Time:
    """Represents the time of day."""

    def print_time(self):
        s = f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
        print(s)

    def time_to_int(self):
        minutes = self.hour * 60 + self.minute
        seconds = minutes * 60 + self.second
        return seconds

    def add_time(self, hours, minutes, seconds):
        duration = make_time(hours, minutes, seconds)
        total = Time.time_to_int(self) + Time.time_to_int(duration)
        return Time.int_to_time(total)

    @staticmethod
    def int_to_time(seconds):
        minute, second = divmod(seconds, 60)
        hour, minute = divmod(minute, 60)
        return make_time(hour, minute, second)


def make_time(hour, minute, second):
    time = Time()
    time.hour = hour
    time.minute = minute
    time.second = second
    return time


def main():
    start = make_time(9, 45, 0)

    # 在实例上调用方法
    start.print_time()  # 09:45:00

    # 另一个方法
    secs = start.time_to_int()
    print(f"Seconds since midnight: {secs}")  # 35100

    # 调用返回新对象的方法
    end = start.add_time(1, 32, 0)
    end.print_time()  # 11:17:00

    # 通过类调用静态方法
    t = Time.int_to_time(3661)
    t.print_time()  # 01:01:01


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

实例方法（带有 `&self`）在对象上调用：`start.print_time()`。在方法内部，`self` 指向接收对象。静态方法（没有 `&self`）在类型本身上调用：`Time.int_to_time(3661)`。它们不在特定实例上操作，适用于创建对象或执行与类型相关的计算的工具函数。

## 比较 Time 对象

作为另一个示例，让我们将 `is_after` 编写为方法。因为我们要比较两个对象，第一个参数是 `self`，所以我们将第二个参数命名为 `other`：

```auto
fn is_after(&self, other: Time) -> bool {
    return self.time_to_int() > other.time_to_int()
}
```

要使用这个方法，我们在一个对象上调用它，并将另一个对象作为参数传递：

```auto
let end = make_time(11, 17, 0)
print(end.is_after(start))    // true
print(start.is_after(end))    // false
```

这种语法的一个好处是它几乎读起来像一个问题："`end` 在 `start` 之后吗？"

## init 方法

最重要的特殊方法是 `init`，因为它用于初始化新对象的字段。`Time` 类型的 `init` 方法可能如下所示：

```auto
fn init(&self, hour: int = 0, minute: int = 0, second: int = 0) {
    self.hour = hour
    self.minute = minute
    self.second = second
}
```

现在当我们实例化一个 `Time` 对象时，Auto 会调用 `init` 并传递参数。因此我们可以同时创建对象并初始化字段：

```auto
let time = Time(9, 40, 0)
print(time)  // 09:40:00
```

在这个示例中，参数有默认值，因此如果你不带参数调用 `Time`，你会得到默认值：

```auto
let time = Time()
print(time)  // 00:00:00
```

如果你提供一个参数，它会覆盖 `hour`：

```auto
let time = Time(9)
print(time)  // 09:00:00
```

如果你提供三个参数，它们会覆盖所有三个默认值。

编写新类型时，好的做法是先编写 `init`（使创建对象更容易）和 `to_string`（用于调试）。

<Listing number="15-2" file-name="init_constructor.auto" caption="用于初始化对象的 init 构造函数">

```auto
type Time {
    hour: int,
    minute: int,
    second: int,
}

// init 构造函数 -- 实例化时自动调用
fn init(&self, hour: int = 0, minute: int = 0, second: int = 0) {
    self.hour = hour
    self.minute = minute
    self.second = second
}

fn to_string(&self) -> str {
    return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
}

fn main() {
    // 提供所有参数
    let t1 = Time(9, 40, 0)
    print(t1.to_string())  // 09:40:00

    // 使用默认值创建（无参数）
    let t2 = Time()
    print(t2.to_string())  // 00:00:00

    // 部分参数
    let t3 = Time(9)
    print(t3.to_string())  // 09:00:00

    let t4 = Time(9, 45)
    print(t4.to_string())  // 09:45:00

    // 命名参数
    let t5 = Time(minute = 30, second = 15)
    print(t5.to_string())  // 00:30:15
}
```

```python
class Time:
    """Represents the time of day."""

    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"


def main():
    # 提供所有参数
    t1 = Time(9, 40, 0)
    print(t1.__str__())  # 09:40:00

    # 使用默认值创建（无参数）
    t2 = Time()
    print(t2.__str__())  # 00:00:00

    # 部分参数
    t3 = Time(9)
    print(t3.__str__())  # 09:00:00

    t4 = Time(9, 45)
    print(t4.__str__())  # 09:45:00

    # 命名参数
    t5 = Time(minute=30, second=15)
    print(t5.__str__())  # 00:30:15


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

Auto 中的 `init` 方法对应 Python 中的 `__init__`。当你使用 `Time(...)` 创建新对象时，它会自动被调用。参数可以有默认值，允许你以不同级别的具体性创建对象 -- 从 `Time()`（全部默认）到 `Time(9, 40, 0)`（全部指定）。命名参数允许你覆盖特定字段而无需提供前面的参数。

> **Python 程序员注意：**
>
> Auto 使用 `fn init(&self, ...)` 代替 Python 的 `def __init__(self, ...)`。`a2p` 转译器会自动将 `init` 转换为 `__init__`。

## `to_string` 方法

编写方法时，你几乎可以选择任何名称。但是，某些名称具有特殊含义。如果对象有一个名为 `to_string` 的方法，Auto 在需要时（例如打印或在 f-string 中使用时）会使用该方法将对象转换为字符串。

这是 Auto 对应 Python `__str__` 方法的方式。

```auto
fn to_string(&self) -> str {
    return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
}
```

你可以以通常的方式调用此方法：

```auto
let s = end.to_string()
print(s)  // 11:17:00
```

但 Auto 也可以自动调用它。如果你打印一个 `Time` 对象，Auto 会使用 `to_string` 方法：

```auto
print(end)  // 11:17:00
```

如果你在 f-string 中使用该对象，也是如此：

```auto
print(f"The time is {end}")  // The time is 11:17:00
```

<Listing number="15-3" file-name="to_string_method.auto" caption="to_string 方法用于字符串表示">

```auto
type Time {
    hour: int,
    minute: int,
    second: int,
}

fn init(&self, hour: int = 0, minute: int = 0, second: int = 0) {
    self.hour = hour
    self.minute = minute
    self.second = second
}

// to_string 方法 -- Auto 等价于 __str__
fn to_string(&self) -> str {
    return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
}

fn main() {
    let start = Time(9, 45, 30)

    // 显式调用 to_string
    let s = start.to_string()
    print(s)  // 09:45:30

    // to_string 由 print 自动调用
    print(start)  // 09:45:30

    // 使用 f-string 插值
    print(f"The time is {start}")  // The time is 09:45:30

    // 通过字符串表示比较两个时间
    let end = Time(10, 30, 0)
    print(start.to_string() < end.to_string())  // true (字典序)

    // 演示格式控制
    let noon = Time(12, 0, 0)
    print(noon.to_string())  // 12:00:00
}
```

```python
class Time:
    """Represents the time of day."""

    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"


def main():
    start = Time(9, 45, 30)

    # 显式调用 __str__
    s = start.__str__()
    print(s)  # 09:45:30

    # __str__ 由 print 自动调用
    print(start)  # 09:45:30

    # 使用 f-string 插值
    print(f"The time is {start}")  # The time is 09:45:30

    # 通过字符串表示比较两个时间
    end = Time(10, 30, 0)
    print(start.__str__() < end.__str__())  # True (字典序)

    # 演示格式控制
    noon = Time(12, 0, 0)
    print(noon.__str__())  # 12:00:00


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

Auto 中的 `to_string` 方法对应 Python 中的 `__str__`。它返回对象的字符串表示。当你打印对象或在 f-string 中使用它时，Auto（通过 `a2p` 转译器）会自动调用此方法。格式说明符 `:02d` 确保分钟和秒始终显示两位数字。

> **Python 程序员注意：**
>
> Auto 使用 `fn to_string(&self)` 代替 Python 的 `def __str__(self)`。`a2p` 转译器会自动将 `to_string` 转换为 `__str__`。阅读 Auto 代码时，任何名为 `to_string` 的方法都是字符串表示方法。

## 运算符重载

通过定义特殊方法，你可以指定运算符在程序员自定义类型上的行为。例如，如果你为 `Time` 类型定义了一个名为 `__add__` 的方法，你就可以在 Time 对象上使用 `+` 运算符。

下面是一个 `__add__` 方法：

```auto
fn __add__(&self, other: Time) -> Time {
    let seconds = self.time_to_int() + other.time_to_int()
    return Time.int_to_time(seconds)
}
```

我们可以这样使用：

```auto
let start = Time(9, 45, 0)
let duration = Time(1, 32, 0)
let end = start + duration
print(end)  // 11:17:00
```

运行这三行代码时发生了很多事情：

- 当我们实例化 `Time` 对象时，`init` 方法被调用。
- 当我们对 `Time` 对象使用 `+` 运算符时，`__add__` 方法被调用。
- 当我们打印 `Time` 对象时，`to_string` 方法被调用。

改变运算符的行为使其适用于程序员自定义类型的过程称为**运算符重载**（operator overloading）。对于每个运算符（如 `+`），都有一个对应的特殊方法（如 `__add__`）。

我们还可以重载 `==` 运算符进行相等比较：

```auto
fn __eq__(&self, other: Time) -> bool {
    return self.time_to_int() == other.time_to_int()
}
```

```auto
print(start == Time(9, 45, 0))  // true
print(start == duration)        // false
```

<Listing number="15-4" file-name="operator_overloading.auto" caption="比较和加法的运算符重载">

```auto
type Time {
    hour: int,
    minute: int,
    second: int,
}

fn init(&self, hour: int = 0, minute: int = 0, second: int = 0) {
    self.hour = hour
    self.minute = minute
    self.second = second
}

fn to_string(&self) -> str {
    return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"
}

fn time_to_int(&self) -> int {
    let minutes = self.hour * 60 + self.minute
    let seconds = minutes * 60 + self.second
    return seconds
}

fn int_to_time(seconds: int) -> Time {
    let (minute, second) = divmod(seconds, 60)
    let (hour, minute) = divmod(minute, 60)
    return Time(hour, minute, second)
}

// 运算符重载：is_after 比较
fn is_after(&self, other: Time) -> bool {
    return self.time_to_int() > other.time_to_int()
}

// 运算符重载：+ 运算符（加法）
fn __add__(&self, other: Time) -> Time {
    let seconds = self.time_to_int() + other.time_to_int()
    return Time.int_to_time(seconds)
}

// 运算符重载：== 运算符（相等）
fn __eq__(&self, other: Time) -> bool {
    return self.time_to_int() == other.time_to_int()
}

fn main() {
    let start = Time(9, 45, 0)
    let end = Time(11, 17, 0)
    let duration = Time(1, 32, 0)

    // 比较：is_after
    print(end.is_after(start))    // true
    print(start.is_after(end))    // false
    print(end.is_after(end))      // false

    // 运算符重载：+
    let result = start + duration
    print(result.to_string())  // 11:17:00

    // 链式加法
    let result2 = start + duration + Time(0, 30, 0)
    print(result2.to_string())  // 11:47:00

    // 运算符重载：==
    print(start == Time(9, 45, 0))  // true
    print(start == end)             // false

    // 组合运算符
    let total = duration + Time(0, 30, 0)
    let finish = start + total
    print(finish.to_string())  // 11:47:00
}
```

```python
class Time:
    """Represents the time of day."""

    def __init__(self, hour=0, minute=0, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"

    def time_to_int(self):
        minutes = self.hour * 60 + self.minute
        seconds = minutes * 60 + self.second
        return seconds

    @staticmethod
    def int_to_time(seconds):
        minute, second = divmod(seconds, 60)
        hour, minute = divmod(minute, 60)
        return Time(hour, minute, second)

    # 运算符重载：比较
    def is_after(self, other):
        return self.time_to_int() > other.time_to_int()

    # 运算符重载：+ 运算符
    def __add__(self, other):
        seconds = self.time_to_int() + other.time_to_int()
        return Time.int_to_time(seconds)

    # 运算符重载：== 运算符
    def __eq__(self, other):
        return self.time_to_int() == other.time_to_int()


def main():
    start = Time(9, 45, 0)
    end = Time(11, 17, 0)
    duration = Time(1, 32, 0)

    # 比较：is_after
    print(end.is_after(start))  # True
    print(start.is_after(end))  # False
    print(end.is_after(end))  # False

    # 运算符重载：+
    result = start + duration
    print(result.__str__())  # 11:17:00

    # 链式加法
    result2 = start + duration + Time(0, 30, 0)
    print(result2.__str__())  # 11:47:00

    # 运算符重载：==
    print(start == Time(9, 45, 0))  # True
    print(start == end)  # False

    # 组合运算符
    total = duration + Time(0, 30, 0)
    finish = start + total
    print(finish.__str__())  # 11:47:00


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

运算符重载允许你定义 `+` 和 `==` 等运算符如何与自定义类型一起工作。当你使用 `+` 时会调用 `__add__` 方法，当你使用 `==` 时会调用 `__eq__` 方法。两者都是将 `&self` 和 `other` 作为参数的实例方法。

`is_after` 方法不是运算符重载 -- 它是一个具有描述性名称的常规方法。但它演示了同样的模式：先将对象转换为更简单的表示形式（整数）再进行比较。

## 调试

如果 `Time` 对象的 `minute` 和 `second` 值在 `0` 到 `60` 之间（包括 `0` 但不包括 `60`），且 `hour` 为正数，则它是有效的。此外，`hour` 和 `minute` 应该是整数值。这类要求称为**不变量**（invariants），因为它们应该始终为真。

编写检查不变量的代码可以帮助检测错误并找到其原因。例如，你可以编写一个 `is_valid` 方法，如果违反不变量则返回 `false`：

```auto
fn is_valid(&self) -> bool {
    if self.hour < 0 or self.minute < 0 or self.second < 0 {
        return false
    }
    if self.minute >= 60 or self.second >= 60 {
        return false
    }
    return true
}
```

然后，在每个方法的开头，你可以检查参数以确保它们是有效的：

```auto
fn is_after(&self, other: Time) -> bool {
    assert self.is_valid(), "self is not a valid Time"
    assert other.is_valid(), "other is not a valid Time"
    return self.time_to_int() > other.time_to_int()
}
```

`assert` 语句评估后面的表达式。如果结果为 `true`，它什么也不做；如果结果为 `false`，它会导致错误。

## 术语表

**面向对象语言：**
提供支持面向对象编程特性的语言，特别是用户自定义类型。

**方法：**
在类型定义内部定义并在该类型的实例上调用的函数。

**接收者：**
方法被调用的对象。

**静态方法：**
无需对象作为接收者即可调用的方法。在 Auto 中，这是没有 `&self` 参数的方法。

**实例方法：**
必须在对象作为接收者上调用的方法。在 Auto 中，这是带有 `&self` 参数的方法。

**特殊方法：**
改变运算符和某些函数如何与对象一起工作的方法。在 Auto 中，这些包括 `init`、`to_string`、`__add__`、`__eq__` 等。

**运算符重载：**
使用特殊方法改变运算符与用户自定义类型一起工作的方式的过程。

**不变量：**
在程序执行期间应始终为真的条件。

## 练习

### 练习

在上一章中，一系列练习要求你编写一个 `Date` 类型和几个处理 `Date` 对象的函数。现在让我们练习将这些函数重写为方法。

1. 编写一个表示日期（年、月、日）的 `Date` 类型定义。包含一个接受 `year`、`month` 和 `day` 作为参数的 `init` 方法。

2. 编写一个 `to_string` 方法，使用 f-string 格式化字段并返回结果。如果你用创建的 `Date` 测试它，结果应该是 `1933-06-22`。

3. 编写一个名为 `is_after` 的方法，接受两个 `Date` 对象，如果第一个在第二个之后则返回 `true`。创建第二个表示 1933 年 9 月 17 日的对象，并检查它是否在第一个对象之后。

提示：你可能需要编写一个名为 `to_tuple` 的方法，返回一个包含 `Date` 字段（年-月-日顺序）的元组。
