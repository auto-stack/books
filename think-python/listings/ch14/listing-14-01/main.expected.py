class Point:
    pass


def print_point(p):
    print(f"({p.x}, {p.y})")


def main():
    # Creating a Point type and instantiating
    lunch = Point()
    print(type(lunch))  # <class '__main__.Point'>

    # Assigning attributes
    lunch.x = 11.0
    lunch.y = 59.0
    print_point(lunch)  # (11.0, 59.0)

    # Reading attributes
    print(lunch.x)  # 11.0

    # Using attributes in expressions
    total_minutes = lunch.x * 60.0 + lunch.y
    print(f"Total minutes: {total_minutes}")  # 719.0

    # Creating another Point
    p = Point()
    p.x = 3.0
    p.y = 4.0
    print_point(p)  # (3.0, 4.0)

    # Distance from origin
    distance = (p.x ** 2 + p.y ** 2) ** 0.5
    print(f"Distance: {distance}")  # 5.0


if __name__ == "__main__":
    main()
