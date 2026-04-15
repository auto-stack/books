def repeat(word, n):
    print(word * n)


def first_two_lines():
    repeat("Spam, ", 4)
    repeat("Spam, ", 4)


def last_three_lines():
    repeat("Spam, ", 2)
    print("(Lovely Spam, Wonderful Spam!)")
    repeat("Spam, ", 2)


def print_verse():
    first_two_lines()
    last_three_lines()


def main():
    # Simple for loop
    print("Counting:")
    for i in range(3):
        print(i)

    # Using a for loop to repeat verses
    print("Two verses:")
    for i in range(2):
        print("Verse", i)
        print_verse()


if __name__ == "__main__":
    main()
