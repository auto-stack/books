def countdown(n):
    if n <= 0:
        print("Blastoff!")
    else:
        print(n)
        countdown(n - 1)


def print_n(string, n):
    if n > 0:
        print(string)
        print_n(string, n - 1)


def main():
    # Countdown from 3
    print("Countdown from 3:")
    countdown(3)
    print()

    # Countdown from 1
    print("Countdown from 1:")
    countdown(1)
    print()

    # Print a string n times
    print("Print 'Spam' 4 times:")
    print_n("Spam", 4)
    print()

    # Print with n = 0 (base case, prints nothing)
    print("Print 'Hello' 0 times:")
    print_n("Hello", 0)


if __name__ == "__main__":
    main()
