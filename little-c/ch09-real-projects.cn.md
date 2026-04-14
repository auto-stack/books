# 第9章：构建真实项目

> 第 91--100 节
> 之前学到的所有知识将汇合在一起。构建库、工具、服务器和解析器。

前面的章节介绍了 C 的基础构建块和 Auto 更安全的替代方案。现在是时候构建真正的软件了。
本章将通过完整的项目进行讲解——从小型库到 CLI 工具、HTTP 服务器和文本解析器。

每节都同时展示 C 方法（你需要手动编写的代码）和 Auto 方法（你实际编写的代码）。
学完本章后，你将掌握构建自己项目所需的模式。

---

## 91. 设计小型库

一个好的库有清晰的 API、最少的依赖和可组合的构建块。

**C 库的模式：**
- 头文件（`.h`）声明公共 API
- 实现文件（`.c`）包含逻辑
- 所有名称加前缀以避免冲突（例如 `vec2_add`、`vec2_length`）

```c
/* vec2.h */
typedef struct { float x; float y; } Vec2;
Vec2 vec2_new(float x, float y);
Vec2 vec2_add(Vec2 a, Vec2 b);
float vec2_length(Vec2 v);
```

**Auto 库的模式：**
- 类型将相关数据分组
- 类型上的方法提供 API
- `mod` 和 `use` 组织模块

```auto
type Vec2 { x float, y float }
fn Vec2.new(x float, y float) Vec2 { ... }
fn Vec2.add(a Vec2, b Vec2) Vec2 { ... }
fn Vec2.length(v Vec2) float { ... }
```

Auto 的方法语法保持 API 简洁。类型名充当命名空间，取代了 C 的手动前缀约定。

<Listing id="listing-09-01" title="设计小型库" path="listings/ch09/listing-09-01" />

---

## 92. 构建 CLI 工具

命令行工具解析参数并执行命令。在 C 中，你使用 `argc`/`argv` 或 `getopt` 等库：

```c
int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <command>\n", argv[0]);
        return 1;
    }
    if (strcmp(argv[1], "add") == 0) {
        printf("Adding task...\n");
    } else if (strcmp(argv[1], "list") == 0) {
        printf("Listing tasks...\n");
    }
}
```

Auto 提供了更简洁的接口：

```auto
fn main(args [str]) {
    is args[1] {
        "add"  => print("Adding task...")
        "list" => print("Listing tasks...")
        else   => print("Unknown command")
    }
}
```

`main(args [str])` 签名告诉 Auto 你希望将命令行参数作为字符串数组获取。
`is` 表达式取代了冗长的 `if`/`else if` 链。

<Listing id="listing-09-02" title="构建 CLI 工具" path="listings/ch09/listing-09-02" />

---

## 93. 微型 HTTP 服务器

在 C 中构建 HTTP 服务器需要套接字编程：

```c
#include <sys/socket.h>
int server = socket(AF_INET, SOCK_STREAM, 0);
bind(server, (struct sockaddr *)&addr, sizeof(addr));
listen(server, 10);
int client = accept(server, NULL, NULL);
char buf[4096];
read(client, buf, sizeof(buf));
write(client, "HTTP/1.1 200 OK\r\n\r\nHello!", 26);
```

这是很底层的操作：你需要手动管理套接字、解析 HTTP 请求，并在每一步处理错误。
生产级服务器还要加入 epoll/kqueue 进行异步 I/O。

Auto 为请求处理提供了更高级的抽象：

```auto
type Request { method str, path str }
type Response { status int, body str }

fn handle_request(req Request) Response {
    is req.path {
        "/"      => Response(200, "Welcome!")
        "/about" => Response(200, "About page")
        else     => Response(404, "Not found")
    }
}
```

路由逻辑是声明式的。你定义请求类型和响应类型，然后对路径进行模式匹配。
Auto 处理套接字的底层细节。

<Listing id="listing-09-03" title="微型 HTTP 服务器" path="listings/ch09/listing-09-03" />

---

## 94. 键值存储

键值存储结合了数据结构和文件 I/O：

**C 实现：**
- 哈希表用于内存查找
- `fopen`/`fwrite` 用于持久化
- 手动管理键和值的内存

```c
typedef struct { char key[64]; char value[256]; } Entry;
Entry store[1024];
int count = 0;

const char *get(const char *key) {
    for (int i = 0; i < count; i++)
        if (strcmp(store[i].key, key) == 0)
            return store[i].value;
    return NULL;
}
```

**Auto 实现：**
- Map 提供内置的键值存储
- 文件 I/O 由标准库处理
- 无需手动内存管理

```auto
let store Map(str, str) = Map.new()
store.set("name", "Alice")
let name str = store.get("name")
```

键值存储模式无处不在：配置、缓存、数据库。理解 C 的实现有助于你体会
Auto 自动化了什么。

---

## 95. 自定义分配器

C 中的内存分配默认使用 `malloc` 和 `free`。对于性能关键代码，你可以编写
自定义分配器：

**竞技场分配器**：分配一个大块，逐块分配，一次性全部释放。

```c
typedef struct {
    char *buf;
    size_t offset;
    size_t capacity;
} Arena;

void *arena_alloc(Arena *a, size_t size) {
    if (a->offset + size > a->capacity) return NULL;
    void *ptr = a->buf + a->offset;
    a->offset += size;
    return ptr;
}

void arena_free(Arena *a) {
    free(a->buf);
    a->offset = 0;
}
```

**池分配器**：为相同大小的对象提供固定大小的块。对于重复分配相同类型，
比 `malloc` 更快。

自定义分配器是 C 独有的高级主题。Auto 的内存管理系统内部使用竞技场分配，
因此你无需自己编写分配器就能获得性能优势。

---

## 96. 文本解析器

解析是基础技能：配置文件、编程语言、数据格式都需要解析。简单的分词器将输入
拆分成有意义的片段。

**C 分词器：**
```c
while (*input) {
    while (isspace(*input)) input++;
    if (!*input) break;
    char *start = input;
    while (*input && !isspace(*input)) input++;
    printf("Token: %.*s\n", (int)(input - start), start);
}
```

**Auto 分词器：**
```auto
fn tokenize(input str) {
    let tokens int = 0
    for i in 0..len(input) {
        if input[i] == " " { tokens = tokens + 1 }
    }
    print("Found", tokens + 1, "tokens")
}
```

Auto 的字符串处理使解析器更简洁。没有指针运算、没有手动空终止、没有缓冲区溢出风险。

<Listing id="listing-09-04" title="文本解析器" path="listings/ch09/listing-09-04" />

---

## 97. 微型解释器

表达式求值器是一个微型解释器。它解析算术表达式并计算结果：

```c
/* C 表达式求值器（简化版） */
int eval(const char *expr) {
    int a, b;
    char op;
    sscanf(expr, "%d %c %d", &a, &op, &b);
    switch (op) {
        case '+': return a + b;
        case '-': return a - b;
        case '*': return a * b;
        case '/': return b != 0 ? a / b : 0;
    }
    return 0;
}
```

一个真正的解释器有更多组件：
1. **词法分析器**：将文本转换为标记
2. **解析器**：构建抽象语法树（AST）
3. **求值器**：遍历 AST 并计算结果

Auto 的 `type` 和 `is` 表达式让 AST 变得很自然：

```auto
type Expr {
    Num  { value int }
    Add  { left Expr, right Expr }
    Mul  { left Expr, right Expr }
}

fn eval(e Expr) int {
    is e {
        Num  => e.value
        Add  => eval(e.left) + eval(e.right)
        Mul  => eval(e.left) * eval(e.right)
    }
}
```

---

## 98. 与 SQLite 交互

SQLite 是世界上部署最广泛的数据库。从 C 中使用它：

```c
#include <sqlite3.h>
sqlite3 *db;
sqlite3_open("test.db", &db);
sqlite3_exec(db, "CREATE TABLE users (name TEXT)", NULL, NULL, NULL);
sqlite3_exec(db, "INSERT INTO users VALUES ('Alice')", NULL, NULL, NULL);
sqlite3_close(db);
```

从 Auto 中使用 FFI：

```auto
sys extern fn sqlite3_open(path str, db *sqlite3) int
sys extern fn sqlite3_exec(db *sqlite3, sql str, ...) int
sys extern fn sqlite3_close(db *sqlite3) int
```

FFI 模式与调用任何 C 库相同：
1. 使用 `sys extern` 声明 C 函数
2. 从 Auto 代码中调用它们
3. a2c 生成正确的 C 函数调用

每个 C 库都可以通过 FFI 成为 Auto 库。

---

## 99. 打包与文档

完整的 Auto 项目结构如下：

```
my-project/
    pac.at          # 项目清单
    src/
        main.at     # 入口点
        lib.at      # 库模块
    tests/
        main.at     # 测试
    docs/           # 文档
```

**pac.at** 声明项目：

```auto
name: "my-project"
version: "1.0.0"
lang: "c"

app("my-project") {}
```

**文档**在 Auto 中使用文档注释：

```auto
// 将两个向量相加并返回结果。
// 两个向量必须具有相同的维度。
fn Vec2.add(a Vec2, b Vec2) Vec2 {
    Vec2(a.x + b.x, a.y + b.y)
}
```

构建和运行：
```bash
$ auto build       # 编译项目
$ auto run         # 运行编译后的二进制文件
$ auto t           # 运行测试
$ auto doc         # 生成文档
```

---

## 100. 练习：构建你自己的项目

这是你的毕业练习。运用所学的一切，从头开始构建一个项目。

<Listing id="listing-09-05" title="构建你自己的项目" path="listings/ch09/listing-09-05" />

**项目创意：**

1. **计算器**：解析并计算算术表达式（结合第 96-97 节）
2. **文件转换器**：读取 CSV，输出 JSON（结合第 94、96 节）
3. **微型数据库**：带文件持久化的键值存储（第 93-94 节）
4. **静态网站生成器**：读取 Markdown 文件，输出 HTML
5. **任务管理器**：带 add/list/complete 命令的 CLI 工具（第 92 节）

**任何项目的步骤：**

1. 先定义类型（数据模型）
2. 将核心逻辑编写为这些类型上的函数
3. 添加 CLI 或 API 接口
4. 为每个函数编写测试
5. 用 `pac.at` 打包

选择一个创意，实现它，然后迭代。listing-09-05 中的模板是你的起点。用你自己的
类型替换占位符类型，添加函数，构建有用的东西。

---

## 速查表

| 节号  | 主题            | C 工具/方法             | Auto 方法                |
|-------|-----------------|------------------------|--------------------------|
| 91    | 小型库          | .h/.c 前缀模式         | 类型 + 方法 + mod/use    |
| 92    | CLI 工具        | argc/argv、getopt      | `main(args [str])`、`is` |
| 93    | HTTP 服务器     | 套接字编程             | Request/Response 类型    |
| 94    | 键值存储        | 哈希表 + 文件 I/O      | 内置 Map 类型            |
| 95    | 自定义分配器    | 竞技场/池分配器        | 运行时处理               |
| 96    | 文本解析器      | 基于指针的分词器       | 基于字符串的分词         |
| 97    | 微型解释器      | 带标签联合的 AST       | 类型 + is 模式匹配       |
| 98    | SQLite FFI      | sqlite3.h C API        | `sys extern` FFI 调用    |
| 99    | 打包            | Makefiles、CMake       | pac.at + `auto` 命令     |
| 100   | 构建你的项目    | 手动配置               | 模板 + auto 工具链       |
