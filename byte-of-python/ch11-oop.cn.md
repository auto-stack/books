# 面向对象编程

在迄今为止我们编写的所有程序中，我们的程序设计都是围绕函数展开的，即操作数据的语句块。这被称为_面向过程_的编程方式。还有一种组织程序的方式，即将数据和功能组合在一起，包装在被称为"对象"的东西中。这就是_面向对象_的编程范式。大多数时候你可以使用面向过程编程，但在编写大型程序或遇到更适合此方法的问题时，可以使用面向对象编程技术。

类和对象是面向对象编程的两个主要方面。**类**创建了一种新的_类型_，而**对象**是该类的_实例_。打个比方，你可以有 `int` 类型的变量，这意味着存储整数的变量是 `int` 类的实例（对象）。

> **静态语言程序员注意**
>
> 请注意，即使是整数也被当作对象（`int` 类的对象）来处理。这与 C++ 和 Java（1.5 版之前）中整数是原始基本类型不同。
>
> 参见 `help(int)` 了解该类的更多详细信息。
>
> C# 和 Java 1.5 程序员会发现这与_装箱和拆箱_概念类似。

对象可以使用属于对象的普通变量来存储数据。属于对象或类的变量被称为**字段**。对象还可以通过使用属于类的函数来具有功能。此类函数被称为该类的**方法**。这个术语很重要，因为它帮助我们区分独立的函数和变量与属于类或对象的函数和变量。字段和方法统称为该类的**属性**。

字段有两种类型——它们可以属于类的每个实例/对象，也可以属于类本身。它们分别被称为**实例变量**和**类变量**。

在 Auto 中，类使用 `type` 关键字创建。类的字段和方法列在由 `{}` 包围的块中。

## `&self` 参数

类方法与普通函数只有一个特定的区别——它们必须在参数列表的开头添加一个额外的第一个参数，但在调用方法时你**不需要**为这个参数提供值，`a2p` 转译器（通过 Python）会自动提供它。在 Auto 中，这个特殊参数写为 `&self`，它引用对象_本身_。

虽然你可以想象给这个参数取任何名称，但 Auto 使用了受 Rust 启发的 `&self` 约定，这可以立即清楚地表明这是对当前实例的引用。这是一个经过深思熟虑的设计选择，使 Auto 区别于 Python 的 `self` 约定，同时保持相同的底层语义。

> **C++/Java/C# 程序员注意**
>
> Auto 中的 `&self`（等同于 Python 的 `self`）在概念上类似于 C++ 中的 `this` 指针以及 Java 和 C# 中的 `this` 引用。

你可能想知道 Python 如何为 `self` 提供值，以及为什么你不需要为它提供值。一个例子会让这一切变得清晰。假设你有一个名为 `MyClass` 的类和该类的一个名为 `myobject` 的实例。当你以 `myobject.method(arg1, arg2)` 的方式调用该对象的方法时，Python 会自动将其转换为 `MyClass.method(myobject, arg1, arg2)` ——这就是 `self` 的全部含义。

这也意味着如果你有一个不需要任何参数的方法，你仍然需要一个参数——`&self`。

> **Python 程序员注意：**
>
> 在 Python 中，`self` 参数是一个命名约定（虽然强烈推荐）。在 Auto 中，`&self` 是方法接收器的语言关键字。`&` 前缀表示该方法接收对实例的引用，反映了 Rust 的借用语义。`a2p` 转译器会将 `&self` 转换为生成的 Python 代码中的 `self`。

## 类

最简单的类如下例所示（保存为 `oop_simplestclass.at`）：

<Listing number="11-1" file-name="oop_simplestclass.auto" caption="创建一个类">

```auto
type Person {}

fn main() {
    let p = Person{}
    print(p)
}
```

```python
class Person:
    pass


def main():
    p = Person()
    print(p)


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ a2p oop_simplestclass.at && python oop_simplestclass.py
<__main__.Person object at 0x...>
```

**工作原理**

我们使用 `type` 语句和类名创建一个新类。后面跟着由 `{}` 包围的块，构成类的主体。在本例中，我们有一个空块。`a2p` 转译器将其转换为 Python 类，以 `pass` 语句作为类体。

接下来，我们使用类名后跟 `{}` 来创建该类的对象/实例。（我们将在[下一节](#init-方法)学习更多关于实例化的内容）。为了验证，我们只需打印该变量来确认其类型。它告诉我们有一个 `__main__` 模块中 `Person` 类的实例。

请注意，对象的计算机内存存储地址也会被打印出来。你的计算机上的地址值会有所不同，因为 Python 可以在找到空间的任何地方存储对象。

> **Python 程序员注意：**
>
> Auto 使用 `type` 代替 Python 的 `class` 关键字。空的 `type Person {}` 等同于 `class Person: pass`。`a2p` 转译器会自动处理此转换。对象使用 `Person{}` 创建，而不是 `Person()`。

## 方法

我们已经讨论过类/对象可以拥有方法，就像函数一样，只是多了一个额外的 `&self` 参数。我们现在来看一个例子（保存为 `oop_method.at`）：

<Listing number="11-2" file-name="oop_method.auto" caption="使用对象方法">

```auto
type Person {
    fn say_hi(&self) {
        print("Hello, how are you?")
    }
}

fn main() {
    let p = Person{}
    p.say_hi()
}
```

```python
class Person:
    def say_hi(self):
        print('Hello, how are you?')


def main():
    p = Person()
    p.say_hi()


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ a2p oop_method.at && python oop_method.py
Hello, how are you?
```

**工作原理**

在这里我们看到了 `&self` 的实际作用。请注意，`say_hi` 方法不接收任何参数，但在函数定义中仍然有 `&self`。`a2p` 转译器将 `fn say_hi(&self)` 转换为 `def say_hi(self)`，方法的调用方式与 Python 中完全相同：`p.say_hi()`。

## `init` 方法

Python 类中有许多具有特殊意义的方法名。现在我们将了解 `__init__` 方法的意义，以及 Auto 如何处理它。

在 Auto 中，构造方法使用 `fn init(&self, ...)` 定义。`a2p` 转译器将其转换为 Python 的 `__init__` 方法。当类的对象被实例化（即创建）时，`init` 方法会立即运行。该方法用于对你想要对对象执行的任何*初始化*操作（即向对象传递初始值）非常有用。

示例（保存为 `oop_init.at`）：

<Listing number="11-3" file-name="oop_init.auto" caption="使用 init 方法">

```auto
type Person {
    name: str

    fn init(&self, name: str) {
        .name = name
    }

    fn say_hi(&self) {
        print("Hello, my name is", .name)
    }
}

fn main() {
    let p = Person{"Swaroop"}
    p.say_hi()
}
```

```python
class Person:
    def __init__(self, name):
        self.name = name

    def say_hi(self):
        print('Hello, my name is', self.name)


def main():
    p = Person('Swaroop')
    p.say_hi()


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ a2p oop_init.at && python oop_init.py
Hello, my name is Swaroop
```

**工作原理**

在这里，我们定义 `init` 方法接收一个参数 `name`（以及通常的 `&self`）。我们在 `type` 块的顶部声明了一个字段 `name: str`。在 `init` 内部，我们使用 `.name = name` 将参数赋值给字段。请注意，虽然它们都叫做 'name'，但这是两个不同的变量。这不会造成问题，因为 `.name` 表示属于对象的一部分（即 `self.name`），而另一个 `name` 是一个局部参数。

当创建 `Person` 类型的新实例 `p` 时，我们使用类型名后跟 `{}` 中的参数：`p = Person{"Swaroop"}`。`a2p` 转译器将 `Person{"Swaroop"}` 转换为生成的 Python 代码中的 `Person('Swaroop')`。

我们不需要显式调用 `init` 方法。这就是这个方法的特殊意义。

现在，我们可以在方法中使用 `.name` 字段（在 Python 中变为 `self.name`），如 `say_hi` 方法所示。

> **Python 程序员注意：**
>
> Auto 使用 `fn init(&self, ...)` 代替 Python 的 `def __init__(self, ...)`。在方法内部，`.field = value` 等同于 `self.field = value`。`a2p` 转译器将 `fn init` 转换为 `def __init__`，将 `.field` 引用转换为 `self.field`。在 `type` 块顶部声明的字段（如 `name: str`）会成为在 `__init__` 中初始化的实例变量。

## 类变量与对象变量

我们已经讨论了类和对象的功能部分（即方法），现在让我们学习数据部分。数据部分，即字段，不过是被_绑定_到类和对象的**命名空间**的普通变量。这意味着这些名称仅在类和对象的上下文中有效。这就是为什么它们被称为_命名空间_。

有两种类型的_字段_——类变量和对象变量，根据变量分别是由类还是由对象_拥有_来分类。

**类变量**是共享的——它们可以被该类的所有实例访问。类变量只有一个副本，当任何一个对象修改类变量时，所有其他实例都会看到这个修改。

**对象变量**由类的每个单独对象/实例拥有。在这种情况下，每个对象都有自己的字段副本，即它们不共享，与不同实例中同名字段没有任何关系。

让我们先看一个对象变量的简单例子（保存为 `oop_objvar.at`）：

<Listing number="11-4" file-name="oop_objvar.auto" caption="使用对象变量">

```auto
type Robot {
    name: str

    fn init(&self, name: str) {
        .name = name
        print(f"(Initializing $.name)")
    }

    fn say_hi(&self) {
        print(f"Greetings, my masters call me $.name.")
    }

    fn die(&self) {
        print(f"$.name is being destroyed!")
    }
}

fn main() {
    let droid1 = Robot{"R2-D2"}
    droid1.say_hi()

    let droid2 = Robot{"C-3PO"}
    droid2.say_hi()

    print("\nRobots can do some work here.\n")

    print("Robots have finished their work. So let's destroy them.")
    droid1.die()
    droid2.die()
}
```

```python
class Robot:
    def __init__(self, name):
        self.name = name
        print(f'(Initializing {self.name})')

    def say_hi(self):
        print(f'Greetings, my masters call me {self.name}.')

    def die(self):
        print(f'{self.name} is being destroyed!')


def main():
    droid1 = Robot('R2-D2')
    droid1.say_hi()

    droid2 = Robot('C-3PO')
    droid2.say_hi()

    print('\nRobots can do some work here.\n')

    print("Robots have finished their work. So let's destroy them.")
    droid1.die()
    droid2.die()


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ a2p oop_objvar.at && python oop_objvar.py
(Initializing R2-D2)
Greetings, my masters call me R2-D2.
(Initializing C-3PO)
Greetings, my masters call me C-3PO.

Robots can do some work here.

Robots have finished their work. So let's destroy them.
R2-D2 is being destroyed!
C-3PO is being destroyed!
```

**工作原理**

在这个例子中，`name` 字段属于每个单独的对象（它在 `init` 方法内部使用 `.name` 赋值），所以每个 `Robot` 实例都有自己的 `name` 副本。方法内部的 `.name` 表示法等同于 Python 中的 `self.name`。这是一个**对象变量**（也称为实例变量）。

现在让我们添加一个**类变量**来跟踪机器人数量（保存为 `oop_classvar.at`）：

<Listing number="11-5" file-name="oop_classvar.auto" caption="类变量与对象变量">

```auto
type Robot {
    population: int = 0

    name: str

    fn init(&self, name: str) {
        .name = name
        print(f"(Initializing $.name)")
        Robot.population += 1
    }

    fn die(&self) {
        print(f"$.name is being destroyed!")
        Robot.population -= 1
        if Robot.population == 0 {
            print(f"$.name was the last one.")
        } else {
            print(f"There are still {Robot.population} robots working.")
        }
    }

    fn say_hi(&self) {
        print(f"Greetings, my masters call me $.name.")
    }

    fn how_many() {
        print(f"We have {Robot.population} robots.")
    }
}

fn main() {
    let droid1 = Robot{"R2-D2"}
    droid1.say_hi()
    Robot.how_many()

    let droid2 = Robot{"C-3PO"}
    droid2.say_hi()
    Robot.how_many()

    print("\nRobots can do some work here.\n")

    print("Robots have finished their work. So let's destroy them.")
    droid1.die()
    droid2.die()

    Robot.how_many()
}
```

```python
class Robot:
    population = 0

    def __init__(self, name):
        self.name = name
        print(f'(Initializing {self.name})')
        Robot.population += 1

    def die(self):
        print(f'{self.name} is being destroyed!')
        Robot.population -= 1
        if Robot.population == 0:
            print(f'{self.name} was the last one.')
        else:
            print(f'There are still {Robot.population} robots working.')

    def say_hi(self):
        print(f'Greetings, my masters call me {self.name}.')

    @classmethod
    def how_many(cls):
        print(f'We have {cls.population} robots.')


def main():
    droid1 = Robot('R2-D2')
    droid1.say_hi()
    Robot.how_many()

    droid2 = Robot('C-3PO')
    droid2.say_hi()
    Robot.how_many()

    print('\nRobots can do some work here.\n')

    print("Robots have finished their work. So let's destroy them.")
    droid1.die()
    droid2.die()

    Robot.how_many()


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ a2p oop_classvar.at && python oop_classvar.py
(Initializing R2-D2)
Greetings, my masters call me R2-D2.
We have 1 robots.
(Initializing C-3PO)
Greetings, my masters call me C-3PO.
We have 2 robots.

Robots can do some work here.

Robots have finished their work. So let's destroy them.
R2-D2 is being destroyed!
There are still 1 robots working.
C-3PO is being destroyed!
C-3PO was the last one.
We have 0 robots.
```

**工作原理**

这是一个较长的例子，但有助于演示类变量和对象变量的本质。在这里，`population` 在 `Robot` 类型的顶部声明为一个字段，默认值为 `0`。由于它使用 `Robot.population`（类型名，而不是 `.population`）来引用，因此它是一个由所有实例共享的**类变量**。`name` 变量属于对象（它使用 `.name` 赋值），因此是**对象变量**。

因此，我们将 `population` 类变量称为 `Robot.population`，而不是 `.population`。我们在该对象的方法中使用 `.name` 表示法来引用对象变量 `name`。请记住类变量和对象变量之间的这个简单区别。还要注意，与类变量同名的对象变量会隐藏类变量！

除了使用 `Robot.population`，我们也可以使用 `self.__class__.population`，因为每个对象都通过 `self.__class__` 属性引用其类。

`how_many` 方法不接收 `&self` 作为参数，这意味着它不是一个实例方法。在 Python 中，这变成了一个 `@classmethod`。它属于类，不属于任何单独的对象。

请注意，`init` 方法用于用名称初始化 `Robot` 实例。在此方法中，我们将 `Robot.population` 计数增加 1，因为又增加了一个机器人。还要注意 `.name` 的值特定于每个对象，这表明了对象变量的性质。

请记住，你必须仅使用 `.field` 表示法来引用同一对象的变量和方法。这被称为*属性引用*。

在 `die` 方法中，我们只是将 `Robot.population` 计数减少 1。

> **Python 程序员注意：**
>
> 在 Auto 中，类变量在 `type` 块的顶部声明为带有默认值的字段（例如 `population: int = 0`）。`a2p` 转译器识别到这些不是通过 `init` 中的 `.field = value` 赋值的，并将它们放置为 Python 输出中的类级属性。没有 `&self` 的方法（如 `fn how_many()`）会被转换为带有 `cls` 参数的 `@classmethod`。

## 继承

面向对象编程的主要好处之一是代码的**复用**，实现这一目标的方式之一是通过**继承**机制。继承最好被理解为在类之间实现一种**类型与子类型**的关系。

假设你想编写一个程序来跟踪学院中的教师和学生。他们有一些共同特征，如姓名、年龄和地址。他们也有特定特征，如教师的薪资、课程和假期，以及学生的成绩和费用。

你可以为每种类型创建两个独立的类来处理它们，但添加一个新的共同特征意味着要添加到这两个独立的类中。这很快就会变得难以管理。

更好的方法是创建一个名为 `SchoolMember` 的公共类，然后让教师和学生类_继承_这个类，即它们将成为该类型的子类型，然后我们可以为这些子类型添加特定特征。

这种方法有很多优点。如果我们添加/更改 `SchoolMember` 中的任何功能，这也会自动反映在子类型中。例如，你可以通过简单地将 ID 卡字段添加到 SchoolMember 类中，为教师和学生添加新的 ID 卡字段。但是，子类型中的更改不会影响其他子类型。另一个优点是你可以将教师或学生对象作为 `SchoolMember` 对象来引用，这在某些情况下可能很有用，例如计算学校成员的数量。这就是**多态**——子类型可以在任何需要父类型的情况下被替换，即对象可以被视为父类的实例。

还要注意，我们复用了父类的代码，不需要像使用独立类时那样在不同的类中重复它。

在这种情况下的 `SchoolMember` 类被称为**基类**或**超类**。`Teacher` 和 `Student` 类被称为**派生类**或**子类**。

在 Auto 中，继承使用类型名后面的冒号表示：`type Sub: Super {}`。`a2p` 转译器将其转换为 Python 中的 `class Sub(Super):`。

我们现在将此示例作为一个程序来看（保存为 `oop_subclass.at`）：

<Listing number="11-6" file-name="oop_subclass.auto" caption="继承">

```auto
type SchoolMember {
    name: str
    age: int

    fn init(&self, name: str, age: int) {
        .name = name
        .age = age
        print(f"(Initialized SchoolMember: $.name)")
    }

    fn tell(&self) {
        print(f"Name:\"$.name\" Age:\"$.age\"", end = " ")
    }
}

type Teacher: SchoolMember {
    salary: int

    fn init(&self, name: str, age: int, salary: int) {
        SchoolMember.init(self, name, age)
        .salary = salary
        print(f"(Initialized Teacher: $.name)")
    }

    fn tell(&self) {
        SchoolMember.tell(self)
        print(f"Salary: \"$.salary\"")
    }
}

type Student: SchoolMember {
    marks: int

    fn init(&self, name: str, age: int, marks: int) {
        SchoolMember.init(self, name, age)
        .marks = marks
        print(f"(Initialized Student: $.name)")
    }

    fn tell(&self) {
        SchoolMember.tell(self)
        print(f"Marks: \"$.marks\"")
    }
}

fn main() {
    let t = Teacher{"Mrs. Shrividya", 40, 30000}
    let s = Student{"Swaroop", 25, 75}

    // 打印一个空行
    print()

    let members = [t, s]
    for member in members {
        // 适用于教师和学生
        member.tell()
    }
}
```

```python
class SchoolMember:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print(f'(Initialized SchoolMember: {self.name})')

    def tell(self):
        print(f'Name:"{self.name}" Age:"{self.age}"', end=" ")


class Teacher(SchoolMember):
    def __init__(self, name, age, salary):
        SchoolMember.__init__(self, name, age)
        self.salary = salary
        print(f'(Initialized Teacher: {self.name})')

    def tell(self):
        SchoolMember.tell(self)
        print(f'Salary: "{self.salary}"')


class Student(SchoolMember):
    def __init__(self, name, age, marks):
        SchoolMember.__init__(self, name, age)
        self.marks = marks
        print(f'(Initialized Student: {self.name})')

    def tell(self):
        SchoolMember.tell(self)
        print(f'Marks: "{self.marks}"')


def main():
    t = Teacher('Mrs. Shrividya', 40, 30000)
    s = Student('Swaroop', 25, 75)

    # 打印一个空行
    print()

    members = [t, s]
    for member in members:
        # 适用于教师和学生
        member.tell()


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ a2p oop_subclass.at && python oop_subclass.py
(Initialized SchoolMember: Mrs. Shrividya)
(Initialized Teacher: Mrs. Shrividya)
(Initialized SchoolMember: Swaroop)
(Initialized Student: Swaroop)

Name:"Mrs. Shrividya" Age:"40" Salary: "30000"
Name:"Swaroop" Age:"25" Marks: "75"
```

**工作原理**

要使用继承，我们在类型定义中类型名后面的冒号后指定基类名（例如 `type Teacher: SchoolMember`）。`a2p` 转译器将其转换为 `class Teacher(SchoolMember):`。

接下来，我们观察到基类的 `init` 方法使用 `SchoolMember.init(self, name, age)` 显式调用，以便我们可以在子类中初始化实例的基类部分。这非常重要——由于我们在 `Teacher` 和 `Student` 子类中定义了 `init` 方法，转译器（与 Python 一样）不会自动调用基类 `SchoolMember` 的构造函数，你必须自己显式调用它。

相比之下，如果我们在子类中没有定义 `init` 方法，则会自动调用基类构造函数。

虽然我们可以像对待 `SchoolMember` 实例一样对待 `Teacher` 或 `Student` 的实例，并访问 `SchoolMember` 的 `tell` 方法，但我们在每个子类中定义了另一个 `tell` 方法（使用 `SchoolMember` 的 `tell` 方法的一部分）来为该子类量身定制。因为我们这样做了，当我们在循环中调用 `member.tell()` 时，会使用该子类对应的正确 `tell` 方法，而不是超类的方法。但是，如果我们在子类中没有 `tell` 方法，则会使用超类中的 `tell` 方法。Python 总是先在实际的子类型中查找方法，如果没有找到，则按类定义中指定的顺序依次查找子类的基类中的方法。

超类 `tell()` 方法中的 `print` 函数使用了 `end` 参数来打印一行并允许下一个 `print` 继续在同一行上。这是一个使 `print` 不在打印末尾输出 `\n`（换行符）的技巧。

> **Python 程序员注意：**
>
> Auto 使用 `type Sub: Super {}` 表示继承，代替 Python 的 `class Sub(Super):`。基类构造函数被显式调用为 `Super.init(self, ...)`，代替 `Super.__init__(self, ...)`。`a2p` 转译器将 `Super.init(self, ...)` 转换为生成的 Python 代码中的 `Super.__init__(self, ...)`。类似地，调用父方法如 `SchoolMember.tell(self)` 在 Python 中被转换为 `SchoolMember.tell(self)`。

## 方法重写与多态

在前面的例子中，我们看到 `Teacher` 和 `Student` 都定义了自己的 `tell` 方法，这重写了 `SchoolMember` 中的 `tell` 方法。这被称为**方法重写**。当我们遍历 `SchoolMember` 对象列表并在每个对象上调用 `tell` 时，会根据对象的实际类型调用适当的版本——这就是**多态**的实际体现。

让我们看一个专注于这个概念的更简单的例子（保存为 `oop_polymorphism.at`）：

<Listing number="11-7" file-name="oop_polymorphism.auto" caption="方法重写与多态">

```auto
type Animal {
    name: str

    fn init(&self, name: str) {
        .name = name
    }

    fn speak(&self) {
        print(f"$.name makes a sound")
    }
}

type Dog: Animal {
    fn speak(&self) {
        print(f"$.name says Woof!")
    }
}

type Cat: Animal {
    fn speak(&self) {
        print(f"$.name says Meow!")
    }
}

fn main() {
    let animals = [Dog{"Rex"}, Cat{"Whiskers"}, Animal("Creature")]
    for animal in animals {
        animal.speak()
    }
}
```

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f'{self.name} makes a sound')


class Dog(Animal):
    def speak(self):
        print(f'{self.name} says Woof!')


class Cat(Animal):
    def speak(self):
        print(f'{self.name} says Meow!')


def main():
    animals = [Dog('Rex'), Cat('Whiskers'), Animal('Creature')]
    for animal in animals:
        animal.speak()


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ a2p oop_polymorphism.at && python oop_polymorphism.py
Rex says Woof!
Whiskers says Meow!
Creature makes a sound
```

**工作原理**

我们定义了一个基类型 `Animal`，带有一个 `speak` 方法，提供默认行为。然后我们创建了两个子类型：`Dog` 和 `Cat`，它们都用各自的实现重写了 `speak` 方法。

在 `main` 中，我们创建了一个包含 `Dog`、`Cat` 和普通 `Animal` 的列表。当我们遍历列表并在每个对象上调用 `animal.speak()` 时，Python 的方法解析顺序确保为每个对象调用正确版本的 `speak`：
- 对于 `Dog` 实例，调用 `Dog.speak`，打印 "Woof!"
- 对于 `Cat` 实例，调用 `Cat.speak`，打印 "Meow!"
- 对于普通的 `Animal` 实例，调用 `Animal.speak`，打印默认声音

这就是多态：相同的方法调用（`speak`）根据对象的实际类型产生不同的行为。这使得我们的代码具有可扩展性——我们可以添加新的动物类型（如 `Bird`、`Fish` 等），而无需更改调用 `speak` 的循环。

> **Python 程序员注意：**
>
> Auto 中的方法重写与 Python 完全相同。如果子类型定义了一个与基类型方法同名的方法，子类型的版本将覆盖基类型的版本。`a2p` 转译器生成标准的 Python 继承，因此 Python 的所有方法解析顺序（MRO）规则都适用于生成的代码。

## 总结

我们现在已经探索了类和对象的各个方面以及与之相关的各种术语。我们也看到了面向对象编程的好处和陷阱。Auto 为 OOP 提供了简洁的、受 Rust 启发的语法，可以直接转译为 Python 类。

本章要点：

- **`type` 定义类** -- Auto 使用 `type` 关键字定义类。`type Person {}` 变为 `class Person: pass`。
- **`&self` 参数** -- 方法将 `&self` 作为第一个参数，等同于 Python 的 `self`。`a2p` 转译器将 `&self` 转换为 `self`。
- **`fn init(&self, ...)`** -- 构造方法。转译为 `def __init__(self, ...)`。
- **`.field` 访问实例** -- 在方法内部，`.field` 引用 `self.field`。转译器处理此转换。
- **字段声明** -- 在 `type` 块顶部声明的字段（如 `name: str`）会成为在 `__init__` 中初始化的实例变量。
- **类变量** -- 带有默认值的字段（如 `population: int = 0`）会成为 Python 中的类级属性。
- **`type Sub: Super {}`** -- 继承语法。转译为 `class Sub(Super):`。
- **方法重写** -- 在子类型中定义与基类型方法同名的方法会覆盖它。多态自然地工作。
- **`ClassName{args}`** -- 对象构造。转译为 `ClassName(args)`。

接下来，我们将学习输入/输出以及如何访问文件。
