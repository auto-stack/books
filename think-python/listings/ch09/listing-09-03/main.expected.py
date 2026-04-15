def main():
    # Looping through a list
    cheeses = ["Cheddar", "Edam", "Gouda"]
    print("Cheeses:")
    for cheese in cheeses:
        print(f" {cheese}")

    # Looping through words from a string
    sentence = "pining for the fjords"
    print("\nWords:")
    for word in sentence.split(" "):
        print(f" {word}")

    # List concatenation
    t1 = [1, 2]
    t2 = [3, 4]
    print(f"\nConcat: {t1 + t2}")

    # List repetition
    print(f"Repeat: {['spam'] * 3}")

    # Sum, min, max
    print(f"Sum: {sum([1, 2, 3, 4])}")
    print(f"Min: {min([5, 2, 8, 1])}")
    print(f"Max: {max([5, 2, 8, 1])}")

    # String <-> List conversions
    s = "hello"
    chars = list(s)
    print(f"list('hello'): {chars}")
    print(f"join: {'-'.join(chars)}")

    # Sorted string letters
    sorted_str = "".join(sorted("letters"))
    print(f"Sorted letters: {sorted_str}")

    # Looping with index using enumerate
    fruits = ["apple", "banana", "cherry"]
    print("\nWith index:")
    for i, fruit in enumerate(fruits):
        print(f"  {i}: {fruit}")


if __name__ == "__main__":
    main()
