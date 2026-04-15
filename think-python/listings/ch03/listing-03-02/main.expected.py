def print_twice(string):
    print(string)
    print(string)


def repeat(word, n):
    result = word * n
    print(result)


def main():
    # Call with a literal argument
    print_twice("Dennis Moore, ")

    # Call with a variable argument
    line = "Dennis Moore, "
    print_twice(line)

    # Call a function with two parameters
    spam = "Spam, "
    repeat(spam, 4)


if __name__ == "__main__":
    main()
