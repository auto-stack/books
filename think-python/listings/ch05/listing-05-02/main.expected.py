def main():
    # Boolean expressions
    x = 5
    y = 7

    print(f"x = {x}, y = {y}")
    print(f"x == y: {x == y}")
    print(f"x != y: {x != y}")
    print(f"x > y: {x > y}")
    print(f"x < y: {x < y}")
    print(f"x >= y: {x >= y}")
    print(f"x <= y: {x <= y}")
    print()

    # Logical operators
    print(f"x > 0 and x < 10: {x > 0 and x < 10}")
    print(f"x % 2 == 0 or x % 3 == 0: {x % 2 == 0 or x % 3 == 0}")
    print(f"not (x > y): {not (x > y)}")
    print()

    # Combining conditions
    age = 25
    has_ticket = True
    print(f"age = {age}, has_ticket = {has_ticket}")
    print(f"Can enter: {age >= 18 and has_ticket}")

    # Negation
    is_raining = False
    print(f"is_raining = {is_raining}")
    print(f"Should go outside: {not is_raining}")


if __name__ == "__main__":
    main()
