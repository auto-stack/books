def pop_first(lst):
    return lst.pop(0)


def append_item(lst, item):
    lst.append(item)


def main():
    # Aliasing: two names, one object
    a = [1, 2, 3]
    b = a
    print(f"b is a: {b is a}")
    print(f"Before change - a: {a}")

    # Modifying through b affects a
    b[0] = 5
    print(f"After b[0] = 5 - a: {a}")

    # Lists are not identical even if equivalent
    c = [1, 2, 3]
    d = [1, 2, 3]
    print(f"c == d: {c == d}")
    print(f"c is d: {c is d}")

    # Strings: aliasing is safe (immutable)
    s1 = "banana"
    s2 = s1
    print(f"s1 is s2: {s1 is s2}")

    # List arguments: caller sees changes
    letters = ["a", "b", "c"]
    print(f"\nBefore pop_first: {letters}")
    first = pop_first(letters)
    print(f"Popped: {first}")
    print(f"After pop_first: {letters}")

    items = ["x", "y"]
    print(f"\nBefore append_item: {items}")
    append_item(items, "z")
    print(f"After append_item: {items}")

    # Copying a list to avoid aliasing
    original = [10, 20, 30]
    copy = original[:]
    copy[0] = 99
    print(f"\noriginal after copy modified: {original}")
    print(f"copy: {copy}")


if __name__ == "__main__":
    main()
