import os


def walk(dirname):
    names = os.listdir(dirname)
    for name in names:
        path = os.path.join(dirname, name)
        if os.path.isfile(path):
            print(path)
        elif os.path.isdir(path):
            walk(path)


def main():
    # Build a word list by reading text files from a directory
    os.makedirs("demo_texts", exist_ok=True)

    # Create sample text files
    f1 = open("demo_texts/story1.txt", "w")
    f1.write("The quick brown fox jumps over the lazy dog\n")
    f1.write("The fox was very quick indeed\n")
    f1.close()

    f2 = open("demo_texts/story2.txt", "w")
    f2.write("A lazy dog slept in the sun all day\n")
    f2.write("The sun was bright and warm\n")
    f2.close()

    f3 = open("demo_texts/story3.txt", "w")
    f3.write("Quick thinking helps in many situations\n")
    f3.write("The dog chased the fox through the field\n")
    f3.close()

    # Collect unique words from all .txt files
    word_set = {}
    total_words = 0
    file_count = 0

    names = os.listdir("demo_texts")
    for name in names:
        path = os.path.join("demo_texts", name)
        if os.path.isfile(path) and path.endswith(".txt"):
            file_count += 1
            content = open(path).read()
            words = content.split()
            for word in words:
                # Clean the word: strip punctuation, lowercase
                cleaned = word.strip(",.!?").lower()
                if cleaned != "":
                    word_set[cleaned] = 1
                    total_words += 1

    print(f"Files read: {file_count}")
    print(f"Total word tokens: {total_words}")
    print(f"Unique words: {len(word_set)}")

    # Show sorted unique words
    sorted_words = sorted(word_set.keys())
    print()
    print("Unique words (sorted):")
    print(sorted_words)

    # Write word list to a file using f-string formatting
    writer = open("demo_texts/word_list.txt", "w")
    writer.write(f"Total unique words: {len(word_set)}\n")
    writer.write(f"Total word tokens: {total_words}\n")
    writer.write(f"Files processed: {file_count}\n")
    writer.write("\nWords:\n")
    for word in sorted_words:
        writer.write(f"{word}\n")
    writer.close()
    print()
    print("Word list written to demo_texts/word_list.txt")


if __name__ == "__main__":
    main()
