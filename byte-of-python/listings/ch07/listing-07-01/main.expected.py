def print_max(a, b):
    if a > b:
        print(f"{a} is maximum")
    elif a < b:
        print(f"{b} is maximum")
    else:
        print("Both are equal")


def main():
    # directly pass literal values
    print_max(3, 4)

    x = 5
    y = 7

    # pass variables as arguments
    print_max(x, y)


if __name__ == "__main__":
    main()
