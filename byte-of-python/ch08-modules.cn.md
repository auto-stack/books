# 模块

你已经看到了如何通过定义函数来在程序中复用代码。如果你想在编写的其他程序中复用大量函数呢？你可能已经猜到了，答案是模块。

编写模块的方法有很多种，但最简单的方式是创建一个扩展名为 `.at` 的文件，其中包含函数和变量。每一个 Auto 文件本身就已经是一个模块。

一个模块可以被另一个程序*导入*（import）以使用其功能。这也是我们使用 Python 标准库的方式——Auto 通过 `a2p` 将其 `use` 语句转译为 Python 的 `import` 语句。首先，我们来看看如何使用标准库模块。

## `use` 语句（导入模块）

在 Auto 中，你使用 `use` 关键字将模块引入程序。当 `a2p` 转译器处理你的 Auto 代码时，它会将 `use` 转换为 Python 的 `import` 语句。这是 Auto 和 Python 语法不同的关键之处之一——Auto 说"use"，而 Python 说"import"。

让我们看一个使用 `sys` 模块的例子：

<Listing number="8-1" file-name="using_sys.auto" caption="使用 sys 模块">

```auto
use sys

fn main() {
    print("The command line arguments are:")
    for arg in sys.argv {
        print(arg)
    }
}
```

```python
import sys


def main():
    print("The command line arguments are:")
    for arg in sys.argv:
        print(arg)


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

首先，我们使用 `use sys` 语句*导入* `sys` 模块。基本上，这告诉 Auto 我们要使用这个模块。`sys` 模块包含与 Python 解释器及其环境相关的功能——也就是 **sys**tem（系统）。

当 `a2p` 转译 `use sys` 时，它会在 Python 代码中输出 `import sys`。`sys` 模块是内置模块之一，所以 Python 知道去哪里找到它。

如果它不是内置模块，Python 解释器会在 `sys.path` 变量中列出的目录中搜索。如果找到了模块，该模块主体中的语句会被执行，模块就会变得*可用*供你使用。请注意，初始化只在*第一次*导入模块时进行。

`sys` 模块中的 `argv` 变量通过点号表示法访问——`sys.argv`。这清楚地表明这个名称是 `sys` 模块的一部分。这种方法的另一个好处是，名称不会与你自己在程序中可能使用的 `argv` 变量冲突。

`sys.argv` 变量是一个字符串*列表*（列表将在[后面的章节](./ch10-data-structures.md#data-structures)中详细解释）。具体来说，`sys.argv` 包含*命令行参数*的列表——即通过命令行传递给你程序的参数。

如果你使用 IDE 来编写和运行这些程序，请在菜单中寻找一种方式来指定程序的命令行参数。

当你带参数执行程序时，Python 会将命令行参数存储在 `sys.argv` 中供你使用。请记住，正在运行的脚本名称始终是 `sys.argv` 中的第一个元素。因此，如果你运行 `a2p using_sys.auto` 然后运行 `python using_sys.py we are arguments`，你将得到 `'using_sys.py'` 作为 `sys.argv[0]`，`'we'` 作为 `sys.argv[1]`，`'are'` 作为 `sys.argv[2]`，`'arguments'` 作为 `sys.argv[3]`。注意计数从 0 开始，而不是 1。

`sys.path` 包含导入模块的目录名称列表。请注意 `sys.path` 中的第一个字符串是空的——这表示当前目录也是搜索路径的一部分。这意味着你可以直接导入位于当前目录中的模块。否则，你需要将模块放在 `sys.path` 中列出的某个目录中。

请注意，当前目录是程序启动时所在的目录。

> **Python 程序员注意：**
>
> Auto 使用 `use` 代替 `import`。`a2p` 转译器会自动将 `use module_name` 转换为 `import module_name`。在编写 Auto 代码时，始终使用 `use`——永远不要直接写 `import`，因为 `a2p` 期望 `use` 关键字来进行正确的转译。

## 字节编译的 `.pyc` 文件

导入模块是一个相对昂贵的操作，所以 Python 使用了一些技巧来加快速度。其中一种方式是创建扩展名为 `.pyc` 的*字节编译*文件，这是 Python 将程序转换成的中间形式。当你下次从不同的程序导入该模块时，这个 `.pyc` 文件会很有用——它将快得多，因为导入模块所需的部分处理工作已经完成了。这些字节编译文件是与平台无关的。

注意：这些 `.pyc` 文件通常创建在 `__pycache__` 目录中。如果 Python 没有权限写入该目录中的文件，那么 `.pyc` 文件将*不会*被创建。

> **Auto 程序员注意：**
>
> 字节编译文件是 Python 运行时的优化。由于 Auto 代码在执行前会被转译为 Python，这个优化应用于生成的 Python 代码，而不是原始的 `.at` 文件。作为 Auto 程序员，你通常不需要担心 `.pyc` 文件。

## `from..import` 语句

如果你想直接将特定的变量或函数导入程序中（以避免每次都输入模块名称），可以在 Auto 中使用 `use module::item` 语法。`a2p` 转译器会将此转换为 Python 的 `from module import item` 语句。

> **警告：** 通常情况下，*避免*使用 `from..import` 语句，而应优先使用普通的 `use` 语句。因为这样你的程序可以避免名称冲突，并且更具可读性。

让我们看一个例子：

<Listing number="8-3" file-name="from_import.auto" caption="使用 from..import 语法">

```auto
use sys::argv

fn main() {
    print(f"The command line arguments are: $argv")
}
```

```python
from sys import argv


def main():
    print(f"The command line arguments are: {argv}")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

在 Auto 中，`use sys::argv` 告诉转译器只从 `sys` 模块中导入 `argv` 变量。`::` 语法借鉴了 Rust 风格的路径表示法，是 Auto 表达"从这个模块中获取这个特定项"的方式。

当通过 `a2p` 转译时，这在 Python 中变成 `from sys import argv`。现在你可以直接使用 `argv`，而无需 `sys.` 前缀。

> **Python 程序员注意：**
>
> Auto 使用 `use sys::argv`，而 Python 使用 `from sys import argv`。`::` 双冒号是 Auto 的命名空间分隔符，类似于 Rust。`a2p` 转译器会自动处理这个转换。
>
> 还要注意，Auto 使用 `$` 进行字符串插值（例如 `$argv`），而 Python 在 f-string 中使用 `{argv}`。转译器会在两者之间进行转换。

## `__name__` 属性

每个 Python 模块都有一个 `__name__` 属性。如果它的值是 `'__main__'`，则意味着该模块正被用户独立运行。这对于判断模块是独立运行还是被导入非常有用。

在 Auto 中，你不需要直接处理 `__name__`。`a2p` 转译器会自动将你的 `fn main()` 包装在生成的 Python 代码中的 `if __name__ == "__main__":` 保护块内。这意味着你的 Auto 程序的 `main` 函数只会在文件被直接执行时运行，而在作为模块导入时不会运行。

<Listing number="8-2" file-name="module_name.auto" caption="通过 Auto 的 main 函数使用 __name__">

```auto
fn main() {
    print("This program is being run by itself")
}
```

```python
def main():
    print("This program is being run by itself")


if __name__ == "__main__":
    main()
```

</Listing>

**工作原理**

在 Auto 中，你只需定义一个 `fn main()` 函数。`a2p` 转译器将其识别为入口点，并将对 `main()` 的调用包装在 `if __name__ == "__main__":` 保护块中。

当你直接运行转译后的 Python 文件时（例如 `python module_name.py`），`__name__` 将是 `'__main__'`，所以 `main()` 会被调用，你会看到输出：

```
This program is being run by itself
```

当另一个 Python 程序导入这个文件时（例如 `import module_name`），`__name__` 将是 `'module_name'`（不是 `'__main__'`），所以 `main()` 函数*不会*被调用。只有 `def main():` 函数定义会被加载。

> **Python 程序员注意：**
>
> 在 Python 中，你需要手动编写 `if __name__ == "__main__":` 来保护你的主代码。在 Auto 中，你只需定义 `fn main()`，`a2p` 转译器会自动添加保护块。这样更简洁，也不容易出错——你永远不会忘记添加保护。

## 创建你自己的模块

在 Auto 中创建自己的模块非常简单。你创建的每一个 `.at` 文件都已经是一个模块！你只需确保其他程序能够找到它——将其放在同一目录中，或者放在 `sys.path` 中列出的某个目录中。

下面是一个简单的模块文件示例。将其保存为 `mymodule.at`：

```auto
// mymodule.at

fn say_hi() {
    print("Hi, this is mymodule speaking.")
}

__version__ = "1.0"
```

现在，你可以在另一个 Auto 程序中使用这个模块。将以下代码保存为 `mymodule_demo.at`：

```auto
use mymodule

fn main() {
    mymodule.say_hi()
    print(f"Version: ${mymodule.__version__}")
}
```

转译并运行后，输出如下：

```
Hi, this is mymodule speaking.
Version: 1.0
```

**工作原理**

请注意，我们使用相同的点号表示法来访问模块的成员：`mymodule.say_hi()` 和 `mymodule.__version__`。`a2p` 转译器将 `use mymodule` 转换为 `import mymodule`，点号访问在两种语言中的工作方式完全相同。

以下是使用 `from..import` 语法的版本：

```auto
use mymodule::say_hi
use mymodule::__version__

fn main() {
    say_hi()
    print(f"Version: $__version__")
}
```

输出是相同的。然而，请注意，如果导入模块中已经存在一个 `__version__` 变量，就会发生名称冲突。这就是为什么始终建议优先使用普通的 `use` 语句，即使它可能会让程序稍微长一些。

> **警告：** 避免使用 `use module::*`（这会从模块中导入所有内容）。这可能导致难以调试的名称冲突。

> **Python 程序员注意：**
>
> Auto 的模块创建与 Python 基本相同。每个 `.at` 文件都是一个模块，就像 Python 中每个 `.py` 文件都是一个模块一样。`a2p` 转译器在转换为 Python 时会保留模块结构。

## `dir` 函数

内置的 `dir()` 函数返回由对象定义的名称列表。如果对象是一个模块，这个列表包含在该模块中定义的函数、类和变量。

这个函数可以接受参数。如果参数是模块的名称，该函数返回该指定模块中的名称列表。如果没有参数，该函数返回当前模块中的名称列表。

```python
$ python
>>> import sys

# 获取 sys 模块中的属性名称
>>> dir(sys)
['__displayhook__', '__doc__',
'argv', 'builtin_module_names',
'version', 'version_info']
# 此处仅显示部分条目

# 获取当前模块的属性名称
>>> dir()
['__builtins__', '__doc__',
'__name__', '__package__', 'sys']

# 创建一个新变量 'a'
>>> a = 5

>>> dir()
['__builtins__', '__doc__', '__name__', '__package__', 'sys', 'a']

# 删除/移除一个名称
>>> del a

>>> dir()
['__builtins__', '__doc__', '__name__', '__package__', 'sys']
```

**工作原理**

首先，我们看到了在导入的 `sys` 模块上使用 `dir` 的情况。我们可以看到它包含的大量属性。

接下来，我们不传参数使用 `dir` 函数。默认情况下，它返回当前模块的属性列表。请注意，已导入模块的列表也是这个列表的一部分。

为了观察 `dir` 的实际效果，我们定义一个新变量 `a` 并给它赋值，然后检查 `dir`，我们观察到列表中多了一个同名的新值。我们使用 `del` 语句删除当前模块的变量/属性，这个变化再次反映在 `dir` 函数的输出中。

关于 `del` 的说明：这个语句用于*删除*一个变量/名称，在语句执行后，在这个例子中是 `del a`，你将不再能访问变量 `a`——就好像它从未存在过一样。

请注意，`dir()` 函数适用于*任何*对象。例如，运行 `dir(str)` 可以查看 `str`（字符串）类的属性。

## 包

到现在为止，你一定已经开始注意到组织程序的层次结构了。变量通常放在函数内部。函数和全局变量通常放在模块内部。如果你想组织模块呢？这就是包发挥作用的地方。

包是模块的文件夹，带有一个特殊的 `__init__.py` 文件，向 Python 指示这个文件夹是特殊的，因为它包含 Python 模块。

假设你想创建一个名为 `world` 的包，其中包含子包 `asia`、`africa` 等，这些子包又包含 `india`、`madagascar` 等模块。

你可以这样组织文件夹结构：

```
- <sys.path 中列出的某个文件夹>/
    - world/
        - __init__.py
        - asia/
            - __init__.py
            - india/
                - __init__.py
                - foo.py
        - africa/
            - __init__.py
            - madagascar/
                - __init__.py
                - bar.py
```

包只是一种方便地按层次结构组织模块的方式。你将在[标准库](./ch14-stdlib.md#stdlib)中看到很多这样的例子。

> **Auto 程序员注意：**
>
> Auto 目前还没有独立于 Python 的包系统。转译后，Auto 模块遵循 Python 的包约定。在未来的版本中，Auto 可能会引入自己的模块解析机制。

## 小结

就像函数是程序的可复用部分一样，模块是可复用的程序。包是组织模块的另一个层次。Python 自带的标准库就是这样一个包和模块的集合的例子。

我们已经学习了如何使用这些模块以及创建自己的模块。以下是 Auto 的关键要点：

- **`use module`** ——导入一个模块。Auto 的 `use` 关键字在转译输出中变成 Python 的 `import`。
- **`use module::item`** ——从模块中导入特定项。这会变成 Python 的 `from module import item`。
- **`fn main()`** ——Auto 的入口点。`a2p` 转译器会自动在 Python 输出中用 `if __name__ == "__main__":` 包装它。
- **每个 `.at` 文件都是一个模块** ——你只需在文件中编写 Auto 代码就可以创建可复用的模块。
- **`dir()`** ——检查模块中可用的名称（Python 内置函数）。

接下来，我们将学习数据结构。
