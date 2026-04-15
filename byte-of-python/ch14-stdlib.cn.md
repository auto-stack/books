# 标准库

Python 标准库包含大量有用的模块，并且是每个标准 Python 安装的一部分。熟悉 Python 标准库非常重要，因为如果你了解这些库能做的事情的范围，许多问题都可以快速解决。

由于 Auto 转译为 Python，你可以使用 `use` 语句导入 Python 标准库中的任何模块。这意味着整个 Python 标准库都可以在你的 Auto 程序中使用。

我们将在本章中探索一些常用的模块。你可以在 Python 安装附带的文档的['库参考'部分](http://docs.python.org/3/library/)中找到 Python 标准库所有模块的完整详细信息。

> **注意：**
>
> 如果你觉得本章的主题太高级，可以跳过本章。但是，强烈建议当你对编程更加熟悉时再回到本章。

## `sys` 模块

`sys` 模块包含系统特定的功能。我们已经看到 `sys.argv` 列表包含命令行参数。

假设我们想检查运行 Auto 程序的 Python 软件的版本——`sys` 模块可以为我们提供这些信息。

将此程序保存为 `sys_module.auto`：

<Listing number="14-1" file-name="sys_module.auto" caption="使用 sys 模块">

```auto
use sys

fn main() {
    print(f"Python version: $sys.version")
    print(f"Version info: $sys.version_info")

    if sys.version_info.major >= 3 {
        print("You are running Python 3 or later.")
    } else {
        print("You need to upgrade to Python 3!")
    }
}
```

```python
import sys


def main():
    print(f"Python version: {sys.version}")
    print(f"Version info: {sys.version_info}")

    if sys.version_info.major >= 3:
        print("You are running Python 3 or later.")
    else:
        print("You need to upgrade to Python 3!")


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ auto run sys_module.auto
Python version: 3.12.0 (main, Oct  2 2024, 08:00:00)
Version info: sys.version_info(major=3, minor=12, micro=0, releaselevel='final', serial=0)
You are running Python 3 or later.
```

**工作原理**

`sys` 模块有一个 `version_info` 元组，为我们提供版本信息。第一个条目是主版本号。我们可以提取这个信息来使用它。

我们使用 f-字符串打印完整的版本字符串（`sys.version`）和版本信息元组（`sys.version_info`）。然后我们使用 `if` 语句检查主版本号是否为 3 或更高，并打印相应的消息。

> **Python 程序员注意：**
>
> Auto 中的 `use sys` 语句在 Python 中转换为 `import sys`。`sys.version_info` 属性和 `sys.version` 属性在两种语言中的工作方式完全相同，因为 Auto 转译为 Python。

## `logging` 模块

如果你想要将一些调试消息或重要消息存储在某个地方，以便你可以检查程序是否按预期运行，该怎么办？如何将这些消息"存储在某个地方"？这可以通过使用 `logging` 模块来实现。

将此程序保存为 `logging_example.auto`：

<Listing number="14-2" file-name="logging_example.auto" caption="使用 logging 模块">

```auto
use os
use platform
use logging

fn main() {
    let platform_name = platform.platform()
    let user_home = os.path.expanduser("~")

    let log_file: str
    if platform_name.contains("Windows") {
        let home_drive = os.environ.get("HOMEDRIVE", "C:")
        let home_path = os.environ.get("HOMEPATH", "\\")
        log_file = os.path.join(home_drive + home_path, "test.log")
    } else {
        log_file = os.path.join(user_home, "test.log")
    }

    logging.basicConfig(
        level = logging.DEBUG,
        format = "%(asctime)s : %(levelname)s : %(message)s",
        filename = log_file
    )

    logging.debug("Start of the program")
    logging.info("Doing something")
    logging.warning("Dying now")

    print(f"Logging to: $log_file")
    print("Check the log file for details.")
}
```

```python
import os
import platform
import logging


def main():
    platform_name = platform.platform()
    user_home = os.path.expanduser("~")

    log_file: str
    if platform_name.contains("Windows"):
        home_drive = os.environ.get("HOMEDRIVE", "C:")
        home_path = os.environ.get("HOMEPATH", "\\")
        log_file = os.path.join(home_drive + home_path, "test.log")
    else:
        log_file = os.path.join(user_home, "test.log")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s : %(levelname)s : %(message)s",
        filename=log_file,
    )

    logging.debug("Start of the program")
    logging.info("Doing something")
    logging.warning("Dying now")

    print(f"Logging to: {log_file}")
    print("Check the log file for details.")


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ auto run logging_example.auto
Logging to: /Users/swa/test.log
Check the log file for details.

$ cat /Users/swa/test.log
2024-03-29 09:27:36,660 : DEBUG : Start of the program
2024-03-29 09:27:36,660 : INFO : Doing something
2024-03-29 09:27:36,660 : WARNING : Dying now
```

**工作原理**

我们使用了标准库中的三个模块——用于与操作系统交互的 `os` 模块、用于获取平台（即操作系统）信息的 `platform` 模块，以及用于*记录*信息的 `logging` 模块。

首先，我们通过检查 `platform.platform()` 返回的字符串来确定我们使用的操作系统。如果是 Windows，我们找出主驱动器、主文件夹以及我们想要存储信息的文件名。将这些部分组合在一起，我们得到了文件的完整位置。对于其他平台，我们只需要知道用户的主文件夹，就可以得到文件的完整位置。

我们使用 `os.path.join()` 函数将这些位置的各个部分组合在一起。使用特殊函数而不是简单地将字符串相加的原因是，这个函数会确保完整位置符合操作系统预期的格式。

我们配置 `logging` 模块，将所有消息以特定格式写入我们指定的文件。

最后，我们可以放置用于调试、信息、警告甚至关键消息的消息。程序运行完成后，我们可以检查这个文件，了解程序中发生了什么，即使没有向运行程序的用户显示任何信息。

> **Python 程序员注意：**
>
> Auto 中的 `use os`、`use platform` 和 `use logging` 语句在 Python 中分别转换为 `import os`、`import platform` 和 `import logging`。所有日志记录函数的工作方式完全相同，因为 Auto 转译为 Python。

## 每周模块推荐

标准库中还有更多值得探索的内容，例如[调试](http://docs.python.org/3/library/pdb.html)、[处理命令行选项](http://docs.python.org/3/library/argparse.html)、[正则表达式](http://docs.python.org/3/library/re.html)等等。

进一步探索标准库的最佳方式是阅读 Doug Hellmann 优秀的 [Python Module of the Week](http://pymotw.com/2/contents.html) 系列（也可作为[书籍](http://amzn.com/0321767349)购买）以及 [Python 文档](http://docs.python.org/3/)。

## 小结

我们探索了 Python 标准库中许多模块的一些功能。强烈建议浏览 [Python 标准库文档](http://docs.python.org/3/library/)，以了解所有可用的模块。

由于 Auto 转译为 Python，通过 `use` 语句，整个 Python 标准库都在你的指尖。这是 Auto 最大的优势之一——你可以获得简洁、现代的语法，同时完全访问 Python 丰富的生态系统。
