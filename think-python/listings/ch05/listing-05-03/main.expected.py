def classify_number(x):
    if x > 0:
        print(f"{x} is positive")
    elif x < 0:
        print(f"{x} is negative")
    else:
        print(f"{x} is zero")


def classify_even_odd(x):
    if x % 2 == 0:
        print(f"{x} is even")
    else:
        print(f"{x} is odd")


def classify_temperature(temp):
    if temp >= 30:
        print(f"{temp} C is hot")
    elif temp >= 20:
        print(f"{temp} C is warm")
    elif temp >= 10:
        print(f"{temp} C is cool")
    else:
        print(f"{temp} C is cold")


def compare(x, y):
    if x < y:
        print(f"{x} is less than {y}")
    elif x > y:
        print(f"{x} is greater than {y}")
    else:
        print(f"{x} and {y} are equal")


def main():
    # if / else
    print("=== Positive / Negative / Zero ===")
    classify_number(5)
    classify_number(-3)
    classify_number(0)
    print()

    # if / else (even/odd)
    print("=== Even / Odd ===")
    classify_even_odd(4)
    classify_even_odd(7)
    print()

    # Chained conditionals (elif)
    print("=== Temperature ===")
    classify_temperature(35)
    classify_temperature(25)
    classify_temperature(15)
    classify_temperature(5)
    print()

    # Chained conditional (three-way comparison)
    print("=== Comparison ===")
    compare(3, 5)
    compare(7, 2)
    compare(4, 4)


if __name__ == "__main__":
    main()
