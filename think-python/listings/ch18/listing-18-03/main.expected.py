class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __gt__(self, other):
        if self.year != other.year:
            return self.year > other.year
        if self.month != other.month:
            return self.month > other.month
        return self.day > other.day


def main():
    p = Point(3.0, 4.0)
    print(p.x)
    print(p.y)

    p2 = Point(1.0, 2.0)
    p3 = Point(3.0, 4.0)
    print(p == p3)
    print(p == p2)

    a, b = p.x, p.y
    print(f"Unpacked: a={a}, b={b}")

    distance = (p.x ** 2 + p.y ** 2) ** 0.5
    print(f"Distance from origin: {distance}")

    grid = {}
    grid[(1.0, 2.0)] = "A"
    grid[(3.0, 4.0)] = "B"
    print(grid)

    birthday = Date(2000, 1, 15)
    print(f"Year: {birthday.year}, Month: {birthday.month}, Day: {birthday.day}")

    today = Date(2025, 4, 15)
    print(today > birthday)


if __name__ == "__main__":
    main()
