# 安装

在本书中，当我们提到 "Python 3" 时，指的是任何等于或大于 [Python 3.10](https://www.python.org/downloads/) 的版本。

## 安装 Auto

Auto 工具链包括 `autoc` 编译器和 `automan` 包管理器。由于本书侧重于将 Auto 代码转译为 Python，你还需要安装 `a2p` 转译器。

### Linux 或 macOS

打开终端并运行：

```console
$ curl --proto '=https' https://sh.auto.dev | sh
```

此命令会下载一个脚本并安装 Auto 工具链。系统可能会提示你输入密码。

接下来，使用 automan 安装 `a2p` 转译器：

```console
$ automan install a2p
```

### Windows

访问 Auto 网站 <https://auto.dev> 下载 Windows 安装程序。运行安装程序并按照屏幕上的说明操作。

> **注意：** 确保在安装过程中勾选将 Auto 添加到系统 `PATH` 的选项。

安装工具链后，安装 `a2p` 转译器：

```console
> automan install a2p
```

## 安装 Python

由于本书使用 `a2p` 将 Auto 代码转译为 Python，你的系统需要安装 Python 3.10 或更高版本。

### Linux

使用你的发行版的包管理器。例如，在 Debian 和 Ubuntu 上：

```console
$ sudo apt-get update && sudo apt-get install python3
```

### macOS

使用 [Homebrew](https://brew.sh)：

```console
$ brew install python3
```

### Windows

从 <https://www.python.org/downloads/> 下载 Python 并运行安装程序。

> **注意：** 确保在安装过程中勾选 `Add Python to PATH` 选项。

## 验证安装

打开终端（Windows 上为命令提示符）并运行以下命令，验证所有工具是否安装正确：

```console
$ autoc --version
```

你应该能看到版本号，例如：

```text
autoc 1.0.0 (2025-01-01)
```

```console
$ a2p --version
```

```console
$ python3 --version
```

你应该能看到类似这样的输出：

```text
Python 3.12.0
```

> **提示：** `$` 是 shell 的提示符。根据你的操作系统设置，它可能会有所不同，因此我用 `$` 符号来表示提示符。在 Windows 上，你可能会看到 `>` 提示符。

> **注意：** 你的计算机上的输出可能有所不同，具体取决于所安装软件的版本。

## 构建代码清单

在本书中，你会遇到可以编译和运行的代码清单。每个清单都是一个 Auto 源文件，可以使用 `a2p` 转译器转译为 Python。

要构建清单，导航到清单所在的目录并运行：

```console
$ auto b
```

此命令会将 Auto 代码转译为 Python 并运行生成的 Python 文件。如果遇到任何错误，请确保 `autoc` 和 `python3` 都已正确安装，并且可以从你的终端访问。

## 小结

从现在开始，我们假定你的系统上已安装 Auto 工具链和 Python 3.10+。

接下来，我们将编写我们的第一个 Auto 程序。
