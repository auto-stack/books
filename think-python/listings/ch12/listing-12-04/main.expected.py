import random


def split_line(line):
    return line.replace("\u2014", " ").split()


def clean_word(word, punctuation):
    return word.strip(punctuation).lower()


def add_bigram(successor_map, bigram):
    first = bigram[0]
    second = bigram[1]

    if first not in successor_map:
        successor_map[first] = [second]
    else:
        successor_map[first].append(second)


def main():
    song = [
        "Half", "a", "bee", "philosophically,",
        "Must", "ipso", "facto,", "half", "not", "be.",
        "But", "half", "the", "bee", "has", "got", "to", "be",
        "Vis", "a", "vis,", "its", "entity.", "D'you", "see?"
    ]

    punctuation = {}
    punc_chars = ",.'"
    for c in punc_chars:
        punctuation[c] = 1
    punc = "".join(punctuation.keys())

    # Build successor map from the song
    successor_map = {}
    window = []

    for string in song:
        word = clean_word(string, punc)
        if word == "":
            continue
        window.append(word)

        if len(window) == 2:
            add_bigram(successor_map, window)
            window.pop(0)

    print("Successor map from song:")
    for key, value in successor_map.items():
        print(f"  '{key}' -> {value}")

    # Markov text generation
    random.seed(42)
    start_word = "half"
    print()
    print(f"Starting word: '{start_word}'")
    print("Generated text:")

    word = start_word
    result = [start_word]

    for i in range(16):
        if word not in successor_map:
            break
        successors = successor_map[word]
        word = random.choice(successors)
        result.append(word)

    print(" ".join(result))


if __name__ == "__main__":
    main()
