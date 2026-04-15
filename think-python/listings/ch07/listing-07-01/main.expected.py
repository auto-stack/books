def has_e(word):
    for letter in word:
        if letter == "E" or letter == "e":
            return True
    return False


def main():
    # Looping over characters in a string
    print("Letters in Gadsby:")
    for letter in "Gadsby":
        print(letter, end=" ")
    print()

    # Checking for 'e' in a word
    print(f"has_e('Gadsby'): {has_e('Gadsby')}")
    print(f"has_e('Emma'): {has_e('Emma')}")
    print(f"has_e('hello'): {has_e('hello')}")
    print(f"has_e('world'): {has_e('world')}")


if __name__ == "__main__":
    main()
