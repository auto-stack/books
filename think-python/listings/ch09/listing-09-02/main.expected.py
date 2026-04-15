def main():
    # append: add one element
    letters = ["a", "b", "c"]
    letters.append("d")
    print(f"After append: {letters}")

    # extend: add multiple elements
    letters.extend(["e", "f"])
    print(f"After extend: {letters}")

    # pop: remove by index
    t = ["a", "b", "c"]
    removed = t.pop(1)
    print(f"Popped: {removed}")
    print(f"After pop: {t}")

    # remove: remove by value
    t2 = ["a", "b", "c"]
    t2.remove("b")
    print(f"After remove: {t2}")

    # sort: sort in place (ascending)
    nums = [3, 1, 4, 1, 5, 9]
    nums.sort()
    print(f"Sorted: {nums}")

    # sorted: returns a new sorted list (original unchanged)
    scramble = ["c", "a", "b"]
    sorted_list = sorted(scramble)
    print(f"Original: {scramble}")
    print(f"Sorted copy: {sorted_list}")

    # reverse
    items = [1, 2, 3]
    items.reverse()
    print(f"Reversed: {items}")

    # index: find position of element
    fruits = ["apple", "banana", "cherry"]
    print(f"index of banana: {fruits.index('banana')}")

    # count: count occurrences
    data = [1, 2, 2, 3, 2]
    print(f"count of 2: {data.count(2)}")


if __name__ == "__main__":
    main()
