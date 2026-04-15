def main():
    # for loop with range
    print("Counting from 0 to 4:")
    for i in range(5):
        print(i, end=" ")
    print()

    # for loop with step range
    print("Even numbers from 0 to 10:")
    for i in range(11):
        if i % 2 == 0:
            print(i, end=" ")
    print()

    # for loop over string
    print("Letters in Auto:")
    for letter in "Auto":
        print(letter, end=" ")
    print()

    # Accumulator pattern: sum from 1 to 10
    total = 0
    for i in range(1, 11):
        total += i
    print(f"Sum from 1 to 10: {total}")


if __name__ == "__main__":
    main()
