# 第十章：组织与文档

> 级别 2 — 认知
>
> 跨文件组织程序：接口、实现和文档。

适合放在一个文件中的程序是脚本。跨越数十个文件的程序是系统。本章介绍 C 如何将代码组织为接口和实现，以及 Auto 的模块系统如何提供更清晰的替代方案。

---

## 10.1 接口文档

在 C 中，**接口**声明在**头文件**（`.h`）中，**实现**位于**源文件**（`.c`）中。头文件就是契约：

```c
// geometry.h — 接口
#ifndef GEOMETRY_H
#define GEOMETRY_H

typedef struct {
    float width;
    float height;
} Rectangle;

float Rectangle_area(Rectangle r);
float Rectangle_perimeter(Rectangle r);

#endif
```

```c
// geometry.c — 实现
#include "geometry.h"

float Rectangle_area(Rectangle r) {
    return r.width * r.height;
}

float Rectangle_perimeter(Rectangle r) {
    return 2.0f * (r.width + r.height);
}
```

需要 `Rectangle` 的其他文件包含该头文件：

```c
// main.c
#include "geometry.h"
#include <stdio.h>

int main(void) {
    Rectangle r = {4.0f, 6.0f};
    printf("Area: %f\n", Rectangle_area(r));
    return 0;
}
```

**文档注释。** C 使用 `/** ... */` 编写文档。许多项目采用类似 Doxygen 的约定：

```c
/**
 * @brief 计算矩形的面积。
 * @param r 矩形
 * @return 面积（float）
 */
float Rectangle_area(Rectangle r);
```

**Auto 的方法。** Auto 用 `mod` 和 `use` 系统替代头文件。类型及其关联函数构成天然接口：

```auto
// geometry.at — 接口和实现合二为一
type Rectangle {
    width float
    height float
}

fn Rectangle.new(w float, h float) Rectangle {
    Rectangle(w, h)
}

fn Rectangle.area(r Rectangle) float {
    r.width * r.height
}

fn Rectangle.perimeter(r Rectangle) float {
    2.0 * (r.width + r.height)
}
```

另一个文件使用 `use` 引入模块：

```auto
// main.at
use geometry

fn main() {
    let r Rectangle = Rectangle.new(4.0, 6.0)
    print("Area:", r.area(r))
}
```

<Listing path="listings/ch10/listing-10-01" title="接口文档" />

a2c 转译器从 Auto 源码自动生成 `.h` 文件。你不需要手写头文件保护符、前向声明或 `#include` 指令。

> **要点：** 在 C 中，头文件就是接口。保持最小化——声明类型和函数签名，但不暴露实现细节。Auto 自动完成这种分离。

---

## 10.2 实现

将接口与实现分离有几个目的：

1. **编译速度。** 修改实现文件不会强制重新编译仅包含头文件的文件。
2. **封装。** 接口的消费者只能看到头文件暴露的内容。内部细节保持隐藏。
3. **并行开发。** 团队可以就头文件达成一致，然后独立实现。

**C 中的多文件项目**需要构建系统。一个简单的 `Makefile`：

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -std=c17

myapp: main.o geometry.o
	$(CC) $(CFLAGS) -o $@ $^

main.o: main.c geometry.h
	$(CC) $(CFLAGS) -c main.c

geometry.o: geometry.c geometry.h
	$(CC) $(CFLAGS) -c geometry.c

clean:
	rm -f *.o myapp
```

**Auto 中的多文件项目**使用 `pac.at` 进行包配置：

```
name: "geometry-app"
version: "0.1.0"
lang: "c"

app("geometry-app") {}
```

`auto build` 命令读取 `pac.at`，解析 `.at` 文件之间的依赖关系，并调用 a2c 随后调用 C 编译器。不需要手动编写 Makefile。

**文档即纪律。** 每个公共函数都应有注释回答三个问题：

- 这个函数**做什么**？
- 它的参数**是什么**？
- 它**返回**什么？

在 C 中：

```c
/**
 * 对整数数组进行升序排序。
 * @param arr  要排序的数组
 * @param n    arr 中的元素数量
 * @return     成功返回 0，错误返回 -1
 */
int sort_ints(int* arr, size_t n);
```

在 Auto 中，函数名和类型签名携带更多信息，减少了对冗长文档的需求：

```auto
// 名称和类型是自文档化的
fn sort_ascending(arr []int) []int {
    // 实现
}
```

> **要点：** 文档是接口的一部分。为每个公共函数编写文档。在 Auto 中，强类型和描述性名称减少但不能消除注释的需求。

---

## 快速参考

| 概念            | C 机制                   | Auto 机制                  |
|----------------|--------------------------|----------------------------|
| 接口            | `.h` 头文件              | `mod`（模块）              |
| 实现            | `.c` 源文件              | `.at` 源文件               |
| 导入            | `#include "file.h"`     | `use module_name`          |
| 头文件保护      | `#ifndef` / `#define`   | 自动                       |
| 前向声明        | `struct Foo;`           | 自动                       |
| 构建配置        | `Makefile`、`CMake`     | `pac.at`                   |
| 构建命令        | `make`                  | `auto build`               |
| 文档注释        | `/** @brief ... */`     | `//` 和自文档化            |

---

*代码组织好并编写文档后，下一章将深入 C 最强大也最危险的特性：指针。*
