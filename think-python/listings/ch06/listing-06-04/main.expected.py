def factorial(n):
    if n == 0:
        return 1
    else:
        recurse = factorial(n - 1)
        return n * recurse


def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def main():
    # Factorial
    print(f"factorial(0): {factorial(0)}")
    print(f"factorial(1): {factorial(1)}")
    print(f"factorial(3): {factorial(3)}")
    print(f"factorial(5): {factorial(5)}")

    # Fibonacci
    print(f"fibonacci(0): {fibonacci(0)}")
    print(f"fibonacci(1): {fibonacci(1)}")
    print(f"fibonacci(5): {fibonacci(5)}")
    print(f"fibonacci(10): {fibonacci(10)}")


if __name__ == "__main__":
    main()
