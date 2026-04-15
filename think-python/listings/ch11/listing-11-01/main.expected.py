def main():
    # Creating tuples
    t = ('l', 'u', 'p', 'i', 'n')
    print(f"Tuple: {t}")

    # Tuple from a string
    t2 = tuple("hello")
    print(f"Tuple from string: {t2}")

    # Single-element tuple
    single = ('p',)
    print(f"Single element: {single}")

    # Indexing
    print(f"First element: {t[0]}")
    print(f"Last element: {t[-1]}")

    # Slicing
    print(f"Slice [1:3]: {t[1:3]}")

    # Concatenation
    combined = tuple("lup") + ('i', 'n')
    print(f"Concatenated: {combined}")

    # Length
    print(f"Length: {len(t)}")

    # Sorted (returns a list)
    print(f"Sorted: {sorted(t)}")

    # Tuple as dictionary key
    d = {}
    d[(1, 2)] = 3
    d[(3, 4)] = 7
    print(f"Dict with tuple keys: {d}")
    print(f"d[(1, 2)]: {d[(1, 2)]}")


if __name__ == "__main__":
    main()
