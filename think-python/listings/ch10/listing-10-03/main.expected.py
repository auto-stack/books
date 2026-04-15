known = {0: 0, 1: 1}


def fibonacci_memo(n):
    if n in known:
        return known[n]
    res = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
    known[n] = res
    return res


def main():
    # Computing Fibonacci numbers with memoization
    print("Fibonacci numbers with memoization:")
    for i in range(11):
        print(f"fib({i}) = {fibonacci_memo(i)}")

    # Large Fibonacci number -- fast with memoization
    print()
    print(f"fib(40) = {fibonacci_memo(40)}")

    # Show what's in the cache
    print()
    print(f"Cache contains {len(known)} entries")

    # Demonstrate reusing the cache
    print(f"fib(35) from cache: {known[35]}")


if __name__ == "__main__":
    main()
