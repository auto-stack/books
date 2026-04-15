def main():
    # Built-in arithmetic functions
    print(round(42.4))
    print(round(42.6))

    # Absolute value
    print(abs(42))
    print(abs(-42))

    # Values and types
    # type(2)        -> int
    # type(42.0)     -> float
    # type("Hello")  -> str

    # Type conversion
    print(int(42.9))      # float to int (rounds down)
    print(float(42))      # int to float

    # String that looks like a number
    print(int("126"))     # string to int
    print(float("12.6"))  # string to float

    # Using converted values in arithmetic
    print(int("126") / 3)

    # Large numbers with underscores
    print(1_000_000)


if __name__ == "__main__":
    main()
