def main():
    word = "banana"

    # Case conversion
    print(f"upper: {word.upper()}")
    print(f"lower: {'BANANA'.lower()}")

    # Searching
    print(f"find 'a': {word.find('a')}")
    print(f"find 'z': {word.find('z')}")
    print(f"contains 'ana': {'ana' in word}")
    print(f"starts with 'ban': {word.startswith('ban')}")
    print(f"ends with 'na': {word.endswith('na')}")

    # Stripping whitespace
    spaced = "  hello world  "
    print(f"strip: {spaced.strip()}")
    print(f"len before: {len(spaced)}")
    print(f"len after: {len(spaced.strip())}")

    # Counting occurrences
    print(f"count 'a': {word.count('a')}")

    # Replacement
    text = "I like cats and cats like me"
    print(f"replace: {text.replace('cats', 'dogs')}")

    # Splitting
    sentence = "pining for the fjords"
    words = sentence.split(" ")
    print(f"split: {words}")

    # Joining
    parts = ["hello", "world"]
    print(f"join: {' '.join(parts)}")


if __name__ == "__main__":
    main()
