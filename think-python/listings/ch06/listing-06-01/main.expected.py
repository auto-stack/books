import math

def circle_area(radius):
    area = math.pi * radius ** 2
    return area


def repeat_string(word, n):
    return word * n


def main():
    # Return value from circle_area
    radius = 3.66
    a = circle_area(radius)
    print(f"Area of circle with radius {radius}: {a}")

    # Using return value in an expression
    total = circle_area(radius) + 2.0 * circle_area(radius / 2.0)
    print(f"Combined area: {total}")

    # Pure function: repeat_string returns a value
    line = repeat_string("Spam, ", 4)
    print(line)

    # Function without return statement returns nothing
    print(repeat_string("Finland, ", 3))


if __name__ == "__main__":
    main()
