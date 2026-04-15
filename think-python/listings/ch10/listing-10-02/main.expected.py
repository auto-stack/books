def value_counts(string):
    counter = {}
    for letter in string:
        if letter not in counter:
            counter[letter] = 1
        else:
            counter[letter] += 1
    return counter


def main():
    # Counting letters in a word
    counter = value_counts("brontosaurus")
    print(f"Letter counts: {counter}")
    print(f"Number of unique letters: {len(counter)}")

    # Looping through keys
    print("Keys:")
    for key in counter:
        print(key, end=" ")
    print()

    # Looping through values
    print("Values:")
    for value in counter.values():
        print(value, end=" ")
    print()

    # Looping through keys and values
    print("Key-value pairs:")
    for key in counter:
        value = counter[key]
        print(f"{key}: {value}")

    # Building a dictionary from a list
    words = ["apple", "banana", "cherry", "date", "elderberry"]
    word_lengths = {}
    for word in words:
        word_lengths[word] = len(word)
    print(f"Word lengths: {word_lengths}")


if __name__ == "__main__":
    main()
