def value_counts(string):
    counter = {}
    for letter in string:
        if letter not in counter:
            counter[letter] = 1
        else:
            counter[letter] += 1
    return counter


def invert_dict(d):
    new = {}
    for key, value in d.items():
        if value not in new:
            new[value] = [key]
        else:
            new[value].append(key)
    return new


def main():
    # Zip: pairing elements from two sequences
    names = ["Alice", "Bob", "Charlie", "Diana"]
    scores = [95, 87, 92, 88]
    print("Zipped pairs:")
    for name, score in zip(names, scores):
        print(f"  {name}: {score}")

    # Building a dictionary from two lists with zip
    letters = "abcde"
    values = [10, 20, 30, 40, 50]
    letter_values = dict(zip(letters, values))
    print(f"Letter values: {letter_values}")

    # Enumerate: pairing elements with their indices
    print("Enumerated:")
    for index, letter in enumerate("hello"):
        print(f"  {index}: {letter}")

    # Dictionary inversion
    d = value_counts("parrot")
    print(f"Original: {d}")
    inverted = invert_dict(d)
    print(f"Inverted: {inverted}")

    # Comparing tuples
    print((0, 1, 2) < (0, 3, 4))
    print((0, 1, 2000000) < (0, 3, 4))


if __name__ == "__main__":
    main()
