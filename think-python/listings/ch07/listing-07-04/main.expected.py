def count_letter(word, target):
    count = 0
    for letter in word:
        if letter == target:
            count += 1
    return count


def main():
    # Counting with accumulator pattern
    print(f"Counting 'l' in 'hello': {count_letter('hello', 'l')}")
    print(f"Counting 'e' in 'Emma': {count_letter('Emma', 'e')}")
    print(f"Counting 'a' in 'banana': {count_letter('banana', 'a')}")
    print(f"Counting 'z' in 'hello': {count_letter('hello', 'z')}")

    # Counting words with 'e' from a list
    words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]
    total = 0
    count_e = 0
    for word in words:
        total += 1
        if count_letter(word, "e") > 0:
            count_e += 1
    print(f"Total words: {total}")
    print(f"Words with 'e': {count_e}")
    print(f"Percentage with 'e': {count_e * 100 // total}")


if __name__ == "__main__":
    main()
