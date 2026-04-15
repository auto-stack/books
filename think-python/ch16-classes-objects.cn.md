# 类与对象

到此为止，我们已经定义了表示一天中的时间和一年中的某天的类，并创建了这些类的对象。我们还定义了创建、修改以及对这些对象进行计算的方法。

在本章中，我们将继续面向对象编程（OOP）的探索，定义表示几何对象的类，包括点、线和矩形。我们将编写创建和修改这些对象的方法。

我们将使用这些类来演示 OOP 主题，包括对象身份与等价、浅拷贝与深拷贝以及多态。

## 创建 Point

在计算机图形学中，屏幕上的位置通常用 `x`-`y` 平面中的一对坐标来表示。按照惯例，点 `(0, 0)` 通常表示屏幕的左上角，`(x, y)` 表示从原点向右 `x` 个单位、向下 `y` 个单位的点。

在 Auto 中有几种表示点的方式：

- 可以将坐标分别存储在两个变量 `x` 和 `y` 中。

- 可以将坐标存储为列表或元组的元素。

- 可以创建一个新类型来将点表示为对象。

在面向对象编程中，最惯用的方式是创建一个新类型。为此，我们从 `Point` 的类定义开始。

```auto
type Point {
    x: float,
    y: float,
}

fn init(&self, x: float = 0.0, y: float = 0.0) {
    self.x = x
    self.y = y
}

fn to_string(&self) -> str {
    return f"Point({self.x}, {self.y})"
}
```

`init` 方法将坐标作为参数并赋值给属性 `x` 和 `y`。`to_string` 方法返回 `Point` 的字符串表示。

现在我们可以这样实例化和显示一个 `Point` 对象：

```auto
let start = Point(0.0, 0.0)
print(start)  // Point(0, 0)
```

如往常一样，程序员自定义类型用一个框表示，类型名在外面，属性在里面。

通常，程序员自定义类型是可变的，所以我们可以编写一个 `translate` 方法，接受两个数字 `dx` 和 `dy`，并将它们加到属性 `x` 和 `y` 上。

```auto
fn translate(&self, dx: float, dy: float) {
    self.x += dx
    self.y += dy
}
```

这个方法将 `Point` 从平面中的一个位置移动到另一个位置。它就地修改现有对象。

## 创建 Line

现在让我们定义一个表示两点之间线段的类。如往常一样，我们从 `init` 方法和 `to_string` 方法开始。

```auto
type Line {
    p1: Point,
    p2: Point,
}

fn init(&self, p1: Point, p2: Point) {
    self.p1 = p1
    self.p2 = p2
}

fn to_string(&self) -> str {
    return f"Line({self.p1}, {self.p2})"
}
```

有了这两个方法，我们就可以实例化和显示一个 `Line` 对象：

```auto
let line = Line(start, end)
print(line)  // Line(Point(0, 0), Point(300, 150))
```

当我们调用 `print` 并传递 `line` 作为参数时，`print` 会在 `line` 上调用 `to_string`。`to_string` 方法使用 f-string 创建 `line` 的字符串表示。

f-string 中有两个花括号中的表达式 `self.p1` 和 `self.p2`。当这些表达式被求值时，结果是 `Point` 对象。然后，当它们被转换为字符串时，会调用 `Point` 类中的 `to_string` 方法。

这就是为什么当我们显示一个 `Line` 时，结果包含了 `Point` 对象的字符串表示。

这是**组合**（composition）的一个例子 -- 一个 `Line` 由两个 `Point` 对象组成。组合是将简单对象组合成更复杂对象的一种方式。

<Listing number="16-1" file-name="point_line_classes.auto" caption="Point 和 Line 类（组合）">

```auto
type Point {
    x: float,
    y: float,
}

fn init(&self, x: float = 0.0, y: float = 0.0) {
    self.x = x
    self.y = y
}

fn to_string(&self) -> str {
    return f"Point(${self.x}, ${self.y})"
}

fn __eq__(&self, other: Point) -> bool {
    return self.x == other.x and self.y == other.y
}

fn translate(&self, dx: float, dy: float) {
    self.x += dx
    self.y += dy
}

type Line {
    p1: Point,
    p2: Point,
}

fn init(&self, p1: Point, p2: Point) {
    self.p1 = p1
    self.p2 = p2
}

fn to_string(&self) -> str {
    return f"Line(${self.p1}, ${self.p2})"
}

fn __eq__(&self, other: Line) -> bool {
    return (self.p1 == other.p1 and self.p2 == other.p2) or
           (self.p1 == other.p2 and self.p2 == other.p1)
}

fn midpoint(&self) -> Point {
    let mx = (self.p1.x + self.p2.x) / 2.0
    let my = (self.p1.y + self.p2.y) / 2.0
    return Point(mx, my)
}

fn main() {
    // 创建 Point 对象
    let start = Point(0.0, 0.0)
    print(start)  // Point(0, 0)

    let end = Point(300.0, 150.0)
    print(end)    // Point(300, 150)

    // 等价与身份
    let p1 = Point(200.0, 100.0)
    let p2 = Point(200.0, 100.0)
    print(p1 == p2)  // true  (等价)
    print(p1 is p2)  // false (不同对象)

    // 平移一个点
    end.translate(50.0, 25.0)
    print(end)  // Point(350, 175)

    // 组合：Line 包含 Point 对象
    let line1 = Line(start, end)
    print(line1)  // Line(Point(0, 0), Point(350, 175))

    // Line 等价（与顺序无关）
    let line2 = Line(end, start)
    print(line1 == line2)  // true

    // 线段的中点
    let mid = line1.midpoint()
    print(mid)  // Point(175, 87.5)
}
```

```python
class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return f"Line({self.p1}, {self.p2})"

    def __eq__(self, other):
        return ((self.p1 == other.p1 and self.p2 == other.p2) or
                (self.p1 == other.p2 and self.p2 == other.p1))

    def midpoint(self):
        mx = (self.p1.x + self.p2.x) / 2
        my = (self.p1.y + self.p2.y) / 2
        return Point(mx, my)


def main():
    # 创建 Point 对象
    start = Point(0.0, 0.0)
    print(start)  # Point(0.0, 0.0)

    end = Point(300.0, 150.0)
    print(end)    # Point(300.0, 150.0)

    # 等价与身份
    p1 = Point(200.0, 100.0)
    p2 = Point(200.0, 100.0)
    print(p1 == p2)  # True  (等价)
    print(p1 is p2)  # False (不同对象)

    # 平移一个点
    end.translate(50.0, 25.0)
    print(end)  # Point(350.0, 175.0)

    # 组合：Line 包含 Point 对象
    line1 = Line(start, end)
    print(line1)  # Line(Point(0.0, 0.0), Point(350.0, 175.0))

    # Line 等价（与顺序无关）
    line2 = Line(end, start)
    print(line1 == line2)  # True

    # 线段的中点
    mid = line1.midpoint()
    print(mid)  # Point(175.0, 87.5)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`Point` 类型有 `x` 和 `y` 字段，带有 `init` 构造函数和 `to_string` 方法。`__eq__` 方法基于坐标定义等价性，`translate` 就地修改点。`Line` 类型演示了**组合** -- 它包含两个 `Point` 对象作为字段。`Line` 的 `__eq__` 方法以任意顺序检查等价性（因为从 A 到 B 的线与从 B 到 A 的线相同）。`midpoint` 方法返回线段中点处的一个新 `Point`。

## 等价与身份

假设我们创建两个坐标相同的点。

```auto
let p1 = Point(200.0, 100.0)
let p2 = Point(200.0, 100.0)
```

如果我们使用 `==` 运算符比较它们，并且我们定义了 `__eq__`，它会检查属性是否相等。

```auto
print(p1 == p2)  // true
```

但 `is` 运算符仍然表明它们是不同的对象。

```auto
print(p1 is p2)  // false
```

不可能重写 `is` 运算符 -- 它总是检查对象是否是同一个。但对于程序员自定义类型，你可以重写 `==` 运算符，使其检查对象是否等价。你可以定义等价的含义。

## 创建 Rectangle

现在让我们定义一个表示矩形的类。为了简单起见，我们假设矩形是垂直或水平的，不是倾斜的。

我们应该使用什么属性来指定矩形的位置和大小？至少有两种可能：

- 可以指定矩形的宽度和高度以及一个角的位置。

- 可以指定两个对角。

让我们实现第一种方式。以下是类定义。

```auto
type Rectangle {
    width: float,
    height: float,
    corner: Point,
}

fn init(&self, width: float, height: float, corner: Point) {
    self.width = width
    self.height = height
    self.corner = corner
}

fn to_string(&self) -> str {
    return f"Rectangle({self.width}, {self.height}, {self.corner})"
}
```

`Rectangle` 类型有三个字段：`width`、`height` 和 `corner`，其中 `corner` 是一个 `Point` 对象。这是组合的另一个例子。

现在我们可以实例化一个 `Rectangle` 对象，使用一个 `Point` 作为左上角的位置。

```auto
let corner = Point(30.0, 20.0)
let box = Rectangle(100.0, 50.0, corner)
print(box)  // Rectangle(100, 50, Point(30, 20))
```

## 修改矩形

现在让我们考虑两个修改矩形的方法：`grow` 和 `translate`。

`grow` 接受两个数字 `dwidth` 和 `dheight`，并将它们加到矩形的 `width` 和 `height` 属性上。

```auto
fn grow(&self, dwidth: float, dheight: float) {
    self.width += dwidth
    self.height += dheight
}
```

`translate` 接受两个数字 `dx` 和 `dy`，并将矩形在 `x` 和 `y` 方向上移动给定的距离。

```auto
fn translate(&self, dx: float, dy: float) {
    self.corner.translate(dx, dy)
}
```

## 深拷贝

当我们使用 `copy` 复制一个 `Rectangle` 时，它复制了 `Rectangle` 对象，但没有复制它包含的 `Point` 对象。因此两个 `Rectangle` 对象是不同的，如预期的那样，但它们的 `corner` 属性指向同一个对象。

```auto
let box2 = copy(box1)
print(box1 is box2)                  // false
print(box1.corner is box2.corner)    // true (共享！)
```

`copy` 所做的称为**浅拷贝**（shallow copy），因为它复制了对象但没有复制它包含的对象。结果是，改变一个 `Rectangle` 的 `width` 或 `height` 不会影响另一个，但改变共享的 `Point` 的属性会影响两者！

这种行为令人困惑且容易出错。例如，如果我们平移 `box2`，两个矩形似乎都移动了：

```auto
box2.translate(30.0, 20.0)
print(box1)  // Rectangle(100, 50, Point(60, 40))  <-- bug!
```

幸运的是，Auto 提供了 `deepcopy`，它不仅复制对象，还复制它引用的对象，以及这些对象引用的对象，以此类推。这种操作称为**深拷贝**（deep copy）。

```auto
let box4 = deepcopy(box3)
print(box3.corner is box4.corner)  // false (独立的！)
```

因为 `box3` 和 `box4` 是完全独立的对象，我们可以修改一个而不影响另一个。

<Listing number="16-2" file-name="rectangle_deepcopy.auto" caption="带有浅拷贝和深拷贝的 Rectangle 类">

```auto
type Point {
    x: float,
    y: float,
}

fn init(&self, x: float = 0.0, y: float = 0.0) {
    self.x = x
    self.y = y
}

fn to_string(&self) -> str {
    return f"Point(${self.x}, ${self.y})"
}

fn __eq__(&self, other: Point) -> bool {
    return self.x == other.x and self.y == other.y
}

fn translate(&self, dx: float, dy: float) {
    self.x += dx
    self.y += dy
}

type Rectangle {
    width: float,
    height: float,
    corner: Point,
}

fn init(&self, width: float, height: float, corner: Point) {
    self.width = width
    self.height = height
    self.corner = corner
}

fn to_string(&self) -> str {
    return f"Rectangle(${self.width}, ${self.height}, ${self.corner})"
}

fn grow(&self, dwidth: float, dheight: float) {
    self.width += dwidth
    self.height += dheight
}

fn translate(&self, dx: float, dy: float) {
    self.corner.translate(dx, dy)
}

fn main() {
    // 使用 Point 作为角创建 Rectangle
    let corner = Point(30.0, 20.0)
    let box1 = Rectangle(100.0, 50.0, corner)
    print(box1)  // Rectangle(100, 50, Point(30, 20))

    // 浅拷贝 -- corner 被共享
    let box2 = copy(box1)
    print(box1 is box2)          // false
    print(box1.corner is box2.corner)  // true (共享！)

    // 增长 box2 不影响 box1
    box2.grow(60.0, 40.0)
    print(box1)  // Rectangle(100, 50, Point(30, 20))
    print(box2)  // Rectangle(160, 90, Point(30, 20))

    // 平移 box2 会移动其 corner，这个 corner 与 box1 共享！
    box2.translate(30.0, 20.0)
    print(box1)  // Rectangle(100, 50, Point(60, 40))  <-- bug!
    print(box2)  // Rectangle(160, 90, Point(60, 40))

    // 深拷贝 -- corner 是独立的
    let corner2 = Point(20.0, 20.0)
    let box3 = Rectangle(100.0, 50.0, corner2)
    let box4 = deepcopy(box3)
    print(box3.corner is box4.corner)  // false (独立的！)

    box3.translate(50.0, 30.0)
    box4.grow(100.0, 60.0)
    print(box3)  // Rectangle(100, 50, Point(70, 50))
    print(box4)  // Rectangle(200, 110, Point(20, 20))
}
```

```python
from copy import copy, deepcopy


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy


class Rectangle:
    def __init__(self, width, height, corner):
        self.width = width
        self.height = height
        self.corner = corner

    def __str__(self):
        return f"Rectangle({self.width}, {self.height}, {self.corner})"

    def grow(self, dwidth, dheight):
        self.width += dwidth
        self.height += dheight

    def translate(self, dx, dy):
        self.corner.translate(dx, dy)


def main():
    # 使用 Point 作为角创建 Rectangle
    corner = Point(30.0, 20.0)
    box1 = Rectangle(100.0, 50.0, corner)
    print(box1)  # Rectangle(100.0, 50.0, Point(30.0, 20.0))

    # 浅拷贝 -- corner 被共享
    box2 = copy(box1)
    print(box1 is box2)                  # False
    print(box1.corner is box2.corner)    # True (共享！)

    # 增长 box2 不影响 box1
    box2.grow(60.0, 40.0)
    print(box1)  # Rectangle(100.0, 50.0, Point(30.0, 20.0))
    print(box2)  # Rectangle(160.0, 90.0, Point(30.0, 20.0))

    # 平移 box2 会移动其 corner，这个 corner 与 box1 共享！
    box2.translate(30.0, 20.0)
    print(box1)  # Rectangle(100.0, 50.0, Point(60.0, 40.0))  <-- bug!
    print(box2)  # Rectangle(160.0, 90.0, Point(60.0, 40.0))

    # 深拷贝 -- corner 是独立的
    corner2 = Point(20.0, 20.0)
    box3 = Rectangle(100.0, 50.0, corner2)
    box4 = deepcopy(box3)
    print(box3.corner is box4.corner)    # False (独立的！)

    box3.translate(50.0, 30.0)
    box4.grow(100.0, 60.0)
    print(box3)  # Rectangle(100.0, 50.0, Point(70.0, 50.0))
    print(box4)  # Rectangle(200.0, 110.0, Point(20.0, 20.0))


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

`Rectangle` 类型演示了与 `Point` 的组合。`grow` 方法改变宽度和高度，而 `translate` 委托给 `Point` 的 `translate` 方法。关键的教训是 `copy`（浅拷贝）和 `deepcopy` 之间的区别：浅拷贝共享嵌套对象，因此修改共享的 `Point` 会影响两个矩形。深拷贝创建所有嵌套对象的独立副本，使两个矩形完全分离。

## 多态

在前面的例子中，我们使用了 `Line` 和 `Rectangle` 对象。我们可以做更有趣的事情：创建一个包含不同类型对象的列表，这些对象都提供一个 `draw` 方法，然后遍历列表并在每个对象上调用 `draw`。

```auto
let shapes = [line1, line2, box3, box4]

for shape in shapes {
    shape.draw()
}
```

第一次和第二次循环时，`shape` 引用一个 `Line` 对象，所以当 `draw` 被调用时，运行的是 `Line` 类中定义的方法。

第三次和第四次循环时，`shape` 引用一个 `Rectangle` 对象，所以当 `draw` 被调用时，运行的是 `Rectangle` 类中定义的方法。

在某种意义上，每个对象知道如何绘制自己。这个特性称为**多态**（polymorphism）。这个词来自希腊语，意为"多种形态"。在面向对象编程中，多态是不同类型提供相同方法的能力，这使得可以通过在不同类型的对象上调用相同的方法来执行许多计算（如绘制形状）。

<Listing number="16-3" file-name="polymorphism_shapes.auto" caption="多态：不同类型，相同接口">

```auto
type Point {
    x: float,
    y: float,
}

fn init(&self, x: float = 0.0, y: float = 0.0) {
    self.x = x
    self.y = y
}

fn to_string(&self) -> str {
    return f"Point(${self.x}, ${self.y})"
}

type Line {
    p1: Point,
    p2: Point,
}

fn init(&self, p1: Point, p2: Point) {
    self.p1 = p1
    self.p2 = p2
}

fn to_string(&self) -> str {
    return f"Line(${self.p1}, ${self.p2})"
}

fn draw(&self) {
    print(f"Drawing line from (${self.p1.x}, ${self.p1.y}) to (${self.p2.x}, ${self.p2.y})")
}

type Rectangle {
    width: float,
    height: float,
    corner: Point,
}

fn init(&self, width: float, height: float, corner: Point) {
    self.width = width
    self.height = height
    self.corner = corner
}

fn to_string(&self) -> str {
    return f"Rectangle(${self.width}, ${self.height}, ${self.corner})"
}

fn draw(&self) {
    let p1 = self.corner
    let p2 = Point(self.corner.x + self.width, self.corner.y)
    let p3 = Point(self.corner.x + self.width, self.corner.y + self.height)
    let p4 = Point(self.corner.x, self.corner.y + self.height)
    print(f"Drawing rectangle with corners (${p1.x},${p1.y}), (${p2.x},${p2.y}), (${p3.x},${p3.y}), (${p4.x},${p4.y})")
}

type Circle {
    center: Point,
    radius: float,
}

fn init(&self, center: Point, radius: float) {
    self.center = center
    self.radius = radius
}

fn to_string(&self) -> str {
    return f"Circle(center=${self.center}, radius=${self.radius})"
}

fn draw(&self) {
    print(f"Drawing circle at (${self.center.x}, ${self.center.y}) with radius ${self.radius}")
}

fn draw_shapes(shapes: list) {
    for shape in shapes {
        shape.draw()
    }
}

fn main() {
    let origin = Point(0.0, 0.0)
    let line1 = Line(origin, Point(300.0, 0.0))
    let line2 = Line(origin, Point(0.0, 150.0))
    let rect = Rectangle(100.0, 50.0, Point(30.0, 20.0))
    let circle = Circle(Point(80.0, 45.0), 25.0)

    // 多态：相同接口，不同类型
    let shapes = [line1, line2, rect, circle]
    draw_shapes(shapes)
    // Drawing line from (0, 0) to (300, 0)
    // Drawing line from (0, 0) to (0, 150)
    // Drawing rectangle with corners (30,20), (130,20), (130,70), (30,70)
    // Drawing circle at (80, 45) with radius 25
}
```

```python
class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point({self.x}, {self.y})"


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return f"Line({self.p1}, {self.p2})"

    def draw(self):
        print(f"Drawing line from ({self.p1.x}, {self.p1.y}) to ({self.p2.x}, {self.p2.y})")


class Rectangle:
    def __init__(self, width, height, corner):
        self.width = width
        self.height = height
        self.corner = corner

    def __str__(self):
        return f"Rectangle({self.width}, {self.height}, {self.corner})"

    def draw(self):
        p1 = self.corner
        p2 = Point(self.corner.x + self.width, self.corner.y)
        p3 = Point(self.corner.x + self.width, self.corner.y + self.height)
        p4 = Point(self.corner.x, self.corner.y + self.height)
        print(f"Drawing rectangle with corners ({p1.x},{p1.y}), ({p2.x},{p2.y}), ({p3.x},{p3.y}), ({p4.x},{p4.y})")


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def __str__(self):
        return f"Circle(center={self.center}, radius={self.radius})"

    def draw(self):
        print(f"Drawing circle at ({self.center.x}, {self.center.y}) with radius {self.radius}")


def draw_shapes(shapes):
    for shape in shapes:
        shape.draw()


def main():
    origin = Point(0.0, 0.0)
    line1 = Line(origin, Point(300.0, 0.0))
    line2 = Line(origin, Point(0.0, 150.0))
    rect = Rectangle(100.0, 50.0, Point(30.0, 20.0))
    circle = Circle(Point(80.0, 45.0), 25.0)

    # 多态：相同接口，不同类型
    shapes = [line1, line2, rect, circle]
    draw_shapes(shapes)
    # Drawing line from (0.0, 0.0) to (300.0, 0.0)
    # Drawing line from (0.0, 0.0) to (0.0, 150.0)
    # Drawing rectangle with corners (30.0,20.0), (130.0,20.0), (130.0,70.0), (30.0,70.0)
    # Drawing circle at (80.0, 45.0) with radius 25.0


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

通过将 `Line`、`Rectangle` 和 `Circle` 对象放入一个列表并在每个对象上调用 `draw()` 来演示多态。即使对象是不同的类型，它们都提供 `draw` 方法。当在循环中调用 `shape.draw()` 时，Auto 根据对象的实际类型分派到正确的方法。`draw_shapes` 函数不需要知道列表中有什么类型 -- 它只调用 `draw()`，每个对象处理自己的绘制。

> **Python 程序员注意：**
>
> Auto 的多态与 Python 的工作方式相同。两种语言都使用动态分派，在运行时根据对象的类型调用正确的方法。

## 调试

在本章中，我们遇到了一个微妙的 bug，因为我们创建了一个被两个 `Rectangle` 对象共享的 `Point`，然后修改了这个 `Point`。

一般来说，有两种方法可以避免这类问题：你可以避免共享对象，或者避免修改它们。

要避免共享对象，可以使用深拷贝，正如我们在本章中所做的那样。

要避免修改对象，可以考虑用创建新对象的纯函数替换像 `translate` 这样的非纯函数。例如，下面是一个 `translated` 版本，它创建一个新的 `Point` 而不修改其属性。

```auto
fn translated(&self, dx: float = 0.0, dy: float = 0.0) -> Point {
    return Point(self.x + dx, self.y + dy)
}
```

创建一个新对象比修改现有对象需要更多时间，但这种差异在实践中很少重要。避免共享对象和非纯函数的程序通常更容易开发、测试和调试 -- 而最好的调试是你不需要做的调试。

## 术语表

**浅拷贝：**
不复制嵌套对象的拷贝操作。

**深拷贝：**
同时复制嵌套对象的拷贝操作。

**组合：**
定义一个包含其他类型对象作为字段的能力。

**多态：**
方法或运算符处理多种类型对象的能力。

## 练习

### 练习

为 `Line` 类编写一个 `__eq__` 方法，如果 `Line` 对象引用等价的 `Point` 对象（顺序不限），则返回 `true`。

### 练习

编写一个名为 `midpoint` 的 `Line` 方法，计算线段的中点并将结果作为 `Point` 对象返回。

### 练习

编写一个名为 `midpoint` 的 `Rectangle` 方法，找到矩形中心的点并将结果作为 `Point` 对象返回。

### 练习

编写一个名为 `Circle` 的类定义，具有属性 `center` 和 `radius`，其中 `center` 是 Point 对象，`radius` 是一个数字。包含 `init`、`to_string` 和 `draw` 方法。然后通过将 `Circle` 添加到形状列表中并全部绘制来演示多态。
