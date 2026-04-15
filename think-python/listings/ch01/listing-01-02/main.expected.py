def main():
    # Strings with single and double quotes
    print("Hello")
    print("world")

    # String with apostrophe using double quotes
    print("it's a small world.")

    # String concatenation with +
    print("Well, " + "it's a small " + "world.")

    # String repetition with *
    print("Spam, " * 4)

    # String length
    print(len("Spam"))

    # f-string with {var} interpolation
    name = "Alice"
    age = 30
    print(f"My name is {name} and I am {age} years old.")


if __name__ == "__main__":
    main()
