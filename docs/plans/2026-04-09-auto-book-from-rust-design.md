# Auto Book from Rust — 设计文档

**日期：** 2026-04-09
**项目：** 基于 Rust 书生成 Auto 语言书籍
**输出目录：** `d:\autostack\book\rust\`

---

## 1. 项目概述

基于《The Rust Programming Language》官方书籍的结构和内容，生成一本 Auto 语言的入门教程。Auto 是一门由 Rust 实现的系统级语言，两门语言在底层模型上有较多共通之处，但在语法表面和部分范式上有显著差异。

**核心策略：** 严格对齐 Rust 书的 21 章结构，逐章逐段地将 Rust 概念翻译为 Auto 概念，保留双语文本和并排代码展示。

---

## 2. 文件组织结构

```
rust/
├── SUMMARY.md                          # 书籍目录
├── title-page.md                       # 标题页
├── foreword.md                         # 前言
├── ch00-introduction.md                # 英文版：Auto 简介
├── ch00-introduction.cn.md             # 中文版：Auto 简介
├── ch01-getting-started.md             # 包含 1.1-1.3 所有节
├── ch01-getting-started.cn.md
├── ch02-guessing-game.md
├── ch02-guessing-game.cn.md
├── ch03-common-concepts.md
├── ch03-common-concepts.cn.md
├── ...（每章一个 .md + .cn.md）
└── listings/                           # 代码清单
    ├── ch01/
    ├── ch02/
    ├── ch03/
    └── ...（每章一个目录）
```

**规则：**
- 每章一个 `.md` 文件（英文）+ 一个 `.cn.md` 文件（中文）
- 文件内用二级标题（`##`）分隔各节
- 代码清单按章组织在 `listings/` 目录下

---

## 3. 代码清单处理

### 3.1 展示方式

每个代码清单包含 Rust 和 Auto 两个版本：

````markdown
```rust
fn main() {
    println!("Hello, world!");
}
```

```auto
fn main() ! {
    print("Hello, world!")
}
```
````

### 3.2 JS 并排展示（后续实现）

- 用 `<div class="code-compare">` 包裹代码对
- JS 渲染为左右并排或标签切换
- 未来扩展时只需加更多语言块（Python, Go 等）

### 3.3 映射原则

- Rust API 需找到 Auto 等价写法
- 暂时找不到映射的，用 `// TODO: 待映射` 占位
- 代码清单文件保持与 Rust 一致的命名

---

## 4. Rust→Auto 章节映射

### 4.1 前 10 章详细映射

| Rust 章 | 标题 | Auto 对应 | 处理策略 |
|---------|------|----------|---------|
| Ch0 | Introduction | Auto 简介与哲学 | 重写为 Auto 介绍 |
| Ch1 | Getting Started | 安装 autoc/autovm | 结构相同，工具名替换 |
| Ch2 | Guessing Game | Auto 猜数字 | 结构相同，代码转 Auto |
| Ch3 | Common Concepts | 变量/类型/函数/控制流 | `mut`→`var`，去掉分号 |
| Ch4 | Ownership | Auto 内存模型 | **重点改编**：隐式 move + AutoFree |
| Ch5 | Structs | `type` 关键字 | `struct`→`type`，`impl`→`ext` |
| Ch6 | Enums & Matching | enum + `is` 语句 | `match`→`is`，`Option<T>`→`?T` |
| Ch7 | Packages/Modules | Auto 包管理 | Cargo→automan，模块对比 |
| Ch8 | Collections | List/HashMap/HashSet | `Vec<T>`→`List<T>` |
| Ch9 | Error Handling | `!T` 和 `?T` | `Result<T,E>`→`!T`，`panic!`→`panic()` |
| Ch10 | Generics/Traits/Lifetimes | 泛型 + spec + AutoFree | traits→spec，lifetimes→AutoFree |

### 4.2 后 11 章详细映射

| Rust 章 | 标题 | Auto 对应 | 处理策略 |
|---------|------|----------|---------|
| Ch11 | Testing | Auto 测试框架 | 结构相似，语法适配 |
| Ch12 | I/O Project | Auto CLI 项目 | 代码转 Auto |
| Ch13 | Closures & Iterators | Auto 闭包和迭代器 | `Fn`/`FnMut`→Auto 闭包语法 |
| Ch14 | Cargo & Crates.io | automan 包管理器 | 理论保留 + 占位符 |
| Ch15 | Smart Pointers | Auto 引用/指针 | **大幅改编** |
| Ch16 | Concurrency | Actor 并发 | **完全重写**：线程→task |
| Ch17 | Async/Await | `~T` 蓝图 + `on` 块 | 模型不同但概念对应 |
| Ch18 | OOP | `is`/`has`/`spec` | **核心章节** |
| Ch19 | Patterns & Matching | `is` 模式匹配 | `match`→`is` |
| Ch20 | Advanced Features | `sys`/comptime | unsafe→`sys`，macros→`#[]` |
| Ch21 | Web Server | Auto Web 项目 | Actor 模型重写 |
| 附录 | Keywords/Operators | Auto 关键字/符号 | 重写为 Auto 版本 |

### 4.3 关键概念映射速查表

| Rust 概念 | Auto 概念 | 备注 |
|-----------|----------|------|
| `let` / `let mut` | `let` / `var` | 默认不可变设计相同 |
| `struct` | `type` | Auto 用 `type` 关键字 |
| `impl` | `ext` | 行为挂载 |
| `trait` | `spec` | 规范定义 |
| `match` | `is` | 模式匹配 |
| `on` (事件处理) | `on` | 异步/UI 事件 |
| `Result<T, E>` | `!T` | 错误传播 |
| `Option<T>` | `?T` | 空值安全 |
| `async/await` | `~T` | 延迟执行/蓝图 |
| `unsafe` | `sys` | 底层操作 |
| `macro_rules!` | `#[]` comptime | 编译期执行 |
| `Cargo` | `automan` | 包管理器 |
| `ownership` | 隐式 move | Auto 隐式管理 |
| `lifetime` | AutoFree | 无需显式标注 |
| `Vec<T>` | `List<T>` | 动态数组 |
| `dyn Trait` | `spec`/`as` | 多态契约 |

---

## 5. AI 工作流程

### 5.1 标准作业步骤（每章）

```
Step 1: 读取 Rust 源文件
  → 读取 d:/book/rust/src/ 中对应章节的所有子文件
  → 读取对应 listings 目录

Step 2: 分析章节内容
  → 标注 Rust 特有 vs 通用概念
  → 确定代码清单映射关系
  → （复杂章节需与用户确认映射策略）

Step 3: 生成英文版 .md
  → 替换 Rust 概念为 Auto 概念
  → 保留 Rust 代码 + 添加 Auto 代码
  → 跳过无 Auto 对应的内容

Step 4: 生成中文版 .cn.md
  → 翻译英文版

Step 5: 处理代码清单
  → 复制 Rust 代码到 listings
  → 编写 .auto 对应文件
```

### 5.2 对话协作模式

- **简单章节**（Ch1, Ch3, Ch5）：一轮对话完成
- **复杂章节**（Ch4 Ownership, Ch10 Lifetimes）：先分析，确认策略，再分节生成
- **特殊章节**（Ch14 Cargo）：理论保留 + 占位符

### 5.3 优先级

从 Ch1 开始顺序推进。后面章节引用前面章节内容。

### 5.4 待详细讨论的章节

以下章节在编写时需要逐节讨论 Rust→Auto 的映射：
- **Ch4 Ownership** — Auto 的隐式 move 和 AutoFree 机制
- **Ch10 Lifetimes** — Auto 的 AutoFree 如何替代显式 lifetime
- **Ch16 Concurrency** — 从线程模型到 Actor 模型的完整映射
- **Ch18 OOP** — `is`/`has`/`spec` 三角关系 vs trait objects

---

## 6. Rust 特有内容处理规则

对于 Rust 有但 Auto 无直接对应的概念：

1. **Auto 有对应但实现不同**（如 lifetime→AutoFree）：保留 Rust 理论描述 + 说明 Auto 方案
2. **Auto 有对应功能但细节不同**（如 Cargo→automan）：保留理论 + 占位符，标注 `[TODO: automan 实现细节]`
3. **待讨论的概念**（如 trait objects）：单独对话确定映射策略
4. **Rust 纯生态内容**（如 Crates.io 发布流程）：保留理论框架 + 占位符

---

## 7. 参考资源

- Rust 书源码：`D:\book\rust\src\`（markdown），`D:\book\rust\listings\`（代码清单）
- Rust 书统计：78 个 .md 文件，~25,949 行，556 个代码清单目录
- Auto 已有书籍：`d:\autostack\book\src\`（独立 Auto 书，非本项目）
- Auto 书大纲：`d:\autostack\book\OUTLINE.md`（独立 Auto 书的大纲）
