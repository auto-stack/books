def split_line(line):
    return line.replace("\u2014", " ").split()


def clean_word(word, punctuation):
    return word.strip(punctuation).lower()


def main():
    # Simulated text from Dr. Jekyll and Mr. Hyde
    text = "The strange case of Dr. Jekyll and Mr. Hyde was a curious affair."
    filename = "dr_jekyll.txt"

    # For this demo, create a sample text directly
    lines = [
        "The strange case of Dr. Jekyll and Mr. Hyde",
        "was a curious affair\u2014indeed, it was most remarkable!",
        "The doctor was not truly one, but two.",
        "Mr. Utterson was the lawyer, a friend of Dr. Jekyll.",
        "The strange door\u2014what secrets did it hide?"
    ]

    # Count unique words (simple version without punctuation cleaning)
    unique_words = {}
    for line in lines:
        seq = line.split()
        for word in seq:
            unique_words[word] = 1
    print(f"Unique words (simple): {len(unique_words)}")

    # Find longest words
    sorted_words = sorted(unique_words.keys(), key=len)
    print(f"Longest words: {sorted_words[-3:]}")

    # Count unique words (cleaned version)
    # Build punctuation set from the text
    punc_marks = {}
    for line in lines:
        for char in line:
            # Simple punctuation detection: check if char is not alphanumeric and not space
            if not char.isalnum() and char != " ":
                punc_marks[char] = 1
    punctuation = "".join(punc_marks.keys())
    print(f"Punctuation marks: {punctuation}")

    # Count cleaned unique words
    unique_words2 = {}
    for line in lines:
        for word in split_line(line):
            cleaned = clean_word(word, punctuation)
            unique_words2[cleaned] = 1
    print(f"Unique words (cleaned): {len(unique_words2)}")

    # Show longest cleaned words
    sorted2 = sorted(unique_words2.keys(), key=len)
    print(f"Longest cleaned words: {sorted2[-3:]}")


if __name__ == "__main__":
    main()
