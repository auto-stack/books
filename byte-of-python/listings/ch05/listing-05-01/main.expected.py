def main():
    # Operator precedence demonstration
    result = 2 + 3 * 4
    print(result)

    # Parentheses change the order
    result2 = (2 + 3) * 4
    print(result2)

    # Mixed operations
    a = 2 + 3 * 4 - 10 / 2
    print(a)

    # Power has higher precedence than multiplication
    b = 2 * 3 ** 2
    print(b)

    # Boolean operators and comparison
    x = 5
    y = 10
    z = x > 3 and y < 20
    print(z)

    w = not (x == 5) or y > 15
    print(w)


if __name__ == "__main__":
    main()
