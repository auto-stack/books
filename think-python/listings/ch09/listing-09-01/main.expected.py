def main():
    # Creating lists
    numbers = [42, 123]
    cheeses = ["Cheddar", "Edam", "Gouda"]
    mixed = ["spam", 2.0, 5, [10, 20]]
    empty = []

    # Accessing elements by index
    print(f"cheeses[0]: {cheeses[0]}")
    print(f"cheeses[1]: {cheeses[1]}")
    print(f"cheeses[2]: {cheeses[2]}")
    print(f"cheeses[-1]: {cheeses[-1]}")

    # Length
    print(f"len(cheeses): {len(cheeses)}")
    print(f"len(numbers): {len(numbers)}")
    print(f"len(empty): {len(empty)}")

    # The 'in' operator
    print(f"Edam in cheeses: {'Edam' in cheeses}")
    print(f"Wensleydale in cheeses: {'Wensleydale' in cheeses}")

    # Nested list: counts as one element
    print(f"len(mixed): {len(mixed)}")
    print(f"10 in mixed: {10 in mixed}")

    # Accessing nested element
    print(f"mixed[3]: {mixed[3]}")
    print(f"mixed[3][0]: {mixed[3][0]}")


if __name__ == "__main__":
    main()
