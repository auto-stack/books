def func(a, b=5, c=10):
    print(f"a is {a} and b is {b} and c is {c}")


def main():
    func(3, 7)
    func(25, c=24)
    func(c=50, a=100)


if __name__ == "__main__":
    main()
