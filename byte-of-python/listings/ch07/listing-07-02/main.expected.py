def func(x):
    print(f"x is {x}")
    x = 2
    print(f"Changed local x to {x}")


def main():
    x = 50
    func(x)
    print(f"x is still {x}")


if __name__ == "__main__":
    main()
