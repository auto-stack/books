def main():
    # Creating an empty dictionary
    numbers = {}
    numbers["zero"] = 0
    numbers["one"] = 1
    numbers["two"] = 2
    print(f"numbers: {numbers}")

    # Creating a dictionary all at once
    scores = {"Alice": 95, "Bob": 87, "Charlie": 92}
    print(f"scores: {scores}")

    # Accessing values
    print(f"Alice's score: {scores['Alice']}")
    print(f"Length of scores: {len(scores)}")

    # Checking if a key exists
    print(f"Contains 'Alice': {'Alice' in scores}")
    print(f"Contains 'David': {'David' in scores}")

    # Using get with a default value
    print(f"Eve's score: {scores.get('Eve', 0)}")
    print(f"Bob's score: {scores.get('Bob', 0)}")


if __name__ == "__main__":
    main()
