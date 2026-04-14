# 第七章：函数

> 级别 1 — 入门
>
> 将逻辑封装为可重用、可组合的单元。

函数是组织代码的主要机制。函数接受输入（参数），执行计算，并产生输出（返回值）。C 和 Auto 共享相同的基本模型，但在语法、类型表达和安全保证上有所不同。

---

## 7.1 简单函数

C 函数有返回类型、名称、参数列表和函数体：

```c
// C
int max(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
```

Auto 函数使用 `fn` 关键字，类型注解在参数名之后：

```auto
// Auto
fn max(a int, b int) int {
    if a > b { a } else { b }
}
```

主要区别：

| 特性                | C                            | Auto                          |
|--------------------|------------------------------|-------------------------------|
| 关键字              | 无（返回类型在前）           | `fn`                          |
| 返回类型            | 函数名之前                   | 参数列表之后                  |
| 参数语法            | `int a, int b`               | `a int, b int`               |
| 返回语句            | `return expr;`               | 最后表达式或 `return`         |
| 空参数              | `void`                       | 空 `()`                       |
| 缺少返回值          | 未定义行为                   | 编译错误                      |

**隐式返回：** 在 Auto 中，块中的最后一个表达式是其值。当函数体是单个表达式或最后一个表达式是预期的返回值时，不需要显式 `return` 关键字：

```auto
fn square(x int) int {
    x * x             // 隐式返回
}

fn clamp(val int, lo int, hi int) int {
    max(lo, min(val, hi))    // 隐式返回
}
```

**前向声明：** 在 C 中，函数必须在使用前声明。这通常需要在文件顶部写前向声明（原型）：

```c
int min(int a, int b);     // 前向声明
int max(int a, int b) { ... }
int clamp(int v, int lo, int hi) { return max(lo, min(v, hi)); }
int min(int a, int b) { return a < b ? a : b; }
```

Auto 不需要前向声明。编译器在单次遍历中解析函数引用，所以你可以在定义之前调用函数：

```auto
fn clamp(val int, lo int, hi int) int {
    max(lo, min(val, hi))
}

fn max(a int, b int) int {
    if a > b { a } else { b }
}

fn min(a int, b int) int {
    if a < b { a } else { b }
}
```

<Listing path="listings/ch07/listing-07-01" title="简单函数" />

> **要点：** Auto 的隐式返回和无需前向声明减少了样板代码。专注于逻辑，而不是仪式。

---

## 7.2 main 是特殊的

每个 C 程序从 `main` 函数开始执行。C 标准定义了两个有效的签名：

```c
// 形式 1：无参数
int main(void) {
    // ...
    return 0;
}

// 形式 2：命令行参数
int main(int argc, char *argv[]) {
    for (int i = 0; i < argc; i++) {
        printf("argv[%d] = %s\n", i, argv[i]);
    }
    return 0;
}
```

Auto 简化了 `main`：

```auto
// Auto：无参数
fn main() {
    // ...
}

// Auto：带命令行参数
fn main(args [str]) {
    for i in 0..len(args) {
        print("arg[", i, "] =", args[i])
    }
}
```

转译器将 `fn main()` 映射为 `int main(void)`，将 `fn main(args [str])` 映射为 `int main(int argc, char *argv[])`。

区别：

| 特性             | C                           | Auto                        |
|-----------------|-----------------------------|------------------------------|
| 返回类型         | `int`（必需）               | 省略（转译器添加）          |
| 返回值           | `return 0;` 表示成功         | 省略（隐式成功）            |
| 参数数量         | `argc`                      | `len(args)`                 |
| 参数数组         | `char *argv[]`              | `[str]`                     |
| 退出码           | `return n;` 或 `exit(n)`    | `return n` 或 `exit(n)`     |

> **要点：** 在 C 中，`main` 返回 `int`。忘记返回值在旧 C 标准（C89）中严格来说是未定义行为，尽管 C99 及以后允许省略。Auto 自动处理这些。

---

## 7.3 递归

如果一个函数调用自身，它就是**递归的**。递归在两种语言中概念相同——区别纯粹是语法上的。

**阶乘**——经典的递归示例：

```c
// C
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}
```

```auto
// Auto
fn factorial(n int) int {
    if n <= 1 {
        1
    } else {
        n * factorial(n - 1)
    }
}
```

**斐波那契**——演示多次递归调用：

```c
// C
int fibonacci(int n) {
    if (n <= 0) return 0;
    if (n == 1) return 1;
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

```auto
// Auto
fn fibonacci(n int) int {
    if n <= 0 { return 0 }
    if n == 1 { return 1 }
    fibonacci(n - 1) + fibonacci(n - 2)
}
```

注意 Auto 在 `if` 块内使用 `return` 作为提前退出。非 `if` 分支的最后一个表达式是隐式返回。

<Listing path="listings/ch07/listing-07-02" title="递归：阶乘与斐波那契" />

### 递归如何工作

每次递归调用创建一个新的**栈帧**，包含：
- 函数的参数
- 局部变量
- 返回地址

对于 `factorial(5)`，调用栈如下增长：

```
factorial(5)
  → 5 * factorial(4)
    → 4 * factorial(3)
      → 3 * factorial(2)
        → 2 * factorial(1)
          → 1   （基本情况）
```

然后结果展开：`1 → 2 → 6 → 24 → 120`。

**栈溢出：** 如果递归太深（例如 `factorial(1000000)`），栈空间会耗尽。C 和 Auto 都面临这个限制。对于深层递归，使用迭代方法或尾调用优化（如果支持）。

> **要点：** 递归很优雅，但要注意栈深度。对于生产代码，可能深度递归的算法优先使用迭代解决方案。

---

## 快速参考

| 概念              | C 语法                       | Auto 语法                    |
|------------------|------------------------------|------------------------------|
| 函数声明          | `int f(int a) { ... }`      | `fn f(a int) int { ... }`   |
| 无返回值          | `void f(void) { ... }`      | `fn f() { ... }`            |
| 返回值            | `return expr;`              | 最后表达式或 `return expr`   |
| 前向声明          | `int f(int a);`             | 不需要                       |
| main（简单）      | `int main(void)`            | `fn main()`                  |
| main（参数）      | `int main(int argc, char *argv[])` | `fn main(args [str])` |
| 递归              | 与普通函数相同               | 与普通函数相同               |
| 提前返回          | `return;` / `return val;`   | `return` / `return val`      |

---

*下一章：[第八章 — C 库函数](ch08-c-library.cn.md)*
