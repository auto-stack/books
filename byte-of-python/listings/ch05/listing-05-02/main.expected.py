def main():
    # Calculate rectangle area and perimeter
    length = 5
    breadth = 2

    area = length * breadth
    print(f"Area is {area}")

    perimeter = 2 * (length + breadth)
    print(f"Perimeter is {perimeter}")

    # Calculate circle area
    radius = 5.0
    pi = 3.14159
    circle_area = pi * radius ** 2
    print(f"Circle area is {circle_area}")

    # Using compound assignment
    total = 10
    total += 5
    print(total)
    total -= 3
    print(total)
    total *= 2
    print(total)


if __name__ == "__main__":
    main()
