def main():
    # List comprehension equivalent: Auto uses for loops
    squares = []
    for i in range(10):
        squares.append(i * i)
    print(squares)

    # Filtering with a for loop
    even_squares = []
    for i in range(10):
        if i % 2 == 0:
            even_squares.append(i * i)
    print(even_squares)

    # Counter pattern: counting word frequencies
    words = ["the", "cat", "in", "the", "hat", "in", "the"]
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    print(counts)

    # Finding the most common
    max_word = ""
    max_count = 0
    for word, count in counts.items():
        if count > max_count:
            max_word = word
            max_count = count
    print(f"Most common: '{max_word}' appears {max_count} times")

    # Grouping with a dictionary (defaultdict pattern)
    letters = "abracadabra"
    positions = {}
    for i, letter in enumerate(letters):
        if letter not in positions:
            positions[letter] = []
        positions[letter].append(i)
    print(positions)


if __name__ == "__main__":
    main()
