# 第一部分：Auto 基础与数据塑形

## 第 1 章：起步 (Getting Started)

开启一门全新语言的学习之旅，往往伴随着复杂的环境配置和冗长的构建等待。但在 Auto 的世界里，一切都被精简到了极致。Auto 的工具链设计秉承了“开箱即用、双栖运行”的微内核哲学。

在本章中，我们将安装 Auto 工具链，配置现代化的编辑器环境，编写并运行那个属于程序员的古老传统——“Hello, World!”。最后，我们将向你展示 Auto 生态中最具革命性的文档交互技术：AutoDown。

### 1.1 安装与核心工具链 (`auto` 统一终端)

Auto 的底层由两个极其硬核的引擎组成：`autoc`（AOT 前端编译器）和 `autovm`（极速微内核运行时）。但为了提供对标顶级脚本语言的丝滑体验，我们将这一切极其克制地收敛在了一个超级终端入口中：**`auto` CLI**。

#### 安装命令行工具
无论你使用何种操作系统，我们都提供了极简的一键安装脚本。

**在 Linux 或 macOS 上：**
打开终端，输入以下命令（它会将二进制文件安全地存放在 `~/.auto/bin` 目录下）：
```bash
curl --proto '=https' --tlsv1.2 -sSf https://auto-lang.cn/autoup.sh | sh
```

**在 Windows 上：**
打开 PowerShell 并运行：
```powershell
Invoke-WebRequest -Uri https://auto-cn.org/autoup.ps1 -OutFile autoup.ps1; .\autoup.ps1
```

安装完成后，重启终端，验证这台双擎驱动的终端是否已准备就绪：
```bash
$ auto --version
auto 1.0.0 (Microkernel Ready & AOT Engine a3f8b9c)
```



#### 现代语言的标配：编辑器支持 (IDE & LSP)
在 2026 年，一门没有顶级智能提示的语言只能被称为玩具。Auto 原生提供了一个极度强悍的语言服务器（Language Server Protocol, LSP）后端引擎。

你不需要进行任何复杂的配置，只需在 **VS Code** 或 **DevEco Studio** 的扩展商店中搜索并安装 **`Auto Language Support`** 插件即可。
这套 LSP 引擎不仅提供实时的语法高亮和毫秒级的自动补全，它甚至会在你敲击键盘的瞬间，在后台进行**极其严苛的逃逸分析与所有权推导**。如果你的代码存在内存隐患，编辑器会立刻用红色的波浪线将你“击毙”在编写阶段。

---

### 1.2 Hello, Auto! (第一个程序的物理剖析)

现在，让我们编写第一个 Auto 程序。找一个你喜欢的目录，新建一个名为 `hello` 的文件夹。在里面创建一个名为 `main.at` 的文件（`.at` 是 Auto 语言极简、干脆的专属后缀），并输入以下代码：

```auto
fn main() ! {
    let target = "Auto"
    print("Hello, " + target + "!")
}
```

保存文件后，在终端中输入以下命令来“点火”执行：

```bash
$ auto main.at
Hello, Auto!
```

恭喜！你刚刚成功触发了底层的 AutoVM 微内核，并在极其安全的沙盒中打印出了这句问候。

让我们像外科医生一样，迅速解剖这段仅仅 4 行代码背后的物理真相：

* **`fn main()` 的家主地位**：在 C++ 或 Java 中，`main` 只是一个普通的入口函数。但在 Auto 中，`main` 是整个 Actor 宇宙的**“创世进程”**。在底层的物理意义上，`main` 运行在隔离的主线程中。它的职责是部署资源、派生（Spawn）其他的 Task，并在一切就绪后劫持当前线程，将控制权彻底移交给底层的 Tokio 调度系统。
* **`!` (错误传播签名)**：`main()` 后面跟着一个极其醒目的惊叹号 `!`。为什么不用传统的 `try/catch`？因为 Auto 认为异常不应该是被隐藏的控制流。`!` 向编译器和 AI 宣告：“这个函数可能会发生致命错误，并具有向上抛出的能力”。即使是系统最顶层的 `main` 函数，也必须直面失败的可能。这体现了 Auto 对系统级安全的绝对偏执。
* **`let target = ...` 的不可变契约**：在 Auto 中，默认使用 `let` 声明变量，这意味着它是**绝对不可变（Immutable）**的。这不仅仅是一个语法糖，更是并发安全的物理保障。因为不可变，这块内存在被传入其他 Task 的信箱时，底层甚至不需要进行深度拷贝（Deep Copy），真正实现了多核时代的零成本数据共享。
* **`print(...)` 的跨界呼叫**：这是一个极其底层的 Native 系统调用接口。当底层引擎解释到这一行时，它穿越了虚拟机的物理边界，通过 FFI（外部函数接口）直接调用了宿主操作系统的标准输出流。

#### 编译为终极形态 (AOT 模式)
如果你想把这个程序部署到没有安装 Auto 环境的服务器上，只需通过 `auto build` 呼叫重型武器（底层会自动路由给 `autoc`）：

```bash
$ auto build main.at
Compiling main.at (AOT Mode)...
Finished release target(s) in 0.82s
```
这会在当前目录下生成一个名为 `main`（或 `main.exe`）的纯粹的机器码二进制文件。它不依赖任何外部运行时，其运行速度与底层 C/Rust 代码完全一致。同一套语义，极速脚本与裸机原生的形态切换，仅仅是一条命令的距离。

---

### 1.3 基于 AutoDown 的在线交互式编程 (Playground)

如果你正在通过网页（或者我们官方的桌面应用）阅读这本《The Auto Programming Language》，那么你其实已经置身于 Auto 生态中最强大的基础设施之一：**AutoDown**。

传统的编程书籍要求你一边看书，一边在终端里痛苦地复制粘贴代码，经常因为少复制了一个大括号而报错。而 Auto 语言主张**“零摩擦的求知欲”**。

作为作者，我们只需要在编写 Markdown 文档时，在代码块的语言标记后加上一个极其简单的 `run` 指令。AutoDown 的底层微型编译器会瞬间将其降级为 AURA 声明式 UI 组件，并在你的眼前渲染出一个带高亮的交互式编辑器。

**现在，请在下面的编辑器中亲自尝试！**
点击代码框右下角的 **"Run"** 按钮。你甚至可以随意修改第二行的字符串，然后再次运行。

```auto run
fn main() ! {
    let planet = "Auto"
    print("Hello, " + planet + " from the interactive Playground!")
}
```

#### 为 AI 与人类共同设计的错误报告
既然可以随意修改，那如果你写错了代码怎么办？
请尝试把上面代码中的 `let planet` 改成 `var planet`（声明为可变变量），但是在后续的代码中却**不去做任何修改**。点击运行，看看会发生什么。

你会看到虚拟终端中弹出了这样一条极其清晰的错误信息：

```rust
[Auto Compiler Error]
 --> main.at:2:9
  |
2 |     var planet = "Auto"
  |     ^^^ 
  |
Error: Variable `planet` is declared as mutable (`var`), but is never mutated.
Hint: To enforce strict safety and optimize memory layout, please change `var` to `let`.
```

当这串代码通过 HTTP 或 IPC 飞向后端的 Rust 沙盒舱时，引擎会进行极其严苛的语义分析。Auto 的错误信息经过了特殊设计，它不仅准确指出物理位置（行号与列标），还会给出**确切的修复建议 (Hint)**。这种极高的“信噪比”不仅让初学者如沐春风，更是让辅助你写代码的 AI 智能体（Agent）能够一次性看懂报错并自动修正代码。

这就是“语言即 AI 操作系统”的冰山一角。你敲下的每一行代码，都在被这个微内核极其温柔地保护着。
