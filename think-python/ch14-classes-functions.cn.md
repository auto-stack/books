# 类与函数

至此你已经知道如何使用函数来组织代码，以及如何使用内置类型来组织数据。下一步是**面向对象编程**（object-oriented programming），它使用程序员自定义的类型来同时组织代码和数据。

面向对象编程是一个很大的主题，因此我们将循序渐进地学习。在本章中，我们将从非惯用代码（即不是有经验的程序员编写的那种代码）开始，但这是一个很好的起点。在接下来的两章中，我们将使用更多特性来编写更惯用的代码。

## 程序员自定义类型

我们已经使用了许多 Auto 的内置类型 -- 现在我们将定义一个新类型。作为第一个示例，我们将创建一个名为 `Time` 的类型来表示一天中的时间。程序员自定义的类型也称为**类**（class）。

在 Auto 中，类型定义指定对象包含的字段：

```auto
type Time {
    hour: int,
    minute: int,
    second: int,
}
```

头部表明新类型名为 `Time`。主体列出了三个字段：`hour`、`minute` 和 `second`。定义类型会创建一个**类对象**。

类对象就像创建对象的工厂。要创建一个 `Time` 对象，你可以用字段值调用 `Time`：

```auto
let lunch = Time{hour: 11, minute: 59, second: 1}
```

结果是一个类型为 `Time` 的新对象。

创建新对象称为**实例化**（instantiation），该对象是类的**实例**（instance）。

## 属性

对象包含变量，称为**属性**（attributes）。在 Auto 中，属性作为类型声明的一部分定义，并使用点表示法访问：

```auto
print(lunch.hour)   // 11
print(lunch.minute) // 59
print(lunch.second) // 1
```

你可以在任何表达式中使用属性：

```auto
let total_minutes = lunch.hour * 60 + lunch.minute
print(total_minutes)  // 719
```

你也可以在 f-string 中使用点运算符：

```auto
print(f"{lunch.hour:02d}:{lunch.minute:02d}:{lunch.second:02d}")  // 11:59:01
```

格式说明符 `:02d` 表示 `minute` 和 `second` 应至少显示两位数字，必要时在前面补零。

我们可以编写一个显示 `Time` 对象的函数：

```auto
fn print_time(time: Time) {
    let s = f"{time.hour:02d}:{time.minute:02d}:{time.second:02d}"
    print(s)
}
```

调用时，我们可以将 `lunch` 作为参数传递：

```auto
print_time(lunch)  // 11:59:01
```

## 对象作为返回值

函数可以返回对象。例如，`make_time` 接受参数，将它们作为字段存储在 `Time` 对象中，并返回新对象：

```auto
fn make_time(hour: int, minute: int, second: int) -> Time {
    return Time{hour: hour, minute: minute, second: second}
}
```

以下是我们如何使用 `make_time` 创建一个 `Time` 对象：

```auto
let time = make_time(11, 59, 1)
print_time(time)  // 11:59:01
```

<Listing number="14-1" file-name="defining_a_type.auto" caption="定义类型和使用属性">

```auto
type Point {
    x: float,
    y: float,
}

fn print_point(p: Point) {
    print(f"({p.x}, {p.y})")
}

fn main() {
    // 创建 Point 类型和实例化
    let lunch = Point{x: 0.0, y: 0.0}
    print(type(lunch))  // Point

    // 赋值属性
    lunch.x = 11.0
    lunch.y = 59.0
    print_point(lunch)  // (11, 59)

    // 读取属性
    print(lunch.x)  // 11.0

    // 在表达式中使用属性
    let total_minutes = lunch.x * 60.0 + lunch.y
    print("Total minutes:", total_minutes)  // 719.0

    // 创建另一个 Point
    let p = Point{x: 3.0, y: 4.0}
    print_point(p)  // (3, 4)

    // 到原点的距离
    let distance = (p.x ** 2.0 + p.y ** 2.0) ** 0.5
    print("Distance:", distance)  // 5.0
}
```

```python
class Point:
    pass


def print_point(p):
    print(f"({p.x}, {p.y})")


def main():
    # 创建 Point 类型和实例化
    lunch = Point()
    print(type(lunch))  # <class '__main__.Point'>

    # 赋值属性
    lunch.x = 11.0
    lunch.y = 59.0
    print_point(lunch)  # (11.0, 59.0)

    # 读取属性
    print(lunch.x)  # 11.0

    # 在表达式中使用属性
    total_minutes = lunch.x * 60.0 + lunch.y
    print(f"Total minutes: {total_minutes}")  # 719.0

    # 创建另一个 Point
    p = Point()
    p.x = 3.0
    p.y = 4.0
    print_point(p)  # (3.0, 4.0)

    # 到原点的距离
    distance = (p.x ** 2 + p.y ** 2) ** 0.5
    print(f"Distance: {distance}")  # 5.0


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`type` 关键字定义一个新的类结构体类型，包含命名字段。在 Auto 中，`type Point { x: float, y: float }` 声明了一个具有两个浮点字段的 `Point` 类型。对象使用 `Point{x: ..., y: ...}` 构造语法创建，字段通过点表示法访问（`p.x`、`p.y`）。

在 Python 中，等价形式是一个空的 `class Point: pass`，属性在实例化后动态赋值。Auto 的类型声明使结构在一开始就明确。

## 对象是可变的

假设你要去看一场晚上 9:20 开始、时长 92 分钟（1 小时 32 分钟）的电影。电影几点结束？

首先，我们创建一个表示开始时间的 `Time` 对象：

```auto
let mut start = make_time(9, 20, 0)
print_time(start)  // 09:20:00
```

要找到结束时间，我们可以修改 `Time` 对象的字段，加上电影的时长：

```auto
start.hour += 1
start.minute += 32
print_time(start)  // 10:52:00
```

我们可以将此封装在一个函数中：

```auto
fn increment_time(time: Time, hours: int, minutes: int, seconds: int) {
    time.hour += hours
    time.minute += minutes
    time.second += seconds
}
```

```auto
let mut start = make_time(9, 20, 0)
increment_time(start, 1, 32, 0)
print_time(start)  // 10:52:00
```

在函数内部，`time` 是 `start` 的别名，因此修改 `time` 时，`start` 也会改变。

这个函数可以工作，但它运行后，名为 `start` 的变量指向的对象表示的是*结束*时间，而我们不再有表示开始时间的对象。更好的做法是保持 `start` 不变，创建一个新对象来表示结束时间。

## 复制

在 Python 中，`copy` 模块提供了一个可以复制任何对象的函数。在 Auto 中，你可以创建一个具有相同值的新对象：

```auto
let end = Time{hour: start.hour, minute: start.minute, second: start.second}
```

现在 `start` 和 `end` 包含相同的数据，但它们是不同的对象。

**浅复制**（shallow copy）复制对象本身，但如果它包含对其他对象的引用，这些引用是共享的。**深复制**（deep copy）复制对象及其引用的所有内容。在大多数简单类型（如 `Time`）的情况下，浅复制就足够了。

## 对象作为返回值

函数可以返回对象，这使得组合操作变得容易。例如，下面是一个创建 `Rectangle` 类型的函数，其中一个字段是 `Point`：

```auto
type Point {
    x: float,
    y: float,
}

type Rectangle {
    corner: Point,
    width: float,
    height: float,
}
```

像 `find_center` 这样的函数可以接收一个 `Rectangle` 并返回一个 `Point`：

```auto
fn find_center(box: Rectangle) -> Point {
    let cx = box.corner.x + box.width / 2.0
    let cy = box.corner.y + box.height / 2.0
    return Point{x: cx, y: cy}
}
```

<Listing number="14-2" file-name="objects_as_return_values.auto" caption="创建和返回对象的函数">

```auto
type Rectangle {
    corner: Point,
    width: float,
    height: float,
}

type Point {
    x: float,
    y: float,
}

fn print_point(p: Point) {
    print(f"({p.x}, {p.y})")
}

fn print_rect(box: Rectangle) {
    print("Corner:", box.corner)
    print(f"Width: {box.width}, Height: {box.height}")
}

fn find_center(box: Rectangle) -> Point {
    let cx = box.corner.x + box.width / 2.0
    let cy = box.corner.y + box.height / 2.0
    return Point{x: cx, y: cy}
}

fn grow_rectangle(box: Rectangle, dwidth: float, dheight: float) -> Rectangle {
    return Rectangle{
        corner: box.corner,
        width: box.width + dwidth,
        height: box.height + dheight,
    }
}

fn main() {
    // 创建一个 Point
    let origin = Point{x: 0.0, y: 0.0}

    // 创建一个 Rectangle（对象作为字段）
    let box = Rectangle{corner: origin, width: 100.0, height: 200.0}
    print_rect(box)

    // 返回对象的函数
    let center = find_center(box)
    print("Center:")
    print_point(center)  // (50, 100)

    // 增大矩形返回一个新对象
    let grown = grow_rectangle(box, 50.0, 100.0)
    print_rect(grown)

    // 原始对象未改变
    print_rect(box)
}
```

```python
class Point:
    pass


class Rectangle:
    pass


def print_point(p):
    print(f"({p.x}, {p.y})")


def print_rect(box):
    print(f"Corner: ({box.corner.x}, {box.corner.y})")
    print(f"Width: {box.width}, Height: {box.height}")


def find_center(box):
    cx = box.corner.x + box.width / 2
    cy = box.corner.y + box.height / 2
    result = Point()
    result.x = cx
    result.y = cy
    return result


def grow_rectangle(box, dwidth, dheight):
    result = Rectangle()
    result.corner = box.corner
    result.width = box.width + dwidth
    result.height = box.height + dheight
    return result


def main():
    # 创建一个 Point
    origin = Point()
    origin.x = 0.0
    origin.y = 0.0

    # 创建一个 Rectangle（对象作为字段）
    box = Rectangle()
    box.corner = origin
    box.width = 100.0
    box.height = 200.0
    print_rect(box)

    # 返回对象的函数
    center = find_center(box)
    print("Center:")
    print_point(center)  # (50.0, 100.0)

    # 增大矩形返回一个新对象
    grown = grow_rectangle(box, 50.0, 100.0)
    print_rect(grown)

    # 原始对象未改变
    print_rect(box)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

对象可以包含其他对象作为字段。`Rectangle` 类型有一个类型为 `Point` 的 `corner` 字段。函数可以返回新对象 -- `find_center` 计算并返回一个新的 `Point`，而 `grow_rectangle` 返回一个具有修改后尺寸的新 `Rectangle`。

这种创建并返回新对象（而不是修改现有对象）的模式是**纯函数**的基础。

## 纯函数

我们可以编写不修改其参数的纯函数。**纯函数**（pure function）不修改传递给它的任何对象，其唯一作用是返回一个值。

例如，下面是一个将 `Time` 转换为整数（自午夜以来的秒数）并转换回来的函数：

```auto
fn time_to_int(time: Time) -> int {
    let minutes = time.hour * 60 + time.minute
    let seconds = minutes * 60 + time.second
    return seconds
}

fn int_to_time(seconds: int) -> Time {
    let (minute, second) = divmod(seconds, 60)
    let (hour, minute) = divmod(minute, 60)
    return make_time(hour, minute, second)
}
```

使用这些转换函数，我们可以编写一个简洁的 `add_time`：

```auto
fn add_time(time: Time, hours: int, minutes: int, seconds: int) -> Time {
    let duration = make_time(hours, minutes, seconds)
    let total_seconds = time_to_int(time) + time_to_int(duration)
    return int_to_time(total_seconds)
}
```

第一行将参数转换为一个 `Time` 对象。第二行将两者都转换为秒并相加。第三行将总和转换回 `Time` 并返回。

```auto
let start = make_time(9, 40, 0)
let end = add_time(start, 1, 32, 0)
print_time(start)  // 09:40:00  -- 未改变！
print_time(end)    // 11:12:00
```

非纯函数（修改器）能做的事情，纯函数也能做到。使用纯函数的程序可能更不容易出错，但非纯函数有时更方便且更高效。一般来说，在合理的情况下尽量编写纯函数。这种方法可以称为**函数式编程风格**。

<Listing number="14-3" file-name="pure_functions_vs_modifiers.auto" caption="纯函数与修改器的对比">

```auto
type Time {
    hour: int,
    minute: int,
    second: int,
}

fn print_time(time: Time) {
    print(f"{time.hour:02d}:{time.minute:02d}:{time.second:02d}")
}

fn make_time(hour: int, minute: int, second: int) -> Time {
    return Time{hour: hour, minute: minute, second: second}
}

fn time_to_int(time: Time) -> int {
    let minutes = time.hour * 60 + time.minute
    let seconds = minutes * 60 + time.second
    return seconds
}

fn int_to_time(seconds: int) -> Time {
    let (minute, second) = divmod(seconds, 60)
    let (hour, minute) = divmod(minute, 60)
    return make_time(hour, minute, second)
}

// 修改器：就地更改对象
fn increment_time(time: Time, hours: int, minutes: int, seconds: int) {
    time.hour += hours
    time.minute += minutes
    time.second += seconds
    let (carry, time.second) = divmod(time.second, 60)
    let (carry, time.minute) = divmod(time.minute + carry, 60)
    let (_, time.hour) = divmod(time.hour + carry, 24)
}

// 纯函数：不修改原始对象
fn add_time(time: Time, hours: int, minutes: int, seconds: int) -> Time {
    let duration = make_time(hours, minutes, seconds)
    let total_seconds = time_to_int(time) + time_to_int(duration)
    return int_to_time(total_seconds)
}

fn main() {
    // --- 修改器方式 ---
    let mut start = make_time(9, 40, 0)
    print("Start (modifier):", end = " ")
    print_time(start)  // 09:40:00

    increment_time(start, 1, 32, 0)
    print("After increment: ", end = " ")
    print_time(start)  // 11:12:00
    // 注意：start 已被改变！

    // --- 纯函数方式 ---
    let fresh = make_time(9, 40, 0)
    let end = add_time(fresh, 1, 32, 0)
    print("Start (pure):    ", end = " ")
    print_time(fresh)  // 09:40:00  -- 未改变！
    print("End (pure):      ", end = " ")
    print_time(end)    // 11:12:00

    // 纯函数处理大数值
    let end2 = add_time(fresh, 0, 90, 120)
    print("End (+90m +120s):", end = " ")
    print_time(end2)   // 11:12:00

    // 转换为整数和从整数转换回来
    let t = make_time(1, 1, 1)
    let secs = time_to_int(t)
    print("01:01:01 =", secs, "seconds")  // 3661 seconds
    let back = int_to_time(secs)
    print_time(back)  // 01:01:01
}
```

```python
class Time:
    pass


def print_time(time):
    s = f"{time.hour:02d}:{time.minute:02d}:{time.second:02d}"
    print(s)


def make_time(hour, minute, second):
    time = Time()
    time.hour = hour
    time.minute = minute
    time.second = second
    return time


def time_to_int(time):
    minutes = time.hour * 60 + time.minute
    seconds = minutes * 60 + time.second
    return seconds


def int_to_time(seconds):
    minute, second = divmod(seconds, 60)
    hour, minute = divmod(minute, 60)
    return make_time(hour, minute, second)


# 修改器：就地更改对象
def increment_time(time, hours, minutes, seconds):
    time.hour += hours
    time.minute += minutes
    time.second += seconds
    carry, time.second = divmod(time.second, 60)
    carry, time.minute = divmod(time.minute + carry, 60)
    _, time.hour = divmod(time.hour + carry, 24)


# 纯函数：不修改原始对象
def add_time(time, hours, minutes, seconds):
    duration = make_time(hours, minutes, seconds)
    total_seconds = time_to_int(time) + time_to_int(duration)
    return int_to_time(total_seconds)


def main():
    # --- 修改器方式 ---
    start = make_time(9, 40, 0)
    print("Start (modifier): ", end="")
    print_time(start)  # 09:40:00

    increment_time(start, 1, 32, 0)
    print("After increment:  ", end="")
    print_time(start)  # 11:12:00
    # 注意：start 已被改变！

    # --- 纯函数方式 ---
    fresh = make_time(9, 40, 0)
    end = add_time(fresh, 1, 32, 0)
    print("Start (pure):     ", end="")
    print_time(fresh)  # 09:40:00  -- 未改变！
    print("End (pure):       ", end="")
    print_time(end)  # 11:12:00

    # 纯函数处理大数值
    end2 = add_time(fresh, 0, 90, 120)
    print("End (+90m +120s): ", end="")
    print_time(end2)  # 11:12:00

    # 转换为整数和从整数转换回来
    t = make_time(1, 1, 1)
    secs = time_to_int(t)
    print(f"01:01:01 = {secs} seconds")  # 3661 seconds
    back = int_to_time(secs)
    print_time(back)  # 01:01:01


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

修改器 `increment_time` 就地更改 `Time` 对象 -- 调用后，原始变量现在持有不同的值。纯函数 `add_time` 创建并返回一个新的 `Time` 对象，保持原始对象不变。

转换函数 `time_to_int` 和 `int_to_time` 提供了一种处理时间值算术运算的简洁方法：将时间转换为整数表示（自午夜以来的秒数），进行数学运算，然后转换回来。这避免了手动处理小时、分钟和秒之间的进位的复杂性。

## 原型与修补

在前面的示例中，`increment_time` 和 `add_time` 似乎可以工作，但如果我们尝试另一个例子，就会发现它们并不完全正确。假设电影在 9:40 开始，而不是 9:20：

```auto
let start = make_time(9, 40, 0)
let end = add_time(start, 1, 32, 0)
print_time(end)  // 11:12:00  -- 正确！
```

但如果时长是 92 分钟而不是 1 小时 32 分钟呢？

```auto
let end = add_time(start, 0, 92, 0)
```

如果没有正确处理，结果不是一个有效的时间。关键洞察是使用 `divmod` 正确处理进位：

```auto
fn increment_time(time: Time, hours: int, minutes: int, seconds: int) {
    time.hour += hours
    time.minute += minutes
    time.second += seconds
    let (carry, time.second) = divmod(time.second, 60)
    let (carry, time.minute) = divmod(time.minute + carry, 60)
    let (_, time.hour) = divmod(time.hour + carry, 24)
}
```

本节演示了一种称为**原型与修补**（prototype and patch）的开发计划 -- 从一个简单的原型开始，使其适用于第一个示例，然后用更困难的示例进行测试，发现错误时进行修复。这种方法很有效，但增量修正可能会生成不必要地复杂的代码。

## 设计优先的开发

另一种方案是**设计优先的开发**（design-first development），它涉及在原型制作之前进行更多的规划。在设计优先的过程中，对问题的高层次洞察可以使编程变得更加容易。

在本例中，洞察在于我们可以将 `Time` 对象视为一个以 60 为基数（六十进制）的三位数。`second` 字段是"个位"，`minute` 字段是"六十位"，`hour` 字段是"三千六百位"。

这一观察建议将 `Time` 对象转换为整数，并利用 Auto 知道如何进行整数算术运算这一事实。前一节中展示的 `time_to_int` 和 `int_to_time` 函数实现了这种方法。

讽刺的是，有时把一个问题变得更难 -- 或更通用 -- 反而使它变得更简单，因为特殊情况更少，出错的机会也更少。

## 调试

Auto 提供了几个内置函数，用于测试和调试处理对象的程序。例如，你可以检查对象的类型：

```auto
print(type(start))  // Time
```

你也可以使用 `isinstance` 检查对象是否是特定类型的实例：

```auto
print(isinstance(end, Time))  // true
```

要获取所有字段及其值，可以使用 `vars`：

```auto
print(vars(start))  // {hour: 9, minute: 40, second: 0}
```

## 术语表

**面向对象编程：**
一种使用对象来组织代码和数据的编程风格。

**类：**
程序员自定义的类型。类定义创建一个新的类对象。

**类对象：**
表示类的对象 -- 它是类型定义的结果。

**实例化：**
创建属于类的对象的过程。

**实例：**
属于类的对象。

**属性：**
与对象关联的变量，也称为实例变量。在 Auto 中，属性作为类型定义中的字段声明。

**格式说明符：**
在 f-string 中，格式说明符确定值如何转换为字符串。

**纯函数：**
不修改其参数或除返回值外没有其他任何效果的函数。

**函数式编程风格：**
尽可能使用纯函数的编程方式。

**原型与修补：**
通过从粗略草稿开始，逐步添加功能和修复错误来开发程序的方法。

**设计优先的开发：**
比原型与修补更仔细地规划程序的开发方法。

## 练习

### 练习

编写一个名为 `subtract_time` 的函数，接受两个 `Time` 对象，并返回它们之间的间隔（以秒为单位）-- 假设它们是同一天中的两个时间。

### 练习

编写一个名为 `is_after` 的函数，接受两个 `Time` 对象，如果第一个时间在一天中比第二个时间更晚，则返回 `true`，否则返回 `false`。

### 练习

下面是一个表示日期（年、月、日）的 `Date` 类型定义：

```auto
type Date {
    year: int,
    month: int,
    day: int,
}
```

1. 编写一个名为 `make_date` 的函数，接受 `year`、`month` 和 `day` 作为参数并返回一个新的 `Date` 对象。创建一个表示 1933 年 6 月 22 日的对象。

2. 编写一个名为 `print_date` 的函数，接受一个 `Date` 对象，使用 f-string 格式化字段并打印结果。如果你用创建的 `Date` 测试它，结果应该是 `1933-06-22`。

3. 编写一个名为 `is_after` 的函数，接受两个 `Date` 对象，如果第一个在第二个之后则返回 `true`。创建第二个表示 1933 年 9 月 17 日的对象，并检查它是否在第一个对象之后。

提示：你可能需要编写一个名为 `date_to_tuple` 的函数，返回一个包含 `Date` 字段（年、月、日顺序）的元组。
