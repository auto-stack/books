def main():
    # Single and double quotes
    name = "Swaroop"
    greeting = "Hello"

    # Multiline string
    story = """This is a multi-line string.
This is the second line.
"What's your name?" I asked.
He said "Bond, James Bond."
"""

    # f-string with {var} interpolation
    age = 20
    print(f"{name} was {age} years old when he wrote this book")
    print(f"Why is {name} playing with that python?")

    # String concatenation
    print(name + " is " + "awesome")

    print(story)


if __name__ == "__main__":
    main()
