x = 50


def func():
    global x
    print(f"x is {x}")
    x = 2
    print(f"Changed global x to {x}")


def main():
    func()
    print(f"Value of x is {x}")


if __name__ == "__main__":
    main()
