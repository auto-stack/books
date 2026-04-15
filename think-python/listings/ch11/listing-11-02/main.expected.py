def min_max(t):
    return (min(t), max(t))


def swap(a, b):
    return (b, a)


def main():
    # Tuple assignment
    x, y = 10, 20
    print(f"x: {x} y: {y}")

    # Splitting a string with tuple assignment
    email = "monty@python.org"
    username, domain = email.split("@")
    print(f"Username: {username}")
    print(f"Domain: {domain}")

    # Swapping variables
    a, b = 3, 7
    print(f"Before swap: a = {a} b = {b}")
    a, b = swap(a, b)
    print(f"After swap:  a = {a} b = {b}")

    # divmod -- returning a tuple
    quotient, remainder = divmod(17, 5)
    print(f"17 / 5 = {quotient} remainder {remainder}")

    # Function returning a tuple
    numbers = (4, 1, 7, 2, 9, 3)
    low, high = min_max(numbers)
    print(f"Numbers: {numbers}")
    print(f"Min: {low} Max: {high}")

    # Iterating dictionary items with tuple assignment
    scores = {"Alice": 95, "Bob": 87, "Charlie": 92}
    print("Scores:")
    for name, score in scores.items():
        print(f"  {name}: {score}")


if __name__ == "__main__":
    main()
