def split_line(line):
    return line.replace("\u2014", " ").split()


def clean_word(word, punctuation):
    return word.strip(punctuation).lower()


def second_element(t):
    return t[1]


def subtract(d1, d2):
    res = {}
    for key in d1:
        if key not in d2:
            res[key] = d1[key]
    return res


def print_most_common(word_counter, num=5):
    items = sorted(word_counter.items(), key=second_element, reverse=True)
    for i in range(num):
        word, freq = items[i]
        print(f"{freq}\t{word}")


def main():
    lines = [
        "The strange case of Dr. Jekyll and Mr. Hyde",
        "was a curious affair\u2014indeed, it was most remarkable!",
        "The doctor was not truly one, but two.",
        "Mr. Utterson was the lawyer, a friend of Dr. Jekyll.",
        "The strange door\u2014what secrets did it hide?",
        "Dr. Jekyll was a well-known man in the city.",
        "Mr. Hyde was a strange and violent man.",
        "The lawyer Utterson was worried about his friend Dr. Jekyll."
    ]

    # Build punctuation set
    punc_marks = {}
    for line in lines:
        for char in line:
            if not char.isalnum() and char != " ":
                punc_marks[char] = 1
    punctuation = "".join(punc_marks.keys())

    # Build word frequency counter
    word_counter = {}
    for line in lines:
        for word in split_line(line):
            cleaned = clean_word(word, punctuation)
            if cleaned == "":
                continue
            if cleaned not in word_counter:
                word_counter[cleaned] = 1
            else:
                word_counter[cleaned] += 1

    # A small valid word list for demonstration
    valid_word_list = [
        "the", "a", "was", "and", "of", "not", "but", "it",
        "strange", "case", "door", "man", "city", "two",
        "friend", "worried", "violent", "his", "about"
    ]
    valid_words = {}
    for word in valid_word_list:
        valid_words[word] = 1

    # Dictionary subtraction: find words in text not in valid list
    diff = subtract(word_counter, valid_words)

    print("Words possibly misspelled (most common):")
    print_most_common(diff, 8)

    # Find singletons (words that appear only once)
    singletons = []
    for word, freq in diff.items():
        if freq == 1:
            singletons.append(word)
    print()
    print(f"Singletons: {len(singletons)} words")
    print(f"Sample: {singletons[-5:]}")


if __name__ == "__main__":
    main()
