# 数据结构

数据结构基本上就是——它们是可以将一些*数据*放在一起的*结构*。换句话说，它们用于存储相关数据的集合。

Auto 中有四种内置数据结构——_List（列表）、Tuple（元组）、HashMap（哈希映射）和 HashSet（哈希集合）_。我们将了解如何使用它们中的每一种，以及它们如何让我们的生活更轻松。

## List（列表）

`List` 是一种数据结构，用于保存有序的项目集合，即你可以在列表中存储一系列项目。这很容易想象，如果你能想到一个购物清单，上面有你要购买的项目，只不过在购物清单上每个项目可能单独占一行，而在 Auto 中你用逗号将它们分隔开。

项目列表应该用方括号括起来，以便 Auto 理解你正在指定一个列表。一旦你创建了一个列表，你可以添加、删除或搜索列表中的项目。由于我们可以添加和删除项目，我们说列表是一种*可变的*数据类型，即这种类型可以被修改。

## 对象与方法简介

虽然我们一直将对象和类的讨论推迟到现在，但这里需要做一点解释，以便你能更好地理解列表。我们将在[后面的章节](./ch11-oop.md#oop)中详细探讨这个话题。

列表是使用对象和方法的一个例子。当你使用变量 `i` 并给它赋一个值，比如整数 `5`，你可以把它看作是创建了一个 `int` 类（即类型）的*对象*（即实例）`i`。

一个类也可以有*方法*，即专门为该类定义的函数。只有当你拥有该类的对象时，你才能使用这些功能。例如，Auto 为 `List` 类型提供了一个 `append` 方法，允许你将项目添加到列表末尾。例如，`mylist.append('an item')` 会将该字符串添加到列表 `mylist` 中。注意使用点号来访问对象的方法。

方法通过点号来访问，例如，`mylist.append('an item')`。

<Listing number="9-1" file-name="list.auto" caption="使用列表">

```auto
fn main() {
    let mut shoplist: [str] = ["apple", "mango", "carrot", "banana"]

    print(f"I have ${shoplist.len()} items to purchase.")

    print("These items are:", end = " ")
    for item in shoplist {
        print(item, end = " ")
    }

    print("\nI also have to buy rice.")
    shoplist.append("rice")
    print("My shopping list is now:", shoplist)

    print("I will sort my list now")
    shoplist.sort()
    print("Sorted shopping list is:", shoplist)

    print("The first item I will buy is:", shoplist[0])
    let olditem = shoplist[0]
    shoplist.remove(0)
    print("I bought the", olditem)
    print("My shopping list is now:", shoplist)
}
```

```python
def main():
    shoplist = ["apple", "mango", "carrot", "banana"]

    print(f"I have {len(shoplist)} items to purchase.")

    print("These items are:", end=" ")
    for item in shoplist:
        print(item, end=" ")

    print("\nI also have to buy rice.")
    shoplist.append("rice")
    print("My shopping list is now:", shoplist)

    print("I will sort my list now")
    shoplist.sort()
    print("Sorted shopping list is:", shoplist)

    print("The first item I will buy is:", shoplist[0])
    olditem = shoplist[0]
    del shoplist[0]
    print("I bought the", olditem)
    print("My shopping list is now:", shoplist)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

变量 `shoplist` 是某人去市场时的购物清单。在 `shoplist` 中，我们只存储要购买物品名称的字符串，但你可以将_任何类型的对象_添加到列表中，包括数字甚至其他列表。

我们还使用了 `for..in` 循环来遍历列表中的项目。到现在为止，你一定已经意识到列表也是一个序列。序列的特殊性将在[后面的章节](#sequence)中讨论。

注意在调用 `print` 函数时使用了 `end` 参数，表示我们希望以空格而不是通常的换行符结束输出。

接下来，我们使用列表对象的 `append` 方法向列表中添加一个项目，正如之前讨论的那样。然后，我们通过简单地将列表传递给 `print` 函数来打印列表的内容，从而验证项目确实已添加到列表中。

然后，我们使用列表的 `sort` 方法对列表进行排序。重要的是要理解，这个方法会影响列表本身，而不是返回一个修改后的列表——这与字符串的工作方式不同。这就是我们说列表是_可变的_而字符串是_不可变的_的含义。

接下来，当我们在市场上买完一个物品后，我们想把它从列表中移除。我们通过使用 `remove` 方法来实现这一点。这里，我们通过指定索引来指出要从列表中移除哪个项目。我们指定要移除列表中的第一个项目，因此使用 `shoplist.remove(0)`（记住 Auto 从 0 开始计数）。

> **Python 程序员注意：**
>
> 在 Auto 中，你使用 `shoplist.remove(0)` 按索引移除项目，而 Python 使用 `del shoplist[0]`。`a2p` 转译器会将 `list.remove(index)` 转换为生成的 Python 代码中的 `del list[index]`。此外，Auto 使用 `list.len()` 作为方法调用，而 Python 使用 `len(list)` 作为内置函数。

## Tuple（元组）

元组用于将多个对象组合在一起。可以把它看作类似于列表，但没有列表类型提供的丰富功能。元组的一个主要特征是它们像字符串一样是*不可变的*，即你不能修改元组。

元组通过在括号内用逗号分隔指定项目来定义。

元组通常用于语句或用户定义的函数可以安全地假定值的集合（即使用的元组值）不会改变的情况。

<Listing number="9-2" file-name="tuple.auto" caption="使用元组">

```auto
fn main() {
    let zoo: (str, str, str) = ("python", "elephant", "penguin")
    print(f"Number of animals in the zoo is ${zoo.len()}")

    let new_zoo: (str, (str, str, str), str) = ("monkey", zoo, "dolphin")
    print(f"Number of cages in the new zoo is ${new_zoo.len()}")
    print(f"All animals in new zoo are ${new_zoo}")
    print(f"Animals brought from old zoo are ${new_zoo[1]}")
    print(f"Last animal brought from old zoo is ${new_zoo[1][2]}")
    print(f"Number of animals in the new zoo is ${len(new_zoo) - 1 + new_zoo[1].len()}")
}
```

```python
def main():
    zoo = ("python", "elephant", "penguin")
    print(f"Number of animals in the zoo is {len(zoo)}")

    new_zoo = ("monkey", zoo, "dolphin")
    print(f"Number of cages in the new zoo is {len(new_zoo)}")
    print(f"All animals in new zoo are {new_zoo}")
    print(f"Animals brought from old zoo are {new_zoo[1]}")
    print(f"Last animal brought from old zoo is {new_zoo[1][2]}")
    print(f"Number of animals in the new zoo is {len(new_zoo) - 1 + len(new_zoo[1])}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

变量 `zoo` 引用一个项目元组。我们看到 `len` 函数可以用来获取元组的长度。这也表明元组也是一个[序列](#sequence)。

我们现在正在将这些动物转移到一个新的动物园，因为旧的动物园即将关闭。因此，`new_zoo` 元组包含一些已经存在的动物以及从旧动物园带来的动物。回到现实，请注意元组中的元组不会失去其身份。

我们可以通过在方括号内指定项目的位置来访问元组中的项目，就像我们对列表所做的那样。这被称为_索引_操作符。我们通过指定 `new_zoo[2]` 来访问 `new_zoo` 中的第三个项目，并通过指定 `new_zoo[2][2]` 来访问 `new_zoo` 元组中第三个项目内的第三个项目。一旦你理解了这个习惯用法，这就非常简单了。

> **包含 0 个或 1 个项目的元组**
>
> 空元组通过一对空括号构造，例如 `myempty = ()`。然而，只有一个项目的元组就没那么简单了。你必须在第一个（也是唯一的）项目后面指定一个逗号，以便 Auto 可以区分元组和表达式中包围对象的一对括号，即如果你想表示一个包含项目 `2` 的元组，你必须指定 `singleton = (2 , )`。

<!-- -->

> **Python 程序员注意：**
>
> Auto 使用 `Tuple` 作为类型名称，使用 `(T1, T2, ...)` 作为元组类型注解，而 Python 使用 `tuple`。`a2p` 转译器处理这种转换。列表中的列表不会失去其身份，即列表不会被扁平化。这同样适用于元组中的元组、列表中的元组或元组中的列表等。

## Dictionary（HashMap，字典）

`HashMap` 就像一个地址簿，你可以通过知道一个人的名字来查找他/她的地址或联系方式，即我们将*键*（名字）与*值*（详细信息）关联起来。请注意，键必须是唯一的，就像你不能在有两个完全同名的人时找到正确的信息一样。

请注意，你只能使用不可变对象（如字符串）作为 HashMap 的键，但你可以使用不可变或可变对象作为 HashMap 的值。这基本上意味着你应该只使用简单的对象作为键。

键值对在 HashMap 中通过 `d = {key1 : value1, key2 : value2 }` 的表示法来指定。请注意，键值对用冒号分隔，对之间用逗号分隔，所有这些都被括在一对花括号中。

请记住，HashMap 中的键值对没有任何顺序。如果你想要特定的顺序，那么你必须在事先对它们进行排序。

<Listing number="9-3" file-name="dict.auto" caption="使用字典（HashMap）">

```auto
fn main() {
    let mut ab: HashMap<str, int> = {"swaroop": 4098, "matz": 4139}
    print(f"ab is $ab")

    ab["guido"] = 4127
    print(f"\nab is now $ab")

    // delete a key-value pair
    // ab.remove("swaroop")
    print(f"\nab is now $ab")

    for name in ab.keys() {
        print(f"Contact $name at $ab[name]")
    }

    if ab.contains_key("guido") {
        let addr = ab["guido"]
        print(f"\nguido's address is $addr")
    }
}
```

```python
def main():
    ab = {"swaroop": 4098, "matz": 4139}
    print(f"ab is {ab}")

    ab["guido"] = 4127
    print(f"\nab is now {ab}")

    # delete a key-value pair
    # del ab["swaroop"]
    print(f"\nab is now {ab}")

    for name in ab.keys():
        print(f"Contact {name} at {ab[name]}")

    if "guido" in ab:
        addr = ab["guido"]
        print(f"\nguido's address is {addr}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

我们使用上面讨论的表示法创建了字典 `ab`。然后我们通过使用在列表和元组的上下文中讨论过的索引操作符来访问键值对。观察一下简单的语法。

我们可以使用 HashMap 的 `remove` 方法来删除键值对。我们只需指定 HashMap 和要删除的键。此操作无需知道与键对应的值。

接下来，我们使用 `keys` 方法访问 HashMap 的每个键值对，该方法返回所有键的集合。我们使用 `for..in` 循环检索每个键，然后使用索引操作符访问相应的值。

我们可以简单地使用索引操作符访问一个键并赋值来添加新的键值对，正如我们在上面的例子中为 Guido 所做的那样。

我们可以使用 `contains_key` 方法来检查某个键是否存在。

> **Python 程序员注意：**
>
> Auto 使用 `HashMap<K, V>` 作为类型名称，而 Python 使用 `dict`。Auto 使用 `map.contains_key("key")` 来检查键是否存在，而 Python 使用 `"key" in map`。`a2p` 转译器会自动将 `HashMap` 转换为 `dict`，将 `contains_key` 转换为 `in` 操作符。同样，Auto 使用 `map.remove("key")`，而 Python 使用 `del map["key"]`。

## 序列

列表、元组和字符串都是序列的例子，但什么是序列，它们有什么特别之处呢？

主要特性是*成员测试*（即 `contains` 方法）和*索引操作*，这允许我们直接获取序列中的特定项目。

上述三种序列类型——列表、元组和字符串，还有一个*切片*操作，允许我们检索序列的一个切片，即序列的一部分。

<Listing number="9-4" file-name="seq.auto" caption="序列（索引和切片）">

```auto
fn main() {
    let shoplist: [str] = ["apple", "mango", "carrot", "banana"]

    // Indexing or 'subscription' operation
    print("Item 0 is:", shoplist[0])
    print("Item 1 is:", shoplist[1])
    print("Item 2 is:", shoplist[2])
    print("Item 3 is:", shoplist[3])
    print("Item -1 is:", shoplist[-1])
    print("Item -2 is:", shoplist[-2])

    // Slicing on a list
    print("Item 1 to 3 is:", shoplist[1:3])
    print("Item 2 to end is:", shoplist[2:])
    print("Item 1 to -1 is:", shoplist[1:-1])
    print("Item start to end is:", shoplist[:])

    // Slicing with step
    print("Item 1 to 3 step 1 is:", shoplist[1:3:1])
    print("Item start to end step 2 is:", shoplist[::2])
    print("Item start to end step 3 is:", shoplist[::3])
    print("Item reversed is:", shoplist[::-1])
}
```

```python
def main():
    shoplist = ["apple", "mango", "carrot", "banana"]

    # Indexing or 'subscription' operation
    print("Item 0 is:", shoplist[0])
    print("Item 1 is:", shoplist[1])
    print("Item 2 is:", shoplist[2])
    print("Item 3 is:", shoplist[3])
    print("Item -1 is:", shoplist[-1])
    print("Item -2 is:", shoplist[-2])

    # Slicing on a list
    print("Item 1 to 3 is:", shoplist[1:3])
    print("Item 2 to end is:", shoplist[2:])
    print("Item 1 to -1 is:", shoplist[1:-1])
    print("Item start to end is:", shoplist[:])

    # Slicing with step
    print("Item 1 to 3 step 1 is:", shoplist[1:3:1])
    print("Item start to end step 2 is:", shoplist[::2])
    print("Item start to end step 3 is:", shoplist[::3])
    print("Item reversed is:", shoplist[::-1])


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

首先，我们看到了如何使用索引来获取序列的各个项目。这也被称为_订阅_操作。每当你在方括号中指定一个数字给序列，如上所示，Auto 会为你获取序列中对应位置的项目。记住 Auto 从 0 开始计数。因此，`shoplist[0]` 获取第一个项目，`shoplist[3]` 获取 `shoplist` 序列中的第四个项目。

索引也可以是负数，在这种情况下，位置从序列末尾开始计算。因此，`shoplist[-1]` 引用序列中的最后一个项目，`shoplist[-2]` 获取序列中的倒数第二个项目。

切片操作通过指定序列名称后跟方括号内用冒号分隔的一对可选数字来使用。请注意，这与你到目前为止使用的索引操作非常相似。记住数字是可选的，但冒号不是。

切片操作中冒号前面的第一个数字指的是切片开始的位置，冒号后面的第二个数字指示切片将在哪里停止。如果未指定第一个数字，Auto 将从序列的开头开始。如果省略第二个数字，Auto 将在序列的末尾停止。请注意，返回的切片从起始位置_开始_，并在_结束_位置之前_结束_，即起始位置包含在内，但结束位置从序列切片中排除。

因此，`shoplist[1:3]` 返回从位置 1 开始的序列切片，包含位置 2 但在位置 3 处停止，因此返回两个项目的*切片*。同样，`shoplist[:]` 返回整个序列的副本。

你也可以使用负数位置进行切片。负数用于从序列末尾开始的位置。例如，`shoplist[:-1]` 将返回一个排除序列最后一个项目但包含其他所有内容的序列切片。

你还可以为切片提供第三个参数，即切片的_步长_（默认情况下，步长为 1）：

```python
>>> shoplist = ['apple', 'mango', 'carrot', 'banana']
>>> shoplist[::1]
['apple', 'mango', 'carrot', 'banana']
>>> shoplist[::2]
['apple', 'carrot']
>>> shoplist[::3]
['apple', 'banana']
>>> shoplist[::-1]
['banana', 'carrot', 'mango', 'apple']
```

请注意，当步长为 2 时，我们获取位置 0、2 的项目……当步长为 3 时，我们获取位置 0、3 的项目等。

序列的妙处在于你可以以相同的方式访问元组、列表和字符串！

> **Python 程序员注意：**
>
> Auto 的切片语法与 Python 相同：`seq[start:stop:step]`。`a2p` 转译器会原样传递切片操作，因为两种语言共享相同的语法。负数索引和切片在两种语言中的工作方式也完全相同。

## Set（HashSet，集合）

集合是简单对象的_无序_集合。当对象在集合中的存在比顺序或出现的次数更重要时，使用集合。

使用集合，你可以测试成员资格、是否是另一个集合的子集、找到两个集合之间的交集等等。

<Listing number="9-5" file-name="set.auto" caption="使用集合（HashSet）">

```auto
fn main() {
    let mut bri: HashSet<str> = ["brazil", "russia", "india"]
    print(f"'india' in bri: ${bri.contains("india")}")
    print(f"'usa' in bri: ${bri.contains("usa")}")

    let mut bric: HashSet<str> = bri.copy()
    bric.add("china")
    print(f"bric is $bric")
    print(f"bric is superset of bri: ${bric.issuperset(bri)}")

    bri.remove("russia")
    print(f"bri is now $bri")

    // intersection
    let common = bri.intersection(bric)
    print(f"bri & bric is $common")
}
```

```python
def main():
    bri = {"brazil", "russia", "india"}
    print(f"'india' in bri: {'india' in bri}")
    print(f"'usa' in bri: {'usa' in bri}")

    bric = bri.copy()
    bric.add("china")
    print(f"bric is {bric}")
    print(f"bric is superset of bri: {bric.issuperset(bri)}")

    bri.remove("russia")
    print(f"bri is now {bri}")

    # intersection
    common = bri.intersection(bric)
    print(f"bri & bric is {common}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

如果你还记得学校里学的基本集合论数学，那么这个例子就很容易理解了。如果不记得，你可以搜索"集合论"和"韦恩图"来更好地理解我们在 Auto 中对集合的使用。

> **Python 程序员注意：**
>
> Auto 使用 `HashSet<T>` 作为类型名称，而 Python 使用 `set`。Auto 使用 `set.contains("item")` 来检查成员资格，而 Python 使用 `"item" in set`。`a2p` 转译器会将 `HashSet` 转换为 `set`，将 `contains` 转换为 `in` 操作符。集合字面量语法 `{...}` 在两种语言中是相同的。

## 引用

当你创建一个对象并将其赋值给一个变量时，该变量只_引用_该对象，并不代表对象本身！也就是说，变量名指向你计算机内存中存储该对象的部分。这被称为将名称*绑定*到对象。

通常，你不需要担心这个问题，但由于引用带来的一个微妙效果你需要了解：

<Listing number="9-6" file-name="reference.auto" caption="引用">

```auto
fn main() {
    print("Making a copy of a list")
    let mylist: [str] = ["a", "b", "c", "d"]
    print("mylist:", mylist)

    // Make a copy by doing a full slice
    let mylist_copy: [str] = mylist[:]
    print("mylist_copy:", mylist_copy)

    // Remove an item from the copy
    mylist_copy.remove(0)
    print("mylist after removing first item:", mylist)
    print("mylist_copy after removing first item:", mylist_copy)
}
```

```python
def main():
    print("Making a copy of a list")
    mylist = ["a", "b", "c", "d"]
    print("mylist:", mylist)

    # Make a copy by doing a full slice
    mylist_copy = mylist[:]
    print("mylist_copy:", mylist_copy)

    # Remove an item from the copy
    del mylist_copy[0]
    print("mylist after removing first item:", mylist)
    print("mylist_copy after removing first item:", mylist_copy)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

请记住，如果你想复制一个列表或此类序列或复杂对象（而不是整数等简单_对象_），你必须使用切片操作来制作副本。如果你只是将变量名赋值给另一个名称，它们都将''引用''同一个对象，如果你不小心，这可能会带来麻烦。

输出显示修改副本（`mylist_copy`）不会影响原始列表（`mylist`）。这是因为我们使用 `mylist[:]` 创建了一个真正的副本，而不仅仅是一个引用。

> **Python 程序员注意：**
>
> 引用行为在 Auto 和 Python 中是相同的。请记住，列表的赋值语句**不会**创建副本。你必须使用切片操作（`mylist[:]`）来制作序列的副本。这在两种语言中的工作方式完全相同。

## 更多关于字符串

我们之前已经详细讨论过字符串了。还有什么可以了解的呢？嗯，你知道字符串也是对象吗，它们有可以完成从检查字符串的一部分到去除空格等所有操作的方法？

你在程序中使用的字符串都是 `str` 类型的。下一个例子中演示了该类型的一些有用的方法。

<Listing number="9-7" file-name="str_methods.auto" caption="字符串方法">

```auto
fn main() {
    let name: str = "Swaroop"

    if name.startswith("Swa") {
        print("Yes, the string starts with 'Swa'")
    }

    if name.contains("war") {
        print("Yes, it contains the string 'war'")
    }

    if name.contains("xyz") {
        print("Yes, it contains the string 'xyz'")
    } else {
        print("No, it does not contain 'xyz'")
    }

    let delim = "-*-"
    let mylist: [str] = ["Brazil", "Russia", "India", "China"]
    print(delim.join(mylist))

    print(name.replace("oo", "aa"))

    print("This is a sentence".split())
}
```

```python
def main():
    name = "Swaroop"

    if name.startswith("Swa"):
        print("Yes, the string starts with 'Swa'")

    if "war" in name:
        print("Yes, it contains the string 'war'")

    if "xyz" in name:
        print("Yes, it contains the string 'xyz'")
    else:
        print("No, it does not contain 'xyz'")

    delim = "-*-"
    mylist = ["Brazil", "Russia", "India", "China"]
    print(delim.join(mylist))

    print(name.replace("oo", "aa"))

    print("This is a sentence".split())


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

在这里，我们看到了许多字符串方法的实际应用。`startswith` 方法用于找出字符串是否以给定的字符串开头。`contains` 方法用于检查给定字符串是否是该字符串的一部分。

`str` 类型还有一个方便的 `join` 方法，可以用字符串作为序列中每个项目之间的分隔符将序列的项目连接起来，并返回由此生成的更大的字符串。

> **Python 程序员注意：**
>
> 大多数字符串方法在两种语言中的工作方式相同。关键区别在于 Auto 使用 `str.contains("substr")`，而 Python 使用 `"substr" in str`。`a2p` 转译器会将 `contains` 转换为 `in` 操作符。`startswith`、`replace`、`join` 和 `split` 等方法在两种语言中是完全相同的。

## 小结

我们已经详细探讨了 Auto 的各种内置数据结构。这些数据结构对于编写规模合理的程序至关重要。以下是关键要点：

- **`List`**（`[T]`）——可变的有序集合。使用 `list.append()`、`list.remove()`、`list.sort()` 和 `list.len()`。
- **`Tuple`**（`(T1, T2, ...)`）——不可变的有序集合。创建后不能修改。
- **`HashMap<K, V>`**（`{k: v, ...}`）——键值对。使用 `map.contains_key()`、`map.keys()` 和 `map.remove()`。
- **`HashSet<T>`**（`{v1, v2, ...}`）——唯一值。使用 `set.contains()`、`set.add()`、`set.remove()` 和 `set.intersection()`。
- **序列**——列表、元组和字符串都支持索引（`seq[0]`）、切片（`seq[1:3]`）和负数索引（`seq[-1]`）。
- **引用**——使用 `seq[:]` 来制作序列的副本，而不是仅仅创建另一个引用。
- **字符串方法**——`startswith`、`contains`、`replace`、`join`、`split` 等等。

现在我们已经掌握了 Auto 的许多基础知识，接下来我们将看到如何设计和编写一个实际的程序。
