def uses_any(word, letters):
    for letter in word.lower():
        if letter in letters.lower():
            return True
    return False


def find(word, letter):
    index = 0
    for ch in word:
        if ch == letter:
            return index
        index += 1
    return -1


def main():
    # Testing uses_any (linear search)
    print(f"uses_any('banana', 'aeiou'): {uses_any('banana', 'aeiou')}")
    print(f"uses_any('apple', 'xyz'): {uses_any('apple', 'xyz')}")
    print(f"uses_any('Banana', 'AEIOU'): {uses_any('Banana', 'AEIOU')}")

    # Testing find (search for first occurrence)
    print(f"find('hello', 'l'): {find('hello', 'l')}")
    print(f"find('hello', 'o'): {find('hello', 'o')}")
    print(f"find('hello', 'z'): {find('hello', 'z')}")


if __name__ == "__main__":
    main()
