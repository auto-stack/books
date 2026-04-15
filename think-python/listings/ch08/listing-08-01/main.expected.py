def main():
    fruit = "banana"

    # Indexing: accessing individual characters
    print(f"fruit[0]: {fruit[0]}")
    print(f"fruit[1]: {fruit[1]}")
    print(f"fruit[-1]: {fruit[-1]}")
    print(f"fruit[-2]: {fruit[-2]}")

    # Slicing: accessing substrings
    print(f"fruit[0:3]: {fruit[0:3]}")
    print(f"fruit[2:5]: {fruit[2:5]}")
    print(f"fruit[:3]: {fruit[:3]}")
    print(f"fruit[3:]: {fruit[3:]}")
    print(f"fruit[:]: {fruit[:]}")

    # Empty slice
    print(f"fruit[3:3]: {fruit[3:3]}")

    # Length
    print(f"len(fruit): {len(fruit)}")


if __name__ == "__main__":
    main()
