# 解决问题

我们已经探索了 Auto 语言的各个方面，现在让我们来看看如何将所有这些部分组合在一起，通过设计和编写一个*真正有用*的程序来巩固所学。我们的目标是学会如何独立编写 Auto 脚本。

## 问题

我们要解决的问题如下：

> 我想要一个程序，能创建所有重要文件的备份。

虽然这是一个简单的问题，但仅凭这些信息我们无法开始着手解决。我们需要进行更多的*分析*。例如，我们如何指定要备份*哪些*文件？它们*如何*存储？存储在*哪里*？

在充分分析问题之后，我们*设计*程序。我们列出了程序应该如何工作的各项要点。在本例中，我根据自己的需求创建了以下列表。如果你自己来做设计，可能不会得出完全相同的分析结果，因为每个人的做事方式不同，这完全没有问题。

- 要备份的文件和目录在一个列表中指定。
- 备份必须存储在一个主备份目录中。
- 文件被备份到一个 zip 文件中。
- zip 归档文件的名称是当前的日期和时间。
- 我们使用任何标准 GNU/Linux 或 Unix 发行版中默认可用的标准 `zip` 命令。注意，只要你有任何带有命令行界面的归档命令，都可以使用。

> **Windows 用户注意**
>
> Windows 用户可以从 [GnuWin32 项目页面](http://gnuwin32.sourceforge.net/packages/zip.htm) [安装](http://gnuwin32.sourceforge.net/downlinks/zip.php) `zip` 命令，并将 `C:\Program Files\GnuWin32\bin` 添加到系统的 `PATH` 环境变量中。

## 解决方案

由于我们程序的设计现在已经相当稳定，我们可以编写代码来*实现*我们的解决方案。

由于 Auto 通过 `a2p` 转译为 Python，我们可以在 Auto 代码中使用 Python 的标准库模块，如 `os` 和 `time`。Auto 中的 `use` 关键字在生成的 Python 代码中会变成 `import`。

将其保存为 `backup_ver1.at`：

<Listing number="10-1" file-name="backup_ver1.auto" caption="备份脚本 - 版本 1">

```auto
use os
use time

fn main() {
    // 1. The files and directories to be backed up are
    // specified in a list.
    // Example on Windows:
    // source = ["C:\\My Documents"]
    // Example on Mac OS X and Linux:
    let source = ["/Users/swa/notes"]
    // Notice we have to use double quotes inside a string
    // for names with spaces in it. We could have also used
    // a raw string by writing [r'C:\My Documents'].

    // 2. The backup must be stored in a
    // main backup directory
    // Example on Windows:
    // target_dir = "E:\\Backup"
    // Example on Mac OS X and Linux:
    let target_dir = "/Users/swa/backup"
    // Remember to change this to which folder you will be using

    // 3. The files are backed up into a zip file.
    // 4. The name of the zip archive is the current date and time
    let target = target_dir + os.sep +
        time.strftime("%Y%m%d%H%M%S") + ".zip"

    // Create target directory if it is not present
    if !os.path.exists(target_dir) {
        os.mkdir(target_dir)  // make directory
    }

    // 5. We use the zip command to put the files in a zip archive
    let zip_command = f"zip -r $target ${source.join(' ')}"

    // Run the backup
    print("Zip command is:")
    print(zip_command)
    print("Running:")
    if os.system(zip_command) == 0 {
        print("Successful backup to", target)
    } else {
        print("Backup FAILED")
    }
}
```

```python
import os
import time


def main():
    # 1. The files and directories to be backed up are
    # specified in a list.
    # Example on Windows:
    # source = ["C:\\My Documents"]
    # Example on Mac OS X and Linux:
    source = ['/Users/swa/notes']
    # Notice we have to use double quotes inside a string
    # for names with spaces in it. We could have also used
    # a raw string by writing [r'C:\My Documents'].

    # 2. The backup must be stored in a
    # main backup directory
    # Example on Windows:
    # target_dir = "E:\\Backup"
    # Example on Mac OS X and Linux:
    target_dir = '/Users/swa/backup'
    # Remember to change this to which folder you will be using

    # 3. The files are backed up into a zip file.
    # 4. The name of the zip archive is the current date and time
    target = target_dir + os.sep + \
        time.strftime('%Y%m%d%H%M%S') + '.zip'

    # Create target directory if it is not present
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)  # make directory

    # 5. We use the zip command to put the files in a zip archive
    zip_command = f"zip -r {target} {' '.join(source)}"

    # Run the backup
    print('Zip command is:')
    print(zip_command)
    print('Running:')
    if os.system(zip_command) == 0:
        print('Successful backup to', target)
    else:
        print('Backup FAILED')


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ a2p backup_ver1.at && python backup_ver1.py
Zip command is:
zip -r /Users/swa/backup/20140328084844.zip /Users/swa/notes
Running:
  adding: Users/swa/notes/ (stored 0%)
  adding: Users/swa/notes/blah1.txt (stored 0%)
  adding: Users/swa/notes/blah2.txt (stored 0%)
  adding: Users/swa/notes/blah3.txt (stored 0%)
Successful backup to /Users/swa/backup/20140328084844.zip
```

现在，我们进入了*测试*阶段，测试程序是否正常工作。如果程序的行为不符合预期，我们就需要*调试*程序，即从程序中*消除*（remove）*错误*（bugs）。

如果上述程序在你的机器上无法运行，请复制输出中 `Zip command is` 之后打印的那一行命令，粘贴到 shell（在 GNU/Linux 和 Mac OS X 上）或 `cmd`（在 Windows 上）中，看看有什么错误并尝试修复。同时检查 zip 命令的手册，看看可能出了什么问题。如果这个命令能成功执行，那么问题可能出在程序本身，请检查程序是否与上面写的完全一致。

**工作原理**

你会注意到我们是如何将*设计*一步步地转化为*代码*的。

我们首先使用 `use` 关键字导入 `os` 和 `time` 模块。然后，在 `source` 列表中指定要备份的文件和目录。`target_dir` 变量指定了我们存储所有备份文件的目标目录。我们要创建的 zip 归档文件名是当前日期和时间，使用 `time.strftime()` 函数生成。它还会有 `.zip` 扩展名，并存储在 `target_dir` 目录中。

请注意 `os.sep` 变量的使用——它根据你的操作系统提供目录分隔符，即在 GNU/Linux、Unix、macOS 上为 `'/'`，在 Windows 上为 `'\\'`。直接使用 `os.sep` 而不是这些字符本身，可以让我们的程序具有可移植性，在所有这些系统上都能正常工作。

`time.strftime()` 函数接受一个格式字符串，如我们在上面程序中使用的那个。`%Y` 格式代码会被替换为包含世纪的年份。`%m` 格式代码会被替换为 `01` 到 `12` 之间的十进制月份数，以此类推。完整格式代码列表可以在 [Python 参考手册](http://docs.python.org/3/library/time.html#time.strftime) 中找到。

我们使用 `+` 运算符创建目标 zip 文件名，它会*连接*字符串，即将两个字符串连接在一起并返回一个新字符串。然后，我们使用 f-string（`f"..."`）和 `$variable` 插值创建 `zip_command` 字符串，在 Python 输出中它会变成 `{variable}`。`$` 语法是 Auto 在字符串中嵌入表达式的方式，而 Python 使用 `{}`。

我们使用的 `zip` 命令有一些可用的选项，其中之一是 `-r`。`-r` 选项指定 zip 命令应该对目录进行**递归**操作，即包含所有子目录和文件。选项后面是 zip 归档文件的名称，然后是要备份的文件和目录列表。我们使用 `join` 方法将 `source` 列表转换为字符串。

然后，我们最终使用 `os.system` 函数*运行*命令，该函数会像从*系统*（即在 shell 中）运行一样执行命令——如果命令成功则返回 `0`，否则返回错误编号。

根据命令的结果，我们打印相应的消息，表示备份成功或失败。

就是这样，我们已经创建了一个备份重要文件的脚本！

> **Auto 程序员注意：**
>
> Auto 使用 `!` 进行逻辑取反（not），而不是 Python 的 `not` 关键字。`a2p` 转译器会自动将 `!expr` 转换为 `not expr`。同样，Auto 在 f-string 中使用 `$var`，而 Python 使用 `{var}`。

> **Windows 用户注意**
>
> 除了双反斜杠转义序列，你也可以使用原始字符串。例如，使用 `"C:\\Documents"` 或 `r"C:\Documents"`。但是，*不要*使用 `"C:\Documents"`，因为你最终会使用一个未知的转义序列 `\D`。

现在我们有了一个可工作的备份脚本，我们可以在任何时候用它来备份文件。这就是软件的*运行*阶段或*部署*阶段。

## 第二版

我们的脚本第一版可以工作。但是，我们可以对其进行一些改进，使其在日常使用中更加方便。这被称为软件的*维护*阶段。

我觉得有用的改进之一是更好的文件命名机制——使用*时间*作为文件名，在主备份目录中按当前*日期*创建子目录。第一个好处是你的备份以分层方式存储，因此更容易管理。第二个好处是文件名更短。第三个好处是单独的目录可以帮助你检查每天是否都做了备份，因为只有在当天做了备份时才会创建该目录。

将其保存为 `backup_ver2.at`：

<Listing number="10-2" file-name="backup_ver2.auto" caption="备份脚本 - 版本 2（每日备份命名）">

```auto
use os
use time

fn main() {
    // 1. The files and directories to be backed up are
    // specified in a list.
    // Example on Windows:
    // source = ["C:\\My Documents", "C:\\Code"]
    // Example on Mac OS X and Linux:
    let source = ["/Users/swa/notes"]
    // Notice we had to use double quotes inside the string
    // for names with spaces in it.

    // 2. The backup must be stored in a
    // main backup directory
    // Example on Windows:
    // target_dir = "E:\\Backup"
    // Example on Mac OS X and Linux:
    let target_dir = "/Users/swa/backup"
    // Remember to change this to which folder you will be using

    // Create target directory if it is not present
    if !os.path.exists(target_dir) {
        os.mkdir(target_dir)  // make directory
    }

    // 3. The files are backed up into a zip file.
    // 4. The current day is the name of the subdirectory
    // in the main directory.
    let today = target_dir + os.sep + time.strftime("%Y%m%d")
    // The current time is the name of the zip archive.
    let now = time.strftime("%H%M%S")

    // The name of the zip file
    let target = today + os.sep + now + ".zip"

    // Create the subdirectory if it isn't already there
    if !os.path.exists(today) {
        os.mkdir(today)
        print("Successfully created directory", today)
    }

    // 5. We use the zip command to put the files in a zip archive
    let zip_command = f"zip -r $target ${source.join(' ')}"

    // Run the backup
    print("Zip command is:")
    print(zip_command)
    print("Running:")
    if os.system(zip_command) == 0 {
        print("Successful backup to", target)
    } else {
        print("Backup FAILED")
    }
}
```

```python
import os
import time


def main():
    # 1. The files and directories to be backed up are
    # specified in a list.
    # Example on Windows:
    # source = ["C:\\My Documents", "C:\\Code"]
    # Example on Mac OS X and Linux:
    source = ['/Users/swa/notes']
    # Notice we had to use double quotes inside the string
    # for names with spaces in it.

    # 2. The backup must be stored in a
    # main backup directory
    # Example on Windows:
    # target_dir = "E:\\Backup"
    # Example on Mac OS X and Linux:
    target_dir = '/Users/swa/backup'
    # Remember to change this to which folder you will be using

    # Create target directory if it is not present
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)  # make directory

    # 3. The files are backed up into a zip file.
    # 4. The current day is the name of the subdirectory
    # in the main directory.
    today = target_dir + os.sep + time.strftime('%Y%m%d')
    # The current time is the name of the zip archive.
    now = time.strftime('%H%M%S')

    # The name of the zip file
    target = today + os.sep + now + '.zip'

    # Create the subdirectory if it isn't already there
    if not os.path.exists(today):
        os.mkdir(today)
        print('Successfully created directory', today)

    # 5. We use the zip command to put the files in a zip archive
    zip_command = f"zip -r {target} {' '.join(source)}"

    # Run the backup
    print('Zip command is:')
    print(zip_command)
    print('Running:')
    if os.system(zip_command) == 0:
        print('Successful backup to', target)
    else:
        print('Backup FAILED')


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ a2p backup_ver2.at && python backup_ver2.py
Successfully created directory /Users/swa/backup/20140329
Zip command is:
zip -r /Users/swa/backup/20140329/073201.zip /Users/swa/notes
Running:
  adding: Users/swa/notes/ (stored 0%)
  adding: Users/swa/notes/blah1.txt (stored 0%)
  adding: Users/swa/notes/blah2.txt (stored 0%)
  adding: Users/swa/notes/blah3.txt (stored 0%)
Successful backup to /Users/swa/backup/20140329/073201.zip
```

**工作原理**

程序的大部分保持不变。变化之处在于我们使用 `os.path.exists` 函数检查主备份目录中是否存在以当天日期命名的子目录。如果不存在，我们使用 `os.mkdir` 函数创建它。

## 第三版

第二版在我做多次备份时工作良好，但当备份很多时，我发现很难区分每个备份是做什么用的！例如，我可能对某个程序或演示文稿做了重大修改，然后我想将这些修改的内容与 zip 归档文件的名称关联起来。这可以通过将用户提供的注释附加到 zip 归档文件名中来轻松实现。

> **警告：** 下面的程序不能正常工作，所以请不要惊讶，请继续阅读，因为这里有一个教训。

将其保存为 `backup_ver3.at`：

<Listing number="10-3" file-name="backup_ver3.auto" caption="备份脚本 - 版本 3（带用户注释 - 有 BUG！）">

```auto
use os
use time

fn main() {
    // 1. The files and directories to be backed up are
    // specified in a list.
    // Example on Windows:
    // source = ["C:\\My Documents", "C:\\Code"]
    // Example on Mac OS X and Linux:
    let source = ["/Users/swa/notes"]
    // Notice we had to use double quotes inside the string
    // for names with spaces in it.

    // 2. The backup must be stored in a
    // main backup directory
    // Example on Windows:
    // target_dir = "E:\\Backup"
    // Example on Mac OS X and Linux:
    let target_dir = "/Users/swa/backup"
    // Remember to change this to which folder you will be using

    // Create target directory if it is not present
    if !os.path.exists(target_dir) {
        os.mkdir(target_dir)  // make directory
    }

    // 3. The files are backed up into a zip file.
    // 4. The current day is the name of the subdirectory
    // in the main directory.
    let today = target_dir + os.sep + time.strftime("%Y%m%d")
    // The current time is the name of the zip archive.
    let now = time.strftime("%H%M%S")

    // Take a comment from the user to
    // create the name of the zip file
    let comment = input("Enter a comment --> ")
    // Check if a comment was entered
    if comment.len() == 0 {
        let target = today + os.sep + now + ".zip"
    } else {
        // BUG: This line is split across two lines without
        // a continuation character, causing a SyntaxError!
        let target = today + os.sep + now + "_" +
            comment.replace(" ", "_") + ".zip"
    }

    // Create the subdirectory if it isn't already there
    if !os.path.exists(today) {
        os.mkdir(today)
        print("Successfully created directory", today)
    }

    // 5. We use the zip command to put the files in a zip archive
    let zip_command = f"zip -r $target ${source.join(' ')}"

    // Run the backup
    print("Zip command is:")
    print(zip_command)
    print("Running:")
    if os.system(zip_command) == 0 {
        print("Successful backup to", target)
    } else {
        print("Backup FAILED")
    }
}
```

```python
import os
import time


def main():
    # 1. The files and directories to be backed up are
    # specified in a list.
    # Example on Windows:
    # source = ["C:\\My Documents", "C:\\Code"]
    # Example on Mac OS X and Linux:
    source = ['/Users/swa/notes']
    # Notice we had to use double quotes inside the string
    # for names with spaces in it.

    # 2. The backup must be stored in a
    # main backup directory
    # Example on Windows:
    # target_dir = "E:\\Backup"
    # Example on Mac OS X and Linux:
    target_dir = '/Users/swa/backup'
    # Remember to change this to which folder you will be using

    # Create target directory if it is not present
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)  # make directory

    # 3. The files are backed up into a zip file.
    # 4. The current day is the name of the subdirectory
    # in the main directory.
    today = target_dir + os.sep + time.strftime('%Y%m%d')
    # The current time is the name of the zip archive.
    now = time.strftime('%H%M%S')

    # Take a comment from the user to
    # create the name of the zip file
    comment = input('Enter a comment --> ')
    # Check if a comment was entered
    if len(comment) == 0:
        target = today + os.sep + now + '.zip'
    else:
        # BUG: This line is split across two lines without
        # a continuation character, causing a SyntaxError!
        target = today + os.sep + now + '_' +
            comment.replace(' ', '_') + '.zip'

    # Create the subdirectory if it isn't already there
    if not os.path.exists(today):
        os.mkdir(today)
        print('Successfully created directory', today)

    # 5. We use the zip command to put the files in a zip archive
    zip_command = f"zip -r {target} {' '.join(source)}"

    # Run the backup
    print('Zip command is:')
    print(zip_command)
    print('Running:')
    if os.system(zip_command) == 0:
        print('Successful backup to', target)
    else:
        print('Backup FAILED')


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ a2p backup_ver3.at && python backup_ver3.py
  File "backup_ver3.py", line 39
    target = today + os.sep + now + '_' +
                                        ^
SyntaxError: invalid syntax
```

**为什么这个程序不能工作**

*这个程序不能正常工作！* Python 提示有语法错误，这意味着脚本不符合 Python 期望的结构。当我们观察 Python 给出的错误时，它还告诉我们检测到错误的位置。所以我们从那行开始*调试*程序。

仔细观察后，我们发现一条逻辑行被拆分成了两条物理行，但我们没有指定这两条物理行属于同一个逻辑行。基本上，Python 在逻辑行中找到了加法运算符（`+`）但没有操作数，因此它不知道如何继续。请记住，我们可以通过在物理行末尾使用反斜杠来指定逻辑行在下一行继续。所以，我们对程序进行这个修正。发现错误时对程序进行修正称为*修复 bug*。

> **Auto 程序员注意：**
>
> 这是一个很好的例子，展示了 Auto 相对于 Python 的一个设计优势。在 Auto 中，语句以 `}`（对于代码块）结束，或者以块内自然的行边界结束，因此像这样的行续行问题根本不会出现。Auto 基于 `{}` 的代码块语法清楚地标明了语句的开始和结束。版本 4 的代码将展示如何在 Auto 中使用 `if/else` 表达式更优雅地修复这个问题。

## 第四版

将其保存为 `backup_ver4.at`：

<Listing number="10-4" file-name="backup_ver4.auto" caption="备份脚本 - 版本 4（修复了用户注释功能）">

```auto
use os
use time

fn main() {
    // 1. The files and directories to be backed up are
    // specified in a list.
    // Example on Windows:
    // source = ["C:\\My Documents", "C:\\Code"]
    // Example on Mac OS X and Linux:
    let source = ["/Users/swa/notes"]
    // Notice we had to use double quotes inside the string
    // for names with spaces in it.

    // 2. The backup must be stored in a
    // main backup directory
    // Example on Windows:
    // target_dir = "E:\\Backup"
    // Example on Mac OS X and Linux:
    let target_dir = "/Users/swa/backup"
    // Remember to change this to which folder you will be using

    // Create target directory if it is not present
    if !os.path.exists(target_dir) {
        os.mkdir(target_dir)  // make directory
    }

    // 3. The files are backed up into a zip file.
    // 4. The current day is the name of the subdirectory
    // in the main directory.
    let today = target_dir + os.sep + time.strftime("%Y%m%d")
    // The current time is the name of the zip archive.
    let now = time.strftime("%H%M%S")

    // Take a comment from the user to
    // create the name of the zip file
    let comment = input("Enter a comment --> ")
    // Check if a comment was entered
    let target = if comment.len() == 0 {
        today + os.sep + now + ".zip"
    } else {
        today + os.sep + now + "_" +
            comment.replace(" ", "_") + ".zip"
    }

    // Create the subdirectory if it isn't already there
    if !os.path.exists(today) {
        os.mkdir(today)
        print("Successfully created directory", today)
    }

    // 5. We use the zip command to put the files in a zip archive
    let zip_command = f"zip -r $target ${source.join(' ')}"

    // Run the backup
    print("Zip command is:")
    print(zip_command)
    print("Running:")
    if os.system(zip_command) == 0 {
        print("Successful backup to", target)
    } else {
        print("Backup FAILED")
    }
}
```

```python
import os
import time


def main():
    # 1. The files and directories to be backed up are
    # specified in a list.
    # Example on Windows:
    # source = ["C:\\My Documents", "C:\\Code"]
    # Example on Mac OS X and Linux:
    source = ['/Users/swa/notes']
    # Notice we had to use double quotes inside the string
    # for names with spaces in it.

    # 2. The backup must be stored in a
    # main backup directory
    # Example on Windows:
    # target_dir = "E:\\Backup"
    # Example on Mac OS X and Linux:
    target_dir = '/Users/swa/backup'
    # Remember to change this to which folder you will be using

    # Create target directory if it is not present
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)  # make directory

    # 3. The files are backed up into a zip file.
    # 4. The current day is the name of the subdirectory
    # in the main directory.
    today = target_dir + os.sep + time.strftime('%Y%m%d')
    # The current time is the name of the zip archive.
    now = time.strftime('%H%M%S')

    # Take a comment from the user to
    # create the name of the zip file
    comment = input('Enter a comment --> ')
    # Check if a comment was entered
    if len(comment) == 0:
        target = today + os.sep + now + '.zip'
    else:
        target = today + os.sep + now + '_' + \
            comment.replace(' ', '_') + '.zip'

    # Create the subdirectory if it isn't already there
    if not os.path.exists(today):
        os.mkdir(today)
        print('Successfully created directory', today)

    # 5. We use the zip command to put the files in a zip archive
    zip_command = f"zip -r {target} {' '.join(source)}"

    # Run the backup
    print('Zip command is:')
    print(zip_command)
    print('Running:')
    if os.system(zip_command) == 0:
        print('Successful backup to', target)
    else:
        print('Backup FAILED')


if __name__ == "__main__":
    main()
```

</Listing>

输出：

```
$ a2p backup_ver4.at && python backup_ver4.py
Enter a comment --> added new examples
Zip command is:
zip -r /Users/swa/backup/20140329/074122_added_new_examples.zip /Users/swa/notes
Running:
  adding: Users/swa/notes/ (stored 0%)
  adding: Users/swa/notes/blah1.txt (stored 0%)
  adding: Users/swa/notes/blah2.txt (stored 0%)
  adding: Users/swa/notes/blah3.txt (stored 0%)
Successful backup to /Users/swa/backup/20140329/074122_added_new_examples.zip
```

**工作原理**

这个程序现在可以正常工作了！让我们看看在版本 3 中所做的实际改进。我们使用 `input` 函数获取用户的注释，然后使用 `len` 函数（在 Auto 中写为字符串上的 `.len()`）检查用户是否实际输入了内容。如果用户只是按了回车键而没有输入任何内容（也许只是常规备份或没有做特殊修改），那么我们就像之前一样处理。

但是，如果提供了注释，那么这个注释会附加到 zip 归档文件名中，在 `.zip` 扩展名之前。请注意，我们将注释中的空格替换为下划线——这是因为没有空格的文件名更容易管理。

请注意我们如何修复了版本 3 中的 bug。在 Auto 代码中，我们使用 `if/else` 表达式直接赋值给 `let target`，这完全避免了行续行的问题。`a2p` 转译器将此转换为带有反斜杠续行的标准 Python `if/else` 语句。这是一个展示 Auto 语法如何帮助你避免常见 Python 陷阱的例子。

## 更多改进

第四版对于大多数用户来说已经是一个令人满意的脚本，但总有改进的空间。例如，你可以通过指定 `-v` 选项来增加 zip 命令的*详细*程度，让你的程序更健谈，或者使用 `-q` 选项让它*安静*。

另一个可能的改进是允许在命令行将额外的文件和目录传递给脚本。我们可以从 `sys.argv` 列表中获取这些名称，并使用 `list` 类提供的 `extend` 方法将它们添加到我们的 `source` 列表中。

最重要的改进是不使用 `os.system` 的方式来创建归档，而是使用 [zipfile](http://docs.python.org/3/library/zipfile.html) 或 [tarfile](http://docs.python.org/3/library/tarfile.html) 内置模块来创建这些归档。它们是标准库的一部分，已经可供你使用，无需依赖计算机上安装的 zip 程序。

但是，在上面的例子中，我纯粹出于教学目的使用了 `os.system` 的方式来创建备份，这样示例足够简单以便每个人都能理解，同时也足够真实以具有实用性。

你能尝试编写使用 [zipfile](http://docs.python.org/3/library/zipfile.html) 模块而不是 `os.system` 调用的第五版吗？

## 软件开发过程

我们现在已经经历了编写软件的各种*阶段*。这些阶段可以总结如下：

1. 是什么（分析）
2. 怎么做（设计）
3. 开始做（实现）
4. 测试（测试和调试）
5. 使用（运行或部署）
6. 维护（改进）

推荐的编写程序的方法是我们在创建备份脚本时遵循的过程：进行分析和设计。从简单版本开始实现。测试并调试它。使用它以确保按预期工作。现在，添加你想要的任何功能，并根据需要继续重复"实现-测试-使用"循环。

请记住：

> 软件是生长出来的，而不是构建出来的。
> -- [Bill de hOra](http://97things.oreilly.com/wiki/index.php/Great_software_is_not_built,_it_is_grown)

## 小结

我们已经学习了如何创建自己的 Auto 程序/脚本，以及编写此类程序所涉及的各个阶段。你可能会发现，像我们在本章中所做的那样创建自己的程序会很有用，这样你就能更加熟悉 Auto 和解决问题。

本章的关键要点：

- **`use` 导入 Python 模块** -- Auto 可以通过 `use` 关键字使用 Python 的标准库模块，如 `os`、`time` 和 `sys`。`a2p` 转译器会将它们转换为 `import` 语句。
- **`os.system()`** -- 运行一个 shell 命令并返回退出码。返回值为 `0` 表示成功。
- **`os.sep`** -- 操作系统特定的路径分隔符（Unix 上为 `/`，Windows 上为 `\\`）。
- **`os.path.exists()`** 和 **`os.mkdir()`** -- 检查目录是否存在以及创建目录。
- **`time.strftime()`** -- 将日期和时间格式化为字符串。
- **`input()`** -- 从控制台读取用户输入。
- **`.len()`** -- 获取字符串的长度（Auto 风格；Python 使用 `len()`）。
- **`.replace()`** -- 替换字符串中的子串。
- **`.join()`** -- 使用分隔符将列表元素连接为字符串。
- **f-string 中的 `$var`** -- Auto 的字符串插值语法，转译为 Python 的 f-string `{var}` 语法。
- **`if/else` 表达式** -- Auto 支持 `if/else` 作为返回值的表达式，有助于避免缺少行续行符等常见 bug。

接下来，我们将学习数据结构。
