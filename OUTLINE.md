# The Auto Programming Language (TAPL)

## 前言：语言即AI操作系统 (Language as AIOS)
* **Auto 的诞生哲学**：极速热重载、零 GC、并发原生。
* **微内核视角的编程**：Task、Mailbox 与 AutoVM 的核心隐喻。
* **AOT 与 VM 的物理对齐**：同一套语义，两种极致形态。
* **AI原生**：Auto是一门AI生成为主的语言。

---

## 第一部分：Auto 基础与数据塑形 (The Basics & Data Shaping)

### 第 1 章：起步 (Getting Started)
* 1.1 安装与工具链 (`autoc` 与 `autovm`)
* 1.2 Hello, Auto! (第一个程序)
* 1.3 基于 AutoDown 的在线交互式编程 (Playground)

### 第 2 章：通用编程概念与智能流控 (Concepts & Smart Control Flow)
* 2.1 变量与常量：`let` 与 `var`
* 2.2 基础标量类型与表达式
* 2.3 函数签名与基本控制流 (`while`, `for`)
* **2.4 动态嗅探与智能流控 (Smart Casts)**：
    * `if x is T` 模式：流敏感推导（Flow-Sensitive Typing），分支内自动安全降维。
    * 联合类型 (Sum Types: `T | U`) 的极速拆箱与匹配。

### 第 3 章：复合类型与集合
* 3.1 连续内存布局：定长数组 `[]T`
* 3.2 动态堆分配：`List<T>` 与底层扩容机制
* 3.3 多维数组：`grid`
* 3.4 对象：`object`
* 3.5 节点：`node`
* 3.6 哈希映射：`HashMap`
* 3.7 集合：`HashSet`

### 第 4 章：引用与指针

* 4.1 只读引用 `view T`
* 4.2 可变引用 `mut T`
* 4.3 裸指针 `*T`：突破安全边界的物理探针

### 第 4 章：面向对象的解构与重塑 (Object-Oriented Reshaping)
*(注：本章是 Auto 语言表达力的巅峰，深度解析 `is`、`has`、`as` 黄金三角)*
* **4.1 数据容器的极简美学 (`type`)**：换行符推导、隐式 `let` 与默认构造。
* **4.2 `is` 关键字：物理层面的单继承 (The "Is-A" Relationship)**
    * 语法表达：`type Hawk is Bird { ... }`
    * 底层真相：内存布局的首部对齐与零开销指针强转。
* **4.3 `has` 关键字：带魔法的组合 (The "Has-A" Relationship)**
    * 语法表达：`type Person has Hand { ... }`
    * 革新性设计：编译器自动生成隐式字段，并**自动代理转发（Delegation）**目标类型的所有公开接口。彻底消除样板代码！
* **4.4 `spec` 与 `as` 关键字：多态契约与实现 (The "Conforms-To" Relationship)**
    * `spec`：定义能力规范（取代传统的 Interface/Trait）。
    * `as` 的内部实现：声明时直接履约（`type File as Reader { ... }`）。
    * 动态分发表（VTable）的生成与胖指针结构。
* **4.5 `ext` 关键字：行为挂载与事后扩展 (Behavior Extension)**
    * 数据与行为的彻底解耦：使用 `ext` 为现有类型追加方法。
    * 孤儿规则与外部实现：强行让第三方类型符合规范（`ext File as Reader { ... }`）。

---

## 第二部分：类型系统与核心范式 (Type System & Core Paradigm)

### 第 5 章：三大终极修饰符类型 (`!T`, `?T`, `~T`)
* 5.1 绝对的空值安全：`?T` 与可选链
* 5.2 优雅的错误传播：`!T` 与结尾的 `!` 抛出
* 5.3 时间的魔法：`~T` 蓝图与延迟执行

### 第 6 章：泛型与多态 (Generics & Polymorphism)
* 6.1 泛型函数与泛型结构体
* 6.2 结合 `spec` 的特征约束 (Trait Bounds)
* 6.3 编译期单态化 (Monomorphization)：零开销抽象

### 第 7 章：内存模型与隐式所有权 (Memory & Implicit Move)
* 7.1 逃逸分析与栈/堆决断
* 7.2 隐式 Move 语义：跨作用域的绝对交接
* 7.3 瞬时生命周期与零 GC 原理

---

## 第三部分：并发微内核与元编程 (Concurrency & Metaprogramming)

### 第 8 章：Actor 并发模型 (The Actor Concurrency)
* 8.1 并发原语：`task` 与 `spawn`
* 8.2 信箱、状态隔离 (`task.ram`) 与消息投递 (`send`)
* 8.3 `main` 的独立家主地位：“先部署，后点火”

### 第 9 章：模式匹配与路由引擎 (Pattern Matching & Routing)
* 9.1 `on` 块的解构：字面量与深层绑定
* 9.2 多态分发引擎：配合 `is` 与 `has` 的状态机流转

### 第 10 章：编译期执行 (Comptime)
* 10.1 宏与 `#[]` 编译期指令
* 10.2 在 AOT 阶段完成重度逻辑
* 10.3 目标平台探测与条件编译

---

*(第四、五、六部分分别对应：**标准库指南**、**跨端/AutoUI互操作**、**底层极客解密（VM与装载器）**，维持原版宏大结构不变。)*

---
