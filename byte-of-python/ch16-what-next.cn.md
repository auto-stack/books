# 接下来做什么

如果你已经认真阅读了本书并练习编写了大量程序，你一定已经对 Auto 感到得心应手了。你可能已经编写了一些 Auto 程序来尝试各种功能和锻炼你的新技能。如果你还没有这样做，现在就开始吧。接下来的问题是"接下来做什么？"。

## 推荐项目

巩固所学知识的最佳方式就是构建真实的项目。以下是几个帮你入门的项目创意：

### 通讯录

创建一个命令行*通讯录*程序，你可以用它来浏览、添加、修改、删除或搜索你的联系人，例如朋友、家人和同事，以及他们的电子邮件地址和/或电话号码等信息。详细信息必须保存以便日后检索。

如果你回顾一下到目前为止我们学过的所有内容，这个项目其实相当简单——使用类来表示联系人信息，使用字典以姓名为键存储联系人，使用 `json` 或 `pickle` 模块将数据持久化到磁盘。

### 文件替换工具

实现一个命令行工具，在一系列文件中将一个字符串替换为另一个字符串。这个工具可以很简单，也可以很复杂——从简单的字符串替换到使用正则表达式搜索模式，随你决定。

### 简单网页抓取器

使用 `urllib` 模块（或第三方 `requests` 库）获取网页并从中提取有用信息。你可以抓取天气数据、新闻标题或书籍价格——任何你感兴趣的内容。

### 命令行计算器

构建一个从命令行读取表达式并求值的计算器。从基本算术开始，然后添加对变量、函数的支持，甚至可以处理运算符优先级。

如果你觉得这些项目太简单，这里还有一些更多的创意和综合项目列表供你探索：

- [Exercises for Programmers: 57 Challenges to Develop Your Coding Skills](https://pragprog.com/book/bhwb/exercises-for-programmers)
- [Intermediate Python Projects](https://openhatch.org/wiki/Intermediate_Python_Workshop/Projects)
- [GitHub 上的项目列表](https://github.com/thekarangoel/Projects#numbers)

## 进一步探索 Auto

Auto 不仅仅是一个单语言工具。它独特的优势之一是能够转译到多种目标语言。以下是一些值得探索的方向：

### 使用 a2r 转译为 Rust

`a2r` 转译器将 Auto 代码转换为地道的 Rust。这让你在享受 Auto 友好语法的同时，获得 Rust 的性能和安全保证。如果你需要高性能或想要发布系统级软件，a2r 是前进的道路。

### 使用 a2ts 转译为 TypeScript

`a2ts` 转译器将 Auto 代码转换为 TypeScript，为你打开整个 JavaScript 生态系统的大门。用它来构建 Web 前端、Node.js 后端或全栈应用——全部使用单一、一致的语言编写。

### 使用 a2c 转译为 C

`a2c` 转译器将 Auto 代码转换为 C。当你需要面向嵌入式系统、操作系统或任何以 C 为标准的环境时，这非常有用。Auto 让你编写安全的高级代码，编译为高效的 C 代码。

### 本系列的其他书籍

Auto 有不断增长的书籍集合，面向不同背景和目标语言。寻找其他"A Byte of Auto"系列书籍，通过不同的转译目标和高级主题继续你的学习之旅。

## 进一步探索 Python

由于 Auto 转译为 Python，你学到的所有 Python 知识都直接适用于你的 Auto 程序。以下是几个值得探索的领域：

### 使用 Flask 进行 Web 开发

[Flask](http://flask.pocoo.org) 是一个轻量级的 Python Web 框架。它是构建 Web 应用程序的绝佳起点。一些资源：

- [Flask 官方快速入门](http://flask.pocoo.org/docs/quickstart/)
- [Flask 超级教程](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

### 数据科学

Python 是数据科学和机器学习领域的主导语言。值得探索的关键库：

- [NumPy](https://numpy.org) -- 数值计算
- [Pandas](https://pandas.pydata.org) -- 数据处理和分析
- [Matplotlib](https://matplotlib.org) -- 数据可视化

### 测试

编写测试是每个程序员的关键技能。Python 拥有出色的测试工具：

- **pytest** -- 一个强大、灵活的测试框架
- **unittest** -- Python 内置的测试模块（在 Auto 中可通过 `use unittest` 使用）

### 使用 pip 进行包管理

[Python 包索引 (PyPI)](https://pypi.org) 托管着数十万个第三方包。使用 [pip](https://pip.pypa.io) 来安装和管理这些包：

```
$ pip install requests
```

### 虚拟环境

在处理多个项目时，使用虚拟环境是一种好习惯，这样每个项目都有自己的依赖集合。Python 内置的 `venv` 模块让这变得很容易：

```
$ python -m venv myproject_env
$ source myproject_env/bin/activate  (Linux/macOS)
$ myproject_env\Scripts\activate     (Windows)
```

## 延伸阅读

以下是一些继续你的编程之旅的资源：

- [Python 官方文档](https://docs.python.org/3/) -- Python 的权威参考
- [Python 包索引 (PyPI)](https://pypi.org) -- 查找和安装第三方库
- [Automate the Boring Stuff with Python](https://automatetheboringstuff.com) -- 面向初学者的实用 Python 项目
- [Python Module of the Week](https://pymotw.com/3/) -- 标准库模块的深度指南
- [The Hitchhiker's Guide to Python!](https://docs.python-guide.org/) -- 最佳实践和 Python 风格指南

## 小结

我们现在已经到了本书的结尾，但正如人们所说，这是*结束的开始*。你现在是一名 Auto 程序员，准备好解决许多问题了。你可以自动化你的计算机来完成各种以前难以想象的事情，构建 Web 应用程序，分析数据，或将代码转译为 Rust、TypeScript 或 C 以在任何环境中部署。

现在最重要的是继续练习。选择一个让你兴奋的项目并开始构建。你写的每一行代码都会让你成为一个更好的程序员。

所以，开始行动吧！
