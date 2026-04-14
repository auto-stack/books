# 编译器架构

本章通过介绍 TypeScript 和 Auto 共享的编译流水线来解释编译器的工作原理。
我们不会把编译器当作一个黑盒，而是打开它，逐一检查每个阶段：从原始源代码
一直到最终的输出产物。理解这条流水线对于理解错误信息、调试类型问题以及
了解按下编译按钮时"幕后"发生了什么至关重要。

## 编译流水线

TypeScript 和 Auto 编译器都遵循相同的通用流水线。每个阶段都有**单一的
职责**，并通过定义良好的数据结构与下一个阶段通信：

```
┌──────────┐    ┌────────┐    ┌───────┐    ┌───────┐    ┌─────────┐    ┌─────────┐
│  源代码   │───▶│扫描器  │───▶│ 词法  │───▶│解析器 │───▶│  AST    │───▶│ 绑定器  │
│           │    │(Lexer) │    │ 单元  │    │       │    │         │    │         │
└──────────┘    └────────┘    └───────┘    └───────┘    └─────────┘    └─────────┘
                                                                      │
                                                                      ▼
┌─────────┐    ┌─────────┐    ┌───────┐    ┌───────┐    ┌─────────┐  ┌─────────┐
│  输出    │◀───│发射器  │◀───│ 类型  │◀───│检查器 │◀───│ 符号    │◀─┘         │
│ (JS/TS)  │    │         │    │       │    │       │    │         │            │
└─────────┘    └─────────┘    └───────┘    └───────┘    └─────────┘            │
                                                                          ┌─────┴──────┐
                                                                          │   绑定器    │
                                                                          └────────────┘
```

简而言之：**源代码**变成**词法单元**，再变成 **AST**，再产生**符号**，
经过检查产生**类型**，最终被发射为**输出**。

每个阶段都是独立的，可以单独测试。这种模块化设计使得构建语言服务器、
格式化工具和代码检查器成为可能——它们可以复用流水线的某些部分而不需要
运行完整的编译器。

## 扫描器（词法分析器）

**扫描器**（也称为**词法分析器**）将原始源文本转换为**词法单元**（token）
流。词法单元是源代码中最小的有意义的单元。每个词法单元携带两条信息：

- **类型（Kind）** — 它是什么类型的词法单元（关键字、标识符、字面量、
  运算符、标点符号）
- **位置（Position）** — 它在源文件中出现的位置（行号、列号、偏移量）

TypeScript 的扫描器通过 `ts.createScanner()` 访问，它为每个词法单元返回
`SyntaxKind` 枚举值。Auto 的扫描器遵循相同的设计，产生 Auto 特定的词法
单元类型。

考虑这个简单的声明：

```
let x = 42
```

扫描器产生以下词法单元流：

```
[LetKeyword, Identifier("x"), EqualsToken, IntLiteral(42), EndOfFileToken]
```

注意空白符被**丢弃**了——扫描器会去除空格、换行符和注释（除非配置为保留
它们，供格式化工具等使用）。扫描器不执行任何语义分析。它不知道（也不关心）
`x` 是否已声明。它的工作纯粹是**词法的**：识别文本中词法单元的形状。

**扫描器错误**是最基本的编译器错误，包括无法识别的字符和未终止的字符串
字面量。如果你在编辑器中见过"Unexpected character"这样的错误，那来自
扫描器阶段。

## 解析器

**解析器**将词法单元流转换为**抽象语法树（AST）**。AST 是程序结构的
层次化、树状表示。树中的每个节点都有：

- **类型（Kind）** — 它表示什么语法构造（函数、变量、调用表达式等）
- **位置（Position）** — 它在源代码中出现的位置（从词法单元继承）
- **子节点（Children）** — 形成子树的内嵌节点

TypeScript 的 AST 使用 `SyntaxKind` 枚举来标识节点类型，包含超过 500 个
不同的值，覆盖了所有可能的 JavaScript 和 TypeScript 构造。Auto 使用类似的
AST 结构，但使用 Auto 特定的节点类型。

解析器采用**递归下降**策略——每个语法规则都实现为一个函数，调用其他函数。
例如，`parseFunctionDeclaration()` 调用 `parseIdentifier()`，然后调用
`parseParameterList()`，最后调用 `parseBlock()`。

解析我们的 `let x = 42` 示例会产生：

```
VariableDeclaration
├── IdentifierToken  "let"
├── Identifier       "x"
├── EqualsToken      "="
└── IntLiteral       42
```

**解析器错误**包括语法错误：缺少分号、括号不匹配、无效的词法单元序列。
这些就是你在编辑器中看到的"Expected X, got Y"消息。

## 绑定器

**绑定器**遍历 AST 并创建**符号（Symbol）**——程序的语义构建块。这是编译器
从**语法**（代码看起来是什么样子）过渡到**语义**（代码意味着什么）的阶段。

**符号**将一个名称连接到它的声明。当解析器遇到 `let x = 42` 时，它创建
一个 `VariableDeclaration` 节点。绑定器随后为 `x` 创建一个 `Symbol`，
并存储对该节点的引用。稍后，当解析器在表达式中遇到 `x` 时，绑定器将其
解析为同一个 `Symbol`。

```
AST（语法）                       符号（语义）
───────────                       ────────────
let x = 42        ──────────▶    Symbol("x") → VariableDeclaration
x + 1             ──────────▶    Symbol("x") → 解析为同一声明
```

没有绑定器，AST 只是一棵词法单元的树。绑定器通过建立声明与其使用之间的
关系来添加**含义**。这就是编译器如何知道 `x + 1` 中的 `x` 指的是第 3 行
声明的 `x`，而不是某个其他的 `x`。

在 TypeScript 中，绑定器不被直接调用——它由检查器按需驱动。这种惰性方法
意味着只有实际被类型检查的程序部分才会被绑定。

## 类型检查器

**类型检查器**是两个编译器中最大、最复杂的组件。仅 TypeScript 的检查器
就有超过 23,000 行代码。它的职责包括：

- **类型检查**所有表达式和语句的正确性
- **类型推断**——确定 `let x = 42` 的类型，无需显式注解
- **解析泛型**——将类型参数替换为具体类型
- **生成诊断信息**——产生你在编辑器中看到的错误和警告消息

检查器消耗两个输入：

```
AST（来自解析器）  +  符号（来自绑定器）  →  类型 + 诊断信息
```

TypeScript 中的一个关键设计决策是**惰性类型解析**。类型不是立即被检查的——
它们按需解析。当语言服务器需要某个表达式的类型时（例如用于悬停信息），
检查器只解析足够回答该查询的部分。这就是 TypeScript 即使在大型代码库上
也能保持响应速度的原因。

Auto 的类型检查器遵循类似的模型，但执行**更严格的规则**：没有 `any` 类型，
没有隐式 `undefined`，泛型在定义时而非使用时检查。这意味着 Auto 可以在
编译时捕获更多错误，代价是需要稍微多一些的类型注解。

## 发射器

**发射器**接收验证过的 AST 和类型信息，产生最终输出。这是实际生成程序
运行代码的阶段。

TypeScript 有**两个**发射器：

| 发射器 | 输入 | 输出 |
|--------|------|------|
| JavaScript 发射器 | TypeScript AST | JavaScript (`.js`) |
| 声明文件发射器 | TypeScript AST | 类型声明文件 (`.d.ts`) |

Auto 的发射器主要目标是 TypeScript，然后可以由 TypeScript 编译器编译为
JavaScript。对于原生目标，Auto 还有一个 Rust 发射器：

| 发射器 | 输入 | 输出 |
|--------|------|------|
| TypeScript 发射器 | Auto AST | TypeScript (`.ts`) |
| Rust 发射器 | Auto AST | Rust (`.rs`) |

发射器尽可能**保留注释和格式**，使输出保持可读性。它还会生成**源映射
（source map）**——将输出中的每个位置映射回源代码中对应位置的文件。源映射
使得即使在浏览器运行 JavaScript 时，你也可以在原始 TypeScript 或 Auto
代码中设置断点和阅读堆栈跟踪。

## Auto 与 TypeScript 编译器对比

虽然两个编译器共享相同的流水线架构，但每个阶段的工作方式都有重要差异：

```
TypeScript 流水线：
  源代码 → 扫描器 → 词法单元 → 解析器 → AST → 绑定器 → 符号
  → 检查器 → 类型 → JS 发射器 → .js
                      └──────→ .d.ts 发射器 → .d.ts

Auto 流水线：
  源代码 → 扫描器 → 词法单元 → 解析器 → AST → 绑定器 → 符号
  → 检查器 → 类型 → TS 发射器 → .ts → (tsc) → .js
                      └──────→ Rust 发射器 → .rs
```

关键架构差异：

- **输出目标**：Auto 编译为 TypeScript（然后是 JS），而非直接编译为 JS。
  这意味着 Auto 可以发出 TypeScript 保留的类型注解。

- **更严格的检查**：Auto 没有 `any` 类型，泛型约束中没有双变性，
  也没有隐式 `undefined`。检查器在编译时拒绝更多程序。

- **模式匹配**：Auto 的 `is` 关键字为类型检查器添加了**穷尽性检查**。
  当你对标记联合体编写 `match` 时，检查器会验证每个变体都被处理。

- **Has 组合**：Auto 的 `has` 关键字将类型组合在一起。这由绑定器在
  编译时解析，将 `has` 展开为等价的结构类型。

- **错误传播**：Auto 的 `?` 错误传播运算符由发射器转换为输出 TypeScript
  中的 `try`/`catch` 块。这意味着 Auto 中的错误处理在源码层面很简洁，
  但编译为标准的 JavaScript 错误处理。

<Listing name="pipeline" file="listings/ch15-pipeline">

```auto
// Auto — this file demonstrates the compilation pipeline
// The Auto compiler transforms this source through these stages:
//
// 1. SCANNER:  Converts text to tokens
//    "fn add(a int, b int) int { a + b }"
//    → [FnKeyword, Identifier("add"), LParen, Identifier("a"),
//       IntKeyword, Comma, Identifier("b"), IntKeyword, RParen,
//       IntKeyword, LBrace, Identifier("a"), Plus, Identifier("b"), RBrace]
//
// 2. PARSER:   Converts tokens to AST
//    → FunctionDecl(name: "add", params: [Param("a", int), Param("b", int)],
//                    return_type: int, body: BinaryExpr(Ident("a"), Plus, Ident("b")))
//
// 3. BINDER:   Creates symbols from AST declarations
//    → Symbol("add"), Symbol("a"), Symbol("b")
//
// 4. CHECKER:  Validates types and resolves generics
//    → int + int = int ✓ (return type matches annotation)
//
// 5. EMITTER:  Generates TypeScript output
//    → function add(a: number, b: number): number { return a + b; }

fn add(a int, b int) int {
    a + b
}

fn main() {
    print("add(3, 4) = {add(3, 4)}")
}
```

</Listing>

同样的函数用 TypeScript 编写会经历类似的流水线：

```typescript
// TypeScript — the TypeScript compiler pipeline
// This file demonstrates the TypeScript compilation stages:
//
// 1. SCANNER:  Converts text to tokens
//    "function add(a: number, b: number): number { return a + b; }"
//    → [FunctionKeyword, Identifier("add"), LParen, Identifier("a"),
//       Colon, NumberKeyword, Comma, Identifier("b"), Colon,
//       NumberKeyword, RParen, Colon, NumberKeyword, LBrace,
//       ReturnKeyword, Identifier("a"), Plus, Identifier("b"), Semicolon, RBrace]
//
// 2. PARSER:   Converts tokens to AST
//    → FunctionDeclaration(name: "add", params: [...], returnType: NumberKeyword,
//                          body: Block(ReturnStatement(BinaryExpression(...))))
//
// 3. BINDER:   Creates symbols for all declarations
//    → Symbol("add", flags: Function), Symbol("a"), Symbol("b")
//
// 4. CHECKER:  Type checks and validates
//    → number + number = number ✓
//
// 5. EMITTER:  Generates JavaScript output
//    → function add(a, b) { return a + b; }

function add(a: number, b: number): number {
    return a + b;
}

console.log("add(3, 4) = " + add(3, 4));
```

注意 TypeScript 的词法单元流要冗长得多。每个类型注解（`: number`）都会
生成三个词法单元（标识符、冒号、关键字）。Auto 的空格分隔注解在词法单元
层面更加简洁。

## 快速参考

| 概念 | TypeScript | Auto |
|------|-----------|------|
| 扫描器 API | `ts.createScanner()` | 内部扫描器模块 |
| AST 节点标识 | `SyntaxKind` 枚举（500+ 值） | `SyntaxKind` 枚举（Auto 特定） |
| 解析器策略 | 递归下降 | 递归下降 |
| 符号创建 | 绑定器（由检查器驱动） | 绑定器（相同的惰性方法） |
| 类型检查器规模 | ~23,000 行 | 更小（更严格，更少转义路径） |
| 主要输出 | `.js` + `.d.ts` | `.ts`（然后通过 tsc 生成 `.js`） |
| 次要输出 | 源映射 | 源映射 + 可选 `.rs` |
| 错误传播 | `try`/`catch` | `?` 运算符（发射为 `try`/`catch`） |
| 模式匹配穷尽性 | 不检查 | 由类型检查器检查 |
| 类型系统严格度 | 可配置（`strict` 标志） | 始终严格（无 `any`） |
| 惰性类型解析 | 是 | 是 |
